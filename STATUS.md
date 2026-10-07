# Project Status - Milk Depot Coffee Roaster

**Last Updated:** 2026-10-07
**Quote Ref:** PO P00041 (thermocouples)
**Status:** Development
**Payment Terms:** Invoice on delivery (GPA Trading)

---

## Current Phase: Development

**DIRECTION RESET (30 September 2026).** Controller and display: LilyGO T-Display-S3. Thermocouple front end: one custom 4-channel board (3 fitted), each channel galvanically isolated, because the probes are grounded-junction. Everything in one custom 3D-printed enclosure. The Pi + HMI running Artisan is unchanged. The Nano/stripboard plan, the 20×4 LCD and the full-system ESP32 PCB are dropped. Isolation parts ordered and paid (DigiKey, 30 September 2026). T-Display-S3 and panel buttons ordered and paid (AliExpress, 30 September and 2 October 2026). Schematic drawn 2–7 October 2026 in `kicad/tc-board-4ch/` and ERC-clean on 7 October 2026; footprints checked and chassis network dropped the same day; PCB layout is next. Design notes: `docs/2026-09-30-tc-board-design-notes.md`.

---

## Task Status

### Completed

| Task | Completed | Notes |
|------|-----------|-------|
| Git repository setup | 2024-12-30 | GitHub remote configured |
| Artisan v3.4.0 installation | 2024-11-10 | On Raspberry Pi 4 |
| Arduino TC4 firmware | 2024-12-30 | 3-channel MAX31855 support |
| Helper scripts | 2024-12-30 | compile, upload, detect, monitor |
| Serial communication verified | 2025-11-10 | 115200 baud, TC4 protocol working |
| Technical documentation | 2024-12-30 | BOM, wiring, protocol, specs |
| Thermocouple specification | 2026-01-12 | Custom probe specs finalized |
| Quote from GPA Trading | 2026-01-23 | 6 probes quoted, pricing accepted |
| PO P00041 placed | 2026-02-02 | Thermocouples ordered |
| Thermocouple delivery | 2026-03-13 | 6x custom K-type probes received |
| Invoice + payment | 2026-02-24 | Invoice received, POP sent same day |
| All BOM components procured | 2026-03-13 | Thermocouples from GPA, rest locally |
| KiCad tooling installed | 2026-03-13 | MCP servers + skills for schematic/PCB design |
| RPi SSH access | 2026-03-13 | 10.0.10.102, user jason, key-based auth |
| KiCad schematic created | 2026-03-13 | Arduino Nano, 2x MAX31855, OLED, 100nF caps |
| OLED bezel designed | 2026-03-13 | OpenSCAD snap-fit bezel (`3d-prints/oled-bezel.scad`) |
| OpenSCAD bezel rendered | 2026-03-13 | STL exported (25KB), PNG previews from 4 angles |
| FreeCAD bezel redesign | 2026-03-13 | Manual design with real caliper measurements (WIP) |
| WireViz installed | 2026-03-13 | v0.4.1, for wiring diagram generation |
| WireViz wiring diagram | 2026-03-17 | YAML source + PNG/SVG/HTML output with BOM |
| Fritzing breadboard layout | 2026-03-17 | Nano + 2x MAX31855 + OLED + caps, verified |
| WIRING.md rewrite | 2026-03-17 | Updated from 3-channel UNO to 2-channel Nano |
| OLED 5V confirmed | 2026-03-17 | Onboard voltage regulator visible on PCB back |
| Firmware updated for Nano 2-channel | 2026-03-18 | TC4 protocol + SH1106 OLED + MAX31855 hardware |
| First power-up test | 2026-03-18 | Firmware works, OLED works, knockoff MAX31855 smoked |
| Redesign decision | 2026-03-18 | ESP32 + genuine MAX31855 ICs + custom PCB + 2.42" OLED |
| Component sourcing | 2026-03-18 | DigiKey ZA (MAX31855KASA+) + Mantech (ESP32 KS5019) |
| BOM v2.0 rewrite | 2026-03-20 | ESP32 redesign, specific 0805 MPNs, DigiKey order checklist |
| DigiKey cart cross-reference | 2026-03-20 | All passives confirmed in Fairfield combined order |
| OLED display selected | 2026-03-20 | Adafruit 2719 (SSD1305), DigiKey 1528-1591-ND — superseded by LCD |
| Display switched to LCD | 2026-03-23 | Keyestudio MD0074 20×4 I2C LCD (Mantech 15M8244, R184.47 ex-VAT) |
| BSS138 level shifters added | 2026-03-23 | BSS138CT-ND × 4, for 3.3V↔5V I2C on custom PCB |
| PCB strategy decided | 2026-03-23 | MAX31855 breakout board first, then full system PCB |
| DigiKey unified order placed | 2026-03-28 | Via Fairfield project (FD-PROC-010), roaster parts included |
| KiCad 10 project scaffolded | 2026-03-28 | New project with JLCPCB design rules, old schematic archived |
| Schematic symbols placed | 2026-03-30 | ESP32, 2× MAX31855, 2× BSS138 — validated against datasheets |
| BSS138 sourced from Mantech | 2026-03-30 | Stock 35M3468, R1.20 each (ON Semi, SOT-23) |
| 4-channel board schematic | 2026-10-07 | `kicad/tc-board-4ch/`, root + channel sheet ×4, ERC 0 violations |
| Footprint check + chassis decision | 2026-10-07 | DG127 footprint added to `kicad/libs/milk-depot.pretty/`; chassis network left out (grounded probes) |

