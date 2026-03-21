# Project Resume

## Right Now
**Phase:** Development — Hardware Redesign (ESP32 + Custom PCB)
**Last (20 Mar 2026):** BOM session. Rewrote docs/BOM.md v2.0 for ESP32 redesign — specific 0805 part numbers, DigiKey order checklist, ESP32 GPIO pin assignments. Cross-referenced against actual DigiKey cart (downloaded CSV). Confirmed all 0805 passives (100nF, 10nF, 10µF caps + 10K resistors) already in Fairfield combined order. Selected Adafruit 2719 OLED (SSD1305, 2.42", DigiKey 1528-1591-ND) over Waveshare SSD1309 — premium quality, standard 2.54mm header, avoids driver confusion. Only 2 items still need adding to cart: screw terminals + OLED.
**Previous (18-19 Mar 2026):** Major pivot session — firmware tested on Nano, knockoff MAX31855 smoked, decided on ESP32 + genuine parts redesign.
**Next:** Add screw terminals (277-1247-ND × 6) + Adafruit OLED (1528-1591-ND × 1) to DigiKey cart, place order, buy Mantech KS5019 dev board, design custom PCB in KiCad for ESP32
**Blocked:** Waiting on component orders (DigiKey + Mantech)

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- **REDESIGN in progress**: ESP32-WROOM-32E + genuine MAX31855KASA+ on custom PCB
- **DigiKey cart nearly complete** — all shared components in cart, just need screw terminals + OLED added
- **0805 for all passives** — confirmed, matches Fairfield order. Not 0603.
- **OLED**: Adafruit 2719 (SSD1305 controller, uses `Adafruit_SSD1305` library, NOT SSD1306)
- **Custom PCB uses bare ESP32-WROOM-32E-N4** module — needs full support circuitry (LDO, auto-reset, etc.), all covered by Fairfield order components
- RPi 4 accessible via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Connect RPi 4 to network~~ ✓ SSH at 10.0.10.102
2. ~~Create KiCad schematic~~ ✓ (needs redesign for ESP32)
3. ~~Design OLED bezel~~ ✓ (needs redesign for 2.42" Adafruit OLED)
4. ~~Create wiring documentation~~ ✓ (needs update for ESP32)
5. ~~Update firmware for 2-channel~~ ✓ Done (but for Nano — needs ESP32 port)
6. ~~First power-up test~~ ✓ Firmware works, OLED works (garbled), MAX31855 knockoff smoked
7. ~~Update BOM for ESP32 redesign~~ ✓ v2.0 with specific part numbers, DigiKey checklist
8. Add 2 remaining items to DigiKey cart and place order
9. Buy KS5019 ESP32 dev board from Mantech (R238.20 ex-VAT)
10. Design custom PCB in KiCad — bare ESP32 + 2× MAX31855 + OLED header + button + support circuitry
11. Order PCBs from JLCPCB
12. Hand-assemble PCBs (SOIC-8 MAX31855, 0805 passives, headers)
13. Port firmware to ESP32 (pin reassignment, ESP32 Arduino core, SSD1305 library)
14. Clone repo to RPi properly
15. Calibrate thermocouples (ice water + boiling water)
16. Mount probes in roaster (BT + ET positions)
17. First test roast with Artisan

## Key Files
- `docs/BOM.md` - Bill of Materials v2.0 (updated 20 Mar — ESP32 redesign, specific part numbers)
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` - Production firmware (Nano version — needs ESP32 port)
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic (needs ESP32 redesign)
- `docs/WIRING.md` - Wiring guide (needs update for ESP32)

## DigiKey Order Status
**Cart file**: `~/Downloads/2026-03-20T095833.csv` (20 items, combined with Fairfield)
**Still need to add:**
- 277-1247-ND × 6 — 2-pin 5mm screw terminal (Phoenix Contact 1725656)
- 1528-1591-ND × 1 — Adafruit 2.42" OLED module 2719

### Mantech
- KS5019 ESP32-WROOM-32 USB-C 38-pin — R238.20 ex-VAT (stock code ME106299)
