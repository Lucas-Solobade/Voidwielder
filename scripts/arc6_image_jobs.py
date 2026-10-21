"""Print focused image-generation jobs for the remaining arc-six pages."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {page["number"]: page for page in json.loads((ROOT / "reader/medieval/arc6-831-924.json").read_text(encoding="utf-8"))["pages"]}
CANON = json.loads((ROOT / "reader/medieval/canon.json").read_text(encoding="utf-8"))

LOOKS = {
    "ilyan": "young adult slim human man, warm light olive skin, beardless oval face, very long WAVY black hair, indigo vest, blunt copper-guard sword sheathed unless the scene says otherwise",
    "runa": "young adult human woman, cool fair skin, very long STRAIGHT jet black hair and straight bangs, small silver septum ring, floral tattoo only on LEFT arm, plum and charcoal medieval clothes",
    "liria": "young adult human woman, copper-olive skin, gray-green eyes, hooked nose, TWO tight dark brown braids, short chin scar, gray student coat with red stitching and brass-chained notebook",
    "sere": "young adult dark brown-skinned elf woman, amber eyes, pointed ears, ONE long thick silver-white braid, dark forest-green cloak and ash recurve bow",
    "tovo": "tall broad young half-orc man, sage-green skin, short tightly curled brown hair, small lower tusks, warm brown eyes",
    "caio": "slim young warm brown-skinned man, short tidy reddish-brown hair, thick straight brows, petrol-blue guard tunic",
    "beren": "58-year-old light brown-skinned mason man, short gray hair, thick gray beard, metal brace on LEFT knee, sandstone work clothes",
    "eda": "38-year-old warm brown-skinned human woman, short dark brown curls pulled back, petrol-blue surveying cloak, wooden measure staff",
    "adra": "adult orc woman, slate-green skin, two small lower tusks, black braids with shells, two joined fingers on RIGHT hand from old scar, deep blue captain's cloak",
    "ysra": "adult brown earth-skinned fae woman, wholly golden eyes, long bark-textured dark hair, TWO little living twigs at temples, moss/umber clothes",
    "talin": "adult FEMALE elf, bronze-light skin, SHORT copper-red curls, freckles, pointed ears, tiny leaf-shaped scar on RIGHT cheek, ochre cloak and ash staff",
    "neral": "adult copper-brown fae woman, long face, wholly gold eyes, short fine BLACK braids, THREE pale parallel marks on LEFT cheek, dark reed mantle, NO antlers or temple twigs",
    "hessa": "46-year-old dark olive-green orc woman, broad face, little lower tusks, black braids with silver threads, short scar above RIGHT brow, ochre shawl",
    "iri": "adult distinct fae healer woman, deep umber skin, dark eyes, long bark-black braids, two slender green twigs at temples, simple moss cloak",
    "menina_gnoma": "small CHILD gnome girl, honey-brown skin, green-blue eyes, short pointed ears, copper curls to nape, ochre tunic and small woven green apron",
    "ordelia": "older silver-gray haired stern female school headmistress in oxblood robe; keep exactly her attached reference face",
    "oru": "short elderly compact GNOME man, bald crown, ONE braided silver beard, round copper spectacles, green teaching robes",
    "teren": "middle-aged dark-skinned bald smith man, square gray beard, scarred forearm, leather forge apron",
    "curandeira": "adult brown-curly-haired female school healer, blue-gray practical healing robes",
}

REF_FALLBACK = {
    "ordelia": "reader/medieval/references/individual/ordelia.png",
    "oru": "reader/medieval/references/oru-sheet.png",
}

PLACE_REFERENCE = {
    "casa-arquivos": 831,
    "patio-central": 833,
    "patio-treino": 841,
    "enfermaria-leste": 861,
    "sala-elementos": 873,
    "forja-leste": 874,
    "portao-sul": 729,
    "barca-enseada": 791,
    "cais-porto": 795,
    "hospedaria-hessa": 797,
    "camara-contrapesos": 810,
    "passagem-entre-margens": 809,
    "entremeio-ponte": 894,
    "entremeio-muralha": 894,
    "entremeio-aldeia": 914,
}

def image_path(number):
    original = ROOT / f"reader/medieval/art/page-{number}.png"
    return original if original.exists() else ROOT / f"reader/static/reader/images/medieval/page-{number}.webp"

def job(number):
    page = PAGES[number]
    cast = page["cast"]
    primary = cast[:2]
    refs = []
    for name in primary:
        ref = CANON["references"].get(name, REF_FALLBACK.get(name))
        if ref and (ROOT / ref).exists():
            refs.append(str(ROOT / ref))
    location_ref = PLACE_REFERENCE.get(page["place"])
    if location_ref and image_path(location_ref).exists() and location_ref != number:
        refs.append(str(image_path(location_ref)))
    descriptions = "; ".join(f"{name.upper()}: {LOOKS.get(name, 'use exact fixed canon identity')}" for name in primary)
    layout = page["layout"]
    prompt = (
        f"Original painted 2D MEDIEVAL FANTASY COMIC illustration for numbered page {number}; portrait aspect 2:3, 1024x1536. "
        f"Scene/time: {page['time']}, setting {page['place']}. {page['scene']} "
        f"Foreground LEFT speaker {primary[0].upper()}, foreground RIGHT speaker {primary[1].upper()}. {descriptions}. "
        f"Use visual identity and architecture in attached references, adapting wardrobe only as story requires. "
        f"Composition: {layout}; vary panel sizes and perspective, no repeated three horizontal strips. "
        "CRITICAL LETTERING SPACE: fully ILLUSTRATED unoccupied background in top 38 percent of page, with NO human/creature heads, eyes, hands or main action there. "
        "Place primary speakers' entire heads and faces below 43 percent page height; keep left and right face clearly separated, with a short unobstructed route from each upper corner to the corresponding speaker. "
        "The dialogue balloons will be overlaid later and MUST NOT cover any face or action. Do NOT draw any text, balloon, caption, handwriting, logo, beige blank panel, wide empty strip, or labels. "
        "Both characters must have anatomically plausible necks, exactly two arms and two hands, five fingers per hand, no floating/extra limbs or duplicate faces. "
        "Illustrate only the stated physical action and source-based magic, no supernatural beams without a source. Rich painterly ink detail, elegant copper/indigo/moss/ivory palette, consistent world geography."
    )
    if number == 917:
        prompt += " For the small earlier inset, Eda and Neral are secondary and their faces also remain BELOW 43 percent; Sere and Talin dominate the lower main panel. Four-night wait before next low tide is shown by modest sequential cues, not by identical duplicate people."
    if number == 894:
        prompt += " The Entremeio is a LIVED-IN alternate arrangement of the same watery margin: inhabited woven-reed houses, suspended pools in roots and a practical reed bridge; no cosmic portal, no modern city, no random ruins."
    if 900 <= number <= 913:
        prompt += " Raspa-frio creature if present is a pale articulated plated cold predator following heat/mineral, no human face. Preserve count and action exactly as script says. The Entremeio has reed houses and ROOT BRIDGES like the location reference, plus a rough salt wall; there are NO school banners, grand cathedrals, city towers or castle skyline here."
    return {"number": number, "prompt": prompt, "refs": refs}

if __name__ == "__main__":
    print(json.dumps([job(int(x)) for x in sys.argv[1:]], ensure_ascii=False))
