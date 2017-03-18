#!/bin/bash

procID=`sudo ps -aux | pgrep -f "serial_dpot"`
if ! ["$procID" -eq "$procID"] 2>/dev/null # Check that proc is and integer. It will be empty of no process was found.
then
    sudo kill -SIGINT $procID
fi
python /home/pi/you-do-drone-on/serial_dpot.py

