"""Generate the animated terminal header (assets/header-dark.svg and assets/header-light.svg).

Usage: python3 tools/make_header.py <path to Backtest 3 equity_curve.csv> assets
Needs pyfiglet (pip install pyfiglet). Only the total_equity column is read.
"""
import csv, sys, html
import pyfiglet

EQUITY_CSV, OUT_DIR = sys.argv[1], sys.argv[2]

# --- equity curve (total equity only), downsampled -------------------------
vals = []
with open(EQUITY_CSV) as f:
    for row in csv.DictReader(f):
        vals.append(float(row["total_equity"]))
N = 110
step = (len(vals) - 1) / (N - 1)
pts = [vals[round(i * step)] for i in range(N)]
lo, hi = min(pts), max(pts)

W, H = 900, 370
SP_X, SP_Y, SP_W, SP_H = 610, 70, 260, 80
coords = [
    (SP_X + i * SP_W / (N - 1), SP_Y + SP_H - (v - lo) / (hi - lo) * SP_H)
    for i, v in enumerate(pts)
]
line = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
area = f"{SP_X},{SP_Y + SP_H} " + line + f" {SP_X + SP_W},{SP_Y + SP_H}"

ascii_lines = pyfiglet.figlet_format("GIOVANNI", font="ansi_shadow", width=200).rstrip("\n").split("\n")
ascii_lines = [l for l in ascii_lines if l.strip()]

PROMPT = "giovanni@bocconi:~$"
session = [
    ("cmd", "whoami"),
    ("out", "Giovanni De Stasio · BSc International Economics & Finance @ Bocconi · Milan"),
    ("cmd", "cat interests.txt"),
    ("hl", "quant finance · financial markets · venture capital · startups · apps"),
    ("cmd", "ls research/"),
    ("dir", "hormuz-shock-2026.pdf   macro-financial-regime-2026.pdf   vix-futures-strategy/"),
]

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 g1="#3fb950", g2="#58a6ff", accent="#3fb950", dir="#58a6ff", hl="#d2a8ff", area="#3fb950"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#656d76",
                  g1="#1a7f37", g2="#0969da", accent="#1a7f37", dir="#0969da", hl="#8250df", area="#1a7f37"),
}

FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def build(t):
    e = html.escape
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
               f'aria-label="Giovanni De Stasio — finance student at Bocconi University">')
    out.append(f"""<style>
  text {{ font-family: {FONT}; }}
  .ascii {{ font-size: 13px; fill: url(#grad); }}
  .t {{ font-size: 14px; fill: {t['text']}; }}
  .p {{ fill: {t['accent']}; font-weight: 600; }}
  .m {{ fill: {t['muted']}; }}
  .d {{ fill: {t['dir']}; }}
  .h {{ fill: {t['hl']}; }}
  .lbl {{ font-size: 11px; fill: {t['muted']}; letter-spacing: .06em; }}
  .big {{ font-size: 22px; font-weight: 700; fill: {t['accent']}; }}
  .ln {{ animation: show .35s ease-out both; }}
  .spark {{ stroke-dasharray: 1200; animation: draw 2.6s ease-out .4s both; }}
  .fill {{ opacity: .14; animation: fade 1s ease-out 2.6s both; }}
  .cursor {{ animation: blink 1s steps(1) infinite; }}
  @keyframes show {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: .14; }} }}
  @keyframes draw {{ from {{ stroke-dashoffset: 1200; }} to {{ stroke-dashoffset: 0; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .ln, .spark, .fill, .cursor {{ animation: none; }}
  }}
</style>""")
    out.append(f"""<defs><linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="28" y1="0" x2="480" y2="0">
  <stop offset="0" stop-color="{t['g1']}"/><stop offset="1" stop-color="{t['g2']}"/></linearGradient></defs>""")
    # window
    out.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    out.append(f'<path d="M0.5 36 V10.5 a10 10 0 0 1 10 -10 H{W-10.5} a10 10 0 0 1 10 10 V36 Z" fill="{t["bar"]}" stroke="{t["border"]}"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        out.append(f'<circle cx="{22 + i*20}" cy="18" r="6" fill="{c}"/>')
    out.append(f'<text x="{W/2}" y="23" text-anchor="middle" class="lbl">giovanni@bocconi — zsh</text>')
    # ascii banner
    CW, CH, X0, Y0 = 7.4, 13, 28, 56
    blocks, shadows = [], []
    for r, l in enumerate(ascii_lines):
        for c, ch in enumerate(l):
            if ch == " ":
                continue
            x, y = X0 + c * CW, Y0 + r * CH
            if ch == "█":
                blocks.append(f'<rect x="{x:.1f}" y="{y}" width="{CW+0.3:.1f}" height="{CH+0.3}"/>')
            else:
                shadows.append(f'<rect x="{x+CW*0.25:.1f}" y="{y+CH*0.25:.1f}" width="{CW*0.75:.1f}" height="{CH*0.75:.1f}"/>')
    out.append(f'<g fill="{t["muted"]}" opacity=".35">' + "".join(shadows) + "</g>")
    out.append('<g fill="url(#grad)">' + "".join(blocks) + "</g>")
    # sparkline panel
    out.append(f'<text x="{SP_X}" y="62" class="lbl">VIX RESEARCH · BACKTEST 3 · 2013–26</text>')
    out.append(f'<polygon points="{area}" fill="{t["area"]}" class="fill"/>')
    out.append(f'<polyline points="{line}" fill="none" stroke="{t["accent"]}" stroke-width="2" '
               f'stroke-linejoin="round" stroke-linecap="round" class="spark"/>')
    out.append(f'<text x="{SP_X}" y="{SP_Y + SP_H + 28}" class="big">16.7% CAGR</text>')
    out.append(f'<text x="{SP_X}" y="{SP_Y + SP_H + 48}" class="t m" style="font-size:12px">Sharpe 0.82 · Max DD −24.1%</text>')
    # session
    y0, dy, delay = 222, 22, 0.6
    for i, (kind, txt) in enumerate(session):
        y = y0 + i * dy
        style = f'style="animation-delay:{delay:.1f}s"'
        if kind == "cmd":
            out.append(f'<text x="28" y="{y}" class="t ln" {style} xml:space="preserve"><tspan class="p">{PROMPT}</tspan> {e(txt)}</text>')
            delay += 0.9
        else:
            cls = {"out": "", "hl": "h", "dir": "d"}[kind]
            out.append(f'<text x="28" y="{y}" class="t ln {cls}" {style} xml:space="preserve">{e(txt)}</text>')
            delay += 0.5
    y = y0 + len(session) * dy
    out.append(f'<text x="28" y="{y}" class="t ln" style="animation-delay:{delay:.1f}s" xml:space="preserve">'
               f'<tspan class="p">{PROMPT}</tspan> <tspan class="cursor">▌</tspan></text>')
    out.append("</svg>")
    return "\n".join(out)


for name, theme in THEMES.items():
    with open(f"{OUT_DIR}/header-{name}.svg", "w") as f:
        f.write(build(theme))
print("ok", len(ascii_lines), "ascii lines")
