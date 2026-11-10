"""
Realistic (Fritzing-style) SVG drawings of the robot-car components.

Every component function returns a Part: local SVG markup, its size and a dict
of pin positions in local coordinates. `place()` positions/rotates a Part on the
canvas and converts its pins to global coordinates.

Scale: S px per millimetre (motors are drawn smaller, see motor()).
"""
import math

S = 4.2                 # px per mm
P = 2.54 * S            # 0.1" header pitch in px  (10.67)

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, monospace"


# ----------------------------------------------------------------- helpers --
def r(x, y, w, h, fill, stroke="none", sw=1, rx=0, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def c(x, y, rad, fill, stroke="none", sw=1, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def t(x, y, s, size=7, fill="#fff", anchor="middle", weight="600", rot=0, font=FONT, extra=""):
    tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{tr} {extra}>{s}</text>')


def ln(x1, y1, x2, y2, stroke, sw=1, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


DEFS = """
<defs>
  <linearGradient id="gMetal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f3f4f6"/><stop offset=".45" stop-color="#c7cbd1"/>
    <stop offset=".55" stop-color="#aeb3ba"/><stop offset="1" stop-color="#e5e7eb"/></linearGradient>
  <linearGradient id="gMetalH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#e5e7eb"/><stop offset=".5" stop-color="#9ca3af"/><stop offset="1" stop-color="#e5e7eb"/></linearGradient>
  <linearGradient id="gGold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fde68a"/><stop offset="1" stop-color="#b45309"/></linearGradient>
  <radialGradient id="gLens" cx=".35" cy=".35" r=".7">
    <stop offset="0" stop-color="#93c5fd"/><stop offset=".3" stop-color="#1e3a8a"/><stop offset="1" stop-color="#020617"/></radialGradient>
  <radialGradient id="gTrans" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#4b5563"/><stop offset=".75" stop-color="#1f2937"/><stop offset="1" stop-color="#111827"/></radialGradient>
  <radialGradient id="gLedRed" cx=".35" cy=".3" r=".75">
    <stop offset="0" stop-color="#fecaca"/><stop offset=".35" stop-color="#ef4444"/><stop offset="1" stop-color="#7f1d1d"/></radialGradient>
  <radialGradient id="gLedWhite" cx=".35" cy=".3" r=".75">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#e5e7eb"/><stop offset="1" stop-color="#9ca3af"/></radialGradient>
  <linearGradient id="gCell1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#60a5fa"/><stop offset=".5" stop-color="#1d4ed8"/><stop offset="1" stop-color="#1e3a8a"/></linearGradient>
  <linearGradient id="gCell2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4ade80"/><stop offset=".5" stop-color="#15803d"/><stop offset="1" stop-color="#14532d"/></linearGradient>
  <linearGradient id="gYellow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fde047"/><stop offset="1" stop-color="#ca8a04"/></linearGradient>
  <linearGradient id="gCan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f9fafb"/><stop offset=".5" stop-color="#9ca3af"/><stop offset="1" stop-color="#e5e7eb"/></linearGradient>
  <linearGradient id="gHeat" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#111827"/><stop offset=".5" stop-color="#374151"/><stop offset="1" stop-color="#111827"/></linearGradient>
  <pattern id="pMesh" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="3" fill="#374151"/><circle cx="1.5" cy="1.5" r=".8" fill="#111827"/></pattern>
  <pattern id="pTread" width="12" height="8" patternUnits="userSpaceOnUse">
    <rect width="12" height="8" fill="#1f2937"/><path d="M0 4 L6 0 L12 4 M0 8 L6 4 L12 8" stroke="#374151" stroke-width="2" fill="none"/></pattern>
  <filter id="fShadow" x="-10%" y="-10%" width="130%" height="130%">
    <feDropShadow dx="2" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity=".28"/></filter>
</defs>
"""


class Part:
    def __init__(self, svg, w, h, pins, name=""):
        self.svg, self.w, self.h, self.pins, self.name = svg, w, h, pins, name


class Placed:
    def __init__(self, part, x, y, rot=0, opacity=1.0):
        self.part, self.x, self.y, self.rot, self.opacity = part, x, y, rot, opacity
        self.pins = {k: self._g(*v) for k, v in part.pins.items()}

    def _g(self, px, py):
        a = math.radians(self.rot)
        return (self.x + px * math.cos(a) - py * math.sin(a),
                self.y + px * math.sin(a) + py * math.cos(a))

    def svg(self, opacity=None):
        op = self.opacity if opacity is None else opacity
        return (f'<g transform="translate({self.x:.1f},{self.y:.1f}) rotate({self.rot})" opacity="{op}" '
                f'filter="url(#fShadow)">{self.part.svg}</g>')


def header(x, y, n, vertical=False, pitch=P, female=False):
    """Black header strip with square gold pins. Returns svg and pin centres."""
    out, pts = [], []
    if vertical:
        out.append(r(x - pitch / 2, y - pitch / 2, pitch, pitch * n, "#111" if not female else "#1f1f1f", rx=1))
    else:
        out.append(r(x - pitch / 2, y - pitch / 2, pitch * n, pitch, "#111" if not female else "#1f1f1f", rx=1))
    for i in range(n):
        px, py = (x, y + i * pitch) if vertical else (x + i * pitch, y)
        if female:
            out.append(r(px - 2.2, py - 2.2, 4.4, 4.4, "#000"))
        else:
            out.append(r(px - 2.4, py - 2.4, 4.8, 4.8, "url(#gGold)", "#78350f", .4))
        pts.append((px, py))
    return "".join(out), pts


def screw_terminal(x, y, n, pitch=5.0 * S, vertical=True, color="#1d4ed8"):
    """Blue screw terminal block. Returns svg and the wire-entry points."""
    out, pts = [], []
    w, h = (8 * S, pitch * n) if vertical else (pitch * n, 8 * S)
    out.append(r(x, y, w, h, color, "#1e3a8a", 1, 2))
    for i in range(n):
        if vertical:
            cx, cy = x + w * .55, y + pitch * (i + .5)
        else:
            cx, cy = x + pitch * (i + .5), y + h * .45
        out.append(c(cx, cy, 2.6 * S / 1.6, "url(#gMetal)", "#6b7280", .8))
        out.append(ln(cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, "#4b5563", 1.6))
        pts.append((cx, cy))
    return "".join(out), pts


# ============================================================== ARDUINO UNO ==
def arduino_uno():
    W, H = 68.6 * S, 53.4 * S
    o = []
    o.append(f'<path d="M6,0 H{W-8} L{W},8 V{H-30} L{W-8},{H-22} V{H} H6 Q0,{H} 0,{H-6} V6 Q0,0 6,0 Z" '
             f'fill="#00878f" stroke="#005f66" stroke-width="1.5"/>')
    for hx, hy in [(15, 2.5 * S + 6), (W - 10, 10), (W - 10, H - 40), (15 * S, H - 10)]:
        o.append(c(hx, hy, 6, "#e5e7eb", "#9ca3af"))
    # traces (decorative)
    for i in range(7):
        o.append(f'<path d="M{90+i*14},{60} v{30+i*3} h{40}" stroke="#0a9aa3" stroke-width="2" fill="none" opacity=".6"/>')
    # USB-B + barrel jack
    o.append(r(-24, 38, 64, 48, "url(#gMetal)", "#6b7280", 1, 3))
    o.append(r(-24, 50, 10, 24, "#9ca3af"))
    o.append(t(10, 66, "USB", 8, "#4b5563"))
    o.append(r(-20, 150, 58, 38, "#111827", "#000", 1, 4))
    o.append(c(-6, 169, 7, "#374151"))
    o.append(t(22, 172, "DC", 7, "#9ca3af"))
    # reset button
    o.append(r(30, 8, 22, 22, "url(#gMetal)", "#6b7280", 1, 2))
    o.append(c(41, 19, 6, "#b91c1c"))
    # chip ATmega328P DIP-28
    o.append(r(120, 120, 140, 34, "#1f2937", "#111", 1, 2))
    for i in range(14):
        o.append(r(124 + i * 9.6, 115, 4, 5, "#d1d5db"))
        o.append(r(124 + i * 9.6, 154, 4, 5, "#d1d5db"))
    o.append(t(190, 141, "ATMEGA328P", 9, "#9ca3af", weight="700", font=MONO))
    # crystal + caps + regulator
    o.append(r(80, 160, 26, 10, "url(#gMetal)", "#6b7280", .8, 5))
    o.append(r(58, 100, 18, 26, "#111827", rx=2))
    o.append(c(80, 135, 8, "#111827", "#6b7280"))
    o.append(c(60, 140, 8, "#111827", "#6b7280"))
    # logo
    o.append(f'<g transform="translate(150,82)" fill="none" stroke="#fff" stroke-width="4"><circle cx="-14" cy="0" r="11"/><circle cx="14" cy="0" r="11"/></g>')
    o.append(t(150, 86, "−   +", 10, "#fff", weight="800"))
    o.append(t(212, 92, "UNO", 22, "#fff", weight="800"))
    o.append(t(212, 106, "ARDUINO", 8, "#e0f2f1", weight="700"))
    # status LEDs
    for i, nm in enumerate(["L", "TX", "RX"]):
        o.append(r(108, 34 + i * 12, 7, 5, "#fde68a"))
        o.append(t(122, 39 + i * 12, nm, 6, "#fff", anchor="start"))
    o.append(r(W - 30, 70, 7, 5, "#86efac")); o.append(t(W - 34, 75, "ON", 6, "#fff", anchor="end"))
    # ICSP
    hs, _ = header(W - 14, H / 2 - 12, 3, vertical=True)
    o.append(hs)
    hs, _ = header(W - 24, H / 2 - 12, 3, vertical=True)
    o.append(hs)

    pins = {}
    # top digital headers (female) — from left: SCL SDA AREF GND 13 12 ~11 ~10 ~9 8 | 7 ~6 ~5 4 ~3 2 TX1 RX0
    top1 = ["SCL", "SDA", "AREF", "GND2", "D13", "D12", "D11", "D10", "D9", "D8"]
    lab1 = ["SCL", "SDA", "AREF", "GND", "13", "12", "~11", "~10", "~9", "8"]
    top2 = ["D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0"]
    lab2 = ["7", "~6", "~5", "4", "~3", "2", "TX→1", "RX←0"]
    x0 = 96.5
    hs, pts = header(x0, 9, 10, female=True)
    o.append(hs)
    for n, l, p in zip(top1, lab1, pts):
        pins[n] = p
        o.append(t(p[0] + 2.5, 18, l, 6.2, "#fff", anchor="end", rot=-90))
    x1 = x0 + 10 * P + 0.16 * 25.4 * S - P * 0  # famous odd gap
    x1 = x0 + 10 * P + 4
    hs, pts = header(x1, 9, 8, female=True)
    o.append(hs)
    for n, l, p in zip(top2, lab2, pts):
        pins[n] = p
        o.append(t(p[0] + 2.5, 18, l, 6.2, "#fff", anchor="end", rot=-90))
    o.append(t(x1 + 30, 50, "DIGITAL (PWM ~)", 7, "#fff"))
    # bottom headers: power + analog
    bot1 = ["NC", "IOREF", "RESET", "3V3", "5V", "GND", "GND3", "VIN"]
    labb1 = ["", "IOREF", "RESET", "3.3V", "5V", "GND", "GND", "Vin"]
    xb0 = 122
    hs, pts = header(xb0, H - 9, 8, female=True)
    o.append(hs)
    for n, l, p in zip(bot1, labb1, pts):
        pins[n] = p
        o.append(t(p[0] + 2.5, H - 18, l, 6.2, "#fff", anchor="start", rot=-90))
    xb1 = xb0 + 8 * P + 6
    hs, pts = header(xb1, H - 9, 6, female=True)
    o.append(hs)
    for i, p in enumerate(pts):
        pins[f"A{i}"] = p
        o.append(t(p[0] + 2.5, H - 18, f"A{i}", 6.2, "#fff", anchor="start", rot=-90))
    o.append(t(xb0 + 40, H - 48, "POWER", 7, "#fff"))
    o.append(t(xb1 + 27, H - 48, "ANALOG IN", 7, "#fff"))
    return Part("".join(o), W, H, pins, "Arduino UNO")


# ==================================================================== L298N ==
def l298n():
    W = H = 43 * S
    o = [r(0, 0, W, H, "#b91c1c", "#7f1d1d", 1.5, 6)]
    for hx, hy in [(10, 10), (W - 10, 10), (10, H - 10), (W - 10, H - 10)]:
        o.append(c(hx, hy, 5.5, "#e5e7eb", "#7f1d1d"))
    # heatsink
    hx, hw = W * .27, W * .46
    o.append(r(hx, 0, hw, 68, "url(#gHeat)", "#000", 1, 2))
    for i in range(1, 9):
        o.append(ln(hx + i * hw / 9, 2, hx + i * hw / 9, 66, "#4b5563", 1.4))
    o.append(c(W / 2, 40, 4, "#9ca3af"))
    # chip legs under heatsink
    o.append(r(W / 2 - 34, 68, 68, 12, "#111827"))
    o.append(t(W / 2, 77, "L298N", 7.5, "#d1d5db", weight="700", font=MONO))
    for i in range(15):
        o.append(r(W / 2 - 33 + i * 4.6, 80, 2, 8, "#d1d5db"))
    # regulator + caps
    o.append(r(16, 96, 22, 18, "#111827", rx=2)); o.append(r(20, 114, 3, 6, "#d1d5db")); o.append(r(31, 114, 3, 6, "#d1d5db"))
    o.append(t(27, 108, "78M05", 4.5, "#9ca3af"))
    for cx in (W - 30, W - 56):
        o.append(c(cx, 106, 11, "#1f2937", "#6b7280", 1.5))
        o.append(f'<path d="M{cx-5},{106} h10 M{cx},{101} v10" stroke="#6b7280" stroke-width="1.2"/>')
    o.append(t(W / 2, 128, "Motor Driver", 6.5, "#fecaca"))
    # motor terminals left (OUT1, OUT2) and right (OUT3, OUT4)
    pins = {}
    s1, p1 = screw_terminal(-6, 52, 2)
    o.append(s1)
    pins["OUT1"], pins["OUT2"] = (-6, p1[0][1]), (-6, p1[1][1])
    o.append(t(36, p1[0][1] + 3, "OUT1", 6.5, "#fff", anchor="start")); o.append(t(36, p1[1][1] + 3, "OUT2", 6.5, "#fff", anchor="start"))
    s2, p2 = screw_terminal(W - 8 * S + 6, 52, 2)
    o.append(s2)
    pins["OUT3"], pins["OUT4"] = (W + 6, p2[0][1]), (W + 6, p2[1][1])
    o.append(t(W - 36, p2[0][1] + 3, "OUT3", 6.5, "#fff", anchor="end")); o.append(t(W - 36, p2[1][1] + 3, "OUT4", 6.5, "#fff", anchor="end"))
    # power terminal (3 way) bottom-left
    s3, p3 = screw_terminal(14, H - 8 * S + 6, 3, vertical=False)
    o.append(s3)
    for nm, p in zip(["12V", "GND", "5V"], p3):
        pins[nm] = (p[0], H + 6)
        o.append(t(p[0], H - 8 * S - 2, {"12V": "+12V", "GND": "GND", "5V": "+5V"}[nm], 6.5, "#fff"))
    # 5V-EN jumper (ON)
    o.append(r(86, 150, 10, 16, "#111", rx=1)); o.append(t(91, 147, "5V-EN", 4.5, "#fecaca"))
    # control header: ENA(2 pins) IN1..IN4 ENB(2 pins)
    hx0 = W - 6 * P - 4
    hy = H - 14
    names = ["ENA", "IN1", "IN2", "IN3", "IN4", "ENB"]
    for i, nm in enumerate(names):
        px = hx0 + i * P
        hs, pts = header(px, hy, 1)
        o.append(hs)
        pins[nm] = (px, hy)
        if nm in ("ENA", "ENB"):           # 5V pin above, jumper removed
            hs, _ = header(px, hy - P, 1)
            o.append(hs)
        o.append(t(px + 2.4, hy - P * (1.8 if nm in ("ENA", "ENB") else 1) + 2, nm, 5.6, "#fff", anchor="start", rot=-90))
    return Part("".join(o), W, H, pins, "L298N")


# ================================================================ ESP32-CAM ==
ESP_LEFT = ["IO4", "IO2", "IO14", "IO15", "IO13", "IO12", "GND", "5V"]
ESP_RIGHT = ["GND_R1", "U0T", "U0R", "VCC", "GND_R2", "IO0", "IO16", "3V3"]


def esp32cam():
    W, H = 27 * S, 40.5 * S
    o = [r(0, 0, W, H, "#1c1c1c", "#000", 1.5, 4)]
    # module shield
    o.append(r(10, 66, W - 20, 52, "url(#gMetal)", "#6b7280", 1, 2))
    o.append(t(W / 2, 88, "ESP32-S", 8, "#4b5563", weight="800"))
    o.append(t(W / 2, 99, "AI-Thinker", 5.5, "#6b7280"))
    # SD slot
    o.append(r(16, 120, W - 32, 20, "url(#gMetal)", "#6b7280", .8, 1))
    o.append(t(W / 2, 133, "micro SD", 5, "#4b5563"))
    # camera ribbon + module
    o.append(r(W / 2 - 13, 2, 26, 34, "#b45309", "#78350f", .6, 1))
    o.append(r(W / 2 - 18, 16, 36, 36, "#0b0b0b", "#333", 1, 3))
    o.append(c(W / 2, 34, 13, "#111", "#4b5563", 1.5))
    o.append(c(W / 2, 34, 9, "url(#gLens)"))
    o.append(c(W / 2 - 3, 31, 2, "#fff", extra='opacity=".7"'))
    o.append(t(W / 2, 61, "OV2640", 5.5, "#9ca3af"))
    # flash LED
    o.append(r(W - 26, 144, 13, 13, "#fef9c3", "#a16207", .8, 2))
    o.append(t(W - 19.5, 165, "FLASH", 4.5, "#fde68a"))
    # reset button
    o.append(r(8, 144, 14, 10, "url(#gMetal)", "#6b7280", .6, 2))
    o.append(t(15, 162, "RST", 4.5, "#9ca3af"))
    pins = {}
    y0 = H - 7.5 * P - 6
    hs, pl = header(6, y0, 8, vertical=True)
    o.append(hs)
    hs, pr = header(W - 6, y0, 8, vertical=True)
    o.append(hs)
    for nm, p in zip(ESP_LEFT, pl):
        pins[nm] = p
    for nm, p in zip(ESP_RIGHT, pr):
        pins[nm] = p
    return Part("".join(o), W, H, pins, "ESP32-CAM")


def esp_labels(pl: Placed, used=()):
    """Pin labels drawn OUTSIDE the board (they are printed on the back of the real board)."""
    o = []
    for nm in ESP_LEFT:
        x, y = pl.pins[nm]
        lab = nm
        bold = nm in used
        o.append(t(x - 12, y + 3, lab, 9 if bold else 8, "#111827" if bold else "#6b7280", anchor="end", weight="800" if bold else "500"))
    for nm in ESP_RIGHT:
        x, y = pl.pins[nm]
        lab = nm.split("_")[0]
        bold = nm in used
        o.append(t(x + 12, y + 3, lab, 9 if bold else 8, "#111827" if bold else "#6b7280", anchor="start", weight="800" if bold else "500"))
    return "".join(o)


# ================================================================== HC-SR04 ==
def hcsr04():
    W, H = 45 * S, 20 * S
    o = [r(0, 0, W, H, "#1565c0", "#0d47a1", 1.5, 4)]
    for hx in (8, W - 8):
        for hy in (8, H - 8):
            o.append(c(hx, hy, 4, "#e5e7eb", "#0d47a1"))
    for cx, lab in [(W * .23, "T"), (W * .77, "R")]:
        o.append(c(cx, H / 2 - 4, 34, "url(#gMetal)", "#6b7280", 1.5))
        o.append(c(cx, H / 2 - 4, 26, "url(#pMesh)", "#111", 1.5))
        o.append(t(cx, H / 2 + 38, lab, 7, "#bfdbfe"))
    o.append(r(W / 2 - 14, 6, 28, 12, "url(#gMetal)", "#6b7280", .8, 6))
    o.append(t(W / 2, 36, "HC-SR04", 8, "#fff", weight="800"))
    pins = {}
    x0 = W / 2 - 1.5 * P
    hs, pts = header(x0, H + 5, 4)
    o.append(hs)
    for nm, lab, p in zip(["VCC", "TRIG", "ECHO", "GND"], ["Vcc", "Trig", "Echo", "Gnd"], pts):
        pins[nm] = p
        o.append(t(p[0] + 2, H - 4, lab, 5, "#fff", anchor="start", rot=-90))
    return Part("".join(o), W, H + 10, pins, "HC-SR04")


# ================================================================== LM2596 ==
def lm2596():
    W, H = 43 * S, 21 * S
    o = [r(0, 0, W, H, "#1e40af", "#1e3a8a", 1.5, 3)]
    # pads
    pins = {}
    for nm, (px, py) in {"IN+": (9, 18), "IN-": (9, H - 18), "OUT+": (W - 9, 18), "OUT-": (W - 9, H - 18)}.items():
        o.append(c(px, py, 6.5, "url(#gGold)", "#78350f", 1))
        o.append(c(px, py, 2.5, "#1e293b"))
        pins[nm] = (px, py)
        o.append(t(px, py + (15 if py < H / 2 else -10), nm.replace("-", "−"), 6.5, "#fff"))
    # chip
    o.append(r(36, H / 2 - 16, 30, 32, "#111827", rx=2))
    o.append(t(51, H / 2 + 2, "LM2596", 4.6, "#9ca3af", weight="700"))
    # inductor
    o.append(r(72, H / 2 - 26, 50, 52, "#27272a", "#000", 1, 6))
    o.append(c(97, H / 2, 18, "#b45309", "#78350f", 1))
    o.append(c(97, H / 2, 9, "#27272a"))
    o.append(t(97, H / 2 + 3, "330", 6, "#fbbf24", weight="700"))
    # caps
    for cx, cy in [(132, 20), (132, H - 20)]:
        o.append(c(cx, cy, 9, "#1f2937", "#6b7280", 1.5))
        o.append(f'<path d="M{cx-5},{cy} h10 M{cx},{cy-5} v10" stroke="#6b7280" stroke-width="1.2"/>')
    # trimpot
    o.append(r(146, H / 2 - 9, 18, 18, "#2563eb", "#1e3a8a", 1, 2))
    o.append(c(155, H / 2, 6, "url(#gGold)", "#78350f", .8))
    o.append(ln(151, H / 2 + 4, 159, H / 2 - 4, "#78350f", 1.4))
    o.append(t(155, H / 2 + 17, "ADJ", 5, "#bfdbfe"))
    return Part("".join(o), W, H, pins, "LM2596")


# ============================================================ 18650 HOLDER ==
def battery_holder():
    W, H = 78 * S, 42 * S
    o = [r(0, 0, W, H, "#18181b", "#000", 1.5, 6)]
    for i, (g, lab) in enumerate([("url(#gCell1)", "18650  3.7V  2500mAh"), ("url(#gCell2)", "18650  3.7V  2500mAh")]):
        y = 10 + i * (H / 2 - 4)
        o.append(r(26, y, W - 52, H / 2 - 16, g, "#0f172a", 1, 10))
        o.append(r(W - 30, y + 18, 8, H / 2 - 52, "url(#gMetal)", "#6b7280", .6, 2))
        o.append(t(W / 2, y + (H / 2 - 16) / 2 + 4, lab, 9, "#fff", weight="700"))
        # springs
        o.append(f'<path d="M12,{y+10} l6,6 l-6,6 l6,6 l-6,6 l6,6 l-6,6" stroke="#d1d5db" stroke-width="2" fill="none"/>')
        o.append(r(W - 22, y + 14, 10, 34, "url(#gMetal)", "#6b7280", .6))
        sym = "+" if i == 0 else "−"
    o.append(t(W - 14, 16, "+", 12, "#ef4444", weight="800"))
    o.append(t(W - 14, H - 6, "−", 14, "#e5e7eb", weight="800"))
    pins = {"+": (W, 28), "-": (W, H - 28)}
    return Part("".join(o), W, H, pins, "2×18650 holder")


def switch():
    W, H = 22 * S, 14 * S
    o = [r(0, 0, W, H, "#111827", "#000", 1, 4), r(6, 6, W - 12, H - 12, "#dc2626", "#7f1d1d", 1, 3)]
    o.append(r(W / 2, 8, W / 2 - 8, H - 16, "#ef4444", rx=2))
    o.append(t(W / 2 - 12, H / 2 + 4, "O", 9, "#fff", weight="800"))
    o.append(t(W / 2 + 16, H / 2 + 4, "I", 10, "#fff", weight="800"))
    pins = {"A": (0, H / 2), "B": (W, H / 2)}
    return Part("".join(o), W, H, pins, "Switch")


# ======================================================= TT MOTOR + WHEEL ==
def motor(mirror=False, label=""):
    """Top view: wheel | yellow gearbox | silver motor can | tabs. Tabs on the right."""
    k = 2.3
    o = []
    # wheel
    o.append(r(0, 0, 26 * k, 66 * k, "url(#pTread)", "#000", 1.5, 10))
    o.append(r(26 * k, 66 * k / 2 - 4, 8, 8, "#d1d5db"))
    # gearbox
    gx, gy, gw, gh = 26 * k + 6, 66 * k / 2 - 22 * k / 2, 64 * k, 22 * k
    o.append(r(gx, gy, gw, gh, "url(#gYellow)", "#a16207", 1.5, 4))
    o.append(c(gx + 18, gy + gh / 2, 7, "#fef08a", "#a16207"))
    for hx in (gx + gw * .55, gx + gw * .85):
        o.append(c(hx, gy + 8, 3, "#a16207")); o.append(c(hx, gy + gh - 8, 3, "#a16207"))
    o.append(t(gx + gw * .6, gy + gh / 2 + 4, "TT 1:48", 9, "#713f12", weight="700"))
    # can
    cx = gx + gw
    o.append(f'<path d="M{cx},{gy+5} h{20*k} q8,0 8,8 v{gh-26} q0,8 -8,8 h-{20*k} z" fill="url(#gCan)" stroke="#6b7280" stroke-width="1.2"/>')
    ex = cx + 20 * k + 8
    pa, pb = (ex + 9, gy + 12), (ex + 9, gy + gh - 12)
    for p in (pa, pb):
        o.append(r(ex - 2, p[1] - 3, 12, 6, "#d97706", "#92400e", .6, 1))
    # 100nF cap across tabs
    o.append(ln(ex + 4, pa[1], ex + 14, gy + gh / 2, "#9ca3af", 1.4)); o.append(ln(ex + 4, pb[1], ex + 14, gy + gh / 2, "#9ca3af", 1.4))
    o.append(c(ex + 17, gy + gh / 2, 5, "#ea580c", "#9a3412", .8))
    W, H = ex + 24, 66 * k
    if label:
        o.append(t(gx + gw / 2 - 10, gy - 8, label, 11, "#111827", weight="800"))
    pins = {"A": pa, "B": pb}
    return Part("".join(o), W, H, pins, "TT motor")


# ============================================================== BREADBOARD ==
class Breadboard:
    """Half-size 400-point breadboard. 30 columns, rows a-j, 2 rails top and bottom."""
    COLS = 30

    def __init__(self):
        self.W = (self.COLS + 3) * P
        self.H = 22 * P

    def hole_local(self, col, row):
        x = (col + 0.8) * P
        rows = "abcdefghij"
        if row in rows:
            i = rows.index(row)
            y = (6 + i + (1 if i >= 5 else 0)) * P
        elif row == "T+":
            y = 1.3 * P
        elif row == "T-":
            y = 2.3 * P
        elif row == "B-":
            y = 18.7 * P
        elif row == "B+":
            y = 19.7 * P
        else:
            raise ValueError(row)
        return x, y

    @staticmethod
    def rail_col_ok(col):
        return col % 6 != 1

    def part(self):
        W, H = self.W, self.H
        o = [r(0, 0, W, H, "#f8f8f4", "#d4d4cf", 1.5, 6)]
        o.append(r(0, 3.6 * P, W, .9, "#e5e5e0"))
        o.append(r(0, 17.4 * P, W, .9, "#e5e5e0"))
        o.append(r(.6 * P, 11.15 * P, W - 1.2 * P, .9 * P, "#e7e7e2", rx=2))   # centre channel
        # rail stripes
        o.append(ln(P, .6 * P, W - P, .6 * P, "#dc2626", 1.6)); o.append(ln(P, 3.0 * P, W - P, 3.0 * P, "#2563eb", 1.6))
        o.append(ln(P, 18.0 * P, W - P, 18.0 * P, "#2563eb", 1.6)); o.append(ln(P, 20.4 * P, W - P, 20.4 * P, "#dc2626", 1.6))
        for y, s, col in [(1.3, "+", "#dc2626"), (2.3, "−", "#2563eb"), (18.7, "−", "#2563eb"), (19.7, "+", "#dc2626")]:
            o.append(t(.45 * P, y * P + 3, s, 9, col, weight="800"))
            o.append(t(W - .45 * P, y * P + 3, s, 9, col, weight="800"))
        for col in range(1, self.COLS + 1):
            for row in "abcdefghij":
                x, y = self.hole_local(col, row)
                o.append(r(x - 1.9, y - 1.9, 3.8, 3.8, "#3f3f46", rx=.6))
            if self.rail_col_ok(col):
                for row in ("T+", "T-", "B-", "B+"):
                    x, y = self.hole_local(col, row)
                    o.append(r(x - 1.9, y - 1.9, 3.8, 3.8, "#3f3f46", rx=.6))
            if col == 1 or col % 5 == 0:
                x, _ = self.hole_local(col, "a")
                o.append(t(x, 4.9 * P, str(col), 6, "#71717a", weight="500"))
                o.append(t(x, 17.0 * P, str(col), 6, "#71717a", weight="500"))
        for i, row in enumerate("abcdefghij"):
            _, y = self.hole_local(1, row)
            o.append(t(.35 * P, y + 2.5, row, 6, "#71717a", weight="500"))
            o.append(t(W - .35 * P, y + 2.5, row, 6, "#71717a", weight="500"))
        return Part("".join(o), W, H, {}, "Breadboard")


# ======================================================== small parts =====
BANDS = {"220": ["#dc2626", "#dc2626", "#78350f"], "1k": ["#78350f", "#111", "#dc2626"],
         "2k": ["#dc2626", "#111", "#dc2626"]}


def resistor(p1, p2, value):
    """Resistor between two global points (Fritzing style)."""
    (x1, y1), (x2, y2) = p1, p2
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = math.hypot(x2 - x1, y2 - y1)
    bw = min(L - 8, 6.3 * S)
    o = [ln(x1, y1, x2, y2, "#9ca3af", 2.2, 'stroke-linecap="round"')]
    g = [f'<g transform="translate({(x1+x2)/2:.1f},{(y1+y2)/2:.1f}) rotate({ang:.1f})">',
         r(-bw / 2, -5.5, bw, 11, "#e8d3a9", "#a8875a", .8, 5)]
    for i, col in enumerate(BANDS[value]):
        g.append(r(-bw / 2 + 5 + i * 5, -5.5, 3, 11, col))
    g.append(r(bw / 2 - 8, -5.5, 3, 11, "#d4a017"))
    g.append("</g>")
    o.append("".join(g))
    o.append(c(x1, y1, 2.2, "#71717a")); o.append(c(x2, y2, 2.2, "#71717a"))
    return "".join(o)


def led(anode, cathode, color="red"):
    (x1, y1), (x2, y2) = anode, cathode
    mx, my = (x1 + x2) / 2, min(y1, y2) - 14
    o = [f'<path d="M{x1},{y1} L{x1},{my+6} L{mx-2},{my+4}" stroke="#9ca3af" stroke-width="2" fill="none"/>',
         f'<path d="M{x2},{y2} L{x2},{my+8} L{mx+2},{my+4}" stroke="#9ca3af" stroke-width="2" fill="none"/>',
         c(mx, my, 10.5, "url(#gLedRed)" if color == "red" else "url(#gLedWhite)", "#7f1d1d" if color == "red" else "#6b7280", 1),
         c(mx - 3.5, my - 3.5, 2.5, "#fff", extra='opacity=".7"'),
         t(x1, y1 + 13, "+", 9, "#b91c1c", weight="800")]
    return "".join(o)


def buzzer(plus, minus):
    (x1, y1), (x2, y2) = plus, minus
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    rad = 6 * S
    o = [c(mx, my, rad, "#18181b", "#000", 1.5, 'filter="url(#fShadow)"'), c(mx, my, rad - 5, "#27272a"),
         c(mx, my, 3.5, "#09090b"), t(mx - rad * .55, my - rad * .3, "+", 10, "#fff", weight="800"),
         t(mx, my + rad * .6, "BUZZER", 5.5, "#a1a1aa")]
    return "".join(o)


def capacitor(plus, minus, label="2200µF"):
    (x1, y1), (x2, y2) = plus, minus
    mx, my = (x1 + x2) / 2 + 22, (y1 + y2) / 2
    o = [f'<path d="M{x1},{y1} L{mx-6},{my-3}" stroke="#9ca3af" stroke-width="2" fill="none"/>',
         f'<path d="M{x2},{y2} L{mx-6},{my+3}" stroke="#9ca3af" stroke-width="2" fill="none"/>',
         c(mx + 6, my, 5 * S, "#1e3a8a", "#172554", 1.2, 'filter="url(#fShadow)"'),
         f'<path d="M{mx+6-5*S*0.9},{my+5*S*0.45} A{5*S} {5*S} 0 0 0 {mx+6+5*S*0.9} {my+5*S*0.45}" stroke="#cbd5e1" stroke-width="6" fill="none"/>',
         t(mx + 6, my - 2, label, 6, "#fff"), t(mx + 6, my + 15, "− − −", 6, "#1e3a8a")]
    return "".join(o)


# ==================================================================== wires ==
def wire(pts, color, label=None, width=5.5, opacity=1.0, dash=None):
    """Fritzing-like wire through orthogonal points with rounded corners."""
    if len(pts) < 2:
        return ""
    rad = 10
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        l1 = math.hypot(x1 - x0, y1 - y0) or 1
        l2 = math.hypot(x2 - x1, y2 - y1) or 1
        rr = min(rad, l1 / 2, l2 / 2)
        ax, ay = x1 - (x1 - x0) / l1 * rr, y1 - (y1 - y0) / l1 * rr
        bx, by = x1 + (x2 - x1) / l2 * rr, y1 + (y2 - y1) / l2 * rr
        d += f" L{ax:.1f},{ay:.1f} Q{x1:.1f},{y1:.1f} {bx:.1f},{by:.1f}"
    d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    dk = darker(color)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    o = [f'<g opacity="{opacity}">',
         f'<path d="{d}" fill="none" stroke="{dk}" stroke-width="{width+2.2}" stroke-linecap="round" stroke-linejoin="round"{ds}/>',
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{ds}/>',
         f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="{width*0.3}" stroke-linecap="round" stroke-linejoin="round" transform="translate(-1,-1)"{ds}/>']
    for (x, y) in (pts[0], pts[-1]):
        o.append(c(x, y, width * 0.75, "#d1d5db", dk, 1.2))
    o.append("</g>")
    return "".join(o)


def darker(hexc, f=0.6):
    hexc = hexc.lstrip("#")
    rr, gg, bb = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    return "#%02x%02x%02x" % (int(rr * f), int(gg * f), int(bb * f))


def tag(x, y, text, color, anchor="middle", size=10):
    w = len(text) * size * 0.58 + 12
    x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
    return (r(x0, y - size, w, size + 7, "#fff", color, 1.4, 4) +
            t(x0 + w / 2, y + 1.5, text, size, darker(color, .75), weight="800"))


def callout(x, y, n, color="#0f172a"):
    return c(x, y, 13, color, "#fff", 2.5) + t(x, y + 5, str(n), 13, "#fff", weight="800")
