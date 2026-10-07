function factorialTrace(n) {
  const events = [];
  let serial = 0;
  function visit(value, depth) {
    const id = serial++;
    events.push({ type: "call", id, depth, label: `fat(${value})`, args: `${value}`, base: value <= 1 });
    if (value <= 1) {
      events.push({ type: "return", id, depth, label: `fat(${value})`, value: 1, base: true });
      return 1;
    }
    const result = value * visit(value - 1, depth + 1);
    events.push({ type: "return", id, depth, label: `fat(${value})`, value: result, base: false });
    return result;
  }
  const result = visit(n, 0);
  return { events, result };
}

function fibonacciTrace(n) {
  const events = [];
  let serial = 0;
  function visit(value, depth) {
    const id = serial++;
    events.push({ type: "call", id, depth, label: `fib(${value})`, args: `${value}`, base: value <= 1 });
    if (value <= 1) {
      events.push({ type: "return", id, depth, label: `fib(${value})`, value, base: true });
      return value;
    }
    const result = visit(value - 1, depth + 1) + visit(value - 2, depth + 1);
    events.push({ type: "return", id, depth, label: `fib(${value})`, value: result, base: false });
    return result;
  }
  const result = visit(n, 0);
  return { events, result };
}

function gcdTrace(a, b) {
  const events = [];
  let serial = 0;
  function visit(left, right, depth) {
    const id = serial++;
    events.push({ type: "call", id, depth, label: `mdc(${left}, ${right})`, args: `${left}, ${right}`, base: right === 0 });
    if (right === 0) {
      events.push({ type: "return", id, depth, label: `mdc(${left}, ${right})`, value: left, base: true });
      return left;
    }
    const result = visit(right, left % right, depth + 1);
    events.push({ type: "return", id, depth, label: `mdc(${left}, ${right})`, value: result, base: false });
    return result;
  }
  const result = visit(a, b, 0);
  return { events, result };
}

export function buildTrace(algorithm, values) {
  if (algorithm === "fibonacci") return fibonacciTrace(Math.max(0, Math.min(8, Number(values.n) || 0)));
  if (algorithm === "gcd") return gcdTrace(Math.max(1, Number(values.a) || 1), Math.max(0, Number(values.b) || 0));
  return factorialTrace(Math.max(1, Math.min(8, Number(values.n) || 1)));
}

export function stackAt(events, step) {
  const frames = [];
  for (let index = 0; index <= step && index < events.length; index += 1) {
    const event = events[index];
    if (event.type === "call") frames.push({ ...event, returned: false });
    else if (index === step) {
      const frame = frames.find((item) => item.id === event.id);
      if (frame) Object.assign(frame, { returned: true, value: event.value, base: event.base });
    } else {
      const frameIndex = frames.findIndex((item) => item.id === event.id);
      if (frameIndex >= 0) frames.splice(frameIndex, 1);
    }
  }
  return frames;
}

