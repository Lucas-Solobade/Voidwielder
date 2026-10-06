import assert from 'node:assert/strict';
import test from 'node:test';
import {LEVELS, cellKey, createLevel, step} from '../reader/static/reader/js/garden/core.mjs';

const directions = [[1, 0], [-1, 0], [0, 1], [0, -1]];

function route(state, target) {
  const start = cellKey(state.player.col, state.player.row);
  const queue = [{key: start, moves: []}];
  const seen = new Set([start]);
  for (const item of queue) {
    if (item.key === target) return item.moves;
    const [col, row] = item.key.split(',').map(Number);
    for (const [dx, dy] of directions) {
      const x = col + dx;
      const y = row + dy;
      const key = cellKey(x, y);
      if (x < 0 || x >= state.width || y < 0 || y >= state.height ||
          state.walls.has(key) || state.water.has(key) || seen.has(key)) continue;
      seen.add(key);
      queue.push({key, moves: [...item.moves, [dx, dy]]});
    }
  }
  throw new Error(`Unreachable garden tile: ${target}`);
}

function travel(state, target) {
  for (const [dx, dy] of route(state, target)) state = step(state, dx, dy).state;
  return state;
}

test('every garden can be completed without losing a seed', () => {
  LEVELS.forEach((_, index) => {
    let state = createLevel(index);
    const flowerCount = state.buds.size;
    for (let flower = 0; flower < flowerCount; flower += 1) {
      state = travel(state, [...state.seeds][0]);
      assert.equal(state.carrying, true);
      state = travel(state, [...state.buds].find((key) => !state.bloomed.has(key)));
      assert.equal(state.carrying, false);
      assert.equal(state.bloomed.size, flower + 1);
    }
    assert.equal(state.complete, true);
    assert.equal(state.seeds.size, 0);
  });
});

test('blocked moves and invalid directions cannot change the garden', () => {
  const state = createLevel(0);
  assert.equal(step(state, -1, 0).state.player.col, state.player.col - 1);
  assert.throws(() => step(state, 2, 0), TypeError);
  const edge = {...state, player: {col: 0, row: 0}};
  assert.equal(step(edge, -1, 0).event, 'blocked');
  assert.equal(edge.moves, 0);
});
