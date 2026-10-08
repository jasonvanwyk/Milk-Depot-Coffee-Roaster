# Host-Side Routing Plan — 4-Channel TC Board

Written 8 October 2026 (layout session 4). Generated and DRC-checked by `kicad/tc-board-4ch/host-routing.py`, which applies the part moves and all tracks/vias to a scratch copy of the board and runs `kicad-cli pcb drc --refill-zones`. Result on the scratch copy: 0 clearance / shorting / starved-thermal errors, 0 unconnected items (was 37). Only silk and library warnings remain.

## Why five parts move

- **U1 (SN74AHC125)** sat at x 60–68 directly above C105, so the drops from its bottom pin row had nowhere to go. It moves east to the empty strip between the channel 1 DC-DC and J1, where every pin column is clear above and below.
- **C3** is U1's 3V3 decoupling and follows it.
- **C1, C2** (5V input caps) sat in the only corridor between the bus lanes and channel 2's isolator pins. They move onto the +5V bus between the DC-DC modules, each with its own via.
- **J2** (button header) moves up 1.5 mm so the MISO4 lane can pass under it.

| Ref | Old (x, y, rot) | New (x, y, rot) |
|-----|-----------------|-----------------|
| U1 | 64, 54.7, 90 | **77.5, 54.7, 90** |
| C3 | 58, 54.7, 90 | **71.7, 54.7, 90** |
| C1 | 87, 56.5, 0 | **96.3, 62.5, -90** |
| C2 | 90.5, 56.5, 0 | **118.5, 62.5, -90** |
| J2 | 112, 54, 0 | **112, 52.5, 0** |

Move these first (select part → E → Position). Rotation -90 puts pin 1 of C1/C2 at the top (y 61.55).

## Scheme

Short verticals on F.Cu from each pad to a via; one horizontal lane per net on B.Cu. All tracks 0.25 mm, vias 0.6/0.3 mm. Lanes are 0.63 mm apart so a via on any lane clears its neighbours by 0.205 mm.

| Lane y (B.Cu) | Net | Span x |
|---|---|---|
| 53.75 | MISO4 | 76.23 → 125.365 |
| 54.38 | CS3 | 78.77 → 105.2 |
| 55.01 | MISO3 | 80.04 → 103.365 |
| 55.64 | CS4 | 74.96 → 104.32 |
| 56.27 | +3V3 | 64.75 → 130.75 |
| 56.90 | SCK | 61.905 → 127.905 |
| 57.53 | MISO | 82.3 → 94.16 |
| 58.40 | CS1, then CS4 east leg | 60.635 → 96.7, then 104.32 → 126.635 |
| 59.05 | MISO1 west, CS2 east | 59.365 → 74.96, then 77.5 → 99.24 |
| 59.70 | MISO2 | 78.77 → 81.365 |
| 60.40 | +5V | 71.5 → 137.5 |

U1 after the move: bottom row (pins 1–7) at y 57.175, top row (pins 8–14) at y 52.225, columns x = 73.69, 74.96, 76.23, 77.5, 78.77, 80.04, 81.31. Top-row pins drop a short stub *down* under the body to a via on their lane; bottom-row pins drop *below* the body. MISO (pins 3, 6, 8, 11) is joined by an F.Cu bar at y 55.85 under the body that exits east at x 82.3. +5V reaches each DC-DC pin 1 by a short B.Cu stub straight up from the pin (no via, the pin is through-hole). GND needs only two kinds of tie: U_02 pin 2 to C_05 pin 2 on each channel, and a stub down from U1 pin 7, which clears the starved-thermal warnings.

## Step list, one net at a time

Coordinates are (x, y) in mm. Draw each track on the layer named, then DRC after each net.

### +3V3

1. F.Cu track (73.69, 52.225) → (73.69, 55.3)
2. F.Cu track (73.69, 55.3) → (71.7, 55.65)
3. F.Cu track (71.7, 55.65) → (70.6, 56.27)
4. Via at (70.6, 56.27)
5. B.Cu track (64.75, 56.27) → (130.75, 56.27)
6. Via at (64.75, 56.27)
7. F.Cu track (64.75, 56.27) → (64.75, 59.5)
8. F.Cu track (64.75, 59.5) → (64.445, 61.85)
9. Via at (86.75, 56.27)
10. F.Cu track (86.75, 56.27) → (86.75, 59.5)
11. F.Cu track (86.75, 59.5) → (86.445, 61.85)
12. Via at (108.75, 56.27)
13. F.Cu track (108.75, 56.27) → (108.75, 59.5)
14. F.Cu track (108.75, 59.5) → (108.445, 61.85)
15. Via at (130.75, 56.27)
16. F.Cu track (130.75, 56.27) → (130.75, 59.5)
17. F.Cu track (130.75, 59.5) → (130.445, 61.85)
18. F.Cu track (89.08, 52.5) → (89.08, 56.27)
19. Via at (89.08, 56.27)

### /SCK

1. B.Cu track (61.905, 56.9) → (127.905, 56.9)
2. Via at (61.905, 56.9)
3. F.Cu track (61.905, 56.9) → (61.905, 61.85)
4. Via at (83.905, 56.9)
5. F.Cu track (83.905, 56.9) → (83.905, 61.85)
6. Via at (105.905, 56.9)
7. F.Cu track (105.905, 56.9) → (105.905, 61.85)
8. Via at (127.905, 56.9)
9. F.Cu track (127.905, 56.9) → (127.905, 61.85)
10. F.Cu track (91.62, 52.5) → (91.62, 56.9)
11. Via at (91.62, 56.9)

