#!/bin/bash
# Monitor Arduino serial output

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PORT="${1:-/dev/ttyACM0}"
BAUD="${2:-115200}"

echo "Monitoring Arduino serial output..."
echo "Port: $PORT"
echo "Baud rate: $BAUD"
echo "Press Ctrl+C to stop"
echo "----------------------------------------"

python3 "$PROJECT_DIR/test_serial.py"
