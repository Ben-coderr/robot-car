"""Shared design system (CSS + HTML helpers) for the robot-car PDF handbook."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "docs" / "images"


def img(name):
    return (IMG / name).as_uri()


CSS = r"""
@page { size: A4; margin: 15mm 15mm 17mm 15mm; }
* { box-sizing: border-box; }
:root{
  --navy:#0b1f3a; --ink:#0f172a; --muted:#475569; --soft:#64748b; --line:#e2e8f0; --bg:#f8fafc;
  --accent:#f97316; --accent-soft:#fff7ed; --teal:#0ea5e9; --teal-soft:#f0f9ff;
  --green:#16a34a; --green-soft:#f0fdf4; --red:#dc2626; --red-soft:#fef2f2; --violet:#7c3aed;
}
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ margin:0; font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif; font-size:9.6pt;
  line-height:1.5; color:var(--ink); }
h1,h2,h3,h4{ font-family:"Avenir Next","Helvetica Neue",sans-serif; color:var(--navy); margin:0; line-height:1.2; }
p{ margin:0 0 7pt; }
b,strong{ font-weight:700; }
code,.mono{ font-family:Menlo,Consolas,monospace; font-size:8.6pt; background:#f1f5f9; border:1px solid #e2e8f0;
  border-radius:4px; padding:0 4px; }
pre{ font-family:Menlo,Consolas,monospace; font-size:8.3pt; background:#0f172a; color:#e2e8f0; border-radius:8px;
  padding:9pt 11pt; margin:6pt 0 10pt; white-space:pre-wrap; line-height:1.45; break-inside:avoid; }
pre .c{ color:#94a3b8; } pre .k{ color:#fbbf24; } pre .s{ color:#86efac; }
a{ color:var(--teal); text-decoration:none; }
.pb{ break-before:page; }
.avoid{ break-inside:avoid; }
.muted{ color:var(--muted); }
.small{ font-size:8.4pt; }

/* ---------- section headers ---------- */
.sec{ display:flex; align-items:center; gap:10pt; margin:2pt 0 10pt; padding-bottom:7pt; border-bottom:2px solid var(--line); }
.sec .num{ width:26pt; height:26pt; border-radius:7pt; background:var(--accent); color:#fff; font-weight:800; font-size:12pt;
  display:flex; align-items:center; justify-content:center; flex:none; }
.sec h1{ font-size:19pt; font-weight:800; letter-spacing:-.01em; }
.sec .kicker{ font-size:7.5pt; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); font-weight:700; }
h2{ font-size:13pt; font-weight:800; margin:14pt 0 6pt; break-after:avoid; }
h3{ font-size:10.5pt; font-weight:700; margin:10pt 0 4pt; color:var(--ink); break-after:avoid; }

