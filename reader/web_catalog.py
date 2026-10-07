"""The web development textbook, paginated without dropping manuscript blocks."""

import html
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

MANUSCRIPT = Path(__file__).resolve().parent / "books" / "web" / "manuscript.md"
PARTS = ("Iniciante", "Intermediário", "Avançado")
INLINE = re.compile(r"`([^`]+)`|\[([^]]+)\]\((https://[^)\s]+)\)|\*\*([^*]+)\**")
CHAPTER = re.compile(r"^(\d+)\.\s+(.+)$")
DIAGRAMS = {1: "request", 3: "semantic", 4: "layout", 5: "dom", 10: "api", 11: "database", 14: "security", 16: "deploy"}


def _inline(source: str) -> str:
    result: list[str] = []
    start = 0
    for match in INLINE.finditer(source):
        result.append(html.escape(source[start : match.start()]))
        if match.group(1) is not None:
            result.append(f"<code>{html.escape(match.group(1))}</code>")
        elif match.group(2) is not None:
            label, url = html.escape(match.group(2)), html.escape(match.group(3), quote=True)
            result.append(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>')
        else:
            result.append(f"<strong>{html.escape(match.group(4))}</strong>")
        start = match.end()
    result.append(html.escape(source[start:]))
    return "".join(result)


@dataclass(frozen=True)
class Block:
    kind: str
    source: str
    body_html: str

    @property
    def weight(self) -> int:
        return min(len(self.source), 850) if self.kind == "code" else len(self.source)


def _block(lines: list[str]) -> Block | None:
    if not lines or not "".join(lines).strip():
        return None
    source = "\n".join(lines).strip()
    if source.startswith("```"):
        first, _, remainder = source.partition("\n")
        language = first[3:].strip().upper() or "CÓDIGO"
        code = remainder.rsplit("\n```", 1)[0]
        return Block("code", source, f'<div class="web-code"><span>{html.escape(language)}</span><pre><code>{html.escape(code)}</code></pre></div>')
    if source.startswith("| "):
        rows = [line.strip().strip("|").split("|") for line in lines if line.strip().startswith("|")]
        if len(rows) >= 2:
            headings = "".join(f"<th>{_inline(cell.strip())}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{_inline(cell.strip())}</td>" for cell in row) + "</tr>" for row in rows[2:])
            return Block("table", source, f'<div class="web-table"><table><thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>')
    if all(line.startswith("- ") for line in lines):
        items = "".join(f"<li>{_inline(line[2:])}</li>" for line in lines)
        return Block("list", source, f"<ul>{items}</ul>")
    paragraph = " ".join(line.strip() for line in lines)
    kind = "answer" if paragraph.startswith("**Conferência:**") else "exercise" if paragraph.startswith("**Exercício") else "paragraph"
    return Block(kind, source, f"<p>{_inline(paragraph)}</p>")


def _blocks(lines: list[str]) -> list[Block]:
    blocks: list[Block] = []
    pending: list[str] = []
    fenced = False

    def flush() -> None:
        block = _block(pending)
        if block is not None:
            if block.kind == "answer" and blocks and blocks[-1].kind == "exercise":
                exercise = blocks.pop()
                blocks.append(Block("exercise", exercise.source + "\n\n" + block.source,
                                    f'<div class="web-exercise">{exercise.body_html}<details><summary>Conferir resposta</summary>{block.body_html}</details></div>'))
            else:
                blocks.append(block)
        pending.clear()

    for line in lines:
        if line.startswith("```"):
            if not fenced:
                flush()
                fenced = True
                pending.append(line)
            else:
                pending.append(line)
                fenced = False
                flush()
        elif fenced:
            pending.append(line)
        elif not line.strip() or line.strip() == "---":
            flush()
        elif pending and ((line.startswith("- ") and not pending[0].startswith("- ")) or
                          (pending[0].startswith("- ") and not line.startswith("- ")) or
                          (line.startswith("| ") and not pending[0].startswith("| ")) or
                          (pending[0].startswith("| ") and not line.startswith("| "))):
            flush()
            pending.append(line)
        else:
            pending.append(line)
    flush()
    if fenced:
        raise ValueError("Bloco de código sem fechamento no manuscrito")
    return blocks


