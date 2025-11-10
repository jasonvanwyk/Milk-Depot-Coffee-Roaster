#!/bin/bash
# Compile Arduino firmware

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ARDUINO_CLI="$PROJECT_DIR/bin/arduino-cli"

# Add Arduino CLI to PATH
export PATH="$PROJECT_DIR/bin:$PATH"

SKETCH_DIR="${1:-$PROJECT_DIR/arduino-firmware/temp_monitor}"
FQBN="arduino:avr:uno"

echo "Compiling Arduino sketch..."
echo "Sketch: $SKETCH_DIR"
echo "Board: $FQBN"
echo ""

$ARDUINO_CLI compile --fqbn $FQBN "$SKETCH_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Compilation successful!"
else
    echo ""
    echo "✗ Compilation failed!"
    exit 1
fi
