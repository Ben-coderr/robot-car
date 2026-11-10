#!/usr/bin/env python3
"""
3D model of the finished robot car, as a coloured 3MF file (opens in SolidCraft, PrusaSlicer,
Bambu Studio, Windows 3D Viewer, Blender ...).

    python3 tools/3d/make_3d_model.py   ->  docs/3d/robot_car_assembly.3mf, .stl, robot_car_3d_viewer.html

Units: millimetres. Axes: X = left(-)/right(+), Y = rear(-)/front(+), Z = up.
Every part is a simple block or cylinder with the real part's outside size, so you can see
where everything sits and how big the finished car is. Wires are not drawn.
"""
import math, os, struct, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "docs" / "3d"

# ------------------------------------------------------------------ colours
COL = {
    "acrylic": "#BFE3F2CC", "tyre": "#1F1F1FFF", "rim": "#F2C230FF", "motor": "#E8C33AFF", "metal": "#B8BCC2FF",
    "l298n": "#C62828FF", "heatsink": "#202020FF", "uno": "#00838FFF", "header": "#111111FF",
    "bb": "#F4F1E8FF", "esp": "#1B1B1BFF", "lens": "#0D47A1FF", "hc": "#1565C0FF", "silver": "#D9D9D9FF",
    "batt_box": "#202020FF", "cell1": "#1E5BD8FF", "cell2": "#2E9E44FF", "switch": "#D32F2FFF",
    "led_red": "#FF1744FF", "led_white": "#FAFAFAFF", "buzzer": "#111111FF", "cap": "#1A3D8FFF",
    "brass": "#C9A13BFF", "usb": "#C0C0C0FF", "beam": "#FFF59D66",
}
MATS = list(COL)

parts = []   # (name, material, vertices, triangles)


def add(name, mat, mesh):
    v, t = mesh
    parts.append((name, mat, v, t))


