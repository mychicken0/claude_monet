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
rows = vnoise(xx / 220.0, yy / 7.0, 5) * 0.7 + vnoise(xx / 80.0, yy / 3.0, 6) * 0.3
# wash extent with brushy edges
right = 1 - sstep(760, 960, xx + (rows - 0.5) * 200 + (fbm(xx / 30.0, yy / 25.0, 9) - 0.5) * 110)
left = sstep(22, 44, xx + (rows - 0.5) * 16)
top = sstep(30, 46, yy + (fbm(xx / 45.0, 0 * yy, 11) - 0.5) * 22)
bot = 1 - sstep(338, 358, yy + (fbm(xx / 40.0, 0 * yy + 3, 12) - 0.5) * 26)
alpha = 0.97 * right * left * top * bot
# dry-brush breaks inside the fading edges only
dry = sstep(0.25, 0.75, alpha / 0.97)
alpha *= np.clip(0.6 + 0.4 * dry + (rows - 0.5) * (1 - dry) * 1.2, 0, 1)
# slate colour: darker toward the left/center, a little cooler and lighter toward the fading edge
mott = fbm(xx / 140.0, yy / 90.0, 21) - 0.5
base = np.array([0.20, 0.23, 0.31], np.float32)
light = np.array([0.27, 0.30, 0.39], np.float32)
t = np.clip(xx / 1000.0 * 0.6 + mott * 0.5 + (rows - 0.5) * 0.25, 0, 1)[..., None]
rgb = base * (1 - t) + light * t
rgb *= (1 + (rows - 0.5) * 0.06)[..., None]

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

gold = (0.88, 0.73, 0.45)
line(img, 16, 22, 16, 362, 3.6, gold, 1.0)                    # left
line(img, 16, 22, 820, 22, 3.6, gold, 1.0, fade_from=0.72)    # top, fading out to the right
line(img, 16, 362, 330, 362, 3.6, gold, 0.95, fade_from=0.6)    # bottom, shorter
for (cx, cy) in [(16, 22), (16, 362)]:                          # corner dots
    line(img, cx - 4, cy, cx + 4, cy, 5.0, gold, 1.0)
Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8), "RGBA").save("quest_panel_v2.png")
print("ok")
