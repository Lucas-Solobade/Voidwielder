"""The fixed story and character canon for As Estradas do Crepúsculo."""

import json
from pathlib import Path

STORY_DIR = Path(__file__).with_name("medieval")
STORY = json.loads((STORY_DIR / "story.json").read_text(encoding="utf-8"))
ARC_TWO = json.loads((STORY_DIR / "arc2.json").read_text(encoding="utf-8"))
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-81-90.json").read_text(encoding="utf-8"))["pages"])
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-91-134.json").read_text(encoding="utf-8"))["pages"])
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-135-149.json").read_text(encoding="utf-8"))["pages"])
ARC_TWO["pages"].extend(json.loads((STORY_DIR / "arc2-150-171.json").read_text(encoding="utf-8"))["pages"])
ARC_THREE = json.loads((STORY_DIR / "arc3.json").read_text(encoding="utf-8"))
ARC_THREE["pages"].extend(json.loads((STORY_DIR / "arc3-179-189.json").read_text(encoding="utf-8"))["pages"])
for first, last in ((190, 201), (202, 213), (214, 225), (226, 237), (238, 250), (251, 268),
                    (269, 280), (281, 292), (293, 304), (305, 316)):
    ARC_THREE["pages"].extend(
        page for page in json.loads((STORY_DIR / f"arc3-{first}-{last}.json").read_text(encoding="utf-8"))["pages"]
        if page["number"] <= 311
    )
ARC_THREE["pages"].extend(json.loads((STORY_DIR / "arc3-312-355.json").read_text(encoding="utf-8"))["pages"])
ARC_FOUR = json.loads((STORY_DIR / "arc4-356-366.json").read_text(encoding="utf-8"))
ARC_FOUR_CONTINUED = json.loads((STORY_DIR / "arc4-367-420.json").read_text(encoding="utf-8"))
ARC_FOUR["arc"] = ARC_FOUR_CONTINUED["arc"]
ARC_FOUR["pages"].extend(ARC_FOUR_CONTINUED["pages"])
ARC_FOUR_NEW = json.loads((STORY_DIR / "arc4-421-435.json").read_text(encoding="utf-8"))
ARC_FOUR["arc"]["chapters"].extend(ARC_FOUR_NEW["chapters"])
ARC_FOUR["pages"].extend(ARC_FOUR_NEW["pages"])
ARC_FOUR_LAST = json.loads((STORY_DIR / "arc4-436-450.json").read_text(encoding="utf-8"))
ARC_FOUR["arc"]["chapters"][-1]["end"] = 449
ARC_FOUR["arc"]["chapters"].extend(ARC_FOUR_LAST["chapters"])
ARC_FOUR["pages"].extend(ARC_FOUR_LAST["pages"])
ARC_FOUR_NEXT = json.loads((STORY_DIR / "arc4-451-502.json").read_text(encoding="utf-8"))
ARC_FOUR["arc"]["chapters"][-1]["end"] = 502
ARC_FOUR["pages"].extend(ARC_FOUR_NEXT["pages"])
ARC_FOUR_END = json.loads((STORY_DIR / "arc4-503-518.json").read_text(encoding="utf-8"))
ARC_FOUR["arc"]["chapters"].extend(ARC_FOUR_END["chapters"])
ARC_FOUR["pages"].extend(ARC_FOUR_END["pages"])
ARC_FOUR["arc"]["status"] = "Concluído"
ARC_FIVE = json.loads((STORY_DIR / "arc5-519-524.json").read_text(encoding="utf-8"))
ARC_FIVE_NEXT = json.loads((STORY_DIR / "arc5-525-532.json").read_text(encoding="utf-8"))
ARC_FIVE["arc"]["chapters"].extend(ARC_FIVE_NEXT["chapters"])
ARC_FIVE["pages"].extend(ARC_FIVE_NEXT["pages"])
ARC_FIVE_LAST = json.loads((STORY_DIR / "arc5-533-554.json").read_text(encoding="utf-8"))
ARC_FIVE["arc"]["chapters"].extend(ARC_FIVE_LAST["chapters"])
ARC_FIVE["pages"].extend(ARC_FIVE_LAST["pages"])
ARC_FIVE_RAIN = json.loads((STORY_DIR / "arc5-555-604.json").read_text(encoding="utf-8"))
ARC_FIVE["arc"]["chapters"].extend(ARC_FIVE_RAIN["chapters"])
ARC_FIVE["pages"].extend(ARC_FIVE_RAIN["pages"])
ARC_FIVE_SCHOOL = json.loads((STORY_DIR / "arc5-605-644.json").read_text(encoding="utf-8"))
ARC_FIVE["arc"]["chapters"].extend(ARC_FIVE_SCHOOL["chapters"])
ARC_FIVE["pages"].extend(ARC_FIVE_SCHOOL["pages"])
ARC_FIVE_END = json.loads((STORY_DIR / "arc5-645-728.json").read_text(encoding="utf-8"))
ARC_FIVE["arc"]["chapters"].extend(ARC_FIVE_END["chapters"])
ARC_FIVE["pages"].extend(ARC_FIVE_END["pages"])
ARC_FIVE["arc"]["status"] = "Concluído"
ARC_SIX = json.loads((STORY_DIR / "arc6-729-741.json").read_text(encoding="utf-8"))
ARC_SIX_CONTINUED = json.loads((STORY_DIR / "arc6-742-795.json").read_text(encoding="utf-8"))
ARC_SIX["arc"]["chapters"][-1]["end"] = 760
ARC_SIX["arc"]["chapters"].extend(ARC_SIX_CONTINUED["chapters"])
ARC_SIX["pages"].extend(ARC_SIX_CONTINUED["pages"])
ARC_SIX_PORT = json.loads((STORY_DIR / "arc6-796-830.json").read_text(encoding="utf-8"))
ARC_SIX["arc"]["chapters"][-1]["end"] = 830
ARC_SIX["pages"].extend(ARC_SIX_PORT["pages"])
ARC_SIX_FURTHER = json.loads((STORY_DIR / "arc6-831-924.json").read_text(encoding="utf-8"))
ARC_SIX["arc"]["chapters"].extend(ARC_SIX_FURTHER["chapters"])
ARC_SIX["pages"].extend(ARC_SIX_FURTHER["pages"])
CANON = json.loads((STORY_DIR / "canon.json").read_text(encoding="utf-8"))


