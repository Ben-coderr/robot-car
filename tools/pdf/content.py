"""Content of every handbook module. Each function returns a dict used by build_pdfs.py."""
from design import *

# wire colours used in the realistic diagrams
RED, BLK, ORG = "#e11d48", "#27272a", "#f97316"
C = dict(ENA="#8b5cf6", IN1="#0ea5e9", IN2="#14b8a6", IN3="#22c55e", IN4="#84cc16", ENB="#d946ef",
         TX="#06b6d4", RX="#ec4899", TRIG="#eab308", ECHO="#10b981", A0="#ef4444", A2="#94a3b8", A3="#a855f7", A4="#facc15",
         M1="#b45309", M2="#1d4ed8")


def collage(names):
    return '<div class="collage">' + "".join(f'<div><img src="{img("part_" + n + ".svg")}"></div>' for n in names) + "</div>"


def hero(name, pad=True):
    return f'<img src="{img(name)}">'


BLOCK_DIAGRAM = """
<svg viewBox="0 0 720 300" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, sans-serif">
 <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#475569"/></marker></defs>
 <g font-size="12">
  <rect x="10" y="95" width="130" height="110" rx="14" fill="#0b1f3a"/>
  <text x="75" y="128" fill="#fff" text-anchor="middle" font-weight="800" font-size="15">PHONE + PC</text>
  <text x="75" y="150" fill="#cbd5e1" text-anchor="middle">phone: drive app</text>
  <text x="75" y="168" fill="#cbd5e1" text-anchor="middle">PC: class viewer</text>
  <text x="75" y="186" fill="#cbd5e1" text-anchor="middle">radar · alarm</text>
  <rect x="215" y="95" width="150" height="110" rx="14" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
  <text x="290" y="128" fill="#14532d" text-anchor="middle" font-weight="800" font-size="15">ESP32-CAM</text>
  <text x="290" y="150" fill="#166534" text-anchor="middle">camera · WiFi</text>
  <text x="290" y="168" fill="#166534" text-anchor="middle">web server</text>
  <text x="290" y="186" fill="#166534" text-anchor="middle">2 web pages</text>
  <rect x="440" y="95" width="140" height="110" rx="14" fill="#ccfbf1" stroke="#0f766e" stroke-width="2"/>
  <text x="510" y="128" fill="#134e4a" text-anchor="middle" font-weight="800" font-size="15">ARDUINO UNO</text>
  <text x="510" y="150" fill="#115e59" text-anchor="middle">motor control</text>
  <text x="510" y="168" fill="#115e59" text-anchor="middle">sensor · alarm</text>
  <text x="510" y="186" fill="#115e59" text-anchor="middle">lights · auto-brake</text>
  <line x1="140" y1="135" x2="212" y2="135" stroke="#475569" stroke-width="2.5" marker-end="url(#ar)"/>
  <line x1="215" y1="165" x2="143" y2="165" stroke="#475569" stroke-width="2.5" marker-end="url(#ar)"/>
  <text x="177" y="125" text-anchor="middle" fill="#0f172a" font-weight="700" font-size="11">WiFi</text>
  <text x="177" y="185" text-anchor="middle" fill="#64748b" font-size="10">video + data</text>
  <line x1="365" y1="135" x2="437" y2="135" stroke="#475569" stroke-width="2.5" marker-end="url(#ar)"/>
  <line x1="440" y1="165" x2="368" y2="165" stroke="#475569" stroke-width="2.5" marker-end="url(#ar)"/>
  <text x="402" y="125" text-anchor="middle" fill="#0f172a" font-weight="700" font-size="11">UART</text>
  <text x="402" y="185" text-anchor="middle" fill="#64748b" font-size="10">commands / distance</text>
  <g font-size="11.5">
   <rect x="630" y="20" width="84" height="56" rx="10" fill="#fee2e2" stroke="#b91c1c" stroke-width="1.6"/>
   <text x="672" y="44" text-anchor="middle" font-weight="800" fill="#991b1b">L298N</text><text x="672" y="62" text-anchor="middle" fill="#7f1d1d">4 motors</text>
   <rect x="630" y="92" width="84" height="56" rx="10" fill="#e0f2fe" stroke="#0369a1" stroke-width="1.6"/>
   <text x="672" y="116" text-anchor="middle" font-weight="800" fill="#075985">HC-SR04</text><text x="672" y="134" text-anchor="middle" fill="#0c4a6e">rear sensor</text>
   <rect x="630" y="164" width="84" height="56" rx="10" fill="#f3e8ff" stroke="#7e22ce" stroke-width="1.6"/>
   <text x="672" y="188" text-anchor="middle" font-weight="800" fill="#6b21a8">LIGHTS</text><text x="672" y="206" text-anchor="middle" fill="#581c87">+ buzzer</text>
   <rect x="630" y="236" width="84" height="56" rx="10" fill="#fef3c7" stroke="#b45309" stroke-width="1.6"/>
   <text x="672" y="260" text-anchor="middle" font-weight="800" fill="#92400e">SERVO</text><text x="672" y="278" text-anchor="middle" fill="#78350f">optional</text>
  </g>
  <path d="M580,130 C605,130 600,48 627,48" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>
  <path d="M580,145 C605,145 605,120 627,120" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>
  <path d="M580,160 C605,160 605,192 627,192" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#ar)"/>
  <path d="M580,175 C605,175 600,264 627,264" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#ar)"/>
  <rect x="215" y="235" width="365" height="52" rx="12" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="397" y="257" text-anchor="middle" font-weight="800" fill="#0f172a">POWER: 2×18650 (7.4 V) → switch</text>
  <text x="397" y="276" text-anchor="middle" fill="#475569">7.4 V → L298N (motors) + UNO VIN · UNO 5V pin → ESP32-CAM, sensor, lights</text>
 </g>
</svg>"""

DIVIDER_SVG = """
<svg viewBox="0 0 330 150" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, sans-serif" font-size="12">
 <text x="10" y="40" font-weight="800" fill="#0f766e">UNO D2</text><text x="10" y="56" fill="#64748b" font-size="10">5 V signal</text>
 <line x1="70" y1="35" x2="110" y2="35" stroke="#ec4899" stroke-width="3"/>
 <path d="M110,35 l6,-8 l8,16 l8,-16 l8,16 l8,-16 l8,16 l6,-8" fill="none" stroke="#ec4899" stroke-width="3"/>
 <text x="137" y="20" text-anchor="middle" font-weight="800">R1 = 1 kΩ</text>
 <line x1="162" y1="35" x2="230" y2="35" stroke="#ec4899" stroke-width="3"/>
 <circle cx="195" cy="35" r="5" fill="#ec4899"/>
 <text x="238" y="40" font-weight="800" fill="#5b21b6">ESP IO15</text><text x="238" y="56" fill="#64748b" font-size="10">≈ 3.3 V ✓</text>
 <line x1="195" y1="35" x2="195" y2="62" stroke="#ec4899" stroke-width="3"/>
 <path d="M195,62 l-8,6 l16,8 l-16,8 l16,8 l-16,8 l16,8 l-8,6" fill="none" stroke="#ec4899" stroke-width="3"/>
 <text x="215" y="96" font-weight="800">R2 = 2 kΩ</text>
 <line x1="195" y1="114" x2="195" y2="124" stroke="#27272a" stroke-width="3"/>
 <line x1="183" y1="124" x2="207" y2="124" stroke="#27272a" stroke-width="3"/><line x1="188" y1="130" x2="202" y2="130" stroke="#27272a" stroke-width="3"/><line x1="192" y1="136" x2="198" y2="136" stroke="#27272a" stroke-width="3"/>
 <text x="215" y="134" fill="#27272a" font-weight="700">GND</text>
</svg>"""

SENSOR_SIDE_SVG = """
<svg viewBox="0 0 600 210" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Avenir Next, Helvetica, sans-serif" font-size="12">
 <rect x="0" y="180" width="600" height="30" fill="#e2e8f0"/><text x="590" y="200" text-anchor="end" fill="#64748b">floor</text>
 <rect x="330" y="105" width="240" height="40" rx="8" fill="#cbd5e1" stroke="#64748b"/>
 <circle cx="370" cy="160" r="22" fill="#1f2937"/><circle cx="530" cy="160" r="22" fill="#1f2937"/>
 <text x="450" y="130" text-anchor="middle" fill="#334155" font-weight="700">car (side view) → front</text>
 <rect x="318" y="82" width="14" height="30" rx="3" fill="#1565c0"/>
 <path d="M318,97 L40,60 L40,120 Z" fill="#0ea5e9" fill-opacity=".14" stroke="#0ea5e9" stroke-dasharray="5 4"/>
 <line x1="318" y1="97" x2="40" y2="90" stroke="#0ea5e9" stroke-width="2"/>
 <text x="150" y="52" fill="#075985" font-weight="800">ultrasound beam ≈ 30°</text>
 <text x="40" y="160" fill="#075985">tilt slightly UP (≈ 5°) so it never "sees" the floor</text>
 <line x1="300" y1="97" x2="300" y2="180" stroke="#f97316" stroke-width="2" marker-start="url(#a1)" marker-end="url(#a1)"/>
 <defs><marker id="a1" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><circle cx="4" cy="4" r="3" fill="#f97316"/></marker></defs>
 <text x="292" y="135" text-anchor="end" fill="#c2410c" font-weight="800">8–12 cm</text>
 <text x="325" y="74" text-anchor="middle" fill="#1565c0" font-weight="800" font-size="11">HC-SR04</text>
</svg>"""


