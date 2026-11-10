#!/usr/bin/env python3
"""
Shopping list PDF for the robot car (one car), with optional dzduino.com prices.

    python3 tools/pdf/build_shopping_list.py [prices.json]

prices.json (optional): {"<item id>": ["<store product name>", "DZD 1,200.00", "In Stock"], ...}
"""
import asyncio, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from design import CSS, ROOT, footer  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

OUT = ROOT / "docs" / "pdf" / "Shopping_List_Robot_Car.pdf"
PRICES = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}

# id, part, exact spec to ask for, used, BUY, note
MAIN = [
    ("chassis", "4WD robot car chassis kit", "2 acrylic plates + <b>4 TT gear motors 3–6 V</b> + 4 wheels + screws/spacers", 1, 1, "Often includes the 2×18650 holder and switch: check the box"),
    ("esp32cam", "ESP32-CAM", "<b>AI-Thinker</b>, <b>OV2640</b> camera, 4 MB PSRAM", 1, 1, "Camera + WiFi"),
    ("esp32mb", "ESP32-CAM-MB programmer", "Micro-USB board the ESP32-CAM plugs into", 1, 1, "For uploading code. Often sold together with the ESP32-CAM"),
    ("uno", "Arduino UNO R3", "ATmega328P, CH340 clone is fine, <b>with USB cable</b>", 1, 1, "Motors, sensor, buzzer"),
    ("l298n", "L298N motor driver", "Red dual H-bridge board with heatsink", 1, 1, ""),
    ("hcsr04", "HC-SR04 ultrasonic sensor", "5 V, 2–400 cm", 1, 1, "Mounted at the rear"),
    ("buzzer", "Buzzer, <b>ACTIVE</b> 5 V", "Ask for “active” (beeps by itself). 2-pin or 3-pin module", 1, 2, "Not passive!"),
    ("cells", "18650 Li-ion battery", "3.7 V, <b>real</b> 2000–3000 mAh, high-drain", 2, 2, "Avoid “9900 mAh” fakes"),
    ("holder", "2×18650 battery holder", "<b>Series</b> (7.4 V), with wires", 1, 1, "Skip if in the kit"),
    ("charger", "18650 charger", "2-slot Li-ion charger, or 2 × TP4056 modules", 1, 1, "Skip if you have one"),
    ("switch", "On/off switch", "Rocker or slide switch, ≥ 3 A", 1, 1, "Skip if in the kit"),
]
SMALL = [
    ("ledred", "LED red 5 mm", "Diffused red", 1, 5, "Rear flashing LED, A0"),
    ("ledwhite", "LED white 5 mm", "Bright white", 3, 6, "Reverse light (A2) + <b>2 headlights</b> (A4)"),
    ("r220", "Resistor 220 Ω", "1/4 W", 4, 10, "One per LED (4 LEDs)"),
    ("r1k", "Resistor 1 kΩ", "1/4 W", 1, 5, "Voltage divider"),
    ("r2k", "Resistor 2 kΩ", "1/4 W (or use 2 × 1 kΩ in series)", 1, 5, "Voltage divider"),
    ("c2200", "Capacitor <b>2200 µF 16 V</b>", "Electrolytic (1000–2200 µF, 10 V or more also OK)", 1, 1, "At ESP32-CAM 5V: stops reboots"),
    ("c100n", "Capacitor 100 nF (“104”)", "Ceramic", 4, 10, "One across each motor"),
]
WIRING = [
    ("breadboard", "Breadboard, half size", "400 points, with + / − rails both sides", 1, 1, "Holds the 5 V rails, LEDs, buzzer, divider"),
    ("jmf", "Jumper wires <b>male–female</b>", "Dupont, 20 cm, pack of 40", 18, 40, "UNO ↔ L298N, sensor, ESP32-CAM, headlights at the front"),
    ("jmm", "Jumper wires <b>male–male</b>", "Dupont, 20 cm, pack of 40", 14, 40, "UNO ↔ breadboard, breadboard links"),
    ("jff", "Jumper wires <b>female–female</b>", "Dupont, 20 cm, pack of 40", 0, 40, "Spare / FTDI wiring"),
    ("wire", "Wire 22 AWG (0.5 mm²)", "Red + black", "1 m each", "2 m", "Battery → switch → L298N, L298N → UNO VIN, motors"),
    ("shrink", "Heat-shrink tube", "Assorted sizes", "—", "1 set", "Covers solder joints"),
    ("ties", "Cable ties (zip ties)", "Small, 100 mm", "10", "1 pack", "Tidy wiring"),
    ("tape", "Double-sided foam tape", "Strong", "—", "1 roll", "Mount boards on the chassis"),
    ("standoffs", "M3 nylon standoffs + screws", "10 mm", "8", "1 set", "Mount UNO / L298N (optional)"),
]
TOOLS = [
    ("multimeter", "Multimeter", "Any digital multimeter", "Required: check battery polarity and the 5 V rail"),
    ("iron", "Soldering iron + solder", "30–60 W, 0.8 mm solder", "Motor wires and capacitors"),
    ("screwdriver", "Small screwdriver set", "Flat + Phillips", "L298N screw terminals"),
    ("stripper", "Wire stripper / cutter", "", ""),
]
OPTIONAL = [
    ("bracket", "Ultrasonic sensor mounting bracket", "For HC-SR04", 1, "Holds the sensor at the rear"),
    ("sg90", "SG90 micro servo", "+ SG90 bracket", 1, "Scanning radar (USE_SERVO). Needs its own 5 V supply"),
    ("ftdi", "FTDI USB-serial adapter", "FT232RL / CP2102, 3.3 V / 5 V", 1, "Only if no ESP32-CAM-MB"),
    ("antenna", "2.4 GHz IPEX antenna", "For ESP32-CAM", 1, "Longer WiFi range"),
    ("usb", "Micro-USB cable (data)", "For the ESP32-CAM-MB", 1, "Skip if you have one"),
]


