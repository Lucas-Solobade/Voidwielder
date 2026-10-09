from pathlib import Path

from django.urls import reverse

from reader.medieval_catalog import CANON, PAGES, STORY, page_art


def test_medieval_canon_and_page_sequence():
    assert [page["number"] for page in PAGES] == list(range(1, 13))
    assert all(len(page["panels"]) == 3 for page in PAGES)
    assert all(set(page["cast"]) <= set(CANON["characters"]) for page in PAGES)
    assert "avel" not in PAGES[2]["cast"] and "sere" not in PAGES[2]["cast"]
    assert {"avel", "sere"} <= set(PAGES[4]["cast"])
    assert set(PAGES[10]["cast"]) == {"ilyan", "bram"}
    assert "mira" not in {character for page in PAGES for character in page["cast"]}
    assert STORY["arc"]["status"] == "Em andamento"


def test_medieval_art_is_published_for_every_page():
    static_dir = Path(__file__).resolve().parents[1] / "static"
    assert (static_dir / STORY["cover"]).is_file()
    for page in PAGES:
        assert (static_dir / page_art(page["number"])).is_file()


def test_medieval_catalog_shows_series_and_reader_navigation(client):
    catalog = client.get(reverse("reader:search"), {"tipo": "hq"})
    assert catalog.status_code == 200
    html = catalog.content.decode()
    assert STORY["title"] in html
    assert STORY["arc"]["title"] not in html

    detail = client.get(reverse("reader:medieval_detail"))
    arc = client.get(reverse("reader:medieval_arc"))
    assert detail.status_code == arc.status_code == 200
    assert STORY["arc"]["title"] in detail.content.decode()
    assert arc.content.decode().count('class="twilight-page-card"') == 12

    first = client.get(reverse("reader:medieval_read", args=(1,)))
    last = client.get(reverse("reader:medieval_read", args=(12,)))
    assert first.status_code == last.status_code == 200
    assert first.content.decode().count('class="twilight-panel twilight-panel-') == 3
    assert 'rel="next"' in first.content.decode()
    assert 'rel="prev"' in last.content.decode()
    assert client.get(reverse("reader:medieval_read", args=(13,))).status_code == 404