# =========================================================================== 01
def m01():
    parts = [
        ("chassis", "part_motor.svg", "4WD chassis kit", "2 acrylic plates, 4 × TT gear motors (3–6 V, 1:48), 4 wheels 65 mm, spacers, screws", "1 kit", "$12–18"),
        ("uno", "part_uno.svg", "Arduino UNO R3 (or Nano)", "ATmega328P, USB cable. CH340 clones are fine", "1", "$5–12"),
        ("esp", "part_esp32cam.svg", "ESP32-CAM (AI-Thinker)", "OV2640 camera, 4 MB PSRAM. Get the ESP32-CAM-MB USB board too", "1 + MB", "$9–13"),
        ("l298n", "part_l298n.svg", "L298N motor driver", "Dual H-bridge with heatsink, 5 V regulator, ENA/ENB jumpers", "1", "$2–4"),
        ("hc", "part_hcsr04.svg", "HC-SR04 ultrasonic", "5 V, 2–400 cm. Mounted at the rear of the car", "1", "$1–2"),
        ("bat", "part_battery.svg", "2 × 18650 + holder", "Protected Li-ion 3.7 V, real 2000–3000 mAh, series holder = 7.4 V", "2 + 1", "$8–14"),
        ("bb", "part_breadboard.svg", "Half breadboard", "400 points with + / − rails on both sides", "1", "$1–2"),
        ("sw", "part_switch.svg", "Rocker switch", "≥ 3 A, often included in the kit", "1", "$0.3"),
        ("buz", "part_buzzer.svg", "Active buzzer 5 V", "ACTIVE type: it beeps on plain 5 V (test it on a battery)", "1", "$0.5"),
        ("led", "part_leds.svg", "LEDs 5 mm", "1 red (rear warning) + 3 white (reverse light + 2 headlights). Buy a few spares", "4", "$0.4"),
        ("res", "part_resistors.svg", "Resistors", "220 Ω × 4 · 1 kΩ × 1 · 2 kΩ × 1 (or 2 × 1 kΩ)", "6", "$0.5"),
    ]
    cards = "".join(
        f'<div class="card part"><div class="ph"><img src="{img(f)}"></div><div class="nm">{n}</div>'
        f'<div class="sp">{s}</div><div class="meta"><span class="qty">Qty {q}</span><span class="pr">{p}</span></div></div>'
        for _, f, n, s, q, p in parts)
    feats = [("📱", "Phone control", "Joystick in the phone browser. No app to install."),
             ("🎥", "Live video", "The camera at the front streams to the phone."),
             ("🔊", "Parking alarm", "Buzzer and LED beep faster as an obstacle gets closer."),
             ("🛑", "Auto-brake", "The car refuses to reverse into an obstacle."),
             ("📡", "Radar display", "Rear distance shown as a radar on the phone."),
             ("💡", "Headlights", "Two white front lights: OFF, ON or HAZARD from the app."),
             ("🖥️", "Classroom viewer", "A second page for a PC or projector: video, radar, chart, status."),
             ("📸", "Photos &amp; video", "Save photos on the phone, record video on the PC."),
             ("🛡️", "Fail-safe", "Stops by itself if WiFi or the phone is lost.")]
    fhtml = '<div class="grid3">' + "".join(
        f'<div class="card feat"><div class="fi">{i}</div><div><div class="ft">{t}</div><div class="fd">{d}</div></div></div>'
        for i, t, d in feats) + "</div>"
    body = f"""
{sec(1, "Module 01", "Project overview")}
<p>In this project you build a <b>four-wheel-drive robot car that you drive from a smartphone</b>. A camera at the front sends
live video to the phone. A sensor at the back measures the distance to obstacles. When you reverse, the car warns you like a real car's
<b>parking sensor</b>: a buzzer beeps and a red light flashes, faster and faster as you get closer, and the car brakes by itself before it hits anything.
The phone shows the measurement as a <b>radar</b>.</p>
{objectives(["Explain the job of every part in the car and how they talk to each other",
             "Choose correct parts (voltage, current, type) and avoid common bad buys",
             "Read a power budget and explain why the car uses two power rails (7.4 V and 5 V)",
             "Check your kit against the parts list before you start building"], 45)}
<h2>What the finished car can do</h2>
{fhtml}
<h2>How it works</h2>
<figure class="card" style="padding:6pt 30pt">{BLOCK_DIAGRAM}</figure>
<div class="grid2">
{co("tip", "Why two small computers?", "<p>The <b>ESP32-CAM</b> is great at WiFi and video, but it has only about 4 free pins and is busy streaming. "
    "The <b>Arduino UNO</b> handles the motors, the sensor and the alarm in real time. If WiFi lags, the parking alarm and auto-brake still react instantly.</p>")}
{co("note", "Two power rails", "<p><b>7.4 V</b> from the batteries goes to the motor driver and to the UNO's <b>VIN</b> pin. The UNO's own regulator makes the <b>5 V</b> for "
    "all the electronics. A big <b>2200 µF capacitor</b> at the ESP32-CAM covers the short dips when the motors start, so the camera does not reboot.</p>")}
</div>

{sec(2, "Module 01", "Parts list")}
<p>Everything below is needed for the standard build. Prices are approximate (online shops, 2026) and only for planning.</p>
<div class="grid4">{cards}</div>
<h2>Small parts</h2>
{table(["Part", "Specification", "Qty", "Used for"], [
    ["Electrolytic capacitor", "<b>2200 µF 16 V</b> (any value 1000–2200 µF, 10 V or more)", "1", "Stops the ESP32-CAM rebooting when motors start"],
    ["Ceramic capacitor", "100 nF (marked “104”)", "4", "Soldered across each motor: less electrical noise"],
    ["Jumper wires", "Dupont 20 cm: M-M, M-F, F-F (20 of each)", "1 set", "Signal connections"],
    ["Power wire", "22 AWG (0.5 mm²) red + black, ~1 m each", "—", "Battery → switch → L298N, L298N → UNO VIN"],
    ["ESP32-CAM-MB", "Micro-USB programmer board for the ESP32-CAM", "1", "Uploading code (or use an FTDI adapter)"],
    ["18650 charger", "2-slot Li-ion charger (or 2 × TP4056)", "1", "Charging the batteries safely"],
], ["24%", "38%", "8%", "30%"])}
{co("warn", "Avoid these bad buys", bullets([
    "<b>“9900 mAh” 18650 cells</b>: they are fakes that sag under load and make the ESP32 reboot. Buy known brands (Samsung, LG, Sony/Murata, Molicel).",
    "<b>Passive buzzer</b>: it only clicks on DC. You need an <b>active</b> buzzer, which beeps when connected straight to 5 V.",
    "<b>ESP32-CAM without PSRAM</b>: the video then works only at a small size. Look for “4 MB PSRAM”.",
    "<b>9 V PP3 battery or 4 × AA</b>: far too weak for 4 motors."]))}
<div class="keep"><h2>Checklist: check your kit</h2>
<div class="grid2"><ul class="check">
<li>4 TT motors + 4 wheels + chassis plates</li><li>Arduino UNO + USB cable</li><li>ESP32-CAM + camera + MB board</li>
<li>L298N motor driver</li><li>HC-SR04 sensor</li><li>Active buzzer</li></ul>
<ul class="check"><li>2 × 18650 cells (charged) + holder</li><li>Switch, breadboard, jumper wires</li><li>LEDs: 1 red + 3 white</li>
<li>Resistors 220 Ω ×4, 1 kΩ, 2 kΩ</li><li>Capacitors 2200 µF + 4 × 100 nF</li><li>Multimeter + soldering iron</li></ul></div>
<div class="sig"><div>Checked by (student)</div><div>Approved by (teacher)</div></div></div>

<div class="pb"></div>
{sec(3, "Module 01", "Tools &amp; power budget")}
<h2>Tools</h2>
{table(["Tool", "Needed for", ""], [
    ["<b>Multimeter</b>", "Checking the battery polarity and the 5 V rail", '<span class="badge req">REQUIRED</span>'],
    ["Soldering iron + solder", "Motor wires and capacitors", '<span class="badge req">REQUIRED</span>'],
    ["Small screwdrivers", "L298N screw terminals", '<span class="badge req">REQUIRED</span>'],
    ["Wire stripper / cutter", "Preparing power wires", '<span class="badge req">REQUIRED</span>'],
    ["Computer + Arduino IDE 2", "Programming both boards", '<span class="badge req">REQUIRED</span>'],
    ["FTDI USB-serial adapter", "Only if you have no ESP32-CAM-MB board", '<span class="badge opt">OPTIONAL</span>'],
    ["Hot glue, zip ties, M3 nylon standoffs", "Neat, vibration-proof mounting", '<span class="badge opt">OPTIONAL</span>'],
], ["32%", "50%", "18%"])}
<h2>Power budget: why these parts?</h2>
{table(["Load", "Rail", "Typical", "Peak"], [
    ["4 × TT motors", "7.4 V via L298N", "0.6–1.0 A", "2.5 A (start / stall)"],
    ["ESP32-CAM (WiFi + video)", "5 V", "180 mA", "<b>350 mA spikes</b>"],
    ["Arduino UNO itself", "5 V", "50 mA", "60 mA"],
    ["HC-SR04 + buzzer", "5 V", "30 mA", "45 mA"],
    ["4 LEDs (rear, reverse, 2 headlights)", "5 V", "0–60 mA", "60 mA"],
    ["<b>Total from the UNO 5V pin</b>", "", "<b>≈ 0.3 A</b>", "<b>≈ 0.5 A</b> for a moment: OK for the UNO regulator"],
    ["SG90 servo (optional)", "<b>own 5 V supply</b>", "100 mA", "600 mA: too much for the UNO, never on this rail"],
], ["36%", "20%", "18%", "26%"])}
<div class="grid2">
{co("tip", "Why 7.4 V?", "<p>The L298N loses about 2 V, so the TT motors receive about <b>5.4 V</b>, which is their sweet spot. "
    "Two 18650 cells in series give exactly that.</p>")}
{co("warn", "Why the UNO's 5 V, not the L298N's?", "<p>The L298N's small regulator gets hot and its 5 V dips when the motors start, so the ESP32-CAM resets (“brownout”). "
    "The UNO's regulator is stronger. With the 2200 µF capacitor it keeps the camera running. It gets warm: that is normal.</p>")}
</div>
"""
    return dict(file="01_Overview_and_Parts_List.pdf", footer="Module 01 · Overview & Parts List", module="01",
                title="Overview &amp; Parts List", subtitle="What we are building, how it works, and exactly which parts to buy.",
                hero=collage(["uno", "esp32cam", "l298n", "hcsr04", "leds", "motor", "battery", "breadboard"]), body=body)


