#!/bin/bash

ME=$(whoami)

if [ "$ME" != "root" ]
then
    echo "you must be root(or use sudo) to run this"
    exit 1
fi

iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -F
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m tcp -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -m tcp -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -j REJECT

echo "iptables adjusted"
