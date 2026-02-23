# Shopping List - Milk Depot Coffee Roaster

Printable shopping list for the 3-channel thermocouple temperature monitoring system.

**Date**: December 2024
**Project**: Milk Depot Coffee Roaster Temperature Monitor
**Budget Estimate**: R800 - R1,500 (depending on thermocouple source)

---

## Priority 1: Thermocouples (CRITICAL - Get These Right!)

**Required Specification:**
- K-type insertion probe (NOT surface mount)
- 3mm diameter stainless steel sheath
- 100-150mm probe length
- 1.5m cable with miniature K-type connector
- Grounded junction preferred

See [THERMOCOUPLE_SPEC.md](THERMOCOUPLE_SPEC.md) for detailed specifications.

### Option A: RS Components South Africa (Recommended)

| Qty | RS Part # | Description | Price Est. | Notes |
|-----|-----------|-------------|------------|-------|
| 3 | 3971264 | Type K MI Thermocouple, 150mm, 3mm dia, +1100°C | ~R400-600 ea | **Best match** - mineral insulated, flexible |

**Website**: [za.rs-online.com](https://za.rs-online.com/web/p/thermocouples/3971264)
**Phone**: 011 691 9300

**Alternative RS options:**
- 7877848: Type K MI, 1.5m length, 3mm dia (longer probe)
- 3428990: Type K Air Probe, 110mm, 4mm dia (slightly thicker)

### Option B: Custom Manufacture - Thermon South Africa

**Best for exact specifications - can make to order.**

| Contact | Details |
|---------|---------|
| Johannesburg | +27 11 966 9800 |
| Cape Town | +27 21 762 8995 |
| Email | salessa@energisolutionsafrica.com |
| Website | [thermon.co.za](https://www.thermon.co.za) |

**Capabilities:**
- Custom thermocouples to your spec
- Mineral insulated down to 0.5mm diameter
- "SOS" fast turnaround service
- All types: J, K, T, R, S, PT100

**Request quote using template in THERMOCOUPLE_SPEC.md**

### Option C: Custom Manufacture - Thermocouple Products (Pty) Ltd

**Local manufacturer in Edenvale (Gauteng)**

| Contact | Details |
|---------|---------|
| Location | Edenvale, Gauteng |
| Website | [thermocoupleproducts.co.za](https://thermocoupleproducts.co.za) |
| Specialty | Custom thermocouples for any industry |

**Request quote using template in THERMOCOUPLE_SPEC.md**

### Option D: Ready-Made (Higher Price)

| Supplier | Product | Price | Notes |
|----------|---------|-------|-------|
| Ecotao Store | Type K 150mm, 4.5mm dia | R665 | Slightly thick but available |
| Hanna SA | HI766E2 220mm, 5mm dia | R2,639 | Expensive, includes handle |

**Ecotao**: [ecotao-store.co.za](https://www.ecotao-store.co.za/shop/laboratory/thermometers/datalogging-thermometer/type-k-heavy-duty-thermocouple-150mm-length-4-5mm-diameter-350c/)

### Thermocouple Cost Estimate

| Source | Unit Price | Qty 3 Total |
|--------|------------|-------------|
| RS Components | R400-600 | R1,200-1,800 |
| Custom (Thermon) | R200-400 est. | R600-1,200 |
| Ecotao | R665 | R1,995 |

---

## Priority 2: Thermocouple Amplifiers

| Qty | Item | Description | Est. Price Each | Total |
|-----|------|-------------|-----------------|-------|
| 3 | MAX31855 Module | K-Type thermocouple amp, SPI interface | R50-80 | R150-240 |

**Where to buy** (check stock/prices):
- [ ] Communica: [communica.co.za](https://www.communica.co.za) (search "MAX31855")
- [ ] Micro Robotics: [robotics.org.za](https://www.robotics.org.za)
- [ ] DIY Electronics: [diyelectronics.co.za](https://www.diyelectronics.co.za)
- [ ] Netram: [netram.co.za](https://www.netram.co.za)
- [ ] AliExpress (longer shipping): search "MAX31855 module"

**Important**: Ensure modules have miniature K-type socket (yellow, flat blade style)

---

## Priority 3: Enclosure & Mounting

| Qty | Item | Description | Est. Price | Notes |
|-----|------|-------------|------------|-------|
| 1 | ABS Project Box | 150x100x50mm (approx) | R80-120 | Black or gray |
| 3 | Panel Mount K-Type Socket | Female miniature thermocouple connector | R30-50 each | Optional but recommended |
| 1 | Cable Gland PG9 | For USB cable entry | R15-25 | Or use rubber grommet |
| 1 | Pack M3 Standoffs | Brass, 10mm, for Arduino mount | R20-30 | Pack of 4+ |

**Where to buy**:
- [ ] Communica: [communica.co.za](https://www.communica.co.za)
- [ ] Mantech: [mantech.co.za](https://www.mantech.co.za)
- [ ] Builders Warehouse (cable glands)
- [ ] RS Components: [za.rs-online.com](https://za.rs-online.com) (panel mount connectors)

**Subtotal: ~R175-275**

---

## Priority 4: Wiring & Assembly

| Qty | Item | Description | Est. Price |
|-----|------|-------------|------------|
| 1 | Jumper Wire Kit | Male-Female + Female-Female Dupont, 20cm | R30-50 |
| 1 | Perfboard 5x7cm | For mounting MAX31855 modules | R10-20 |
| 1 | Heat Shrink Kit | Assorted sizes | R20-30 |
| 1 | USB A-B Cable 2m | Arduino to Raspberry Pi | R25-40 |

**Subtotal: ~R85-140**

---

## Priority 5: Optional Extras

| Qty | Item | Description | Est. Price | Notes |
|-----|------|-------------|------------|-------|
| 1 | SSD1306 OLED | 0.96" 128x64 I2C display | R40-60 | Local temperature readout |
| 1 | Power LED + Resistor | 5mm green LED + 220Ω | R5 | Power indicator |

**Subtotal: ~R45-65**

---

## Budget Summary

| Category | Budget Option | Premium Option |
|----------|---------------|----------------|
| Thermocouples (3x) | R600 (custom) | R1,800 (RS) |
| Amplifiers (3x) | R150 | R240 |
| Enclosure & Mounting | R175 | R275 |
| Wiring & Assembly | R85 | R140 |
| Optional Extras | R0 | R65 |
| **TOTAL** | **R1,010** | **R2,520** |

---

## Quick Shopping Checklist

### Step 1: Thermocouples (do this first - longest lead time)

**Option A - RS Components Order:**
- [ ] 3x RS Part# 3971264 (Type K MI, 150mm, 3mm)
- [ ] Or browse: [za.rs-online.com/thermocouples](https://za.rs-online.com/web/c/automation-control-gear/sensors/thermocouples/)

**Option B - Custom Quote:**
- [ ] Email Thermon SA: salessa@energisolutionsafrica.com
- [ ] Or call: 011 966 9800 (JHB) / 021 762 8995 (CPT)
- [ ] Use quote template from THERMOCOUPLE_SPEC.md

### Step 2: Electronics (Communica/Netram/etc)
- [ ] 3x MAX31855 thermocouple amplifier module
- [ ] 1x Jumper wire kit (Dupont cables)
- [ ] 1x Perfboard 5x7cm
- [ ] 1x Heat shrink tubing assortment
- [ ] 1x Pack M3 brass standoffs 10mm
- [ ] 1x USB A-B cable 2m
- [ ] (Optional) 1x SSD1306 0.96" OLED display

### Step 3: Enclosure (Communica/Mantech/Builders)
- [ ] 1x ABS project box ~150x100x50mm
- [ ] 1x Cable gland PG9 (or rubber grommet)
- [ ] (Optional) 3x Panel mount K-type socket

---

## Supplier Contact Directory

### Thermocouples (Custom/Industrial)

| Supplier | Phone | Website | Notes |
|----------|-------|---------|-------|
| Thermon SA (JHB) | 011 966 9800 | thermon.co.za | Custom manufacture |
| Thermon SA (CPT) | 021 762 8995 | thermon.co.za | Custom manufacture |
| Thermocouple Products | - | thermocoupleproducts.co.za | Edenvale, custom |
| RS Components | 011 691 9300 | za.rs-online.com | Stock items |
| Temperature Controls | - | tempcon.co.za | Since 1952 |

### Electronics

| Supplier | Phone | Website |
|----------|-------|---------|
| Communica | 011 792 7646 | communica.co.za |
| Mantech | 011 452 1935 | mantech.co.za |
| Netram | - | netram.co.za |
| Micro Robotics | - | robotics.org.za |
| DIY Electronics | - | diyelectronics.co.za |

### Enclosures & Hardware

| Supplier | Website |
|----------|---------|
| Communica | communica.co.za |
| Mantech | mantech.co.za |
| Builders Warehouse | builders.co.za |

---

## Important Notes

### Thermocouple Selection Criteria

**MUST HAVE:**
- [x] K-type (Chromel/Alumel)
- [x] Insertion/probe style with stainless steel sheath
- [x] Closed tip (not exposed wires)
- [x] 2-4mm probe diameter (3mm ideal)
- [x] Miniature K-type connector (flat blade, yellow)
- [x] 1m+ cable length

**AVOID:**
- Surface mount / washer / ring style
- Exposed junction (bare wires)
- Probes thicker than 6mm (too slow)
- "Air probes" with plastic handles

### Why 3mm Diameter Matters

From coffee roasting research ([Barista Hustle](https://www.baristahustle.com/lesson/htr-1-06-temperature-probes/), [Scott Rao](https://www.scottrao.com/blog/be-careful-when-interpreting-bean-data)):

| Diameter | Response | Coffee Roasting Suitability |
|----------|----------|----------------------------|
| 1.5mm | Very fast | Fragile, may break |
| **3mm** | **Fast (4-6s)** | **Ideal balance** |
| 5mm | Medium (8-12s) | Acceptable |
| 6mm+ | Slow (15s+) | Too much thermal lag |

Thicker probes cause "thermal lag" which:
- Delays detection of first crack
- Smooths out the roast curve (hides problems)
- Makes RoR (Rate of Rise) calculations inaccurate

---

**Next Steps After Shopping:**
1. Assembly → See [WIRING.md](WIRING.md)
2. Firmware setup → See [arduino-firmware/README.md](../arduino-firmware/README.md)
3. Artisan config → See [ARTISAN_INTEGRATION.md](ARTISAN_INTEGRATION.md)
