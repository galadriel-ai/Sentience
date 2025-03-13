#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PIDS=$(pgrep -f "$SCRIPT_DIR/api/run.py")

if [ -n "$PIDS" ]; then
    echo "Killing existing instance(s) of Tee Host API..."
    kill $PIDS
    sleep 1
fi

echo "Starting API..."
nohup python "$SCRIPT_DIR/api/run.py" > "$SCRIPT_DIR/logs/api.log" 2>&1 &
echo "Started API with PID $!"

echo "Tee host API has been started."
