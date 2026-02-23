# Thermocouple Specification for Coffee Roasting

Technical specification for K-type thermocouple probes suitable for the Milk Depot Coffee Roaster temperature monitoring system.

## Application Overview

**Use Case**: Coffee drum roaster temperature monitoring
**Environment**: Hot air (up to 300°C), contact with coffee beans, food-safe requirement
**Integration**: MAX31855 thermocouple amplifier → Arduino → Artisan software

**Three probes required:**

| Probe | Location | Measures | Typical Range |
|-------|----------|----------|---------------|
| BT (Bean Temperature) | Inside drum, in bean mass | Coffee bean temperature | 20-230°C |
| ET (Exhaust Temperature) | Exhaust duct | Air leaving drum | 20-280°C |
| FT (Flame Temperature) | Near burner | Heat source temperature | 50-400°C |

---

## Detailed Specification (For Custom Manufacturer)

### General Requirements

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Thermocouple Type** | K-Type (Chromel/Alumel) | ANSI/IEC 60584 |
| **Accuracy Class** | Class 1 or Class 2 | ±1.5°C or ±2.5°C |
| **Temperature Range** | -50°C to +500°C minimum | 700°C preferred for safety margin |
| **Quantity** | 3 probes | BT, ET, FT |

### Probe Sheath (Critical)

| Parameter | Specification | Reason |
|-----------|---------------|--------|
| **Style** | Insertion/Immersion probe | Must penetrate into bean mass |
| **Material** | AISI 316 Stainless Steel | Food-safe, corrosion resistant |
| **Diameter** | 3.0mm (preferred) | Fast response, durable. Range: 2-4mm acceptable |
| **Length** | 100-150mm | Deep enough for drum insertion |
| **Tip Style** | Closed, rounded or pointed | Sealed, no exposed wires |

**Why 3mm diameter?**
- Thinner = faster response (critical for tracking roast dynamics)
- 1.5-2mm: Very fast but fragile
- 3mm: Good balance of speed and durability
- 5-6mm: Too slow, causes "thermal lag" in readings

### Junction Type

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Junction** | Grounded (preferred) | Faster response (~2s vs ~5s ungrounded) |
| **Alternative** | Ungrounded acceptable | If electrical noise is a concern |

**Grounded**: Junction welded to sheath tip - faster heat transfer
**Ungrounded**: Junction insulated from sheath - electrically isolated but slower

### Cable/Lead Wire

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Length** | 1.5-2.0 meters | Reach from roaster to electronics enclosure |
| **Insulation** | Fiberglass or PTFE | High temperature rated |
| **Shielding** | Stainless steel overbraid | EMI protection, mechanical protection |
| **Temperature Rating** | 350°C minimum at probe end | Cable can be cooler further from probe |

### Connector

