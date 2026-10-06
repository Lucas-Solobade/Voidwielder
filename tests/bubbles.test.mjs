import assert from 'node:assert/strict';
import test from 'node:test';
import {LEVELS, createLevel, dash, key, lightPath, move, placeBubble, ready, tick} from '../reader/static/reader/js/bubbles/core.mjs';

test('six maps retain reachable stars, visitors and exits after soft clouds clear', () => {
  assert.equal(LEVELS.length, 6);
  LEVELS.forEach((_, index) => {
    const state = createLevel(index, 1);
    assert.equal(state.width, 11);
    assert.equal(state.height, 7);
    const queue = [state.player], seen = new Set([key(state.player.x, state.player.y)]);
    for (const {x, y} of queue) for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
      const cell = key(x + dx, y + dy);
      if (x + dx < 0 || x + dx >= state.width || y + dy < 0 || y + dy >= state.height ||
          state.walls.has(cell) || seen.has(cell)) continue;
      seen.add(cell); queue.push({x:x + dx, y:y + dy});
    }
    for (const objective of [...state.stars, ...state.enemies.map(({x,y}) => key(x,y)), state.exit, ...state.clouds]) {
      assert.ok(seen.has(objective), `fase ${index + 1}: ${objective} inacessível`);
    }
    if (index === 5) assert.equal(state.boss.cells.size, 4);
  });
});

test('visitors chase Lilo and fast visitors avoid an imminent light wave', () => {
  let state = createLevel(0, 1);
  state.player = {x:5, y:2};
  for (let beat = 0; beat < 3; beat += 1) state = tick(state).state;
  assert.equal(state.enemies[0].x, 6);

  state = createLevel(1, 1);
  const hunter = state.enemies.find((enemy) => enemy.kind === 'hunter');
  state.bubbles = [{x:hunter.x, y:hunter.y + 1, fuse:2, range:2}];
  const result = tick(state);
  const predicted = new Set(lightPath(result.state, result.state.bubbles[0]));
  const moved = result.state.enemies.find((enemy) => enemy.id === hunter.id);
  assert.notEqual(key(moved.x, moved.y), key(hunter.x, hunter.y));
  assert.ok(!predicted.has(key(moved.x, moved.y)));
});

test('destroyed clouds reveal seeded random items that improve movement', () => {
  let state = createLevel(0, 1);
  state.player = {x:3, y:1};
  state = placeBubble(state).state;
  for (let beat = 0; beat < 3; beat += 1) state = tick(state).state;
  assert.ok(state.items.size > 0);
  assert.ok(state.items.has(key(4,1)));
  state.player = {x:3, y:1};
  const result = move(state, 1, 0);
  assert.equal(result.event, 'item');
  assert.equal(result.item, 'skates');
  assert.equal(result.state.stats.skates, 1);
  assert.equal(dash(result.state, 1, 0).event, 'noWings');
  result.state.stats.wings = 1;
  assert.equal(dash(result.state, 1, 0).state.player.x, 6);
});

test('stone and clouds limit light, while the boss exposes a larger core after warning', () => {
  const stage = createLevel(0, 1);
  const path = new Set(lightPath(stage, {x:3,y:1,range:4}));
  assert.ok(path.has(key(4,1)));
  assert.ok(!path.has(key(5,1)));

  let state = createLevel(5, 1);
  state.beat = 2;
  state.player = {x:5,y:4};
  state = placeBubble(state).state;
  state.player = {x:2,y:2};
  state = tick(state).state;
  assert.equal(state.boss.mode, 'warning');
  state.player = {x:3,y:3};
  const warning = tick(state);
  assert.equal(warning.state.boss.mode, 'attack');
  assert.ok(warning.attack.has(key(2,2)));
  const opening = tick(warning.state);
  assert.equal(opening.state.boss.mode, 'open');
  assert.equal(opening.state.boss.hearts, 3);
  assert.ok(opening.state.enemies.some((enemy) => enemy.id >= 100));
  assert.equal(ready(opening.state), false);
  assert.throws(() => move(opening.state, 2, 0), TypeError);
});
