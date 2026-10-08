# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: placement and ground zones done, DRC clean on copper; routing channel 1 is next. LilyGO T-Display-S3 is the controller + display.

**Last (8 Oct 2026, layout session 2):** Ground zones drawn, filled and checked.
- Jason drew five multi-layer zones (F.Cu + B.Cu, clearance 0.3, min width 0.25, thermal reliefs, remove islands Always): `GND` (50.5,50.5)–(145.5,65) and `/CHn/GND_ISO` (55+22k, 68)–(75+22k, 115.5). Grid 0.5 mm, corners clicked from the status bar.
- Claude refilled a scratch copy with `kicad-cli pcb drc --refill-zones --save-board` and exported F.Cu/B.Cu SVGs: fills correct, 2 mm bare gap between islands, slots between host strip and islands, thermal reliefs on every ground pad.
- DRC: 0 clearance / isolation / edge / courtyard. **5 `starved_thermal` errors** on host GND, F.Cu: isolator pin 2 (GND1) on U102/U202/U302/U402 and C105 pin 2 — decoupling cap sits tight above the pin so only one spoke fits. Expect the GND tie track to clear it; otherwise set those five pads to solid zone connection. 80 silk warnings deferred, 137 unconnected (nothing routed).
- Fill polygons are saved in the board file after a final B + Ctrl+S; Claude still refills a scratch copy before checking.

**Next:**
1. **Start here: route channel 1 island** (Claude gives pad-to-pad order; plan: SCK/CS/MISO straight verticals, CS pull-up stub needs 2 vias across SCK, R102 3V3 feed needs 2 vias, one via for the T+/T− crossing at the terminal, +5V_ISO 0.4 mm). Then channels 2–4 the same, then host: verticals on F.Cu, ten horizontal buses on B.Cu lanes Y 55.5–60.0 (+5V, +3V3, SCK, MISO2–4, CS1–4), vias at SMD ends.
2. Silk tidy, full DRC, `/pcb-review-engineer`, order from JLCPCB.
3. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

**Blocked:** Nothing. DigiKey and two AliExpress deliveries still in transit (buttons due ~28 Oct 2026).

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets are local labels, so each channel gets its own copy.
- **How Claude checks:** copy board to scratchpad, `kicad-cli pcb drc --refill-zones --save-board --severity-all` and `kicad-cli pcb export svg` on the saved board; parse pad positions from the `.kicad_pcb`. Never edit the board while KiCad has it open; bulk edits only with the editor closed and a backup in the scratchpad.
- **T-Display-S3:** 1.9" IPS, 6 clean spare pins + 5V pin, native USB. Glance display with pages cycled by a panel button.
- **USB plan:** firmware in TinyUSB CDC mode with `enableReboot(false)`; fallback is UART0 through a USB-serial adapter.
- **Orders in transit (all paid):** DigiKey isolation parts (30 Sep 2026); T-Display-S3, AliExpress ref 3076608492140357; panel buttons, AliExpress ref 3076815630860357, estimated 28 Oct 2026.
- **No longer in the design:** Arduino Nano + stripboard, MD0074 20×4 LCD, BSS138 level shifters, full-system ESP32 PCB, `kicad/breakout-max31855/`.
- RPi 4 via SSH at 10.0.10.102 (user: jason, key-based auth)

## Development Plan
1. ~~Probes delivered and confirmed grounded-junction~~ ✓
2. ~~Choose controller + display~~ ✓ T-Display-S3
3. ~~Order isolation parts, T-Display-S3 and panel buttons~~ ✓
4. ~~4-channel schematic, ERC clean~~ ✓ 7 Oct 2026
5. PCB layout: ~~placement, slots, holes, ground zones~~ ✓ 8 Oct 2026 → routing **next**, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb` — the board, placed, zones in, unrouted; `.kicad_dru` — isolation DRC rules; `.kicad_pro` — net classes
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
