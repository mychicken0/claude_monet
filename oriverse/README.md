# Monet RPG — Oriverse source

`monet_day_prototype.weave` is the full Oriverse world (Weave). It is the source of truth:
paste it into the Oriverse editor (or have Claude stage it) to reload the scene.

The look: a Monet / impressionist plein-air landscape — a meadow corridor along a road, a
river with a stone bridge, and a small town on the far bank. The world is painted as brush
strokes, and plants move in a few held frames a second, like hand-drawn animation.

## How the painted look is built

| Layer | Where | What it does |
|---|---|---|
| Screen paint pass | `#shader MonetPaintPass` (`material MonetPaint`), set in `#class player` | Fullscreen oil-paint filter: jittered brush-dab cells along a flow field, then a 7x7 Kuwahara filter. Violet shadows / cream lights grade, and distance haze on scenery only (sky excluded). Plants (green pixels) get a ragged brush boil repainted per dab at its own moment. **P** cycles oil paint / PS1 (`Ps1ScreenPass`) / off. |
| Painted sky | `#shader PaintedSky` on `mesh.SkyDomeMesh` (`display SkyDomeShell`) | Our own sky, not the engine skybox. `skyBase` is the smooth underpainting: light-blue horizon, clear cerulean overhead, cumulus with cream lit tops and lilac undersides, and a warm glow toward the sun. `skyPaint` lays overlapping horizontal brush strokes (round head, tapering ragged tail, bristle streaks) in cerulean, lilac and cream over it. The 480 m sphere is pushed out by its vertex hook to wrap the camera about 3 km away. It is unlit, casts no shadow and has `cast_shadow = false`. |
| River water | `#adjuster` section "River" | Engine water with its planar reflection on: it mirrors the bridge, the houses and the painted sky, and gives underwater colour and swimming. (A fully painted river surface was tried and removed; it could not mirror the real scene.) |
| Painted grass | `#shader PaintedGrass`, `#meshpart PaintBlade`, `#mesh GrassTuftA/B` (+ `lod: 1/2`), `#scatter GrassTuftsA/B` | Our own grass. Engine terrain grass is off because it takes no custom shader. Each tuft holds a pose and jumps to the next on its own beat (about 4 poses a second), with gust fronts rolling across the field. Blades part around the player, are painted as flat broken-colour dabs up each blade, and sink into the painted ground past about 40 m. |
| Flowers | `#shader MeadowSway`, `#meshpart MonetFlower` / `MonetLavender`, `#scatter MeadowDaisies/Cosmos/Lavender` | Daisies, cosmos and lavender with stepped sway; each flower steps on its own beat. |
| Surfaces | `#texture Monet*` | Plaster, stone, roof, grass and path sample Codex-painted images (`oriverse/textures/*.png`, imported as `projimg.` project images). Wood, window and bark stay procedural. |

Everything that grows (grass, flowers, trees) is placed with terrain scatters / forests, so
it sits on the ground only, never on walls or roads.

## Tuning knobs

| What | Where | Current |
|---|---|---|
| Screen paint strength / grade / haze / Kuwahara stride / dab size / wobble / plant repaints per s / plant wobble | `SetMaterialParameterNumber(Material.MonetPaint, 0..7, …)` in `#class player` | 0.65 / 0.55 / 0.35 / 2.6 / 8 / 0.65 / 4 / 3 |
| Grass poses per second / sway (m) / sink distance (m) | `PaintGrass`, `PaintGrassDry`: `param3` / `param7` / `param11` | 4 / 0.12 / 40 |
| Grass density | `#scatter GrassTuftsA` `spacing`, `GrassTuftsB` `spacing` + `density_pct` | 36 cm; 70 cm at 50 % |
| Sky colours, clouds, stroke size | `fn skyBase` / `fn skyPaint` in `#shader PaintedSky` | — |
| Sunlight (strong warm sun, cool blue shade, rich colour) | `#adjuster` "Monet daylight" | Sun 8 `#FFD9A0`; sky light 1.4 `#98ADEB` (saturation 1.2); shadow opacity 0.6; saturation 1.35; contrast 1.15; bloom 0.3 |
| River water | `#adjuster` "River" | Waves 3 cm, shallow `#86C0C8`, deep `#3F6FA0`, reflection 1 |
| Depth of field | `#adjuster` (editor Adjust panel) | Engine distance fog is **off**: it washed the painted sky to grey. Distance haze (light blue air) comes from the screen pass. |

## Scene layout (sim cm, Z up)
- Road along +X: `RoadSouth` (x -1500..1745) and `RoadNorth` (x 2855..8000), y ±220.
- River along Y at x ≈ 2300 (carved by `carve_path` in `#terrain MonetValley`). `Bridge` is at (2300, 0).
- Town on the far bank: `House1-8`, `Tower1`. Meadow fields north and south of the road: `GrassA/B*`, `Daisies*`, `Cosmos*` and `Lavender*` region objects.
- Painted cloud cards (`Cloud1-10`) and distant set-piece cards (`Bd*`) sit in front of the sky dome.

## Reusable kits
| Section | What it is | How to reuse / tweak |
|---|---|---|
| `#tree MonetRoundTree`, `#tree MonetCypress`, `#forest MeadowTrees` | Tree species sharing `MonetLeafCard` | Copy a species and change `seed`, `leaf_tint`, `crown_ellipsoid`; place with `model = "tree.Name"` or scatter via `#forest` |
| `#meshpart MonetHouseKit` | Parametric house (width, depth, floors, windows, lean, roof twist, materials) | New variant = new `#mesh` calling `part(MonetHouseKit, w: ..., floors: ..., wall_mat: ...)` |
| `#meshpart MonetTowerKit`, `MonetChurchKit` | Round tower with conical roof; church | `part(MonetTowerKit, r: ..., h: ...)` |
| `#meshpart MonetBridgeKit` | Hump stone bridge (walkable, `collision = mesh`) | `half`, `width`, `rise` params; mesh needs `sim_box` + `anchor(mode: "origin")` |
| `#meshpart MonetFieldWall` | Rough dry-stone field wall | `len`, `h`, `seed` |
| `#meshpart PaintBlade` | One tapering grass ribbon | `h`, `lean`, `w`, `mat` (`PaintGrass` / `PaintGrassDry`) |

## Art-direction rules (keep these)
- Warm sun `#FFE2B4`, cool sky light; shadows lean lavender / blue-violet, highlights cream / warm yellow.
- Everything reads as brush strokes: overlapping tapered strokes with bristle streaks, never hard square cells.
- Motion is hand-drawn: few held frames a second, and every tuft, flower and stroke keeps its own beat. Nothing may change in sync across the whole field; global engine wind/wave re-rolls caused that flicker before.
- The sky, the water and the light share one palette: clear cerulean sky, warm golden sun, blue-violet shade. The river mirrors the sky and the town.

## Work in progress
- **Water:** back on the engine water (reflections of the bridge and houses work). A painted look for the water itself is still to come.
- **Leftovers in the file:** unused `#scatter FlowersPink/FlowersRed`, the engine grass knobs in `#adjuster` (engine grass is off), and an outdated `#rules` text ("no heavy fullscreen oil-paint filter", "MonetBrushSurface").

## Painted textures
`oriverse/textures/*.png` are Monet-style oil textures generated with Codex CLI image generation, made seamless (originals in `textures/source/`).
They are imported into the Oriverse project from this public repo's raw URLs
(`https://raw.githubusercontent.com/mychicken0/claude_monet/main/oriverse/textures/<file>.png`) and referenced as `projimg.<name>_<hash>` handles in the `.weave` file.
