# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board: all four islands routed, DRC clean on copper; host-side routing is next. LilyGO T-Display-S3 is the controller + display.

**Last (8 Oct 2026, layout session 3):** All four islands routed, DRC clean on copper.
- Jason drew every island track in the GUI from Claude's pad-by-pad order; Claude checked each save with `kicad-cli pcb drc --refill-zones` on a scratch copy plus F.Cu/B.Cu renders. Channels 2–4 verified as exact +22 mm copies of channel 1 (pad positions compared by script), so the same order was reused.
- Per island: SCK/CS/MISO straight verticals; CS pull-up stub 2 vias under SCK; +3V3 feed to R_02 2 vias under the three verticals; U_03 pin 2 → tab linked on B.Cu with 2 vias under the 0.4 mm +5V_ISO run (KiCad does list same-numbered pads as unconnected); T+/T− cross once above the terminal with 2 vias (J pin 1 is the right-hand diode net); each TVS pad 1 (GND) sits between ferrite and TVS pad 2 so the signal detours around the diode. 8 vias per island, 32 total.
- Pre-defined track widths 0.4 and 0.25 added in Board Setup (`.kicad_pro`); existing +5V_ISO runs widened with Edit → Edit Track & Via Properties filtered by net.
- Result: 0 clearance / isolation / edge / courtyard errors, no island pad unconnected, unconnected 137 → 37 (all host side). The 5 host starved-thermal errors remain for the host pass.
- Host-side pad data gathered (J1 1×10 header at Y 52.5 X 84–106.86, U1 SN74AHC125 at (64, 54.7), C1/C2/C3, C_05 ×4, isolator host pads at Y 61.85, DC-DC +5V/GND at X 71.5+22k); bus plan not yet written.

**Next:**
1. **Start here: host-side routing.** Claude writes the order from the gathered pads: 37 connections — +5V (J1.2, C1, C2, PS_01 pin 1 ×4), +3V3 (J1.3, C3, U1.14, C_05 ×4, isolator pin 1 ×4), SCK (J1.4, isolator pin 3 ×4), MISO/MISO1–4/CS1–4 through U1 buffer to isolator pins 4/5 and J1.5–9, BTN (J1.10 → J2.1). Plan: short verticals on F.Cu, horizontal buses on B.Cu lanes Y 55.5–60.0, vias at the SMD ends; GND tie tracks to clear the 5 starved thermals (else set those pads to solid connection). **Method:** write a scratchpad script that checks each bus lane and via position against the pad table and prints the order, then hand it to Jason one net at a time. Do not work the geometry out in reasoning — that stalled silently for 20 min at the end of session 3 and nothing survived.
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
5. PCB layout: ~~placement, slots, holes, ground zones, island routing~~ ✓ 8 Oct 2026 → host routing **next**, silk, review, order from JLCPCB
6. Hand-assemble the board
7. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
8. Design and print the enclosure
9. Clone repo to RPi properly
10. Calibrate (ice water + boiling water)
11. Mount probes in roaster, first test roast with Artisan

## Key Files
- `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb` — the board, placed, zones in, islands routed, host unrouted; `.kicad_dru` — isolation DRC rules; `.kicad_pro` — net classes
- `kicad/tc-board-4ch/tc-board-4ch.kicad_sch` + `channel.kicad_sch` — schematic, ERC clean
- `kicad/libs/milk-depot.kicad_sym` — custom symbols; `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
