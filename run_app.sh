#!/bin/bash

cd /home/lucianasterion/Documents/ojoloco

while true
do
    /home/lucianasterion/Documents/ojoloco/.venv/bin/python App.py
    echo "App cerrada, reiniciando en 2 segundos..."
    sleep 2
done