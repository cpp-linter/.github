# /// script
# requires-python = ">=3.9"
# dependencies = ["fonttools[woff]"]
# ///
"""Generate the animated banner of the organization profile README.

Writes assets/profile-banner-light.svg and assets/profile-banner-dark.svg.
Run from anywhere in the repository:

    uv run branding/profile-banner/generate.py

The fonts in ./fonts are subset to the characters the banner uses and embedded,
together with ./logo-72.png (branding/logo.png scaled to 72 px), so the SVG files
load nothing else. Edit the copy in the scene functions below and run it again.
"""

import base64
import html
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"
ASSETS = HERE.parent.parent / "assets"

W, H = 880, 280
SCENE_SECONDS = 3.5

FONT_FILES = {
    "b": "bricolage-grotesque-latin.woff2",
    "s": "instrument-sans-latin.woff2",
    "m": "jetbrains-mono-latin.woff2",
}
FAMILY = {"b": "Bricolage Grotesque", "s": "Instrument Sans", "m": "JetBrains Mono"}
WEIGHTS = {"b": "700", "s": "400 700", "m": "400 800"}

# ---------------------------------------------------------------- measuring

_instances = {}


def _instance(ff, weight, opsz=None):
    key = (ff, weight, opsz)
    if key not in _instances:
        font = TTFont(FONTS / FONT_FILES[ff])
        location = {"wght": weight}
        if ff == "b":
            location["opsz"] = opsz or 36
        _instances[key] = instancer.instantiateVariableFont(font, location)
    return _instances[key]


def measure(text, ff, size, weight=400, ls=0.0):
    """Advance width of `text` in px, without kerning."""
    font = _instance(ff, weight, size if ff == "b" else None)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    upem = font["head"].unitsPerEm
    width = 0
    for ch in text:
        glyph = cmap.get(ord(ch))
        width += hmtx[glyph][0] if glyph else upem * 0.5
    return width * size / upem + ls * size * len(text)


USED = {"b": set(), "s": set(), "m": set()}

# ---------------------------------------------------------------- palette

LIGHT = dict(
    page="#FFFFFF", card="#F7F5EF", cardStroke="#E4DFD1", ink="#171A2E", muted="#5A5E70",
    faint="#7D8092", yellow="#FFC20A", green="#40B385", indigo="#4051B5", panel="#FFFFFF",
    panelStroke="#E4DFD1", strip="#F4F1E8", addBg="#E1F3E9", addText="#1F5E43", delBg="#FBE6E3",
    delText="#8A2A1C", warnBg="#FFF4D6", warnIcon="#B7791F", noteBg="#ECEFFB", noteIcon="#4051B5",
    track="#E4DFD1", fill="#171A2E", shadow="#171A2E", shadowOpacity="0.16", avatar="#171A2E",
    button="#4051B5", highlight="#E1F3E9", line="#E4DFD1", cursorFill="#FFFFFF", cursorStroke="#171A2E",
)
DARK = dict(
    page="#0D1117", card="#16182A", cardStroke="#2A2E48", ink="#F4F2EC", muted="#A9AEC8",
    faint="#8A8FAD", yellow="#FFC20A", green="#40B385", indigo="#8E9CF5", panel="#1E2136",
    panelStroke="#353A5C", strip="#262A45", addBg="#173628", addText="#A3E2C2", delBg="#3A1F25",
    delText="#F4B9AF", warnBg="#3A3220", warnIcon="#F2C14E", noteBg="#262B4D", noteIcon="#8E9CF5",
    track="#353A5C", fill="#F4F2EC", shadow="#000000", shadowOpacity="0.45", avatar="#8E9CF5",
    button="#5566D1", highlight="#173628", line="#353A5C", cursorFill="#FFFFFF", cursorStroke="#16182A",
)

# ---------------------------------------------------------------- primitives


def esc(s):
    return html.escape(s, quote=True)


def text(x, y, s, ff, size, fill, weight=400, anchor=None, ls=None, cls=None):
    # SVG collapses leading spaces, so indent code by position instead
    indent = len(s) - len(s.lstrip(" "))
    if indent and ff == "m":
        x += indent * measure(" ", "m", size)
        s = s.lstrip(" ")
    USED[ff].update(s)
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'class="ff-{ff}{(" " + cls) if cls else ""}"',
             f'font-size="{size:g}"', f'font-weight="{weight}"', f'fill="{fill}"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if ls:
        attrs.append(f'letter-spacing="{ls * size:.2f}"')
    return f'<text {" ".join(attrs)}>{esc(s)}</text>'


