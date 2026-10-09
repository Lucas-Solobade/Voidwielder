import re
from pathlib import Path

from django.urls import reverse

from reader.medieval_catalog import ARCS, CANON, PAGES, STORY, page_art


def test_medieval_canon_and_page_sequence():
    assert [page["number"] for page in PAGES] == list(range(1, 81))
    assert all(len(page["panels"]) == 3 for page in PAGES[:25])
    assert len({page["layout"] for page in PAGES[25:]}) >= 5
    assert all(set(page["cast"]) <= set(CANON["characters"]) for page in PAGES)
    assert "avel" not in PAGES[2]["cast"] and "sere" not in PAGES[2]["cast"]
    assert {"avel", "sere"} <= set(PAGES[4]["cast"])
    assert set(PAGES[10]["cast"]) == {"ilyan", "bram"}
    assert {"mira", "runa", "bram", "lumen"}.isdisjoint(
        {character for page in PAGES[12:25] for character in page["cast"]}
    )
    assert STORY["arc"]["status"] == "Concluído"
    assert ARCS[1]["status"] == "Em andamento"
    assert "porta" in PAGES[24]["title"].lower()
    assert "vestibule" in PAGES[25]["scene"].lower()
    assert "cart" in PAGES[31]["scene"].lower()
    assert all("nima" not in page["cast"] for page in PAGES[32:])
    assert all(page["place"] in CANON["school_map"] for page in PAGES[25:])
    assert [int(re.search(r"Dia (\d+)", page["time"]).group(1)) for page in PAGES[25:]] == sorted(
        int(re.search(r"Dia (\d+)", page["time"]).group(1)) for page in PAGES[25:]
    )
    assert [number for chapter in ARCS[1]["chapters"] for number in range(chapter["start"], chapter["end"] + 1)] == list(range(26, 81))
    assert "runa" not in PAGES[33]["cast"]
    assert "runa" in PAGES[34]["cast"]
    assert all(
        line.get("balloon") or line["speaker"] == "Narração"
        for page in PAGES[12:25]
        for panel in page["panels"]
        for line in panel["lines"]
    )
    assert all(
        line["speaker"] in ({CANON["characters"][name]["name"] for name in page["cast"]} | ({"Avel"} if "avel" in page["cast"] else set()))
        and 0 <= line["balloon"]["x"] <= 100 - line["balloon"]["w"]
        and 0 <= line["balloon"]["y"] <= 90
        and 0 <= line["balloon"]["target_x"] <= 100
        and 0 <= line["balloon"]["target_y"] <= 100
        for page in PAGES[25:] for line in page["lines"]
    )


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
    arc2 = client.get(reverse("reader:medieval_arc2"))
    assert detail.status_code == arc.status_code == arc2.status_code == 200
    assert STORY["arc"]["title"] in detail.content.decode()
    assert ARCS[1]["title"] in detail.content.decode()
    assert arc.content.decode().count('class="twilight-page-card"') == 25
    assert arc2.content.decode().count('class="twilight-page-card"') == 55

    first = client.get(reverse("reader:medieval_read", args=(1,)))
    last = client.get(reverse("reader:medieval_read", args=(80,)))
    assert first.status_code == last.status_code == 200
    assert first.content.decode().count('class="twilight-panel twilight-panel-') == 3
    assert 'rel="next"' in first.content.decode()
    assert 'rel="prev"' in last.content.decode()
    assert 'class="twilight-speech"' in client.get(
        reverse("reader:medieval_read", args=(13,))
    ).content.decode()
    transition = client.get(reverse("reader:medieval_read", args=(25,))).content.decode()
    assert 'rel="next"' in transition
    assert 'class="twilight-page-scroll"' in client.get(reverse("reader:medieval_read", args=(26,))).content.decode()
    assert client.get(reverse("reader:medieval_read", args=(81,))).status_code == 404
