#!/usr/bin/env bash
cd /
cd /home/pi/stl-upload-server
nohup python3 server.py > /dev/null 2>&1 &
