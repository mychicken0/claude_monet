# Traveler base bodies (male, female): anatomy tables -> closed ring lofts + ellipsoid masses.
# One source for two outputs:
#   python3 traveler_body.py render <out.png> [male|female]                  local flat-shaded front/back/side sheet
#   python3 traveler_body.py weave  <out.weave> [male|female] [--no-textures]  the #mesh source for the Oriverse world
# The module-level tables are the male body; FEMALE holds the same names for the female body (select("female")).
# Both meshes share the TravelerSkin / TravelerCloth textures: emit the second one with --no-textures.
# Frame: cm, Z up, the character FACES +X, LEFT hand = +Y (Oriverse canon). T-pose rest.
# The right side (negative Y) is authored; the left side is its mirror.
import sys
import numpy as np

NAME = "TravelerBody"
HEIGHT = 180.0

# ---------------------------------------------------------------- anatomy tables
# torso: z, half width (y), front depth (+x), back depth (-x), superellipse exponent
TORSO = [
    (84, 5.0, 5.0, 6.0, 2.2),
    (88, 13.5, 8.0, 9.5, 2.4),
    (93, 16.5, 9.5, 11.5, 2.6),     # hips
    (98, 16.8, 9.8, 11.2, 2.6),
    (104, 15.5, 9.6, 9.6, 2.5),
    (111, 14.2, 9.4, 8.6, 2.4),     # waist
    (118, 14.8, 10.0, 9.0, 2.5),
    (125, 16.2, 11.0, 10.0, 2.6),
    (132, 17.5, 12.2, 10.8, 2.8),   # chest
    (138, 18.2, 12.4, 11.0, 2.8),
    (143, 18.5, 11.2, 11.0, 2.7),
    (147, 17.5, 9.5, 10.5, 2.5),
    (150.5, 13.0, 7.5, 9.0, 2.3),   # shoulder slope
    (153, 8.0, 6.2, 7.5, 2.1),
    (156, 6.0, 5.8, 6.2, 2.0),      # neck
    (161, 5.8, 6.0, 6.0, 2.0),
]
# head: z, half width, front, back, exponent (centre pushed 1 cm forward)
HEAD_CX = 1.0
HEAD = [
    (156.5, 5.0, 6.2, 5.2, 2.0),
    (159.5, 6.4, 8.8, 6.4, 2.1),    # chin / jaw
    (163.5, 7.5, 9.8, 8.6, 2.2),
    (168, 8.1, 10.0, 9.6, 2.3),     # cheeks
    (172.5, 8.2, 9.8, 10.0, 2.3),   # brow
    (176.5, 7.5, 8.8, 9.4, 2.2),
    (179, 5.2, 6.2, 6.8, 2.0),
    (180.5, 2.0, 2.4, 2.8, 2.0),
]
# right arm, T-pose along -Y from the shoulder joint: distance out, front (+x), back (-x), up, down, exponent
SHOULDER = np.array([0.0, -19.0, 145.0])
ELBOW_D, WRIST_D, TIP_D = 28.0, 53.0, 71.0
ARM = [
    (-5, 5.0, 5.0, 3.4, 5.6, 2.0),
    (0, 6.0, 6.0, 4.2, 6.2, 2.2),
    (4, 6.2, 6.0, 5.6, 6.4, 2.2),   # deltoid
    (9, 5.8, 5.6, 5.7, 6.0, 2.2),
    (15, 5.3, 5.0, 5.0, 5.3, 2.1),  # biceps / triceps
    (22, 4.7, 4.5, 4.4, 4.6, 2.1),
    (28, 4.2, 4.1, 4.0, 4.0, 2.0),  # elbow
    (32, 4.6, 4.4, 4.4, 4.2, 2.1),  # forearm
    (40, 4.0, 3.8, 3.6, 3.6, 2.1),
    (48, 3.1, 3.1, 2.6, 2.6, 2.0),
    (53, 2.9, 2.9, 2.1, 2.1, 2.2),  # wrist
    (56, 4.2, 4.0, 2.0, 2.0, 3.0),  # palm
    (61, 4.8, 4.4, 1.9, 1.9, 3.5),
    (66, 4.4, 4.2, 1.7, 1.7, 3.5),
    (71, 3.2, 3.0, 1.4, 1.4, 3.0),  # finger tips (mitten)
]
# right leg, bottom up: z, centre x, centre y, half width outer (-y), inner (+y), front, back, exponent
LEG = [
    (4, 0.5, -11.5, 3.4, 3.2, 3.6, 4.6, 2.0),
    (10, 0.8, -11.4, 3.3, 3.2, 3.5, 3.7, 2.0),   # ankle
    (18, 0.5, -11.3, 3.8, 3.6, 3.9, 4.4, 2.0),
    (27, 0.3, -11.2, 4.8, 4.5, 4.5, 5.8, 2.1),
    (36, 0.3, -11.0, 5.8, 5.3, 4.9, 6.8, 2.2),   # calf
    (44, 0.8, -10.8, 5.4, 5.2, 5.4, 5.8, 2.2),
    (50, 1.6, -10.6, 5.6, 5.4, 6.2, 5.2, 2.2),   # knee
    (56, 1.2, -10.4, 6.0, 5.8, 6.6, 5.8, 2.2),
    (65, 0.8, -10.1, 7.0, 6.6, 7.8, 7.0, 2.3),
    (75, 0.4, -9.8, 8.0, 7.6, 8.8, 8.2, 2.4),
    (84, 0.0, -9.6, 8.6, 8.2, 9.2, 9.4, 2.4),
    (91, 0.0, -9.5, 8.4, 8.2, 8.8, 10.2, 2.4),
    (96, 0.0, -9.3, 7.0, 7.0, 7.5, 9.0, 2.2),
]
# right foot along +X: x, half width, height
FOOT_CY = -11.5
FOOT = [(-6.5, 2.4, 4.5), (-3, 3.3, 7.5), (2, 3.8, 8.5), (7, 4.4, 6.0), (12, 4.8, 4.0), (17, 4.6, 2.8), (20.5, 3.4, 1.8)]
# muscle masses (right side; mirrored): centre, radii
LUMPS = [
    ("ell", (-7.0, -7.5, 94.0), (4.6, 7.2, 7.2)),      # glute (centre, radii)
]
THUMB = ((4.0, -74.0, 145.0), (9.0, -80.0, 144.0), 2.8)   # start, end, thickness (right hand)
EAR = ((0.5, -8.3, 166.5), (2.6, 1.6, 5.6))
# face planes on the centre line: (size, centre)
FACE = [((3.0, 2.8, 5.0), (10.8, 0.0, 167.2)),    # nose
        ((2.2, 11.6, 2.0), (9.6, 0.0, 171.6))]    # brow ridge

