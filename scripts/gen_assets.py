#!/usr/bin/env python3
"""Generate the profile README's SVG panels in the pixshaft.com visual language.

Run from the repo root:  python3 scripts/gen_assets.py
Palette / type / glass / aurora are lifted from shaft-web's globals.css and the
snap/pixshaft/*.svg panels in CeuiLiSA/Pixiv-Shaft so the profile reads as the same brand.
Animations are SMIL + CSS keyframes inside the SVG — GitHub renders both when the SVG is
embedded through <img>.
"""
from __future__ import annotations

import base64
import html
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

INK = "#07060f"
BRAND = "#7c6cff"
ACCENT = "#22d3ee"
GLOW = "#a78bfa"
PINK = "#f6339a"
AMBER = "#fbbf24"
GREEN = "#34d399"
FONT = ("Inter, Sora, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
        "'PingFang SC', 'Hiragino Sans GB', 'Noto Sans CJK SC', 'Microsoft YaHei', system-ui, sans-serif")
LOGO_URL = "https://raw.githubusercontent.com/CeuiLiSA/Pixiv-Shaft/classic/snap/pixshaft/shaft-logo.png"


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def text_width(s: str, size: float, weight: int = 600) -> float:
    """Rough Inter advance-width estimate; generous so pills never clip on other fonts."""
    factor = 0.64 if weight >= 700 else 0.60
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o > 0x2E7F:          # CJK / emoji
            w += size * 1.05
        elif ch in "iljI.,'·:| ":
            w += size * 0.30
        elif ch.isupper() or ch in "mw@":
            w += size * factor * 1.18
        else:
            w += size * factor
    return w


def defs_common(prefix: str) -> str:
    return f"""
  <linearGradient id="{prefix}-brand" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BRAND}"/><stop offset="1" stop-color="#5b6ee1"/>
  </linearGradient>
  <linearGradient id="{prefix}-text" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#d9d4ff"/><stop offset="1" stop-color="{ACCENT}"/>
    <animate attributeName="x1" values="-0.6;0.4;-0.6" dur="7s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="0.7;1.7;0.7" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <radialGradient id="{prefix}-a1" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{BRAND}" stop-opacity=".75"/><stop offset="1" stop-color="{BRAND}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{prefix}-a2" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity=".45"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{prefix}-a3" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{PINK}" stop-opacity=".35"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
  </radialGradient>
  <filter id="{prefix}-grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .06 0"/>
  </filter>
  <filter id="{prefix}-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
  <pattern id="{prefix}-grid" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="#ffffff" fill-opacity=".07"/>
  </pattern>
"""


def aurora(prefix: str, w: int, h: int, scale: float = 1.0) -> str:
    """Three drifting blobs, like hero.tsx's blurred radial gradients."""
    r1, r2, r3 = 420 * scale, 300 * scale, 280 * scale
    return f"""
  <g filter="url(#{prefix}-blur)" opacity=".9">
    <circle cx="{w*0.22:.0f}" cy="{h*0.1:.0f}" r="{r1:.0f}" fill="url(#{prefix}-a1)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 60 30; -30 20; 0 0" dur="18s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{w*0.82:.0f}" cy="{h*0.25:.0f}" r="{r2:.0f}" fill="url(#{prefix}-a2)">
      <animateTransform attributeName="transform" type="translate" values="0 0; -50 40; 20 -30; 0 0" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{w*0.6:.0f}" cy="{h*0.95:.0f}" r="{r3:.0f}" fill="url(#{prefix}-a3)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 40 -40; -40 10; 0 0" dur="26s" repeatCount="indefinite"/>
    </circle>
  </g>
  <rect width="{w}" height="{h}" fill="url(#{prefix}-grid)"/>
  <rect width="{w}" height="{h}" filter="url(#{prefix}-grain)" opacity=".6"/>
"""


def panel_open(prefix: str, w: int, h: int, title: str, rx: int = 28, scale: float = 1.0) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<title>{title}</title>
<defs>{defs_common(prefix)}
  <clipPath id="{prefix}-clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
</defs>
<g clip-path="url(#{prefix}-clip)">
  <rect width="{w}" height="{h}" rx="{rx}" fill="{INK}"/>
  {aurora(prefix, w, h, scale)}
"""


def panel_close(w: int, h: int, rx: int = 28) -> str:
    return f"""</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="#ffffff" stroke-opacity=".10"/>
