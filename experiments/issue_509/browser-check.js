// Run with Playwright MCP browser_run_code_unsafe, against the generated site.
async (page) => {
  const origin = 'http://127.0.0.1:8765';
  const out = '/tmp/gh-issue-solver-1795727741728/docs/screenshots/issue-509';
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'], {origin});
  await page.setViewportSize({width:1280, height:900});
  await page.goto(`${origin}/?verification=509#processes?stage=1`);
  await page.waitForSelector('[data-ain-form]');
  const kit = await (await page.request.get(`${origin}/data/a-in-kit.json`)).json();
  const equal = (actual, expected, label) => { if (actual !== expected) throw new Error(label); };
  const checkCopy = async (card, body) => {
    await card.locator('[data-testkit-index]').click();
    await page.waitForFunction(expected => navigator.clipboard.readText().then(text => text.endsWith('\n\n' + expected)), body);
  };
  for (const step of kit.steps) {
    const card = page.locator(`[data-ain-step="${step.id}"]`);
    equal(await card.locator('.testkit-prompt-text').textContent(), step.prompt, `${step.id}: default full`);
    await checkCopy(card, step.prompt);
    await card.locator('[data-ain-form="compact"]').click();
    equal(await card.locator('.testkit-prompt-text').textContent(), step.compactPrompt, `${step.id}: compact`);
    await checkCopy(card, step.compactPrompt);
    await card.locator('[data-ain-form="full"]').click();
    equal(await card.locator('.testkit-prompt-text').textContent(), step.prompt, `${step.id}: restored full`);
  }
  await page.locator('[data-copy-ain-contract]').click();
  await page.waitForFunction(expected => navigator.clipboard.readText().then(text => text === expected), kit.contract.prompt);
  await page.locator('#bcreq-a-in-contract').scrollIntoViewIfNeeded();
  await page.screenshot({path:`${out}/after-contract.png`});
  const first = page.locator('[data-ain-step="AIN-01"]');
  await first.locator('[data-ain-form="compact"]').click();
  await first.scrollIntoViewIfNeeded();
  await page.screenshot({path:`${out}/after.png`});
  await page.setViewportSize({width:390, height:844});
  await first.locator('[data-ain-form="compact"]').scrollIntoViewIfNeeded();
  equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'narrow layout overflow');
  await page.screenshot({path:`${out}/after-mobile.png`});
  await page.setViewportSize({width:1280, height:900});
  await page.locator('[data-step-format="system"]').click();
  equal(await page.locator('[data-ain-form]').count(), 0, 'system track has no AIN forms');
  equal(await page.locator('.testkit-step').count(), 14, 'system step count');
  const starter = page.locator('.testkit-step').first();
  const starterBody = await starter.locator('.testkit-prompt-text').textContent();
  equal(starterBody.includes('Формат шагов: системный'), true, 'system format in starter');
  await checkCopy(starter, starterBody);
  await page.locator('[data-step-format="decomposed"]').click();
  equal(await page.locator('[data-ain-step="AIN-01"] [data-ain-form="compact"]').getAttribute('aria-pressed'), 'true', 'form retained on return');
  equal(await page.locator('[data-ain-step="AIN-02"] [data-ain-form="full"]').getAttribute('aria-pressed'), 'true', 'form isolated by step');
  return {ainCards:24, clipboardBodiesChecked:50, forms:'full/compact/full', systemSteps:14, narrowWidth:390, overflow:false, contractVersion:kit.contract.version};
}
