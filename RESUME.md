# Project Resume

## Right Now
**Phase:** Development — Hardware Assembly & Integration
**Last (13 Mar 2026):** Rendered OpenSCAD bezel (STL + PNG previews). Redesigned OLED bezel from scratch in FreeCAD with real caliper measurements. Completed: PCB outline sketch (35.5×33.6mm + 4 mounting holes for Essentra 27PIF0045B push-in fasteners), bezel face (41.5×39.6mm), 1.6mm pad, window cutout (35×19mm positioned from actual screen measurements).
**Next:** Complete FreeCAD bezel (pocket window, PCB shelf walls, snap tabs), create WireViz wiring diagram, clone repo to RPi, hardware assembly
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
3. ~~Design OLED bezel~~ ✓ OpenSCAD draft → FreeCAD redesign
4. ~~Render/test OLED bezel~~ ✓ OpenSCAD STL + PNG renders
5. Complete FreeCAD bezel — pocket window, PCB shelf walls, snap tabs
6. Create WireViz wiring diagram YAML
7. Clone repo to RPi properly
8. Update firmware for Arduino Nano (board type + 2-channel)
9. Hardware assembly — wire on veroboard (50×70mm)
10. Enable MAX31855 hardware code in firmware
11. Calibrate thermocouples (ice water + boiling water)
12. Mount probes in roaster (BT + ET positions)
13. First test roast with Artisan

## Key Files
- `FreeCad/oled-1.3inch-holder.FCStd` - FreeCAD OLED bezel (active design, WIP)
- `FreeCad/draw_bezel.py` - FreeCAD console script for PCB outline rectangle
- `3d-prints/oled-bezel.scad` - OpenSCAD bezel (superseded by FreeCAD version)
- `3d-prints/oled-bezel.stl` - Exported STL from OpenSCAD render
- `kicad/generate_schematic.py` - Programmatic KiCad schematic generator
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic
- `docs/WIRING.md` - Wiring diagrams (needs update for 2-channel Nano)
- `docs/BOM.md` - Bill of Materials (all procured)
- `arduino-firmware/tc4_emulator/` - Production firmware (needs Nano + 2-channel update)

## Session Notes
- **OLED actual measurements** (caliper-verified): screen 35×19.5mm, 6mm from PCB top, 8mm from PCB bottom. Screen center ~1mm above PCB center — datasheet offset was wrong.
- **FreeCAD bezel state**: PCB outline sketch → bezel face sketch → Pad 1.6mm → window sketch (35×19mm at BL -17.5, -8.45). Pocket not yet applied. Still needs: PCB shelf walls, snap tabs.
- **FreeCAD Sketcher tip**: Use Constrain Lock (K, L) for positioning — more reliable than scripted DistanceX/Y constraints
- **Push-in fasteners**: Essentra 27PIF0045B for OLED PCB mounting, 3mm holes
- **3D printing**: Recommend Tough PLA Black (A1 slot), modified Strong preset, print face-down for snap-tab strength
- **OLED bezel**: Based on Thingiverse thing:4680559, snap-fit front panel mount only
