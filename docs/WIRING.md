# Wiring Diagram - 3-Channel Thermocouple System

Complete wiring reference for the Milk Depot Coffee Roaster temperature monitoring system.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ROASTER                                         │
│                                                                              │
│    [DRUM]◄────────────── BT Probe (Bean Temp)                               │
│       │                                                                      │
│       ▼                                                                      │
│   [EXHAUST]◄───────────── ET Probe (Exhaust Temp)                           │
│                                                                              │
│   [BURNER]◄────────────── FT Probe (Flame Temp)                             │
│                                                                              │
└──────┬──────────────────────┬──────────────────────┬────────────────────────┘
       │                      │                      │
       │ 1.5m K-type          │ 1.5m K-type          │ 1.5m K-type
       │ thermocouple         │ thermocouple         │ thermocouple
       │                      │                      │
┌──────┴──────────────────────┴──────────────────────┴────────────────────────┐
│                           ENCLOSURE                                          │
│  ┌─────────┐          ┌─────────┐          ┌─────────┐                      │
│  │ K-Type  │          │ K-Type  │          │ K-Type  │   Panel-mount        │
│  │ Socket  │          │ Socket  │          │ Socket  │   connectors         │
│  │  (BT)   │          │  (ET)   │          │  (FT)   │                      │
│  └────┬────┘          └────┬────┘          └────┬────┘                      │
│       │                    │                    │                           │
│  ┌────┴────┐          ┌────┴────┐          ┌────┴────┐                      │
│  │MAX31855 │          │MAX31855 │          │MAX31855 │   Thermocouple       │
│  │   #1    │          │   #2    │          │   #3    │   amplifiers         │
│  │  (BT)   │          │  (ET)   │          │  (FT)   │                      │
│  └────┬────┘          └────┬────┘          └────┬────┘                      │
│       │                    │                    │                           │
│       └────────────────────┴────────────────────┘                           │
│                            │                                                 │
│                    SPI Bus (shared)                                          │
│                            │                                                 │
│                   ┌────────┴────────┐                                        │
│                   │  ARDUINO UNO    │                                        │
│                   │      R3         │                                        │
│                   └────────┬────────┘                                        │
│                            │ USB                                             │
│  ┌─────────────┐           │                                                 │
│  │    OLED     │◄──I2C─────┤                                                 │
│  │   Display   │           │                                                 │
│  │  (optional) │           │                                                 │
│  └─────────────┘           │                                                 │
└────────────────────────────┼────────────────────────────────────────────────┘
                             │
                        USB Cable (2m)
                             │
                    ┌────────┴────────┐
                    │  RASPBERRY PI   │
                    │       4         │
                    │                 │
                    │  [Artisan SW]   │
                    └─────────────────┘
```

## Arduino UNO R3 Pinout

```
                                    ┌─────────────────┐
                                    │   ARDUINO UNO   │
                                    │       R3        │
                                    │                 │
                            ┌───────┤ D13 (SCK)       │──── SPI Clock (to all MAX31855)
                            │       │                 │
                            │   ┌───┤ D12 (MISO)      │──── SPI Data (from all MAX31855)
                            │   │   │                 │
                            │   │   │ D11             │     (unused)
                            │   │   │                 │
   MAX31855 #1 (ET) CS ─────│───│───┤ D10             │
                            │   │   │                 │
   MAX31855 #2 (BT) CS ─────│───│───┤ D9              │
                            │   │   │                 │
   MAX31855 #3 (FT) CS ─────│───│───┤ D8              │
                            │   │   │                 │
                            │   │   │ D7-D2           │     (unused)
                            │   │   │                 │
                            │   │   │ D1 (TX)         │──── Serial TX (to USB)
                            │   │   │                 │
                            │   │   │ D0 (RX)         │──── Serial RX (from USB)
                            │   │   │                 │
           OLED SCL ────────│───│───┤ A5 (SCL)        │
                            │   │   │                 │
           OLED SDA ────────│───│───┤ A4 (SDA)        │
                            │   │   │                 │
                            │   │   │ A3-A0           │     (unused, analog simulation)
                            │   │   │                 │
    All VCC ────────────────│───│───┤ 5V              │
                            │   │   │                 │
    All GND ────────────────┴───┴───┤ GND             │
                                    │                 │
                                    └─────────────────┘
