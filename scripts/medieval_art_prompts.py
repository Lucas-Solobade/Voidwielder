"""Build identity-locked image prompts for arc two, one finished page at a time."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BASE = ROOT / "reader" / "medieval"
REF = BASE / "references"
ART = BASE / "art"
CHARACTER_ANCHORS = {
    "avel": 28,
    "sere": 31,
    "ordelia": 34,
    "caio": 36,
    "tovo": 39,
    "teren": 40,
    "beren": 73,
}
IDENTITIES = {
    "ilyan": "Ilyan: 17-year-old clean-shaven teen, very long WAVY center-part black hair, indigo vest and blunt short sword",
    "nima": "Nima: adult very short gnome with copper curly bob, green cap, brass goggles, teal vest, NOT a child",
    "avel": "Avel: mature dark-skinned woman, silver-white braids HIGH BUN, navy robe with moon phases",
    "sere": "Sere: dark-skinned elf archer, ONE long silver braid, moss green cloak",
    "runa": "Runa: 17-year-old woman with very long STRAIGHT black hair and blunt bangs, silver septum, floral tattoos LEFT ARM, plum medieval dress",
    "caio": "Caio: 18-year-old tan male with SHORT auburn hair, teal guard tunic",
    "tovo": "Tovo: broad young HALF-ORC, sage green skin, short tight brown curls, tiny tusks, amber kitchen apron over blue tunic",
    "ordelia": "Ordelia: older olive-skinned woman with iron-gray LOW BRAID, maroon registrar gown and keys",
    "teren": "Teren: bald dark-skinned mature smith with square gray beard and dark leather apron",
    "beren": "Beren: gray-bearded pale-brown-skinned mason, one LEFT metal knee brace, sandstone work clothes",
}

LAYOUTS = {
    "splash": "ONE dominant full-page cinematic illustration with only a tiny inset detail if needed; do not divide into three equal bands",
    "duo": "TWO distinctly unequal comic panels, a large scene and a smaller reaction/detail, clear reading order",
    "asymmetric": "ASYMMETRIC comic page with one large scene and two small offset detail insets; no equal horizontal bands",
    "vertical": "VERTICAL editorial composition: one tall dramatic panel beside two smaller panels, clear reading order",
    "triptych": "THREE unequal panels with varied widths/heights and a dynamic focal panel, never three equal horizontal strips",
    "wide": "one extra-WIDE establishing panel with one slim action/reaction inset, generous architectural view",
}

LOCATION_ANCHORS = {
    "anexo-agrimensores": 26,
    "secretaria": 30,
    "patio-central": 33,
    "sala-ritmos": 36,
    "patio-treino": 38,
    "forja-leste": 40,
    "refeitorio": 42,
    "biblioteca-galeria": 46,
    "anexo-exterior": 68,
}
LOCATION_LOCKS = {
    "secretaria": "Registry room: copper lamps, exactly three ledgers, east-facing counter, carved stone arch to courtyard.",
    "patio-central": "Central courtyard: circular reflecting pool, four limestone paths, south gate, east training yard, north refectory and library towers.",
    "sala-ritmos": "Four Rhythms classroom: oak WEST door, high NORTH windows, charcoal EAST slate with four routes, TWO rows of benches.",
    "patio-treino": "East training yard: chalk circle CENTER, archery targets beyond NORTH fence, equipment rack SOUTH.",
    "forja-leste": "East school forge: brick EAST furnace, WEST water trough, exactly THREE anvils aligned north to south.",
    "refeitorio": "North refectory: long east-west oak tables and the fixed FOUR moon-phase mural on its WEST wall.",
    "biblioteca-galeria": "Upper library gallery: barred archive door WEST, map cabinets SOUTH, spiral staircase NORTHEAST.",
    "anexo-exterior": "Outside west campus wall at old surveyors' annex: FOUR copper mirrors and a PHYSICAL locked oak door; maintain the same foundation stones.",
}


def job(page: dict) -> dict:
    number = page["number"]
    time = page["time"]
    place = page["place"]
    layout = page["layout"]
    cast = page["cast"]
    scene = page["scene"]
    spoken = [(line["speaker"], line["text"]) for line in page["lines"]]
    refs = [REF / "ilyan-sheet.png"]
    if "runa" in cast:
        refs.append(REF / "runa-sheet.png")
    if "nima" in cast:
        refs.append(REF / "travelers-sheet.png")
    for person in cast:
        anchor = CHARACTER_ANCHORS.get(person)
        if anchor and anchor < number and (ART / f"page-{anchor:02}.png").exists():
            refs.append(ART / f"page-{anchor:02}.png")
        elif person in ("caio", "tovo", "ordelia", "teren", "beren"):
            refs.append(REF / "school-cast-sheet.png")
    anchor = LOCATION_ANCHORS.get(place)
    if anchor and anchor < number and (ART / f"page-{anchor:02}.png").exists():
        refs.append(ART / f"page-{anchor:02}.png")
    if number in (29, 68) and (ART / "page-25.png").exists():
        refs.append(ART / "page-25.png")
    refs = list(dict.fromkeys(refs))
    identity_refs = [path for path in refs if path.name in {"ilyan-sheet.png", "runa-sheet.png"}]
    other_refs = [path for path in refs if path not in identity_refs]
    refs = identity_refs + other_refs[-(5 - len(identity_refs)) :]
    names = ", ".join(speaker for speaker, _ in spoken)
    identity = "; ".join(IDENTITIES[person] for person in cast if person in IDENTITIES)
    location = LOCATION_LOCKS.get(place, "")
    absence = "Nima has already left; NO red-haired gnome appears in this scene. " if number >= 33 else ""
    prompt = (
        f"Original medieval fantasy graphic novel, As Estradas do Crepúsculo, PAGE {number}, {time}. "
        f"Create a complete VERTICAL 2:3 comic page, not a character sheet. {LAYOUTS[layout]}. "
        f"Exact scene and action: {scene} "
        f"Fixed location geometry: {location} "
        f"Characters physically in scene only as described: {identity}. Visual identity locked to attached sheets. "
        f"The dialogue speakers in reading order are {names}; depict each speaking character in the scene, "
        "leave SMALL natural patches of unobstructed sky, wall or parchment near upper-left and right/mid panel "
        "for later compact HTML speech balloons; keep all faces and hands unobscured. "
        "Medieval architecture and clothing, lush beautiful scenery, precise hand ink linework and painterly "
        "warm copper, indigo, moss, ivory colors; dramatic expressive acting and distinctive art direction. "
        "NO text, NO letters, NO speech balloons, NO captions, NO watermark. "
        "Within each panel show each person exactly ONCE, no accidental character clones, doubled faces, extra limbs, or random new cast. "
        f"{absence}"
        "A character may recur in a different panel only when it is a clear sequential moment. "
        "Honor the exact room features of a supplied previous location image, including doors, windows and furniture."
    )
    return {"number": number, "prompt": prompt, "refs": [str(path) for path in refs]}


if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    pages = json.loads((BASE / "arc2.json").read_text(encoding="utf-8"))["pages"]
    for page in pages:
        if start <= page["number"] <= end:
            print(json.dumps(job(page), ensure_ascii=False))
