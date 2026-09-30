# Paints the quest panel background (quest_panel.png, RGBA 1024x384 = the 320x120 HUD panel at 3.2x):
# a smooth dark-slate wash with gentle mottling, feathered dry-brush edges (long horizontal
# bristle streaks fading out on the right), and a thin gold frame line on the left, top and bottom
# with small corner dots - the look of the reference quest panel.
import numpy as np
from PIL import Image
W, H = 1024, 384
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def h(i):
    return (np.sin(i * 12.9898 + 78.233) * 43758.5453) % 1.0

def vnoise(x, y, seed):
    xi, yi = np.floor(x), np.floor(y); xf, yf = x - xi, y - yi
    xf = xf * xf * (3 - 2 * xf); yf = yf * yf * (3 - 2 * yf)
    def g(a, b): return h(a * 157.0 + b * 311.7 + seed * 71.3)
    return (g(xi, yi) * (1 - xf) + g(xi + 1, yi) * xf) * (1 - yf) + (g(xi, yi + 1) * (1 - xf) + g(xi + 1, yi + 1) * xf) * yf

def fbm(x, y, seed, oct=4):
    s, a, f = 0.0, 0.5, 1.0
    for o in range(oct):
        s = s + a * vnoise(x * f, y * f, seed + o); a *= 0.5; f *= 2.0
    return s

def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

# bristle rows: a per-row value that changes every ~3 px vertically, smooth along x
# --- the indigo wash (reference: slate-indigo, darkest across the upper middle, cooling to a
# lighter blue toward the lower-left and the right, where it dissolves in soft dry-brush patches;
# watercolour-like mottling and a faint horizontal brush drag, no hard stripes) ---
drag = fbm(xx / 70.0, yy / 7.0, 5)                       # horizontal brush drag (soft, not hair-thin)
patch = fbm(xx / 34.0, yy / 14.0, 9)                     # patchy dry-brush break-up for the edges
mott = fbm(xx / 150.0, yy / 80.0, 21)                    # large watercolour mottling
# soft, uneven edges
right = 1 - sstep(680, 1010, xx + (patch - 0.5) * 120 + (drag - 0.5) * 50)
left = sstep(18, 52, xx + (patch - 0.5) * 26)
top = sstep(28, 56, yy + (fbm(xx / 60.0, 0 * yy, 11) - 0.5) * 16)
bot = 1 - sstep(324, 364, yy + (fbm(xx / 45.0, 0 * yy + 3, 12) - 0.5) * 24)
alpha = 0.93 * right * left * top * bot
# dry-brush: inside the fading margins the paint breaks into patches following the drag
edge = 1 - sstep(0.55, 0.95, alpha / 0.93)
alpha *= np.clip(1 - edge * sstep(0.35, 0.7, 1 - patch * 0.7 - drag * 0.3) * 0.75, 0, 1)
# colour: deep slate-indigo core, cooler lighter blue toward edges / lower-left
core = np.array([0.225, 0.26, 0.345], np.float32)       # ~ #3C4455
deep = np.array([0.20, 0.225, 0.29], np.float32)          # darker band across the upper middle
cool = np.array([0.36, 0.42, 0.54], np.float32)           # ~ #5C6B8A toward the edges
band = np.exp(-((yy - 130) / 90.0) ** 2) * sstep(60, 300, xx) * (1 - sstep(560, 820, xx))
t_edge = np.clip(edge * 0.6 + sstep(600, 990, xx) * 0.6 + sstep(250, 370, yy) * (1 - sstep(80, 420, xx)) * 0.5 + (mott - 0.5) * 0.5, 0, 1)
rgb = core * (1 - t_edge[..., None]) + cool * t_edge[..., None]
rgb = rgb * (1 - band[..., None] * 0.55) + deep * band[..., None] * 0.55
rgb *= (1 + (drag - 0.5) * 0.10 + (mott - 0.5) * 0.08)[..., None]
alpha *= np.clip(0.92 + (drag - 0.5) * 0.18, 0, 1)
img = np.dstack([rgb, alpha])

