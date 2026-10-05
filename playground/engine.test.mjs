import test from 'node:test';
import assert from 'node:assert/strict';
import { LEVELS, runProgram } from '../dist/playground/engine.mjs';

test('as três missões podem ser concluídas', () => {
  const solutions = [
    ['forward2', 'forward', 'left', 'forward2', 'forward'],
    ['forward', 'left', 'forward2', 'forward2', 'right', 'forward2', 'forward'],
    ['forward2', 'forward2', 'forward', 'right', 'forward2', 'forward2', 'forward', 'right', 'forward2', 'right', 'right', 'forward2'],
  ];
  LEVELS.forEach((level, index) => {
    const result = runProgram(level, solutions[index]);
    assert.equal(result.status, 'success', `Missão ${index + 1}`);
    assert.equal(result.collected, level.signals.length);
  });
});

test('meteoros impedem passagem e mantêm a centelha no último espaço seguro', () => {
  const result = runProgram(LEVELS[1], ['forward2']);
  assert.equal(result.status, 'collision');
  assert.deepEqual([result.frames.at(-1).x, result.frames.at(-1).y], [1, 4]);
});

test('chegar ao farol sem sinais não conclui a missão', () => {
  const result = runProgram(LEVELS[0], ['left', 'forward2', 'forward', 'right', 'forward2', 'forward']);
  assert.equal(result.status, 'incomplete');
  assert.equal(result.collected, 0);
});

test('comandos inválidos são rejeitados', () => {
  assert.throws(() => runProgram(LEVELS[0], ['teleport']), TypeError);
  assert.throws(() => runProgram(LEVELS[0], Array(21).fill('forward')), TypeError);
});
