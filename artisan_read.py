#!/usr/bin/env python3
"""
Script for Artisan to read Arduino temperature data
Outputs in format: ET,BT (drum temp, bean temp)
"""
import serial
import sys

PORT = '/dev/ttyACM0'
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=2)

    # Read one line from Arduino
    line = ser.readline().decode('utf-8', errors='replace').strip()
    ser.close()

    # Parse: BT:xx.x,DT:xx.x
    if 'BT:' in line and 'DT:' in line:
        parts = line.split(',')
        bt = parts[0].split(':')[1]  # Extract bean temp
        dt = parts[1].split(':')[1]  # Extract drum temp

        # Output in Artisan format: ET,BT (drum, bean)
        print(f"{dt},{bt}")
    else:
        # If can't parse, output zeros to avoid errors
        print("0,0")

except Exception as e:
    # On any error, output zeros
    print("0,0")
    sys.exit(0)
