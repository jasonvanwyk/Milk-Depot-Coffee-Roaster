# Hot Plate / PCB Preheater Options for South Africa

Date: 09 October 2026. Target: reflow a 96 x 66 mm 2-layer board (SOIC + 0805) from Johannesburg.

## Method and limits

Web search plus page fetches. Most SA shop sites (Communica, Mantech, Takealot) render with JavaScript and returned no product data, so their stock is **unverified**, not "none". Only DIY Electronics surfaced via search. Import prices below are marked "est." where I could not load a live AliExpress/Banggood page. Exchange rate assumed about R17.50/US$ (not checked live). Verify before ordering.

## Key finding: plate size decides it

The board is 96 x 66 mm (diagonal about 116 mm). Plates must exceed about 100 x 70 mm to heat it evenly.

- Miniware MHP30 plate is 30 x 30 mm: **too small**.
- Miniware MHP50 / FNIRSI HT-P1A plate is 50 x 50 mm: **too small** for the whole board (would only heat part; large gradients, warping risk).
- A 100 x 100 mm plate is the practical minimum; 200 x 200 mm is comfortable and gives even heat.

## Comparison table

| Product | Plate size | Max temp | Control | Price ZAR | Source | Lead time | URL |
|---|---|---|---|---|---|---|---|
| Miniware MHP30 PD | 30 x 30 mm | 300-350 C | Preset temps, USB-C PD, 60 W | R2,207.00 | DIY Electronics (SA) | local, days | https://www.diyelectronics.co.za/store/soldering-irons/3887-miniware-mhp30-pd-mini-hot-plate-preheater.html |
| Miniware MHP50-A5 aluminium | 50 x 50 mm | 350 C | PID, USB-C PD / DC | R1,699.15 (sale from R1,999.00) | DIY Electronics (SA) | local, days | https://www.diyelectronics.co.za/store/solder-accessories/5243-miniware-mhp50-a5-aluminium-hot-plate-preheater.html |
| Miniware MHP50-B5 brass | 50 x 50 mm | 350 C | PID, USB-C PD / DC | R2,399.95 | DIY Electronics (SA) | local, days | https://www.diyelectronics.co.za/store/soldering-irons/5244-miniware-mhp50-b5-brass-hot-plate-preheater.html |
| FNIRSI HT-P1A | 50 x 50 mm | 350 C | PID +/-3 C, 100-150 W, USB-C PD/DC | not found in SA (about A$154 in AU) | import only | 3-5 wk | https://core-electronics.com.au/fnirsi-ht-p1a-150w-mini-hot-plate-reflow-station.html |
| UYUE 946-1010 | 100 x 100 mm (per model name; size unverified) | about 350 C | Digital, thermostat | est. R1,300-1,900 landed | AliExpress / eBay | 3-5 wk | https://probots.co.in/uyue-946-1010-preheat-desoldering-rework-station-aluminium-heating-plate-220v-us-plug-bga-smd.html (spec page) |
| UYUE 946C | 200 x 200 mm, 15 mm Al plate | 350 C | Digital LED, +/-1.5 C, 800 W, 220 V | est. R2,200-2,900 landed (eBay US$87-124 + shipping + VAT) | AliExpress / eBay | 3-5 wk | https://probots.co.in/946c-800w-electronic-hot-plate-preheating-station-200x200mm.html (spec page) |
| Generic 946B/T-946 Mcup | 180 x 240 mm, 800-850 W | about 350 C | Digital | est. R1,800-2,600 landed | eBay / AliExpress | 3-5 wk | https://www.ebay.de/itm/196802474458 |
| Yihua 853A (IR plate) | 120 x 120 mm | not confirmed | PID | not found in SA | import | 3-5 wk | https://probots.co.in/yihua-853a-preheat-desoldering-rework-station-ir-heating-plate-220v-us-plug-esd-bga.html |
| Hakko FR-860 / Weller WXHP120 | large | professional | professional | well over R10,000, not priced | distributors | weeks | https://valuetronics.com/apps/aeo/ai/md/default/products/fr860-02-hakko-soldering-new.md |
| Generic 100x100 / 200x200 PTC plate | 100 or 200 mm | about 200-250 C only | Fixed PTC, no control | not priced | AliExpress | 3-5 wk | n/a |

## Notes per candidate

