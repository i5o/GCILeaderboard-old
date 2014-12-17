#!/bin/sh
python update.py
python main.py 5000 &

while true; do
	sleep 5m
	python update.py
done
