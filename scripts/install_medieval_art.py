"""Copy a reviewed generated page into source art and its optimized web asset."""

import shutil
import sys
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[1]
number = int(sys.argv[1])
source = Path(sys.argv[2])
if not source.is_file():
    raise SystemExit(f"Missing generated art: {source}")
png = root / "reader" / "medieval" / "art" / f"page-{number}.png"
webp = root / "reader" / "static" / "reader" / "images" / "medieval" / f"page-{number}.webp"
shutil.copyfile(source, png)
with Image.open(source) as image:
    image.convert("RGB").save(webp, "WEBP", quality=86, method=6)
print(number, png, webp)
