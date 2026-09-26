"""Isometric 'career as a city' scene. Imported by build.py.

One 20s loop: each era's district rises in turn, then everything holds, fades, and restarts.
Base styles are the finished skyline, and animations only play in from a hidden start, so
renderers that skip animation (and prefers-reduced-motion) show the complete city.
"""

W, H = 1200, 540
CX, CY, S = 790, 165, 24  # screen position of grid origin, pixels per grid unit
C = 0.866  # cos 30
CYCLE = 20  # seconds

# (start, end) seconds each era takes to build
ERAS = [(0.4, 2.4), (3.0, 5.0), (5.6, 7.6), (8.2, 10.2), (10.8, 12.8)]
HOLD_END, FADE_END = 18.4, 19.4

CAPTIONS = [
    ("2015", "Data foundations", "ETL Developer, InnoMinds", "Data Engineer, DSO MCS Group", "Warehouses, pipelines, the first roads."),
    ("2019", "Cloud at scale", "Senior Data Engineer, Charles Schwab", "Multi-PB to GCP · 1B+ records a day", "$1M+ saved, zero data loss."),
    ("2022", "GenAI accelerators", "Lead Data Engineer, HCA Healthcare", "100+ TB HIPAA migration to GCP", "Delivery timelines cut 50%."),
    ("2024", "Forward deployed", "NRG Energy · Definity", "AWS to GCP Databricks, near-zero downtime", "COBOL to BigQuery via GenAI, 12 workstreams."),
    ("2026", "Applied GenAI", "Forward Deployed AI Architect, Wiley", "RAG over 50M+ documents · 95% grounded", "Every district now feeds the AI core."),
]

# (x, y, w, d, h, era) on a 12x12 grid
BUILDINGS = [
    (0.5, 8.5, 2, 2, 1.2, 0), (3.2, 9.4, 2, 1.2, 0.8, 0), (0.6, 5.8, 1.6, 1.6, 1.0, 0), (3.4, 7.2, 1.2, 1.2, 1.6, 0),
    (6.8, 7.4, 1, 1, 4.2, 1), (8.6, 8.2, 1, 1.6, 5.2, 1), (6.6, 9.8, 1.8, 1, 3.2, 1), (9.8, 5.6, 1, 1, 6.0, 1),
    (1.2, 1.4, 1, 1, 4.6, 2), (3.4, 1.0, 1.6, 1, 3.0, 2), (7.8, 0.8, 1, 1, 5.6, 2), (10.0, 2.2, 1, 1, 4.0, 2),
    (10.6, 10.0, 1, 1, 2.8, 3), (0.2, 3.4, 1, 1.4, 2.2, 3), (6.2, 3.2, 1, 1, 3.4, 3),
]
SPIRE = (5.1, 5.1, 0.8, 0.8, 11.0)
ROADS = [((0, 5.0), (12, 5.0)), ((5.0, 0), (5.0, 12)), ((0, 6.8), (12, 6.8)), ((6.8, 0), (6.8, 12))]
BRIDGES = [((2.4, 9.4, 1.2), (6.8, 7.4, 4.2)), ((4.2, 1.5, 3.0), (7.8, 0.8, 5.6)), ((0.7, 4.1, 2.2), (1.7, 1.9, 4.6)), ((11.1, 10.5, 2.8), (9.1, 9.0, 5.2))]

PALETTE = {
    "dark": dict(
        bg="#0d1117", fg="#e6edf3", muted="#8b949e", ground="#11161d", road="#1f2630", accent="#58a6ff", window="#f2cc60",
        eras=[("#3d444d", "#2a3038", "#1c2128"), ("#2f81f7", "#1f5fc4", "#16469a"), ("#8d62e9", "#6a44c4", "#4f3197"),
              ("#2ea099", "#207a74", "#175a56"), ("#79c0ff", "#4b9cf0", "#2f7ad6")]),
    "light": dict(
        bg="#ffffff", fg="#1f2328", muted="#59636e", ground="#f3f5f8", road="#dfe4ea", accent="#0969da", window="#d4a72c",
        eras=[("#d0d7de", "#b5bec8", "#98a3ae"), ("#6cb6ff", "#3b8eea", "#2170c9"), ("#b9a3f5", "#9476e6", "#7556cf"),
              ("#6fd3c9", "#3fb3a8", "#2a9187"), ("#8ec9ff", "#54aeff", "#218bff")]),
}


