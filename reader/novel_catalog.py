"""The illustrated Estradas novel: real manuscript pages, never placeholders."""

from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from .book_catalog import SENTENCE_BOUNDARY

CHAPTER_DIR = Path(__file__).resolve().parent / "books" / "estradas_crepusculo" / "chapters"
PLATE_DIR = Path(__file__).resolve().parent / "static" / "reader" / "images" / "novel"
ILLUSTRATED_LEAVES = frozenset({0})
EXPECTED_CHAPTERS = 48
TARGET_PAGES = 956


@dataclass(frozen=True)
class NovelPage:
    number: int
    chapter_number: int
    chapter_title: str
    chapter_start: bool
    illustration: str | None
    paragraphs: tuple[str, ...]
    word_count: int

    def as_json(self) -> dict[str, object]:
        return asdict(self)


def _sentences(source: str) -> tuple[str, list[tuple[int, str]]]:
    blocks = [block.strip() for block in source.strip().split("\n\n") if block.strip()]
    if not blocks or not blocks[0].startswith("# "):
        raise ValueError("Cada capítulo precisa começar com um título Markdown")
    title = blocks[0][2:]
    sentences = [
        (index, sentence.strip())
        for index, block in enumerate(blocks[1:])
        for sentence in SENTENCE_BOUNDARY.split(block)
        if sentence.strip()
    ]
    return title, sentences


def _boundaries(sentences: list[tuple[int, str]], count: int) -> list[int]:
    """Balance prose at sentence boundaries with room for ink illustrations."""
    prefix = [0]
    for _, sentence in sentences:
        prefix.append(prefix[-1] + len(sentence.split()))
    if prefix[-1] < count * 55:
        raise ValueError(f"Capítulo curto: {prefix[-1]} palavras para {count} páginas")
    weights = [0.76 if index in ILLUSTRATED_LEAVES else 1 for index in range(count)]
    unit = prefix[-1] / sum(weights)
    costs: list[dict[int, tuple[float, int]]] = [{0: (0, -1)}]
    for page_index in range(count):
        current: dict[int, tuple[float, int]] = {}
        minimum = 42 if page_index in ILLUSTRATED_LEAVES else 55
        for start, (prior_cost, _) in costs[-1].items():
            for end in range(start + 1, len(sentences) + 1):
                words = prefix[end] - prefix[start]
                if words > 155:
                    break
                if words < minimum:
                    continue
                penalty = 14 if end < len(sentences) and sentences[end - 1][0] == sentences[end][0] else 0
                cost = prior_cost + (words - unit * weights[page_index]) ** 2 + penalty
                if end not in current or cost < current[end][0]:
                    current[end] = (cost, start)
        costs.append(current)
    if len(sentences) not in costs[-1]:
        raise ValueError("O capítulo não cabe em páginas legíveis sem cortar frases")
    bounds = [len(sentences)]
    for index in range(count, 0, -1):
        bounds.append(costs[index][bounds[-1]][1])
    return list(reversed(bounds))


def _paragraphs(sentences: list[tuple[int, str]]) -> tuple[str, ...]:
    result: list[str] = []
    previous = -1
    for index, sentence in sentences:
        if index == previous:
            result[-1] += f" {sentence}"
        else:
            result.append(sentence)
            previous = index
    return tuple(result)


@lru_cache(maxsize=1)
def get_novel_pages() -> tuple[NovelPage, ...]:
    pages: list[NovelPage] = []
    chapters = sorted(CHAPTER_DIR.glob("[0-9][0-9].md"))
    if not chapters or len(chapters) > EXPECTED_CHAPTERS:
        raise ValueError("Número inválido de capítulos do romance")
    for chapter_number, chapter_path in enumerate(chapters, start=1):
        if chapter_path.stem != f"{chapter_number:02}":
            raise ValueError("Os capítulos devem ser sequenciais")
        title, sentences = _sentences(chapter_path.read_text(encoding="utf-8"))
        count = 16 if chapter_number == EXPECTED_CHAPTERS else 20
        plate_available = chapter_number in range(21, 25) or (PLATE_DIR / f"chapter-{chapter_number:02}.webp").is_file()
        bounds = _boundaries(sentences, count)
        for leaf in range(count):
            content = _paragraphs(sentences[bounds[leaf] : bounds[leaf + 1]])
            pages.append(NovelPage(
                number=len(pages) + 1,
                chapter_number=chapter_number,
                chapter_title=title,
                chapter_start=leaf == 0,
                illustration=f"{chapter_number:02}-1" if leaf in ILLUSTRATED_LEAVES and plate_available else None,
                paragraphs=content,
                word_count=sum(len(paragraph.split()) for paragraph in content),
            ))
    if len(chapters) == EXPECTED_CHAPTERS and len(pages) != TARGET_PAGES:
        raise ValueError("O romance completo deve ter 956 páginas reais")
    return tuple(pages)


NOVEL = {
    "slug": "as-estradas-do-crepusculo-o-ferro-que-escuta",
    "title": "As Estradas do Crepúsculo",
    "subtitle": "O Ferro que Escuta",
    "author": "Voidwielder",
    "genre": "Fantasia medieval",
    "detail": (
        "Ilyan herda uma pergunta escrita pela mãe e parte da forja de Pedra-Mansa "
        "para uma escola onde mapas, aço e magia têm preço."
    ),
    "topics": "Ilyan Runa Nima Mira fantasia medieval romance escola magia elfos gnomos fadas orcs",
    "url": "/livros/as-estradas-do-crepusculo/",
    "page_count": len(get_novel_pages()),
    "chapter_count": len(list(CHAPTER_DIR.glob("[0-9][0-9].md"))),
    "target_pages": TARGET_PAGES,
    "complete": len(get_novel_pages()) == TARGET_PAGES,
}
