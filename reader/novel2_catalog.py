"""Second Estradas volume: sixth through eleventh arcs."""

from functools import lru_cache
from pathlib import Path

from .novel_catalog import NovelPage, _boundaries, _paragraphs, _sentences

CHAPTER_DIR = Path(__file__).resolve().parent / "books" / "estradas_crepusculo_ii" / "chapters"
PLATE_DIR = Path(__file__).resolve().parent / "static" / "reader" / "images" / "novel"
EXPECTED_CHAPTERS = 98


@lru_cache(maxsize=1)
def get_novel2_pages() -> tuple[NovelPage, ...]:
    chapters = sorted(CHAPTER_DIR.glob("[0-9][0-9].md"))
    if len(chapters) != EXPECTED_CHAPTERS:
        raise ValueError(f"O volume II exige seus {EXPECTED_CHAPTERS} capítulos completos")
    pages: list[NovelPage] = []
    for chapter_number, chapter_path in enumerate(chapters, start=1):
        if chapter_path.stem != f"{chapter_number:02}":
            raise ValueError("Os capítulos do segundo volume devem ser sequenciais")
        title, sentences = _sentences(chapter_path.read_text(encoding="utf-8"))
        words = sum(len(sentence.split()) for _, sentence in sentences)
        if chapter_number <= 26:
            minimum_pages = 10
        elif chapter_number <= 42:
            minimum_pages = 8
        elif chapter_number <= 74:
            minimum_pages = 5
        else:
            minimum_pages = 1
        page_count = max(minimum_pages, round(words / 125))
        bounds = _boundaries(sentences, page_count, minimum_words=90)
        plate_available = (PLATE_DIR / f"volume-2-chapter-{chapter_number:02}.webp").is_file()
        for leaf in range(page_count):
            content = _paragraphs(sentences[bounds[leaf]:bounds[leaf + 1]])
            pages.append(NovelPage(
                number=len(pages) + 1,
                chapter_number=chapter_number,
                chapter_title=title,
                chapter_start=leaf == 0,
                illustration=f"v2-{chapter_number:02}" if leaf == 0 and plate_available else None,
                paragraphs=content,
                word_count=sum(len(paragraph.split()) for paragraph in content),
            ))
    return tuple(pages)


NOVEL_II = {
    "slug": "as-estradas-do-crepusculo-o-avesso-das-aguas",
    "title": "As Estradas do Crepúsculo",
    "subtitle": "O Avesso das Águas · Volume II",
    "author": "Voidwielder",
    "genre": "Fantasia medieval",
    "detail": (
        "De Porto das Cinzas ao Entremeio, Ilyan e seus amigos investigam Mira. "
        "Em A Estrada dos Ausentes, uma carta de Aram leva o grupo a uma travessia "
        "ameaçada e aproxima Ilyan das perguntas que guardou para a mãe."
    ),
    "topics": "Ilyan Runa Líria Caio Sere Tovo Nima Mira Porto das Cinzas Entremeio Talveira Vigília de Aram magia fantasia medieval",
    "url": "/livros/as-estradas-do-crepusculo-volume-ii/",
    "read_url": "/livros/as-estradas-do-crepusculo-volume-ii/ler/",
    "pages_url": "/static/reader/book/estradas-crepusculo-ii/pages.json",
    "volume_number": 2,
    "page_count": len(get_novel2_pages()),
    "chapter_count": EXPECTED_CHAPTERS,
    "published_arc": 11,
    "target_pages": None,
    "complete": False,
    "endmark": "FIM DO ARCO 11 · O VOLUME CONTINUA",
}
