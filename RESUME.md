# Project Resume

## Right Now
**Phase:** Development — schematic for the 4-channel isolated thermocouple board, with LilyGO T-Display-S3 as controller + display

**Last (30 Sep – 2 Oct 2026):** Restarted after a five-month gap, reset the direction, and ordered all main parts.
- Reconciled this repo with `~/tools/kicad-coffee-roaster/`, where the April breakout sessions (grounded probes confirmed, isolation pivot) had been recorded but never copied here.
- Researched ESP32 boards with a built-in display and the ESP32-S3 USB reset question — 4 reports in `docs/research/`.
- **Decided:** LilyGO T-Display-S3 (non-touch) replaces the Nano/stripboard and the bare ESP32 + 20×4 LCD plans.
- **Decided:** one 4-channel thermocouple board (fit 3: BT, ET, FT), each channel on its own isolated island, instead of three separate breakouts.
- **Decided:** one custom 3D-printed enclosure for the T-Display-S3 and the board.
- Chose the isolation parts, checked all nine datasheets against the cart, and **Jason ordered and paid for the DigiKey order**.
- **Panel buttons ordered and paid (2 Oct 2026)**: 10× 16 mm flat-head metal push button, momentary, 1NO, no LED, pre-wired tails, DIANQI Electric Official Store on AliExpress, ref 3076815630860357, R329.00 total, estimated delivery 28 Oct 2026. Wires to a spare T-Display-S3 pin and GND via a 2-pin connector on the thermocouple board; firmware uses the internal pull-up.
- **Spare RFB-0505S** bought by Jason (supplier and quantity not recorded).
- **T-Display-S3 ordered and paid**: 1× non-touch, unsoldered pins, LilyGO Official Store on AliExpress, ref 3076608492140357, R373.98 incl. shipping. Seller has up to 12 days to ship.
- Wrote `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order list, still-to-buy list.

**Next:**
1. **Start here next session:** draw the 4-channel schematic from the design notes — one channel sheet reused four times + a host sheet (include the 2-pin button connector). Wire, ERC to zero. First ask Jason the open question: does he draw it in KiCad from an updated guide (as in April), or does Claude generate the schematic file for him to review?
2. Still to choose at layout time: the board-to-display connector. Optional: a second T-Display-S3 as a spare.
3. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker — see the USB research report).
4. PCB layout (isolation slots, two ground zones per channel), `/pcb-review-engineer`, order from JLCPCB.

**Blocked:** Nothing. Waiting on DigiKey and two AliExpress deliveries; the schematic does not depend on them.

## Quick Context
- Client: Quenton (Milk Depot) — coffee roaster temperature monitoring
- **Signal chain:** 3 probes → 4-channel isolated board → T-Display-S3 (own 1.9" screen + page button) → USB → Raspberry Pi 4 running Artisan → HMI screen (already owned)
- **Probes are grounded-junction** — per-channel isolation is required whatever the controller. Possibly what killed the first prototype's MAX31855.
- **T-Display-S3:** 1.9" IPS, screen about 43×23 mm, 6 clean spare pins + 5V pin, native USB. Glance display: pages of one or two large readings (9–14 mm digits), cycled by a panel button.
- **USB plan:** firmware in TinyUSB CDC mode with `enableReboot(false)`; fallback is UART0 through a USB-serial adapter.
- **No longer in the design:** Arduino Nano + stripboard, MD0074 20×4 LCD, BSS138 level shifters, full-system ESP32 PCB (`kicad/milk-depot-coffee-roaster.kicad_sch` is abandoned).
- 0805 for all passives. MAX31855KASA+ ×9, NCP1117 ×10, DG127 screw terminals ×15 on hand.
- RPi 4 via SSH at 10.0.10.102 (user: jason, key-based auth)
- `~/tools/kicad-coffee-roaster/` still says "Nano" and "three breakouts" — stale on both; its isolation reasoning is still valid.

## Existing drawing to reuse
`kicad/breakout-max31855/breakout-max31855.kicad_sch` has 15 components of one channel placed with footprints and part numbers, unwired (41 ERC items, expected). It becomes the repeated channel sheet. Its `README.md` and `schematic-guide.md` describe the old single-breakout v1.0 and need replacing.

## Development Plan
1. ~~Probes delivered and confirmed grounded-junction~~ ✓
2. ~~Choose controller + display~~ ✓ T-Display-S3
3. ~~Order isolation parts~~ ✓ DigiKey, 30 Sep 2026
4. ~~Order T-Display-S3 and panel buttons~~ ✓ AliExpress, 30 Sep and 2 Oct 2026
5. 4-channel schematic, ERC clean
6. PCB layout, review, order from JLCPCB
7. Hand-assemble the board
8. Port firmware to ESP32-S3: 3 channels, display pages, page button, TC4 protocol
9. Design and print the enclosure
10. Clone repo to RPi properly
11. Calibrate (ice water + boiling water)
12. Mount probes in roaster, first test roast with Artisan

## Key Files
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, still-to-buy
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `docs/parts-specs/` — datasheets for the ordered parts
- `kicad/breakout-max31855/` — single-channel drawing to reuse
- `kicad/datasheets/` — MAX31855, NCP1117, DG127 and other datasheets
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
