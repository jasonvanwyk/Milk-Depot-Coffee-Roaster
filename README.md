# Coffee Roasting System

A custom coffee roasting system using Artisan roasting software on Raspberry Pi 4, with Arduino-based temperature monitoring.

**GitHub Repository**: [Milk-Depot-Coffee-Roaster](https://github.com/jasonvanwyk/Milk-Depot-Coffee-Roaster)

## Overview

This project integrates:
- **Artisan Coffee Roasting Software** - Profile creation, logging, and roast control
- **Arduino R3** - Temperature probe interface (bean temp + drum temp)
- **Raspberry Pi 4** - Running Artisan and communicating with Arduino via serial

## Hardware

### Components
- Raspberry Pi 4 running Raspberry Pi OS (Debian Trixie)
- Arduino UNO R3
- 2x Temperature probes (connected to Arduino)
  - Bean temperature probe
  - Drum temperature probe
- USB cable for Arduino → Raspberry Pi serial communication

### Connections
- Arduino connects to Raspberry Pi via USB (appears as `/dev/ttyACM0` or `/dev/ttyUSB0`)
- Temperature probes connect to Arduino analog/digital pins (documented in firmware)

## Software Stack

### Raspberry Pi
- **OS**: Raspberry Pi OS (Debian GNU/Linux 13 - Trixie)
- **Python**: 3.13.5
- **Artisan**: v3.4.0+ (installed via .deb package)

### Arduino
- **Platform**: Arduino UNO R3
- **Firmware**: Custom temperature monitoring (see `arduino-firmware/`)
- **Baud Rate**: 115200

## Project Structure

```
/home/jason/artisan/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── arduino-firmware/        # Custom Arduino temperature monitoring code
│   ├── temp_monitor/        # Main Arduino sketch
│   └── README.md           # Firmware documentation
├── artisan-source/          # Artisan source code (for reference/modifications)
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

- [x] Git repository initialized
- [x] Directory structure created
- [x] Artisan v3.4.0 installed
- [x] Arduino firmware written and uploaded
- [x] Serial communication tested ✅ **WORKING PERFECTLY**
- [x] Arduino CLI configured
- [x] Helper scripts created
- [ ] Temperature sensors connected (MAX31855 modules needed)
- [ ] Sensor calibration
- [ ] First successful roast

### Latest Test Results (2025-11-10)

**Serial Communication**: ✅ Working flawlessly at 115200 baud
```
BT:63.0,DT:63.0
BT:62.8,DT:62.6
BT:66.2,DT:66.0
```

**Arduino Status**: ✅ Fully functional (UNO R3 at /dev/ttyACM0)
**Current Readings**: ~63-66°C (floating analog pins - no sensors connected yet)
**Next Step**: Connect MAX31855 thermocouple modules

See `CURRENT_STATUS.md` for detailed system status.

---

**Last Updated**: 2025-11-10
