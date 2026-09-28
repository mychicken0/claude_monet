# Monet RPG — Oriverse source

`monet_day_prototype.weave` is the full Oriverse world (Weave). It is the source of truth:
paste it into the Oriverse editor (or have Claude stage it) to reload the scene.

## Layout of the file

| Section | What it is | How to reuse / tweak |
|---|---|---|
| `#adjuster` | Sun, sky light, fog, water, grade | Tune live in the editor's Adjust panel; edits save back into this block |
| `#texture Monet*` | Plaster, stone, roof, grass, path and the tree leaf card sample Codex-painted images (`oriverse/textures/*.png`, imported as `projimg.` project images); wood, window, bark stay procedural | `tint` and `desat` params are sliders; derive colour variants with `material X { base = "MonetPlaster" tint = "#..." }` |
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

## Painted textures
`oriverse/textures/*.png` are Monet-style oil textures generated with Codex CLI image generation, made seamless (originals in `textures/source/`).
They are imported into the Oriverse project from this public repo's raw URLs
(`https://raw.githubusercontent.com/mychicken0/claude_monet/main/oriverse/textures/<file>.png`) and referenced as `projimg.<name>_<hash>` handles in the `.weave` file.
