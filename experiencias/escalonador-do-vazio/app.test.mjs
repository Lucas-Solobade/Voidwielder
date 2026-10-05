import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const source = await readFile(new URL("./app.js", import.meta.url), "utf8");
const { schedule } = await import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);

const example = [
  { id: "P1", arrival: 0, burst: 5 },
  { id: "P2", arrival: 1, burst: 3 },
  { id: "P3", arrival: 2, burst: 2 },
  { id: "P4", arrival: 4, burst: 4 },
];

const fcfs = schedule(example, "fcfs");
assert.deepEqual(fcfs.segments.map(({ id, duration }) => [id, duration]), [["P1", 5], ["P2", 3], ["P3", 2], ["P4", 4]]);
assert.equal(fcfs.averageWait, 4);

const sjf = schedule(example, "sjf");
assert.deepEqual(sjf.segments.map(({ id }) => id), ["P1", "P3", "P2", "P4"]);
assert.equal(sjf.averageWait, 3.75);

const rr = schedule(example, "rr", 2);
assert.equal(rr.details.every((item) => item.completion >= item.arrival + item.burst), true);
assert.equal(rr.total, 14);
assert.equal(rr.contextSwitches, 7);

const idle = schedule([{ id: "P1", arrival: 3, burst: 2 }], "fcfs");
assert.deepEqual(idle.segments.map(({ id, duration }) => [id, duration]), [["idle", 3], ["P1", 2]]);

console.log("Escalonador do Vazio: 4 cenários validados.");
