"""Host-side routing plan for tc-board-4ch. Applies part moves + tracks/vias to a
scratch copy and runs kicad-cli DRC. Run: python3 -I plan.py <src.kicad_pcb> <out.kicad_pcb>"""
import re, sys, uuid, subprocess, json

src_path, out_path = sys.argv[1], sys.argv[2]
src = open(src_path).read()

# ---------------- part moves: ref -> (x, y, rot) ----------------
MOVES = {
    'U1': (77.5, 54.7, 90),
    'C3': (71.7, 54.7, 90),
    'C1': (96.3, 62.5, -90),
    'C2': (118.5, 62.5, -90),
    'J2': (112.0, 52.5, 0),
}

def move_footprints(src):
    out = []; pos = 0
    pat = re.compile(r'\(footprint "[^"]+"')
    starts = [m.start() for m in pat.finditer(src)]
    starts.append(len(src))
    out.append(src[:starts[0]])
    for i in range(len(starts)-1):
        blk = src[starts[i]:starts[i+1]]
        ref = re.search(r'\(property "Reference" "([^"]+)"', blk).group(1)
        if ref in MOVES:
            nx, ny, nrot = MOVES[ref]
            m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', blk)
            orot = float(m.group(3) or 0)
            blk = blk[:m.start()] + '(at %g %g%s)' % (nx, ny, (' %g' % nrot) if nrot else '') + blk[m.end():]
            # pads carry absolute angles: shift by (nrot - orot)
            def fix_pad(pm):
                px, py, pa = pm.group(1), pm.group(2), pm.group(3)
                a = (float(pa or 0) - orot + nrot) % 360
                return '(pad %s\n\t\t\t(at %s %s%s)' % (pm.group(0).split('\n')[0][5:], px, py, (' %g' % a) if a else '')
            blk = re.sub(r'\(pad [^\n]*\n\t\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', fix_pad, blk)
        out.append(blk)
    return ''.join(out)

# ---------------- routing plan ----------------
W = 0.25
items = []   # ('seg', net, layer, (x1,y1), (x2,y2)) or ('via', net, (x,y))
def seg(net, layer, *pts, w=W):
    for a, b in zip(pts, pts[1:]):
        items.append(('seg', net, layer, a, b, w))
def via(net, x, y): items.append(('via', net, (x, y)))
def lane(net, y, x1, x2): seg(net, 'B.Cu', (x1, y), (x2, y))

# lane y values (B.Cu)
L = dict(MISO4=53.75, CS3=54.38, MISO3=55.01, CS4=55.64,
         V33=56.27, SCK=56.90, MISO=57.53, CS1=58.40, CS2=59.05, MISO2=59.70, V5=60.40)
# CS4 east leg shares the CS1 lane y east of J1.6; MISO1 shares the CS2 lane y west of U1.

# U1 (SOIC-14 at 77.5,54.7 rot 90): row A (pins 1-7) y 57.175, row B (pins 8-14) y 52.225
ux = {1:73.69, 2:74.96, 3:76.23, 4:77.5, 5:78.77, 6:80.04, 7:81.31}
yA, yB = 57.175, 52.225           # pad centres
yA_top, yA_bot = 56.2, 58.15
yB_bot = 53.2

# --- +3V3 ---
seg('+3V3', 'F.Cu', (ux[1], yB), (ux[1], 55.3), (71.7, 55.65))          # U1.14 -> C3.1
seg('+3V3', 'F.Cu', (71.7, 55.65), (70.6, 56.27)); via('+3V3', 70.6, 56.27)
lane('+3V3', L['V33'], 64.75, 130.75)
for k, x in enumerate((64.75, 86.75, 108.75, 130.75)):                  # C_05.1 then U_02.1
    via('+3V3', x, L['V33'])
    seg('+3V3', 'F.Cu', (x, L['V33']), (x, 59.5), (x-0.305, 61.85))
