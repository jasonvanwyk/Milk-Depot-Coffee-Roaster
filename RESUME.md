# Project Resume

## Right Now
**Phase:** Development — 4-channel isolated thermocouple board schematic complete and ERC-clean; PCB layout is next. LilyGO T-Display-S3 is the controller + display.

**Last (7 Oct 2026, pre-layout session):** Footprint check and the chassis-network decision, both recorded in `docs/2026-09-30-tc-board-design-notes.md`.
- DC-DC on the Traco TMA footprint confirmed against the RFB-0505S drawing (pads 0/2.54/7.62/12.7 mm, 1.0 mm drill). JST PH button connector and 1×10 host header pass. Tantalum, TVS, ferrite footprints match ordered MPNs.
- Screw terminals: Phoenix MSTBA outline was 12 mm deep vs the real DG127 8.1 mm. Claude generated `milk-depot:Degson_DG127-5.08-02P_1x02_P5.08mm_Horizontal` (true outline, box 3D model in `kicad/libs/milk-depot.3dshapes/`); Jason assigned it to J101 in KiCad, all four channels follow. ERC still 0 violations.
- **Chassis network left out.** Grounded-junction probes already reference each island to the roaster body; the jumper could never be closed. Mounting holes are plain. Caveat recorded: insulated-junction probes in a future revision would want the 1 MΩ + 10 nF bleed network (parts on hand).

**Next:**
1. **Start here: PCB layout** in `kicad/tc-board-4ch/`. Isolation slot and two ground zones per channel, TVS/ferrite at the terminal edge, DG127 pin row 4.2 mm from the board edge for a flush wire face. Choose the board-to-display cable and swap J1's placeholder header to match. Then `/pcb-review-engineer`, then order from JLCPCB.
2. When the T-Display-S3 arrives, bench-test USB serial with Artisan on the Pi (not a blocker).

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
- `kicad/libs/milk-depot.kicad_sym` — custom symbols (ISO7731DW, RFB-0505S); `milk-depot.pretty/` — DG127 footprint
- `docs/2026-09-30-tc-board-design-notes.md` — design rules, pinouts, order, footprint check, chassis decision
- `docs/research/2026-09-30-*.md` — board comparison, SA availability, Artisan fit, USB reset
- `docs/parts-specs/`, `kicad/datasheets/` — datasheets
- `arduino-firmware/tc4_emulator/tc4_emulator.ino` — Nano firmware, to be ported
- `docs/BOM.md`, `docs/WIRING.md` — stale (pre-isolation, pre-T-Display-S3)
- `docs/archive/SESSION-INDEX.md` — older sessions
