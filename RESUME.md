# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: islands routed; host-side routing plan written and DRC-clean on a scratch copy, waiting to be applied to the real board. LilyGO T-Display-S3 is the controller + display.

**Last (8 Oct 2026, layout session 4):** Host-side routing plan generated and verified, not yet applied.
- Claude wrote `kicad/tc-board-4ch/host-routing.py`: it moves five parts, injects 75 tracks + 37 vias for all 37 remaining connections into a scratch copy, and runs `kicad-cli pcb drc --refill-zones`. Result: **0 clearance / shorting / starved-thermal errors, 0 unconnected** (was 37). Only silk + library warnings remain.
- Five parts must move (U1 sat over C105 so its bottom-row drops had no exit; C1/C2 blocked the corridor to channel 2): U1 → (77.5, 54.7, 90), C3 → (71.7, 54.7, 90), C1 → (96.3, 62.5, -90), C2 → (118.5, 62.5, -90), J2 → (112, 52.5, 0).
- Scheme: F.Cu verticals pad → via; eleven B.Cu lanes y 53.75–60.4 at 0.63 mm pitch, one net per lane (two lanes shared end-to-end). +5V reaches each DC-DC pin by a B.Cu stub, no via. GND: U_02.2 → C_05.2 tie per channel plus a stub under U1.7 clear all five starved thermals.
- Full move table, lane table and per-net step list: `docs/2026-10-08-host-routing-plan.md`.
- Session ended early to keep the context under 200k tokens; **Jason has not yet chosen how to apply the plan.**

**Next:**
1. **Start here: ask Jason which way to apply the host routing.** (a) He draws it in the GUI from the step list and Claude checks each save, or (b) Claude runs `host-routing.py` on the real board with KiCad closed (no `~*.lck` files) and a backup in the scratchpad — the output is exactly the file that passed DRC, so (b) is lower risk. Either way, finish with a DRC on the real board and F/B renders.
2. Silk tidy (~85 silk warnings, more after the moves), full DRC, `/pcb-review-engineer`, order from JLCPCB.
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
5. PCB layout: ~~placement, slots, holes, ground zones, island routing~~ ✓ 8 Oct 2026 → host routing **planned, apply next**, silk, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb` — the board, islands routed, host unrouted; `.kicad_dru` — isolation DRC rules; `.kicad_pro` — net classes
- `kicad/tc-board-4ch/host-routing.py` — host routing generator (moves + tracks + vias), run as `python3 -I host-routing.py in.kicad_pcb out.kicad_pcb`
- `docs/2026-10-08-host-routing-plan.md` — move table, lane table, per-net step list
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
