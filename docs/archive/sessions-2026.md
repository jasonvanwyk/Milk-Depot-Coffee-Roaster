# Sessions 2026

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

