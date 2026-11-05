#!/usr/bin/env python3
"""Build the hand-designed profile SVGs. Standard library only; no network calls.

Run from any directory: python3 scripts/build_assets.py
Metrics and contribution data are owned by their workflows, never this script.
"""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, LINE = "#080E19", "#0D1A2A", "#263E50"
WHITE, MUTED, CYAN = "#F2F6FA", "#A4B7C7", "#8CC8D8"


def text(x, y, value, size=18, color=WHITE, weight=400, mono=False, spacing=0, anchor="start", extra=""):
    font = "'SFMono-Regular',Consolas,'Liberation Mono',monospace" if mono else "'Segoe UI',Arial,Helvetica,sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}" {extra}>{escape(value)}</text>'


def rect(x, y, w, h, fill=PANEL, stroke=LINE, radius=12, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" {extra}/>'


def path(d, color=LINE, width=1, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def circle(x, y, r, fill="none", stroke=LINE, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'


def label(x, y, value, size=12, color=CYAN):
    return text(x, y, value, size, color, 500, True, 1.6)


def start(width, height, title, description, grid=False):
    defs = '''<defs>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0D1A2A"/><stop offset="1" stop-color="#080E19"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#32677B" stop-opacity=".26"/><stop offset="1" stop-color="#32677B" stop-opacity="0"/></radialGradient>
<radialGradient id="planet" cx=".3" cy=".25" r=".8"><stop stop-color="#203C50"/><stop offset=".7" stop-color="#0D1A2A"/><stop offset="1" stop-color="#080E19"/></radialGradient>
<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#8CC8D8" stroke-opacity=".055"/></pattern>
</defs>'''
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>', f'<desc id="desc">{escape(description)}</desc>', defs,
            rect(.5, .5, width-1, height-1, "url(#surface)", LINE, 16),
            rect(1, 1, width-2, height-2, "url(#grid)", "none", 16) if grid else ""]


def save(name, parts):
    target = ROOT / "assets" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(parts) + "\n</svg>\n", encoding="utf-8")


def static_variant(name):
    """A picture-source fallback for clients that don't pass motion preferences to SVGs."""
    source = ROOT / "assets" / name
    content = source.read_text(encoding="utf-8")
    content = re.sub(r"<style>.*?</style>", "", content, flags=re.S)
    if "typing" in name:
        content = content.replace("</svg>", '<style>.phrase{display:none}.p1{display:inline}.reveal{width:var(--line-width)}</style></svg>')
    source.with_name(source.stem+"-static.svg").write_text(content, encoding="utf-8")


def heading(parts, w, number, section, aside="", mobile=False):
    x = 26 if mobile else 40
    parts += [label(x, 39 if mobile else 42, f"{number} / {section}"),
              path(f"M{x} {58 if mobile else 62}H{w-x}")]
    if aside and not mobile:
        parts.append(text(w-x, 42, aside, 11, MUTED, 400, True, .8, "end"))


def orbital(x, y, scale=1):
    return f'''<g transform="translate({x} {y}) scale({scale})">
<circle r="205" fill="url(#halo)"/>
<g fill="none" stroke="#52758A" stroke-width=".8">
<circle r="133" opacity=".45"/><circle r="145" opacity=".25" stroke-dasharray="2 11"/>
<path d="M-158 0H158M0-154V154" opacity=".2"/>
</g>
<g transform="rotate(-27)">
<ellipse rx="174" ry="64" fill="none" stroke="#8CC8D8" stroke-opacity=".45"/>
<ellipse rx="174" ry="64" fill="none" stroke="#8CC8D8" stroke-dasharray="25 18 2 86" stroke-opacity=".55" class="orbit-dashes"/>
</g>
<ellipse rx="158" ry="58" transform="rotate(48)" fill="none" stroke="#52758A" stroke-opacity=".3"/>
<circle r="80" fill="url(#planet)" stroke="#62869B" stroke-width=".85"/>
<g fill="none" stroke="#6D92A5" stroke-width=".7" opacity=".33">
<ellipse rx="35" ry="80"/><ellipse rx="63" ry="80"/>
<ellipse rx="80" ry="26"/><path d="M-72-35Q0-12 72-35M-72 35Q0 12 72 35M-80 0H80M0-80V80"/>
</g>
<path d="M-56-56A79 79 0 0 1 57-55" stroke="#AEDAE4" stroke-width="1.3" fill="none"/>
<g transform="rotate(-27) scale(1 .368)">
<g class="orbiter"><g transform="translate(174 0) scale(1 2.717) rotate(27)">
<circle r="18" fill="#8CC8D8" opacity=".06"/>
<g fill="#152D40" stroke="#B9DCE5" stroke-width="1.2" transform="rotate(-18)">
<rect x="-5" y="-6" width="10" height="12" rx="1"/>
<rect x="-25" y="-8" width="15" height="16"/><rect x="10" y="-8" width="15" height="16"/>
<path d="M-10 0H-5M5 0H10M-20-8V8M-15-8V8M15-8V8M20-8V8M-25 0H-10M10 0H25M0-6V-14"/>
</g></g></g></g>
<circle cx="-135" cy="-96" r="2" fill="#8CC8D8"/>
<path d="M-129-96H-102L-88-82" fill="none" stroke="#56788B" stroke-width=".7"/>
<circle cx="125" cy="109" r="2" fill="#8CC8D8"/>
<path d="M85 123H111L125 109" fill="none" stroke="#56788B" stroke-width=".7"/>
</g>'''


MOTION = '''<style>
.orbiter{animation:orbit 32s linear infinite;transform-origin:0 0}
.orbit-dashes{animation:drift 40s linear infinite}
.entrance{animation:arrive 1.1s ease-out both}
@keyframes orbit{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes drift{to{stroke-dashoffset:-520}}
@keyframes arrive{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){.orbiter,.orbit-dashes,.entrance{animation:none!important}}
</style>'''


def hero(mobile=False):
    w, h, x = (420, 496, 26) if mobile else (960, 338, 40)
    p = start(w, h, "SENYOBRAHHH — Software • Robotics • Space", "Enyo's engineering journal. An animated satellite circles a blueprint globe. Motion pauses when reduced motion is requested.", True)
    p += [MOTION]
    if mobile:
        p += [label(x, 37, "ENYO / ENGINEERING JOURNAL", 11), orbital(210, 245, .88),
              text(x, 91, "SENYOBRAHHH", 39, WHITE, 700, spacing=-1.4),
              text(x, 122, "Software • Robotics • Space", 18, CYAN, 500),
              path("M26 433H394"), label(x, 463, "CURIOSITY. ENGINEERING. EXPLORATION.", 10)]
    else:
        p += [label(x, 38, "ENYO / ENGINEERING JOURNAL"),
              text(920, 38, "LEARNING IN PUBLIC", 11, MUTED, 400, True, 1.4, "end"),
              orbital(758, 182), '<g class="entrance">',
              text(x-2, 158, "SENYOBRAHHH", 63, WHITE, 700, spacing=-2.4),
              text(x, 199, "Software • Robotics • Space", 25, CYAN, 400),
              path("M40 231H92", CYAN, 2),
              text(x, 265, "Curiosity. Engineering. Exploration.", 17, MUTED), '</g>',
              path("M40 298H920"), label(x, 320, "DEVELOPER  /  CURIOUS BUILDER", 10),
              text(920, 320, "BUILD. TEST. LEARN. REPEAT.", 10, MUTED, 400, True, 1.4, "end")]
    save("mobile/banner.svg" if mobile else "banner.svg", p)


def typing(mobile=False):
    w, h, size = (420, 55, 15) if mobile else (960, 60, 18)
    phrases = ["SQL / C# / Python", "Software + Robotics + Space", "Fitness / Gaming / Travel", "Building skills, one project at a time"]
    if mobile:
        phrases[-1] = "One project at a time"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">SQL / C# / Python. Software + Robotics + Space. Fitness / Gaming / Travel. Building skills, one project at a time.</title>',
         '<style>.phrase{opacity:0;animation:show 20s steps(1,end) infinite}.p2{animation-delay:5s}.p3{animation-delay:10s}.p4{animation-delay:15s}.reveal{animation:type 5s steps(var(--chars),end) infinite}@keyframes show{0%,24.99%{opacity:1}25%,100%{opacity:0}}@keyframes type{0%{width:0}42%,82%{width:var(--line-width)}98%,100%{width:0}}@media(prefers-reduced-motion:reduce){.phrase,.reveal{animation:none!important}.phrase{opacity:0}.p1{opacity:1}.reveal{width:var(--line-width)}}</style>']
    for i, value in enumerate(phrases, 1):
        tw = len(value) * size * .61
        p += [f'<defs><clipPath id="type{i}"><rect class="reveal" x="0" y="0" width="{tw+10}" height="{h}" style="--line-width:{tw+10}px;--chars:{len(value)}"/></clipPath></defs>',
              f'<g transform="translate({(w-tw)/2:.2f} 0)" class="phrase p{i}"><g clip-path="url(#type{i})">',
              text(0, 34, value, size, CYAN, 400, True), '</g></g>']
    save("mobile/typing.svg" if mobile else "typing.svg", p)


