# Laboratório do Vazio

Experimento em `/playground/`, listado na categoria Jogos e na busca do catálogo. A página Django está em `reader/templates/reader/playground.html`; seu CSS e JavaScript próprios ficam em `reader/static/reader/playground/`. A exportação pública fica em `dist/playground/`.

O experimento **Constelação Programada** transforma comandos simples em um caminho no mapa. São três desafios de sequência, desvio e repetição. Ao vencer, o caminho vira uma constelação que pode ser salva como PNG. O progresso das missões é local ao navegador.

Testes do motor de regras:

```bash
node playground/engine.test.mjs
```

Para ver localmente, execute `uv run python manage.py runserver` ou sirva `dist/` por HTTP e abra `/playground/`. O experimento não exige dependências adicionais.
