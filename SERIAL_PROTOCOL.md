# Serial Communication Protocol

Documentation for serial communication between Arduino and Artisan software.

## Overview

The Arduino sends temperature readings over USB serial connection to the Raspberry Pi. Artisan reads this data to display real-time temperature curves and control the roasting process.

## Connection Details

### Physical Connection
- **Interface**: USB Serial (CDC ACM)
- **Cable**: USB Type-B to USB Type-A
- **Device**: Appears as `/dev/ttyACM0` or `/dev/ttyUSB0` on Raspberry Pi

### Serial Parameters
- **Baud Rate**: 115200 bps
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1
- **Flow Control**: None
- **Line Ending**: LF (`\n`)

## Data Format

### Temperature Data Message

Each message contains both temperature readings in a single line:

```
BT:xxx.x,DT:xxx.x\n
```

**Fields**:
- `BT`: Bean Temperature (in degrees Celsius)
- `DT`: Drum Temperature (in degrees Celsius)
- Values have 1 decimal place precision
- Fields are comma-separated
- Line ends with newline (`\n`)

### Example Messages

```
BT:23.5,DT:24.1
BT:205.3,DT:187.2
BT:218.9,DT:205.5
```

### Comment Lines

The Arduino may send comment lines starting with `#`:

```
# Milk Depot Coffee Roaster - Temperature Monitor
# Ready to send temperature data
# Format: BT:xxx.x,DT:xxx.x
```

**Note**: Artisan should ignore lines starting with `#`.

## Timing

- **Sample Rate**: 1 Hz (one reading per second)
- **Interval**: 1000 milliseconds between messages
- **Latency**: < 50ms from measurement to transmission

## Data Flow

```
┌──────────┐      USB Serial       ┌───────────────┐
│          │     115200 baud       │               │
│ Arduino  ├──────────────────────>│ Raspberry Pi  │
│   UNO    │   BT:xxx,DT:xxx      │  (Artisan)    │
│          │                       │               │
└──────────┘                       └───────────────┘
```

## Artisan Configuration

### External Program Method

1. Open Artisan
2. Go to **Config** → **Device Assignment**
3. Select device type: **External Program**
4. Configure program to read from serial port:

**External Program Command** (Linux):
```bash
stty -F /dev/ttyACM0 115200 raw -echo
cat /dev/ttyACM0
```

Or use a Python script (recommended):
```python
#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

while True:
    line = ser.readline().decode('utf-8').strip()
    if line and not line.startswith('#'):
        print(line)
```

### Serial Port Direct Method

1. Open Artisan
2. Go to **Config** → **Device**
3. Device type: **Phidget 1048** (or similar CSV format)
4. Configure:
   - **Port**: `/dev/ttyACM0`
   - **Baud**: 115200
   - **Byte Size**: 8
   - **Parity**: None
   - **Stop Bits**: 1

5. Map channels:
   - **Channel 1 (ET)**: Bean Temperature (BT)
   - **Channel 2 (BT)**: Drum Temperature (DT)

### Custom CSV Parsing

If needed, you can configure Artisan to parse the custom format:

1. **Config** → **Events** → **Serial**
2. Add parsing rule:
   - Pattern: `BT:(\d+\.\d+),DT:(\d+\.\d+)`
   - Group 1 → ET (Environment/Bean Temperature)
   - Group 2 → BT (Bean Temperature in Artisan's terminology, which is actually drum)

**Note**: Artisan uses ET (Environment Temp) and BT (Bean Temp) terminology, which may differ from your hardware labels.

## Error Handling

### Error Conditions

The Arduino may send error messages:

```
# ERROR: Thermocouple disconnected
# ERROR: Temperature out of range
# WARNING: Probe 1 reading unstable
```

All error messages start with `#` and can be logged by Artisan.

### Connection Loss

If serial connection is lost:
- Artisan will show "disconnected" status
- Last known temperature values remain on screen
- User should check USB cable and Arduino power
- Artisan can be configured to sound an alarm

### Invalid Data

If Artisan receives malformed data:
- Invalid lines are skipped
- Artisan continues waiting for valid data
- Check Arduino Serial Monitor for actual output
- Verify baud rate matches on both sides

## Testing

### Test with Screen

```bash
# View raw serial output
screen /dev/ttyACM0 115200

# Expected output:
# Milk Depot Coffee Roaster - Temperature Monitor
# Ready to send temperature data
# Format: BT:xxx.x,DT:xxx.x
BT:23.5,DT:24.1
BT:23.6,DT:24.1
BT:23.5,DT:24.2
```

Exit: Press `Ctrl-A` then `K` then `Y`

### Test with Python

```python
#!/usr/bin/env python3
import serial
import time

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
print("Waiting for Arduino to initialize...")
time.sleep(2)

print("Reading temperature data:")
try:
    for i in range(10):  # Read 10 samples
        line = ser.readline().decode('utf-8').strip()
        print(line)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    ser.close()
```

### Test with Arduino Serial Monitor

1. Open Arduino IDE
2. **Tools** → **Serial Monitor**
3. Set baud rate: **115200**
4. Verify output format matches specification

## Protocol Extensions (Future)

Possible future enhancements:

### Bidirectional Communication

Arduino could accept commands from Artisan:
```
> HEATER:50        # Set heater to 50%
< ACK:HEATER:50   # Arduino acknowledges
> FAN:75          # Set fan to 75%
< ACK:FAN:75      # Arduino acknowledges
```

### Additional Sensors

```
BT:205.3,DT:187.2,AT:25.5,RH:45.2
```
- `AT`: Ambient Temperature
- `RH`: Relative Humidity

### Metadata

```
# FW_VERSION:1.0
# DEVICE:Milk-Depot-Roaster
# PROBES:2
BT:205.3,DT:187.2
```

## Troubleshooting

### No Data Received

1. Check Arduino is powered (LED on)
2. Verify USB connection: `ls -la /dev/ttyACM*`
3. Check permissions: user should be in `dialout` group
4. Test with `cat /dev/ttyACM0`
5. Verify baud rate: `stty -F /dev/ttyACM0`

### Garbled Data

1. Verify baud rate matches (115200)
2. Check for electromagnetic interference
3. Try a different USB cable
4. Move Arduino away from high-voltage lines
5. Add ferrite beads to USB cable

### Slow Updates

1. Check `SAMPLE_INTERVAL_MS` in Arduino code
2. Verify Artisan polling rate settings
3. Check for USB hub latency (connect directly)
4. Monitor system load on Raspberry Pi

### Temperature Spikes

1. Check probe connections (loose wires)
2. Verify grounding
3. Add software filtering in Arduino code
4. Use shielded thermocouple cables
5. Enable Artisan's smoothing/filtering

## References

- [Arduino Serial Reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [Artisan External Program Documentation](https://artisan-scope.org/docs/external-programs/)
- [Linux Serial Port Programming](https://tldp.org/HOWTO/Serial-Programming-HOWTO/)
- [PySerial Documentation](https://pyserial.readthedocs.io/)

## Version History

- **v1.0** (2025-11-10): Initial protocol definition
  - Two-channel temperature data (BT, DT)
  - 115200 baud serial communication
  - CSV-like format

---

**Last Updated**: 2025-11-10