# fitted garments = the body tables grown by GAP, fused on their own (a second material, a clean hem).
# torso / leg: the z range each tube covers; lumps: indices into LUMPS it must also cover; gusset: centre, radii of the
# ellipsoid closing the gap under the torso; p / secs / band only name the DSL variables.
GAP = 1.5
GARMENTS = [
    dict(name="trunks", p="tr", secs="t", band="hips", torso=(86.5, 103.0), leg=(81.0, 96.0), lumps=[0],
         gusset=((-0.5, 0, 85), (7.8, 6.8, 3.4)), verts=420),
]
# how far a garment vertex may look for skin to copy weights from (cap vertices sit deep inside the torso)
REACH = 8
# where each bone's skin region starts (z unless noted): see the region list in weave()
SKIN = dict(spine=101, torso=114, neck=152, neck_w=12, head=158, arm_z=120, thigh=86, shin=48, foot=9, toe_x=12)
# wearable mount points (bone-pinned): name, position, axis, bone. Rigid pieces attach with AttachToAnchor(body, name).
SOCKETS = [
    ("Hat", (1, 0, 181), (0, 0, 1), "Head"), ("Face", (11, 0, 169), (1, 0, 0), "Head"),
    ("Chest", (12.5, 0, 134), (1, 0, 0), "Torso"), ("Back", (-11.5, 0, 132), (-1, 0, 0), "Torso"),
    ("BeltFront", (10, 0, 103), (1, 0, 0), "Root"), ("BeltBack", (-10, 0, 103), (-1, 0, 0), "Root"),
    ("HipR", (0, -17.5, 97), (0, -1, 0), "Root"), ("HipL", (0, 17.5, 97), (0, 1, 0), "Root"),
    ("ShoulderR", (0, -19, 150), (0, 0, 1), "ScapulaR"), ("ShoulderL", (0, 19, 150), (0, 0, 1), "ScapulaL"),
    ("HoldR", (0, -80, 143), (1, 0, 0), "HandR"), ("HoldL", (0, 80, 143), (1, 0, 0), "HandL"),
]

# rig (canon names). Knees sit 2 cm forward so leg IK knows which way to bend.
BONES = [
    ("Root", (0, 0, 96), None), ("Spine", (0, 0, 104), "Root"), ("Torso", (0, 0, 118), "Spine"),
    ("Neck", (0, 0, 151), "Torso"), ("Head", (0, 0, 157.5), "Neck"),
    ("ScapulaR", (0, -7, 148), "Torso"), ("UpperArmR", (0, -19, 145), "ScapulaR"),
    ("ForearmR", (0, -19 - ELBOW_D, 145), "UpperArmR"), ("HandR", (0, -19 - WRIST_D, 145), "ForearmR"),
    ("ScapulaL", (0, 7, 148), "Torso"), ("UpperArmL", (0, 19, 145), "ScapulaL"),
    ("ForearmL", (0, 19 + ELBOW_D, 145), "UpperArmL"), ("HandL", (0, 19 + WRIST_D, 145), "ForearmL"),
    ("ThighR", (0, -9.6, 92), "Root"), ("ShinR", (2.2, -10.6, 50), "ThighR"),
    ("FootR", (0.8, -11.4, 10), "ShinR"), ("ToeR", (13, -11.5, 2), "FootR"),
    ("ThighL", (0, 9.6, 92), "Root"), ("ShinL", (2.2, 10.6, 50), "ThighL"),
    ("FootL", (0.8, 11.4, 10), "ShinL"), ("ToeL", (13, 11.5, 2), "FootL"),
]

