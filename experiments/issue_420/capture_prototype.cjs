/* NODE_PATH=$(npm root -g) node experiments/issue_420/capture_prototype.cjs
 * Issue #420: screenshots of the proposed Standards page prototype (not part of site/).
 */
const {chromium} = require('playwright');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const url = 'file://' + path.join(__dirname, 'prototype/standards-v2.html');
const shots = path.join(root, 'docs/screenshots');
(async () => {
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    await page.goto(url);
    await page.screenshot({path: path.join(shots, 'issue-420-proposal-top.png')});
    await page.locator('#standard-0').screenshot({path: path.join(shots, 'issue-420-proposal-introduction.png')});
    for (const n of ['1', '3']) {
      await page.locator(`#standard-${n}`).screenshot({path: path.join(shots, `issue-420-proposal-section-${n}-card.png`)});
    }
    const audit = await page.evaluate(() => [...document.querySelectorAll('[data-bcreq-section]')].map(card => ({
      section: card.dataset.bcreqSection,
      blocks: [...card.querySelectorAll(':scope > h3, :scope > .std-special h3, :scope > details summary')].map(x => x.textContent.trim()),
      checks: card.querySelectorAll('.standard-checklist li').length,
      checksAnchoredToOneSubsection: card.querySelectorAll('.standard-checklist li > .ref').length,
    })));
    console.log(JSON.stringify(audit, null, 1));
    const mobile = await browser.newPage({viewport: {width: 390, height: 844}});
    await mobile.goto(url);
    await mobile.screenshot({path: path.join(shots, 'issue-420-proposal-mobile.png')});
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
