#!/bin/sh
set -o pipefail # exit non-zero on any failure in piped commands
set -e # exit non-zero from script if any command fails
set -u # treat unset variable references as error, exit non-zero
set -f # disable globbing