def box(x0, x1, y0, y1, z0, z1):
    v = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    t = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
         (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    return v, t


def boxc(cx, cy, cz, sx, sy, sz):
    return box(cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, cz - sz / 2, cz + sz / 2)


def cyl(c, axis, r, h, n=40, r2=None):
    """Cylinder (or cone if r2) from point c along axis 'x'|'y'|'z' (sign by h)."""
    r2 = r if r2 is None else r2
    cx, cy, cz = c
    def P(a, rr, d):
        u, w = rr * math.cos(a), rr * math.sin(a)
        if axis == "z": return (cx + u, cy + w, cz + d)
        if axis == "y": return (cx + u, cy + d, cz + w)
        return (cx + d, cy + u, cz + w)
    v = [P(2 * math.pi * i / n, r, 0) for i in range(n)] + [P(2 * math.pi * i / n, r2, h) for i in range(n)]
    v += [P(0, 0, 0), P(0, 0, h)]
    b, tp = 2 * n, 2 * n + 1
    t = []
    for i in range(n):
        j = (i + 1) % n
        t += [(i, j, n + i), (j, n + j, n + i), (b, j, i), (tp, n + i, n + j)]
    if (h < 0) != (axis == "y"):          # keep normals pointing outwards
        t = [(a, c_, b_) for a, b_, c_ in t]
    return v, t


def merge(*meshes):
    V, T = [], []
    for v, t in meshes:
        o = len(V); V += v; T += [(a + o, b + o, c + o) for a, b, c in t]
    return V, T


# ================================================================== the car
PW, PL, TH = 150, 250, 3          # chassis plate width, length, thickness
ZB, ZT = 46, 80                    # bottom of lower plate, bottom of upper plate
AX_Y, AX_Z = 82, 32.5              # axle position (front/rear), axle height (65 mm wheels)

# --- chassis plates + brass spacers
add("Bottom plate (acrylic)", "acrylic", box(-PW/2, PW/2, -PL/2, PL/2, ZB, ZB + TH))
add("Top plate (acrylic)", "acrylic", box(-PW/2, PW/2, -PL/2 + 10, PL/2 - 10, ZT, ZT + TH))
for i, (x, y) in enumerate([(-60, 100), (60, 100), (-60, -100), (60, -100), (-60, 0), (60, 0)]):
    add(f"Spacer {i+1} (brass M3, 30 mm)", "brass", cyl((x, y, ZB + TH), "z", 3, ZT - ZB - TH, n=6))

# --- 4 TT motors under the bottom plate + wheels
for side, sx in (("LEFT", -1), ("RIGHT", 1)):
    for end, sy in (("FRONT", 1), ("REAR", -1)):
        y = sy * AX_Y
        # gearbox (yellow) 37 long, motor can (silver) 28 long, along X
        add(f"{side} {end} TT motor gearbox", "motor", boxc(sx * 47, y, AX_Z, 37, 22, 19))
        add(f"{side} {end} wheel shaft", "rim", cyl((sx * 65, y, AX_Z), "x", 2.7, sx * 14, n=12))
        add(f"{side} {end} TT motor", "metal", cyl((sx * 28.5, y, AX_Z), "x", 10, -sx * 26))
        add(f"{side} {end} motor bracket", "acrylic", boxc(sx * 47, y + sy * 0, ZB - 6, 37, 4, 12))
        # wheel: tyre + rim, outside the plate
        wx = sx * 79
        add(f"{side} {end} wheel tyre (65 mm)", "tyre", cyl((wx, y, AX_Z), "x", 32.5, sx * 26, n=60))
        add(f"{side} {end} wheel rim", "rim", cyl((wx + sx * 26, y, AX_Z), "x", 20, sx * 0.8, n=40))
        add(f"{side} {end} 100nF capacitor", "rim", boxc(sx * 14, y, AX_Z, 2.5, 5, 4))

ZBT = ZB + TH   # top surface of the bottom plate

# --- bottom plate: L298N (centre), battery (rear), switch (side)
add("L298N board", "l298n", box(-21.5, 21.5, -10, 33, ZBT + 4, ZBT + 5.6))
add("L298N heatsink", "heatsink", boxc(0, 22, ZBT + 5.6 + 11, 23, 16, 22))
add("L298N screw terminals", "hc", merge(boxc(-19, 8, ZBT + 10, 8, 15, 9), boxc(19, 8, ZBT + 10, 8, 15, 9), boxc(0, -6, ZBT + 10, 23, 8, 9)))
add("L298N standoffs", "brass", merge(*[cyl((x, y, ZBT), "z", 2.5, 4, n=8) for x in (-18, 18) for y in (-7, 30)]))

add("2x18650 battery holder", "batt_box", box(-41, 41, -100, -58, ZBT, ZBT + 21))
add("18650 cell (blue)", "cell1", cyl((-33, -89, ZBT + 11.5), "x", 9.2, 65))
add("18650 cell (green)", "cell2", cyl((-33, -68.5, ZBT + 11.5), "x", 9.2, 65))
add("ON/OFF switch", "switch", box(PW/2 - 22, PW/2 - 2, -40, -26, ZBT, ZBT + 14))

# --- top plate
ZTT = ZT + TH
# Arduino UNO (68.6 x 53.4), USB/DC jack towards the left side
ux0, uy0 = -26.7, -5
add("Arduino UNO board", "uno", box(ux0, ux0 + 53.4, uy0, uy0 + 68.6, ZTT + 5, ZTT + 6.6))
add("UNO USB-B socket", "usb", box(ux0 - 6, ux0 + 10, uy0 + 38, uy0 + 50, ZTT + 6.6, ZTT + 17.5))
add("UNO DC jack", "heatsink", box(ux0 - 2, ux0 + 12, uy0 + 7, uy0 + 16, ZTT + 6.6, ZTT + 17.5))
add("UNO chip (ATmega328P)", "heatsink", box(ux0 + 18, ux0 + 28, uy0 + 12, uy0 + 47, ZTT + 6.6, ZTT + 10))
add("UNO pin headers", "header", merge(box(ux0 + 50.5, ux0 + 53, uy0 + 4, uy0 + 64, ZTT + 6.6, ZTT + 15),
                                        box(ux0 + 0.5, ux0 + 3, uy0 + 20, uy0 + 64, ZTT + 6.6, ZTT + 15)))
add("UNO standoffs", "brass", merge(*[cyl((ux0 + x, uy0 + y, ZTT), "z", 2.5, 5, n=8) for x, y in ((4, 4), (49, 4), (4, 64), (49, 64))]))

# Breadboard 82 x 55 x 9.5, rear part of the top plate
add("Breadboard (400 points)", "bb", box(-41, 41, -80, -25, ZTT, ZTT + 9.5))
add("Breadboard + rail strip", "led_red", box(-38, 38, -27.5, -26.5, ZTT + 9.5, ZTT + 9.7))
add("Breadboard - rail strip", "hc", box(-38, 38, -78.5, -77.5, ZTT + 9.5, ZTT + 9.7))
# resistors / divider (small blocks on the breadboard)
for i, x in enumerate((-30, -18, -6, 6, 18)):
    add(f"Resistor {i+1}", "rim", boxc(x, -40, ZTT + 11, 7, 2.4, 2.4))

# Buzzer on the breadboard, rear left
add("Active buzzer", "buzzer", cyl((24, -58, ZTT + 9.5), "z", 6, 9.5))

# ESP32-CAM at the front edge, standing up, lens forward, tilted up ~7 deg (drawn upright)
ey = PL/2 - 18
add("ESP32-CAM holder", "acrylic", box(-18, 18, ey - 10, ey, ZTT, ZTT + 4))
add("ESP32-CAM board", "esp", box(-13.5, 13.5, ey, ey + 4.5, ZTT + 4, ZTT + 44))
add("ESP32-CAM camera (OV2640)", "heatsink", box(-4.5, 4.5, ey + 4.5, ey + 9, ZTT + 30, ZTT + 39))
add("ESP32-CAM lens", "lens", cyl((0, ey + 9, ZTT + 34.5), "y", 3.2, 2.5))
add("ESP32-CAM flash LED", "led_white", box(6, 10, ey + 4.5, ey + 5.5, ZTT + 10, ZTT + 14))
add("ESP32-CAM metal shield", "silver", box(-11, 11, ey + 4.5, ey + 6, ZTT + 12, ZTT + 28))

# 2200 uF capacitor next to the ESP32-CAM
add("2200uF 16V capacitor", "cap", cyl((26, ey - 8, ZTT), "z", 6.5, 26))
add("2200uF capacitor top", "silver", cyl((26, ey - 8, ZTT + 26), "z", 6.5, 0.6))

# Headlights: 2 white 5 mm LEDs at the front corners, pointing forward
for nm, x in (("LEFT", -62), ("RIGHT", 62)):
    add(f"{nm} headlight holder", "header", box(x - 5, x + 5, PL/2 - 18, PL/2 - 10, ZTT, ZTT + 12))
    add(f"{nm} HEADLIGHT (white LED, A4)", "led_white", merge(cyl((x, PL/2 - 10, ZTT + 7), "y", 2.5, 5.5), cyl((x, PL/2 - 4.5, ZTT + 7), "y", 2.5, 2.5, r2=0.6)))
    add(f"{nm} headlight beam (light)", "beam", cyl((x, PL/2 - 2, ZTT + 7), "y", 2.5, 45, r2=14))

# HC-SR04 at the rear edge, facing backwards, on its bracket
hy = -PL/2 + 12
add("HC-SR04 bracket", "header", box(-24, 24, hy, hy + 10, ZTT, ZTT + 3))
add("HC-SR04 board", "hc", box(-22.5, 22.5, hy - 1.6, hy, ZTT + 3, ZTT + 23))
for i, x in enumerate((-13, 13)):
    add(f"HC-SR04 transducer {i+1}", "silver", cyl((x, hy - 1.6, ZTT + 13), "y", 8, -12))
add("HC-SR04 pins", "header", box(-5, 5, hy, hy + 6, ZTT + 20, ZTT + 23))

# Rear lights: red (A0) left corner, white reverse (A2) right corner, pointing backwards
for nm, x, mat in (("Red rear LED (A0)", -62, "led_red"), ("White reverse LED (A2)", 62, "led_white")):
    add(nm + " holder", "header", box(x - 5, x + 5, -PL/2 + 10, -PL/2 + 18, ZTT, ZTT + 12))
    add(nm, mat, merge(cyl((x, -PL/2 + 10, ZTT + 7), "y", 2.5, -5.5), cyl((x, -PL/2 + 4.5, ZTT + 7), "y", 2.5, -2.5, r2=0.6)))


# ================================================================== writers
def hexcol(c):
    return "#" + c.lstrip("#").upper()


def write_3mf(path):
    res = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">',
           '<metadata name="Title">Robot Car - final assembly</metadata>',
           '<metadata name="Designer">Robot Car project</metadata>', '<resources>',
           '<basematerials id="1">' + "".join(f'<base name="{m}" displaycolor="{hexcol(COL[m])}"/>' for m in MATS) + '</basematerials>']
    for i, (name, mat, v, t) in enumerate(parts):
        oid = i + 2
        res.append(f'<object id="{oid}" type="model" name="{name}" pid="1" pindex="{MATS.index(mat)}"><mesh><vertices>')
        res.append("".join(f'<vertex x="{x:.3f}" y="{y:.3f}" z="{z:.3f}"/>' for x, y, z in v))
        res.append("</vertices><triangles>")
        res.append("".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t))
        res.append("</triangles></mesh></object>")
    res.append("</resources><build>" + "".join(f'<item objectid="{i + 2}"/>' for i in range(len(parts))) + "</build></model>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr("3D/3dmodel.model", "\n".join(res))


def write_stl(path):
    tris = []
    for _, _, v, t in parts:
        for a, b, c in t:
            tris.append((v[a], v[b], v[c]))
    with open(path, "wb") as f:
        f.write(b"Robot Car final assembly".ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for p, q, r in tris:
            ux, uy, uz = (q[0]-p[0], q[1]-p[1], q[2]-p[2]); vx, vy, vz = (r[0]-p[0], r[1]-p[1], r[2]-p[2])
            n = (uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx); L = math.sqrt(sum(k*k for k in n)) or 1
            f.write(struct.pack("<12fH", n[0]/L, n[1]/L, n[2]/L, *p, *q, *r, 0))


VIEWER = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robot Car 3D</title><style>body{margin:0;background:#eef2f6;font-family:system-ui,sans-serif;overflow:hidden}
#info{position:fixed;left:12px;top:10px;background:#fffd;padding:8px 12px;border-radius:10px;font-size:13px;color:#0f172a;max-width:340px}
#tip{position:fixed;left:12px;bottom:10px;background:#0f172aee;color:#fff;padding:5px 10px;border-radius:8px;font-size:13px;pointer-events:none;display:none}</style></head>
<body><div id="info"><b>Robot Car: final assembly</b><br>Drag = rotate · scroll = zoom · right-drag = move · hover a part to see its name.<br>Sizes in mm, wires not drawn.</div><div id="tip"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const D=__DATA__;
const r=new THREE.WebGLRenderer({antialias:true}); r.setPixelRatio(devicePixelRatio); r.setSize(innerWidth,innerHeight); r.setClearColor(0xeef2f6); document.body.appendChild(r.domElement);
const s=new THREE.Scene(); s.add(new THREE.HemisphereLight(0xffffff,0x667788,0.9)); const dl=new THREE.DirectionalLight(0xffffff,0.7); dl.position.set(200,-150,400); s.add(dl);
const grid=new THREE.GridHelper(600,30,0xbcc6d2,0xd8dee6); grid.rotation.x=Math.PI/2; s.add(grid);
const cam=new THREE.PerspectiveCamera(35,innerWidth/innerHeight,1,5000); cam.up.set(0,0,1); cam.position.set(-330,380,300);
const ctl=new THREE.OrbitControls(cam,r.domElement); ctl.target.set(0,0,60); ctl.update();
const meshes=[];
for(const p of D){const g=new THREE.BufferGeometry(); g.setAttribute("position",new THREE.Float32BufferAttribute(p.v,3)); g.setIndex(p.t); g.computeVertexNormals();
 const h=p.c.slice(1), a=parseInt(h.slice(6,8),16)/255;
 const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:"#"+h.slice(0,6),transparent:a<1,opacity:a,side:THREE.DoubleSide,roughness:.6,flatShading:true})); m.name=p.n; s.add(m); if(a>.5) meshes.push(m);}
