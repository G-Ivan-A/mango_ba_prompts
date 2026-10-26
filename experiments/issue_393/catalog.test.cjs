// Exercise the shipped app functions in a lightweight DOM, without booting fetch.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { test } = require('node:test');
const data = JSON.parse(fs.readFileSync('site/data/prompts.json', 'utf8'));
const source = fs.readFileSync('site/app.js', 'utf8').replace(/\ninit\(\);\s*$/, '');
function app(tokens = [], query = '') {
  const node = () => ({dataset: {}, children: [], addEventListener() {}, setAttribute() {}, append(...children) {this.children.push(...children);}, replaceChildren(...children) {this.children = children;}});
  const context = vm.createContext({document: {querySelector: node, createElement: node, addEventListener() {}}, window: {addEventListener() {}}, data, tokens, query});
  vm.runInContext(source, context);
  vm.runInContext('state.prompts = data.prompts; state.promptsData = data; state.stats = {totals: {processes: {}, operations: {}, modes: {}}}; state.selectedFilters = new Set(tokens); state.query = query;', context);
  return expression => JSON.parse(JSON.stringify(vm.runInContext(expression, context)));
}
test('process selection restricts operation counts to actual prompts', () => {
  const run = app(['process:Приём и контекст']);
  assert.deepEqual(run('facetCounts("operation")'), {understanding: 2, impact_analysis: 1});
  assert.equal(run('visiblePrompts().length'), 3);
});
test('operation selection restricts processes in reverse', () => {
  const run = app(['operation:modeling']);
  assert.deepEqual(run('facetCounts("process")'), {'Требования и предварительное согласование': 1, 'Дизайн решения и оценка': 1, 'Сценарии вне документа': 1});
  assert.equal(run('visiblePrompts().length'), 2);
});
test('facets honor other selections, query, mode and family; own values are OR', () => {
  const run = app(['process:Требования и предварительное согласование', 'process:Дизайн решения и оценка', 'operation:documentation', 'operation:modeling', 'mode:stepwise', 'family:bcreq']);
  assert.equal(run('visiblePrompts().length'), 4);
  assert.deepEqual(run('facetCounts("process")'), {'Требования и предварительное согласование': 3, 'Дизайн решения и оценка': 2});
  assert.deepEqual(run('facetCounts("operation")'), {documentation: 3, risk_analysis: 1, solution_design: 1, modeling: 1});
  const searched = app(['process:Приём и контекст'], 'bcreq-products-impact');
  assert.deepEqual(searched('facetCounts("operation")'), {impact_analysis: 1});
  assert.deepEqual(app(['family:missing'])('facetCounts("process")'), {});
});
test('zero-count selections can be removed and unselected choices are disabled both ways', () => {
  const run = app(['process:Приём и контекст', 'operation:modeling']);
  const buttons = run('renderFilters(); nodes.filters.children.flatMap(group => group.children[1].children).map(button => ({token: button.dataset.filterToken, disabled: !!button.disabled}))');
  assert.equal(buttons.find(b => b.token === 'process:Приём и контекст').disabled, false);
  assert.equal(buttons.find(b => b.token === 'process:Конституция и управление').disabled, true);
  assert.equal(buttons.find(b => b.token === 'operation:modeling').disabled, false);
  assert.equal(buttons.find(b => b.token === 'operation:research').disabled, true);
});
