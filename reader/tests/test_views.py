from django.urls import reverse


def test_home_links_to_catalog_and_studies(client):
    response = client.get(reverse("reader:home"))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("reader:search") in content
    assert reverse("reader:studies") in content


def test_studies_catalog_opens_each_project_without_showing_the_whole_track(client):
    from reader.study_catalog import STUDY_PROJECTS
    from scripts.export_static import build_catalog

    catalog = client.get(reverse("reader:studies"))
    assert catalog.status_code == 200
    html = catalog.content.decode()
    assert "study-catalog-grid" in html
    assert "study-week-head" not in html
    for project in STUDY_PROJECTS:
        assert project["title"] in html
        assert f'href="{project["url"]}"' in html
        assert project["image"] in html

    guide = client.get(reverse("reader:study_guide"))
    assert guide.status_code == 200
    assert "study-week-head" in guide.content.decode()
    assert "Voltar aos estudos" in guide.content.decode()

    search = client.get(reverse("reader:search"), {"tipo": "estudos"})
    assert search.status_code == 200
    assert search.content.decode().count('class="study-result-card"') == len(STUDY_PROJECTS)
    assert len([item for item in build_catalog() if item["category"] == "estudos"]) == len(STUDY_PROJECTS)


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


def test_garden_game_is_listed_and_playable(client):
    url = reverse("reader:garden_game")
    catalog = client.get(reverse("reader:search"), {"tipo": "jogos"}).content.decode()
    assert 'Mila e o Jardim das Nuvens' in catalog
    assert f'href="{url}"' in catalog
    assert 'garden-card' in catalog

    page = client.get(url)
    assert page.status_code == 200
    assert 'data-garden-canvas' in page.content.decode()
    assert 'garden/game.mjs' in page.content.decode()


def test_bubble_game_is_listed_and_playable(client):
    url = reverse("reader:bubble_game")
    catalog = client.get(reverse("reader:search"), {"tipo": "jogos"}).content.decode()
    assert "Lilo e o Festival das Bolhas" in catalog
    assert f'href="{url}"' in catalog
    assert "bubble-card" in catalog

    page = client.get(url)
    assert page.status_code == 200
    content = page.content.decode()
    assert "data-bubble-canvas" in content
    assert "bubbles/game.mjs" in content


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


def test_linux_textbook_is_in_books_and_has_stable_deep_links(client):
    catalog = client.get(reverse("reader:search"), {"tipo": "livros"})
    assert catalog.status_code == 200
    assert "Linux: do zero ao avançado" in catalog.content.decode()
    detail = client.get(reverse("reader:linux_detail"))
    assert detail.status_code == 200
    assert "554" in detail.content.decode()
    assert "data-linux-art=\"cover\"" in detail.content.decode()
    for number in (1, 9, 344, 554):
        response = client.get(reverse("reader:read_linux", args=(number,)))
        assert response.status_code == 200
        assert f'data-page="{number}"' in response.content.decode()
    assert client.get(reverse("reader:read_linux", args=(555,))).status_code == 404


def test_linux_manuscript_has_real_unique_pages_and_every_lesson():
    from reader.linux_catalog import get_linux_lessons, get_linux_pages

    pages = get_linux_pages()
    lessons = get_linux_lessons()
    assert len(pages) == 554
    assert len(lessons) == 78
    assert [page.number for page in pages] == list(range(1, 555))
    assert min(len(page.body.split()) for page in pages) >= 40
    assert len({page.body for page in pages}) == 554
    assert [sum(page.lesson_number == lesson.number for page in pages) for lesson in lessons] == [7] * 78
    assert {page.diagram for page in pages if page.diagram} == {"rede", "boot", "container"}


def test_python_book_is_in_catalog_and_all_deep_links_resolve(client):
    catalog = client.get(reverse("reader:search"), {"tipo": "livros"})
    assert catalog.status_code == 200
    assert "Python: do zero ao avançado" in catalog.content.decode()
    detail = client.get(reverse("reader:python_detail"))
    assert detail.status_code == 200
    assert "<strong>39</strong> desafios" in detail.content.decode()
    for number in (1, 9, 142, 281):
        response = client.get(reverse("reader:read_python", args=(number,)))
        assert response.status_code == 200
        assert f'data-page="{number}"' in response.content.decode()
        assert "python-lab" in response.content.decode()
    assert client.get(reverse("reader:read_python", args=(282,))).status_code == 404


def test_python_manuscript_and_exercise_solutions_are_complete():
    import asyncio

    from reader.python_catalog import get_python_lessons, get_python_pages
    from reader.python_exercises import EXERCISES

    pages = get_python_pages()
    lessons = get_python_lessons()
    assert len(pages) == 281
    assert len(lessons) == len(EXERCISES) == 39
    assert len({page.body for page in pages}) == 281
    assert [sum(page.lesson_number == lesson.number for page in pages) for lesson in lessons] == [7] * 39

    def raises_value_error(fn, *args):
        try:
            fn(*args)
        except ValueError:
            return True
        return False

    def carteiras_independentes(cls):
        first, second = cls(0), cls(0)
        first.depositar(2)
        return first.saldo == 2 and second.saldo == 0

    async def await_result(awaitable, expected):
        return await awaitable == expected

    for exercise in EXERCISES:
        scope = {
            "_raises_value_error": raises_value_error,
            "_carteiras_independentes": carteiras_independentes,
            "_await_result": await_result,
        }
        exec(exercise.solution, scope)
        for label, check in exercise.tests:
            result = asyncio.run(eval(check[6:], scope)) if check.startswith("await ") else eval(check, scope)
            assert result, f"Lição {exercise.lesson}: {label}"


def test_web_book_has_complete_curriculum_and_direct_page_links(client):
    import re

    from reader.web_catalog import MANUSCRIPT, WEB_BOOK, _sections, get_web_pages, get_web_sections

    pages = get_web_pages()
    sections = get_web_sections()
    assert len(pages) == WEB_BOOK["page_count"] >= 60
    assert [section.chapter_number for section in sections if section.chapter_number] == list(range(1, 18))
    manuscript = "\n".join(page.plain_text for page in pages)
    original = "\n".join(block.source for _, _, _, blocks in _sections(MANUSCRIPT.read_text(encoding="utf-8")) for block in blocks)
    assert re.sub(r"\s+", " ", manuscript) == re.sub(r"\s+", " ", original)
    for topic in ("Use elementos pelo papel", "display: flex", "fetch", "node:http", "WHERE id", "CSRF", "observabilidade"):
        assert topic.casefold() in manuscript.casefold()
    assert "Conferir resposta" in "".join(page.body_html for page in pages)
    assert "&lt;html" in "".join(page.body_html for page in pages)

    catalog = client.get(reverse("reader:search"), {"tipo": "livros"})
    assert WEB_BOOK["title"] in catalog.content.decode()
    assert client.get(reverse("reader:web_detail")).status_code == 200
    for number in (1, 32, WEB_BOOK["page_count"]):
        response = client.get(reverse("reader:read_web", args=(number,)))
        assert response.status_code == 200
        assert f'data-page="{number}"' in response.content.decode()
    assert client.get(reverse("reader:read_web", args=(WEB_BOOK["page_count"] + 1,))).status_code == 404


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
