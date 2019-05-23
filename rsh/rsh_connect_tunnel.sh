#!/bin/sh

while true
do
    echo "starting"
    ssh -p 443 -o ProxyCommand="nc -X connect -x 127.0.0.1:54321 %h %p" -L 9999:localhost:9999 user@host
    echo "restarting in 5s"
    sleep 5
done
