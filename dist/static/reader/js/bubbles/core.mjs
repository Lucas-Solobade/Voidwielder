// Pure rules for Lilo's light-bubble puzzle. A beat lasts 650 ms in the view.
export const LEVELS = [
  {name: 'Praça dos Sorrisos', hint: 'Aprenda a acender uma bolha e liberar a primeira nuvenzinha.', sky: '#c6eeec', map: [
    '###########', '#p...s...e#', '#..c......#', '#...m.....#', '#.........#', '#.........#', '###########',
  ]},
  {name: 'Ponte de Marshmallow', hint: 'Nuvens macias abrem caminhos quando recebem luz.', sky: '#dce9fb', map: [
    '###########', '#p..c....e#', '#...#.....#', '#s..#..m..#', '#...c.....#', '#......s..#', '###########',
  ]},
  {name: 'Trilha das Estrelinhas', hint: 'As pedras seguram a luz. Encontre um ângulo novo.', sky: '#e8ddfb', map: [
    '###########', '#p..c..s.e#', '#.#.#.#.#.#', '#...m..c..#', '#.#.#.#.#.#', '#s...c..m.#', '###########',
  ]},
  {name: 'Bosque do Algodão', hint: 'Duas nuvenzinhas sonolentas esperam você.', sky: '#f9e1eb', map: [
    '###########', '#p.c..s..e#', '#...c.c...#', '#m...#..m.#', '#..s.#....#', '#.c....c..#', '###########',
  ]},
  {name: 'Festa dos Confetes', hint: 'Use as bolhas para fazer a festa brilhar de novo.', sky: '#ffe9cf', map: [
    '###########', '#p..c.s..e#', '#.#...#...#', '#m..c...m.#', '#...#...#.#', '#s..c..s..#', '###########',
  ]},
  {name: 'Castelo da Neblina', hint: 'A Rainha Névoa pisca antes do sopro. Acerte-a quando o escudo estiver apagado.', sky: '#d9d5fa', map: [
    '###########', '#p...s...e#', '#..#...#..#', '#..c...c..#', '#......b..#', '#..c...c..#', '###########',
  ]},
];

export const key = (x, y) => `${x},${y}`;
export const point = (cell) => cell.split(',').map(Number);

export function createLevel(index) {
  const level = LEVELS[index];
  if (!level) throw new RangeError('Fase inexistente');
  const width = level.map[0].length;
  const height = level.map.length;
  const walls = new Set(), clouds = new Set(), stars = new Set(), shadows = new Set();
  let player, exit, boss;
  level.map.forEach((line, y) => {
    if (line.length !== width) throw new Error('Mapa irregular');
    [...line].forEach((tile, x) => {
      const cell = key(x, y);
      if (tile === '#') walls.add(cell);
      else if (tile === 'c') clouds.add(cell);
      else if (tile === 's') stars.add(cell);
      else if (tile === 'm') shadows.add(cell);
      else if (tile === 'p') player = {x, y};
      else if (tile === 'e') exit = cell;
      else if (tile === 'b') boss = cell;
      else if (tile !== '.') throw new Error(`Peça desconhecida: ${tile}`);
    });
  });
  if (!player || !exit || (index === LEVELS.length - 1) !== Boolean(boss)) throw new Error('Mapa incompleto');
  return {index, width, height, spawn: {...player}, player, exit, walls, clouds, stars, shadows,
    boss, bossHearts: boss ? 3 : 0, bubbles: [], beat: 0, collected: 0, complete: false};
}

export function ready(state) {
  return !state.stars.size && !state.shadows.size && state.bossHearts === 0;
}

export function move(state, dx, dy) {
  if (!Number.isInteger(dx) || !Number.isInteger(dy) || Math.abs(dx) + Math.abs(dy) !== 1) throw new TypeError('Direção inválida');
  if (state.complete) return {state, event: 'complete'};
  const x = state.player.x + dx, y = state.player.y + dy, cell = key(x, y);
  if (x < 0 || x >= state.width || y < 0 || y >= state.height || state.walls.has(cell) ||
      state.clouds.has(cell) || state.shadows.has(cell) || (state.bossHearts && state.boss === cell) ||
      state.bubbles.some((bubble) => bubble.x === x && bubble.y === y)) return {state, event: 'blocked'};
  const next = {...state, player: {x, y}, stars: new Set(state.stars)};
  let event = 'move';
  if (next.stars.delete(cell)) {
    next.collected += 1;
    event = 'star';
  }
  if (cell === state.exit) {
    if (ready(next)) { next.complete = true; event = 'finished'; }
    else event = 'locked';
  }
  return {state: next, event};
}

export function placeBubble(state) {
  if (state.complete || state.bubbles.length >= 2 || state.bubbles.some((bubble) =>
    bubble.x === state.player.x && bubble.y === state.player.y)) return {state, event: 'limit'};
  return {state: {...state, bubbles: [...state.bubbles, {...state.player, fuse: 3}]}, event: 'placed'};
}

function lightPath(state, bubble) {
  const cells = [key(bubble.x, bubble.y)];
  for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
    for (let distance = 1; distance <= 2; distance += 1) {
      const cell = key(bubble.x + dx * distance, bubble.y + dy * distance);
      if (state.walls.has(cell) || bubble.x + dx * distance < 0 || bubble.y + dy * distance < 0 ||
          bubble.x + dx * distance >= state.width || bubble.y + dy * distance >= state.height) break;
      cells.push(cell);
      if (state.clouds.has(cell)) break;
    }
  }
  return cells;
}

export function tick(state) {
  if (state.complete) return {state, event: 'complete', light: new Set()};
  const beat = state.beat + 1;
  const next = {...state, beat, clouds: new Set(state.clouds), shadows: new Set(state.shadows), bubbles: []};
  const light = new Set();
  const queue = state.bubbles.map((bubble) => ({...bubble, fuse: bubble.fuse - 1}));
  const exploded = new Set();
  const pending = queue.filter((bubble) => bubble.fuse <= 0);
  while (pending.length) {
    const bubble = pending.shift();
    const cell = key(bubble.x, bubble.y);
    if (exploded.has(cell)) continue;
    exploded.add(cell);
    for (const lit of lightPath(next, bubble)) {
      light.add(lit);
      next.clouds.delete(lit);
      next.shadows.delete(lit);
      for (const other of queue) if (lit === key(other.x, other.y) && !exploded.has(lit)) {
        other.fuse = 0;
        pending.push(other);
      }
    }
  }
  next.bubbles = queue.filter((bubble) => !exploded.has(key(bubble.x, bubble.y)));
  // The boss shield is transparent for two of every four beats.
  const bossOpen = beat % 4 >= 2;
  let event = light.size ? 'pop' : 'tick';
  if (next.bossHearts && bossOpen && light.has(next.boss)) {
    next.bossHearts -= 1;
    event = next.bossHearts ? 'bossHit' : 'bossCleared';
  }
  // A lavender row warns one beat before the boss' gentle wind.
  const windy = next.bossHearts && beat % 6 === 0 && next.player.y === 4;
  if (light.has(key(next.player.x, next.player.y)) || windy) {
    next.player = {...next.spawn};
    event = 'respawn';
  }
  return {state: next, event, light};
}
