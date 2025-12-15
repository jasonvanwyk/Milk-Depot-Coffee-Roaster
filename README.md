# Coffee Roasting System

A custom coffee roasting temperature monitoring system using Artisan roasting software on Raspberry Pi 4, with Arduino Nano-based temperature monitoring and local OLED display.

**GitHub Repository**: [Milk-Depot-Coffee-Roaster](https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster)

## Overview

This project integrates:
- **Artisan Coffee Roasting Software** - Profile creation, logging, and roast control on Raspberry Pi
- **Arduino Nano** - Temperature probe interface with local OLED display
- **K-type Thermocouples** - High-temperature probes (rated 500°C+) for bean and exhaust temps
- **1.3" OLED Display** - Local temperature display with push-button screen cycling
- **Raspberry Pi 4** - Running Artisan and communicating with Arduino via USB serial

## Hardware

### Components

| Component | Model/Spec | Purpose |
|-----------|------------|---------|
| Raspberry Pi 4 | 4GB RAM, Raspberry Pi OS (Trixie) | Runs Artisan software |
| Arduino Nano | ATmega328P, CH340 USB | Temperature reading & display |
| MAX31855 Module x2 | K-type, SPI interface | Thermocouple amplifiers |
| K-type Thermocouple x2 | 500°C+ rated, 3mm probe | Bean & exhaust temperature |
| 1.3" OLED Display | 128x64, SH1106, I2C | Local temperature display |
| Push Button | 6x6mm tactile | Cycle display screens |
| Project Enclosure | ABS plastic box | House Arduino & display |

### Display Screens (Button Cycling)
1. **Startup Screen** - "MILK DEPOT Coffee Roaster"
2. **Runtime Screen** - Shows elapsed roast time (HH:MM:SS)
3. **Temperature Screen** - Bean temp & exhaust temp readings

### Connections
- Arduino Nano connects to Raspberry Pi via USB (power + serial data)
- MAX31855 modules connect via SPI (shared CLK/MISO, separate CS pins)
- OLED connects via I2C (A4=SDA, A5=SCL)
- Push button connects to D2 (interrupt pin) with internal pullup

See `HARDWARE.md` for detailed wiring diagrams and pin assignments.

## Software Stack

### Raspberry Pi
- **OS**: Raspberry Pi OS (Debian GNU/Linux 13 - Trixie)
- **Python**: 3.13.5
- **Artisan**: v3.4.0+ (installed via .deb package)

### Arduino
- **Platform**: Arduino Nano (ATmega328P)
- **Firmware**: Custom temperature monitoring with OLED display (see `arduino-firmware/`)
- **Baud Rate**: 115200
- **Libraries**: Adafruit_MAX31855, U8g2lib (OLED)

## Project Structure

```
Milk-Depot-Coffee-Roaster/
├── README.md                 # This file
├── HARDWARE.md              # Detailed wiring and component guide
├── CLAUDE.md                # Development instructions for Claude Code
├── .gitignore               # Git ignore rules
├── arduino-firmware/        # Arduino firmware
│   ├── temp_monitor/        # Main sketch with OLED display
│   ├── tc4_emulator/        # TC4 protocol emulator for Artisan
│   ├── blank/               # Utility sketch (stops serial output)
│   └── README.md            # Firmware documentation
├── hardware/                # Hardware design files
│   ├── coffee-roaster.kicad_sch  # KiCAD schematic
│   ├── coffee-roaster.kicad_pcb  # KiCAD PCB layout (optional)
│   ├── enclosure.FCStd      # FreeCAD enclosure design
│   └── simulation/          # ngspice circuit simulations
├── scripts/                 # Helper scripts
│   ├── compile.sh           # Compile Arduino firmware
│   ├── upload.sh            # Upload to Arduino
│   ├── detect.sh            # Detect connected Arduino
│   └── monitor.sh           # Monitor serial output
├── bin/                     # Local tools
│   └── arduino-cli          # Arduino CLI v1.3.1
└── roast-profiles/          # (Future) Saved roast profiles
```

## Serial Communication Protocol

### Arduino → Artisan
The Arduino sends temperature data over serial at 115200 baud.

**Data Format**:
```
BT:205.3,DT:187.2\n
```
- `BT` = Bean Temperature (°C)
- `DT` = Drum Temperature (°C)
- Data sent every 1000ms (1 Hz)

### Configuration in Artisan
1. Open Artisan
2. Go to **Config** → **Device Assignment**
3. Select device type: **External Program** (or custom configuration)
4. Set serial port: `/dev/ttyACM0` (or appropriate device)
5. Set baud rate: **115200**
6. Configure data parsing for custom format

## Installation

### 1. Install Artisan

Download and install the latest Artisan .deb package:
```bash
cd ~/Downloads
wget https://github.com/artisan-roaster-scope/artisan/releases/download/v3.4.0/artisan-linux-3.4.0_raspbian-bookworm.deb
sudo dpkg -i artisan-linux-3.4.0_raspbian-bookworm.deb
sudo apt-get install -f  # Install any missing dependencies
```

