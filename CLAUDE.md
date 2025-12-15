# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a coffee roasting control system integrating:
- **Arduino Nano**: Custom firmware for reading two K-type thermocouples via MAX31855 modules
- **1.3" OLED Display**: Local temperature display with button-cycled screens
- **Raspberry Pi 4**: Running Artisan coffee roasting software
- **Serial Communication**: Arduino sends temperature data to Pi at 115200 baud

**Key Concept**: The Arduino reads K-type thermocouples (rated 500°C+) via MAX31855 SPI modules, displays temperatures locally on an OLED screen, and transmits formatted data (`BT:xx.x,DT:xx.x`) over USB serial to Artisan on the Raspberry Pi.

## Development Environment

- **Platform**: Raspberry Pi 4, Raspberry Pi OS (Debian Trixie)
- **Python**: 3.13.5 with pyserial installed
- **Arduino CLI**: v1.3.1 installed locally in `bin/arduino-cli`
- **Arduino Core**: arduino:avr@1.8.6 for Arduino Nano (ATmega328P)
- **Arduino IDE**: v1.8.19 also available for GUI development
- **Artisan**: v3.4.0 installed system-wide at `/usr/bin/artisan`
- **KiCAD**: Available for schematic/PCB design (install with `sudo apt install kicad`)
- **ngspice**: Available for circuit simulation
- **FreeCAD**: Available for 3D enclosure design

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

### Arduino Nano Pin Assignments

```
SPI (Thermocouples):
  D13 (SCK)  → MAX31855 CLK (both, shared)
  D12 (MISO) → MAX31855 DO (both, shared)
  D10        → MAX31855 #1 CS (Bean Temp)
  D9         → MAX31855 #2 CS (Exhaust Temp)

I2C (OLED Display):
  A4 (SDA)   → OLED SDA
  A5 (SCL)   → OLED SCL

Button:
  D2 (INT0)  → Push button (with internal pullup)

Power:
  5V         → MAX31855 VCC (both), OLED VCC
  GND        → All grounds
  USB        → Raspberry Pi (power + serial data)
```

### Arduino Firmware (`arduino-firmware/temp_monitor/`)
- **Temperature Reading**: MAX31855 modules via SPI (Bean on CS D10, Exhaust on CS D9)
- **OLED Display**: 1.3" 128x64 SH1106 via I2C (address 0x3C)
- **Button**: D2 with interrupt, cycles through 3 display screens
- **Serial Output**: Prints `BT:xxx.x,DT:xxx.x` at 115200 baud, 1 Hz
- **Libraries**: Adafruit_MAX31855, U8g2lib (or Adafruit_SH1106)

### Display Screens (Button Cycling)
1. **Startup**: "MILK DEPOT Coffee Roaster"
2. **Runtime**: Elapsed time in HH:MM:SS format
3. **Temperature**: Bean and Exhaust temps in large font

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
- `HARDWARE.md`: Detailed wiring diagrams, component specs, assembly guide
- `ARDUINO_CLI.md`: Comprehensive Arduino CLI guide, troubleshooting
- `SERIAL_PROTOCOL.md`: Detailed serial communication specification
- `ARTISAN_INTEGRATION.md`: How to connect Arduino data to Artisan
- `CURRENT_STATUS.md`: Latest system status and test results
- `arduino-firmware/README.md`: Firmware documentation
- `hardware/coffee-roaster.kicad_sch`: KiCAD schematic
- `hardware/simulation/thermocouple.cir`: ngspice circuit simulation

## Testing Data Flow

To verify the complete pipeline:
1. **Test Arduino Output**: `python3 test_serial.py` should show `BT:xx.x,DT:xx.x` lines
2. **Test Pi Output**: `python3 test_output.py` outputs "output from pi #N" every 2s
3. **Test with Artisan**: Launch Artisan, configure device, click ON button to see curves

Current readings (no sensors): BT and DT both around 63-71°C from floating analog pins.

## Next Hardware Integration

### Components to Order (~$22-28 from AliExpress)
- Arduino Nano V3 Clone (ATmega328P, CH340)
- MAX31855 K-type Thermocouple Module x2
- K-type Thermocouple Probes (500°C+ rated) x2
- 1.3" OLED Display (SH1106, I2C)
- Tactile Push Button 6x6mm
- Project Enclosure

### When Parts Arrive
1. Wire components per `HARDWARE.md` diagram
2. Install Arduino libraries: `Adafruit_MAX31855`, `U8g2lib`
3. Update firmware to use MAX31855 SPI reading
4. Add OLED display code and button handling
5. Test temperature accuracy with ice water (0°C) and boiling water (100°C)
6. Calibrate if needed using offset/scale factors
7. Assemble into enclosure
