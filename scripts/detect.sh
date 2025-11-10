#!/bin/bash
# Detect connected Arduino boards

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ARDUINO_CLI="$PROJECT_DIR/bin/arduino-cli"

# Add Arduino CLI to PATH
export PATH="$PROJECT_DIR/bin:$PATH"

echo "Detecting Arduino boards..."
echo ""

$ARDUINO_CLI board list

echo ""
echo "Checking for serial devices..."
ls -la /dev/ttyACM* /dev/ttyUSB* 2>/dev/null

if [ $? -ne 0 ]; then
    echo "No serial devices found."
    echo ""
    echo "Troubleshooting:"
    echo "  1. Connect Arduino via USB"
    echo "  2. Check USB cable (try a different one)"
    echo "  3. Try a different USB port"
    echo "  4. Check dmesg for USB connection messages: dmesg | tail -20"
fi
