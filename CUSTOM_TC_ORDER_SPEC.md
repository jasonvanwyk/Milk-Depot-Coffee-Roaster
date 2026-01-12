# Custom K-Type Thermocouple Order Specification

**Project:** Milk Depot Coffee Roaster Temperature Monitoring System
**Date:** January 2026
**Quantity:** 6 probes (3 different lengths, 2 of each)

---

## Application Summary

Coffee drum roaster temperature monitoring with three measurement points:

| Position | Location | Environment | Max Operating Temp |
|----------|----------|-------------|-------------------|
| BT | Inside roasting drum, immersed in coffee beans | Direct bean contact, agitation, hot air | 250°C |
| ET | Exhaust duct, 10-15cm from drum exit | Hot air flow, no contact with beans | 300°C |
| FT | Near gas burner, measuring flame area | Radiant heat, occasional flame proximity | 450°C |

**Integration:** MAX31855 thermocouple amplifier → Arduino UNO → Artisan roasting software

**Note:** Ordering multiple lengths to determine optimal fit for each position, plus spares.

---

## Common Specifications (All 6 Probes)

| Parameter | Specification |
|-----------|---------------|
| **Thermocouple Type** | K-Type (Chromel-Alumel) per IEC 60584 |
| **Accuracy Class** | Class 1 preferred (±1.5°C), Class 2 acceptable (±2.5°C) |
| **Sheath Material** | AISI 316L Stainless Steel (food-grade, corrosion resistant) |
| **Junction Type** | Grounded (junction welded to sheath tip for fast response) |
| **Tip Style** | Closed, rounded (sealed, no exposed elements) |
| **Cable Insulation** | Fiberglass inner, stainless steel overbraid outer |
| **Cable Temperature Rating** | 700°C at sheath transition |
| **Cable Termination** | Bare wire ends, tinned (for screw terminal connection) |
| **Mounting** | Threaded compression fitting with lock nut (see mounting section) |

---

## Order Summary

**6 probes in 3 lengths (2 of each):**

| Qty | Sheath Length | Sheath Diameter | Temp Rating | Mounting Thread |
|-----|---------------|-----------------|-------------|-----------------|
| 2 | 35mm | 2.5mm | 700°C | M8 x 1.0 |
| 2 | 50mm | 3.0mm | 700°C | M8 x 1.0 |
| 2 | 70mm | 3.0mm | 700°C | M8 x 1.0 |

**Total: 6 probes**

**Design rationale:**
- 35mm probes: 2.5mm diameter for fastest response (likely BT position)
- 50mm/70mm probes: 3.0mm standard diameter for durability
- All probes 700°C rated: fully interchangeable for any position

---

## Probe Specifications by Size

### 35mm Probes (Qty: 2) - Fast Response

| Parameter | Specification | Rationale |
|-----------|---------------|-----------|
| **Sheath Diameter** | 2.5mm (±0.2mm) | Fastest response for BT position |
| **Sheath Length** | 35mm | Compact fit into drum |
| **Cable Length** | 2.0 meters | Reach to electronics enclosure |
| **Temperature Range** | -40°C to +700°C | Full interchangeability |
| **Response Time (t63)** | ≤3 seconds in moving air | Critical for first crack detection |

### 50mm Probes (Qty: 2) - Standard

| Parameter | Specification | Rationale |
|-----------|---------------|-----------|
| **Sheath Diameter** | 3.0mm (±0.2mm) | Balance of response and durability |
| **Sheath Length** | 50mm | Medium insertion depth |
| **Cable Length** | 2.0 meters | Reach to electronics enclosure |
| **Temperature Range** | -40°C to +700°C | Full interchangeability |
| **Response Time (t63)** | ≤5 seconds in moving air | Adequate for monitoring |

### 70mm Probes (Qty: 2) - Deep Insertion

| Parameter | Specification | Rationale |
|-----------|---------------|-----------|
| **Sheath Diameter** | 3.0mm (±0.2mm) | Durability at high temps |
| **Sheath Length** | 70mm | Deeper insertion, positioning flexibility |
| **Cable Length** | 2.0 meters | Reach to electronics enclosure |
| **Temperature Range** | -40°C to +700°C | Full interchangeability |
| **Response Time (t63)** | ≤5 seconds in moving air | Adequate for monitoring |

**All probes - Construction:**
- Smooth sheath surface (no burrs or rough welds)
- Flexible cable transition to handle movement and vibration
- Quality junction weld for thermal cycling durability

---

## Cable Termination

All probes terminate in **bare wire ends** for connection to MAX31855 screw terminals:

```
Cable End: Bare conductors, tinned
Wire Length: 20-30mm exposed from cable sheath
Polarity Marking: Clear color coding or labeling

  ══════════════╗
  SS Overbraid  ║
  + Fiberglass  ║
  ══════════════╝
        │
        ├──── + (Yellow) ──── Chromel (positive)
        │
        └──── - (Red) ─────── Alumel (negative)

  Wire gauge: Appropriate for thermocouple type (typically 24-20 AWG)
  Tinning: Solder-tinned ends for easy insertion into screw terminals
```

**Important:** K-type polarity is counter-intuitive:
- **Yellow wire = Positive (+)** = Chromel
- **Red wire = Negative (-)** = Alumel

