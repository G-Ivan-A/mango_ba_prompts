/* NODE_PATH=$(npm root -g) node experiments/issue_450/capture.cjs <before|after>
 * Issue #450: screenshots of the "Процессы" page (test-kit step cards).
 * Serves site/ as is at the canonical origin; only password-hashes.json is
 * replaced in the browser by a synthetic hash, the repository is not modified.
 * Outputs: site/screenshots/issue-450/<label>-*.png and
 * experiments/issue_450/audit-<label>.json (console errors, card checks).
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const served = path.join(root, 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const label = process.argv[2] || 'after';
const shot = name => path.join(root, 'site/screenshots/issue-450', `${label}-${name}.png`);

async function open(browser, viewport, hashes, password) {
  const context = await browser.newContext({viewport});
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: 'https://g-ivan-a.github.io'});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) return route.abort();
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
    if (relative === 'password-hashes.json') return route.fulfill({contentType: 'application/json', body: JSON.stringify(hashes)});
    const file = path.resolve(served, relative);
    if (!file.startsWith(served + path.sep)) return route.abort();
    const types = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
    try { await route.fulfill({body: await fs.readFile(file), contentType: types[path.extname(file)] || 'application/octet-stream'}); }
    catch { await route.fulfill({status: 404, body: ''}); }
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('requestfailed', r => errors.push('requestfailed ' + r.url()));
  await page.goto(home + '#about');
  await page.waitForURL(home + 'login.html');
  await page.locator('#password').fill(password);
  await page.locator('button[type=submit]').click();
  await page.waitForURL(home);
  return {context, page, errors};
}

async function main() {
  const hashes = JSON.parse(await fs.readFile(path.join(served, 'password-hashes.json')));
  const password = 'Issue-448-Synthetic-Login';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  const audit = {label};
  try {
    for (const [name, viewport] of [['desktop', {width: 1440, height: 1000}], ['mobile', {width: 390, height: 844}]]) {
      const {context, page, errors} = await open(browser, viewport, hashes, password);
      await page.goto(home + '#processes');
      await page.locator('#bcreq-testkit-steps li').first().waitFor({state: 'visible'});
      await page.waitForTimeout(500);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({path: shot(`processes-${name}`), fullPage: false});
      await page.locator('#bcreq-testkit').screenshot({path: shot(`testkit-${name}`)});
      audit[name] = await page.evaluate(() => {
        const cards = [...document.querySelectorAll('#bcreq-testkit-steps li.testkit-step')];
        const visible = cards.filter(card => card.offsetParent !== null);
        return {
          cards: cards.length,
          visibleCards: visible.length,
          withPrepare: cards.filter(card => card.querySelector('[data-field="prepare"]')).length,
          withActions: cards.filter(card => card.querySelector('ol.bcreq-actions li')).length,
          withResult: cards.filter(card => card.querySelector('[data-field="result"]')).length,
          tabs: [...document.querySelectorAll('[data-process-tab]')].map(tab => tab.textContent.trim()),
          horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
          // Elements whose right edge goes past the viewport (overflow causes).
          overflowing: [...document.querySelectorAll('body *')]
            .filter(node => node.offsetParent !== null && node.getBoundingClientRect().right > window.innerWidth + 1)
            .slice(0, 8)
            .map(node => `${node.tagName.toLowerCase()}${node.id ? '#' + node.id : ''}.${[...node.classList].join('.')} right=${Math.round(node.getBoundingClientRect().right)}`),
        };
      });
      // Copy check: the first line of the copied text names the prompt.
      const copy = page.locator('#bcreq-testkit-steps li.testkit-step .copy-icon').first();
      if (await copy.isVisible()) {
        await copy.click();
        await page.waitForTimeout(300);
        const text = await page.evaluate(() => navigator.clipboard.readText());
        audit[name].copiedFirstLine = text.split('\n')[0];
      }
      // Each process tab, if present.
      const tabs = page.locator('[data-process-tab]');
      for (let i = 0; i < await tabs.count(); i++) {
        await tabs.nth(i).click();
        await page.waitForTimeout(300);
        const key = await tabs.nth(i).getAttribute('data-process-tab');
        if (name === 'desktop') await page.screenshot({path: shot(`tab-${key}`), fullPage: false});
        audit[name][`tab:${key}`] = await page.evaluate(() => ({
          hash: window.location.hash,
          visibleCards: [...document.querySelectorAll('#bcreq-testkit-steps li.testkit-step')]
            .filter(node => node.offsetParent !== null).map(node => node.querySelector('.bcreq-step-number').textContent),
          visibleSections: [...document.querySelectorAll('section[data-page="processes"]')]
            .filter(node => !node.hidden).map(node => node.id),
          horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
          overflowing: [...document.querySelectorAll('body *')]
            .filter(node => node.offsetParent !== null && node.getBoundingClientRect().right > window.innerWidth + 1)
            .slice(0, 6)
            .map(node => `${node.tagName.toLowerCase()}${node.id ? '#' + node.id : ''}.${[...node.classList].join('.')} right=${Math.round(node.getBoundingClientRect().right)}`),
        }));
      }
      // The old deep link to a manual step still opens it (issue #423).
      await page.goto(home + '#processes?step=5');
      await page.waitForTimeout(300);
      audit[name].deepLinkStep5 = await page.evaluate(() => ({
        visibleSections: [...document.querySelectorAll('section[data-page="processes"]')]
          .filter(node => !node.hidden).map(node => node.id),
        focused: document.activeElement?.id || '',
      }));
      audit[name].errors = errors;
      await context.close();
    }
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(root, `experiments/issue_450/audit-${label}.json`), JSON.stringify(audit, null, 2) + '\n');
  console.log(JSON.stringify(audit, null, 2));
}
main().catch(error => { console.error(error); process.exit(1); });
