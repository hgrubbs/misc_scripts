#!/bin/sh -x
#script to copy/sync dropbox via rclone, if you pass an argument it must be either 'sync' or 'copy', else defaults to 'copy'

COMMAND="copy"

if [ $# -gt 0 ]; then
    COMMAND=$1
fi

echo "begin sync $(date)"
echo "COMMAND is '$COMMAND'"

cd /plex/dropbox

rclone ${COMMAND} dropbox:"Camera Uploads" "Camera Uploads"
rclone ${COMMAND} dropbox:/Documents Documents
rclone ${COMMAND} dropbox:/Photos Photos
rclone ${COMMAND} dropbox:/Videos Videos
rclone ${COMMAND} dropbox:/incoming incoming

echo "end sync $(date)"
