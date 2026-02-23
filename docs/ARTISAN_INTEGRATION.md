# Artisan Integration Guide - 3-Channel Setup

How to configure Artisan coffee roasting software for the Milk Depot 3-channel thermocouple system.

## System Overview

```
┌─────────────────┐     USB Serial      ┌──────────────────┐
│   Arduino UNO   │◄──────────────────►│   Raspberry Pi   │
│                 │     115200 baud     │                  │
│  3x MAX31855    │                     │     Artisan      │
│  thermocouples  │                     │     v3.4.0       │
└─────────────────┘                     └──────────────────┘

Temperature Channels:
  Channel 1 (ET) ─── Exhaust Temperature
  Channel 2 (BT) ─── Bean Temperature
  Channel 3 (FT) ─── Flame Temperature
```

## Quick Setup (ArduinoTC4)

This is the recommended configuration using the TC4 protocol.

### Step 1: Verify Arduino Connection

```bash
# Check Arduino is connected
ls -la /dev/ttyACM*

# Test serial communication
python3 test_serial.py
```

### Step 2: Configure Primary Device

1. **Launch Artisan**: `artisan`

2. **Open Device Configuration**:
   - Menu: **Config** → **Device**

3. **Set Primary Device**:
   - Device: **ArduinoTC4**
   - Port: `/dev/ttyACM0`
   - Baud Rate: **115200**

4. **Click OK** to save

### Step 3: Add Extra Device for Flame Temperature

1. **Open Device Configuration**:
   - Menu: **Config** → **Device**

2. **Go to Extra Devices Tab**

3. **Click Add (+)**:
   - Device: **ArduinoTC4_34**
   - Leave other settings default

4. **Click OK** to save

### Step 4: Configure Curve Labels (Optional)

1. **Menu**: **Config** → **Curves**

2. **Rename curves for clarity**:
   - Extra 1: "FT" or "Flame"
   - Extra 2: (unused, can hide)

3. **Adjust colors** if desired:
   - ET: Blue
   - BT: Red/Brown
   - FT: Orange

### Step 5: Start Monitoring

1. **Click the ON button** (green button in toolbar)
2. You should see three temperature curves:
   - ET (Channel 1) - Exhaust
   - BT (Channel 2) - Bean
   - FT (Channel 3) - Flame

## Alternative: External Program Method

If you prefer continuous output (using `temp_monitor` firmware):

### Step 1: Create Parser Script

The Arduino outputs: `ET:xxx.x,BT:xxx.x,FT:xxx.x`

Artisan External Program expects: `temp1,temp2,temp3,...`

Create `/home/jason/artisan/artisan_3ch_read.py`:

```python
#!/usr/bin/env python3
"""
Parse 3-channel Arduino output for Artisan External Program
"""
import serial
import sys

PORT = '/dev/ttyACM0'
BAUD = 115200

try:
    ser = serial.Serial(PORT, BAUD, timeout=2)

    # Read lines until we get valid data
    for _ in range(5):
        line = ser.readline().decode('utf-8', errors='replace').strip()

        # Skip comments
        if line.startswith('#') or not line:
            continue

        # Parse: ET:xx.x,BT:xx.x,FT:xx.x
        if 'ET:' in line and 'BT:' in line and 'FT:' in line:
            parts = line.split(',')
            et = parts[0].split(':')[1]
            bt = parts[1].split(':')[1]
            ft = parts[2].split(':')[1]

            # Output for Artisan: ET,BT,extra1
            print(f"{et},{bt},{ft}")
            break
    else:
        print("0,0,0")

    ser.close()

except Exception as e:
    print("0,0,0")
    sys.exit(0)
```

Make it executable:
```bash
chmod +x /home/jason/artisan/artisan_3ch_read.py
```

### Step 2: Configure Artisan

1. **Config** → **Device**
2. Device: **External Program**
3. Program: `/usr/bin/python3 /home/jason/artisan/artisan_3ch_read.py`
4. **OK**

## Channel Mapping Reference

| Artisan Device | Channels Provided | Notes |
|----------------|-------------------|-------|
| ArduinoTC4 | ET (Ch1), BT (Ch2) | Primary device |
| ArduinoTC4_34 | Extra1 (Ch3), Extra2 (Ch4) | Extra device for additional channels |
| ArduinoTC4_56 | Heater duty, Fan duty | For output control logging |
| ArduinoTC4_78 | PID SV, Internal temp | For PID control logging |

