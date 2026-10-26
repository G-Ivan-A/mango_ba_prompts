/* NODE_PATH=$(npm root -g) node experiments/issue_395/browser-check.cjs [--before]
 * Serve local files at the canonical origin, using a synthetic login password.
 * No requests or content are published; all other origins are blocked.
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const before = process.argv.includes('--before');
const shots = path.join(root, 'site/screenshots/issue-395');

async function main() {
  const hashes = JSON.parse(await fs.readFile(path.join(root, 'site/password-hashes.json')));
  const password = 'Issue-395-Synthetic-Login';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  try {
    const context = await browser.newContext({viewport: {width: 1440, height: 1050}});
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
    page.setDefaultTimeout(15000);
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await fs.mkdir(shots, {recursive: true});
    await page.goto(home + '#standards');
    await page.waitForURL(home + 'login.html');
    await page.locator('#password').fill(password);
    await page.locator('button[type=submit]').click();
    await page.waitForURL(home);
    await page.locator('.prompt-card').first().waitFor();
    await page.goto(home + '#standards');
    if (before) {
      await page.locator('.prompt-card').first().waitFor();
      assert.equal(await page.locator('[data-nav=standards]').count(), 0);
      await page.screenshot({path: path.join(shots, 'before.png')});
      console.log('REPRODUCED: #standards falls back to catalog; no menu or acceptance criteria.');
      return;
    }
    await page.locator('#standards').waitFor({state: 'visible'});
    assert.deepEqual(await page.locator('#topnav a').allTextContents(), ['Каталог', 'Стандарты', 'Дашборд', 'Процессы']);
    assert.equal(await page.locator('#standards [data-bcreq-section]').count(), 8);
    assert.equal(await page.locator('section[data-page]:visible').count(), 1);
    for (let i = 1; i <= 8; i++) {
      const section = page.locator(`[data-bcreq-section="${i}"]`);
      assert.ok(await section.locator('li').count() >= 3);
      assert.ok(await section.locator('a[href^="https://"]').count() >= 1);
    }
    await page.screenshot({path: path.join(shots, 'after-desktop.png')});
    await page.screenshot({path: path.join(shots, 'after-full.png'), fullPage: true});
    await page.locator('[data-standard-target="3"]').click();
    assert.equal(new URL(page.url()).hash, '#standards?section=3');
    await page.waitForFunction(() => document.activeElement?.id === 'standard-3');
    await page.locator('#standard-3').screenshot({path: path.join(shots, 'after-criteria.png')});
    await page.reload();
    await page.waitForFunction(() => document.activeElement?.id === 'standard-3');
    await page.evaluate(() => scrollTo(0, 0));
    await page.locator('#theme-toggle').click();
    await page.screenshot({path: path.join(shots, 'after-dark.png')});
    await page.locator('#theme-toggle').click();
    for (const width of [320, 390, 720, 721, 768, 1024, 1440]) {
      await page.setViewportSize({width, height: 844});
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      const layout = await page.evaluate(() => ({width: innerWidth, scroll: document.documentElement.scrollWidth, x: scrollX,
        overflow: [...document.querySelectorAll('body *')]
          .filter(el => el.getBoundingClientRect().right + scrollX > innerWidth || el.scrollWidth > el.clientWidth + 1)
          .slice(0, 20).map(el => ({tag: el.tagName, id: el.id, class: el.className, right: el.getBoundingClientRect().right, scroll: el.scrollWidth, client: el.clientWidth}))}));
      assert.ok(layout.scroll <= layout.width, `horizontal overflow at ${width}px: ${JSON.stringify(layout)}`);
    }
    await page.setViewportSize({width: 390, height: 844});
    await page.evaluate(() => scrollTo(0, 0));
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({path: path.join(shots, 'after-mobile.png')});
    // Keyboard activation retains the standards route and focuses the section.
    await page.locator('[data-standard-target="8"]').focus();
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.activeElement?.id === 'standard-8');
    await page.setViewportSize({width: 1440, height: 1050});
    await page.locator('[data-nav=catalog]').click();
    assert.equal(await page.locator('.prompt-card').count(), 14);
    await page.locator('[data-nav=dashboard]').click();
    await page.locator('section[data-page=dashboard]:visible').first().waitFor();
    await page.locator('[data-nav=processes]').click();
    await page.locator('#bcreq-manual').waitFor({state: 'visible'});
    assert.equal(await page.locator('section[data-page=processes]:visible').count(), 2);
    assert.equal(await page.locator('#bcreq-steps [data-copy-id]').count(), 11);
    await page.goto(home + 'reports/index.html');
    await page.waitForFunction(() => document.documentElement.dataset.gate === 'open');
    await page.goto(home + '#standards');
    await page.locator('#standards').waitFor({state: 'visible'});
    await page.locator('#site-logout').click();
    await page.waitForURL(home + 'login.html');
    await page.goto(home + '#standards');
    await page.waitForURL(home + 'login.html');
    assert.equal(await page.evaluate(() => sessionStorage.getItem('mango-site-access')), null);
    assert.deepEqual(errors, []);
    console.log('PASS: gated route, real login/logout, menu, 8 checklists, section deep links/reload, keyboard, dark/mobile layout, catalog/dashboard/processes/report smoke checks.');
  } finally { await browser.close(); }
}
main().catch(e => {console.error(e); process.exitCode = 1;});
