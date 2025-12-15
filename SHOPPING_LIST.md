# Shopping List - Coffee Roaster Temperature Monitor

**Estimated Total: $22-28 USD (AliExpress)**

---

## Required Components

### 1. Arduino Nano V3.0 Clone
| Spec | Value |
|------|-------|
| MCU | ATmega328P |
| USB Chip | CH340 |
| Voltage | 5V |
| Quantity | 1 |
| Est. Price | $2-3 |

**Search terms:**
- AliExpress: `Arduino Nano V3.0 CH340 ATmega328P`
- Temu: `Arduino Nano V3.0 CH340`

**What to look for:**
- Pre-soldered headers (easier to use)
- CH340 USB chip (cheaper, works fine)
- Mini-USB or Micro-USB connector

---

### 2. MAX31855 Thermocouple Module (x2)
| Spec | Value |
|------|-------|
| Type | K-type thermocouple amplifier |
| Range | -200°C to +1350°C |
| Interface | SPI |
| Accuracy | ±2°C |
| Quantity | 2 |
| Est. Price | $4 each ($8 total) |

**Search terms:**
- AliExpress: `MAX31855 K type thermocouple module`
- Temu: `MAX31855 thermocouple module`

**What to look for:**
- Breakout board with screw terminals for thermocouple
- 5-pin header (VCC, GND, SCK, SO/DO, CS)
- Some include a short thermocouple - still buy separate probes

---

### 3. K-type Thermocouple Probes (x2)
| Spec | Value |
|------|-------|
| Type | K-type (Chromel-Alumel) |
| Max Temp | 500°C+ continuous |
| Probe Material | Stainless Steel 316 |
| Probe Diameter | 3mm (recommended) |
| Probe Length | 100-150mm |
| Cable Length | 1-2 meters |
| Quantity | 2 |
| Est. Price | $3 each ($6 total) |

**Search terms:**
- AliExpress: `K type thermocouple 500C stainless steel probe`
- AliExpress: `K type thermocouple high temperature probe 3mm`
- Temu: `K type thermocouple stainless probe`

**What to look for:**
- Stainless steel probe (not bare wire)
- Temperature rating 500°C or higher
- 3mm diameter (good balance of response time and durability)
- Fiberglass insulated cable (heat resistant)
- Standard K-type connector OR bare wires for screw terminals

**Important:** Check that probe length is sufficient to reach into your roaster!

---

### 4. 1.3" OLED Display (128x64, I2C)
| Spec | Value |
|------|-------|
| Size | 1.3 inches diagonal |
| Resolution | 128 x 64 pixels |
| Controller | SH1106 |
| Interface | I2C (4-pin) |
| Voltage | 3.3V - 5V |
| I2C Address | 0x3C |
| Quantity | 1 |
| Est. Price | $3-4 |

**Search terms:**
- AliExpress: `1.3 inch OLED I2C SH1106 128x64`
- AliExpress: `1.3" OLED display module I2C white`
- Temu: `1.3 inch OLED I2C display`

**What to look for:**
- 4-pin version (GND, VCC, SDA, SCL) - NOT 7-pin SPI version
- SH1106 controller (not SSD1306 - different driver)
- White or blue display (white is more readable)

**Alternative:** 0.96" OLED (SSD1306) is cheaper (~$1.50) but smaller

---

### 5. Tactile Push Button
| Spec | Value |
|------|-------|
| Type | Momentary tactile switch |
| Size | 6x6mm |
| Quantity | 1 (or pack of 10-20) |
| Est. Price | $0.50-1 (for pack) |

**Search terms:**
- AliExpress: `tactile push button 6x6mm`
- AliExpress: `micro switch button 6x6`
- Temu: `tactile switch 6x6mm`

**What to look for:**
- 6x6mm size (standard, fits most enclosures)
- 4-pin through-hole
- With or without cap (caps available separately)

---

### 6. Project Enclosure
| Spec | Value |
|------|-------|
| Material | ABS plastic |
| Size | 100mm x 60mm x 25mm (minimum internal) |
| Features | Space for display cutout |
| Quantity | 1-2 (extra for mistakes) |
| Est. Price | $1-3 |

**Recommended Products:**