def rich(x, y, parts, ff, size, fill):
    """parts: list of (string, weight, fill-or-None)"""
    spans = []
    for s, weight, color in parts:
        USED[ff].update(s)
        spans.append(f'<tspan font-weight="{weight}"{f" fill={chr(34)}{color}{chr(34)}" if color else ""}>{esc(s)}</tspan>')
    return f'<text x="{x:g}" y="{y:g}" class="ff-{ff}" font-size="{size:g}" fill="{fill}">{"".join(spans)}</text>'


def rect(x, y, w, h, fill="none", rx=0, stroke=None, extra=""):
    s = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"'
    if rx:
        s += f' rx="{rx:g}"'
    s += f' fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}"'
    return s + (f" {extra}" if extra else "") + "/>"


def g(inner, cls=None, extra=""):
    return f'<g{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{(" " + extra) if extra else ""}>{"".join(inner)}</g>'


# ---------------------------------------------------------------- layout

PX, PY = 40, 34            # card padding
RX0, RW = 480, 360         # right column
PANEL = (RX0, 70, RW, 176)  # x, y, w, h
IX = RX0 + 14              # panel inner x


def avatar(c, cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="{c["avatar"]}"/>'
            f'<path d="M{cx - 4} {cy + 0.5}l2.6 2.6 5-5.2" fill="none" stroke="{c["page"]}" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def author_row(c, y, verb):
    name = "github-actions"
    nw = measure(name, "s", 12, 600)
    return [avatar(c, IX + 9, y - 4),
            text(IX + 24, y, name, "s", 12, c["ink"], 600),
            text(IX + 24 + nw + 6, y, verb, "s", 12, c["muted"])]


def warn_icon(c, cx, cy):
    return (f'<path d="M{cx} {cy - 5.5}l5.8 10H{cx - 5.8}z" fill="{c["warnIcon"]}" stroke="{c["warnIcon"]}" '
            f'stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="M{cx} {cy - 2}v3" stroke="{c["panel"]}" stroke-width="1.4" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy + 3}" r="0.8" fill="{c["panel"]}"/>')


def info_icon(c, cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="none" stroke="{c["noteIcon"]}" stroke-width="1.4"/>'
            f'<path d="M{cx} {cy - 0.5}v3" stroke="{c["noteIcon"]}" stroke-width="1.4" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy - 2.8}" r="0.8" fill="{c["noteIcon"]}"/>')


def caret(c, x, cy):
    return f'<path d="M{x} {cy - 4}l4 4-4 4z" fill="{c["muted"]}"/>'


def check_circle(c, cx, cy, r=8):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["green"]}"/>'
            f'<path d="M{cx - r * 0.45} {cy + 0.3}l{r * 0.3:.2f} {r * 0.3:.2f} {r * 0.55:.2f} -{r * 0.6:.2f}" fill="none" '
            f'stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')


# Scene titles are the headings of the cpp-linter-action README, and each chip is
# the action input that turns the feature on. The strings inside the scenes match
# what cpp-linter posts: annotation titles and messages (rest_api/github_api.py),
# the report used by the thread comment and the step summary (rest_api/__init__.py),
# the review headings (clang_tools/*.py) and the default auto-fix commit message.