# =========================================================================== 02
def conn(rows):
    return table(["", "From", "To", "Note"], [[sw(c), a, b, n] for c, a, b, n in rows], ["7%", "31%", "31%", "31%"])


def step_block(n, title, sub, image, intro, todo, rows, extra="", img_style=""):
    return f"""
<div class="step">
 <div class="step-h"><div class="n">{n}</div><div><h2>{title}</h2><div class="sub">{sub}</div></div></div>
 {fig(img(image), "", img_style)}
 {intro}
 {steps(todo)}
 {conn(rows)}
 {extra}
</div>"""


def m02():
    U, E, L = (lambda p: pin(p, "u")), (lambda p: pin(p, "e")), (lambda p: pin(p, "l"))
    body = f"""
{sec(1, "Module 02", "Wiring guide")}
<p>This module shows <b>every connection</b> in the car, one step at a time. Each step has a close-up picture with the
wires of that step highlighted, a list of actions and a connection table. Do the steps <b>in order</b> and test as you go.</p>
{objectives(["Wire a two-rail power system safely (7.4 V and 5 V) with a common ground",
             "Connect the motors, motor driver, sensor, buzzer and LEDs to the Arduino",
             "Use a voltage divider to connect a 5 V board to a 3.3 V board",
             "Check a circuit with a multimeter before powering it"], 120)}
{co("warn", "Golden rules: read before you touch a wire", bullets([
    "Always wire with the <b>battery switched OFF</b> (better: batteries out of the holder).",
    "Check the <b>battery polarity with the multimeter</b> before the first power-on: battery + must reach the switch, the L298N +12V and the UNO <b>VIN</b>.",
    "<b>All GNDs are connected together</b>: battery −, L298N, UNO, ESP32-CAM, sensor, buzzer, LEDs.",
    "7.4 V goes <b>only</b> to the L298N +12V terminal and the UNO <b>VIN</b> pin. Never to a 5V pin or to the ESP32-CAM.",
    "Never connect a 5 V output straight to an ESP32 pin: use the voltage divider (step 7)."]))}
<h2>The complete wiring</h2>
{fig(img("wiring_full.svg"), "Complete realistic wiring diagram. An A3 poster version is in <b>Robot_Car_Wiring_Poster.pdf</b>.")}
<div class="grid2">
{co("tip", "How to read the pictures", "<p>Each coloured line is one jumper wire. Where wires cross they are <b>not</b> connected (they are insulated). "
    "The breadboard's long <b style='color:#dc2626'>red + rail</b> is the 5 V bus and the <b style='color:#2563eb'>blue − rail</b> is the GND bus.</p>")}
{co("note", "Breadboard rails", "<p>On some breadboards the rails are split in the middle. Check with the multimeter (continuity mode) that "
    "column 1 and column 30 of each rail are connected. If not, add a short jumper across the gap.</p>")}
</div>

{step_block(1, "Power system", "Battery → switch → L298N +12V · second wires: +12V → UNO VIN, GND → breadboard − rail", "step1_power_zoom.svg",
  co("note", "Two wires in one screw terminal", "<p>The L298N <b>+12V</b> terminal holds two red wires: the one from the switch and the one to the UNO <b>VIN</b>. "
     "The <b>GND</b> terminal holds two black wires: battery − and the wire to the breadboard − rail. Twist the bare ends together, push them in and tighten firmly. "
     "No buck converter is needed: the UNO makes the 5 V (step 4).</p>"),
  ["Battery <b>+</b> (red) → switch, first pin.", "Switch second pin → <b>L298N +12V</b>.", "Battery <b>−</b> (black) → <b>L298N GND</b>.",
   "Second red wire: <b>L298N +12V → UNO VIN</b> (power header, next to GND).",
   "Second black wire: <b>L298N GND → breadboard − rail</b>.",
   "On the L298N: <b>remove the ENA and ENB jumpers</b> and keep the 5V-EN jumper on. Leave the L298N +5V terminal empty."],
  [(RED, "Battery +", "Switch", "22 AWG wire"), (RED, "Switch", "L298N +12V", "carries the motor current"), (BLK, "Battery −", "L298N GND", ""),
   (RED, "L298N +12V", U("VIN"), "7.4 V into the UNO regulator"), (BLK, "L298N GND", "Breadboard − rail", "= GND bus")])}

{step_block(2, "Motors", "Left pair on OUT1/OUT2 · right pair on OUT3/OUT4", "step2_motors_zoom.svg",
  "<p>The two motors on the same side are wired <b>in parallel</b>: both wires of the front motor and both wires of the rear motor go into the same two screws.</p>",
  ["Solder about 15 cm wires and a <b>100 nF capacitor</b> to each motor (see Module 03).",
   "Left front + left rear: wire A → <b>OUT1</b>, wire B → <b>OUT2</b>.",
   "Right front + right rear: wire A → <b>OUT3</b>, wire B → <b>OUT4</b>.",
   "Tighten the screws and pull gently on each wire to check it is held."],
  [(C["M1"], "Left motors, wire A", "L298N OUT1", "both motors"), (C["M2"], "Left motors, wire B", "L298N OUT2", "both motors"),
   (C["M1"], "Right motors, wire A", "L298N OUT3", "both motors"), (C["M2"], "Right motors, wire B", "L298N OUT4", "both motors")],
  co("tip", "Wrong direction later?", "<p>If one motor turns against its partner, swap <b>only that motor's</b> two wires. If a whole side is backwards, "
     "change <code>INVERT_LEFT</code> / <code>INVERT_RIGHT</code> in the UNO code.</p>"))}

{step_block(3, "L298N → Arduino UNO", "Six control wires, side by side", "step3_control_zoom.svg",
  "<p>The pins were chosen so the six wires run in the same order on both boards. Use six different colours.</p>",
  ["ENA → <b>D11</b> (PWM ~, left speed).", "IN1 → <b>D10</b>, IN2 → <b>D9</b> (left direction).",
   "IN3 → <b>D8</b>, IN4 → <b>D7</b> (right direction).", "ENB → <b>D6</b> (PWM ~, right speed).",
   "Test now: upload <code>tests/01_motor_test</code> with the wheels in the air (Module 05)."],
  [(C["ENA"], L("ENA"), U("D11 ~"), "left speed (PWM)"), (C["IN1"], L("IN1"), U("D10"), "left direction"),
   (C["IN2"], L("IN2"), U("D9"), "left direction"), (C["IN3"], L("IN3"), U("D8"), "right direction"),
   (C["IN4"], L("IN4"), U("D7"), "right direction"), (C["ENB"], L("ENB"), U("D6 ~"), "right speed (PWM)")])}

{step_block(4, "5 V rail from the Arduino", "UNO 5V and GND to the breadboard rails", "step4_uno_power_zoom.svg",
  "<p>The UNO turns the 7.4 V on <b>VIN</b> into a steady <b>5 V</b>. Its <b>5V pin</b> now feeds the breadboard + rail, and that rail powers the ESP32-CAM, the sensor, the buzzer and the LEDs.</p>",
  ["UNO <b>GND</b> → breadboard <b>− rail</b>.", "UNO <b>5V</b> → breadboard <b>+ rail</b>.",
   "Do <b>not</b> also plug a power supply into the UNO's DC jack: VIN is already used.",
   "Check: battery on, multimeter between the + and − rails = <b>4.9–5.1 V</b>."],
  [(BLK, U("GND"), "Breadboard − rail", "power header"), (ORG, U("5V"), "Breadboard + rail", "= 5 V bus for everything")],
  co("ok", "Can I keep the USB cable plugged in?", "<p>Yes. The UNO picks the stronger supply by itself. On USB only (battery off) the electronics and the camera work but the motors do not move. That is handy while testing.</p>"))}

{step_block(5, "Rear ultrasonic sensor", "TRIG → D13 · ECHO → D12 · power from the rails", "step5_sensor_zoom.svg",
  "<p>The HC-SR04 is mounted at the <b>rear</b> of the car, facing backwards (Module 03 shows the height).</p>",
  ["HC-SR04 <b>TRIG</b> → UNO <b>D13</b>.", "HC-SR04 <b>ECHO</b> → UNO <b>D12</b>.",
   "<b>VCC</b> → + rail, <b>GND</b> → − rail.", "Test: <code>tests/02_ultrasonic_test</code>."],
  [(C["TRIG"], "HC-SR04 TRIG", U("D13"), "UNO sends the ping"), (C["ECHO"], "HC-SR04 ECHO", U("D12"), "UNO measures the echo"),
   (ORG, "HC-SR04 VCC", "+ rail", "5 V"), (BLK, "HC-SR04 GND", "− rail", "")])}

{step_block(6, "Lights + buzzer", "A0 red rear LED · A2 white reverse LED · A3 buzzer · A4 two headlights", "step6_alarm_zoom.svg",
  "<p>These parts sit on the breadboard. The analog pins A0–A4 work as normal digital outputs. The rear parts use the <b>bottom half</b> of the breadboard, the headlights the <b>top half</b>.</p>",
  ["A0 wire → hole <b>4f</b>. 220 Ω resistor from <b>4h</b> to <b>8h</b>. Red LED: long leg (+) in <b>8j</b>, short leg in the <b>− rail</b>.",
   "A2 wire → <b>12f</b>. 220 Ω from <b>12h</b> to <b>16h</b>. White LED: long leg in <b>16j</b>, short leg in the − rail.",
   "A3 wire → <b>20f</b>. Buzzer <b>+</b> leg in <b>20h</b>, − leg in <b>23h</b>, short black jumper from <b>23j</b> to the − rail.",
   "<b>Headlights:</b> A4 wire → <b>24a</b>. 220 Ω from <b>24c</b> to <b>27c</b>, white LED long leg in <b>27a</b>, short leg in the <b>top − rail</b>. "
   "Second 220 Ω from <b>24d</b> to <b>21d</b>, white LED long leg in <b>21a</b>, short leg in the top − rail.",
   "Black jumper from the <b>top − rail</b> to the <b>bottom − rail</b> (column 1), so the top rail is GND too.",
   "On the car the headlights sit at the <b>front</b>: put each LED on two female-male jumpers instead of in the breadboard.",
   "Test: <code>tests/03_buzzer_led_test</code>."],
  [(C["A0"], U("A0"), "220 Ω → red LED (+)", "rear warning light"), (C["A2"], U("A2"), "220 Ω → white LED (+)", "reverse light"),
   (C["A3"], U("A3"), "Buzzer +", "buzzer − to − rail"), (C["A4"], U("A4"), "2 × (220 Ω → white LED +)", "headlights, one resistor each"),
   (BLK, "Top − rail", "Bottom − rail", "bridge jumper")],
  co("tip", "LED tips", "<p>The <b>longer leg</b> is + (anode); an LED wired backwards simply stays off. "
     "Each headlight has <b>its own 220 Ω</b>: with one shared resistor the brighter LED would take most of the current. Two headlights on A4 (≈ 26 mA) are fine for one UNO pin.</p>"),
  "max-height:72mm")}

{step_block(7, "ESP32-CAM", "IO14 → D3 · D2 → divider → IO15 · 5V / GND · 2200 µF capacitor", "step7_esp32cam_zoom.svg",
  f'<div class="grid2" style="align-items:center"><div>{co("note", "Why a voltage divider?", "<p>The UNO speaks 5 V, but ESP32 pins only accept 3.3 V. Two resistors make 5 V × 2k / (1k + 2k) = <b>3.33 V</b>. The other direction (3.3 V into the UNO) needs no divider: the UNO reads 3.3 V as HIGH.</p>")}</div><div class="card">{DIVIDER_SVG}</div></div>',
  ["Divider: UNO <b>D2</b> wire → hole <b>25f</b>. <b>1 kΩ</b> from <b>25h</b> to <b>29h</b>. <b>2 kΩ</b> from <b>29j</b> to the − rail.",
   "ESP32-CAM <b>IO15</b> → hole <b>29f</b> (middle of the divider).",
   "ESP32-CAM <b>IO14</b> → UNO <b>D3</b> (direct wire).",
   "ESP32-CAM <b>5V</b> → + rail, <b>GND</b> → − rail (use the 5V pin, <b>not</b> 3V3).",
   "<b>2200 µF capacitor</b> across the rails next to the ESP wires: the leg on the side with the stripe (−) goes in the − rail.",
   "Leave <b>U0T, U0R and IO0</b> free: they are for programming."],
  [(C["TX"], E("IO14") + " (TX)", U("D3") + " (RX)", "direct wire"), (C["RX"], U("D2") + " (TX)", "1 kΩ → " + E("IO15") + " (RX)", "2 kΩ from IO15 to GND"),
   (ORG, E("5V"), "+ rail", "not 3V3!"), (BLK, E("GND"), "− rail", "")])}

<div class="pb"></div>
{sec("✓", "Module 02", "Full pin map &amp; final check")}
<div class="grid2">
<div><h3>Arduino UNO</h3>{table(["Pin", "Connected to"], [
    [U("D2"), "→ 1 kΩ → ESP32 IO15 (2 kΩ to GND)"], [U("D3"), "← ESP32 IO14"], [U("D6 ~"), "L298N ENB"], [U("D7"), "L298N IN4"],
    [U("D8"), "L298N IN3"], [U("D9"), "L298N IN2"], [U("D10"), "L298N IN1"], [U("D11 ~"), "L298N ENA"],
    [U("D12"), "HC-SR04 ECHO"], [U("D13"), "HC-SR04 TRIG"], [U("A0"), "Red rear LED (220 Ω)"], [U("A1"), "Servo (optional)"],
    [U("A2"), "White reverse LED (220 Ω)"], [U("A3"), "Active buzzer +"], [U("A4"), "2 headlights (220 Ω each)"],
    [U("VIN"), "L298N +12V (7.4 V)"], [U("5V / GND"), "+ rail / − rail"], [U("D0 / D1"), "free (USB)"]], ["30%", "70%"])}</div>
<div><h3>ESP32-CAM</h3>{table(["Pin", "Connected to"], [
    [E("5V"), "+ rail"], [E("GND"), "− rail"], [E("IO14"), "TX → UNO D3"], [E("IO15"), "RX ← divider ← UNO D2"],
    [E("IO4"), "on-board flash LED = cam light"], [E("IO33"), "on-board red LED = status"], [E("U0T U0R IO0"), "programming only"]], ["34%", "66%"])}
<h3>L298N</h3>{table(["Terminal", "Connected to"], [
    [L("OUT1/OUT2"), "left motors (parallel)"], [L("OUT3/OUT4"), "right motors (parallel)"], [L("+12V"), "switch (battery +) and UNO VIN"],
    [L("GND"), "battery − and breadboard − rail"], [L("+5V"), "not connected"], [L("ENA…ENB"), "UNO D11, D10, D9, D8, D7, D6"]], ["34%", "66%"])}</div>
</div>
<h2>Final check before the first power-on</h2>
<div class="grid2"><ul class="check">
<li>Battery polarity checked, 5 V rail reads 4.9–5.1 V</li><li>ENA/ENB jumpers removed, 5V-EN jumper on</li><li>No 7.4 V wire touches a 5 V or signal pin</li>
<li>All grounds connected (check with the multimeter)</li></ul><ul class="check">
<li>Divider in place between D2 and IO15</li><li>ESP32-CAM on 5V (not 3V3)</li><li>2200 µF capacitor polarity correct</li>
<li>Wheels off the ground for the first test</li></ul></div>
<div class="sig"><div>Wired by (student)</div><div>Checked by (teacher)</div><div>Date</div></div>

<div class="pb"></div>
{sec("S", "Module 02", "Schematic view")}
<p>The same circuit drawn as a schematic. It is useful for understanding and for finding faults.</p>
{fig(img("schematic.svg"))}
"""
    return dict(file="02_Wiring_Guide.pdf", footer="Module 02 · Wiring Guide", module="02", title="Wiring Guide",
                subtitle="Every connection step by step, with realistic pictures, connection tables and checks.",
                hero=hero("wiring_full.svg"), body=body)


