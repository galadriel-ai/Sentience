#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting DNS forwarder..."
nohup python "$SCRIPT_DIR/dns_forwarder.py" > "$SCRIPT_DIR/dns_forwarder.log" 2>&1 &
echo "Started DNS forwarder with PID $!"

echo "Starting traffic forwarder..."
nohup python "$SCRIPT_DIR/traffic_forwarder.py" > "$SCRIPT_DIR/traffic_forwarder.log" 2>&1 &
echo "Started traffic forwarder with PID $!"