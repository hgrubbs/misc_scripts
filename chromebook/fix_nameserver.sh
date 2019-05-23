#!/bin/bash
grep -q 'nameserver 8.8.8.8' /etc/resolv.conf
if [ $? -eq 1 ];
then
	sudo sh -c "echo nameserver 8.8.8.8 >> /etc/resolv.conf"
	echo "nameserver ADDED"
else
	echo "nameserver ALREADY ADDED"
fi;
