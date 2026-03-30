# Project Resume

## Right Now
**Phase:** Development — KiCad Schematic Capture (ESP32 Custom PCB)
**Last (28-30 Mar 2026):** Scaffolded new KiCad 10 project from scratch. Archived old Nano schematic to `kicad/archive/v1-nano/`. Set up JLCPCB-compatible design rules (0.2mm clearance, 0.15mm min trace, 0.3mm min drill), Power/Default net classes, A3 schematic page, project-local symbol/footprint libraries. Validated KiCad built-in symbols against datasheets for: ESP32-WROOM-32E (pin-for-pin match, footprint override 32D→32E required), MAX31855KASA (pin-for-pin match), BSS138 (GSD pinout confirmed). Placed U1 (ESP32), U2+U3 (MAX31855), Q1+Q2 (BSS138) with BOM fields. Discovered DigiKey order placed via Fairfield project — screw terminals ordered as ED2600-ND (5.08mm, OSTTC020162) not Phoenix Contact 277-1247-ND. BSS138 NOT in DigiKey order — sourcing from Mantech (35M3468, R1.20 each). LCD connector ordered as JST PH 4-pin (455-1706-ND) not 2.54mm pin header.
**Previous (23 Mar 2026):** Display decision — LCD replaces OLED. BSS138 level shifters added to plan. PCB strategy: breakout board first.
**Next:** Continue schematic capture — place remaining symbols (screw terminals, LCD connector, passives, tactile switch, NCP1117 LDO, MMBT2222A auto-reset). Wire up the schematic. Run ERC.
**Blocked:** BSS138 not ordered yet — add to Mantech order (35M3468 × 4-6)

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- **REDESIGN in progress**: ESP32-WROOM-32E + genuine MAX31855KASA+ on custom PCB
- **DigiKey cart nearly complete** — need screw terminals + BSS138 level shifters added
- **0805 for all passives** — confirmed, matches Fairfield order. Not 0603.
- **Display**: Keyestudio 20×4 I2C LCD (MD0074, HD44780 + PCF8574 backpack, `LiquidCrystal_I2C` library) — replaces OLED
- **Custom PCB uses bare ESP32-WROOM-32E-N4** module — needs full support circuitry (LDO, auto-reset, etc.), all covered by Fairfield order components
- **PCB strategy**: MAX31855 breakout board first, then full system PCB
- RPi 4 accessible via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Connect RPi 4 to network~~ ✓ SSH at 10.0.10.102
2. ~~Create KiCad schematic~~ ✓ (needs redesign for ESP32)
3. ~~Design OLED bezel~~ ✓ (needs redesign for 2.42" Adafruit OLED)
4. ~~Create wiring documentation~~ ✓ (needs update for ESP32)
5. ~~Update firmware for 2-channel~~ ✓ Done (but for Nano — needs ESP32 port)
6. ~~First power-up test~~ ✓ Firmware works, OLED works (garbled), MAX31855 knockoff smoked
7. ~~Update BOM for ESP32 redesign~~ ✓ v2.0 with specific part numbers, DigiKey checklist
8. Add screw terminals + BSS138 to DigiKey cart and place order
9. Buy Mantech order — KS5019 ESP32 dev board + MD0074 LCD (R486.07 incl. VAT)
10. Design MAX31855 breakout board in KiCad (validate thermocouples with dev board)
11. Design full system PCB — bare ESP32 + 2× MAX31855 + LCD header + button + BSS138 level shifters
12. Order PCBs from JLCPCB
13. Hand-assemble PCBs (SOIC-8 MAX31855, 0805 passives, headers)
14. Port firmware to ESP32 (pin reassignment, ESP32 Arduino core, LiquidCrystal_I2C library)
15. Clone repo to RPi properly
16. Calibrate thermocouples (ice water + boiling water)
17. Mount probes in roaster (BT + ET positions)
18. First test roast with Artisan

## Key Files
- `docs/BOM.md` - Bill of Materials v2.0 (updated 20 Mar — ESP32 redesign, specific part numbers)
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` - Production firmware (Nano version — needs ESP32 port)
- `kicad/milk-depot-coffee-roaster.kicad_sch` - New ESP32 schematic (in progress, symbols placed)
- `kicad/milk-depot-coffee-roaster.kicad_pro` - Project settings with JLCPCB design rules
- `kicad/milk-depot-coffee-roaster.kicad_pcb` - Empty PCB with 2-layer setup
- `kicad/archive/v1-nano/` - Archived old Arduino Nano schematic
- `kicad/datasheets/` - Downloaded component datasheets (ESP32, MAX31855, BSS138)
- `docs/WIRING.md` - Wiring guide (needs update for ESP32)

## DigiKey Order Status
**Unified order placed** via Fairfield project: `fairfield-water/docs/planning/internal/FD-PROC-010-digikey-unified-order.csv`
Roaster-specific items in that order: ESP32-WROOM-32E-N4 (×12 shared), MAX31855KASA+ (×8), 10nF caps (×10), NCP1117 3.3V LDO (×10 shared), MMBT2222A (×20 shared), 1µF caps (×10 shared), JST PH 4-pin header (×10), screw terminals OSTTC020162/ED2600-ND (×10, 5.08mm pitch).
**NOT in DigiKey order:** BSS138 — order from Mantech instead.

### Mantech Order (pending)
| Item | Stock Code | Price (ex-VAT) |
|------|-----------|------:|
| KS5019 ESP32-WROOM-32 USB-C 38-pin | ME106299 | R238.20 |
| MD0074 Keyestudio 20×4 I2C LCD | 15M8244 | R184.47 |
| BSS138 N-MOSFET SOT-23 (×4-6) | 35M3468 | R1.20 ea |
| **Subtotal (4× BSS138)** | | **R427.47** |
| **VAT (15%)** | | **R64.12** |
| **Total** | | **R491.59** |
