#!/bin/bash

LOGFILE="/home/lucianasterion/Documents/ojoloco/run_app.log"

echo "========== $(date) ==========" >> "$LOGFILE"
echo "run_app.sh iniciado" >> "$LOGFILE"

sleep 8
cd /home/lucianasterion/Documents/ojoloco || exit 1

echo "Entrando al loop" >> "$LOGFILE"

while true
do
    echo "Lanzando App.py" >> "$LOGFILE"
    python3 App.py >> "$LOGFILE" 2>&1
    echo "App cerrada con codigo $?" >> "$LOGFILE"
    echo "Reiniciando en 2 segundos..." >> "$LOGFILE"
    sleep 2
done