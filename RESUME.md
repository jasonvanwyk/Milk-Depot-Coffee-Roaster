# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: placement complete, DRC clean on copper; routing is next. LilyGO T-Display-S3 is the controller + display.

**Last (8 Oct 2026, layout session 1):** Board set up and every part placed in `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb`.
- Board setup done by Jason in the GUI: 2-layer 1.6 mm, net classes `Default` + `ISO1`–`ISO4` (0.2 clearance, 0.25 track, 0.6/0.3 via) with twelve wildcard assignments (`/CHn/*`, `Net-(Dn*`, `Net-(Un*`), copper-to-edge 0.3. Custom rules in `tc-board-4ch.kicad_dru` (Claude): 2 mm between any island copper and anything outside that island via `hasNetclass('ISOn')`, 0.5 mm copper-to-edge, JLCPCB floors. Syntax checked clean.
- Outline (50,50)–(146,116), 96 × 66 mm. Claude wrote all 82 footprint positions into the board file by script with the editor closed (same split as the schematic starter). Channel 1 table is in the session transcript summary below; channels 2–4 are +22/+44/+66 mm in X.
- Key placement facts: isolator at (60, 66.5) rot 270 and DC-DC at (71.5, 61.42) both straddle the barrier line Y 66.5; MAX31855 at (60, 83) rot 90 puts its SCK/CS/MISO pads directly below the isolator's island outputs (X 61.91 / 60.63 / 59.37) so those three traces are straight verticals; TC filter column at X 62.46 / 67.54 down to the terminal pins at Y 111.8, wire face flush with the bottom edge.
- Jason drew the eight isolation slots (1.6 mm, Y 65.7–67.3; per channel X 55–65 under the isolator and 67–74 under the DC-DC, +22k) and four M3 holes H1–H4 at (53.5|142.5, 53.5|112.5) using Create Array (Ctrl+T).
- DRC: 0 clearance/courtyard/edge violations. 76 silk-text overlaps remain, to tidy at the end (hide values, nudge refs). J1 stays a 2.54 mm 1×10 header with a Dupont ribbon to the T-Display-S3.

**Next:**
1. **Start here: step 5a, ground zones.** Five zones, both layers, clearance 0.3, min width 0.25, thermal reliefs: `GND` (50.5,50.5)–(145.5,65.0); `/CHn/GND_ISO` (55+22k, 68)–(75+22k, 115.5). Then B to fill, save, Claude checks.
2. Route channel 1 island (Claude gives pad-to-pad order; plan: SCK/CS/MISO straight verticals, CS pull-up stub needs 2 vias across SCK, R102 3V3 feed needs 2 vias, one via for the T+/T− crossing at the terminal, +5V_ISO 0.4 mm). Then channels 2–4 the same, then host: verticals on F.Cu, ten horizontal buses on B.Cu lanes Y 55.5–60.0 (+5V, +3V3, SCK, MISO2–4, CS1–4), vias at SMD ends.
3. Silk tidy, full DRC, `/pcb-review-engineer`, order from JLCPCB.
4. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

**Blocked:** Nothing. DigiKey and two AliExpress deliveries still in transit (buttons due ~28 Oct 2026).

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets are local labels, so each channel gets its own copy.
- **How Claude checks:** `kicad-cli pcb drc --severity-all` and `kicad-cli pcb export svg` on the saved board; parse pad positions from the `.kicad_pcb`. Never edit the board while KiCad has it open; bulk edits only with the editor closed and a backup in the scratchpad.
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
5. PCB layout: ~~placement, slots, holes~~ ✓ 8 Oct 2026 → zones + routing **next**, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb` — the board, placed, unrouted; `.kicad_dru` — isolation DRC rules; `.kicad_pro` — net classes
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
