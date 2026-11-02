// Exercise the shipped app functions in a lightweight DOM, without booting fetch.
// Issue #423: the active catalog is the 39 BCREQ classes over the 4 stages of
// process v0.2; the 14 stage-1 prompts are visible only with the «Архив» family.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { test } = require('node:test');
const data = JSON.parse(fs.readFileSync('site/data/prompts.json', 'utf8'));
const source = fs.readFileSync('site/app.js', 'utf8').replace(/\ninit\(\);\s*$/, '');
const IN = 'A-IN · Приём задачи';
const CORE = 'A-CORE · Требования';
const WORK = 'A-WORK · Решение';
const RELEASE = 'A-RELEASE · Выпуск';
function app(tokens = [], query = '') {
  const node = () => ({dataset: {}, children: [], addEventListener() {}, setAttribute() {}, append(...children) {this.children.push(...children);}, replaceChildren(...children) {this.children = children;}});
  const context = vm.createContext({document: {querySelector: node, querySelectorAll: () => [], createElement: node, addEventListener() {}}, window: {addEventListener() {}}, data, tokens, query});
  vm.runInContext(source, context);
  vm.runInContext('state.prompts = data.prompts; state.promptsData = data; state.stats = {totals: {processes: {}, operations: {}, modes: {}}}; state.selectedFilters = new Set(tokens); state.query = query;', context);
  return expression => JSON.parse(JSON.stringify(vm.runInContext(expression, context)));
}
test('default catalog shows the 39 classes and hides the archive', () => {
  const run = app();
  assert.equal(run('visiblePrompts().length'), 39);
  assert.ok(run('visiblePrompts().every(p => p.classId && !p.archived)'));
  assert.deepEqual(run('facetCounts("mode")'), {manual: 39});
});
test('the «Архив» family shows the 14 stage-1 prompts with their own modes', () => {
  const run = app(['family:archive']);
  assert.equal(run('visiblePrompts().length'), 14);
  assert.ok(run('visiblePrompts().every(p => p.archived && p.family === "archive")'));
  assert.deepEqual(run('facetCounts("mode")'), {stepwise: 8, oneshot: 6});
  assert.equal(app(['mode:stepwise'])('visiblePrompts().length'), 0);
  assert.equal(app(['family:bcreq', 'family:archive'])('visiblePrompts().length'), 53);
});
test('stage selection restricts operation counts to actual prompts', () => {
  const run = app([`process:${IN}`]);
  assert.deepEqual(run('facetCounts("operation")'), {ingestion: 3, understanding: 2, impact_analysis: 2, research: 2, validation: 3, documentation: 3, governance: 4, modeling: 2});
  assert.equal(run('visiblePrompts().length'), 21);
});
test('operation selection restricts stages in reverse', () => {
  const run = app(['operation:modeling']);
  assert.deepEqual(run('facetCounts("process")'), {[CORE]: 3, [WORK]: 3, [IN]: 2});
  assert.equal(run('visiblePrompts().length'), 4);
});
test('facets honor other selections, query, mode and family; own values are OR', () => {
  const run = app([`process:${CORE}`, `process:${RELEASE}`, 'operation:documentation', 'operation:governance', 'mode:manual', 'family:bcreq']);
  assert.equal(run('visiblePrompts().length'), 13);
  assert.deepEqual(run('facetCounts("process")'), {[IN]: 7, [CORE]: 11, [WORK]: 12, [RELEASE]: 8});
  assert.deepEqual(run('facetCounts("operation")'), {understanding: 2, impact_analysis: 2, research: 2, ingestion: 1, validation: 4, documentation: 8, governance: 5, modeling: 3, quality: 1, release_readiness: 1});
  const searched = app([`process:${IN}`], 'c07-web-evidence');
  assert.deepEqual(searched('facetCounts("operation")'), {research: 1});
  assert.deepEqual(app(['family:missing'])('facetCounts("process")'), {});
});
test('zero-count selections can be removed and unselected choices are disabled both ways', () => {
  const run = app([`process:${IN}`, 'operation:modeling']);
  const buttons = run('renderFilters(); nodes.filters.children.flatMap(group => group.children[1].children).map(button => ({token: button.dataset.filterToken, disabled: !!button.disabled}))');
  assert.equal(buttons.find(b => b.token === `process:${IN}`).disabled, false);
  assert.equal(buttons.find(b => b.token === `process:${RELEASE}`).disabled, true);
  assert.equal(buttons.find(b => b.token === 'operation:modeling').disabled, false);
  assert.equal(buttons.find(b => b.token === 'operation:solution_design').disabled, true);
});
