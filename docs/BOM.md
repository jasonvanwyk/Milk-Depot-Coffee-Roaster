# Bill of Materials (BOM)

Complete parts list for the Milk Depot Coffee Roaster temperature monitoring system.

## Overview

This system uses 3 K-type thermocouples with MAX31855 amplifier modules connected to an Arduino UNO, which communicates with Artisan roasting software on a Raspberry Pi 4.

**Temperature Channels:**
- **BT (Bean Temperature)**: Probe inside the drum, measures bean mass temperature
- **ET (Exhaust/Environment Temperature)**: Probe in exhaust path, measures air leaving the drum
- **FT (Flame Temperature)**: Probe near burner, measures heat source temperature

## Core Components

### Thermocouples

**See [THERMOCOUPLE_SPEC.md](THERMOCOUPLE_SPEC.md) for detailed specifications.**

| Qty | Description | Supplier Options | Est. Price (ZAR) |
|-----|-------------|------------------|------------------|
| 3 | K-Type Thermocouple Probe, 3mm dia, 150mm length, 1.5m cable, SS316 sheath, grounded, miniature connector | RS Components / Thermon SA / Thermocouple Products | R200-600 each |

**Recommended Sources:**
- **RS Components**: Part# 3971264 (Type K MI, 150mm, 3mm) - [za.rs-online.com](https://za.rs-online.com/web/p/thermocouples/3971264)
- **Thermon SA**: Custom manufacture - 011 966 9800 (JHB) / 021 762 8995 (CPT)
- **Thermocouple Products**: Custom manufacture - [thermocoupleproducts.co.za](https://thermocoupleproducts.co.za)

**Critical Requirements:**
- Insertion/probe style (NOT surface mount)
- 3mm diameter stainless steel sheath
- Miniature K-type connector (yellow, flat blade)

### Thermocouple Amplifiers

| Qty | Part Number | Description | Supplier | Unit Price (ZAR) | Total (ZAR) |
|-----|-------------|-------------|----------|------------------|-------------|
| 3 | MAX31855 Module | K-Type Thermocouple Amplifier Breakout, SPI interface | AliExpress / Communica / DIYElectronics | ~R50-80 | ~R150-240 |

**Notes:**
- MAX31855 modules typically include the miniature K-type socket
- Ensure modules have the standard pinout: VCC, GND, SCK, CS, DO (MISO)
- Alternative: Adafruit MAX31855 breakout (more expensive but higher quality)

### Microcontroller

| Qty | Part Number | Description | Supplier | Unit Price (ZAR) | Total (ZAR) |
|-----|-------------|-------------|----------|------------------|-------------|
| 1 | Arduino UNO R3 | ATmega328P microcontroller, already owned | - | R0 | R0 |

### Display (Optional - for standalone readout)

| Qty | Part Number | Description | Supplier | Unit Price (ZAR) | Total (ZAR) |
|-----|-------------|-------------|----------|------------------|-------------|
| 1 | SSD1306 OLED | 0.96" 128x64 I2C OLED Display | AliExpress / Communica | ~R40-60 | ~R40-60 |

## Enclosure & Mounting

| Qty | Part Number | Description | Supplier | Est. Price (ZAR) |
|-----|-------------|-------------|----------|------------------|
| 1 | ABS Project Box | ~150x100x50mm, for Arduino + amplifiers | Communica / Mantech | ~R80-120 |
| 3 | Panel Mount K-Type Socket | Female miniature K-type connector, panel mount | RS Components / DigiKey | ~R30-50 each |
| 1 | Cable Gland PG9 | For USB cable entry | Communica / Builders | ~R15 |
| 4 | M3 Standoffs | 10mm brass standoffs for Arduino mounting | Communica | ~R20 (pack) |
| 1 | Prototype PCB | 5x7cm perfboard for amplifier mounting | Communica | ~R15 |

## Wiring & Connectors

| Qty | Description | Supplier | Est. Price (ZAR) |
|-----|-------------|----------|------------------|
| 1 | Jumper Wire Kit | Male-Female, Female-Female Dupont wires | Communica / AliExpress | ~R40 |
| 1 | USB A-B Cable | 2m, Arduino to Raspberry Pi | Any electronics store | ~R30 |
| 1 | Heat Shrink Tubing | Assorted sizes | Communica | ~R25 |

## Tools Required (not included in BOM)

- Soldering iron + solder
- Wire strippers
- Drill with step bit (for enclosure holes)
- Multimeter

---

## Cost Summary

| Category | Estimated Cost (ZAR) |
|----------|----------------------|
| Thermocouples (3x) | R121 |
| MAX31855 Modules (3x) | R150-240 |
| OLED Display | R40-60 |
| Enclosure & Mounting | R200-300 |
| Wiring & Connectors | R95 |
| **TOTAL** | **R606 - R816** |

*Note: Arduino UNO R3 and Raspberry Pi 4 already owned, not included in total.*

---

## Supplier Quick Reference (South Africa)

| Supplier | Website | Notes |
|----------|---------|-------|
| DigiKey ZA | digikey.co.za | Thermocouples, high-quality components |
| Communica | communica.co.za | General electronics, enclosures |
| Mantech | mantech.co.za | Arduino, sensors, modules |
| DIYElectronics | diyelectronics.co.za | Arduino ecosystem |
| RS Components | za.rs-online.com | Industrial connectors |
| Micro Robotics | robotics.org.za | Arduino, sensors |
| NetRam | netram.co.za | Components, tools |

---

## Pin Assignment

### Arduino UNO R3 Pinout

| Pin | Function | Connected To |
|-----|----------|--------------|
| 5V | Power | All MAX31855 VCC |
| GND | Ground | All MAX31855 GND, OLED GND |
| D13 | SPI SCK | All MAX31855 SCK (shared) |
| D12 | SPI MISO | All MAX31855 DO (shared) |
| D10 | CS - BT | MAX31855 #1 CS (Bean Temp) |
| D9 | CS - ET | MAX31855 #2 CS (Exhaust Temp) |
| D8 | CS - FT | MAX31855 #3 CS (Flame Temp) |
| A4 | I2C SDA | OLED SDA (optional) |
| A5 | I2C SCL | OLED SCL (optional) |

### SPI Bus (Shared)

All three MAX31855 modules share:
- **SCK** (Clock): Arduino D13
- **MISO/DO** (Data Out): Arduino D12

Each module has its own Chip Select:
- **CS_BT**: D10 (Bean Temperature)
- **CS_ET**: D9 (Exhaust Temperature)
- **CS_FT**: D8 (Flame Temperature)

---

## Wiring Diagram (Text Description)

```
                                    +------------------+
                                    |   RASPBERRY PI   |
                                    |       USB        |
                                    +--------+---------+
                                             |
                                        USB Cable
                                             |
+---------------------------+       +--------+---------+
|      ENCLOSURE            |       |   ARDUINO UNO    |
|                           |       |                  |
|  +-------+  +-------+     |       |  D13 ----+------ | ---> SCK (shared)
|  |MAX31855| |MAX31855|    |       |  D12 ----+------ | ---> MISO (shared)
|  |  BT    | |  ET    |    |       |  D10 ----------- | ---> CS_BT
|  +---+----+ +---+----+    |       |  D9  ----------- | ---> CS_ET
|      |          |         |       |  D8  ----------- | ---> CS_FT
|  +---+----+ +---+----+    |       |  5V  ----+------ | ---> VCC (shared)
|  |MAX31855| | OLED   |    |       |  GND ----+------ | ---> GND (shared)
|  |  FT    | |Display |    |       |  A4  ----------- | ---> OLED SDA
|  +---+----+ +---+----+    |       |  A5  ----------- | ---> OLED SCL
|      |          |         |       +------------------+
+------+----------+---------+
       |          |
   Panel Mount K-Type Sockets
       |          |
   +---+---+  +---+---+  +---+---+
   | TC BT |  | TC ET |  | TC FT |
   +-------+  +-------+  +-------+
   (1.5m leads to roaster)
```

---

## Assembly Notes

1. **Enclosure Layout**: Position Arduino on one side, MAX31855 modules on perfboard in center, panel-mount sockets on front face.

2. **Thermocouple Routing**: The 1.5m leads allow flexible positioning. Route away from high-heat areas except at the probe tip.

3. **Grounding**: Use star grounding - all GND wires meet at a single point to reduce noise.

4. **SPI Wiring**: Keep SCK and MISO wires short and away from power lines to minimize interference.

5. **Probe Placement**:
   - **BT**: Insert into drum through existing port, tip in bean mass
   - **ET**: Position in exhaust duct, 10-15cm from drum exit
   - **FT**: Position near burner, protected from direct flame contact

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-30 | Initial 3-channel thermocouple design |