def P(x, y, z=0):
    return CX + (x - y) * C * S, CY + (x + y) * 0.5 * S - z * S


def pts(*ps):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in ps)


def pct(sec):
    return f"{sec / CYCLE * 100:.2f}%"


def keyframes():
    out = []
    for i, (a, b) in enumerate(ERAS):
        hide = f"0%, {pct(a)}"
        out.append(f"@keyframes rise{i} {{ {hide} {{ transform: scaleY(0); opacity: 0; }} {pct(b)}, {pct(HOLD_END)} {{ transform: scaleY(1); opacity: 1; }} {pct(FADE_END)}, 100% {{ transform: scaleY(1); opacity: 0; }} }}")
        out.append(f"@keyframes show{i} {{ {hide} {{ opacity: 0; }} {pct(b)}, {pct(HOLD_END)} {{ opacity: 1; }} {pct(FADE_END)}, 100% {{ opacity: 0; }} }}")
        nxt = ERAS[i + 1][0] if i + 1 < len(ERAS) else None
        if nxt is None:
            out.append(f"@keyframes cap{i} {{ 0%, {pct(a)} {{ opacity: 0; transform: translateY(8px); }} {pct(a + 0.6)}, {pct(HOLD_END)} {{ opacity: 1; transform: none; }} {pct(FADE_END)}, 100% {{ opacity: 0; }} }}")
        else:
            out.append(f"@keyframes cap{i} {{ 0%, {pct(a)} {{ opacity: 0; transform: translateY(8px); }} {pct(a + 0.6)}, {pct(nxt - 0.4)} {{ opacity: 1; transform: none; }} {pct(nxt)}, 100% {{ opacity: 0; }} }}")
    rules = "\n  ".join(out)
    era_rules = "\n  ".join(
        f".r{i} {{ animation: rise{i} {CYCLE}s cubic-bezier(.2,.8,.2,1) infinite; }} .s{i} {{ animation: show{i} {CYCLE}s ease-out infinite; }} .c{i} {{ animation: cap{i} {CYCLE}s ease-out infinite; }}"
        for i in range(len(ERAS)))
    return f"""<style>
  .r0, .r1, .r2, .r3, .r4 {{ transform-box: fill-box; transform-origin: 50% 100%; }}
  .cap {{ opacity: 0; }} .c4 {{ opacity: 1; }}
  .twinkle {{ animation: twinkle 3.2s ease-in-out infinite; }}
  .flow {{ stroke-dasharray: 4 10; animation: flow 1.2s linear infinite; }}
  .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.6s ease-in-out infinite; }}
  {era_rules}
  {rules}
  @keyframes twinkle {{ 0%, 100% {{ opacity: .95; }} 50% {{ opacity: .25; }} }}
  @keyframes flow {{ to {{ stroke-dashoffset: -28; }} }}
  @keyframes pulse {{ 0%, 100% {{ transform: scale(.8); opacity: .55; }} 50% {{ transform: scale(1.15); opacity: 1; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .r0, .r1, .r2, .r3, .r4, .s0, .s1, .s2, .s3, .s4, .c4, .twinkle, .flow, .pulse {{ animation: none; }}
    .c0, .c1, .c2, .c3 {{ animation: none; opacity: 0; }}
    .packet {{ display: none; }}
  }}
</style>"""


