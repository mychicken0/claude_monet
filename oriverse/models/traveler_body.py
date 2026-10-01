# Traveler base bodies (male, female): anatomy tables -> closed ring lofts + ellipsoid masses.
# One source for two outputs:
#   python3 traveler_body.py render <out.png> [male|female]                  local flat-shaded front/back/side sheet
#   python3 traveler_body.py weave  <out.weave> [male|female] [--no-textures]  one self-contained base-body #mesh
#   python3 traveler_body.py wardrobe <out.weave>                            shared tables, garment parts, outfit meshes, hat + pack
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
# hair shell rings: z, centre x, half width, front, back
HAIR = [
    (161.0, -4.0, 5.6, 1.5, 4.6),
    (164.0, -3.0, 8.3, 2.5, 7.4),
    (168.0, -2.0, 9.3, 3.0, 9.4),
    (172.0, -1.0, 9.5, 4.5, 10.2),
    (174.5, -0.3, 9.4, 6.5, 10.4),   # hairline: the front swings forward over the crown
    (176.5, 0.5, 8.8, 10.6, 10.4),
    (179.0, 0.5, 6.6, 8.2, 8.4),
    (181.3, 0.5, 3.6, 4.4, 4.6),
    (182.4, 0.5, 1.0, 1.2, 1.2),
]
HAIR_RINGS = 12
SKIRT = None
# wardrobe landmarks: garment z ranges on this body (see pieces() for what is built from them)
WEAR = dict(P="TravelerM", t="tm", crotch=86.5, waist=103.0, gusset=((-0.5, 0, 85), (7.8, 6.8, 3.4)),
            trunks_hem=81.0, knee_hem=43.0, ankle_hem=9.0, boot_top=31.0, shirt_hem=97.0, neck=152.0,
            sleeve_long=51.0, sleeve_short=22.0, vest=(100.0, 149.0), chest_lump=None, shoe_top=13.0)
