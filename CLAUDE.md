# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a coffee roasting control system integrating:
- **Arduino UNO R3**: Custom firmware for reading two temperature probes
- **Raspberry Pi 4**: Running Artisan coffee roasting software
- **Serial Communication**: Arduino sends temperature data to Pi at 115200 baud

**Key Concept**: The Arduino continuously reads analog temperature sensors and transmits formatted data (`BT:xx.x,DT:xx.x`) over USB serial, which Artisan software uses to display real-time temperature curves and control the roast.

## Development Environment

- **Platform**: Raspberry Pi 4, Raspberry Pi OS (Debian Trixie)
- **Python**: 3.13.5 with pyserial installed
- **Arduino CLI**: v1.3.1 installed locally in `bin/arduino-cli`
- **Arduino Core**: arduino:avr@1.8.6 for Arduino UNO R3
- **Arduino IDE**: v1.8.19 also available for GUI development
- **Artisan**: v3.4.0 installed system-wide at `/usr/bin/artisan`

## Common Arduino Commands

All commands should be run from `/home/jason/artisan/`:

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
export PATH="/home/jason/artisan/bin:$PATH"
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

### Arduino Firmware (`arduino-firmware/temp_monitor/`)
- **Main Loop**: Reads analog pins A0 (bean) and A1 (drum) every 1000ms
- **Conversion**: Placeholder formula `voltage * 50.0` - needs calibration with actual sensors
- **Output**: Prints formatted string to Serial at 115200 baud
- **Future Hardware**: Code has placeholders for MAX31855 thermocouple modules

### Python Tools
- `test_serial.py`: Production serial reader with 2-second init delay, displays 20 lines
- `read_arduino.py`: Flexible reader accepting baud rate as argument
- `test_output.py`: Simulates data output for testing Artisan without Arduino

### Helper Scripts (`scripts/`)
All scripts use `SCRIPT_DIR` to locate project root and `arduino-cli` in `bin/`:
- Set PATH to include `$PROJECT_DIR/bin`
- Default FQBN: `arduino:avr:uno`
- Scripts handle success/failure with clear messages

## Artisan Integration

**Launch**: `artisan` (system-wide installation)

**Configuration Approaches**:
1. **Direct Serial**: Config → Device → Fuji PXR → Port `/dev/ttyACM0`, Baud `115200`
2. **External Program**: Config → Device → External Program → `/usr/bin/python3 /home/jason/artisan/test_serial.py`

The data format `BT:xx.x,DT:xx.x` is designed to be compatible with Artisan's serial input parsing.

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

## Documentation Map

- `README.md`: Project overview and hardware/software stack
- `ARDUINO_CLI.md`: Comprehensive Arduino CLI guide, troubleshooting
- `SERIAL_PROTOCOL.md`: Detailed serial communication specification
- `ARTISAN_INTEGRATION.md`: How to connect Arduino data to Artisan
- `CURRENT_STATUS.md`: Latest system status and test results
- `arduino-firmware/README.md`: Hardware setup, wiring, calibration procedures

## Testing Data Flow

To verify the complete pipeline:
1. **Test Arduino Output**: `python3 test_serial.py` should show `BT:xx.x,DT:xx.x` lines
2. **Test Pi Output**: `python3 test_output.py` outputs "output from pi #N" every 2s
3. **Test with Artisan**: Launch Artisan, configure device, click ON button to see curves

Current readings (no sensors): BT and DT both around 63-71°C from floating analog pins.

## Next Hardware Integration

When MAX31855 thermocouple modules arrive:
1. Uncomment library includes in `temp_monitor.ino` (lines 34-36)
2. Update `readBeanTemperature()` and `readDrumTemperature()` to use `readCelsius()`
3. Define SPI pins for MAX31855 modules
4. Recompile and upload
5. Calibrate with ice water (0°C) and boiling water (100°C)
