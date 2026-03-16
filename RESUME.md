# Project Resume

## Right Now
**Phase:** Development — Hardware Assembly & Integration
**Last (16 Mar 2026):** Designed OLED back piece in FreeCAD (frame with corner bosses + 3.2mm fastener holes). Pivoted from custom snap hooks to downloaded mounting frame from Printables (werner_rh). Test print of display-testpanel.stl sent to Bambu X1 in PETG-CF.
**Next:** Evaluate test print fit, decide between custom FreeCAD design or Printables frame, complete OLED mounting solution, create WireViz wiring diagram, clone repo to RPi, hardware assembly
**Blocked:** None — waiting on test print result

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
5. ~~FreeCAD back piece~~ ✓ Frame with corner bosses + 3.2mm holes (WIP)
6. OLED mounting solution — test print Printables frame OR finish custom design
6. Create WireViz wiring diagram YAML
7. Clone repo to RPi properly
8. Update firmware for Arduino Nano (board type + 2-channel)
9. Hardware assembly — wire on veroboard (50×70mm)
10. Enable MAX31855 hardware code in firmware
11. Calibrate thermocouples (ice water + boiling water)
12. Mount probes in roaster (BT + ET positions)
13. First test roast with Artisan

## Key Files
- `FreeCad/oled-1.3inch-holder-bezel.FCStd` - FreeCAD OLED bezel (front piece)
- `FreeCad/oled-1.3inch-holder2.FCStd` - FreeCAD OLED back piece (frame + bosses + holes)
- `FreeCad/draw_bezel.py` - FreeCAD console script for PCB outline rectangle
- `3d-prints/display-testpanel.stl` - Printables OLED test panel (fit check)
- `3d-prints/displayframe-oled-1_3inch-sh1106.stl` - Printables OLED mounting frame
- `3d-prints/display-washer.stl` - Printables OLED washer (2.2mm)
- `3d-prints/oled-bezel.scad` - OpenSCAD bezel (superseded by FreeCAD version)
- `3d-prints/oled-bezel.stl` - Exported STL from OpenSCAD render
- `kicad/generate_schematic.py` - Programmatic KiCad schematic generator
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic
- `docs/WIRING.md` - Wiring diagrams (needs update for 2-channel Nano)
- `docs/BOM.md` - Bill of Materials (all procured)
- `arduino-firmware/tc4_emulator/` - Production firmware (needs Nano + 2-channel update)

## Session Notes
- **OLED mounting holes NOT symmetric**: TL (-15.25, 13.80), TR (15.25, 13.80), BL (-15.25, -14.70), BR (15.25, -14.70) — X is symmetric, Y values differ
- **FreeCAD back piece**: Outer 45.5×43.5mm frame, inner 35.5×33.6mm cutout, 4 corner bosses with 3.2mm through-holes for push-in fastener posts
- **Snap hooks abandoned**: Drawing cantilever profiles on side faces in FreeCAD Part Design was too complex for manual GUI work. Pivoted to downloaded mounting frame.
- **Printables frame** (werner_rh, model 1338552): Press-fits into 36×26mm panel cutout, M3 screw mounting, designed for SH1106 1.3" OLED. Test print sent in PETG-CF.
- **PETG-CF print settings**: 245°C nozzle, 70°C bed, 0.2mm layers, 20% infill, supports on build plate, outer brim 5mm, polyholes ON
- **FreeCAD bezel state**: Bezel front piece complete in `oled-1.3inch-holder-bezel.FCStd` (exported to STL + 3MF)
