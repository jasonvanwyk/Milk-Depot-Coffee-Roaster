#!/usr/bin/env python3
"""
Simple test script to output a message every 2 seconds
Use this to test Artisan's external program input
"""
import time
import sys

# Counter for demo
counter = 0

print("# Test output from Pi starting...", flush=True)
print("# Outputting message every 2 seconds", flush=True)
print("# Press Ctrl+C to stop", flush=True)

try:
    while True:
        counter += 1
        print(f"output from pi #{counter}", flush=True)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n# Stopped by user", flush=True)
    sys.exit(0)