def box(x, y, w, d, h, faces, windows, lit):
    top, left, right = faces
    t = pts(P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h))
    lf = pts(P(x, y + d), P(x + w, y + d), P(x + w, y + d, h), P(x, y + d, h))
    rf = pts(P(x + w, y), P(x + w, y + d), P(x + w, y + d, h), P(x + w, y, h))
    parts = [f'<polygon points="{lf}" fill="{left}"/>', f'<polygon points="{rf}" fill="{right}"/>', f'<polygon points="{t}" fill="{top}"/>']
    if windows and h >= 1.5:
        # inset window band so windows don't touch roof or ground
        lw = pts(P(x + .15, y + d, .35), P(x + w - .15, y + d, .35), P(x + w - .15, y + d, h - .3), P(x + .15, y + d, h - .3))
        rw = pts(P(x + w, y + .15, .35), P(x + w, y + d - .15, .35), P(x + w, y + d - .15, h - .3), P(x + w, y + .15, h - .3))
        parts.append(f'<polygon points="{lw}" fill="url(#winL)"/><polygon points="{rw}" fill="url(#winR)"/>')
        if lit:
            parts.append(f'<polygon class="twinkle" style="animation-delay:{lit:.1f}s" points="{lw}" fill="url(#litL)"/>')
    return "".join(parts)