STOCKNOTE = ('<div class="stockn"><b style="color:#dc2626">Prices and stock from dzduino.com, checked 9 Nov 2026.</b> '
             'The <b>ESP32-CAM, ESP32-CAM-MB, HC-SR04 and 2×18650 holder</b> showed <b>out of stock online</b>. Ask at the counter: '
             'the shop may still have them. <b>No LM2596 / buck converter is needed</b>: the Arduino makes the 5 V.</div>')


def price_cells(iid):
    p = PRICES.get(iid)
    if not p:
        return '<td class="pr"><span class="ask">Not online: ask at the counter</span></td>'
    name, price, stock = p
    oos = "out" in stock.lower()
    return (f'<td class="pr"><b>{price.replace("DZD ", "").replace(".00", "")} DA</b>'
            f'<div class="sn">{name}</div><div class="{"oos" if oos else "ins"}">{stock}</div></td>')


def rows(items, start):
    h, n = "", start
    for iid, part, spec, used, buy, note in items:
        h += (f'<tr><td class="ck"><span class="box"></span></td><td class="n">{n}</td><td><b>{part}</b><div class="spec">{spec}</div></td>'
              f'<td class="q">{used}</td><td class="q buy">{buy}</td>{price_cells(iid) if PRICES else ""}<td class="nt">{note}</td></tr>')
        n += 1
    return h, n


def tbl(title, items, start, color):
    body, n = rows(items, start)
    pc = '<th style="width:17%">dzduino price</th>' if PRICES else ""
    return (f'<h2><span class="bar" style="background:{color}"></span>{title}</h2><table class="sl"><thead><tr>'
            f'<th style="width:4%">✓</th><th style="width:4%">#</th><th>Part · what to ask for</th><th style="width:7%">Used</th>'
            f'<th style="width:9%">BUY</th>{pc}<th style="width:{"20" if PRICES else "28"}%">Note</th></tr></thead><tbody>{body}</tbody></table>'), n


