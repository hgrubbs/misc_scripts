#!/bin/bash
sudo stop shill
sudo start shill BLACKLISTED_DEVICES=tun0
#sudo start shill --device-black-list="tun0,tun1,tun2"
