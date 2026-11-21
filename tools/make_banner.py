"""Generate the animated profile banner (assets/banner-dark.svg and assets/banner-light.svg).

The banner replays the portfolio's intro: the ticker GDS is typed into a terminal, a lookup
row resolves it, Enter is pressed, and the profile card appears.

Every animation only *hides* things before their moment (fill-mode: backwards). With
animations off or under reduced motion, the SVG shows its final state: the profile card.

Usage: python3 tools/make_banner.py
"""

import html
from pathlib import Path

W, H = 900, 380
OUT = Path(__file__).resolve().parent.parent / "assets"

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"

FACTS = [
    ("IMC PROSPERITY 4", "Finalist of 18,803 teams"),
    ("VANTEDGE", "Co-founder, Head of DCM"),
    ("BSQF", "Quant analyst, two papers"),
    ("BOCCONI", "Computer Science 30L/30"),
]

THEMES = {
    "dark": dict(bg="#0e0f11", panel="#16171a", ink="#ecebe5", mute="#8f8e89", faint="#5f5e5a",
                 line="#ecebe5", line_op=0.1, accent="#8fd6a0", pick_ink="#16171a"),
    "light": dict(bg="#f4f2ed", panel="#ebe8e1", ink="#17181a", mute="#6a6964", faint="#97958f",
                  line="#17181a", line_op=0.12, accent="#2f8f57", pick_ink="#f4f2ed"),
}

# Timeline in seconds.
TYPE_AT = [0.55, 0.74, 0.88]
LOOKUP_AT = 1.15
ENTER_AT = 2.15
STAGE1_END = 2.75
STAGE2_AT = 2.85