def scene_notes(c):
    x, y, w, h = PANEL
    out = [rect(x, y, w, 26, c["strip"]),
           text(IX, y + 17, "src/parser.cpp", "m", 11, c["muted"]),
           text(IX, y + 43, "41", "m", 11, c["faint"]),
           text(IX + 36, y + 43, "int parse(const char *src) {", "m", 11.5, c["ink"]),
           rect(x, y + 50, w, 19, c["addBg"]),
           text(IX, y + 63, "42", "m", 11, c["addText"]),
           text(IX + 22, y + 63, "+", "m", 11.5, c["addText"]),
           text(IX + 36, y + 63, "  char *end = 0;", "m", 11.5, c["addText"])]
    a1y = y + 76
    out.append(g([rect(x + 10, a1y, w - 20, 38, c["warnBg"], rx=6),
                  warn_icon(c, x + 24, a1y + 14),
                  text(x + 38, a1y + 16, "src/parser.cpp:42:15 [modernize-use-nullptr]", "s", 11, c["ink"], 600),
                  text(x + 38, a1y + 31, "use nullptr", "s", 11, c["muted"])], cls="cl-a1"))
    a2y = a1y + 44
    out.append(g([rect(x + 10, a2y, w - 20, 52, c["noteBg"], rx=6),
                  info_icon(c, x + 24, a2y + 13),
                  text(x + 38, a2y + 16, "Run clang-format on src/parser.cpp", "s", 11, c["ink"], 600),
                  text(x + 38, a2y + 31, "File src/parser.cpp does not conform to Custom", "s", 11, c["muted"]),
                  text(x + 38, a2y + 45, "style guidelines. (lines 42)", "s", 11, c["muted"])], cls="cl-a2"))
    return out


def scene_comment(c):
    x, y, w, h = PANEL
    out = author_row(c, y + 22, "commented")
    out.append(f'<path d="M{x} {y + 34}h{w}" stroke="{c["line"]}"/>')
    out.append(text(IX, y + 58, "Cpp-Linter Report", "s", 16, c["ink"], 600))
    out.append(warn_icon(c, IX + 6, y + 75))
    out.append(text(IX + 18, y + 79, "Some files did not pass the configured checks!", "s", 11.5, c["ink"]))
    r1 = y + 90
    out.append(g([rect(x + 10, r1, w - 20, 30, c["strip"], rx=6), caret(c, IX + 2, r1 + 15),
                  rich(IX + 14, r1 + 19, [("clang-format (v21) reports: ", 400, None),
                                          ("1 file(s) not formatted", 600, None)], "s", 11.5, c["ink"])], cls="cl-r1"))
    r2 = r1 + 36
    out.append(g([rect(x + 10, r2, w - 20, 30, c["strip"], rx=6), caret(c, IX + 2, r2 + 15),
                  rich(IX + 14, r2 + 19, [("clang-tidy (v21) reports: ", 400, None),
                                          ("2 concern(s)", 600, None)], "s", 11.5, c["ink"])], cls="cl-r2"))
    return out


def scene_summary(c):
    x, y, w, h = PANEL
    out = [rect(x, y, w, 26, c["strip"]),
           text(IX, y + 18, "cpp-linter summary", "s", 12, c["ink"], 600),
           text(IX, y + 48, "Cpp-Linter Report", "s", 16, c["ink"], 600),
           warn_icon(c, IX + 6, y + 62),
           text(IX + 18, y + 66, "Some files did not pass the configured checks!", "s", 11.5, c["ink"]),
           caret(c, IX + 2, y + 82),
           rich(IX + 14, y + 86, [("clang-format (v21) reports: ", 400, None),
                                  ("1 file(s) not formatted", 600, None)], "s", 11.5, c["ink"]),
           f'<path d="M{IX} {y + 100}l4 4 4-4z" fill="{c["muted"]}"/>',
           rich(IX + 14, y + 105, [("clang-tidy (v21) reports: ", 400, None),
                                   ("2 concern(s)", 600, None)], "s", 11.5, c["ink"])]
    out.append(g([f'<circle cx="{IX + 18}" cy="{y + 120}" r="1.8" fill="{c["ink"]}"/>',
                  rich(IX + 24, y + 124, [("src/parser.cpp:42:15:", 600, None),
                                          (" warning: [modernize-use-nullptr]", 400, None)], "s", 11, c["ink"]),
                  rect(IX + 24, y + 130, 2.5, 14, c["line"]),
                  text(IX + 32, y + 141, "use nullptr", "s", 11, c["muted"])], cls="cl-sd"))
    out.append(text(IX, y + 166, "Job summary generated at run-time", "s", 10.5, c["muted"]))
    return out


