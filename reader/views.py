from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .catalog import ARCS, MANGA, get_arc, get_chapter_for_page

FINALE_PAGES = {
    74: {
        "title": "A prova que chegou antes do crime",
        "panels": (
            (
                "reader/images/pages/page-73.webp",
                "A Vardo projeta uma gravação adulterada: Isaac supostamente teria sabotado a transmissão.",
            ),
            (
                "reader/images/pages/page-65.webp",
                "Elen encontra a falha: o arquivo tem uma data que ainda não aconteceu.",
            ),
            (
                "reader/images/pages/page-66.webp",
                "Alan usa a lupa ao contrário; Johnny oferece recibos de tecido. Nenhum dos dois ajuda, mas tentam.",
            ),
            (
                "reader/images/pages/page-70.webp",
                "O drone anuncia a acusação: ‘Disrupção sonora’. Isaac responde: ‘Meu beat nem tem grave hoje!’",
            ),
        ),
    },
    75: {
        "title": "Ordem de silêncio",
        "panels": (
            (
                "reader/images/pages/page-70.webp",
                "A Vardo chama uma ‘inspeção’ que não aceita perguntas.",
            ),
            (
                "reader/images/pages/page-68.webp",
                "Elen pede a ordem judicial. A Vardo entrega uma folha sem assinatura.",
            ),
            (
                "reader/images/pages/page-71.webp",
                "As luzes apagam para criar pânico; a Faze Azul ilumina a escada.",
            ),
            (
                "reader/images/pages/page-73.webp",
                "No escuro, os drones cercam Isaac e declaram prisão por uma prova que eles mesmos criaram.",
            ),
        ),
    },
    76: {
        "title": "A prisão mais covarde da cidade",
        "panels": (
            (
                "reader/images/pages/page-72.webp",
                "A plateia tenta cantar mais alto; a Vardo corta o som e exibe o vídeo falso nos drones.",
            ),
            (
                "reader/images/pages/page-64.webp",
                "Geraldo, ainda em reparo supervisionado, avisa por vídeo: ‘Não assinem nada. Eles querem um bode expiatório.’",
            ),
            (
                "reader/images/pages/page-62.webp",
                "Clotilde leva a chave da Faze Azul para longe; Isaac pede que ninguém lute por ele.",
            ),
            (
                "reader/images/pages/page-73.webp",
                "Isaac é levado sem violência física, sob luz vermelha e uma acusação fabricada.",
            ),
        ),
    },
    77: {
        "title": "A batida não ficou presa",
        "panels": (
            (
                "reader/images/pages/page-58.webp",
                "Bia, Nara e Luna transformam as cartas dos fãs em uma linha do tempo da fraude.",
            ),
            (
                "reader/images/pages/page-68.webp",
                "Elen copia os metadados em três lugares da rede comunitária.",
            ),
            (
                "reader/images/pages/page-60.webp",
                "Johnny promete ‘advocacia de capa’, e Clotilde responde com um pi-pi de reprovação.",
            ),
            (
                "reader/images/pages/page-69.webp",
                "Mesmo preso, o refrão de Isaac continua nos telhados: a cidade não esqueceu.",
            ),
        ),
    },
    78: {
        "title": "Próxima faixa: alguém novo",
        "panels": (
            (
                "reader/images/pages/page-65.webp",
                "A Vardo celebra a prisão em seus monitores, sem perceber que a fraude deixou rastros.",
            ),
            (
                "reader/images/pages/page-68.webp",
                "Elen guarda a prova e diz: ‘Agora precisamos de alguém que saiba entrar onde eles se escondem.’",
            ),
            (
                "reader/images/pages/page-72.webp",
                "Alan, Johnny, Bia, Nara, Luna e Clotilde olham a cidade: ‘A gente traz o Isaac de volta.’",
            ),
            (
                "reader/images/pages/page-73.webp",
                "Narração: ‘FIM DO ARCO FAZE AZUL. O PRÓXIMO NOME JÁ ESTÁ A CAMINHO.’",
            ),
        ),
    },
}


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
            "story": FINALE_PAGES.get(page),
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
            "story": FINALE_PAGES.get(page),
        },
    )


@require_GET
def search(request: HttpRequest) -> HttpResponse:
    query = " ".join(request.GET.get("q", "").split())[:80]
    results: list[dict[str, object]] = []
    if query:
        needle = query.casefold()
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
    context = {"manga": MANGA, "query": query, "results": results}
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