</svg>
"""


def pill(x: float, y: float, label: str, dot: str | None = None, size: float = 15,
         fill: str = "#ffffff", fill_op: float = .88, bg_op: float = .06, weight: int = 600) -> tuple[str, float]:
    pad = 22
    dot_w = 22 if dot else 0
    w = pad * 2 + dot_w + text_width(label, size, weight)
    h = size * 2.4
    parts = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="#ffffff" fill-opacity="{bg_op}" stroke="#ffffff" stroke-opacity=".12"/>']
    if dot:
        parts.append(f'<circle cx="{x+pad+4:.1f}" cy="{y+h/2:.1f}" r="4.5" fill="{dot}"/>')
    parts.append(f'<text x="{x+pad+dot_w:.1f}" y="{y+h/2+size*0.36:.1f}" font-family="{FONT}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}" fill-opacity="{fill_op}">{label}</text>')
    return "".join(parts), w


def button(x: float, y: float, label: str, primary: bool, prefix: str, size: float = 17) -> tuple[str, float]:
    pad = 28
    w = pad * 2 + text_width(label, size, 700)
    h = 50
    if primary:
        bg = f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="url(#{prefix}-brand)"/>'
        color = "#ffffff"
    else:
        bg = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="#ffffff" fill-opacity=".06" '
              f'stroke="#ffffff" stroke-opacity=".14"/>')
        color = "#ffffff"
    txt = (f'<text x="{x+w/2:.1f}" y="{y+h/2+size*0.36:.1f}" text-anchor="middle" font-family="{FONT}" '
           f'font-size="{size}" font-weight="700" fill="{color}">{label}</text>')
    return bg + txt, w


def gradient_heading(x: float, y: float, text: str, prefix: str, size: float = 30) -> str:
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="800" '
            f'letter-spacing="-0.5" fill="url(#{prefix}-text)">{text}</text>')


def logo_data_uri() -> str:
    cache = ROOT / "scripts" / ".shaft-logo.png"
    if not cache.exists():
        cache.write_bytes(urllib.request.urlopen(LOGO_URL, timeout=30).read())
    return "data:image/png;base64," + base64.b64encode(cache.read_bytes()).decode()


# ───────────────────────────── hero ─────────────────────────────

def hero() -> str:
    W, H, P = 1200, 560, "h"
    s = panel_open(P, W, H, "Ikura — I build Shaft: the whole of Pixiv, in your pocket.")
    s += f'<image href="{logo_data_uri()}" x="56" y="52" width="64" height="64"/>'
    s += (f'<text x="136" y="97" font-family="{FONT}" font-size="34" font-weight="800" fill="#ffffff">Ikura</text>'
          f'<text x="238" y="97" font-family="{FONT}" font-size="18" font-weight="500" fill="#ffffff" fill-opacity=".55">@SoxiaLiSA · Tokyo</text>')
    p, _ = pill(56, 138, "Android · Backend · Web — one small team, one stack", dot=ACCENT, size=15)
    s += p
    # headline: three lines, kept inside the left column (tiles start at x=800)
    s += gradient_heading(56, 258, "I build Shaft —", P, 60)
    s += gradient_heading(56, 326, "the whole of Pixiv,", P, 60)
    s += gradient_heading(56, 394, "in your pocket.", P, 60)
    s += (f'<text x="56" y="438" font-family="{FONT}" font-size="17" fill="#ffffff" fill-opacity=".72">'
          f'An open-source Pixiv client for Android —</text>'
          f'<text x="56" y="462" font-family="{FONT}" font-size="17" fill="#ffffff" fill-opacity=".72">'
          f'plus the cloud behind it and the site in front of it.</text>')
    x = 56
    for label, primary in (("pixshaft.com", True), ("Pixiv-Shaft on GitHub", False), ("Google Play", False)):
        b, w = button(x, 486, label, primary, P, size=16)
        s += b
        x += w + 12
    s += (f'<text x="{W-56}" y="{H-24}" text-anchor="end" font-family="{FONT}" font-size="14" fill="#ffffff" fill-opacity=".5">'
          f'ずっと真夜中でいいのに</text>')
    # floating tiles on the right
    tiles = [
        (800, 150, "📱", "Pixiv-Shaft", "Kotlin · Material You", BRAND, "0 0; 0 -10; 0 0", "7s"),
        (840, 262, "☁️", "pixshaft-api", "Hono · SQLite · pm2", ACCENT, "0 0; 0 10; 0 0", "8s"),
        (800, 374, "🌐", "shaft-web", "Next.js 16 · React 19", PINK, "0 0; 0 -8; 0 0", "9s"),
    ]
    for tx, ty, emoji, name, note, color, values, dur in tiles:
        tw, th = 304, 88
        s += f"""<g>
  <animateTransform attributeName="transform" type="translate" values="{values}" dur="{dur}" repeatCount="indefinite"/>
  <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="20" fill="#14122a" fill-opacity=".72" stroke="#ffffff" stroke-opacity=".12"/>
  <rect x="{tx}" y="{ty+18}" width="4" height="{th-36}" rx="2" fill="{color}"/>
  <text x="{tx+26}" y="{ty+54}" font-family="{FONT}" font-size="30">{emoji}</text>
  <text x="{tx+78}" y="{ty+40}" font-family="{FONT}" font-size="21" font-weight="800" fill="#ffffff">{name}</text>
  <text x="{tx+78}" y="{ty+64}" font-family="{FONT}" font-size="14" fill="#ffffff" fill-opacity=".6">{note}</text>
