#!/usr/bin/env python3
"""Build the portfolio into _site/ from content/site.json.

One page per language: / (English), /fr/ (French), /ar/ (Arabic, right-to-left).
Standard library only. Run:  python3 build.py   then open _site/index.html
or serve it:  python3 -m http.server -d _site
"""

import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
DATA = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
S = DATA["shared"]
LANGS = DATA["langs"]
PATHS = {"en": "/", "fr": "/fr/", "ar": "/ar/"}
RTL = {"ar"}


def e(text):
    return escape(text, quote=True)


# --------------------------------------------------------------------------
# Hero diagram: the AIS pipeline as a small DAG, mirrored for right-to-left.
# --------------------------------------------------------------------------
NODES = {  # id: (label, depth)
    "src": ("NOAA AIS", 0), "clean": ("clean", 1), "metrics": ("metrics", 2),
    "db": ("PostgreSQL", 3), "api": ("FastAPI", 4), "dash": ("Streamlit", 4),
}
EDGES = [("src", "clean"), ("clean", "metrics"), ("metrics", "db"), ("db", "api"), ("db", "dash")]
# Node centres for each layout. Horizontal for wide screens, vertical for phones.
LAYOUTS = {
    "h": dict(W=640, H=230, NW=104, NH=38, pos={
        "src": (54, 115), "clean": (184, 115), "metrics": (314, 115),
        "db": (444, 115), "api": (584, 58), "dash": (584, 172)}),
    "v": dict(W=320, H=330, NW=128, NH=38, pos={
        "src": (160, 22), "clean": (160, 92), "metrics": (160, 162),
        "db": (160, 232), "api": (82, 306), "dash": (238, 306)}),
}
STEP, START, TRAVEL = 0.55, 0.5, 0.5  # seconds


def dag_svg(kind, rtl):
    L = LAYOUTS[kind]
    W, H, NW, NH = L["W"], L["H"], L["NW"], L["NH"]
    pos = {k: ((W - x) if rtl else x, y) for k, (x, y) in L["pos"].items()}
    parts = [
        f'<svg class="dag-svg dag-{kind}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="dag-cap" xmlns="http://www.w3.org/2000/svg">'
    ]
    for i, (a, b) in enumerate(EDGES):
        (ax, ay), (bx, by) = pos[a], pos[b]
        if kind == "h":
            sgn = -1 if rtl else 1
            x1, y1, x2, y2 = ax + sgn * NW / 2, ay, bx - sgn * NW / 2, by
            mid = (x1 + x2) / 2
            d = f"M{x1},{y1} C{mid},{y1} {mid},{y2} {x2},{y2}"
        else:
            x1, y1, x2, y2 = ax, ay + NH / 2, bx, by - NH / 2
            mid = (y1 + y2) / 2
            d = f"M{x1},{y1} C{x1},{mid} {x2},{mid} {x2},{y2}"
        t = START + NODES[a][1] * STEP
        pid = f"{kind}e{i}"
        parts.append(f'<path id="{pid}" class="edge" d="{d}"/>')
        parts.append(
            f'<circle class="packet" r="4" opacity="0">'
            f'<animateMotion dur="{TRAVEL}s" begin="{t:.2f}s" fill="freeze"><mpath href="#{pid}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.8;1" '
            f'dur="{TRAVEL}s" begin="{t:.2f}s" fill="freeze"/></circle>'
        )
    for nid, (cx, cy) in pos.items():
        label, depth = NODES[nid]
        lit = START + (depth - 1) * STEP + TRAVEL if depth else START - 0.2
        parts.append(
            f'<g class="node" style="--lit:{lit:.2f}s">'
            f'<rect x="{cx - NW / 2}" y="{cy - NH / 2}" width="{NW}" height="{NH}" rx="5"/>'
            f'<text x="{cx}" y="{cy + 5}" text-anchor="middle">{e(label)}</text></g>'
        )
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
def fonts(lang):
    fam = "family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600"
    if lang == "ar":
        fam += "&family=IBM+Plex+Sans+Arabic:wght@400;500;600"
    return (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">'
    )


