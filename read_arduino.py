#!/usr/bin/env python3
"""
Simple script to read Arduino serial output
Works with any baud rate
"""
import serial
import time
import sys

PORT = '/dev/ttyACM0'
BAUD = int(sys.argv[1]) if len(sys.argv) > 1 else 9600

print(f"Opening {PORT} at {BAUD} baud...")
print("Reading Arduino output (Ctrl+C to stop):")
print("-" * 50)

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    ser.reset_input_buffer()

    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        if line:
            print(line)

except serial.SerialException as e:
    print(f"\nError: {e}")
    print("\nTroubleshooting:")
    print("  1. Close Arduino IDE Serial Monitor")
    print("  2. Check: lsof /dev/ttyACM0")
    print("  3. Verify Arduino is connected: ls -la /dev/ttyACM*")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n\nStopped by user")
    sys.exit(0)
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
