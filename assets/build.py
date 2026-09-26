"""Regenerate the profile SVGs: python3 assets/build.py"""
from pathlib import Path

from city import city

OUT = Path(__file__).parent
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", fg="#e6edf3", muted="#8b949e", line="#21262d", card="#161b22", accent="#58a6ff", accent2="#3fb950"),
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", line="#d1d9e0", card="#f6f8fa", accent="#0969da", accent2="#1a7f37"),
}
MOTION = """<style>
  /* Base state is fully visible; animations only play in from a hidden start, so a renderer that skips them still shows everything. */
  .draw { stroke-dasharray: 1600; animation: draw 2.4s ease-out .2s backwards; }
  .pop { animation: pop .5s ease-out backwards; }
  @keyframes draw { from { stroke-dashoffset: 1600; } }
  @keyframes pop { from { opacity: 0; } }
  @media (prefers-reduced-motion: reduce) { .draw, .pop { animation: none; } }
</style>"""


def header(t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-label="Jagadeesh Thiruveedula, Forward Deployed AI Engineer">
  <defs>
    <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t['line']}" stroke-opacity=".6"/></pattern>
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{t['bg']}"/><stop offset=".55" stop-color="{t['bg']}" stop-opacity=".92"/><stop offset="1" stop-color="{t['bg']}" stop-opacity="0"/></linearGradient>
  </defs>
  {MOTION}
  <rect x=".5" y=".5" width="1199" height="259" rx="12" fill="{t['bg']}" stroke="{t['line']}"/>
  <rect x="1" y="1" width="1198" height="258" rx="12" fill="url(#g)"/>
  <rect x="1" y="1" width="1198" height="258" rx="12" fill="url(#fade)"/>
  <g font-family="{FONT}">
    <text x="64" y="84" fill="{t['accent']}" font-size="14" font-weight="600" letter-spacing="3">FORWARD DEPLOYED AI ENGINEER · DALLAS, TX</text>
    <text x="62" y="148" fill="{t['fg']}" font-size="54" font-weight="700" letter-spacing="-1.5">Jagadeesh Thiruveedula</text>
    <text x="64" y="196" fill="{t['muted']}" font-size="20">I take GenAI from demo to production inside enterprise teams.</text>
  </g>
  <rect x="64" y="220" width="48" height="3" rx="1.5" fill="{t['accent']}"/>
  <g stroke="{t['accent']}" stroke-width="1.5" fill="none">
    <path class="draw" d="M960 176L1010 96L1090 150L960 176M1010 96L1130 70M1090 150L1050 206" stroke-opacity=".55"/>
  </g>
  <g fill="{t['accent']}">
    <circle class="pop" style="animation-delay:.3s" cx="960" cy="176" r="5"/><circle class="pop" style="animation-delay:.6s" cx="1010" cy="96" r="6"/>
    <circle class="pop" style="animation-delay:.9s" cx="1090" cy="150" r="5"/><circle class="pop" style="animation-delay:1.2s" cx="1130" cy="70" r="4"/>
    <circle class="pop" style="animation-delay:1.5s" cx="1050" cy="206" r="4"/>
  </g>
