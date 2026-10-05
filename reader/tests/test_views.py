from django.urls import reverse


def test_home_links_to_catalog_and_studies(client):
    response = client.get(reverse("reader:home"))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("reader:search") in content
    assert reverse("reader:studies") in content


def test_reader_rejects_page_outside_arc(client):
    response = client.get(reverse("reader:read", args=("invasao-desastrada", 18)))
    assert response.status_code == 404


def test_search_finds_clotilde_chapter(client):
    response = client.get(reverse("reader:search"), {"q": "Clotilde"})
    assert response.status_code == 200
    assert "A Agência e Clotilde" in response.content.decode()


def test_game_is_in_catalog_and_has_own_page(client):
    search = client.get(reverse("reader:search"), {"tipo": "jogos"})
    assert search.status_code == 200
    assert "Pipo e o Correio das Estrelas" in search.content.decode()
    game = client.get(reverse("reader:game"))
    assert game.status_code == 200
    content = game.content.decode()
    assert "data-canvas" in content
    assert "game/main.js" in content


def test_canonical_page_ranges():
    from reader.catalog import ARCS

    assert ARCS[0].start_page == 1 and ARCS[0].end_page == 17
    assert ARCS[1].start_page == 18 and ARCS[1].end_page == 50
    assert ARCS[2].start_page == 51 and ARCS[2].end_page == 78
    assert ARCS[3].start_page == 79 and ARCS[3].end_page == 96
    assert sum(arc.page_count for arc in ARCS) == 96


def test_arc_book_reader_has_all_pages(client):
    response = client.get(reverse("reader:read_arc", args=("faze-azul",)))
    content = response.content.decode()
    assert response.status_code == 200
    assert "page-51.webp" in content
    assert "page-78.webp" in content
    assert "story-page" not in content
