# Monet RPG — Oriverse source

`monet_day_prototype.weave` is the full Oriverse world (Weave). It is the source of truth:
paste it into the Oriverse editor (or have Claude stage it) to reload the scene.

The look: a Monet / impressionist plein-air landscape — a meadow corridor along a road, a
river with a stone bridge, and a small town on the far bank. The world is painted as brush
strokes, and plants move in a few held frames a second, like hand-drawn animation.

## Game direction
An open-world traveling RPG/FPS in a medieval Monet world. Travel matters more than fighting.
- **Player:** a traveler, courier and mapmaker exploring a world whose map is still incomplete.
- **Core loop:** take a job → pack goods (weight) → plan a route → walk or ride → explore and map → meet road events → deliver → unlock new information and routes.
- **Activities:** delivery jobs, finding new routes, talking to NPCs, events on the road, and slowly making roads safer and easier to travel.
- **Horse vs. on foot:** the horse is for long distances and carrying goods; walking is for forests, mountains, ruins, secret paths and detailed exploration.

## How the painted look is built

| Layer | Where | What it does |
|---|---|---|
| Screen paint pass | `#shader MonetPaintPass` (`material MonetPaint`), set in `#class player` | Fullscreen oil-paint filter: jittered brush-dab cells along a flow field, then a 7x7 Kuwahara filter. Violet shadows / cream lights grade, and distance haze on scenery only (sky excluded). Plants (green pixels) get a ragged brush boil repainted per dab at its own moment. **P** cycles oil paint / PS1 (`Ps1ScreenPass`) / off. |
| Painted sky | `#shader PaintedSky` on `mesh.SkyDomeMesh` (`display SkyDomeShell`) | Our own sky, not the engine skybox. `skyBase` is the smooth underpainting: light-blue horizon, clear cerulean overhead, cumulus with cream lit tops and lilac undersides, and a warm glow toward the sun. `skyPaint` lays overlapping horizontal brush strokes (round head, tapering ragged tail, bristle streaks) in cerulean, lilac and cream over it. The 480 m sphere is pushed out by its vertex hook to wrap the camera about 3 km away. It is unlit, casts no shadow and has `cast_shadow = false`. |
| River water | `#adjuster` section "River" | Engine water with its planar reflection on: it mirrors the bridge, the houses and the painted sky, and gives underwater colour and swimming. (A fully painted river surface was tried and removed; it could not mirror the real scene.) |
| Painted grass | `#shader PaintedGrass`, `#meshpart PaintBlade`, `#mesh GrassTuftA/B` (+ `lod: 1/2`), `#scatter GrassTuftsA/B` | Our own grass. Engine terrain grass is off because it takes no custom shader. Each tuft holds a pose and jumps to the next on its own beat (about 4 poses a second), with gust fronts rolling across the field. Blades part around the player, are painted as flat broken-colour dabs up each blade, and sink into the painted ground past about 40 m. |
| Flowers | `#shader MeadowSway`, `#meshpart MonetFlower` / `MonetLavender`, `#scatter MeadowDaisies/Cosmos/Lavender` | Daisies, cosmos and lavender with stepped sway; each flower steps on its own beat. |
| Wild bank flowers | `#meshpart MonetUmbel` / `MonetSmallBloom`, `#mesh WildLace/WildLaceCream/WildChamomile/WildButtercup` (+ `lod: 1`), `#scatter BankLace/BankLaceCream/BankChamomile/BankButtercup` | Small, low white specks tucked in among the grass (a bent, forked sprig with loose white dots, 25-40 cm, below the grass tips) plus tiny chamomile and buttercups, in drifts along the river banks, the town edges and the road verges. Keep them small and low: tall, stiff, big stems stand out and do not read like the reference. Drift shapes come from each scatter's `shape` blobs. |
| Window boxes | `#meshpart MonetWindow` (`flowers`, `bloom`) | Boxes spilling with red/pink blooms and trailing leaves. |
| Quest HUD | `saved QuestPanelUi` → `screenCanvas QuestPanel : QuestHud` (scene UI, one copy per player, spawned in `#class player`), `#svg QuestDiamond/QuestDiamondOutline` | Top-left quest panel like the reference: a painted slate wash with a dry-brush right edge and a thin gold frame (`oriverse/ui/quest_panel_v5.png`, painted by `oriverse/ui/paint_panel.py`, imported as `image.@ghohoh404040.quest_panel_v5`), text in EB Garamond (Google font) with a soft shadow. It shows, holds for `HoldSecs` (6 s), then fades away by itself over `FadeSecs` (2 s) to `IdleOpacity` (0), so it does not sit on top of the painting. `QuestHud.ShowQuest(Title, Goal, Hint)` swaps the text and shows it again. Scene UI is used instead of `#html` because only scene UI can pick a font. |
| Map screen | `saved MapScreenUi` → `screenCanvas MapScreen : MapHud`, `material MapBackdrop` (screen `#shader`), `#svg MapFleur` / `MapGlow` / `Map*` icons, `oriverse/ui/map_paper.png` + `map_side_panel.png` | **M** opens it and freezes the player; **M** again closes it, and the corner quest panel shows once more and fades. Clear glass bars (near-black `#14181E` at about 55 %) with a hairline gold edge that thins to nothing at the sides, top tabs (Journal / Map / Inventory / Skills / System), a charcoal torn-paper side panel (current objective, discovered locations, region progress) and a warm tan parchment sheet with torn edges, over a blurred backdrop. The sheet is blank for now. Only the Map tab and M are wired; the other tabs and the hint bar (Place Marker, Zoom, Center on Player, Show Journal) are layout only, and the location list and progress are placeholder values. `MapHud.SetQuest(Title, Body)` and `SetRegionProgress(Found, Total)` fill the side panel. The sheet and panel are painted by `oriverse/ui/paint_map_ui.py` (`--straight` writes true-alpha copies for local mock-ups); `oriverse/ui/map_screen_mock.png` is the approved target look. The blur is the screen shader, which is one setting for the whole world: with several players, one player opening the map blurs everyone's view. |
| Traveler body | `#mesh TravelerBody` (`#texture TravelerSkin` / `TravelerCloth`), `SetModel(Ori.mesh.TravelerBody)` in `#class player`, generated by `oriverse/models/traveler_body.py` | The player's base body: a male figure about 7.5 heads tall (180 cm), slightly low-poly and flat-shaded so the paint pass reads it as planes. It is built from anatomy tables (torso, head, arm, leg, foot rings), fused and decimated to about 1500 vertices, with 21 canon bones in a T-pose, so the engine's idle / walk / run / fall play on it with no clips of our own. **V** switches between first person and third person. Wearables: fitted garments are the same tables grown by a gap (the cream trunks use 1.5 cm) and copy their weights from the skin they cover (`transfer_weights`), so an outfit is one mesh swapped with `SetModel`; rigid pieces attach with `AttachToAnchor` to 12 bone-pinned sockets (`Hat`, `Face`, `Chest`, `Back`, `BeltFront`, `BeltBack`, `HipL/R`, `ShoulderL/R`, `HoldL/R`). Edit the tables in the script and run `python3 traveler_body.py weave out.weave` to regenerate the block (`render out.png` draws a local front/back/side sheet). No hair, eyes or fingers yet; the sockets have not been tried with a real item. |
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