# =========================================================================== 03
def m03():
    legend = [(1, "ESP32-CAM: front edge, lens forward, tilted up 5–10°"), (2, "L298N motor driver: bottom plate, centre, heatsink free"),
              (3, "Arduino UNO: top plate, centre"), (4, "Breadboard: 5 V / GND rails, resistors, LEDs, buzzer"),
              (5, "2200 µF capacitor next to the ESP32-CAM 5V"), (6, "ON/OFF switch: on the side, easy to reach"),
              (7, "2×18650 battery: low and towards the rear"), (8, "HC-SR04: rear edge, facing back, 8–12 cm high"),
              (9, "Buzzer: anywhere at the rear"), (10, "Rear: red LED (A0) left, white reverse LED (A2) right"),
              (11, "2 white headlights (A4) at the front corners")]
    leg = "".join(f'<div style="display:flex;gap:7pt;margin-bottom:5pt;align-items:flex-start"><span class="qty" style="background:#f97316;color:#fff;border-radius:99pt;min-width:16pt;text-align:center;font-weight:800;font-size:8pt;padding:1pt 4pt">{n}</span><span class="small">{t}</span></div>' for n, t in legend)
    body = f"""
{sec(1, "Module 03", "Mechanical assembly")}
<p>A neat mechanical build makes wiring easier and the car more reliable. Motors and the battery go on the
<b>bottom plate</b>; the electronics go on the <b>top plate</b>. Follow the layout below.</p>
{objectives(["Prepare motors with noise-suppression capacitors", "Place every part where it works best (camera, sensor, battery, antenna)",
             "Mount the rear sensor at the right height and angle", "Do a mechanical safety check before power-on"], 90)}
<div style="display:grid;grid-template-columns:1.35fr 1fr;gap:12pt;align-items:start">
{fig(img("chassis_layout.svg"), "Top view: where each part goes (front at the top)")}
<div class="card" style="margin-top:6pt"><h3 style="margin-top:0">Layout legend</h3>{leg}
{co("tip", "WiFi antenna", "<p>Keep the ESP32-CAM antenna end (the zig-zag gold trace on the module) away from metal, motors and the L298N. Otherwise the WiFi range drops.</p>")}</div>
</div>

<div class="pb"></div>
{sec(2, "Module 03", "Step by step")}
<h2>Step 1: Prepare the motors</h2>
{steps(["Solder about 15 cm of wire to both tabs of each motor (red + black or two colours).",
        "Solder a <b>100 nF ceramic capacitor</b> across the two tabs of each motor. This reduces electrical noise that disturbs the camera and WiFi.",
        "Twist each motor's two wires together.",
        "Mount the motors with the acrylic brackets so all <b>tabs face inwards</b>."])}
<h2>Step 2: Bottom plate</h2>
{steps(["Fix the <b>L298N</b> in the centre, motor terminals facing the motors. Leave air around the heatsink.",
        "Place the <b>battery holder</b> towards the rear. Mount the <b>switch</b> on the side.",
        "Connect the motor wires to OUT1–OUT4 (Module 02, step 2)."])}
<h2>Step 3: Spacers and top plate</h2>
{steps(["Screw in the brass spacers and mount the top plate.",
        "Pass the control wires (ENA…ENB) and the power wires up through the centre opening.",
        "Fix the <b>Arduino UNO</b> (nylon standoffs or foam tape) and stick the <b>breadboard</b> next to it."])}
<h2>Step 4: Front, the camera and the headlights</h2>
{steps(["Mount the <b>ESP32-CAM at the very front</b>, camera looking forward, tilted up 5–10° (3D-printed holder, L-bracket or foam tape).",
        "Make sure the camera ribbon cable is fully inserted and the black latch is closed.",
        "Fix the <b>two white headlights</b> at the front corners, pointing forward (5 mm LED holders or hot glue). Do not cover the camera lens.",
        "Run the headlight wires back to the breadboard along the side of the plate (long leg = + towards its 220 Ω resistor)."])}
<h2>Step 5: Rear, sensor, buzzer and LEDs</h2>
<figure class="card" style="padding:8pt">{SENSOR_SIDE_SVG}<figcaption>Side view: correct sensor height and angle</figcaption></figure>
{steps(["Mount the <b>HC-SR04 on the rear edge, facing straight back</b>, 8–12 cm above the floor, tilted up slightly.",
        "Nothing (wires, screws, wheels) may stick out in front of its two “eyes”.",
        "Fix the red LED at the left rear corner (like a brake light), the white reverse LED at the right rear corner, and the buzzer at the rear."])}
{co("warn", "Sensor too low or pointing down?", "<p>It will detect the floor and beep, or block reversing, all the time. Raise it and tilt it up.</p>")}
<h2>Step 6: Cable management</h2>
{bullets(["Keep the power wires short. Use zip ties to keep wires away from the wheels.",
          "Route signal wires away from motor wires where possible.",
          "Battery low and centred or slightly to the rear: a skid-steer car turns better that way."])}
<h2>Mechanical check</h2>
<div class="grid2"><ul class="check"><li>All 4 wheels turn freely by hand</li><li>No wire can touch a wheel</li><li>Battery holder is firmly fixed</li></ul>
<ul class="check"><li>Camera faces forward and is tilted up a little</li><li>Sensor faces back, 8–12 cm high, nothing in front of it</li><li>Headlights at the front, pointing forward</li><li>Switch is reachable</li></ul></div>
<div class="sig"><div>Built by (student)</div><div>Checked by (teacher)</div></div>
"""
    return dict(file="03_Assembly_Guide.pdf", footer="Module 03 · Assembly Guide", module="03", title="Assembly Guide",
                subtitle="Where every part goes on the chassis, how to mount it, and the mechanical safety check.",
                hero=hero("chassis_layout.svg"), body=body)


