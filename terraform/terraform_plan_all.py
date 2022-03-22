#    Copyright 2021 Hunter Grubbs < hunter DOT grubbs AT protonmail DOT com >
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import os
from pathlib import Path
import json
import logging
import hashlib
import random
import pdb
import shutil
import argparse
import multiprocessing as mp
import datetime
import time
from slack_sdk import WebClient
import re

SLACK_CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID', None)
SLACK_OAUTH_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN', None)

working_directory = os.getcwd()


def discover_chunks():
    """Returns an array of all terraform chunks beneath working directory"""
    all_paths = [a_path for a_path in os.walk(os.curdir)]
    chunks = []

    for item in all_paths:
        current_path = item[0]
        current_files = item[2]

        if current_path.find('/modules/') > -1:  # this is a module, not a chunk, skip it
            continue

        if len(current_files) == 0:  # no files in this path? not a chunk, let's continue
            continue
        elif len(current_files) > 0:  # this path contains files
            for a_file in current_files:
                if a_file.endswith('.tf'):  # do we contain any .tf files?
                    chunks.append(current_path)  # add this path to the list of chunks

    return set(chunks)  # return the unique values in 'chunks' array


def ext_command(cmd):
    """Runs external command. Returns a dict: {'stdout': '...', 'stderr': '...', 'returncode': <int>}"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return {'stdout': stdout.decode(), 'stderr': stderr.decode(), 'returncode': p.returncode}


def random_scan_id():
    """Returns 4-character random IDs"""
    m = hashlib.sha256()
    random_string = str(random.random()).encode()
    m.update(random_string)
    return m.hexdigest()[0:4]


def slack_post_message(msg):
    """Sends message to slack, returns thread_ts"""
    logger = logging.getLogger('slack_post_message')

    # if token or channel id is unset, abort
    if SLACK_OAUTH_TOKEN is None or SLACK_CHANNEL_ID is None:
        logger.debug("SLACK_OAUTH_TOKEN or SLACK_CHANNEL_ID unset, not sending msg")
        return None

    client = WebClient(token=SLACK_OAUTH_TOKEN)
    response = client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=msg)
    return response.data['ts']


def slack_post_thread_file(thread_ts, file_contents):
    """Posts file to slack conversation identified by thread_ts. Does not return a value."""
    logger = logging.getLogger('slack_post_thread_file')
    logger.debug("posting to thread_ts %s", thread_ts)

    # if token or channel id is unset, abort
    if SLACK_OAUTH_TOKEN is None or SLACK_CHANNEL_ID is None:
        logger.debug("SLACK_OAUTH_TOKEN or SLACK_CHANNEL_ID unset, not sending msg")
        return None

    client = WebClient(token=SLACK_OAUTH_TOKEN)
    client.files_upload(channels=SLACK_CHANNEL_ID, title="terraform plan", content=file_contents, thread_ts=thread_ts)


def tf_chunk_process(chunk, working_directory, scan_id, args):
    """
    Initializes and plans a chunk. Failures are reported to slack.

    returns:
    {
        "chunk": chunk,
        "init": init,
        "init_details": init_details,
        "plan": plan,
        "plan_details": plan_details,
        "chunk_started": chunk_started,
        "chunk_finished": chunk_finished
    }

    """
    chunk_started = datetime.datetime.now()
    logger = logging.getLogger('tf_chunk_process')
    logger.debug("processing %s", chunk)

    # set all of these, so we can return them
    init = None
    init_details = None
    plan = None
    plan_details = None

    (init, init_details) = tf_chunk_init(chunk, working_directory, args)
    if init is False:
        slack_post_message(f"{scan_id}: init failed on chunk: {chunk}")
    elif init is True:
        (plan, plan_details) = tf_chunk_plan(chunk, working_directory, args)
        if plan is False:
            thread_ts = slack_post_message(f"{scan_id}: plan failed on chunk: {chunk}")
            logging.debug("chunk %s thead_ts = %s", chunk, thread_ts)

            # take stdout, and remove everything above "Terraform Detected", and below "Note: You didn't use"
            tf_plan_output = plan_details['stdout']
            tf_plan_output = re.sub(r'.*Terraform detected', 'Terraform detected', tf_plan_output, flags=re.DOTALL)
            tf_plan_output = re.sub(r"Note: You didn't.*", '', tf_plan_output, flags=re.DOTALL)
            slack_post_thread_file(thread_ts, tf_plan_output)

    chunk_finished = datetime.datetime.now()
    return {
        "chunk": chunk,
        "init": init,
        "init_details": init_details,
        "plan": plan,
        "plan_details": plan_details,
        "chunk_started": chunk_started,
        "chunk_finished": chunk_finished
    }


def tf_chunk_init(chunk, working_directory, args):
    """
    Initializes a terraform chunk. Returns (True, None) or (False, dict).

    In the event of failure, `dict` will be a dictionary containing stdout/stderr/returncode.
    """

    logger = logging.getLogger('tf_chunk_init')

    logger.debug("changing directory: %s", working_directory)
    os.chdir(working_directory)

    logger.debug("changing directory: %s", chunk)
    os.chdir(chunk)

    logger.debug("removing .terraform")
    try:
        shutil.rmtree('.terraform')
    except FileNotFoundError:
        pass

    logger.debug("initializing chunk: %s", chunk)
    init_result = ext_command('terraform init -no-color')
    if init_result['returncode'] != 0:
        logger.error("terraform init FAILED: %s: %s", chunk, init_result)
        os.chdir(working_directory)
        return (False, init_result)
    elif init_result['returncode'] == 0:
        logger.debug("chunk INITIALIZED: %s", chunk)
        os.chdir(working_directory)
        return (True, None)


def tf_chunk_plan(chunk, working_directory, args):
    """
    Plans a terraform chunk. Returns (True, None) or (False, dict).

    In the event of failure, `dict` will be a dictionary containing stdout/stderr/returncode.
    """

    logger = logging.getLogger('tf_chunk_plan')

    #logger.debug("changing directory: %s", working_directory)
    os.chdir(working_directory)

    #logger.debug("changing directory: %s", chunk)
    os.chdir(chunk)

    logger.debug("planning chunk: %s", chunk)
    plan_result = ext_command("terraform plan -lock=false -no-color -detailed-exitcode -parallelism={}".format(args.tf_parallelism))
    if plan_result['returncode'] != 0:
        logger.info("terraform plan FAILED: %s", chunk)
        logger.debug("failed plan for %s: %s", chunk, plan_result)
        os.chdir(working_directory)
        return (False, plan_result)
    elif plan_result['returncode'] == 0:
        logger.debug("chunk planned CLEAN: %s", chunk)
        os.chdir(working_directory)
        return (True, None)


def return_skipped_chunks(chunks):
    """
    Consumes an array of chunks, returns array of following form:
    [
        {
            "chunk": "./path/to/chunk",
            "reason": "<contents of .skip_plan_scanner>"
        },
    ]
    """
    logger = logging.getLogger('return_skipped_chunks')

    skipped_chunks = []

    for chunk in chunks:
        # check if there is a .skip_plan_scanner file
        skip_plan = Path(chunk + '/.skip_plan_scanner')
        if skip_plan.is_file():
            f = open(chunk + '/.skip_plan_scanner', 'r')
            reason = f.read()
            f.close()
            logger.debug("Skipping chunk: %s - reason: %s", chunk, reason)
            skip = {"chunk": chunk, "reason": reason}
            skipped_chunks.append(skip)
    return skipped_chunks


def main(args):
    timestamp_begin = datetime.datetime.now()
    logger = logging.getLogger('main')
    logger.debug(args)

    scan_id = random_scan_id()
    slack_post_message(f"{scan_id}: terraform scanner started")

    chunks = discover_chunks()

    logger.debug("Chunks to examine:")
    for chunk in chunks:
        logger.debug(chunk)

    logger.info("Chunk count: %s", len(chunks))

    processed_chunks = []
    failed_chunks = []
    passed_chunks = []

    skipped_chunks = return_skipped_chunks(chunks)

    # remove skipped chunks from list of ALL chunks
    for skipped in skipped_chunks:
        chunks_to_delete = [c['chunk'] for c in skipped_chunks]
        chunks = list(set(chunks) - set(chunks_to_delete))
        chunks = sorted(chunks)
    logger.info("Skipped {} chunks".format(len(skipped_chunks)))

    # dictionary to hold results, keys are chunk paths
    chunks_results = {}

    logger.info("Starting scan...")
    pool = mp.Pool(processes=args.processes)  # create mp pool
    # feed all the chunks into mp pool to run tf_chunk_process()
    results = [pool.apply_async(tf_chunk_process, args=(
        chunk,
        working_directory,
        scan_id,
        args,
    )) for chunk in chunks]

    # these variables track number of pool workers that return, so we can report on newly completed workers
    processed = -1
    processed_last = 0

    # loop until all pool workers have returned, collecting results within chunks_results dict
    while processed != len(chunks):
        processed = len(chunks_results.keys())
        if processed != processed_last:  # only log progress if we've made some
            processed_last = processed
            logger.info("progress: %s / %s processed", processed, len(chunks))
            logger.debug("processed count:      %s", processed)
            logger.debug("chunks total:         %s", len(chunks))
            logger.debug("remaining chunks:     %s", len(chunks) - processed)

        for result in results:
            if result.ready() is True:
                r = result.get()
                if r['chunk'] not in chunks_results:
                    chunks_results[r['chunk']] = r
                    logging.debug("chunk %s COMPLETE", r['chunk'])

        time.sleep(0.01) # don't pin CPU


    # summarize results
    timestamp_end = datetime.datetime.now()
    elapsed_seconds = (timestamp_end - timestamp_begin).seconds
    passed = []
    failed = []
    for r in chunks_results.keys():
        if chunks_results[r]['plan'] is True:
            passed.append(chunks_results[r]['chunk'])
        elif chunks_results[r]['plan'] is not True:
            failed.append(chunks_results[r]['chunk'])
    summary = "{}: scan complete! Summary: {} Passed, {} Failed, {} Skipped, {} elapsed seconds".format(scan_id, len(passed), len(failed), len(skipped_chunks), elapsed_seconds)
    slack_post_message(summary)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--log-level", help="log level eg 'DEBUG', 'INFO', 'WARNING', 'ERROR'. default 'INFO'", default='INFO')
    argparser.add_argument("--processes", help="concurrent processes to use, default is 2", default=2, type=int)
    argparser.add_argument("--tf-parallelism", help="terraform parallelism to use, default is 10", default=10, type=int)
    args = argparser.parse_args()
    logging.basicConfig(level=args.log_level)
    main(args)
