// Run with Playwright MCP browser_run_code_unsafe; returns JSON evidence.
// No PDF, image or binary body is requested by the no-JavaScript context.
async (page) => {
  const context = await page.context().browser().newContext({javaScriptEnabled: false});
  await context.route('**/*', route => ['image', 'media', 'font', 'stylesheet', 'script']
    .includes(route.request().resourceType()) ? route.abort() : route.continue());
  const probe = await context.newPage();
  const pages = [];
  try {
    for (const branch of ['', '1_nachat-zdes/', '3_produkty-i-prilozheniya/3_kontakt-tsentr/',
      '4_integratsii/', '5_api-i-razrabotka/', '6_administrirovanie/']) {
      const url = 'https://docs.mango-office.ru/ru/' + branch + 'index.html';
      const response = await probe.goto(url, {waitUntil: 'domcontentloaded'});
      pages.push({url, status: response.status(), headers: await response.allHeaders(),
        ...await probe.evaluate(() => {
          const body = document.querySelector('.dc-doc-page__body,.dc-doc-leading-page__content,.dc-doc-leading-page__main');
          return {title: document.title, body_found: !!body,
            text_chars: (body?.textContent || '').length,
            link_count: document.querySelectorAll('a[href]').length};
        })});
    }
  } finally {
    await context.close();
  }
  await page.goto('https://www.mango-office.ru/support/1_nachat-zdes/', {waitUntil: 'domcontentloaded'});
  const cross_origin_fetch = await page.evaluate(async () => {
    try {
      const r = await fetch('https://docs.mango-office.ru/ru/index.html', {mode: 'cors', credentials: 'omit'});
      return {request_origin: location.origin, target: r.url, status: r.status,
        type: r.type, text_chars: (await r.text()).length};
    } catch (e) {
      return {request_origin: location.origin, error: String(e)};
    }
  });
  return {observed_at: new Date().toISOString(), javascript_disabled: true,
    asset_requests_blocked: true, pages, cross_origin_fetch};
}
