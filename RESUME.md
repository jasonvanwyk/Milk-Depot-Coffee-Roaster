# Project Resume

## Right Now
**Phase:** Development — drawing the schematic for the 4-channel isolated thermocouple board (channel sheet about three-quarters wired), with LilyGO T-Display-S3 as controller + display

**Last (2 Oct 2026, schematic session 1):** Started the schematic. Jason draws in KiCad; Claude prepared the starter project and checks each step read-only.
- Confirmed KiCad 10.0.6 is the latest stable release.
- Created `kicad/tc-board-4ch/` — root (host) sheet plus `channel.kicad_sch` used four times (CH1–CH4). 82 parts placed with footprints and part numbers; references numbered by channel (U101, U201, ...).
- Added two custom symbols to `kicad/libs/milk-depot.kicad_sym`: ISO7731DW and RFB-0505S.
- **Channel sheet wired and checked:** island power (RFB-0505S → NCP1117), isolator (both sides, both 10K pull-ups, EN pins flagged no-connect), MAX31855 (power, SCK, SO, CS).
- Caught and fixed one mistake: a `GND2` power symbol on the island side joined all four island grounds. Island nets must be local labels only.
- Starter choices still to confirm with Jason: chassis network (mounting hole, solder jumper, 1 MΩ, 10 nF 630V) left out; host connector is 10 pins (tenth = button line); the April test point dropped.

**Next:**
1. **Start here:** Step 5, probe input on the channel sheet. Per line: terminal → TVS to `GND_ISO` → ferrite → 1 nF to `GND_ISO` → MAX31855. T+ = J101 pin 1 → FB101 → U101 pin 3 (D101, C103). T− = J101 pin 2 → FB102 → U101 pin 2 (D102, C104). C102 (10 nF) across T+/T− on the chip side.
2. Root sheet: add sheet pins (SCK, CS, MISO) to CH1–CH4; wire host connector, 5V entry capacitors, SN74AHC125 (A = channel MISO, OE = channel CS, Y = shared MISO), button connector; PWR_FLAG on +5V, +3V3, GND. ERC to zero.
3. Check the provisional footprints before layout: DC-DC (uses the Traco TMA footprint, same pin positions), button connector (2-pin JST PH), host connector (plain header until chosen).
4. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).
5. PCB layout (isolation slots, two ground zones per channel), `/pcb-review-engineer`, order from JLCPCB.

**Blocked:** Nothing. Waiting on DigiKey and two AliExpress deliveries; the schematic does not depend on them.

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets (`GND_ISO`, `+3V3_ISO`, `+5V_ISO`, `SCK_ISO`, `CS_ISO`, `MISO_ISO`) are local labels, so each channel gets its own copy.
- **How Claude checks:** export the netlist with `kicad-cli` and read the nets; never edit the schematic files once Jason is drawing.
- **T-Display-S3:** 1.9" IPS, 6 clean spare pins + 5V pin, native USB. Glance display with pages cycled by a panel button.
- **USB plan:** firmware in TinyUSB CDC mode with `enableReboot(false)`; fallback is UART0 through a USB-serial adapter.
- **Orders in transit (all paid):** DigiKey isolation parts (30 Sep 2026); T-Display-S3, AliExpress ref 3076608492140357; panel buttons, AliExpress ref 3076815630860357, estimated 28 Oct 2026.
- **No longer in the design:** Arduino Nano + stripboard, MD0074 20×4 LCD, BSS138 level shifters, full-system ESP32 PCB, the single-channel `kicad/breakout-max31855/` drawing (superseded by `kicad/tc-board-4ch/`).
- RPi 4 via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Probes delivered and confirmed grounded-junction~~ ✓
2. ~~Choose controller + display~~ ✓ T-Display-S3
3. ~~Order isolation parts, T-Display-S3 and panel buttons~~ ✓
4. 4-channel schematic, ERC clean — **in progress**
5. PCB layout, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pro` — the schematic project (root + `channel.kicad_sch`)
- `kicad/libs/milk-depot.kicad_sym` — custom symbols (ISO7731DW, RFB-0505S)
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, still-to-buy
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `docs/parts-specs/`, `kicad/datasheets/` — datasheets
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
