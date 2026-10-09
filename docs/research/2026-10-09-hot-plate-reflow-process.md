# Hot-Plate Reflow: Process and Consumables

Date: 9 October 2026. Board: 96 x 66 mm, 2-layer, SOIC-8, SOIC-16W, 0805, plus through-hole screw terminals and pin headers. One person, South Africa, 2-5 boards.

Confidence note: alloy temperatures and JLCPCB stencil facts come from the sources below. SA retail prices could not be verified from search (no Communica, Mantech or Takealot pages were returned) and must be checked by hand. Items marked "(general practice)" are standard hobbyist guidance, not tied to a fetched page.

## 1. Solder paste

| Alloy | Melts | Typical peak | Plate suitability |
|-------|-------|--------------|-------------------|
| Sn63/Pb37 (Chip Quik SMD291AX, MG Chemicals) | 183 C | 205-215 C | Most forgiving: low peak, good wetting, wide margin below component limits |
| Sn42/Bi58 | 138 C | 165-180 C | Gentlest on the board and easiest on a plate, but joints are brittle and a mixed Bi/Pb contamination weakens joints. Not ideal for a roaster-adjacent product with vibration/heat cycling |
| SAC305 | 217-220 C | 230-250 C | Hardest on a plate: needs a hot, well-controlled plate and a tight peak window. Use only if lead-free is required |

Recommendation: Sn63/Pb37 syringe for a hobby build used by Jason (workshop use, not sold as a consumer product). If the board will be handed to a client or must be RoHS-clean, use SAC305 and expect to need a plate that reaches 250 C and an IR thermometer.

Storage and handling (general practice): keep paste in a fridge (about 2-10 C), never freezer. Let it reach room temperature unopened for 2-4 hours before use to avoid condensation. Leaded paste in a fridge lasts roughly 6-12 months; check the label. Do not return used paste to the syringe.

Syringe vs jar: syringe (15-35 g) for hand dispensing and for small runs; it keeps paste sealed and is easy to dab onto pads. Jars (250 g) suit stencil printing at volume, not 2-5 boards.

SA availability and price: not verified. RS Components ZA lists Chip Quik SMD291AX (Sn63, no-clean) in 15 g and 35 g syringes (overseas RS prices: about 12.89 GBP for 15 g, 19.23 GBP for 35 g ex VAT, so expect roughly R350-R800 in SA after import and VAT). Check Communica, Mantech, RS ZA and Takealot directly. If SA stock is poor, DigiKey ZA (already used on this project) stocks Chip Quik TS391AX (15 g) and MG Chemicals 4860P-35G.

## 2. Stencil

JLCPCB offers framed stencils (for printing machines, fixed standard sizes) and unframed ("frameless") stencils with a custom outline. Unframed starts from about US$3 and can ship in the same parcel as the PCBs if smaller than 200 x 200 mm. A 96 x 66 mm board fits easily. Order the unframed, custom-size, stainless-steel, top-side stencil, with stencil size chosen just larger than the board (for example 120 x 100 mm) to leave a margin for tape.

Jig (general practice): tape the board down on a flat surface with a few spare bare PCBs (or 1.6 mm sheet) of equal thickness on three sides, so the stencil lies flat. Align stencil apertures to pads under good light, tape one edge with Kapton to act as a hinge, drag paste with a plastic card or small metal squeegee at roughly 45 degrees in one pass, then peel straight up.

Stencil vs syringe for 2-5 boards: with SOIC-16W (1.27 mm pitch) and 0805, hand dispensing is workable but slow and uneven. A stencil at about US$3 plus shipping is cheap compared with the time and the bridging risk, so it is worth ordering with the PCBs. Because there are through-hole parts, make sure the stencil file only has SMD apertures (the default).

## 3. Process

Typical hot-plate profile (lead-free reference values; scale down for leaded):

| Stage | Lead-free reference | Sn63 on a plate |
|-------|--------------------|-----------------|
| Preheat | ramp about 1-1.5 C/s | ramp to about 100-120 C |
| Soak | about 60 s near 150-180 C | 60-90 s at 130-150 C (general practice) |
| Reflow | peak about 245 C, 20-30 s above liquidus | peak 205-215 C, 30-60 s above 183 C |
| Cooling | gradual | lift board with tweezers/spatula onto a cool surface, no quenching |

