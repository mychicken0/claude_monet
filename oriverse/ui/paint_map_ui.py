# Paints the map-screen backings (RGBA PNGs):
#   map_paper.png       the blank map sheet: pale warm parchment with soft watercolour stains,
#                       darker worn edges, a fine torn outline, a faint inner rule and a soft shadow
#   map_side_panel.png  the side panel: charcoal slate paper with a torn, slightly dry-brushed edge
# Both are painted larger than they draw (paper 1160x728 base units, panel 336x560).
# The UI blend treats image alpha roughly like a gamma-2.2 value, so alpha is stored as alpha^(1/2.2)
# (same step as paint_panel.py). Pass --straight to keep true alpha (for local mock-ups).
import sys
import numpy as np
from PIL import Image

STRAIGHT = "--straight" in sys.argv
OUT = "."
for a in sys.argv[1:]:
    if not a.startswith("--"):
        OUT = a


def vnoise(w, h, cell, seed):
    """Smooth value noise in 0..1 with features about `cell` px wide."""
    r = np.random.default_rng(seed)
    gw, gh = int(w / cell) + 4, int(h / cell) + 4
    g = Image.fromarray(r.random((gh, gw)).astype(np.float32), mode="F")
    big = g.resize((int(gw * cell), int(gh * cell)), Image.BICUBIC)
    return np.clip(np.asarray(big, dtype=np.float32)[:h, :w], 0, 1)


