# Sessions 2026

## 8 October 2026 — layout session 5: host routing applied to the real board, verified beyond DRC

**Last (8 Oct 2026, layout session 5):** Host routing applied to the real board and verified beyond DRC.
- Jason closed the PCB editor; Claude ran `host-routing.py` on the real board (backup in the scratchpad first), then saved refilled zones into the file. All 14 host nets match the plan to 1 µm.
- DRC on the real board: **0 unconnected (was 37), 0 copper errors (5 starved thermals gone)**. 85 silk warnings + 4 harmless library-path warnings remain.
- Thorough check beyond DRC: schematic netlist vs board = 276/276 pins agree; net classes = 40 island nets in exactly one ISO class, 34 Default; island rules proven to fire on both layers by planted tracks; zone fills recede 2.00 mm from foreign-class copper; measured gaps 2.0 mm island↔island, 3.0 mm island↔host; +5V/+3V3 at 0.25 mm are fine for <100 mA total.
- **Suspected a kicad-cli DRC blind spot, then disproved it (9 Oct):** a planted track inside a foreign pad raised nothing only because KiCad re-nets a floating track from the pad it touches on load. A real drawn short (track from J1 pin 4 into pin 5) is caught: shorting_items + solder_mask_bridge + tracks_crossing. Kept `kicad/tc-board-4ch/geom-audit.py` and `zone-audit.py` as an independent second opinion (both 0 violations; validated with planted defects). Run as `python3 -I geom-audit.py tc-board-4ch.kicad_pcb tc-board-4ch.kicad_pro`.
- KiCad 10.0.7 (7 Oct 2026) fixes two zone-fill short bugs; Arch still ships 10.0.6. Refill zones + DRC again when it lands.

## 8 October 2026 — layout session 4: host routing plan generated and DRC-clean on a scratch copy

**Last (8 Oct 2026, layout session 4):** Host-side routing plan generated and verified, not yet applied.
- Claude wrote `kicad/tc-board-4ch/host-routing.py`: it moves five parts, injects 75 tracks + 37 vias for all 37 remaining connections into a scratch copy, and runs `kicad-cli pcb drc --refill-zones`. Result: **0 clearance / shorting / starved-thermal errors, 0 unconnected** (was 37). Only silk + library warnings remain.
- Five parts must move (U1 sat over C105 so its bottom-row drops had no exit; C1/C2 blocked the corridor to channel 2): U1 → (77.5, 54.7, 90), C3 → (71.7, 54.7, 90), C1 → (96.3, 62.5, -90), C2 → (118.5, 62.5, -90), J2 → (112, 52.5, 0).
- Scheme: F.Cu verticals pad → via; eleven B.Cu lanes y 53.75–60.4 at 0.63 mm pitch, one net per lane (two lanes shared end-to-end). +5V reaches each DC-DC pin by a B.Cu stub, no via. GND: U_02.2 → C_05.2 tie per channel plus a stub under U1.7 clear all five starved thermals.
- Full move table, lane table and per-net step list: `docs/2026-10-08-host-routing-plan.md`.
- Session ended early to keep the context under 200k tokens; **Jason has not yet chosen how to apply the plan.**


## 8 October 2026 — layout session 3: all four islands routed, DRC clean on copper

**Last (8 Oct 2026, layout session 3):** All four islands routed, DRC clean on copper.
- Jason drew every island track in the GUI from Claude's pad-by-pad order; Claude checked each save with `kicad-cli pcb drc --refill-zones` on a scratch copy plus F.Cu/B.Cu renders. Channels 2–4 verified as exact +22 mm copies of channel 1 (pad positions compared by script), so the same order was reused.
- Per island: SCK/CS/MISO straight verticals; CS pull-up stub 2 vias under SCK; +3V3 feed to R_02 2 vias under the three verticals; U_03 pin 2 → tab linked on B.Cu with 2 vias under the 0.4 mm +5V_ISO run (KiCad does list same-numbered pads as unconnected); T+/T− cross once above the terminal with 2 vias (J pin 1 is the right-hand diode net); each TVS pad 1 (GND) sits between ferrite and TVS pad 2 so the signal detours around the diode. 8 vias per island, 32 total.
- Pre-defined track widths 0.4 and 0.25 added in Board Setup (`.kicad_pro`); existing +5V_ISO runs widened with Edit → Edit Track & Via Properties filtered by net.
- Result: 0 clearance / isolation / edge / courtyard errors, no island pad unconnected, unconnected 137 → 37 (all host side). The 5 host starved-thermal errors remain for the host pass.
- Host-side pad data gathered (J1 1×10 header at Y 52.5 X 84–106.86, U1 SN74AHC125 at (64, 54.7), C1/C2/C3, C_05 ×4, isolator host pads at Y 61.85, DC-DC +5V/GND at X 71.5+22k); bus plan not yet written.

