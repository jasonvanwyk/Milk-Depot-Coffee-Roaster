# Artisan Integration Guide

How to connect your Arduino temperature data to Artisan coffee roasting software.

## Quick Test: Pi Output (No Arduino Needed)

Before connecting the Arduino, test Artisan's external program feature:

### 1. Run Test Script
```bash
cd /home/jason/artisan
python3 test_output.py
```

You should see:
```
# Test output from Pi starting...
# Outputting message every 2 seconds
# Press Ctrl+C to stop
output from pi #1
output from pi #2
output from pi #3
```

### 2. Configure Artisan for External Program

1. **Launch Artisan**:
   ```bash
   artisan
   ```

2. **Open Device Configuration**:
   - Go to **Config** → **Device**

3. **Select External Program**:
   - Device: **External Program**
   - Click on the **Program** field

4. **Enter Command**:
   ```
   /usr/bin/python3 /home/jason/artisan/test_output.py
   ```

5. **Click ON Button**:
   - The green **ON** button should turn to **OFF** (meaning it's active)
   - You should see "output from pi" messages in Artisan's message log

6. **View Messages**:
   - Go to **Help** → **Messages** to see the output
   - Or check the bottom status bar

## Arduino Temperature Data Integration

Once you've tested with the Pi script, connect the real Arduino data:

### Option 1: Direct Serial Port (Simplest)

1. **Make sure Arduino is connected and running** temp_monitor firmware:
   ```bash
   python3 test_serial.py
   # Should show: BT:xx.x,DT:xx.x
   ```

2. **Launch Artisan**

3. **Configure Serial Device**:
   - Config → Device
   - Device: **Fuji PXR** (accepts custom serial format)
   - Port: `/dev/ttyACM0`
   - Baud: `115200`
   - Click **ON**

4. **Map Channels**:
   - Config → Device Assignment
   - Map your channels to ET (Environment Temp) and BT (Bean Temp)

### Option 2: External Program with Python Parser

Create a parser script to format Arduino data for Artisan:

**File**: `/home/jason/artisan/arduino_to_artisan.py`

```python
#!/usr/bin/env python3
"""
Read Arduino serial data and format for Artisan
"""
import serial
import time
import sys
import re

PORT = '/dev/ttyACM0'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # Wait for Arduino to initialize
    ser.reset_input_buffer()

    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()

        # Skip comments
        if line.startswith('#') or not line:
            continue

        # Parse: BT:205.3,DT:187.2
        match = re.match(r'BT:([\d.]+),DT:([\d.]+)', line)
        if match:
            bt = match.group(1)
            dt = match.group(2)

            # Output in Artisan format
            # Format: ET,BT (comma separated)
            print(f"{bt},{dt}", flush=True)

except serial.SerialException as e:
    print(f"# Serial error: {e}", file=sys.stderr)
    sys.exit(1)
except KeyboardInterrupt:
    sys.exit(0)
```

Then in Artisan:
- Device: **External Program**
- Program: `/usr/bin/python3 /home/jason/artisan/arduino_to_artisan.py`

### Option 3: Use Artisan's TC4 Device Type

The TC4 (thermocouple) device type expects a specific format. You can modify the Arduino firmware to output TC4-compatible data:

**Arduino Output Format for TC4**:
```
# timestamp,channel1,channel2,channel3,channel4
0.0,205.3,187.2,0.0,0.0
1.0,206.1,188.5,0.0,0.0
2.0,207.5,190.3,0.0,0.0
```

Then in Artisan:
- Device: **ArduinoTC4**
- Configure channels accordingly

## Troubleshooting

### Artisan Shows "Not Connected"

1. **Check Arduino is sending data**:
   ```bash
   python3 test_serial.py
   ```

2. **Verify port**:
   ```bash
   ls -la /dev/ttyACM*
   ```

3. **Check permissions**:
   ```bash
   groups  # Should include 'dialout'
   ```

4. **Close other programs** using the serial port:
   ```bash
   lsof /dev/ttyACM0
   ```

### Data Not Appearing in Artisan

1. **Check Artisan's Messages window**:
   - Help → Messages
   - Look for error messages

2. **Verify data format**:
   - Artisan expects specific formats for each device type
   - Use External Program with custom parser for flexibility

3. **Enable Artisan debug mode**:
   - Help → Debug → ON
   - Check debug output

### Temperature Curves Not Updating

1. **Click the ON button** in Device menu

2. **Check sampling rate**:
   - Config → Device
   - Sampling interval should be 1-5 seconds

3. **Verify channels are mapped**:
   - Config → Device Assignment
   - Make sure ET and BT channels are assigned

## Testing Without Roasting

You can test the complete system without actual roasting:

### 1. Simulate Temperature Changes

Modify `test_output.py` to simulate temperature ramp:

```python
#!/usr/bin/env python3
import time
import sys

temp = 25.0  # Start at room temp

print("# Simulated roast data", flush=True)

try:
    while temp < 250:
        # Simulate temperature rising
        temp += 0.5  # +0.5°C per second

        # Output in Arduino format
        bt = temp + (2 * (0.5 - (time.time() % 1)))  # Add noise
        dt = temp - 5  # Drum slightly cooler

        print(f"BT:{bt:.1f},DT:{dt:.1f}", flush=True)
        time.sleep(1)

    print("# Simulation complete", flush=True)

except KeyboardInterrupt:
    sys.exit(0)
```

### 2. Record a Test Roast

1. Start the simulation script
2. In Artisan, click **ON** to start recording
3. Click **Start** when ready
4. Let it run for 10-15 minutes
5. Click **Drop** to end the roast
6. **File** → **Save** to save the profile

### 3. Analyze the Data

- **Roast** → **Analyzer** to review the roast
- Check temperature curves
- Verify rate-of-rise calculations
- Export data if needed

## Advanced: Real-Time Roast Control

Once you have sensors working, you can:

### 1. Monitor Rate of Rise (RoR)

Artisan automatically calculates RoR from your temperature data:
- View → Rate of Rise
- Shows how fast temperature is increasing

### 2. Follow a Profile

1. Create a target profile:
   - Roast → Designer
   - Draw your target temperature curve

2. During roasting:
   - Load the profile
   - Artisan shows target vs. actual in real-time

### 3. Log Events

Mark important events during roasting:
- **Charge**: Beans added
- **Dry End**: Drying phase complete
- **First Crack**: Beans start cracking
- **Second Crack**: Deeper roast
- **Drop**: Remove beans

Use buttons in Artisan interface or keyboard shortcuts.

### 4. PID Control (Advanced)

If your roaster has electronic heater/fan control:
- Connect Arduino outputs to relays
- Configure PID in Artisan
- Artisan can automatically adjust heat to follow profile

## Next Steps

1. ✅ **Test with Pi script** (`test_output.py`)
2. ✅ **Test with Arduino** serial data
3. ⏳ **Connect MAX31855 sensors** (once hardware arrives)
4. ⏳ **Calibrate sensors**
5. ⏳ **First test roast** with real beans!

## Resources

- [Artisan Documentation](https://artisan-scope.org/docs/)
- [Artisan Device Configuration](https://artisan-scope.org/devices/index)
- [Artisan Tutorials](https://artisan-scope.org/docs/started/)
- [Home Roasters Forum](https://homeroasters.org)

---

**Last Updated**: 2025-11-10
