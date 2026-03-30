#!/usr/bin/env python3
"""Generate KiCad 9 schematic for Milk Depot Coffee Roaster thermocouple system.

Updated design based on actual components on hand:
- Arduino Nano (USB-C, ATmega328P) — powered via USB from RPi
- 2x MAX31855 breakout modules (BT and ET channels)
- 1.3" IIC OLED display (SH1106/SSD1306, I2C)
- 2x K-type thermocouples (35mm/2.5mm for BT, 50mm/3.0mm for ET)
- 2x 100nF decoupling capacitors on MAX31855 VCC/GND
- No barrel jack — all powered from RPi USB via Arduino Nano
"""

import json
import uuid
import os

def uid():
    return str(uuid.uuid4())

ROOT_UUID = uid()

# === LAYOUT POSITIONS (schematic coords: x-right, y-down) ===

NANO_POS = (195, 95)

# Two MAX31855 modules, stacked vertically with good spacing
MAX_POSITIONS = {
    'BT': (100, 65),
    'ET': (100, 110),
}

# Thermocouple connectors (mirrored y, so pins face right)
TC_POSITIONS = {
    'BT': (62, 65),
    'ET': (62, 110),
}

# OLED connector position (right side of schematic, near Arduino I2C pins)
OLED_POS = (240, 85)

# Decoupling cap positions (near each MAX31855)
CAP_POSITIONS = {
    'BT': (85, 50),   # above U1
    'ET': (85, 95),    # above U2
}

# === PIN POSITIONS (symbol-local coords, y-up) ===

def pin_abs(sym_pos, pin_local):
    """Convert symbol-local pin position to schematic absolute position."""
    sx, sy = sym_pos
    px, py = pin_local
    return (sx + px, sy - py)

def pin_abs_mirror_y(sym_pos, pin_local):
    """Convert with y-axis mirror (x negated in local coords)."""
    sx, sy = sym_pos
    px, py = pin_local
    return (sx - px, sy - py)

# Arduino Nano v3.x pin positions (symbol-local)
NANO_PINS = {
    'D0/RX': (-12.7, 15.24), 'D1/TX': (-12.7, 12.7),
    'D2': (-12.7, 10.16), 'D3': (-12.7, 7.62),
    'D4': (-12.7, 5.08), 'D5': (-12.7, 2.54),
    'D6': (-12.7, 0), 'D7': (-12.7, -2.54),
    'D8': (-12.7, -5.08), 'D9': (-12.7, -7.62),
    'D10': (-12.7, -10.16), 'D11': (-12.7, -12.7),
    'D12': (-12.7, -15.24), 'D13': (-12.7, -17.78),
    '+5V': (5.08, 25.4), 'GND': (0, -25.4), 'GND_2': (2.54, -25.4),
    'VIN': (-2.54, 25.4), '3V3': (2.54, 25.4),
    'A0': (12.7, 0), 'A1': (12.7, -2.54),
    'A2': (12.7, -5.08), 'A3': (12.7, -7.62),
    'A4': (12.7, -10.16), 'A5': (12.7, -12.7),
    'A6': (12.7, -15.24), 'A7': (12.7, -17.78),
}

# All Nano pin numbers for the symbol instance
NANO_PIN_NUMS = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
]

# MAX31855 pin positions (symbol-local)
MAX_PINS = {
    'T+': (-10.16, 2.54), 'T-': (-10.16, -2.54),
    'VCC': (0, 10.16), 'GND': (0, -7.62),
    'SCK': (10.16, 5.08), 'SO': (10.16, 2.54),
    'CS': (10.16, -2.54),
}
MAX_PIN_NUMS = ['1', '2', '3', '4', '5', '6', '7', '8']

# Conn_01x02 pin positions (symbol-local)
CONN2_PINS = {
    'Pin_1': (-5.08, 0),
    'Pin_2': (-5.08, -2.54),
}

# Conn_01x04 pin positions (symbol-local) — for OLED
CONN4_PINS = {
    'Pin_1': (-5.08, 3.81),
    'Pin_2': (-5.08, 1.27),
    'Pin_3': (-5.08, -1.27),
    'Pin_4': (-5.08, -3.81),
}

# Device:C pin positions (symbol-local)
CAP_PINS = {
    '1': (0, 3.81),   # top, angle 270
    '2': (0, -3.81),  # bottom, angle 90
}


