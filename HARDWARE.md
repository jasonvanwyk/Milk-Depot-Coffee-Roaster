# Hardware Guide - Coffee Roaster Temperature Monitor

This document provides detailed hardware specifications, wiring diagrams, and assembly instructions for the coffee roaster temperature monitoring system.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    COFFEE ROASTER SYSTEM                        │
│                                                                 │
│  ┌─────────────┐    USB     ┌─────────────┐                    │
│  │ Raspberry   │◄──────────►│  Arduino    │                    │
│  │ Pi 4        │  (power    │  Nano       │                    │
│  │             │   + data)  │             │                    │
│  │ ┌─────────┐ │            │ ┌─────────┐ │    ┌────────────┐  │
│  │ │ Artisan │ │            │ │  OLED   │ │    │ Thermocouple│  │
│  │ │Software │ │            │ │ Display │ │    │ Probes     │  │
│  │ └─────────┘ │            │ └─────────┘ │    │ (in roaster)│  │
│  └─────────────┘            │ [Button]    │    └────────────┘  │
│                             └──────┬──────┘          │         │
│                                    │                 │         │
│                             ┌──────┴──────┐          │         │
│                             │  MAX31855   │◄─────────┘         │
│                             │  Modules x2 │                    │
│                             └─────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### Arduino Nano V3

| Specification | Value |
|---------------|-------|
| Microcontroller | ATmega328P |
| Operating Voltage | 5V |
| Flash Memory | 32 KB |
| SRAM | 2 KB |
| Clock Speed | 16 MHz |
| Digital I/O Pins | 14 (6 PWM) |
| Analog Input Pins | 8 |
| USB | Mini-B (CH340 chip) |
| Dimensions | 45mm x 18mm |

### MAX31855 Thermocouple Amplifier

| Specification | Value |
|---------------|-------|
| Thermocouple Type | K-type |
| Temperature Range | -200°C to +1350°C |
| Resolution | 0.25°C |
| Accuracy | ±2°C (typical) |
| Interface | SPI (3-wire) |
| Supply Voltage | 3.0V to 3.6V (module has regulator) |
| Cold Junction Compensation | Built-in |

### K-type Thermocouple Probes

| Specification | Value |
|---------------|-------|
| Type | K (Chromel-Alumel) |
| Temperature Range | -200°C to +1350°C |
| Probe Material | Stainless Steel 316 |
| Probe Diameter | 3mm (recommended) |
| Probe Length | 100-150mm |
| Cable Insulation | Fiberglass |
| Response Time | ~2 seconds |

### 1.3" OLED Display

| Specification | Value |
|---------------|-------|
| Size | 1.3 inches (diagonal) |
| Resolution | 128 x 64 pixels |
| Display Area | ~30mm x 15mm |
| Controller | SH1106 |
| Interface | I2C (default address 0x3C) |
| Supply Voltage | 3.3V - 5V |
| Colors | White on black |

---

## Pin Assignments

### Arduino Nano Pinout

```
                    ┌───────────────┐
                    │   USB Mini-B  │
                    └───────┬───────┘
               D13 ─┤●     │     ●├─ D12
               3V3 ─┤●           ●├─ D11
               REF ─┤●           ●├─ D10  → MAX31855 #1 CS (Bean)
                A0 ─┤●           ●├─ D9   → MAX31855 #2 CS (Exhaust)
                A1 ─┤●           ●├─ D8
                A2 ─┤●           ●├─ D7
                A3 ─┤●           ●├─ D6
         OLED SDA → A4 ─┤●           ●├─ D5
         OLED SCL → A5 ─┤●           ●├─ D4
                A6 ─┤●           ●├─ D3
                A7 ─┤●           ●├─ D2   → Button (to GND)
                5V ─┤●           ●├─ GND
               RST ─┤●           ●├─ RST
               GND ─┤●           ●├─ RX0
               VIN ─┤●           ●├─ TX1
                    └─────────────┘

SPI Bus (shared):
  D13 (SCK)  → MAX31855 CLK (both modules)
  D12 (MISO) → MAX31855 DO  (both modules)
```

### Complete Wiring Table

| Arduino Pin | Function | Connected To |
|-------------|----------|--------------|
| 5V | Power | MAX31855 VCC (both), OLED VCC |
| GND | Ground | MAX31855 GND (both), OLED GND, Button |
| D13 | SPI Clock | MAX31855 CLK (both, shared) |
| D12 | SPI MISO | MAX31855 DO (both, shared) |
| D10 | CS Bean | MAX31855 #1 CS |
| D9 | CS Exhaust | MAX31855 #2 CS |
| A4 | I2C SDA | OLED SDA |
| A5 | I2C SCL | OLED SCL |
| D2 | Button | Push button (other leg to GND) |

---

## Wiring Diagrams

### Full System Wiring