# ---------------------------------------------------------------- female body (same names as above)
_FS = np.array([0.0, -16.5, 135.0])
_FE, _FW = 26.0, 49.0
FEMALE = dict(
    NAME="TravelerBodyF", HEIGHT=168.0, REACH=20,
    TORSO=[
        (78, 5.0, 5.0, 6.0, 2.2),
        (82, 13.8, 8.0, 9.5, 2.4),
        (87, 17.2, 9.3, 11.5, 2.6),     # hips
        (92, 16.8, 9.4, 11.0, 2.6),
        (98, 14.2, 8.8, 9.2, 2.5),
        (104, 12.0, 8.2, 7.8, 2.4),     # waist
        (110, 12.4, 8.6, 8.0, 2.4),
        (116, 13.4, 9.4, 8.8, 2.5),     # ribcage
        (122, 14.4, 10.2, 9.4, 2.6),    # bust line (the breasts are LUMPS[1])
        (127, 15.0, 10.0, 9.6, 2.6),
        (132, 15.4, 9.2, 9.6, 2.6),
        (136, 14.8, 8.0, 9.2, 2.5),
        (139.5, 11.0, 6.6, 8.0, 2.3),   # shoulder slope
        (142, 6.8, 5.4, 6.6, 2.1),
        (145, 5.0, 5.0, 5.4, 2.0),      # neck
        (150, 4.8, 5.2, 5.2, 2.0),
    ],
    HEAD_CX=1.0,
    HEAD=[
        (145.5, 4.4, 5.6, 4.8, 2.0),
        (148.3, 5.6, 8.0, 6.0, 2.1),    # chin / jaw
        (152, 6.9, 9.2, 8.2, 2.2),
        (156.2, 7.6, 9.5, 9.2, 2.3),    # cheeks
        (160.5, 7.8, 9.3, 9.6, 2.3),    # brow
        (164.2, 7.2, 8.4, 9.0, 2.2),
        (166.6, 5.0, 6.0, 6.6, 2.0),
        (168, 2.0, 2.4, 2.8, 2.0),
    ],
    SHOULDER=_FS, ELBOW_D=_FE, WRIST_D=_FW, TIP_D=66.0,
    ARM=[
        (-5, 4.3, 4.3, 3.0, 4.8, 2.0),
        (0, 5.0, 5.0, 3.6, 5.3, 2.2),
        (4, 5.1, 5.0, 4.6, 5.4, 2.2),   # deltoid
        (9, 4.7, 4.6, 4.6, 5.0, 2.2),
        (15, 4.3, 4.1, 4.0, 4.3, 2.1),
        (21, 3.8, 3.7, 3.6, 3.8, 2.1),
        (26, 3.5, 3.4, 3.3, 3.3, 2.0),  # elbow
        (30, 3.8, 3.6, 3.6, 3.5, 2.1),  # forearm
        (37, 3.3, 3.2, 3.0, 3.0, 2.1),
        (44.5, 2.6, 2.6, 2.2, 2.2, 2.0),
        (49, 2.4, 2.4, 1.8, 1.8, 2.2),  # wrist
        (52, 3.6, 3.4, 1.7, 1.7, 3.0),  # palm
        (56.5, 4.1, 3.8, 1.6, 1.6, 3.5),
        (61, 3.8, 3.6, 1.5, 1.5, 3.5),
        (66, 2.8, 2.6, 1.2, 1.2, 3.0),  # finger tips (mitten)
    ],
    LEG=[
        (3.8, 0.5, -10.6, 3.1, 2.9, 3.3, 4.2, 2.0),
        (9.5, 0.8, -10.5, 3.0, 2.9, 3.2, 3.4, 2.0),   # ankle
        (17, 0.5, -10.4, 3.5, 3.3, 3.6, 4.1, 2.0),
        (25, 0.3, -10.3, 4.4, 4.1, 4.1, 5.3, 2.1),
        (33.5, 0.3, -10.2, 5.2, 4.8, 4.5, 6.2, 2.2),  # calf
        (41, 0.8, -10.1, 4.9, 4.8, 5.0, 5.3, 2.2),
        (46.5, 1.6, -10.0, 5.2, 5.1, 5.8, 4.9, 2.2),  # knee
        (52, 1.2, -9.9, 5.8, 5.6, 6.2, 5.5, 2.2),
        (60.5, 0.8, -9.8, 6.7, 6.4, 7.2, 6.7, 2.3),
        (70, 0.4, -9.7, 7.8, 7.4, 8.1, 7.8, 2.4),
        (78, 0.0, -9.6, 8.6, 8.2, 8.6, 9.0, 2.4),
        (84.5, 0.0, -9.5, 8.5, 8.2, 8.3, 9.8, 2.4),
        (89, 0.0, -9.3, 7.2, 7.2, 7.2, 8.8, 2.2),
    ],
    FOOT_CY=-10.6,
    FOOT=[(-6, 2.2, 4.2), (-2.8, 3.0, 7.0), (1.8, 3.4, 7.8), (6.4, 4.0, 5.5), (11, 4.3, 3.7), (15.5, 4.1, 2.6), (18.5, 3.0, 1.7)],
    LUMPS=[
        ("ell", (-7.0, -7.6, 88.0), (4.8, 7.4, 7.4)),     # glute
        ("ell", (7.4, -6.6, 122.5), (5.4, 6.0, 5.8)),     # breast
    ],
    THUMB=((3.6, -69.0, 135.0), (8.2, -74.5, 134.0), 2.5),
    EAR=((0.5, -7.9, 155.0), (2.4, 1.5, 5.2)),
    FACE=[((2.6, 2.4, 4.4), (10.2, 0.0, 155.6)),      # nose
          ((1.6, 10.6, 1.6), (9.0, 0.0, 159.8))],     # brow ridge (softer)
    GARMENTS=[
        dict(name="briefs", p="br", secs="b", band="hips", torso=(80.5, 94.5), leg=(75.5, 89.0), lumps=[0],
             gusset=((-0.5, 0, 79), (7.8, 6.8, 3.4)), verts=420),
        dict(name="bandeau", p="ba", secs="a", band="band", torso=(116.5, 126.5), leg=None, lumps=[1], gusset=None, verts=320),
    ],
    SKIN=dict(spine=94, torso=106, neck=141.5, neck_w=11, head=147, arm_z=110, thigh=80, shin=44.5, foot=9, toe_x=11),
    SOCKETS=[
        ("Hat", (1, 0, 168.5), (0, 0, 1), "Head"), ("Face", (10.5, 0, 157), (1, 0, 0), "Head"),
        ("Chest", (13.5, 0, 124), (1, 0, 0), "Torso"), ("Back", (-10, 0, 122), (-1, 0, 0), "Torso"),
        ("BeltFront", (9, 0, 97), (1, 0, 0), "Root"), ("BeltBack", (-10, 0, 97), (-1, 0, 0), "Root"),
        ("HipR", (0, -18, 90), (0, -1, 0), "Root"), ("HipL", (0, 18, 90), (0, 1, 0), "Root"),
        ("ShoulderR", (0, -16.5, 139.5), (0, 0, 1), "ScapulaR"), ("ShoulderL", (0, 16.5, 139.5), (0, 0, 1), "ScapulaL"),
        ("HoldR", (0, -73, 133.3), (1, 0, 0), "HandR"), ("HoldL", (0, 73, 133.3), (1, 0, 0), "HandL"),
    ],
    BONES=[
        ("Root", (0, 0, 89), None), ("Spine", (0, 0, 96.5), "Root"), ("Torso", (0, 0, 109.5), "Spine"),
        ("Neck", (0, 0, 140.5), "Torso"), ("Head", (0, 0, 146.5), "Neck"),
        ("ScapulaR", (0, -6.3, 137.8), "Torso"), ("UpperArmR", (0, -16.5, 135), "ScapulaR"),
        ("ForearmR", (0, -16.5 - _FE, 135), "UpperArmR"), ("HandR", (0, -16.5 - _FW, 135), "ForearmR"),
        ("ScapulaL", (0, 6.3, 137.8), "Torso"), ("UpperArmL", (0, 16.5, 135), "ScapulaL"),
        ("ForearmL", (0, 16.5 + _FE, 135), "UpperArmL"), ("HandL", (0, 16.5 + _FW, 135), "ForearmL"),
        ("ThighR", (0, -9.6, 85.5), "Root"), ("ShinR", (2.2, -10.0, 46.5), "ThighR"),
        ("FootR", (0.8, -10.5, 9.5), "ShinR"), ("ToeR", (12, -10.6, 2), "FootR"),
        ("ThighL", (0, 9.6, 85.5), "Root"), ("ShinL", (2.2, 10.0, 46.5), "ThighL"),
        ("FootL", (0.8, 10.5, 9.5), "ShinL"), ("ToeL", (12, 10.6, 2), "FootL"),
    ],
)


