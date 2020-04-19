#!/bin/bash --

RELEASE=https://raw.githubusercontent.com/expelledboy/bitbar-covid/master/main.py

read_path () {
	cd $HOME
	READ_DIR=$(read -p "> " -re input ; printf "%s" "${input}")
	eval "${1}"=\"\$\{READ_DIR\}\"
}

echo "Where is your BitBar Plugin Directory?"
read_path BITBAR_PLUGIN_DIR

FULL_BITBAR_PLUGIN_DIR=$(cd $HOME/$BITBAR_PLUGIN_DIR && pwd)
SCRIPT=$FULL_BITBAR_PLUGIN_DIR/covid.10m.py

wget -O $SCRIPT $RELEASE 
chmod +x $SCRIPT
