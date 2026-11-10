"""Schematic-style wiring diagram. Run: python3 tools/diagrams/make_schematic.py"""
import os, sys
sys.argv=[sys.argv[0], os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","docs","images","schematic.svg")]
import sys
W,H=1480,1000
o=[]
def a(s): o.append(s)
def rect(x,y,w,h,fill,stroke,rx=10,sw=2): a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def text(x,y,t,size=13,anchor="start",weight="400",fill="#111827",italic=False):
    st=' font-style="italic"' if italic else ''
    a(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}"{st}>{t}</text>')
def line(pts,color,w=3,dash=None):
    d="M"+" L".join(f"{x},{y}" for x,y in pts)
    ds=f' stroke-dasharray="{dash}"' if dash else ''
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{ds}/>')
def path(d,color,w=3): a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
def dot(x,y,c="#111827"): a(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>')
def pin(x,y,label,side,color="#111827"):
    a(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#fff" stroke="{color}" stroke-width="2"/>')
    if side=="l": text(x+10,y+4,label,12,"start","600")
    elif side=="r": text(x-10,y+4,label,12,"end","600")
    elif side=="b": a(f'<text x="{x}" y="{y-10}" font-size="12" text-anchor="middle" font-weight="600" fill="#111827">{label}</text>')
    elif side=="t": a(f'<text x="{x}" y="{y+18}" font-size="12" text-anchor="middle" font-weight="600" fill="#111827">{label}</text>')
def wlabel(x,y,t,color,anchor="middle"):
    wdt=len(t)*6.6+10
    x0 = x-wdt/2 if anchor=="middle" else (x if anchor=="start" else x-wdt)
    a(f'<rect x="{x0}" y="{y-10}" width="{wdt}" height="15" rx="3" fill="#fff" stroke="{color}" stroke-width="1"/>')
    text(x0+wdt/2,y+1.5,t,10.5,"middle","700",color)
def resistor_h(x1,x2,y,color,label):
    # zigzag between x1..x2
    n=6; step=(x2-x1)/n; d=f"M{x1},{y}"
    for i in range(n): d+=f" L{x1+step*(i+0.5)},{y+(-7 if i%2==0 else 7)}"
    d+=f" L{x2},{y}"; path(d,color,2.5); text((x1+x2)/2,y-12,label,11,"middle","700")
def resistor_v(x,y1,y2,color,label,lx=12):
    n=6; step=(y2-y1)/n; d=f"M{x},{y1}"
    for i in range(n): d+=f" L{x+(-7 if i%2==0 else 7)},{y1+step*(i+0.5)}"
    d+=f" L{x},{y2}"; path(d,color,2.5); text(x+lx,(y1+y2)/2+4,label,11,"start","700")
def gnd_sym(x,y):
    line([(x,y),(x,y+8)],"#111827",2.5)
    for i,wd in enumerate([16,10,4]): line([(x-wd/2,y+8+i*5),(x+wd/2,y+8+i*5)],"#111827",2.5)
def led(x,y,color,label):
    # vertical LED, anode top at y, cathode bottom at y+30
    a(f'<path d="M{x-10},{y+8} L{x+10},{y+8} L{x},{y+24} Z" fill="{color}" stroke="#111827" stroke-width="1.5"/>')
    line([(x-10,y+24),(x+10,y+24)],"#111827",2.5)
    line([(x,y),(x,y+8)],"#111827",2.5); line([(x,y+24),(x,y+32)],"#111827",2.5)
    path(f"M{x+13},{y+10} l8,-6 M{x+13},{y+17} l8,-6","#f59e0b",1.6)
    text(x+16,y+38,label,11,"start","600")
def hop_v(x,y1,y2,yc,color,w=3):
    # vertical line from y1 to y2 (y1>y2 upward) hopping over horizontal at yc
    if y1>y2: path(f"M{x},{y1} V{yc+6} a6,6 0 0 1 0,-12 V{y2}",color,w)
    else: path(f"M{x},{y1} V{yc-6} a6,6 0 0 1 0,12 V{y2}",color,w)
def hop_h(x1,x2,y,xc,color,w=3):
    path(f"M{x1},{y} H{xc-6} a6,6 0 0 1 12,0 H{x2}",color,w)

C=dict(bat="#dc2626",gnd="#111827",v5="#ea580c",m1="#92400e",m2="#2563eb",
 ena="#7c3aed",in1="#0284c7",in2="#0d9488",in3="#16a34a",in4="#65a30d",enb="#c026d3",
 tx="#0891b2",rx="#db2777",trig="#ca8a04",echo="#059669",buz="#9333ea",led="#dc2626",wled="#64748b",head="#4f46e5")

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(40,44,"ROBOT CAR – SCHEMATIC WIRING DIAGRAM",24,"start","800")
text(40,68,"4WD chassis · L298N · Arduino UNO/Nano · ESP32-CAM · HC-SR04 (rear) · buzzer + rear LEDs · 2 headlights · 2×18650 (no buck converter: the UNO makes the 5 V)",13,"start","400","#4b5563")

# ---------------- MOTORS ----------------
def motor(x,y,name):
    rect(x,y,140,60,"#fef3c7","#92400e",8)
    a(f'<circle cx="{x+32}" cy="{y+30}" r="18" fill="#fff" stroke="#92400e" stroke-width="2"/>')
    text(x+32,y+35,"M",15,"middle","800","#92400e")
    text(x+58,y+26,name,12,"start","700"); text(x+58,y+42,"3–6 V TT motor",10,"start","400","#6b7280")
motor(30,110,"LEFT FRONT"); motor(30,190,"LEFT REAR")
motor(30,350,"RIGHT FRONT"); motor(30,430,"RIGHT REAR")

# ---------------- L298N ----------------
LX,LY,LW,LH=270,100,220,410
rect(LX,LY,LW,LH,"#fee2e2","#b91c1c",12)
text(LX+LW/2,LY+28,"L298N",20,"middle","800","#991b1b")
text(LX+LW/2,LY+46,"motor driver",11,"middle","400","#7f1d1d")
for nm,y in [("OUT1",140),("OUT2",160),("OUT3",380),("OUT4",400)]: pin(LX,y,nm,"l")
ctrl=[("ENA",200,C['ena']),("IN1",230,C['in1']),("IN2",260,C['in2']),("IN3",290,C['in3']),("IN4",320,C['in4']),("ENB",350,C['enb'])]
for nm,y,c in ctrl: pin(LX+LW,y,nm,"r",c)
for nm,x in [("+12V",300),("GND",360),("+5V",430)]: pin(x,LY+LH,nm,"b")
a(f'<rect x="{LX+86}" y="{LY+62}" width="120" height="44" rx="6" fill="#fff" stroke="#b91c1c" stroke-dasharray="4 3"/>')
text(LX+146,LY+80,"REMOVE ENA/ENB",10.5,"middle","800","#b91c1c"); text(LX+146,LY+96,"jumpers",10.5,"middle","700","#b91c1c")
text(430,LY+LH+26,"not used",10,"middle","400","#6b7280",True)

# motor wiring (left pair in parallel on OUT1/OUT2)
def motor_pair(yA,yB,y2A,y2B,outA,outB):
    line([(170,yA),(LX,outA)],C['m1']); line([(170,yB),(LX,outB)],C['m2'])
    line([(170,y2A),(210,y2A)],C['m1']); hop_v(210,y2A,outA,outB,C['m1']); dot(210,outA,C['m1'])
    line([(170,y2B),(235,y2B),(235,outB)],C['m2']); dot(235,outB,C['m2'])
    for yy in (yA,yB,y2A,y2B): a(f'<circle cx="170" cy="{yy}" r="3.5" fill="#92400e"/>')
motor_pair(140,160,220,240,140,160)
motor_pair(380,400,460,480,380,400)
text(100,280,"same-side motors",10.5,"middle","600","#92400e"); text(100,294,"in PARALLEL",10.5,"middle","800","#92400e")

# ---------------- ARDUINO UNO ----------------
UX,UY,UW,UH=650,170,250,350
rect(UX,UY,UW,UH,"#dbeafe","#1d4ed8",12)
text(UX+UW/2,UY+130,"ARDUINO",20,"middle","800","#1e3a8a")
text(UX+UW/2,UY+152,"UNO / NANO",16,"middle","700","#1e3a8a")
text(UX+UW/2,UY+172,"motors · sensor · alarm",11,"middle","400","#1e40af")
uno_l=[("D11 ~",200,C['ena']),("D10",230,C['in1']),("D9",260,C['in2']),("D8",290,C['in3']),("D7",320,C['in4']),("D6 ~",350,C['enb'])]
for nm,y,c in uno_l: pin(UX,y,nm,"l",c)
for (nm,y,c),(_,_,_) in zip(ctrl,uno_l): line([(LX+LW,y),(UX,y)],c)
for nm,y,c in ctrl: wlabel((LX+LW+UX)/2,y,f"{nm} → {dict(ENA='D11',IN1='D10',IN2='D9',IN3='D8',IN4='D7',ENB='D6')[nm]}",c)
pin(UX+UW,200,"D3 (RX)","r",C['tx']); pin(UX+UW,240,"D2 (TX)","r",C['rx'])
pin(UX+UW,488,"A4","r",C['head']); pin(UX,470,"VIN","l",C['bat'])
pin(UX+UW,420,"D13","r",C['trig']); pin(UX+UW,460,"D12","r",C['echo'])
for nm,x in [("A3",680),("A0",740),("A2",800),("5V",850),("GND",882)]: pin(x,UY+UH,nm,"b")

# ---------------- ESP32-CAM ----------------
EX,EY,EW,EH=1130,130,220,250
rect(EX,EY,EW,EH,"#dcfce7","#15803d",12)
text(EX+EW/2,EY+175,"ESP32-CAM",20,"middle","800","#14532d")
text(EX+EW/2,EY+195,"AI-Thinker + OV2640",11,"middle","400","#166534")
text(EX+EW/2,EY+211,"WiFi · camera · web app",11,"middle","400","#166534")
a(f'<rect x="{EX+EW/2+30}" y="{EY+20}" width="44" height="44" rx="6" fill="#111827"/><circle cx="{EX+EW/2+52}" cy="{EY+42}" r="12" fill="#374151" stroke="#9ca3af"/>')
pin(EX,200,"IO14 (TX)","l",C['tx']); pin(EX,240,"IO15 (RX)","l",C['rx'])
pin(EX+EW,300,"5V","r",C['v5']); pin(EX+EW,340,"GND","r")
text(EX+EW/2,EY+EH-14,"front of car, lens forward",10,"middle","400","#166534",True)

# UART
line([(UX+UW,200),(EX,200)],C['tx']); wlabel(1015,200,"IO14 → D3  (direct)",C['tx'])
line([(UX+UW,240),(935,240)],C['rx']); resistor_h(935,995,240,C['rx'],"R1 1 kΩ")
line([(995,240),(EX,240)],C['rx']); dot(1035,240,C['rx'])
resistor_v(1035,250,320,C['rx'],"R2 2 kΩ"); line([(1035,240),(1035,250)],C['rx']); line([(1035,320),(1035,330)],C['rx']); gnd_sym(1035,330)
wlabel(1080,262,"to IO15 (3.3 V)",C['rx'])
text(965,300,"voltage divider",10.5,"middle","700","#be185d"); text(965,314,"5 V → 3.3 V",10.5,"middle","400","#be185d")

# ---------------- HC-SR04 ----------------
HX,HY,HW,HH=1130,540,220,110
rect(HX,HY,HW,HH,"#e0f2fe","#0369a1",12)
for cx in (HX+100,HX+170):
    a(f'<circle cx="{cx}" cy="{HY+55}" r="22" fill="#cbd5e1" stroke="#475569" stroke-width="2"/><circle cx="{cx}" cy="{HY+55}" r="12" fill="#64748b"/>')
text(HX+HW/2,HY+20,"HC-SR04  (REAR, facing back)",12,"middle","800","#075985")
pin(HX,580,"TRIG","l",C['trig']); pin(HX,612,"ECHO","l",C['echo'])
pin(HX+40,HY+HH,"VCC","b",C['v5']); pin(HX+HW-40,HY+HH,"GND","b")
line([(UX+UW,420),(1070,420),(1070,580),(HX,580)],C['trig']); wlabel(985,420,"D13 → TRIG",C['trig'])
line([(UX+UW,460),(1050,460),(1050,612),(HX,612)],C['echo']); wlabel(985,460,"D12 ← ECHO",C['echo'])

# ---------------- BUZZER + LEDs ----------------
BY=UY+UH
GB_=740
line([(680,BY),(680,600)],C['buz'])
a(f'<circle cx="680" cy="628" r="26" fill="#111827"/><circle cx="680" cy="628" r="6" fill="#374151"/>')
text(680,606,"+",14,"middle","800","#fff"); text(640,628,"BUZZER",11,"end","700"); text(640,642,"5 V active",10,"end","400","#6b7280")
line([(680,654),(680,740)],C['gnd'])
line([(740,BY),(740,560)],C['led']); resistor_v(740,560,600,C['led'],"220 Ω",-50); line([(740,600),(740,620)],C['led'])
led(740,620,"#ef4444",""); text(726,648,"RED",10,"end","700","#dc2626"); line([(740,652),(740,740)],C['gnd'])
line([(800,BY),(800,560)],C['wled']); resistor_v(800,560,600,C['wled'],"220 Ω",12); line([(800,600),(800,620)],C['wled'])
led(800,620,"#f8fafc",""); text(812,672,"WHITE",10,"start","700","#475569"); text(812,686,"REV",10,"start","700","#475569"); line([(800,652),(800,740)],C['gnd'])

# headlights: A4 -> two branches, each 220 Ω + white LED
line([(UX+UW,488),(1015,488),(1015,520)],C['head']); dot(945,488,C['head']); line([(945,488),(945,520)],C['head'])
for hx in (945,1015):
    resistor_v(hx,520,560,C['head'],"220 Ω",-50 if hx==945 else -58); line([(hx,560),(hx,580)],C['head'])
    led(hx,580,"#f8fafc",""); line([(hx,612),(hx,GB_)],C['gnd']); dot(hx,GB_)
wlabel(980,672,"2 HEADLIGHTS (front)",C['head'])

# ---------------- POWER ----------------
# battery
rect(30,600,200,90,"#fef2f2","#991b1b",10)
for i in range(2):
    a(f'<rect x="{48+i*88}" y="625" width="78" height="40" rx="8" fill="#16a34a" stroke="#14532d" stroke-width="1.5"/>')
    text(87+i*88,650,"18650",11,"middle","800","#fff")
text(130,617,"2×18650 = 7.4 V (8.4 V full)",10.5,"middle","700","#7f1d1d")
pin(230,620,"+","r",C['bat']); pin(230,670,"−","r")
# switch
line([(230,620),(250,620)],C['bat']); a(f'<circle cx="252" cy="620" r="4" fill="#111827"/><circle cx="285" cy="620" r="4" fill="#111827"/>')
line([(254,618),(282,604)],"#111827",3); text(268,598,"SWITCH",10,"middle","800")
line([(287,620),(300,620)],C['bat'])
line([(300,620),(300,LY+LH)],C['bat']); dot(300,620,C['bat'])
# second wire from the L298N +12V terminal -> UNO VIN
dot(300,560,C['bat']); hop_h(300,620,560,360,C['bat']); line([(620,560),(620,470),(UX,470)],C['bat'])
wlabel(500,560,"7.4 V → UNO VIN",C['bat'])
# GND bus y=740 and 5V bus y=790
GB,VB=740,790
line([(230,670),(270,670),(270,GB)],C['gnd'])
line([(270,GB),(1385,GB)],C['gnd'],4)
line([(360,LY+LH),(360,GB)],C['gnd']); dot(360,GB)
for x in (680,740,800): dot(x,GB)
# 5 V bus starts at the UNO 5V pin
line([(850,VB),(1420,VB)],C['v5'],4)
rect(30,830,720,150,"#fff7ed","#ea580c",10,1.5)
text(50,856,"POWER — no buck converter needed",13,"start","800","#9a3412")
for i,tl in enumerate(["• Battery 7.4 V → switch → L298N +12V. A 2nd wire in the same +12V terminal → UNO VIN.",
                       "• The UNO regulator makes the 5 V: UNO 5V pin → 5 V bus (ESP32-CAM, HC-SR04, buzzer, LEDs).",
                       "• 2200 µF 16 V capacitor right at the ESP32-CAM 5V/GND pins (+ leg to 5V).",
                       "• L298N: keep the 5V-EN jumper ON, remove ENA/ENB jumpers, leave its +5V pin unused.",
                       "• Do not add a servo to this 5 V bus (the UNO regulator is too small for it)."]):
    text(50,880+i*20,tl,11.5,"start","400","#431407")
# UNO power
line([(882,BY),(882,GB)],C['gnd']); dot(882,GB)
hop_v(850,BY,VB,GB,C['v5']); dot(850,VB,C['v5']); wlabel(850,812,"UNO 5V",C['v5'])
# HC-SR04 power
line([(HX+HW-40,HY+HH),(HX+HW-40,GB)],C['gnd']); dot(HX+HW-40,GB)
hop_v(HX+40,HY+HH,VB,GB,C['v5']); dot(HX+40,VB,C['v5'])
# ESP power (right side, down)
line([(EX+EW,340),(1385,340),(1385,GB)],C['gnd']); dot(1385,GB)
line([(EX+EW,300),(1420,300),(1420,VB)],C['v5']); dot(1420,VB,C['v5'])
# capacitor between 1385 and 1420 at y 470
line([(1385,470),(1396,470)],C['gnd'],2.5); line([(1409,470),(1420,470)],C['v5'],2.5)
line([(1396,456),(1396,484)],"#111827",3); path("M1412,456 Q1405,470 1412,484","#111827",3)
dot(1385,470); dot(1420,470,C['v5'])
text(1376,466,"2200 µF",11,"end","800"); text(1376,480,"16 V",10,"end","400","#6b7280"); text(1435,462,"+",13,"start","800",C['v5'])
wlabel(1150,GB,"GND BUS (all grounds together)",C['gnd'])
wlabel(1000,VB,"+5 V BUS (from the UNO 5V pin)",C['v5'])

# ---------------- legend + notes ----------------
rect(770,830,690,150,"#f9fafb","#d1d5db",10,1.5)
text(790,864,"WIRE COLOURS",12,"start","800")
leg=[("Battery +7.4 V",C['bat']),("+5 V",C['v5']),("GND",C['gnd']),("Motor wires",C['m1']),("UART ESP→UNO",C['tx']),("UART UNO→ESP",C['rx']),
     ("TRIG",C['trig']),("ECHO",C['echo']),("Buzzer",C['buz']),("Headlights",C['head'])]
for i,(n,c) in enumerate(leg):
    x=790+(i%5)*134; y=888+(i//5)*22
    line([(x,y-4),(x+24,y-4)],c,4); text(x+30,y,n,11)
text(790,946,"• Wires crossing with a small hop are NOT connected. A black dot = connected.",11,"start","400","#374151")
text(790,964,"• ALL grounds must be common. Never feed 7.4 V into the ESP32-CAM or UNO 5V pin.",11,"start","700","#b91c1c")
a('</svg>')
open(sys.argv[1],"w").write("\n".join(o))
