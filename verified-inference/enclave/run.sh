#!/bin/bash

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   api.openai.com" >> /etc/hosts

#mkdir -p /run/resolvconf
#echo "nameserver 127.0.0.1" > /run/resolvconf/resolv.conf

# run TLS traffic forwarder
python3.10 /app/traffic_forwarder.py 127.0.0.1 443 &

# sleep so there is time to open enclave debug logs before the server potentially crashes
# python3.10 /app/check_proxies.py

# Start the server
echo "Starting API..."
python3.10 /app/api/run.py
