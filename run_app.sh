#!/bin/bash

sleep 8
cd /home/lucianasterion/Documents/ojoloco

while true
do
    python3 App.py
    echo "App cerrada, reiniciando en 2 segundos..."
    sleep 2
done