def page(lang):
    L = LANGS[lang]
    rtl = lang in RTL
    url = S["url"] + PATHS[lang]

    alternates = "".join(
        f'<link rel="alternate" hreflang="{k}" href="{S["url"]}{p}">' for k, p in PATHS.items()
    ) + f'<link rel="alternate" hreflang="x-default" href="{S["url"]}/">'

    switch = "".join(
        f'<li><a href="{PATHS[k]}" lang="{k}" hreflang="{k}"'
        + (' aria-current="page"' if k == lang else "")
        + f'>{e(v["label"])}</a></li>'
        for k, v in LANGS.items()
    )
    nav = "".join(f'<li><a href="#{k}">{e(v)}</a></li>' for k, v in L["nav"].items())

    projects = []
    for p in S["projects"]:
        t = L["projects"][p["id"]]
        link = f'<a class="proj-link" href="{e(p["repo"])}">{e(L["code"])}</a>' if p["repo"] else ""
        projects.append(
            f'<article class="proj" id="p-{p["id"]}"><h3>{e(t["title"])}</h3>'
            f'<p>{e(t["desc"])}</p><p class="stack" dir="ltr">{e(p["stack"])}</p>{link}</article>'
        )

    roles = "".join(
        f'<li><p class="when">{e(r["dates"])}</p><h3>{e(r["role"])}</h3>'
        f'<p class="org">{e(r["org"])}</p><ul>'
        + "".join(f"<li>{e(b)}</li>" for b in r["bullets"])
        + "</ul></li>"
        for r in L["experience"]
    )

    skills = "".join(
        f'<div><dt>{e(L["skill_groups"][k])}</dt><dd dir="ltr">{e(v)}</dd></div>'
        for k, v in S["skills"].items()
    )
    edu = "".join(
        f'<li><span class="deg">{e(x["degree"])}</span>'
        f'<span class="sch">{e(x["school"])}, {e(x["year"])}</span></li>'
        for x in L["education"]
    )
    certs = "".join(f'<li dir="ltr">{e(c)}</li>' for c in S["certs"])
    outside = L["outside"].replace("{chess}", e(S["chess"]))
    mail = f'mailto:{S["email"]}'
    name = L.get("name", S["name"])

    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L["title"])}</title>
<meta name="description" content="{e(L["meta"])}">
<link rel="canonical" href="{url}">
{alternates}
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(L["title"])}">
<meta property="og:description" content="{e(L["meta"])}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#0d6e70">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{fonts(lang)}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">{e(L["skip"])}</a>
<header class="top">
  <div class="wrap top-in">
    <a class="home" href="{PATHS[lang]}">{e(name)}</a>
    <nav class="sections" aria-label="{e(L["sectionsnav"])}"><ul>{nav}</ul></nav>
    <nav class="langs" aria-label="{e(L["langnav"])}"><ul>{switch}</ul></nav>
  </div>
</header>

<main id="main">
<section class="hero wrap">
  <div class="hero-text">
    <p class="status"><span class="dot" aria-hidden="true"></span>{e(L["status"])}</p>
    <h1>{e(name)}</h1>
    <p class="role">{e(L["role"])}</p>
    <p class="intro">{e(L["intro"])}</p>
    <p class="actions">
      <a class="btn btn-main" href="{mail}">{e(L["cta_email"])}</a>
      <a class="btn" href="{e(S["linkedin"])}">LinkedIn</a>
      <a class="btn" href="{e(S["github"])}">GitHub</a>
    </p>
  </div>
  <figure class="dag">
    {dag_svg("h", rtl)}{dag_svg("v", rtl)}
    <figcaption id="dag-cap">{e(L["dag_caption"])} <a href="#p-ais">{e(L["dag_link"])}</a></figcaption>
  </figure>
</section>

<section class="sec wrap" id="projects">
  <h2>{e(L["projects_title"])}</h2>
  <div class="sec-body">
    {"".join(projects)}
    <p class="more"><a href="{e(S["github"])}?tab=repositories">{e(L["more"])}</a></p>
  </div>
</section>

<section class="sec wrap" id="experience">
  <h2>{e(L["experience_title"])}</h2>
  <div class="sec-body"><ol class="timeline">{roles}</ol></div>
</section>

<section class="sec wrap" id="skills">
  <h2>{e(L["skills_title"])}</h2>
  <div class="sec-body"><dl class="skills">{skills}</dl></div>
</section>

<section class="sec wrap" id="education">
  <h2>{e(L["education_title"])}</h2>
  <div class="sec-body">
    <ul class="edu">{edu}</ul>
    <h3 class="sub">{e(L["certs_title"])}</h3>
    <ul class="certs">{certs}</ul>
    <p class="outside">{outside}</p>
  </div>
</section>

<section class="sec wrap" id="contact">
  <h2>{e(L["contact_title"])}</h2>
  <div class="sec-body">
    <p>{e(L["contact_text"])}</p>
    <p><a class="mail" href="{mail}" dir="ltr">{e(S["email"])}</a></p>
    <p class="links"><a href="{e(S["linkedin"])}">LinkedIn</a> <a href="{e(S["github"])}">GitHub</a></p>
  </div>
</section>
</main>

<footer class="foot wrap">
  <p>© {date.today().year} <bdi>{e(name)}</bdi>. {e(L["footer"])}</p>
</footer>
</body>
</html>
"""


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for lang, path in PATHS.items():
        target = OUT / path.strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(lang), encoding="utf-8")
    shutil.copy(ROOT / "404.html", OUT / "404.html")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(PATHS)} pages into {OUT}")


if __name__ == "__main__":
    build()