```

## MAX31855 Module Wiring

Each MAX31855 module has 5 pins. Three modules share the SPI bus but have individual chip select (CS) lines.

### Module Pinout

```
┌─────────────────────────────┐
│        MAX31855 Module      │
│                             │
│  VCC ──────── +5V           │
│  GND ──────── GND           │
│  SCK ──────── D13 (shared)  │
│  DO  ──────── D12 (shared)  │
│  CS  ──────── D10/D9/D8     │  (unique per module)
│                             │
│  [K-Type Socket]            │
│       + -                   │
└─────────────────────────────┘
```

### SPI Bus Connection Detail

```
                    Arduino UNO
                    ┌─────────┐
                    │         │
            ┌───────┤ D13 SCK │
            │       │         │
            │   ┌───┤ D12 MISO│
            │   │   │         │
            │   │   │ D10     ├───────┐
            │   │   │         │       │
            │   │   │ D9      ├───────│───────┐
            │   │   │         │       │       │
            │   │   │ D8      ├───────│───────│───────┐
            │   │   │         │       │       │       │
            │   │   │ 5V      ├───┬───│───┬───│───┬───│───┐
            │   │   │         │   │   │   │   │   │   │   │
            │   │   │ GND     ├───│───┴───│───┴───│───┴───│───┐
            │   │   │         │   │       │       │       │   │
            │   │   └─────────┘   │       │       │       │   │
            │   │                 │       │       │       │   │
        ┌───┴───┴─────────────────┴───────┴───────┴───────┴───┴───┐
        │   SCK DO    VCC  GND   CS      CS      CS               │
        │    │   │     │    │    │       │       │                │
        │  ┌─┴───┴─────┴────┴────┴─┐ ┌───┴───┐ ┌─┴─────┐          │
        │  │      MAX31855 #1      │ │ #2    │ │  #3   │          │
        │  │         (ET)          │ │ (BT)  │ │ (FT)  │          │
        │  └───────────┬───────────┘ └───┬───┘ └───┬───┘          │
        │              │                 │         │              │
        │         [K-Socket]        [K-Socket] [K-Socket]         │
        └──────────────┴─────────────────┴─────────┴──────────────┘
                       │                 │         │
                 ET Probe           BT Probe   FT Probe
                 (Exhaust)           (Bean)    (Flame)
```

## OLED Display Wiring (Optional)

```
    OLED SSD1306 (I2C)              Arduino UNO
    ┌─────────────┐                 ┌─────────┐
    │             │                 │         │
    │ VCC ────────│─────────────────┤ 5V      │
    │             │                 │         │
    │ GND ────────│─────────────────┤ GND     │
    │             │                 │         │
    │ SDA ────────│─────────────────┤ A4      │
    │             │                 │         │
    │ SCL ────────│─────────────────┤ A5      │
    │             │                 │         │
    └─────────────┘                 └─────────┘
