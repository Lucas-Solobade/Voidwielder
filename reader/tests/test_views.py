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


def test_playground_is_in_games_and_search(client):
    games = client.get(reverse("reader:search"), {"tipo": "jogos"}).content.decode()
    assert "Laboratório do Vazio" in games
    assert 'href="/playground/"' in games

    search = client.get(reverse("reader:search"), {"tipo": "jogos", "q": "Laboratório"})
    assert "Laboratório do Vazio" in search.content.decode()

    page = client.get(reverse("reader:playground"))
    assert page.status_code == 200
    assert "lab.mjs" in page.content.decode()


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


def test_book_catalog_and_reader_deep_links(client):
    catalog = client.get(reverse("reader:search"), {"tipo": "livros"})
    assert catalog.status_code == 200
    assert "A Casa das Medidas" in catalog.content.decode()
    assert 'data-book-art="cover"' in catalog.content.decode()

    detail = client.get(reverse("reader:book_detail"))
    assert detail.status_code == 200
    assert "150 páginas" in detail.content.decode()

    for page_number in (1, 74, 150):
        page = client.get(reverse("reader:read_book", args=(page_number,)))
        assert page.status_code == 200
        assert f'data-page="{page_number}"' in page.content.decode()
        assert len(page.content) > 2000
    assert client.get(reverse("reader:read_book", args=(151,))).status_code == 404


def test_book_pagination_preserves_every_sentence_once():
    from reader.book_catalog import CHAPTER_DIR, _split_chapter, get_book_pages

    pages = get_book_pages()
    assert len(pages) == 150
    assert [page.number for page in pages] == list(range(1, 151))
    assert [page.chapter_number for page in pages if page.chapter_start] == list(range(1, 16))
    assert min(page.word_count for page in pages) >= 80
    assert max(page.word_count for page in pages) <= 185
    for chapter_number, path in enumerate(sorted(CHAPTER_DIR.glob("*.md")), start=1):
        _, source = _split_chapter(path.read_text(encoding="utf-8"))
        original = " ".join(sentence for _, sentence in source)
        published = " ".join(
            paragraph
            for page in pages if page.chapter_number == chapter_number
            for paragraph in page.paragraphs
        )
        assert published == original
