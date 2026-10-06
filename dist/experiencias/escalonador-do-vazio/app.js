const COLORS = ["#7cf7d4", "#fbcd5d", "#a58cff", "#ff719a", "#64b5ff", "#ff9d66"];
const EXAMPLE = [
  { id: "P1", arrival: 0, burst: 5 },
  { id: "P2", arrival: 1, burst: 3 },
  { id: "P3", arrival: 2, burst: 2 },
  { id: "P4", arrival: 4, burst: 4 },
];

const clone = (items) => items.map((item) => ({ ...item }));

function normalise(processes) {
  return processes.map((process, index) => ({
    ...process,
    order: index,
    arrival: Math.max(0, Number(process.arrival) || 0),
    burst: Math.max(1, Number(process.burst) || 1),
    remaining: Math.max(1, Number(process.burst) || 1),
  }));
}

function mergeSegment(segments, id, start, duration) {
  const last = segments.at(-1);
  if (last && last.id === id && last.start + last.duration === start) last.duration += duration;
  else segments.push({ id, start, duration });
}

function nonPreemptive(processes, shortestFirst = false) {
  const pending = normalise(processes);
  const segments = [];
  const completion = {};
  const firstStart = {};
  let time = 0;

  while (pending.length) {
    const ready = pending.filter((item) => item.arrival <= time);
    if (!ready.length) {
      const next = Math.min(...pending.map((item) => item.arrival));
      mergeSegment(segments, "idle", time, next - time);
      time = next;
      continue;
    }
    ready.sort((a, b) => shortestFirst ? a.burst - b.burst || a.arrival - b.arrival || a.order - b.order : a.arrival - b.arrival || a.order - b.order);
    const process = ready[0];
    pending.splice(pending.indexOf(process), 1);
    firstStart[process.id] = time;
    mergeSegment(segments, process.id, time, process.burst);
    time += process.burst;
    completion[process.id] = time;
  }
  return finalise(processes, segments, completion, firstStart);
}

function roundRobin(processes, quantum = 2) {
  const all = normalise(processes).sort((a, b) => a.arrival - b.arrival || a.order - b.order);
  const queue = [];
  const segments = [];
  const completion = {};
  const firstStart = {};
  let cursor = 0;
  let time = 0;

  while (cursor < all.length || queue.length) {
    if (!queue.length && cursor < all.length && all[cursor].arrival > time) {
      mergeSegment(segments, "idle", time, all[cursor].arrival - time);
      time = all[cursor].arrival;
    }
    while (cursor < all.length && all[cursor].arrival <= time) queue.push(all[cursor++]);
    const process = queue.shift();
    if (!process) continue;
    if (!(process.id in firstStart)) firstStart[process.id] = time;
    const slice = Math.min(process.remaining, Math.max(1, quantum));
    mergeSegment(segments, process.id, time, slice);
    time += slice;
    process.remaining -= slice;
    while (cursor < all.length && all[cursor].arrival <= time) queue.push(all[cursor++]);
    if (process.remaining > 0) queue.push(process);
    else completion[process.id] = time;
  }
  return finalise(processes, segments, completion, firstStart);
}

function finalise(processes, segments, completion, firstStart) {
  const details = processes.map((process) => {
    const turnaround = completion[process.id] - process.arrival;
    return { ...process, start: firstStart[process.id], completion: completion[process.id], turnaround, wait: turnaround - process.burst };
  });
  const average = (field) => details.reduce((sum, item) => sum + item[field], 0) / details.length;
  const active = segments.filter((segment) => segment.id !== "idle");
  return {
    segments,
    details,
    averageWait: average("wait"),
    averageTurnaround: average("turnaround"),
    contextSwitches: Math.max(0, active.length - 1),
    total: segments.reduce((sum, segment) => sum + segment.duration, 0),
  };
}

export function schedule(processes, algorithm = "fcfs", quantum = 2) {
  if (!processes.length) return { segments: [], details: [], averageWait: 0, averageTurnaround: 0, contextSwitches: 0, total: 0 };
  if (algorithm === "rr") return roundRobin(processes, quantum);
  return nonPreemptive(processes, algorithm === "sjf");
}

