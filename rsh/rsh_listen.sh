#!/bin/sh

socat file:`tty`,raw,echo=0 tcp-listen:9999
