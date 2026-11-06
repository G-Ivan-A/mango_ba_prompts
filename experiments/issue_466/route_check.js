// Execute the real hash router with a small DOM boundary; no browser install.
// Browser/layout/keyboard coverage is in browser_check.js (Playwright MCP).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const app = fs.readFileSync(process.argv[2] || path.join(root, 'site/app.js'), 'utf8');
const route = app.slice(app.indexOf('function applyRoute()'), app.indexOf('function applyTheme('));
assert.ok(route.startsWith('function applyRoute()'));

for (const section of ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ttz']) {
  const group = {tagName: 'DETAILS', open: false, parentElement: null};
  const wrapper = {tagName: 'DIV', parentElement: group};
  let focused = false;
  let scrolled = false;
  const id = section === '0' ? 'standard-intro' : section === '9' ? 'standard-industry'
    : section === 'ttz' ? 'standard-ttz' : `standard-${section}`;
  const target = {parentElement: wrapper,
    focus: () => { assert.ok(group.open, 'must reveal before focus'); focused = true; },
    scrollIntoView: () => { assert.ok(group.open); scrolled = true; }};
  const ctx = vm.createContext({
    currentPage: () => 'standards', closeProcessModal: () => {}, URLSearchParams,
    window: {location: {hash: `#standards?section=${section}`}, scrollTo: () => {}},
    document: {querySelectorAll: () => [], getElementById: actual => {
      assert.equal(actual, id); return target;
    }}, nodes: {topnav: {querySelectorAll: () => []}},
  });
  vm.runInContext(route + '\napplyRoute();', ctx);
  assert.ok(group.open && focused && scrolled, section);
}
// Unknown input must remain safe; no attempt to resolve arbitrary DOM IDs.
for (const section of ['', '10', 'ttz-invalid', '<script>']) {
  vm.runInNewContext(route + '\napplyRoute();', {
    currentPage: () => 'standards', closeProcessModal: () => {}, URLSearchParams,
    window: {location: {hash: `#standards?section=${section}`}, scrollTo: () => {}},
    document: {querySelectorAll: () => [], getElementById: () => assert.fail('invalid route')},
    nodes: {topnav: {querySelectorAll: () => []}},
  });
}
console.log('TTZ router: 11 deep links + 4 invalid inputs passed');
