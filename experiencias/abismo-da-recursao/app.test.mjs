import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const source = await readFile(new URL("./app.js", import.meta.url), "utf8");
const { buildTrace, stackAt } = await import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);

const factorial = buildTrace("factorial", { n: 5 });
assert.equal(factorial.result, 120);
assert.equal(factorial.events.length, 10);
assert.deepEqual(stackAt(factorial.events, 4).map((frame) => frame.label), ["fat(5)", "fat(4)", "fat(3)", "fat(2)", "fat(1)"]);
assert.equal(stackAt(factorial.events, 5).at(-1).returned, true);

const fibonacci = buildTrace("fibonacci", { n: 6 });
assert.equal(fibonacci.result, 8);
assert.equal(fibonacci.events.some((event) => event.base && event.label === "fib(0)"), true);

const gcd = buildTrace("gcd", { a: 48, b: 18 });
assert.equal(gcd.result, 6);
assert.deepEqual(gcd.events.filter((event) => event.type === "call").map((event) => event.label), ["mdc(48, 18)", "mdc(18, 12)", "mdc(12, 6)", "mdc(6, 0)"]);

const finalStack = stackAt(gcd.events, gcd.events.length - 1);
assert.equal(finalStack.length, 1);
assert.equal(finalStack[0].value, 6);

console.log("Abismo da Recursão: fatorial, Fibonacci, Euclides e pilha validados.");
