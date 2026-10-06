export const LEVELS = [
  {
    name: 'Pradinho de Algodão',
    note: 'Um jardim pequeno para aprender a plantar estrelas.',
    sky: ['#cdeffc', '#fce5d8'],
    map: [
      '.........',
      '.P..S....',
      '..#...F..',
      '.........',
      '.F..#S...',
      '.........',
    ],
  },
  {
    name: 'Lago dos Soninhos',
    note: 'Passeie ao redor do lago e acorde três flores.',
    sky: ['#d7eafa', '#e4d9fa'],
    map: [
      '..S...F..',
      '.P..~....',
      '.#..~..S.',
      '....~....',
      '.F..~..F.',
      '..S......',
    ],
  },
  {
    name: 'Pomar da Lua',
    note: 'O último jardim espera quatro flores e um céu cheio de cor.',
    sky: ['#e9dafa', '#fce3df'],
    map: [
      'F...S...F',
      '.#..~..#.',
      'S..P~..S.',
      '.#..~..#.',
      'F...S...F',
      '.........',
    ],
  },
];

export const cellKey = (col, row) => `${col},${row}`;

export function createLevel(index) {
  const level = LEVELS[index];
  if (!level) throw new RangeError('Fase inexistente');
  const width = level.map[0].length;
  const walls = new Set();
  const water = new Set();
  const seeds = new Set();
  const buds = new Set();
  let player = null;

  level.map.forEach((line, row) => {
    if (line.length !== width) throw new Error('Mapa irregular');
    [...line].forEach((tile, col) => {
      const key = cellKey(col, row);
      if (tile === '#') walls.add(key);
      else if (tile === '~') water.add(key);
      else if (tile === 'S') seeds.add(key);
      else if (tile === 'F') buds.add(key);
      else if (tile === 'P') {
        if (player) throw new Error('Mapa com mais de um personagem');
        player = {col, row};
      } else if (tile !== '.') throw new Error('Peça desconhecida');
    });
  });
  if (!player || seeds.size !== buds.size || !buds.size) throw new Error('Mapa incompleto');

  return {
    index,
    width,
    height: level.map.length,
    player,
    walls,
    water,
    seeds,
    buds,
    bloomed: new Set(),
    carrying: false,
    moves: 0,
    complete: false,
  };
}

export function step(state, dx, dy) {
  if (!Number.isInteger(dx) || !Number.isInteger(dy) || Math.abs(dx) + Math.abs(dy) !== 1) {
    throw new TypeError('Movimento deve ser de uma casa na horizontal ou vertical');
  }
  if (state.complete) return {state, event: 'complete'};

  const col = state.player.col + dx;
  const row = state.player.row + dy;
  const key = cellKey(col, row);
  if (col < 0 || col >= state.width || row < 0 || row >= state.height ||
      state.walls.has(key) || state.water.has(key)) {
    return {state, event: 'blocked'};
  }

  const next = {
    ...state,
    player: {col, row},
    seeds: new Set(state.seeds),
    bloomed: new Set(state.bloomed),
    moves: state.moves + 1,
  };
  let event = 'move';
  if (next.seeds.has(key)) {
    if (next.carrying) event = 'handsFull';
    else {
      next.seeds.delete(key);
      next.carrying = true;
      event = 'pickup';
    }
  }
  if (next.buds.has(key) && !next.bloomed.has(key)) {
    if (!next.carrying) event = 'needsSeed';
    else {
      next.bloomed.add(key);
      next.carrying = false;
      next.complete = next.bloomed.size === next.buds.size;
      event = next.complete ? 'finished' : 'planted';
    }
  }
  return {state: next, event};
}