def scene_tidy_review(c):
    x, y, w, h = PANEL
    out = author_row(c, y + 22, "reviewed")
    out.append(text(IX, y + 46, "clang-tidy diagnostics", "s", 13, c["ink"], 600))
    out.append(f'<circle cx="{IX + 4}" cy="{y + 60}" r="1.8" fill="{c["ink"]}"/>')
    out.append(rich(IX + 12, y + 64, [("use nullptr [", 400, None), ("modernize-use-nullptr", 400, c["indigo"]),
                                      ("]", 400, None)], "s", 11.5, c["ink"]))
    bx, by, bw = x + 10, y + 74, w - 20
    rows = [("-", "  char *end = 0;", c["delBg"], c["delText"]),
            ("+", "  char *end = nullptr;", c["addBg"], c["addText"])]
    box = [rect(bx, by, bw, 20, c["strip"]),
           text(bx + 10, by + 14, "Suggested change", "s", 10.5, c["muted"])]
    for i, (sign, code, bg, fg) in enumerate(rows):
        ry = by + 20 + i * 17
        box += [rect(bx, ry, bw, 17, bg), text(bx + 10, ry + 12.5, sign, "m", 11.5, fg),
                text(bx + 26, ry + 12.5, code, "m", 11.5, fg)]
    hb = 20 + len(rows) * 17
    out.append(f'<clipPath id="{c["_id"]}-tidy"><rect x="{bx}" y="{by}" width="{bw}" height="{hb}" rx="6"/></clipPath>')
    out.append(g(box, extra=f'clip-path="url(#{c["_id"]}-tidy)"'))
    out.append(rect(bx + 0.5, by + 0.5, bw - 1, hb - 1, "none", rx=6, stroke=c["panelStroke"]))
    label = "Commit suggestion"
    btw = measure(label, "s", 11, 600) + 22
    btx, bty = x + w - 10 - btw, by + hb + 8
    out.append(rect(btx, bty, btw, 22, c["button"], rx=6))
    out.append(text(btx + btw / 2, bty + 15, label, "s", 11, "#FFFFFF", 600, anchor="middle"))
    return out


def scene_format_review(c):
    x, y, w, h = PANEL
    out = author_row(c, y + 22, "reviewed")
    out.append(text(IX, y + 46, "clang-format suggestion", "s", 13, c["ink"], 600))
    bx, by, bw = x + 10, y + 54, w - 20
    rows = [("-", "if(ok){return 1;}", c["delBg"], c["delText"]),
            ("+", "if (ok) {", c["addBg"], c["addText"]),
            ("+", "  return 1;", c["addBg"], c["addText"]),
            ("+", "}", c["addBg"], c["addText"])]
    box = [rect(bx, by, bw, 20, c["strip"]),
           text(bx + 10, by + 14, "Suggested change", "s", 10.5, c["muted"])]
    for i, (sign, code, bg, fg) in enumerate(rows):
        ry = by + 20 + i * 17
        box += [rect(bx, ry, bw, 17, bg), text(bx + 10, ry + 12.5, sign, "m", 11.5, fg),
                text(bx + 26, ry + 12.5, code, "m", 11.5, fg)]
    out.append(f'<clipPath id="{c["_id"]}-sug"><rect x="{bx}" y="{by}" width="{bw}" height="{20 + 4 * 17}" rx="6"/></clipPath>')
    out.append(g(box, extra=f'clip-path="url(#{c["_id"]}-sug)"'))
    out.append(rect(bx + 0.5, by + 0.5, bw - 1, 20 + 4 * 17 - 1, "none", rx=6, stroke=c["panelStroke"]))
    label = "Commit suggestion"
    lw = measure(label, "s", 11, 600)
    btw, bth = lw + 22, 22
    btx, bty = x + w - 10 - btw, by + 20 + 4 * 17 + 8
    out.append(g([rect(btx, bty, btw, bth, c["button"], rx=6),
                  text(btx + btw / 2, bty + 15, label, "s", 11, "#FFFFFF", 600, anchor="middle")], cls="cl-btn"))
    # pointer that clicks the button
    cx, cy = btx + btw * 0.62, bty + bth * 0.55
    out.append(g([f'<path d="M0 0v15.5l4-3.6 2.8 6.2 2.6-1.1-2.7-6.1h5.4z" fill="{c["cursorFill"]}" '
                  f'stroke="{c["cursorStroke"]}" stroke-width="1.2" stroke-linejoin="round"/>'],
                 cls="cl-cursor", extra=f'transform="translate({cx:.1f} {cy:.1f})"'))
    return out