### Session Completed Items (7 Oct 2026 — pre-layout session)
- [x] ~~Footprint check: RFB-0505S on Traco TMA footprint, JST PH button, 1×10 header, tantalum, TVS, ferrite all pass~~
- [x] ~~Generated true-outline DG127 screw-terminal footprint + box 3D model in the project library; assigned to J101–J401, ERC still clean~~
- [x] ~~Chassis network decided: left out, caveat for insulated probes recorded in design notes~~

Older sessions: `docs/archive/SESSION-INDEX.md`.

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| DigiKey orders shipped & received | DONE | #122880837 (37 items) + #123184654 (ICs). All roaster parts on hand. |
| Mantech LCD + screw terminals received | DONE | #178252 (MD0074 LCD) + #210901 (DG127 terminals, headers) |
| BSS138 from Mantech | NOT NEEDED | Dropped from design — digital isolators handle the voltage levels |
| Full-system ESP32 schematic | ABANDONED | Replaced by T-Display-S3 + isolated breakouts |
| Isolation parts order (DigiKey) | ORDERED + PAID | 30 Sep 2026. 9 lines, enough for 2 boards. Awaiting delivery |
| T-Display-S3 order (AliExpress) | ORDERED + PAID | 30 Sep 2026. 1× non-touch, unsoldered pins, LilyGO Official Store, ref 3076608492140357, R373.98 incl. shipping. Awaiting delivery |
| Panel buttons order (AliExpress) | ORDERED + PAID | 2 Oct 2026. 10× 16 mm flat-head momentary 1NO, no LED, pre-wired, DIANQI Electric Official Store, ref 3076815630860357, R329.00. Estimated delivery 28 Oct 2026 |
| Spare RFB-0505S | BOUGHT | Supplier and quantity not recorded |
| Buy remaining parts | TODO | Board-to-display connector (choose at layout); optional second T-Display-S3 |
| Bench-test T-Display-S3 USB with Artisan | TODO | Not a blocker; firmware fix and UART fallback known |
| Footprint check before layout | DONE | 7 Oct 2026. DG127 custom footprint; chassis network left out |
| PCB layout | NEXT | Isolation slot and separate ground zone per channel; DG127 pin row 4.2 mm from edge; choose display cable, update J1; review before fab |
| Order PCBs | TODO | JLCPCB |
| Hand-assemble the board | TODO | SOIC-8 MAX31855, SOIC-16W isolators, 0805 passives |
| Port firmware to ESP32-S3 | TODO | 3 channels, TFT pages, page button, TC4 protocol |
| Design + print enclosure | TODO | T-Display-S3 window, panel button, 4-channel board, probe entries |
| Clone repo to RPi | TODO | Old ~/artisan/ dir exists, needs proper clone |
| Sensor calibration | TODO | Ice water + boiling water tests |
| Mount probes in roaster | TODO | BT, ET and FT positions |
| First test roast | TODO | Full integration test |

---

## Financial Summary

### GPA Trading (PO P00041) - Thermocouples

| Item | Qty | Unit Price | Total | Status |
|------|-----|-----------|-------|--------|
| 35mm/2.5mm K-type probe | 2 | R370 | R740 | Delivered |
| 50mm/3.0mm K-type probe | 2 | R395 | R790 | Delivered |
| 70mm/3.0mm K-type probe | 2 | R415 | R830 | Delivered |
| 1/8" SS compression fitting | 6 | R550 | R3,300 | Delivered |
| **Subtotal** | | | **R5,660** | Nett, Ex VAT |
| **VAT (15%)** | | | **R849** | |
| **Total incl. VAT** | | | **R6,509** | |

### Redesign Components (Estimated — March 2026 plan, superseded)

DigiKey isolation parts order of 30 September 2026: placed and paid; order number and total not yet recorded here.

LilyGO T-Display-S3 ×1, AliExpress ref 3076608492140357, 30 September 2026: R344.00 + R29.98 shipping = R373.98, paid by card.

Panel buttons ×10, AliExpress ref 3076815630860357, 2 October 2026: R110.00 goods, R329.00 total, paid by card.

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| MAX31855KASA+ IC | 5 | ~R900 | DigiKey ZA | 2/board × 2 boards + spare |
| ESP32-WROOM-32 USB-C (KS5019) | 1 | R238.20 | Mantech | Dev board for prototyping |
| Keyestudio 20×4 I2C LCD (MD0074) | 1 | R184.47 | Mantech | HD44780 + PCF8574 backpack |
| BSS138 N-MOSFET (SOT-23) | 4 | ~R4 | DigiKey | I2C level shifting (3.3V↔5V) |
| 10nF ceramic caps | 5 | ~R10 | DigiKey | Thermocouple input filter |
| 2-pin screw terminals | 6 | ~R50 | DigiKey | Thermocouple connections |
| Custom PCB | 5 | ~R80-100 | JLCPCB | Bundle with Fairfield order |
| **Estimated Total** | | **~R1,470-1,510** | | |

