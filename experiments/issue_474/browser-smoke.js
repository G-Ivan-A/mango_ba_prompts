async (page) => {
  const screenshotDir = null; // Optional absolute output directory in the browser environment.
  const baseUrl = 'http://127.0.0.1:8768/';
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.setViewportSize({width:1280,height:960});
  await page.goto(baseUrl + '#processes');
  await page.reload();
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  const panel = page.locator('#a-in-proposal');
  const steps = await page.evaluate(async () => (await (await fetch('data/a-in-kit.json')).json()).steps);
  if (steps.length !== 24) throw new Error('Expected 24 steps');
  for (const step of steps) {
    await panel.locator(`[data-ain-copy="${step.id}"]`).click();
    await page.waitForFunction(async text => (await navigator.clipboard.readText()) === text, step.prompt);
  }
  const preview = panel.locator('[data-ain-preview="AIN-21"]');
  await preview.locator('summary').click();
  await page.waitForFunction(text => document.querySelector('[data-ain-preview="AIN-21"] pre').textContent === text,
    steps.find(step => step.id === 'AIN-21').prompt);
  await preview.locator('summary').click();
  const scrollToPanel = async () => {
    await panel.locator('summary').first().evaluate(el => {
      const header = document.querySelector('.topbar').getBoundingClientRect().height;
      window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - header - 16);
    });
  };
  // Reset toast without waiting; it otherwise hides screenshot content.
  await page.reload();
  await scrollToPanel();
  if (screenshotDir) await page.screenshot({path:screenshotDir+'/after-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  await scrollToPanel();
  if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)) throw new Error('Mobile overflow');
  if (screenshotDir) await page.screenshot({path:screenshotDir+'/after-mobile.png'});
  // A failed request must leave copy usable for a subsequent successful retry.
  await page.route('**/data/a-in-kit.json', route => route.abort());
  await page.reload();
  const first = panel.locator('[data-ain-copy="AIN-01"]');
  await first.click();
  await page.waitForFunction(() => !document.querySelector('[data-ain-copy="AIN-01"]').disabled);
  if (!(await page.locator('#toast').innerText()).includes('Не удалось')) throw new Error('Missing error feedback');
  await page.unroute('**/data/a-in-kit.json');
  await first.click();
  await page.waitForFunction(async text => (await navigator.clipboard.readText()) === text, steps[0].prompt);
  if (errors.length) throw new Error(errors.join('\n'));
  return {copies:24,byteEqual:true,previewEqual:true,mobileOverflow:false,errorRetry:true,pageErrors:errors};
}
