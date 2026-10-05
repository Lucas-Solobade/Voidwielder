from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .book_catalog import BOOK, get_book_pages
from .catalog import ARCS, MANGA, get_arc, get_chapter_for_page
from .game_catalog import GAMES
from .linux_catalog import LINUX_BOOK, PARTS, get_linux_lessons, get_linux_pages
from .study_catalog import STUDY_GUIDE


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/home.html", {"manga": MANGA, "arcs": ARCS})


@require_GET
def hq_detail(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/hq_detail.html", {"manga": MANGA, "arcs": ARCS})


@require_GET
def arc_detail(request: HttpRequest, arc_slug: str) -> HttpResponse:
    arc = get_arc(arc_slug)
    if arc is None:
        raise Http404("Arco não encontrado")
    return render(request, "reader/arc_detail.html", {"manga": MANGA, "arc": arc})


@require_GET
def read_arc(request: HttpRequest, arc_slug: str) -> HttpResponse:
    """Render an entire arc as one continuous, book-like reader."""
    arc = get_arc(arc_slug)
    if arc is None:
        raise Http404("Arco não encontrado")
    pages = [
        {
            "number": page,
            "filename": f"reader/images/pages/page-{page:02}.webp",
            "chapter": get_chapter_for_page(page),
        }
        for page in range(arc.start_page, arc.end_page + 1)
    ]
    return render(request, "reader/read_arc.html", {"manga": MANGA, "arc": arc, "pages": pages})


@require_GET
def read_page(request: HttpRequest, arc_slug: str, page: int) -> HttpResponse:
    arc = get_arc(arc_slug)
    if arc is None or not arc.start_page <= page <= arc.end_page:
        raise Http404("Página não encontrada neste arco")

    previous_url = None
    next_url = None
    if page > 1:
        previous_arc = next(item for item in ARCS if item.start_page <= page - 1 <= item.end_page)
        previous_url = reverse("reader:read", args=(previous_arc.slug, page - 1))
    if page < ARCS[-1].end_page:
        next_arc = next(item for item in ARCS if item.start_page <= page + 1 <= item.end_page)
        next_url = reverse("reader:read", args=(next_arc.slug, page + 1))

    return render(
        request,
        "reader/read.html",
        {
            "manga": MANGA,
            "arc": arc,
            "chapter": get_chapter_for_page(page),
            "page_number": page,
            "page_filename": f"reader/images/pages/page-{page:02}.webp",
            "previous_url": previous_url,
            "next_url": next_url,
            "page_range": range(arc.start_page, arc.end_page + 1),
        },
    )


@require_GET
def search(request: HttpRequest) -> HttpResponse:
    query = " ".join(request.GET.get("q", "").split())[:80]
    category = request.GET.get("tipo", "todos")
    if category not in {"todos", "hq", "livros", "jogos", "estudos"}:
        category = "todos"
    results: list[dict[str, object]] = []
    if category in {"todos", "livros"}:
        book_text = f"{BOOK['title']} {BOOK['author']} {BOOK['genre']} {BOOK['detail']} {BOOK['topics']}".casefold()
        if not query or query.casefold() in book_text:
            results.append({
                "kind": "Livro", "title": BOOK["title"], "url": BOOK["url"],
                "detail": f"{BOOK['author']} · {BOOK['genre']} · 150 páginas. {BOOK['detail']}",
                "book_art": True,
            })
        linux_text = f"{LINUX_BOOK['title']} {LINUX_BOOK['detail']} {LINUX_BOOK['topics']}".casefold()
        if not query or query.casefold() in linux_text:
            results.append({
                "kind": "Livro didático", "title": LINUX_BOOK["title"], "url": LINUX_BOOK["url"],
                "detail": f"13 partes · 78 lições · {LINUX_BOOK['page_count']} páginas. {LINUX_BOOK['detail']}",
                "linux_art": True,
            })
    if category in {"todos", "hq"}:
        needle = query.casefold()
        manga_text = f"{MANGA['title']} {MANGA['description']} {MANGA['tagline']}".casefold()
        if not query or needle in manga_text:
            results.append(
                {
                    "kind": "HQ",
                    "title": MANGA["title"],
                    "url": reverse("reader:hq"),
                    "detail": MANGA["description"],
                    "cover": MANGA["cover"],
                }
            )
        if query:
            for arc in ARCS:
                arc_text = f"{arc.title} {arc.description}".casefold()
                if needle in arc_text:
                    results.append(
                        {
                            "kind": "Arco",
                            "title": arc.title,
                            "url": reverse("reader:arc", args=(arc.slug,)),
                            "detail": arc.description,
                        }
                    )
                for chapter in arc.chapters:
                    chapter_text = f"{chapter.title} {chapter.subtitle}".casefold()
                    if needle in chapter_text or needle == str(chapter.number):
                        results.append(
                            {
                                "kind": "Capítulo",
                                "title": chapter.title,
                                "url": f"{reverse('reader:read_arc', args=(arc.slug,))}#capitulo-{chapter.number}",
                                "detail": chapter.subtitle,
                            }
                        )
    if category in {"todos", "estudos"}:
        study_text = f"{STUDY_GUIDE['title']} {STUDY_GUIDE['detail']} {' '.join(STUDY_GUIDE['topics'])}".casefold()
        if not query or query.casefold() in study_text:
            results.append(
                {
                    "kind": "Trilha de estudos",
                    "title": STUDY_GUIDE["title"],
                    "url": reverse("reader:studies"),
                    "detail": STUDY_GUIDE["detail"],
                }
            )
    if category in {"todos", "jogos"}:
        for game_item in GAMES:
            game_text = f"{game_item['title']} {game_item['detail']} {game_item['topics']}".casefold()
            if not query or query.casefold() in game_text:
                results.append(
                    {
                        "kind": "Jogo",
                        "title": game_item["title"],
                        "url": game_item["url"],
                        "detail": game_item["detail"],
                    }
                )
    titles = {
        "todos": "Explore o catálogo",
        "livros": "Livros",
        "hq": "HQs",
        "jogos": "Jogos",
        "estudos": "Estudos",
    }
    context = {
        "manga": MANGA,
        "query": query,
        "category": category,
        "category_title": titles[category],
        "results": results,
    }
    return render(request, "reader/search.html", context)


@require_GET
def book_detail(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/book_detail.html", {"book": BOOK})


@require_GET
def read_book(request: HttpRequest, page: int) -> HttpResponse:
    pages = get_book_pages()
    if not 1 <= page <= len(pages):
        raise Http404("Página não encontrada")
    chapter_starts = [item for item in pages if item.chapter_start]
    return render(request, "reader/book_read.html", {
        "book": BOOK, "page": pages[page - 1], "next_page": pages[page] if page < len(pages) else None,
        "previous_number": page - 1 if page > 1 else None,
        "next_number": page + 1 if page < len(pages) else None,
        "chapter_starts": chapter_starts,
    })


@require_GET
def linux_detail(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/linux_detail.html", {
        "book": LINUX_BOOK, "parts": list(enumerate(PARTS, start=1)),
        "lessons": get_linux_lessons(),
    })


@require_GET
def read_linux(request: HttpRequest, page: int) -> HttpResponse:
    pages = get_linux_pages()
    if not 1 <= page <= len(pages):
        raise Http404("Página não encontrada")
    return render(request, "reader/linux_read.html", {
        "book": LINUX_BOOK, "page": pages[page - 1],
        "next_page": pages[page] if page < len(pages) else None,
        "previous_number": page - 1 if page > 1 else None,
        "next_number": page + 1 if page < len(pages) else None,
        "lessons": get_linux_lessons(),
    })


@require_GET
def studies(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/studies.html", {"manga": MANGA})


@require_GET
def game(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/game.html", {"manga": MANGA})


@require_GET
def playground(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/playground.html")


@require_GET
def robots(_: HttpRequest) -> HttpResponse:
    body = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    return HttpResponse(body, content_type="text/plain")


@require_GET
def sitemap(request: HttpRequest) -> HttpResponse:
    urls = [request.build_absolute_uri(reverse("reader:home"))]
    urls.append(request.build_absolute_uri(reverse("reader:hq")))
    urls.append(request.build_absolute_uri(reverse("reader:studies")))
    urls.append(request.build_absolute_uri(reverse("reader:game")))
    urls.append(request.build_absolute_uri(reverse("reader:playground")))
    urls.append(request.build_absolute_uri(reverse("reader:book_detail")))
    urls.extend(request.build_absolute_uri(reverse("reader:read_book", args=(page,))) for page in range(1, 151))
    urls.append(request.build_absolute_uri(reverse("reader:linux_detail")))
    urls.extend(request.build_absolute_uri(reverse("reader:read_linux", args=(page,))) for page in range(1, LINUX_BOOK["page_count"] + 1))
    urls.extend(request.build_absolute_uri(reverse("reader:arc", args=(arc.slug,))) for arc in ARCS)
    urls.extend(
        request.build_absolute_uri(reverse("reader:read_arc", args=(arc.slug,))) for arc in ARCS
    )
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{entries}</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml")
