# Wiring & Assembly Guide

Complete wiring and assembly reference for the Milk Depot Coffee Roaster temperature monitoring system.

**Updated:** 2-channel design with Arduino Nano, 2x MAX31855, 1.3" SH1106 OLED.

## System Overview

```
                    ┌─────────────────────────────────────────────────┐
                    │                     ROASTER                     │
                    │                                                 │
                    │    [DRUM]◄───── BT Probe (35mm/2.5mm)          │
                    │       │                                         │
                    │       ▼                                         │
                    │   [EXHAUST]◄─── ET Probe (50mm/3.0mm)          │
                    │                                                 │
                    └──────┬───────────────────┬──────────────────────┘
                           │                   │
                           │ 1.5m K-type        │ 1.5m K-type
                           │ bare tinned wire   │ bare tinned wire
                           │                   │
┌──────────────────────────┴───────────────────┴──────────────────────┐
│                           ENCLOSURE (61×80×23mm)                    │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │              50×70mm Veroboard                              │   │
│   │                                                             │   │
│   │   ┌──────────────┐   ┌─────────┐   ┌─────────┐            │   │
│   │   │ Arduino Nano │   │MAX31855 │   │MAX31855 │            │   │
│   │   │   (USB-C)    │   │   BT    │   │   ET    │            │   │
│   │   │              │   │  ┌─┐    │   │  ┌─┐    │            │   │
│   │   │   D13──SCK──►│──►│  │C1    │   │  │C2    │            │   │
│   │   │   D12◄─DO───◄│──◄│  └─┘    │   │  └─┘    │            │   │
│   │   │   D10──CS───►│──►│  100nF  │   │  100nF  │            │   │
│   │   │   D9───CS───►│───│─────────│──►│         │            │   │
│   │   │   A4──SDA──► │   │  TC+ TC-│   │  TC+ TC-│            │   │
│   │   │   A5──SCL──► │   └────┬──┬─┘   └────┬──┬─┘            │   │
│   │   │   5V──VCC──► │        │  │          │  │               │   │
│   │   │   GND─GND──► │   BT probe      ET probe               │   │
│   │   └──────┬───────┘                                         │   │
│   │          │ USB-C                                           │   │
│   └──────────┼─────────────────────────────────────────────────┘   │
│              │                         ┌────────────┐              │
│              │                         │ 1.3" OLED  │ Front panel  │
│              │                         │  (I2C)     │ bezel mount  │
│              │                         └────────────┘              │
└──────────────┼─────────────────────────────────────────────────────┘
               │
          USB-C Cable (2m)
               │
      ┌────────┴────────┐
      │  RASPBERRY PI 4 │
      │  10.0.10.102    │
      │  [Artisan SW]   │
      └─────────────────┘
```

## Arduino Nano Pinout

```
              Arduino Nano (USB-C variant)
              Top view, USB connector at top

         Left Header              Right Header
         ───────────              ────────────
    TX ─ │ D1          D13 │ ─ SPI SCK ──► BT SCK, ET SCK
    RX ─ │ D0          3V3 │
         │ RST        AREF │
   GND ◄─│ GND          A0 │
         │ D2           A1 │
         │ D3           A2 │
         │ D4           A3 │
         │ D5      SDA  A4 │ ─ I2C SDA ──► OLED SDA
         │ D6      SCL  A5 │ ─ I2C SCL ──► OLED SCL
         │ D7           A6 │
         │ D8           A7 │
  CS ET ─│ D9           5V │ ─ VCC ──► BT, ET, OLED
  CS BT ─│ D10         RST │
         │ D11         GND │ ─ GND ──► BT, ET, OLED
SPI DO ◄─│ D12         VIN │
         ────────┬──────────
                 │
              USB-C
```

## Pin Assignment Table