```
                                 ARDUINO NANO
                          ┌─────────────────────┐
                          │                     │
    ┌──────────────┐      │  5V ────────────────┼───┬───┬───┐
    │  MAX31855    │      │                     │   │   │   │
    │  (Bean)      │      │  GND ───────────────┼─┬─┼─┬─┼─┬─┼───┐
    │              │      │                     │ │ │ │ │ │ │   │
    │  VCC ────────┼──────┼─────────────────────┘ │ │ │ │ │ │   │
    │  GND ────────┼──────┼───────────────────────┘ │ │ │ │ │   │
    │  CLK ────────┼──────┼─ D13 (SCK) ─────────────┼─┼─┼─┘ │   │
    │  DO  ────────┼──────┼─ D12 (MISO) ────────────┼─┼─┘   │   │
    │  CS  ────────┼──────┼─ D10 ───────────────────┼─┘     │   │
    │              │      │                     │           │   │
    │  TC+ ○───────┤      │                     │           │   │
    │  TC- ○───────┤      │                     │           │   │
    └──────────────┘      │                     │           │   │
         │                │                     │           │   │
    [K-type probe]        │                     │           │   │
     (Bean temp)          │                     │           │   │
                          │                     │           │   │
    ┌──────────────┐      │                     │           │   │
    │  MAX31855    │      │                     │           │   │
    │  (Exhaust)   │      │                     │           │   │
    │              │      │                     │           │   │
    │  VCC ────────┼──────┼─────────────────────┼───────────┘   │
    │  GND ────────┼──────┼─────────────────────┼───────────────┘
    │  CLK ────────┼──────┼─ D13 (shared) ──────┤
    │  DO  ────────┼──────┼─ D12 (shared) ──────┤
    │  CS  ────────┼──────┼─ D9 ────────────────┤
    │              │      │                     │
    │  TC+ ○───────┤      │                     │
    │  TC- ○───────┤      │                     │
    └──────────────┘      │                     │
         │                │                     │
    [K-type probe]        │                     │
    (Exhaust temp)        │                     │
                          │                     │
    ┌──────────────┐      │                     │
    │  1.3" OLED   │      │                     │
    │              │      │                     │
    │  VCC ────────┼──────┼─ 5V ────────────────┤
    │  GND ────────┼──────┼─ GND ───────────────┤
    │  SDA ────────┼──────┼─ A4 ────────────────┤
    │  SCL ────────┼──────┼─ A5 ────────────────┤
    └──────────────┘      │                     │
                          │                     │
    ┌──────────────┐      │                     │
    │  Button      │      │                     │
    │  ┌───┐       │      │                     │
    │  │   │───────┼──────┼─ D2 ────────────────┤ (internal pullup)
    │  │   │───────┼──────┼─ GND ───────────────┤
    │  └───┘       │      │                     │
    └──────────────┘      │                     │
                          │  USB ───────────────┼──► Raspberry Pi
                          │                     │    (power + data)
                          └─────────────────────┘
```

### MAX31855 Module Detail

```
MAX31855 Breakout Module
┌─────────────────────────┐
│  ┌───────────────────┐  │
│  │    MAX31855 IC    │  │
│  └───────────────────┘  │
│                         │
│  [VCC] [GND] [DO] [CS] [CLK]    ← Pin header
│    │     │    │    │    │
│    │     │    │    │    └── SPI Clock (D13)
│    │     │    │    └─────── Chip Select (D10 or D9)
│    │     │    └──────────── Data Out / MISO (D12)
│    │     └───────────────── Ground
│    └─────────────────────── 3.3V-5V Power
│                         │
│  [TC+]  [TC-]              ← Thermocouple screw terminals
│    │      │
│    │      └── Thermocouple negative (yellow wire)
│    └───────── Thermocouple positive (red wire)
└─────────────────────────┘
```

### I2C OLED Module Detail

```
1.3" OLED Display Module (SH1106)
┌─────────────────────────┐
│  ┌───────────────────┐  │
│  │                   │  │
│  │   128 x 64        │  │
│  │   OLED Display    │  │
│  │                   │  │
│  └───────────────────┘  │
│                         │
│  [GND] [VCC] [SCL] [SDA]   ← Pin header (4 pins)
│    │     │     │     │
│    │     │     │     └── I2C Data (A4)
│    │     │     └──────── I2C Clock (A5)
│    │     └────────────── 3.3V-5V Power
│    └──────────────────── Ground
│                         │
│  I2C Address: 0x3C      │
└─────────────────────────┘
```

---

## Assembly Instructions

### Step 1: Prepare Components

1. Verify all components are present:
   - Arduino Nano x1
   - MAX31855 modules x2
   - K-type thermocouple probes x2
   - 1.3" OLED display x1
   - Tactile push button x1
   - Jumper wires (Dupont female-female)
   - Project enclosure x1

2. Check thermocouple wire colors:
   - Red wire = positive (+)
   - Yellow wire = negative (-)

### Step 2: Connect MAX31855 Modules

**Module 1 (Bean Temperature):**
| MAX31855 Pin | Arduino Pin |
|--------------|-------------|
| VCC | 5V |
| GND | GND |
| CLK | D13 |
| DO | D12 |
| CS | D10 |

**Module 2 (Exhaust Temperature):**
| MAX31855 Pin | Arduino Pin |
|--------------|-------------|
| VCC | 5V |
| GND | GND |
| CLK | D13 (shared) |
| DO | D12 (shared) |
| CS | D9 |

