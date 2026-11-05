/* NODE_PATH=$(npm root -g) node experiments/issue_460/browser-check.cjs
 * Issue #460: acceptance criteria in a real browser, site/ served at the canonical
 * origin. SITE_ROOT selects another checkout. SKIP_SHOTS=1 keeps screenshots untouched.
 * Outputs: experiments/issue_460/browser-check.json, site/screenshots/issue-460/after-*.png
 * Exit code 1 when any check fails.
 */
const {chromium} = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(process.env.SITE_ROOT || path.join(__dirname, '../..'));
const served = path.join(root, 'site');
const home = 'https://g-ivan-a.github.io/mango_ba_prompts/';
const shotDir = path.join(__dirname, '../../site/screenshots/issue-460');
const TYPES = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml'};
const VIEWPORTS = {desktop: {width: 1440, height: 900}, tablet: {width: 900, height: 800}, mobile: {width: 375, height: 812}};

const results = [];
const check = (name, ok, detail = '') => {
  results.push({name, ok: Boolean(ok), detail});
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ` — ${detail}` : ''}`);
};

async function open(browser, viewport, colorScheme = 'light') {
  const context = await browser.newContext({viewport, colorScheme});
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: 'https://g-ivan-a.github.io'});
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (!url.href.startsWith(home)) return route.abort();
    const relative = decodeURIComponent(url.pathname.slice(new URL(home).pathname.length)) || 'index.html';
    const file = path.resolve(served, relative.endsWith('/') ? `${relative}index.html` : relative);
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

const visibleCards = page => page.locator('#bcreq-testkit-steps .testkit-step:visible');
const ready = page => page.waitForSelector('#bcreq-testkit-steps .testkit-prompt-text', {state: 'attached'});
const openProcesses = async (page, query = '') => {
  await page.goto(`${home}#processes${query}`);
  await ready(page);
};