</svg>
'''


# (year, role, company, proof, label above-left of dot?) — the curve rises, so above-left and below-right never cross it
MILESTONES = [
    (2015, "ETL Developer", "InnoMinds", "Enterprise warehouse pipelines", False),
    (2018, "Data Engineer", "DSO MCS Group", "Unified mainframe + Teradata", True),
    (2019, "Senior Data Engineer", "Charles Schwab", "Multi-PB to GCP · $1M+ saved", False),
    (2022, "Lead Data Engineer", "HCA Healthcare", "GenAI accelerators · 50% faster", True),
    (2024, "FD Data Architect", "NRG · Definity", "COBOL to GCP via GenAI", False),
    (2026, "FD AI Architect", "John Wiley &amp; Sons", "RAG over 50M+ docs · 95%", True),
]
ERAS = [(2015, 2019, "Data foundations"), (2019, 2022, "Cloud at scale"), (2022, 2026.6, "Applied GenAI")]


def arc(t):
    x = lambda yr: 90 + (yr - 2015) * 92
    y = lambda yr: 260 - (yr - 2015) ** 1.35 * 6
    pts = [(x(m[0]), y(m[0])) for m in MILESTONES]
    path = "M" + " ".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    eras = "".join(
        f'<rect x="{x(a):.0f}" y="345" width="{x(b) - x(a) - 6:.0f}" height="4" rx="2" fill="{t["accent2"] if i == 2 else t["line"]}"/>'
        f'<text x="{x(a):.0f}" y="370" fill="{t["fg"] if i == 2 else t["muted"]}" font-size="13" font-weight="600" letter-spacing="1.5">{n.upper()}</text>'
        for i, (a, b, n) in enumerate(ERAS)
    )
    nodes = []
    for i, ((yr, role, co, proof, up), (px, py)) in enumerate(zip(MILESTONES, pts)):
        last = i == len(MILESTONES) - 1
        ty = py - 58 if up else py + 30
        anchor = "end" if up else "start"
        tx = px + 8 if up else px - 8
        nodes.append(f'''<g class="pop" style="animation-delay:{0.3 + i * 0.35:.2f}s">
    {f'<circle cx="{px:.0f}" cy="{py:.0f}" r="14" fill="{t["accent"]}" fill-opacity=".15"/>' if last else ''}
    <circle cx="{px:.0f}" cy="{py:.0f}" r="6" fill="{t['bg']}" stroke="{t['accent']}" stroke-width="2.5"/>
    <text x="{tx:.0f}" y="{ty:.0f}" text-anchor="{anchor}" font-size="12" font-weight="700" fill="{t['accent']}" letter-spacing="1">{yr}{" · NOW" if last else ""}</text>
    <text x="{tx:.0f}" y="{ty + 18:.0f}" text-anchor="{anchor}" font-size="15" font-weight="600" fill="{t['fg']}">{role}</text>
    <text x="{tx:.0f}" y="{ty + 36:.0f}" text-anchor="{anchor}" font-size="12.5" fill="{t['muted']}">{co} · {proof}</text>
  </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="392" viewBox="0 0 1200 392" role="img" aria-label="Career arc from ETL developer in 2015 to forward deployed AI architect in 2026">
  {MOTION}
  <rect x=".5" y=".5" width="1199" height="391" rx="12" fill="{t['bg']}" stroke="{t['line']}"/>
  <g font-family="{FONT}">
    <text x="40" y="44" fill="{t['muted']}" font-size="13" font-weight="600" letter-spacing="2">ELEVEN YEARS, ONE DIRECTION</text>
    <path d="{path}" fill="none" stroke="{t['line']}" stroke-width="2"/>
    <path class="draw" d="{path}" fill="none" stroke="{t['accent']}" stroke-width="2.5" stroke-linecap="round"/>
    {"".join(nodes)}
    {eras}
  </g>
</svg>
'''


STEPS = [
    ("01", "Embed", "Sit with the team that owns", "the problem. Find the real metric."),
    ("02", "Prototype", "Working slice on their data", "in days, not a slide deck."),
    ("03", "Evaluate", "RAGAS, LLM-as-judge, human", "review. Prove it before scaling."),
    ("04", "Harden", "Guardrails, observability, cost", "controls, handover playbook."),
]


def flow(t):
    w, gap, x0 = 262, 30, 40
    cards = []
    for i, (n, title, l1, l2) in enumerate(STEPS):
        cx = x0 + i * (w + gap)
        arrow = "" if i == len(STEPS) - 1 else f'<path d="M{cx + w + 6} 120h{gap - 12}m-6 -5l6 5-6 5" fill="none" stroke="{t["muted"]}" stroke-width="1.5"/>'
        cards.append(f'''<g class="pop" style="animation-delay:{0.2 + i * 0.3:.1f}s">
    <rect x="{cx}" y="64" width="{w}" height="112" rx="10" fill="{t['card']}" stroke="{t['accent'] if i == 3 else t['line']}"/>
    <text x="{cx + 22}" y="98" font-size="12" font-weight="700" fill="{t['accent']}" letter-spacing="1.5">{n}</text>
    <text x="{cx + 52}" y="98" font-size="17" font-weight="600" fill="{t['fg']}">{title}</text>
    <text x="{cx + 22}" y="130" font-size="13" fill="{t['muted']}">{l1}</text>
    <text x="{cx + 22}" y="150" font-size="13" fill="{t['muted']}">{l2}</text>
  </g>{arrow}''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="210" viewBox="0 0 1200 210" role="img" aria-label="How I ship: embed, prototype, evaluate, harden">
  {MOTION}
  <rect x=".5" y=".5" width="1199" height="209" rx="12" fill="{t['bg']}" stroke="{t['line']}"/>
  <g font-family="{FONT}">
    <text x="40" y="42" fill="{t['muted']}" font-size="13" font-weight="600" letter-spacing="2">HOW AN ENGAGEMENT RUNS</text>
    {"".join(cards)}
  </g>
</svg>
'''


for name, t in THEMES.items():
    for kind, fn in (("header", header), ("arc", arc), ("flow", flow)):
        (OUT / f"{kind}-{name}.svg").write_text(fn(t))
    (OUT / f"city-{name}.svg").write_text(city(name))
