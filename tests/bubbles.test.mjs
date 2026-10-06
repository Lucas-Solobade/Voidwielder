import assert from 'node:assert/strict';
import test from 'node:test';
import {LEVELS, createLevel, key, move, placeBubble, ready, tick} from '../reader/static/reader/js/bubbles/core.mjs';

test('six hand-built maps expose every objective after soft clouds clear', () => {
  assert.equal(LEVELS.length, 6);
  LEVELS.forEach((_, index) => {
    const state = createLevel(index);
    assert.equal(state.width, 11);
    assert.equal(state.height, 7);
    const queue = [key(state.player.x, state.player.y)], seen = new Set(queue);
    for (const cell of queue) {
      const [x, y] = cell.split(',').map(Number);
      for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        const next = key(x + dx, y + dy);
        if (x + dx < 0 || x + dx >= state.width || y + dy < 0 || y + dy >= state.height ||
            state.walls.has(next) || seen.has(next)) continue;
        seen.add(next); queue.push(next);
      }
    }
    for (const objective of [...state.stars, ...state.shadows, state.exit, ...(state.boss ? [state.boss] : [])]) {
      assert.ok(seen.has(objective), `fase ${index + 1}: objetivo inacessível ${objective}`);
    }
  });
});

test('a bubble pops after three beats and clears a cloud and a sleepy visitor', () => {
  let state = createLevel(0);
  state.player = {x: 4, y: 2};
  state = placeBubble(state).state;
  assert.equal(state.bubbles.length, 1);
  state = tick(state).state;
  state = tick(state).state;
  assert.equal(state.clouds.size, 1);
  const result = tick(state);
  assert.ok(result.light.has(key(4, 3)));
  assert.equal(result.state.shadows.size, 0);
  assert.deepEqual(result.state.player, result.state.spawn);
});

test('the final boss loses a heart only while the shield is transparent', () => {
  let state = createLevel(5);
  state.player = {x: 5, y: 4};
  state = placeBubble(state).state;
  for (let i = 0; i < 3; i += 1) state = tick(state).state;
  assert.equal(state.bossHearts, 2);
  assert.equal(ready(state), false);
  assert.throws(() => move(state, 2, 0), TypeError);
});