| Parameter | Specification | Notes |
|-----------|---------------|-------|
| **Type** | Miniature K-type flat blade | ANSI standard, yellow color code |
| **Pin Spacing** | 7.16mm (0.282") center-to-center | Standard miniature TC connector |
| **Gender** | Male plug on cable end | Mates with MAX31855 module socket |

**Connector Diagram:**
```
    ┌─────────────┐
    │  YELLOW     │  ← K-type color code (ANSI)
    │   ┌───┐     │
    │   │ + │     │  ← Larger pin (positive, Chromel)
    │   └───┘     │
    │   ┌───┐     │
    │   │ - │     │  ← Smaller pin (negative, Alumel)
    │   └───┘     │
    └─────────────┘
       Male plug
```

### Mounting (Optional)

| Parameter | Options | Notes |
|-----------|---------|-------|
| **Thread** | M6 x 1.0 or M8 x 1.25 | For fixed mounting through roaster wall |
| **Compression Fitting** | 1/8" or 6mm | Adjustable depth |
| **None** | Probe only | Will fabricate own mounting |

For this project: **No mounting hardware required** - will fabricate custom mounting brackets.

---

## Performance Requirements

| Parameter | Requirement | Test Method |
|-----------|-------------|-------------|
| **Response Time (t90)** | ≤5 seconds in moving air | Step change in air temperature |
| **Accuracy at 200°C** | ±2.5°C or better | Calibrated reference |
| **Repeatability** | ±0.5°C | Multiple measurements |
| **Long-term Drift** | <1°C/year | - |

### Response Time Guidance

| Probe Diameter | Approximate t90 (air) | Approximate t90 (liquid) |
|----------------|----------------------|--------------------------|
| 1.5mm | 2-3 seconds | <1 second |
| 3.0mm | 4-6 seconds | 1-2 seconds |
| 6.0mm | 10-15 seconds | 3-5 seconds |

*t90 = time to reach 90% of final temperature*

---

## Summary Specification Table

**For quoting purposes - provide this to suppliers:**

| Item | BT Probe | ET Probe | FT Probe |
|------|----------|----------|----------|
| **Type** | K-Type Thermocouple | K-Type Thermocouple | K-Type Thermocouple |
| **Sheath Material** | 316 Stainless Steel | 316 Stainless Steel | 316 Stainless Steel |
| **Sheath Diameter** | 3.0mm | 3.0mm | 3.0mm |
| **Sheath Length** | 100mm | 100mm | 150mm |
| **Junction** | Grounded | Grounded | Grounded |
| **Cable Length** | 1.5m | 1.5m | 1.5m |
| **Cable Insulation** | Fiberglass + SS braid | Fiberglass + SS braid | Fiberglass + SS braid |
| **Connector** | Miniature K-type male | Miniature K-type male | Miniature K-type male |
| **Temp Range** | -50 to +500°C | -50 to +500°C | -50 to +700°C |
| **Mounting** | None (bare probe) | None (bare probe) | None (bare probe) |

**Quantity: 3 probes total (1 of each)**

---

## What NOT to Order

Avoid these styles - they won't work for coffee roasting:

| Style | Why Not Suitable |
|-------|------------------|
| Surface/Washer/Ring mount | Measures surface temp, not insertion |
| Exposed junction (bare wires) | Fragile, not food-safe |
| Air temperature probes (with handle) | Handle melts, wrong form factor |
| Pipe clamp style | Wrong application |
| Very thick probes (>6mm) | Too slow response time |

---

## Reference Standards

- **IEC 60584-1**: Thermocouple reference tables (Type K)
- **IEC 60584-2**: Thermocouple tolerances
- **ASTM E230**: Standard specification for thermocouples
- **ANSI MC96.1**: Temperature measurement thermocouples (color codes)

---

## Ordering Checklist

When ordering, confirm:

- [ ] K-type thermocouple (Chromel/Alumel)
- [ ] Insertion/immersion probe style (NOT surface mount)
- [ ] 316 stainless steel sheath
- [ ] 3mm diameter (2-4mm acceptable)
- [ ] 100-150mm probe length
- [ ] Grounded junction
- [ ] 1.5m+ cable with fiberglass/SS braid insulation
- [ ] Miniature K-type connector (male, yellow)
- [ ] Food-safe materials
- [ ] Temperature rating to at least 400°C

---

## Supplier Communication Template

**Email template for requesting quotes:**

```
Subject: Quote Request - K-Type Thermocouple Probes for Coffee Roaster

Dear [Supplier],

I require 3x K-type thermocouple probes for a coffee roasting application.

Specifications:
- Type: K-type thermocouple
- Probe style: Insertion/immersion (stainless steel sheath with closed tip)
- Sheath material: AISI 316 stainless steel (food-safe)
- Sheath diameter: 3.0mm (±0.5mm acceptable)
- Sheath length: 100-150mm
- Junction type: Grounded
- Cable length: 1.5 meters minimum
- Cable: Fiberglass insulated with stainless steel overbraid
- Connector: Miniature K-type male plug (ANSI yellow)
- Temperature range: -50°C to +500°C minimum
- Mounting: None required (bare probe)

Application: Coffee drum roaster, measuring bean mass temperature (up to 230°C),
exhaust air temperature (up to 280°C), and burner area temperature (up to 400°C).
Food-safe materials required.

Please provide:
1. Unit price for 3 probes
2. Lead time
3. Datasheet or drawing
4. Any MOQ requirements

Thank you,
[Your name]
```

---

*Document Version: 1.0*
*Date: December 2024*
*Project: Milk Depot Coffee Roaster*
