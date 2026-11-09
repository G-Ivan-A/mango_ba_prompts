// Run actual shipped filter functions in a small DOM stub; no browser/build needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {test} = require('node:test');
const data = JSON.parse(fs.readFileSync('site/data/prompts.json','utf8'));
const source = fs.readFileSync(process.env.MANGO_APP_SOURCE || 'site/app.js','utf8').replace(/\ninit\(\);\s*$/,'');
const IN = 'A-IN · Приём задачи';
function app(tokens=[], query='') {
  const node=()=>({dataset:{},children:[],addEventListener(){},setAttribute(){},append(...c){this.children.push(...c)},replaceChildren(...c){this.children=c}});
  const c=vm.createContext({document:{querySelector:node,querySelectorAll:()=>[],createElement:node,addEventListener(){}},window:{addEventListener(){}},data,tokens,query});
  vm.runInContext(source,c,{timeout:1000});
  vm.runInContext('state.prompts=data.prompts; state.promptsData=data; state.selectedFilters=new Set(tokens); state.query=query;',c,{timeout:1000});
  return expression=>JSON.parse(JSON.stringify(vm.runInContext(expression,c,{timeout:1000})));
}
test('archive + A-IN finds the original intake prompts and four 2.7.0 snapshots', {timeout:5000},()=>{
  const run=app(['family:archive',`process:${IN}`]);
  const prompts=run('visiblePrompts()');
  assert.ok(prompts.some(p=>p.file==='bcreq-context-understanding-stepwise.md' && !p.archiveInfo));
  assert.equal(prompts.filter(p=>p.archiveInfo).length,4);
  assert.ok(run('facetCounts("process")')[IN]>0);
  assert.ok(run('facetCounts("operation")').understanding>0);
});
test('archive facets honor process/operation OR, group AND, modes and searches', {timeout:5000},()=>{
  const tokens=['family:archive',`process:${IN}`,'operation:understanding','operation:impact_analysis','mode:stepwise'];
  const prompts=app(tokens)('visiblePrompts()');
  assert.equal(prompts.length,4);
  assert.ok(prompts.every(p=>p.archived && ['understanding','impact_analysis'].includes(p.operation.id)));
  assert.equal(app([...tokens,'mode:oneshot'])('visiblePrompts().length'),6);
  assert.equal(app(['family:archive',`process:${IN}`],'2.7.0')('visiblePrompts().length'),4);
  assert.equal(app(['family:archive',`process:${IN}`,'operation:ingestion'])('visiblePrompts().length'),1);
  assert.equal(app(['family:archive','operation:solution_design',`process:${IN}`])('visiblePrompts().length'),0);
});
test('history remains opt-in; all old active filters and both families still work', {timeout:5000},()=>{
  assert.equal(app()('visiblePrompts().length'),39);
  assert.equal(app(['family:archive'])('visiblePrompts().length'),18);
  assert.equal(app(['family:archive','family:bcreq'])('visiblePrompts().length'),57);
  assert.equal(app([`process:${IN}`])('visiblePrompts().length'),21);
  assert.equal(app(['mode:stepwise'])('visiblePrompts().length'),0);
  assert.equal(app(['family:archive'],'no-such-id')('visiblePrompts().length'),0);
});
