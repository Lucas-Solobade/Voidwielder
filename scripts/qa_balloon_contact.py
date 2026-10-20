"""Create a visual QA sheet with approximate balloon footprints over comic art.

The output is temporary review material; published images are never edited.
"""

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    pages = {page["number"]: page for page in json.loads(args.source.read_text(encoding="utf-8"))["pages"]}
    numbers = list(range(args.start, args.end + 1))
    cell_width, cell_height, columns = 440, 570, 4
    sheet = Image.new("RGB", (columns * cell_width, math.ceil(len(numbers) / columns) * cell_height), "#ddd")
    labels = ImageDraw.Draw(sheet)
    root = Path("reader/static/reader/images/medieval")
    for index, number in enumerate(numbers):
        if not (root / f"page-{number}.webp").exists():
            continue
        image = Image.open(root / f"page-{number}.webp").convert("RGBA")
        width, height = image.size
        draw = ImageDraw.Draw(image, "RGBA")
        for line_index, line in enumerate(pages[number].get("lines", [])):
            balloon = line["balloon"]
            x = balloon["x"] / 100 * width
            y = balloon["y"] / 100 * height
            bubble_width = balloon["w"] / 100 * width
            # Average rendered height of a named two-line balloon on desktop.
            bubble_height = .064 * height
            color = (255, 15, 15, 125) if line_index % 2 == 0 else (0, 80, 255, 125)
            draw.rectangle((x, y, x + bubble_width, y + bubble_height), fill=color, outline=(0, 0, 0, 255), width=3)
            draw.text((x + 8, y + 8), line["speaker"], fill=(0, 0, 0, 255))
        top = image.crop((0, 0, width, int(.72 * height))).convert("RGB")
        top.thumbnail((cell_width - 8, cell_height - 30))
        left = (index % columns) * cell_width + 4
        above = (index // columns) * cell_height + 26
        sheet.paste(top, (left, above))
        labels.text((left, above - 20), str(number), fill="black")
    sheet.save(args.output, quality=90)


if __name__ == "__main__":
    main()
