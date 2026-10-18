import re
from hashlib import sha256
from pathlib import Path

from django.urls import reverse

from reader.medieval_catalog import ARCS, CANON, PAGES, STORY, page_art


def test_medieval_canon_and_page_sequence():
    assert [page["number"] for page in PAGES] == list(range(1, 729))
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
    assert ARCS[1]["status"] == "Concluído"
    assert ARCS[1]["end"] == 171
    assert ARCS[2]["start"] == 172
    assert ARCS[2]["status"] == "Concluído"
    assert ARCS[3]["start"] == 356
    assert ARCS[3]["end"] == 518
    assert ARCS[3]["status"] == "Concluído"
    assert ARCS[4]["start"] == 519
    assert ARCS[4]["end"] == 728
    assert ARCS[4]["status"] == "Concluído"
    assert "porta" in PAGES[24]["title"].lower()
    assert "vestibule" in PAGES[25]["scene"].lower()
    assert "cart" in PAGES[31]["scene"].lower()
    assert [page["number"] for page in PAGES[32:] if "nima" in page["cast"]] == [383, 384, 388, 389, 396]
    assert all(
        page["place"] == "pedra-mansa" or "pedra-mansa" in page.get("places", [])
        for page in PAGES if "nima" in page["cast"] and page["number"] > 32
    )
    assert PAGES[383]["time"] == "Dia 250–255 · cinco dias de estrada"
    assert PAGES[383]["places"] == ["pedra-mansa", "casa-das-quatro-luas"]
    assert all(page["place"] in (CANON["school_map"] | CANON["places"]) for page in PAGES[25:])
    assert [int(re.search(r"Dia (\d+)", page["time"]).group(1)) for page in PAGES[25:]] == sorted(
        int(re.search(r"Dia (\d+)", page["time"]).group(1)) for page in PAGES[25:]
    )
    assert [number for chapter in ARCS[1]["chapters"] for number in range(chapter["start"], chapter["end"] + 1)] == list(range(26, 172))
    assert [number for chapter in ARCS[2]["chapters"] for number in range(chapter["start"], chapter["end"] + 1)] == list(range(172, 356))
    assert [number for chapter in ARCS[3]["chapters"] for number in range(chapter["start"], chapter["end"] + 1)] == list(range(356, 519))
    assert [number for chapter in ARCS[4]["chapters"] for number in range(chapter["start"], chapter["end"] + 1)] == list(range(519, 729))
    assert "Dia 50" in PAGES[171]["time"] and "Dia 72" in PAGES[354]["time"]
    assert "Dia 73" in PAGES[355]["time"] and "Dia 480" in PAGES[-1]["time"]
    assert PAGES[178]["title"] == "A licença tem limites"
    assert PAGES[188]["title"] == "A armadilha fica"
    assert PAGES[189]["title"] == "O ferro embrulhado"
    assert PAGES[249]["title"] == "A direção que falta"
    assert PAGES[267]["title"] == "O som que não devia voltar"
    assert "daro" in CANON["characters"] and "talin" in CANON["characters"]
    assert all("nima" not in page["cast"] for page in PAGES[189:382])
    assert "cervo-de-casca" in CANON["creatures"]
    assert "runa" not in PAGES[33]["cast"]
    assert "runa" in PAGES[34]["cast"]
    assert all(
        line.get("balloon") or line["speaker"] == "Narração"
        for page in PAGES[12:25]
        for panel in page["panels"]
        for line in panel["lines"]
    )
    assert all(
        line["speaker"] in ({CANON["characters"][name]["name"] for name in page["cast"]} | {"Avel", "Estudante", "Curandeira"})
        and 0 <= line["balloon"]["x"] <= 100 - line["balloon"]["w"]
        and 0 <= line["balloon"]["y"] <= 96
        and 0 <= line["balloon"]["target_x"] <= 100
        and 0 <= line["balloon"]["target_y"] <= 100
        and line["balloon"].get("kind", "normal") in {"normal", "shout", "thought", "whisper"}
        for page in PAGES[25:] for line in page["lines"]
    )
    assert all(
        line["balloon"]["y"] + (10 if page["number"] < 269 else 6) <= line["balloon"]["target_y"]
        for page in PAGES[189:311]
        for line in page["lines"]
    )


def test_medieval_art_is_published_for_every_page():
    static_dir = Path(__file__).resolve().parents[1] / "static"
    assert (static_dir / STORY["cover"]).is_file()
    for page in PAGES:
        assert (static_dir / page_art(page["number"])).is_file()
    assert (static_dir / ARCS[2]["art"]).is_file()
    assert (static_dir / ARCS[3]["art"]).is_file()
    assert (static_dir / ARCS[4]["art"]).is_file()


