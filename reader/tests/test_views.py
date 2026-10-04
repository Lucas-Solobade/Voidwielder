from django.urls import reverse


def test_home_lists_both_arcs(client):
    response = client.get(reverse("reader:home"))
    assert response.status_code == 200
    assert "A Invasão Mais Desastrada da Terra" in response.content.decode()
    assert "O Palco Veludo de Geraldo" in response.content.decode()


def test_reader_rejects_page_outside_arc(client):
    response = client.get(reverse("reader:read", args=("invasao-desastrada", 18)))
    assert response.status_code == 404


def test_search_finds_clotilde_chapter(client):
    response = client.get(reverse("reader:search"), {"q": "Clotilde"})
    assert response.status_code == 200
    assert "A Agência e Clotilde" in response.content.decode()


def test_canonical_page_ranges():
    from reader.catalog import ARCS

    assert ARCS[0].start_page == 1 and ARCS[0].end_page == 17
    assert ARCS[1].start_page == 18 and ARCS[1].end_page == 50
    assert sum(arc.page_count for arc in ARCS) == 50