const root = typeof document === "undefined" ? null : document.querySelector("#laboratorio");
if (root) {
  const $ = (selector) => document.querySelector(selector);
  const settings = {
    factorial: { rule: "fat(n) = n × fat(n − 1)\nfat(1) = 1", help: "Cada chamada reduz n até alcançar 1.", label: "Calcular n!", min: 1, max: 8, value: 5 },
    fibonacci: { rule: "fib(n) = fib(n − 1) + fib(n − 2)\nfib(0) = 0 · fib(1) = 1", help: "A função abre dois ramos até alcançar 0 ou 1.", label: "Calcular fib(n)", min: 0, max: 8, value: 5 },
    gcd: { rule: "mdc(a, b) = mdc(b, a mod b)\nmdc(a, 0) = a", help: "O resto diminui até que o segundo valor seja zero." },
  };
  const state = { algorithm: "factorial", step: 0, trace: null, timer: null };

  function values() {
    return { n: Number($("#numberInput").value), a: Number($("#gcdA").value), b: Number($("#gcdB").value) };
  }

  function rebuild(reset = true) {
    state.trace = buildTrace(state.algorithm, values());
    if (reset) state.step = 0;
    state.step = Math.min(state.step, state.trace.events.length - 1);
    stop();
    render();
  }

  function narration(event) {
    if (event.type === "call" && event.base) return `${event.label} alcançou o caso-base. Nenhuma nova chamada será criada aqui.`;
    if (event.type === "call") return `${event.label} entrou na pilha e precisa de uma chamada menor para continuar.`;
    if (event.base) return `${event.label} devolve ${event.value}. A subida da pilha pode começar.`;
    return `${event.label} recebeu os resultados internos e devolve ${event.value} para a chamada anterior.`;
  }

  function render() {
    const { events, result } = state.trace;
    const event = events[state.step];
    const frames = stackAt(events, state.step);
    $("#stepNow").textContent = state.step + 1;
    $("#stepTotal").textContent = events.length;
    $("#previous").disabled = state.step === 0;
    $("#next").disabled = state.step === events.length - 1;
    $("#finalResult").textContent = state.step === events.length - 1 ? result : "—";
    $("#eventKind").textContent = event.type === "return" ? "RETORNO" : event.base ? "CASO-BASE" : "CHAMADA";
    $("#eventKind").className = `event-kind ${event.type === "return" ? "return" : event.base ? "base" : ""}`;
    $("#narration").textContent = narration(event);
    $("#stack").innerHTML = frames.length ? frames.map((frame, index) => `
      <div class="frame ${frame.returned ? "returned" : index === frames.length - 1 ? "current" : ""}" style="--indent:${Math.min(frame.depth, 7)}">
        <div class="frame-head"><code>${frame.label}</code>${frame.returned ? `<span class="frame-value">retorna ${frame.value}</span>` : `<small>nível ${frame.depth}</small>`}</div>
      </div>`).join("") : '<p class="empty-stack">A pilha está vazia.</p>';
    $("#trace").innerHTML = events.map((item, index) => `<li class="${index < state.step ? "done" : index === state.step ? "active" : ""} ${item.type}"><span>${item.label}</span><small>${item.type === "return" ? `↩ ${item.value}` : item.base ? "base" : "↓"}</small></li>`).join("");
    $("#trace").children[state.step]?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function stop() {
    clearInterval(state.timer);
    state.timer = null;
    $("#play").innerHTML = "▶ <span>Reproduzir</span>";
    $("#play").setAttribute("aria-label", "Reproduzir");
  }

  function play() {
    if (state.timer) { stop(); return; }
    if (state.step === state.trace.events.length - 1) state.step = 0;
    $("#play").innerHTML = "Ⅱ <span>Pausar</span>";
    $("#play").setAttribute("aria-label", "Pausar");
    state.timer = setInterval(() => {
      if (state.step >= state.trace.events.length - 1) { stop(); return; }
      state.step += 1;
      render();
    }, 1750 - Number($("#speed").value));
    render();
  }

  $("#algorithm").addEventListener("change", (event) => {
    state.algorithm = event.target.value;
    const config = settings[state.algorithm];
    $("#singleInput").hidden = state.algorithm === "gcd";
    $("#gcdInputs").hidden = state.algorithm !== "gcd";
    if (state.algorithm !== "gcd") {
      $("#numberLabel").textContent = config.label;
      $("#numberInput").min = config.min;
      $("#numberInput").max = config.max;
      $("#numberInput").value = config.value;
    }
    $("#rule").textContent = config.rule;
    $("#ruleHelp").textContent = config.help;
    rebuild();
  });
  ["#numberInput", "#gcdA", "#gcdB"].forEach((selector) => $(selector).addEventListener("change", () => rebuild()));
  $("#previous").addEventListener("click", () => { stop(); state.step = Math.max(0, state.step - 1); render(); });
  $("#next").addEventListener("click", () => { stop(); state.step = Math.min(state.trace.events.length - 1, state.step + 1); render(); });
  $("#play").addEventListener("click", play);
  $("#speed").addEventListener("change", () => { if (state.timer) { stop(); play(); } });

  $("#rule").textContent = settings.factorial.rule;
  $("#ruleHelp").textContent = settings.factorial.help;
  rebuild();
}
