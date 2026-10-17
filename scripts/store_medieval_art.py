"""Copy an approved generated comic page and encode its static WebP twin."""

import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
number = int(sys.argv[1])
source = Path(sys.argv[2]).resolve()
assert 451 <= number <= 518
assert source.is_file() and source.suffix.lower() == ".png"
target = ROOT / f"reader/medieval/art/page-{number}.png"
static = ROOT / f"reader/static/reader/images/medieval/page-{number}.webp"
if target.exists() or static.exists():
    raise SystemExit(f"Page {number} already exists; review it before replacing")
shutil.copy2(source, target)
with Image.open(source) as image:
    image.save(static, "WEBP", quality=86, method=6)
print(number, target.stat().st_size, static.stat().st_size)