# === ELEMENT GENERATORS ===

def wire(x1, y1, x2, y2):
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1}) (xy {x2} {y2})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid()}")
\t)"""

def label(name, x, y, angle=0):
    return f"""\t(label "{name}"
\t\t(at {x} {y} {angle})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t)
\t\t(uuid "{uid()}")
\t)"""

def text_note(txt, x, y, size=1.524):
    return f"""\t(text "{txt}"
\t\t(exclude_from_sim no)
\t\t(at {x} {y} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size {size} {size})
\t\t\t)
\t\t\t(justify left)
\t\t)
\t\t(uuid "{uid()}")
\t)"""

pwr_counter = [1]
def next_pwr():
    n = pwr_counter[0]
    pwr_counter[0] += 1
    return f"#PWR{n:02d}"

def power_symbol(lib_id, ref, value, x, y, angle=0):
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} {angle})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x} {y + 3.81 if 'GND' not in ref else y - 3.81} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x} {y - 3.556 if value == '+5V' else y + 3.81} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project ""
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""

def component_symbol(lib_id, ref_prefix, ref, value, x, y, angle=0,
                     mirror_y=False, pin_nums=None):
    mirror = "\n\t\t(mirror y)" if mirror_y else ""
    pins = ""
    if pin_nums:
        for pnum in pin_nums:
            pins += f'\n\t\t(pin "{pnum}"\n\t\t\t(uuid "{uid()}")\n\t\t)'

    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} {angle}){mirror}
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x} {y - 15 if ref_prefix == 'A' else y - 10} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x} {y + 15 if ref_prefix == 'A' else y + 10} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t){pins}
\t\t(instances
\t\t\t(project ""
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""


# === BUILD SCHEMATIC ELEMENTS ===

elements = []

# --- Title and annotations ---
elements.append(text_note(
    "Milk Depot Coffee Roaster — 2-Channel Thermocouple System", 55, 28, 2.0))
elements.append(text_note("K-Type Thermocouples", 48, 48))
elements.append(text_note("SPI Bus (shared)", 125, 48))
elements.append(text_note("I2C OLED Display", 225, 70))

# --- Arduino Nano ---
elements.append(component_symbol(
    "MCU_Module:Arduino_Nano_v2.x", "A", "A1", "Arduino Nano",
    *NANO_POS, pin_nums=NANO_PIN_NUMS))

# --- MAX31855 modules (BT and ET only) ---
max_refs = {'BT': 'U1', 'ET': 'U2'}
for ch in ['BT', 'ET']:
    elements.append(component_symbol(
        "Sensor_Temperature:MAX31855KASA", "U", max_refs[ch], "MAX31855KASA",
        *MAX_POSITIONS[ch], pin_nums=MAX_PIN_NUMS))

# --- Thermocouple connectors (mirrored y so pins face right) ---
tc_refs = {'BT': 'J1', 'ET': 'J2'}
tc_labels = {'BT': 'BT Thermocouple\\n(35mm/2.5mm)', 'ET': 'ET Thermocouple\\n(50mm/3.0mm)'}
for ch in ['BT', 'ET']:
    elements.append(component_symbol(
        "Connector_Generic:Conn_01x02", "J", tc_refs[ch], tc_labels[ch],
        *TC_POSITIONS[ch], mirror_y=True, pin_nums=['1', '2']))

# --- OLED connector (Conn_01x04, mirrored y) ---
elements.append(component_symbol(
    "Connector_Generic:Conn_01x04", "J", "J3", "OLED 1.3in IIC",
    *OLED_POS, mirror_y=True, pin_nums=['1', '2', '3', '4']))

# --- Decoupling capacitors ---
for ch in ['BT', 'ET']:
    cap_ref = 'C1' if ch == 'BT' else 'C2'
    elements.append(component_symbol(
        "Device:C", "C", cap_ref, "100nF",
        *CAP_POSITIONS[ch], pin_nums=['1', '2']))


# === WIRING ===

LABEL_STUB = 7.62

# --- Thermocouple connectors to MAX31855 T+/T- ---
for ch in ['BT', 'ET']:
    cx, cy = TC_POSITIONS[ch]
    mx, my = MAX_POSITIONS[ch]

    c_pin1 = pin_abs_mirror_y((cx, cy), CONN2_PINS['Pin_1'])
    c_pin2 = pin_abs_mirror_y((cx, cy), CONN2_PINS['Pin_2'])
    m_tplus = pin_abs((mx, my), MAX_PINS['T+'])
    m_tminus = pin_abs((mx, my), MAX_PINS['T-'])

    # Wire Pin_1 → T+
    if abs(c_pin1[1] - m_tplus[1]) < 0.01:
        elements.append(wire(c_pin1[0], c_pin1[1], m_tplus[0], m_tplus[1]))
    else:
        elements.append(wire(c_pin1[0], c_pin1[1], c_pin1[0], m_tplus[1]))
        elements.append(wire(c_pin1[0], m_tplus[1], m_tplus[0], m_tplus[1]))

    # Wire Pin_2 → T-
    if abs(c_pin2[1] - m_tminus[1]) < 0.01:
        elements.append(wire(c_pin2[0], c_pin2[1], m_tminus[0], m_tminus[1]))
    else:
        elements.append(wire(c_pin2[0], c_pin2[1], c_pin2[0], m_tminus[1]))
        elements.append(wire(c_pin2[0], m_tminus[1], m_tminus[0], m_tminus[1]))

# --- SPI labels on MAX31855 side (with wire stubs) ---
for ch in ['BT', 'ET']:
    mx, my = MAX_POSITIONS[ch]
    sck = pin_abs((mx, my), MAX_PINS['SCK'])
    so = pin_abs((mx, my), MAX_PINS['SO'])
    cs = pin_abs((mx, my), MAX_PINS['CS'])

    elements.append(wire(sck[0], sck[1], sck[0] + LABEL_STUB, sck[1]))
    elements.append(wire(so[0], so[1], so[0] + LABEL_STUB, so[1]))
    elements.append(wire(cs[0], cs[1], cs[0] + LABEL_STUB, cs[1]))

    elements.append(label("SCK", sck[0] + LABEL_STUB, sck[1], 0))
    elements.append(label("MISO", so[0] + LABEL_STUB, so[1], 0))
    elements.append(label(f"CS_{ch}", cs[0] + LABEL_STUB, cs[1], 0))

# --- SPI labels on Nano side (with wire stubs) ---
# D13=SCK, D12=MISO, D10=CS_BT, D9=CS_ET
for pin_name, lbl in [('D13', 'SCK'), ('D12', 'MISO'),
                       ('D10', 'CS_BT'), ('D9', 'CS_ET')]:
    pos = pin_abs(NANO_POS, NANO_PINS[pin_name])
    elements.append(wire(pos[0], pos[1], pos[0] - LABEL_STUB, pos[1]))
    elements.append(label(lbl, pos[0] - LABEL_STUB, pos[1], 180))

# --- I2C labels on Nano side (with wire stubs) ---
for pin_name, lbl in [('A4', 'SDA'), ('A5', 'SCL')]:
    pos = pin_abs(NANO_POS, NANO_PINS[pin_name])
    elements.append(wire(pos[0], pos[1], pos[0] + LABEL_STUB, pos[1]))
    elements.append(label(lbl, pos[0] + LABEL_STUB, pos[1], 0))

# --- OLED connector wiring (mirrored y) ---
# OLED pins: 1=VDD, 2=GND, 3=SCK(SCL), 4=SDA
oled_pin1 = pin_abs_mirror_y(OLED_POS, CONN4_PINS['Pin_1'])  # VDD
oled_pin2 = pin_abs_mirror_y(OLED_POS, CONN4_PINS['Pin_2'])  # GND
oled_pin3 = pin_abs_mirror_y(OLED_POS, CONN4_PINS['Pin_3'])  # SCL
oled_pin4 = pin_abs_mirror_y(OLED_POS, CONN4_PINS['Pin_4'])  # SDA

# +5V on OLED VDD
elements.append(power_symbol("power:+5V", next_pwr(), "+5V",
                             oled_pin1[0] + 5.08, oled_pin1[1]))
elements.append(wire(oled_pin1[0], oled_pin1[1],
                     oled_pin1[0] + 5.08, oled_pin1[1]))

# GND on OLED GND
elements.append(power_symbol("power:GND", next_pwr(), "GND",
                             oled_pin2[0] + 5.08, oled_pin2[1]))
elements.append(wire(oled_pin2[0], oled_pin2[1],
                     oled_pin2[0] + 5.08, oled_pin2[1]))

# SCL and SDA labels on OLED side
elements.append(wire(oled_pin3[0], oled_pin3[1],
                     oled_pin3[0] + LABEL_STUB, oled_pin3[1]))
elements.append(label("SCL", oled_pin3[0] + LABEL_STUB, oled_pin3[1], 0))

elements.append(wire(oled_pin4[0], oled_pin4[1],
                     oled_pin4[0] + LABEL_STUB, oled_pin4[1]))
elements.append(label("SDA", oled_pin4[0] + LABEL_STUB, oled_pin4[1], 0))

# --- Decoupling cap wiring ---
for ch in ['BT', 'ET']:
    mx, my = MAX_POSITIONS[ch]
    cpx, cpy = CAP_POSITIONS[ch]

    # Cap pin 1 (top) → +5V
    cap_top = pin_abs((cpx, cpy), CAP_PINS['1'])
    elements.append(power_symbol("power:+5V", next_pwr(), "+5V",
                                 cap_top[0], cap_top[1]))

    # Cap pin 2 (bottom) → GND
    cap_bot = pin_abs((cpx, cpy), CAP_PINS['2'])
    elements.append(power_symbol("power:GND", next_pwr(), "GND",
                                 cap_bot[0], cap_bot[1]))

# --- Power symbols on MAX31855 modules ---
for ch in ['BT', 'ET']:
    mx, my = MAX_POSITIONS[ch]
    vcc = pin_abs((mx, my), MAX_PINS['VCC'])
    gnd = pin_abs((mx, my), MAX_PINS['GND'])
    elements.append(power_symbol("power:+5V", next_pwr(), "+5V", vcc[0], vcc[1]))
    elements.append(power_symbol("power:GND", next_pwr(), "GND", gnd[0], gnd[1]))

# --- Power symbols on Arduino Nano ---
nano_5v = pin_abs(NANO_POS, NANO_PINS['+5V'])
nano_gnd = pin_abs(NANO_POS, NANO_PINS['GND'])
elements.append(power_symbol("power:+5V", next_pwr(), "+5V", nano_5v[0], nano_5v[1]))
elements.append(power_symbol("power:GND", next_pwr(), "GND", nano_gnd[0], nano_gnd[1]))


# === ASSEMBLE SCHEMATIC FILE ===

def read_lib_symbol(lib_file, symbol_name):
    """Extract a symbol definition from a .kicad_sym library file."""
    with open(f'/usr/share/kicad/symbols/{lib_file}') as f:
        content = f.read()

    start_marker = f'(symbol "{symbol_name}"'
    start = content.find(start_marker)
    if start == -1:
        raise ValueError(f"Symbol {symbol_name} not found in {lib_file}")

    depth = 0
    i = start
    while i < len(content):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                break
        i += 1

    raw = content[start:i+1]
    lines = raw.split('\n')
    indented = '\n'.join('\t\t' + line if line.strip() else line for line in lines)
    return indented


lib_symbols = []
# Use v2.x directly — v3.x uses 'extends' which doesn't work in embedded lib_symbols
lib_symbols.append(read_lib_symbol('MCU_Module.kicad_sym', 'Arduino_Nano_v2.x'))
lib_symbols.append(read_lib_symbol('Sensor_Temperature.kicad_sym', 'MAX31855KASA'))
lib_symbols.append(read_lib_symbol('Connector_Generic.kicad_sym', 'Conn_01x02'))
lib_symbols.append(read_lib_symbol('Connector_Generic.kicad_sym', 'Conn_01x04'))
lib_symbols.append(read_lib_symbol('Device.kicad_sym', 'C'))
lib_symbols.append(read_lib_symbol('power.kicad_sym', '+5V'))
lib_symbols.append(read_lib_symbol('power.kicad_sym', 'GND'))

lib_symbols_text = '\n'.join(lib_symbols)

# Add library prefixes to top-level symbol names
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "Arduino_Nano_v2.x"', '(symbol "MCU_Module:Arduino_Nano_v2.x"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "MAX31855KASA"', '(symbol "Sensor_Temperature:MAX31855KASA"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "Conn_01x02"', '(symbol "Connector_Generic:Conn_01x02"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "Conn_01x04"', '(symbol "Connector_Generic:Conn_01x04"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "C"', '(symbol "Device:C"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "+5V"', '(symbol "power:+5V"', 1)
lib_symbols_text = lib_symbols_text.replace(
    '(symbol "GND"', '(symbol "power:GND"', 1)

schematic = f"""(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid "{ROOT_UUID}")
\t(paper "A4")
\t(title_block
\t\t(title "Milk Depot Coffee Roaster - 2-Channel Thermocouple System")
\t\t(date "2026-03-13")
\t\t(company "Precept Systems (Pty) Ltd")
\t\t(comment 1 "2-channel K-type thermocouple interface for Artisan coffee roasting software")
\t\t(comment 2 "Arduino Nano + 2x MAX31855 via SPI + 1.3in OLED (I2C) + RPi 4")
\t)
\t(lib_symbols
{lib_symbols_text}
\t)
{chr(10).join(elements)}
)
"""

sch_path = os.path.join(os.path.dirname(__file__), 'milk-depot-coffee-roaster.kicad_sch')
with open(sch_path, 'w') as f:
    f.write(schematic)
print(f"Wrote schematic: {sch_path}")

# Write project file
pro_path = os.path.join(os.path.dirname(__file__), 'milk-depot-coffee-roaster.kicad_pro')
project = {
    "board": {
        "3dviewports": [], "layer_pairs": [], "layer_presets": [], "viewports": [],
        "ipc2581": {"dist": "", "distpn": "", "internal_id": "", "mfg": "", "mpn": ""},
    },
    "boards": [],
    "cvpcb": {"equivalence_files": []},
    "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
    "meta": {"filename": "milk-depot-coffee-roaster.kicad_pro", "version": 2},
    "net_settings": {
        "classes": [{"bus_width": 12, "clearance": 0.2, "diff_pair_gap": 0.25,
                     "diff_pair_via_gap": 0.25, "diff_pair_width": 0.2, "line_style": 0,
                     "microvia_diameter": 0.3, "microvia_drill": 0.1, "name": "Default",
                     "pcb_color": "rgba(0, 0, 0, 0.000)",
                     "schematic_color": "rgba(0, 0, 0, 0.000)", "track_width": 0.2,
                     "via_diameter": 0.6, "via_drill": 0.3, "wire_width": 6}],
        "meta": {"version": 3}, "net_colors": None,
        "netclass_assignments": None, "netclass_patterns": []
    },
    "pcbnew": {
        "last_paths": {"gencad": "", "idf": "", "netlist": "", "plot": "",
                       "pos_files": "", "specctra_dsn": "", "step": "",
                       "svg": "", "vrml": ""},
        "page_layout_descr_file": ""
    },
    "schematic": {
        "annotate_start_num": 0, "bom_export_filename": "", "bom_fmt_presets": [],
        "bom_fmt_settings": {"field_delimiter": ",", "ref_delimiter": ",",
                             "ref_range_delimiter": "", "string_delimiter": "\""},
        "bom_presets": [], "connection_grid_size": 50.0,
        "drawing": {
            "dashed_lines_dash_length_ratio": 12.0, "dashed_lines_gap_length_ratio": 3.0,
            "default_line_thickness": 6.0, "default_text_size": 50.0, "field_names": [],
            "intersheets_ref_own_page": False, "intersheets_ref_prefix": "",
            "intersheets_ref_short": False, "intersheets_ref_show": False,
            "intersheets_ref_suffix": "", "junction_size_choice": 3,
            "label_size_ratio": 0.375,
            "operating_point_overlay_i_precision": 3, "operating_point_overlay_i_range": "~A",
            "operating_point_overlay_v_precision": 3, "operating_point_overlay_v_range": "~V",
            "overbar_offset_ratio": 1.23, "pin_symbol_size": 25.0, "text_offset_ratio": 0.15
        },
        "legacy_lib_dir": "", "legacy_lib_list": [], "meta": {"version": 1},
        "net_format_name": "", "page_layout_descr_file": "", "plot_directory": "",
        "spice_current_sheet_as_root": False, "spice_external_command": "spice \"%I\"",
        "spice_model_current_sheet_as_root": True, "spice_save_all_currents": False,
        "spice_save_all_dissipations": False, "spice_save_all_voltages": False,
        "subpart_first_id": 65, "subpart_id_separator": 0
    },
    "sheets": [[ROOT_UUID, ""]]
}

with open(pro_path, 'w') as f:
    json.dump(project, f, indent=2)

print(f"Wrote project: {pro_path}")
print("Done! Open milk-depot-coffee-roaster.kicad_pro in KiCad.")
