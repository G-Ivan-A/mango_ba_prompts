/* NODE_PATH=$(npm root -g) node experiments/issue_454/site_walkthrough.cjs [COPIES_DIR]
 * Issue #454: real browser walk through what a BA gets from the site in main (Stage 1, manual prompts).
 * Serves site/ at the canonical origin: the repository and production stay untouched. Since site 2.5.0 (issue #460)
 * the password is off while BL-157в is debugged, so no login. This proves main, not production: docs/site-access.md.
 * For every kit card: fields are visible, the ⧉ button with the assigned edition selected, and after switching to
 * the other edition, really puts on the clipboard `<!-- id · step -->\n\nbody` with the body of that text.
 * The clipboard texts are saved to COPIES_DIR/{main,alt}/<step>.md: RUN-0089 ran the 2.4.0 buttons, whose bytes are the same.
 * Outputs: experiments/issue_454/site_walkthrough.json, site/screenshots/issue-454/*.png.
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../..');
const served = path.join(root, 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const copies = process.argv[2] || '/tmp/run88/site-copies';
const shots = path.join(root, 'site/screenshots/issue-454');
const sha = text => crypto.createHash('sha256').update(text).digest('hex');
const blocked = new Set(); // Outside origins are cut off on purpose: fonts must not decide the result.
const SECTIONS = ['Глоссарий', 'Бизнес-контекст', 'Функциональные требования', 'Нефункциональные требования', 'Описание разрабатываемого решения', 'Особенности реализации', 'UC', 'Дополнительные'];

async function open(browser, viewport) {
  const context = await browser.newContext({viewport});
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: 'https://g-ivan-a.github.io'});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) { blocked.add(url.origin); return route.abort(); }
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
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
  // ERR_FAILED in the console is the abort above; a failed request to the site itself still counts through requestfailed.
  page.on('console', m => { if (m.type() === 'error' && !m.text().includes('net::ERR_FAILED')) errors.push(m.text()); });
  page.on('requestfailed', r => { if (r.url().startsWith(home)) errors.push(`${r.url()} ${r.failure()?.errorText}`); });
  return {context, page, errors};
}

async function clipboardAfter(page, button) {
  await page.evaluate(() => navigator.clipboard.writeText(''));
  await button.click();
  await page.waitForFunction(() => navigator.clipboard.readText().then(t => t.length > 0));
  return page.evaluate(() => navigator.clipboard.readText());
}

async function main() {
  const kit = JSON.parse(await fs.readFile(path.join(served, 'data/test-kit.json')));
  const catalog = JSON.parse(await fs.readFile(path.join(served, 'data/prompts.json')));
  const bodyOf = id => catalog.prompts.find(p => p.id === id)?.body;
  await fs.mkdir(shots, {recursive: true});
  for (const kind of ['main', 'alt']) await fs.mkdir(path.join(copies, kind), {recursive: true});
  const browser = await chromium.launch({args: ['--disable-dev-shm-usage']});
  const audit = {kit: kit.kit.version, siteMain: true, production: 'не проверяется этим скриптом: audit_flow_coverage.py', cards: [], problems: []};
  try {
    const {page, errors} = await open(browser, {width: 1440, height: 1000});
    await page.goto(home + '#processes');
    await page.locator('#bcreq-testkit-steps li').first().waitFor({state: 'visible'});
    await page.waitForTimeout(400);
    // A BA lands on "Все шаги": every card visible at once (issue #460).
    audit.defaultVisibleCards = await page.locator('#bcreq-testkit-steps li.testkit-step:visible').count();
    if (audit.defaultVisibleCards !== kit.steps.length) audit.problems.push({defaultVisibleCards: audit.defaultVisibleCards});
    for (const group of kit.groups) {
      await page.locator(`[data-process-tab="${group.id}"]`).click();
      await page.locator('#bcreq-testkit').screenshot({path: path.join(shots, `testkit-stage-${group.number}-desktop.png`)});
    }
    audit.lead = (await page.locator('#bcreq-testkit .bcreq-lead').first().innerText()).replace(/\s+/g, ' ');
    audit.kitLink = await page.locator('#bcreq-testkit-summary a').first().getAttribute('href');
    for (let index = 0; index < kit.steps.length; index += 1) {
      const step = kit.steps[index];
      const code = step.step.split(' ')[0];
      const card = page.locator(`#bcreq-testkit-step-${index + 1}`);
      // Cards live behind the "Этап N" tabs, one tab per kit group: a BA opens the tab first.
      await page.locator(`[data-process-tab="${step.group}"]`).click();
      await card.waitFor({state: 'visible'});
      const primaryKind = step.mode === 'by-test' ? 'draft' : 'published';
      const altKind = primaryKind === 'draft' ? 'published' : 'draft';
      const primary = step[primaryKind];
      const alt = step[altKind];
      const row = {step: code, mode: step.mode, visible: await card.isVisible(),
        prepare: await card.locator('[data-field="prepare"]').count(), actions: await card.locator('ol.bcreq-actions li').count(),
        result: await card.locator('[data-field="result"]').count(), purpose: await card.locator('.testkit-purpose').count(),
        gate: await card.locator('[data-field="gate"]').count() ? (await card.locator('[data-field="gate"]').innerText()).slice(0, 60) : null};
      const copyButton = card.locator('button.testkit-copy');
      row.assignedSelected = await card.locator(`[data-testkit-edition="${primaryKind}"]`).getAttribute('aria-pressed') === 'true';
      const copied = await clipboardAfter(page, copyButton);
      const body = primaryKind === 'draft' ? primary.body : bodyOf(primary.id);
      row.mainCopyExact = copied === `<!-- ${primary.id} · ${step.step} -->\n\n${body}`;
      row.mainSha256 = sha(copied);
      row.mainBytes = Buffer.byteLength(copied);
      row.firstLine = copied.split('\n')[0];
      await fs.writeFile(path.join(copies, 'main', `${code}.md`), copied);
      if (alt) {
        await card.locator(`[data-testkit-edition="${altKind}"]`).click();
        const altCopied = await clipboardAfter(page, copyButton);
        const altBody = altKind === 'draft' ? alt.body : bodyOf(alt.id);
        row.altCopyExact = altCopied === `<!-- ${alt.id} · ${step.step} -->\n\n${altBody}`;
        row.altSha256 = sha(altCopied);
        await fs.writeFile(path.join(copies, 'alt', `${code}.md`), altCopied);
        await card.locator(`[data-testkit-edition="${primaryKind}"]`).click();
      } else {
        row.altCopyExact = null;
      }
      const fieldsOk = row.visible && row.prepare === 1 && row.actions > 0 && row.result === 1 && row.purpose === 1;
      const gateOk = (step.gate && step.gate !== '—') === Boolean(row.gate);
      if (!fieldsOk || !gateOk || !row.assignedSelected || !row.mainCopyExact || row.altCopyExact === false) audit.problems.push(row);
      audit.cards.push(row);
    }
    audit.gateCards = audit.cards.filter(c => c.gate).map(c => `${c.step}: ${c.gate}`);
    for (const [index, name] of [[2, 'sh2-gate-in'], [5, 'sh5-gate-c1'], [10, 'shv-gate-w'], [11, 'shr-release']]) {
      await page.locator(`[data-process-tab="${kit.steps[index].group}"]`).click();
      await page.locator(`#bcreq-testkit-step-${index + 1}`).screenshot({path: path.join(shots, `card-${name}-desktop.png`)});
    }
    await page.goto(home + '#standards');
    await page.waitForTimeout(500);
    const standardsText = await page.locator('main').innerText();
    audit.standardsPage = SECTIONS.map(name => ({name, shown: standardsText.includes(name)}));
    audit.problems.push(...audit.standardsPage.filter(s => !s.shown));
    await page.screenshot({path: path.join(shots, 'standards-8-sections-desktop.png')});
    audit.consoleErrors = errors;
    audit.blockedOrigins = [...blocked];
    if (errors.length) audit.problems.push({consoleErrors: errors});
    const mobile = await open(browser, {width: 390, height: 844});
    await mobile.page.goto(home + '#processes');
    await mobile.page.locator('#bcreq-testkit-steps li').first().waitFor({state: 'visible'});
    await mobile.page.waitForTimeout(300);
    audit.mobile = await mobile.page.evaluate(() => ({
      cards: document.querySelectorAll('#bcreq-testkit-steps li.testkit-step').length,
      overflowX: document.documentElement.scrollWidth > window.innerWidth,
    }));
    if (audit.mobile.cards !== kit.steps.length || audit.mobile.overflowX) audit.problems.push({mobile: audit.mobile});
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(__dirname, 'site_walkthrough.json'), JSON.stringify(audit, null, 1) + '\n');
  console.log(`cards ${audit.cards.length}; exact main copies ${audit.cards.filter(c => c.mainCopyExact).length}; exact alt copies ${audit.cards.filter(c => c.altCopyExact).length}; gates ${audit.gateCards.length}; problems ${audit.problems.length}`);
  for (const p of audit.problems) console.log(JSON.stringify(p).slice(0, 300));
  process.exit(audit.problems.length ? 1 : 0);
}
main().catch(e => { console.error(e); process.exit(2); });
