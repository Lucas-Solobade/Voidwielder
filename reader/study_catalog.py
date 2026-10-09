"""Search metadata for the beginner study track."""

STUDY_GUIDE = {
    "title": "Lógica de Programação e Algoritmos",
    "detail": "Roteiro para iniciantes em seis semanas: lógica, Python, decisões, laços, funções, coleções e um projeto de forca.",
    "topics": (
        "algoritmo pseudocódigo fluxograma",
        "print input variáveis tipos strings operações",
        "if else elif decisões booleanos",
        "while for repetição contador acumulador",
        "funções parâmetros retorno exceções",
        "tuplas listas dicionários métodos forca",
    ),
}

STUDY_PROJECTS = (
    {
        "title": STUDY_GUIDE["title"],
        "kind": "Trilha guiada",
        "subject": "Programação",
        "detail": STUDY_GUIDE["detail"],
        "meta": "6 semanas · Python · projeto final",
        "url": "/estudos/logica-de-programacao-e-algoritmos/",
        "image": "reader/images/studies/logic.svg",
        "topics": " ".join(STUDY_GUIDE["topics"]),
    },
    {
        "title": "Escalonador do Vazio",
        "kind": "Simulador interativo",
        "subject": "Sistemas operacionais",
        "detail": "Compare FCFS, SJF e Round Robin e acompanhe a CPU em uma linha do tempo visual.",
        "meta": "CPU · algoritmos · tempo de espera",
        "url": "/experiencias/escalonador-do-vazio/",
        "image": "reader/images/studies/scheduler.svg",
        "topics": "processos escalonamento FCFS SJF Round Robin sistemas operacionais",
    },
    {
        "title": "Abismo da Recursão",
        "kind": "Laboratório interativo",
        "subject": "Algoritmos",
        "detail": "Explore fatorial, Fibonacci e Euclides passo a passo, com chamadas e retornos na pilha.",
        "meta": "Recursão · pilha · casos-base",
        "url": "/experiencias/abismo-da-recursao/",
        "image": "reader/images/studies/recursion.svg",
        "topics": "recursão recursividade fatorial Fibonacci Euclides pilha chamadas caso-base",
    },
    {
        "title": "Labirinto da Memória",
        "kind": "Simulador interativo",
        "subject": "Sistemas operacionais",
        "detail": "Compare FIFO, LRU e Ótimo e acompanhe acertos, faltas e substituições nos quadros da memória.",
        "meta": "Memória virtual · páginas · FIFO · LRU",
        "url": "/experiencias/labirinto-da-memoria/",
        "image": "reader/images/studies/memory.svg",
        "topics": "memória virtual paginação substituição de páginas FIFO LRU ótimo faltas de página quadros",
    },
)
