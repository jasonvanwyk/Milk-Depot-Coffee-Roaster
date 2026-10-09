# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: fully routed (islands + host), 0 unconnected, DRC and independent audits clean; silk tidy and review next. LilyGO T-Display-S3 is the controller + display.

**Last (9 Oct 2026, hot plate):** Chose and ordered the reflow hot plate so it arrives before the PCBs.
- `/cheap-research` (3 Sonnet agents) → `docs/research/2026-10-09-hot-plate-{requirements,products-sa,reflow-process}.md`. Key finding: the 96 × 66 mm board with pours on both layers needs a plate that overhangs it on all sides, so every SA-stocked plate (MHP30/MHP50/HT-P1A, 30–50 mm) is out.
- Compared four AliExpress 946C listings in Chrome (seller rating, stated specs, shipping). Ordered **UYUE 946C 200 × 200 mm, 600 W, 220 V EU plug** from Caius Store, ref 3076880346740357, R2,556.99 (R556 + R2,000.99 courier), due 22 Oct 2026. Fit an earthed IEC lead, bin the supplied adapter.
- Reflow oven considered and rejected for 2–5 single-sided boards; T-962 would need firmware + insulation mods.
- Follow-ups: leaded Sn63/Pb37 paste syringe (SA stock unverified — Communica or DigiKey ZA), add unframed stainless stencil to the JLCPCB order, K-type or IR thermometer for board temp.
**Next:**
1. **Start here:** Jason opens the board, eyeballs the host strip, runs DRC in the GUI once. Then silk tidy: 37 overlaps, 39 refs over copper (C_01/C_03/C_05, U_03, U1, J1), 9 silk items within 0.5 mm of slots (J_01 and PS_01 outlines, J2 label).
2. `/pcb-review-engineer`, then order from JLCPCB. Re-run `geom-audit.py` + `zone-audit.py` after any copper edit.
3. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

**Blocked:** Nothing. DigiKey and three AliExpress deliveries still in transit (hot plate due ~22 Oct, buttons due ~28 Oct 2026).

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **Schematic rule:** power symbols (`+5V`, `+3V3`, `GND`) only on the host side. Island nets are local labels, so each channel gets its own copy.
- **How Claude checks:** copy board to scratchpad, `kicad-cli pcb drc --refill-zones --save-board --severity-all` and `kicad-cli pcb export svg` on the saved board; parse pad positions from the `.kicad_pcb`. Never edit the board while KiCad has it open; bulk edits only with the editor closed and a backup in the scratchpad. **For routing: generate geometry by script and let DRC judge it — never work clearances out in reasoning.**
- **T-Display-S3:** 1.9" IPS, 6 clean spare pins + 5V pin, native USB. Glance display with pages cycled by a panel button.
- **USB plan:** firmware in TinyUSB CDC mode with `enableReboot(false)`; fallback is UART0 through a USB-serial adapter.
- **Orders in transit (all paid):** DigiKey isolation parts (30 Sep 2026); T-Display-S3, AliExpress ref 3076608492140357; panel buttons, AliExpress ref 3076815630860357, estimated 28 Oct 2026; UYUE 946C hot plate (200 mm, 220 V), AliExpress ref 3076880346740357, R2,556.99, ordered 9 Oct 2026, estimated 22 Oct 2026. Use leaded Sn63/Pb37 paste + JLCPCB stencil (see `docs/research/2026-10-09-hot-plate-reflow-process.md`).
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
- `kicad/tc-board-4ch/geom-audit.py`, `zone-audit.py` — independent clearance audits, second opinion to DRC; run after any copper edit
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
