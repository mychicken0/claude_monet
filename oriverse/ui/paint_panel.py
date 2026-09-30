# Paints the HUD panel background (hud_panel.png, RGBA): overlapping horizontal oil-paint
# strokes in slate blue / lilac / teal. Each stroke is a bundle of bristle streaks; smooth
# noise breaks the streaks into dry-brush gaps toward the tail and along the outer edge.
# Rendered at 2x and downsampled so every edge is soft.
import numpy as np
from PIL import Image
S = 2
W, H = 1024 * S, 384 * S
rng = np.random.default_rng(11)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
rgb = np.zeros((H, W, 3), np.float32)
a = np.zeros((H, W), np.float32)

def over(col, alpha):
    global rgb, a
    alpha = np.clip(alpha, 0, 1)
    out_a = alpha + a * (1 - alpha)
    rgb = (col * alpha[..., None] + rgb * (a * (1 - alpha))[..., None]) / np.maximum(out_a, 1e-4)[..., None]
    a = out_a

def h(i):
    return (np.sin(i * 12.9898 + 78.233) * 43758.5453) % 1.0

def noise1(t, k):
    # smooth value noise along t, independent per bristle k
    i = np.floor(t); f = t - i; f = f * f * (3 - 2 * f)
    return h(i + k * 57.3) * (1 - f) + h(i + 1 + k * 57.3) * f

def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

def stroke(x0, x1, yc, hh, col, alpha, dry=0.35, bend=0.0, seed=0):
    x0 *= S; x1 *= S; yc *= S; hh *= S; bend *= S
    lo, hi = int(max(yc - hh - abs(bend) - 4, 0)), int(min(yc + hh + abs(bend) + 4, H))
    X = xx[lo:hi]; Y = yy[lo:hi]
    u = (X - x0) / (x1 - x0)
    v = (Y - yc - bend * np.sin(np.clip(u, 0, 1) * np.pi)) / hh
    # rounded loaded head, long tapering tail; a wobbly outline
    head = np.sqrt(np.clip(u / 0.06, 0, 1))
    tail = 1 - 0.6 * sstep(0.55, 1.0, u)
    wob = 0.9 + 0.1 * noise1(u * 14, seed + 3)
    prof = head * tail * wob
    nb = hh / (1.6 * S)
    k = np.floor((v + 1) * 0.5 * nb)
    brv = h(k + seed * 13.0)
    # dry brush: streaks break up more toward the tail and on the stroke's outer bristles
    dryness = dry * sstep(0.35, 1.0, u) + 0.25 * sstep(0.6, 1.0, np.abs(v))
    gaps = sstep(dryness - 0.08, dryness + 0.08, noise1(u * (x1 - x0) / (26 * S), k + seed))
    body = sstep(0.0, 0.08, prof - np.abs(v)) * sstep(0.0, 0.01, u) * sstep(0.0, 0.01, 1 - u)
    m = body * gaps
    shade = (0.86 + 0.26 * brv)[..., None]
    sub = rgb[lo:hi].copy(); suba = a[lo:hi].copy()
    al = np.clip(m * alpha, 0, 1)
    out_a = al + suba * (1 - al)
    c = np.asarray(col, np.float32)[None, None, :] * shade
    rgb[lo:hi] = (c * al[..., None] + sub * (suba * (1 - al))[..., None]) / np.maximum(out_a, 1e-4)[..., None]
    a[lo:hi] = out_a

# underpainting: a dark wash filling the middle, so the text always sits on solid paint;
# its edge is broken by noise, the strokes above carry the ragged outline
dx = np.maximum(np.maximum(90 * S - xx, xx - (W - 90 * S)), 0) / S
dy = np.maximum(np.maximum(52 * S - yy, yy - (H - 52 * S)), 0) / S
edge_n = noise1(yy / (9 * S), 7.0) * 30 + noise1(xx / (11 * S), 9.0) * 14
wash = 1 - sstep(0, 40, np.sqrt(dx * dx + dy * dy) + edge_n - 12)
over(np.array([0.15, 0.19, 0.28], np.float32)[None, None, :], wash * 0.82)
base = [(0.16, 0.20, 0.30), (0.19, 0.24, 0.36), (0.22, 0.28, 0.41), (0.26, 0.26, 0.39),
        (0.17, 0.27, 0.32), (0.28, 0.32, 0.46)]
# underlayer: long strokes, ragged ends, alternating direction
y = 34
while y < 384 - 30:
    hh = rng.uniform(14, 24)
    left, right = rng.uniform(10, 70), 1024 - rng.uniform(10, 80)
    col = base[rng.integers(len(base))]
    if rng.random() < 0.5:
        stroke(left, right, y, hh, col, 0.9, dry=0.75, bend=rng.uniform(-5, 5), seed=y)
    else:
        stroke(right, left, y, hh, col, 0.9, dry=0.75, bend=rng.uniform(-5, 5), seed=y)
    y += hh * rng.uniform(0.95, 1.3)
# broken colour on top: shorter strokes
for i in range(60):
    L = rng.uniform(140, 420)
    xs = rng.uniform(40, 1024 - 40 - L)
    yc = rng.uniform(50, 384 - 50)
    hh = rng.uniform(6, 13)
    col = tuple(c * rng.uniform(0.95, 1.2) for c in base[rng.integers(len(base))])
    if rng.random() < 0.5:
        stroke(xs, xs + L, yc, hh, col, 0.5, dry=0.9, bend=rng.uniform(-3, 3), seed=1000 + i)
    else:
        stroke(xs + L, xs, yc, hh, col, 0.5, dry=0.9, bend=rng.uniform(-3, 3), seed=1000 + i)
# faint cream / gold dry-brush rim, top and bottom
stroke(rng.uniform(40, 100), 1024 - rng.uniform(60, 160), 26, 4.5, (0.93, 0.85, 0.64), 0.5, dry=0.9, seed=5001)
stroke(1024 - rng.uniform(40, 100), rng.uniform(80, 200), 384 - 28, 4.0, (0.93, 0.85, 0.64), 0.4, dry=0.95, seed=5002)
a *= 0.88
img = np.dstack([np.clip(rgb, 0, 1) * a[..., None], a])  # premultiply for clean downsampling
im = Image.fromarray((img * 255).astype(np.uint8), "RGBA").resize((1024, 384), Image.LANCZOS)
arr = np.asarray(im).astype(np.float32) / 255
al = arr[..., 3:4]
arr[..., :3] = np.where(al > 1e-3, arr[..., :3] / np.maximum(al, 1e-3), 0)
Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGBA").save("hud_panel.png")
print("ok")