def overview(mobile=False):
    w, h, x = (420, 564, 26) if mobile else (960, 356, 40)
    p = start(w, h, "Hi, I'm Enyo. Developer working in data engineering.", "Current toolkit: SQL for relational data, C# for backend development, and Python for scripting and data. Learning electronics and robotics is the next direction.")
    heading(p, w, "01", "PROFILE", "PRESENT + DIRECTION", mobile)
    p += [text(x, 107 if mobile else 116, "Code today.", 31 if mobile else 35, WHITE, 600, spacing=-.7),
          text(x, 147 if mobile else 159, "Physical systems tomorrow.", 25 if mobile else 32, WHITE, 600, spacing=-.6)]
    for j, line in enumerate(["I'm Enyo. I work in data engineering,", "with SQL, C# and Python.", "My next chapter: electronics and robotics."]):
        p.append(text(x, (190 if mobile else 204)+27*j, line, 16 if mobile else 18, MUTED))
    tx, ty = (26, 290) if mobile else (599, 105)
    if not mobile:
        p.append(path("M559 91V281"))
    p.append(label(tx, ty, "CURRENT TOOLKIT", 11))
    for i, (lang, context) in enumerate([("SQL", "Relational data"), ("C#", "Backend development"), ("Python", "Scripting & data")]):
        y = ty+40+i*57
        p += [text(tx, y, lang, 24, WHITE, 600),
              text(w-x, y-1, context, 14, MUTED, anchor="end"),
              path(f"M{tx} {y+17}H{w-x}")]
    fy = 516 if mobile else 310
    p += [path(f"M{x} {fy}H{w-x}"), label(x, fy+27, "FOCUS", 10),
          text(x+64, fy+27, "Data workflows · Backend fundamentals", 12 if mobile else 14, MUTED)]
    save("mobile/dashboard-overview.svg" if mobile else "dashboard-overview.svg", p)


