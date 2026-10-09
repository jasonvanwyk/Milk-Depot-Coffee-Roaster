# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: fully routed (islands + host), 0 unconnected, DRC and independent audits clean; silk tidy and review next. LilyGO T-Display-S3 is the controller + display.

**Last (8 Oct 2026, layout session 5):** Host routing applied to the real board and verified beyond DRC.
- Jason closed the PCB editor; Claude ran `host-routing.py` on the real board (backup in the scratchpad first), then saved refilled zones into the file. All 14 host nets match the plan to 1 µm.
- DRC on the real board: **0 unconnected (was 37), 0 copper errors (5 starved thermals gone)**. 85 silk warnings + 4 harmless library-path warnings remain.
- Thorough check beyond DRC: schematic netlist vs board = 276/276 pins agree; net classes = 40 island nets in exactly one ISO class, 34 Default; island rules proven to fire on both layers by planted tracks; zone fills recede 2.00 mm from foreign-class copper; measured gaps 2.0 mm island↔island, 3.0 mm island↔host; +5V/+3V3 at 0.25 mm are fine for <100 mA total.
- **Found a kicad-cli DRC blind spot (KiCad 10.0.6):** a track lying inside or crossing a pad of another net reports nothing, with any flags. Written two independent audits that do catch it: `kicad/tc-board-4ch/geom-audit.py` (pad/track/via pairs, 0.2 mm same class, 2 mm across classes) and `zone-audit.py` (zone-fill boundary vs foreign-class items). Both validated with planted defects; both report 0 violations on the real board. Run as `python3 -I geom-audit.py tc-board-4ch.kicad_pcb tc-board-4ch.kicad_pro`.
**Next:**
1. **Start here:** Jason opens the board, eyeballs the host strip, runs DRC in the GUI once (GUI engine may differ from kicad-cli on pad overlaps). Then silk tidy: 37 overlaps, 39 refs over copper (C_01/C_03/C_05, U_03, U1, J1), 9 silk items within 0.5 mm of slots (J_01 and PS_01 outlines, J2 label).
2. `/pcb-review-engineer`, then order from JLCPCB. Re-run `geom-audit.py` + `zone-audit.py` after any copper edit.
3. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

**Blocked:** Nothing. DigiKey and two AliExpress deliveries still in transit (buttons due ~28 Oct 2026).

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets are local labels, so each channel gets its own copy.
- **How Claude checks:** copy board to scratchpad, `kicad-cli pcb drc --refill-zones --save-board --severity-all` and `kicad-cli pcb export svg` on the saved board; parse pad positions from the `.kicad_pcb`. Never edit the board while KiCad has it open; bulk edits only with the editor closed and a backup in the scratchpad. **For routing: generate geometry by script and let DRC judge it — never work clearances out in reasoning.**
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
5. PCB layout: ~~placement, slots, holes, ground zones, island routing, host routing~~ ✓ 8 Oct 2026 → silk tidy, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb` — the board, fully routed, 0 unconnected; `.kicad_dru` — isolation DRC rules; `.kicad_pro` — net classes
- `kicad/tc-board-4ch/host-routing.py` — host routing generator (moves + tracks + vias), run as `python3 -I host-routing.py in.kicad_pcb out.kicad_pcb`
- `docs/2026-10-08-host-routing-plan.md` — move table, lane table, per-net step list (applied 8 Oct 2026)
- `kicad/tc-board-4ch/geom-audit.py`, `zone-audit.py` — independent clearance audits covering the kicad-cli pad-overlap blind spot; run after any copper edit
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
