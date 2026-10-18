"""Make a labeled contact sheet of local reader screenshots for visual QA."""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2] / "arc-audit" / "review-451-502"
numbers = [int(value) for value in sys.argv[1:]]
columns = 7
tile_w, tile_h = 210, 338
rows = (len(numbers) + columns - 1) // columns
sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), "#dddddd")
draw = ImageDraw.Draw(sheet)
for index, number in enumerate(numbers):
    source = root / f"{number}-desktop.png"
    with Image.open(source) as page:
        page.thumbnail((tile_w - 8, tile_h - 26))
        x = (index % columns) * tile_w + (tile_w - page.width) // 2
        y = (index // columns) * tile_h + 22
        sheet.paste(page, (x, y))
        draw.text((index % columns * tile_w + 5, index // columns * tile_h + 4), str(number), fill="black")
out = root / (f"contact-{numbers[0]}-{numbers[-1]}.jpg")
sheet.save(out, quality=90)
print(out)