```

## Complete Wire List

| From | To | Wire Color (suggested) | Notes |
|------|----|-----------------------|-------|
| Arduino 5V | Breadboard +5V rail | Red | Power bus |
| Arduino GND | Breadboard GND rail | Black | Ground bus |
| Arduino D13 | All MAX31855 SCK | Yellow | SPI Clock (shared) |
| Arduino D12 | All MAX31855 DO | Green | SPI Data (shared) |
| Arduino D10 | MAX31855 #1 CS | Blue | ET chip select |
| Arduino D9 | MAX31855 #2 CS | Purple | BT chip select |
| Arduino D8 | MAX31855 #3 CS | Gray | FT chip select |
| Arduino A4 | OLED SDA | White | I2C Data |
| Arduino A5 | OLED SCL | Orange | I2C Clock |
| +5V rail | All MAX31855 VCC | Red | Module power |
| +5V rail | OLED VCC | Red | Display power |
| GND rail | All MAX31855 GND | Black | Module ground |
| GND rail | OLED GND | Black | Display ground |

## Enclosure Layout

```
┌──────────────────────────────────────────────────────────────────┐
│                        FRONT PANEL                                │
│                                                                   │
│    ┌───────┐      ┌───────┐      ┌───────┐      ┌───────────┐   │
│    │ ET    │      │ BT    │      │ FT    │      │   OLED    │   │
│    │Socket │      │Socket │      │Socket │      │  Window   │   │
│    └───────┘      └───────┘      └───────┘      └───────────┘   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                         SIDE VIEW                                 │
│                                                                   │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │                   Internal Layout                        │   │
│    │                                                          │   │
│    │   ┌─────────┐  ┌───────────────────────────────────┐    │   │
│    │   │ Arduino │  │       Perfboard with               │    │   │
│    │   │  UNO    │  │     3x MAX31855 modules            │    │   │
│    │   │         │  │         + OLED                     │    │   │
│    │   └─────────┘  └───────────────────────────────────┘    │   │
│    │                                                          │   │
│    └────┬────────────────────────────────────────────────────┘   │
│         │                                                         │
│    ┌────┴────┐                                                   │
│    │USB Cable│ (Cable Gland PG9)                                 │
│    │  Exit   │                                                   │
│    └─────────┘                                                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                         TOP VIEW (internal)                       │
│                                                                   │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                                                          │    │
│   │   ┌─────────┐                                            │    │
│   │   │ Arduino │     ┌───┐ ┌───┐ ┌───┐                     │    │
│   │   │  UNO    │     │ET │ │BT │ │FT │  MAX31855           │    │
│   │   │         │     │   │ │   │ │   │  modules            │    │
│   │   │    USB◄─│─────│   │ │   │ │   │                     │    │
│   │   │         │     └─┬─┘ └─┬─┘ └─┬─┘                     │    │
│   │   └─────────┘       │     │     │                       │    │
│   │                     │     │     │                       │    │
│   │              ┌──────┴─────┴─────┴──────┐                │    │
│   │              │    Panel-mount          │ Front panel    │    │
│   │              │    K-type sockets       │                │    │
│   │              └─────────────────────────┘                │    │
│   │                                                          │    │
│   └──────────────────────────────────────────────────────────┘    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Probe Placement on Roaster

```
                    ┌─────────────────────────────────┐
                    │           EXHAUST               │
                    │             ▲                   │
                    │             │                   │
                    │      ┌──────┴──────┐           │
                    │      │             │           │
                    │      │   ◄─────────│── ET Probe│ (in exhaust flow)
                    │      │             │           │
                    │      │    DRUM     │           │
                    │      │             │           │
                    │      │   ●●●●●     │           │
                    │      │   ●●●●● ◄───│── BT Probe│ (in bean mass)
                    │      │   ●●●●●     │           │
                    │      │             │           │
                    │      └──────┬──────┘           │
                    │             │                   │
                    │      ┌──────┴──────┐           │
                    │      │   BURNER    │           │
                    │      │             │           │
                    │      │   🔥🔥🔥 ◄───│── FT Probe│ (near flame)
                    │      │             │           │
                    │      └─────────────┘           │
                    │                                 │
                    └─────────────────────────────────┘

Probe Guidelines:
- BT: Tip should be in contact with bean mass, ~2-3cm into drum
- ET: Position 10-15cm from drum exit, in exhaust airflow path
- FT: Near burner but protected from direct flame, measures radiant heat
```

## Safety Notes

1. **Heat Protection**: Thermocouple leads are rated for high temp, but keep connectors/electronics away from heat sources
2. **Grounding**: Ensure proper grounding to reduce electrical noise in readings
3. **Cable Routing**: Route thermocouple cables away from power cables to minimize interference
4. **Strain Relief**: Use cable ties or strain relief at enclosure entry points
5. **Probe Sheathing**: K-type probes are typically stainless steel sheathed - suitable for food contact
