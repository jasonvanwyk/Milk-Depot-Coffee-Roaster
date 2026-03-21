# Project Status - Milk Depot Coffee Roaster

**Last Updated:** 2026-03-20
**Quote Ref:** PO P00041 (thermocouples)
**Status:** Development
**Payment Terms:** Invoice on delivery (GPA Trading)

---

## Current Phase: Development

**REDESIGN IN PROGRESS.** First hardware build revealed knockoff MAX31855 module failure (smoke on power-up). Pivoting to ESP32-WROOM-32E + genuine MAX31855KASA+ ICs on custom PCB + 2.42" Adafruit OLED (SSD1305). BOM v2.0 complete with specific 0805 part numbers. DigiKey cart nearly complete — all passives and ICs in shared Fairfield order, only screw terminals + OLED still to add. Awaiting order placement.

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
| OLED display selected | 2026-03-20 | Adafruit 2719 (SSD1305), DigiKey 1528-1591-ND |

### Session Completed Items (20 Mar 2026)
- [x] ~~Rewrote docs/BOM.md v2.0 for ESP32 redesign with specific 0805 part numbers~~
- [x] ~~Cross-referenced DigiKey cart CSV — all passives already in Fairfield combined order~~
- [x] ~~Selected Adafruit 2719 OLED (SSD1305) over Waveshare SSD1309 — quality + standard header~~
- [x] ~~Confirmed 0805 for all passives (not 0603) — matches Fairfield order~~
- [x] ~~Identified only 2 items still needed in DigiKey cart: screw terminals + OLED~~
- [x] ~~Updated DigiKey checklist with in-cart vs still-short items~~

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| Add 2 items to DigiKey cart + place order | TODO | 277-1247-ND (screw terminals) + 1528-1591-ND (Adafruit OLED) |
| Buy ESP32 dev board from Mantech | TODO | KS5019, R238.20 ex-VAT, stock ME106299 |
| Design custom PCB | TODO | KiCad: bare ESP32 + 2× MAX31855 + OLED header + button + support circuitry |
| Order PCBs | TODO | JLCPCB, after KiCad design complete |
| Port firmware to ESP32 | TODO | Pin reassignment, ESP32 Arduino core |
| Hand-assemble PCBs | TODO | SOIC-8 MAX31855, passives, headers |
| Clone repo to RPi | TODO | Old ~/artisan/ dir exists, needs proper clone |
| Sensor calibration | TODO | Ice water + boiling water tests |
| Mount probes in roaster | TODO | BT + ET positions |
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

### Redesign Components (Estimated)

| Item | Qty | Est. Cost | Source | Notes |
|------|-----|-----------|--------|-------|
| MAX31855KASA+ IC | 5 | ~R900 | DigiKey ZA | 2/board × 2 boards + spare |
| ESP32-WROOM-32 USB-C (KS5019) | 1 | R238.20 | Mantech | Dev board for prototyping |
| Adafruit 2719 OLED 2.42" (SSD1305) | 1 | ~R460-550 | DigiKey ZA | Premium, standard header |
| 10nF ceramic caps | 5 | ~R10 | DigiKey | Thermocouple input filter |
| 2-pin screw terminals | 5 | ~R50 | DigiKey | Thermocouple connections |
| Custom PCB | 5 | ~R80-100 | JLCPCB | Bundle with Fairfield order |
| **Estimated Total** | | **~R1,830-1,960** | | |

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
13. **2.42" OLED** — Adafruit 2719 (SSD1305) replaces 1.3" SH1106 — premium quality, standard header, `Adafruit_SSD1305` library
14. **Custom PCB** instead of veroboard — ESP32 + MAX31855 ICs directly on board
15. **Separate PCB** from Fairfield project — different purpose, only 2 boards needed
16. **0805 for all SMD passives** — optimal for hand soldering, matches Fairfield order
17. **5mm pitch screw terminals** for thermocouple connections — easier hand assembly than 3.5mm

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
