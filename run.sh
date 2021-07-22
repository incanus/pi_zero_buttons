#!/usr/bin/env bash

echo 'Starting up...'

./buttons.py

EXIT=$?

echo 22 > /sys/class/gpio/export 2>/dev/null
echo out > /sys/class/gpio/gpio22/direction
echo 0 > /sys/class/gpio/gpio22/value

if [[ $EXIT -eq 1 ]]; then
    echo 'Powering down...'
    /sbin/poweroff
else
    echo 'Quitting!'
fi