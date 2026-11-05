/* SITE_ROOT=<checkout with the gate commit reverted> NODE_PATH=$(npm root -g) \
 *   node experiments/issue_460/revert-browser-check.cjs
 * Issue #460: after `git revert` of the gate commit the login form works again.
 * The hash is synthetic and exists only in the browser route: the repository
 * password is neither known nor needed. Exit code 1 on any failed check.
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');

const served = path.join(path.resolve(process.env.SITE_ROOT), 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const TYPES = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
const PASSWORD = 'Issue-460-Synthetic-Login';
const results = [];
const check = (name, ok, detail = '') => {
  results.push({name, ok});
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? `  (${detail})` : ''}`);
};

(async () => {
  const hashes = JSON.parse(await fs.readFile(path.join(served, 'password-hashes.json')));
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + PASSWORD).digest('hex');
  const browser = await chromium.launch();
  const context = await browser.newContext({viewport: {width: 1280, height: 800}});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) return route.abort();
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
    if (relative === 'password-hashes.json') return route.fulfill({contentType: 'application/json', body: JSON.stringify(hashes)});
    const file = path.resolve(served, relative.endsWith('/') ? `${relative}index.html` : relative);
    if (!file.startsWith(served + path.sep)) return route.abort();
    try { await route.fulfill({body: await fs.readFile(file), contentType: TYPES[path.extname(file)] || 'application/octet-stream'}); }
    catch { await route.fulfill({status: 404, body: ''}); }
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);

  await page.goto(home);
  await page.waitForURL(/login\.html/);
  check('прямая ссылка ведёт на форму входа', page.url().includes('login.html'), page.url());

  await page.locator('#password').fill('wrong-password');
  await page.locator('button[type=submit]').click();
  await page.waitForFunction(() => document.querySelector('#login-error').textContent !== '');
  check('неверный пароль отклонён', (await page.locator('#login-error').textContent()) === 'Неверный пароль');

  await page.locator('#password').fill(PASSWORD);
  await page.locator('button[type=submit]').click();
  await page.waitForURL(home);
  await page.goto(`${home}#processes`);
  await page.waitForSelector('#bcreq-testkit-steps .testkit-step');
  const visible = await page.evaluate(() =>
    [...document.querySelectorAll('#bcreq-testkit-steps .testkit-step')].filter(node => node.getClientRects().length > 0).length);
  check('после входа видны все 13 шагов', visible === 13, String(visible));
  check('кнопка выхода на месте', (await page.locator('#site-logout').count()) === 1);

  await page.locator('#site-logout').click();
  await page.waitForURL(/login\.html/);
  check('выход возвращает на форму входа', page.url().includes('login.html'));

  await browser.close();
  const failed = results.filter(item => !item.ok).length;
  console.log(`${results.length - failed}/${results.length} passed`);
  process.exit(failed ? 1 : 0);
})().catch(error => { console.error(error); process.exit(1); });