</g>"""
    # signal lines between the tiles (animated dash = requests flowing app → api → web)
    s += (f'<path d="M952 238 C 960 250, 985 250, 992 262 M 992 350 C 985 362, 960 362, 952 374" '
          f'fill="none" stroke="{GLOW}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="6 8">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="1.6s" repeatCount="indefinite"/></path>')
    s += panel_close(W, H)
    return s


# ───────────────────────────── marquee ─────────────────────────────

ROW1 = [("Illustrations", BRAND), ("Manga", ACCENT), ("Novels", PINK), ("Rankings", GLOW), ("PixiVision", GREEN),
        ("FANBOX", AMBER), ("pixiv COMIC", BRAND), ("Trending tags", ACCENT), ("Following feed", PINK),
        ("Ugoira interpolation", GLOW), ("GIF / MP4", GREEN), ("Batch download", AMBER), ("Resumable downloads", BRAND),
        ("Reverse image search", ACCENT), ("Watch later", PINK), ("Local library", GLOW), ("Network self-check", GREEN),
        ("Tablet two-pane", AMBER), ("Multi-account", ACCENT), ("Material You", GREEN)]
ROW2 = [("Cloud sync", ACCENT), ("Remote config", BRAND), ("In-app push", PINK), ("Plans · Afdian fulfilment", AMBER),
        ("HMAC-signed requests", GLOW), ("Rate limiting", GREEN), ("SQLite · WAL", BRAND), ("Community events", ACCENT),
        ("Trending API", PINK), ("WebSocket", GLOW), ("Admin console", GREEN), ("Next.js 16 site", AMBER),
        ("Web discover", BRAND), ("Switchable skins", ACCENT), ("Guestbook", PINK), ("Super-resolution", GLOW),
        ("Smart cut-out", GREEN), ("Manga translation", AMBER), ("RIFE interpolation", BRAND), ("ONNX on device", ACCENT)]


def marquee_row(items, y: float, prefix: str, reverse: bool, dur: int) -> str:
    x = 0.0
    chunk = []
    for label, color in items:
        p, w = pill(x, y, label, dot=color, size=15)
        chunk.append(p)
        x += w + 12
    total = x
    anim = f"{prefix}-{'rev' if reverse else 'fwd'}"
    return (f'<g class="{anim}">' + "".join(chunk) + f'<g transform="translate({total:.1f} 0)">' + "".join(chunk) + "</g></g>",
            total)


def marquee() -> str:
    W, H, P = 1200, 150, "m"
    s = panel_open(P, W, H, "What Shaft does — a scrolling wall of capabilities", rx=24, scale=.5)
    r1, t1 = marquee_row(ROW1, 30, P, False, 60)
    r2, t2 = marquee_row(ROW2, 84, P, True, 66)
    s += f"""<style>
  .{P}-fwd {{ animation: {P}-fwd 70s linear infinite; }}
  .{P}-rev {{ animation: {P}-rev 76s linear infinite; }}
  @keyframes {P}-fwd {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{t1:.1f}px); }} }}
  @keyframes {P}-rev {{ from {{ transform: translateX(-{t2:.1f}px); }} to {{ transform: translateX(0); }} }}
</style>"""
    s += r1 + r2
    # edge fades
    s += f"""<defs>
  <linearGradient id="{P}-fadeL" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
  <linearGradient id="{P}-fadeR" x1="1" x2="0"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
