# Monet RPG — Oriverse source

`monet_day_prototype.weave` is the full Oriverse world (Weave). It is the source of truth:
paste it into the Oriverse editor (or have Claude stage it) to reload the scene.

## Layout of the file

| Section | What it is | How to reuse / tweak |
|---|---|---|
| `#adjuster` | Sun, sky light, fog, water, grade | Tune live in the editor's Adjust panel; edits save back into this block |
| `#texture Monet*` | Painterly base materials (grass, path, stone, plaster, roof, wood, bark, window, leaf card) | `param` colours are sliders; derive colour variants with `material X { base = "MonetPlaster" tint = "#..." }` |
| `#tree MonetRoundTree`, `#tree MonetCypress` | Reusable tree species sharing `MonetLeafCard` | Copy a species and change `seed`, `leaf_tint`, `crown_ellipsoid`; place with `model = "tree.Name"` or scatter via `#forest` |
| `#meshpart MonetHouseKit` | Parametric house (width, depth, floors, windows, lean, roof twist, materials) | New variant = new `#mesh` calling `part(MonetHouseKit, w: ..., floors: ..., wall_mat: ...)` |
| `#meshpart MonetTowerKit` | Round tower with conical roof | `part(MonetTowerKit, r: ..., h: ...)` |
| `#meshpart MonetBridgeKit` | Hump stone bridge (walkable, `collision = mesh`) | `half`, `width`, `rise` params; mesh needs `sim_box` + `anchor(mode: "origin")` |
| `#meshpart MonetFieldWall` | Rough dry-stone field wall | `len`, `h`, `seed` |
| `#meshpart MonetFlowerClump` + `#scatter Flowers*` | Low-poly flower clumps scattered over regions | Change `bloom` material; resize the region objects |

## Art-direction rules (keep these)
- Monet look lives in the assets and lighting: warm sun `#FFE2B4`, cool sky light `#9CB0E4`, lavender shadow tones inside textures.
- No heavy fullscreen oil-paint filter; post-process stays subtle.
- Low-poly geometry with deliberate irregularity (`shear`, roof `jitter`/twist), low-frequency painterly texture breakup.
