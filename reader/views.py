from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .catalog import ARCS, MANGA, get_arc, get_chapter_for_page


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(request, "reader/home.html", {"manga": MANGA, "arcs": ARCS})


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
    if category in {"todos", "hq"}:
        needle = query.casefold()
        for arc in ARCS:
            arc_text = f"{arc.title} {arc.description}".casefold()
            if not needle or needle in arc_text:
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
                if not needle or needle in chapter_text or needle == str(chapter.number):
                    results.append(
                        {
                            "kind": "Capítulo",
                            "title": chapter.title,
                            "url": f"{reverse('reader:read_arc', args=(arc.slug,))}#capitulo-{chapter.number}",
                            "detail": chapter.subtitle,
                        }
                    )
    context = {"manga": MANGA, "query": query, "category": category, "results": results}
    return render(request, "reader/search.html", context)


@require_GET
def robots(_: HttpRequest) -> HttpResponse:
    body = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    return HttpResponse(body, content_type="text/plain")


@require_GET
def sitemap(request: HttpRequest) -> HttpResponse:
    urls = [request.build_absolute_uri(reverse("reader:home"))]
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