const ray=new THREE.Raycaster(), mp=new THREE.Vector2(), tip=document.getElementById("tip");
addEventListener("pointermove",e=>{mp.set(e.clientX/innerWidth*2-1,-e.clientY/innerHeight*2+1); ray.setFromCamera(mp,cam); const hit=ray.intersectObjects(meshes)[0];
 if(hit){tip.textContent=hit.object.name; tip.style.display="block";} else tip.style.display="none";});
addEventListener("resize",()=>{cam.aspect=innerWidth/innerHeight; cam.updateProjectionMatrix(); r.setSize(innerWidth,innerHeight);});
(function loop(){requestAnimationFrame(loop); r.render(s,cam);})();
</script></body></html>"""


def write_html(path):
    import json
    data = [dict(n=n, c=COL[m], v=[round(c, 2) for p in v for c in p], t=[i for tr in t for i in tr]) for n, m, v, t in parts]
    Path(path).write_text(VIEWER.replace("__DATA__", json.dumps(data, separators=(",", ":"))), encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    write_3mf(OUT / "robot_car_assembly.3mf")
    write_stl(OUT / "robot_car_assembly.stl")
    write_html(OUT / "robot_car_3d_viewer.html")
    allv = [p for _, _, v, _ in parts for p in v]
    size = [max(p[i] for p in allv) - min(p[i] for p in allv) for i in range(3)]
    print(f"{len(parts)} parts · size {size[0]:.0f} x {size[1]:.0f} x {size[2]:.0f} mm (W x L x H)")
    print("written", OUT, ": robot_car_assembly.3mf / .stl / robot_car_3d_viewer.html")
