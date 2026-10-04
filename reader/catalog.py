from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chapter:
    number: int
    slug: str
    title: str
    subtitle: str
    start_page: int
    end_page: int
    cover: str

    @property
    def page_count(self) -> int:
        return self.end_page - self.start_page + 1


@dataclass(frozen=True, slots=True)
class Arc:
    number: int
    slug: str
    title: str
    description: str
    cover: str
    start_page: int
    end_page: int
    chapters: tuple[Chapter, ...]

    @property
    def page_count(self) -> int:
        return self.end_page - self.start_page + 1


ARCS = (
    Arc(
        number=1,
        slug="invasao-desastrada",
        title="A Invasão Mais Desastrada da Terra",
        description=(
            "Alan, o Homus Bananus, chega à Terra decidido a conquistar tudo — e descobre "
            "que romance, vendas e rivalidade são bem mais perigosos que qualquer exército."
        ),
        cover="reader/images/covers/intro-arc.webp",
        start_page=1,
        end_page=17,
        chapters=(
            Chapter(
                1,
                "alien-caiu-do-ceu",
                "O Alien que Caiu do Céu",
                "Primeiro contato, péssima cantada.",
                1,
                6,
                "reader/images/pages/page-01.webp",
            ),
            Chapter(
                2,
                "guerra-das-calcinhas",
                "A Guerra das Calcinhas",
                "Alan contra Johnny: dignidade vendida separadamente.",
                7,
                12,
                "reader/images/pages/page-07.webp",
            ),
            Chapter(
                3,
                "agencia-clotilde",
                "A Agência e Clotilde",
                "Uma nova equipe e uma galinha robótica muito específica.",
                13,
                17,
                "reader/images/pages/page-13.webp",
            ),
        ),
    ),
    Arc(
        number=2,
        slug="palco-veludo-geraldo",
        title="O Palco Veludo de Geraldo",
        description=(
            "Um convite dourado leva a equipe até Geraldo, a Ilha Orfeu e o Projeto Veludo. "
            "O golpe vira guerra quando a corporação Vardo decide apagar todos os envolvidos."
        ),
        cover="reader/images/covers/geraldo-arc.webp",
        start_page=18,
        end_page=50,
        chapters=(
            Chapter(
                4,
                "convite-dourado",
                "O Convite Dourado",
                "Geraldo abre as portas do pior bom negócio do mundo.",
                18,
                23,
                "reader/images/pages/page-18.webp",
            ),
            Chapter(
                5,
                "ilha-orfeu",
                "Ilha Orfeu",
                "A corrida pelo verdadeiro Núcleo Veludo.",
                24,
                35,
                "reader/images/pages/page-24.webp",
            ),
            Chapter(
                6,
                "palco-veludo",
                "O Palco Veludo",
                "Traição, drones e uma aliança que ninguém pediu.",
                36,
                43,
                "reader/images/pages/page-36.webp",
            ),
            Chapter(
                7,
                "ultima-cortina",
                "A Última Cortina",
                "O aplauso vira arma e a Vardo mostra o tamanho da ameaça.",
                44,
                50,
                "reader/images/pages/page-44.webp",
            ),
        ),
    ),
)

MANGA = {
    "title": "Homus Bananus: Guerra do Absurdo",
    "tagline": "Conquistar a Terra era a parte fácil.",
    "description": (
        "Mangá brasileiro de comédia e ação sobre Alan, um alienígena fantasiado de banana, "
        "seus rivais improváveis e uma conspiração corporativa perigosamente teatral."
    ),
    "cover": "reader/images/covers/main-cover.webp",
}


def get_arc(slug: str) -> Arc | None:
    return next((arc for arc in ARCS if arc.slug == slug), None)


def get_chapter_for_page(page: int) -> Chapter | None:
    return next(
        (
            chapter
            for arc in ARCS
            for chapter in arc.chapters
            if chapter.start_page <= page <= chapter.end_page
        ),
        None,
    )
