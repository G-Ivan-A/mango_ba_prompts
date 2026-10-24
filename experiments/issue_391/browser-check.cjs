/* Real-browser regression. Run with NODE_PATH pointing to installed playwright.
 * --fixed-password verifies the issue credential in memory; no traces/logged values.
 */
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const shots = path.join(root, 'docs/screenshots/issue-391');

async function main() {
  let password = 'Browser-Fixture-Only';
  const hashes = JSON.parse(await fs.readFile(path.join(root, 'site/password-hashes.json')));
  if (process.argv.includes('--fixed-password')) {
    const { body } = JSON.parse(execFileSync('gh', ['issue', 'view', '391', '--repo', 'G-Ivan-A/mango_ba_prompts', '--json', 'body']));
    const candidates = [...new Set(body.split('\n').filter(line => /парол/i.test(line)).flatMap(line => line.match(/(?<![\p{L}])[А-ЯЁ]{5,}(?![\p{L}])/gu) || []))];
    const matching = candidates.filter(value => crypto.createHash('sha256').update(hashes.site.salt + value).digest('hex') === hashes.site.hash);
    assert.equal(matching.length, 1, 'configured credential matches issue');
    password = matching[0];
    assert.equal(crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex'), hashes.site.hash);
  } else {
    hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  }
  const catalog = JSON.parse(await fs.readFile(path.join(root, 'site/data/prompts.json')));
  const browser = await chromium.launch({ headless: true, args: ['--disable-dev-shm-usage'] });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, permissions: ['clipboard-read', 'clipboard-write'] });
    const errors = [];
    let catalogBeforeLogin = 0;
    let authenticated = false;
    let hashFailure = false;
    await context.route('**/*', async route => {
      const url = new URL(route.request().url());
      if (!url.href.startsWith(home)) return route.abort();
      const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
      if (relative === 'password-hashes.json') {
        return route.fulfill({ status: hashFailure ? 503 : 200, contentType: 'application/json', body: JSON.stringify(hashes) });
      }
      if (relative.startsWith('data/') && !authenticated) catalogBeforeLogin++;
      const file = path.resolve(root, 'site', relative);
      assert.ok(file.startsWith(path.join(root, 'site') + path.sep));
      const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml' };
      try { await route.fulfill({ body: await fs.readFile(file), contentType: types[path.extname(file)] || 'application/octet-stream' }); }
      catch { await route.fulfill({ status: 404, body: '' }); }
    });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(home);
    await page.waitForURL(home + 'login.html');
    assert.equal(catalogBeforeLogin, 0, 'catalog must not load before login');
    assert.equal(await page.locator('input').count(), 1);
    await fs.mkdir(shots, { recursive: true });
    await page.screenshot({ path: path.join(shots, 'after-login.png') });
    for (const wrong of ['incorrect', password.toLowerCase(), ` ${password}`, `${password} `]) {
      await page.locator('#password').fill(wrong);
      await page.locator('button[type=submit]').click();
      await page.getByText('Неверный пароль', { exact: true }).waitFor();
      assert.equal(page.url(), home + 'login.html');
    }
    await page.locator('#password').fill('');
    await page.screenshot({ path: path.join(shots, 'after-login-error.png') });
    hashFailure = true;
    await page.locator('#password').fill('unavailable');
    await page.locator('button[type=submit]').click();
    await page.getByText('Не удалось проверить пароль. Повторите попытку.').waitFor();
    assert.equal(page.url(), home + 'login.html');
    hashFailure = false;
    await page.locator('#password').fill(password);
    authenticated = true;
    await page.locator('button[type=submit]').click();
    await page.waitForURL(home);
    await page.locator('.prompt-card').first().waitFor();
    assert.equal(await page.locator('.prompt-card').count(), catalog.prompts.length);
    await page.screenshot({ path: path.join(shots, 'after-catalog.png'), fullPage: true });
    await page.locator('[data-nav=processes]').click();
    await page.locator('#bcreq-manual').waitFor({ state: 'visible' });
    assert.equal(await page.locator('section[data-page=processes]:visible').count(), 2);
    const copies = page.locator('#bcreq-steps [data-copy-id]');
    assert.equal(await copies.count(), 11);
    for (let i = 0; i < await copies.count(); i++) {
      const button = copies.nth(i);
      const id = await button.getAttribute('data-copy-id');
      await button.click();
      const copied = await page.evaluate(() => navigator.clipboard.readText());
      const prompt = catalog.prompts.find(prompt => prompt.id === id);
      assert.equal(copied, `<!-- ${id} -->\n\n${prompt.body}`);
    }
    await page.locator('#toast[data-visible=false]').waitFor({ state: 'attached' });
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: path.join(shots, 'after-processes.png'), fullPage: true });
    for (const route of ['dashboard', 'roadmap', 'patterns', 'catalog']) {
      await page.locator(`[data-nav=${route}]`).click();
      await page.locator(`section[data-page=${route}]:visible`).first().waitFor();
    }
    await page.locator('#theme-toggle').click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
    await page.locator('#theme-toggle').click();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('[data-nav=processes]').click();
    await page.locator('#bcreq-manual').waitFor({ state: 'visible' });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'mobile page must fit viewport');
    assert.equal(await page.locator('.topnav a').evaluateAll(links => links.every(link => link.scrollWidth <= link.clientWidth)), true, 'mobile navigation labels must fit their buttons');
    await page.screenshot({ path: path.join(shots, 'after-mobile.png') });
    await page.locator('#site-logout').click();
    await page.waitForURL(home + 'login.html');
    authenticated = false;
    assert.equal(await page.evaluate(() => sessionStorage.getItem('mango-site-access')), null);
    await page.goto(home + 'reports/index.html');
    await page.waitForURL(/login\.html\?next=/);
    await page.locator('#password').fill(password);
    authenticated = true;
    await page.locator('button[type=submit]').click();
    await page.waitForURL(home + 'reports/index.html');
    // Rotation invalidates the old session; configuration failure must stay locked.
    hashes.site.hash = '0'.repeat(64);
    await page.goto(home);
    await page.waitForURL(home + 'login.html');
    assert.deepEqual(errors, []);
    console.log(`PASS: separate login, exact credential, failure/retry, canonical redirect, ${catalog.prompts.length} BCREQ cards, 11 copies, two process blocks, other routes, mobile, logout, reports and rotation`);
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
