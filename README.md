# Homus Bananus: Guerra do Absurdo

Leitor responsivo em Django para o mangá, com 78 páginas canônicas divididas em três arcos e leitura contínua por arco.

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
- Clotilde é sempre uma pequena galinha robótica branca, de crista vermelha, bico laranja, olhos azuis luminosos, asas prateadas e pés mecânicos dourados.
- Versões intermediárias descartadas durante a criação não fazem parte do projeto.

Consulte `STORY_AUDIT.md` para as decisões editoriais e inconsistências encontradas.
