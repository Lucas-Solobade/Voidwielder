# Desenvolvimento web, do primeiro arquivo à produção

**Um livro didático em três etapas: iniciante, intermediária e avançada**

Edição de 6 de outubro de 2026 · Português brasileiro

Este livro ensina a construir uma aplicação web pequena de ponta a ponta. A aplicação de exemplo, **Tarefas**, começa como uma página estática, ganha interação no navegador e depois uma API. O objetivo não é decorar ferramentas: é entender o que cada parte faz, reconhecer falhas e saber onde investigar.

**Como estudar.** Leia um capítulo, execute o exemplo, faça o exercício sem olhar a resposta e registre em Git o que funcionou. Use um servidor HTTP local para testar páginas com módulos, `fetch` ou armazenamento; abrir um HTML por `file://` pode produzir um comportamento diferente. Os comandos pressupõem um terminal com Git e Node.js instalados; caminhos e comandos para criar pastas variam entre sistemas. Nenhum framework específico é necessário.

## Roteiro

| Etapa | Capítulos | Você será capaz de |
| --- | --- | --- |
| Iniciante | 1–6 | Explicar o caminho de uma requisição e criar uma página responsiva, acessível e interativa. |
| Intermediária | 7–12 | Colaborar com Git, consumir e criar uma API, persistir dados e testar o fluxo principal. |
| Avançada | 13–17 | Projetar autenticação, reduzir riscos, medir desempenho, publicar e operar uma aplicação. |

Ao fim de cada etapa há um projeto de consolidação. O gabarito é uma orientação para conferir o raciocínio, não uma solução única.

---

# Parte I — Iniciante

## 1. O que acontece quando você abre um site

Uma **URL** identifica um recurso. O navegador localiza o servidor, faz uma requisição HTTP e recebe uma resposta com status, cabeçalhos e, muitas vezes, um corpo. Se o corpo for HTML, o navegador lê sua estrutura, busca CSS, JavaScript e imagens referenciados e desenha a página. O JavaScript do cliente pode pedir mais dados sem recarregar tudo. [Visão geral de HTTP — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview).

```
Pessoa → navegador → GET /tarefas → servidor
Pessoa ← página desenhada ← 200 + HTML ← servidor
                            ↘ CSS / JS / imagens
```

**HTML** descreve conteúdo e significado; **CSS** define apresentação; **JavaScript** implementa comportamento. O **servidor** recebe requisições, aplica regras e pode ler um **banco de dados**. O navegador não deve ser tratado como fonte confiável: qualquer pessoa pode editar uma requisição antes de enviá-la.

Exemplos de respostas: `200` indica sucesso; `201`, criação; `400`, pedido inválido; `401`, autenticação necessária; `403`, acesso negado; `404`, recurso não encontrado; `500`, erro interno. O mesmo status pode aparecer em aplicações diferentes; leia também a resposta e os logs. HTTP é sem estado por natureza: a identidade entre requisições depende de mecanismos como cookies ou tokens.

**Experimento.** Abra as ferramentas de desenvolvedor do navegador, aba **Network/Rede**, e recarregue uma página. Identifique o documento HTML, um CSS, um JavaScript, o status de cada pedido e o tamanho transferido. Depois, na aba **Elements/Elementos**, compare o DOM exibido com o HTML original.

**Exercício 1.** Uma página mostra o título, mas não aplica estilos. Cite três verificações objetivas.

**Conferência:** caminho do CSS no HTML, resposta da requisição CSS na aba Rede, erro de sintaxe ou seletor CSS na aba Estilos.

## 2. Preparar o ambiente sem depender de ferramentas mágicas

Crie uma pasta `tarefas-web` com três arquivos: `index.html`, `style.css` e `app.js`. Abra-a em um editor de texto que preserve UTF-8. No terminal, confirme `git --version` e `node --version`. Para servir a pasta localmente, um exemplo simples é `python -m http.server 8000 --bind 127.0.0.1`, se Python estiver disponível. Digite `http://127.0.0.1:8000/` no navegador manualmente e encerre o servidor com `Ctrl+C` ao terminar. Use outra porta livre se necessário.

O editor ajuda a escrever; o navegador executa e exibe; o terminal executa comandos; Git registra versões. Quando algo falhar, localize em qual dessas camadas está o problema antes de instalar outra ferramenta.

**Exercício 2.** Visite `/pagina-inexistente` no servidor local. Qual status aparece na Rede? O erro é do HTML, do JavaScript ou da rota solicitada?

