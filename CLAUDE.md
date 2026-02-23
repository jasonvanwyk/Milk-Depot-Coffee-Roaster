# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a coffee roasting control system integrating:
- **Arduino UNO R3**: Custom firmware for reading three temperature probes via MAX31855 modules
- **Raspberry Pi 4**: Running Artisan coffee roasting software
- **Serial Communication**: Arduino sends temperature data to Pi at 115200 baud using TC4 protocol

**Temperature Channels:**
- **ET (Channel 1)**: Exhaust/Environment Temperature - air leaving the drum
- **BT (Channel 2)**: Bean Temperature - probe in the bean mass
- **FT (Channel 3)**: Flame Temperature - near the burner

**Key Concept**: The Arduino reads 3 K-type thermocouples via MAX31855 SPI amplifiers. Artisan sends `READ` commands, Arduino responds with comma-separated temperatures. Artisan displays real-time temperature curves and calculates rate-of-rise.

## Development Environment

- **Target Platform**: Raspberry Pi 4, Raspberry Pi OS (Debian Trixie)
- **Python**: 3.13.5 with pyserial installed
- **Arduino CLI**: v1.3.1 installed locally in `bin/arduino-cli`
- **Arduino Core**: arduino:avr@1.8.6 for Arduino UNO R3
- **Arduino Libraries**: Adafruit MAX31855, Adafruit SSD1306 (optional)
- **Artisan**: v3.4.0 installed system-wide at `/usr/bin/artisan`

**Note**: The repo may be cloned to different paths on different machines. All scripts use relative paths from the project root.

## Common Arduino Commands

All commands should be run from the project root:

### Compile Arduino Firmware
```bash
./scripts/compile.sh [sketch_path]
# Default: arduino-firmware/tc4_emulator (production firmware)
# Example: ./scripts/compile.sh arduino-firmware/temp_monitor
```

### Upload to Arduino
```bash
./scripts/upload.sh [sketch_path] [port]
# Default sketch: arduino-firmware/tc4_emulator
# Default port: /dev/ttyACM0
# Note: If firmware is continuously sending data, press RESET button immediately after starting upload
```

### Detect Connected Arduino
```bash
./scripts/detect.sh
# Shows Arduino boards and serial devices
```

### Monitor Serial Output
```bash
./scripts/monitor.sh
# Runs test_serial.py at 115200 baud

# Or read at specific baud rate:
python3 read_arduino.py [baudrate]
```

### Manual Arduino CLI Usage
```bash
export PATH="$(pwd)/bin:$PATH"
arduino-cli compile --fqbn arduino:avr:uno <sketch_dir>
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno <sketch_dir>
arduino-cli board list
```

## Hardware Architecture

### Pin Assignments

| Arduino Pin | Function | Connected To |
|-------------|----------|--------------|
| D13 | SPI SCK | All MAX31855 SCK (shared) |
| D12 | SPI MISO | All MAX31855 DO (shared) |
| D10 | CS_ET | MAX31855 #1 (Exhaust Temp) |
| D9 | CS_BT | MAX31855 #2 (Bean Temp) |
| D8 | CS_FT | MAX31855 #3 (Flame Temp) |
| A4 | I2C SDA | OLED Display (optional) |
| A5 | I2C SCL | OLED Display (optional) |
| 5V | Power | All modules VCC |
| GND | Ground | All modules GND |

### SPI Bus Configuration

All three MAX31855 modules share the SPI bus (SCK, MISO) but have individual Chip Select (CS) lines. The Adafruit library uses software SPI, allowing flexible pin assignment.

## Serial Communication Protocol

### TC4 Protocol (Production - tc4_emulator)

**Command/Response format for Artisan ArduinoTC4 device:**

```
Artisan sends:  READ
Arduino sends:  25.00,180.50,195.20,350.00,0.00\n
                 │     │      │      │      └── Channel 4 (unused)
                 │     │      │      └── Channel 3 (FT - Flame)
                 │     │      └── Channel 2 (BT - Bean)
                 │     └── Channel 1 (ET - Exhaust)
                 └── Ambient temperature
```