Please ensure clear polarity marking on each probe.

---

## Mounting Specification

Probes require a **threaded fitting with lock nut** to mount through the roaster casing:

```
                     Roaster Wall (steel, ~2-3mm thick)
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
    │   INSIDE ROASTER      │      OUTSIDE          │
    │                       │                       │
    │         Probe Tip     │                       │
    │            ○──────────┼──────┬────────────────│───► To cable
    │                       │      │                │
    │                       │   ┌──┴──┐             │
    │                       │   │ NUT │ Lock nut    │
    │                       │   └──┬──┘             │
    │                       │      │                │
    │                    ┌──┴──────┴──┐             │
    │                    │   FITTING   │            │
    │                    │  (threaded) │            │
    │                    └─────────────┘            │
    │                                               │
    └───────────────────────────────────────────────┘
```

### Fitting Requirements

| Parameter | 35mm Probes (2.5mm dia) | 50mm & 70mm Probes (3.0mm dia) |
|-----------|-------------------------|--------------------------------|
| **Thread Size** | M8 x 1.0 | M8 x 1.0 |
| **Fitting Type** | Compression or brazed | Compression or brazed |
| **Nut Included** | Yes - hex lock nut | Yes - hex lock nut |
| **Sealing** | Metal-to-metal or with washer | Metal-to-metal or with washer |
| **Drill Size** | 8mm hole in roaster wall | 8mm hole in roaster wall |

**Alternative thread sizes acceptable:** M6 x 1.0 (if M8 not available for 2.5mm sheath)

### Mounting Style Options (in order of preference)

1. **Adjustable Compression Fitting** (preferred)
   - Allows depth adjustment after installation
   - Probe can be repositioned without disassembly
   - Ferrule seals around sheath

2. **Fixed Brazed/Welded Fitting**
   - Fitting permanently attached to sheath
   - Fixed insertion depth
   - More robust, no ferrule to wear

### Insertion Depth

The fitting should be positioned to allow:
- **Minimum 20mm** of sheath protruding inside roaster (measurement point)
- **Remaining sheath length** transitions to cable outside

```
Example for 50mm probe:

    Inside Roaster    │ Wall │    Outside
                      │      │
    ←─── 25-30mm ────►│ 3mm  │←── 17-22mm ──► to cable
                      │      │
         ○────────────┼──────┼────────╮
         Tip          │ Fit  │        Cable
                      │      │
```

---

## Construction Diagram

```
         Sheath (316L SS)
        ┌─────────────────────┐
   Tip  │  Grounded junction  │  Threaded     Transition
  (seal)│  welded at tip      │  Fitting      to cable
    ○───┴─────────────────────┴────┬────────────╮
                                   │            │
    |←── Sheath Length ──────────→||            │
         (35mm / 50mm / 70mm)    M8x1.0         │
                                 + Nut          │
                                                │
                                         ╭──────┴───────╮
                                         │ SS Overbraid │
                                         │ + Fiberglass │
                                         │    Cable     │
                                         │   (2.0m)     │
                                         ╰──────┬───────╯
                                                │
                                         ╭──────┴───────╮
                                         │  Bare Wire   │
                                         │   Tinned     │
                                         │   + / -      │
                                         ╰──────────────╯
```

---

## Quality Requirements

| Test | Requirement | Method |
|------|-------------|--------|
| Insulation Resistance | >100MΩ at 500VDC | Megger test |
| Continuity | <10Ω loop resistance | Multimeter |
| Calibration Check | Within Class tolerance at 0°C and 200°C | Ice bath, boiling water |
| Visual Inspection | No cracks, proper crimp, clean welds | Visual |

---

## Materials Certification

Please provide:
- [ ] Material certificate for 316L stainless steel sheath
- [ ] Thermocouple wire certificate (Chromel/Alumel composition)
- [ ] Calibration certificate or test data (optional but appreciated)

---

## Delivery Requirements

- Individual labeling: Each probe marked with length and diameter (e.g., "35mm/2.5mm", "70mm/3.0mm")
- Protective packaging: Probe tips and threaded fittings protected during shipping
- Documentation: Basic datasheet or drawing of final product
- Lock nuts: Included with each probe (6 total)

---

## Contact Information

**Project:** Milk Depot Coffee Roaster
**Location:** South Africa
**Email:** [your email]
**Phone:** [your phone]

---

## Notes for Manufacturer

1. **Food Contact:** Probes will contact coffee beans. 316L SS is required. No lubricants, oils, or coatings that could contaminate food.

2. **Two Diameter Variants (all 700°C rated):**
   - 35mm probes: 2.5mm diameter
   - 50mm & 70mm probes: 3.0mm diameter

3. **Mounting Hardware:** Each probe requires threaded fitting (M8 x 1.0 preferred) with hex lock nut included. Compression style preferred for adjustable insertion depth.

4. **Cable Termination:** Bare tinned wire ends, NOT plug connectors. Will connect directly to screw terminals on amplifier board.

5. **Polarity Marking:** Critical - please clearly mark polarity on cable. K-type: Yellow = +/Chromel, Red = -/Alumel.

6. **Labelling:** Mark each probe with: sheath length (35/50/70mm) and diameter (2.5/3.0mm).

---

*Specification Version: 1.0*
*Project: Milk Depot Coffee Roaster*
