# Serial Communication Protocol

Documentation for serial communication between Arduino and Artisan software.

## Overview

The Arduino reads 3 K-type thermocouples via MAX31855 amplifiers and communicates with Artisan roasting software on Raspberry Pi over USB serial.

**Temperature Channels:**
- **ET (Channel 1)**: Exhaust/Environment Temperature
- **BT (Channel 2)**: Bean Temperature
- **FT (Channel 3)**: Flame/Burner Temperature

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

---

## Protocol Options

### Option 1: TC4 Protocol (Recommended)

**Firmware**: `tc4_emulator`
**Artisan Device**: ArduinoTC4 + ArduinoTC4_34 (for channel 3)

This is a **command/response** protocol. Artisan sends commands, Arduino responds.

#### READ Command

```
Artisan sends:  READ\n
Arduino sends:  25.00,180.50,195.20,350.00,0.00\n
```

**Response format**: `ambient,chan1,chan2,chan3,chan4`

| Field | Description | Example |
|-------|-------------|---------|
| ambient | Ambient/reference temperature | 25.00 |
| chan1 | ET (Exhaust Temperature) | 180.50 |
| chan2 | BT (Bean Temperature) | 195.20 |
| chan3 | FT (Flame Temperature) | 350.00 |
| chan4 | Unused | 0.00 |

#### Other Commands

| Command | Description | Response |
|---------|-------------|----------|
| `READ` | Request temperature data | `ambient,c1,c2,c3,c4` |
| `CHAN;ijkl` | Set channel mapping | `# CHAN: acknowledged` |
| `UNITS;C` or `UNITS;F` | Set temperature units | `# Units: Celsius` |
| `FILT;ijkl` | Set filter values | `# FILT: acknowledged` |
| `OT1;nnn` | Heater output (0-100%) | (silent) |
| `OT2;nnn` | Fan output (0-100%) | (silent) |
| `PID;...` | PID control commands | `# PID: acknowledged` |

#### Comment Lines

Lines starting with `#` are comments (ignored by Artisan):

```
# Milk Depot Coffee Roaster
# TC4 Emulator - 3 Channel
# Channels: ET, BT, FT
# Baud: 115200
```

---

### Option 2: Continuous Output Protocol

**Firmware**: `temp_monitor`
**Artisan Device**: External Program

Arduino sends data continuously every 1000ms without commands.

#### Data Format

```
ET:xxx.x,BT:xxx.x,FT:xxx.x\n
```

**Example:**
```
ET:180.5,BT:195.2,FT:350.0
ET:181.2,BT:196.1,FT:352.3
ET:182.0,BT:197.0,FT:348.5
```

#### Fields
- `ET`: Exhaust Temperature (°C, 1 decimal)
- `BT`: Bean Temperature (°C, 1 decimal)
- `FT`: Flame Temperature (°C, 1 decimal)

---

## Data Flow Diagrams

### TC4 Protocol (Command/Response)

```
┌──────────────┐                      ┌──────────────┐
│   Artisan    │                      │   Arduino    │
│  (Raspberry  │                      │     UNO      │
│     Pi)      │                      │              │
└──────┬───────┘                      └──────┬───────┘
       │                                     │
       │  ────── READ\n ──────────────────>  │
       │                                     │
       │  <──── 25.00,180.5,195.2,350.0,0.00 │
       │                                     │
       │           (1 second later)          │
       │                                     │
       │  ────── READ\n ──────────────────>  │
       │                                     │
       │  <──── 25.00,181.2,196.1,352.3,0.00 │
       │                                     │
```

### Continuous Output Protocol

```
┌──────────────┐                      ┌──────────────┐
│   Artisan    │                      │   Arduino    │
│  (Raspberry  │                      │     UNO      │
│     Pi)      │                      │              │
└──────┬───────┘                      └──────┬───────┘
       │                                     │
       │  <──── ET:180.5,BT:195.2,FT:350.0   │
       │                                     │
       │           (1 second later)          │
       │                                     │
       │  <──── ET:181.2,BT:196.1,FT:352.3   │
       │                                     │
       │           (1 second later)          │
       │                                     │
       │  <──── ET:182.0,BT:197.0,FT:348.5   │
       │                                     │
```

