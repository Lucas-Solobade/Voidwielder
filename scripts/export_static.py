"""Export the read-only Django catalogue to a deployable static site."""

import json
import os
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.test import Client  # noqa: E402

from reader.catalog import ARCS  # noqa: E402

DIST_DIR = BASE_DIR / "dist"
STATIC_SOURCE = BASE_DIR / "reader" / "static" / "reader"


def destination_for(path: str) -> Path:
    if path == "/":
        return DIST_DIR / "index.html"
    return DIST_DIR / path.strip("/") / "index.html"


def write_page(client: Client, path: str) -> None:
    response = client.get(path)
    if response.status_code != 200:
        raise RuntimeError(f"Could not export {path}: HTTP {response.status_code}")
    html = response.content.decode("utf-8").replace(
        '<html lang="pt-BR">', '<html lang="pt-BR" data-static-export>'
    )
    destination = destination_for(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")


def build_catalog() -> list[dict[str, str | int]]:
    return [
        {
            "kind": "Arco",
            "title": arc.title,
            "detail": arc.description,
            "url": f"/arcos/{arc.slug}/",
        }
        for arc in ARCS
    ] + [
        {
            "kind": "Capítulo",
            "title": chapter.title,
            "detail": chapter.subtitle,
            "url": f"/ler/arco/{arc.slug}/#capitulo-{chapter.number}",
            "number": chapter.number,
        }
        for arc in ARCS
        for chapter in arc.chapters
    ]


def main() -> None:
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    DIST_DIR.mkdir()
    shutil.copytree(
        STATIC_SOURCE, DIST_DIR / "static" / "reader", ignore=shutil.ignore_patterns("*.png")
    )

    client = Client()
    routes = ["/", "/buscar/"]
    routes.extend(f"/arcos/{arc.slug}/" for arc in ARCS)
    routes.extend(f"/ler/arco/{arc.slug}/" for arc in ARCS)
    routes.extend(
        f"/ler/{arc.slug}/{page}/"
        for arc in ARCS
        for page in range(arc.start_page, arc.end_page + 1)
    )
    for route in routes:
        write_page(client, route)

    (DIST_DIR / "catalog.json").write_text(
        json.dumps(build_catalog(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    (DIST_DIR / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", encoding="utf-8"
    )
    origin = os.getenv("SITE_ORIGIN", "https://example.invalid").rstrip("/")
    (DIST_DIR / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{origin}{route}</loc></url>" for route in routes)
        + "</urlset>",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
