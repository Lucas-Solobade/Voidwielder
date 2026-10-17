"""Guard the published manuscript's pagination and chronology."""

from pathlib import Path

from django.urls import reverse

from reader.novel_catalog import CHAPTER_DIR, NOVEL, get_novel_pages


def test_novel_pages_are_real_and_contiguous() -> None:
    pages = get_novel_pages()
    assert len(pages) == NOVEL["page_count"] == 720
    assert [page.number for page in pages] == list(range(1, 721))
    assert all(page.paragraphs and 42 <= page.word_count <= 155 for page in pages)
    assert len([page for page in pages if page.illustration]) == 36
    assert [page.number for page in pages if page.chapter_start] == list(range(1, 721, 20))
    assert all(page.illustration is None or page.chapter_start for page in pages)
    assert all(page.word_count >= 75 for page in pages if page.chapter_number >= 21)
    manuscript = "\n".join(path.read_text(encoding="utf-8") for path in sorted(CHAPTER_DIR.glob("*.md")))
    rendered = " ".join(paragraph for page in pages for paragraph in page.paragraphs)
    assert "quatro espelhos" in rendered.casefold()
    opening = "\n".join((CHAPTER_DIR / f"{chapter:02}.md").read_text(encoding="utf-8") for chapter in range(1, 7))
    assert "Runa" not in opening  # She first arrives on day 5, after the first part ends.
    assert "Runa" in manuscript


def test_novel_has_chapter_plates() -> None:
    plate_dir = Path(__file__).resolve().parents[1] / "static" / "reader" / "images" / "novel"
    assert (plate_dir / "cover.webp").is_file()
    for chapter in range(1, 37):
        assert (plate_dir / f"chapter-{chapter:02}.webp").is_file()
    assert [page.chapter_number for page in get_novel_pages() if page.illustration] == list(range(1, 37))


def test_novel_routes_and_catalog(client) -> None:
    assert client.get(reverse("reader:novel_detail")).status_code == 200
    first = client.get(reverse("reader:read_novel", args=(1,)))
    last = client.get(reverse("reader:read_novel", args=(720,)))
    assert first.status_code == last.status_code == 200
    assert "CONTINUA" in last.content.decode("utf-8")
    assert client.get(reverse("reader:read_novel", args=(721,))).status_code == 404
    assert "As Estradas do Crepúsculo" in client.get("/buscar/?tipo=livros").content.decode("utf-8")
