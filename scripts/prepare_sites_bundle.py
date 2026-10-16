"""Keep the Sites package small by using the public GitHub Pages art mirror.

GitHub Pages builds the complete static export from source. Sites has a 256 MB
expanded package limit, so its build uses the same published images for the
original 96-page comic while retaining all new medieval art locally.
"""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = (ROOT / "dist").resolve()
ART = (DIST / "static/reader/images/pages").resolve()
ART.relative_to(DIST)
MIRROR = "https://lucas-solobade.github.io/Voidwielder"
LOCAL = "/static/reader/images/pages/"

if not (DIST / "index.html").is_file():
    raise SystemExit("Run scripts/export_static.py before preparing the Sites bundle")

images = sorted(ART.glob("page-*.webp"))
if len(images) != 96 or any(not re.fullmatch(r"page-\d{2}\.webp", path.name) for path in images):
    raise SystemExit("Expected the 96 original comic images before slimming the Sites bundle")

rewrites = 0
for path in DIST.rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    changed = html.replace(LOCAL, MIRROR + LOCAL)
    if changed != html:
        rewrites += html.count(LOCAL)
        path.write_text(changed, encoding="utf-8")

if rewrites < 96:
    raise SystemExit("Too few image references were rewritten; local images were retained")

saved = sum(path.stat().st_size for path in images)
for path in images:
    path.unlink()
ART.rmdir()
print(f"Sites bundle: {rewrites} references use GitHub Pages; saved {saved / 1048576:.1f} MiB")
