"""Make a compact visual review sheet of consecutive generated comic pages."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
first, last = map(int, sys.argv[1:3])
cols = 4
thumb_w, thumb_h = 280, 420
rows = (last - first + cols) // cols
sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + 24)), "#191a24")
draw = ImageDraw.Draw(sheet)
for index, number in enumerate(range(first, last + 1)):
    path = root / "reader/medieval/art" / f"page-{number}.png"
    if not path.is_file():
        continue
    with Image.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((thumb_w, thumb_h))
        x = (index % cols) * thumb_w
        y = (index // cols) * (thumb_h + 24)
        sheet.paste(image, (x + (thumb_w - image.width) // 2, y))
        draw.text((x + 8, y + thumb_h + 3), str(number), fill="white")
out = root.parent / "arc-audit" / f"arc5-contact-{first}-{last}.jpg"
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out, quality=90)
print(out)
