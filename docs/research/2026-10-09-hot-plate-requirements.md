# Hot Plate Requirements for the 96 x 66 mm Roaster Board

Researched 9 October 2026. Lean pass: a few web searches plus engineering judgement. Items marked (judgement) are not directly sourced and should be checked against a specific product's datasheet.

## Board Being Assembled

- 2-layer FR4, 96 x 66 mm, large copper zones on both layers
- SOIC-8 (MAX31855), SOIC-16W (isolators, isolated DC-DC modules), 0805 passives
- A few through-hole screw terminals and headers
- Volume: one-off, 2 to 5 boards

## Method Comparison

| Method | Fit for this board | Notes |
|--------|-------------------|-------|
| Hot plate | Good, if all SMD parts are on one side | Cheapest. Heats from below, so the bottom side must be empty. Through-hole parts are hand-soldered afterwards. |
| Hot air only | Workable but slow | Hard to heat a 96 x 66 mm board with big copper pours evenly. Best as a touch-up tool. |
| Reflow oven (toaster conversion or purpose-built) | Best uniformity | More cost, more setup. Overkill for 2 to 5 boards. |

Conclusion: a hot plate is sufficient for this board. SOIC-8, SOIC-16W and 0805 are all easy reflow packages with no hidden joints (no BGA, QFN or large thermal pads). Keep a hot air gun or iron as a rework tool.

## Why Ground Pours Matter on a Plate