def fbm(w, h, cell, seed, octaves=4):
    s, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        s = s + amp * vnoise(w, h, max(cell / 2 ** o, 1.5), seed * 31 + o)
        tot += amp
        amp *= 0.5
    return s / tot


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def rgb(hexstr):
    return np.array([int(hexstr[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32) / 255


def mix(a, b, t):
    return a + (b - a) * t[..., None]


def rounded_inside(w, h, radius):
    """Distance (px) from each pixel to the outline of a rounded rectangle filling the image; >0 inside."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    qx = np.abs(xx - w / 2) - (w / 2 - radius)
    qy = np.abs(yy - h / 2) - (h / 2 - radius)
    out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - radius
    return -out


def blur(arr, radius):
    # separable gaussian (PIL's GaussianBlur does not take float images)
    n = max(int(radius * 3), 1)
    k = np.exp(-0.5 * (np.arange(-n, n + 1) / radius) ** 2).astype(np.float32)
    k /= k.sum()
    a = np.pad(arr.astype(np.float32), ((n, n), (n, n)), mode="edge")
    a = sum(k[i] * a[:, i:i + arr.shape[1]] for i in range(2 * n + 1))
    a = sum(k[i] * a[i:i + arr.shape[0], :] for i in range(2 * n + 1))
    return a


def save(name, col, alpha):
    if not STRAIGHT:
        alpha = np.power(np.clip(alpha, 0, 1), 1 / 2.2)
    out = np.dstack([np.clip(col, 0, 1), np.clip(alpha, 0, 1)[..., None]])
    Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA").save(f"{OUT}/{name}", optimize=True)
    print(name, out.shape[1], "x", out.shape[0])


# ------------------------------------------------------------------ paper
def paint_paper():
    S = 1.75
    W, H = int(1160 * S), int(728 * S)
    d = rounded_inside(W, H, 10 * S)
    # torn outline: a slow wander, nicks, fine fuzz, and a few deeper bites
    wander = fbm(W, H, 150 * S, 11, 2) - 0.5
    nick = fbm(W, H, 20 * S, 12, 2) - 0.5
    fuzz = vnoise(W, H, 2.4 * S, 13) - 0.5
    bite = sstep(0.70, 0.86, vnoise(W, H, 46 * S, 14))
    thr = (10 + wander * 5 + nick * 6 + fuzz * 4.2 + bite * 5) * S
    inner = d - thr                                   # px inside the torn outline
    mask = np.clip(inner / 1.3 + 0.5, 0, 1)

    # paper tone: pale warm cream, slow drift, soft watercolour mottling
    drift = fbm(W, H, 520 * S, 21, 3)
    mott = fbm(W, H, 110 * S, 22, 4)
    col = mix(rgb("#D5C2A5"), rgb("#E7D4B9"), sstep(0.2, 0.8, drift * 0.6 + mott * 0.4))
    # grey-brown age stains: loose patches everywhere, heavier toward the edges and corners
    reach = (60 + 170 * fbm(W, H, 260 * S, 23, 3)) * S
    pool = np.clip(1 - inner / reach, 0, 1) ** 1.6
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    corner = (np.abs(xx / W - 0.5) * 2) ** 3 * (np.abs(yy / H - 0.5) * 2) ** 3
    wash = fbm(W, H, 210 * S, 24, 5)
    stain = sstep(0.50, 1.05, pool * 0.55 + wash * 0.62 + corner * 0.35)
    col = mix(col, rgb("#B49E80"), stain * 0.70)
    # dirtier, mottled band hugging the edge
    band = (1 - sstep(0, 46 * S, inner)) * (0.35 + 0.65 * fbm(W, H, 38 * S, 30, 3))
    col = mix(col, rgb("#B89E7C"), band * 0.50)
    # soft mid-size mottling across the sheet
    blot = sstep(0.52, 0.80, fbm(W, H, 48 * S, 32, 3))
    col = mix(col, rgb("#C2AD8F"), blot * 0.26)
    # a few pale blooms and small foxing specks
    bloom = sstep(0.60, 0.85, fbm(W, H, 300 * S, 25, 3)) * (1 - pool)
    col = mix(col, rgb("#EDDDC4"), bloom * 0.35)
    speck = sstep(0.86, 0.95, vnoise(W, H, 4.5 * S, 28)) * sstep(0.5, 0.75, fbm(W, H, 160 * S, 29, 2))
    col = mix(col, rgb("#A39178"), speck * 0.09)
    # worn dark lip at the tear
    lip = 1 - sstep(0, 5 * S, inner)
    col = mix(col, rgb("#8E775A"), lip * 0.55)
    # faint hand-ruled line a little inside the edge, broken here and there
    wob = (fbm(W, H, 90 * S, 26, 2) - 0.5) * 3 * S
    rule = np.exp(-((inner - 10 * S - wob) / (0.8 * S)) ** 2)
    broken = sstep(0.38, 0.55, fbm(W, H, 70 * S, 27, 2))
    col = mix(col, rgb("#6F5C45"), rule * broken * 0.38)
    # fine grain and soft fibres
    r = np.random.default_rng(31)
    grain = blur(r.normal(0, 1, (H, W)), 0.7 * S)
    fibre = blur(r.normal(0, 1, (H, W)), 2.2 * S)
    col = col * (1 + grain[..., None] * 0.030 + fibre[..., None] * 0.045)

    # soft shadow under the sheet
    sh = blur(mask, 5 * S)
    sh = np.roll(sh, int(3 * S), axis=0) * 0.42
    alpha = mask + (1 - mask) * sh
    col = col * (mask / np.maximum(alpha, 1e-4))[..., None]
    save("map_paper.png", col, alpha)


# ------------------------------------------------------------------ side panel
def paint_panel():
    S = 2.0
    W, H = int(336 * S), int(560 * S)
    d = rounded_inside(W, H, 8 * S)
    wander = fbm(W, H, 90 * S, 41, 2) - 0.5
    nick = fbm(W, H, 13 * S, 42, 2) - 0.5
    fuzz = vnoise(W, H, 2.6 * S, 43) - 0.5
    thr = (7 + wander * 5 + nick * 6 + fuzz * 2.6) * S
    inner = d - thr
    mask = np.clip(inner / 1.3 + 0.5, 0, 1)
    # dry-brush break-up right at the edge: short horizontal bristle skips
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    bristle = vnoise(W, max(H // 3, 4), 26 * S, 44)
    bristle = np.asarray(Image.fromarray(bristle, mode="F").resize((W, H), Image.BILINEAR), dtype=np.float32)
    skip = sstep(0.60, 0.80, bristle) * (1 - sstep(0, 5 * S, inner))
    mask = mask * (1 - skip * 0.7)

    drift = fbm(W, H, 300 * S, 51, 3)
    mott = fbm(W, H, 70 * S, 52, 4)
    col = mix(rgb("#25282C"), rgb("#32363C"), sstep(0.15, 0.85, drift * 0.55 + mott * 0.45))
    drag = fbm(W, max(H // 6, 4), 60 * S, 53, 2)
    drag = np.asarray(Image.fromarray(drag, mode="F").resize((W, H), Image.BILINEAR), dtype=np.float32)
    col = col * (0.965 + drag[..., None] * 0.07)
    r = np.random.default_rng(54)
    grain = blur(r.normal(0, 1, (H, W)), 0.7 * S)
    col = col * (1 + grain[..., None] * 0.035)
    # a slightly darker rim
    rim = 1 - sstep(0, 22 * S, inner)
    col = col * (1 - rim[..., None] * 0.12)

    alpha = mask * 0.965
    save("map_side_panel.png", col, alpha)


paint_paper()
paint_panel()
