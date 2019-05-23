#!/bin/bash
sleep 2

sudo powertop --auto-tune
touch $HOME/local/log/powertop_tuned

killall syndaemon
syndaemon -i 0.50 -m 0.050 -K -v -d -R &> /dev/null
touch $HOME/local/log/syndaemon_restarted
