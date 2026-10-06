# Voidwielder

Portal responsivo em Django para HQs, livros, jogos e materiais de estudo. O catálogo atual inclui a HQ *Homus Bananus: Guerra do Absurdo*, com 96 páginas em quatro arcos, uma trilha de seis semanas de Lógica de Programação e Algoritmos e os jogos *Pipo e o Correio das Estrelas*, *Mila e o Jardim das Nuvens* e *Lilo e o Festival das Bolhas*.

As categorias de livros e jogos têm navegação e pesquisa próprias. Novos itens podem ser adicionados ao catálogo sem alterar o menu principal.

## Jogo: Pipo e o Correio das Estrelas

Platformer infantil feito com Canvas API, sem imagens ou bibliotecas gráficas externas. Pipo entrega cartas brilhantes em três fases: **Jardim Lunar**, **Arquipélago de Algodão** e **Observatório do Cochilo**. O chefe final, **Rabugão das Nuvens**, avisa antes de atacar, cansa após as ondas e muda de padrão quando perde energia.

- **Teclado:** A/D ou setas para mover; Espaço para pular; X para o sopro de estrelas; Esc para pausar; Enter nos menus.
- **Toque:** botões de direção, pulo e sopro aparecem em telas menores.
- **Sopro:** atordoa criaturas próximas; durante a pausa do chefe, é a forma de acordá-lo. Recarrega automaticamente.
- **Arquivos:** `reader/templates/reader/game.html` contém a página; `reader/static/reader/css/game.css` define o layout; `reader/static/reader/js/game/` contém fases, arte procedural e lógica de jogo.

Com o servidor iniciado, abra `/jogos/pipo-e-o-correio-das-estrelas/`. O progresso entre fases fica salvo somente no navegador atual.

## Jogo: Mila e o Jardim das Nuvens

Aventura infantil de três jardins desenhada com Canvas API. Mila recolhe sementinhas luminosas e acorda flores, sem cronômetro ou vidas. Use as setas ou WASD no teclado; no celular, use os botões de direção ou deslize o dedo no jardim. O progresso fica salvo no navegador atual.

Abra `/jogos/mila-e-o-jardim-das-nuvens/` ou selecione o jogo na categoria Jogos. A lógica das fases está em `reader/static/reader/js/garden/core.mjs` e pode ser verificada com `node tests/garden.test.mjs`.

## Jogo: Lilo e o Festival das Bolhas

Em seis fases, Lilo solta bolhas de luz que brilham em cruz após três batidas. A luz abre nuvens macias e acorda visitantes sonolentos. Recolha as estrelas e alcance o portal; a última fase traz a Rainha Névoa, com escudo alternado e um vento anunciado antes de soprar. A luz apenas devolve Lilo ao início da fase, sem tirar o progresso.

Use setas ou WASD para mover, Espaço para colocar a bolha e Esc para pausar. No celular, há botões de direção e bolha, além de gestos sobre o tabuleiro. Abra `/jogos/lilo-e-o-festival-das-bolhas/`. A lógica pura fica em `reader/static/reader/js/bubbles/core.mjs` e o progresso local desbloqueia fases sem conta.

## Executar com UV

```bash
uv sync
uv run python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

## Qualidade

```bash
uv run ruff check .
uv run pytest
uv run python manage.py check
```

## Produção

Defina as variáveis descritas em `.env.example`, use `DJANGO_DEBUG=False` e execute:

```bash
uv run python manage.py collectstatic --noinput
```

O WhiteNoise entrega os arquivos estáticos com nomes versionados e compressão.

## HQ publicada

- Arco 1 — páginas 1–17: `A Invasão Mais Desastrada da Terra`.
- Arco 2 — páginas 18–50: `O Palco Veludo de Geraldo`.
- Arco 3 — páginas 51–78: `Faze Azul: O Beat Contra a Vardo`.
- Arco 4 — páginas 79–96: `A Última Poda: O Fim da Vardo`.
- Clotilde é sempre uma pequena galinha robótica branca, de crista vermelha, bico laranja, olhos azuis luminosos, asas prateadas e pés mecânicos dourados.
- Versões intermediárias descartadas durante a criação não fazem parte do projeto.

Consulte `STORY_AUDIT.md` para as decisões editoriais e inconsistências encontradas.

## Versão pública estática

O projeto conserva o código Django como fonte. O comando a seguir exporta o catálogo,
o leitor e as páginas ilustradas para `dist/`, usado na hospedagem pública:

```bash
SITE_ORIGIN=https://voidwielder.alves-lucas0200.chatgpt.site \
  uv run python scripts/export_static.py
```

O GitHub Pages publica automaticamente a mesma versão estática em
`https://lucas-solobade.github.io/Voidwielder/` a cada envio para `main`.
O workflow em `.github/workflows/pages.yml` gera o site com
`SITE_ORIGIN=https://lucas-solobade.github.io/Voidwielder`, incluindo o
prefixo `/Voidwielder/` nos links e arquivos estáticos. O código Django
continua sendo a fonte das páginas; o Pages serve o resultado exportado.
