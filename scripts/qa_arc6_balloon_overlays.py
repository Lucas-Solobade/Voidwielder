"""Make a contact sheet with planned balloons over the actual comic art.

This is a conservative visual QA aid, not a replacement for browser review:
the red shapes approximate the browser's text wrapping at full page width.
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "reader/medieval/arc6-831-924.json").read_text(encoding="utf-8"))
PAGES = {page["number"]: page for page in DATA["pages"]}
first = int(sys.argv[1])
last = int(sys.argv[2])
out = Path(sys.argv[3])
selected = [PAGES[n] for n in range(first, last + 1) if (ROOT / f"reader/static/reader/images/medieval/page-{n}.webp").is_file()]
columns = min(5, len(selected))
tile_w, tile_h = 250, 395
sheet = Image.new("RGB", (columns * tile_w, math.ceil(len(selected) / columns) * tile_h), "#101319")
font = ImageFont.load_default()

for index, page in enumerate(selected):
    image = Image.open(ROOT / f"reader/static/reader/images/medieval/page-{page['number']}.webp").convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    width, height = image.size
    for line in page["lines"]:
        b = line["balloon"]
        x = width * b["x"] / 100
        y = height * b["y"] / 100
        w = width * b["w"] / 100
        wrapped_lines = max(1, math.ceil(len(line["text"]) / 39))
        h = 44 + wrapped_lines * 24
        draw.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=(255, 251, 238, 180), outline=(230, 20, 30, 255), width=6)
        draw.text((x + 12, y + 9), line["speaker"], fill=(0, 0, 0, 255), font=font)
        draw.line((x + w / 2, y + h, width * b["target_x"] / 100, height * b["target_y"] / 100), fill=(230, 20, 30, 255), width=3)
    thumb = ImageOps.contain(image.convert("RGB"), (tile_w - 10, tile_h - 40))
    px = (index % columns) * tile_w + (tile_w - thumb.width) // 2
    py = (index // columns) * tile_h
    sheet.paste(thumb, (px, py))
    ImageDraw.Draw(sheet).text(((index % columns) * tile_w + 8, py + tile_h - 31), str(page["number"]), fill="white", font=font)

out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(f"Wrote {out} for {len(selected)} pages")