### 2. Upload Arduino Firmware

1. Open Arduino IDE on your development machine
2. Load `arduino-firmware/temp_monitor/temp_monitor.ino`
3. Connect Arduino UNO R3 via USB
4. Select **Tools** → **Board** → **Arduino UNO**
5. Select correct serial port
6. Click **Upload**

### 3. Connect Hardware

1. Connect Arduino to Raspberry Pi via USB
2. Verify device appears:
   ```bash
   ls -la /dev/ttyACM*
   ```
3. User `jason` is already in `dialout` group (serial permissions configured)

### 4. Configure Artisan

1. Launch Artisan: `artisan` (or from Applications menu)
2. Configure device settings (see "Serial Communication Protocol" above)
3. Click **ON** to start monitoring temperatures
4. Test with room temperature before roasting

## Usage

### Starting a Roast Session

1. Power on the roaster hardware
2. Launch Artisan on Raspberry Pi
3. Load or create a roast profile
4. Connect to Arduino (click **ON** button)
5. Verify temperature readings are updating
6. Begin roasting and follow the profile

### Creating Roast Profiles

1. Open Artisan
2. Go to **Roast** → **Designer**
3. Design temperature curve
4. Save profile for future use

### Recording Roast Logs

- Artisan automatically logs temperature data during roasting
- Logs are saved with timestamps
- Analyze past roasts in **Roast** → **Analyzer**

## Development

### Arduino Firmware

The custom Arduino firmware is located in `arduino-firmware/`.

To modify:
1. Edit the sketch in Arduino IDE
2. Test thoroughly with serial monitor
3. Upload to Arduino
4. Verify communication with Artisan
5. Commit changes to git

### Artisan Source Code

The full Artisan source code is cloned in `artisan-source/` for reference and potential custom modifications.

## Troubleshooting

### Arduino Not Detected

```bash
# Check if device is connected
ls -la /dev/ttyACM* /dev/ttyUSB*

# Check permissions
groups  # Should include 'dialout'

# Monitor serial output
sudo apt-get install screen
screen /dev/ttyACM0 115200
```

### Temperature Readings Not Updating

1. Verify Arduino firmware is uploaded correctly
2. Check serial port and baud rate in Artisan config
3. Open Arduino IDE Serial Monitor to verify data output
4. Check physical connections to temperature probes

### Artisan Won't Start

```bash
# Check installation
which artisan
artisan --version

# Check logs
journalctl -xe
```

## Resources

### Documentation
- [Artisan Official Docs](https://artisan-scope.org/docs/)
- [Artisan GitHub](https://github.com/artisan-roaster-scope/artisan)
- [Arduino Reference](https://www.arduino.cc/reference/en/)

### Community
- [Home Roasters Forum](https://homeroasters.org)
- [Artisan User Group](https://groups.google.com/g/artisan-roasterscope)

## Version Control

This project uses Git for version control and is hosted on GitHub.

**Repository**: `git@github.com:jasonvanwyk/Milk-Depot-Coffee-Roaster.git`

### Clone Repository
```bash
git clone git@github.com:jasonvanwyk/Milk-Depot-Coffee-Roaster.git
cd Milk-Depot-Coffee-Roaster
```

### What's Tracked
- Arduino firmware in `arduino-firmware/`
- Artisan source modifications in `artisan-source/`
- Project documentation
- Configuration files
- Roast profiles can be added to version control (currently gitignored)

### Git Configuration
```bash
git config user.name "jason"
git config user.email "jason@precept.co.za"
```

## License

- Artisan is licensed under GPL-3.0
- Custom Arduino firmware in this repository: [Specify your license]

## Author

Jason (jason@precept.co.za)

## Status

### Completed
- [x] Git repository initialized
- [x] Directory structure created
- [x] Artisan v3.4.0 installed
- [x] Basic Arduino firmware written and tested
- [x] Serial communication tested (working at 115200 baud)
- [x] Arduino CLI configured
- [x] Helper scripts created

### In Progress
- [ ] Hardware design (KiCAD schematic)
- [ ] Component ordering (Arduino Nano, MAX31855, OLED, thermocouples)
- [ ] Updated firmware with OLED display support

### Pending (After Parts Arrive)
- [ ] Assemble hardware
- [ ] Temperature sensor calibration
- [ ] Enclosure assembly
- [ ] First successful roast

### Hardware Shopping List (~$22-28)

| Component | Est. Price | Source |
|-----------|------------|--------|
| Arduino Nano V3 Clone | ~$2-3 | AliExpress |
| MAX31855 Module x2 | ~$8 | AliExpress |
| K-type Thermocouple x2 (500°C+) | ~$6 | AliExpress |
| 1.3" OLED Display (SH1106) | ~$3-4 | AliExpress |
| Push Button + Enclosure | ~$4 | AliExpress |

See plan file for detailed component links and specifications.

---

**Last Updated**: 2025-12-15
