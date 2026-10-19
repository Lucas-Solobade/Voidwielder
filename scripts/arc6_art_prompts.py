"""Emit identity-locked prompts for the first pages of arc six."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIEVAL = ROOT / "reader" / "medieval"
PAGES = json.loads((MEDIEVAL / "arc6-729-741.json").read_text(encoding="utf-8"))["pages"]
CANON = json.loads((MEDIEVAL / "canon.json").read_text(encoding="utf-8"))
REFERENCES = {
    "ilyan": "references/individual/ilyan.png",
    "teren": "references/individual/teren.png",
    "oru": "references/oru-sheet.png",
    "runa": "references/runa-sheet.png",
    "ordelia": "references/individual/ordelia.png",
    "liria": "../static/reader/images/medieval/page-536.webp",
    "caio": "references/individual/caio.png",
    "sere": "references/individual/sere.png",
}
LAYOUTS = {
    "panoramic-with-map-detail": "One large panoramic interaction and one small map-only inset. No repeated people.",
    "large-forge-and-small-metal-detail": "Large forge scene with an irregular small metal-only inset. No repeated people.",
    "diagonal-action-with-nail-detail": "Dynamic diagonal action composition with one small fallen-nail-only inset. No repeated people.",
    "single-cinematic": "One uninterrupted cinematic panel, no insets.",
    "tall-figures-and-ash-detail": "Tall central scene and one tiny ash-only detail panel. No repeated people.",
    "two-unequal-views": "Main two-person scene and one narrow object-only detail panel. No repeated people.",
    "large-table-and-object-inset": "Large table scene and one stone-spoon-only detail inset. No repeated people.",
    "single-cinematic-with-ember-detail": "One dramatic main scene and one very small dead-coal-only inset. No repeated people.",
    "panoramic-work-and-bucket-detail": "Wide forge work scene and one tiny bucket or window-only inset. No repeated people.",
    "high-library-and-ledger-detail": "Tall library architecture around a large two-person panel with ledger-only inset. No repeated people.",
    "two-rivals-and-map-detail": "One confrontational two-person panel and a small map-only detail inset. No repeated people.",
    "single-table-with-two-column-detail": "Single table scene and small paper-only detail inset. No repeated people.",
    "wide-training-action-and-ribbon-detail": "Dynamic wide training action with ribbon-only inset. No repeated people.",
}


def prompt_for(page: dict) -> dict:
    cast = page["cast"]
    identity = " ".join(
        f"{CANON['characters'][key]['name']}: {CANON['characters'][key]['fixed_appearance']} "
        f"Wardrobe: {CANON['characters'][key]['fixed_clothing']}"
        for key in cast
    )
    place = CANON["school_map"][page["place"]]
    prompt = (
        f"Create original VERTICAL PORTRAIT 2:3 medieval fantasy comic page, 1024 pixels WIDE and 1536 pixels TALL, "
        f"upright book-page format, never landscape, for As Estradas do Crepúsculo page {page['number']}. "
        "Detailed painterly 2D illustrated graphic novel, refined ink lines, natural anatomy, warm copper, indigo and ivory palette; "
        "match the established reference faces precisely. This is a visual scene with NO printed words or balloons; "
        "speech will be added separately in the website. "
        f"Depict precisely this event and no later story events: {page['scene']} "
        f"Time: {page['time']}. Permanent location design: {place} "
        f"Exactly TWO clearly visible principal people, ordered LEFT to RIGHT: {cast[0]} then {cast[1]}. "
        f"Locked character identities: {identity} "
        "Use reference images only for the specified person's face, scale, hair, age and wardrobe; never replicate their background or extra figures. "
        f"Panel design: {LAYOUTS[page['layout']]} "
        "All heads and facial expressions must be fully visible and placed between 26% and 44% down the page, "
        "one left of center and one right of center. Reserve the top 20% as open architecture or quiet atmosphere "
        "for two short later speech balloons directly above the respective speakers. Never put a face, hand, clue or action in that balloon area. "
        "No face hidden by hair or hands, no crossed or dislocated neck, no duplicated figure, exactly two arms and two hands per person, "
        "five fingers on each visible hand, anatomically credible joints and perspective. "
        "Avoid extreme camera distortion, oversized hands, crossed eyes, extra limbs, cropped faces, modern objects, logos, letters, labels or watermarks. "
        "Magic can guide only a physically present element, never create fire or wind from nothing."
    )
    return {
        "number": page["number"],
        "prompt": prompt,
        "refs": [str((MEDIEVAL / REFERENCES[key]).resolve()) for key in cast],
    }


if __name__ == "__main__":
    first, last = map(int, sys.argv[1:3])
    print(json.dumps([prompt_for(p) for p in PAGES if first <= p["number"] <= last], ensure_ascii=False))