### /MISO

1. F.Cu track (76.23, 57.175) → (76.23, 55.85)
2. F.Cu track (76.23, 55.85) → (82.3, 55.85)
3. F.Cu track (82.3, 55.85) → (82.3, 52.225)
4. F.Cu track (82.3, 52.225) → (81.31, 52.225)
5. F.Cu track (80.04, 57.175) → (80.04, 55.85)
6. F.Cu track (77.5, 52.225) → (77.5, 55.85)
7. F.Cu track (82.3, 55.85) → (82.3, 57.53)
8. Via at (82.3, 57.53)
9. B.Cu track (82.3, 57.53) → (94.16, 57.53)
10. F.Cu track (94.16, 52.5) → (94.16, 57.53)
11. Via at (94.16, 57.53)

### /CS1

1. F.Cu track (73.69, 57.175) → (73.69, 58.4)
2. Via at (73.69, 58.4)
3. B.Cu track (60.635, 58.4) → (96.7, 58.4)
4. Via at (60.635, 58.4)
5. F.Cu track (60.635, 58.4) → (60.635, 61.85)
6. F.Cu track (96.7, 52.5) → (96.7, 58.4)
7. Via at (96.7, 58.4)

### /MISO1

1. F.Cu track (74.96, 57.175) → (74.96, 59.05)
2. Via at (74.96, 59.05)
3. B.Cu track (59.365, 59.05) → (74.96, 59.05)
4. Via at (59.365, 59.05)
5. F.Cu track (59.365, 59.05) → (59.365, 61.85)

### /CS2

1. F.Cu track (77.5, 57.175) → (77.5, 59.05)
2. Via at (77.5, 59.05)
3. B.Cu track (77.5, 59.05) → (99.24, 59.05)
4. Via at (82.635, 59.05)
5. F.Cu track (82.635, 59.05) → (82.635, 61.85)
6. F.Cu track (99.24, 52.5) → (99.24, 59.05)
7. Via at (99.24, 59.05)

### /MISO2

1. F.Cu track (78.77, 57.175) → (78.77, 59.7)
2. Via at (78.77, 59.7)
3. B.Cu track (78.77, 59.7) → (81.365, 59.7)
4. Via at (81.365, 59.7)
5. F.Cu track (81.365, 59.7) → (81.365, 61.85)

### /MISO4

1. F.Cu track (76.23, 52.225) → (76.23, 53.75)
2. Via at (76.23, 53.75)
3. B.Cu track (76.23, 53.75) → (125.365, 53.75)
4. Via at (125.365, 53.75)
5. F.Cu track (125.365, 53.75) → (125.365, 61.85)

### /CS3

1. F.Cu track (78.77, 52.225) → (78.77, 54.38)
2. Via at (78.77, 54.38)
3. B.Cu track (78.77, 54.38) → (105.2, 54.38)
4. F.Cu track (101.78, 52.5) → (101.78, 54.38)
5. Via at (101.78, 54.38)
6. Via at (105.2, 54.38)
7. F.Cu track (105.2, 54.38) → (105.2, 60.3)
8. F.Cu track (105.2, 60.3) → (104.635, 60.865)
9. F.Cu track (104.635, 60.865) → (104.635, 61.85)

### /MISO3

1. F.Cu track (80.04, 52.225) → (80.04, 55.01)
2. Via at (80.04, 55.01)
3. B.Cu track (80.04, 55.01) → (103.365, 55.01)
4. Via at (103.365, 55.01)
5. F.Cu track (103.365, 55.01) → (103.365, 61.85)

### /CS4

1. F.Cu track (74.96, 52.225) → (74.96, 55.64)
2. Via at (74.96, 55.64)
3. B.Cu track (74.96, 55.64) → (104.32, 55.64)
4. F.Cu track (104.32, 52.5) → (104.32, 58.4)
5. Via at (104.32, 55.64)
6. Via at (104.32, 58.4)
7. B.Cu track (104.32, 58.4) → (126.635, 58.4)
8. Via at (126.635, 58.4)
9. F.Cu track (126.635, 58.4) → (126.635, 61.85)

### +5V

1. B.Cu track (71.5, 60.4) → (137.5, 60.4)
2. B.Cu track (71.5, 61.42) → (71.5, 60.4)
3. B.Cu track (93.5, 61.42) → (93.5, 60.4)
4. B.Cu track (115.5, 61.42) → (115.5, 60.4)
5. B.Cu track (137.5, 61.42) → (137.5, 60.4)
6. F.Cu track (86.54, 52.5) → (86.54, 55.3)
7. F.Cu track (86.54, 55.3) → (87.85, 55.3)
8. F.Cu track (87.85, 55.3) → (87.85, 60.4)
9. Via at (87.85, 60.4)
10. Via at (96.3, 60.4)
11. F.Cu track (96.3, 60.4) → (96.3, 61.55)
12. Via at (118.5, 60.4)
13. F.Cu track (118.5, 60.4) → (118.5, 61.55)

### /BTN

1. F.Cu track (106.86, 52.5) → (112, 52.5)

### GND

1. F.Cu track (81.31, 57.175) → (81.31, 58.7)
2. F.Cu track (63.175, 61.85) → (62.85, 59.5)
3. F.Cu track (85.175, 61.85) → (84.85, 59.5)
4. F.Cu track (107.175, 61.85) → (106.85, 59.5)
5. F.Cu track (129.175, 61.85) → (128.85, 59.5)
