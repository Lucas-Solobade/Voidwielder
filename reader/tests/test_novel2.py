"""The new volume must be a complete readable arc with one plate per chapter."""

from pathlib import Path

from django.urls import reverse

from reader.novel2_catalog import NOVEL_II, get_novel2_pages


def test_second_volume_has_dense_sequential_pages_and_one_plate_per_chapter() -> None:
    pages = get_novel2_pages()
    assert len(pages) == NOVEL_II["page_count"] == 193
    assert [page.number for page in pages] == list(range(1, 194))
    assert all(page.paragraphs and 90 <= page.word_count <= 155 for page in pages)
    starts = [page for page in pages if page.chapter_start]
    assert [page.chapter_number for page in starts] == list(range(1, 18))
    assert all(page.illustration == f"v2-{page.chapter_number:02}" for page in starts)
    assert all(page.illustration is None for page in pages if not page.chapter_start)
    plate_dir = Path(__file__).resolve().parents[1] / "static" / "reader" / "images" / "novel"
    assert (plate_dir / "volume-2-cover.webp").is_file()
    assert all((plate_dir / f"volume-2-chapter-{number:02}.webp").is_file() for number in range(1, 18))


def test_second_volume_routes_and_first_volume_link(client) -> None:
    detail = client.get(reverse("reader:novel2_detail"))
    first = client.get(reverse("reader:read_novel2", args=(1,)))
    last = client.get(reverse("reader:read_novel2", args=(193,)))
    assert detail.status_code == first.status_code == last.status_code == 200
    assert "Volume II · Arcos 6 e 7 completos" in detail.content.decode("utf-8")
    assert "FIM DO ARCO 7" in last.content.decode("utf-8")
    assert client.get(reverse("reader:read_novel2", args=(194,))).status_code == 404
    assert reverse("reader:novel2_detail") in client.get(reverse("reader:novel_detail")).content.decode("utf-8")
