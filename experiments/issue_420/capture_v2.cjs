/* NODE_PATH=$(npm root -g) node experiments/issue_420/capture_v2.cjs
 * Issue #420 (RFC v0.2): screenshots of ALL site pages with the recommended content.
 * Serves experiments/issue_420/site-v2/out/ (built by site-v2/build.py from a copy of site/)
 * at the canonical origin with a synthetic login password. site/ itself is NOT modified.
 * Outputs: docs/screenshots/issue-420-v2-*.png and experiments/issue_420/site-v2/audit.json
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const served = path.join(root, 'experiments/issue_420/site-v2/out');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const shots = path.join(root, 'docs/screenshots');
const shot = name => path.join(shots, `issue-420-v2-${name}.png`);

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
  const password = 'Issue-420-Synthetic-Login';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  const audit = {};
  try {
    const {context, page, errors} = await open(browser, {width: 1440, height: 1000}, hashes, password);
    await go(page, '#about', '#about');
    await page.screenshot({path: shot('about'), fullPage: true});
    await go(page, '#catalog', '#catalog');
    await page.screenshot({path: shot('catalog')});
    await go(page, '#standards', '#standards');
    await page.screenshot({path: shot('standards-top')});
    await page.addStyleTag({content: '.topbar{position:static !important}'});
    await page.locator('#standard-intro').screenshot({path: shot('standards-intro')});
    for (let n = 1; n <= 8; n++) await page.locator(`#standard-${n}`).screenshot({path: shot(`standards-card-${n}`)});
    await page.locator('#standard-3 details').evaluate(d => { d.open = true; });
    await page.locator('#standard-3').screenshot({path: shot('standards-card-3-example')});
    await go(page, '#processes', '#bcreq-manual');
    await page.screenshot({path: shot('processes')});
    await page.evaluate(() => document.querySelectorAll('.v2-stream').forEach(d => { d.open = false; }));
    await page.screenshot({path: shot('processes-collapsed')});
    await go(page, '#dashboard', '#dashboard');
    await page.screenshot({path: shot('dashboard'), fullPage: true});
    await go(page, '#glossary', '#glossary');
    await page.screenshot({path: shot('glossary'), fullPage: true});
    // A term link on the Standards page opens the Справочник entry.
    await go(page, '#standards', '#standards');
    await page.locator('#standard-intro a.v2-term', {hasText: 'ФДР'}).first().click();
    await page.locator('#term-fdr.is-highlighted').waitFor({state: 'visible'});
    await page.waitForTimeout(300);
    await page.screenshot({path: shot('glossary-term-link')});

    audit.pages = await page.evaluate(() => [...document.querySelectorAll('#topnav a[data-nav]')].map(a => a.textContent.trim()));
    await go(page, '#standards', '#standards');
    Object.assign(audit, await page.evaluate(() => {
      const cards = [...document.querySelectorAll('#standards [data-bcreq-section]')].map(card => ({
        section: card.dataset.bcreqSection,
        title: card.querySelector('h2').textContent.trim(),
        blocks: [...card.querySelectorAll(':scope > h3')].map(h => h.textContent.trim()),
        example: card.querySelector(':scope > details summary').textContent.trim(),
      }));
      const text = document.querySelector('#standards').innerText;
      return {
        h1: document.querySelector('#standards h1').textContent.trim(),
        introItems: [...document.querySelectorAll('.v2-intro-list > li')].length,
        introTables: document.querySelectorAll('#standard-intro table').length,
        cards,
        sameTemplate: cards.every(c => JSON.stringify(c.blocks) === JSON.stringify(cards[0].blocks)),
        forbidden: ['Коротко', 'за одну минуту', 'Что готовим на каждой стадии', 'EARS', 'Как читать эту памятку', '3.1.1']
          .filter(s => text.includes(s)),
        ftIds: (text.match(/ФТ-\d\d/g) || []).length,
        termLinks: document.querySelectorAll('#standards a.v2-term').length,
      };
    }));
    const termIds = await page.evaluate(() => [...document.querySelectorAll('a.v2-term')].map(a => a.getAttribute('href').split('term=')[1]));
    audit.brokenTermLinks = await page.evaluate(ids => ids.filter(id => !document.getElementById(`term-${id}`)), termIds);
    audit.dashboardPhaseSummaryVisible = await page.evaluate(() => [...document.querySelectorAll('.phase-summary')].some(p => p.offsetParent));
    audit.consoleErrors = errors;
    await context.close();

    const mobile = await open(browser, {width: 390, height: 844}, hashes, password);
    await go(mobile.page, '#standards', '#standards');
    await mobile.page.screenshot({path: shot('standards-mobile')});
    await mobile.context.close();
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(root, 'experiments/issue_420/site-v2/audit.json'), JSON.stringify(audit, null, 2) + '\n');
  console.log(JSON.stringify(audit, null, 2));
}

main().catch(error => { console.error(error); process.exit(1); });