**Other supported commands:** `CHAN`, `UNITS`, `FILT`, `OT1`, `OT2`, `PID`

### Continuous Output (temp_monitor)

```
ET:xxx.x,BT:xxx.x,FT:xxx.x\n
```

## Architecture

### Arduino Firmware (`arduino-firmware/`)

| Sketch | Purpose | Baud | Protocol |
|--------|---------|------|----------|
| `tc4_emulator/` | Production firmware, TC4 protocol | 115200 | Command/response |
| `temp_monitor/` | Continuous output mode | 115200 | `ET:xx.x,BT:xx.x,FT:xx.x` |
| `serial_test/` | Simple test output | 9600 | Basic serial |
| `blank/` | Empty sketch for easy uploads | - | None |

**tc4_emulator**: Responds to Artisan TC4 commands. Reads 3x MAX31855 via SPI. Output: `ambient,chan1,chan2,chan3,chan4`. Use with Artisan ArduinoTC4 + ArduinoTC4_34 (extra device).

**temp_monitor**: Continuous output every 1000ms. Reads 3x MAX31855. Use with Artisan External Program device type.

### Python Tools
- `test_serial.py`: Production serial reader with 2-second init delay, displays 20 lines
- `read_arduino.py`: Flexible reader accepting baud rate as argument
- `artisan_read.py`: External Program script for Artisan (outputs `ET,BT` format)
- `test_output.py`: Simulates data output for testing Artisan without Arduino

### Helper Scripts (`scripts/`)
All scripts use `SCRIPT_DIR` to locate project root and `arduino-cli` in `bin/`:
- Set PATH to include `$PROJECT_DIR/bin`
- Default FQBN: `arduino:avr:uno`
- Scripts handle success/failure with clear messages

### Project Structure

```
├── CLAUDE.md                 # AI assistant instructions (this file)
├── README.md                 # Project overview
├── RESUME.md                 # Quick session resume context
├── STATUS.md                 # Project status and task tracking
├── assets/                   # Precept branding and company details
├── correspondence/           # Supplier/client correspondence
├── docs/                     # Technical documentation
│   ├── BOM.md                # Bill of Materials
│   ├── WIRING.md             # Wiring diagrams
│   ├── ARTISAN_INTEGRATION.md # Artisan configuration guide
│   ├── SERIAL_PROTOCOL.md    # Serial communication details
│   ├── ARDUINO_CLI.md        # Arduino CLI workflow
│   ├── THERMOCOUPLE_SPEC.md  # Thermocouple technical spec
│   ├── CUSTOM_TC_ORDER_SPEC.md # Custom order spec for GPA Trading
│   ├── SHOPPING_LIST.md      # Printable shopping list
│   └── parts-specs/          # Component research (DigiKey CSV exports)
├── arduino-firmware/         # Arduino sketches
├── scripts/                  # Helper scripts
├── bin/                      # Local binaries (arduino-cli)
├── pics/                     # Photos and screenshots
└── *.py                      # Python utility scripts
```

### Documentation Files (`docs/`)
- `BOM.md`: Complete Bill of Materials with pricing
- `WIRING.md`: Detailed wiring diagrams and enclosure layout
- `ARTISAN_INTEGRATION.md`: Artisan configuration guide
- `SERIAL_PROTOCOL.md`: Serial communication protocol details
- `ARDUINO_CLI.md`: Arduino CLI workflow guide
- `THERMOCOUPLE_SPEC.md`: Thermocouple technical specification
- `CUSTOM_TC_ORDER_SPEC.md`: Custom order spec sent to GPA Trading
- `SHOPPING_LIST.md`: Printable shopping list with SA suppliers

## Artisan Integration

**Launch**: `artisan` (system-wide installation)

