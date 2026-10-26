/* Local-file Chromium regression. NODE_PATH must resolve playwright.
 * --before captures the unchanged baseline and reproduces stale counts.
 * Canonical-origin routing exercises the actual login/report redirects locally.
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const before = process.argv.includes('--before');
const shots = path.join(root, 'docs/screenshots/issue-393');
const stages = ['Приём и контекст', 'Требования и предварительное согласование', 'Дизайн решения и оценка', 'Конституция и управление', 'Валидация второй ролью', 'Сценарии вне документа'];

async function main() {
  const catalog = JSON.parse(await fs.readFile(path.join(root, 'site/data/prompts.json')));
  const hashes = JSON.parse(await fs.readFile(path.join(root, 'site/password-hashes.json')));
  const password = 'Issue-393-Browser-Fixture';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({headless: true, args: ['--disable-dev-shm-usage']});
  try {
    const context = await browser.newContext({viewport: {width: 1440, height: 1050}, permissions: ['clipboard-read', 'clipboard-write']});
    await context.route('**/*', async route => {
      const url = new URL(route.request().url());
      if (!url.href.startsWith(home)) return route.abort();
      const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
      if (relative === 'password-hashes.json') return route.fulfill({contentType: 'application/json', body: JSON.stringify(hashes)});
      const file = path.resolve(root, 'site', relative);
      assert.ok(file.startsWith(path.join(root, 'site') + path.sep));
      const types = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
      try { await route.fulfill({body: await fs.readFile(file), contentType: types[path.extname(file)] || 'application/octet-stream'}); }
      catch { await route.fulfill({status: 404, body: ''}); }
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await fs.mkdir(shots, {recursive: true});
    await page.goto(home);
    await page.waitForURL(home + 'login.html');
    async function login() {
      await page.locator('#password').fill(password);
      await page.locator('button[type=submit]').click();
    }
    await login();
    await page.waitForURL(home);
    await page.locator('.prompt-card').first().waitFor();
    const button = (kind, value) => page.locator(`[data-filter-token=${JSON.stringify(`${kind}:${value}`)}]`);
    async function reset() { if (await page.locator('#clear-filters-button').isVisible()) await page.locator('#clear-filters-button').click(); }
    async function verifyFacets() {
      const tokens = await page.locator('[data-filter-token][aria-pressed=true]').evaluateAll(nodes => nodes.map(n => n.dataset.filterToken));
      const query = await page.locator('#search-input').inputValue();
      assert.equal(query, '', 'matrix uses an empty query');
      for (const kind of ['process', 'operation']) {
        const expected = {};
        const candidates = catalog.prompts.filter(prompt => ['process', 'operation', 'mode', 'family'].every(other => {
          if (other === kind) return true;
          const values = tokens.filter(t => t.startsWith(other + ':')).map(t => t.slice(other.length + 1));
          const actual = other === 'process' ? prompt.processes : [other === 'operation' ? prompt.operation.id : prompt[other]];
          return values.length === 0 || actual.some(value => values.includes(value));
        }));
        for (const prompt of candidates) for (const value of kind === 'process' ? prompt.processes : [prompt.operation.id]) expected[value] = (expected[value] || 0) + 1;
        const rendered = await page.locator(`[data-filter-token^="${kind}:"]`).evaluateAll(nodes => nodes.map(node => ({value: node.dataset.filterToken.slice(node.dataset.filterToken.indexOf(':') + 1), count: Number(node.querySelector('.filter-count').textContent), disabled: node.disabled, selected: node.getAttribute('aria-pressed') === 'true'})));
        for (const option of rendered) {
          assert.equal(option.count, expected[option.value] || 0, `${tokens}: ${kind} count ${option.value}`);
          assert.equal(option.disabled, option.count === 0 && !option.selected, `${kind} availability ${option.value}`);
        }
      }
      const matches = catalog.prompts.filter(prompt => ['process', 'operation', 'mode', 'family'].every(kind => {
        const values = tokens.filter(t => t.startsWith(kind + ':')).map(t => t.slice(kind.length + 1));
        return !values.length || (kind === 'process' ? prompt.processes : [kind === 'operation' ? prompt.operation.id : prompt[kind]]).some(value => values.includes(value));
      }));
      assert.equal(await page.locator('.prompt-card').count(), matches.length);
    }
    if (before) {
      await page.screenshot({path: path.join(shots, 'before-catalog.png')});
      assert.equal(await page.locator('.filter-group--processes button').count(), 9);
      await button('process', 'Risk Analysis').click();
      const stale = Number(await button('operation', 'documentation').locator('.filter-count').textContent());
      const actual = catalog.prompts.filter(p => p.processes.includes('Risk Analysis') && p.operation.id === 'documentation').length;
      assert.notEqual(stale, actual, 'reproduce catalog-wide counter in selected process');
      await reset();
      await button('operation', 'modeling').click();
      assert.equal(await button('process', 'Статистика').getAttribute('aria-disabled'), null, 'reproduce absent reverse cascade');
      console.log(`REPRODUCED: nine legacy stages; documentation count ${stale} vs ${actual}; unrelated process remains available after modeling selection`);
      return;
    }
    assert.deepEqual(await page.locator('.filter-group--processes .filter-label').allTextContents(), stages);
    assert.deepEqual(await page.locator('.filter-title').allTextContents(), ['Набор', 'Процессы БА', 'Операции', 'Режимы']);
    assert.equal(await page.locator('.filter-group--operations button').count(), 13);
    assert.deepEqual(await page.locator('#topnav > *').allTextContents().then(values => values.map(v => v.trim())), ['Каталог', 'Дашборд', 'Процессы', '⏻', '◐']);
    await verifyFacets();
    await page.screenshot({path: path.join(shots, 'after-catalog.png')});
    for (const stage of stages) {
      await reset(); await button('process', stage).click(); await verifyFacets();
      const active = await page.locator('.filter-group--operations button:not(:disabled)').count();
      assert.ok(active > 0);
    }
    for (const operation of catalog.filters.operations.filter(op => catalog.prompts.some(p => p.operation.id === op.id))) {
      await reset(); await button('operation', operation.id).click(); await verifyFacets();
    }
    await reset();
    await button('process', stages[1]).click();
    await button('process', stages[2]).click();
    await button('operation', 'documentation').click();
    await button('operation', 'modeling').click();
    await button('mode', 'stepwise').click();
    await button('family', 'bcreq').click();
    await verifyFacets();
    assert.equal(await page.locator('.prompt-card').count(), 4);
    await reset();
    await button('process', stages[0]).click();
    await page.screenshot({path: path.join(shots, 'after-process-cascade.png')});
    await page.locator('#search-input').fill('bcreq-products-impact');
    assert.equal(await page.locator('.prompt-card').count(), 1);
    assert.equal(await button('operation', 'impact_analysis').locator('.filter-count').textContent(), '1');
    assert.equal(await button('operation', 'understanding').isDisabled(), true);
    await page.locator('#search-input').fill('no-matching-prompt');
    assert.equal(await page.locator('.prompt-card').count(), 0);
    assert.equal(await button('process', stages[0]).isEnabled(), true, 'selected zero-count option remains removable');
    await button('process', stages[0]).click();
    await page.locator('#clear-search-button').click();
    await verifyFacets();
    await button('operation', 'modeling').click();
    await page.screenshot({path: path.join(shots, 'after-operation-cascade.png')});
    await reset();
    for (const prompt of catalog.prompts) {
      await page.locator(`#prompt-grid [data-copy-id="${prompt.id}"]`).first().click();
      assert.equal(await page.evaluate(() => navigator.clipboard.readText()), `<!-- ${prompt.id} -->\n\n${prompt.body}`);
    }
    await page.locator('[data-nav=dashboard]').click();
    await page.locator('section[data-page=dashboard]:visible').first().waitFor();
    await page.locator('[data-nav=processes]').click();
    await page.locator('#bcreq-manual').waitFor({state: 'visible'});
    assert.equal(await page.locator('section[data-page=processes]:visible').count(), 2);
    const steps = page.locator('#bcreq-steps [data-copy-id]');
    assert.equal(await steps.count(), 11);
    for (let i = 0; i < await steps.count(); i++) {
      const copy = steps.nth(i);
      const id = await copy.getAttribute('data-copy-id');
      await copy.click();
      assert.equal(await page.evaluate(() => navigator.clipboard.readText()), `<!-- ${id} -->\n\n${catalog.prompts.find(p => p.id === id).body}`);
    }
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({path: path.join(shots, 'after-processes.png'), fullPage: true});
    await page.locator('#theme-toggle').click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
    await page.locator('#theme-toggle').click();
    for (const route of ['roadmap', 'patterns']) {
      await page.goto(home + '#' + route);
      await page.locator(`section[data-page=${route}]:visible`).first().waitFor();
    }
    await page.goto(home);
    await page.locator('.prompt-card').first().waitFor();
    await page.setViewportSize({width: 390, height: 844});
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({path: path.join(shots, 'after-mobile.png')});
    for (const route of ['reports/index.html', 'reports/run-0060/index.html', 'reports/run-0060/detailed-gap-report.html']) {
      await page.goto(home + route);
      await page.waitForFunction(() => document.documentElement.dataset.gate === 'open');
      assert.equal(page.url(), home + route);
      await page.evaluate(() => sessionStorage.removeItem('mango-site-access'));
      await page.reload();
      await page.waitForURL(/login\.html\?next=/);
      await login();
      await page.waitForURL(home + route);
      await page.waitForFunction(() => document.documentElement.dataset.gate === 'open');
    }
    await page.goto(home);
    await page.locator('.prompt-card').first().waitFor();
    await page.locator('#site-logout').click();
    await page.waitForURL(home + 'login.html');
    assert.equal(await page.evaluate(() => sessionStorage.getItem('mango-site-access')), null);
    assert.deepEqual(errors, []);
    console.log('PASS: six stage mappings; reciprocal counts/availability matrix; multi-select, search, mode, family, reset; five menu items; 14 catalog and 11 step copies; two process blocks; dashboard, theme, mobile, legacy direct routes; all three gated report routes and logout');
  } finally { await browser.close(); }
}
main().catch(error => {console.error(error); process.exitCode = 1;});
