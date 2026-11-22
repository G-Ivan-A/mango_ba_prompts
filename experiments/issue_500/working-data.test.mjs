import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";
import { makeWorkingCatalog } from "../../scripts/generate-pages-data.mjs";

async function load(relative) {
  return JSON.parse(await readFile(new URL(`../../${relative}`, import.meta.url), "utf8"));
}

const kit = await load("site/data/test-kit.json");
const ain = await load("site/data/a-in-kit.json");
const { classes } = await load("standards/bcreq-manual-classes/catalog.json");
const catalog = await load("site/data/prompts.json");
const operations = new Map(catalog.filters.operations.map((item) => [item.id, item]));

test("generator detects an unknown class from A-IN", async () => {
  const mutated = structuredClone(ain);
  mutated.steps[0].operation = "К-99";
  await assert.rejects(makeWorkingCatalog(kit, mutated, classes, operations), /bcreq-a-in-route.*AIN-01.*К-99/);
});

test("generator detects an unknown step from flow_step", async () => {
  const mutated = structuredClone(classes);
  mutated[0].flow_step = "Ш-99";
  await assert.rejects(makeWorkingCatalog(kit, ain, mutated, operations), /catalog.json.*К-01.*Ш-99/);
});

test("generator detects an edition with a missing source", async () => {
  const mutated = structuredClone(kit);
  mutated.steps[0].draft.sourcePath = "prompts/drafts/missing.md";
  await assert.rejects(makeWorkingCatalog(mutated, ain, classes, operations), /bcreq-run-kit.*mango-bcreq-constitution.*missing.md/);
});

test("generator detects an ID that resolves to two source paths", async () => {
  const mutated = structuredClone(ain);
  mutated.steps[1].prompt = mutated.steps[1].prompt.replace("mango-bcreq-ain-02-stepwise", "mango-bcreq-ain-01-stepwise");
  await assert.rejects(makeWorkingCatalog(kit, mutated, classes, operations), /bcreq-a-in-route.*AIN-02.*повторный ID/);
});