def test_bosque_journey_keeps_permissions_and_travel_order(client):
    by_number = {page["number"]: page for page in PAGES}
    assert [by_number[number]["novel_chapter"] for number in range(421, 436)] == [29] * 15
    assert "talin" not in by_number[429]["cast"]
    assert "talin" in by_number[430]["cast"]
    assert "ysra" not in by_number[431]["cast"]
    assert "ysra" in by_number[432]["cast"]
    assert by_number[428]["place"] == "portao-sul"
    assert by_number[429]["place"] == "balsa-do-sal"
    assert by_number[430]["place"] == "escada-de-ambar"
    assert by_number[434]["place"] == by_number[435]["place"] == "pedra-medicao-vidraca"
    assert all("nima" not in by_number[number]["cast"] for number in range(421, 436))
    assert "page-384.webp?v=cart-pose-3" in client.get(
        reverse("reader:medieval_read", args=(384,))
    ).content.decode()


def test_bosque_return_follows_repair_and_public_records():
    pages = {page["number"]: page for page in PAGES}
    assert [pages[number]["novel_chapter"] for number in range(436, 450)] == [29] * 14
    assert pages[450]["novel_chapter"] == 30
    assert pages[438]["place"] == pages[440]["place"] == "bosque-vidraca"
    assert pages[441]["place"] == "posto-guardioes-ambar"
    assert pages[445]["place"] == "enseada-das-conchas"
    assert pages[448]["place"] == "balsa-do-sal"
    assert pages[449]["place"] == "casa-das-quatro-luas"
    assert pages[450]["place"] == "valecobre"
    assert all("nima" not in pages[number]["cast"] for number in range(436, 451))
    assert all("ysra" not in pages[number]["cast"] for number in range(444, 451))
    assert all(page["lines"] or page.get("narration") for page in (pages[n] for n in range(436, 451)))


def test_page_384_keeps_the_corrected_cart_pose(client):
    art = Path(__file__).resolve().parents[1] / "static" / page_art(384)
    assert sha256(art.read_bytes()).hexdigest() == "b505e7940c7e006f444fd2d3223e6b8effb6916c80ce9bacbd177f6777f535cd"
    html = client.get(reverse("reader:medieval_read", args=(384,))).content.decode()
    assert "page-384.webp?v=cart-pose-3" in html


def test_page_32_keeps_corrected_nima_art(client):
    art = Path(__file__).resolve().parents[1] / "static" / page_art(32)
    assert sha256(art.read_bytes()).hexdigest() == "c0f1b0118cbfb79b2ecd1e27732ab42a7ecb767f235f9a0d49c6a2fbcf2f8f44"
    html = client.get(reverse("reader:medieval_read", args=(32,))).content.decode()
    assert "page-32.webp?v=anatomy-2" in html


def test_page_114_keeps_corrected_runa_hand(client):
    art = Path(__file__).resolve().parents[1] / "static" / page_art(114)
    assert sha256(art.read_bytes()).hexdigest() == "dd6ab185520878a1f5b66562afbdd181f96ca152d686f73c929f68fa23652dea"
    html = client.get(reverse("reader:medieval_read", args=(114,))).content.decode()
    assert "page-114.webp?v=hand-2" in html


def test_arc_five_anatomy_repairs_and_ilyan_balloon_are_kept(client):
    static = Path(__file__).resolve().parents[1] / "static"
    expected = {
        535: "bf6c3f52ebb9afb7b4e52b118e92648f7dbdbb5d0326db1f3a1a089a2de01082",
        540: "db8a6ae338a3e2256337cb91a6335e72d715d66d4ad7182d342587f1aa466257",
        542: "2c30d846a5f04c6d80baa60c6e443176ec63d6045acb3f3c46560406ef09c405",
    }
    for number, digest in expected.items():
        art = static / page_art(number)
        assert sha256(art.read_bytes()).hexdigest() == digest
        assert f"page-{number}.webp?v=anatomy-3" in client.get(
            reverse("reader:medieval_read", args=(number,))
        ).content.decode()
    page = PAGES[546]  # Page 547, using a zero-based index.
    ilyan = next(line for line in page["lines"] if line["speaker"] == "Ilyan")
    assert ilyan["balloon"]["x"] == 22 and ilyan["balloon"]["y"] == 25


def test_arc_five_flood_route_keeps_permissions_and_cast():
    pages = {page["number"]: page for page in PAGES}
    assert all(pages[n]["novel_chapter"] == 32 for n in range(555, 605))
    assert pages[562]["place"] == "portao-sul"
    assert pages[564]["place"] == "cais-leste"
    assert pages[565]["place"] == "barca-enseada"
    assert pages[566]["place"] == "estrada-enseada"
    assert pages[599]["place"] == "borda-norte"
    assert pages[603]["place"] == "valecobre"
    assert pages[604]["place"] == "patio-central"
    assert all("runa" not in pages[n]["cast"] for n in range(558, 594))
    assert "talin" not in pages[597]["cast"] and "talin" in pages[598]["cast"]
    assert all("nima" not in pages[n]["cast"] for n in range(555, 605))


