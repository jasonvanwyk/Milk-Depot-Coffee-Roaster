# Project Resume

## Right Now
**Phase:** Development — Hardware Redesign (ESP32 + Custom PCB)
**Last (23 Mar 2026):** Display decision — switched from OLED to 20×4 I2C LCD (Keyestudio MD0074 from Mantech, R184.47 ex-VAT). HD44780 + PCF8574 backpack — zero driver headaches, no burn-in, better readability near roaster. Library: `LiquidCrystal_I2C`. Removed Adafruit OLED from DigiKey cart. Added BSS138 level shifters (BSS138CT-ND × 4) for 3.3V↔5V I2C on custom PCB. Started KiCad PCB discussion — decided MAX31855 breakout board first (validate thermocouples before full system PCB).
**Previous (20 Mar 2026):** BOM v2.0 rewrite, DigiKey cart cross-reference, OLED selection (now superseded by LCD).
**Next:** Add screw terminals (277-1247-ND × 6) + BSS138 (BSS138CT-ND × 4) to DigiKey cart, place order. Buy Mantech order (ESP32 KS5019 + LCD MD0074). Design MAX31855 breakout board in KiCad.
**Blocked:** Waiting on component orders (DigiKey + Mantech)

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
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic (needs ESP32 redesign)
- `docs/WIRING.md` - Wiring guide (needs update for ESP32)

## DigiKey Order Status
**Cart file**: `~/Downloads/2026-03-20T095833.csv` (20 items, combined with Fairfield)
**Still need to add:**
- 277-1247-ND × 6 — 2-pin 5mm screw terminal (Phoenix Contact 1725656)
- BSS138CT-ND × 4 — BSS138 N-MOSFET (SOT-23) for I2C level shifting

**Removed:** ~~1528-1591-ND (Adafruit OLED)~~ — replaced by Mantech LCD

### Mantech Order
| Item | Stock Code | Price (ex-VAT) |
|------|-----------|------:|
| KS5019 ESP32-WROOM-32 USB-C 38-pin | ME106299 | R238.20 |
| MD0074 Keyestudio 20×4 I2C LCD | 15M8244 | R184.47 |
| **Subtotal** | | **R422.67** |
| **VAT (15%)** | | **R63.40** |
| **Total** | | **R486.07** |
