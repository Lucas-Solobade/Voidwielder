"""The fixed story and character canon for As Estradas do Crepúsculo."""

import json
from pathlib import Path

STORY_DIR = Path(__file__).with_name("medieval")
STORY = json.loads((STORY_DIR / "story.json").read_text(encoding="utf-8"))
ARC_TWO = json.loads((STORY_DIR / "arc2.json").read_text(encoding="utf-8"))
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-81-90.json").read_text(encoding="utf-8"))["pages"])
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-91-134.json").read_text(encoding="utf-8"))["pages"])
CANON = json.loads((STORY_DIR / "canon.json").read_text(encoding="utf-8"))


def page_art(number: int) -> str:
    extension = "svg" if number >= 133 else "webp"
    return f"reader/images/medieval/page-{number:02}.{extension}"


PAGES = tuple(
    {**page, "art": page_art(page["number"])}
    for page in [*STORY["pages"], *ARC_TWO["pages"]]
)
PAGES_BY_NUMBER = {page["number"]: page for page in PAGES}
SERIES_URL = f"/hqs/{STORY['slug']}/"
ARC_URL = f"{SERIES_URL}arcos/{STORY['arc']['slug']}/"
ARC2_URL = f"{SERIES_URL}arcos/{ARC_TWO['arc']['slug']}/"
ARCS = (
    {**STORY["arc"], "start": STORY["pages"][0]["number"], "end": STORY["pages"][-1]["number"], "url": ARC_URL, "art": STORY["cover"]},
    {**ARC_TWO["arc"], "end": ARC_TWO["pages"][-1]["number"], "url": ARC2_URL, "art": "reader/images/medieval/page-33.webp"},
)


def get_arc_for_page(number: int) -> dict | None:
    return next((arc for arc in ARCS if arc["start"] <= number <= arc["end"]), None)


def page_url(number: int) -> str:
    return f"{SERIES_URL}ler/{number}/"