| Arduino Pin | Function    | Wire Colour | Connected To          |
|-------------|-------------|-------------|-----------------------|
| D13         | SPI SCK     | Yellow      | BT SCK + ET SCK      |
| D12         | SPI MISO    | Green       | BT DO + ET DO         |
| D10         | CS_BT       | Blue        | BT CS (Bean Temp)     |
| D9          | CS_ET       | Violet      | ET CS (Exhaust Temp)  |
| A4          | I2C SDA     | White       | OLED SDA              |
| A5          | I2C SCL     | Orange      | OLED SCL              |
| 5V          | Power       | Red         | BT VCC, ET VCC, OLED VCC |
| GND         | Ground      | Black       | BT GND, ET GND, OLED GND |
| USB-C       | Serial/Power| —           | RPi 4 via USB cable   |

## MAX31855 Module Wiring

Both modules share the SPI bus (SCK, DO) but have individual chip select (CS) lines.

```
┌─────────────────────────┐       ┌─────────────────────────┐
│    MAX31855 - BT        │       │    MAX31855 - ET        │
│    (Bean Temperature)   │       │    (Exhaust Temperature) │
│                         │       │                         │
│  VCC ─── 5V (Red)      │       │  VCC ─── 5V (Red)      │
│  GND ─── GND (Black)   │       │  GND ─── GND (Black)   │
│  SCK ─── D13 (Yellow)  │       │  SCK ─── D13 (Yellow)  │
│  DO  ─── D12 (Green)   │       │  DO  ─── D12 (Green)   │
│  CS  ─── D10 (Blue)    │       │  CS  ─── D9 (Violet)   │
│                         │       │                         │
│  TC+ ─── Yellow wire   │       │  TC+ ─── Yellow wire   │
│  TC- ─── Red wire ⚠    │       │  TC- ─── Red wire ⚠    │
│         (red=NEGATIVE!) │       │         (red=NEGATIVE!) │
│                         │       │                         │
│  ┌─┐ 100nF (C1)        │       │  ┌─┐ 100nF (C2)        │
│  └─┘ across VCC/GND    │       │  └─┘ across VCC/GND    │
└─────────────────────────┘       └─────────────────────────┘
```

> **⚠ POLARITY WARNING:** K-type thermocouple red wire is **NEGATIVE**. Reversing polarity causes readings to go negative as temperature increases.

## Decoupling Capacitors

Each MAX31855 module gets a 100nF (code "104") ceramic capacitor soldered directly across VCC and GND, as close to the module pins as possible. This filters high-frequency noise on the power supply.

| Cap | Module | Connection |
|-----|--------|------------|
| C1  | BT     | BT VCC to BT GND |
| C2  | ET     | ET VCC to ET GND |

## OLED Display (I2C)

The 1.3" SH1106 OLED mounts in a bezel on the enclosure front panel, connected via 4 wires to the veroboard.

```
    1.3" SH1106 OLED               Arduino Nano
    ┌─────────────┐                 ┌──────────┐
    │ VCC ────────│── Red ──────────┤ 5V       │
    │ GND ────────│── Black ────────┤ GND      │
    │ SDA ────────│── White ────────┤ A4       │
    │ SCL ────────│── Orange ───────┤ A5       │
    └─────────────┘                 └──────────┘

    OLED PCB: 35.5 × 33.6mm
    Screen:   35 × 19.5mm (128×64 pixels)
    Mounting: 4× Essentra 27PIF0045B push-in fasteners
```

## Complete Wire List

