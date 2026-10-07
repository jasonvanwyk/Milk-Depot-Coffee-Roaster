# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board schematic complete and ERC-clean; PCB layout is next. LilyGO T-Display-S3 is the controller + display.

**Last (7 Oct 2026, schematic session 2):** Finished the schematic. Jason drew, Claude checked each step by exporting the netlist with `kicad-cli` and running ERC.
- The PC shut down unexpectedly on 6 Oct; KiCad had the project open but nothing had been saved, so no work was lost (files matched the last commit).
- **Channel sheet (`channel.kicad_sch`) finished:** probe input chain per line — J101 → TVS (SMAJ5.0CA, connector side) → ferrite → 1 nF to `GND_ISO` (chip side) → MAX31855 T+/T−, plus 10 nF C102 across T+/T−. No-connect on U101 pin 8.
- **Root sheet (`tc-board-4ch.kicad_sch`) finished:** sheet pins SCK/CS/MISO on CH1–CH4 (Place Pins from Sheet), 10-pin host connector J1 (1 GND, 2 +5V, 3 +3V3, 4 SCK, 5 MISO, 6–9 CS1–CS4, 10 BTN), 5V entry caps C1/C2, SN74AHC125 (OE = CSn, A = MISOn, Y = shared MISO), U1 power + C3, button connector J2 (BTN, GND), PWR_FLAG on +5V/+3V3/GND.
- **ERC: 0 violations on all five sheets.** Only intentional unconnected pins remain (MAX31855 pin 8, isolator EN/NC pins), all flagged.
- Reverted KiCad save-noise on the superseded `kicad/breakout-max31855/` and `kicad/milk-depot-coffee-roaster.kicad_sch` files.

**Next:**
1. **Start here:** check the provisional footprints before layout: DC-DC PS10x (uses the Traco TMA footprint, confirm pin positions against the RFB-0505S datasheet), button connector J2 (2-pin JST PH), host connector J1 (plain 1×10 header until the board-to-display cable is chosen).
2. Decide the chassis network question (mounting hole, solder jumper, 1 MΩ, 10 nF 630 V) — currently left out of the schematic.
3. PCB layout: isolation slot and two ground zones per channel, TVS/ferrite at the terminal edge, then `/pcb-review-engineer`, then order from JLCPCB.
4. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

**Blocked:** Nothing. DigiKey and two AliExpress deliveries still in transit (buttons due ~28 Oct 2026); layout does not depend on them.

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets (`GND_ISO`, `+3V3_ISO`, `+5V_ISO`, `SCK_ISO`, `CS_ISO`, `MISO_ISO`) are local labels, so each channel gets its own copy.
- **How Claude checks:** export the netlist with `kicad-cli` and read the nets; never edit the schematic files once Jason is drawing. Open KiCad on a workspace with `setsid nohup kicad <project> &` then move the window by address (Hyprland uses Lua dispatch syntax here).
- **T-Display-S3:** 1.9" IPS, 6 clean spare pins + 5V pin, native USB. Glance display with pages cycled by a panel button.
- **USB plan:** firmware in TinyUSB CDC mode with `enableReboot(false)`; fallback is UART0 through a USB-serial adapter.
- **Orders in transit (all paid):** DigiKey isolation parts (30 Sep 2026); T-Display-S3, AliExpress ref 3076608492140357; panel buttons, AliExpress ref 3076815630860357, estimated 28 Oct 2026.
- **No longer in the design:** Arduino Nano + stripboard, MD0074 20×4 LCD, BSS138 level shifters, full-system ESP32 PCB, the single-channel `kicad/breakout-max31855/` drawing (superseded by `kicad/tc-board-4ch/`).
- RPi 4 via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Probes delivered and confirmed grounded-junction~~ ✓
2. ~~Choose controller + display~~ ✓ T-Display-S3
3. ~~Order isolation parts, T-Display-S3 and panel buttons~~ ✓
4. ~~4-channel schematic, ERC clean~~ ✓ 7 Oct 2026
5. PCB layout, review, order from JLCPCB — **next**
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pro` — the schematic project (root + `channel.kicad_sch`), ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols (ISO7731DW, RFB-0505S)
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, still-to-buy
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `docs/parts-specs/`, `kicad/datasheets/` — datasheets
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