async function access(browser) {
  const {context, page, errors} = await open(browser, VIEWPORTS.desktop);
  const started = Date.now();
  await page.goto(home);
  await ready(page);
  check('direct link stays on the site', page.url() === home, page.url());
  check('site is visible, gate open', await page.evaluate(() => document.documentElement.dataset.gate === 'open' && getComputedStyle(document.body).visibility === 'visible'));
  check('no password field', await page.locator('input[type=password]').count() === 0);
  check('no logout button', await page.locator('#site-logout').count() === 0);
  console.log(`      load until reader rendered: ${Date.now() - started} ms`);

  await page.goto(`${home}#processes?view=g2`);
  await ready(page);
  check('deep link keeps its address', page.url().endsWith('#processes?view=g2'), page.url());

  await page.goto(`${home}login.html`);
  await page.waitForURL(home);
  check('stale login.html opens the site', true);
  await page.goto(`${home}login.html?next=${encodeURIComponent(`${home}#processes?view=g3`)}`);
  await page.waitForURL(/view=g3/);
  check('login.html?next keeps the destination', true);
  await page.goto(`${home}login.html?next=${encodeURIComponent('https://example.com/phish')}`);
  await page.waitForURL(home);
  check('foreign next is ignored', page.url() === home, page.url());

  await page.goto(`${home}reports/`);
  await page.waitForLoadState('load');
  await page.waitForTimeout(300);
  check('reports index opens without the site password', !page.url().includes('login.html') && await page.evaluate(() => getComputedStyle(document.body).visibility === 'visible'), page.url());
  await page.goto(`${home}reports/run-0060/`);
  await page.waitForLoadState('load');
  await page.waitForTimeout(300);
  check('RUN-0060 keeps its own report password (decision flagged in the PR)', await page.locator('#password').count() === 1 && !page.url().includes('login.html'));
  check('no console errors on access paths', errors.length === 0, errors.join(' | '));
  await context.close();
}

async function tabs(browser) {
  const {context, page, errors} = await open(browser, VIEWPORTS.desktop);
  await openProcesses(page);
  check('13 steps visible without choosing a tab', await visibleCards(page).count() === 13);
  const active = page.locator('[data-process-tab][data-active="true"]');
  check('«Все шаги» is the active tab', (await active.getAttribute('data-process-tab')) === 'all', await active.innerText());
  const counts = {};
  for (const view of ['g1', 'g2', 'g3', 'g4']) {
    await page.locator(`[data-process-tab="${view}"]`).click();
    await page.waitForFunction(id => document.querySelector(`[data-process-tab="${id}"]`).dataset.active === 'true', view);
    counts[view] = await visibleCards(page).count();
  }
  check('stage tabs filter and sum to 13', Object.values(counts).reduce((a, b) => a + b, 0) === 13 && Object.values(counts).every(n => n > 0 && n < 13), JSON.stringify(counts));
  await page.locator('[data-process-tab="manual"]').click();
  await page.waitForSelector('#bcreq-manual:not([hidden])');
  check('full process tab still works', await page.locator('#bcreq-testkit').isHidden());
  await page.locator('[data-process-tab="approval"]').click();
  await page.waitForSelector('#bcreq-approval:not([hidden])');
  check('approval tab still works', await page.locator('#bcreq-manual').isHidden());
  await openProcesses(page, '?view=nonsense');
  await page.waitForFunction(() => document.querySelector('[data-process-tab="all"]')?.dataset.active === 'true');
  check('unknown view falls back to all steps', await visibleCards(page).count() === 13);
  check('no console errors on tabs', errors.length === 0, errors.join(' | '));
  await context.close();
}

async function reader(browser) {
  const kit = JSON.parse(await fs.readFile(path.join(served, 'data/test-kit.json')));
  const catalog = new Map(JSON.parse(await fs.readFile(path.join(served, 'data/prompts.json'))).prompts.map(item => [item.id, item]));
  const body = (step, kind) => (kind === 'draft' ? step.draft.body : catalog.get(step.published.id).body);
  const {context, page, errors} = await open(browser, VIEWPORTS.desktop);
  await openProcesses(page);
  const cards = page.locator('#bcreq-testkit-steps .testkit-step');
  let textOk = 0; let copyOk = 0; let switchOk = 0; let singles = 0; let scrollable = 0; let bounded = 0;
  const failures = [];
  for (let index = 0; index < kit.steps.length; index += 1) {
    const step = kit.steps[index];
    const card = cards.nth(index);
    const text = card.locator('.testkit-prompt-text');
    const assigned = step.mode === 'by-test' ? 'draft' : 'published';
    const other = assigned === 'draft' ? 'published' : 'draft';
    const box = await text.evaluate(node => ({maxHeight: getComputedStyle(node).maxHeight, overflowY: getComputedStyle(node).overflowY, client: node.clientHeight, scroll: node.scrollHeight, shown: node.textContent}));
    if (box.shown === body(step, assigned)) textOk += 1; else failures.push(`${step.step}: text differs`);
    if (box.maxHeight === `${VIEWPORTS.desktop.height * 0.6}px` && box.overflowY === 'auto' && box.client <= VIEWPORTS.desktop.height * 0.6) bounded += 1; else failures.push(`${step.step}: ${JSON.stringify({m: box.maxHeight, o: box.overflowY, c: box.client})}`);
    if (box.scroll > box.client) scrollable += 1;

    const copy = card.locator('.testkit-copy');
    await copy.click();
    const copied = await page.evaluate(() => navigator.clipboard.readText());
    const variantOf = kind => (kind === 'draft' ? step.draft : step.published);
    const expected = kind => `<!-- ${variantOf(kind).id} · ${step.step} -->\n\n${body(step, kind)}`;
    let copyGood = copied === expected(assigned);

    const buttons = card.locator('[data-testkit-edition]');
    if (variantOf(other)) {
      await text.evaluate(node => { node.scrollTop = 200; });
      await card.locator(`[data-testkit-edition="${other}"]`).click();
      const after = await text.evaluate(node => ({shown: node.textContent, top: node.scrollTop}));
      const comparison = await card.locator('.testkit-reader-note').getAttribute('data-comparison');
      const pressed = await card.locator(`[data-testkit-edition="${other}"]`).getAttribute('aria-pressed');
      if (after.shown === body(step, other) && after.top === 0 && comparison === 'true' && pressed === 'true') switchOk += 1;
      else failures.push(`${step.step}: switch ${JSON.stringify({same: after.shown === body(step, other), top: after.top, comparison, pressed})}`);
      await copy.click();
      copyGood = copyGood && (await page.evaluate(() => navigator.clipboard.readText())) === expected(other);
      await card.locator(`[data-testkit-edition="${assigned}"]`).click();
      if ((await text.textContent()) !== body(step, assigned)) failures.push(`${step.step}: switch back`);
    } else {
      singles += 1;
      if (await buttons.count() !== 1 || !(await buttons.first().isDisabled())) failures.push(`${step.step}: single edition control`);
      if (!/Единственная/.test(await card.locator('.testkit-reader-note').innerText())) failures.push(`${step.step}: single edition note`);
    }
    if (copyGood) copyOk += 1; else failures.push(`${step.step}: copied text differs`);
  }
  check('displayed text equals the source for all steps', textOk === 13, `${textOk}/13`);
  check('containers bounded by 60vh with overflow-y auto', bounded === 13, `${bounded}/13`);
  check('long prompts scroll inside the container', scrollable === 13, `${scrollable}/13`);
  check('edition switch works where two editions exist', switchOk === 12, `${switchOk}/12`);
  check('single-edition step has a disabled control and a note', singles === 1, `${singles}/1`);
  check('copy puts the selected edition with the first line', copyOk === 13, `${copyOk}/13`);
  check('no reader failures', failures.length === 0, failures.join(' | '));
  check('no console errors in the reader', errors.length === 0, errors.join(' | '));
  await context.close();
}

async function sticky(browser, name, viewport) {
  const {context, page, errors} = await open(browser, viewport);
  await openProcesses(page);
  const card = page.locator('#bcreq-testkit-steps .testkit-step').nth(4);
  const probe = () => card.evaluate(node => {
    const bar = node.querySelector('.testkit-reader-bar');
    const topbar = document.querySelector('.topbar');
    const topbarBottom = getComputedStyle(topbar).position === 'sticky' ? topbar.getBoundingClientRect().bottom : 0;
    const controls = [...bar.querySelectorAll('button')].map(button => {
      const rect = button.getBoundingClientRect();
      const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
      return {inView: rect.top >= topbarBottom - 0.5 && rect.bottom <= innerHeight, onTop: hit === button};
    });
    return {barTop: bar.getBoundingClientRect().top, topbarBottom, controls, readerTop: node.querySelector('.testkit-reader').getBoundingClientRect().top};
  });
  // Scroll the page until the reader's top edge has passed under the top bar while its text is on screen.
  await card.locator('.testkit-reader').evaluate(node => {
    const top = node.getBoundingClientRect().top + scrollY;
    const topbar = document.querySelector('.topbar');
    const offset = getComputedStyle(topbar).position === 'sticky' ? topbar.offsetHeight : 0;
    scrollTo({top: top - offset + innerHeight * 0.3, behavior: "instant"});
  });
  await page.waitForTimeout(150);
  const stuck = await probe();
  check(`${name}: toolbar is stuck while the reader is scrolled past`, stuck.readerTop < stuck.topbarBottom && Math.abs(stuck.barTop - stuck.topbarBottom) < 1, JSON.stringify({bar: stuck.barTop, topbar: stuck.topbarBottom, reader: stuck.readerTop}));
  check(`${name}: buttons in view and not overlapped`, stuck.controls.length >= 2 && stuck.controls.every(item => item.inView && item.onTop), JSON.stringify(stuck.controls));
  await card.locator('.testkit-copy').click({trial: true, timeout: 2000});
  if (!process.env.SKIP_SHOTS && name !== 'tablet') await page.screenshot({path: path.join(shotDir, `after-sticky-${name}.png`)});
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check(`${name}: no horizontal page scroll`, overflow <= 0, `overflow ${overflow}px`);
  const steps = await visibleCards(page).count();
  check(`${name}: 13 steps visible`, steps === 13, String(steps));
  check(`${name}: no console errors`, errors.length === 0, errors.join(' | '));
  await context.close();
}

async function looks(browser) {
  if (process.env.SKIP_SHOTS) return;
  const light = await open(browser, VIEWPORTS.desktop);
  await openProcesses(light.page);
  const card = light.page.locator('#bcreq-testkit-steps .testkit-step').nth(3);
  await card.locator('[data-testkit-edition="draft"]').click();
  await card.scrollIntoViewIfNeeded();
  await card.screenshot({path: path.join(shotDir, 'after-comparison-desktop.png')});
  const single = light.page.locator('#bcreq-testkit-steps .testkit-step').nth(11);
  await single.scrollIntoViewIfNeeded();
  await single.screenshot({path: path.join(shotDir, 'after-single-edition-desktop.png')});
  await light.context.close();

  const dark = await open(browser, VIEWPORTS.desktop);
  await dark.page.addInitScript(() => localStorage.setItem('mango-theme', 'dark'));
  await openProcesses(dark.page);
  await dark.page.evaluate(() => { document.documentElement.dataset.theme = 'dark'; });
  const darkCard = dark.page.locator('#bcreq-testkit-steps .testkit-step').nth(0);
  await darkCard.scrollIntoViewIfNeeded();
  await darkCard.screenshot({path: path.join(shotDir, 'after-dark-desktop.png')});
  await dark.context.close();
}

(async () => {
  const browser = await chromium.launch();
  try {
    await access(browser);
    await tabs(browser);
    await reader(browser);
    for (const [name, viewport] of Object.entries(VIEWPORTS)) await sticky(browser, name, viewport);
    await looks(browser);
  } finally {
    await browser.close();
  }
  const failed = results.filter(item => !item.ok);
  await fs.writeFile(path.join(__dirname, process.env.REPORT_NAME || 'browser-check.json'), `${JSON.stringify({total: results.length, failed: failed.length, results}, null, 2)}\n`);
  console.log(`\n${results.length - failed.length}/${results.length} passed`);
  process.exitCode = failed.length ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
