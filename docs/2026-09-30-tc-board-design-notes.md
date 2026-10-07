# 4-Channel Isolated Thermocouple Board — Design Notes

Decided 30 September 2026. One board carries four isolated MAX31855 channels (three fitted: BT, ET, FT) and connects to a LilyGO T-Display-S3. These notes are the input for the schematic; they supersede the single-breakout v1.0/v1.1 guide in `kicad/breakout-max31855/schematic-guide.md` wherever the two disagree.

## Why each channel has its own isolated island

All six probes are grounded-junction (DMM test, April 2026), so every probe tip is joined to the others through the roaster chassis. The MAX31855 connects T− to its own ground through an internal switch during conversion and opens that switch during fault detection (datasheet, "Conversion Functions"). On a shared island, a chip in its fault-detection phase would see T− tied to ground through a neighbouring chip and report a short-to-GND fault. This is inferred from the datasheet, not bench-tested. Separate islands remove the path entirely.

## Per channel (isolated side, nets suffixed `_ISO`)

- RFB-0505S isolated DC-DC: host 5V in, `+5V_ISO` out. Output runs above 5V at light load (load regulation is only specified from 10%).
- NCP1117ST33T3G: `+5V_ISO` → `+3V3_ISO`. Output capacitor must be the 10 µF tantalum (TPSB106K016R0800, ESR 0.8 Ω max); the regulator needs 0.033–2.2 Ω ESR and 0805 ceramics are too low. Stripe on the tantalum = positive.
- MAX31855KASA+ with 100 nF decoupling and 10K CS pull-up to `+3V3_ISO`.
- ISO7731DWR island side powered from `+3V3_ISO` (not from the DC-DC output).
- 10K pull resistor on `MISO_ISO`: the MAX31855 SO pin is high-impedance when CS is high, so the isolator input must not float.
- Input filter and protection per probe line: ferrite BLM21AG471SN1D in series on T+ and T−, 10 nF across T+/T−, 1 nF from each line to `GND_ISO`, SMAJ5.0CA from each line to `GND_ISO`. The TVS can leak up to 1.6 mA at 5V; it only sees millivolts here, but it is the first suspect if false faults appear at bring-up.
- DG127-5.08-02P screw terminal. Pin 1 = T+, pin 2 = T−. K-type red wire is negative.
- Chassis network (mounting hole, solder jumper, 10 nF 630V, 1 MΩ): **left out, decided 7 October 2026.** The probes are grounded-junction, so each island is already referenced to the roaster body through its probe; closing the jumper would put T− to island ground in parallel with that and give a constant short-to-GND fault, so the jumper could never be closed. The plastic enclosure has no chassis to bond to, and the ferrite / TVS / 1 nF input filters cover the noise role. Mounting holes are plain, unconnected. **Caveat for a future revision:** if insulated-junction probes are ever fitted, the islands float and a bleed network (1 MΩ + 10 nF 630 V from island ground to a chassis point) becomes worth having. The RC0805FR-071ML and C0805C103KBRACAUTO parts from the 30 September order are on hand for that.

## Host side (shared by all channels)

- 5V from the T-Display-S3 5V pin feeds the four DC-DC inputs (each draws 25–30 mA idle, about 120 mA total) with 10 µF + 100 nF at the entry.
- 3.3V from the T-Display-S3 feeds the host side of every ISO7731 and the SN74AHC125, so nothing driven back to the ESP32 exceeds 3.3V.
- SN74AHC125DR quad buffer: each channel's isolator MISO output goes through one buffer whose active-low enable is that channel's CS. Without it, four isolator outputs would drive the shared MISO line at once.
- ISO7731 (non-F) outputs default high if the input side loses power, which keeps each MAX31855 deselected.
- Host connector: GND, +5V, +3V3, SCK, MISO, CS1, CS2, CS3, CS4.

## ISO7731DWR pinout (SOIC-16 wide)

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | VCC1 | 16 | VCC2 |
| 2 | GND1 | 15 | GND2 |
| 3 | INA | 14 | OUTA |
| 4 | INB | 13 | OUTB |
| 5 | OUTC | 12 | INC |
| 6 | NC | 11 | NC |
| 7 | EN1 | 10 | EN2 |
| 8 | GND1 | 9 | GND2 |

From `docs/parts-specs/iso7730.pdf` Figure 4-2. Side 1 = host (SCK and CS in on A/B, MISO out on C). Side 2 = island. EN pins are active high and may be left open.

## RFB-0505S pinout (SIP7)

Pin 1 +Vin, pin 2 −Vin, pin 4 −Vout, pin 6 +Vout. 19.6 × 6.0 × 10.2 mm. 1 kVDC functional isolation.

## DigiKey order — placed and paid 30 September 2026

Enough for two boards (eight channels).

