# Homus Bananus: Guerra do Absurdo

Leitor responsivo em Django para o mangá, com 96 páginas canônicas divididas em quatro arcos e leitura contínua por arco.

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

## Cânone utilizado

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
SITE_ORIGIN=https://homus-bananus-guerra-do-absurdo.alves-lucas0200.chatgpt.site \
  uv run python scripts/export_static.py
```