def icon(kind, x, y):
    paths = {
        "space": '<ellipse cx="20" cy="20" rx="22" ry="9" transform="rotate(-35 20 20)"/><circle cx="20" cy="20" r="12"/><path d="M20 8C8 15 8 25 20 32M20 8C32 15 32 25 20 32"/>',
        "robot": '<path d="M4 36H36M10 36V29L21 17L15 8M15 8L26 4L33 10M30 7L34 3M33 10L37 9"/><circle cx="21" cy="17" r="4"/><circle cx="10" cy="29" r="3"/><path d="M30 25V35M25 30H35"/>',
        "design": '<path d="M20 2L37 12V31L20 41L3 31V12ZM3 12L20 22L37 12M20 22V41M20 2V22"/><path d="M3 31L20 22L37 31" stroke-dasharray="2 4"/>'
    }
    return f'<g transform="translate({x} {y})" fill="none" stroke="{CYAN}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'


def interests(mobile=False):
    w, h, x = (420, 704, 26) if mobile else (960, 368, 40)
    p = start(w, h, "What pulls me forward", "Engineering interests: spacecraft, satellites, avionics, embedded systems, autonomous robots, robotic arms, medical and surgical technology, CAD, CNC, 3D printing, experiments and prototypes. Outside engineering: fitness, gaming, travel, cars and entrepreneurship.")
    heading(p, w, "02", "CURIOSITY", "BEYOND THE TERMINAL", mobile)
    data = [("space", "Space & embedded", ["Spacecraft, satellites, avionics.", "Microcontrollers & electronics."]),
            ("robot", "Robotics & medtech", ["Autonomous systems & arms.", "Medical & surgical technology."]),
            ("design", "Design & prototyping", ["CAD, CNC & 3D printing.", "Mechanisms, ideas & experiments."])]
    for i, (kind, title, lines) in enumerate(data):
        xx, yy = (x, 96+i*162) if mobile else (x+i*301, 96)
        if i and not mobile:
            p.append(path(f"M{xx-19} 96V255"))
        p += [icon(kind, xx, yy), text(xx, yy+74, title, 22 if mobile else 21, WHITE, 600)]
        for j, line in enumerate(lines):
            p.append(text(xx, yy+103+25*j, line, 16, MUTED))
    y = 599 if mobile else 288
    p += [path(f"M{x} {y}H{w-x}"), label(x, y+30, "OFF THE CLOCK", 11)]
    if mobile:
        p += [text(x, y+58, "Fitness · Gaming · Travel", 17, WHITE),
              text(x, y+84, "Cars · Entrepreneurship", 17, WHITE)]
    else:
        p += [text(x+174, y+30, "Fitness · Gaming · Travel · Cars · Entrepreneurship", 18, WHITE),
              text(x+174, y+57, "A life beyond the screen. A curiosity that follows me everywhere.", 14, MUTED)]
    save("mobile/dashboard-interests.svg" if mobile else "dashboard-interests.svg", p)