def _sections(source: str) -> list[tuple[int, int, str, list[Block]]]:
    sections: list[tuple[int, int, str, list[Block]]] = []
    part = chapter = 0
    title = "Apresentação"
    lines: list[str] = []
    fenced = False

    def flush() -> None:
        blocks = _blocks(lines)
        if blocks:
            sections.append((part, chapter, title, blocks))
        lines.clear()

    for line in source.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("# Parte "):
            flush()
            part += 1
            chapter = 0
            title = ""
        elif not fenced and line.startswith("## "):
            flush()
            heading = line[3:].strip()
            match = CHAPTER.match(heading)
            if match:
                chapter = int(match.group(1))
                title = match.group(2).replace("`", "")
            else:
                chapter = 0
                title = heading
        elif not fenced and line.startswith("# Desenvolvimento web,"):
            continue
        else:
            lines.append(line)
    flush()
    return sections


@dataclass(frozen=True)
class WebPage:
    number: int
    part_number: int
    part_title: str
    chapter_number: int
    chapter_title: str
    section_title: str
    body_html: str
    plain_text: str
    diagram: str

    def as_json(self) -> dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True)
class WebSection:
    part_number: int
    part_title: str
    chapter_number: int
    title: str
    start_page: int


@lru_cache(maxsize=1)
def get_web_pages() -> tuple[WebPage, ...]:
    pages: list[WebPage] = []
    chapters: set[int] = set()
    for part, chapter, title, blocks in _sections(MANUSCRIPT.read_text(encoding="utf-8")):
        if chapter:
            chapters.add(chapter)
        groups: list[list[Block]] = []
        current: list[Block] = []
        weight = 0
        for block in blocks:
            limit = 480 if not groups and chapter in DIAGRAMS else 830
            if current and (block.kind == "code" or weight + block.weight > limit or len(current) >= 3):
                groups.append(current)
                current, weight = [], 0
            current.append(block)
            weight += block.weight
            if block.kind == "code":
                groups.append(current)
                current, weight = [], 0
        if current:
            groups.append(current)
        for index, group in enumerate(groups):
            pages.append(WebPage(
                number=len(pages) + 1,
                part_number=part if chapter else 4 if part == 3 else 0,
                part_title=PARTS[part - 1] if chapter else "Referências" if part == 3 else "Abertura",
                chapter_number=chapter,
                chapter_title=title,
                section_title=title if index == 0 else f"{title} · continuação",
                body_html="".join(block.body_html for block in group),
                plain_text=" ".join(block.source for block in group),
                diagram=DIAGRAMS.get(chapter, "") if index == 0 else "",
            ))
    if chapters != set(range(1, 18)):
        raise ValueError("O livro precisa conter os 17 capítulos completos")
    return tuple(pages)


@lru_cache(maxsize=1)
def get_web_sections() -> tuple[WebSection, ...]:
    seen: set[tuple[int, str]] = set()
    result: list[WebSection] = []
    for page in get_web_pages():
        identity = (page.chapter_number, page.chapter_title)
        if identity in seen:
            continue
        seen.add(identity)
        result.append(WebSection(page.part_number, page.part_title, page.chapter_number,
                                 page.chapter_title, page.number))
    return tuple(result)


WEB_BOOK = {
    "slug": "desenvolvimento-web-do-zero-ao-avancado",
    "title": "Desenvolvimento web: do primeiro arquivo à produção",
    "author": "Voidwielder",
    "genre": "Livro didático · Desenvolvimento web",
    "detail": "HTML, CSS, JavaScript, Git, APIs, bancos de dados, testes, segurança e publicação em um projeto guiado do início ao fim.",
    "topics": "web front-end backend html css javascript git api banco dados acessibilidade responsivo segurança deploy iniciante intermediário avançado",
    "url": "/livros/desenvolvimento-web-do-zero-ao-avancado/",
    "page_count": len(get_web_pages()),
}