/* ---------- callouts ---------- */
.co{ display:flex; gap:9pt; border-radius:9pt; padding:8pt 11pt; margin:7pt 0 10pt; break-inside:avoid; border:1px solid; }
.co .ic{ width:18pt; height:18pt; flex:none; border-radius:50%; display:flex; align-items:center; justify-content:center;
  color:#fff; font-weight:800; font-size:10pt; margin-top:1pt; }
.co .bd{ flex:1; } .co .tt{ font-weight:800; margin-bottom:1pt; }
.co p:last-child, .co ul:last-child{ margin-bottom:0; }
.co.warn{ background:var(--red-soft); border-color:#fecaca; } .co.warn .ic{ background:var(--red); } .co.warn .tt{ color:#991b1b; }
.co.tip{ background:var(--teal-soft); border-color:#bae6fd; } .co.tip .ic{ background:var(--teal); } .co.tip .tt{ color:#075985; }
.co.note{ background:var(--accent-soft); border-color:#fed7aa; } .co.note .ic{ background:var(--accent); } .co.note .tt{ color:#9a3412; }
.co.ok{ background:var(--green-soft); border-color:#bbf7d0; } .co.ok .ic{ background:var(--green); } .co.ok .tt{ color:#166534; }

/* ---------- tables ---------- */
table{ width:100%; border-collapse:separate; border-spacing:0; margin:5pt 0 11pt; font-size:8.9pt; break-inside:auto; }
th{ background:var(--navy); color:#fff; text-align:left; font-weight:700; padding:5pt 7pt; font-size:8.3pt; letter-spacing:.02em; }
th:first-child{ border-top-left-radius:7pt; } th:last-child{ border-top-right-radius:7pt; }
td{ padding:4.6pt 7pt; border-bottom:1px solid var(--line); vertical-align:top; }
tr:nth-child(even) td{ background:#f8fafc; }
tr{ break-inside:avoid; }
.sw{ display:inline-block; width:18pt; height:6pt; border-radius:3pt; vertical-align:middle; margin-right:5pt; border:1px solid rgba(0,0,0,.15); }
.pin{ display:inline-block; font-family:Menlo,monospace; font-weight:700; font-size:8.2pt; padding:0 5pt; border-radius:4pt;
  background:#e0f2fe; color:#075985; }
.pin.u{ background:#ccfbf1; color:#115e59; } .pin.e{ background:#ede9fe; color:#5b21b6; } .pin.l{ background:#fee2e2; color:#991b1b; }
.box{ display:inline-block; width:10pt; height:10pt; border:1.5px solid var(--soft); border-radius:2.5pt; vertical-align:middle; }

/* ---------- figures ---------- */
figure{ margin:6pt 0 11pt; break-inside:avoid; }
figure img{ width:100%; display:block; border-radius:9pt; border:1px solid var(--line); background:#fff; }
figcaption{ font-size:8pt; color:var(--soft); margin-top:4pt; text-align:center; }

/* ---------- step blocks ---------- */
.step{ break-before:page; }
.step figure img{ max-height:96mm; width:auto; max-width:100%; margin:0 auto; }
.grid4{ display:grid; grid-template-columns:repeat(4,1fr); gap:7pt; }
.grid4 .part .ph{ height:60pt; } .grid4 .part .ph img{ max-height:54pt; }
.grid4 .part .sp{ font-size:7.6pt; } .grid4 .part .nm{ font-size:9pt; }
.keep{ break-inside:avoid; }
.step-h{ display:flex; align-items:center; gap:10pt; margin-bottom:8pt; }
.step-h .n{ width:34pt; height:34pt; border-radius:50%; background:var(--navy); color:#fff; font-weight:800; font-size:16pt;
  display:flex; align-items:center; justify-content:center; flex:none; border:3px solid var(--accent); }
.step-h h2{ margin:0; font-size:15pt; } .step-h .sub{ color:var(--muted); font-size:9pt; }
ol.do{ counter-reset:i; list-style:none; padding:0; margin:4pt 0 9pt; }
ol.do li{ counter-increment:i; position:relative; padding-left:22pt; margin-bottom:4.5pt; }
ol.do li:before{ content:counter(i); position:absolute; left:0; top:0; width:15pt; height:15pt; border-radius:50%;
  background:var(--accent-soft); border:1.5px solid var(--accent); color:#9a3412; font-weight:800; font-size:7.8pt;
  display:flex; align-items:center; justify-content:center; }
ul{ margin:3pt 0 8pt; padding-left:15pt; } li{ margin-bottom:2.5pt; }

/* ---------- cards ---------- */
.grid2{ display:grid; grid-template-columns:1fr 1fr; gap:9pt; }
.grid3{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:9pt; }
.card{ border:1px solid var(--line); border-radius:10pt; padding:9pt; break-inside:avoid; background:#fff; }
.part{ display:flex; flex-direction:column; }
.part .ph{ height:84pt; display:flex; align-items:center; justify-content:center; background:var(--bg); border-radius:7pt; margin-bottom:7pt; }
.part .ph img{ max-height:76pt; max-width:92%; }
.part .nm{ font-weight:800; font-size:10pt; color:var(--navy); }
.part .sp{ font-size:8.2pt; color:var(--muted); margin:2pt 0 5pt; flex:1; }
.part .meta{ display:flex; justify-content:space-between; font-size:8pt; font-weight:700; }
.part .qty{ background:var(--navy); color:#fff; border-radius:99pt; padding:1pt 7pt; }
.part .pr{ color:var(--accent); }
.feat{ display:flex; gap:8pt; align-items:flex-start; }
.feat .fi{ width:26pt; height:26pt; border-radius:8pt; background:var(--accent-soft); color:var(--accent); flex:none;
  display:flex; align-items:center; justify-content:center; font-size:13pt; }
.feat .ft{ font-weight:800; color:var(--navy); } .feat .fd{ font-size:8.4pt; color:var(--muted); }
.obj{ background:var(--navy); color:#e2e8f0; border-radius:12pt; padding:12pt 14pt; margin:4pt 0 12pt; break-inside:avoid; }
.obj h3{ color:#fff; margin:0 0 5pt; font-size:10.5pt; } .obj ul{ margin:0; } .obj li{ margin-bottom:2pt; }
.obj .tag{ color:var(--accent); font-size:7.5pt; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
.kv{ display:grid; grid-template-columns:auto 1fr; gap:3pt 10pt; font-size:9pt; }
.check li{ list-style:none; margin-left:-15pt; padding-left:18pt; position:relative; margin-bottom:5pt; }
.check li:before{ content:""; position:absolute; left:0; top:1.5pt; width:10pt; height:10pt; border:1.5px solid var(--soft); border-radius:2.5pt; }
.sig{ display:flex; gap:12pt; margin-top:14pt; } .sig div{ flex:1; border-top:1px solid var(--soft); padding-top:3pt; font-size:8pt; color:var(--soft); }
.badge{ display:inline-block; font-size:7.4pt; font-weight:800; letter-spacing:.06em; padding:1pt 6pt; border-radius:99pt; background:#e2e8f0; color:#334155; }
.badge.req{ background:#fee2e2; color:#991b1b; } .badge.opt{ background:#e0f2fe; color:#075985; }
.shot{ position:relative; }
.shot .dot{ position:absolute; width:17pt; height:17pt; border-radius:50%; background:var(--accent); color:#fff; font-weight:800;
  font-size:8.5pt; display:flex; align-items:center; justify-content:center; border:2px solid #fff; box-shadow:0 1px 4px rgba(0,0,0,.35); }

/* ---------- cover ---------- */
.cover{ width:210mm; height:297mm; position:relative; overflow:hidden; background:var(--navy); color:#fff;
  background-image:linear-gradient(rgba(255,255,255,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.045) 1px, transparent 1px);
  background-size:9mm 9mm; padding:20mm 18mm; display:flex; flex-direction:column; }
.cover .brand{ display:flex; align-items:center; gap:8pt; font-weight:800; letter-spacing:.2em; font-size:9pt; color:#cbd5e1; }
.cover .brand i{ width:9pt; height:9pt; border-radius:50%; background:var(--accent); display:inline-block; }
.cover .mod{ margin-top:22mm; font-size:10pt; letter-spacing:.24em; color:var(--accent); font-weight:800; }
.cover .big{ font-size:96pt; font-weight:800; line-height:.9; color:transparent; -webkit-text-stroke:1.6px rgba(255,255,255,.35); margin-top:4mm; }
.cover h1{ color:#fff; font-size:38pt; font-weight:800; letter-spacing:-.02em; margin-top:2mm; line-height:1.05; }
.cover .subt{ color:#cbd5e1; font-size:13pt; margin-top:5mm; max-width:150mm; line-height:1.4; }
.cover .hero{ margin-top:auto; background:#fff; border-radius:14pt; padding:8pt; box-shadow:0 18px 40px rgba(0,0,0,.35); }
.cover .hero img{ width:100%; display:block; border-radius:9pt; max-height:112mm; object-fit:contain; }
.cover .foot{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:9mm; gap:10mm; }
.cover .foot .who{ display:flex; gap:6mm; flex:1; }
.cover .foot .who div{ flex:1; border-bottom:1px solid rgba(255,255,255,.4); font-size:8pt; color:#94a3b8; padding-bottom:12pt; }
.cover .foot .ed{ font-size:8pt; color:#94a3b8; text-align:right; white-space:nowrap; }
.collage{ display:grid; grid-template-columns:repeat(4,1fr); gap:6pt; padding:6pt; }
.collage div{ background:#f8fafc; border-radius:8pt; height:42mm; display:flex; align-items:center; justify-content:center; }
.collage img{ max-width:88%; max-height:36mm; border:none !important; }
.toc{ counter-reset:t; } .toc .row{ display:flex; align-items:baseline; gap:8pt; padding:9pt 0; border-bottom:1px solid var(--line); }
.toc .row .k{ font-weight:800; color:var(--accent); width:30pt; font-size:13pt; } .toc .row .t{ font-weight:800; font-size:12pt; color:var(--navy); }
.toc .row .d{ color:var(--muted); font-size:9pt; flex:1; }
"""

ICON = {"warn": "!", "tip": "i", "note": "★", "ok": "✓"}


def co(kind, title, body):
    return (f'<div class="co {kind}"><div class="ic">{ICON[kind]}</div><div class="bd">'
            f'<div class="tt">{title}</div>{body}</div></div>')


def table(headers, rows, widths=None):
    cols = ""
    if widths:
        cols = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>"
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>{cols}<thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"


def sw(color):
    return f'<span class="sw" style="background:{color}"></span>'


def pin(p, kind=""):
    return f'<span class="pin {kind}">{p}</span>'


def sec(n, kicker, title):
    return f'<div class="sec"><div class="num">{n}</div><div><div class="kicker">{kicker}</div><h1>{title}</h1></div></div>'


def fig(src, caption="", style=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><img src="{src}" style="{style}">{cap}</figure>'


def steps(items):
    return '<ol class="do">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def bullets(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def objectives(items, minutes=None):
    t = f' · about {minutes} min' if minutes else ""
    return (f'<div class="obj"><div class="tag">Learning objectives{t}</div><h3>By the end of this module you can:</h3>'
            + bullets(items) + "</div>")


def cover(module, title, subtitle, hero_html, edition="Edition 2026"):
    num = module if module.isdigit() else ""
    return f"""
<div class="cover">
  <div class="brand"><i></i>ROBOT CAR PROJECT</div>
  <div class="mod">{'MODULE ' + module if num else module}</div>
  <div class="big">{num}</div>
  <h1>{title}</h1>
  <div class="subt">{subtitle}</div>
  <div class="hero">{hero_html}</div>
  <div class="foot">
    <div class="who"><div>Name</div><div>Class / Group</div><div>Date</div></div>
    <div class="ed">4WD · Arduino UNO · ESP32-CAM<br>{edition}</div>
  </div>
</div>"""


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


def footer(text):
    return (f'<div style="font-family:Avenir Next,Helvetica,sans-serif;font-size:7.5px;width:100%;padding:0 15mm;'
            f'display:flex;justify-content:space-between;color:#64748b;">'
            f'<span><b style="color:#f97316">●</b>&nbsp; Robot Car Project · {text}</span>'
            f'<span>Page <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
