# Milk Depot Coffee Roaster

A custom coffee roasting temperature monitoring system using Artisan roasting software on Raspberry Pi 4, with Arduino-based 3-channel thermocouple interface.

**GitHub Repository**: [Milk-Depot-Coffee-Roaster](https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster)

## Overview

This project integrates:
- **Artisan Coffee Roasting Software** - Profile creation, logging, and roast control
- **Arduino UNO R3** - 3-channel thermocouple interface via MAX31855 amplifiers
- **Raspberry Pi 4** - Running Artisan and communicating with Arduino via USB serial
- **3x K-Type Thermocouples** - Bean, Exhaust, and Flame temperature monitoring

## Temperature Channels

| Channel | Name | Description | Artisan Mapping |
|---------|------|-------------|-----------------|
| 1 | ET | Exhaust/Environment Temperature | Primary ET |
| 2 | BT | Bean Temperature | Primary BT |
| 3 | FT | Flame/Burner Temperature | Extra (ArduinoTC4_34) |

## Hardware

### Components

| Qty | Component | Description |
|-----|-----------|-------------|
| 1 | Raspberry Pi 4 | Running Raspberry Pi OS (Debian Trixie) + Artisan |
| 1 | Arduino UNO R3 | Thermocouple interface controller |
| 3 | Olimex TC-K-TYPE-1.5M | K-type thermocouples, -50°C to 700°C, 1.5m lead |
| 3 | MAX31855 Module | K-type thermocouple amplifier, SPI interface |
| 1 | SSD1306 OLED | 128x64 I2C display for local readout (optional) |
| 1 | ABS Enclosure | ~150x100x50mm project box |

### Connections

- Arduino connects to Raspberry Pi via USB (appears as `/dev/ttyACM0`)
- Thermocouples connect to MAX31855 modules via miniature K-type connectors
- MAX31855 modules connect to Arduino via SPI bus (shared SCK/MISO, individual CS)
- Optional OLED connects via I2C (A4/A5)

See [WIRING.md](WIRING.md) for detailed wiring diagrams.

## Software Stack

### Raspberry Pi
- **OS**: Raspberry Pi OS (Debian GNU/Linux 13 - Trixie)
- **Python**: 3.13.5
- **Artisan**: v3.4.0+ (installed via .deb package)

### Arduino
- **Platform**: Arduino UNO R3
- **Firmware**: TC4 emulator with 3-channel MAX31855 support
- **Baud Rate**: 115200
- **Libraries**: Adafruit MAX31855, Adafruit SSD1306 (optional)

## Project Structure

```
Milk-Depot-Coffee-Roaster/
├── README.md                 # This file
├── CLAUDE.md                 # AI assistant instructions
├── BOM.md                    # Bill of Materials
├── WIRING.md                 # Wiring diagrams
├── ARTISAN_INTEGRATION.md    # Artisan configuration guide
├── SERIAL_PROTOCOL.md        # Serial communication details
├── arduino-firmware/         # Arduino sketches
│   ├── tc4_emulator/         # Production firmware (TC4 protocol)
│   ├── temp_monitor/         # Continuous output firmware
│   ├── serial_test/          # Testing sketch
│   └── blank/                # Empty sketch for easy uploads
├── scripts/                  # Helper scripts
│   ├── compile.sh            # Compile Arduino firmware
│   ├── upload.sh             # Upload to Arduino
│   ├── detect.sh             # Detect connected boards
│   └── monitor.sh            # Monitor serial output
├── bin/                      # Local binaries
│   └── arduino-cli           # Arduino CLI v1.3.1
├── parts-specs/              # Component research & datasheets
└── *.py                      # Python utility scripts
```

## Quick Start

### 1. Hardware Setup

1. Wire the 3x MAX31855 modules to Arduino (see [WIRING.md](WIRING.md))
2. Connect thermocouples to MAX31855 module sockets
3. Connect Arduino to Raspberry Pi via USB

### 2. Firmware Upload

