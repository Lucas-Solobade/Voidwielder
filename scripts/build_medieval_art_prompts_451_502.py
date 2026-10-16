"""Produce reproducible, speaker-aware art directions for pages 451–502."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / "reader/medieval/arc4-451-502.json").read_text(encoding="utf-8"))["pages"]
CANON = json.loads((ROOT / "reader/medieval/canon.json").read_text(encoding="utf-8"))

LAYOUTS = {
    "split": "Two unequal vertical comic panels. The first speaker appears in the left panel, with mouth around (24%, 27%) of the full canvas; second speaker appears in the right panel, mouth around (76%, 27%). Leave (4–44%, 12–20%) and (55–95%, 12–20%) as open wall or sky for small speech balloons with very short tails. Smaller evidence/action inserts may occupy the bottom, without new speakers.",
    "stack": "Two asymmetric horizontal comic scenes. First speaker is in the upper scene, mouth around (25%, 27%) of the full canvas; second speaker is in the lower scene, mouth around (77%, 77%). Leave clear plain wall/sky at upper-left (4–46%, 12–20%) and in lower scene upper-right (55–96%, 62–70%) for later speech balloons with very short tails. Do not put faces in those clear areas.",
    "asymmetric": "An asymmetrical comic page: larger top-left conversation scene with first speaker mouth around (26%, 27%); an offset lower-right scene with second speaker mouth around (76%, 79%); one narrow object/detail inset. Reserve clear scenery at (5–46%, 12–20%) and (54–95%, 64–72%) for later speech balloons with very short tails.",
    "wide": "A cinematic wide conversation panel in the upper half, first speaker on left mouth at (25%, 27%), second on right mouth at (76%, 27%), with irregular smaller evidence/action panels below. Reserve clear architecture or sky at (4–45%, 12–20%) and (55–95%, 12–20%) for later speech balloons with very short tails. Do not place heads or hands in those regions.",
}

STYLE = (
    "A new original page of the existing As Estradas do Crepúsculo medieval-fantasy graphic novel, "
    "portrait 2:3, richly hand-painted 2D comic art in warm copper, indigo, moss and ivory, "
    "crisp dark panel gutters, expressive believable adult faces, physically correct five-finger hands and natural necks. "
    "Use provided references only to preserve established character faces, clothing and visual style; "
    "do not copy a prior scene. No printed words, speech balloons, captions, letters, logos, watermarks or ornamental text. "
    "Website speech balloons will be added later into the explicitly reserved areas. "
    "No extra characters, duplicate body parts, impossible anatomy, or character merged with another. "
)


def appearance(character_id):
    character = CANON["characters"][character_id]
    return f"{character['name']}: {character['fixed_appearance']} Clothing: {character['fixed_clothing']}"


def references_for(page):
    number = page["number"]
    refs = ["reader/medieval/art/page-450.png"]
    if 464 < number <= 469:
        refs.append("reader/medieval/art/page-464.png")
    if 476 <= number <= 478:
        refs.append("reader/medieval/art/page-168.png")
    if 487 <= number <= 490:
        refs.append("reader/medieval/art/page-442.png")
    for character_id in page["cast"]:
        path = f"reader/medieval/references/individual/{character_id}.png"
        if (ROOT / path).exists() and path not in refs:
            refs.append(path)
    return refs[:4]


manifest = []
for page in PAGES:
    speaker_order = [line["speaker"] for line in page["lines"]]
    cast = "\n".join(appearance(character_id) for character_id in page["cast"])
    prompt = (
        STYLE
        + f"Page {page['number']} of arc 4. Location and moment: {page['place']}, {page['time']}. "
        + f"Specific visible action: {page['scene']} "
        + f"Speaker order and positions: {speaker_order[0]} speaks first; {speaker_order[1]} replies. "
        + LAYOUTS[page["layout"]]
        + " Exact identity locks for the characters depicted:\n"
        + cast
        + "\nNo invented characters. Faces must be unobscured and physically distinct. "
        + "Place props consistently with the scene and era. Both dialogue lines will be typeset in the web page; do not draw any text."
    )
    manifest.append({
        "page": page["number"],
        "prompt": prompt,
        "reference_images": references_for(page),
        "output_png": f"reader/medieval/art/page-{page['number']}.png",
        "output_webp": f"reader/static/reader/images/medieval/page-{page['number']}.webp",
    })

path = ROOT / "reader/medieval/art-prompts-451-502.json"
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(manifest)} prompts to {path}")