## 8 October 2026 — layout session 2: ground zones in, fills verified, DRC clean on copper

**Last (8 Oct 2026, layout session 2):** Ground zones drawn, filled and checked.
- Jason drew five multi-layer zones (F.Cu + B.Cu, clearance 0.3, min width 0.25, thermal reliefs, remove islands Always): `GND` (50.5,50.5)–(145.5,65) and `/CHn/GND_ISO` (55+22k, 68)–(75+22k, 115.5). Grid 0.5 mm, corners clicked from the status bar.
- Claude refilled a scratch copy with `kicad-cli pcb drc --refill-zones --save-board` and exported F.Cu/B.Cu SVGs: fills correct, 2 mm bare gap between islands, slots between host strip and islands, thermal reliefs on every ground pad.
- DRC: 0 clearance / isolation / edge / courtyard. **5 `starved_thermal` errors** on host GND, F.Cu: isolator pin 2 (GND1) on U102/U202/U302/U402 and C105 pin 2 — decoupling cap sits tight above the pin so only one spoke fits. Expect the GND tie track to clear it; otherwise set those five pads to solid zone connection. 80 silk warnings deferred, 137 unconnected (nothing routed).
- Fill polygons are saved in the board file after a final B + Ctrl+S; Claude still refills a scratch copy before checking.

## 8 October 2026 — layout session 1: board set up, all parts placed, slots and holes in

**Last (8 Oct 2026, layout session 1):** Board set up and every part placed in `kicad/tc-board-4ch/tc-board-4ch.kicad_pcb`.
- Board setup done by Jason in the GUI: 2-layer 1.6 mm, net classes `Default` + `ISO1`–`ISO4` (0.2 clearance, 0.25 track, 0.6/0.3 via) with twelve wildcard assignments (`/CHn/*`, `Net-(Dn*`, `Net-(Un*`), copper-to-edge 0.3. Custom rules in `tc-board-4ch.kicad_dru` (Claude): 2 mm between any island copper and anything outside that island via `hasNetclass('ISOn')`, 0.5 mm copper-to-edge, JLCPCB floors. Syntax checked clean.
- Outline (50,50)–(146,116), 96 × 66 mm. Claude wrote all 82 footprint positions into the board file by script with the editor closed (same split as the schematic starter). Channel 1 table is in the session transcript summary below; channels 2–4 are +22/+44/+66 mm in X.
- Key placement facts: isolator at (60, 66.5) rot 270 and DC-DC at (71.5, 61.42) both straddle the barrier line Y 66.5; MAX31855 at (60, 83) rot 90 puts its SCK/CS/MISO pads directly below the isolator's island outputs (X 61.91 / 60.63 / 59.37) so those three traces are straight verticals; TC filter column at X 62.46 / 67.54 down to the terminal pins at Y 111.8, wire face flush with the bottom edge.
- Jason drew the eight isolation slots (1.6 mm, Y 65.7–67.3; per channel X 55–65 under the isolator and 67–74 under the DC-DC, +22k) and four M3 holes H1–H4 at (53.5|142.5, 53.5|112.5) using Create Array (Ctrl+T).
- DRC: 0 clearance/courtyard/edge violations. 76 silk-text overlaps remain, to tidy at the end (hide values, nudge refs). J1 stays a 2.54 mm 1×10 header with a Dupont ribbon to the T-Display-S3.

## 7 October 2026 — pre-layout session: footprint check and chassis decision

