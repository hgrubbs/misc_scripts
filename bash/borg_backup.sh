#!/usr/bin/bash
set -x
set -e
shopt -s expand_aliases


touch /media/hgrubbs/borg/this_is_a_test_file

alias timestamp_military='date +"%Y%m%d.%H%M%S"'
borg create --compression lz4 --stats --progress /media/hgrubbs/borg/borg_repo_1::$(timestamp_military) /home/hgrubbs