def scene_autofix(c):
    x, y, w, h = PANEL
    out = [text(IX, y + 24, "Commits", "s", 12, c["muted"], 600),
           f'<path d="M{IX + 7} {y + 42}V{y + 118}" stroke="{c["line"]}" stroke-width="2"/>',
           f'<circle cx="{IX + 7}" cy="{y + 48}" r="4.5" fill="{c["panel"]}" stroke="{c["faint"]}" stroke-width="1.6"/>',
           text(IX + 22, y + 52, "fix: handle an empty input", "s", 12, c["ink"]),
           text(x + w - 14, y + 52, "you", "s", 11, c["muted"], anchor="end")]
    hy = y + 66
    out.append(g([rect(x + 8, hy, w - 16, 50, c["highlight"], rx=8),
                  check_circle(c, IX + 7, hy + 18),
                  text(IX + 22, hy + 22, "style: apply clang-format fixes", "s", 12, c["ink"], 600),
                  text(IX + 22, hy + 39, "auto-fix · 2 files changed", "s", 11, c["muted"])], cls="cl-c2"))
    out.append(text(IX, y + 146, "clang-format -i runs on the files with style issues,", "s", 11, c["muted"]))
    out.append(text(IX, y + 161, "and the result is pushed to the pull request branch.", "s", 11, c["muted"]))
    return out


# (title, action input, drawing)
SCENES = [
    ("Annotations", "file-annotations", scene_notes),
    ("Thread Comment", "thread-comments", scene_comment),
    ("Step Summary", "step-summary", scene_summary),
    ("Pull Request Review", "tidy-review", scene_tidy_review),
    ("Pull Request Review", "format-review", scene_format_review),
    ("Auto-fix", "auto-fix", scene_autofix),
]
N = len(SCENES)
CYCLE = SCENE_SECONDS * N
STILL = 3  # the scene shown without animation (tidy-review)


def banner_body(c, logo_markup):
    """Everything inside <svg> except <style>."""
    idp = c["_id"]
    parts = [f'<title id="{idp}-t">cpp-linter: C/C++ pull requests that arrive already checked.</title>',
             f'<desc id="{idp}-d">A loop of the ways cpp-linter-action reports on a pull request: file annotations, '
             f'a thread comment, the step summary, pull request reviews from clang-tidy and clang-format, '
             f'and auto-fix.</desc>']
    parts.append("<defs>"
                 f'<clipPath id="{idp}-card"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24"/></clipPath>'
                 f'<clipPath id="{idp}-panel"><rect x="{PANEL[0]}" y="{PANEL[1]}" width="{PANEL[2]}" height="{PANEL[3]}" rx="12"/></clipPath>'
                 f'<filter id="{idp}-shadow" x="-20%" y="-20%" width="140%" height="160%">'
                 f'<feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="{c["shadow"]}" flood-opacity="{c["shadowOpacity"]}"/></filter>'
                 "</defs>")
    parts.append(rect(0, 0, W, H, c["page"]))
    parts.append(g([rect(0, 0, W, H, c["card"]),
                    f'<circle cx="{W + 58 - 150}" cy="{18 + 150}" r="147" fill="none" stroke="{c["yellow"]}" stroke-width="6"/>'],
                   extra=f'clip-path="url(#{idp}-card)"'))
    parts.append(rect(0.5, 0.5, W - 1, H - 1, "none", rx=24, stroke=c["cardStroke"]))

    # left column
    parts.append(logo_markup)
    parts.append(text(PX + 46, PY + 26, "cpp-linter", "b", 24, c["ink"], 700, ls=-0.01))
    lines = ["C/C++ pull requests", "that arrive", "already checked."]
    base = PY + 36 + 22 + 30
    for i, s in enumerate(lines):
        parts.append(text(PX, base + i * 40, s, "b", 36, c["ink"], 700, ls=-0.02))
    w3 = measure(lines[2], "b", 36, 700, ls=-0.02)
    # the brush loop spans x 14..350 and y 8..70 of its 360x74 drawing
    b3 = base + 80
    sx = (w3 + 40) / 336
    sy = 58 / 62
    ex, ey = PX - 20 - 14 * sx, b3 - 38 - 8 * sy
    parts.append(f'<path d="M14 44C18 20 118 8 212 10C300 12 350 24 346 42C342 62 250 70 166 68C90 66 20 58 16 40C14 30 40 20 70 16" '
                 f'transform="translate({ex:.1f} {ey:.1f}) scale({sx:.4f} {sy:.4f})" fill="none" stroke="{c["yellow"]}" '
                 f'stroke-width="{4.5 / ((sx + sy) / 2):.2f}" stroke-linecap="round"/>')
    parts.append(text(PX, base + 80 + 38, "clang-format and clang-tidy, reported on the pull request.", "s", 13.5, c["muted"]))

    # right column: caption with the action input, progress, panel
    gap = 5
    seg_w = (RW - (N - 1) * gap) / N
    for i in range(N):
        sx = RX0 + i * (seg_w + gap)
        parts.append(rect(sx, 56, seg_w, 3, c["track"], rx=1.5))
        parts.append(rect(sx, 56, seg_w, 3, c["fill"], rx=1.5, extra=f'class="cl-seg cl-f{i}"'))
    parts.append(rect(*PANEL, c["panel"], rx=12, extra=f'filter="url(#{idp}-shadow)"'))
    for i, (title, flag, scene) in enumerate(SCENES):
        tw = measure(title, "s", 13, 600)
        fw = measure(flag, "m", 10.5) + 12
        inner = [text(RX0, 45, title, "s", 13, c["ink"], 600),
                 rect(RX0 + tw + 8, 32, fw, 17, c["panel"], rx=4, stroke=c["panelStroke"]),
                 text(RX0 + tw + 14, 44.5, flag, "m", 10.5, c["muted"]),
                 text(RX0 + RW, 45, f"{i + 1} / {N}", "s", 11, c["muted"], anchor="end")]
        body = g(scene(c), extra=f'clip-path="url(#{idp}-panel)"')
        parts.append(g(inner + [body], cls=f"cl-s cl-s{i}"))
    parts.append(rect(PANEL[0] + 0.5, PANEL[1] + 0.5, PANEL[2] - 1, PANEL[3] - 1, "none", rx=11.5, stroke=c["panelStroke"]))
    return "".join(parts)


