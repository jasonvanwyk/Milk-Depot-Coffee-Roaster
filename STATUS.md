# Project Status - Milk Depot Coffee Roaster

**Last Updated:** 2026-02-23
**Quote Ref:** PO P00041 (thermocouples)
**Status:** Hardware Procurement
**Payment Terms:** Invoice on delivery (GPA Trading)

---

## Current Phase: Hardware Procurement

Software stack is 100% complete and tested. Custom thermocouple probes ordered from GPA Trading (PO P00041, Feb 2 2026). Awaiting delivery and invoice. Remaining BOM items (MAX31855 modules, enclosure, wiring) still to be ordered.

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

### In Progress

| Task | Status | Notes |
|------|--------|-------|
| Thermocouple delivery | IN TRANSIT | Sam receiving stock today (Feb 23), Courier Guy collecting same day |
| Arrange Courier Guy collection | DONE | Courier Guy dispatched to collect from Sam (Feb 23) |
| Remaining BOM procurement | PENDING | MAX31855 modules, enclosure, wiring - awaiting 3rd party quotes |

### Awaiting Supplier

| Task | Status | Notes |
|------|--------|-------|
| Invoice + banking details from GPA Trading | WAITING | Reminded Sam on Feb 9 |

### Future Work

| Task | Status | Notes |
|------|--------|-------|
| Hardware assembly | TBC | After all components arrive |
| Enable MAX31855 in firmware | TBC | Uncomment library code, recompile |
| Sensor calibration | TBC | Ice water + boiling water tests |
| Mount probes in roaster | TBC | BT, ET, FT positions |
| First test roast | TBC | Full integration test |

---

## Financial Summary

### GPA Trading (PO P00041) - Thermocouples

| Item | Qty | Unit Price | Total | Status |
|------|-----|-----------|-------|--------|
| 35mm/2.5mm K-type probe | 2 | R370 | R740 | Ordered |
| 50mm/3.0mm K-type probe | 2 | R395 | R790 | Ordered |
| 70mm/3.0mm K-type probe | 2 | R415 | R830 | Ordered |
| 1/8" SS compression fitting | 6 | R550 | R3,300 | Ordered |
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
3. 3-channel system: ET, BT, FT via shared SPI bus with individual CS lines
4. Bare tinned wire termination (direct to MAX31855 screw terminals, no connectors)
5. 6 probes ordered (2 of each size) for positioning flexibility and spares

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

---

## Files Reference

- `README.md` - Project overview
- `RESUME.md` - Quick resume context
- `CLAUDE.md` - AI assistant instructions
- `correspondence/` - Supplier correspondence
- `docs/` - Technical documentation