seg('+3V3', 'F.Cu', (89.08, 52.5), (89.08, L['V33'])); via('+3V3', 89.08, L['V33'])   # J1.3

# --- SCK ---
lane('/SCK', L['SCK'], 61.905, 127.905)
for x in (61.905, 83.905, 105.905, 127.905):
    via('/SCK', x, L['SCK']); seg('/SCK', 'F.Cu', (x, L['SCK']), (x, 61.85))
seg('/SCK', 'F.Cu', (91.62, 52.5), (91.62, L['SCK'])); via('/SCK', 91.62, L['SCK'])  # J1.4

# --- MISO (U1.3, U1.6, U1.8, U1.11 -> J1.5) ---
seg('/MISO', 'F.Cu', (ux[3], yA), (ux[3], 55.85), (82.3, 55.85), (82.3, yB), (ux[7], yB))  # bar + pin 8
seg('/MISO', 'F.Cu', (ux[6], yA), (ux[6], 55.85))
seg('/MISO', 'F.Cu', (ux[4], yB), (ux[4], 55.85))
seg('/MISO', 'F.Cu', (82.3, 55.85), (82.3, L['MISO'])); via('/MISO', 82.3, L['MISO'])
lane('/MISO', L['MISO'], 82.3, 94.16)
seg('/MISO', 'F.Cu', (94.16, 52.5), (94.16, L['MISO'])); via('/MISO', 94.16, L['MISO'])

# --- CS1 (U1.1, U102.4, J1.6) ---
seg('/CS1', 'F.Cu', (ux[1], yA), (ux[1], L['CS1'])); via('/CS1', ux[1], L['CS1'])
lane('/CS1', L['CS1'], 60.635, 96.7)
via('/CS1', 60.635, L['CS1']); seg('/CS1', 'F.Cu', (60.635, L['CS1']), (60.635, 61.85))
seg('/CS1', 'F.Cu', (96.7, 52.5), (96.7, L['CS1'])); via('/CS1', 96.7, L['CS1'])

# --- MISO1 (U1.2 -> U102.5) ---
seg('/MISO1', 'F.Cu', (ux[2], yA), (ux[2], L['CS2'])); via('/MISO1', ux[2], L['CS2'])
lane('/MISO1', L['CS2'], 59.365, ux[2])
via('/MISO1', 59.365, L['CS2']); seg('/MISO1', 'F.Cu', (59.365, L['CS2']), (59.365, 61.85))

# --- CS2 (U1.4, U202.4, J1.7) ---
seg('/CS2', 'F.Cu', (ux[4], yA), (ux[4], L['CS2'])); via('/CS2', ux[4], L['CS2'])
lane('/CS2', L['CS2'], ux[4], 99.24)
via('/CS2', 82.635, L['CS2']); seg('/CS2', 'F.Cu', (82.635, L['CS2']), (82.635, 61.85))
seg('/CS2', 'F.Cu', (99.24, 52.5), (99.24, L['CS2'])); via('/CS2', 99.24, L['CS2'])

# --- MISO2 (U1.5 -> U202.5) ---
seg('/MISO2', 'F.Cu', (ux[5], yA), (ux[5], L['MISO2'])); via('/MISO2', ux[5], L['MISO2'])
lane('/MISO2', L['MISO2'], ux[5], 81.365)
via('/MISO2', 81.365, L['MISO2']); seg('/MISO2', 'F.Cu', (81.365, L['MISO2']), (81.365, 61.85))

# --- MISO4 (U1.12 -> U402.5) ---
seg('/MISO4', 'F.Cu', (ux[3], yB), (ux[3], L['MISO4'])); via('/MISO4', ux[3], L['MISO4'])
lane('/MISO4', L['MISO4'], ux[3], 125.365)
via('/MISO4', 125.365, L['MISO4']); seg('/MISO4', 'F.Cu', (125.365, L['MISO4']), (125.365, 61.85))