Tell reflow is done: paste turns from grey and matte to shiny and silvery, the joints visibly slump and the parts self-align (small nudge of the board shifts them into place). Stop heating about 10-15 s after all joints are shiny; an IR thermometer or a K-type thermocouple taped to the board with Kapton confirms the temperature. Plate surface temperature differs from board temperature, so measure the board.

Defects:
- Tombstoning on 0805: caused by uneven heating or unequal paste on the two pads. Use equal paste, symmetrical pads, and heat the whole board evenly from below with a slow ramp.
- Bridging on SOIC-16W: caused by too much paste. Use the stencil with a thinner aperture reduction, or dab less paste; fix after reflow with flux and a clean iron tip or solder wick.
- Nudging: use tweezers or a toothpick only before the paste melts, and after melt a very light touch. Re-seat any skewed IC while the paste is liquid.

After reflow: clean flux residue with isopropyl alcohol and a stiff brush if using no-clean paste on a board that must look tidy (optional for no-clean). Then fit through-hole screw terminals and pin headers with an iron and rosin-core solder, since they cannot take plate reflow without damage. Order of operations if parts are on the back side: reflow one side first, then flip. For a hot plate, the side with the heavier or taller parts goes on the plate last only if it can sit flat; otherwise reflow the lighter side first. Parts on the plate side may sag but small parts usually stay by surface tension. Keep the second side to lower-mass parts, and with the same alloy do not exceed the melt for long. A Sn63 board flipped onto a Sn42/Bi58 second pass is a common trick for double-sided boards.

## 4. Safety

- Leaded paste: wash hands after handling, do not eat/drink at the bench, keep away from children, dispose of contaminated wipes as hazardous waste.
- Fumes: flux fumes irritate eyes and lungs. Ventilate, or use a small fan pulling fumes away from your face, ideally a carbon-filter fume extractor.
- Plate burns: the surface stays above 100 C well after switching off. Mark it, keep it on a heat-proof surface, use long tweezers and a metal spatula, and keep Kapton and plastics away from the hot surface.
- Do not put on the plate: components rated for low temperature (electrolytic caps, LCD modules, plastic connectors, pin headers with plastic bodies if avoidable), batteries, ESP32 modules without checking the datasheet, food-use pans or anything later used for cooking. Do not use the plate near flammable liquids such as IPA; keep IPA in a capped bottle away from the plate.

## 5. Shopping checklist

| Item | Notes |
|------|-------|
| Sn63/Pb37 paste, 15-35 g syringe (Chip Quik SMD291AX or similar) | Fridge storage |
| JLCPCB unframed stainless stencil | Order with the PCBs, size just over 96 x 66 mm |
| Squeegee / old plastic card | |
| Kapton tape | Hinge the stencil, tape the thermocouple |
| Tacky no-clean flux (gel or pen) | For rework and bridges |
| Fine tweezers (ESD, angled) | |
| Desoldering wick, 1.5-2.5 mm | Bridge fixing |
| Isopropyl alcohol 99% and stiff brush | Flux cleaning |
| IR thermometer and/or K-type thermocouple with meter | Check board temperature |
| Fume extractor or fan, nitrile gloves, safety glasses | |
| Metal spatula or long tweezers to lift board | |
| Spare bare PCBs or offcuts | Stencil jig |
| Rosin-core solder and iron for through-hole parts | |

## Sources

- https://jlcpcb.com/blog/solder-melting-point-guide
- https://jlcpcb.com/blog/low-temperature-solder-paste-sn-bi-guide
- https://docs.voltera.io/v-one/v-one-fundamentals/reflowing-solder-paste
- https://jlcpcb.com/blog/reflow-soldering-profile-explained
- https://www.allpcb.com/allelectrohub/reflow-soldering-technology-defects
- https://jlcpcb.com/resources/jlcpcb-stencil
- https://jlcpcb.com/blog/413-how-to-choose-a-smt-stencil
- https://jlcpcb.com/help/article/How-to-order-a-stencil
- https://uk.rs-online.com/web/p/solder-pastes/1466188
- https://uk.rs-online.com/web/p/solder-pastes/1466187
- https://www.digikey.com/en/products/detail/chip-quik-inc/TS391AX/7802225
- https://www.digikey.at/en/products/detail/mg-chemicals/4860P-35G/4967239
