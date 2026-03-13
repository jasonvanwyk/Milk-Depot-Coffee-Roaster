# Project Status - Milk Depot Coffee Roaster

**Last Updated:** 2026-03-13
**Quote Ref:** PO P00041 (thermocouples)
**Status:** Development
**Payment Terms:** Invoice on delivery (GPA Trading)

---

## Current Phase: Development

All components procured. RPi networked via SSH. KiCad schematic created for actual components (Arduino Nano, 2x MAX31855, OLED, decoupling caps). OLED bezel redesigned in FreeCAD with caliper-verified measurements. Ready for hardware assembly.

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

### Session Completed Items
- [x] ~~Rendered OpenSCAD bezel — STL export + 4-angle PNG previews~~
- [x] ~~Reviewed 3D print settings for bezel (Tough PLA, modified Strong preset)~~
- [x] ~~Started FreeCAD bezel redesign with real caliper measurements~~
- [x] ~~PCB outline sketch: 35.5×33.6mm rect + 4× 3mm mounting holes (Essentra 27PIF0045B)~~
- [x] ~~Bezel face sketch: 41.5×39.6mm (3mm border), padded 1.6mm~~
- [x] ~~Window cutout sketch: 35×19mm, positioned from actual OLED screen measurements~~

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| Complete FreeCAD bezel | In Progress | Pocket window, PCB shelf walls, snap tabs remaining |
| Create WireViz wiring diagram | TODO | YAML definition for build instructions |
| Clone repo to RPi | TODO | Old ~/artisan/ dir exists, needs proper clone |
| Update firmware for Nano | TODO | Change board type, 2-channel config |
| Hardware assembly | TODO | 50×70mm veroboard, all components on hand |
| Enable MAX31855 in firmware | TODO | Uncomment library code, recompile |
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

### Remaining Components (Estimated)

| Item | Est. Cost | Notes |
|------|-----------|-------|
| 3x MAX31855 modules | R150-240 | Communica / AliExpress |
| Enclosure + mounting | R175-275 | ABS box, standoffs, glands |
| Wiring + assembly | R85-140 | Jumpers, perfboard, USB cable |
| OLED display (optional) | R40-60 | SSD1306 |
| **Estimated Total** | **R450-715** | |

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
- `3d-prints/` - 3D printable parts (OLED bezel — OpenSCAD + STL)
- `FreeCad/` - FreeCAD bezel project (active design, WIP)