</defs>
<rect x="0" y="0" width="90" height="{H}" fill="url(#{P}-fadeL)"/>
<rect x="{W-90}" y="0" width="90" height="{H}" fill="url(#{P}-fadeR)"/>"""
    s += panel_close(W, H, rx=24)
    return s


# ───────────────────────────── section header ─────────────────────────────

def header(prefix: str, title_plain: str, title_accent: str, subtitle: str, name: str) -> str:
    W, H = 1200, 118
    s = panel_open(prefix, W, H, f"{title_plain} {title_accent}", rx=24, scale=.45)
    s += (f'<text x="40" y="58" font-family="{FONT}" font-size="30" font-weight="800" letter-spacing="-0.5" fill="#ffffff">'
          f'{title_plain} <tspan fill="url(#{prefix}-text)">{title_accent}</tspan></text>')
    s += f'<text x="40" y="90" font-family="{FONT}" font-size="15" fill="#ffffff" fill-opacity=".62">{subtitle}</text>'
    s += panel_close(W, H, rx=24)
    return s


# ───────────────────────────── project cards ─────────────────────────────

def card(prefix: str, emoji: str, name: str, kicker: str, lines: list[str], chips: list[str],
         color: str, cta: str, lock: bool = False) -> str:
    W, H = 392, 404
    s = panel_open(prefix, W, H, f"{name} — {kicker}", rx=24, scale=.45)
    s += f'<rect x="0" y="0" width="{W}" height="4" fill="{color}"/>'
    # glow pulse behind the icon
    s += (f'<circle cx="56" cy="62" r="34" fill="{color}" fill-opacity=".22" filter="url(#{prefix}-blur)">'
          f'<animate attributeName="r" values="30;44;30" dur="4s" repeatCount="indefinite"/></circle>')
    s += f'<text x="34" y="74" font-family="{FONT}" font-size="34">{emoji}</text>'
    s += f'<text x="88" y="58" font-family="{FONT}" font-size="24" font-weight="800" fill="#ffffff">{name}</text>'
    s += f'<text x="88" y="80" font-family="{FONT}" font-size="13.5" font-weight="600" fill="{color}">{kicker}</text>'
    y = 122
    for ln in lines:
        s += f'<text x="34" y="{y}" font-family="{FONT}" font-size="14.5" fill="#ffffff" fill-opacity=".78">{ln}</text>'
        y += 22
    # chips (wrap)
    cx, cy = 34, y + 10
    for c in chips:
        p, w = pill(cx, cy, c, size=12.5, bg_op=.07, fill_op=.85)
        if cx + w > W - 34:
            cx, cy = 34, cy + 40
            p, w = pill(cx, cy, c, size=12.5, bg_op=.07, fill_op=.85)
        s += p
        cx += w + 8
    # CTA line
    s += f'<line x1="34" y1="{H-58}" x2="{W-34}" y2="{H-58}" stroke="#ffffff" stroke-opacity=".08"/>'
    s += (f'<text x="34" y="{H-26}" font-family="{FONT}" font-size="14" font-weight="700" fill="{ACCENT}">{cta} →</text>')
    if lock:
        s += (f'<text x="{W-34}" y="{H-26}" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="#ffffff" fill-opacity=".5">'
              f'🔒 private for now</text>')
    s += panel_close(W, H, rx=24)
    return s


def small_card(prefix: str, name: str, desc: list[str], chips: list[str], color: str) -> str:
    W, H = 392, 210
    s = panel_open(prefix, W, H, name, rx=22, scale=.4)
    s += f'<rect x="0" y="22" width="4" height="{H-44}" rx="2" fill="{color}"/>'
    s += f'<text x="34" y="52" font-family="{FONT}" font-size="21" font-weight="800" fill="#ffffff">{name}</text>'
    y = 84
    for ln in desc:
        s += f'<text x="34" y="{y}" font-family="{FONT}" font-size="14" fill="#ffffff" fill-opacity=".74">{ln}</text>'
        y += 21
    cx = 34
    for c in chips:
        p, w = pill(cx, H - 56, c, size=12, bg_op=.07)
        s += p
        cx += w + 8
    s += panel_close(W, H, rx=22)
    return s


# ───────────────────────────── CTA ─────────────────────────────

def cta() -> str:
    W, H, P = 1200, 230, "c"
    s = panel_open(P, W, H, "Start browsing Pixiv the Shaft way", rx=28, scale=.6)
    p, w = pill(56, 44, "Free · Open source · No ads", dot=ACCENT, size=14)
    s += p
    s += (f'<text x="56" y="120" font-family="{FONT}" font-size="38" font-weight="800" letter-spacing="-0.5" fill="#ffffff">'
          f'Start browsing Pixiv <tspan fill="url(#{P}-text)">the Shaft way.</tspan></text>')
    s += (f'<text x="56" y="152" font-family="{FONT}" font-size="16" fill="#ffffff" fill-opacity=".7">'
          f'Android 7.0+ · direct connection in mainland China · Google Play or the latest APK from GitHub.</text>')
    x = 56
    for label, primary in (("Get it on Google Play", True), ("GitHub Releases", False), ("pixshaft.com", False)):
        b, bw = button(x, 168, label, primary, P, size=15)
        s += b
        x += bw + 12
    # right side: pulsing rings
    s += f"""<g transform="translate(1040 115)">
  <circle r="26" fill="none" stroke="{BRAND}" stroke-opacity=".8" stroke-width="2"><animate attributeName="r" values="26;70" dur="3s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="3s" repeatCount="indefinite"/></circle>
  <circle r="26" fill="none" stroke="{ACCENT}" stroke-opacity=".8" stroke-width="2"><animate attributeName="r" values="26;70" dur="3s" begin="1.5s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".8;0" dur="3s" begin="1.5s" repeatCount="indefinite"/></circle>
  <circle r="30" fill="url(#{P}-brand)"/>
  <text x="0" y="9" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="900" fill="#ffffff">oï</text>
