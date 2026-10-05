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

from reader.book_catalog import BOOK, get_book_pages  # noqa: E402
from reader.catalog import ARCS, MANGA  # noqa: E402
from reader.game_catalog import GAMES  # noqa: E402
from reader.linux_catalog import LINUX_BOOK, get_linux_pages  # noqa: E402
from reader.python_catalog import PYTHON_BOOK, get_python_pages  # noqa: E402
from reader.python_exercises import EXERCISES  # noqa: E402
from reader.study_catalog import STUDY_GUIDE  # noqa: E402

DIST_DIR = BASE_DIR / "dist"
STATIC_SOURCE = BASE_DIR / "reader" / "static" / "reader"


def write_book_data() -> Path:
    destination = STATIC_SOURCE / "book" / "casa-medidas" / "pages.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps([page.as_json() for page in get_book_pages()], ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return destination


def write_linux_data() -> Path:
    destination = STATIC_SOURCE / "book" / "linux" / "pages.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps([page.as_json() for page in get_linux_pages()], ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return destination


def write_python_data() -> tuple[Path, Path]:
    directory = STATIC_SOURCE / "book" / "python"
    directory.mkdir(parents=True, exist_ok=True)
    pages = directory / "pages.json"
    exercises = directory / "exercises.json"
    pages.write_text(json.dumps([page.as_json() for page in get_python_pages()], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    exercises.write_text(json.dumps([exercise.as_json() for exercise in EXERCISES], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return pages, exercises


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
    origin = os.getenv("SITE_ORIGIN", "https://voidwielder.alves-lucas0200.chatgpt.site").rstrip("/")
    html = html.replace(f"http://testserver{path}", f"{origin}{path}")
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    destination = destination_for(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8")


def build_catalog() -> list[dict[str, str | int]]:
    return [{
        "category": "livros", "kind": "Livro", "title": BOOK["title"],
        "detail": f"{BOOK['author']} · {BOOK['genre']} · 150 páginas. {BOOK['detail']}",
        "url": BOOK["url"], "topics": BOOK["topics"], "book_art": True,
    }, {
        "category": "livros", "kind": "Livro didático", "title": LINUX_BOOK["title"],
        "detail": f"13 partes · 78 lições · {LINUX_BOOK['page_count']} páginas. {LINUX_BOOK['detail']}",
        "url": LINUX_BOOK["url"], "topics": LINUX_BOOK["topics"], "linux_art": True,
    }, {
        "category": "livros", "kind": "Livro didático", "title": PYTHON_BOOK["title"],
        "detail": f"13 partes · 39 lições · 39 desafios · {PYTHON_BOOK['page_count']} páginas. {PYTHON_BOOK['detail']}",
        "url": PYTHON_BOOK["url"], "topics": PYTHON_BOOK["topics"], "python_art": True,
    }, {
        "category": "hq",
        "kind": "HQ",
        "title": MANGA["title"],
        "detail": MANGA["description"],
        "url": "/hqs/homus-bananus/",
        "cover": MANGA["cover"],
    }] + [
        {
            "category": "hq",
            "kind": "Arco",
            "title": arc.title,
            "detail": arc.description,
            "url": f"/arcos/{arc.slug}/",
        }
        for arc in ARCS
    ] + [
        {
            "category": "hq",
            "kind": "Capítulo",
            "title": chapter.title,
            "detail": chapter.subtitle,
            "url": f"/ler/arco/{arc.slug}/#capitulo-{chapter.number}",
            "number": chapter.number,
        }
        for arc in ARCS
        for chapter in arc.chapters
    ] + [
        {
            "category": "estudos",
            "kind": "Trilha de estudos",
            "title": STUDY_GUIDE["title"],
            "detail": STUDY_GUIDE["detail"],
            "url": "/estudos/",
            "topics": " ".join(STUDY_GUIDE["topics"]),
        }
    ] + [
        {
            "category": "jogos",
            "kind": "Jogo",
            **game,
        }
        for game in GAMES
    ]


def main() -> None:
    write_book_data()
    write_linux_data()
    write_python_data()
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    DIST_DIR.mkdir()
    shutil.copytree(
        STATIC_SOURCE, DIST_DIR / "static" / "reader", ignore=shutil.ignore_patterns("*.png")
    )

    client = Client()
    routes = ["/", "/buscar/", "/estudos/", "/hqs/homus-bananus/"]
    routes.append(BOOK["url"])
    routes.extend(f"{BOOK['url']}ler/{page}/" for page in range(1, 151))
    routes.append(LINUX_BOOK["url"])
    routes.extend(f"{LINUX_BOOK['url']}ler/{page}/" for page in range(1, LINUX_BOOK["page_count"] + 1))
    routes.append(PYTHON_BOOK["url"])
    routes.extend(f"{PYTHON_BOOK['url']}ler/{page}/" for page in range(1, PYTHON_BOOK["page_count"] + 1))
    routes.extend(game["url"] for game in GAMES)
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
    origin = os.getenv("SITE_ORIGIN", "https://voidwielder.alves-lucas0200.chatgpt.site").rstrip("/")
    (DIST_DIR / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{origin}{route}</loc></url>" for route in routes)
        + "</urlset>",
        encoding="utf-8",
    )


def book_only() -> None:
    """Publish the book without rebuilding unrelated, hand-tuned static pages."""
    data = write_book_data()
    for source in (
        STATIC_SOURCE / "css" / "book.css",
        STATIC_SOURCE / "js" / "book" / "art.mjs",
        STATIC_SOURCE / "js" / "book" / "reader.mjs",
        data,
    ):
        destination = DIST_DIR / "static" / "reader" / source.relative_to(STATIC_SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    client = Client()
    write_page(client, BOOK["url"])
    for page in get_book_pages():
        write_page(client, f"{BOOK['url']}ler/{page.number}/")
    (DIST_DIR / "catalog.json").write_text(
        json.dumps(build_catalog(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    search_path = DIST_DIR / "buscar" / "index.html"
    search_html = search_path.read_text(encoding="utf-8")
    if "reader/css/book.css" not in search_html:
        search_html = search_html.replace(
            "</head>", '<link rel="stylesheet" href="/static/reader/css/book.css?v=1"></head>', 1
        )
    if "reader/js/book/art.mjs" not in search_html:
        search_html = search_html.replace(
            "</body>", '<script type="module" src="/static/reader/js/book/art.mjs?v=1"></script></body>', 1
        )
    search_path.write_text(search_html, encoding="utf-8")
    sitemap_path = DIST_DIR / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    origin = os.getenv("SITE_ORIGIN", "https://voidwielder.alves-lucas0200.chatgpt.site").rstrip("/")
    book_urls = [BOOK["url"]] + [f"{BOOK['url']}ler/{page.number}/" for page in get_book_pages()]
    if f"{origin}{BOOK['url']}" not in sitemap:
        sitemap = sitemap.replace("</urlset>", "".join(f"<url><loc>{origin}{url}</loc></url>" for url in book_urls) + "</urlset>")
        sitemap_path.write_text(sitemap, encoding="utf-8")


def linux_only() -> None:
    """Export the textbook while preserving unrelated hand-tuned static pages."""
    data = write_linux_data()
    for source in (
        STATIC_SOURCE / "css" / "linux-book.css",
        STATIC_SOURCE / "js" / "linux-book" / "art.mjs",
        STATIC_SOURCE / "js" / "linux-book" / "reader.mjs",
        STATIC_SOURCE / "js" / "site.js",
        data,
    ):
        destination = DIST_DIR / "static" / "reader" / source.relative_to(STATIC_SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    client = Client()
    write_page(client, LINUX_BOOK["url"])
    for page in get_linux_pages():
        write_page(client, f"{LINUX_BOOK['url']}ler/{page.number}/")
    (DIST_DIR / "catalog.json").write_text(
        json.dumps(build_catalog(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    search_path = DIST_DIR / "buscar" / "index.html"
    search_html = search_path.read_text(encoding="utf-8")
    if "reader/css/linux-book.css" not in search_html:
        search_html = search_html.replace(
            "</head>", '<link rel="stylesheet" href="/static/reader/css/linux-book.css?v=1"></head>', 1
        )
    if "reader/js/linux-book/art.mjs" not in search_html:
        search_html = search_html.replace(
            "</body>", '<script type="module" src="/static/reader/js/linux-book/art.mjs?v=1"></script></body>', 1
        )
    search_path.write_text(search_html, encoding="utf-8")
    sitemap_path = DIST_DIR / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    origin = os.getenv("SITE_ORIGIN", "https://voidwielder.alves-lucas0200.chatgpt.site").rstrip("/")
    book_urls = [LINUX_BOOK["url"]] + [f"{LINUX_BOOK['url']}ler/{page.number}/" for page in get_linux_pages()]
    if f"{origin}{LINUX_BOOK['url']}" not in sitemap:
        sitemap = sitemap.replace(
            "</urlset>", "".join(f"<url><loc>{origin}{url}</loc></url>" for url in book_urls) + "</urlset>"
        )
        sitemap_path.write_text(sitemap, encoding="utf-8")


def python_only() -> None:
    """Publish the Python book while preserving the existing site export."""
    data = write_python_data()
    for source in (
        STATIC_SOURCE / "css" / "python-book.css",
        STATIC_SOURCE / "js" / "python-book" / "art.mjs",
        STATIC_SOURCE / "js" / "python-book" / "reader.mjs",
        STATIC_SOURCE / "js" / "python-book" / "worker.mjs",
        STATIC_SOURCE / "js" / "site.js",
        *data,
    ):
        destination = DIST_DIR / "static" / "reader" / source.relative_to(STATIC_SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    client = Client()
    write_page(client, PYTHON_BOOK["url"])
    for page in get_python_pages():
        write_page(client, f"{PYTHON_BOOK['url']}ler/{page.number}/")
    (DIST_DIR / "catalog.json").write_text(
        json.dumps(build_catalog(), ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    search_path = DIST_DIR / "buscar" / "index.html"
    search_html = search_path.read_text(encoding="utf-8")
    if "reader/css/python-book.css" not in search_html:
        search_html = search_html.replace("</head>", '<link rel="stylesheet" href="/static/reader/css/python-book.css?v=1"></head>', 1)
    if "reader/js/python-book/art.mjs" not in search_html:
        search_html = search_html.replace("</body>", '<script type="module" src="/static/reader/js/python-book/art.mjs?v=1"></script></body>', 1)
    search_path.write_text(search_html, encoding="utf-8")
    sitemap_path = DIST_DIR / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    origin = os.getenv("SITE_ORIGIN", "https://voidwielder.alves-lucas0200.chatgpt.site").rstrip("/")
    book_urls = [PYTHON_BOOK["url"]] + [f"{PYTHON_BOOK['url']}ler/{page.number}/" for page in get_python_pages()]
    if f"{origin}{PYTHON_BOOK['url']}" not in sitemap:
        sitemap = sitemap.replace("</urlset>", "".join(f"<url><loc>{origin}{url}</loc></url>" for url in book_urls) + "</urlset>")
        sitemap_path.write_text(sitemap, encoding="utf-8")


if __name__ == "__main__":
    if "--book-only" in sys.argv:
        book_only()
    elif "--linux-only" in sys.argv:
        linux_only()
    elif "--python-only" in sys.argv:
        python_only()
    else:
        main()
