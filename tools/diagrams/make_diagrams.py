#!/usr/bin/env python3
"""
Generates the realistic wiring diagrams (SVG) for the robot car:

    docs/images/wiring_full.svg          everything
    docs/images/step1_power.svg ...      one image per wiring step
    docs/images/part_*.svg               single components (for the parts list)

Run:  python3 tools/diagrams/make_diagrams.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from components import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "docs", "images")
os.makedirs(OUT, exist_ok=True)

CW, CH = 1790, 1380
OX, OY = 30, 92   # content offset (room for the title)

# ------------------------------------------------------------- colours ----
RED, BLK, ORG = "#e11d48", "#27272a", "#f97316"
COL = dict(ENA="#8b5cf6", IN1="#0ea5e9", IN2="#14b8a6", IN3="#22c55e", IN4="#84cc16", ENB="#d946ef",
           TX="#06b6d4", RX="#ec4899", TRIG="#eab308", ECHO="#10b981", A0="#ef4444", A2="#94a3b8",
           A3="#a855f7", A4="#facc15", M1="#b45309", M2="#1d4ed8")

# ------------------------------------------------------------- placement --
bb = Breadboard()
BBX, BBY = 1230, 880


def H(col, row):
    lx, ly = bb.hole_local(col, row)
    return (BBX + lx, BBY + ly)


def build():
    P_ = {}
    P_["l298n"] = Placed(l298n(), 560, 150)
    m = motor()
    P_["LF"] = Placed(m, 40, 60)
    P_["LR"] = Placed(m, 40, 270)
    mr = motor()
    P_["RF"] = Placed(mr, 1010 + mr.w, 60 + mr.h, 180)
    P_["RR"] = Placed(mr, 1010 + mr.w, 270 + mr.h, 180)
    P_["uno"] = Placed(arduino_uno(), 860, 600)
    P_["hc"] = Placed(hcsr04(), 680, 830, -90)
    P_["esp"] = Placed(esp32cam(), 1600, 160)
    P_["bb"] = Placed(bb.part(), BBX, BBY)
    P_["bat"] = Placed(battery_holder(), 40, 900)
    P_["sw"] = Placed(switch(), 230, 800)
    return P_


def orth(*pts):
    return list(pts)


def connections(P_):
    """Every wire: (step, points, colour, label, label_pos)"""
    L, U, E, HC = P_["l298n"].pins, P_["uno"].pins, P_["esp"].pins, P_["hc"].pins
    W = []

    def add(step, pts, color, label=None, lp=None, anchor="middle"):
        W.append(dict(step=step, pts=pts, color=color, label=label, lp=lp, anchor=anchor))

    # ---- step 1: power ----------------------------------------------------
    bp, bm = P_["bat"].pins["+"], P_["bat"].pins["-"]
    sa, sb = P_["sw"].pins["A"], P_["sw"].pins["B"]
    v12, gnd = L["12V"], L["GND"]
    add(1, [bp, (386, bp[1]), (386, 880), (215, 880), (215, sa[1]), sa], RED)
    add(1, [sb, (400, sb[1]), (400, 380), (v12[0] - 4, 380), (v12[0] - 4, v12[1])], RED, "+7.4 V", (360, sb[1] - 14))
    add(1, [bm, (412, bm[1]), (412, 396), (gnd[0] - 4, 396), (gnd[0] - 4, gnd[1])], BLK, "GND", (440, bm[1] - 12))
    # second wire in each L298N screw terminal: 7.4 V to the UNO VIN, GND to the breadboard - rail
    vin = U["VIN"]
    add(1, [(v12[0] + 4, v12[1]), (v12[0] + 4, 1240), (vin[0], 1240), vin], RED, "+7.4 V → UNO VIN", (840, 1240))
    add(1, [(gnd[0] + 4, gnd[1]), (gnd[0] + 4, 1200), (H(8, "B-")[0], 1200), H(8, "B-")], BLK, "GND → breadboard −", (840, 1200 + 16))

    # ---- step 2: motors --------------------------------------------------
    for mk, (o1, o2) in (("LF", ("OUT1", "OUT2")), ("LR", ("OUT1", "OUT2"))):
        a, b = P_[mk].pins["A"], P_[mk].pins["B"]
        x1, x2 = (440, 420) if mk == "LF" else (510, 490)
        add(2, [a, (x1, a[1]), (x1, L[o1][1]), L[o1]], COL["M1"])
        add(2, [b, (x2, b[1]), (x2, L[o2][1]), L[o2]], COL["M2"])
    for mk, (o3, o4) in (("RF", ("OUT3", "OUT4")), ("RR", ("OUT3", "OUT4"))):
        a, b = P_[mk].pins["A"], P_[mk].pins["B"]          # rotated: A is now the lower tab
        x1, x2 = (870, 850) if mk == "RF" else (930, 910)
        add(2, [b, (x2, b[1]), (x2, L[o3][1]), L[o3]], COL["M1"])
        add(2, [a, (x1, a[1]), (x1, L[o4][1]), L[o4]], COL["M2"])

    # ---- step 3: L298N -> UNO -------------------------------------------
    pairs = [("ENA", "D11"), ("IN1", "D10"), ("IN2", "D9"), ("IN3", "D8"), ("IN4", "D7"), ("ENB", "D6")]
    for i, (ln_, un) in enumerate(pairs):
        a, b = L[ln_], U[un]
        yj = 490 - i * 11
        add(3, [a, (a[0], yj), (b[0], yj), b], COL[ln_], None)

    # ---- step 4: UNO power -----------------------------------------------
    add(4, [U["GND"], (U["GND"][0], 1150), (H(2, "B-")[0], 1150), H(2, "B-")], BLK)
    add(4, [U["5V"], (U["5V"][0], 1160), (H(3, "B+")[0], 1160), H(3, "B+")], ORG)

    # ---- step 5: HC-SR04 --------------------------------------------------
    add(5, [U["D13"], (U["D13"][0], 575), (812, 575), (812, HC["TRIG"][1]), HC["TRIG"]], COL["TRIG"], "D13 → TRIG", (900, 575 - 9))
    add(5, [U["D12"], (U["D12"][0], 562), (800, 562), (800, HC["ECHO"][1]), HC["ECHO"]], COL["ECHO"], "D12 ← ECHO", (900, 562 - 22))
    add(5, [HC["GND"], (826, HC["GND"][1]), (826, 1170), (H(4, "B-")[0], 1170), H(4, "B-")], BLK)
    add(5, [HC["VCC"], (788, HC["VCC"][1]), (788, 1180), (H(5, "B+")[0], 1180), H(5, "B+")], ORG)

    # ---- step 6: buzzer + LEDs -------------------------------------------
    add(6, [U["A0"], (U["A0"][0], 872), (H(4, "f")[0], 872), H(4, "f")], COL["A0"], "A0", (H(4, "f")[0], 866), "middle")
    add(6, [U["A2"], (U["A2"][0], 861), (H(12, "f")[0], 861), H(12, "f")], COL["A2"], "A2", (H(12, "f")[0], 855))
    add(6, [U["A3"], (U["A3"][0], 850), (H(20, "f")[0], 850), H(20, "f")], COL["A3"], "A3", (H(20, "f")[0], 844))
    add(6, [H(23, "j"), H(23, "B-")], BLK)
    # headlights: A4 -> top half of the breadboard, top − rail bridged to the bottom − rail
    add(6, [U["A4"], (U["A4"][0], 839), (H(24, "a")[0], 839), H(24, "a")], COL["A4"], "A4", (H(24, "a")[0] + 22, 833))
    add(6, [H(1, "T-"), H(1, "B-")], BLK)

    # ---- step 7: ESP32-CAM ------------------------------------------------
    add(7, [U["D3"], (U["D3"][0], 545), (1440, 545), (1440, E["IO14"][1]), E["IO14"]], COL["TX"], "IO14 → D3", (1300, 545 - 9))
    add(7, [U["D2"], (U["D2"][0], 588), (1540, 588), (1540, H(25, "f")[1] - 14), (H(25, "f")[0], H(25, "f")[1] - 14), H(25, "f")], COL["RX"], "D2 → divider", (1300, 588 + 18))
    add(7, [E["IO15"], (1556, E["IO15"][1]), (1556, H(29, "f")[1] - 16), (H(29, "f")[0], H(29, "f")[1] - 16), H(29, "f")], COL["RX"], "→ IO15", (1610, 600))
    add(7, [E["GND"], (1574, E["GND"][1]), (1574, 1140), (H(28, "B-")[0], 1140), H(28, "B-")], BLK)
    add(7, [E["5V"], (1594, E["5V"][1]), (1594, 1150), (H(27, "B+")[0], 1150), H(27, "B+")], ORG)
    return W


def bb_parts(step_filter):
    """Components plugged into the breadboard: (step, svg)"""
    items = [
        (6, resistor(H(4, "h"), H(8, "h"), "220")), (6, led(H(8, "j"), H(9, "B-"))),
        (6, resistor(H(12, "h"), H(16, "h"), "220")), (6, led(H(16, "j"), H(17, "B-"), "white")),
        (6, buzzer(H(20, "h"), H(23, "h"))),
        (6, resistor(H(24, "c"), H(27, "c"), "220")), (6, led(H(27, "a"), H(26, "T-"), "white")),
        (6, resistor(H(24, "d"), H(21, "d"), "220")), (6, led(H(21, "a"), H(22, "T-"), "white")),
        (7, resistor(H(25, "h"), H(29, "h"), "1k")), (7, resistor(H(29, "j"), H(26, "B-"), "2k")),
        (7, capacitor(H(30, "B+"), H(30, "B-"))),
    ]
    return [(s, svg) for s, svg in items if step_filter(s)]


PART_STEPS = {  # which steps involve each part
    "bat": {1}, "sw": {1}, "l298n": {1, 2, 3}, "bb": {1, 4, 5, 6, 7},
    "LF": {2}, "LR": {2}, "RF": {2}, "RR": {2}, "uno": {1, 3, 4, 5, 6, 7}, "hc": {5}, "esp": {7},
}

LABELS = {"LF": "LEFT FRONT motor", "LR": "LEFT REAR motor", "RF": "RIGHT FRONT motor", "RR": "RIGHT REAR motor"}


CROPS = {  # content-coordinate crop (x, y, w, h) for the step close-ups
    1: (20, 80, 1420, 1200), 2: (20, 40, 1330, 470), 3: (520, 110, 660, 740),
    4: (840, 560, 800, 690), 5: (620, 515, 740, 730), 6: (980, 790, 700, 470), 7: (1040, 140, 760, 1135),
}


def render(step=None, title=None, subtitle=None, fname="wiring_full.svg", crop=False):
    P_ = build()
    W = connections(P_)
    if crop and step in CROPS:
        cx, cy, cw, ch = CROPS[step]
        vb = f"{cx+OX} {cy+OY} {cw} {ch}"
        size = f'width="{cw}" height="{ch}"'
        title = None
    else:
        vb, size = f"0 0 {CW} {CH}", f'width="{CW}" height="{CH}"'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" {size}>', DEFS,
         f'<rect width="{CW}" height="{CH}" fill="#ffffff"/>',
         # subtle grid
         '<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#f1f5f9" stroke-width="1"/></pattern></defs>',
         f'<rect width="{CW}" height="{CH}" fill="url(#grid)"/>']
    if title:
        o.append(t(30, 44, title, 28, "#0f172a", anchor="start", weight="800"))
        if subtitle:
            o.append(t(30, 72, subtitle, 15, "#475569", anchor="start", weight="500"))
    o.append(f'<g transform="translate({OX},{OY})">')

    def active(k):
        return step is None or step in PART_STEPS[k]

    order = ["bb", "bat", "sw", "LF", "LR", "RF", "RR", "l298n", "uno", "hc", "esp"]
    for k in order:
        o.append(P_[k].svg(1.0 if active(k) else 0.22))
    # labels for parts
    lab = lambda k, x, y, s, anc="middle": o.append(t(x, y, s, 13, "#0f172a" if active(k) else "#cbd5e1", anchor=anc, weight="800"))
    for k in ("LF", "LR"):
        pl = P_[k]; lab(k, pl.x + 175, pl.y - 6, LABELS[k])
    for k in ("RF", "RR"):
        pl = P_[k]; lab(k, pl.x - pl.part.w + 120, pl.y - pl.part.h - 6, LABELS[k])
    lab("l298n", 650, 140, "L298N motor driver")
    lab("uno", 1004, 590 - 52, "") if False else None
    lab("uno", 930, 850, "Arduino UNO")
    lab("hc", 727, 618, "HC-SR04 (REAR)")
    lab("esp", 1656, 150, "ESP32-CAM (FRONT)")
    lab("bb", BBX - 12, BBY + 20, "Breadboard", "end")
    o.append(t(BBX - 12, BBY + 38, "+ rail = 5 V bus", 11, "#dc2626" if active("bb") else "#e2e8f0", anchor="end", weight="700"))
    o.append(t(BBX - 12, BBY + 54, "− rail = GND bus", 11, "#2563eb" if active("bb") else "#e2e8f0", anchor="end", weight="700"))
    lab("bat", 200, 892, "2 × 18650 battery (7.4 V)")
    lab("sw", 276, 792, "ON/OFF switch")
    o.append(esp_labels(P_["esp"], ("IO14", "IO15", "5V", "GND") if active("esp") else ()))

    # breadboard parts
    for s, svg in bb_parts(lambda s: step is None or s <= step):
        o.append(f'<g opacity="{1 if (step is None or s == step) else 0.35}">{svg}</g>')
    # wires
    for w in W:
        if step is not None and w["step"] > step:
            continue
        op = 1.0 if (step is None or w["step"] == step) else 0.18
        o.append(wire(w["pts"], w["color"], opacity=op))
    for w in W:
        if w["label"] and (step is None or w["step"] == step):
            o.append(tag(w["lp"][0], w["lp"][1], w["label"], w["color"], w["anchor"]))
    # pin-pair tags for the L298N bundle
    if step in (None, 3):
        pairs = [("ENA", "D11"), ("IN1", "D10"), ("IN2", "D9"), ("IN3", "D8"), ("IN4", "D7"), ("ENB", "D6")]
        for i, (a, b) in enumerate(pairs):
            o.append(tag(800 + (i % 3) * 82, 395 + (i // 3) * 22 if False else 0, "", COL[a]) if False else "")
        gx, gy = (60, 452) if step is None else (548, 690)
        o.append(r(gx, gy, 180, 124, "#ffffff", "#cbd5e1", 1.2, 10))
        o.append(t(gx + 90, gy + 22, "L298N  →  Arduino UNO", 12, "#0f172a", weight="800"))
        for i, (a, b) in enumerate(pairs):
            y = gy + 42 + i * 14
            o.append(r(gx + 14, y - 7, 24, 7, COL[a], rx=3))
            o.append(t(gx + 48, y, f"{a}", 11, "#0f172a", anchor="start", weight="700"))
            o.append(t(gx + 100, y, "→", 11, "#64748b"))
            o.append(t(gx + 120, y, b, 11, "#0f172a", anchor="start", weight="800"))
    # step-specific notes
    notes = {
        None: [],
        1: [(650, 112 - 8, "Remove the ENA + ENB jumpers · keep the 5V-EN jumper ON", "#b91c1c")],
        6: [(1330, 1208, "Headlights: 2 white LEDs on A4, one 220 Ω each — mount them at the FRONT", "#a16207"),
            (1180, 1240, "Black jumper: top − rail ↔ bottom − rail (col 1)", "#334155")],
        7: [(1440, 1250, "Divider: D2 → 1 kΩ → IO15, and 2 kΩ from IO15 to GND (5 V → 3.3 V)", "#be185d")],
    }
    for x, y, s, col in notes.get(step, []):
        o.append(tag(x, y, s, col, size=12))
    o.append("</g></svg>")
    with open(os.path.join(OUT, fname), "w") as f:
        f.write("".join(o))
    return fname


STEPS = [
    (1, "step1_power.svg", "Step 1 — Power", "Battery → switch → L298N +12V · second wires: +12V → UNO VIN, GND → breadboard − rail"),
    (2, "step2_motors.svg", "Step 2 — Motors", "Left pair on OUT1/OUT2, right pair on OUT3/OUT4 (same-side motors in parallel)"),
    (3, "step3_control.svg", "Step 3 — L298N → Arduino", "Six control wires, side by side"),
    (4, "step4_uno_power.svg", "Step 4 — 5 V rail from the Arduino", "UNO 5V and GND to the breadboard rails: the UNO makes the 5 V for everything"),
    (5, "step5_sensor.svg", "Step 5 — Rear ultrasonic sensor", "TRIG → D13, ECHO → D12, VCC and GND to the rails"),
    (6, "step6_alarm.svg", "Step 6 — Lights + buzzer", "A0 red rear LED · A2 white reverse LED · A3 buzzer · A4 two white headlights (220 Ω per LED)"),
    (7, "step7_esp32cam.svg", "Step 7 — ESP32-CAM", "IO14 → D3 · D2 → divider → IO15 · 5V/GND + 2200 µF capacitor"),
]


def part_images():
    items = {
        "uno": arduino_uno(), "l298n": l298n(), "esp32cam": esp32cam(), "hcsr04": hcsr04(),
        "battery": battery_holder(), "switch": switch(), "motor": motor(),
        "breadboard": bb.part(),
    }
    for k, p in items.items():
        pad = 34
        w, h = p.w + 2 * pad, p.h + 2 * pad
        ox, oy = pad + (24 if k == "uno" else 0), pad
        w += 24 if k == "uno" else 0
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">'
               f'{DEFS}{Placed(p, ox, oy).svg()}</svg>')
        open(os.path.join(OUT, f"part_{k}.svg"), "w").write(svg)
    # small parts
    smalls = {
        "resistors": "".join([resistor((20, 30), (110, 30), "220"), resistor((20, 70), (110, 70), "1k"), resistor((20, 110), (110, 110), "2k"),
                              t(122, 34, "220 Ω", 12, "#0f172a", anchor="start"), t(122, 74, "1 kΩ", 12, "#0f172a", anchor="start"),
                              t(122, 114, "2 kΩ", 12, "#0f172a", anchor="start")]),
        "leds": led((40, 110), (60, 110)) + led((110, 110), (130, 110), "white"),
        "buzzer": buzzer((50, 70), (90, 70)),
        "capacitor": capacitor((30, 50), (30, 90)),
    }
    for k, s in smalls.items():
        open(os.path.join(OUT, f"part_{k}.svg"), "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 140" width="180" height="140">{DEFS}{s}</svg>')


if __name__ == "__main__":
    render(None, "Robot Car — Complete Wiring", "Arduino UNO · L298N · ESP32-CAM · HC-SR04 · 2×18650 — realistic view (sizes approximate)")
    for st, fn, ti, sub in STEPS:
        render(st, ti, sub, fn)
        render(st, ti, sub, fn.replace(".svg", "_zoom.svg"), crop=True)
    part_images()
    print("diagrams written to", OUT)


# ------------------------------------------------------------ chassis layout --
def chassis_layout():
    """Top view of where every part sits on the chassis (front = top)."""
    Wc, Hc = 980, 1220
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wc} {Hc}" width="{Wc}" height="{Hc}">', DEFS,
         f'<rect width="{Wc}" height="{Hc}" fill="#fff"/>']
    # acrylic plate
    o.append(f'<path d="M260,90 H720 Q760,90 760,130 V1110 Q760,1150 720,1150 H260 Q220,1150 220,1110 V130 Q220,90 260,90 Z" '
             f'fill="#e0f2fe" fill-opacity=".55" stroke="#7dd3fc" stroke-width="3"/>')
    for x, y in [(300, 300), (680, 300), (300, 940), (680, 940), (490, 620)]:
        o.append(c(x, y, 9, "#fff", "#7dd3fc", 2))
    o.append(t(490, 60, "▲  FRONT  (driving direction)", 20, "#0f172a", weight="800"))
    o.append(t(490, 1195, "▼  REAR", 20, "#0f172a", weight="800"))
    k = 0.62
    m = motor()

    def put(part, x, y, rot=0, sc=k, op=1):
        return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})" opacity="{op}" filter="url(#fShadow)">{part.svg}</g>')

    # motors at the corners (wheel outside)
    o.append(put(m, 130, 170)); o.append(put(m, 130, 880))
    o.append(put(m, 850, 170 + m.h * k, 180)); o.append(put(m, 850, 880 + m.h * k, 180))
    # ESP32-CAM front centre
    e = esp32cam(); o.append(put(e, 490 - e.w * .45, 105, 0, .9))
    # L298N centre
    L = l298n(); o.append(put(L, 490 - L.w * .4, 300, 0, .8))
    # UNO
    u = arduino_uno(); o.append(put(u, 490 - u.w * .32, 470, 0, .64))
    # breadboard
    b = bb.part(); o.append(put(b, 490 - b.w * .3, 640, 0, .6))
    # 2200 uF capacitor next to the ESP32-CAM, battery + switch
    o.append(f'<g transform="translate(330,175)">{capacitor((0, 0), (0, 40), "2200µF")}</g>')
    bt = battery_holder(); o.append(put(bt, 490 - bt.w * .3, 900, 0, .6))
    sw = switch(); o.append(put(sw, 640, 810, 0, .8))
    # HC-SR04 at rear edge, transducers facing back
    hc = hcsr04(); o.append(put(hc, 490 + hc.w * .4, 1140, 180, .8))
    # LEDs + buzzer at the rear corners
    o.append(c(290, 1120, 11, "url(#gLedRed)", "#7f1d1d")); o.append(c(690, 1120, 11, "url(#gLedWhite)", "#6b7280"))
    # headlights at the front corners
    for hx in (262, 718):
        o.append(f'<path d="M{hx-14},96 L{hx-34},40 L{hx+34},40 L{hx+14},96 Z" fill="#fde68a" opacity=".55"/>')
        o.append(c(hx, 104, 12, "url(#gLedWhite)", "#6b7280"))
    o.append(c(250, 1050, 18, "#18181b", "#000"))

    # callouts
    notes = [
        (1, 490, 120, 905, 140, "ESP32-CAM: front edge, lens forward, tilted up 5–10°"),
        (2, 560, 360, 905, 330, "L298N on the bottom plate, centre"),
        (3, 540, 540, 905, 520, "Arduino UNO (top plate)"),
        (4, 560, 690, 905, 680, "Breadboard: 5 V / GND rails, resistors"),
        (5, 330, 195, 75, 230, "2200 µF capacitor at the ESP32-CAM 5V"),
        (6, 680, 830, 905, 820, "ON/OFF switch at the side"),
        (7, 490, 960, 905, 960, "2×18650 battery: low, at the rear"),
        (8, 490, 1110, 905, 1100, "HC-SR04 on the rear edge, 8–12 cm high"),
        (9, 250, 1050, 75, 1060, "Buzzer"),
        (10, 290, 1120, 75, 1130, "Rear: red LED (A0) left, white reverse LED (A2) right"),
        (11, 262, 104, 75, 60, "2 white HEADLIGHTS (A4) at the front corners"),
    ]
    for n, x, y, lx, ly, s_ in notes:
        o.append(f'<path d="M{x},{y} L{lx + (-18 if lx > 490 else 18)},{ly}" stroke="#0f172a" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>')
        o.append(callout(lx, ly, n, "#f97316"))
    o.append("</svg>")
    open(os.path.join(OUT, "chassis_layout.svg"), "w").write("".join(o))
    return notes


if __name__ == "__main__":
    chassis_layout()
