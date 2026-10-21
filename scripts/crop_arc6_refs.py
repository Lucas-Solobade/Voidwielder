"""Extract unaltered individual reference crops from the published cast sheets."""

from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1] / "reader/medieval/references"
out = root / "individual"
out.mkdir(exist_ok=True)

for name, source, box in [
    ("sere", "travelers-sheet.png", (740, 0, 1120, 1024)),
    ("caio", "school-cast-sheet.png", (0, 0, 310, 1024)),
    ("tovo", "school-cast-sheet.png", (310, 0, 620, 1024)),
    ("ordelia", "school-cast-sheet.png", (620, 0, 925, 1024)),
    ("teren", "school-cast-sheet.png", (925, 0, 1230, 1024)),
]:
    Image.open(root / source).crop(box).save(out / f"{name}.png")