- A solid pour facing sparse routing on the other layer gives one region far more thermal mass and a different expansion curve, which drives warpage ([bestpcbs](https://www.bestpcbs.com/blog/2026/06/board-warpage/), [venture-mfg](https://www.venture-mfg.com/why-pcbs-warp-during-reflow/), [pcbpower](https://www.pcbpower.com/blog-detail/taking-care-of-warpage-and-thermal-profile-issues-during-assembly)).
- Similar copper coverage on both sides keeps the board flatter ([pcbpower](https://www.pcbpower.com/blog-detail/taking-care-of-warpage-and-thermal-profile-issues-during-assembly)). This board has zones on both layers, which helps.
- Board edges lose heat faster than the centre, so edge parts see a lower temperature ([pcbpower](https://www.pcbpower.com/blog-detail/taking-care-of-warpage-and-thermal-profile-issues-during-assembly)). On a plate smaller than the board this gets worse.
- (judgement) On a plate, a pour-heavy board is heated from below, so the bottom copper heats first and the top-side pads under big pours lag. SOIC pins tied to ground pours (thermal reliefs help) are the likeliest cold joints. Use the soak stage and judge by the paste, not the clock.
- (judgement) A board that bows can lift off the plate and heat unevenly. A flat aluminium plate and a gentle ramp reduce this.

## Spec Table

| Spec | Minimum sensible | Preferred | Why |
|------|-----------------|-----------|-----|
| Plate area | 100 x 100 mm usable | 150 x 120 mm or larger | Board is 96 x 66 mm. The plate must extend beyond all edges to avoid cool edges. |
| Max temperature | 280 C | 300 C+ | Lead-free peak 240 to 250 C at the board needs a plate set higher because of losses. |
| Control | PID, closed loop, with set-point | PID with programmable ramp/soak/peak profile | Fixed-temperature plates overshoot and lack a defined profile. |
| Heating element | Aluminium plate with embedded heater, or ceramic | Aluminium (spreads heat evenly) | PTC plates are self-limiting, often max out near 250 C or lower; check before buying. |
| Power at 230 V | 300 to 600 W | 600 to 1000 W | Needs enough power to ramp 1 to 2 C/s on a large plate. Check the 230 V version, not a 110 V one. |
| Uniformity | Within about 5 C across the usable area (judgement) | Stated in datasheet | Ask for or measure with a thermocouple. |
| Extras | Over-temperature protection | External thermocouple input | Lets you read the board, not the plate. |
| Reference product class | FNIRSI HT-P1A, 150 W mini plate ([core-electronics](https://core-electronics.com.au/fnirsi-ht-p1a-150w-mini-hot-plate-reflow-station.html)) | Larger 600 W+ units | The 150 W mini class is small for a 96 x 66 mm board. Check its plate dimensions first. |

## Solder Paste Temperatures

| Alloy | Melting | Typical peak | Time above liquidus |
|-------|---------|-------------|--------------------|
| Sn96.5/Ag3/Cu0.5 (SAC305) | 217 to 220 C | 240 to 250 C | 45 to 90 s |
| Sn63/Pb37 | 183 C (eutectic) | 210 to 230 C | 45 to 75 s |

Sources: [JLCPCB solder guide](https://jlcpcb.com/blog/solder-melting-point-guide), [zbotic profile](https://zbotic.in/pcb-reflow-profile-temperature-curve-for-lead-free/), [IPC](https://www.ipc.org/system/files/technical_resource/E16%26S39-03.pdf).

Leaded paste is more forgiving: lower peak, lower warpage risk, and an easier first hot plate board. Lead-free needs a plate that comfortably exceeds 250 C. The choice of paste should be settled before buying the plate.

Typical profile for guidance ([zbotic](https://zbotic.in/reflow-soldering-with-hot-plate-diy-smd-assembly-guide/)):

- Preheat: ramp 1 to 2 C/s from 25 to 150 C
- Soak: 150 to 200 C for 60 to 90 s
- Reflow: above 217 C, peak 235 to 250 C for 20 to 30 s
- Cool: about 2 to 4 C/s

## Pitfalls

- **Thermal lag:** the plate surface leads the board temperature, and a thick pour-heavy board lags further. Do not trust the plate display as the board temperature.
- **Measure the board:** tape a thermocouple (K-type, which this project already has) to a pad or the board top next to a SOIC. (judgement)
- **Tombstoning of 0805:** caused by one pad wetting before the other. Mitigations: even paste volume, slow ramp, a soak stage, and heating from below only (plates already heat evenly, which helps). Avoid one pad tied to a big pour without thermal relief. (judgement)
- **Through-hole parts:** do not put on the plate. Solder the screw terminals and headers by hand afterwards.
- **Bottom-side parts:** a plate cannot reflow a populated bottom side. Keep all SMD on the top, or do the second side with hot air or an oven.
- **When to pull the board:** when the paste visibly turns shiny and flows, and the parts self-align, then hold briefly and lift. Lifting the board off the plate onto a heat-safe surface cools faster than waiting for the plate. (judgement)
- **Cool-down:** the plate stays hot for a long time. Lift the board off with tweezers or a spatula and let it cool in air, avoiding cold-metal shock. Warp risk is highest when a hot board sits on a cooling plate.
- **Flux and fumes:** ventilate. (judgement)

## Recommended Spec Sheet to Shop Against

- Aluminium plate, at least 120 x 120 mm usable (bigger than 96 x 66 mm with margin on every side)
- 230 V mains, 600 W or more
- Max temperature 300 C or better (280 C absolute minimum for lead-free)
- PID control, ideally with a programmable profile; at least accurate set-point holding
- Over-temperature cutoff
- Separate thermocouple input is a bonus; otherwise buy a K-type meter or use the existing MAX31855 hardware
- Flat surface and sturdy legs (board must sit flat)
- Budget stance: for 2 to 5 boards, a mid-range PID plate is enough. Do not pay for a reflow oven.
- Use leaded paste if it is acceptable for this one-off, otherwise lead-free with a 300 C plate.
- Also get: a hot air gun or fine-tip iron for touch-up, a stencil or syringe paste dispenser, and tweezers.

## Sources

- https://zbotic.in/reflow-soldering-with-hot-plate-diy-smd-assembly-guide/
- https://zbotic.in/pcb-hot-plate-reflow-soldering-with-pid-control/
- https://zbotic.in/pcb-reflow-profile-temperature-curve-for-lead-free/
- https://core-electronics.com.au/fnirsi-ht-p1a-150w-mini-hot-plate-reflow-station.html
- https://www.pcbpower.com/blog-detail/taking-care-of-warpage-and-thermal-profile-issues-during-assembly
- https://www.venture-mfg.com/why-pcbs-warp-during-reflow/
- https://www.bestpcbs.com/blog/2026/06/board-warpage/
- https://jlcpcb.com/blog/solder-melting-point-guide
- https://www.ipc.org/system/files/technical_resource/E16%26S39-03.pdf
