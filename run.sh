#!/bin/sh
python main.py 5000 &

while true; do
        git pull --force
        python update.py
        sleep 5m
done
