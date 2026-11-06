// Run with Playwright MCP browser_run_code_unsafe(filename=absolute path).
// Serve site/ on 127.0.0.1:8766 first. No npm dependency or build required.
async (page) => {
  const base = 'http://127.0.0.1:8766/';
  const out = 'site/screenshots/issue-466/';
  const errors = [];
  const onError = error => errors.push(error.message);
  const check = (value, message) => { if (!value) throw new Error(message); };
  page.setDefaultTimeout(5000);
  page.on('pageerror', onError);
  try {
    await page.setViewportSize({width:1440, height:1000});
    await page.goto(base + '#standards');
    await page.reload();
    await page.waitForFunction(() => document.querySelector('[data-site-version]')?.textContent === 'v2.8.0');
    const groups = page.locator('#standards > details.standards-group');
    check(await groups.count() === 3, 'three top-level groups');
    check(await page.locator('#standards-bcreq [data-bcreq-section]').count() === 8, 'eight BCREQ sections preserved');
    for (let index = 0; index < 3; index++) {
      const group = groups.nth(index);
      const summary = group.locator(':scope > summary');
      await summary.focus();
      await page.keyboard.press('Enter');
      check(await group.evaluate(el => el.open), 'Enter opens group');
      check(await groups.evaluateAll(els => els.filter(el => el.open).length) === 1, 'independent groups');
      await page.keyboard.press('Space');
      check(!(await group.evaluate(el => el.open)), 'Space closes group');
    }
    await page.locator('#standards-title').scrollIntoViewIfNeeded();
    await page.evaluate(() => document.activeElement.blur());
    await page.screenshot({path:out + 'after-overview.png'});
    for (const section of ['0','1','2','3','4','5','6','7','8','9','ttz']) {
      await groups.evaluateAll(els => els.forEach(el => el.open = false));
      await page.goto(base + '#standards?section=' + section);
      const id = section === '0' ? 'standard-intro' : section === '9' ? 'standard-industry'
        : section === 'ttz' ? 'standard-ttz' : 'standard-' + section;
      const target = page.locator('#' + id);
      await target.waitFor({state:'visible'});
      check(await target.evaluate(el => document.activeElement === el), 'focus follows deep link ' + section);
      check(await target.evaluate(el => el.closest('details').open), 'deep link reveals group ' + section);
    }
    await page.locator('#standards-ttz > summary').scrollIntoViewIfNeeded();
    await page.evaluate(() => document.activeElement.blur());
    await page.screenshot({path:out + 'after-ttz-desktop.png'});
    // Invalid routes and repeated navigation must leave the view usable.
    await page.goto(base + '#standards?section=invalid');
    check(await page.locator('#standards-title').isVisible(), 'invalid route stays on standards');
    await page.goto(base + '#standards?section=ttz');
    await page.setViewportSize({width:390, height:844});
    for (const theme of ['light', 'dark']) {
      await page.evaluate(theme => document.documentElement.dataset.theme = theme, theme);
      await groups.evaluateAll(els => els.forEach(el => el.open = true));
      check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'no mobile overflow: ' + theme);
    }
    await groups.evaluateAll(els => els.forEach(el => el.open = el.id === 'standards-ttz'));
    await page.locator('#standards-ttz > summary').scrollIntoViewIfNeeded();
    await page.screenshot({path:out + 'after-ttz-mobile-dark.png'});
    check(errors.length === 0, 'runtime exceptions: ' + errors.join('; '));
    return {groups:3, bcreqSections:8, deepLinks:11, keyboard:'passed', themes:2, mobile:'passed', runtimeErrors:errors};
  } finally {
    page.off('pageerror', onError);
  }
}
