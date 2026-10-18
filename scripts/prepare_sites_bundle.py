"""Keep the Sites package small by using the public GitHub Pages art mirror.

GitHub Pages builds the complete static export from source. Sites has a 256 MB
expanded package limit, so its build uses the same published images for the
original 96-page comic, the first 150 medieval pages and two established vector
pages while retaining all new medieval art locally.
"""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = (ROOT / "dist").resolve()
ART = (DIST / "static/reader/images/pages").resolve()
ART.relative_to(DIST)
MEDIEVAL_ART = (DIST / "static/reader/images/medieval").resolve()
MEDIEVAL_ART.relative_to(DIST)
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

vector_pages = [MEDIEVAL_ART / f"page-{number}.svg" for number in (133, 134)]
if any(not path.is_file() for path in vector_pages):
    raise SystemExit("Expected both established vector pages before slimming the Sites bundle")
vector_rewrites = {path.name: 0 for path in vector_pages}
for page in DIST.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    changed = html
    for path in vector_pages:
        local = f"/static/reader/images/medieval/{path.name}"
        vector_rewrites[path.name] += changed.count(local)
        changed = changed.replace(local, MIRROR + local)
    if changed != html:
        page.write_text(changed, encoding="utf-8")
if any(count == 0 for count in vector_rewrites.values()):
    raise SystemExit("Vector art references were not found; local images were retained")

saved = sum(path.stat().st_size for path in [*images, *vector_pages])
for path in [*images, *vector_pages]:
    path.unlink()
ART.rmdir()

early_medieval = [
    MEDIEVAL_ART / f"page-{number:02}.webp"
    for number in range(1, 151)
    if number not in (133, 134)  # These pages have SVG assets above.
]
if any(not path.is_file() for path in early_medieval):
    raise SystemExit("Expected the first 150 medieval pages, apart from the two SVG pages")
early_rewrites = 0
for page in DIST.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    changed = html
    for art in early_medieval:
        local = f"/static/reader/images/medieval/{art.name}"
        early_rewrites += changed.count(local)
        changed = changed.replace(local, MIRROR + local)
    if changed != html:
        page.write_text(changed, encoding="utf-8")
if early_rewrites < len(early_medieval):
    raise SystemExit("Too few medieval image references were rewritten")

saved += sum(path.stat().st_size for path in early_medieval)
for path in early_medieval:
    path.unlink()
print(f"Sites bundle: {rewrites + sum(vector_rewrites.values()) + early_rewrites} references use GitHub Pages; saved {saved / 1048576:.1f} MiB")