| MPN | DigiKey PN | Qty | Use |
|---|---|---|---|
| ISO7731DWR | 296-44899-1-ND | 10 | Digital isolator, one per channel |
| RFB-0505S | 945-3158-ND | 8 | Isolated DC-DC, one per channel (no spares) |
| SN74AHC125DR | 296-4530-1-ND | 10 | MISO buffer, one per board |
| TPSB106K016R0800 | 478-2398-1-ND | 20 | 10 µF tantalum, regulator output |
| BLM21AG471SN1D | 490-1039-1-ND | 20 | Ferrite, two per channel |
| CL21B102KBANNNC | 1276-1020-1-ND | 20 | 1 nF, two per channel |
| SMAJ5.0CA-13-F | SMAJ5.0CA-FDICT-ND | 20 | TVS, two per channel |
| RC0805FR-071ML | 311-1.00MCRCT-ND | 10 | 1 MΩ bleed |
| C0805C103KBRACAUTO | 399-C0805C103KBRACAUTOCT-ND | 20 | 10 nF 630V, optional fit |

All nine datasheets are in `docs/parts-specs/` and were checked against the order. Already on hand: MAX31855KASA+ ×9, NCP1117ST33T3G ×10, DG127 screw terminals ×15, 0805 10K / 100 nF / 10 nF / 10 µF, pin headers.

## Still to buy

- ~~LilyGO T-Display-S3, non-touch~~ — ordered 30 September 2026: 1× with unsoldered pins from the LilyGO Official Store on AliExpress, ref 3076608492140357, R373.98 including shipping. A second as a spare is optional (Micro Robotics lists it at R315.00 ex VAT, no stock on 30 September 2026).
- ~~Panel-mount push button for cycling display pages~~ — ordered 2 October 2026: 10× 16 mm flat-head metal, momentary, 1NO, no LED, pre-wired, AliExpress ref 3076815630860357. Needs a 16 mm panel hole. Wire to a spare T-Display-S3 pin and GND through a 2-pin connector on this board; internal pull-up in firmware.
- ~~Spare RFB-0505S~~ — bought.
- Connector and cable between the board and the T-Display-S3, chosen at layout time.
- PCBs from JLCPCB once the layout is done.

## Corrections to the April 2026 notes in `~/tools/kicad-coffee-roaster/`

- ISO7421 was named as the isolator; it has only two channels. Three are needed.
- NMA0505SC was named as a DC-DC candidate; it is a dual-output part.
- Three breakouts sharing one MISO line would have clashed; the quad buffer fixes this.
- 3 kV isolation was specified; the fitted DC-DC is 1 kV functional, which is sufficient for ground-loop and ignition-noise isolation (this is not a mains safety barrier).

## Footprint check before layout (7 October 2026)

Each provisional footprint was compared with the part drawing. Pad positions and drills are the pass/fail items; body outlines matter only for placement.

| Ref | Part | Footprint | Result |
|---|---|---|---|
| PS101–PS401 | RFB-0505S (SIP7, pins 1/2/4/6) | `Converter_DCDC_TRACO_TMA-05xxS_12xxS_Single_THT` | **Pass.** Pads at 0 / 2.54 / 7.62 / 12.7 mm, 1.0 mm drill, exactly the RFB recommended footprint. Body outline 19.7 × 6.3 mm vs 19.6 × 6.0 mm, pin 1 2.2 mm from the end vs 2.0 mm. Keep. |
| J2 | Button, JST PH 2-pin (B2B-PH-K-S) | `JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | **Pass.** 2.0 mm pitch, 0.75 mm drill for the 0.7 mm hole JST specifies. Keep. |
| J1 | Host, 1×10 header | `PinHeader_1x10_P2.54mm_Vertical` | **Placeholder.** Correct for a plain header; replace once the board-to-display cable is chosen. |
| J101–J401 | DG127-5.08-02P screw terminal | `PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal` | **Pads pass, outline wrong.** 5.08 mm pitch and 1.4 mm drill match the DG127 drawing. The Phoenix body is drawn 12 mm deep (2 mm behind the pin row, 10 mm to the wire face); the DG127 is 8.1 mm deep (3.9 mm behind the pins, 4.2 mm to the wire face). Replaced by `milk-depot:Degson_DG127-5.08-02P_1x02_P5.08mm_Horizontal` (true 10.16 × 8.1 mm outline, pin row 3.9 mm from the back edge and 4.2 mm from the wire face, box 3D model in `kicad/libs/milk-depot.3dshapes/`). Assign it to J101 in `channel.kicad_sch`; the four instances follow. |
| C108–C408 | TPSB106K016R0800 (B case) | `CP_EIA-3528-21_Kemet-B` | Pass. |
| D101–D402 | SMAJ5.0CA-13-F | `D_SMA` | Pass. |
| FB101–FB402 | BLM21AG471SN1D | `L_0805_2012Metric` | Pass (BLM21 is 0805). |

Everything else is 0805, SOIC-8, SOIC-14, SOIC-16W or SOT-223 and matches the ordered MPNs.