| Product | Price | Link |
|---------|-------|------|
| ABS DIY Plastic Project Box 100x60x25mm | ~$1.34 | [AliExpress](https://www.aliexpress.com/item/32816989679.html) |
| Screwless Electronic Enclosure 100x60x25mm | ~$2.95 | [AliExpress](https://www.aliexpress.com/item/32777782150.html) |

**Search terms:**
- AliExpress: `100x60x25 project box`
- AliExpress: `ABS enclosure 100x60`
- AliExpress: `arduino nano case`
- AliExpress: `electronic enclosure LCD window`
- Temu: `Arduino enclosure box`

**What to look for:**
- Size to fit Arduino Nano + OLED (at least 100x60x25mm internal)
- Easy to drill/cut for display window and button
- Screw-on lid (not snap-fit, harder to modify)
- Consider buying 2 in case of cutting mistakes

**Cutouts you'll need to make:**

| Cutout | Size | Tool |
|--------|------|------|
| OLED window | ~32 x 20mm | Drill corners + hobby knife |
| Button hole | 6-7mm diameter | Drill bit |
| USB port | ~10 x 8mm slot | Drill + file |
| Thermocouple cables x2 | 5-6mm holes | Drill bit |

---

### 7. Dupont Jumper Wires (Optional)
| Spec | Value |
|------|-------|
| Type | Female-to-Female |
| Length | 10-20cm |
| Quantity | 20-40 wires |
| Est. Price | $1-2 |

**Search terms:**
- AliExpress: `dupont wire female female 20cm`
- Temu: `jumper wire female`

**Note:** Only needed if you don't want to solder. For permanent installation, soldering is recommended.

---

## Shopping Summary

| # | Component | Qty | Est. Price |
|---|-----------|-----|------------|
| 1 | Arduino Nano V3.0 (CH340) | 1 | $2-3 |
| 2 | MAX31855 Module | 2 | $8 |
| 3 | K-type Thermocouple Probe (500°C+) | 2 | $6 |
| 4 | 1.3" OLED Display (SH1106, I2C) | 1 | $3-4 |
| 5 | Tactile Push Button 6x6mm | 1+ | $1 |
| 6 | Project Enclosure | 1 | $2-4 |
| 7 | Dupont Wires (optional) | 1 set | $1-2 |
| | **TOTAL** | | **$23-28** |

---

## Direct Search Links

### AliExpress
- [Arduino Nano V3.0](https://www.aliexpress.com/w/wholesale-arduino-nano-v3.0-ch340.html)
- [MAX31855 Module](https://www.aliexpress.com/w/wholesale-max31855-thermocouple-module.html)
- [K-type Thermocouple Probe](https://www.aliexpress.com/w/wholesale-k-type-thermocouple-500c-stainless.html)
- [1.3" OLED SH1106](https://www.aliexpress.com/w/wholesale-1.3-inch-oled-i2c-sh1106.html)
- [Tactile Button 6x6mm](https://www.aliexpress.com/w/wholesale-tactile-push-button-6x6mm.html)
- [Project Enclosure 100x60x25](https://www.aliexpress.com/w/wholesale-100x60x25-project-box.html)
- [Specific Enclosure Option ($1.34)](https://www.aliexpress.com/item/32816989679.html)

### Temu
- Search: `Arduino Nano V3`
- Search: `MAX31855 thermocouple`
- Search: `K type thermocouple probe`
- Search: `1.3 inch OLED display`
- Search: `tactile push button`
- Search: `electronic project box`

---

## Tips for Ordering

1. **Combine shipping**: Order all from one seller if possible to save on shipping
2. **Check reviews**: Look for items with photos in reviews
3. **Delivery time**: AliExpress typically 2-4 weeks, Temu similar
4. **Order extras**: Consider ordering 2x Arduino Nano and extra buttons (they're cheap)
5. **Thermocouple length**: Measure your roaster before ordering - make sure probes are long enough!

---

## Optional Upgrades

| Item | Purpose | Price |
|------|---------|-------|
| 2.42" OLED | Larger display | +$6-8 |
| Waterproof enclosure | Better protection | +$3-5 |
| Heat shrink tubing | Clean wiring | +$1 |
| Panel mount USB | Clean enclosure connection | +$2 |

---

**Document Version:** 1.0
**Last Updated:** 2025-12-15
