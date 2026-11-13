#pragma once
// AUTO-GENERATED from web/view.html by tools/build_ui.py - do not edit by hand
static const char VIEW_HTML[] = R"rawhtml(<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff" id="metaThemeColor">
<title>Rover Mission Control &amp; Telemetry Viewer</title>
<style>
:root {
  --font: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;

  /* LIGHT THEME (Clean Architecture White) */
  --bg: #f8fafc;
  --bg-subtle: #f1f5f9;
  --panel: #ffffff;
  --panel-subtle: #f8fafc;
  --panel-active: #f1f5f9;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --text: #0f172a;
  --text-muted: #64748b;
  --text-dim: #94a3b8;

  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-subtle: #eff6ff;
  --accent-border: #bfdbfe;
  --accent-glow: rgba(37, 99, 235, 0.15);

  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px -2px rgba(0,0,0,0.04);
  --shadow-lg: 0 12px 28px -6px rgba(0,0,0,0.08);
}

[data-theme="dark"] {
  /* OBSIDIAN STEALTH DARK THEME */
  --bg: #090a0f;
  --bg-subtle: #0f131c;
  --panel: #131722;
  --panel-subtle: #181d2b;
  --panel-active: #222a3d;
  --border: #232b3e;
  --border-strong: #333d56;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;

  --accent: #06b6d4;
  --accent-hover: #0891b2;
  --accent-subtle: rgba(6, 182, 212, 0.12);
  --accent-border: rgba(6, 182, 212, 0.35);
  --accent-glow: rgba(6, 182, 212, 0.3);

  --success: #10b981;
  --warning: #f59e0b;
  --danger: #f43f5e;

  --shadow-sm: 0 2px 4px rgba(0,0,0,0.4);
  --shadow-md: 0 6px 18px rgba(0,0,0,0.5);
  --shadow-lg: 0 16px 36px rgba(0,0,0,0.6);
}

* { box-sizing: border-box; }
html, body {
  margin: 0; min-height: 100%; background: var(--bg); color: var(--text);
  font-family: var(--font); font-size: 14px; line-height: 1.4;
  transition: background-color .25s ease, color .25s ease;
}
body { display: flex; flex-direction: column; min-height: 100vh; }
button { font: inherit; color: inherit; cursor: pointer; border: 0; outline: none; }
svg.icon { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; flex: none; }
.hidden { display: none !important; }

/* ---------------- Mission Control Header ---------------- */
header {
  display: flex; align-items: center; gap: 14px; padding: 14px 24px;
  background: var(--panel); border-bottom: 1px solid var(--border); box-shadow: var(--shadow-sm);
}
.brand { display: flex; align-items: center; gap: 12px; }
.brand-badge {
  width: 38px; height: 38px; border-radius: var(--radius-sm);
  background: linear-gradient(135deg, var(--accent), #4f46e5); color: #fff;
  display: grid; place-items: center; box-shadow: 0 2px 8px var(--accent-glow);
}
.brand h1 { margin: 0; font-size: 16px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }
.brand small { display: block; color: var(--text-muted); font-size: 11px; font-weight: 600; letter-spacing: .08em; }

.chips { display: flex; gap: 8px; flex-wrap: wrap; margin-left: auto; align-items: center; }
.chip {
  display: inline-flex; align-items: center; gap: 7px; padding: 6px 12px;
  border-radius: var(--radius-full); background: var(--panel-subtle); border: 1px solid var(--border);
  font-size: 11px; font-weight: 700; font-family: var(--mono); color: var(--text-muted); white-space: nowrap;
}
.chip .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--text-dim); }
.chip.ok .dot { background: var(--success); box-shadow: 0 0 6px var(--success); }
.chip.bad .dot { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
.chip.warn .dot { background: var(--warning); box-shadow: 0 0 6px var(--warning); }
.chip b { color: var(--text); }

.clock {
  font-family: var(--mono); font-weight: 800; font-size: 14px;
  color: var(--text-muted); min-width: 80px; text-align: right;
}
.btn-icon {
  width: 38px; height: 38px; border-radius: var(--radius-md); background: var(--panel-subtle);
  border: 1px solid var(--border); color: var(--text-muted); display: grid; place-items: center;
  transition: all .15s;
}
.btn-icon:hover { color: var(--text); border-color: var(--border-strong); background: var(--panel-active); }

/* ---------------- Main Control Grid ---------------- */
main {
  display: grid; gap: 14px; padding: 16px 24px 24px;
  grid-template-columns: minmax(0, 1.85fr) minmax(350px, 1fr);
  grid-template-areas: "video side" "chart log";
  flex: 1;
}
@media (max-width: 1024px) {
  main { grid-template-columns: 1fr; grid-template-areas: "video" "side" "chart" "log"; }
}

.card {
  background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm); display: flex; flex-direction: column; overflow: hidden; min-width: 0; min-height: 0;
}
.card-header {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding: 12px 16px 8px; font-size: 11px; font-weight: 800; letter-spacing: .12em;
  text-transform: uppercase; color: var(--text-muted); background: var(--panel-subtle);
  border-bottom: 1px solid var(--border);
}
.card-header b {
  font-family: var(--mono); color: var(--text); font-size: 12px; font-weight: 700;
  text-transform: none; letter-spacing: 0;
}

/* ---------------- Optical Stream Viewport ---------------- */
.video { grid-area: video; }
.viewport {
  position: relative; flex: 1; min-height: 340px; margin: 12px; border-radius: var(--radius-md);
  overflow: hidden; background: #000; box-shadow: inset 0 0 30px rgba(0,0,0,0.6);
}
.viewport img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; }

