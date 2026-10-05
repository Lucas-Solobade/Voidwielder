/** Pure rules for the Voidwielder playground. No DOM, timers, or storage. */
export const LEVELS = Object.freeze([
  {
    title: 'Acenda a primeira estrela',
    concept: 'Sequência',
    story: 'A centelha saiu do vazio. Faça uma rota até o farol, recolhendo o sinal no caminho.',
    hint: 'Siga para a direita até o sinal, vire à esquerda e suba até o farol.',
    size: 4,
    start: [0, 3, 'E'],
    goal: [3, 0],
    signals: [[3, 3]],
    rocks: [],
  },
  {
    title: 'Desvie da chuva de meteoros',
    concept: 'Desvio',
    story: 'Há pedras no caminho. Encontre uma rota segura para pegar o sinal e alcançar o farol.',
    hint: 'Avance uma casa, vire para cima e passe pelo corredor da coluna 1.',
    size: 5,
    start: [0, 4, 'E'],
    goal: [4, 0],
    signals: [[1, 1]],
    rocks: [[2, 4], [2, 3], [2, 2], [3, 2]],
  },
  {
    title: 'Desenhe uma constelação',
    concept: 'Repetição',
    story: 'Dois sinais estão perdidos. O farol só acende depois que você coletar ambos.',
    hint: 'Suba pela coluna 0, atravesse a linha 0, desça na coluna 5 até o segundo sinal e volte ao farol.',
    size: 6,
    start: [0, 5, 'N'],
    goal: [5, 0],
    signals: [[0, 0], [5, 2]],
    rocks: [[2, 1], [2, 2], [2, 3], [2, 4], [4, 3], [4, 4]],
  },
]);

const DIRECTIONS = ['N', 'E', 'S', 'W'];
const VECTORS = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
export const OPERATIONS = Object.freeze({ forward: 'Avançar', left: 'Girar ↶', right: 'Girar ↷', forward2: 'Repetir 2×' });

export function runProgram(level, program) {
  if (!Array.isArray(program) || program.length > 20 || program.some((op) => !Object.hasOwn(OPERATIONS, op))) {
    throw new TypeError('O programa aceita até 20 comandos conhecidos.');
  }
  const [startX, startY, startDirection] = level.start;
  let x = startX;
  let y = startY;
  let direction = startDirection;
  const collected = new Set();
  const frames = [{ x, y, direction, command: -1, action: 'start', collected: [] }];
  const rocks = new Set(level.rocks.map(([rx, ry]) => `${rx},${ry}`));
  const signalAt = (px, py) => level.signals.findIndex(([sx, sy]) => sx === px && sy === py);

  for (const [command, operation] of program.entries()) {
    if (operation === 'left' || operation === 'right') {
      const turn = operation === 'left' ? -1 : 1;
      direction = DIRECTIONS[(DIRECTIONS.indexOf(direction) + turn + 4) % 4];
      frames.push({ x, y, direction, command, action: operation, collected: [...collected] });
      continue;
    }
    const repeat = operation === 'forward2' ? 2 : 1;
    for (let step = 0; step < repeat; step += 1) {
      const [dx, dy] = VECTORS[direction];
      const nextX = x + dx;
      const nextY = y + dy;
      if (nextX < 0 || nextY < 0 || nextX >= level.size || nextY >= level.size || rocks.has(`${nextX},${nextY}`)) {
        frames.push({ x, y, direction, command, action: 'collision', collected: [...collected] });
        return { status: 'collision', frames, collected: collected.size };
      }
      x = nextX;
      y = nextY;
      const signal = signalAt(x, y);
      if (signal >= 0) collected.add(signal);
      frames.push({ x, y, direction, command, action: 'forward', collected: [...collected] });
    }
  }
  const atGoal = x === level.goal[0] && y === level.goal[1];
  return {
    status: atGoal && collected.size === level.signals.length ? 'success' : 'incomplete',
    frames,
    collected: collected.size,
  };
}
