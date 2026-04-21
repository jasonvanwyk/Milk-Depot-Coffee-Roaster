# MD-TC-BRK v1.0 — Schematic Drawing Guide

Reference for drawing the MAX31855 thermocouple breakout schematic from scratch in KiCad 10 Eeschema. Derived from SparkFun DEV-13266 topology, forked for the Milk Depot Coffee Roaster project.

Keep this open alongside Eeschema while drawing. Use the SparkFun reference in `eagle-source/SparkFun_Thermocouple_Breakout.sch` (open in Eagle) or the PDF in `~/tools/kicad-coffee-roaster/docs/reference-designs/sparkfun-max31855k/` as a visual template.

## Design intent (locked session 2)

- Fork of SparkFun DEV-13266, released under CC-BY-SA 4.0
- MAX31855KASA+ genuine Maxim (not MAX31855K from Eagle origin)
- DG127-5.08-02P screw terminal (not SparkFun's PCB pad pattern)
- 0805 passives throughout (upsized from SparkFun 0603)
- DNP footprints for EMI/surge mitigation (populate only if burner EMI shows up at bring-up)
- Chassis-bond footprint with default hard-bond jumper + soft-bond DNP option

## Component reference table

All symbols and footprints use KiCad 10 stock libraries unless flagged otherwise.

| Ref | Value | Symbol (`lib:name`) | Footprint (`lib:name`) | DNP | Notes |
|---|---|---|---|:---:|---|
| **U1** | MAX31855KASA+ | `Sensor_Temperature:MAX31855KASA` | `Package_SO:SOIC-8_3.9x4.9mm_P1.27mm` | | MPN field = `MAX31855KASA+`. Pin map: 1=GND, 2=T−, 3=T+, 4=VCC, 5=SCK, 6=CS, 7=SO(MISO), 8=NC |
| **C1** | 100 nF X7R 16 V | `Device:C` | `Capacitor_SMD:C_0805_2012Metric` | | +3V3 → GND decoupling, place within 5 mm of U1 pin 4 |
| **C2** | 10 nF X7R 50 V | `Device:C` | `Capacitor_SMD:C_0805_2012Metric` | | T+ ↔ T− differential filter, post-ferrite |
| **C3** | 1 nF X7R 50 V | `Device:C` | `Capacitor_SMD:C_0805_2012Metric` | **Y** | T+ ↔ GND common-mode (populate only if burner EMI) |
| **C4** | 1 nF X7R 50 V | `Device:C` | `Capacitor_SMD:C_0805_2012Metric` | **Y** | T− ↔ GND common-mode |
| **L1** | 470 Ω @ 100 MHz | `Device:FerriteBead` | `Inductor_SMD:L_0805_2012Metric` | | In-line on T+ between J1 and U1 |
| **L2** | 470 Ω @ 100 MHz | `Device:FerriteBead` | `Inductor_SMD:L_0805_2012Metric` | | In-line on T− |
| **R1** | 10 kΩ 1% | `Device:R` | `Resistor_SMD:R_0805_2012Metric` | | CS ↔ +3V3 pull-up (holds MAX31855 deselected at boot) |
| **D1** | SMAJ5.0CA (5 V bidi TVS) | `Device:D_TVS` | `Diode_SMD:D_SMA` | **Y** | T+ ↔ GND surge clamp |
| **D2** | SMAJ5.0CA (5 V bidi TVS) | `Device:D_TVS` | `Diode_SMD:D_SMA` | **Y** | T− ↔ GND surge clamp |
| **J1** | DG127-5.08-02P | `Connector:Screw_Terminal_01x02` | `Connector_Phoenix_MSTB:PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal` | | **Verify DG127 pad/drill against MSTB footprint before fab** — if mismatch, create `milk-depot.pretty/DG127-5.08-02P.kicad_mod`. Pin 1 = T+, Pin 2 = T− |
| **JP1** | 1×06 male header 2.54 mm | `Connector_Generic:Conn_01x06` | `Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical` | | Pin 1=GND, 2=+3V3, 3=SCK, 4=MISO, 5=NC, 6=CS. Cable-compatible with SparkFun DEV-13266; we rename "VCC" → "3V3" on silkscreen to be voltage-explicit (prevents 5V mis-wiring on stripboard). |
| **TP1** | T+ post-filter | `Connector:TestPoint` | `TestPoint:TestPoint_Pad_D1.5mm` | | Multimeter probe pad |
| **TP2** | T− post-filter | `Connector:TestPoint` | `TestPoint:TestPoint_Pad_D1.5mm` | | |
| **MH1** | M3 mount / chassis | `Mechanical:MountingHole_Pad` | `MountingHole:MountingHole_3.2mm_M3_Pad` | | Net = `CHASSIS` |
| **SJ1** | Solder jumper (closed) | `Jumper:SolderJumper_2_Bridged` | `Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm` | | CHASSIS ↔ GND, default populated (hard bond) |
| **CY1** | 10 nF 250 V Y1 | `Device:C` | `Capacitor_SMD:C_0805_2012Metric` | **Y** | CHASSIS ↔ GND soft-bond cap (populate only if breaking SJ1) |
| **RB1** | 1 MΩ | `Device:R` | `Resistor_SMD:R_0805_2012Metric` | | CHASSIS ↔ GND bleed (keeps chassis at DC ground when only CY1 is present) |

**DNP note:** in KiCad 10, DNP is set per-symbol via Properties → *Do not populate* checkbox (or keystroke `V`). DNP symbols stay on the PCB but are flagged in BOM exports so the assembly house skips them.

## Net list — what wires where

U1 (MAX31855KASA) pin-by-pin connections:

```
U1 pin 1 (GND)   → GND
U1 pin 2 (T−)    → node after L2 → {C2 one side, C4 top, D2 anode, TP2, J1 pin 2}
U1 pin 3 (T+)    → node after L1 → {C2 other side, C3 top, D1 anode, TP1, J1 pin 1}
U1 pin 4 (Vcc)   → +3V3 → {C1 top, R1 top, JP1 pin 2}
U1 pin 5 (SCK)   → SCK → JP1 pin 3
U1 pin 6 (CS)    → CS  → {R1 bottom, JP1 pin 6}
U1 pin 7 (SO)    → MISO → JP1 pin 4
U1 pin 8 (NC)    → No-Connect flag (don't leave floating — ERC needs explicit NC)

C1, C3, C4, D1, D2 grounds → GND
JP1 pin 1 → GND
JP1 pin 5 → No-Connect flag

CHASSIS (MH1) → SJ1 (closed) → GND
CHASSIS → CY1 → GND  (DNP)
CHASSIS → RB1 → GND
```

**Filter topology reminder** (SparkFun LC, preserved):

```
J1 ─┬── L1(470Ω) ── TP1 ── U1 pin 3 (T+)
    │                  │
    │                  └── C2(10nF) ──┐
    │                                 │
    │                  ┌── C3(1nF DNP) ─ GND
    │                  │
    │                  └── D1(TVS DNP) ─ GND
    │
    └── L2(470Ω) ── TP2 ── U1 pin 2 (T−)
                       │
                       └── (C2 other side — shared)
                       │
                       ├── C4(1nF DNP) ─ GND
                       │
                       └── D2(TVS DNP) ─ GND
```

## Draw order

1. **Power rails first** — drop `Power:+3V3` and `Power:GND` symbols (voltage-explicit names prevent the 3V3-vs-5V mis-wiring risk on the stripboard). Add a `Power:PWR_FLAG` on each (kills `power_pin_not_driven` ERC errors at source).
2. **U1 centred** — place `Sensor_Temperature:MAX31855KASA` in the middle of the sheet. Label all 8 pins with their nets before adding anything else around it.
3. **Filter network to the left of U1** — J1 → L1/L2 → U1's T+/T−, with C2 bridging between them and C3/C4 pulling down to GND; TP1/TP2 on the post-filter nets.
4. **Protection cluster** — D1/D2 on the J1 side of the filter (clamps before the ferrites, protects upstream energy).
5. **VCC cluster above U1** — C1 decoupling, R1 CS pull-up.
6. **JP1 to the right of U1** — 6-pin header, connect one wire at a time to VCC/GND/SCK/MISO/CS. Drop an explicit `No Connect` marker on JP1 pin 5.
7. **Chassis bond cluster** — MH1 + SJ1 + CY1 + RB1 in a corner, net-label `CHASSIS`. SJ1 defaults populated (hard bond); CY1 is DNP for the soft-bond option.
8. **U1 pin 8** — drop a `No Connect` marker (KiCad ERC requires it for pins marked NC in the symbol, to confirm the intent).
9. **Title block** — KiCad Eeschema → File → Page Settings:
   - Title: `MAX31855 Thermocouple Breakout — MD-TC-BRK v1.0`
   - Date: today (e.g. `2026-04-21`)
   - Rev: `1.0`
   - Company: `Precept Systems (Pty) Ltd`
   - Comment 1: `Fork of SparkFun DEV-13266 — CC-BY-SA 4.0`
   - Comment 2: `MAX31855KASA+ / DG127-5.08-02P / 0805 / DNP EMI+TVS`
   - Comment 3: `Designer: Jason van Wyk — jason@precept.co.za`

## ERC verification checklist

After drawing, run ERC (Eeschema → Inspect → Electrical Rules Checker). Target: **0 errors, 0 warnings.** Expected issues if something's missed:

- [ ] All power nets have PWR_FLAG (VCC + GND) — otherwise `power_pin_not_driven`
- [ ] U1 pin 8 has explicit No Connect — otherwise `pin_not_connected`
- [ ] JP1 pin 5 has explicit No Connect — otherwise `pin_not_connected`
- [ ] All components have footprints assigned — otherwise `footprint_link_issues`
- [ ] All components have MPN (custom property) for BOM — check via Edit Symbol Fields (Ctrl-E from Eeschema top menu)
- [ ] No dangling wires (look for green dots)
- [ ] All net labels match exactly (CS, SCK, MISO, VCC, GND, CHASSIS — no typos)

Command-line ERC (fastest iteration):

```bash
cd /home/jason/Projects/Milk-Depot-Coffee-Roaster/kicad/breakout-max31855
kicad-cli sch erc --output erc.txt breakout-max31855.kicad_sch
```

## BOM export

Once ERC-clean, export BOM for cross-check against `docs/BOM.md`:

```bash
kicad-cli sch export bom \
  --fields "Reference,Value,Footprint,MPN,DNP" \
  --group-by Value,Footprint \
  --preset "CSV" \
  --output breakout-max31855-bom.csv \
  breakout-max31855.kicad_sch
```

## Silkscreen + layout notes (for later, not schematic)

These go on the PCB, not the schematic:

- **Pin 1 dot** on U1
- **Red = NEGATIVE** warning next to J1
- **+** / **−** marked on J1 pin 1 / pin 2 silkscreen
- **3V3** label on JP1 pin 2 (replaces SparkFun's "VCC" label — voltage-explicit, eliminates the need for a separate "3.3V ONLY" warning)
- Board ID: `MD-TC-BRK v1.0 / CC-BY-SA 4.0 / fork of SparkFun DEV-13266`
- Attribution: `derived from SparkFun DEV-13266`

## References

- **SparkFun upstream (Eagle):** `eagle-source/SparkFun_Thermocouple_Breakout.sch`
- **Maxim datasheet:** `../datasheets/max31855.pdf`
- **Project design spec:** `../../docs/planning/` (architecture decisions)
- **Degson DG127 datasheet:** confirm pad/drill dimensions at <https://www.degson.com/product/DG127> before fab
- **KiCad 10 symbol libs:** `/usr/share/kicad/symbols/`
- **KiCad 10 footprint libs:** `/usr/share/kicad/footprints/`

## Design spec cross-reference

Full electrical + mechanical spec lives in the tool-repo memory: `~/.claude/projects/-home-jason-tools-kicad-coffee-roaster/memory/design-spec-v2.md`. Any deviation from this guide must go back to update that memory.
