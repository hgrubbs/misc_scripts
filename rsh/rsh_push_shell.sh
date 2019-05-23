#!/bin/sh
while true
do
    echo "starting"
    socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:localhost:9999
    echo "restarting in 5s"
    sleep 5
done
