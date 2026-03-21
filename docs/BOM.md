# Bill of Materials (BOM)

Complete parts list for the Milk Depot Coffee Roaster temperature monitoring system.

**Revision 2.0** — ESP32 redesign with genuine MAX31855 ICs on custom PCB.

## Overview

This system uses 2 K-type thermocouples with genuine MAX31855KASA+ thermocouple-to-digital converters connected to an ESP32, which communicates with Artisan roasting software on a Raspberry Pi 4 via USB serial.

**Temperature Channels:**
- **BT (Bean Temperature)**: 35mm/2.5mm probe inside the drum, measures bean mass temperature
- **ET (Exhaust/Environment Temperature)**: 50mm/3.0mm probe in exhaust path, measures air leaving the drum

**Design Decisions:**
- ESP32-WROOM-32E replaces Arduino Nano — 3.3V native (no level shifters for MAX31855), WiFi capability, more GPIO/RAM
- Genuine MAX31855KASA+ ICs (SOIC-8) on custom PCB — knockoff breakout modules proved unreliable (one smoked on first power-up)
- 2.42" OLED (SSD1309) replaces 1.3" SH1106 — 4× screen area, same 128×64 resolution
- All SMD passives are **0805** — optimal size for hand soldering with fine-tip iron or hot air

---

## Thermocouples (Delivered)

**PO P00041 — GPA Trading (Sam Hattingh) — DELIVERED & PAID**

See [THERMOCOUPLE_SPEC.md](THERMOCOUPLE_SPEC.md) and [CUSTOM_TC_ORDER_SPEC.md](CUSTOM_TC_ORDER_SPEC.md) for detailed specifications.

| Qty | Description | Assignment | Unit Price | Total |
|-----|-------------|-----------|-----------|-------|
| 2 | 35mm/2.5mm K-type probe, 1.5m cable, SS316L, grounded | BT (Bean Temp) | R370 | R740 |
| 2 | 50mm/3.0mm K-type probe, 1.5m cable, SS316L, grounded | ET (Exhaust Temp) | R395 | R790 |
| 2 | 70mm/3.0mm K-type probe, 1.5m cable, SS316L, grounded | Spare | R415 | R830 |
| 6 | 1/8" SS compression fitting | Panel mount | R550 | R3,300 |
| | **Subtotal (ex VAT)** | | | **R5,660** |
| | **VAT (15%)** | | | **R849** |
| | **Total incl. VAT** | | | **R6,509** |

Bare tinned wire termination — direct to screw terminals on PCB, no miniature connectors.

---

## ICs — DigiKey ZA

| Qty | MPN | Description | Package | DigiKey PN | Est. Unit | Est. Total |
|-----|-----|-------------|---------|-----------|-----------|-----------|
| 5 | MAX31855KASA+ | K-type thermocouple-to-digital converter | SOIC-8 | MAX31855KASA+-ND | ~R150 | ~R750 |
| 2 | ESP32-WROOM-32E-N4 | WiFi/BT module, 4MB flash | Module | ESP32-WROOM-32E-N4CT-ND | ~R57 | ~R114 |

**MAX31855 qty 5**: 2 per board × 2 boards + 1 spare.
**ESP32 qty 2**: For custom PCB (not dev board). 1 active + 1 spare.

---

## Passive Components — DigiKey ZA (all 0805 SMD)

| Qty | MPN | Value | Specs | DigiKey PN | Purpose |
|-----|-----|-------|-------|-----------|---------|
| 10 | CL21B104KBCNNNC | 100nF | X7R, 50V, ±10% | 1276-1003-1-ND | IC decoupling (VCC to GND) |
| 10 | CL21B103KBANNNC | 10nF | X7R, 50V, ±10% | 1276-1015-1-ND | MAX31855 TC input filter (T+ to T-) |
| 10 | GRM21BR61C106KE15L | 10µF | X5R, 16V, ±10% | 490-3886-1-ND | ESP32 bulk decoupling |
| 10 | RC0805FR-0710KL | 10K Ω | 1%, 1/8W | 311-10.0KCRCT-ND | I2C pull-ups, ESP32 EN/IO0 |

**Why these specific parts:**
- Samsung CL21B series (100nF, 10nF) — widely stocked, consistent quality, good price
- Murata GRM21B series (10µF) — premium MLCC, excellent DC bias characteristics
- Yageo RC0805FR — industry standard thick film resistor, 1% tolerance
- All 0805 (2.0 × 1.25mm) — one size simplifies assembly and ordering
- All passives shared with Fairfield project DigiKey order (100 qty each)

---

## Connectors — DigiKey ZA (through-hole)

