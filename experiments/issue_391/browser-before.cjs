// Baseline reproduction: run against prepared commit 6f4cc146 with its site/
// served on port 8000. The fixed tree deliberately has no .site-gate overlay.
const { chromium } = require('playwright');
const fs = require('node:fs');
(async () => {
 const browser = await chromium.launch({headless: true, args: ['--disable-dev-shm-usage']});
 try {
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  await page.route('**/widgets.mango-office.ru/**', route => route.abort());
  await page.goto('http://127.0.0.1:8000/');
  await page.locator('.site-gate').waitFor();
  fs.mkdirSync('docs/screenshots/issue-391', {recursive:true});
  await page.screenshot({path:'docs/screenshots/issue-391/before-login.png'});
  const { site } = JSON.parse(fs.readFileSync('site/password-hashes.json'));
  await page.evaluate(hash => localStorage.setItem('mango-site-access',hash), site.hash);
  await page.reload();
  await page.locator('.prompt-card').first().waitFor();
  console.log('Before catalog cards:', await page.locator('.prompt-card').count());
  await page.screenshot({path:'docs/screenshots/issue-391/before-catalog.png'});
  await page.goto('http://127.0.0.1:8000/#processes');
  console.log('Before process blocks:', await page.locator('section[data-page="processes"]').count());
  await page.screenshot({path:'docs/screenshots/issue-391/before-processes.png',fullPage:true});
 } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
