#!/bin/bash
PNAME=${1:-java}
top -p `ps -ef | grep $PNAME | grep -v grep | awk '{print $2}' | tr "\n" "," | sed 's/,$//'`
#top -p `pgrep $PNAME | tr "\n" "," | sed 's/,$//'`