def pct(seconds):
    """A moment in the loop as a keyframe percentage."""
    return f"{round(100 * seconds / CYCLE, 2):g}%"


# parts of a scene that slide in: (scene, seconds after the scene appears)
ENTRIES = {"a1": (0, 0.6), "a2": (0, 1.5), "r1": (1, 0.6), "r2": (1, 1.3), "sd": (2, 1.0), "c2": (5, 0.8)}
CLICK_SCENE = 4  # format-review: the pointer commits the suggestion


def keyframes():
    k = []
    fade = 0.3  # seconds
    # each scene fades in while the previous one fades out
    for i in range(N):
        a, b = i * SCENE_SECONDS, (i + 1) * SCENE_SECONDS
        if i == 0:
            frames = f"0%,{pct(b - fade)}{{opacity:1}}{pct(b)},{pct(CYCLE - fade)}{{opacity:0}}100%{{opacity:1}}"
        elif i == N - 1:
            frames = f"0%,{pct(a - fade)}{{opacity:0}}{pct(a)},{pct(CYCLE - fade)}{{opacity:1}}100%{{opacity:0}}"
        else:
            frames = f"0%,{pct(a - fade)}{{opacity:0}}{pct(a)},{pct(b - fade)}{{opacity:1}}{pct(b)},100%{{opacity:0}}"
        k.append(f"@keyframes cl-s{i}{{{frames}}}")
    # progress segments fill during their scene and reset with the loop
    for i in range(N):
        a, b = i * SCENE_SECONDS, (i + 1) * SCENE_SECONDS
        empty = "0%" if i == 0 else f"0%,{pct(a)}"
        full = f"{pct(b)},99.9%" if i < N - 1 else "99.9%"
        k.append(f"@keyframes cl-f{i}{{{empty}{{transform:scaleX(0)}}{full}{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}")
    for name, (scene, at) in ENTRIES.items():
        t = scene * SCENE_SECONDS + at
        k.append(f"@keyframes cl-{name}{{0%,{pct(t)}{{opacity:0;transform:translateY(6px)}}"
                 f"{pct(t + 0.4)},100%{{opacity:1;transform:translateY(0)}}}}")
    # the pointer glides to the button, clicks, and the button answers
    s = CLICK_SCENE * SCENE_SECONDS
    k.append(f"@keyframes cl-cursor{{0%,{pct(s + 0.4)}{{opacity:0;translate:-90px 6px}}"
             f"{pct(s + 0.7)}{{opacity:1;translate:-90px 6px}}{pct(s + 1.4)}{{opacity:1;translate:0 0;scale:1}}"
             f"{pct(s + 1.6)}{{scale:.82}}{pct(s + 1.8)}{{scale:1}}{pct(s + 2.8)}{{opacity:1;translate:0 0}}"
             f"{pct(s + 3.1)},100%{{opacity:0;translate:0 0}}}}")
    k.append(f"@keyframes cl-btn{{0%,{pct(s + 1.55)}{{opacity:1}}{pct(s + 1.65)}{{opacity:.7}}{pct(s + 1.9)},100%{{opacity:1}}}}")
    return "".join(k)