def build_html():
    t1, n = tbl("A · Main parts", MAIN, 1, "#f97316")
    t2, n = tbl("B · Small components", SMALL, n, "#2563eb")
    t3, n = tbl("C · Wires, breadboard &amp; mounting", WIRING, n, "#16a34a")
    tools = "".join(f'<tr><td class="ck"><span class="box"></span></td><td><b>{a}</b><div class="spec">{b}</div></td><td class="nt">{c}</td>{price_cells(i) if PRICES else ""}</tr>'
                    for i, a, b, c in TOOLS)
    opt = "".join(f'<tr><td class="ck"><span class="box"></span></td><td><b>{a}</b><div class="spec">{b}</div></td><td class="q">{q}</td><td class="nt">{c}</td>{price_cells(i) if PRICES else ""}</tr>'
                  for i, a, b, q, c in OPTIONAL)
    pth = "<th style='width:20%'>dzduino price</th>" if PRICES else ""
    total = ""
    if PRICES:
        def val(i, qty):
            p = PRICES.get(i)
            if not p: return 0
            try: return float(p[1].replace("DZD", "").replace(",", "").strip()) * qty
            except ValueError: return 0
        packs = {"jmf", "jmm", "jff", "wire", "shrink", "ties", "tape", "standoffs", "breadboard"}
        items = MAIN + SMALL + WIRING
        s = sum(val(i, 1 if i in packs or not isinstance(b, int) else b) for i, _, _, _, b, _ in items)
        missing = ", ".join(part.replace("<b>", "").replace("</b>", "") for i, part, *_ in items if i not in PRICES)
        total = (f'<div class="tot">Total of the parts with an online price (A + B + C): <b>≈ {s:,.0f} DA</b>'
                 f'<span>Plus the parts not listed online: {missing}. Free delivery over 5000 DA.</span></div>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
body{{font-size:8.6pt}}
.hd{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #f97316;padding-bottom:6pt;margin-bottom:8pt}}
.hd h1{{font-size:20pt;margin:0}} .hd .k{{font-size:7.5pt;letter-spacing:.18em;color:#f97316;font-weight:800}}
.hd .r{{text-align:right;font-size:8pt;color:#475569}}
h2{{font-size:11pt;margin:10pt 0 4pt;display:flex;align-items:center;gap:6pt}} .bar{{width:5pt;height:13pt;border-radius:2pt;display:inline-block}}
table.sl td,table.t2 td{{vertical-align:top;padding:2pt 5pt !important;line-height:1.22}} table.sl th,table.t2 th{{padding:3pt 5pt !important}} .spec{{color:#64748b;font-size:7.6pt;margin-top:1pt}}
.q{{text-align:center;font-weight:600}} .buy{{background:#fff7ed;color:#c2410c;font-weight:800;font-size:9.5pt}}
.n{{color:#94a3b8;font-weight:700}} .nt{{font-size:7.6pt;color:#475569}} .ck{{text-align:center}}
.pr{{font-size:8.5pt}} .sn{{font-size:6.6pt;color:#64748b;line-height:1.2}} .ins{{font-size:6.6pt;color:#16a34a;font-weight:700}} .oos{{font-size:6.6pt;color:#dc2626;font-weight:700}}
  .ask{{font-size:7pt;color:#b45309;font-weight:700}} .stockn{{background:#fef2f2;border:1px solid #fecaca;border-radius:6pt;padding:5pt 8pt;font-size:7.8pt;margin-bottom:4pt}}
.tot{{margin-top:8pt;background:#0b1f3a;color:#fff;border-radius:8pt;padding:8pt 12pt;font-size:10pt}} .tot span{{display:block;font-size:7.5pt;color:#cbd5e1;margin-top:2pt}}
.say{{display:grid;grid-template-columns:1fr 1fr;gap:6pt;margin-top:6pt}}
</style></head><body>
<div class="hd"><div><div class="k">ROBOT CAR PROJECT · SHOPPING LIST</div><h1>Everything to buy for one car</h1></div>
<div class="r">Phone-controlled 4WD car · ESP32-CAM · rear parking radar<br><b>BUY</b> = quantity to buy (includes spares) · <b>Used</b> = on the car</div></div>
{STOCKNOTE if PRICES else ""}{t1}{t2}{t3}
{total}
<h2><span class="bar" style="background:#0b1f3a"></span>D · Tools (if you don't have them)</h2>
<table class="t2"><thead><tr><th style="width:4%">✓</th><th>Tool</th><th>Why</th>{pth}</tr></thead><tbody>{tools}</tbody></table>
<h2><span class="bar" style="background:#94a3b8"></span>E · Optional upgrades</h2>
<table class="t2"><thead><tr><th style="width:4%">✓</th><th>Part</th><th style="width:7%">Qty</th><th>Why</th>{pth}</tr></thead><tbody>{opt}</tbody></table>
<h2><span class="bar" style="background:#dc2626"></span>Check before you pay</h2>
<div class="say">
<div class="co warn"><div class="ic">!</div><div class="bd"><div class="tt">Buzzer must be ACTIVE</div><p>Active = it beeps when you connect 5 V. Ask the seller to test it, or look for a sealed back with a sticker. A passive one stays silent on DC.</p></div></div>
<div class="co warn"><div class="ic">!</div><div class="bd"><div class="tt">ESP32-CAM: AI-Thinker + OV2640</div><p>Check the camera ribbon is in the box. Buying it together with the MB programmer board avoids the FTDI wiring.</p></div></div>
<div class="co tip"><div class="ic">i</div><div class="bd"><div class="tt">18650 batteries</div><p>Real cells weigh about 45 g. Very light cells with “9900 mAh” are fake and will make the ESP32-CAM reboot.</p></div></div>
<div class="co tip"><div class="ic">i</div><div class="bd"><div class="tt">Chassis kit contents</div><p>If the kit already has the battery holder, switch or wires, don't buy them twice: tick them off in the list.</p></div></div>
</div>
<p class="small muted" style="margin-top:8pt">Why these quantities: 4 resistors 220 Ω (red LED A0, white reverse LED A2, 2 white headlights A4: one resistor each), 2200 µF at the ESP32-CAM, 1 kΩ + 2 kΩ divider (UNO D2 → ESP32 IO15), 4 × 100 nF (one per motor).
About 18 male–female and 14 male–male jumpers are used; buy packs of 40 for spares. Prices on dzduino.com change: check them in the shop.</p>
</body></html>"""


async def main():
    html = build_html()
    tmp = OUT.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    async with async_playwright() as p:
        try:
            b = await p.chromium.launch(channel="chrome")
        except Exception:
            b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto(tmp.as_uri(), wait_until="networkidle")
        await pg.pdf(path=str(OUT), format="A4", print_background=True,
                     margin=dict(top="12mm", bottom="14mm", left="12mm", right="12mm"),
                     display_header_footer=True, header_template="<div></div>", footer_template=footer("Shopping list"))
        await b.close()
    tmp.unlink()
    print("written", OUT)


if __name__ == "__main__":
    asyncio.run(main())