# =========================================================================== 04
def m04():
    dots = [(1, 4.5, 30), (2, 1.0, 61), (3, 28, 40), (4, 37.5, 19), (5, 36.5, 70), (6, 25.8, 81),
            (7, 75.5, 22), (8, 74.6, 68), (9, 74.6, 80), (10, 81, 0.5), (11, 92.4, 8), (12, 38, 1.5)]
    dhtml = "".join(f'<div class="dot" style="left:{x}%;top:{y}%">{n}</div>' for n, x, y in dots)
    body = f"""
{sec(1, "Module 04", "Software &amp; uploading")}
<p>The car runs two programs: one on the <b>Arduino UNO</b> (motors, sensor, alarm) and one on the <b>ESP32-CAM</b>
(WiFi, camera, phone app). Both are uploaded with the free <b>Arduino IDE 2</b>. No extra libraries are needed.</p>
{objectives(["Install the Arduino IDE and the ESP32 board package", "Upload code to an Arduino UNO and to an ESP32-CAM",
             "Read the Serial Monitor to check that a board works", "Connect a phone and use every feature of the app"], 60)}
<h2>1 · Install the software</h2>
{steps(["Download and install <b>Arduino IDE 2</b> from <code>arduino.cc/en/software</code>.",
        "Open <b>File → Preferences</b>. In <i>Additional boards manager URLs</i> paste:<pre>https://espressif.github.io/arduino-esp32/package_esp32_index.json</pre>",
        "Open <b>Tools → Board → Boards Manager</b>, search <b>esp32</b> and install <b>“esp32 by Espressif Systems”</b> (version 3.x).",
        "Open the project folder. The code is in <code>firmware/uno_controller</code> and <code>firmware/esp32cam_robot</code>."])}
<h2>2 · Board settings</h2>
{table(["Setting", "Arduino UNO", "ESP32-CAM"], [
    ["Sketch", "<code>uno_controller.ino</code>", "<code>esp32cam_robot.ino</code>"],
    ["Tools → Board", "Arduino AVR Boards → <b>Arduino Uno</b>", "esp32 → <b>AI Thinker ESP32-CAM</b>"],
    ["Partition scheme", "—", "<b>Huge APP (3MB No OTA)</b>"], ["PSRAM", "—", "Enabled (if the menu exists)"],
    ["Port", "the UNO's USB port", "the MB board's port (CH340)"]], ["24%", "38%", "38%"])}
{co("tip", "Arduino Nano or a clone?", "<p>Choose <b>Arduino Nano</b> and, if the upload fails, set <b>Processor → ATmega328P (Old Bootloader)</b>.</p>")}

<h2>3 · Upload the Arduino UNO</h2>
{steps(["Open <code>uno_controller.ino</code> and select the board and port.", "Click <b>Upload</b> (→). You can leave all wires connected.",
        "After a reset you hear a <b>short beep</b> and the <b>headlights blink</b>: the UNO is running."])}

<div class="pb"></div>
<h2>4 · Upload the ESP32-CAM</h2>
<div class="grid2">
<div class="card"><h3 style="margin-top:0">Option A: ESP32-CAM-MB board <span class="badge opt">EASY</span></h3>
{steps(["Unplug the ESP32-CAM from the car and press it onto the MB board.", "Connect the USB cable, select the port, click <b>Upload</b>.",
        "Stuck at <code>Connecting....</code>? Hold <b>IO0</b>, tap <b>RST</b>, release IO0.", "When it is done, press <b>RST</b> to start the program."])}</div>
<div class="card"><h3 style="margin-top:0">Option B: FTDI adapter</h3>
{table(["FTDI", "ESP32-CAM"], [["5V (jumper on 5 V)", "5V"], ["GND", "GND"], ["TX", "U0R"], ["RX", "U0T"], ["—", "<b>IO0 → GND</b> while uploading"]])}
<p class="small">Press RST, upload, then <b>remove the IO0–GND wire</b> and press RST again.</p></div>
</div>
<h3>Check the Serial Monitor (115200 baud)</h3>
<pre>=== ROBOT CAR ESP32-CAM ===
WiFi network <span class="s">"RobotCar"</span> / password <span class="s">"12345678"</span>
Open  http://192.168.4.1  on your phone
Ready.</pre>
{co("warn", "“Camera init FAILED”", "<p>The ribbon cable is not fully inserted (open the latch, push it in, close it) or the wrong board type is selected.</p>")}
<h2>5 · Connect the phone</h2>
{steps(["Switch on the car. The small red LED on the back of the ESP32-CAM <b>blinks</b>: it is waiting for a phone.",
        "On the phone, open WiFi settings → network <b>RobotCar</b>, password <b>12345678</b>. If the phone warns “no internet”, choose <b>stay connected</b>.",
        "Open the browser at <b>http://192.168.4.1</b>. The chips show <b>connected</b> and <b>car ok</b>.",
        "Turn the phone sideways and tap ⛶ for full screen. Tip: <b>Add to Home screen</b> so it opens like an app.",
        "The first time, a short <b>tips</b> screen explains the controls. Tap <b>Let's drive</b>.",
        "Optional: on a PC joined to the same WiFi, open <b>http://192.168.4.1/view</b> for the classroom viewer (section 3)."])}
{co("ok", "Built-in safety", "<p>Release the joystick or press the red <b>STOP</b>: the car stops. Lock the phone, switch app or lose WiFi: it stops within 0.6 s. "
    "It never reverses closer than the auto-brake distance (forward still works).<br><b>Keyboard</b> (app on a laptop): W A S D or arrows = drive · Space = horn · L = headlights · Esc = stop.</p>")}

<div class="pb"></div>
{sec(2, "Module 04", "Using the app")}
<div class="shot">{fig(img("app_landscape.png"), "The phone app in landscape: reversing towards an obstacle at 21 cm, headlights on")}{dhtml}</div>
{table(["#", "Element", "What it does"], [
    ["1", "<b>Joystick</b>", "Drag up/down = forward/back, left/right = turn. Release = stop. (A D-pad mode is in the settings.)"],
    ["2", "Speed gears", "<b>Slow</b> 40 % · <b>Normal</b> 70 % · <b>Fast</b> 100 %. Start with Slow"],
    ["3", "<b>Live video</b>", "From the front camera. A flashing <b>red border</b> means an obstacle is close behind while reversing"],
    ["4", "Status tags", "<b>REVERSE</b> while backing up, <b>AUTO-BRAKE</b> when the car refuses to go back, <b>LIGHTS</b> when the headlights are on"],
    ["5", "Parking bar", "More bars lit = closer, green → amber → red. Shows the distance in cm"],
    ["6", "Video buttons", "<b>Pause</b> the video · save a <b>Photo</b> on the phone · <b>Cam light</b> = the camera's own flash LED · ⛶ full screen"],
    ["7", "<b>Rear radar</b>", "Distance behind the car: green, amber or red zone, beam cone, big distance number and zone name"],
    ["8", "<b>Headlights</b>", "<b>OFF</b> · <b>ON</b> · <b>HAZARD</b> (headlights and red rear LED blink together)"],
    ["9", "<b>Horn</b>", "Hold to sound the car's buzzer"],
    ["10", "<b>STOP</b>", "Stops the car at once"],
    ["11", "Settings", "See the next page"],
    ["12", "Status chips", "<b>connected</b> to the car and <b>car ok</b> (the UNO answers). Amber or red = check the WiFi"]], ["6%", "20%", "74%"])}


<div class="pb"></div>
<h2>Settings</h2>
<div style="display:grid;grid-template-columns:.9fr 1.1fr;gap:10pt;align-items:start">
<div>{fig(img("app_settings.png"), "Settings sheet (tap the sliders icon)")}
{fig(img("app_portrait.png"), "Portrait mode works too", "max-width:45%")}</div>
<div>{table(["Setting", "Meaning"], [
    ["<b>Parking alarm</b>", ""],
    ["Start beeping at", "Beeping starts below this distance (default 100 cm)"],
    ["Danger / auto-brake at", "Continuous tone + brake below this (default 15 cm)"],
    ["Auto-brake when reversing", "Block reversing near obstacles"], ["Alarm also when not reversing", "Beep in any direction"],
    ["Mute the car buzzer", "The LED still flashes"], ["Beep on this phone / Vibrate", "The phone copies the alarm"],
    ["<b>Driving</b>", ""],
    ["Controls", "Joystick or D-pad"], ["Exact speed", "Fine-tune the speed gear (30–100 %)"], ["Turn sensitivity", "How sharp the car turns"],
    ["<b>Camera</b>", ""],
    ["Resolution / picture quality", "VGA = default. QVGA = smoothest video"], ["Cam light brightness", "Brightness of the camera's flash LED"],
    ["Flip / Mirror", "If the image is upside down or reversed"],
    ["<b>Radar &amp; connection</b>", ""],
    ["Radar range", "Distance shown at the edge of the radar"], ["Car address", "Leave 192.168.4.1 unless you changed the WiFi mode"],
    ["Show the tips again", "Opens the first-time tips screen"]], ["42%", "58%"])}</div>
</div>
<div class="pb"></div>
{sec(3, "Module 04", "Classroom viewer on a PC")}
<p>The car serves a <b>second page</b> made for a computer or a projector. One student drives with the phone while the class watches the
video, the radar and live data on the big screen. Nothing needs to be installed.</p>
{steps(["Connect the PC to the WiFi <b>RobotCar</b> (password <b>12345678</b>).",
        "Open <b>http://192.168.4.1/view</b> in Chrome, Edge or Firefox. (The phone app shows the same link in its settings, and a banner on a PC.)",
        "Press <b>F11</b> or the full-screen button for the projector."])}
{fig(img("app_pc_view.png"), "The classroom viewer (here in demo mode, reversing at 28 cm)")}
{table(["Part of the page", "What it shows or does"], [
    ["<b>Front camera</b>", "Big live video with the REVERSE / AUTO-BRAKE tags and a large distance number while reversing"],
    ["Save photo · Record video", "Photo as JPG with a data strip (time, distance, speeds). Video as a WebM file with the distance drawn on it"],
    ["<b>Rear radar</b>", "The same radar as on the phone, larger"],
    ["<b>Car status</b>", "Picture of the car: headlight beams, rear and reverse lights, wheel arrows, left/right motor bars, alarm and horn"],
    ["Distance chart", "The distance behind the car for the last 60 s, with the warning and danger lines. Closest value shown"],
    ["Events", "Log with time: reversing, alarms, auto-brake, lights, connection"],
    ["Teacher controls", "Headlights, horn, cam light, radar range, and <b>keyboard driving</b> (W A S D / arrows, Space = horn, Esc = stop)"]],
    ["28%", "72%"])}
<div class="grid2">
{co("note", "How many screens?", "<p>Up to <b>3 video screens</b> at once (for example the phone and two PCs). All screens get the radar and data. "
    "Close unused tabs if a screen says “too many viewers”.</p>")}
{co("tip", "Exam and report ideas", "<p>Record a video of a parking manoeuvre, then use the chart to read the closest distance and the moment the auto-brake stopped the car.</p>")}
</div>

<h2>Customising the car</h2>
{table(["File · setting", "Default", "Change it to…"], [
    ["<code>config.h</code> · AP_SSID / AP_PASSWORD", "RobotCar / 12345678", "give every group its own WiFi name"],
    ["<code>config.h</code> · STA_SSID", "empty", "join a school WiFi or phone hotspot instead"],
    ["<code>config.h</code> · CAM_VFLIP", "0", "1 if the camera is mounted upside down"],
    ["<code>uno_controller.ino</code> · MIN_PWM", "90", "raise if the car doesn't move at low speed"],
    ["<code>uno_controller.ino</code> · INVERT_LEFT/RIGHT", "false", "flip a side that drives backwards"],
    ["<code>uno_controller.ino</code> · USE_SERVO", "0", "1 = scanning radar with an SG90 servo on A1"]], ["44%", "22%", "34%"])}
<div class="grid2">
{co("note", "Several cars in one classroom", "<p>Give each car a different <code>AP_SSID</code> (RobotCar1, RobotCar2 …) and a different <code>AP_CHANNEL</code> (1, 6, 11) so they don't interfere.</p>")}
{co("tip", "Editing the pages", "<p>The phone app is <code>web/index.html</code>, the PC viewer <code>web/view.html</code>. Open them on a computer to try them in <b>demo mode</b>. Then run <code>python3 tools/build_ui.py</code> and upload the ESP32-CAM again.</p>")}
</div>
"""
    return dict(file="04_Software_and_App_Guide.pdf", footer="Module 04 · Software & App Guide", module="04", title="Software &amp; App Guide",
                subtitle="Install the tools, upload both boards, connect the phone and master every control.",
                hero=hero("app_landscape.png"), body=body)