## Troubleshooting

### No Connection / "Not Connected"

1. **Verify port**:
   ```bash
   ls /dev/ttyACM*
   # If not found, try:
   ls /dev/ttyUSB*
   ```

2. **Check permissions**:
   ```bash
   groups  # Should include 'dialout'
   ```

3. **Verify Arduino is responding**:
   ```bash
   # Open serial monitor
   screen /dev/ttyACM0 115200
   # Type: READ
   # Should see: 25.00,xxx.xx,xxx.xx,xxx.xx,0.00
   # Exit with Ctrl-A, K, Y
   ```

### Temperatures Not Updating

1. **Check sampling**:
   - Config → Device → Sampling should be 1.0s

2. **Verify data format**:
   ```bash
   python3 test_serial.py
   ```

3. **Check Artisan messages**:
   - Help → Messages
   - Look for error messages

### Extra Device Not Showing

1. Ensure **ArduinoTC4_34** is added in Extra Devices tab
2. Check Config → Curves to ensure Extra 1 curve is enabled/visible
3. Restart Artisan after adding extra device

### Flame Temperature (FT) Reads Zero

1. Verify Channel 3 is connected in firmware
2. Check MAX31855 #3 wiring (CS → D8)
3. Test thermocouple with multimeter (should show ~0-40mV at room temp)

## Curve Display Configuration

### Recommended Setup

1. **Config** → **Curves**

2. **Labels**:
   | Curve | Label | Color |
   |-------|-------|-------|
   | ET | "Exhaust" | Blue (#0000FF) |
   | BT | "Bean" | Brown (#8B4513) |
   | Extra 1 | "Flame" | Orange (#FF8C00) |

3. **Rate of Rise (RoR)**:
   - Enable for BT (most useful for roasting)
   - Optionally enable for ET

4. **Hide Unused**:
   - Extra 2 (Channel 4) can be hidden

## Testing Without Roasting

### Simulate Temperature Ramp

Use this Python script to simulate a roast:

```python
#!/usr/bin/env python3
"""Simulate a coffee roast temperature profile"""
import time
import sys

# Starting temps (room temperature)
et = 25.0
bt = 25.0
ft = 150.0  # Burner on

print("# Simulated roast starting...", flush=True)

try:
    while bt < 220:  # End at typical dark roast temp
        # Simulate temperature rise
        et += 0.8
        bt += 0.5
        ft = 350 + (50 * (0.5 - (time.time() % 1)))  # Fluctuating flame

        # Simulate first crack plateau around 195-200°C
        if 195 <= bt <= 205:
            bt += 0.2  # Slower rise during crack

        print(f"ET:{et:.1f},BT:{bt:.1f},FT:{ft:.1f}", flush=True)
        time.sleep(1)

    print("# Roast complete", flush=True)

except KeyboardInterrupt:
    sys.exit(0)
```

Save as `simulate_roast.py` and run to generate test data.

## Recording a Roast

### Standard Workflow

1. **Before roasting**:
   - Click **ON** to start monitoring
   - Verify all three curves are updating
   - Preheat roaster to target charge temperature

2. **During roast**:
   - Click **CHARGE** when beans enter drum
   - Mark **DRY END** (~160°C, color change)
   - Mark **FCs** (First Crack Start, ~196°C)
   - Mark **FCe** (First Crack End)
   - Mark **SCs** if going darker
   - Click **DROP** when beans exit

3. **After roast**:
   - Click **OFF** to stop recording
   - File → Save to store profile

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Start/Stop recording |
| C | Charge |
| D | Drop |
| 1 | First Crack Start |
| 2 | First Crack End |
| 3 | Second Crack Start |

## Advanced: PID Control (Future)

If you add heater/fan control via relays:

1. Wire relay control to Arduino digital outputs
2. Update firmware to handle `OT1` and `OT2` commands
3. Configure Artisan PID with appropriate tuning
4. Enable ArduinoTC4_56 extra device for duty logging

## Resources

- [Artisan Documentation](https://artisan-scope.org/docs/)
- [Artisan Arduino/TC4 Setup](https://artisan-scope.org/devices/arduino/)
- [TC4 Protocol Reference](https://github.com/greencardigan/TC4-shield)
- [Home Roasters Forum](https://homeroasters.org)

---

**Last Updated**: 2024-12-30