def line(img, x0, y0, x1, y1, w, col, a, fade_from=None):
    # thin, slightly uneven gold line; optional fade toward the end
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(n):
        f = i / max(n - 1, 1)
        x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
        k = a * (0.8 + 0.2 * h(i * 0.37 + x0))
        if fade_from is not None and f > fade_from:
            k *= 1 - (f - fade_from) / (1 - fade_from)
        xi, yi = int(round(x)), int(round(y))
        r = w / 2
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                px, py = xi + dx, yi + dy
                if 0 <= px < W and 0 <= py < H:
                    d = np.hypot(dx, dy)
                    cov = np.clip(r + 0.5 - d, 0, 1) * k
                    if cov <= 0: continue
                    ca = img[py, px, 3]
                    oa = cov + ca * (1 - cov)
                    img[py, px, :3] = (np.array(col) * cov + img[py, px, :3] * ca * (1 - cov)) / max(oa, 1e-4)
                    img[py, px, 3] = oa

gold = (0.86, 0.72, 0.46)

def over_px(img, px, py, cov, col):
    if 0 <= px < W and 0 <= py < H and cov > 0:
        ca = img[py, px, 3]
        oa = cov + ca * (1 - cov)
        img[py, px, :3] = (np.array(col) * cov + img[py, px, :3] * ca * (1 - cov)) / max(oa, 1e-4)
        img[py, px, 3] = oa

def pen(img, pts, w, col, a, seed, wobble=2.2, fade_from=None, dry=0.08):
    # a hand-drawn ink/gold line: the path wanders a little, the width swells and thins,
    # and the nib skips (dry gaps) now and then - never a ruler-straight, even line
    pts = np.asarray(pts, np.float32)
    seg = np.diff(pts, axis=0); L = np.hypot(seg[:, 0], seg[:, 1]); total = L.sum()
    n = int(total * 2) + 2
    for k in range(n):
        t = k / (n - 1); d = t * total
        j = min(np.searchsorted(np.cumsum(L), d), len(L) - 1)
        d0 = np.cumsum(L)[j] - L[j]; u = (d - d0) / max(L[j], 1e-4)
        x, y = pts[j] + seg[j] * u
        nx, ny = -seg[j][1] / max(L[j], 1e-4), seg[j][0] / max(L[j], 1e-4)
        off = (float(vnoise(np.float32(d / 55.0), np.float32(0), seed)) - 0.5) * 2 * wobble \
            + (float(vnoise(np.float32(d / 13.0), np.float32(3), seed)) - 0.5) * 0.8
        x += nx * off; y += ny * off
        r = w * 0.5 * (0.45 + 0.9 * float(vnoise(np.float32(d / 40.0), np.float32(7), seed)))
        k_a = a * (0.75 + 0.25 * float(vnoise(np.float32(d / 9.0), np.float32(11), seed)))
        if float(vnoise(np.float32(d / 7.0), np.float32(17), seed)) < dry:
            k_a *= 0.0
        if fade_from is not None and t > fade_from:
            k_a *= max(0.0, 1 - (t - fade_from) / (1 - fade_from)) ** 1.5
        xi, yi = int(np.floor(x)), int(np.floor(y))
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                dist = np.hypot(xi + dx + 0.5 - x, yi + dy + 0.5 - y)
                cov = float(np.clip(r + 0.5 - dist, 0, 1)) * k_a * 0.5
                over_px(img, xi + dx, yi + dy, cov, col)

# frame: left side, top (with a faint second stroke that drifts off), short bottom;
# lines overshoot a little at the corners with a small curl, as if drawn by hand
pen(img, [(17, 8), (15, 190), (18, 376)], 4.6, gold, 1.0, seed=1)
pen(img, [(4, 23), (300, 21), (620, 24), (860, 20)], 4.4, gold, 1.0, seed=2, fade_from=0.62)
pen(img, [(240, 15), (520, 13), (700, 16)], 2.6, gold, 0.6, seed=3, fade_from=0.4, dry=0.25)
pen(img, [(4, 362), (180, 364), (360, 361)], 4.0, gold, 0.95, seed=4, fade_from=0.5)
for (cx, cy, sd) in [(16, 22, 5), (16, 362, 6)]:
    # a small ink knot where the drawn lines cross
    pen(img, [(cx - 2, cy - 1), (cx + 2, cy + 1)], 6.0, gold, 1.0, seed=sd, wobble=0, dry=0.0)
# the engine's UI blend treats alpha roughly like a gamma-2.2 value (alpha 0.86 shows as ~0.5),
# so pre-compensate: store alpha^(1/2.2) and the panel lands at the painted opacity in game
img[..., 3] = np.clip(img[..., 3], 0, 1) ** (1 / 2.2)
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), "RGBA").save("quest_panel_v5.png")
print("ok")