def rules():
    loop = f"{CYCLE:g}s"
    return (
        ".ff-b{font-family:'Bricolage Grotesque',sans-serif}"
        ".ff-s{font-family:'Instrument Sans',-apple-system,'Segoe UI',sans-serif}"
        ".ff-m{font-family:'JetBrains Mono',ui-monospace,Menlo,monospace}"
        # without animation, or with reduced motion, one scene stays on screen
        f".cl-s{{opacity:0}}.cl-s{STILL}{{opacity:1}}"
        ".cl-seg{transform-box:fill-box;transform-origin:0 50%;transform:scaleX(0)}"
        + ",".join(f".cl-f{i}" for i in range(STILL + 1)) + "{transform:scaleX(1)}"
        ".cl-cursor{opacity:0}"
        "@media (prefers-reduced-motion:no-preference){"
        + "".join(f".cl-s{i}{{animation:cl-s{i} {loop} linear infinite}}" for i in range(N))
        + "".join(f".cl-f{i}{{animation:cl-f{i} {loop} linear infinite}}" for i in range(N))
        + "".join(f".cl-{n}{{transform-box:fill-box;animation:cl-{n} {loop} ease-out infinite}}" for n in ENTRIES)
        + ".cl-cursor>path{transform-box:fill-box;transform-origin:0 0}"
        f".cl-cursor>path{{animation:cl-cursor {loop} cubic-bezier(.4,0,.2,1) infinite}}.cl-cursor{{opacity:1}}"
        f".cl-btn{{animation:cl-btn {loop} linear infinite}}"
        "}"
    )


def subset_font(ff):
    """The font file, cut down to the characters the banner uses, as woff2 bytes."""
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    options.hinting = False
    font = subset.load_font(str(FONTS / FONT_FILES[ff]), options)
    subsetter = subset.Subsetter(options)
    subsetter.populate(text="".join(sorted(USED[ff] | set(" "))))
    subsetter.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, options)
    return buf.getvalue()


def main():
    variants = {"light": dict(LIGHT, _id="cll"), "dark": dict(DARK, _id="cld")}
    logo = base64.b64encode((HERE / "logo-72.png").read_bytes()).decode()
    logo_markup = f'<image href="data:image/png;base64,{logo}" x="{PX}" y="{PY}" width="36" height="36"/>'
    # draw first: the fonts are subset to the characters the drawing used
    bodies = {name: banner_body(c, logo_markup) for name, c in variants.items()}

    faces = []
    for ff in ("b", "s", "m"):
        data = base64.b64encode(subset_font(ff)).decode()
        faces.append(f"@font-face{{font-family:'{FAMILY[ff]}';src:url(data:font/woff2;base64,{data}) format('woff2');"
                     f"font-weight:{WEIGHTS[ff]};font-display:block}}")
    style = "".join(faces) + rules() + keyframes()

    for name, c in variants.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
               f'role="img" aria-labelledby="{c["_id"]}-t {c["_id"]}-d"><style>{style}</style>{bodies[name]}</svg>\n')
        out = ASSETS / f"profile-banner-{name}.svg"
        out.write_text(svg)
        print(f"wrote {out.relative_to(HERE.parent.parent)} ({len(svg.encode()) // 1024} KB)")


if __name__ == "__main__":
    main()