---

## Artisan Configuration

### For TC4 Protocol

1. **Config** → **Device**
2. Device: **ArduinoTC4**
3. Port: `/dev/ttyACM0`
4. Baud: **115200**

5. **Config** → **Device** → **Extra Devices**
6. Add: **ArduinoTC4_34** (for Flame Temperature on channel 3)

### For Continuous Output

1. **Config** → **Device**
2. Device: **External Program**
3. Program: `/usr/bin/python3 /path/to/artisan_3ch_read.py`

Parser script example:
```python
#!/usr/bin/env python3
import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
for _ in range(5):
    line = ser.readline().decode().strip()
    if 'ET:' in line and 'BT:' in line:
        parts = line.split(',')
        et = parts[0].split(':')[1]
        bt = parts[1].split(':')[1]
        ft = parts[2].split(':')[1]
        print(f"{et},{bt},{ft}")
        break
ser.close()
```

---

## Timing

| Parameter | Value |
|-----------|-------|
| Sample Rate | 1 Hz (1 reading/second) |
| Sample Interval | 1000 ms |
| Response Latency | < 50 ms |
| Thermocouple Read Time | ~100 ms per channel |

---

## Error Handling

### Thermocouple Errors

When MAX31855 reports an error (open circuit, short, etc.):
- Arduino returns last good reading
- Prevents graph spikes in Artisan
- Error flag set internally (visible on OLED if enabled)

### Connection Loss

If USB disconnects:
- Artisan shows "disconnected" status
- Reconnect USB cable
- Click OFF then ON in Artisan to reconnect

### Invalid Data

- Malformed lines are ignored
- Artisan continues waiting for valid data
- Check Arduino Serial Monitor for debugging

---

## Testing

### Test TC4 Protocol

```bash
# Open serial connection
screen /dev/ttyACM0 115200

# Type (then press Enter):
READ

# Expected response:
25.00,65.32,67.45,68.12,0.00

# Exit: Ctrl-A, K, Y
```

### Test Continuous Output

```bash
# Monitor serial output
python3 test_serial.py

# Expected:
# Milk Depot Coffee Roaster - 3 Channel Temperature Monitor
# Format: ET:xxx.x,BT:xxx.x,FT:xxx.x
ET:65.3,BT:67.4,FT:68.1
ET:65.5,BT:67.6,FT:68.3
```

### Test with Python

```python
#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
time.sleep(2)  # Wait for Arduino init

# Test TC4 protocol
ser.write(b'READ\n')
response = ser.readline().decode().strip()
print(f"Response: {response}")

# Parse response
values = response.split(',')
print(f"Ambient: {values[0]}°C")
print(f"ET: {values[1]}°C")
print(f"BT: {values[2]}°C")
print(f"FT: {values[3]}°C")

ser.close()
```

---

## Troubleshooting

### No Data Received

1. Check Arduino power (LED on)
2. Verify USB: `ls -la /dev/ttyACM*`
3. Check permissions: `groups` (should include `dialout`)
4. Test raw: `cat /dev/ttyACM0`

### Garbled Data

1. Verify baud rate (115200 on both sides)
2. Check for EMI interference
3. Try different USB cable
4. Try direct USB connection (no hub)

### Slow/Delayed Readings

1. Thicker thermocouple probes = slower response
2. Check `SAMPLE_INTERVAL_MS` in firmware
3. USB hubs add latency

### Temperature Spikes

1. Check probe connections
2. Verify thermocouple polarity (red = negative for K-type)
3. Add grounding/shielding
4. Enable Artisan smoothing filter

---

## References

- [Arduino Serial Reference](https://www.arduino.cc/reference/en/language/functions/communication/serial/)
- [Artisan ArduinoTC4 Documentation](https://artisan-scope.org/devices/arduino/)
- [TC4 Protocol Reference](https://github.com/greencardigan/TC4-shield)
- [PySerial Documentation](https://pyserial.readthedocs.io/)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2024-12-30 | 3-channel support, TC4 protocol, MAX31855 |
| 1.0 | 2024-11-10 | Initial 2-channel protocol |

---

**Last Updated**: 2024-12-30