| Qty | MPN | Description | Pitch | DigiKey PN | Purpose |
|-----|-----|-------------|-------|-----------|---------|
| 6 | 1725656 | 2-pin screw terminal | 5.0mm | 277-1247-ND | Thermocouple wire connections |
| 5 | B3F-1000 | Tactile switch, 6×6mm | - | SW400-ND | OLED page button |
| 3 | - | 4-pin 2.54mm pin header | 2.54mm | - | OLED display connector |

**Screw terminal qty 6**: 2 per board × 2 boards + 2 spares. 5mm pitch chosen for hand-assembly ease.

---

## Dev Board — Mantech (Prototyping)

| Qty | Product | Stock Code | Price (ex VAT) |
|-----|---------|-----------|---------------|
| 1 | Keyestudio KS5019 ESP32-WROOM-32 USB-C 38-pin | ME106299 | R238.20 |

For prototyping before custom PCB arrives. Has USB-C, 3.3V LDO, USB-UART bridge, boot button — everything needed to test firmware and MAX31855 ICs.

---

## Display — DigiKey ZA (Adafruit)

| Qty | MPN | Description | Controller | DigiKey PN | Est. Price |
|-----|-----|-------------|-----------|-----------|-----------|
| 1 | 2719 | Adafruit 2.42" 128×64 OLED Module Kit | SSD1305 | 1528-1591-ND | ~R460-550 |

Upgrade from 1.3" SH1106. Same 128×64 resolution, ~4× screen area. Premium Adafruit quality with bezel, 4 mounting holes, and standard 2.54mm header. Uses `Adafruit_SSD1305` library (same GFX API as SSD1306, only init object changes). Adding to DigiKey order avoids a separate purchase.

---

## Prototyping Supplies

| Qty | Description | Source | Est. Price |
|-----|-------------|--------|-----------|
| 5-10 | SOIC-8 to DIP adapter PCBs | AliExpress | ~R20-40 pack |
| 1 | Breadboard (if needed) | On hand | R0 |
| 1 | Jumper wire kit | On hand | R0 |

SOIC-8 adapters needed because MAX31855KASA+ cannot be breadboarded directly. Solder IC + decoupling cap to adapter, then plug into breadboard for prototype testing.

---

## Custom PCBs — JLCPCB (Future)

| Qty | Description | Est. Price |
|-----|-------------|-----------|
| 5 | MAX31855 breakout PCB (small, SOIC-8 + caps + screw terminal) | ~R40-50 |
| 5 | Main ESP32 system PCB (full integration) | ~R80-100 |

Breakout PCB ordered first for prototyping. Main PCB designed after prototype validation.

---

## Enclosure & Mounting

| Qty | Description | Supplier | Est. Price |
|-----|-------------|----------|-----------|
| 1 | ABS project box (~150×100×50mm or larger) | Communica / Mantech | R80-120 |
| 1 | Cable gland PG9 (USB cable entry) | Communica / Builders | R15 |
| 4 | M3 standoffs, 10mm brass | Communica | R20 (pack) |
| 1 | Heat shrink tubing, assorted | Communica | R25 |

Enclosure may need to be larger than originally planned to accommodate 2.42" OLED (wider than 1.3").

---

## Cost Summary

| Category | Est. Cost (ZAR) | Status |
|----------|----------------|--------|
| Thermocouples + fittings (GPA Trading) | R6,509 incl VAT | **Paid** |
| MAX31855KASA+ × 5 (DigiKey) | ~R750 | Pending |
| ESP32-WROOM-32E-N4 × 2 (DigiKey) | ~R114 | Pending |
| Passive components (DigiKey) | ~R50 | Pending |
| Connectors (DigiKey) | ~R100 | Pending |
| ESP32 dev board (Mantech) | ~R274 incl VAT | Pending |
| Adafruit 2.42" OLED (DigiKey) | ~R460-550 | Pending |
| Prototyping supplies | ~R40 | Pending |
| Custom PCBs (JLCPCB) | ~R120-150 | Future |
| Enclosure & mounting | ~R140 | Future |
| **DigiKey order subtotal** | **~R1,474-1,564** | |
| **Total new components** | **~R1,830-1,960** | |
| **Project total (incl. thermocouples)** | **~R8,340-R8,470** | |

*DigiKey ZA: Free delivery on orders over R2,000. Combining with Fairfield project order to reach threshold.*
*Raspberry Pi 4 already owned, not included.*

---

## DigiKey Order Checklist

Combined order with Fairfield project for R2,000 free shipping threshold.

