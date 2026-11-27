async (page) => {
  const root = 'http://127.0.0.1:8750';
  const address = 'https://kb.example.test/guide?test=1&lang=ru';
  const externalRequests = [];
  const verification = `510-${Date.now()}`;
  await page.unrouteAll();
  await page.route('**/*', route => {
    if (route.request().url().startsWith(`${root}/`)) {
      const url = new URL(route.request().url());
      url.searchParams.set('verification', verification);
      return route.continue({url: url.toString()});
    }
    externalRequests.push(route.request().url());
    return route.abort();
  });
  await page.context().grantPermissions(['clipboard-read', 'clipboard-write'], {origin: root});
  await page.setViewportSize({width: 1280, height: 900});
  await page.goto(`${root}/?verification=${verification}#processes?stage=1`, {waitUntil: 'domcontentloaded'});
  const starter = page.locator('#bcreq-testkit-Ш-0');
  const source = starter.getByRole('textbox', {name: 'Источники БЗ'});
  const preview = starter.locator('.testkit-prompt-text');
  const size = starter.locator('.testkit-size');
  const copy = starter.locator('[data-testkit-index]');

  async function checkBody(suffix) {
    const text = await preview.textContent();
    if (!text.endsWith(suffix)) throw new Error(`Wrong starter text: ${text.slice(-160)}`);
    await copy.click();
    await page.waitForFunction(expected => navigator.clipboard.readText().then(copied => {
      return copied.startsWith('<!-- ') && copied.slice(copied.indexOf('\n\n') + 2) === expected;
    }), text);
  }

  await source.waitFor({state: 'visible'});
  await checkBody('декомпозированный\nИсточники БЗ: нет\n');
  const emptySize = await size.textContent();
  await source.fill(address);
  await checkBody(`декомпозированный\nИсточники БЗ: ${address}\n`);
  if (await size.textContent() === emptySize) throw new Error('Ш-0 size did not update');
  await starter.locator('[data-testkit-edition="published"]').click();
  await checkBody(`декомпозированный\nИсточники БЗ: ${address}\n`);
  await starter.locator('[data-testkit-edition="draft"]').click();
  await page.locator('#toast[data-visible="true"]').waitFor({state: 'hidden'});

  const top = await page.locator('#bcreq-testkit').evaluate(node => node.getBoundingClientRect().top + scrollY);
  await page.evaluate(y => window.scrollTo(0, y), Math.max(0, top - 85));
  await page.screenshot({path: 'docs/screenshots/pr-510/after.png'});

  await page.locator('[data-step-format="system"]').click();
  await page.locator('[data-step-format="system"][aria-current="true"]').waitFor();
  if (await source.inputValue() !== address) throw new Error('The format switch lost the address');
  await checkBody(`системный\nИсточники БЗ: ${address}\n`);
  await source.fill('');
  await checkBody('системный\nИсточники БЗ: нет\n');
  await page.locator('[data-step-format="decomposed"]').click();
  await page.locator('[data-step-format="decomposed"][aria-current="true"]').waitFor();
  for (const id of ['AIN-06', 'AIN-22']) {
    const check = await page.locator(`#bcreq-testkit-${id} .testkit-check`).textContent();
    if (!check.includes('Если возражений нет')) throw new Error(`Missing hybrid receipt note for ${id}`);
  }
  await page.setViewportSize({width: 390, height: 844});
  await source.fill(address);
  const fieldFits = await source.evaluate(node => node.getBoundingClientRect().right <= innerWidth);
  if (!fieldFits) throw new Error('Ш-0 source overflows the mobile viewport');
  if (externalRequests.some(url => url.startsWith(address))) throw new Error('The site fetched the source');
  return 'Verified both routes, both editions, clipboard parity, gap handoff notes and the mobile input.';
}
