# Project Resume

## Right Now
**Phase:** Development — Hardware Redesign (ESP32 + Custom PCB)
**Last (18-19 Mar 2026):** Major pivot session. Updated firmware for Arduino Nano 2-channel, installed arduino-cli AVR core + libraries (Adafruit MAX31855, SH110X, GFX) on Arch workstation. Flashed firmware via Arduino IDE (CLI had port issues — FTDI chip, stty left port in bad state). Firmware working: TC4 protocol responding, OLED displaying (garbled top line — SH1106 init issue, partially fixed). One MAX31855 knockoff module smoked on first power-up (BT channel, near decoupling cap). Decision: **rebuild with quality components** — ESP32-WROOM-32E replaces Arduino Nano, genuine MAX31855KASA+ ICs on custom PCB replaces knockoff modules, 2.42" OLED replaces 1.3". Sourced components from DigiKey ZA + Mantech. Decided to keep coffee roaster PCB separate from Fairfield project PCB.
**Previous (17 Mar 2026):** Created complete wiring documentation suite: WireViz, Fritzing, WIRING.md rewrite.
**Next:** Finalise DigiKey order (MAX31855KASA+ × 5 + passives), buy ESP32 KS5019 from Mantech, design custom coffee roaster PCB in KiCad, update firmware for ESP32
**Blocked:** Waiting on component orders (DigiKey + Mantech)

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- **REDESIGN in progress**: Switching from Arduino Nano + knockoff modules to ESP32 + genuine parts + custom PCB
- **New platform**: ESP32-WROOM-32E (3.3V native, WiFi, more RAM)
- **MAX31855 knockoff smoked** — one BT module released smoke near cap on first power-up. Don't trust cheap MAX31855 modules.
- **Custom PCB**: MAX31855KASA+ (SOIC-8) directly on PCB, no breakout boards needed. ESP32 is 3.3V so no level shifters required.
- DigiKey order pending — combining with Fairfield project order for free shipping (R2,000 threshold)
- RPi 4 accessible via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Connect RPi 4 to network~~ ✓ SSH at 10.0.10.102
2. ~~Create KiCad schematic~~ ✓ (needs redesign for ESP32)
3. ~~Design OLED bezel~~ ✓ (needs redesign for 2.42" OLED)
4. ~~Create wiring documentation~~ ✓ (needs update for ESP32)
5. ~~Update firmware for 2-channel~~ ✓ Done (but for Nano — needs ESP32 port)
6. ~~First power-up test~~ ✓ Firmware works, OLED works (garbled), MAX31855 knockoff smoked
7. Order components — DigiKey (MAX31855KASA+ ICs, caps, screw terminals) + Mantech (ESP32 KS5019)
8. Design custom PCB in KiCad — ESP32 + 2× MAX31855 + OLED header + button
9. Order PCBs from JLCPCB
10. Hand-assemble PCBs (SOIC-8 MAX31855, passives, headers)
11. Port firmware to ESP32 (pin reassignment, ESP32 Arduino core)
12. Clone repo to RPi properly
13. Calibrate thermocouples (ice water + boiling water)
14. Mount probes in roaster (BT + ET positions)
15. First test roast with Artisan

## Key Files
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` - Production firmware (updated: 2-channel, SH1106 OLED, MAX31855 hardware enabled, DIAG command)
- `kicad/milk-depot-coffee-roaster.kicad_sch` - Circuit schematic (needs ESP32 redesign)
- `docs/BOM.md` - Bill of Materials (needs update for new components)
- `docs/WIRING.md` - Wiring guide (needs update for ESP32)

## Component Orders (Pending)
### DigiKey ZA
- MAX31855KASA+-ND × 5 (2 per board × 2 boards + 1 spare)
- 10nF ceramic caps × 5 (thermocouple input filter)
- 2-pin screw terminals × 5 (thermocouple connections)
- (Plus Fairfield project components to hit R2,000 free shipping)

### Mantech
- KS5019 ESP32-WROOM-32 USB-C 38-pin — R238.20 ex-VAT (stock code ME106299)
