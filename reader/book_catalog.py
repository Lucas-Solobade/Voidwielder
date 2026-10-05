"""The original book and its stable, sentence-aware pagination."""

import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

BOOK = {
    "slug": "a-casa-das-medidas",
    "title": "A Casa das Medidas",
    "author": "Helena Bastos",
    "genre": "Terror psicológico",
    "detail": (
        "Ao medir um prédio condenado, Teresa encontra um corredor maior que a fachada. "
        "A planta que deveria explicá-lo leva sua assinatura de vinte e quatro anos antes."
    ),
    "topics": "livro terror suspense psicológico mistério prédio memória culpa Helena Bastos",
    "url": "/livros/a-casa-das-medidas/",
    "page_count": 150,
}

CHAPTER_DIR = Path(__file__).resolve().parent / "books" / "casa_medidas" / "chapters"
PAGE_COUNT_PER_CHAPTER = 10
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[«\"“A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ0-9])")


@dataclass(frozen=True)
class BookPage:
    number: int
    chapter_number: int
    chapter_title: str
    chapter_start: bool
    paragraphs: tuple[str, ...]
    word_count: int

    def as_json(self) -> dict[str, object]:
        return asdict(self)


def _split_chapter(source: str) -> tuple[str, list[tuple[int, str]]]:
    blocks = [block.strip() for block in source.strip().split("\n\n") if block.strip()]
    title = blocks[0].removeprefix("# ")
    sentences: list[tuple[int, str]] = []
    for paragraph_index, paragraph in enumerate(blocks[1:]):
        sentences.extend(
            (paragraph_index, sentence.strip())
            for sentence in SENTENCE_BOUNDARY.split(paragraph)
            if sentence.strip()
        )
    return title, sentences


def _page_boundaries(sentences: list[tuple[int, str]]) -> list[int]:
    """Balance ten pages per chapter without cutting a sentence or padding text."""
    total_sentences = len(sentences)
    prefix = [0]
    for _, sentence in sentences:
        prefix.append(prefix[-1] + len(sentence.split()))

    average = prefix[-1] / PAGE_COUNT_PER_CHAPTER
    targets = [average * 0.75] + [average * (PAGE_COUNT_PER_CHAPTER - 0.75) / 9] * 9
    costs: list[dict[int, tuple[float, int]]] = [{0: (0, -1)}]
    for page_index, target in enumerate(targets):
        previous = costs[-1]
        current: dict[int, tuple[float, int]] = {}
        for end in range(page_index + 1, total_sentences + 1):
            for start, (prior_cost, _) in previous.items():
                if start >= end:
                    continue
                words = prefix[end] - prefix[start]
                if words < 65 or words > 185:
                    continue
                paragraph_penalty = 0
                if end < total_sentences and sentences[end - 1][0] == sentences[end][0]:
                    paragraph_penalty = 18
                candidate = prior_cost + (words - target) ** 2 + paragraph_penalty
                if end not in current or candidate < current[end][0]:
                    current[end] = (candidate, start)
        costs.append(current)

    if total_sentences not in costs[-1]:
        raise ValueError("O capítulo não cabe em dez páginas de leitura equilibradas")
    boundaries = [total_sentences]
    for page_index in range(PAGE_COUNT_PER_CHAPTER, 0, -1):
        boundaries.append(costs[page_index][boundaries[-1]][1])
    return list(reversed(boundaries))


def _paragraphs(sentences: list[tuple[int, str]]) -> tuple[str, ...]:
    result: list[str] = []
    current_index = -1
    for paragraph_index, sentence in sentences:
        if paragraph_index != current_index:
            result.append(sentence)
            current_index = paragraph_index
        else:
            result[-1] = f"{result[-1]} {sentence}"
    return tuple(result)


@lru_cache(maxsize=1)
def get_book_pages() -> tuple[BookPage, ...]:
    pages: list[BookPage] = []
    chapters = sorted(CHAPTER_DIR.glob("[0-9][0-9].md"))
    if len(chapters) != 15:
        raise ValueError("O manuscrito precisa ter 15 capítulos")
    for chapter_number, chapter_path in enumerate(chapters, start=1):
        title, sentences = _split_chapter(chapter_path.read_text(encoding="utf-8"))
        bounds = _page_boundaries(sentences)
        for page_index in range(PAGE_COUNT_PER_CHAPTER):
            content = _paragraphs(sentences[bounds[page_index] : bounds[page_index + 1]])
            pages.append(
                BookPage(
                    number=len(pages) + 1,
                    chapter_number=chapter_number,
                    chapter_title=title,
                    chapter_start=page_index == 0,
                    paragraphs=content,
                    word_count=sum(len(paragraph.split()) for paragraph in content),
                )
            )
    return tuple(pages)
