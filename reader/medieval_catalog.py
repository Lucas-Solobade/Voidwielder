"""The fixed story and character canon for As Estradas do Crepúsculo."""

import json
from pathlib import Path

STORY_DIR = Path(__file__).with_name("medieval")
STORY = json.loads((STORY_DIR / "story.json").read_text(encoding="utf-8"))
CANON = json.loads((STORY_DIR / "canon.json").read_text(encoding="utf-8"))
PAGES = tuple({**page, "art": f"reader/images/medieval/page-{page['number']:02}.webp"} for page in STORY["pages"])
PAGES_BY_NUMBER = {page["number"]: page for page in PAGES}
SERIES_URL = f"/hqs/{STORY['slug']}/"
ARC_URL = f"{SERIES_URL}arcos/{STORY['arc']['slug']}/"


def page_url(number: int) -> str:
    return f"{SERIES_URL}ler/{number}/"


def page_art(number: int) -> str:
    return f"reader/images/medieval/page-{number:02}.webp"
