"""Encode approved comic artwork for the public static site."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "reader" / "medieval" / "art"
DESTINATION = ROOT / "reader" / "static" / "reader" / "images" / "medieval"


def build() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for name in (f"page-{number:02}" for number in range(13, 26)):
        source = SOURCE / f"{name}.png"
        if not source.is_file():
            raise FileNotFoundError(f"Arte aprovada ausente: {source}")
        with Image.open(source) as artwork:
            artwork.convert("RGB").save(
                DESTINATION / f"{name}.webp", "WEBP", quality=86, method=6
            )


if __name__ == "__main__":
    build()
