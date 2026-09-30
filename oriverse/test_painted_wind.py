"""Run with python3 oriverse/test_painted_wind.py."""
from math import floor
from pathlib import Path
import re

source = Path(__file__).with_name("monet_day_prototype.weave").read_text()
shader = re.search(r"#shader MeadowSway\n([\s\S]*?)\n#end", source)[1]
clock = re.search(r"let t = (.*);", shader)[1].replace("u_camera.time_seconds", "seconds")
rates = re.findall(r'material (?:GrassBlade\w*|FlowerStem|Petal\w*|FlowerEye) \{[^\n]*param7 = ([\d.]+)', source)
assert len(rates) == 9 and set(rates) == {"8"}, "All plant materials must share the 8 fps clock"

def held_time(seconds):
    return eval(clock, {"__builtins__": {}, "floor": floor}, {"seconds": seconds, "fps": 8.0})

samples = [held_time(frame / 60) for frame in range(60)]
assert len(set(samples)) == 8, "Wind should hold eight poses across a 60 fps second"
assert held_time(0.124) == 0 and held_time(0.125) == 0.125
assert held_time(0.249) == 0.125 and held_time(0.250) == 0.250
assert "let tick = floor(u_camera.time_seconds * fps);" in shader
assert "pigment *= ctx.mesh_color.rgb;" in shader, "Keep plant pigments and instance tint"
assert source.count("    PaintFields(Ori.model.mesh.") == 6, "Reuse six static GPU batches"
assert len(re.findall(r'display \w+ \{[^\n]*tag = Tag.Paint', source)) == 24, "Every planting region must route to a batch"
assert 'plants.SetBatchMaterial(Pigment)' in source and 'SetTerrainGrassVisible(false)' in source
assert not re.search(r'object \w+ \{[^\n]*model = "scatter.Meadow', source), "No static scatter plants left behind"
print("Painted wind: 8 held poses/sec, aligned repaint clock, six batches and 24 planting regions.")
