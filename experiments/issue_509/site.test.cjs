// Actual shipped copy and composition functions, with a small DOM stub.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {test} = require('node:test');
const source = fs.readFileSync(process.env.MANGO_APP_SOURCE || 'site/app.js', 'utf8').replace(/\ninit\(\);\s*$/, '');
const ain = JSON.parse(fs.readFileSync('site/data/a-in-kit.json', 'utf8'));

function app() {
  const node = () => ({dataset:{}, children:[], addEventListener(){}, setAttribute(){},
    append(...children){this.children.push(...children)}, replaceChildren(...children){this.children=children}});
  const ctx = vm.createContext({document:{querySelector:node, querySelectorAll:()=>[], createElement:node, addEventListener(){}},
    window:{addEventListener(){}}, ain});
  vm.runInContext(source, ctx, {timeout:1000});
  vm.runInContext('state.ainKit=ain; state.workingPrompts=ain.steps.map(s=>({id:s.id,body:s.prompt}));', ctx);
  return expression => vm.runInContext(expression, ctx, {timeout:1000});
}

test('all 24 full and compact copied bodies equal their generated source', {timeout:5000}, () => {
  const run = app();
  for (const step of ain.steps) {
    const expr = `{step:"${step.id}",ainId:"${step.id}",draft:{id:"${step.id}"}}`;
    assert.equal(run(`testKitBody(${expr}, "draft")`), step.prompt);
    run(`state.ainForms["${step.id}"]="compact"`);
    assert.equal(run(`testKitBody(${expr}, "draft")`), step.compactPrompt);
    run(`state.ainForms["${step.id}"]="full"`);
    assert.equal(run(`testKitBody(${expr}, "draft")`), step.prompt);
  }
});

test('size includes token estimate and warning only above interface threshold', {timeout:5000}, () => {
  const run = app();
  assert.match(run('promptSizeLabel("текст")'), /5 символов.*≈2 токенов/);
  assert.doesNotMatch(run('promptSizeLabel("а".repeat(30000))'), /вставьте текстом/);
  assert.match(run('promptSizeLabel("а".repeat(30001))'), /Если чат читает файлы частично, вставьте текстом/);
});

test('starter retains selected step format; card form is per step', {timeout:5000}, () => {
  const run = app();
  run('state.workingPrompts.push({id:"starter",body:"Конституция"}); state.stepFormat="system"');
  assert.match(run('testKitBody({step:"Ш-0 Конституция",draft:{id:"starter"}},"draft")'), /Формат шагов: системный/);
  assert.equal(run('Object.keys(state.ainForms).length'), 0);
});
