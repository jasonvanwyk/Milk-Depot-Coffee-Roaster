# Milk Depot Coffee Roaster - Precept Systems Project

## Client Information

| Field | Details |
|-------|---------|
| **Client Name** | Quenton (Milk Depot) |
| **Contact** | Via Jason van Wyk |
| **Project** | Coffee Roaster Temperature Monitoring System |

## Project Overview

Custom coffee roasting temperature monitoring system integrating Arduino-based 3-channel thermocouple interface with Artisan roasting software on Raspberry Pi 4. The system reads Bean Temperature (BT), Exhaust Temperature (ET), and Flame Temperature (FT) via MAX31855 amplifiers and displays real-time temperature curves with rate-of-rise calculations.

## Project Scope

1. **Arduino Firmware** - TC4 protocol emulator for 3-channel MAX31855 thermocouple reading
2. **Hardware Integration** - 3x custom K-type thermocouple probes with compression fittings, MAX31855 amplifiers, enclosure
3. **Software Configuration** - Artisan v3.4.0 setup on Raspberry Pi 4 with ArduinoTC4 device
4. **Calibration & Testing** - Probe calibration and first test roast

## Current Status

**See `STATUS.md` for detailed task tracking and current project status.**

### Quick Status
- **Phase:** Hardware Procurement
- **Software:** Complete and tested (firmware + Artisan)
- **Hardware:** Thermocouples on order from GPA Trading (PO P00041)

### Milestones
- [x] Git repository initialized
- [x] Artisan v3.4.0 installed on Raspberry Pi
- [x] Arduino TC4 firmware written and tested
- [x] Helper scripts created (compile, upload, detect, monitor)
- [x] Documentation complete
- [x] Custom thermocouple probes ordered (GPA Trading)
- [ ] Thermocouple probes delivered
- [ ] MAX31855 modules + remaining components procured
- [ ] Hardware assembly in enclosure
- [ ] Sensor calibration
- [ ] First test roast

## Hardware Summary

| Component | Status |
|-----------|--------|
| Raspberry Pi 4 | Owned, Artisan installed |
| Arduino UNO R3 | Owned, firmware tested |
| 3x Custom K-Type Probes | On order (GPA Trading, PO P00041) |
| 3x MAX31855 Modules | To be procured |
| ABS Enclosure | To be procured |
| SSD1306 OLED (optional) | To be procured |

## Temperature Channels

| Channel | Name | Description | Artisan Mapping |
|---------|------|-------------|-----------------|
| 1 | ET | Exhaust/Environment Temperature | Primary ET |
| 2 | BT | Bean Temperature | Primary BT |
| 3 | FT | Flame/Burner Temperature | Extra (ArduinoTC4_34) |

## Key Files

| File | Purpose |
|------|---------|
| `STATUS.md` | **Current project status and task tracking** |
| `RESUME.md` | Quick session resume context |
| `CLAUDE.md` | AI assistant project context |
| `correspondence/` | All client/supplier correspondence |
| `docs/` | Technical documentation and planning |
| `arduino-firmware/` | Arduino sketches (TC4 emulator, temp monitor, etc.) |
| `scripts/` | Helper scripts (compile, upload, detect, monitor) |

## Documentation

All technical documentation is in `docs/`:

| Document | Description |
|----------|-------------|
| [BOM.md](docs/BOM.md) | Bill of Materials with pricing |
| [WIRING.md](docs/WIRING.md) | Wiring diagrams and enclosure layout |
| [ARTISAN_INTEGRATION.md](docs/ARTISAN_INTEGRATION.md) | Artisan configuration guide |
| [SERIAL_PROTOCOL.md](docs/SERIAL_PROTOCOL.md) | TC4 serial communication protocol |
| [ARDUINO_CLI.md](docs/ARDUINO_CLI.md) | Arduino CLI workflow guide |
| [THERMOCOUPLE_SPEC.md](docs/THERMOCOUPLE_SPEC.md) | Thermocouple technical specification |
| [CUSTOM_TC_ORDER_SPEC.md](docs/CUSTOM_TC_ORDER_SPEC.md) | Custom order spec sent to GPA Trading |
| [SHOPPING_LIST.md](docs/SHOPPING_LIST.md) | Printable shopping list with suppliers |

## Quick Start

```bash
# Compile firmware
./scripts/compile.sh arduino-firmware/tc4_emulator

# Upload to Arduino (press RESET if needed)
./scripts/upload.sh arduino-firmware/tc4_emulator

# Monitor serial output
./scripts/monitor.sh

# Detect Arduino boards
./scripts/detect.sh
```

## Workflow Notes

1. Always update `STATUS.md` when tasks are completed or status changes
2. Correspondence goes in `correspondence/` folder with date prefix
3. Technical documents go in `docs/` folder
4. Use git commits with descriptive messages

## License

- Artisan is licensed under GPL-3.0
- This project: MIT License

## Author

Jason van Wyk (jason@precept.co.za) - Precept Systems (Pty) Ltd
