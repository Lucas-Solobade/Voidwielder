"""Stable page and lesson index for the original Linux textbook."""

import html
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

LINUX_BOOK = {
    "slug": "linux-do-zero-ao-avancado",
    "title": "Linux: do zero ao avançado",
    "author": "Voidwielder",
    "genre": "Livro didático · Tecnologia",
    "detail": (
        "Um caminho guiado para começar no Linux e avançar até redes, segurança, "
        "automação, contêineres e desenvolvimento, com práticas em laboratório."
    ),
    "topics": (
        "linux sistema operacional iniciante avançado terminal bash comandos ubuntu debian "
        "fedora kernel rede segurança programação administração virtualização livro didático"
    ),
    "url": "/livros/linux-do-zero-ao-avancado/",
    "page_count": 554,
}
PARTS = (
    "Fundamentos e história",
    "Instalação e desktop",
    "Terminal e arquivos",
    "Texto, busca e fluxos",
    "Permissões e usuários",
    "Programas e atualizações",
    "Processos e serviços",
    "Discos e backup",
    "Redes",
    "Segurança e operação",
    "Bash e automação",
    "Sistema avançado",
    "Desenvolvimento e futuro",
)
ROOT = Path(__file__).resolve().parent / "books" / "linux"
INLINE_CODE = re.compile(r"`([^`]+)`")


def _html(body: str) -> str:
    """Format trusted, local manuscript text after escaping every character."""
    escaped = html.escape(body)
    return INLINE_CODE.sub(lambda match: f"<code>{match.group(1)}</code>", escaped)


@dataclass(frozen=True)
class LinuxPage:
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
class LinuxLesson:
    number: int
    part_number: int
    part_title: str
    title: str
    start_page: int


def _sections(source: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^## (.+)$", source, re.MULTILINE))
    return [
        (match.group(1).strip(), source[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(source)].strip())
        for index, match in enumerate(matches)
    ]


@lru_cache(maxsize=1)
def get_linux_pages() -> tuple[LinuxPage, ...]:
    pages: list[LinuxPage] = []
    front = _sections((ROOT / "front.md").read_text(encoding="utf-8"))
    if len(front) != 8:
        raise ValueError("A abertura precisa ter oito páginas")
    for title, body in front:
        pages.append(LinuxPage(len(pages) + 1, 0, "Abertura", 0, "Antes de começar", title, body, _html(body), ""))

    part_files = sorted((ROOT / "parts").glob("[0-9][0-9].md"))
    if len(part_files) != len(PARTS):
        raise ValueError("O livro precisa ter treze partes")
    lesson_number = 0
    for part_number, path in enumerate(part_files, start=1):
        source = path.read_text(encoding="utf-8")
        lessons = list(re.finditer(r"^# (.+)$", source, re.MULTILINE))
        if len(lessons) != 6:
            raise ValueError(f"{path.name}: cada parte precisa de seis lições")
        for index, match in enumerate(lessons):
            lesson_number += 1
            title = match.group(1).strip()
            block = source[match.end() : lessons[index + 1].start() if index + 1 < len(lessons) else len(source)]
            sections = _sections(block)
            if len(sections) != 7:
                raise ValueError(f"{path.name}: {title} precisa de sete páginas")
            for section_index, (section_title, body) in enumerate(sections):
                if len(body.split()) < 40:
                    raise ValueError(f"Página curta em {path.name}: {section_title}")
                diagram = ""
                if section_index == 0:
                    diagram = {(9, 1): "rede", (12, 1): "boot", (12, 4): "container"}.get(
                        (part_number, index + 1), ""
                    )
                pages.append(
                    LinuxPage(
                        len(pages) + 1, part_number, PARTS[part_number - 1], lesson_number,
                        title, section_title, body, _html(body), diagram,
                    )
                )
    if len(pages) != LINUX_BOOK["page_count"]:
        raise ValueError("O número de páginas não corresponde à ficha do livro")
    return tuple(pages)


@lru_cache(maxsize=1)
def get_linux_lessons() -> tuple[LinuxLesson, ...]:
    return tuple(
        LinuxLesson(page.lesson_number, page.part_number, page.part_title, page.lesson_title, page.number)
        for page in get_linux_pages()
        if page.lesson_number and (page.number == 9 or get_linux_pages()[page.number - 2].lesson_number != page.lesson_number)
    )
