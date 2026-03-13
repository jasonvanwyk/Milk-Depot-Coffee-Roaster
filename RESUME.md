# Project Resume

## Right Now
**Phase:** Development — Hardware Assembly & Integration
**Last (13 Mar 2026):** All components procured. Email review confirmed invoice paid, thermocouples delivered. Installed KiCad MCP servers + skills.
**Next:** Connect RPi to network, hardware assembly, review firmware/software on RPi, calibration
**Blocked:** RPi not on network yet — firmware/software review happens directly on device

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- All hardware components on hand — ready to build
- Software complete and tested (TC4 firmware, Artisan integration)
- Firmware currently in simulation mode — needs MAX31855 code enabled

## Development Plan
1. Connect RPi 4 to network (currently offline)
2. Hardware assembly — wire MAX31855 modules, mount in enclosure (`docs/WIRING.md`)
3. Review and update firmware/software directly on RPi
4. Enable MAX31855 hardware code in `tc4_emulator` firmware
5. Calibrate thermocouples (ice water + boiling water)
6. Mount probes in roaster (BT, ET, FT positions)
7. First test roast with Artisan

## Key Files
- `docs/WIRING.md` - Wiring diagrams and enclosure layout
- `docs/BOM.md` - Bill of Materials (all procured)
- `arduino-firmware/tc4_emulator/` - Production firmware (needs MAX31855 enablement)
- `docs/ARTISAN_INTEGRATION.md` - Artisan configuration guide