**Last (7 Oct 2026, pre-layout session):** Footprint check and the chassis-network decision, both recorded in `docs/2026-09-30-tc-board-design-notes.md`.
- DC-DC on the Traco TMA footprint confirmed against the RFB-0505S drawing (pads 0/2.54/7.62/12.7 mm, 1.0 mm drill). JST PH button connector and 1×10 host header pass. Tantalum, TVS, ferrite footprints match ordered MPNs.
- Screw terminals: Phoenix MSTBA outline was 12 mm deep vs the real DG127 8.1 mm. Claude generated `milk-depot:Degson_DG127-5.08-02P_1x02_P5.08mm_Horizontal` (true outline, box 3D model in `kicad/libs/milk-depot.3dshapes/`); Jason assigned it to J101 in KiCad, all four channels follow. ERC still 0 violations.
- **Chassis network left out.** Grounded-junction probes already reference each island to the roaster body; the jumper could never be closed. Mounting holes are plain. Caveat recorded: insulated-junction probes in a future revision would want the 1 MΩ + 10 nF bleed network (parts on hand).

## 7 October 2026 — schematic session 2: 4-channel board ERC-clean

**Last (7 Oct 2026, schematic session 2):** Finished the schematic. Jason drew, Claude checked each step by exporting the netlist with `kicad-cli` and running ERC.
- The PC shut down unexpectedly on 6 Oct; KiCad had the project open but nothing had been saved, so no work was lost (files matched the last commit).
- **Channel sheet (`channel.kicad_sch`) finished:** probe input chain per line — J101 → TVS (SMAJ5.0CA, connector side) → ferrite → 1 nF to `GND_ISO` (chip side) → MAX31855 T+/T−, plus 10 nF C102 across T+/T−. No-connect on U101 pin 8.
- **Root sheet (`tc-board-4ch.kicad_sch`) finished:** sheet pins SCK/CS/MISO on CH1–CH4 (Place Pins from Sheet), 10-pin host connector J1 (1 GND, 2 +5V, 3 +3V3, 4 SCK, 5 MISO, 6–9 CS1–CS4, 10 BTN), 5V entry caps C1/C2, SN74AHC125 (OE = CSn, A = MISOn, Y = shared MISO), U1 power + C3, button connector J2 (BTN, GND), PWR_FLAG on +5V/+3V3/GND.
- **ERC: 0 violations on all five sheets.** Only intentional unconnected pins remain (MAX31855 pin 8, isolator EN/NC pins), all flagged.
- Reverted KiCad save-noise on the superseded `kicad/breakout-max31855/` and `kicad/milk-depot-coffee-roaster.kicad_sch` files.

## 2 October 2026 — schematic session 1: starter project, channel sheet three-quarters wired

**Last (2 Oct 2026, schematic session 1):** Started the schematic. Jason draws in KiCad; Claude prepared the starter project and checks each step read-only.
- Confirmed KiCad 10.0.6 is the latest stable release.
- Created `kicad/tc-board-4ch/` — root (host) sheet plus `channel.kicad_sch` used four times (CH1–CH4). 82 parts placed with footprints and part numbers; references numbered by channel (U101, U201, ...).
- Added two custom symbols to `kicad/libs/milk-depot.kicad_sym`: ISO7731DW and RFB-0505S.
- **Channel sheet wired and checked:** island power (RFB-0505S → NCP1117), isolator (both sides, both 10K pull-ups, EN pins flagged no-connect), MAX31855 (power, SCK, SO, CS).
- Caught and fixed one mistake: a `GND2` power symbol on the island side joined all four island grounds. Island nets must be local labels only.
- Starter choices still to confirm with Jason: chassis network (mounting hole, solder jumper, 1 MΩ, 10 nF 630V) left out; host connector is 10 pins (tenth = button line); the April test point dropped.

## 30 September – 2 October 2026 — direction reset to T-Display-S3 + 4-channel isolated board; all parts ordered

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

## 13–22 April 2026 — breakout sessions 1–5 (recorded in `~/tools/kicad-coffee-roaster/`)

**Previous (21–22 Apr 2026, recorded in tool repo):** DMM test confirmed all 6 probes are grounded-junction. Pivoted breakout from v1.0 to v1.1 with per-breakout galvanic isolation (isolated DC-DC + digital isolator). Hand-drew 15 components of the breakout schematic with footprints and BOM fields; not yet wired.

- [x] ~~Scaffolded MD-TC-BRK breakout sub-project from SparkFun DEV-13266; redrew schematic by hand (15 components, BOM fields)~~
- [x] ~~Confirmed all 6 probes are grounded-junction by DMM continuity~~
- [x] ~~Pivoted breakout to v1.1 with per-breakout galvanic isolation~~