**Configuration for 3-Channel Setup:**

1. **Primary Device (ArduinoTC4)**:
   - Config → Device → ArduinoTC4
   - Port: `/dev/ttyACM0`, Baud: `115200`
   - This provides ET (Chan1) and BT (Chan2)

2. **Extra Device for Flame Temp**:
   - Config → Device → Extra Devices tab
   - Add: **ArduinoTC4_34**
   - This provides FT (Chan3) as extra curve

3. **Channel Labels**:
   - Config → Curves → rename extra channel to "FT" or "Flame"

## Important Caveats

### Upload Blocking Issue
When firmware is continuously sending data, it blocks the bootloader from syncing during upload. **Solution**: Press the Arduino RESET button immediately after starting the upload command. The bootloader runs for ~2 seconds after reset.

Alternatively, upload the `blank.ino` sketch first.

### Enabling MAX31855 Hardware

The firmware ships in simulation mode (reads analog noise). To enable real thermocouples:

1. Install Adafruit MAX31855 library via Arduino IDE Library Manager
2. In `tc4_emulator.ino`:
   - Uncomment `#include <Adafruit_MAX31855.h>`
   - Uncomment thermocouple object declarations
   - In each `readTemperature_XX()` function, uncomment library code and remove simulation code
3. Recompile and upload

### Thermocouple Polarity

K-type thermocouples have polarity. The red wire is **negative** (opposite of typical conventions). Reversing polarity causes readings to go negative as temperature increases.

### Temperature Readings Without Sensors

When MAX31855 modules have no thermocouple connected, they report NaN. The firmware returns the last good reading on error to prevent Artisan graph glitches.

## Hardware Sourcing

The `docs/parts-specs/` directory contains component research (CSV exports from DigiKey ZA). See `docs/BOM.md` for complete parts list with pricing.

**Key Components:**
- 6x Custom K-type thermocouple probes (ordered from GPA Trading, PO P00041)
- 3x MAX31855 modules (to be procured)
- SSD1306 OLED display (optional)
- ABS enclosure ~150x100x50mm

## Calibration Procedure

1. Place all probes in ice water bath (0°C)
2. Note the reading for each channel
3. Set calibration offsets in firmware:
   ```cpp
   float calibOffset_ET = 0.0 - reading;  // e.g., -2.3 if it reads 2.3°C
   float calibOffset_BT = 0.0 - reading;
   float calibOffset_FT = 0.0 - reading;
   ```
4. Recompile and upload
5. Verify with boiling water (100°C at sea level, ~96°C at Johannesburg altitude)

## Git Workflow

**Remote**: `git@github.com:jasonvanwyk/Milk-Depot-Coffee-Roaster.git`
**Branch**: `master`

All commits include the footer:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Git is configured with:
- user.name: "jason"
- user.email: "jason@precept.co.za"

SSH authentication is set up with ED25519 key.

## Testing Data Flow

To verify the complete pipeline:

1. **Test Arduino Output**:
   ```bash
   python3 test_serial.py
   ```
   Should show temperature readings (simulated or real)

2. **Test TC4 Protocol**:
   ```bash
   # In one terminal, start serial monitor
   screen /dev/ttyACM0 115200
   # Type: READ
   # Should get: 25.00,xx.xx,xx.xx,xx.xx,0.00
   ```

3. **Test with Artisan**:
   - Launch Artisan
   - Configure ArduinoTC4 device
   - Add ArduinoTC4_34 extra device
   - Click ON button
   - Should see 3 temperature curves

## Next Steps

1. Follow up on GPA Trading thermocouple delivery (PO P00041)
2. Procure remaining components (see `docs/BOM.md` and `docs/SHOPPING_LIST.md`)
3. Assemble electronics in enclosure (see `docs/WIRING.md`)
4. Enable MAX31855 code in firmware
5. Calibrate thermocouples
6. Install probes in roaster
7. First test roast