def build(t):
    e = html.escape
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="Giovanni De Stasio. Finance at Bocconi, Milan. I study financial markets, build trading systems and develop apps.">')
    o.append(f"""<style>
  .m {{ font-family: {MONO}; }}
  .s {{ font-family: {SANS}; }}
  .stage1 {{ opacity: 0; animation: stage1 {STAGE1_END}s linear backwards; }}
  @keyframes stage1 {{ 0%, 92% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
  .hide-until {{ animation-name: hidden; animation-timing-function: step-end; animation-fill-mode: backwards; }}
  @keyframes hidden {{ from, to {{ opacity: 0; }} }}
  .cursor {{ animation: blink 0.9s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .rise {{ animation: rise 0.7s cubic-bezier(.22,1,.36,1) backwards; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} }}
  .fade {{ animation: fade 0.35s ease-out backwards; }}
  @keyframes fade {{ from {{ opacity: 0; }} }}
  .pick {{ fill-opacity: 0; animation: pick 0.12s ease-out {ENTER_AT}s forwards; }}
  @keyframes pick {{ to {{ fill-opacity: 1; }} }}
  .pick-text {{ animation: pickText 0.12s ease-out {ENTER_AT}s forwards; }}
  @keyframes pickText {{ to {{ fill: {t['pick_ink']}; }} }}
  .bar {{ transform: scaleX(0); transform-origin: 0 0; animation: bar 0.45s cubic-bezier(.23,1,.32,1) {ENTER_AT + 0.05}s forwards; }}
  @keyframes bar {{ to {{ transform: scaleX(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>""")
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>')

    # ---- Stage 1: the terminal lookup ----
    o.append('<g class="stage1">')
    o.append(f'<rect class="bar" x="0" y="0" width="{W}" height="2" fill="{t["accent"]}"/>')
    x0, y0 = 250, 150
    o.append(f'<text x="{x0}" y="{y0}" class="m" font-size="54" fill="{t["faint"]}">›</text>')
    for i, ch in enumerate("GDS"):
        o.append(f'<text x="{x0 + 52 + i * 40}" y="{y0}" class="m hide-until" font-size="54" letter-spacing="2" '
                 f'fill="{t["ink"]}" style="animation-duration:{TYPE_AT[i]}s">{ch}</text>')
    o.append(f'<rect class="cursor" x="{x0 + 52 + 3 * 40 + 6}" y="{y0 - 42}" width="24" height="48" fill="{t["ink"]}"/>')
    ry = 185
    o.append(f'<g class="fade" style="animation-delay:{LOOKUP_AT}s">')
    o.append(f'<rect x="{x0}" y="{ry}" width="400" height="50" rx="9" fill="{t["ink"]}" class="pick"/>')
    o.append(f'<rect x="{x0 + .5}" y="{ry + .5}" width="399" height="49" rx="9" fill="none" stroke="{t["line"]}" stroke-opacity="{t["line_op"] + .06}"/>')
    o.append(f'<text x="{x0 + 18}" y="{ry + 30}" class="m pick-text" font-size="14" font-weight="600" letter-spacing="2" fill="{t["ink"]}">GDS</text>')
    o.append(f'<text x="{x0 + 74}" y="{ry + 30}" class="m pick-text" font-size="13" fill="{t["mute"]}">Giovanni De Stasio · Bocconi · Milan</text>')
    o.append('</g>')
    o.append(f'<g class="fade" style="animation-delay:{LOOKUP_AT + 0.2}s">')
    o.append(f'<text x="{x0}" y="{ry + 82}" class="m" font-size="12" fill="{t["faint"]}">1 result</text>')
    o.append(f'<rect x="{x0 + 290}" y="{ry + 64}" width="110" height="28" rx="14" fill="{t["panel"]}"/>')
    o.append(f'<text x="{x0 + 345}" y="{ry + 83}" class="m" font-size="12" text-anchor="middle" fill="{t["ink"]}">Enter ↵</text>')
    o.append('</g>')
    o.append('</g>')

    # ---- Stage 2: the profile card (the resting state) ----
    pad = 56
    o.append('<g>')
    o.append(f'<g class="rise" style="animation-delay:{STAGE2_AT}s">'
             f'<circle cx="{pad + 3}" cy="{pad + 2}" r="3" fill="{t["accent"]}"/>'
             f'<text x="{pad + 16}" y="{pad + 6}" class="m" font-size="12" letter-spacing="2.2" fill="{t["mute"]}">GDS · FINANCE AT BOCCONI · MILAN</text></g>')
    o.append(f'<g class="rise" style="animation-delay:{STAGE2_AT + 0.09}s">'
             f'<text x="{pad - 3}" y="{pad + 86}" class="s" font-size="68" font-weight="300" letter-spacing="-2.6" fill="{t["ink"]}">Giovanni '
             f'<tspan font-weight="650">De Stasio</tspan></text></g>')
    o.append(f'<g class="rise" style="animation-delay:{STAGE2_AT + 0.2}s">'
             f'<text x="{pad}" y="{pad + 132}" class="s" font-size="20" fill="{t["mute"]}">I study financial markets, build '
             f'<tspan fill="{t["ink"]}" font-weight="600">trading systems</tspan> and develop '
             f'<tspan fill="{t["ink"]}" font-weight="600">apps</tspan>.</text></g>')
    fy = 262
    o.append(f'<g class="fade" style="animation-delay:{STAGE2_AT + 0.35}s">')
    o.append(f'<line x1="{pad}" x2="{W - pad}" y1="{fy}" y2="{fy}" stroke="{t["line"]}" stroke-opacity="{t["line_op"]}"/>')
    col = (W - 2 * pad) / 4
    for i, (k, v) in enumerate(FACTS):
        x = pad + i * col
        o.append(f'<text x="{x}" y="{fy + 34}" class="m" font-size="10.5" letter-spacing="1.8" fill="{t["faint"]}">{e(k)}</text>')
        o.append(f'<text x="{x}" y="{fy + 60}" class="s" font-size="15" fill="{t["ink"]}">{e(v)}</text>')
    o.append('</g>')
    o.append('</g>')
    o.append("</svg>")

    # Stage 2 must not show while stage 1 plays: wrap it in a hider that releases at STAGE2_AT.
    svg = "\n".join(o)
    return svg.replace("<g>\n<g class=\"rise\"", f'<g class="hide-until" style="animation-duration:{STAGE2_AT}s">\n<g class="rise"', 1)


for name, theme in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(build(theme), encoding="utf-8")
print("written:", ", ".join(f"banner-{n}.svg" for n in THEMES))
