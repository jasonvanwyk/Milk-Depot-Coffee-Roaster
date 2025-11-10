#!/bin/bash
# Upload Arduino firmware

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ARDUINO_CLI="$PROJECT_DIR/bin/arduino-cli"

# Add Arduino CLI to PATH
export PATH="$PROJECT_DIR/bin:$PATH"

SKETCH_DIR="${1:-$PROJECT_DIR/arduino-firmware/temp_monitor}"
PORT="${2:-/dev/ttyACM0}"
FQBN="arduino:avr:uno"

echo "Uploading Arduino sketch..."
echo "Sketch: $SKETCH_DIR"
echo "Port: $PORT"
echo "Board: $FQBN"
echo ""

$ARDUINO_CLI upload -p $PORT --fqbn $FQBN "$SKETCH_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Upload successful!"
    echo ""
    echo "To monitor serial output, run:"
    echo "  ./scripts/monitor.sh"
else
    echo ""
    echo "✗ Upload failed!"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check Arduino is connected: ls -la /dev/ttyACM*"
    echo "  2. Verify permissions: groups (should include 'dialout')"
    echo "  3. Try unplugging and replugging the Arduino"
    echo "  4. Press reset button on Arduino just before uploading"
    exit 1
fi
