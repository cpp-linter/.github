"""Build the cpp-linter status marks from the logo (../../icon.png).

passed = the logo itself: amber ring + green brush check.
warned / failed = the same ring with an amber "!" or a red brush X that
breaks out of the ring's gap exactly where the logo's check does.
row-* = the glyph alone on the same ink tile, for table rows and inline use.

Run: python3 make_marks.py  (needs numpy and Pillow)
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).parent
SS = 4  # supersampling for the drawn strokes
INK = (0x26, 0x24, 0x1F)
GOLD = (0xF8, 0xC4, 0x18)
GREEN = (0x48, 0xB8, 0x88)
RED = (0xEC, 0x5B, 0x52)


def logo_layers():
    logo = np.array(Image.open(HERE / "../../icon.png").convert("RGBA")).astype(float)
    r, g, a = logo[..., 0], logo[..., 1], logo[..., 3]
    goldness = np.clip((r - g) / 60.0, 0, 1)  # amber pixels have r >> g
    return a * goldness, a * (1 - goldness)


def layer(alpha, color):
    im = np.zeros(alpha.shape + (4,), np.uint8)
    im[..., :3] = color
    im[..., 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(im, "RGBA")


def spline(pts, n=24):
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[j], float) for j in (i - 1, i, i + 1, i + 2))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    out.append(np.array(pts[-1], float))
    return np.array(out)


def brush(w0, wm, w1, peak):
    """Stroke width along the stroke: press in, then lift off with a taper."""
    def width(t):
        if t < peak:
            return w0 + (wm - w0) * math.sin(t / peak * math.pi / 2)
        return wm + (w1 - wm) * ((t - peak) / (1 - peak)) ** 1.4
    return width


def stroke(draw, pts, width, color):
    c = spline(pts)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))]
    t = s / s[-1]
    left, right = [], []
    for i in range(len(c)):
        d = c[min(i + 1, len(c) - 1)] - c[max(i - 1, 0)]
        d /= np.linalg.norm(d) + 1e-9
        n = np.array([-d[1], d[0]]) * width(t[i]) / 2
        left.append(c[i] + n)
        right.append(c[i] - n)
    draw.polygon([tuple(p * SS) for p in left + right[::-1]], fill=color)
    for i in (0, len(c) - 1):
        w = width(t[i]) / 2 * SS
        x, y = c[i] * SS
        draw.ellipse([x - w, y - w, x + w, y + w], fill=color)


def drawn(fn):
    im = Image.new("RGBA", (400 * SS, 400 * SS), (0, 0, 0, 0))
    fn(ImageDraw.Draw(im))
    return im.resize((400, 400), Image.LANCZOS)


def bang(d):
    col = GOLD + (255,)
    stroke(d, [(285, 60), (254, 141), (220, 220)], brush(40, 44, 22, 0.15), col)
    x, y, r = 203, 271, 23
    d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=col)


def cross(d):
    col = RED + (255,)
    stroke(d, [(150, 140), (204, 202), (254, 262)], brush(28, 42, 26, 0.45), col)
    stroke(d, [(152, 274), (234, 177), (322, 72)], brush(38, 42, 14, 0.3), col)


def tile(parts, out, content, box):
    canvas = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    for p in parts:
        canvas = Image.alpha_composite(canvas, p)
    x0, y0, x1, y1 = box
    side = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    crop = canvas.crop((int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2)))
    big = out * 8
    inner = int(big * content)
    crop = crop.resize((inner, inner), Image.LANCZOS)
    base = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, big - 1, big - 1], radius=big // 4, fill=255)
    base.paste(Image.new("RGBA", (big, big), INK + (255,)), (0, 0), mask)
    off = (big - inner) // 2
    base.alpha_composite(crop, (off, off))
    return base.resize((out, out), Image.LANCZOS)


def main():
    ring_a, check_a = logo_layers()
    ring, check = layer(ring_a, GOLD), layer(check_a, GREEN)
    glyphs = {"passed": check, "warned": drawn(bang), "failed": drawn(cross)}
    row_box = {"passed": (110, 40, 350, 300), "warned": (85, 40, 345, 300), "failed": (100, 45, 360, 315)}
    for name, glyph in glyphs.items():
        # heading mark, shown at 24px; row mark, shown at 20px (4x for retina)
        tile([ring, glyph], 96, 0.80, (60, 55, 340, 340)).save(HERE / f"{name}.png")
        tile([glyph], 80, 0.82, row_box[name]).save(HERE / f"row-{name}.png")


if __name__ == "__main__":
    main()
