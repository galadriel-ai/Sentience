SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PIDS=$(pgrep -f "$SCRIPT_DIR/dns_forwarder.py")

if [ -n "$PIDS" ]; then
    echo "Killing existing instance(s) of DNS forwarder..."
    kill $PIDS
    sleep 1
fi

PIDS=$(pgrep -f "$SCRIPT_DIR/traffic_forwarder.py")

if [ -n "$PIDS" ]; then
    echo "Killing existing instance(s) of traffic forwarder..."
    kill $PIDS
    sleep 1
fi

echo "All forwarders have been stopped."
