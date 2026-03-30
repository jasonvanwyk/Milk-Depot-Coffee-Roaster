# Project Resume

## Right Now
**Phase:** Development — KiCad Schematic Capture (ESP32 Custom PCB)
**Last (30 Mar 2026):** Full procurement audit — read ALL invoices across 5 suppliers (3× DigiKey, 3× Mantech, Communica, DIY Electronics, Micro Robotics). Discovered DigiKey #122017091 (first Fairfield order) was fully returned via credit memo. DigiKey #122880837 is the real unified order (37 line items) containing ALL roaster parts: NCP1117ST33T3G (SOT-223), MMBT2222A, 10nF/1µF/100nF/10µF 0805 caps, tactile switches (TL3342), JST PH 4-pin, screw terminals (OSTTC020162), ESP32, MAX31855. Built complete component grid with verified MPNs, manufacturers, supplier PNs. Downloaded all datasheets to `kicad/datasheets/`. Verified KiCad footprints against datasheets — TL3342 tactile switch needs custom footprint (4.80×2.80mm pad pattern, no built-in match). Screw terminal decision: using Degson DG127-5.08-02P (Mantech 15M0713) — footprint compatible with Phoenix 5.08mm. Started placing components with BOM fields (R1-R6, C1 in progress).
**Previous (28-30 Mar 2026):** Scaffolded KiCad 10 project, placed U1/U2/U3/Q1/Q2 with BOM fields.
**Next:** Finish placing remaining schematic symbols (C2-C9, U4, Q3-Q4, J1-J4, SW1). Create custom TL3342 footprint. Wire up schematic with net labels. Run ERC.
**Blocked:** BSS138 on order from Mantech (35M3468) — not yet delivered

## Quick Context
- Client: Quenton (Milk Depot) - coffee roaster temperature monitoring system
- **REDESIGN in progress**: ESP32-WROOM-32E + genuine MAX31855KASA+ on custom PCB
- **DigiKey orders SHIPPED** — all roaster parts received (invoice #122880837 + #123184654)
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
- `kicad/datasheets/` - All component datasheets (ESP32, MAX31855, BSS138, NCP1117, MMBT2222A, TL3342, OSTTC020162, DG127, B4B-PH-K-S, caps)
- `docs/WIRING.md` - Wiring guide (needs update for ESP32)

## DigiKey Orders — SHIPPED & RECEIVED
- **#122880837** (23 Mar) — unified order, 37 items. ALL roaster passives (0805), NCP1117, MMBT2222A, TL3342, JST PH, screw terminals, ESP32 ×3, MAX31855 ×3
- **#123184654** (27 Mar) — IC top-up: MAX31855 ×6, ESP32 ×10 (shared w/ Fairfield)
- **#122017091** (6 Mar) — FULLY RETURNED via credit memo 122017091-1 (18 Mar). Was 0603 prototype order.

### Mantech Orders — RECEIVED
- **#178252** (23 Mar) — MD0074 LCD ×1, JST PH crimp parts, solder paste, flux pen
- **#210781** (23 Mar) — battery holders (Fairfield)
- **#210901** (27 Mar) — DG127 screw terminals ×15, JST PH headers ×80, pin header strips ×15

### Other Suppliers — RECEIVED
- **Communica** (24 Mar) — CZM5-2E terminal blocks ×10, cable glands, PoE splitters
- **Micro Robotics** (23 Mar) — JST PH 4-pin ×2, crimp tool, pin headers, antennas
- **DIY Electronics** (23 Mar) — tools and wire only

### Still Outstanding
- **BSS138** — on order from Mantech (35M3468, R1.20 ea)