# =========================================================================== 05
def m05():
    rec = lambda rows: table(["#", "Test", "How", "Expected result", "Pass"], [[str(i + 1)] + r + ['<span class="box"></span>'] for i, r in enumerate(rows)],
                             ["5%", "18%", "33%", "36%", "8%"])
    body = f"""
{sec(1, "Module 05", "Testing, step by step")}
<p>Never test everything at once. Upload the small <b>test sketches</b> in <code>tests/</code> one by one: when something fails,
you know exactly which part to look at. Fill in this record as you go.</p>
{objectives(["Test a system part by part (unit tests before system tests)", "Use the Serial Monitor and a multimeter to find faults",
             "Fix the most common problems on your own"], 60)}
<h2>Lab record: bring-up tests</h2>
{rec([["Power", "Battery on, multimeter on the breadboard + and − rails (= UNO 5V)", "4.9–5.1 V"],
      ["Motors", "Upload <code>01_motor_test</code>, wheels in the air", "All forward → all back → spin left → spin right"],
      ["Sensor", "Upload <code>02_ultrasonic_test</code>, Serial Monitor 115200", "Distance in cm follows your hand"],
      ["Lights + buzzer", "Upload <code>03_buzzer_led_test</code>", "Headlights on, 4 hazard blinks, then beeps get faster and continuous. Red LED in sync"],
      ["Bench alarm", "Upload <code>06_parking_alarm_bench</code>, hand towards sensor", "SAFE → WARN (faster beeps) → STOP! (continuous)"],
      ["Camera only", "Upload <code>05_esp32cam_test</code>, join WiFi “CamTest”, open 192.168.4.1", "Live video, Photo works, flash LED dims"],
      ["ESP32-CAM", "Upload <code>esp32cam_robot</code>, Serial Monitor", "“Ready.” and WiFi “RobotCar” visible"],
      ["Serial link", "Upload <code>04_link_test</code> on the UNO, open the app", "Radar shows 20→200 cm. Serial shows <code>M,…</code> lines"],
      ["Full car", "Upload <code>uno_controller</code>", "Drive with the phone"]])}
<h2>Acceptance test: the finished car</h2>
{rec([["Drive", "Forward 2 m, turn left and right", "Smooth, straight, responds immediately"],
      ["Video", "Watch the camera while driving", "Clear image, little delay"],
      ["Parking alarm", "Reverse slowly towards a wall", "Beeping starts at about 100 cm and speeds up, continuous near 20 cm"],
      ["Auto-brake", "Keep reversing", "Stops at about 15 cm, AUTO-BRAKE tag on the phone. Forward still works"],
      ["Radar", "Move a box behind the car", "Radar distance and colour change"],
      ["Headlights", "Tap ON, then HAZARD in the app", "Both front LEDs light. HAZARD blinks them with the red rear LED"],
      ["PC viewer", "Open <code>192.168.4.1/view</code> on a PC while driving", "Video, radar, car status and chart update live"],
      ["Fail-safe", "Drive, then turn phone WiFi off", "Car stops within 1 s"]])}
<div class="sig"><div>Tested by (student)</div><div>Verified by (teacher)</div><div>Date</div></div>

<div class="pb"></div>
{sec(2, "Module 05", "Troubleshooting")}
<h2>Power &amp; resets</h2>
{table(["Symptom", "Likely cause", "Fix"], [
    ["ESP32-CAM reboots when the motors start (<code>Brownout detector was triggered</code>)", "5 V dips", "Check the 2200 µF capacitor (polarity, close to the ESP). ESP on the UNO 5V rail, not the L298N's 5V. Short power wires, good charged 18650s. Try the Slow gear"],
    ["Everything dies at full speed", "Weak or fake batteries", "Better cells, charge them, lower the speed slider"],
    ["L298N gets hot", "Normal up to ~60 °C", "Keep the heatsink free. Don't stall the motors"],
    ["UNO regulator (next to the DC jack) very hot", "Too much on the 5 V rail", "Warm is normal. Never put a servo or motor on the 5 V rail"],
    ["Nothing turns on with the battery", "VIN wire missing or loose", "Check the second red wire L298N +12V → UNO VIN and the battery polarity"]], ["38%", "22%", "40%"])}
<h2>Motors</h2>
{table(["Symptom", "Fix"], [
    ["Nothing moves, but the app shows L/R values", "ENA/ENB jumpers still on? L298N GND connected? Battery on? Chip says “car not responding” → serial link"],
    ["One side drives backwards", "Swap that side's OUT wires, or set <code>INVERT_LEFT/RIGHT = true</code>"],
    ["One motor of a pair fights the other", "Swap only that motor's two wires"],
    ["Turns left when you push right", "Swap the left and right OUT pairs (OUT1/2 ↔ OUT3/4)"],
    ["Hums but doesn't move at low speed", "Raise <code>MIN_PWM</code> (110–130)"],
    ["Won't reverse even with nothing behind", "Sensor sees the floor or the chassis: mount it higher, tilt it up. Or turn auto-brake off"]], ["40%", "60%"])}
<h2>Camera &amp; WiFi</h2>
{table(["Symptom", "Fix"], [
    ["<code>Camera init FAILED</code>", "Re-seat the ribbon cable, close the latch. Board = AI Thinker ESP32-CAM"],
    ["No “RobotCar” network", "Check the Serial Monitor. Maybe STA mode is set in <code>config.h</code>"],
    ["Phone switches back to mobile data", "Turn mobile data off, or choose “stay connected” when the phone says “no internet”"],
    ["Video stutters", "Settings → QVGA, quality 15–20. Keep the camera away from the motors"],
    ["Video OK but controls “offline”", "Reload the page. Use <code>http://</code>, not https. Disable data-saver mode"]], ["40%", "60%"])}
<h2>Sensor &amp; alarm</h2>
{table(["Symptom", "Fix"], [
    ["Radar: “waiting for sensor…”", "UNO not sending: check D2 → 1k → IO15, IO14 → D3, common GND, UNO powered"],
    ["Distance always “&gt;400”", "TRIG/ECHO swapped, no 5 V on VCC, or nothing within 4 m"],
    ["Buzzer silent, LED works", "Passive buzzer (needs an active one), wrong polarity, or “Mute the car buzzer” is on"]], ["40%", "60%"])}
<h2>Lights &amp; PC viewer</h2>
{table(["Symptom", "Fix"], [
    ["No headlight lights up", "A4 wire in row 24 (top half)? Top − rail bridged to the bottom − rail? Does the LIGHTS tag appear in the app?"],
    ["Only one headlight works", "That LED is backwards (long leg = +), or its resistor is not in the same column as the LED's long leg"],
    ["PC viewer: “too many viewers”", "Max 3 video screens at once. Close other tabs or the photo page"],
    ["PC viewer: no data, only demo", "Open <code>http://192.168.4.1/view</code>, not the file from the project folder. PC on the RobotCar WiFi"]], ["40%", "60%"])}
<h2>Multimeter checks</h2>
{table(["Measure between", "Should read"], [
    ["Battery + and −", "7.0–8.4 V (recharge below 6.8 V)"], ["UNO 5V (+ rail) and GND", "4.9–5.1 V"],
    ["ESP32-CAM 5V and GND while driving", "above 4.75 V"], ["ESP32 IO15 and GND, car idle", "≈ 3.3 V (divider OK). <b>Never 5 V</b>"]], ["50%", "50%"])}
"""
    return dict(file="05_Testing_and_Troubleshooting.pdf", footer="Module 05 · Testing & Troubleshooting", module="05",
                title="Testing &amp; Troubleshooting", subtitle="Test one part at a time, record the results, and fix the common problems yourself.",
                hero=hero("step6_alarm_zoom.svg"), body=body)