def select(variant):
    """Swap the module tables to a variant ("male" is the module default)."""
    if variant == "female":
        globals().update(FEMALE)
    elif variant != "male":
        raise SystemExit(f"unknown variant {variant}")


# ---------------------------------------------------------------- geometry
def densify(rows, extra=1):
    """Catmull-Rom between key stations so the lofts read smooth."""
    a = np.array(rows, dtype=float)
    if extra <= 0:
        return a
    out = []
    n = len(a)
    for i in range(n - 1):
        p0, p1, p2, p3 = a[max(i - 1, 0)], a[i], a[i + 1], a[min(i + 2, n - 1)]
        for s in range(extra + 1):
            t = s / (extra + 1)
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(a[-1])
    return np.array(out)


def superring(centre, u, v, up, um, vp, vm, exp, n):
    """Ring of n points: superellipse with separate half-extents on each side of u and v."""
    pts = []
    for j in range(n):
        th = 2 * np.pi * j / n
        c, s = np.cos(th), np.sin(th)
        e = 2.0 / exp
        du = (up if c > 0 else um) * np.sign(c) * abs(c) ** e
        dv = (vp if s > 0 else vm) * np.sign(s) * abs(s) ** e
        pts.append(np.array(centre) + du * np.array(u) + dv * np.array(v))
    return np.array(pts)


def lofts():
    """Returns {name: [ring, ...]} for the right side + centre parts. Rings wind CCW seen along the loft direction."""
    X, Y, Z = np.eye(3)
    parts = {}
    parts["torso"] = [superring((0, 0, z), X, Y, f, b, w, w, e, 14) for z, w, f, b, e in densify(TORSO)]
    parts["head"] = [superring((HEAD_CX, 0, z), X, Y, f, b, w, w, e, 10) for z, w, f, b, e in densify(HEAD)]
    parts["armR"] = [superring(SHOULDER + np.array([0, -d, 0]), X, Z, f, b, up, dn, e, 8) for d, f, b, up, dn, e in densify(ARM)]
    parts["legR"] = [superring((cx, cy, z), X, Y, f, b, wi, wo, e, 8) for z, cx, cy, wo, wi, f, b, e in densify(LEG)]
    foot = []
    for x, w, h in densify(FOOT):
        prof = [(-w, 0.3), (-w * 0.6, 0), (w * 0.6, 0), (w, 0.3), (w, h * 0.6), (w * 0.55, h), (-w * 0.55, h), (-w, h * 0.6)]
        foot.append(np.array([(x, FOOT_CY + y, z) for y, z in prof]))
    parts["footR"] = foot
    return parts


