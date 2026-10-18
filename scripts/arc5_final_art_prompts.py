"""Print locked-character image prompts for the ending of arc five."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pages = json.loads((root / "reader/medieval/arc5-645-728.json").read_text(encoding="utf-8"))["pages"]
canon = json.loads((root / "reader/medieval/canon.json").read_text(encoding="utf-8"))
ref_root = root / "reader/medieval"
refs = {
    "ilyan": "references/ilyan-sheet.png", "runa": "references/runa-sheet.png",
    "oru": "references/oru-sheet.png", "liria": "art/page-544.png",
    "ordelia": "references/individual/ordelia.png", "eda": "references/individual/eda.png",
    "sere": "references/individual/sere.png", "caio": "references/individual/caio.png",
    "beren": "references/individual/beren.png", "talin": "references/individual/talin.png",
    "braka": "references/individual/braka.png", "maelor": "art/page-476.png",
    "teren": "references/individual/teren.png", "adra": "references/individual/adra.png",
}
layouts = [
    "A dominant cinematic panel and one narrow asymmetric detail inset, no three equal strips.",
    "Two unequal panels with a tall left scene and a small right evidence or reaction inset.",
    "One upper panoramic action panel above two small unequal lower details, readable sequence.",
    "Single dramatic scene with a tiny inset only if the event requires it.",
]

first, last = map(int, sys.argv[1:3])
out = []
for p in pages:
    n = p["number"]
    if not first <= n <= last:
        continue
    cast = p["cast"]
    identities = " ".join(
        f"{canon['characters'][key]['name']}: {canon['characters'][key]['fixed_appearance']} "
        f"Clothes: {canon['characters'][key]['fixed_clothing']}"
        for key in cast
    )
    references = [str(ref_root / refs[key]) for key in cast if key in refs]
    place = canon["places"].get(p["place"], canon["school_map"].get(p["place"], ""))
    prompt = (
        f"Original illustrated medieval fantasy comic page {n}, portrait 2:3. "
        "Match the established As Estradas do Crepúsculo art: detailed painterly 2D inked comic, "
        "natural human anatomy, warm copper and indigo palette, dramatic but legible action. "
        f"Show this ONE sequential story moment precisely: {p['scene']} "
        f"Time {p['time']}. Place {p['place']}: {place} "
        f"Exactly two principal visible speakers, placed LEFT TO RIGHT in this exact order: {cast[0]}, then {cast[1]}. "
        f"Identity locks: {identities} "
        "Reference images establish face, hair, age and clothing ONLY; DO NOT repeat reference background or poses. "
        f"Page layout: {layouts[(n - 645) % len(layouts)]} "
        "Reserve the UPPER 28 PERCENT as quiet architecture, sky or dark unimportant wall for TWO later web speech balloons. "
        "Place BOTH speaker heads entirely BELOW the upper 36 percent, faces approximately at left 25 percent and right 75 percent. "
        "Keep the OUTER shoulder beside each speaker visible near mid page, and no other faces in the top half. "
        "Do not draw any text, speech balloons, letters, signage, logos or watermarks in the art. "
        "Exactly two arms and two hands per person, FIVE fingers per hand, coherent knees and necks, no mirrored or extra limbs, no duplicated people. "
        "No gore beyond minor battle cuts, no modern items, no fantasy spell from empty air. "
        "The scene may include distant anonymous workers when the story requires them, but no duplicate main characters."
    )
    out.append({"number": n, "prompt": prompt, "refs": references})
print(json.dumps(out, ensure_ascii=False))