## UI design direction (approved: the quest panel)
Every HUD panel follows the quest panel (`screenCanvas QuestPanel`, art `oriverse/ui/quest_panel_v5.png`):
- **Backing:** a painted indigo watercolour wash, not a flat box. Dark slate-indigo core (about `#3C4455`), darkest across the upper middle, cooling to a lighter blue toward the edges. Soft mottling and a faint horizontal brush drag. Edges dissolve in soft dry-brush patches; the right side fades out gradually. No hard stripes, no solid rectangles.
- **Frame:** thin gold lines (about `#DBB875`) drawn as if by hand: the line wavers a little, swells and thins, and the nib skips now and then. Left side full height, top line fading out to the right with a faint second stroke, short bottom line, small ink knots at the corners. Never ruler-straight, even-width lines.
- **Type:** EB Garamond (`font.google.EB_Garamond`). Titles in warm gold (`#E8C88A`), body in cream (`#F3ECDC` / `#E7DDC8`), a very light text shadow (`#00000030`). Thin and quiet, not bold.
- **Icons:** small gold diamonds: an outline diamond for headings, a filled `◆` (`#E3A84E`) for objectives.
- **How to build:** use scene UI (`screenCanvas` / `frame` / `textLabel` / `image`), not `#html`, because only scene UI can pick a font. Paint the backing art with `oriverse/ui/paint_panel.py` (numpy/PIL), push it to this repo, and import it into the project from the raw GitHub URL.
- **Engine quirk:** the UI blend treats image alpha roughly like a gamma-2.2 value (alpha 0.86 shows as about 0.5), so the painter stores `alpha^(1/2.2)`. Keep that step for every new panel image, and check panels over both bright sky and dark foliage.

## Work in progress
- **Water:** back on the engine water (reflections of the bridge and houses work). A painted look for the water itself is still to come.
- **Leftovers in the file:** unused `#scatter FlowersPink/FlowersRed`, the engine grass knobs in `#adjuster` (engine grass is off), and an outdated `#rules` text ("no heavy fullscreen oil-paint filter", "MonetBrushSurface").

## Painted textures
`oriverse/textures/*.png` are Monet-style oil textures generated with Codex CLI image generation, made seamless (originals in `textures/source/`).
They are imported into the Oriverse project from this public repo's raw URLs
(`https://raw.githubusercontent.com/mychicken0/claude_monet/main/oriverse/textures/<file>.png`) and referenced as `projimg.<name>_<hash>` handles in the `.weave` file.
