"""Authored Python textbook pages and their stable lesson index."""

import html
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

PYTHON_BOOK = {
    "slug": "python-do-zero-ao-avancado",
    "title": "Python: do zero ao avançado",
    "author": "Voidwielder",
    "genre": "Livro didático · Programação",
    "detail": (
        "Aprenda lógica, algoritmos e Python desde o primeiro programa até POO, "
        "bibliotecas, automação, APIs, dados e machine learning, praticando no navegador."
    ),
    "topics": (
        "python programação iniciante avançado lógica algoritmos orientação objetos poo bibliotecas "
        "numpy pandas matplotlib fastapi httpx playwright bots automação empresas machine learning "
        "scikit-learn uv sqlite sqlalchemy pytest exercícios interativos"
    ),
    "url": "/livros/python-do-zero-ao-avancado/",
    "page_count": 281,
}
PARTS = (
    "Pensar como programador",
    "Primeiros passos em Python",
    "Decisões e repetição",
    "Coleções e texto",
    "Funções e organização",
    "Arquivos, erros e testes",
    "Orientação a objetos",
    "Python avançado",
    "Biblioteca padrão",
    "Dados e visualização",
    "Web e automação",
    "Machine learning",
    "Empresas e projeto final",
)
ROOT = Path(__file__).resolve().parent / "books" / "python"
INLINE_CODE = re.compile(r"`([^`]+)`")


def _rich_text(source: str) -> str:
    blocks = re.split(r"(```(?:python|text)?\n[\s\S]*?\n```)", source.strip())
    rendered: list[str] = []
    for block in blocks:
        if not block.strip():
            continue
        if block.startswith("```"):
            code = block.split("\n", 1)[1].rsplit("\n```", 1)[0]
            rendered.append(f"<pre><code>{html.escape(code)}</code></pre>")
        else:
            for paragraph in block.strip().split("\n\n"):
                escaped = html.escape(" ".join(paragraph.splitlines()))
                formatted = INLINE_CODE.sub(lambda match: f"<code>{match.group(1)}</code>", escaped)
                rendered.append(f"<p>{formatted}</p>")
    return "".join(rendered)


def _manuscript(source: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """Parse Markdown headings outside fenced code blocks."""
    lessons: list[tuple[str, list[tuple[str, str]]]] = []
    title = ""
    pages: list[tuple[str, str]] = []
    section = ""
    body: list[str] = []
    in_code = False
    for line in source.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("# "):
            if section:
                pages.append((section, "\n".join(body).strip()))
                section, body = "", []
            if title:
                lessons.append((title, pages))
                pages = []
            title = line[2:].strip()
        elif not in_code and line.startswith("## "):
            if section:
                pages.append((section, "\n".join(body).strip()))
                body = []
            section = line[3:].strip()
        elif section:
            body.append(line)
    if section:
        pages.append((section, "\n".join(body).strip()))
    if title:
        lessons.append((title, pages))
    return lessons


@dataclass(frozen=True)
class PythonPage:
    number: int
    part_number: int
    part_title: str
    lesson_number: int
    lesson_title: str
    section_title: str
    body: str
    body_html: str
    diagram: str

    def as_json(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True)
class PythonLesson:
    number: int
    part_number: int
    part_title: str
    title: str
    start_page: int


@lru_cache(maxsize=1)
def get_python_pages() -> tuple[PythonPage, ...]:
    pages: list[PythonPage] = []
    front = _manuscript("# Antes de começar\n" + (ROOT / "front.md").read_text(encoding="utf-8"))
    if len(front) != 1 or len(front[0][1]) != 8:
        raise ValueError("A abertura precisa ter oito páginas")
    for section, body in front[0][1]:
        pages.append(PythonPage(len(pages) + 1, 0, "Abertura", 0, "Antes de começar", section, body, _rich_text(body), ""))

    part_files = sorted((ROOT / "parts").glob("[0-9][0-9].md"))
    if len(part_files) != len(PARTS):
        raise ValueError("O livro precisa ter treze partes")
    lesson_number = 0
    for part_number, path in enumerate(part_files, start=1):
        lessons = _manuscript(path.read_text(encoding="utf-8"))
        if len(lessons) != 3:
            raise ValueError(f"{path.name}: cada parte precisa ter três lições")
        for lesson_index, (lesson_title, sections) in enumerate(lessons, start=1):
            lesson_number += 1
            if len(sections) != 7:
                raise ValueError(f"{path.name}: {lesson_title} precisa ter sete páginas")
            for section_index, (section_title, body) in enumerate(sections):
                if len(re.sub(r"```[\s\S]*?```", "", body).split()) < 35:
                    raise ValueError(f"Página curta em {path.name}: {section_title}")
                diagram = ""
                if section_index == 0:
                    diagram = {
                        (1, 1): "algoritmo", (3, 1): "condicao", (7, 1): "objeto",
                        (10, 1): "array", (11, 3): "bot", (12, 1): "ml",
                    }.get((part_number, lesson_index), "")
                pages.append(PythonPage(
                    len(pages) + 1, part_number, PARTS[part_number - 1], lesson_number,
                    lesson_title, section_title, body, _rich_text(body), diagram,
                ))
    if len(pages) != PYTHON_BOOK["page_count"]:
        raise ValueError("O número de páginas não corresponde à ficha do livro")
    return tuple(pages)


@lru_cache(maxsize=1)
def get_python_lessons() -> tuple[PythonLesson, ...]:
    return tuple(
        PythonLesson(page.lesson_number, page.part_number, page.part_title, page.lesson_title, page.number)
        for page in get_python_pages()
        if page.lesson_number and (page.number == 9 or get_python_pages()[page.number - 2].lesson_number != page.lesson_number)
    )