# how far a garment vertex may look for skin to copy weights from (cap vertices sit deep inside the torso)
REACH = 8
# where each bone's skin region starts (z unless noted): see the region list in weave()
SKIN = dict(spine=101, torso=114, neck=152, neck_w=12, head=158, arm_z=120, thigh=86, shin=48, foot=9, toe_x=12)
# wearable mount points (bone-pinned): name, position, axis, bone. Rigid pieces attach with AttachToAnchor(body, name).
SOCKETS = [
    ("Hat", (1, 0, 178), (0, 0, 1), "Head"), ("Face", (11, 0, 169), (1, 0, 0), "Head"),
    ("Chest", (12.5, 0, 134), (1, 0, 0), "Torso"), ("Back", (-21, 0, 128), (0, 0, 1), "Torso"),
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
    HAIR=[
        (128.0, -11.5, 3.2, 1.6, 2.6),   # a low ponytail down the back
        (133.0, -11.5, 4.6, 2.2, 3.2),
        (138.0, -9.8, 5.6, 2.4, 3.8),
        (143.0, -7.0, 6.4, 2.6, 4.6),
        (147.5, -4.2, 7.6, 3.0, 6.0),
        (151.0, -2.6, 8.5, 3.0, 8.0),
        (155.5, -1.6, 9.0, 3.2, 9.4),
        (159.5, -0.8, 9.1, 4.6, 10.0),
        (162.2, -0.2, 9.0, 6.6, 10.2),   # hairline
        (164.2, 0.5, 8.5, 10.0, 10.0),
        (166.6, 0.5, 6.4, 7.6, 8.2),
        (168.8, 0.5, 3.4, 4.2, 4.4),
        (169.8, 0.5, 1.0, 1.2, 1.2),
    ],
    HAIR_RINGS=18,
    # knee-length skirt rings: z, half width, front, back (worn outside the blouse, under the bodice)
    SKIRT=[
        # z, half width, front, back - kept 2 cm outside the shirt at the hips, so a tucked shirt never shows through
        (55.0, 23.0, 14.5, 15.5),
        (64.0, 22.6, 14.3, 15.6),
        (74.0, 22.2, 14.1, 15.8),
        (84.0, 22.0, 14.0, 16.0),
        (90.0, 21.6, 14.0, 15.9),
        (96.0, 20.6, 13.8, 15.2),
        (101.0, 18.4, 13.2, 13.8),
        (104.0, 17.0, 12.6, 12.8),
    ],
    WEAR=dict(P="TravelerF", t="tf", crotch=80.5, waist=96.0, gusset=((-0.5, 0, 79), (7.8, 6.8, 3.4)),
              trunks_hem=75.5, knee_hem=40.0, ankle_hem=9.0, boot_top=29.0, shirt_hem=92.0, neck=141.0,
              sleeve_long=47.0, sleeve_short=20.0, vest=(103.0, 137.0), chest_lump=1, shoe_top=12.5),
    SKIN=dict(spine=94, torso=106, neck=141.5, neck_w=11, head=147, arm_z=110, thigh=80, shin=44.5, foot=9, toe_x=11),
    SOCKETS=[
        ("Hat", (1, 0, 165.6), (0, 0, 1), "Head"), ("Face", (10.5, 0, 157), (1, 0, 0), "Head"),
        ("Chest", (13.5, 0, 124), (1, 0, 0), "Torso"), ("Back", (-20, 0, 119), (0, 0, 1), "Torso"),
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


MALE = {k: globals()[k] for k in FEMALE}


def select(variant):
    """Swap the module tables to a variant ("male" is the module default)."""
    if variant not in ("male", "female"):
        raise SystemExit(f"unknown variant {variant}")
    globals().update(FEMALE if variant == "female" else MALE)


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


B = 400   # selection boxes reach this far (cm)


def rig(L, body="body", sockets=True, skin=True):
    """Append bones, sockets and the region skinning of `body`; returns the name of the fully skinned geometry.
    Every rigged mesh gets a "Fit" socket at the authored origin: wearable pieces snap onto the body with
    piece.AttachToAnchor(body, "Fit", "Fit"), whatever their own bounds are."""
    for n, p, par in BONES:
        L.append(f'bone("{n}", pos: ({f(p[0])}, {f(p[1])}, {f(p[2])})' + (f', parent: "{par}"' if par else "") + ");")
    for n, p, ax, bn in (SOCKETS if sockets else []):
        L.append(f'socket("{n}", at: ({f(p[0])}, {f(p[1])}, {f(p[2])}), axis: ({f(ax[0])}, {f(ax[1])}, {f(ax[2])}), bone: "{bn}");')
    L.append('socket("Fit", at: (0, 0, 0), axis: (0, 0, 1));')
    if not skin:
        return body
    # Skin: everything starts on Root; each bone then claims the box beyond its joint, blended over `soft` cm
    # back toward its parent. Parents come before children; a limb pins the other side so legs never share weights.
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
    L.append(f'let rooted = skin_weights({body}, selection: select_verts({body}, min: (-{B}, -{B}, -{B}), max: ({B}, {B}, {B})), bones: "Root", weights: [1]);')
    prev = "rooted"
    for i, (bone, lo, hi, soft, pin) in enumerate(regions):
        v = lambda t: f"({f(t[0])}, {f(t[1])}, {f(t[2])})"
        pins = f", pins: select_verts({prev}, min: {v(pin[0])}, max: {v(pin[1])})" if pin else ""
        L.append(f'let w{i} = soft_selection({prev}, selection: select_verts({prev}, min: {v(lo)}, max: {v(hi)}), radius: {soft}, falloff: "smooth", distance: "surface"{pins});')
        L.append(f'let s{i} = skin_weights({prev}, selection: w{i}, bones: "{bone}", weights: [1]);')
        prev = f"s{i}"
    return prev


def weave(path, voxel=1.2, verts=1500, fuse=True, textures=True, dressed=False):
    S = lambda t: f'sample_path_axis({t}, axis: "z", at: k, interpolation: "pchip")'
    L = [f"#mesh {NAME}"]
    if textures:
        L += ["#texture TravelerSkin color=#B9784F roughness=0.8", "#texture TravelerCloth color=#D8D0BC roughness=0.9"]
    L += ["// Generated by oriverse/models/traveler_body.py - edit the tables there, not this block.",
         "// Each limb is a loft of superellipse rings sampled from the tables (two columns per table, keyed by the last value).",
         "budget(verts: 30000, indices: 90000);",
         # the player object is a 40 x 40 x 180 box and SetModel fits a model's reference box into it by height:
         # without this the 168 cm woman is drawn 7% too big and pokes through every piece she wears
         "sim_box(min: (-20, -20, 0), max: (20, 20, 180));",
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
        # underwear is a wardrobe piece of its own (hidden under trousers, or the two would share one surface);
        # dressed=True fuses it into the body instead, for a stand-alone figure
        worn = GARMENTS if dressed else []
        for g in worn:
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
        for g in worn:
            L.append(f'let {g["name"]}_flat = flat_shade({g["name"]});')
    else:
        L.append("let body = flat_shade(raw);")
    prev = rig(L)
    if fuse and dressed:
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


# ---------------------------------------------------------------- wardrobe emit
# Every wearable is its own rigged mesh: the garment geometry alone, on the same 21 bones as the body. In the world
# each worn piece is an object attached to the player ("Fit" socket) that is told to play the same clip in the same
# tick, so it moves exactly like the skin under it; SetColor tints it, so one white mesh serves every colour.
# Geometry lives in #meshpart blocks that read the shared tables from #meshdefs; bones and skin weights are
# mesh-level statements, so each piece #mesh repeats the rig.
TEXTURES = [("TravWear", "#F4F1EA"), ("TravStraw", "#D9BE7C"), ("TravIndigo", "#3F4C78"), ("TravTan", "#8C6240"),
            ("TravLeather", "#3E2C22"), ("TravCream", "#D8CDB2")]
LAYER = dict(pants=1.5, shirt=2.3, boot=2.4, sole=1.6, vest=3.4)   # cm off the skin; a larger layer is worn outside
BUST = 0.6     # extra room over the bust: a low-poly dome cuts inside the rounder one under it


def defs(t):
    """Shared table lets for the current variant, prefixed so no mesh local can shadow them."""
    T = [(f"{t}_to_a", TORSO, (1, 2)), (f"{t}_to_b", TORSO, (3, 4)), (f"{t}_he_a", HEAD, (1, 2)), (f"{t}_he_b", HEAD, (3, 4)),
         (f"{t}_ar_a", ARM, (1, 2)), (f"{t}_ar_b", ARM, (3, 4)), (f"{t}_ar_c", ARM, (5, 5)),
         (f"{t}_le_a", LEG, (1, 2)), (f"{t}_le_b", LEG, (3, 4)), (f"{t}_le_c", LEG, (5, 6)), (f"{t}_le_d", LEG, (7, 7)),
         (f"{t}_fo_a", FOOT, (1, 2)), (f"{t}_ha_a", HAIR, (1, 2)), (f"{t}_ha_b", HAIR, (3, 4))]
    if SKIRT:
        T += [(f"{t}_sk_a", SKIRT, (1, 2)), (f"{t}_sk_b", SKIRT, (3, 3))]
    return [f"let {n} = {table(rows, cols, 0)};" for n, rows, cols in T]


def parts():
    """#meshpart blocks for the current variant."""
    P, t, W = WEAR["P"], WEAR["t"], WEAR
    S = lambda n: f'sample_path_axis({t}_{n}, axis: "z", at: k, interpolation: "pchip")'
    L = []

    def ring(n, e, up, um, vp, vm, pt, secs="secs", ind="    "):
        return [ind + x for x in RING.format(secs=secs, n=n, e=e, up=up, um=um, vp=vp, vm=vm, pt=pt).split("\n")]

    def tube(name, params, k, lets, **kw):
        """A loft through `n` rings between two table stations, grown by `gap`."""
        L.append(f"#meshpart {P}{name}")
        L.extend(f"param {a} = {b};" for a, b in params)
        L.extend(["var secs = [];", "for i 0..n {", f"    let k = {k};"] + ["    " + x for x in lets])
        L.extend([x[4:] if False else x for x in RING.format(secs="secs", **kw).split("\n")])
        L.extend(["}", 'out.geo = loft_quads(sections: secs, caps: "both", material: mat);', "#end"])

    # ---- the skin: every limb lofted, fused into one surface, decimated, flat shaded
    M = 'material: "TravelerSkin"'
    L.append(f"#meshpart {P}Skin")

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
    for nm, secs in (("torso", "to_secs"), ("head", "he_secs"), ("arm_r", "ar_secs"), ("leg_r", "le_secs"), ("foot_r", "fo_secs")):
        L.append(f'let {nm} = loft_quads(sections: {secs}, caps: "both", {M});')
    names = ["torso", "head"]
    for i, (kind, c, r) in enumerate(LUMPS):
        L.append(f'let lump{i} = center(scale(icosphere(radius: 10, subdivisions: 2, {M}), ({r[0] / 10:.2f}, {r[1] / 10:.2f}, {r[2] / 10:.2f})), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
    (a, b, th) = THUMB
    a, b = np.array(a), np.array(b)
    mid, ln, yaw = (a + b) / 2, np.linalg.norm(b - a), np.degrees(np.arctan2(b[1] - a[1], b[0] - a[0]))
    L.append(f'let thumb = center(rotate_z(quad_box(size: ({f(ln)}, {f(th)}, {f(th * 0.8)}), res: (2, 2, 2), {M}), degrees: {f(yaw)}), at: ({f(mid[0])}, {f(mid[1])}, {f(mid[2])}));')
    c, sz = EAR
    L.append(f'let ear = center(quad_box(size: ({f(sz[0])}, {f(sz[1])}, {f(sz[2])}), res: (2, 2, 2), {M}), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
    for i, (sz, c) in enumerate(FACE):
        L.append(f'let face{i} = center(quad_box(size: ({f(sz[0])}, {f(sz[1])}, {f(sz[2])}), res: (2, 2, 2), {M}), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));')
        names.append(f"face{i}")
    side = ["arm_r", "leg_r", "foot_r", "thumb", "ear"] + [f"lump{i}" for i in range(len(LUMPS))]
    L.append(f"let right = merge({', '.join(side)});")
    L.append(f"let raw = merge({', '.join(names)}, right, mirror(right, normal: (0, 1, 0)));")
    L.append('out.geo = flat_shade(decimate(voxel_remesh(raw, voxel: 1.2, mode: "smooth"), verts: 1500));')
    L.append("#end")

    # ---- building blocks: one tube per limb, grown by `gap`
    C = [("mat", '"TravWear"')]
    tube("Torso", [("z0", f(W["crotch"])), ("z1", f(W["waist"])), ("gap", "1.5"), ("n", "7")] + C, "z0 + (z1 - z0) * i / (n - 1)",
         [f"let a = {S('to_a')};", f"let b = {S('to_b')};"],
         n=14, e="b.y", up="(a.y + gap)", um="(b.x + gap)", vp="(a.x + gap)", vm="(a.x + gap)", pt="(du, dv, k)")
    tube("Leg", [("z0", f(W["trunks_hem"])), ("z1", f(LEG[-1][0])), ("gap", "1.5"), ("inner", "1.2"), ("n", "7")] + C, "z0 + (z1 - z0) * i / (n - 1)",
         [f"let a = {S('le_a')};", f"let b = {S('le_b')};", f"let c3 = {S('le_c')};", f"let d = {S('le_d')};"],
         n=8, e="d.x", up="(c3.x + gap)", um="(c3.y + gap)", vp="(b.y + gap + inner)", vm="(b.x + gap)", pt="(a.x + du, a.y + dv, k)")
    tube("Arm", [("d0", "-5"), ("d1", f(W["sleeve_long"])), ("gap", "2.3"), ("n", "12")] + C, "d0 + (d1 - d0) * i / (n - 1)",
         [f"let a = {S('ar_a')};", f"let b = {S('ar_b')};", f"let c3 = {S('ar_c')};"],
         n=8, e="c3.x", up="(a.x + gap)", um="(a.y + gap)", vp="(b.x + gap)", vm="(b.y + gap)", pt=f"(du, {f(SHOULDER[1])} - k, {f(SHOULDER[2])} + dv)")
    x0, x1 = FOOT[0][0], FOOT[-1][0]
    L += [f"#meshpart {P}Foot", "param gap = 1.6;", 'param mat = "TravWear";', "var secs = [];", "for i 0..10 {",
          f"    let k = {f(x0)} + {f(x1 - x0)} * i / 9;", f"    let a = {S('fo_a')};",
          f"    let x = {f((x0 + x1) / 2)} + (k - {f((x0 + x1) / 2)}) * (1 + 2 * gap / {f(x1 - x0)});",
          f"    let y = {f(FOOT_CY)};", "    let w = a.x + gap;", "    let h = a.y + gap;",
          "    secs = append(secs, [(x, y - w, 0.3), (x, y - w * 0.6, 0), (x, y + w * 0.6, 0), (x, y + w, 0.3), (x, y + w, h * 0.6), (x, y + w * 0.55, h), (x, y - w * 0.55, h), (x, y - w, h * 0.6)]);",
          "}", 'out.geo = loft_quads(sections: secs, caps: "both", material: mat);', "#end"]
    for i, (kind, c, r) in enumerate(LUMPS):
        L += [f"#meshpart {P}Lump{i}", "param gap = 1.5;", 'param mat = "TravWear";',
              f"out.geo = center(scale(icosphere(radius: 10, subdivisions: 2, material: mat), (({f(r[0])} + gap) / 10, ({f(r[1])} + gap) / 10, ({f(r[2])} + gap) / 10)), at: ({f(c[0])}, {f(c[1])}, {f(c[2])}));",
              "#end"]

    FUSE = lambda src, verts: f'flat_shade(decimate(voxel_remesh({src}, voxel: 1.2, mode: "smooth"), verts: {verts}))'
    MIR = lambda v: f"mirror({v}, normal: (0, 1, 0))"
    gc, gr = W["gusset"]
    lump = W["chest_lump"]

    # ---- garments
    L += [f"#meshpart {P}Hair", 'param mat = "TravWear";', "var secs = [];", f"for i 0..{HAIR_RINGS} {{",
          f"    let k = {f(HAIR[0][0])} + {f(HAIR[-1][0] - HAIR[0][0])} * i / {HAIR_RINGS - 1};",
          f"    let a = {S('ha_a')};", f"    let b = {S('ha_b')};"]
    L += RING.format(secs="secs", n=10, e="2.3", up="b.x", um="b.y", vp="a.y", vm="a.y", pt="(a.x + du, dv, k)").split("\n")
    L += ["}", 'out.geo = flat_shade(loft_quads(sections: secs, caps: "both", material: mat));', "#end"]

    # trousers: hip tube + leg tube + seat + gusset. hem picks the length (trunks, knee breeches, ankle).
    L += [f"#meshpart {P}Trousers", 'param mat = "TravWear";', f"param hem = {f(W['ankle_hem'])};", "param n = 14;", "param verts = 520;",
          f"let hips = part({P}Torso, z0: {f(W['crotch'])}, z1: {f(W['waist'])}, gap: {LAYER['pants']}, mat: mat);",
          f"let side = merge(part({P}Leg, z0: hem, z1: {f(LEG[-1][0])}, gap: {LAYER['pants']}, n: n, mat: mat), part({P}Lump0, gap: {LAYER['pants']}, mat: mat));",
          f"let gusset = center(scale(icosphere(radius: 10, subdivisions: 2, material: mat), ({gr[0] / 10:.2f}, {gr[1] / 10:.2f}, {gr[2] / 10:.2f})), at: ({f(gc[0])}, {f(gc[1])}, {f(gc[2])}));",
          f"out.geo = {FUSE(f'merge(hips, gusset, side, {MIR(chr(115) + chr(105) + chr(100) + chr(101))})', 'verts')};", "#end"]
    # shirt: torso tube to the collar + sleeves (sleeve = how far down the arm)
    chest = f", part({P}Lump{lump}, gap: {f(LAYER['shirt'] + BUST)}, mat: mat)" if lump is not None else ""
    L += [f"#meshpart {P}Shirt", 'param mat = "TravWear";', f"param sleeve = {f(W['sleeve_long'])};",
          f"let trunk = part({P}Torso, z0: {f(W['shirt_hem'])}, z1: {f(W['neck'])}, gap: {LAYER['shirt']}, n: 12, mat: mat);",
          f"let side = merge(part({P}Arm, d1: sleeve, gap: {LAYER['shirt']}, mat: mat){chest});" if lump is not None else
          f"let side = part({P}Arm, d1: sleeve, gap: {LAYER['shirt']}, mat: mat);",
          f"out.geo = {FUSE(f'merge(trunk, side, {MIR(chr(115) + chr(105) + chr(100) + chr(101))})', 640 if lump is None else 760)};", "#end"]
    # vest / bodice: a sleeveless tube worn over the shirt
    v0, v1 = W["vest"]
    vest_src = f"part({P}Torso, z0: {f(v0)}, z1: {f(v1)}, gap: {LAYER['vest']}, n: 10, mat: mat)"
    if lump is not None:
        L += [f"#meshpart {P}Vest", 'param mat = "TravWear";', f"let bust = part({P}Lump{lump}, gap: {f(LAYER['vest'] + BUST)}, mat: mat);",
              f"out.geo = {FUSE(f'merge({vest_src}, bust, {MIR(chr(98) + chr(117) + chr(115) + chr(116))})', 380)};", "#end"]
    else:
        L += [f"#meshpart {P}Vest", 'param mat = "TravWear";', f"out.geo = {FUSE(vest_src, 360)};", "#end"]
    # boots: sole + shaft over the trouser hem, one side fused then mirrored (top = shaft height: boots or low shoes)
    L += [f"#meshpart {P}Boots", 'param mat = "TravWear";', f"param top = {f(W['boot_top'])};", "param n = 6;", "param verts = 170;",
          f"let boot = decimate(voxel_remesh(merge(part({P}Foot, gap: {LAYER['sole']}, mat: mat), part({P}Leg, z0: {f(LEG[0][0])}, z1: top, gap: {LAYER['boot']}, inner: 0, n: n, mat: mat)), voxel: 1.2, mode: \"smooth\"), verts: verts);",
          f"out.geo = flat_shade(merge(boot, {MIR('boot')}));", "#end"]
    for g in GARMENTS:
        if g["leg"] is None:
            # underwear band (her bandeau): a short torso tube + the bust, at the underwear gap
            i = g["lumps"][0]
            L += [f"#meshpart {P}Band", 'param mat = "TravelerCloth";', f"let bust = part({P}Lump{i}, gap: {f(GAP)}, mat: mat);",
                  f"out.geo = {FUSE(f'merge(part({P}Torso, z0: {f(g['torso'][0])}, z1: {f(g['torso'][1])}, gap: {f(GAP)}, n: 7, mat: mat), bust, {MIR(chr(98) + chr(117) + chr(115) + chr(116))})', g['verts'])};", "#end"]
    if SKIRT:
        # 15 rings (3.5 cm apart) so the waist can follow the body's own weights; squarer than the hips it has to clear
        L += [f"#meshpart {P}SkirtPart", 'param mat = "TravWear";', "var secs = [];", "for i 0..15 {",
              f"    let k = {f(SKIRT[0][0])} + {f(SKIRT[-1][0] - SKIRT[0][0])} * i / 14;",
              f"    let a = {S('sk_a')};", f"    let b = {S('sk_b')};"]
        L += RING.format(secs="secs", n=16, e="2.6", up="a.y", um="b.x", vp="a.x", vm="a.x", pt="(du, dv, k)").split("\n")
        L += ["}", 'out.geo = flat_shade(loft_quads(sections: secs, caps: "both", material: mat));', "#end"]
    return L


def pieces():
    """Wearable pieces of the current variant: (mesh name, garment expression, how it is skinned).
    copy = weights copied from the skin under it, head = rigid on the head, own = its own regions (skirt)."""
    P, W, S, M = WEAR["P"], WEAR, "Trav" + WEAR["P"][-1], 'mat: "TravWear"'
    out = [("Hair", f"part({P}Hair, {M})", "head"),
           ("Shirt", f"part({P}Shirt, {M})", "copy"),
           ("Tee", f"part({P}Shirt, {M}, sleeve: {f(W['sleeve_short'])})", "copy"),
           ("Vest", f"part({P}Vest, {M})", "copy"),
           ("Trousers", f"part({P}Trousers, {M})", "copy"),
           ("Breeches", f"part({P}Trousers, {M}, hem: {f(W['knee_hem'])}, n: 9, verts: 460)", "copy"),
           ("Boots", f"part({P}Boots, {M})", "copy"),
           ("Shoes", f"part({P}Boots, {M}, top: {f(W['shoe_top'])}, n: 4, verts: 120)", "copy")]
    if SKIRT:
        out.append(("Skirt", f"part({P}SkirtPart, {M})", "own"))
    # underwear: the trouser part cut at the trunk hem; worn whenever nothing covers it (see ShowWorn in the world)
    out.append(("Under", f'part({P}Trousers, mat: "TravelerCloth", hem: {f(W["trunks_hem"])}, n: 7, verts: 420)', "copy"))
    if any(g["leg"] is None for g in GARMENTS):
        out.append(("Band", f'part({P}Band, mat: "TravelerCloth")', "copy"))
    return [(S + n, e, k) for n, e, k in out]


def piece(name, expr, skin, textures=()):
    ALL = f"min: (-{B}, -{B}, -{B}), max: ({B}, {B}, {B})"
    L = [f"#mesh {name}"] + [f"#texture {n} color={c} roughness=0.9" for n, c in textures]
    L += ["// Wearable piece: garment only, rigged like the body so it plays the same clips; tinted per object with SetColor.",
          "budget(verts: 60000, indices: 240000);",
          # one reference box for every piece: a slot object can swap its model (SetModel) without being rescaled
          "sim_box(min: (-45, -100, 0), max: (45, 100, 190));"]
    if skin == "copy":
        L += [f"let body = part({WEAR['P']}Skin);", f"let wear = {expr};"]
        prev = rig(L, sockets=False)
        L.append(f"out.geo = transfer_weights(wear, source: {prev}, selection: select_verts(wear, {ALL}), max_distance: 20);")
    elif skin == "head":
        L.append(f"let wear = {expr};")
        rig(L, sockets=False, skin=False)
        L.append(f'out.geo = skin_weights(wear, selection: select_verts(wear, {ALL}), bones: "Head", weights: [1]);')
    else:
        # loose cloth: above the hips it copies the body (so it moves exactly like a shirt tucked into it);
        # below, nothing sits under it - the cloth hangs from Root and each side mostly follows its thigh
        K, SOFT = SKIN, 'falloff: "smooth", distance: "surface"'
        L += [f"let body = part({WEAR['P']}Skin);", f"let wear = {expr};"]
        prev = rig(L, sockets=False)
        L += [f"let worn = transfer_weights(wear, source: {prev}, selection: select_verts(wear, {ALL}), max_distance: 20);",
              f'let k0 = skin_weights(worn, selection: select_verts(worn, min: (-{B}, -{B}, -{B}), max: ({B}, {B}, {f(K["thigh"] + 1)})), bones: "Root", weights: [1]);',
              f'let v1 = soft_selection(k0, selection: select_verts(k0, min: (-{B}, -{B}, -{B}), max: ({B}, -0.1, {f(K["thigh"])})), radius: 6, {SOFT}, pins: select_verts(k0, min: (-{B}, 0.1, -{B}), max: ({B}, {B}, {B})));',
              'let k1 = skin_weights(k0, selection: v1, bones: "ThighR Root", weights: [0.8, 0.2]);',
              f'let v2 = soft_selection(k1, selection: select_verts(k1, min: (-{B}, 0.1, -{B}), max: ({B}, {B}, {f(K["thigh"])})), radius: 6, {SOFT}, pins: select_verts(k1, min: (-{B}, -{B}, -{B}), max: ({B}, -0.1, {B})));',
              'let k2 = skin_weights(k1, selection: v2, bones: "ThighL Root", weights: [0.8, 0.2]);',
              "out.geo = k2;"]
    return L + ["#end"]


ACCESSORIES = """#mesh TravelerStrawHat
// A straw hat for the Hat socket (centre-to-centre: the brim sits 5 cm under the socket).
var brim = [];
for i 0..2 {
    var ring = [];
    for j 0..14 { ring = append(ring, (cos(360 * j / 14) * 21, sin(360 * j / 14) * 19.5, i * 0.9)); }
    brim = append(brim, ring);
}
var crown = [];
for p in [(11, 9.8, 0.9), (10.6, 9.4, 6), (9, 8, 9.4), (4, 3.6, 10.6)] {
    var ring = [];
    for j 0..12 { ring = append(ring, (cos(360 * j / 12) * p.x, sin(360 * j / 12) * p.y, p.z)); }
    crown = append(crown, ring);
}
var band = [];
for p in [(11.5, 10.3, 1), (11.3, 10.1, 3.4)] {
    var ring = [];
    for j 0..12 { ring = append(ring, (cos(360 * j / 12) * p.x, sin(360 * j / 12) * p.y, p.z)); }
    band = append(band, ring);
}
out.geo = flat_shade(merge(loft_quads(sections: brim, caps: "both", material: "TravStraw"), loft_quads(sections: crown, caps: "both", material: "TravStraw"), loft_quads(sections: band, caps: "both", material: "TravIndigo")));
#end

#mesh TravelerPack
// A courier's pack for the Back socket: bag, flap, side pocket and a bedroll on top. Faces +X like the body.
let bag = center(quad_box(size: (13, 25, 30), res: (2, 2, 2), material: "TravTan"), at: (0, 0, 0));
let flap = center(quad_box(size: (14.4, 26, 10), res: (2, 2, 2), material: "TravLeather"), at: (-0.4, 0, 11));
let pocket = center(quad_box(size: (5, 16, 12), res: (2, 2, 2), material: "TravLeather"), at: (-8, 0, -6));
var roll = [];
for i 0..2 {
    var ring = [];
    for j 0..10 { ring = append(ring, (cos(360 * j / 10) * 5.5, -15 + 30 * i, 20.5 + sin(360 * j / 10) * 5.5)); }
    roll = append(roll, ring);
}
out.geo = flat_shade(merge(bag, flap, pocket, loft_quads(sections: roll, caps: "both", material: "TravCream")));
#end
"""


def wardrobe(path):
    D, PT, O = ["#meshdefs", "// Traveler anatomy tables (generated by oriverse/models/traveler_body.py): tm_ = male, tf_ = female."], [], []
    tex = TEXTURES
    for v in ("male", "female"):
        select(v)
        D += defs(WEAR["t"])
        PT += parts()
        for name, expr, skin in pieces():
            O += piece(name, expr, skin, tex) + [""]
            tex = ()
    select("male")
    D.append("#end")
    text = "\n".join(D) + "\n\n" + "\n".join(PT) + "\n\n" + "\n".join(O) + ACCESSORIES
    open(path, "w").write(text)
    print("saved", path, len(text), "chars", text.count("\n"), "lines")


if __name__ == "__main__":
    args = [a for a in sys.argv[3:] if not a.startswith("--")]
    select(args[0] if args else "male")
    if sys.argv[1] == "render":
        sheet(sys.argv[2])
    elif sys.argv[1] == "wardrobe":
        wardrobe(sys.argv[2])
    else:
        weave(sys.argv[2], textures="--no-textures" not in sys.argv, dressed="--dressed" in sys.argv)
