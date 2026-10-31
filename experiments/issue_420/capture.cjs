/* NODE_PATH=$(npm root -g) node experiments/issue_420/capture.cjs
 * Issue #420: capture the current Standards page (read-only) and audit its structure.
 * Serves local site/ files at the canonical origin with a synthetic login password
 * (same approach as experiments/issue_395/browser-check.cjs). No network requests leave
 * the machine; the site itself is NOT modified.
 * Outputs: docs/screenshots/issue-420-*.png and experiments/issue_420/page-audit.json
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const shots = path.join(root, 'docs/screenshots');

async function open(browser, viewport, hashes, password) {
  const context = await browser.newContext({viewport});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) return route.abort();
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
    if (relative === 'password-hashes.json') return route.fulfill({contentType: 'application/json', body: JSON.stringify(hashes)});
    const file = path.resolve(root, 'site', relative);
    if (!file.startsWith(path.join(root, 'site') + path.sep)) return route.abort();
    const types = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
    try { await route.fulfill({body: await fs.readFile(file), contentType: types[path.extname(file)] || 'application/octet-stream'}); }
    catch { await route.fulfill({status: 404, body: ''}); }
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  await page.goto(home + '#standards');
  await page.waitForURL(home + 'login.html');
  await page.locator('#password').fill(password);
  await page.locator('button[type=submit]').click();
  await page.waitForURL(home);
  await page.goto(home + '#standards');
  await page.locator('#standards').waitFor({state: 'visible'});
  await page.waitForTimeout(400);
  return {context, page};
}

async function main() {
  const hashes = JSON.parse(await fs.readFile(path.join(root, 'site/password-hashes.json')));
  const password = 'Issue-420-Synthetic-Login';
  hashes.site.hash = crypto.createHash('sha256').update(hashes.site.salt + password).digest('hex');
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  try {
    const {context, page} = await open(browser, {width: 1440, height: 1000}, hashes, password);
    await page.screenshot({path: path.join(shots, 'issue-420-standards-top.png')});
    // The sticky top bar would overlap element screenshots of long cards.
    await page.addStyleTag({content: '.topbar{position:static !important}'});
    await page.locator('#standard-2').screenshot({path: path.join(shots, 'issue-420-section-2-card.png')});
    await page.locator('#standard-3').screenshot({path: path.join(shots, 'issue-420-section-3-card.png')});
    await page.locator('#standard-1').screenshot({path: path.join(shots, 'issue-420-section-1-card.png')});

    const audit = await page.evaluate(() => {
      const words = s => (s.trim().match(/[\p{L}\p{N}]+(?:[-–][\p{L}\p{N}]+)*/gu) || []).length;
      const nav = document.querySelector('.standards-index').getBoundingClientRect();
      const content = document.querySelector('.standards-content').getBoundingClientRect();
      const cards = [...document.querySelectorAll('#standards [data-bcreq-section]')].map(card => {
        const blocks = [...card.children].map(el => {
          if (el.classList.contains('standard-heading')) return 'heading';
          if (el.tagName === 'P' && el.classList.contains('standard-sources')) return 'sources';
          if (el.tagName === 'P') return 'lead';
          if (el.tagName === 'DL') return `definitions(${el.querySelectorAll('dt').length})`;
          if (el.tagName === 'H3') return `h3:${el.textContent.trim()}`;
          if (el.tagName === 'UL') return `checklist(${el.querySelectorAll('li').length})`;
          if (el.tagName === 'DETAILS') return `example:${el.querySelector('summary').textContent.trim()}`;
          return el.tagName.toLowerCase();
        });
        const items = [...card.querySelectorAll('.standard-checklist li')].map(li => {
          const text = li.textContent.trim();
          const subs = [...new Set(text.match(/\b\d\.\d(?:\.\d)?\b/g) || [])];
          return {words: words(text), subsections: subs, merged: subs.length >= 2};
        });
        return {
          section: card.dataset.bcreqSection,
          title: card.querySelector('h2').textContent.trim(),
          eyebrow: card.querySelector('.eyebrow').textContent.trim(),
          blocks,
          words: words(card.textContent),
          checklistItems: items.length,
          mergedSubsectionItems: items.filter(i => i.merged).map(i => i.subsections),
          longestItemWords: Math.max(...items.map(i => i.words)),
          hasWhatFirst: card.children[1].tagName === 'P',
          hasExample: !!card.querySelector('details'),
          industrySources: card.querySelectorAll('.standard-sources a').length - 1,
        };
      });
      return {
        navSide: nav.left < content.left ? 'left' : 'right',
        navItems: [...document.querySelectorAll('.standards-index a')].map(a => a.textContent.trim()),
        hasDocumentStructureOverview: !!document.querySelector('#standards [data-document-structure]'),
        subsectionNumbersInNav: [...document.querySelectorAll('.standards-index a')].some(a => /\d\.\d/.test(a.textContent)),
        introWords: words(document.querySelector('.standards-intro').textContent),
        workflowWords: words(document.querySelector('.standards-workflow').textContent),
        totalWords: words(document.querySelector('#standards').textContent),
        cards,
      };
    });
    await fs.writeFile(path.join(__dirname, 'page-audit.json'), JSON.stringify(audit, null, 2) + '\n');
    console.log(JSON.stringify(audit, null, 2));
    await context.close();

    const mobile = await open(browser, {width: 390, height: 844}, hashes, password);
    await mobile.page.screenshot({path: path.join(shots, 'issue-420-standards-mobile.png')});
    await mobile.context.close();
  } finally {
    await browser.close();
  }
}
main().catch(e => { console.error(e); process.exit(1); });
