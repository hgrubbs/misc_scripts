#!/bin/bash
if [ $# -eq 1 ] 
then
    echo read/write SSH: $(tmate -S $1 display -p '#{tmate_ssh}')
    echo read-only  SSH: $(tmate -S $1 display -p '#{tmate_ssh_ro}')
else
    echo "usage: $0 <tmate_socket>"
fi
