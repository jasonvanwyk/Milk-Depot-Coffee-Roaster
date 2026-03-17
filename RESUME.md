# Project Resume

## Right Now
**Phase:** Development — Hardware Assembly & Integration
**Last (17 Mar 2026):** Created complete wiring documentation suite: WireViz YAML diagram (`docs/wiring.yml` → PNG/SVG/HTML), rewrote `docs/WIRING.md` for 2-channel Nano design with veroboard layout, built Fritzing breadboard layout with all components wired and verified. Downloaded Adafruit Fritzing parts for MAX31855 and 1.3" OLED. Exported FreeCAD bezel front piece to STL. Confirmed OLED module accepts 5V (has onboard voltage regulator).
**Previous (16 Mar 2026):** Designed OLED back piece in FreeCAD. Pivoted from custom snap hooks to Printables mounting frame. Test print sent to Bambu X1 in PETG-CF.
**Next:** Evaluate OLED test print fit, clone repo to RPi, update firmware for Nano (2-channel), hardware assembly on veroboard
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
5. ~~FreeCAD back piece~~ ✓ Frame with corner bosses + 3.2mm holes
6. ~~Create wiring documentation~~ ✓ WireViz + Fritzing + WIRING.md rewrite
7. OLED mounting solution — evaluate test print fit
8. Clone repo to RPi properly
9. Update firmware for Arduino Nano (board type + 2-channel)
10. Hardware assembly — wire on veroboard (50×70mm)
11. Enable MAX31855 hardware code in firmware
12. Calibrate thermocouples (ice water + boiling water)
13. Mount probes in roaster (BT + ET positions)
14. First test roast with Artisan

## Key Files
- `FreeCad/oled-1.3inch-holder-bezel.FCStd` - FreeCAD OLED bezel (front piece, exported to STL)
- `FreeCad/oled-1.3inch-holder2.FCStd` - FreeCAD OLED back piece (frame + bosses + holes)
- `docs/wiring.yml` - WireViz YAML source (generates PNG/SVG/HTML)
- `docs/wiring.png` - WireViz harness-style wiring diagram
- `docs/WIRING.md` - Complete wiring & assembly guide (updated for 2-channel Nano)
- `fritzing/parts/` - Adafruit MAX31855 + OLED 1.3" Fritzing parts (.fzpz)
- `fritzing/milk-depot-coffee-roaster.fzz` - Fritzing breadboard layout (user saves)
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic
- `3d-prints/display-testpanel.stl` - Printables OLED test panel (fit check)
- `3d-prints/displayframe-oled-1_3inch-sh1106.stl` - Printables OLED mounting frame
- `docs/BOM.md` - Bill of Materials (all procured)
- `arduino-firmware/tc4_emulator/` - Production firmware (needs Nano + 2-channel update)

## Session Notes
- **OLED accepts 5V**: Back of PCB shows onboard voltage regulator (SOT-23 package). Safe to power from Nano 5V pin.
- **OLED pin mapping**: Physical pins VDD/GND/SCK/SDA → Nano 5V/GND/A5(SCL)/A4(SDA). "SCK" on OLED = I2C clock.
- **Fritzing parts**: Adafruit MAX31855 (#269) and OLED 1.3" (#938) from GitHub. Arduino Nano 3.0 in core library. Import .fzpz via File → Open.
- **Tactile switch planned**: 6×6mm DIP 4-pin, connect to D2 + GND (internal pull-up), for paging OLED display screens. Not yet in wiring docs.
- **6×6mm tactile switch pinout**: Pairs connected across top/bottom (1-2 always connected, 3-4 always connected). Use multimeter to verify which pair.
- **Fritzing workflow**: Breadboard view is primary. Schematic/PCB auto-generate from connections. Click a pin to highlight all connected pins for verification.