```bash
# Enable MAX31855 in firmware (uncomment library includes)
nano arduino-firmware/tc4_emulator/tc4_emulator.ino

# Compile
./scripts/compile.sh arduino-firmware/tc4_emulator

# Upload (press RESET if needed)
./scripts/upload.sh arduino-firmware/tc4_emulator
```

### 3. Configure Artisan

1. Launch Artisan: `artisan`
2. Config → Device:
   - Device: **ArduinoTC4**
   - Port: `/dev/ttyACM0`
   - Baud: **115200**
3. Config → Device → Extra Devices:
   - Add **ArduinoTC4_34** for Flame Temperature on channel 3
4. Click **ON** to start monitoring

See [ARTISAN_INTEGRATION.md](ARTISAN_INTEGRATION.md) for detailed setup.

## Serial Protocol

The Arduino uses TC4 protocol for Artisan compatibility:

**Command/Response:**
```
Artisan sends:  READ
Arduino sends:  25.00,180.50,195.20,350.00,0.00
                 │     │      │      │      └── Chan4 (unused)
                 │     │      │      └── Chan3 (FT - Flame)
                 │     │      └── Chan2 (BT - Bean)
                 │     └── Chan1 (ET - Exhaust)
                 └── Ambient temp
```

## Calibration

After hardware assembly:

1. Place all probes in ice water bath
2. Note readings for each channel
3. Update `calibOffset_XX` values in firmware:
   ```cpp
   float calibOffset_ET = 0.0 - reading_ET;
   float calibOffset_BT = 0.0 - reading_BT;
   float calibOffset_FT = 0.0 - reading_FT;
   ```
4. Verify with boiling water (100°C at sea level)
5. Recompile and upload

## Development

### Prerequisites

- Arduino CLI (included in `bin/`)
- Python 3.x with pyserial
- Adafruit MAX31855 library (install via Arduino IDE)

### Common Commands

```bash
# Compile firmware
./scripts/compile.sh arduino-firmware/tc4_emulator

# Upload firmware
./scripts/upload.sh arduino-firmware/tc4_emulator

# Monitor serial output
./scripts/monitor.sh

# Detect Arduino boards
./scripts/detect.sh
```

### Testing Without Hardware

The firmware includes simulation mode using analog noise from floating pins. This allows testing Artisan integration before thermocouples are connected.

## Troubleshooting

### Arduino Not Detected

```bash
# Check if device is connected
ls -la /dev/ttyACM* /dev/ttyUSB*

# Check permissions (user should be in dialout group)
groups

# Check dmesg for USB events
dmesg | tail -20
```

### Upload Fails

When firmware is continuously sending data, it can block the bootloader. Solutions:

1. Press Arduino RESET button immediately after starting upload
2. Or first upload the `blank.ino` sketch

### Temperature Readings Erratic

- Check thermocouple polarity (red = negative for K-type)
- Verify SPI wiring (SCK, MISO, CS connections)
- Check for loose connections at MAX31855 socket
- Ensure proper grounding

### Artisan Not Receiving Data

1. Verify correct port: `ls /dev/ttyACM*`
2. Check baud rate matches (115200)
3. Test with: `python3 test_serial.py`
4. Check Artisan Messages window (Help → Messages)

## Resources

### Documentation
- [Artisan Official Docs](https://artisan-scope.org/docs/)
- [Artisan Arduino/TC4 Setup](https://artisan-scope.org/devices/arduino/)
- [MAX31855 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31855.pdf)

### Community
- [Home Roasters Forum](https://homeroasters.org)
- [Artisan User Group](https://groups.google.com/g/artisan-roasterscope)

## Status

- [x] Git repository initialized
- [x] Artisan v3.4.0 installed
- [x] Arduino firmware for 3-channel TC4 protocol
- [x] Helper scripts created
- [x] Documentation complete
- [ ] MAX31855 modules purchased
- [ ] K-type thermocouples purchased (Olimex TC-K-TYPE-1.5M)
- [ ] Hardware assembly
- [ ] Sensor calibration
- [ ] First test roast

## License

- Artisan is licensed under GPL-3.0
- This project: MIT License

## Author

Jason (jason@precept.co.za)

---

**Last Updated**: 2024-12-30