def test_arc_five_school_return_keeps_source_and_sanctions():
    pages = {page["number"]: page for page in PAGES}
    assert pages[605]["novel_chapter"] == 32
    assert all(pages[n]["novel_chapter"] == 33 for n in range(606, 633))
    assert all(pages[n]["novel_chapter"] == 34 for n in range(633, 645))
    assert pages[616]["place"] == "patio-central"
    assert all("nima" not in pages[n]["cast"] for n in range(605, 645))
    assert pages[625]["place"] == "sala-publica-arquivo"
    assert pages[633]["place"] == pages[635]["place"] == "sala-conselho"
    assert pages[644]["place"] == "galeria-biblioteca"


def test_arc_five_end_preserves_rivalry_evidence_and_balloon_speakers():
    pages = {page["number"]: page for page in PAGES}
    for number, expected in ((627, ("Ordelia", "Líria")), (628, ("Oru", "Runa"))):
        first, second = pages[number]["lines"]
        assert (first["speaker"], second["speaker"]) == expected
        assert first["balloon"]["target_x"] > 50
        assert second["balloon"]["target_x"] < 50
    assert "desfigurá-la" in pages[647]["lines"][0]["text"]
    assert pages[648]["lines"][0]["speaker"] == "Ilyan"
    assert pages[648]["place"] == "galeria-biblioteca"
    assert pages[720]["lines"][1]["speaker"] == "Líria"
    assert pages[728]["novel_chapter"] == 36
    assert all("nima" not in pages[n]["cast"] for n in range(645, 729))
    assert [pages[n]["novel_chapter"] for n in range(645, 729)] == sorted(
        pages[n]["novel_chapter"] for n in range(645, 729)
    )


def test_medieval_catalog_shows_series_and_reader_navigation(client):
    catalog = client.get(reverse("reader:search"), {"tipo": "hq"})
    assert catalog.status_code == 200
    html = catalog.content.decode()
    assert STORY["title"] in html
    assert STORY["arc"]["title"] not in html

    detail = client.get(reverse("reader:medieval_detail"))
    arc = client.get(reverse("reader:medieval_arc"))
    arc2 = client.get(reverse("reader:medieval_arc2"))
    arc3 = client.get(reverse("reader:medieval_arc3"))
    arc4 = client.get(reverse("reader:medieval_arc4"))
    arc5 = client.get(reverse("reader:medieval_arc5"))
    assert detail.status_code == arc.status_code == arc2.status_code == arc3.status_code == arc4.status_code == arc5.status_code == 200
    assert STORY["arc"]["title"] in detail.content.decode()
    assert ARCS[1]["title"] in detail.content.decode()
    assert arc.content.decode().count('class="twilight-page-card"') == 25
    assert arc2.content.decode().count('class="twilight-page-card"') == 146
    assert arc3.content.decode().count('class="twilight-page-card"') == 184
    assert arc4.content.decode().count('class="twilight-page-card"') == 163
    assert arc5.content.decode().count('class="twilight-page-card"') == 210
    assert arc2.content.decode().count('data-episode-tab') == len(ARCS[1]["chapters"])

    first = client.get(reverse("reader:medieval_read", args=(1,)))
    last = client.get(reverse("reader:medieval_read", args=(728,)))
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
    assert client.get(reverse("reader:medieval_read", args=(81,))).status_code == 200
    assert 'rel="next"' in client.get(reverse("reader:medieval_read", args=(171,))).content.decode()
    assert 'rel="next"' in client.get(reverse("reader:medieval_read", args=(178,))).content.decode()
    assert client.get(reverse("reader:medieval_read", args=(190,))).status_code == 200
    assert 'twilight-page-stage--direct-tails' in client.get(
        reverse("reader:medieval_read", args=(190,))
    ).content.decode()
    assert client.get(reverse("reader:medieval_read", args=(312,))).status_code == 200
    assert client.get(reverse("reader:medieval_read", args=(421,))).status_code == 200
    assert client.get(reverse("reader:medieval_read", args=(451,))).status_code == 200
    assert client.get(reverse("reader:medieval_read", args=(555,))).status_code == 200
    assert client.get(reverse("reader:medieval_read", args=(729,))).status_code == 404


def test_arc_four_coda_preserves_document_chain_and_speaker_balloon_assignment(client):
    pages = {page["number"]: page for page in PAGES}
    assert [pages[number]["place"] for number in range(509, 516)] == [
        "patio-central", *(["dormitorio-cedro"] * 6)
    ]
    assert pages[511]["lines"] == []  # The kiss is a deliberately silent comic page.
    assert pages[515]["lines"][0]["speaker"] == "Runa"
    assert pages[515]["lines"][1]["speaker"] == "Ilyan"
    assert all(line["balloon"]["embedded"] for number in (515, 517) for line in pages[number]["lines"])
    assert all("nima" not in pages[number]["cast"] for number in range(503, 519))
    assert [pages[number]["time"].split(" · ")[0] for number in range(503, 519)] == sorted(
        pages[number]["time"].split(" · ")[0] for number in range(503, 519)
    )
    html = client.get(reverse("reader:medieval_read", args=(515,))).content.decode()
    assert html.count('data-embedded="true"') == 2