| # | From | To | Colour | Length | Notes |
|---|------|----|--------|--------|-------|
| W1 | Nano D13 | BT SCK | Yellow | ~5cm | SPI clock |
| W2 | Nano D13 | ET SCK | Yellow | ~8cm | SPI clock |
| W3 | Nano D12 | BT DO | Green | ~5cm | SPI data |
| W4 | Nano D12 | ET DO | Green | ~8cm | SPI data |
| W5 | Nano D10 | BT CS | Blue | ~5cm | Chip select BT |
| W6 | Nano D9 | ET CS | Violet | ~8cm | Chip select ET |
| W7 | Nano A4 | OLED SDA | White | ~15cm | I2C data (to panel) |
| W8 | Nano A5 | OLED SCL | Orange | ~15cm | I2C clock (to panel) |
| W9 | Nano 5V | BT VCC | Red | ~5cm | Power |
| W10 | Nano 5V | ET VCC | Red | ~8cm | Power |
| W11 | Nano 5V | OLED VCC | Red | ~15cm | Power (to panel) |
| W12 | Nano GND | BT GND | Black | ~5cm | Ground |
| W13 | Nano GND | ET GND | Black | ~8cm | Ground |
| W14 | Nano GND | OLED GND | Black | ~15cm | Ground (to panel) |
| W15 | TC_BT | BT TC+/TC- | YE/RD | 1.5m | BT thermocouple lead |
| W16 | TC_ET | ET TC+/TC- | YE/RD | 1.5m | ET thermocouple lead |
| USB | RPi USB | Nano USB-C | — | 2m | Power + serial data |

## Veroboard Assembly Layout

50×70mm stripboard. Strips run along the 70mm length (27 holes per strip, 19 strips).

### Component Placement (top view)

```
     Veroboard 50×70mm (copper strips run left-right →)
     Columns: A B C D E F G H I J K L M N O P Q R S
     ═══════════════════════════════════════════════════
 1 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 2 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 3 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 4 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
     ┌─────────────────────────────────────────────────
     │ ZONE A: Arduino Nano (rows 5-19, cols C-H)
     │ Placed spanning cols C and H (0.6" DIP width)
     │ USB connector faces row 5 edge
 5 → ○ ○[TX  ○ ○ ○ ○ D13]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 6 → ○ ○[RX  ○ ○ ○ ○ 3V3]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 7 → ○ ○[RST ○ ○ ○ ○ REF]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 8 → ○ ○[GND ○ ○ ○ ○  A0]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
 9 → ○ ○[D2  ○ ○ ○ ○  A1]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
10 → ○ ○[D3  ○ ○ ○ ○  A2]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
11 → ○ ○[D4  ○ ○ ○ ○  A3]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
12 → ○ ○[D5  ○ ○ ○ ○  A4]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← SDA
13 → ○ ○[D6  ○ ○ ○ ○  A5]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← SCL
14 → ○ ○[D7  ○ ○ ○ ○  A6]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
15 → ○ ○[D8  ○ ○ ○ ○  A7]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
16 → ○ ○[D9  ○ ○ ○ ○  5V]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← CS_ET, 5V
17 → ○ ○[D10 ○ ○ ○ ○ RST]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← CS_BT
18 → ○ ○[D11 ○ ○ ○ ○ GND]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← GND
19 → ○ ○[D12 ○ ○ ○ ○ VIN]○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○  ← SPI DO
     └─────────────────────────────────────────────────
     ┌─────────────────────────────────────────────────
     │ ZONE B: MAX31855 modules (rows 5-12, cols K-S)
     │ BT module: cols K-Q, rows 5-7
     │ ET module: cols K-Q, rows 9-11
     │ Caps soldered near each module
     └─────────────────────────────────────────────────
20 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
     ┌─────────────────────────────────────────────────
     │ ZONE C: OLED + thermocouple header pins
     │ (rows 21-25, cols A-G)
     │ 4-pin header for OLED wires (VCC GND SDA SCL)
     │ Screw terminal or pins for TC leads
     └─────────────────────────────────────────────────
21 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
22 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
23 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
24 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
25 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
26 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
27 → ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
```

### Assembly Notes

1. **Arduino Nano** — Insert pin headers into rows 5-19, columns C and H. USB-C faces the board edge (row 5). The Nano straddles 6 strips.