# =========================================================================== 06
def m06():
    body = f"""
{sec(1, "Module 06", "How the system works")}
<p>This reference explains what happens inside the code: the messages between the phone, the ESP32-CAM and the Arduino, the
safety rules, and the maths behind driving and the parking alarm. Use it for oral exams, reports and your own improvements.</p>
{objectives(["Describe the data flow between phone, ESP32-CAM and Arduino", "Explain a simple text protocol with a checksum",
             "Explain differential (tank) steering and the parking-alarm timing", "Plan an extension of the project"], 45)}
<h2>Data flow</h2>
<pre>Phone browser ──WebSocket ws://192.168.4.1/ws (text)──► ESP32-CAM ──UART 38400──► Arduino UNO
Phone browser ◄────────────────────────────────────── ESP32-CAM ◄─────────────── Arduino UNO
PC  /view     ◄── same WebSocket (data) ─────────────── ESP32-CAM
Phone + PC &lt;img&gt; ◄── MJPEG http://192.168.4.1:81/stream ─ ESP32-CAM  (max 3 screens)</pre>
<h2>Messages</h2>
<h3>Phone → ESP32-CAM (WebSocket)</h3>
{table(["Message", "Meaning", "Handled by"], [
    ["<code>M,&lt;left&gt;,&lt;right&gt;</code>", "Motor speeds −255…255, sent every 100 ms", "forwarded to UNO"],
    ["<code>H,0|1</code>", "Horn off/on", "forwarded"],
    ["<code>C,warn,stop,brake,always,mute</code>", "Alarm settings (cm, cm, 0/1, 0/1, 0/1)", "forwarded (repeated every 3 s)"],
    ["<code>L,0|1|2</code>", "Headlights off / on / hazard", "forwarded (repeated every 3 s)"],
    ["<code>K,0-255</code>", "Cam light: brightness of the ESP32-CAM flash LED", "ESP32"],
    ["<code>F,n</code> / <code>Q,n</code>", "Camera frame size / JPEG quality", "ESP32"],
    ["<code>V,0|1</code> / <code>X,0|1</code>", "Flip / mirror image", "ESP32"],
    ["<code>R,phone</code> / <code>R,view</code>", "The page says what it is: a driving phone or a PC viewer (for the counters)", "ESP32"]], ["34%", "44%", "22%"])}
<h3>ESP32-CAM → UNO (serial, with checksum)</h3>
<p>The same <code>M</code>, <code>H</code>, <code>C</code>, <code>L</code> and <code>S</code> lines, plus <code>*XX</code> = the XOR of every character before the <code>*</code>, in hex.
Example: <code>M,0,0*4D</code>. The UNO's software serial port can lose bytes while it is transmitting. A damaged line fails the checksum and is ignored,
and the next one arrives 150 ms later.</p>
<h3>UNO → ESP32-CAM → phone</h3>
{table(["Message", "Meaning"], [
    ["<code>D,&lt;angle&gt;,&lt;cm&gt;,&lt;flags&gt;</code>", "Every 60 ms. angle = 90 (fixed sensor) or 30–150 (servo). cm = 0 means nothing in range. "
     "flags (add them up): 1 reversing · 2 alarm · 4 auto-brake · 8 horn · 16 headlights lit · 32 hazard"],
    ["<code>T,l,r,light,horn,flash</code>", "ESP32 → every screen, every 250 ms: motor speeds, headlight mode, horn and cam light, so all screens stay in sync"],
    ["<code>I,rssi,phones,uno_ok,viewers</code>", "ESP32 status every 2 s: WiFi signal, number of phones, UNO answering, number of PC viewers"]], ["34%", "66%"])}
<h3>Web addresses</h3>
{table(["Address", "Returns"], [["<code>http://192.168.4.1/</code>", "the phone app"], ["<code>/view</code>", "the PC classroom viewer"],
    ["<code>/status</code>", "JSON with distance, flags, lights, camera settings"],
    ["<code>/cmd?c=M,150,150</code>", "send a command over plain HTTP (for other apps, e.g. MIT App Inventor)"],
    ["<code>/capture</code>", "one JPEG photo"], ["<code>:81/stream</code>", "live MJPEG video"]], ["40%", "60%"])}

<div class="pb"></div>
{sec(2, "Module 06", "Inside the code")}
<h2>Safety rules (fail-safes)</h2>
{table(["Where", "Rule"], [
    ["Phone", "Sends stop when the joystick is released or the page is hidden"],
    ["ESP32-CAM", "No command from the phone for 500 ms → sends stop"],
    ["Arduino", "No command for 600 ms → motors off, horn off"],
    ["Arduino", "Reversing and distance ≤ stop distance and auto-brake on → backwards speed forced to 0"],
    ["Arduino", "Speed ramps 18 PWM steps every 10 ms → no current spikes that could reset the ESP32"]], ["22%", "78%"])}
<h2>Differential (tank) steering</h2>
<p>The joystick gives <b>y</b> (forward/back) and <b>x</b> (left/right) between −1 and 1. Each side's speed is:</p>
<pre>left  = y + x · turn        right = y − x · turn
divide both by max(1, |left|, |right|)   <span class="c">// keep within −1…1</span>
PWM   = value × 255 × speed%</pre>
<p>Push straight up and both sides are equal, so the car goes straight. Push right and the left side is faster, so the car turns right. Push fully right with y = 0 and the sides
are opposite, so the car spins on the spot.</p>
<h2>Parking alarm timing</h2>
<pre>if distance ≤ stop + 5 cm  →  continuous tone
else period = map(distance, stop+5 … warn, 120 ms … 900 ms)
     buzzer ON for the first half of each period</pre>
<p>Closer means a shorter period, so the beeping is faster, exactly like a real car. The distance is the <b>median of the last 3 readings</b>, which removes single wrong echoes.</p>
<h2>Files</h2>
{table(["File", "Main parts"], [
    ["<code>firmware/uno_controller/uno_controller.ino</code>", "<code>setSide()</code> motor driver · <code>rampTo()</code> soft start · <code>pingCm()</code>, <code>median3()</code> sensor · <code>updateAlarm()</code> · <code>handleLine()</code>, <code>checksumOk()</code> protocol"],
    ["<code>firmware/esp32cam_robot/esp32cam_robot.ino</code>", "<code>cameraInit()</code> · <code>streamHandler()</code> video · <code>wsHandler()</code>, <code>wsBroadcast()</code> WebSocket · <code>readUno()</code>, <code>sendToUno()</code>, <code>linkSend()</code>"],
    ["<code>firmware/esp32cam_robot/config.h</code>", "WiFi name and password, pins, camera options"],
    ["<code>web/index.html</code>", "Phone app: joystick, video, radar canvas, headlights, settings, demo mode"],
    ["<code>web/view.html</code>", "PC viewer: video, photo/video recording, radar, car status, chart, events"],
    ["<code>tests/01…06</code>", "Small test sketches for each part (05 = camera only, 06 = bench parking alarm)"]], ["44%", "56%"])}
<h2>Ideas for your own improvements</h2>
<div class="grid2">
{co("note", "Scanning radar", "<p>Mount the HC-SR04 on an SG90 servo (A1) and set <code>USE_SERVO 1</code>. The phone radar then shows a real sweep with blips.</p>")}
{co("note", "Front collision stop", "<p>Add a second HC-SR04 at the front (free pins: D4, D5) and stop forward motion near obstacles.</p>")}
{co("note", "Battery gauge", "<p>Measure the battery with a 10k/4.7k divider on A5 and show the voltage in the app with a new message <code>B,…</code>.</p>")}
{co("note", "Your own app", "<p>Build an MIT App Inventor app that sends <code>/cmd?c=M,…</code> requests and shows <code>/status</code>.</p>")}
</div>
"""
    return dict(file="06_Technical_Reference.pdf", footer="Module 06 · Technical Reference", module="06", title="Technical Reference",
                subtitle="Protocol, safety rules, steering and alarm maths, code structure and extension ideas.",
                hero=hero("schematic.svg"), body=body)