**Already in cart (shared with Fairfield, covers roaster needs):**
- [x] ~~MAX31855KASA+-ND × 10~~ (roaster uses 5)
- [x] ~~1965-ESP32-WROOM-32E-N4CT-ND × 13~~ (roaster uses 2)
- [x] ~~1276-1003-1-ND × 100~~ (100nF 0805, roaster uses ~10)
- [x] ~~1276-1015-1-ND × 100~~ (10nF 0805, roaster uses ~10)
- [x] ~~490-3886-1-ND × 100~~ (10µF 0805, roaster uses ~10)
- [x] ~~311-10.0KCRCT-ND × 100~~ (10K 0805, roaster uses ~10)
- [x] ~~NCP1117ST33T3GOSCT-ND × 10~~ (3.3V LDO, roaster uses ~2)
- [x] ~~1727-4043-1-ND × 20~~ (MMBT2222A, roaster uses ~4)
- [x] ~~EG2531CT-ND × 30~~ (tactile switch SMD, roaster uses ~3)

**Still need to add to cart:**
- [ ] 277-1247-ND × 6 (2-pin 5mm screw terminal, Phoenix Contact 1725656)
- [ ] 1528-1591-ND × 1 (Adafruit 2.42" OLED module 2719)

**Note**: Verify all DigiKey part numbers before ordering — prices and stock change frequently.

---

## Pin Assignment (ESP32)

Pin assignments for custom PCB (final GPIO allocation during KiCad design):

| ESP32 GPIO | Function | Connected To |
|-----------|----------|--------------|
| VSPI SCK (GPIO 18) | SPI Clock | Both MAX31855 SCK (shared) |
| VSPI MISO (GPIO 19) | SPI Data | Both MAX31855 DO (shared) |
| GPIO 5 | CS_BT | MAX31855 #1 CS (Bean Temp) |
| GPIO 17 | CS_ET | MAX31855 #2 CS (Exhaust Temp) |
| GPIO 21 | I2C SDA | OLED SDA (+ 10K pull-up to 3.3V) |
| GPIO 22 | I2C SCL | OLED SCL (+ 10K pull-up to 3.3V) |
| GPIO 4 | Button | Tactile switch to GND (internal pull-up) |
| 3V3 | Power | MAX31855 VCC, OLED VCC |
| GND | Ground | All GND |

**Notes:**
- ESP32 is 3.3V native — MAX31855 operates at 3.0-3.6V, no level shifting needed
- VSPI is the default SPI bus on ESP32 (HSPI also available if needed)
- GPIO 21/22 are the default I2C pins on ESP32
- Avoid GPIO 6-11 (connected to internal flash on WROOM modules)

---

## Wiring Diagram

```
                                    +------------------+
                                    |   RASPBERRY PI   |
                                    |       USB        |
                                    +--------+---------+
                                             |
                                        USB-C Cable
                                             |
+---------------------------+       +--------+---------+
|      ENCLOSURE            |       | ESP32-WROOM-32E  |
|                           |       |                  |
|  +-----------+            |       | GPIO18 ---+----- | ---> SCK (shared)
|  | MAX31855  |            |       | GPIO19 ---+----- | ---> MISO (shared)
|  | #1 (BT)   |           |       | GPIO5  --------- | ---> CS_BT
|  | SOIC-8    |            |       | GPIO17 --------- | ---> CS_ET
|  +-----+-----+            |       | GPIO21 --------- | ---> OLED SDA
|        |                  |       | GPIO22 --------- | ---> OLED SCL
|  +-----------+            |       | GPIO4  --------- | ---> Button
|  | MAX31855  |  +------+  |       | 3V3  ----+----- | ---> VCC (shared)
|  | #2 (ET)   |  | OLED |  |       | GND  ----+----- | ---> GND (shared)
|  | SOIC-8    |  | 2.42"|  |       +------------------+
|  +-----+-----+  +------+  |
|        |                   |
+--------+-------------------+
         |
    5mm Screw Terminals
         |
   +-----+-----+  +-----+-----+
   | TC BT      |  | TC ET      |
   | 35mm/2.5mm |  | 50mm/3.0mm |
   +------------+  +------------+
   (1.5m leads to roaster)
```

---

## Supplier Quick Reference (South Africa)

| Supplier | Website | Use For |
|----------|---------|---------|
| DigiKey ZA | digikey.co.za | ICs, passives, connectors (primary) |
| Mantech | mantech.co.za | ESP32 dev boards, modules |
| RS Components | za.rs-online.com | Industrial connectors, alternative ICs |
| Communica | communica.co.za | Enclosures, general electronics |
| JLCPCB | jlcpcb.com | Custom PCB fabrication |
| AliExpress | aliexpress.com | OLED displays, adapter boards |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-30 | Initial 3-channel Arduino UNO design |
| 2.0 | 2026-03-20 | ESP32 redesign: genuine MAX31855KASA+, 0805 passives, 2.42" OLED, custom PCB |