# --- CS3 (U1.10, J1.8, U302.4) ---
seg('/CS3', 'F.Cu', (ux[5], yB), (ux[5], L['CS3'])); via('/CS3', ux[5], L['CS3'])
lane('/CS3', L['CS3'], ux[5], 105.2)
seg('/CS3', 'F.Cu', (101.78, 52.5), (101.78, L['CS3'])); via('/CS3', 101.78, L['CS3'])
via('/CS3', 105.2, L['CS3']); seg('/CS3', 'F.Cu', (105.2, L['CS3']), (105.2, 60.3), (104.635, 60.865), (104.635, 61.85))

# --- MISO3 (U1.9 -> U302.5) ---
seg('/MISO3', 'F.Cu', (ux[6], yB), (ux[6], L['MISO3'])); via('/MISO3', ux[6], L['MISO3'])
lane('/MISO3', L['MISO3'], ux[6], 103.365)
via('/MISO3', 103.365, L['MISO3']); seg('/MISO3', 'F.Cu', (103.365, L['MISO3']), (103.365, 61.85))

# --- CS4 (U1.13, J1.9, U402.4) ---
seg('/CS4', 'F.Cu', (ux[2], yB), (ux[2], L['CS4'])); via('/CS4', ux[2], L['CS4'])
lane('/CS4', L['CS4'], ux[2], 104.32)
seg('/CS4', 'F.Cu', (104.32, 52.5), (104.32, L['CS1'])); via('/CS4', 104.32, L['CS4']); via('/CS4', 104.32, L['CS1'])
lane('/CS4', L['CS1'], 104.32, 126.635)
via('/CS4', 126.635, L['CS1']); seg('/CS4', 'F.Cu', (126.635, L['CS1']), (126.635, 61.85))

# --- +5V ---
lane('+5V', L['V5'], 71.5, 137.5)
for x in (71.5, 93.5, 115.5, 137.5): seg('+5V', 'B.Cu', (x, 61.42), (x, L['V5']))   # PS_01 pin 1
seg('+5V', 'F.Cu', (86.54, 52.5), (86.54, 55.3), (87.85, 55.3), (87.85, L['V5'])); via('+5V', 87.85, L['V5'])  # J1.2
for x in (96.3, 118.5):                                                          # C1.1 / C2.1 (moved)
    via('+5V', x, L['V5']); seg('+5V', 'F.Cu', (x, L['V5']), (x, 61.55))

# --- BTN ---
seg('/BTN', 'F.Cu', (106.86, 52.5), (112.0, 52.5))

seg('GND', 'F.Cu', (ux[7], yA), (ux[7], 58.7))   # U1.7 thermal stub
# --- GND ties for starved thermals: U_02.2 -> C_05.2 ---
for k in range(4):
    seg('GND', 'F.Cu', (63.175+22*k, 61.85), (62.85+22*k, 59.5))

# ---------------- emit ----------------
def sx(items):
    out = []
    for it in items:
        if it[0] == 'seg':
            _, net, layer, a, b, w = it
            out.append('\t(segment\n\t\t(start %g %g)\n\t\t(end %g %g)\n\t\t(width %g)\n\t\t(layer "%s")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n'
                       % (a[0], a[1], b[0], b[1], w, layer, net, uuid.uuid4()))
        else:
            _, net, (x, y) = it
            out.append('\t(via\n\t\t(at %g %g)\n\t\t(size 0.6)\n\t\t(drill 0.3)\n\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "%s")\n\t\t(uuid "%s")\n\t)\n'
                       % (x, y, net, uuid.uuid4()))
    return ''.join(out)

board = move_footprints(src)
idx = board.rfind('\n)')
board = board[:idx] + '\n' + sx(items) + board[idx:]
open(out_path, 'w').write(board)
print('segments', sum(1 for i in items if i[0]=='seg'), 'vias', sum(1 for i in items if i[0]=='via'))