**Conferência:** em um servidor estático usual, `404`; a rota não encontrou arquivo correspondente.

## 3. HTML: estrutura, semântica e formulários

Use elementos pelo papel que desempenham. `header`, `nav`, `main`, `section`, `article` e `footer` estruturam a página; `button` executa uma ação; `a` navega; `label` nomeia um campo. Uma `div` não substitui automaticamente um botão. Isso ajuda teclado, leitores de tela, manutenção e testes. [Módulo de HTML semântico — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content).

Crie `index.html`:

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tarefas</title>
    <link rel="stylesheet" href="style.css">
    <script src="app.js" defer></script>
  </head>
  <body>
    <header class="cabecalho">
      <h1>Minhas tarefas</h1>
      <p>Uma coisa de cada vez.</p>
    </header>
    <main>
      <form id="form-tarefa">
        <label for="nova-tarefa">Nova tarefa</label>
        <div class="linha">
          <input id="nova-tarefa" name="titulo" required maxlength="80"
                 autocomplete="off">
          <button type="submit">Adicionar</button>
        </div>
      </form>
      <p id="estado" role="status" aria-live="polite"></p>
      <section aria-labelledby="titulo-lista">
        <h2 id="titulo-lista">Lista</h2>
        <ul id="lista-tarefas"></ul>
      </section>
    </main>
  </body>
</html>
```

`lang` informa o idioma; `viewport` ajusta a área em telas pequenas; `defer` executa o script depois que o HTML foi analisado. O atributo `required` ajuda o usuário, mas não substitui a validação no servidor. O `label` está associado ao `input` por `for` e `id`. O par `role="status"`/`aria-live` anuncia mensagens sem exigir que o foco mude.

Evite pular níveis de título por aparência; ajuste a aparência no CSS. Toda imagem informativa precisa de texto alternativo útil; imagens puramente decorativas podem usar `alt=""`. [Formulários HTML — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_forms).

**Exercício 3.** Acrescente um rodapé com uma frase e um link para uma página de ajuda. Teste a navegação com Tab e Enter.

**Conferência:** use `footer` e `a href="..."`; o link recebe foco e funciona sem JavaScript.

## 4. CSS: caixa, fluxo e layout responsivo

Cada elemento ocupa uma caixa: conteúdo, `padding`, borda e margem. `box-sizing: border-box` torna mais previsível a largura declarada. Layout responsivo não é “diminuir tudo”: é permitir que o conteúdo reorganize a largura disponível. [CSS básico — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics); [Layout CSS — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout).

Crie `style.css`:

```css
:root {
  color-scheme: light;
  font: 100%/1.5 system-ui, sans-serif;
  background: #f4f6f8;
  color: #18232d;
}