STAGES = [
    ("Sensors & circuits", "Arduino · electronics fundamentals"),
    ("Telemetry & logging", "ESP32 · wireless data · SD logging"),
    ("Embedded foundations", "STM32 · IMUs · sensor fusion"),
    ("Motion & control", "Motors · feedback loops · PID"),
    ("Autonomous robotics", "Rovers · robotic arms · integration"),
    ("Custom hardware", "PCB design · RTOS architecture"),
    ("Modular avionics", "Flight computers · CAN bus"),
    ("Integrated testbeds", "Spacecraft simulators · robotics"),
]


def roadmap(mobile=False):
    w, h, x = (420, 1086, 26) if mobile else (960, 634, 40)
    p = start(w, h, "Engineering flight plan — all eight stages are planned", "A learning roadmap, not completed projects. " + "; ".join(f"{i+1}. {a}: {b}" for i, (a,b) in enumerate(STAGES)) + ". First planned build: an Arduino sensor station.", True)
    heading(p, w, "03", "FLIGHT PLAN", "ALL STAGES / PLANNED", mobile)
    p += [text(x, 108 if mobile else 113, "From code to systems." if mobile else "From code to physical systems.", 26 if mobile else 32, WHITE, 600, spacing=-.6),
          text(x, 139 if mobile else 147, "A learning path. Every stage below is planned.", 14 if mobile else 17, MUTED)]
    if not mobile:
        p += [label(40, 192, "01—04 / FOUNDATIONS", 11), label(506, 192, "05—08 / SYSTEMS", 11),
              path("M57 232V505", "#365568", 1.4), path("M523 232V505", "#365568", 1.4)]
    else:
        p.append(path("M43 195V902", "#365568", 1.4))
    for i, (title, desc) in enumerate(STAGES):
        xx, yy = (x, 195+i*100) if mobile else (40+(i//4)*466, 236+(i%4)*87)
        p += [circle(xx+17, yy-4, 17, BG, "#537C8E"),
              text(xx+17, yy, f"{i+1:02}", 12, CYAN, 500, True, anchor="middle"),
              text(xx+48, yy+1, title, 21, WHITE, 600),
              text(xx+48, yy+28, desc, 14 if mobile else 16, MUTED)]
    y = 988 if mobile else 553
    p += [rect(x, y, w-2*x, 71, "#102334", "#345366", 9),
          label(x+18, y+25, "FIRST PLANNED BUILD", 10),
          text(x+18, y+51, "Arduino sensor station", 20, WHITE, 500)]
    if not mobile:
        p += [text(898, y+42, "Start small. Document the build. Keep going.", 15, MUTED, anchor="end")]
    save("mobile/dashboard-roadmap.svg" if mobile else "dashboard-roadmap.svg", p)


def telemetry_heading(mobile=False):
    w, h, x = (420, 146, 26) if mobile else (960, 145, 40)
    p = start(w, h, "GitHub telemetry", "Contribution history, repository languages and recent coding patterns, generated from GitHub data by Lowlighter Metrics.")
    heading(p, w, "04", "ACTIVITY", "GITHUB / TELEMETRY", mobile)
    p += [text(x, 106, "Signals from the work.", 27 if mobile else 32, WHITE, 600, spacing=-.6),
          text(x, 131, "Contributions · Repository languages · Coding patterns", 12 if mobile else 16, MUTED)]
    save("mobile/telemetry-heading.svg" if mobile else "telemetry-heading.svg", p)


def empty_metrics():
    # An explicit empty state. Never decorative numbers, fake bars or a fake graph.
    for mobile in (False, True):
        w, h, x = (480, 170, 28) if mobile else (960, 162, 40)
        p = start(w, h, "Activity dashboard awaiting its first successful sync", "No statistics are shown until the Lowlighter Metrics workflow successfully generates real data.")
        p += [circle(x+7, 34, 4, "none", CYAN), label(x+23, 38, "AWAITING FIRST SYNC", 11),
              text(x, 80, "The work will speak for itself.", 25 if mobile else 28, WHITE, 500),
              text(x, 113, "Contribution history, languages and coding patterns.", 15 if mobile else 17, MUTED),
              text(x, 139, "Real data appears after the first successful refresh.", 14 if mobile else 16, MUTED)]
        name = "metrics/github-mobile.svg" if mobile else "metrics/github.svg"
        if not (ROOT / "assets" / name).exists():
            save(name, p)


def footer(mobile=False):
    w, h, x = (420, 130, 26) if mobile else (960, 126, 40)
    p = start(w, h, "Stay curious. Build things. Keep moving.", "Build. Test. Learn. Repeat.")
    p += [path(f"M{x} 31H{x+38}", CYAN, 2),
          text(x, 72, "Stay curious. Keep building.", 25 if mobile else 32, WHITE, 500, spacing=-.6),
          label(x, 102, "BUILD. TEST. LEARN. REPEAT.", 10)]
    if not mobile:
        p.append(text(920, 72, "ENYO / SENYOBRAHHH", 11, MUTED, 400, True, 1, "end"))
    save("mobile/footer.svg" if mobile else "footer.svg", p)


def social(name):
    p = ['<svg xmlns="http://www.w3.org/2000/svg" width="142" height="40" viewBox="0 0 142 40" role="img" aria-labelledby="title">', f'<title id="title">{name}</title>', rect(.5,.5,141,39,PANEL,LINE,8), text(18,26,name,14,WHITE,500), path("M115 25L125 15M117 15H125V23", CYAN, 1.3)]
    save(f"social/{name.lower()}.svg", p)


if __name__ == "__main__":
    for mobile in (False, True):
        for build in (hero, typing, overview, interests, roadmap, telemetry_heading, footer):
            build(mobile)
    empty_metrics()
    social("LinkedIn")
    social("Instagram")
    for name in ("banner.svg", "typing.svg", "mobile/banner.svg", "mobile/typing.svg"):
        static_variant(name)
    print("Built profile assets; existing generated metrics were preserved.")