---

## Key Decisions Made

1. Custom K-type probes from GPA Trading instead of off-the-shelf Olimex (better specs, compression fittings, food-grade 316L SS)
2. TC4 protocol for Artisan integration (command/response, not continuous output)
3. **2-channel system** (revised from 3): BT + ET via shared SPI bus with individual CS lines
4. **Arduino Nano** (revised from UNO R3) — smaller footprint, USB-C
5. Bare tinned wire termination (direct to MAX31855 screw terminals, no connectors)
6. 6 probes ordered (2 of each size) for positioning flexibility and spares
7. USB power from RPi sufficient (~48mA total), no barrel jack needed
8. 100nF ceramic decoupling caps on each MAX31855 VCC/GND
9. 50×70mm veroboard selected (fits enclosure 61×80×23mm better than 60×40mm)
10. Thermocouple assignment: 35mm/2.5mm for BT, 50mm/3.0mm for ET
11. **ESP32-WROOM-32E** replaces Arduino Nano — 3.3V native, WiFi, more GPIO/RAM
12. **Genuine MAX31855KASA+** on custom PCB — knockoff modules unreliable (one smoked)
13. ~~**2.42" OLED** — Adafruit 2719 (SSD1305)~~ **SUPERSEDED** by decision 18
14. **Custom PCB** instead of veroboard — ESP32 + MAX31855 ICs directly on board
15. **Separate PCB** from Fairfield project — different purpose, only 2 boards needed
16. **0805 for all SMD passives** — optimal for hand soldering, matches Fairfield order
17. **5mm pitch screw terminals** for thermocouple connections — easier hand assembly than 3.5mm
18. **20×4 I2C LCD** — Keyestudio MD0074 (HD44780 + PCF8574) replaces OLED — no driver issues, no burn-in, better readability, cheaper
19. **BSS138 level shifters** for 3.3V ESP32 ↔ 5V LCD I2C on custom PCB (direct connection OK for prototype)
20. **MAX31855 breakout board first** — validate thermocouples with dev board before designing full system PCB
21. **Per-breakout galvanic isolation (MD-TC-BRK v1.1)** — probes are grounded-junction; isolated DC-DC + digital isolator on each breakout (22 April 2026)
22. **3 channels again** (BT, ET, FT) — one isolated breakout per probe (April 2026, supersedes decision 3)
23. **LilyGO T-Display-S3** as controller + display — supersedes decisions 4, 11, 14, 18, 19 (30 September 2026)
24. **Single custom 3D-printed enclosure** for T-Display-S3 + thermocouple board, designed and printed in-house (30 September 2026)
25. **One 4-channel thermocouple board** (3 fitted) instead of three breakouts, each channel on its own isolated island — supersedes the separate-breakout part of decision 21 (30 September 2026)
26. **Isolation parts:** ISO7731DWR isolator, Recom RFB-0505S DC-DC, SN74AHC125 MISO buffer, tantalum output capacitor on the NCP1117 (30 September 2026)

---

## Contact Log

| Date | Type | Summary |
|------|------|---------|
| 2026-01-12 | Email | Sent quote request to Sam Hattingh (GPA Trading) for 6 custom K-type probes |
| 2026-01-23 | Email | Sam quoted prices. Jason accepted, mentioned sending full BOM with PO |
| 2026-02-02 | Email | Sent PO P00041 for thermocouples. Quenton needs them urgently |
| 2026-02-02 | Email | Sam confirmed order |
| 2026-02-09 | Email | Jason reminded Sam about invoice + banking details |
| 2026-02-09 | Email | Sam said he'll invoice once goods arrive |
| 2026-02-23 | Email | Jason sent waybill GTRCLK, Courier Guy collecting 24 Feb |
| 2026-02-24 | Email | Sam confirmed courier collected, sent invoice (attached) |
| 2026-02-24 | Email | Jason sent proof of payment |
| 2026-03-04 | Email | Jason sent RFQ for remaining BOM items |
| 2026-03-13 | Email | Sam and Jason agreed remaining BOM not worth supplying via GPA |

---

## Files Reference

- `README.md` - Project overview
- `RESUME.md` - Quick resume context
- `CLAUDE.md` - AI assistant instructions
- `correspondence/` - Supplier correspondence
- `docs/` - Technical documentation
- `kicad/` - KiCad schematic project + generator script
- `3d-prints/` - 3D printable parts (OLED bezel + Printables mounting frame)
- `FreeCad/` - FreeCAD bezel front + back piece projects
- `fritzing/` - Fritzing breadboard layout + imported parts (.fzpz)