def city(theme):
    p = PALETTE[theme]
    ground = pts(P(-0.6, -0.6), P(12.6, -0.6), P(12.6, 12.6), P(-0.6, 12.6))
    roads = "".join(f'<line x1="{P(*a)[0]:.1f}" y1="{P(*a)[1]:.1f}" x2="{P(*b)[0]:.1f}" y2="{P(*b)[1]:.1f}" stroke="{p["road"]}" stroke-width="7" stroke-linecap="round"/>' for a, b in ROADS)

    packets = []
    for i, (a, b) in enumerate(ROADS):
        pa, pb = P(*a), P(*b)
        for k in range(3):
            era = 0 if i < 2 else 1
            packets.append(
                f'<g class="s{era}"><circle class="packet" r="2.6" fill="{p["accent"]}"><animateMotion dur="{4 + i * .7:.1f}s" begin="{k * 1.4 + i * .3:.1f}s" repeatCount="indefinite" '
                f'path="M{pa[0]:.1f} {pa[1]:.1f} L{pb[0]:.1f} {pb[1]:.1f}"/></circle></g>')

    order = sorted(enumerate(BUILDINGS), key=lambda ib: ib[1][0] + ib[1][1] + (ib[1][2] + ib[1][3]) / 2)
    spire_key = SPIRE[0] + SPIRE[1] + SPIRE[2]
    drawn, spire_done = [], False
    sx, sy, sw, sd, sh = SPIRE
    spire_top = P(sx + sw / 2, sy + sd / 2, sh)
    spire = (f'<g class="r4">{box(sx, sy, sw, sd, sh, p["eras"][4], True, 0.4)}</g>'
             f'<g class="s4"><circle class="pulse" cx="{spire_top[0]:.1f}" cy="{spire_top[1]:.1f}" r="22" fill="url(#glow)"/>'
             f'<circle cx="{spire_top[0]:.1f}" cy="{spire_top[1]:.1f}" r="4" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/></g>')
    for idx, (x, y, w, d, h, era) in order:
        if not spire_done and x + y + (w + d) / 2 > spire_key:
            drawn.append(spire)
            spire_done = True
        crown = ""
        if era == 2:
            cx_, cy_ = P(x + w / 2, y + d / 2, h)
            crown = f'<circle class="pulse" style="animation-delay:{idx * .3:.1f}s" cx="{cx_:.1f}" cy="{cy_:.1f}" r="9" fill="url(#glow)"/>'
        drawn.append(f'<g class="r{era}" style="animation-delay:{(idx % 4) * .12:.2f}s">{box(x, y, w, d, h, p["eras"][era], era > 0, (idx * .7) % 3 if era > 0 else 0)}{crown}</g>')
    if not spire_done:
        drawn.append(spire)

    def arc(a, b, lift):
        pa, pb = P(*a), P(*b)
        mx, my = (pa[0] + pb[0]) / 2, min(pa[1], pb[1]) - lift
        return f"M{pa[0]:.1f} {pa[1]:.1f} Q{mx:.1f} {my:.1f} {pb[0]:.1f} {pb[1]:.1f}"

    bridges = "".join(f'<path d="{arc(a, b, 30)}" fill="none" stroke="{p["eras"][3][0]}" stroke-width="2" class="flow"/>' for a, b in BRIDGES)
    beams = "".join(
        f'<path d="{arc((x + w / 2, y + d / 2, h), (sx + sw / 2, sy + sd / 2, sh), 40)}" fill="none" stroke="{p["accent"]}" stroke-width="1.6" stroke-opacity=".8" class="flow" style="animation-delay:{i * .15:.2f}s"/>'
        for i, (x, y, w, d, h, era) in enumerate(BUILDINGS) if era in (1, 2))

    caps = []
    for i, (yr, title, l1, l2, l3) in enumerate(CAPTIONS):
        caps.append(f'''<g class="cap c{i}">
    <text x="56" y="150" font-size="13" font-weight="700" letter-spacing="2" fill="{p["accent"]}">CHAPTER {i + 1} · {yr}</text>
    <text x="54" y="194" font-size="36" font-weight="700" letter-spacing="-1" fill="{p["fg"]}">{title}</text>
    <text x="56" y="232" font-size="16" font-weight="600" fill="{p["fg"]}">{l1}</text>
    <text x="56" y="256" font-size="15" fill="{p["muted"]}">{l2}</text>
    <text x="56" y="280" font-size="15" fill="{p["muted"]}">{l3}</text>
  </g>''')
    ticks = "".join(
        f'<g><rect x="{56 + i * 64}" y="330" width="56" height="4" rx="2" fill="{p["road"]}"/>'
        f'<rect class="s{i}" x="{56 + i * 64}" y="330" width="56" height="4" rx="2" fill="{p["accent"]}"/>'
        f'<text x="{56 + i * 64}" y="354" font-size="11" font-weight="600" fill="{p["muted"]}" letter-spacing="1">{c[0]}</text></g>'
        for i, c in enumerate(CAPTIONS))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career as a city: warehouses in 2015, cloud towers by 2019, GenAI crowns in 2022, bridges to customers in 2024, and a central AI spire in 2026">
  <defs>
    <radialGradient id="glow"><stop offset="0" stop-color="{p["accent"]}" stop-opacity=".9"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="halo" cx=".65" cy=".45" r=".6"><stop offset="0" stop-color="{p["accent"]}" stop-opacity=".10"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
    <pattern id="winL" width="9" height="11" patternUnits="userSpaceOnUse" patternTransform="skewY(30)"><rect x="2" y="2" width="4" height="6" fill="#fff" fill-opacity=".18"/></pattern>
    <pattern id="winR" width="9" height="11" patternUnits="userSpaceOnUse" patternTransform="skewY(-30)"><rect x="2" y="2" width="4" height="6" fill="#000" fill-opacity=".18"/></pattern>
    <pattern id="litL" width="27" height="22" patternUnits="userSpaceOnUse" patternTransform="skewY(30)"><rect x="2" y="2" width="4" height="6" fill="{p["window"]}"/><rect x="20" y="13" width="4" height="6" fill="{p["window"]}"/></pattern>
  </defs>
  {keyframes()}
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{p["bg"]}" stroke="{p["road"]}"/>
  <rect width="{W}" height="{H}" rx="12" fill="url(#halo)"/>
  <g font-family="ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
    <text x="56" y="64" font-size="13" font-weight="600" letter-spacing="2" fill="{p["muted"]}">THE JOURNEY, BUILT ONE DISTRICT AT A TIME</text>
    {"".join(caps)}
    {ticks}
  </g>
  <polygon points="{ground}" fill="{p["ground"]}" stroke="{p["road"]}"/>
  {roads}
  {"".join(packets)}
  {"".join(drawn)}
  <g class="s3">{bridges}</g>
  <g class="s4">{beams}</g>
</svg>
'''
