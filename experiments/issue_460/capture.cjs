/* NODE_PATH=$(npm root -g) node experiments/issue_460/capture.cjs <before|after>
 * Issue #460: what a visitor really sees on "Процессы" and whether the password
 * form appears. Serves site/ as is at the canonical origin, no external requests.
 * "before" logs in with a synthetic hash that exists only in the browser route
 * (the repository password is neither known nor needed).
 * Outputs: site/screenshots/issue-460/<label>-*.png, experiments/issue_460/audit-<label>.json
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(process.env.SITE_ROOT || path.join(__dirname, '../..'));
const served = path.join(root, 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const label = process.argv[2] || 'after';
const shotDir = path.join(__dirname, '../../site/screenshots/issue-460');
const shot = name => path.join(shotDir, `${label}-${name}.png`);
const TYPES = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
const PASSWORD = 'Issue-460-Synthetic-Login';

async function open(browser, viewport) {
  const hashes = JSON.parse(await fs.readFile(path.join(served, 'password-hashes.json')));
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + PASSWORD).digest('hex');
  const context = await browser.newContext({viewport});
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: 'https://g-ivan-a.github.io'});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) return route.abort();
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
    if (relative === 'password-hashes.json') return route.fulfill({contentType: 'application/json', body: JSON.stringify(hashes)});
    const file = path.resolve(served, relative.endsWith('/') ? relative + 'index.html' : relative);
    if (!file.startsWith(served + path.sep)) return route.abort();
    try { await route.fulfill({body: await fs.readFile(file), contentType: TYPES[path.extname(file)] || 'application/octet-stream'}); }
    catch { await route.fulfill({status: 404, body: ''}); }
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED/.test(m.text())) errors.push(m.text()); });
  return {context, page, errors};
}

// Password form on a direct link: the first thing issue #460 complains about.
async function entry(page) {
  await page.goto(home + '#processes');
  await page.waitForLoadState('load');
  await page.waitForTimeout(600);
  const redirected = page.url().includes('login.html');
  if (redirected) {
    await page.locator('#password').fill(PASSWORD);
    await page.locator('button[type=submit]').click();
    await page.waitForURL(home);
    await page.goto(home + '#processes');
  }
  return {askedForPassword: redirected};
}

const visibleSteps = page => page.evaluate(() =>
  [...document.querySelectorAll('#bcreq-testkit-steps .testkit-step')]
    .filter(node => node.getClientRects().length > 0)
    .map(node => node.querySelector('.bcreq-step-title').textContent));

async function main() {
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  const audit = {label};
  try {
    for (const [name, viewport] of [['desktop', {width: 1440, height: 1000}], ['mobile', {width: 390, height: 844}]]) {
      const {context, page, errors} = await open(browser, viewport);
      const result = await entry(page);
      await page.locator('#bcreq-testkit-steps .testkit-step').first().waitFor({state: 'visible'});
      await page.waitForTimeout(400);
      result.defaultVisibleSteps = await visibleSteps(page);
      result.stepsInDom = await page.locator('#bcreq-testkit-steps .testkit-step').count();
      result.tabs = await page.locator('[data-process-tab]').evaluateAll(tabs => tabs.map(t => t.textContent));
      result.promptTextContainers = await page.locator('#bcreq-testkit-steps .testkit-prompt-text').count();
      result.horizontalScroll = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({path: shot(`processes-${name}`)});
      result.errors = errors;
      audit[name] = result;
      await context.close();
    }
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(__dirname, `audit-${label}.json`), JSON.stringify(audit, null, 2) + '\n');
  console.log(JSON.stringify(audit, null, 2));
}
main().catch(error => { console.error(error); process.exit(1); });