const rows = typeof document === "undefined" ? null : document.querySelector("#processRows");
if (rows) {
  const state = { processes: clone(EXAMPLE), algorithm: "fcfs", quantum: 2 };
  const names = { fcfs: "FCFS", sjf: "SJF", rr: "ROUND ROBIN" };
  const explanations = {
    fcfs: "O primeiro processo que chega é o primeiro atendido. É simples e previsível, mas uma tarefa longa pode segurar toda a fila.",
    sjf: "Entre os processos disponíveis, a CPU escolhe o de menor duração. Isso costuma reduzir a espera média, mas tarefas longas podem aguardar mais.",
    rr: "A CPU percorre a fila em ciclos. Cada processo recebe uma fatia limitada pelo quantum, favorecendo a resposta rápida e a alternância.",
  };

  function renderInputs() {
    rows.innerHTML = state.processes.map((process, index) => `
      <div class="table-row" role="row" data-index="${index}">
        <span class="process-name" role="cell"><i class="process-dot" style="--process-color:${COLORS[index % COLORS.length]}"></i>${process.id}</span>
        <input role="cell" data-field="arrival" aria-label="Chegada de ${process.id}" type="number" min="0" max="30" value="${process.arrival}" inputmode="numeric">
        <input role="cell" data-field="burst" aria-label="Duração de ${process.id}" type="number" min="1" max="30" value="${process.burst}" inputmode="numeric">
        <button class="remove" type="button" aria-label="Remover ${process.id}" ${state.processes.length === 1 ? "disabled" : ""}>×</button>
      </div>`).join("");
  }

  function renderResult() {
    const result = schedule(state.processes, state.algorithm, state.quantum);
    document.querySelector("#algorithmBadge").textContent = names[state.algorithm];
    document.querySelector("#explanation").textContent = explanations[state.algorithm];
    document.querySelector("#quantumField").hidden = state.algorithm !== "rr";
    document.querySelector("#averageWait").textContent = result.averageWait.toFixed(1).replace(".0", "");
    document.querySelector("#averageTurnaround").textContent = result.averageTurnaround.toFixed(1).replace(".0", "");
    document.querySelector("#contextSwitches").textContent = result.contextSwitches;
    const colorFor = (id) => COLORS[state.processes.findIndex((process) => process.id === id) % COLORS.length];
    document.querySelector("#timeline").innerHTML = result.segments.map((segment, index) => `<div class="slice ${segment.id === "idle" ? "idle" : ""}" style="--duration:${segment.duration};--index:${index};--process-color:${segment.id === "idle" ? "#22283f" : colorFor(segment.id)}"><span>${segment.id === "idle" ? "CPU livre" : segment.id}</span><small>${segment.duration}u</small></div>`).join("");
    let elapsed = 0;
    document.querySelector("#ticks").innerHTML = result.segments.map((segment) => {
      const start = elapsed;
      elapsed += segment.duration;
      return `<span class="tick" style="--duration:${segment.duration}">${start}</span>`;
    }).join("") + `<span class="tick-end">${result.total}</span>`;
    document.querySelector("#resultRows").innerHTML = result.details.map((item, index) => `<tr><td><span class="result-process"><i class="process-dot" style="--process-color:${COLORS[index % COLORS.length]}"></i>${item.id}</span></td><td>${item.start}</td><td>${item.completion}</td><td>${item.wait}</td><td>${item.turnaround}</td></tr>`).join("");
  }

  function render() { renderInputs(); renderResult(); }

  rows.addEventListener("input", (event) => {
    const field = event.target.dataset.field;
    if (!field) return;
    const index = Number(event.target.closest("[data-index]").dataset.index);
    state.processes[index][field] = Math.max(field === "arrival" ? 0 : 1, Math.min(30, Number(event.target.value) || 0));
    renderResult();
  });
  rows.addEventListener("click", (event) => {
    const button = event.target.closest(".remove");
    if (!button || state.processes.length === 1) return;
    state.processes.splice(Number(button.closest("[data-index]").dataset.index), 1);
    state.processes.forEach((process, index) => { process.id = `P${index + 1}`; });
    render();
  });
  document.querySelector("#addButton").addEventListener("click", () => {
    if (state.processes.length >= 6) return;
    state.processes.push({ id: `P${state.processes.length + 1}`, arrival: 0, burst: 2 });
    render();
  });
  document.querySelector("#resetButton").addEventListener("click", () => { state.processes = clone(EXAMPLE); state.algorithm = "fcfs"; state.quantum = 2; document.querySelector('[name="algorithm"][value="fcfs"]').checked = true; document.querySelector("#quantumInput").value = 2; render(); });
  document.querySelectorAll('[name="algorithm"]').forEach((input) => input.addEventListener("change", () => { state.algorithm = input.value; renderResult(); }));
  document.querySelector("#quantumInput").addEventListener("input", (event) => { state.quantum = Math.max(1, Math.min(9, Number(event.target.value) || 1)); renderResult(); });
  render();
}