- **MHP30 / MHP50 / FNIRSI**: well made, but plates are 30 or 50 mm. Fine for single ICs, not for this board. USB-C PD powered, so no mains-voltage concern.
- **UYUE 946 family**: mains-powered resistive plates, PID-less to simple digital thermostat. The 946C (800 W, 200 x 200) is widely used for exactly this job (Voltlog #210 review: https://www.voltlog.com/?p=978). It has no reflow profile, so you ramp by hand and watch the plate. Fine for leaded or low-temp lead-free paste with a thermocouple/IR thermometer.
- **Generic PTC plates**: cap near 200-250 C, which is marginal for lead-free paste (about 235-245 C peak). Avoid unless using leaded paste.
- **Ersa IRHP, Aixun, Controleo**: nothing SA-stocked found; Ersa/Hakko/Weller are professional pricing. Controleo is a DIY oven controller, not a plate, so it is out of scope for the budget.
- No well-reviewed 2025-2026 100 x 100+ models turned up beyond the 946 family in the searches run. Not exhaustively searched.

## South African stock

| Retailer | Result |
|---|---|
| DIY Electronics | Stocks MHP30 and MHP50 only (prices above). Free shipping over R1,250. No large plate seen. |
| Communica, Mantech, Takealot, RS ZA, Micro Robotics, Robotics.org.za, Netram, Electro Mechanica | Could not be read (JavaScript sites / error page). No hot plate found via search. Check by phone or site search: Communica sales@communicagroup.com, +27 12 657 3500. |

Local sellers on Takealot or Facebook occasionally list the 946C; worth one manual search for "946C" and "YIHUA 946".

## Import options

- **Delivery**: AliExpress Standard to SA is typically 3-5 weeks (you already see about 4 weeks). Banggood and eBay are similar; AliExpress "local warehouse" items are faster but rare for this category.
- **Landed cost**: SARS charges 15% VAT on low-value parcels since the September 2024 change, and the old under-R500 duty concession has been closed down, so expect VAT plus possibly duty on tools/electronics (source below). Budget item price + shipping, then add 15% VAT, and about 10-20% extra for duty/handling in a worst case. Courier clearing fees (DHL/Aramex) can add roughly R100-250 if a courier delivers.
- **Voltage and plug**: 946-family plates are sold as 220 V or 110/220 V. SA mains is 230 V, so 220 V is fine. Listings often say "US plug" or "EU plug": you will need an adapter or to swap the lead, and the plug is the usual trap. SA uses a type M/N plug (the 3-pin round), so buy an earthed adapter or fit a proper SA cord. Do not use a flimsy 2-pin adapter on an 800 W heater. Confirm "220 V" in the title; avoid 110 V-only units.
- **Safety**: cheap mains plates may lack an earth connection; check the plate chassis earth before use.

## Shortlist for a 96 x 66 mm board

| Tier | Pick | Why |
|---|---|---|
| Good | Generic T-946 / 946B 180 x 240 mm plate, 220 V (est. R1,800-2,600 landed) | Cheapest way to get a plate big enough; manual ramping only. |
| Better | UYUE 946C, 200 x 200 mm, 800 W, 220 V (est. R2,200-2,900 landed) | Known reviewed unit with +/-1.5 C stability and thick plate for even heat; 3-5 week wait. |
| Best | Local-first: ask Communica/Mantech for any 200 mm plate; otherwise 946C plus a K-type probe/IR thermometer for profile control | Nothing premium with profiles is SA-stocked at hobby price. Hakko FR-860 / Weller WXHP120 are the pro step-up but cost far more. |

If you must have it this week, the only in-stock SA options (MHP50) cannot cover this board in one go; a stopgap is not recommended.

## Sources

- DIY Electronics MHP30: https://www.diyelectronics.co.za/store/soldering-irons/3887-miniware-mhp30-pd-mini-hot-plate-preheater.html
- DIY Electronics MHP50-B5: https://www.diyelectronics.co.za/store/soldering-irons/5244-miniware-mhp50-b5-brass-hot-plate-preheater.html
- DIY Electronics MHP50-A5: https://www.diyelectronics.co.za/store/solder-accessories/5243-miniware-mhp50-a5-aluminium-hot-plate-preheater.html
- Probots UYUE 946C spec: https://probots.co.in/946c-800w-electronic-hot-plate-preheating-station-200x200mm.html
- Probots UYUE 946-1010: https://probots.co.in/uyue-946-1010-preheat-desoldering-rework-station-aluminium-heating-plate-220v-us-plug-bga-smd.html
- eBay 946C listings (US$87-124): https://www.ebay.de/itm/388508518093
- eBay T-946 Mcup 180x240: https://www.ebay.de/itm/196802474458
- Voltlog 946C review: https://www.voltlog.com/?p=978
- Core Electronics FNIRSI HT-P1A: https://core-electronics.com.au/fnirsi-ht-p1a-150w-mini-hot-plate-reflow-station.html
- Core Electronics MHP30: https://core-electronics.com.au/morning-tools-mini-hot-plate-preheater-mph30.html
- Evetech on 2026 low-value parcel rules: https://evezone.evetech.co.za/quick-bytes/low-value-parcel-rules-2026-changed-sa-shoppers
- Nedbank on Shein/Temu taxes: https://personal.nedbank.co.za/learn/blog/shein-temu-taxes-south-africa.html
