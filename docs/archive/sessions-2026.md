# Sessions 2026

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