def mirror_ring(r):
    m = r.copy()
    m[:, 1] *= -1
    return m[::-1]


def all_lofts():
    p = lofts()
    out = dict(p)
    for k in ("armR", "legR", "footR"):
        out[k[:-1] + "L"] = [mirror_ring(r) for r in p[k]]
    return out


def loft_tris(rings):
    tris = []
    n = len(rings[0])
    for a, b in zip(rings[:-1], rings[1:]):
        for j in range(n):
            k = (j + 1) % n
            tris.append((a[j], a[k], b[k]))
            tris.append((a[j], b[k], b[j]))
    for ring, flip in ((rings[0], True), (rings[-1], False)):
        c = ring.mean(0)
        for j in range(n):
            k = (j + 1) % n
            tris.append((c, ring[k], ring[j]) if flip else (c, ring[j], ring[k]))
    return tris


def ellipsoid_tris(centre, radii, seg=10):
    c, r = np.array(centre, float), np.array(radii, float)
    lat = [np.pi * i / (seg // 2) for i in range(seg // 2 + 1)]
    pts = [[c + r * np.array([np.sin(a) * np.cos(2 * np.pi * j / seg), np.sin(a) * np.sin(2 * np.pi * j / seg), np.cos(a)]) for j in range(seg)] for a in lat]
    tris = []
    for i in range(len(lat) - 1):
        for j in range(seg):
            k = (j + 1) % seg
            tris.append((pts[i][j], pts[i + 1][j], pts[i + 1][k]))
            tris.append((pts[i][j], pts[i + 1][k], pts[i][k]))
    return tris


def lumps_both():
    out = []
    for kind, c, r in LUMPS:
        out.append((kind, c, r))
        out.append((kind, (c[0], -c[1], c[2]), r))
    return out


def soup():
    tris = []
    for rings in all_lofts().values():
        tris += loft_tris(rings)
    for kind, c, r in lumps_both():
        if kind == "ell":
            tris += ellipsoid_tris(c, r)
        else:   # box: 4-sided loft through its two end faces
            c, h = np.array(c), np.array(r) / 2
            ring = lambda z: np.array([(c[0] + h[0], c[1] - h[1], z), (c[0] + h[0], c[1] + h[1], z), (c[0] - h[0], c[1] + h[1], z), (c[0] - h[0], c[1] - h[1], z)])
            tris += loft_tris([ring(c[2] - h[2]), ring(c[2] + h[2])])
    for sz, c in FACE:
        c, h = np.array(c), np.array(sz) / 2
        ring = lambda z: np.array([(c[0] + h[0], c[1] - h[1], z), (c[0] + h[0], c[1] + h[1], z), (c[0] - h[0], c[1] + h[1], z), (c[0] - h[0], c[1] - h[1], z)])
        tris += loft_tris([ring(c[2] - h[2]), ring(c[2] + h[2])])
    return np.array(tris, dtype=float)


# ---------------------------------------------------------------- local preview
def render(tris, view, px_per_cm=4.0, pad=10):
    """Orthographic flat-shaded view. view: 'front' looks at the face, 'back', 'right' (the character's right side)."""
    eye = {"front": (1, 0, 0), "back": (-1, 0, 0), "right": (0, -1, 0)}[view]
    eye = np.array(eye, float)
    up = np.array([0, 0, 1.0])
    right = np.cross(up, eye)          # image +x
    t = tris.reshape(-1, 3)
    sx, sy, sz = t @ right, t @ up, t @ eye
    w = int((sx.max() - sx.min()) * px_per_cm + 2 * pad)
    h = int((HEIGHT + 4) * px_per_cm + 2 * pad)
    X = ((sx - sx.min()) * px_per_cm + pad).reshape(-1, 3)
    Yp = (h - pad - sy * px_per_cm).reshape(-1, 3)
    Zd = sz.reshape(-1, 3)
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    light = np.array([0.55, -0.35, 0.75]) if view != "back" else np.array([-0.55, -0.35, 0.75])
    light = light / np.linalg.norm(light)
    lam = np.abs(n @ light) * 0.55 + 0.45 * (0.5 + 0.5 * n[:, 2]) + 0.12
    img = np.zeros((h, w, 3), np.float32) + np.array([0.56, 0.58, 0.62], np.float32)
    zbuf = np.full((h, w), -1e9, np.float32)
    skin = np.array([0.83, 0.56, 0.36], np.float32)
    for i in range(len(tris)):
        x, y, z = X[i], Yp[i], Zd[i]
        x0, x1 = int(max(np.floor(x.min()), 0)), int(min(np.ceil(x.max()) + 1, w))
        y0, y1 = int(max(np.floor(y.min()), 0)), int(min(np.ceil(y.max()) + 1, h))
        if x1 <= x0 or y1 <= y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        d = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(d) < 1e-9:
            continue
        a = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / d
        b = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / d
        c = 1 - a - b
        zz = a * z[0] + b * z[1] + c * z[2]
        m = (a >= 0) & (b >= 0) & (c >= 0) & (zz > zbuf[y0:y1, x0:x1])
        zbuf[y0:y1, x0:x1][m] = zz[m]
        img[y0:y1, x0:x1][m] = np.clip(skin * lam[i], 0, 1)
    return img, zbuf > -1e8


def sheet(path, ref=None):
    from PIL import Image
    tris = soup()
    cells = [Image.fromarray((render(tris, v)[0] * 255).astype(np.uint8)) for v in ("front", "back", "right")]
    if ref:
        r = Image.open(ref).convert("RGB")
        k = cells[0].height / r.height
        cells.append(r.resize((int(r.width * k), cells[0].height)))
    w = sum(c.width for c in cells) + 10 * (len(cells) - 1)
    out = Image.new("RGB", (w, cells[0].height), (20, 20, 20))
    x = 0
    for c in cells:
        out.paste(c, (x, 0))
        x += c.width + 10
    out.save(path)
    print("saved", path, out.size, "tris", len(tris))


# ---------------------------------------------------------------- weave emit
def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def table(rows, cols, key):
    """A DSL point list (v1, v2, key) so sample_path_axis(..., axis: "z") can interpolate two columns by the key."""
    return "[" + ",".join(f"({f(r[cols[0]])},{f(r[cols[1]])},{f(r[key])})" for r in rows) + "]"


RING = """    var ring = [];
    for j 0..{n} {{
        let c = cos(360 * j / {n});
        let s = sin(360 * j / {n});
        let ex = 2 / {e};
        let du = select(0 - {um}, {up}, c > 0) * pow(abs(c), ex);
        let dv = select(0 - {vm}, {vp}, s > 0) * pow(abs(s), ex);
        ring = append(ring, {pt});
    }}
    {secs} = append({secs}, ring);"""


def weave(path, voxel=1.2, verts=1500, fuse=True, textures=True):
    S = lambda t: f'sample_path_axis({t}, axis: "z", at: k, interpolation: "pchip")'
    L = [f"#mesh {NAME}"]
    if textures:
        L += ["#texture TravelerSkin color=#B9784F roughness=0.8", "#texture TravelerCloth color=#D8D0BC roughness=0.9"]
    L += ["// Generated by oriverse/models/traveler_body.py - edit the tables there, not this block.",
         "// Each limb is a loft of superellipse rings sampled from the tables (two columns per table, keyed by the last value).",
         "budget(verts: 30000, indices: 90000);",
         f"let to_a = {table(TORSO, (1, 2), 0)};", f"let to_b = {table(TORSO, (3, 4), 0)};",
         f"let he_a = {table(HEAD, (1, 2), 0)};", f"let he_b = {table(HEAD, (3, 4), 0)};",
         f"let ar_a = {table(ARM, (1, 2), 0)};", f"let ar_b = {table(ARM, (3, 4), 0)};", f"let ar_c = {table(ARM, (5, 5), 0)};",
         f"let le_a = {table(LEG, (1, 2), 0)};", f"let le_b = {table(LEG, (3, 4), 0)};", f"let le_c = {table(LEG, (5, 6), 0)};", f"let le_d = {table(LEG, (7, 7), 0)};",
         f"let fo_a = {table(FOOT, (1, 2), 0)};"]

    def loop(secs, lo, hi, count, lets, **kw):
        L.append(f"var {secs} = [];")
        L.append(f"for i 0..{count} {{")
        L.append(f"    let k = {f(lo)} + {f(hi - lo)} * i / {count - 1};")
        L.extend("    " + x for x in lets)
        L.append(RING.format(secs=secs, **kw))
        L.append("}")

    loop("to_secs", TORSO[0][0], TORSO[-1][0], 24, [f"let a = {S('to_a')};", f"let b = {S('to_b')};"],
         n=14, e="b.y", up="a.y", um="b.x", vp="a.x", vm="a.x", pt="(du, dv, k)")
    loop("he_secs", HEAD[0][0], HEAD[-1][0], 10, [f"let a = {S('he_a')};", f"let b = {S('he_b')};"],
         n=10, e="b.y", up="a.y", um="b.x", vp="a.x", vm="a.x", pt=f"({f(HEAD_CX)} + du, dv, k)")
    loop("ar_secs", ARM[0][0], ARM[-1][0], 26, [f"let a = {S('ar_a')};", f"let b = {S('ar_b')};", f"let c3 = {S('ar_c')};"],
         n=8, e="c3.x", up="a.x", um="a.y", vp="b.x", vm="b.y", pt=f"(du, {f(SHOULDER[1])} - k, {f(SHOULDER[2])} + dv)")
    loop("le_secs", LEG[0][0], LEG[-1][0], 26, [f"let a = {S('le_a')};", f"let b = {S('le_b')};", f"let c3 = {S('le_c')};", f"let d = {S('le_d')};"],
         n=8, e="d.x", up="c3.x", um="c3.y", vp="b.y", vm="b.x", pt="(a.x + du, a.y + dv, k)")
    L += ["var fo_secs = [];", "for i 0..10 {", f"    let k = {f(FOOT[0][0])} + {f(FOOT[-1][0] - FOOT[0][0])} * i / 9;", f"    let a = {S('fo_a')};",
          f"    let y = {f(FOOT_CY)};",
          "    fo_secs = append(fo_secs, [(k, y - a.x, 0.3), (k, y - a.x * 0.6, 0), (k, y + a.x * 0.6, 0), (k, y + a.x, 0.3), (k, y + a.x, a.y * 0.6), (k, y + a.x * 0.55, a.y), (k, y - a.x * 0.55, a.y), (k, y - a.x, a.y * 0.6)]);",
          "}"]
    M = 'material: "TravelerSkin"'
    L.append(f'let torso = loft_quads(sections: to_secs, caps: "both", {M});')
    L.append(f'let head = loft_quads(sections: he_secs, caps: "both", {M});')
    L.append(f'let arm_r = loft_quads(sections: ar_secs, caps: "both", {M});')
    L.append(f'let leg_r = loft_quads(sections: le_secs, caps: "both", {M});')
    L.append(f'let foot_r = loft_quads(sections: fo_secs, caps: "both", {M});')
    names = ["torso", "head"]
    for i, (kind, c, r) in enumerate(LUMPS):
        at = f"at: ({f(c[0])}, {f(c[1])}, {f(c[2])})"
        if kind == "ell":
            L.append(f'let lump{i} = center(scale(icosphere(radius: 10, subdivisions: 2, {M}), ({r[0] / 10:.2f}, {r[1] / 10:.2f}, {r[2] / 10:.2f})), {at});')
        else:
            L.append(f'let lump{i} = center(quad_box(size: ({f(r[0])}, {f(r[1])}, {f(r[2])}), res: (2, 3, 3), {M}), {at});')
    (a, b, t) = THUMB
    a, b = np.array(a), np.array(b)
    mid, ln, yaw = (a + b) / 2, np.linalg.norm(b - a), np.degrees(np.arctan2(b[1] - a[1], b[0] - a[0]))
    L.append(f'let thumb = center(rotate_z(quad_box(size: ({f(ln)}, {f(t)}, {f(t * 0.8)}), res: (2, 2, 2), {M}), degrees: {f(yaw)}), at: ({f(mid[0])}, {f(mid[1])}, {f(mid[2])}));')
    c, sz = EAR
    L.append(f'let ear = center(quad_box(size: ({f(sz[0])}, {f(sz[1])}, {f(sz[2])}), res: (2, 2, 2), {M}), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
    for i, (sz, c) in enumerate(FACE):
        L.append(f'let face{i} = center(quad_box(size: ({f(sz[0])}, {f(sz[1])}, {f(sz[2])}), res: (2, 2, 2), {M}), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
        names.append(f"face{i}")
    side = ["arm_r", "leg_r", "foot_r", "thumb", "ear"] + [f"lump{i}" for i in range(len(LUMPS))]
    L.append(f"let right = merge({', '.join(side)});")
    L.append(f"let raw = merge({', '.join(names)}, right, mirror(right, normal: (0, 1, 0)));")
    if fuse:
        L.append(f'let fused = voxel_remesh(raw, voxel: {voxel}, mode: "smooth");')
        L.append(f"let low = decimate(fused, verts: {verts});")
        G = f(GAP)
        C = 'material: "TravelerCloth"'
        for g in GARMENTS:
            p, parts, side = g["p"], [], []
            if g["torso"]:
                loop(f"{g['secs']}t_secs", g["torso"][0], g["torso"][1], 7, [f"let a = {S('to_a')};", f"let b = {S('to_b')};"],
                     n=14, e="b.y", up=f"(a.y + {G})", um=f"(b.x + {G})", vp=f"(a.x + {G})", vm=f"(a.x + {G})", pt="(du, dv, k)")
            if g["leg"]:
                loop(f"{g['secs']}l_secs", g["leg"][0], g["leg"][1], 7, [f"let a = {S('le_a')};", f"let b = {S('le_b')};", f"let c3 = {S('le_c')};", f"let d = {S('le_d')};"],
                     n=8, e="d.x", up=f"(c3.x + {G})", um=f"(c3.y + {G})", vp=f"(b.y + {G} + 1.2)", vm=f"(b.x + {G})", pt="(a.x + du, a.y + dv, k)")
            if g["torso"]:
                L.append(f'let {p}_{g["band"]} = loft_quads(sections: {g["secs"]}t_secs, caps: "both", {C});')
                parts.append(f'{p}_{g["band"]}')
            if g["leg"]:
                L.append(f'let {p}_leg = loft_quads(sections: {g["secs"]}l_secs, caps: "both", {C});')
                side.append(f"{p}_leg")
            for i in g["lumps"]:
                kind, c, r = LUMPS[i]
                L.append(f'let {p}_lump{i} = center(scale(icosphere(radius: 10, subdivisions: 2, {C}), ({(r[0] + GAP) / 10:.2f}, {(r[1] + GAP) / 10:.2f}, {(r[2] + GAP) / 10:.2f})), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
                side.append(f"{p}_lump{i}")
            L.append(f"let {p}_right = merge({', '.join(side)});" if len(side) > 1 else f"let {p}_right = {side[0]};")
            if g["gusset"]:
                # gusset: closes the gap under the torso between the two leg tubes
                c, r = g["gusset"]
                L.append(f'let {p}_gusset = center(scale(icosphere(radius: 10, subdivisions: 2, {C}), ({r[0] / 10:.2f}, {r[1] / 10:.2f}, {r[2] / 10:.2f})), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
                parts.append(f"{p}_gusset")
            parts += [f"{p}_right", f"mirror({p}_right, normal: (0, 1, 0))"]
            L.append(f'let {g["name"]} = decimate(voxel_remesh(merge({", ".join(parts)}), voxel: {voxel}, mode: "smooth"), verts: {g["verts"]});')
        L.append("let body = flat_shade(low);")
        for g in GARMENTS:
            L.append(f'let {g["name"]}_flat = flat_shade({g["name"]});')
    else:
        L.append("let body = flat_shade(raw);")
    for n, p, par in BONES:
        L.append(f'bone("{n}", pos: ({f(p[0])}, {f(p[1])}, {f(p[2])})' + (f', parent: "{par}"' if par else "") + ");")
    for n, p, ax, bn in SOCKETS:
        L.append(f'socket("{n}", at: ({f(p[0])}, {f(p[1])}, {f(p[2])}), axis: ({f(ax[0])}, {f(ax[1])}, {f(ax[2])}), bone: "{bn}");')
    # Skin: everything starts on Root; each bone then claims the box beyond its joint, blended over `soft` cm
    # back toward its parent. Parents come before children; a limb pins the other side so legs never share weights.
    B = 400
    sh_y, el_y, wr_y = -SHOULDER[1], -SHOULDER[1] + ELBOW_D, -SHOULDER[1] + WRIST_D
    K = SKIN
    regions = [("Spine", (-B, -B, K["spine"]), (B, B, B), 8, None), ("Torso", (-B, -B, K["torso"]), (B, B, B), 8, None),
               ("Neck", (-B, -K["neck_w"], K["neck"]), (B, K["neck_w"], B), 4, None), ("Head", (-B, -B, K["head"]), (B, B, B), 4, None)]
    for side, sg in (("R", -1), ("L", 1)):
        y0, y1 = (-B, -0.1) if sg < 0 else (0.1, B)
        other = ((-B, 0.1, -B), (B, B, B)) if sg < 0 else ((-B, -B, -B), (B, -0.1, B))
        yy = lambda d: (-B, -d) if sg < 0 else (d, B)
        regions += [(f"UpperArm{side}", (-B, yy(sh_y + 3)[0], K["arm_z"]), (B, yy(sh_y + 3)[1], B), 7, None),
                    (f"Forearm{side}", (-B, yy(el_y + 2)[0], K["arm_z"]), (B, yy(el_y + 2)[1], B), 4, None),
                    (f"Hand{side}", (-B, yy(wr_y + 1.5)[0], K["arm_z"]), (B, yy(wr_y + 1.5)[1], B), 3, None),
                    (f"Thigh{side}", (-B, y0, -B), (B, y1, K["thigh"]), 6, other),
                    (f"Shin{side}", (-B, y0, -B), (B, y1, K["shin"]), 5, other),
                    (f"Foot{side}", (-B, y0, -B), (B, y1, K["foot"]), 3, other),
                    (f"Toe{side}", (K["toe_x"], y0, -B), (B, y1, K["foot"]), 3, other)]
    L.append(f'let rooted = skin_weights(body, selection: select_verts(body, min: (-{B}, -{B}, -{B}), max: ({B}, {B}, {B})), bones: "Root", weights: [1]);')
    prev = "rooted"
    for i, (bone, lo, hi, soft, pin) in enumerate(regions):
        v = lambda t: f"({f(t[0])}, {f(t[1])}, {f(t[2])})"
        pins = f", pins: select_verts({prev}, min: {v(pin[0])}, max: {v(pin[1])})" if pin else ""
        L.append(f'let w{i} = soft_selection({prev}, selection: select_verts({prev}, min: {v(lo)}, max: {v(hi)}), radius: {soft}, falloff: "smooth", distance: "surface"{pins});')
        L.append(f'let s{i} = skin_weights({prev}, selection: w{i}, bones: "{bone}", weights: [1]);')
        prev = f"s{i}"
    if fuse:
        # garments copy the body's weights from the nearest skin, so they bend exactly like what they cover
        flats = [f'{g["name"]}_flat' for g in GARMENTS]
        if len(flats) > 1:
            L.append(f"let dressed = merge({', '.join(flats)});")
        src = flats[0] if len(flats) == 1 else "dressed"
        L.append(f'let worn = transfer_weights({src}, source: {prev}, selection: select_verts({src}, min: (-{B}, -{B}, -{B}), max: ({B}, {B}, {B})), max_distance: {REACH});')
        L.append(f"out.geo = merge({prev}, worn);")
    else:
        L.append(f"out.geo = {prev};")
    L.append("#end")
    open(path, "w").write("\n".join(L) + "\n")
    print("saved", path, sum(len(x) for x in L), "chars")


if __name__ == "__main__":
    args = [a for a in sys.argv[3:] if not a.startswith("--")]
    select(args[0] if args else "male")
    if sys.argv[1] == "render":
        sheet(sys.argv[2])
    else:
        weave(sys.argv[2], textures="--no-textures" not in sys.argv)