def m07():
    R, O, X = '<span class="badge req">Must do</span>', '<span class="badge opt">Optional</span>', '<span class="muted small">Extra</span>'
    lessons = [
        ["1", "Meet the board", "The UNO's pins: digital, PWM (~), analog, power", "Module 02: every wire goes to one of these pins", R],
        ["2", "Blink an LED", "<code>pinMode</code>, <code>digitalWrite</code>, <code>delay</code>", f"Red rear LED {pin('A0')}, white reverse LED {pin('A2')}, headlights {pin('A4')}", R],
        ["3", "Push a button", "Digital input, pull-down resistor", "Not on the car (idea: a start button)", X],
        ["4", "Turn a knob", "<code>analogRead</code>, <code>map()</code>", "<code>map()</code> turns distance into beep speed", O],
        ["5", "Mix colours", "PWM with <code>analogWrite</code> 0–255", f"Motor speed on ENA {pin('D11')} / ENB {pin('D6')}", R],
        ["6", "Sense light", "Analog sensor (LDR)", f"Idea: LDR on {pin('A5')} switches the headlights on when it gets dark", X],
        ["7", "Read a sensor", "HC-SR04, <code>pulseIn()</code>, ÷58 = cm", f"Rear sensor: TRIG {pin('D13')}, ECHO {pin('D12')}", R],
        ["8", "Make a sound", "Buzzer, <code>tone()</code>", f"Alarm buzzer on {pin('A3')}, active type, no <code>tone()</code>", R],
        ["9", "Mini piano", "Arrays and loops", "Idea: a melody for the horn", X],
        ["10", "Control a motor", "PWM speed + transistor driver", "The L298N does the same job and also reverses the motor", R],
        ["11", "Sense heat", "TMP36 temperature sensor", "Not on the car", X],
        ["12", "Sweep a servo", "SG90 servo, <code>Servo.h</code>", f"Scanning radar option <code>USE_SERVO</code>, servo on {pin('A1')}", O],
        ["13", "Spin the wheel", "Stepper + ULN2003", "Not on the car", X],
        ["14", "Smart plant", "Sensor + decision", "Same idea as auto-brake: read → decide → act", X],
        ["15", "Feel the force", "Force sensor", "Not on the car", X],
        ["16", "Build a project", "<b>Parking sensor</b>: zones with comparisons", "The core of our rear alarm, see Test 06", R],
    ]
    body = f"""
{sec(1, "Module 07", "Warm-up with the Learn Arduino website")}
<p><b>learn-arduino-red.vercel.app</b> is a free website with 16 interactive 3D lessons for the Arduino UNO.
Each lesson shows the board and parts in 3D with the wires drawn. The <b>Overview, Pinout, Example and Specifications</b> tabs explain it,
and you can <b>run the sketch in the browser</b> and see the result. Do the lessons marked <b>Must do</b> before you build the car:
they teach every idea the car's UNO code uses.</p>
{objectives(["Explain digitalWrite, analogWrite (PWM), pulseIn and map() in your own words",
             "Read an HC-SR04 distance and turn it into zones with comparisons",
             "Move a sketch from the website's pins to the robot car's pins and test it on a real UNO"], 90)}
{co("tip", "How to use the website", bullets([
    "Open it on a computer (Chrome or Edge) for the best 3D view. Drag to move, <b>Q / E</b> to rotate, scroll to zoom.",
    "Click a part in the 3D scene or a lesson's controls to change its values, then press <b>▶ Run sketch</b> and watch the serial monitor.",
    "The code box is <b>read-only</b>. To change it, press <b>Copy code</b>, paste it into the Arduino IDE and upload it to a real UNO.",
    "The website only knows the <b>Arduino UNO</b>: there is no ESP32-CAM, L298N or WiFi. Those are taught in Modules 02 and 04 of this handbook."]))}
<h2>Lesson map: website → robot car</h2>
{table(["#", "Website lesson", "You learn", "Where the car uses it", ""], lessons, ["5%", "17%", "29%", "37%", "12%"])}

<h2>Same code, different pins</h2>
<p>The website uses its own pins. The car uses other pins because the L298N, the ESP32-CAM link and the sensor all need space.
<b>The code is the same, only the numbers at the top change.</b></p>
{table(["Part", "Website pin", "Robot car pin", "Why the car is different"], [
    ["HC-SR04 TRIG / ECHO", f"{pin('D9')} / {pin('D10')}", f"{pin('D13')} / {pin('D12')}", "D9 and D10 drive the L298N (IN2, IN1)"],
    ["Buzzer", f"{pin('D8')}, passive, <code>tone()</code>", f"{pin('A3')}, active, <code>digitalWrite</code>", "<code>tone()</code> uses Timer2 and would break the PWM on D11 (ENA)"],
    ["LED", f"{pin('D13')} (built-in)", f"{pin('A0')} red, {pin('A2')} white, {pin('A4')} headlights", "D13 is the sensor's TRIG on the car"],
    ["Motor PWM", f"{pin('~D6')} → TIP120", f"{pin('~D11')} ENA, {pin('~D6')} ENB → L298N", "Two sides of the car, and the L298N can reverse"],
    ["Servo", f"{pin('D9')}", f"{pin('A1')}", "Optional scanning radar"],
    ["Serial Monitor", "9600 baud", "115200 baud", "Faster, so printing does not slow the car down"]],
    ["21%", "22%", "27%", "30%"])}
{co("warn", "Active or passive buzzer?", "<p>An <b>active</b> buzzer beeps by itself when its pin is HIGH (this is the one in our parts list). A <b>passive</b> buzzer, like the website's, "
    "needs <code>tone()</code>. On the car <code>tone()</code> would stop the left motors working properly, so keep the active buzzer.</p>")}

<h2 style="break-before:page">Bridge exercise: Test 06, parking alarm on the bench</h2>
<p>Lesson 16 lights a traffic light. Its specifications even say <i>“Next step: add a buzzer from lesson 8”</i>.
<code>tests/06_parking_alarm_bench</code> does exactly that, on the robot car's pins, so the wires stay the same when you move them to the car.</p>
<div class="grid2 keep">
<div>{table(["From", "To"], [
    ["HC-SR04 VCC / GND", f"{pin('5V')} / {pin('GND')}"],
    ["HC-SR04 TRIG", pin("D13")], ["HC-SR04 ECHO", pin("D12")],
    ["Red LED (+) via 220 Ω", pin("A0")], ["White LED (+) via 220 Ω", pin("A2")],
    ["Buzzer (+)", pin("A3")], ["LED (−), buzzer (−)", pin("GND")]], ["55%", "45%"])}</div>
<div>{steps(["Wire the parts on a breadboard with the UNO only (no battery, no motors).",
             "Open <code>tests/06_parking_alarm_bench</code>, select <b>Arduino Uno</b>, upload.",
             "Open the Serial Monitor at <b>115200</b>.",
             "Move your hand slowly towards the sensor and watch the bar grow."])}</div></div>
<div class="keep">{table(["Distance", "Zone", "Buzzer + red LED", "Serial Monitor"], [
    ["more than 100 cm", "SAFE", "Off", "<code>150 cm SAFE ##</code>"],
    ["100 → 20 cm", "WARN", "Beeps, faster as you get closer (900 → 120 ms)", "<code>55 cm WARN ######</code>"],
    ["20 cm or less", "STOP!", "Continuous", "<code>12 cm STOP! ##########</code>"]],
    ["18%", "12%", "35%", "35%"])}</div>

<h2 style="break-before:page">Worksheet</h2>
{table(["#", "Question", "Your answer"], [
    ["1", "Lesson 2: what does <code>digitalWrite(pin, HIGH)</code> do to the pin's voltage?", ""],
    ["2", "Lesson 5: <code>analogWrite(pin, 128)</code>. About what percentage of full power is that?", ""],
    ["3", "Lesson 7: the echo lasted 1160 µs. How far is the obstacle? Show your calculation.", ""],
    ["4", "Lesson 7: why divide by 58 and not by 29? (Hint: the sound travels there <i>and back</i>.)", ""],
    ["5", "Lesson 8: what is the difference between an active and a passive buzzer?", ""],
    ["6", "Lesson 10: why can't an Arduino pin power a motor directly? What does the L298N add?", ""],
    ["7", "Lesson 16: write the comparison that is true only when the obstacle is between 20 and 100 cm.", ""],
    ["8", "Test 06: with <code>map(cm, 20, 100, 120, 900)</code>, what is the beep period at 60 cm?", ""]],
    ["5%", "55%", "40%"]).replace("<td></td>", '<td style="height:15mm"></td>')}
{co("note", "Challenges (extra)", bullets([
    "Add the green / yellow / red traffic light from lesson 16 on free pins and keep the buzzer working.",
    "Change <code>WARN_CM</code> and <code>STOP_CM</code>. What happens if STOP is bigger than WARN? Fix it in code.",
    "Lesson 12: mount the sensor on a servo and print the distance for 5 angles: a text radar."]))}
<h2>Checklist</h2>
{table(["Done", "Item"], [['<span class="box"></span>', x] for x in [
    "Lessons 1, 2, 5, 7, 8, 10 and 16 run on the website", "Worksheet answered",
    "Test 06 works on a real UNO: SAFE / WARN / STOP! zones correct", "I can explain why the car's pins differ from the website's"]], ["10%", "90%"])}
<div class="sig"><div>Student</div><div>Teacher</div><div>Date</div></div>
<p class="small muted" style="margin-top:8pt">Learn Arduino website designed by x.com/DilumSanjaya. This module only links to it; the lessons belong to their author.</p>
"""
    return dict(file="07_Warm_Up_Learn_Arduino.pdf", footer="Module 07 · Warm-up with Learn Arduino", module="07",
                title="Warm-up Lessons", subtitle="Use the free Learn Arduino website to learn every idea the car's code uses, then test it on a real UNO.",
                hero=collage(["uno", "hcsr04", "buzzer", "leds"]), body=body)


MODULES = [m01, m02, m03, m04, m05, m06, m07]