2. **MAX31855 Modules** — Place to the right of the Nano in Zone B. Break copper strips between the Nano and modules to avoid shorts. Each module needs VCC, GND, SCK, DO, CS connected back to the Nano plus TC+/TC- for thermocouple wires.

3. **Decoupling Caps** — Solder C1 and C2 directly across VCC/GND pins of each MAX31855, as close as physically possible.

4. **OLED Header** — 4-pin male header in Zone C for connecting flying leads to the panel-mounted OLED.

5. **Strip Breaks** — Cut copper strips between:
   - Nano left pins and right pins (between cols C-H under the Nano body)
   - Between Zone A and Zone B where different signals share a strip
   - Anywhere two signals that shouldn't connect share a strip row

6. **Power Distribution** — Run a 5V bus and GND bus along available strip rows. Bridge from Nano 5V (row 16, col H) to the bus, and from Nano GND (row 18, col H) to the bus.

7. **SPI Bus** — D13/SCK (row 5, col H) needs to reach both MAX31855 SCK pins. D12/DO (row 19, col C) needs to reach both MAX31855 DO pins. Use wire links on the underside or jumper wires on top.

8. **Thermocouple Leads** — Bare tinned wire from K-type probes connects directly to MAX31855 screw terminals. **Red wire is NEGATIVE** — connect to TC-.

## Thermocouple Assignment

| Probe | Size | Channel | Pin | Position |
|-------|------|---------|-----|----------|
| BT (Bean Temp) | 35mm/2.5mm | D10 | CS_BT | Inside drum, in bean mass |
| ET (Exhaust Temp) | 50mm/3.0mm | D9 | CS_ET | Exhaust path, 10-15cm from drum |

## Probe Placement

```
                    ┌─────────────────────────────────┐
                    │           EXHAUST               │
                    │             ▲                   │
                    │      ┌──────┴──────┐           │
                    │      │             │           │
                    │      │   ◄─────────│── ET      │ 50mm/3.0mm probe
                    │      │             │           │ (in exhaust flow)
                    │      │    DRUM     │           │
                    │      │             │           │
                    │      │   ●●●●●     │           │
                    │      │   ●●●●● ◄───│── BT      │ 35mm/2.5mm probe
                    │      │   ●●●●●     │           │ (in bean mass)
                    │      │             │           │
                    │      └──────┬──────┘           │
                    │             │                   │
                    │      ┌──────┴──────┐           │
                    │      │   BURNER    │           │
                    │      └─────────────┘           │
                    └─────────────────────────────────┘
```

## Power Budget

| Component | Current Draw |
|-----------|-------------|
| Arduino Nano | ~19mA (idle) |
| MAX31855 × 2 | ~1.5mA total |
| 1.3" OLED SH1106 | ~25mA |
| **Total** | **~48mA** |

USB from RPi 4 supplies 500mA minimum — more than sufficient.

## WireViz Diagram

The machine-generated wiring diagram is at:
- `docs/wiring.png` — PNG image
- `docs/wiring.svg` — Scalable vector
- `docs/wiring.html` — Interactive HTML with BOM

Generate from YAML source:
```bash
cd ~/Projects/Milk-Depot-Coffee-Roaster
wireviz docs/wiring.yml
```

## Safety Notes

1. **Thermocouple Polarity**: Red wire is **negative** on K-type thermocouples. Reversing polarity causes readings to decrease with increasing temperature.
2. **Heat Protection**: Keep electronics and connectors away from heat sources. Only probe tips enter hot zones.
3. **Cable Routing**: Route thermocouple leads away from power cables to minimise interference.
4. **Decoupling**: 100nF caps on each MAX31855 are essential for stable readings.
5. **Grounding**: All GND connections should meet at a single point (star ground) to reduce noise.

---

*Version 2.0 — Updated 16 March 2026 for 2-channel Arduino Nano design*
*Previous: v1.0 (3-channel Arduino UNO R3, December 2024)*
