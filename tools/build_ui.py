#!/usr/bin/env python3
"""
Embed the web pages into the ESP32-CAM firmware.

Run this every time you edit a file in web/:
    python3 tools/build_ui.py

    web/index.html  (phone driver app, served at  /     ) -> firmware/esp32cam_robot/index_html.h
    web/view.html   (PC classroom viewer, served at /view) -> firmware/esp32cam_robot/view_html.h
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FW = ROOT / "firmware" / "esp32cam_robot"
PAGES = [("index.html", "index_html.h", "INDEX_HTML"), ("view.html", "view_html.h", "VIEW_HTML")]
DELIM = "rawhtml"

for src, dst, name in PAGES:
    html = (ROOT / "web" / src).read_text(encoding="utf-8")
    # links between the two pages: "view.html" works from disk (demo), "view" on the car
    if src == "index.html":
        html = html.replace('$("viewLink").href = "view.html"; $("pcLink").href = "view.html";', "")
    if f'){DELIM}"' in html:
        raise SystemExit(f"{src} must not contain ){DELIM}\"")
    (FW / dst).write_text(
        "#pragma once\n"
        f"// AUTO-GENERATED from web/{src} by tools/build_ui.py - do not edit by hand\n"
        f'static const char {name}[] = R"{DELIM}(' + html + f'){DELIM}";\n',
        encoding="utf-8",
    )
    print(f"Wrote firmware/esp32cam_robot/{dst} ({len(html.encode('utf-8'))} bytes)")