### Step 3: Connect OLED Display

| OLED Pin | Arduino Pin |
|----------|-------------|
| VCC | 5V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |

### Step 4: Connect Push Button

| Button Pin | Arduino Pin |
|------------|-------------|
| Pin 1 | D2 |
| Pin 2 | GND |

The firmware uses internal pullup resistor - no external resistor needed.

### Step 5: Connect Thermocouples

Insert thermocouple wires into MAX31855 screw terminals:
- **Red wire** → TC+ terminal
- **Yellow wire** → TC- terminal

**Important:** Ensure correct polarity! Reversed wires will give incorrect readings.

### Step 6: Connect to Raspberry Pi

Connect Arduino Nano to Raspberry Pi via USB cable.
- Provides 5V power to entire system
- Provides serial communication (115200 baud)

---

## Enclosure Assembly

### Recommended Enclosure Size

Minimum internal dimensions: 100mm x 60mm x 30mm

### Cutouts Required

1. **Display window**: ~35mm x 35mm for 1.3" OLED
2. **Button hole**: 6mm diameter
3. **USB port access**: 10mm x 8mm slot on side
4. **Thermocouple cable exits**: 2x 5mm holes

### Mounting

1. Mount Arduino Nano using M3 standoffs or double-sided tape
2. Mount OLED display with hot glue or mounting frame
3. Press-fit or glue button into 6mm hole
4. Route thermocouple cables through strain relief grommets

---

## Testing Procedure

### Step 1: Visual Inspection

- Check all connections against wiring diagram
- Verify no shorts between power and ground
- Confirm thermocouple polarity

### Step 2: Power Test

1. Connect USB to Raspberry Pi (or USB power source)
2. OLED should display startup screen
3. No smoke or hot components

### Step 3: Display Test

1. Press button to cycle through screens
2. Verify all three screens display correctly

### Step 4: Temperature Test

**Room Temperature Test:**
- Both probes should read ~20-25°C
- Values should be stable (±1°C)

**Ice Water Test (0°C calibration):**
1. Submerge probe in ice water slurry
2. Wait 30 seconds for stabilization
3. Should read 0°C ±2°C

**Boiling Water Test (100°C calibration):**
1. Submerge probe in boiling water
2. Wait 30 seconds for stabilization
3. Should read ~100°C (varies with altitude)

### Step 5: Serial Communication Test

```bash
# On Raspberry Pi
python3 /home/jason/Milk-Depot-Coffee-Roaster/test_serial.py
```

Should see output like:
```
BT:23.5,DT:24.2
BT:23.5,DT:24.1
```

---

## Troubleshooting

### No Display

| Problem | Solution |
|---------|----------|
| OLED blank | Check VCC/GND connections |
| OLED shows garbage | Check I2C address (should be 0x3C) |
| Display too dim | Normal for OLED - no brightness adjustment |

### Wrong Temperature Readings

| Problem | Solution |
|---------|----------|
| Reads 0°C constant | Thermocouple not connected properly |
| Reads very high/negative | Thermocouple polarity reversed |
| Reads ~25°C always | MAX31855 not communicating (check SPI wiring) |
| Jumpy readings | Check thermocouple wire connections |

### Button Not Working

| Problem | Solution |
|---------|----------|
| No response | Check D2 and GND connections |
| Multiple triggers | Debounce issue - check firmware |

### Serial Communication Issues

| Problem | Solution |
|---------|----------|
| No data received | Check USB connection and port |
| Garbled data | Verify baud rate is 115200 |
| Intermittent data | Check USB cable quality |

---

## Parts Sourcing

### Recommended Suppliers

**AliExpress (Budget):**
- Arduino Nano V3: Search "Arduino Nano V3.0 CH340"
- MAX31855: Search "MAX31855 thermocouple module"
- OLED 1.3": Search "1.3 inch OLED I2C SH1106"
- K-type probe: Search "K type thermocouple 500C stainless"

**Amazon (Faster shipping):**
- Search same terms, typically 2-3x price

**Adafruit/SparkFun (Quality):**
- MAX31855 breakout
- Thermocouple probes with connectors

### Total Estimated Cost

| Component | AliExpress | Amazon |
|-----------|------------|--------|
| Arduino Nano | $2-3 | $8-12 |
| MAX31855 x2 | $8 | $25-30 |
| K-type probes x2 | $6 | $15-20 |
| 1.3" OLED | $3-4 | $10-12 |
| Button + wires | $2 | $5 |
| Enclosure | $3 | $8-10 |
| **Total** | **$24-28** | **$71-89** |

---

## Safety Notes

1. **High Temperature Probes**: Thermocouple probes will get very hot during roasting. Use heat-resistant gloves when handling.

2. **Food Safety**: Use stainless steel 316 probes that are food-safe rated if probe contacts coffee beans.

3. **Electrical**: Keep electronics away from heat sources and steam. Consider conformal coating for humidity protection.

4. **Ventilation**: Coffee roasting produces smoke. Ensure adequate ventilation.

---

**Document Version**: 1.0
**Last Updated**: 2025-12-15
