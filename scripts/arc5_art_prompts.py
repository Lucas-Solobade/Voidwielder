"""Print scene-specific image prompts and stable identity references as JSON."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pages = json.loads((root / "reader/medieval/arc5-605-644.json").read_text(encoding="utf-8"))["pages"]
canon = json.loads((root / "reader/medieval/canon.json").read_text(encoding="utf-8"))["characters"]
ref_root = root / "reader/medieval"
refs = {
    "ilyan": "references/ilyan-sheet.png", "runa": "references/runa-sheet.png",
    "oru": "references/oru-sheet.png", "liria": "art/page-544.png",
    "ordelia": "references/individual/ordelia.png", "eda": "references/individual/eda.png",
    "sere": "references/individual/sere.png", "caio": "references/individual/caio.png",
    "beren": "references/individual/beren.png", "talin": "references/individual/talin.png",
}
layout = [
    "one cinematic wide upper panel, a thin diagonal inset and a large lower detail panel",
    "two UNEQUAL panels: a tall action panel left and a shorter close-up panel right",
    "one main full-width scene with two small asymmetric evidence insets below",
    "one intimate full-height panel with a narrow detail inset; generous scenery visible",
    "one wide establishing panel over two unequal vertical reaction panels",
]

def character_text(key):
    entry = canon.get(key)
    if entry:
        return f"{entry['name']}: {entry.get('fixed_appearance', '')} Clothing: {entry.get('fixed_clothing', '')}"
    return {"curandeira": "One adult school healer in practical dark-blue medieval linen, no unusual marks.",
            "mensageiro": "One adult ordinary courier in brown travel coat, no magic or modern accessories.",
            "escriva-municipal": "One adult municipal woman clerk with brown braided bun and navy archive cloak."}.get(key, key)

out = []
first, last = map(int, sys.argv[1:3])
for p in pages:
    n = p["number"]
    if not first <= n <= last:
        continue
    cast = p["cast"]
    references = [str(ref_root / refs[key]) for key in cast if key in refs][:3]
    identities = " ".join(character_text(key) for key in cast)
    prompt = (
        f"Create ORIGINAL page {n} of the same medieval fantasy illustrated comic As Estradas do Crepúsculo. "
        "Portrait 2:3 page, rich hand-painted 2D graphic novel with crisp dark ink gutters, warm copper, indigo, moss, ivory; "
        "expressive credible adult faces, natural necks and hands with FIVE fingers, exactly two arms per person. "
        f"The event MUST be this exact sequential beat: {p['scene']} Time: {p['time']}. Location: {p['place']}. "
        f"Draw only these visible cast members as appropriate to that beat: {identities}. "
        "References preserve CHARACTER IDENTITIES ONLY, never copy their old scene or pose. "
        f"Panel composition: {layout[(n - 605) % len(layout)]}; vary page rhythm. "
        "KEEP THE UPPER 20% of the page as quiet visible architecture or sky, no faces or hands there, "
        "for web lettering to be added later. Put speaking faces below the upper 25% with clear separation. "
        "NO text of any kind in the generated art: NO words, letters, captions, speech balloons, "
        "blank white oval balloon shapes, labels, logos or watermarks. "
        "Avoid duplicated characters, extra limbs, impossible poses, mismatched faces, floating props, "
        "modern clothes or anachronisms. Preserve fixed room geography and the physical source of any magic."
    )
    out.append({"number": n, "prompt": prompt, "refs": references})
print(json.dumps(out, ensure_ascii=False))