## 30 March 2026

**Last (30 Mar 2026):** Full procurement audit — read ALL invoices across 5 suppliers (3× DigiKey, 3× Mantech, Communica, DIY Electronics, Micro Robotics). Discovered DigiKey #122017091 (first Fairfield order) was fully returned via credit memo. DigiKey #122880837 is the real unified order (37 line items) containing ALL roaster parts: NCP1117ST33T3G (SOT-223), MMBT2222A, 10nF/1µF/100nF/10µF 0805 caps, tactile switches (TL3342), JST PH 4-pin, screw terminals (OSTTC020162), ESP32, MAX31855. Built complete component grid with verified MPNs, manufacturers, supplier PNs. Downloaded all datasheets to `kicad/datasheets/`. Verified KiCad footprints against datasheets — TL3342 tactile switch needs custom footprint (4.80×2.80mm pad pattern, no built-in match). Screw terminal decision: using Degson DG127-5.08-02P (Mantech 15M0713) — footprint compatible with Phoenix 5.08mm. Started placing components with BOM fields (R1-R6, C1 in progress).

- [x] ~~Full procurement audit: read ALL invoices across 5 suppliers (DigiKey ×3, Mantech ×3, Communica, DIY, Micro Robotics)~~
- [x] ~~Corrected stale BOM: DigiKey #122017091 was fully returned, #122880837 is the real order (37 items)~~
- [x] ~~Confirmed all roaster parts on hand: NCP1117 SOT-223, MMBT2222A, 10nF/1µF/100nF/10µF 0805, TL3342, JST PH 4-pin, OSTTC020162~~
- [x] ~~Built complete component grid with MPNs, manufacturers, supplier PNs for all 20 schematic components~~
- [x] ~~Downloaded all datasheets to kicad/datasheets/ (NCP1117, MMBT2222A, TL3342, OSTTC020162, DG127, B4B-PH-K-S, CL21B103, TMK212BJ105KD)~~
- [x] ~~Verified all KiCad footprints against datasheets — TL3342 needs custom footprint (4.80×2.80mm pad pattern)~~
- [x] ~~Screw terminal decision: using Degson DG127-5.08-02P (Mantech 15M0713), 5.08mm pitch compatible~~
- [x] ~~Started placing components with BOM fields: R1-R6 (10K 0805), C1 (100nF 0805)~~

## 28–30 March 2026

**Previous (28-30 Mar 2026):** Scaffolded KiCad 10 project, placed U1/U2/U3/Q1/Q2 with BOM fields.

- [x] ~~Archived old KiCad schematic, scaffolded new KiCad 10 project with JLCPCB design rules~~
- [x] ~~Validated and placed U1 (ESP32), U2+U3 (MAX31855), Q1+Q2 (BSS138) with BOM fields~~

## 23 March 2026

- [x] ~~Switched display from OLED to 20×4 I2C LCD (Keyestudio MD0074) — HD44780, no driver issues, no burn-in~~
- [x] ~~Evaluated and rejected Adafruit OLED (unavailable/expensive), SSD1309 OLED, and Newhaven premium LCD~~
- [x] ~~Added BSS138 N-MOSFET level shifters to BOM for 3.3V ESP32 ↔ 5V LCD I2C~~
- [x] ~~Updated Mantech order: KS5019 ESP32 + MD0074 LCD = R486.07 incl. VAT~~
- [x] ~~Decided PCB strategy: MAX31855 breakout board first to validate thermocouples with dev board~~

## 20 March 2026

- [x] ~~Rewrote docs/BOM.md v2.0 for ESP32 redesign with specific 0805 part numbers~~
- [x] ~~Cross-referenced DigiKey cart CSV — all passives already in Fairfield combined order~~
- [x] ~~Selected Adafruit 2719 OLED (SSD1305) over Waveshare SSD1309 — quality + standard header~~
- [x] ~~Confirmed 0805 for all passives (not 0603) — matches Fairfield order~~
- [x] ~~Identified only 2 items still needed in DigiKey cart: screw terminals + OLED~~
- [x] ~~Updated DigiKey checklist with in-cart vs still-short items~~

