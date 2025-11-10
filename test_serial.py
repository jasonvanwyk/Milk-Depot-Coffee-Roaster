#!/usr/bin/env python3
"""
Simple script to test Arduino serial communication
"""
import serial
import time
import sys

PORT = '/dev/ttyACM0'
BAUD = 115200

try:
    print(f"Opening serial port {PORT} at {BAUD} baud...")
    ser = serial.Serial(PORT, BAUD, timeout=1)

    # Wait for Arduino to reset after serial connection
    print("Waiting for Arduino to initialize (2 seconds)...")
    time.sleep(2)

    # Clear any garbage in the buffer
    ser.reset_input_buffer()

    print("Reading data from Arduino:")
    print("-" * 50)

    # Read 20 lines
    for i in range(20):
        try:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                print(f"{i+1}: {line}")
        except Exception as e:
            print(f"Error reading line: {e}")

    print("-" * 50)
    ser.close()

except serial.SerialException as e:
    print(f"Serial error: {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print("\nStopped by user")
    sys.exit(0)