</g>"""
    s += panel_close(W, H)
    return s


def main() -> None:
    files = {
        "hero.svg": hero(),
        "marquee.svg": marquee(),
        "h-stack.svg": header("hs", "The Shaft", "stack", "One app, one backend, one website — designed together so each can stay small.", "stack"),
        "h-bench.svg": header("hb", "Also on the", "bench", "Smaller things that fell out of building Shaft.", "bench"),
        "h-toolbox.svg": header("ht", "Under the", "hood", "What the three of them are made of.", "toolbox"),
        "card-app.svg": card("ca", "📱", "Pixiv-Shaft", "The client · Android",
                             ["Illustrations, manga, novels, rankings,", "FANBOX and pixiv COMIC in one app.",
                              "On-device AI: super-resolution, cut-out,", "manga translation, RIFE ugoira frames."],
                             ["Kotlin", "Coroutines", "Room", "Retrofit", "Glide", "ONNX Runtime", "C++ / JNI"],
                             BRAND, "github.com/CeuiLiSA/Pixiv-Shaft"),
        "card-api.svg": card("cb", "☁️", "pixshaft-api", "The backend · pixshaft.com",
                             ["Cloud sync for settings, mute lists and", "download config · browse history · remote",
                              "config and in-app push · plans with automatic", "Afdian fulfilment · curated Prime shelves."],
                             ["Node 22", "Hono", "better-sqlite3", "pino", "pm2", "Caddy", "HMAC"],
                             ACCENT, "live at pixshaft.com", lock=True),
        "card-web.svg": card("cc", "🌐", "shaft-web", "The website · pixshaft.com",
                             ["A motion-heavy landing page: bento features,", "showcase, pricing, FAQ, guestbook —",
                              "plus a web discover page at /web with", "switchable skins and a login flow."],
                             ["Next.js 16", "React 19", "TypeScript", "Tailwind v4", "motion", "GSAP", "Lenis"],
                             PINK, "pixshaft.com · /web", lock=True),
        "bench-stackswipe.svg": small_card("b1", "StackSwipe",
                                           ["iOS-style app switcher for Jetpack", "Compose, physics-based animations."],
                                           ["Compose", "Kotlin"], BRAND),
        "bench-login.svg": small_card("b2", "pixiv-login",
                                      ["Android library for Pixiv OAuth 2.0", "login (PKCE). One dependency via JitPack."],
                                      ["Kotlin", "OAuth · PKCE", "JitPack"], ACCENT),
        "bench-shaft-ios.svg": small_card("b3", "Shaft · SwiftUI",
                                          ["A SwiftUI prototype: discover feed, detail,", "token refresh. Full iOS client in progress."],
                                          ["Swift", "SwiftUI"], PINK),
        "cta.svg": cta(),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote assets/{name} ({len(svg)//1024} KB)")


if __name__ == "__main__":
    main()