* { box-sizing: border-box; }
body { margin: 0; }
.cabecalho { padding: 2rem max(1rem, calc((100% - 42rem) / 2));
             background: #17324d; color: #fff; }
main { width: min(100% - 2rem, 42rem); margin: 2rem auto; }
.linha { display: flex; gap: .5rem; }
input { min-width: 0; flex: 1; }
input, button { font: inherit; padding: .7rem; border-radius: .35rem; }
input { border: 1px solid #82929e; }
button { border: 0; background: #075fa9; color: white; cursor: pointer; }
button:hover { background: #084f8b; }
button:focus-visible, input:focus-visible {
  outline: 3px solid #e59013; outline-offset: 2px;
}
ul { list-style: none; padding: 0; }
li { display: flex; align-items: center; gap: .75rem;
     padding: .65rem 0; border-bottom: 1px solid #ccd5db; }
li span { flex: 1; overflow-wrap: anywhere; }
.concluida span { text-decoration: line-through; color: #52616d; }

@media (max-width: 30rem) {
  .linha { flex-direction: column; }
  .cabecalho { padding: 1.5rem 1rem; }
}
```

Teste em uma janela estreita, com zoom de 200% e com texto longo. `min-width: 0` permite que o campo flexível encolha; `overflow-wrap` impede que uma palavra longa estoure a linha. Contraste e foco visível importam tanto quanto a cor da marca.

**Exercício 4.** Retire temporariamente `min-width: 0` e digite uma palavra longa no campo. Compare o resultado em tela pequena; depois restaure a regra.

**Conferência:** o item flexível pode se recusar a encolher e causar transbordamento.

## 5. JavaScript: dados, eventos e DOM

Uma variável guarda um valor; uma função transforma ou usa valores; um evento liga uma ação do usuário ao programa. O **DOM** é a representação da página que o JavaScript consulta e modifica. Mantenha o dado em uma estrutura e redesenhe a parte necessária da interface a partir dele. Não construa HTML com `innerHTML` contendo texto digitado pelo usuário.

Crie `app.js`:

```js
const formulario = document.querySelector('#form-tarefa');
const campo = document.querySelector('#nova-tarefa');
const lista = document.querySelector('#lista-tarefas');
const estado = document.querySelector('#estado');
let tarefas = [];

function renderizar() {
  lista.replaceChildren();
  for (const tarefa of tarefas) {
    const item = document.createElement('li');
    const texto = document.createElement('span');
    const concluir = document.createElement('button');
    const remover = document.createElement('button');

    texto.textContent = tarefa.titulo;
    concluir.type = remover.type = 'button';
    concluir.textContent = tarefa.feita ? 'Desfazer' : 'Concluir';
    concluir.setAttribute('aria-label',
      `${tarefa.feita ? 'Desfazer' : 'Concluir'}: ${tarefa.titulo}`);
    remover.textContent = 'Remover';
    remover.setAttribute('aria-label', `Remover: ${tarefa.titulo}`);
    item.classList.toggle('concluida', tarefa.feita);

    concluir.addEventListener('click', () => {
      tarefas = tarefas.map(t => t.id === tarefa.id ? { ...t, feita: !t.feita } : t);
      renderizar();
    });
    remover.addEventListener('click', () => {
      tarefas = tarefas.filter(t => t.id !== tarefa.id);
      renderizar();
    });
    item.append(texto, concluir, remover);
    lista.append(item);
  }
  estado.textContent = `${tarefas.length} tarefa(s) na lista.`;
}

formulario.addEventListener('submit', evento => {
  evento.preventDefault();
  const titulo = campo.value.trim();
  if (!titulo) return;
  tarefas = [...tarefas, { id: crypto.randomUUID(), titulo, feita: false }];
  campo.value = '';
  campo.focus();
  renderizar();
});

renderizar();
```

O exemplo mantém tudo em memória: ao recarregar, a lista desaparece. Isso é intencional nesta etapa. `textContent` trata o título como texto; `crypto.randomUUID()` cria um identificador adequado para uma demonstração local em contexto seguro, como localhost ou HTTPS. Em produção, o servidor controla os identificadores persistidos.

**Exercício 5.** Conte quantas tarefas estão concluídas e mostre “2 de 5 concluídas” no elemento `#estado`.

**Conferência:** use `tarefas.filter(t => t.feita).length` e `tarefas.length`; chame a atualização após toda mudança.

## 6. Acessibilidade e depuração fazem parte do primeiro projeto

Uma interface acessível deve ser possível de entender e operar de maneiras diferentes. Comece com HTML semântico, rótulos, foco visível, teclado, mensagens claras e contraste. Teste o formulário somente com teclado: Tab percorre os controles; Enter adiciona a tarefa; os botões de cada item podem ser acionados com Enter ou Espaço. Inspecione também a árvore de acessibilidade. [Acessibilidade — MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility).

Quando o programa falhar, leia a primeira mensagem de erro útil no console e tente reproduzir a sequência mínima. Use um `console.log` temporário para saber que dados chegaram; use pontos de interrupção quando a ordem dos eventos importar. Para um bug visual, inspecione regras CSS computadas; para um pedido de rede, abra a aba Rede; para um dado que some, descubra onde ele deveria ser salvo.

**Projeto 1 — checklist pessoal.** Entregue os três arquivos acima com: adicionar, concluir, desfazer e remover; layout que caiba em 320 CSS pixels; rótulos compreensíveis por teclado/leitor de tela; mensagem de estado. Peça a outra pessoa para executar três ações sem instruções verbais. Anote onde ela hesitou e ajuste os rótulos.

**Critérios de aprovação:** nenhuma exceção no console; nenhum controle inacessível por teclado; texto longo não ultrapassa a tela; recarregar apaga dados conforme especificado. Registre o resultado em um commit Git. A parte seguinte ensina como preservar e compartilhar o estado.

---

# Parte II — Intermediária

## 7. Git: trabalhar sem perder o que funciona

Git registra mudanças em **commits**. Um commit útil representa uma unidade compreensível de trabalho e tem uma mensagem que explica o resultado. Um branch aponta para uma linha de desenvolvimento; mesclar integra históricos. Um repositório remoto facilita colaboração e cópia externa, mas não substitui backups. [Livro oficial do Git — ramificações](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).

Na pasta do projeto:

```sh
git init
git add index.html style.css app.js
git commit -m "Cria checklist acessível em HTML, CSS e JavaScript"
git switch -c melhoria/contador
# edite app.js
git status
git diff
git add app.js
git commit -m "Mostra quantidade de tarefas concluídas"
```

Antes de mesclar, execute o projeto e revise `git diff` ou `git show`. Em uma equipe, suba o branch, solicite revisão e integre após as verificações. Nunca coloque senha, token, chave privada ou arquivo `.env` real em um commit. Use `.gitignore` para arquivos locais e forneça um `.env.example` **sem** segredos.

**Exercício 7.** Crie um branch, melhore uma mensagem do formulário, faça o commit e identifique o hash com `git log --oneline -3`.

**Conferência:** `git status` deve mostrar a situação real; a mensagem deve permitir entender a mudança sem abrir o diff.

## 8. Estado persistente e separação de responsabilidades

No exemplo inicial, `tarefas` vive só na memória. Para uma ferramenta pessoal sem conta, `localStorage` pode guardar dados **não sensíveis** neste navegador. Guarde uma estrutura simples e valide o que ler: armazenamento pode estar vazio, ter uma versão antiga ou conter conteúdo inesperado. Nunca confunda `localStorage` com um banco compartilhado ou com um local seguro para segredos.

```js
const CHAVE = 'tarefas-v1';

function carregarTarefas() {
  try {
    const valor = JSON.parse(localStorage.getItem(CHAVE) ?? '[]');
    if (!Array.isArray(valor)) return [];
    return valor.filter(t => typeof t.id === 'string' &&
      typeof t.titulo === 'string' && typeof t.feita === 'boolean');
  } catch {
    return [];
  }
}

function salvarTarefas(tarefas) {
  try {
    localStorage.setItem(CHAVE, JSON.stringify(tarefas));
    return true;
  } catch {
    return false;
  }
}
```

Troque a declaração inicial por `let tarefas = carregarTarefas();`. Após cada alteração da lista, chame `salvarTarefas(tarefas)` antes de `renderizar()` e informe ao usuário se a gravação falhar. Para mais de um dispositivo, colaboração ou regras de negócio, passe a usar um servidor.

Separe funções de **dados** (`adicionarTarefa`, `concluirTarefa`) das funções de **interface** (`renderizar`). Isso permite testar regras sem criar elementos do DOM. Evite estado duplicado: se `quantidadeConcluida` pode ser calculada de `tarefas`, não a armazene em outro lugar sem motivo.

**Exercício 8.** Faça as tarefas sobreviverem ao recarregamento e simule um valor inválido no armazenamento pela aba Application/Armazenamento do navegador.

**Conferência:** a interface deve iniciar sem travar, mesmo que o valor não seja JSON válido.

## 9. Assincronia, `fetch` e a fronteira entre cliente e servidor

Uma chamada de rede leva tempo e pode falhar. `fetch` retorna uma Promise; `await` espera seu resultado dentro de uma função `async`. Uma resposta HTTP com status de erro não gera automaticamente uma exceção em `fetch`: verifique `response.ok`. [Fetch API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch).

```js
async function obterTarefas() {
  const resposta = await fetch('/api/tarefas', {
    headers: { Accept: 'application/json' }
  });
  if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
  return resposta.json();
}

async function atualizarLista() {
  estado.textContent = 'Carregando tarefas…';
  try {
    tarefas = await obterTarefas();
    renderizar();
  } catch (erro) {
    estado.textContent = 'Não foi possível carregar. Tente novamente.';
    console.error(erro);
  }
}
```

Para criar um item, o cliente envia `POST` com JSON; o servidor valida e responde com o registro criado. Atualização pode usar `PATCH`; remoção, `DELETE`. Métodos HTTP comunicam intenção, mas segurança depende da validação e da autorização no servidor. Se frontend e API estiverem em origens diferentes, haverá regras de **CORS**; não “resolva” isso liberando todas as origens sem entender o modelo de confiança.

**Exercício 9.** Inspecione uma requisição com status `404` e outra com `500`. O texto de erro mostrado à pessoa usuária deve conter detalhes internos do servidor?

**Conferência:** não. Dê uma mensagem útil e segura; registre detalhes para diagnóstico no servidor.

## 10. Uma API pequena com Node.js puro

Este servidor usa apenas o módulo nativo `node:http`. É um exercício executável, não uma receita de produção: os dados estão em memória e desaparecem ao reiniciar. Salve como `server.mjs` na mesma pasta dos três arquivos da Parte I, inicie com `node server.mjs` e abra `http://127.0.0.1:8000/`. [Programação no servidor — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps).

```js
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';

const tarefas = new Map();
const arquivos = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/style.css', ['style.css', 'text/css; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']]
]);

function json(res, status, dados) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8',
                          'cache-control': 'no-store' });
  res.end(JSON.stringify(dados));
}

async function corpoJson(req) {
  let texto = '';
  for await (const parte of req) {
    texto += parte;
    if (texto.length > 10_000) throw new Error('corpo grande');
  }
  return JSON.parse(texto);
}

createServer(async (req, res) => {
  try {
    const rota = new URL(req.url, 'http://127.0.0.1:8000').pathname;
    if (req.method === 'GET' && arquivos.has(rota)) {
      const [arquivo, tipo] = arquivos.get(rota);
      res.writeHead(200, { 'content-type': tipo });
      res.end(await readFile(new URL(arquivo, import.meta.url)));
      return;
    }
    if (rota === '/api/tarefas' && req.method === 'GET') {
      json(res, 200, [...tarefas.values()]);
      return;
    }
    if (rota === '/api/tarefas' && req.method === 'POST') {
      const entrada = await corpoJson(req);
      const titulo = typeof entrada?.titulo === 'string' ? entrada.titulo.trim() : '';
      if (!titulo || titulo.length > 80) {
        json(res, 400, { erro: 'Título inválido.' }); return;
      }
      const tarefa = { id: randomUUID(), titulo, feita: false };
      tarefas.set(tarefa.id, tarefa);
      json(res, 201, tarefa);
      return;
    }
    json(res, 404, { erro: 'Rota não encontrada.' });
  } catch (erro) {
    if (erro instanceof SyntaxError || erro.message === 'corpo grande') {
      json(res, 400, { erro: 'JSON inválido ou grande demais.' });
    } else {
      console.error(erro);
      json(res, 500, { erro: 'Falha interna.' });
    }
  }
}).listen(8000, '127.0.0.1', () => {
  console.log('Servidor: http://127.0.0.1:8000/');
});
```

O exemplo atende somente `GET` e `POST`. Não troque o `Map` por uma variável global maior para “persistir”; a etapa seguinte explica banco de dados. Antes de oferecer uma API pública, planeje autenticação, autorização, limites de entrada, observabilidade e testes. A rota está presa a `127.0.0.1` para estudo local.

**Exercício 10.** Use a aba Rede para enviar um título vazio e um título válido. Compare status e corpo. Depois reinicie o servidor e observe os dados.

**Conferência:** `400` para entrada inválida, `201` para criação válida; o `Map` volta vazio após reiniciar.

## 11. Banco de dados: modelo, consultas e mudanças

Um banco relacional guarda registros duráveis em tabelas. **Chave primária** identifica a linha; **índice** acelera consultas seletivas, mas custa escrita e espaço; **transação** agrupa alterações que precisam funcionar juntas. Para tarefas de várias pessoas, inclua o dono no modelo e em toda consulta autorizada.

```sql
CREATE TABLE tarefas (
  id TEXT PRIMARY KEY,
  usuario_id TEXT NOT NULL,
  titulo TEXT NOT NULL,
  feita BOOLEAN NOT NULL DEFAULT FALSE,
  criada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX tarefas_por_usuario_data
  ON tarefas (usuario_id, criada_em);

SELECT id, titulo, feita
FROM tarefas
WHERE usuario_id = ?
ORDER BY criada_em DESC
LIMIT 20;
```

O `?` representa um parâmetro no driver que adotar essa sintaxe; outras bibliotecas usam marcadores diferentes. Passe valores por parâmetros, nunca por concatenação de strings SQL. Filtrar apenas no navegador é insuficiente: a API deve associar o usuário autenticado ao pedido e filtrar no servidor. Uma **migração** versiona mudanças de estrutura: planeje como aplicar e, quando possível, como reverter ou corrigir uma mudança malsucedida.

**Exercício 11.** Se a API recebe `/api/tarefas/123`, por que consultar apenas `WHERE id = ?` pode ser uma falha?

**Conferência:** outro usuário pode tentar o mesmo ID; a consulta e a autorização precisam verificar o proprietário.

## 12. Testes que comprovam comportamento

Um **teste unitário** verifica uma regra isolada; um **teste de integração** verifica componentes em conjunto; um **teste de ponta a ponta** percorre a aplicação como uma pessoa usuária. Poucos testes bem escolhidos protegem mais que muitos testes que apenas repetem o código de produção. Teste também o caminho de erro.

Extraia uma regra pura:

```js
// regras.mjs
export function tituloValido(valor) {
  return typeof valor === 'string' &&
    valor.trim().length >= 1 && valor.trim().length <= 80;
}
```

```js
// regras.test.mjs — execute com: node --test regras.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { tituloValido } from './regras.mjs';

test('aceita título útil e rejeita vazio ou longo', () => {
  assert.equal(tituloValido('  pagar conta  '), true);
  assert.equal(tituloValido('   '), false);
  assert.equal(tituloValido('a'.repeat(81)), false);
});
```

No exemplo do servidor, o teste esperado para criar uma tarefa deve verificar status `201`, formato da resposta e presença no `GET`. Também teste um `POST` malformado e o reinício do servidor. Em uma equipe, rode esses testes antes da integração no branch principal.

**Projeto 2 — tarefas com API.** Evolua o Projeto 1: substitua o armazenamento do navegador pela API, adicione leitura/criação e, como extensão, conclusão/remoção. Salve dados em um banco à sua escolha, use consultas parametrizadas e defina quem pode ver cada tarefa. Se não implementar contas nesta etapa, declare que o projeto é de **um único usuário local**; não simule isolamento que ainda não existe. Entregue instruções de execução, esquema do banco, testes e uma lista dos riscos ainda abertos.

**Critérios de aprovação:** o HTML continua acessível; falhas de rede são mostradas sem travar a interface; uma entrada vazia recebe erro; dados persistem após reiniciar; ao menos um teste exercita a API real.

---

# Parte III — Avançada

## 13. Arquitetura: decisões, fronteiras e dados

Uma aplicação em produção costuma ter quatro fronteiras: interface, API, regras de negócio e persistência. Separá-las ajuda a localizar erros, mas cada divisão traz custo. Comece com um serviço simples e bem organizado; separe serviços independentes apenas quando houver motivo operacional ou de domínio que compense a rede, a implantação e a observabilidade adicionais.

Na aplicação Tarefas, o navegador apresenta a lista e envia comandos; a API autentica a pessoa, valida entradas e chama regras; a camada de dados consulta o banco. A API devolve apenas os campos necessários. O servidor decide quem pode acessar cada tarefa, mesmo que o cliente oculte botões na tela.

```text
Navegador ──HTTPS──> API ──> regras ──> banco
   │                  │                    │
   └─ estado visual   └─ autorização      └─ estado durável
```

Desenhe o contrato antes de escrever telas: quais entradas são aceitas, quais respostas e erros são possíveis, qual recurso tem identidade estável e quem o possui. Por exemplo, `GET /api/tarefas?cursor=...` devolve uma página de tarefas da pessoa autenticada e um cursor opaco para a próxima página. Nunca confie em `usuario_id` recebido do navegador para escolher o dono. Pense em concorrência: duas abas podem alterar a mesma tarefa. Uma versão do registro ou uma condição de atualização permite detectar conflito em vez de sobrescrever silenciosamente.

**Cache** melhora latência, mas introduz a pergunta “quando o dado deixa de ser válido?”. Uma lista privada não deve ser compartilhada entre usuários por engano. Para dados mutáveis, estabeleça regra de expiração ou invalidação e documente o que o usuário verá após editar. Para arquivos estáticos com nome baseado em conteúdo, cache longo é mais simples, pois uma alteração produz outro nome.

**Exercício 13.** Duas abas marcam a mesma tarefa como feita e depois uma delas troca o título antigo. Que informação no pedido ajudaria a evitar perda silenciosa?

**Conferência:** uma versão/revisão da tarefa, verificada pelo servidor antes da gravação; conflito gera resposta apropriada e a interface pede atualização.

## 14. Identidade, autorização e segurança aplicadas

**Autenticação** responde “quem é esta pessoa?”; **autorização**, “ela pode fazer isto neste recurso?”. Uma sessão pode ser identificada por cookie emitido pelo servidor. Proteja o transporte com HTTPS e configure o cookie de sessão com `HttpOnly`, `Secure` e `SameSite` adequados ao fluxo. Renove ou invalide sessões após mudanças sensíveis e ofereça logout real. Senhas exigem algoritmo próprio de derivação e armazenamento seguro; não guarde texto puro nem crie criptografia caseira. Use uma solução de identidade mantida e revisada para um produto real.

Uma rota que modifica a tarefa deve encontrar o registro **dentro do escopo da pessoa autenticada**:

```sql
UPDATE tarefas
SET feita = ?, versao = versao + 1
WHERE id = ? AND usuario_id = ? AND versao = ?;
```

Verifique quantas linhas foram alteradas: zero pode significar tarefa inexistente, sem permissão ou conflito de versão; decida a resposta sem revelar informação privada. Use parâmetros do driver, como no capítulo 11. A interface continua precisando escapar conteúdo não confiável: inserir `titulo` como `textContent` evita interpretá-lo como HTML. Não use `innerHTML` com texto vindo de usuário ou API. Faça validação no servidor mesmo que o formulário já valide no navegador.

Uma sessão por cookie exige atenção a **CSRF** em operações que alteram dados: defina estratégia de proteção apropriada, como token antifalsificação, verificação de origem e política de cookies. **CORS** controla quais origens podem ler certas respostas no navegador; não substitui autenticação ou autorização. Limite tamanho de requisições, trate falhas sem divulgar segredos e mantenha dependências atualizadas. Use o [OWASP Top 10](https://top10.owasp.org/2025/0x00_2025-Introduction/) como mapa de riscos para revisar a aplicação, não como promessa de segurança automática.

**Exercício 14.** Um usuário muda no navegador o ID de `/api/tarefas/123` para `124` e recebe a tarefa de outra pessoa. A tela ocultava essa opção. Onde está a falha e qual é a correção?

**Conferência:** falha de autorização no servidor; toda leitura e escrita deve filtrar ou verificar o proprietário do recurso autenticado.

## 15. Desempenho e acessibilidade medidos

Otimizar sem medir pode piorar o produto. Defina uma ação observável, como “abrir a lista de tarefas em conexão lenta”, registre o comportamento atual e identifique a causa com ferramentas do navegador e métricas reais. Separe **latência de rede**, **tempo do servidor**, **transferência**, **renderização** e **interação**. Confira se a melhoria chegou aos dispositivos mais lentos, não apenas à máquina de desenvolvimento.

Comece pelo necessário: envie menos JavaScript, comprima respostas, evite bibliotecas pesadas para tarefas pequenas, dimensione imagens e não faça uma consulta ao banco por item da lista. Paginação limita trabalho e memória; índices devem acompanhar consultas reais. Faça carregamento diferido do que está fora da tela quando isso não atrasar o conteúdo essencial. [Web performance — MDN](https://developer.mozilla.org/en-US/docs/Web/Performance).

Acessibilidade também é comportamento verificável. Navegue só com teclado; confira ordem de foco, contraste, rótulos de campo, mensagens de erro e leitura por tecnologia assistiva. Um estado de “salvando” precisa ser comunicado sem roubar foco; um erro deve indicar como corrigir. Testes automáticos ajudam a encontrar parte dos problemas, mas não substituem interação humana. [Acessibilidade web — MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility).

**Exercício 15.** A página baixa 4 MB de JavaScript para mostrar dez tarefas. Qual hipótese você testaria primeiro e como comprovaria melhora?

**Conferência:** inspecionar o conteúdo transferido e executado; remover ou dividir código desnecessário; comparar antes/depois em condições de rede e dispositivo equivalentes, inclusive a interação após carregar.

## 16. Entrega contínua, observabilidade e falhas

Uma entrega confiável tem etapas reproduzíveis: instalar versões de dependências definidas, verificar formatação e testes, construir o artefato, aplicar migrações compatíveis, publicar e conferir saúde. O pipeline automatizado deve falhar se uma etapa essencial falhar. Segredos ficam fora do repositório e são fornecidos pelo ambiente de implantação. Separe configuração de desenvolvimento, teste e produção.

Planeje migrações para versões de código que podem coexistir durante uma publicação. Por exemplo: adicionar uma coluna opcional, publicar código que a preenche e lê, migrar dados antigos, só depois torná-la obrigatória. Faça backup e teste restauração: backup que nunca foi restaurado é uma suposição. Para reduzir risco, publique uma mudança pequena, observe seus sinais e tenha caminho de reversão ou correção.

**Observabilidade** responde o que ocorreu e onde: logs estruturados com identificador de requisição, métricas de taxa de erro e latência, e rastreamento quando há múltiplos serviços. Não registre senhas, tokens ou dados pessoais desnecessários. Um alerta útil aponta ação: erro de criação de tarefa acima do normal, banco indisponível ou latência elevada. A página de erro para usuário deve ser compreensível; o log interno deve conservar o contexto técnico.

Teste falhas previsíveis: API indisponível, resposta lenta, banco sem conexão, pedido duplicado e publicação interrompida. Uma operação repetida deve ter comportamento definido. Em comandos críticos, pense em idempotência para evitar duplicação após tentativas de rede, com chave de idempotência quando apropriado.

**Exercício 16.** Após publicar, a lista abre, mas criar tarefa retorna `500`. Que verificações fazem o diagnóstico sem adivinhar?

**Conferência:** reproduzir e registrar horário/ID da requisição; verificar resposta, logs e métricas da rota; conferir variáveis de ambiente, migração e conexão ao banco; reverter ou corrigir conforme a causa.

## 17. Projeto final: Tarefas para várias pessoas

Transforme a aplicação local em um produto pequeno, sem ampliar recursos antes de estabilizar o fluxo central. Defina critérios de aceitação antes de programar:

1. Uma pessoa entra e sai da conta; uma sessão encerrada não acessa tarefas privadas.
2. Cada tarefa pertence a uma pessoa; alterar o ID não permite ler nem modificar a tarefa de outra.
3. A lista tem paginação, estado vazio, carregamento, erro recuperável e navegação por teclado.
4. Criar, editar e concluir preservam dados após reinício do servidor.
5. Entradas inválidas recebem resposta clara; texto de usuário aparece como texto, não HTML executável.
6. Testes cobrem uma regra pura, uma rota real com autorização e um fluxo principal no navegador.
7. Uma publicação de teste registra passos de configuração, migração, backup, monitoramento e retorno à versão anterior.

**Plano de execução.** Primeiro escreva contrato e esquema, incluindo `usuario_id` e `versao`. Depois implemente autenticação com uma solução confiável, autorização por recurso e persistência. Ligue a interface à API, trate os estados de rede e valide acessibilidade. Rode testes, faça uma revisão de segurança e desempenho e publique em um ambiente de teste. Anote decisões e limites no README. Não apresente uma demonstração de autenticação caseira como sistema pronto para produção.

**Rubrica de avaliação (0–2 por item).** Para cada critério acima, atribua 0 se ausente, 1 se funciona parcialmente ou sem teste, 2 se demonstrado por teste ou revisão reproduzível. Total máximo: 14. Antes de publicar para pessoas reais, todo item de privacidade e segurança deve receber 2; uma pontuação total alta não compensa acesso indevido a dados.

**Desafio avançado opcional.** Simule duas abas editando a mesma tarefa. Mostre o conflito sem perder dados. Compare a solução com uma que simplesmente aceita a última gravação e explique o efeito para quem usa o sistema.

---

## Glossário essencial

| Termo | Significado prático |
| --- | --- |
| API | Contrato pelo qual programas pedem dados ou ações uns aos outros. |
| Autenticação / autorização | Identificar a pessoa / decidir o que ela pode fazer. |
| Cache | Cópia reutilizável de um resultado, com regra de validade. |
| DOM | Representação da página que o JavaScript pode consultar e alterar. |
| Endpoint | Combinação de caminho, método e comportamento de uma API. |
| Migração | Mudança versionada da estrutura ou dos dados persistidos. |
| Responsividade | Adaptação útil da interface a tamanhos e formas de interação. |
| Semântica | Uso de elementos conforme o significado e a função do conteúdo. |
| Transação | Conjunto de operações persistentes tratado como unidade. |

## Próximos passos e fontes

Releia o projeto final e escolha a próxima habilidade pela dificuldade que você encontrou: interface, dados, segurança, testes ou operação. A web evolui; confirme detalhes de APIs, comandos e recomendações na documentação atual antes de aplicá-los em produção.

- [MDN Learn Web Development](https://developer.mozilla.org/en-US/docs/Learn_web_development): percurso de fundamentos, HTML, CSS e JavaScript.
- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP): protocolos, métodos, status e cabeçalhos.
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility): referência para interfaces utilizáveis.
- [Livro Pro Git](https://git-scm.com/book/en/v2): conceitos e fluxos de versionamento.
- [OWASP Top 10](https://top10.owasp.org/2025/0x00_2025-Introduction/): panorama de riscos de segurança em aplicações web.

**Verificação final.** Você consegue explicar o caminho de uma requisição, construir uma página acessível, identificar o limite entre cliente e servidor, proteger uma rota privada, testar uma falha e recuperar uma publicação ruim? Se uma resposta ainda depender de copiar código sem entendê-lo, volte ao capítulo correspondente e refaça o exercício com uma pequena variação.
