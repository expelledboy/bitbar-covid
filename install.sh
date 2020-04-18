#!/bin/bash

RELEASE=https://raw.githubusercontent.com/expelledboy/bitbar-covid/master/main.py
SCRIPT=$HOME/Documents/Bitbar/covid.10m.py

wget -O $SCRIPT $RELEASE 
chmod +x $SCRIPT
