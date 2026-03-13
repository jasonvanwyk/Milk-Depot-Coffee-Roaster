# Project Resume

## Right Now
**Phase:** Development — Hardware Assembly & Integration
**Last (13 Mar 2026):** Connected RPi via SSH, created KiCad schematic for actual components (Arduino Nano, 2x MAX31855, OLED, 2x 100nF caps), designed OLED snap-fit bezel in OpenSCAD, installed WireViz.
**Next:** Test/render OLED bezel, create WireViz wiring diagram, clone repo to RPi, hardware assembly
**Blocked:** None

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- All hardware components on hand — ready to build
- **Updated design**: Arduino Nano (not UNO), 2x MAX31855 (BT + ET only, no FT), 1.3" OLED display
- Firmware needs updating for Nano + 2-channel config
- RPi 4 accessible via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Connect RPi 4 to network~~ ✓ SSH at 10.0.10.102
2. ~~Create KiCad schematic~~ ✓ `kicad/milk-depot-coffee-roaster.kicad_sch`
3. ~~Design OLED bezel~~ ✓ Draft in `3d-prints/oled-bezel.scad`
4. Test/render OLED bezel in OpenSCAD or FreeCAD
5. Create WireViz wiring diagram YAML
6. Clone repo to RPi properly
7. Update firmware for Arduino Nano (board type + 2-channel)
8. Hardware assembly — wire on veroboard (50×70mm)
9. Enable MAX31855 hardware code in firmware
10. Calibrate thermocouples (ice water + boiling water)
11. Mount probes in roaster (BT + ET positions)
12. First test roast with Artisan

## Key Files
- `kicad/generate_schematic.py` - Programmatic KiCad schematic generator
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic
- `3d-prints/oled-bezel.scad` - OpenSCAD snap-fit OLED bezel design
- `docs/WIRING.md` - Wiring diagrams (needs update for 2-channel Nano)
- `docs/BOM.md` - Bill of Materials (all procured)
- `arduino-firmware/tc4_emulator/` - Production firmware (needs Nano + 2-channel update)
- `docs/ARTISAN_INTEGRATION.md` - Artisan configuration guide

## Session Notes
- **KiCad symbol gotcha**: `extends` keyword doesn't work in embedded `lib_symbols` within .kicad_sch files — use the parent symbol directly
- **Capacitor codes**: 101 = 100pF (wrong for decoupling), 104 = 100nF (correct)
- **Thermocouple selection**: 35mm/2.5mm for BT, 50mm/3.0mm for ET
- **Power**: USB from RPi sufficient (~48mA total draw), no barrel jack needed
- **WireViz**: Installed v0.4.1, generates diagrams from YAML
- **OLED bezel**: Based on Thingiverse thing:4680559, custom snap-fit front panel mount only