.no-video-overlay {
  position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 10px; text-align: center; color: var(--text-dim); background: var(--panel-subtle);
}
.no-video-overlay svg { width: 56px; height: 56px; opacity: .5; color: var(--text-muted); }
.no-video-overlay p { margin: 0; font-size: 14px; font-weight: 700; color: var(--text-muted); }
.no-video-overlay small { font-size: 11px; color: var(--text-dim); max-width: 360px; line-height: 1.4; }

.viewport-hud {
  position: absolute; inset: 0; pointer-events: none; border: 2px solid transparent;
  border-radius: var(--radius-md);
}
.viewport-hud.alarm { border-color: var(--warning); box-shadow: inset 0 0 40px rgba(245,158,11,0.4); }
.viewport-hud.danger { border-color: var(--danger); box-shadow: inset 0 0 60px rgba(239,68,68,0.6); }

.hud-top-left { position: absolute; top: 14px; left: 14px; display: flex; gap: 8px; }
.hud-top-right { position: absolute; top: 14px; right: 14px; display: flex; gap: 8px; }
.hud-tag {
  padding: 5px 10px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 800;
  font-family: var(--mono); letter-spacing: .08em; background: rgba(0,0,0,0.7); color: #fff;
  backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.15);
}
.hud-tag.rev { background: var(--warning); color: #1a1200; border-color: var(--warning); }
.hud-tag.brake { background: var(--danger); color: #fff; border-color: var(--danger); }
.hud-tag.rec { background: #dc2626; color: #fff; border-color: #dc2626; }
.hud-tag.rec::before {
  content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  background: #fff; margin-right: 6px; animation: blink 1s infinite steps(1);
}
@keyframes blink { 50% { opacity: 0; } }

.tactical-dist {
  position: absolute; left: 14px; bottom: 14px; padding: 10px 18px; border-radius: var(--radius-md);
  background: rgba(0,0,0,0.7); backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.2);
}
.tactical-dist .val { font-family: var(--mono); font-size: 38px; font-weight: 900; line-height: 1; color: #fff; }
.tactical-dist .val small { font-size: 14px; color: var(--text-dim); margin-left: 3px; }
.tactical-dist .sub { font-size: 10px; font-weight: 800; font-family: var(--mono); letter-spacing: .12em; color: var(--text-dim); margin-top: 4px; }

.viewport-toolbar { display: flex; gap: 10px; padding: 0 12px 12px; flex-wrap: wrap; }
.btn-control {
  height: 38px; padding: 0 14px; border-radius: var(--radius-md); background: var(--panel-subtle);
  border: 1px solid var(--border); font-size: 12px; font-weight: 700; color: var(--text-muted);
  display: inline-flex; align-items: center; gap: 8px; transition: all .15s;
}
.btn-control:hover { color: var(--text); border-color: var(--border-strong); background: var(--panel-active); }
.btn-control.active { background: var(--accent-subtle); color: var(--accent); border-color: var(--accent-border); }
.btn-control.rec.active { background: #dc2626; color: #fff; border-color: #dc2626; }
.btn-control.right { margin-left: auto; }

/* ---------------- Side Panel: Sonar & Chassis Status ---------------- */
.side { grid-area: side; display: flex; flex-direction: column; gap: 14px; min-height: 0; }
.radar-wrap { position: relative; flex: 1; min-height: 140px; }
#radar { position: absolute; inset: 0; width: 100%; height: 100%; }

.sonar-readout {
  display: flex; align-items: center; justify-content: space-between; padding: 8px 16px 12px;
  border-bottom: 1px solid var(--border);
}
.sonar-readout .dist-num { font-family: var(--mono); font-size: 30px; font-weight: 800; }
.sonar-readout .dist-num small { font-size: 13px; color: var(--text-muted); margin-left: 3px; }
.sonar-readout .zone-tag {
  padding: 5px 12px; border-radius: var(--radius-full); font-size: 11px; font-weight: 800;
  font-family: var(--mono); letter-spacing: .08em; background: var(--panel-subtle); color: var(--text-muted);
}

.chassis-telemetry { display: grid; grid-template-columns: 100px 1fr; gap: 14px; padding: 12px 16px; align-items: center; }
.carsvg { width: 100px; height: auto; }
.chassis-stats { display: grid; gap: 8px; }
.chassis-row { display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 600; color: var(--text-muted); }
.chassis-row b { font-family: var(--mono); color: var(--text); font-size: 12px; }
.stat-bar { height: 6px; border-radius: 3px; background: var(--border); position: relative; overflow: hidden; margin-top: 3px; }
.stat-bar span { position: absolute; top: 0; bottom: 0; left: 50%; background: var(--accent); border-radius: 3px; }
.badge {
  padding: 3px 8px; border-radius: var(--radius-full); font-size: 10px; font-weight: 800;
  font-family: var(--mono); background: var(--panel-subtle); color: var(--text-muted); border: 1px solid var(--border);
}
.badge.on { background: #fef08a; color: #1a1200; border-color: #facc15; }
.badge.warn { background: var(--warning); color: #fff; border-color: var(--warning); }
.badge.red { background: var(--danger); color: #fff; border-color: var(--danger); }
.badge.ok { background: #ecfdf5; color: #047857; border-color: #a7f3d0; }

/* ---------------- Chart & Events Log ---------------- */
.chart { grid-area: chart; }
.chart .chart-wrap { position: relative; flex: 1; min-height: 180px; margin: 8px 16px 16px; }
#chart { position: absolute; inset: 0; width: 100%; height: 100%; }

.log { grid-area: log; }
.events-list {
  list-style: none; margin: 0; padding: 8px 16px 16px; overflow-y: auto; flex: 1; min-height: 180px;
}
.events-list li {
  display: flex; gap: 10px; align-items: baseline; padding: 6px 0; border-bottom: 1px solid var(--border); font-size: 12px;
}
.events-list time { color: var(--text-muted); font-family: var(--mono); font-size: 11px; flex: none; }
.events-list .dot { width: 7px; height: 7px; border-radius: 50%; flex: none; transform: translateY(-1px); }

/* ---------------- Mission Controls Drawer ---------------- */
details.mission-ctrl {
  margin: 0 24px 24px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
details.mission-ctrl summary {
  padding: 14px 20px; cursor: pointer; font-weight: 800; list-style: none; display: flex; align-items: center; gap: 10px;
  font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--text-muted);
}
details.mission-ctrl summary::-webkit-details-marker { display: none; }
details.mission-ctrl summary span { color: var(--text-dim); font-weight: 600; font-size: 12px; text-transform: none; }
.ctrl-actions { display: flex; flex-wrap: wrap; gap: 10px; padding: 0 20px 18px; align-items: center; }

kbd { background: var(--panel-subtle); border: 1px solid var(--border-strong); border-radius: 4px; padding: 2px 6px; font-family: var(--mono); font-size: 11px; }
select { background: var(--panel-subtle); border: 1px solid var(--border); color: var(--text); border-radius: var(--radius-sm); padding: 6px 10px; font-size: 12px; }

.toast {
  position: fixed; left: 50%; bottom: 24px; transform: translate(-50%, 15px);
  background: var(--panel); border: 1px solid var(--border); padding: 10px 18px; border-radius: var(--radius-full);
  font-weight: 700; font-family: var(--mono); font-size: 12px; box-shadow: var(--shadow-lg); opacity: 0; pointer-events: none;
  transition: all .2s cubic-bezier(0.16, 1, 0.3, 1); z-index: 50;
}
.toast.show { opacity: 1; transform: translate(-50%, 0); }
</style>
</head>
<body>

<header>
  <div class="brand">
    <div class="brand-badge">
      <svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
    </div>
    <div>
      <h1>Rover Mission Control</h1>
      <small>TELEMETRY CONSOLE &amp; CLASSROOM VIEWER</small>
    </div>
  </div>

  <div class="chips">
    <span class="chip bad" id="chWs"><span class="dot"></span><span>OFFLINE</span></span>
    <span class="chip" id="chCar"><span class="dot"></span><span>MCU STANDBY</span></span>
    <span class="chip" id="chDev"><span class="dot"></span><span>0 PILOTS</span></span>
    <span class="chip hidden" id="chRssi"><span class="dot"></span><span></span></span>
  </div>

  <div class="clock" id="clock">--:--:--</div>

  <button class="btn-icon" id="btnTheme" title="Toggle Theme (White / Dark)">
    <svg class="icon" id="iconSun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    <svg class="icon hidden" id="iconMoon" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
  </button>
  <button class="btn-icon" id="btnFull" title="Full Screen Console">
    <svg class="icon" viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
  </button>
</header>

<main>
  <!-- OPTICAL SENSOR FEED (CAMERA) -->
  <section class="card video">
    <div class="card-header">
      <span>Optical Stream</span>
      <b id="vidInfo">LIVE FEED · 25 FPS</b>
    </div>
    <div class="viewport" id="screen">
      <div class="no-video-overlay" id="novideo">
        <svg class="icon" viewBox="0 0 24 24"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
        <p id="novTxt">INITIALIZING STREAM FEED&hellip;</p>
      </div>
      <img id="cam" alt="" crossorigin="anonymous">

      <div class="viewport-hud" id="hud">
        <div class="hud-top-left">
          <span class="hud-tag rev hidden" id="tagRev">REVERSE VECTOR</span>
          <span class="hud-tag brake hidden" id="tagBrk">COLLISION BRAKE</span>
        </div>
        <div class="hud-top-right">
          <span class="hud-tag rec hidden" id="tagRec">REC 00:00</span>
          <span class="hud-tag lights hidden" id="tagLt">BEAMS ACTIVE</span>
          <span class="hud-tag hidden" id="tagDemo">SIMULATION</span>
        </div>
        <div class="tactical-dist">
          <div class="val" id="bdN">--<small>cm</small></div>
          <div class="sub" id="bdZ">REAR SONAR HORIZON</div>
        </div>
      </div>
    </div>

    <div class="viewport-toolbar">
      <button class="btn-control" id="btnSnap">
        <svg class="icon" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        Save Frame
      </button>
      <button class="btn-control rec" id="btnRec">
        <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="6"/></svg>
        <span>Record Video</span>
      </button>
      <button class="btn-control" id="btnPause">
        <svg class="icon" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
        <span>Freeze</span>
      </button>
      <button class="btn-control right" id="btnVidFull">
        <svg class="icon" viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
        Expand Viewport
      </button>
    </div>
  </section>

  <!-- SIDE PANEL: SPATIAL SONAR + CHASSIS VECTOR -->
  <div class="side">
    <section class="card">
      <div class="card-header">
        <span>Spatial Sonar Radar</span>
        <b id="radarMode">FIXED AZIMUTH</b>
      </div>
      <div class="radar-wrap">
        <canvas id="radar"></canvas>
      </div>
      <div class="sonar-readout">
        <div class="dist-num" id="distNum">--<small>cm</small></div>
        <div class="zone-tag" id="zone">NO TARGET</div>
      </div>
    </section>

    <section class="card" style="flex:none">
      <div class="card-header">
        <span>Chassis Dynamics</span>
        <b id="motion">STOPPED</b>
      </div>
      <div class="chassis-telemetry">
        <svg class="carsvg" viewBox="0 0 150 200" id="carSvg">
          <defs><radialGradient id="beam" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#fde047" stop-opacity=".75"/><stop offset="1" stop-color="#fde047" stop-opacity="0"/></radialGradient></defs>
          <g id="beams" opacity="0"><path d="M35 34 L5 -10 L65 -10 Z" fill="url(#beam)"/><path d="M115 34 L85 -10 L145 -10 Z" fill="url(#beam)"/></g>
          <rect x="22" y="40" width="14" height="34" rx="4" fill="#0b0f14" stroke="#334155"/><rect x="114" y="40" width="14" height="34" rx="4" fill="#0b0f14" stroke="#334155"/>
          <rect x="22" y="126" width="14" height="34" rx="4" fill="#0b0f14" stroke="#334155"/><rect x="114" y="126" width="14" height="34" rx="4" fill="#0b0f14" stroke="#334155"/>
          <rect x="34" y="28" width="82" height="146" rx="18" fill="var(--panel-subtle)" stroke="var(--border-strong)" stroke-width="2"/>
          <rect x="50" y="42" width="50" height="22" rx="6" fill="var(--panel)" stroke="var(--accent)" stroke-opacity=".5"/>
          <circle cx="75" cy="53" r="5" fill="var(--accent)" opacity=".7"/>
          <circle id="hlL" cx="44" cy="34" r="6" fill="#334155"/><circle id="hlR" cx="106" cy="34" r="6" fill="#334155"/>
          <circle id="tlL" cx="46" cy="168" r="5" fill="#3f1d24"/><circle id="tlR" cx="104" cy="168" r="5" fill="#3f1d24"/>
          <rect id="rvL" x="64" y="166" width="22" height="5" rx="2" fill="#1f2937"/>
          <path id="arL" d="M29 100 l-7 9 h14 z" fill="var(--accent)" opacity="0"/><path id="arR" d="M121 100 l-7 9 h14 z" fill="var(--accent)" opacity="0"/>
          <text x="75" y="118" text-anchor="middle" fill="var(--text-muted)" font-size="9" font-weight="800" font-family="var(--mono)" letter-spacing="1">FRONT ▲</text>
        </svg>
        <div class="chassis-stats">
          <div>
            <div class="chassis-row"><span>Port Propulsion</span><b id="lV">0%</b></div>
            <div class="stat-bar"><span id="lB"></span></div>
          </div>
          <div>
            <div class="chassis-row"><span>Stbd Propulsion</span><b id="rV">0%</b></div>
            <div class="stat-bar"><span id="rB"></span></div>
          </div>
          <div class="chassis-row"><span>Headlights</span><span class="badge" id="bLt">OFF</span></div>
          <div class="chassis-row"><span>Radar Audio</span><span class="badge" id="bAl">QUIET</span></div>
          <div class="chassis-row"><span>Acoustic Horn</span><span class="badge" id="bHn">OFF</span></div>
        </div>
      </div>
    </section>
  </div>

  <!-- SPATIAL OBSTACLE GRAPH (LAST 60s) -->
  <section class="card chart">
    <div class="card-header">
      <span>Obstacle Distance Trajectory · Last 60s</span>
      <b id="chartInfo"></b>
    </div>
    <div class="chart-wrap"><canvas id="chart"></canvas></div>
  </section>

  <!-- TELEMETRY EVENT LOG -->
  <section class="card log">
    <div class="card-header">
      <span>Mission Event Log</span>
      <button class="btn-control" id="btnClear" style="height:26px;font-size:11px;padding:0 8px">Clear Log</button>
    </div>
    <ul class="events-list" id="events"></ul>
  </section>
</main>

<!-- OPERATOR OVERRIDE CONTROLS -->
<details class="mission-ctrl" id="ctrl">
  <summary>
    <svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/></svg>
    <span>Flight Deck Overrides</span>
  </summary>
  <div class="ctrl-actions">
    <button class="btn-control" data-l="0">Beams Off</button>
    <button class="btn-control" data-l="1">Beams On</button>
    <button class="btn-control" data-l="2">Hazard Mode</button>
    <button class="btn-control" id="pcHorn">Trigger Horn</button>
    <button class="btn-control" id="pcFlash">Aux LED Light</button>
    <label class="btn-control">Radar Horizon <select id="sRange"><option value="100">1.0 m</option><option value="200">2.0 m</option><option value="300">3.0 m</option><option value="400">4.0 m</option></select></label>
    <label class="btn-control">Keyboard Steering <input type="checkbox" id="kbDrive" style="margin-left:6px"></label>
    <span style="color:var(--text-muted);font-size:12px;font-family:var(--mono)"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> drive · <kbd>Space</kbd> horn · <kbd>Esc</kbd> stop</span>
  </div>
</details>

<div class="toast" id="toast"></div>

<script>
(() => {
"use strict";
const $ = id => document.getElementById(id);

/* Theme Engine */
let currentTheme = localStorage.getItem("rcTheme") || "light";
function applyTheme(theme) {
  currentTheme = theme;
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("rcTheme", theme);
  const isLight = theme === "light";
  $("metaThemeColor").setAttribute("content", isLight ? "#ffffff" : "#090a0f");
  $("iconSun").classList.toggle("hidden", isLight);
  $("iconMoon").classList.toggle("hidden", !isLight);
}
$("btnTheme").onclick = () => applyTheme(currentTheme === "light" ? "dark" : "light");
applyTheme(currentTheme);

const servedByCar = (location.hostname === "192.168.4.1" || location.hostname.endsWith(".local")) && !/[?&]demo/.test(location.search);
const demo = !servedByCar;
const HOST = servedByCar ? location.host.replace(/:\d+$/, "") : "192.168.4.1";
let range = 200, warn = 100, stop = 15;
try {
  const s = JSON.parse(localStorage.getItem("robotcar") || "{}");
  warn = s.warn || warn; stop = s.stop || stop;
  range = +(localStorage.getItem("rcViewRange") || 200);
} catch(e) {}

function toast(m) {
  const t = $("toast"); t.textContent = m; t.classList.add("show");
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 1800);
}
const pad = n => String(n).padStart(2, "0");
const hms = (d = new Date()) => `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
setInterval(() => $("clock").textContent = hms(), 500);

/* Event Log */
const COLORS = { info: "var(--accent)", ok: "var(--success)", warn: "var(--warning)", bad: "var(--danger)", light: "#facc15" };
function log(text, kind = "info") {
  const li = document.createElement("li");
  li.innerHTML = `<time>${hms()}</time><span class="dot" style="background:${COLORS[kind]}"></span><span></span>`;
  li.lastChild.textContent = text;
  const ul = $("events"); ul.prepend(li);
  while (ul.children.length > 80) ul.lastChild.remove();
}
$("btnClear").onclick = () => $("events").innerHTML = "";

/* WebSocket Client */
let ws = null, wsOk = false;
const send = m => { if (wsOk && ws.readyState === 1) ws.send(m); };
function setChip(id, cls, txt) {
  const c = $(id); c.className = "chip " + cls; c.querySelector("span:last-child").innerHTML = txt;
}

function connect() {
  if (demo) return;
  try { ws = new WebSocket(`ws://${HOST}/ws`); } catch(e) { setTimeout(connect, 2000); return; }
  ws.onopen = () => {
    wsOk = true; setChip("chWs", "ok", "LINKED"); send("R,view"); log("Viewer session established", "ok");
  };
  ws.onclose = () => {
    if (wsOk) log("Rover connection dropped", "bad");
    wsOk = false; setChip("chWs", "bad", "OFFLINE"); setTimeout(connect, 1500);
  };
  ws.onerror = () => { try { ws.close(); } catch(e){} };
  ws.onmessage = e => onMessage(String(e.data));
}

let lastPhones = -1, lastUno = -1;
function onMessage(m) {
  const p = m.split(",");
  if (p[0] === "D") onSensor(+p[1], +p[2], +p[3]);
  else if (p[0] === "T") onState(+p[1], +p[2], +p[3], +p[4], +p[5]);
  else if (p[0] === "I") {
    const rssi = +p[1], phones = +p[2], uno = +p[3], viewers = +(p[4] || 0);
    setChip("chCar", uno ? "ok" : "bad", uno ? "MCU ACTIVE" : "MCU TIMEOUT");
    setChip("chDev", phones ? "ok" : "warn", `<b>${phones}</b> PILOT${phones === 1 ? "" : "S"} · <b>${viewers}</b> VIEW`);
    if (phones !== lastPhones && lastPhones >= 0) log(phones > lastPhones ? "Pilot connected" : "Pilot disconnected", phones > lastPhones ? "ok" : "warn");
    if (uno !== lastUno && lastUno >= 0) log(uno ? "Arduino link synchronized" : "Arduino serial link lost", uno ? "ok" : "bad");
    lastPhones = phones; lastUno = uno;
    const c = $("chRssi");
    if (rssi) { c.classList.remove("hidden"); setChip("chRssi", rssi > -65 ? "ok" : rssi > -78 ? "warn" : "bad", rssi + " dBm"); }
    else c.classList.add("hidden");
  }
}

/* Sensor Telemetry */
let dist = 0, angle = 90, flags = 0, lastData = 0, servoSeen = -1e9, prevFlags = 0, prevLight = -1, prevHorn = 0;
const blips = [], hist = [];
function zoneOf(d) {
  if (!d) return { name: "CLEAR", hex: "var(--success)", lvl: 0 };
  if (d <= stop + 5) return { name: "CRITICAL", hex: "var(--danger)", lvl: 3 };
  if (d < warn * 0.5) return { name: "WARNING", hex: "var(--danger)", lvl: 2 };
  if (d < warn) return { name: "CAUTION", hex: "var(--warning)", lvl: 1 };
  return { name: "CLEAR", hex: "var(--success)", lvl: 0 };
}

function onSensor(a, d, f) {
  angle = a; dist = d; flags = f; lastData = performance.now();
  if (a !== 90) servoSeen = lastData;
  blips.push({ a, d, t: lastData }); if (blips.length > 160) blips.shift();
  const z = zoneOf(d), txt = (d ? d : "&gt;400") + "<small>cm</small>";
  $("distNum").innerHTML = txt; $("distNum").style.color = z.lvl > 0 ? z.hex : "var(--text)";
  $("bdN").innerHTML = txt; $("bdN").style.color = z.lvl > 0 ? z.hex : "#fff";
  $("bdZ").textContent = z.name; $("bdZ").style.color = z.lvl > 0 ? z.hex : "var(--text-dim)";
  const zEl = $("zone"); zEl.textContent = z.name;
  zEl.style.background = z.lvl > 0 ? z.hex : "var(--panel-subtle)";
  zEl.style.color = z.lvl > 0 ? "#fff" : "var(--text-muted)";

  const rev = !!(f & 1), alarm = !!(f & 2), blocked = !!(f & 4), head = !!(f & 16);
  $("tagRev").classList.toggle("hidden", !rev); $("tagBrk").classList.toggle("hidden", !blocked);
  const hud = $("hud");
  hud.classList.toggle("danger", blocked || (alarm && z.lvl === 3));
  hud.classList.toggle("alarm", alarm && !hud.classList.contains("danger"));

  const al = $("bAl"); al.textContent = blocked ? "BRAKE" : alarm ? "ACTIVE" : "QUIET";
  al.className = "badge " + (blocked ? "red" : alarm ? "warn" : "ok");
  $("hlL").setAttribute("fill", head ? "#fde047" : "#334155");
  $("hlR").setAttribute("fill", head ? "#fde047" : "#334155");
  $("beams").setAttribute("opacity", head ? 1 : 0);
  const tl = (alarm && Date.now() % 400 < 200) || blocked ? "#ef4444" : "#3f1d24";
  $("tlL").setAttribute("fill", tl); $("tlR").setAttribute("fill", tl);
  $("rvL").setAttribute("fill", rev ? "#f8fafc" : "#1f2937");
  if ((f & 1) && !(prevFlags & 1)) log("Reverse trajectory engaged", "warn");
  if ((f & 4) && !(prevFlags & 4)) log(`COLLISION BRAKE: Obstacle at ${d} cm`, "bad");
  else if ((f & 2) && !(prevFlags & 2)) log(`Proximity alert: Obstacle at ${d} cm`, "warn");
  prevFlags = f;
}

function onState(l, r, light, hornOn, flash) {
  const pct = v => Math.round(v / 2.55);
  $("lV").textContent = pct(l) + "%"; $("rV").textContent = pct(r) + "%";
  const setBar = (el, v) => {
    const w = Math.abs(v) / 255 * 50;
    el.style.width = w + "%"; el.style.left = v >= 0 ? "50%" : (50 - w) + "%";
    el.style.background = v >= 0 ? "var(--accent)" : "var(--warning)";
  };
  setBar($("lB"), l); setBar($("rB"), r);
  $("arL").setAttribute("opacity", l ? 1 : 0); $("arR").setAttribute("opacity", r ? 1 : 0);
  $("arL").setAttribute("transform", l < 0 ? "rotate(180 29 104.5)" : "");
  $("arR").setAttribute("transform", r < 0 ? "rotate(180 121 104.5)" : "");

  const avg = (l + r) / 2, turn = l - r;
  $("motion").textContent = !l && !r ? "STOPPED" : Math.abs(turn) > 120 && Math.abs(avg) < 60 ? (turn > 0 ? "PIVOT STARBOARD" : "PIVOT PORT")
    : avg > 0 ? (turn > 60 ? "FORWARD STARBOARD" : turn < -60 ? "FORWARD PORT" : "FORWARD") : (turn > 60 ? "REVERSE STARBOARD" : turn < -60 ? "REVERSE PORT" : "REVERSE");

  const lt = $("bLt"); lt.textContent = ["OFF", "ACTIVE", "HAZARD"][light] || "OFF";
  lt.className = "badge " + (light === 1 ? "on" : light === 2 ? "warn" : "");
  $("tagLt").classList.toggle("hidden", !light); $("tagLt").textContent = light === 2 ? "HAZARD" : "BEAMS ACTIVE";
  const hn = $("bHn"); hn.textContent = hornOn ? "ACTIVE" : "OFF";
  hn.className = "badge " + (hornOn ? "warn" : "");
  if (light !== prevLight && prevLight >= 0) log(["Headlights Off", "Headlights On", "Hazard Flash Engaged"][light] || "Lights", "light");
  if (hornOn && !prevHorn) log("Acoustic Horn Sounded", "info");
  prevLight = light; prevHorn = hornOn;
  $("pcFlash").classList.toggle("active", flash > 0); flashOn = flash > 0;
}
setInterval(() => {
  hist.push({ t: Date.now(), d: performance.now() - lastData < 1000 ? dist : null });
  while (hist.length && hist[0].t < Date.now() - 60000) hist.shift();
}, 200);

/* Optical Stream Engine */
const cam = $("cam"); let paused = false, retry = null;
function noVideo(t) { $("novTxt").innerHTML = t; $("novideo").classList.remove("hidden"); }
function startVideo() {
  clearTimeout(retry);
  if (demo) { noVideo("Camera simulation<br><small>Connect to the vehicle's Wi-Fi network for live optical telemetry</small>"); return; }
  if (paused) { cam.removeAttribute("src"); noVideo("OPTICAL FEED FROZEN"); return; }
  cam.src = `http://${HOST}:81/stream?t=${Date.now()}`;
}
cam.onload = () => $("novideo").classList.add("hidden");
cam.onerror = () => {
  if (paused) return;
  fetch(`http://${HOST}/status`)
    .then(r => r.json())
    .then(st => {
      if (!st.camOk || st.framesize === -1) {
        noVideo("CAMERA NOT DETECTED<br><small>1. Check ribbon cable latch &amp; pin orientation<br>2. Board: <b>AI Thinker ESP32-CAM</b><br>3. Tools &rarr; PSRAM: <b>Enabled</b></small>");
        retry = setTimeout(startVideo, 4000);
      } else {
        noVideo("CONNECTING STREAM&hellip;");
        retry = setTimeout(startVideo, 2000);
      }
    })
    .catch(() => {
      noVideo("RECONNECTING OPTICAL STREAM&hellip;");
      retry = setTimeout(startVideo, 2500);
    });
};
$("btnPause").onclick = () => {
  paused = !paused; $("btnPause").classList.toggle("active", paused);
  $("btnPause").querySelector("span").textContent = paused ? "Resume" : "Freeze"; startVideo();
};
$("btnVidFull").onclick = () => {
  const el = $("screen"); (document.fullscreenElement ? document.exitFullscreen() : el.requestFullscreen()).catch(() => {});
};
$("btnFull").onclick = () => {
  (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()).catch(() => {});
};
const stamp = () => {
  const d = new Date();
  return `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
};
function download(blob, name) {
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
  a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

const rc = document.createElement("canvas"), rg = rc.getContext("2d");
function drawFrame() {
  const w = cam.naturalWidth || 640, h = cam.naturalHeight || 480;
  if (rc.width !== w || rc.height !== h) { rc.width = w; rc.height = h; }
  rg.drawImage(cam, 0, 0, w, h);
  rg.fillStyle = "rgba(0,0,0,.6)"; rg.fillRect(0, h - 28, w, 28);
  rg.fillStyle = "#fff"; rg.font = "bold 13px system-ui"; rg.textBaseline = "middle";
  rg.fillText(`ROVER DECK  ${hms()}  ·  RANGE ${dist ? dist + " cm" : "CLEAR"}  ·  ${$("motion").textContent}`, 10, h - 14);
}
$("btnSnap").onclick = () => {
  if (demo || !cam.naturalWidth) return toast("Photos require live optical feed");
  try {
    drawFrame();
    rc.toBlob(b => { if (b) { download(b, `rover-${stamp()}.jpg`); log("Frame snapshot saved", "ok"); } }, "image/jpeg", 0.92);
  } catch(e) { window.open(`http://${HOST}/capture`, "_blank"); }
};
let rec = null, recChunks = [], recT0 = 0, recTimer = null, recRaf = null;
$("btnRec").onclick = () => {
  if (rec) { rec.stop(); return; }
  if (demo || !cam.naturalWidth) return toast("Recording requires live optical feed");
  try {
    drawFrame();
    const stream = rc.captureStream(15);
    const type = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm", "video/mp4"].find(t => window.MediaRecorder && MediaRecorder.isTypeSupported(t));
    rec = new MediaRecorder(stream, type ? { mimeType: type } : {});
  } catch(e) { rec = null; return toast("Recording format unsupported"); }
  recChunks = []; rec.ondataavailable = e => e.data.size && recChunks.push(e.data);
  rec.onstop = () => {
    cancelAnimationFrame(recRaf); clearInterval(recTimer);
    download(new Blob(recChunks, { type: rec.mimeType || "video/webm" }), `rover-${stamp()}.${(rec.mimeType || "").includes("mp4") ? "mp4" : "webm"}`);
    rec = null; $("btnRec").classList.remove("active"); $("btnRec").querySelector("span").textContent = "Record Video";
    $("tagRec").classList.add("hidden"); log("Optical recording exported", "ok");
  };
  const loop = () => { try { drawFrame(); } catch(e){} recRaf = requestAnimationFrame(loop); }; loop();
  rec.start(1000); recT0 = Date.now();
  $("btnRec").classList.add("active"); $("btnRec").querySelector("span").textContent = "Stop Recording";
  $("tagRec").classList.remove("hidden");
  recTimer = setInterval(() => {
    const s = Math.floor((Date.now() - recT0) / 1000);
    $("tagRec").textContent = `REC ${pad(Math.floor(s/60))}:${pad(s%60)}`;
  }, 500);
  log("Optical recording started", "warn");
};

/* Sonar Radar Canvas */
const cv = $("radar"), g = cv.getContext("2d");
function drawRadar() {
  const dpr = window.devicePixelRatio || 1, W = cv.clientWidth, H = cv.clientHeight;
  if (W && H) {
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) {
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    }
    g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
    const cx = W / 2, R = Math.max(20, Math.min(W / 2 - 14, H - 34)), cy = Math.min(H - 16, H / 2 + R / 2 + 6);
    const now = performance.now(), rad = a => a * Math.PI / 180;
    const isLight = document.documentElement.getAttribute("data-theme") === "light";

    g.beginPath(); g.arc(cx, cy, R, 0, Math.PI, true);
    g.fillStyle = isLight ? "#f1f5f9" : "#0d111a"; g.fill();

    g.strokeStyle = isLight ? "rgba(148, 163, 184, 0.3)" : "rgba(6, 182, 212, 0.25)";
    g.lineWidth = 1; g.fillStyle = isLight ? "#64748b" : "#94a3b8"; g.font = "10px monospace"; g.textAlign = "center";
    const step = range <= 100 ? 25 : 50;
    for (let d = step; d <= range; d += step) {
      g.beginPath(); g.arc(cx, cy, d / range * R, Math.PI, 2 * Math.PI); g.stroke();
      if (d / range * R > 30) g.fillText(d >= 100 ? (d/100) + "m" : d + "", cx + d/range*R - 10, cy + 12);
    }

    const fresh = now - lastData < 1000;
    if (fresh && dist && dist <= range) {
      const z = zoneOf(dist);
      g.strokeStyle = z.hex === "var(--success)" ? "#10b981" : z.hex === "var(--warning)" ? "#f59e0b" : "#ef4444";
      g.lineWidth = 6; g.lineCap = "round";
      g.beginPath(); g.arc(cx, cy, dist / range * R, -rad(105), -rad(75)); g.stroke();
    }

    g.fillStyle = isLight ? "#cbd5e1" : "#1e293b"; g.strokeStyle = isLight ? "#64748b" : "#06b6d4"; g.lineWidth = 1.5;
    g.beginPath(); g.roundRect ? g.roundRect(cx - 20, cy - 4, 40, 14, 3) : g.rect(cx - 20, cy - 4, 40, 14); g.fill(); g.stroke();
  }
  drawChart();
  requestAnimationFrame(drawRadar);
}

/* Real-Time Distance History Chart */
const ch = $("chart"), cg = ch.getContext("2d");
function drawChart() {
  const dpr = window.devicePixelRatio || 1, W = ch.clientWidth, H = ch.clientHeight; if (!W || !H) return;
  if (ch.width !== Math.round(W * dpr) || ch.height !== Math.round(H * dpr)) {
    ch.width = Math.round(W * dpr); ch.height = Math.round(H * dpr);
  }
  cg.setTransform(dpr, 0, 0, dpr, 0, 0); cg.clearRect(0, 0, W, H);
  const L = 38, B = 20, T = 8, top = Math.max(range, warn + 20), now = Date.now();
  const x = t => L + (W - L - 8) * (1 - (now - t) / 60000), y = d => T + (H - T - B) * (1 - Math.min(d, top) / top);
  const isLight = document.documentElement.getAttribute("data-theme") === "light";

  cg.font = "10px monospace"; cg.fillStyle = isLight ? "#64748b" : "#94a3b8";
  cg.strokeStyle = isLight ? "rgba(226, 232, 240, 0.8)" : "rgba(35, 43, 62, 0.8)"; cg.lineWidth = 1;
  cg.textAlign = "right"; cg.textBaseline = "middle";
  for (let d = 0; d <= top; d += top > 200 ? 100 : 50) {
    cg.beginPath(); cg.moveTo(L, y(d)); cg.lineTo(W - 8, y(d)); cg.stroke();
    cg.fillText(d, L - 6, y(d));
  }

  cg.strokeStyle = isLight ? "#2563eb" : "#06b6d4"; cg.lineWidth = 2.5; cg.beginPath(); let pen = false;
  for (const p of hist) {
    if (p.d === null) { pen = false; continue; }
    const yy = y(p.d || top);
    pen ? cg.lineTo(x(p.t), yy) : cg.moveTo(x(p.t), yy);
    pen = true;
  }
  cg.stroke();

  const vals = hist.filter(p => p.d).map(p => p.d);
  $("chartInfo").textContent = vals.length ? `MIN PROXIMITY: ${Math.min(...vals)} cm` : "";
}
requestAnimationFrame(drawRadar);

/* Mission Overrides */
let flashOn = false;
document.querySelectorAll("[data-l]").forEach(b => b.onclick = () => {
  send(`L,${b.dataset.l}`); if (demo) onState(0, 0, +b.dataset.l, 0, 0);
});
const ph = $("pcHorn");
ph.onpointerdown = () => { send("H,1"); ph.classList.add("active"); };
ph.onpointerup = ph.onpointerleave = () => { if (ph.classList.contains("active")) { send("H,0"); ph.classList.remove("active"); } };
$("pcFlash").onclick = () => { flashOn = !flashOn; send(`K,${flashOn ? 180 : 0}`); $("pcFlash").classList.toggle("active", flashOn); };
$("sRange").value = range;
$("sRange").onchange = () => { range = +$("sRange").value; try { localStorage.setItem("rcViewRange", range); } catch(e){} };

const keys = new Set(); let kx = 0, ky = 0;
const kb = () => $("kbDrive").checked;
$("kbDrive").onchange = () => {
  if (kb()) { send("R,phone"); log("Console steering override engaged", "warn"); }
  else { send("M,0,0"); send("R,view"); log("Console steering released"); }
};
addEventListener("keydown", e => {
  if (!kb()) return; const k = e.key.toLowerCase();
  if (k === "escape") { keys.clear(); send("S"); return; }
  if (k === " ") { if (!e.repeat) send("H,1"); e.preventDefault(); return; }
  if (["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"].includes(k)) { keys.add(k); e.preventDefault(); }
});
addEventListener("keyup", e => { const k = e.key.toLowerCase(); if (k === " " && kb()) send("H,0"); keys.delete(k); });
setInterval(() => {
  if (!kb()) return;
  ky = (keys.has("w")||keys.has("arrowup") ? 1 : 0) - (keys.has("s")||keys.has("arrowdown") ? 1 : 0);
  kx = (keys.has("d")||keys.has("arrowright") ? 1 : 0) - (keys.has("a")||keys.has("arrowleft") ? 1 : 0);
  // Invert steering so 'D' / Right Arrow turns right physically on cross-wired chassis:
  let l = ky - kx * .7, r = ky + kx * .7; const m = Math.max(1, Math.abs(l), Math.abs(r));
  send(`M,${Math.round(l / m * 180)},${Math.round(r / m * 180)}`);
}, 100);

if (demo) {
  setChip("chWs", "warn", "SIMULATOR ACTIVE");
}
startVideo();
connect();
})();
</script>
</body>
</html>
)rawhtml";
