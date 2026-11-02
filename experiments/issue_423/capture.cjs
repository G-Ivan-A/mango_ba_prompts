/* NODE_PATH=$(npm root -g) node experiments/issue_423/capture.cjs
 * Issue #423: screenshots of site v2.0.0 (pages of PR #422, 39 BCREQ classes,
 * archive of 14 stage-1 prompts, process v0.2, site version).
 * Serves site/ as is at the canonical origin; only password-hashes.json is
 * replaced in the browser by a synthetic hash, the repository is not modified.
 * Outputs: docs/screenshots/issue-423-*.png and experiments/issue_423/audit.json
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const served = path.join(root, 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const shot = name => path.join(root, 'docs/screenshots', `issue-423-${name}.png`);

async function open(browser, viewport, hashes, password) {
  const context = await browser.newContext({viewport});
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

async function go(page, hash, selector) {
  await page.goto(home + hash);
  await page.locator(selector).first().waitFor({state: 'visible'});
  await page.waitForTimeout(500);
  await page.evaluate(() => window.scrollTo(0, 0));
}

async function main() {
  const hashes = JSON.parse(await fs.readFile(path.join(served, 'password-hashes.json')));
  const password = 'Issue-423-Synthetic-Login';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  const audit = {};
  try {
    const {context, page, errors} = await open(browser, {width: 1440, height: 1000}, hashes, password);
    await go(page, '#about', '#about-version h2');
    await page.screenshot({path: shot('about'), fullPage: true});
    audit.nav = await page.evaluate(() => [...document.querySelectorAll('#topnav a[data-nav]')].map(a => a.textContent.trim()));
    audit.version = await page.evaluate(() => ({
      shown: [...document.querySelectorAll('[data-site-version]')].map(n => n.textContent.trim()),
      panel: document.querySelector('#about-version').innerText,
    }));

    await go(page, '#catalog', '#prompt-grid > *');
    await page.screenshot({path: shot('catalog')});
    audit.catalogDefault = await page.locator('#prompt-grid > *').count();

    await page.locator('[data-filter-token="family:archive"]').click();
    await page.waitForTimeout(400);
    audit.catalogArchiveOnly = await page.locator('#prompt-grid > *').count();
    await page.evaluate(() => document.querySelector('#catalog').scrollIntoView());
    await page.screenshot({path: shot('catalog-archive')});

    await go(page, '#prompt=mango-bcreq-work-solution-design-oneshot', '#prompt-grid > *');
    audit.noAnalogCard = await page.locator('#prompt-grid > *').first().innerText();
    await page.locator('#prompt-grid > *').first().screenshot({path: shot('catalog-archive-no-analog')});

    await go(page, '#standards', '#standards');
    await page.screenshot({path: shot('standards')});

    await go(page, '#processes', '#bcreq-route .bcreq-route-stage');
    await page.addStyleTag({content: '.topbar{position:static !important}'});
    const top = await page.locator('#bcreq-manual').boundingBox();
    const rules = await page.locator('#bcreq-rules').boundingBox();
    await page.screenshot({path: shot('processes-route'), fullPage: true, clip: {x: 0, y: top.y, width: 1440, height: rules.y - top.y}});
    audit.routeChips = await page.locator('#bcreq-route .bcreq-route-chip').count();
    await go(page, '#processes?step=12', '#bcreq-step-12');
    await page.locator('#bcreq-step-12').scrollIntoViewIfNeeded();
    await page.screenshot({path: shot('processes-step')});

    await go(page, '#dashboard', '#metrics-grid > *');
    await page.screenshot({path: shot('dashboard'), fullPage: true});
    audit.dashboardTiles = await page.evaluate(() => [...document.querySelectorAll('#metrics-grid > *')].map(n => n.innerText.replace(/\s+/g, ' ').trim()));

    await go(page, '#glossary', '#glossary');
    await page.screenshot({path: shot('glossary')});
    audit.consoleErrors = errors;
    await context.close();

    const mobile = await open(browser, {width: 390, height: 844}, hashes, password);
    await go(mobile.page, '#catalog', '#prompt-grid > *');
    await mobile.page.screenshot({path: shot('catalog-mobile')});
    audit.mobileErrors = mobile.errors;
    await mobile.context.close();
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(root, 'experiments/issue_423/audit.json'), JSON.stringify(audit, null, 2) + '\n');
  console.log(JSON.stringify(audit, null, 2));
}

main().catch(error => { console.error(error); process.exit(1); });
