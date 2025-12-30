# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a coffee roasting control system integrating:
- **Arduino UNO R3**: Custom firmware for reading two temperature probes
- **Raspberry Pi 4**: Running Artisan coffee roasting software
- **Serial Communication**: Arduino sends temperature data to Pi at 115200 baud

**Key Concept**: The Arduino continuously reads analog temperature sensors and transmits formatted data (`BT:xx.x,DT:xx.x`) over USB serial, which Artisan software uses to display real-time temperature curves and control the roast.

## Development Environment

- **Target Platform**: Raspberry Pi 4, Raspberry Pi OS (Debian Trixie)
- **Python**: 3.13.5 with pyserial installed
- **Arduino CLI**: v1.3.1 installed locally in `bin/arduino-cli`
- **Arduino Core**: arduino:avr@1.8.6 for Arduino UNO R3
- **Arduino IDE**: v1.8.19 also available for GUI development
- **Artisan**: v3.4.0 installed system-wide at `/usr/bin/artisan`

**Note**: The repo may be cloned to different paths on different machines (e.g., `/home/jason/artisan/` on the Pi dev server, or elsewhere on desktop). All scripts use relative paths from the project root.

## Common Arduino Commands

All commands should be run from the project root:

### Compile Arduino Firmware
```bash
./scripts/compile.sh [sketch_path]
# Default: arduino-firmware/temp_monitor
# Example: ./scripts/compile.sh arduino-firmware/serial_test
```

### Upload to Arduino
```bash
./scripts/upload.sh [sketch_path] [port]
# Default sketch: arduino-firmware/temp_monitor
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
# Example: python3 read_arduino.py 9600
```

### Manual Arduino CLI Usage
```bash
export PATH="$(pwd)/bin:$PATH"
arduino-cli compile --fqbn arduino:avr:uno <sketch_dir>
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno <sketch_dir>
arduino-cli board list
```

## Serial Communication Protocol

**Critical Format**: Arduino sends temperature data as:
```
BT:xxx.x,DT:xxx.x\n
```

- `BT`: Bean Temperature (°C, 1 decimal place)
- `DT`: Drum Temperature (°C, 1 decimal place)
- **Baud Rate**: 115200 (for temp_monitor), 9600 (for test sketches)
- **Update Interval**: 1000ms (1 Hz)
- **Device Path**: `/dev/ttyACM0` or `/dev/ttyUSB0`
- Lines starting with `#` are comments/headers

User `jason` is already in the `dialout` group, so no permission changes needed for serial access.

## Architecture

### Arduino Firmware (`arduino-firmware/`)

| Sketch | Purpose | Baud | Protocol |
|--------|---------|------|----------|
| `temp_monitor/` | Main firmware, continuous output | 115200 | `BT:xx.x,DT:xx.x` |
| `tc4_emulator/` | TC4 protocol emulator for ArduinoTC4 device | 115200 | Command/response (READ → temps) |
| `serial_test/` | Simple test output | 9600 | Basic serial |
| `blank/` | Empty sketch for easy uploads | - | None |

**temp_monitor**: Reads analog pins A0 (BT) and A1 (DT) every 1000ms, outputs `BT:xx.x,DT:xx.x`. Has placeholders for MAX31855 thermocouple modules.

**tc4_emulator**: Responds to Artisan's TC4 commands (`READ`, `CHAN`, `UNITS`, etc.). Use with Artisan's ArduinoTC4 device type. Outputs: `ambient,chan1,chan2,chan3,chan4`.

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

## Artisan Integration

**Launch**: `artisan` (system-wide installation)

**Configuration Approaches** (in order of preference):

1. **ArduinoTC4** (requires `tc4_emulator` firmware):
   - Config → Device → ArduinoTC4
   - Port: `/dev/ttyACM0`, Baud: `115200`
   - Best integration - uses native Artisan protocol

2. **External Program** (works with `temp_monitor` firmware):
   - Config → Device → External Program
   - Command: `python3 /path/to/project/artisan_read.py`
   - Script parses `BT:xx.x,DT:xx.x` and outputs `ET,BT`

3. **Direct Serial**: Config → Device → Fuji PXR → Port `/dev/ttyACM0`, Baud `115200`

## Important Caveats

### Upload Blocking Issue
When `temp_monitor` firmware is running and continuously sending data, it blocks the bootloader from syncing during upload. **Solution**: Press the Arduino RESET button immediately after starting the upload command. The bootloader runs for ~2 seconds after reset, providing a window for upload to succeed.

Alternatively, upload the `blank.ino` sketch first (which sends no data) to make subsequent uploads easier.

### Temperature Readings Without Sensors
Analog pins A0/A1 are "floating" when no sensors are connected, picking up electrical noise. This produces readings typically in the 60-70°C range. This is normal and expected. Real temperature readings require connecting MAX31855 thermocouple amplifier modules.

### Artisan Source Code
The `artisan-source/` directory contains Artisan v3.4.0 source code cloned for reference. This is NOT used to run Artisan (the system-wide .deb installation is used). It's included for understanding Artisan's serial protocols and potential custom modifications.

## Git Workflow

**Remote**: `git@github.com:jasonvanwyk/Milk-Depot-Coffee-Roaster.git`
**Branch**: `master`

All commits include the footer:
```
Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

Git is configured with:
- user.name: "jason"
- user.email: "jason@precept.co.za"

SSH authentication is set up with ED25519 key.

## Testing Data Flow

To verify the complete pipeline:
1. **Test Arduino Output**: `python3 test_serial.py` should show `BT:xx.x,DT:xx.x` lines
2. **Test with Artisan**: Launch Artisan, configure device, click ON button to see curves

Current readings (no sensors): BT and DT around 63-71°C from floating analog pins.

## Next Hardware Integration

When MAX31855 thermocouple modules arrive:
1. Uncomment library includes in `temp_monitor.ino` (lines 34-36)
2. Update `readBeanTemperature()` and `readDrumTemperature()` to use `readCelsius()`
3. Define SPI pins for MAX31855 modules
4. Recompile and upload
5. Calibrate with ice water (0°C) and boiling water (100°C)
