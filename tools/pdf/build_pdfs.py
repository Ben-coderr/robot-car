#!/usr/bin/env python3
"""
Builds the student handbook PDFs into docs/pdf/.

    python3 tools/diagrams/make_diagrams.py     # (re)draw the diagrams first
    python3 tools/pdf/build_pdfs.py

Needs:  pip install playwright pypdf   and   playwright install chromium   (or Google Chrome)
"""
import asyncio, io, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from design import CSS, ROOT, cover, footer, img, page  # noqa: E402
from content import MODULES                              # noqa: E402
from playwright.async_api import async_playwright        # noqa: E402
from pypdf import PdfReader, PdfWriter                   # noqa: E402

OUT = ROOT / "docs" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(tempfile.mkdtemp(prefix="robotcar_pdf_"))


async def to_pdf(browser, html, name, fmt="A4", landscape=False, foot=None, margin=True):
    f = TMP / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    pg = await browser.new_page()
    await pg.goto(f.as_uri(), wait_until="networkidle")
    await pg.evaluate("document.fonts.ready")
    opts = dict(format=fmt, landscape=landscape, print_background=True, prefer_css_page_size=False)
    if margin:
        opts["margin"] = dict(top="15mm", bottom="17mm", left="15mm", right="15mm")
    else:
        opts["margin"] = dict(top="0", bottom="0", left="0", right="0")
    if foot:
        opts.update(display_header_footer=True, header_template="<div></div>", footer_template=foot)
    data = await pg.pdf(**opts)
    await pg.close()
    return data


def merge(parts, meta_title):
    w = PdfWriter()
    for p in parts:
        for pg in PdfReader(io.BytesIO(p)).pages:
            w.add_page(pg)
    w.add_metadata({"/Title": meta_title, "/Author": "Robot Car Project", "/Subject": "Student handbook"})
    buf = io.BytesIO()
    w.write(buf)
    return buf.getvalue()


COVER_CSS_FIX = "<style>@page{margin:0}</style>"


async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="chrome")
        except Exception:
            browser = await p.chromium.launch()
        all_parts = []
        toc_rows = []
        for fn in MODULES:
            m = fn()
            cov = await to_pdf(browser, page(cover(m["module"], m["title"], m["subtitle"], m["hero"])) .replace("</head>", COVER_CSS_FIX + "</head>"),
                               f"cover_{m['module']}", margin=False)
            body = await to_pdf(browser, page(m["body"]), f"body_{m['module']}", foot=footer(m["footer"]))
            pdf = merge([cov, body], f"Robot Car · {m['title'].replace('&amp;', '&')}")
            (OUT / m["file"]).write_bytes(pdf)
            all_parts.append(pdf)
            toc_rows.append((m["module"], m["title"], m["subtitle"], len(PdfReader(io.BytesIO(pdf)).pages)))
            print(f"  ✓ {m['file']}  ({toc_rows[-1][3]} pages)")

        # ---------------- handbook: cover + contents + all modules ----------
        hb_cover = page(cover("STUDENT HANDBOOK", "Phone-Controlled Robot Car",
                              "Build a 4WD car with live video, a rear parking radar and auto-brake: parts, wiring, assembly, code and tests.",
                              f'<img src="{img("wiring_full.svg")}">')).replace("</head>", COVER_CSS_FIX + "</head>")
        start, rows = 3, ""
        for mod, title, sub, n in toc_rows:
            rows += (f'<div class="row"><span class="k">{mod}</span><span><span class="t">{title}</span><br><span class="d">{sub}</span></span>'
                     f'<span style="margin-left:auto;font-weight:700;color:#475569">p. {start}</span></div>')
            start += n
        toc = page(f"""
<div class="sec"><div class="num">☰</div><div><div class="kicker">Student handbook</div><h1>Contents</h1></div></div>
<div class="toc">{rows}</div>
<div class="co tip" style="margin-top:16pt"><div class="ic">i</div><div class="bd"><div class="tt">How to use this handbook</div>
<p>Work through the modules in order: <b>01</b> parts → <b>03</b> assembly → <b>02</b> wiring → <b>04</b> software → <b>05</b> tests.
Start with Module <b>07</b> (warm-up lessons on the Learn Arduino website) if you are new to Arduino. Module <b>06</b> is a reference for reports and improvements. Each module ends with a checklist that your teacher can sign.</p></div></div>
<div class="co note"><div class="ic">★</div><div class="bd"><div class="tt">Also in this folder</div>
<p><b>Robot_Car_Wiring_Poster.pdf</b>: A3 poster of the complete wiring (realistic + schematic) for the lab wall.</p></div></div>""")
        hb_c = await to_pdf(browser, hb_cover, "hb_cover", margin=False)
        hb_t = await to_pdf(browser, toc, "hb_toc", foot=footer("Student Handbook"))
        (OUT / "00_Robot_Car_Complete_Handbook.pdf").write_bytes(merge([hb_c, hb_t] + all_parts, "Robot Car · Complete Student Handbook"))
        print("  ✓ 00_Robot_Car_Complete_Handbook.pdf")

        # ---------------- A3 poster -----------------------------------------
        poster = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
@page{{size:A3 landscape;margin:0}} body{{margin:0}}
.pp{{width:420mm;height:297mm;padding:12mm 14mm;display:flex;flex-direction:column;break-after:page}}
.pp .hd{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #f97316;padding-bottom:4mm;margin-bottom:4mm}}
.pp h1{{font-size:28pt}} .pp .k{{font-size:9pt;letter-spacing:.2em;color:#f97316;font-weight:800}}
.pp .im{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}} .pp .im img{{max-width:100%;max-height:100%}}
.pp .ft{{display:flex;gap:6mm;margin-top:3mm;font-size:9pt}} .pp .ft div{{flex:1;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8pt;padding:3mm 4mm}}
</style></head><body>
<div class="pp"><div class="hd"><div><div class="k">ROBOT CAR PROJECT · WIRING POSTER</div><h1>Complete wiring: realistic view</h1></div>
<div class="small muted">L298N ENA–ENB → D11–D6 · TRIG D13 · ECHO D12 · LEDs A0/A2 · buzzer A3 · headlights A4 · IO14→D3 · D2→1k→IO15 (2k to GND)</div></div>
<div class="im"><img src="{img('wiring_full.svg')}"></div>
<div class="ft"><div><b style="color:#dc2626">⚠ Power:</b> battery 7.4 V → switch → L298N +12V, and a 2nd wire from that terminal → UNO VIN. The UNO 5V pin feeds the 5 V rail. 2200 µF at the ESP32-CAM.</div>
<div><b>Remove the ENA/ENB jumpers</b> on the L298N. Keep the 5V-EN jumper.</div><div><b>All GNDs common.</b> 7.4 V only to L298N +12V and UNO VIN, never to a 5V pin.</div></div></div>
<div class="pp"><div class="hd"><div><div class="k">ROBOT CAR PROJECT · WIRING POSTER</div><h1>Complete wiring: schematic view</h1></div></div>
<div class="im"><img src="{img('schematic.svg')}"></div></div>
</body></html>"""
        (OUT / "Robot_Car_Wiring_Poster.pdf").write_bytes(await to_pdf(browser, poster, "poster", fmt="A3", landscape=True, margin=False))
        print("  ✓ Robot_Car_Wiring_Poster.pdf")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
    print("PDFs written to", OUT)
