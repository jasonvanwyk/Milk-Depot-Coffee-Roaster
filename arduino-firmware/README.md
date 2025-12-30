# Arduino Temperature Monitor Firmware

Custom Arduino firmware for the Milk Depot Coffee Roaster - 3-channel thermocouple interface for Artisan software.

## Overview

This firmware reads temperature from three K-type thermocouples via MAX31855 amplifier modules:

| Channel | Name | Description |
|---------|------|-------------|
| 1 | ET | Exhaust/Environment Temperature - air leaving the drum |
| 2 | BT | Bean Temperature - probe in bean mass |
| 3 | FT | Flame Temperature - near the burner |

Temperature data is sent over USB serial to Raspberry Pi running Artisan software.

## Firmware Variants

| Sketch | Protocol | Use Case |
|--------|----------|----------|
| `tc4_emulator/` | TC4 command/response | **Production** - Use with ArduinoTC4 device |
| `temp_monitor/` | Continuous output | Alternative - Use with External Program |
| `serial_test/` | Basic serial | Testing only |
| `blank/` | None | For easy uploads when main firmware blocks |

## Hardware Requirements

### Required Components
- Arduino UNO R3
- 3x MAX31855 thermocouple amplifier modules
- 3x K-type thermocouples (Olimex TC-K-TYPE-1.5M recommended)
- USB cable for Arduino → Raspberry Pi

### Optional
- SSD1306 OLED display (128x64, I2C) for local readout

## Wiring

### SPI Bus (Shared)
```
Arduino D13 (SCK)  ────┬──── MAX31855 #1 SCK
                       ├──── MAX31855 #2 SCK
                       └──── MAX31855 #3 SCK

Arduino D12 (MISO) ────┬──── MAX31855 #1 DO
                       ├──── MAX31855 #2 DO
                       └──── MAX31855 #3 DO
```

### Chip Select (Individual)
```
Arduino D10 ──── MAX31855 #1 CS (ET - Exhaust)
Arduino D9  ──── MAX31855 #2 CS (BT - Bean)
Arduino D8  ──── MAX31855 #3 CS (FT - Flame)
```

### Power (Shared)
```
Arduino 5V  ────┬──── All MAX31855 VCC
                └──── OLED VCC (optional)

Arduino GND ────┬──── All MAX31855 GND
                └──── OLED GND (optional)
```

### I2C for OLED (Optional)
```
Arduino A4 (SDA) ──── OLED SDA
Arduino A5 (SCL) ──── OLED SCL
```

## Installation

### 1. Install Required Libraries

Open Arduino IDE → Sketch → Include Library → Manage Libraries:

- **Adafruit MAX31855** (required)
- **Adafruit BusIO** (dependency)
- **Adafruit SSD1306** (optional, for OLED)
- **Adafruit GFX Library** (optional, for OLED)

### 2. Enable Hardware Support

Edit `tc4_emulator.ino` (or `temp_monitor.ino`):

```cpp
// Uncomment this line:
#include <Adafruit_MAX31855.h>

// Uncomment thermocouple objects:
Adafruit_MAX31855 thermoET(PIN_SCK, PIN_CS_ET, PIN_MISO);
Adafruit_MAX31855 thermoBT(PIN_SCK, PIN_CS_BT, PIN_MISO);
Adafruit_MAX31855 thermoFT(PIN_SCK, PIN_CS_FT, PIN_MISO);
```

In each `readTemperature_XX()` function:
- Uncomment the MAX31855 library code block
- Delete/comment the `readAnalogSimulated()` line

### 3. Compile and Upload

From project root:
```bash
./scripts/compile.sh arduino-firmware/tc4_emulator
./scripts/upload.sh arduino-firmware/tc4_emulator
```

If upload fails (firmware blocking bootloader):
- Press Arduino RESET button immediately after starting upload
- Or upload `blank/blank.ino` first

### 4. Test

```bash
# Monitor serial output
python3 test_serial.py

# Or test TC4 protocol manually
screen /dev/ttyACM0 115200
# Type: READ
# Should see: 25.00,xxx.xx,xxx.xx,xxx.xx,0.00
```

## Serial Protocol

### TC4 Protocol (tc4_emulator)

**Command/Response format:**
```
Artisan sends:  READ
Arduino sends:  25.00,180.50,195.20,350.00,0.00
                 │     │      │      │      └── Chan4 (unused)
                 │     │      │      └── Chan3 (FT)
                 │     │      └── Chan2 (BT)
                 │     └── Chan1 (ET)
                 └── Ambient temp
```

**Supported commands:** `READ`, `CHAN`, `UNITS`, `FILT`, `OT1`, `OT2`, `PID`

### Continuous Output (temp_monitor)

```
ET:180.5,BT:195.2,FT:350.0
```
Sent every 1000ms.

### Settings
- **Baud Rate**: 115200
- **Data Bits**: 8
- **Parity**: None
- **Stop Bits**: 1

## Calibration

### Procedure

1. **Ice Water Test (0°C)**:
   - Place all probes in ice water slurry
   - Wait for readings to stabilize
   - Note offset from 0°C

2. **Update Firmware**:
   ```cpp
   float calibOffset_ET = 0.0 - reading;  // e.g., -2.3
   float calibOffset_BT = 0.0 - reading;
   float calibOffset_FT = 0.0 - reading;
   ```

3. **Verify with Boiling Water** (~96°C at Johannesburg altitude)

### Example
If ET reads 2.3°C in ice water:
```cpp
float calibOffset_ET = -2.3;
```

## Configuration

Edit constants in firmware source:

| Constant | Default | Description |
|----------|---------|-------------|
| `BAUD_RATE` | 115200 | Serial speed |
| `PIN_CS_ET` | 10 | Chip select for ET |
| `PIN_CS_BT` | 9 | Chip select for BT |
| `PIN_CS_FT` | 8 | Chip select for FT |
| `calibOffset_ET` | 0.0 | ET calibration offset |
| `calibOffset_BT` | 0.0 | BT calibration offset |
| `calibOffset_FT` | 0.0 | FT calibration offset |

## Troubleshooting

### No Data / No Response to READ
- Check baud rate (115200)
- Verify USB connection
- Check Arduino power LED
- Re-upload firmware

### "NaN" or Missing Readings
- Thermocouple not connected
- Wrong CS pin wiring
- Module not powered
- Check thermocouple polarity (red = negative for K-type)

### Noisy/Jumping Readings
- Add 0.1µF capacitor across thermocouple input
- Keep thermocouple wires away from power cables
- Use shielded cable
- Ensure good grounding

### Upload Fails
Firmware sending data blocks bootloader:
1. Start upload command
2. Immediately press Arduino RESET button
3. Bootloader has ~2 second window

Or upload `blank.ino` first.

## Safety

- K-type thermocouples rated to 700°C (well above coffee roasting temps)
- Keep electronics away from heat
- Use heat-resistant probe sheathing
- Ensure probes are food-safe (stainless steel)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2024-12-30 | 3-channel support, MAX31855, TC4 protocol |
| 1.0 | 2024-11-10 | Initial 2-channel analog version |

## Resources

- [MAX31855 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31855.pdf)
- [Adafruit MAX31855 Library](https://github.com/adafruit/Adafruit_MAX31855)
- [Artisan TC4 Protocol](https://artisan-scope.org/devices/arduino/)
- [K-type Thermocouple Guide](https://learn.adafruit.com/thermocouples)