def page_art(number: int) -> str:
    extension = "svg" if 133 <= number <= 134 or number == 766 else "webp"
    return f"reader/images/medieval/page-{number:02}.{extension}"


PAGES = tuple(
    {**page, "art": page_art(page["number"])}
    for page in [*STORY["pages"], *ARC_TWO["pages"], *ARC_THREE["pages"], *ARC_FOUR["pages"], *ARC_FIVE["pages"], *ARC_SIX["pages"]]
)
PAGES_BY_NUMBER = {page["number"]: page for page in PAGES}
SERIES_URL = f"/hqs/{STORY['slug']}/"
ARC_URL = f"{SERIES_URL}arcos/{STORY['arc']['slug']}/"
ARC2_URL = f"{SERIES_URL}arcos/{ARC_TWO['arc']['slug']}/"
ARC3_URL = f"{SERIES_URL}arcos/{ARC_THREE['arc']['slug']}/"
ARC4_URL = f"{SERIES_URL}arcos/{ARC_FOUR['arc']['slug']}/"
ARC5_URL = f"{SERIES_URL}arcos/{ARC_FIVE['arc']['slug']}/"
ARC6_URL = f"{SERIES_URL}arcos/{ARC_SIX['arc']['slug']}/"
ARCS = (
    {**STORY["arc"], "start": STORY["pages"][0]["number"], "end": STORY["pages"][-1]["number"], "url": ARC_URL, "art": STORY["cover"]},
    {**ARC_TWO["arc"], "end": ARC_TWO["pages"][-1]["number"], "url": ARC2_URL, "art": "reader/images/medieval/page-33.webp"},
    {**ARC_THREE["arc"], "end": ARC_THREE["pages"][-1]["number"], "url": ARC3_URL, "art": "reader/images/medieval/arc3-cover.webp"},
    {**ARC_FOUR["arc"], "end": ARC_FOUR["pages"][-1]["number"], "url": ARC4_URL, "art": "reader/images/medieval/arc4-cover.webp"},
    {**ARC_FIVE["arc"], "end": ARC_FIVE["pages"][-1]["number"], "url": ARC5_URL, "art": "reader/images/medieval/arc5-cover.webp"},
    {**ARC_SIX["arc"], "end": ARC_SIX["pages"][-1]["number"], "url": ARC6_URL, "art": "reader/images/medieval/arc6-cover.webp"},
)


def get_arc_for_page(number: int) -> dict | None:
    return next((arc for arc in ARCS if arc["start"] <= number <= arc["end"]), None)


def page_url(number: int) -> str:
    return f"{SERIES_URL}ler/{number}/"
