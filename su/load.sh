#!/bin/bash
if which ampy >/dev/null 2>&1; then
    if  ls /dev/ttyUSB0 > /dev/null 2>&1 ; then
        ampy -p /dev/ttyUSB0 put lib
        sync
        echo "Loaded server framework"
        ampy -p /dev/ttyUSB0 put main.py
        sync
        echo "Loaded main"
        ampy -p /dev/ttyUSB0 put acf_network.py
        sync
        echo "Loaded network library"
    else
        echo "Connect ESP device"
    fi
else
    echo "Install ampy to load files"
fi
