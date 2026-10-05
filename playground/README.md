# Laboratório do Vazio

Experimento isolado em `/playground/`. Os arquivos públicos vivem em `dist/playground/`; nenhuma página, view, model ou folha de estilo existente é usada ou modificada.

O experimento **Constelação Programada** transforma comandos simples em um caminho no mapa. São três desafios de sequência, desvio e repetição. Ao vencer, o caminho vira uma constelação que pode ser salva como PNG. O progresso das missões é local ao navegador.

Testes do motor de regras:

```bash
node playground/engine.test.mjs
```

Para ver localmente, sirva `dist/` por HTTP e abra `/playground/`. O projeto Django usa UV, mas esta experiência não exige dependências extras.
