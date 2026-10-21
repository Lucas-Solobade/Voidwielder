"""Check structural continuity and asset completeness before publishing arc-six pages."""

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def validate(allow_missing_art: bool) -> list[str]:
    canon = json.loads((ROOT / "reader/medieval/canon.json").read_text(encoding="utf-8"))
    segment = json.loads((ROOT / "reader/medieval/arc6-831-924.json").read_text(encoding="utf-8"))
    characters = canon["characters"]
    pages = segment["pages"]
    errors: list[str] = []
    numbers = [page["number"] for page in pages]
    if numbers != list(range(831, 925)):
        errors.append("Page numbers must be exactly 831–924 in sequence")

    for page in pages:
        number = page["number"]
        cast = page["cast"]
        if len(cast) != len(set(cast)):
            errors.append(f"{number}: duplicate cast ID")
        for person in cast:
            if person not in characters:
                errors.append(f"{number}: missing canon entry for {person}")
        if len(page["lines"]) != 2:
            errors.append(f"{number}: expected two short spoken lines")
            continue
        for index, line in enumerate(page["lines"]):
            matching = [key for key in cast if characters[key]["name"].casefold() == line["speaker"].casefold()]
            if not matching:
                errors.append(f"{number}: speaker {line['speaker']} is absent from visible cast")
            balloon = line["balloon"]
            for key in ("x", "y", "w", "target_x", "target_y"):
                if not 0 <= balloon[key] <= 100:
                    errors.append(f"{number}: balloon {index + 1} {key} outside page")
            if balloon["x"] + balloon["w"] > 97:
                errors.append(f"{number}: balloon {index + 1} exits right edge")
            if index == 0 and balloon["x"] >= 50:
                errors.append(f"{number}: first speaker is not placed on left")
            if index == 1 and balloon["x"] < 50:
                errors.append(f"{number}: second speaker is not placed on right")
            if balloon["kind"] not in {"normal", "shout", "thought", "whisper"}:
                errors.append(f"{number}: unknown balloon kind")
        if page["novel_volume"] != 2:
            errors.append(f"{number}: unexpected novel volume")

        png = ROOT / f"reader/medieval/art/page-{number}.png"
        webp = ROOT / f"reader/static/reader/images/medieval/page-{number}.webp"
        for path in (png, webp):
            if not path.exists():
                if not allow_missing_art:
                    errors.append(f"{number}: missing {path.relative_to(ROOT)}")
                continue
            try:
                with Image.open(path) as image:
                    if image.size != (1024, 1536):
                        errors.append(f"{number}: unexpected size {image.size} in {path.suffix}")
                    image.verify()
            except Exception as exc:
                errors.append(f"{number}: unreadable {path.suffix}: {exc}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing-art", action="store_true")
    args = parser.parse_args()
    issues = validate(args.allow_missing_art)
    for issue in issues:
        print(issue)
    if issues:
        raise SystemExit(1)
    print("94 pages validated; character attribution, balloons and available assets are consistent.")
