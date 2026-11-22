// Playwright MCP browser_run_code_unsafe. Serve before/site and after/site on port 8137.
async (page) => {
  const base = "http://127.0.0.1:8137";
  const out = "/tmp/mango-ft4";
  const card = (code) => page.locator(`[id="bcreq-testkit-${code}"]`);
  const choices = (code) => card(code).locator(".testkit-route");
  const fail = (message) => { throw new Error(message); };
  const focused = async (code) => card(code).and(page.locator(":focus")).waitFor();

  async function open(tree, code, track) {
    const params = new URLSearchParams({ step: code, track });
    await page.goto(`${base}/${tree}/site/#processes?${params}`);
    await focused(code);
  }
  async function options(code, texts) {
    await choices(code).locator("summary").click();
    const copy = await choices(code).innerText();
    for (const text of texts) if (!copy.includes(text)) fail(`${code}: ${text}`);
    return choices(code);
  }
  async function follow(link, target) {
    await link.focus();
    await page.keyboard.press("Enter");
    await focused(target);
  }

  await page.route(/^https?:\/\//, (route) =>
    new URL(route.request().url()).origin === base ? route.continue() : route.abort());
  await page.setViewportSize({ width: 1100, height: 760 });
  await open("before", "Ш-2", "system");
  if (await choices("Ш-2").count()) fail("В исходном срезе варианты уже есть");
  await card("Ш-2").locator(".testkit-step-info").screenshot({ path: `${out}/before-system.png` });
  await open("after", "Ш-2", "system");
  const systematic = await options("Ш-2", ["Г-IN / дальше", "Запись решения", "Уточнить с моделью", "Остановить"]);
  await card("Ш-2").locator(".testkit-step-info").screenshot({ path: `${out}/after-system.png` });
  await follow(systematic.getByRole("link", { name: "Продолжить → Ш-3" }), "Ш-3");
  const shared = await options("Ш-3", ["допуск-системный → Ш-2", "отзывает допуски"]);
  await follow(shared.getByRole("link", { name: "Сценарии по запросу → Ш-С" }), "Ш-С");
  const scenarios = await options("Ш-С", ["сохранённый контекст", "явное подтверждение"]);
  await follow(scenarios.getByRole("link", { name: "Открыть Ш-3" }), "Ш-3");

  await page.setViewportSize({ width: 390, height: 844 });
  await open("after", "AIN-21", "decomposed");
  const admit = await options("AIN-21", ["AIN-21 / allow", "отдельный AIN-22"]);
  await follow(admit.getByRole("link", { name: "Продолжить → AIN-22" }), "AIN-22");
  await open("after", "AIN-24", "decomposed");
  const handover = await options("AIN-24", ["актуальный AIN-21", "Г-IN / дальше", "Г-IN / CS"]);
  await card("AIN-24").locator(".testkit-step-info").screenshot({ path: `${out}/after-ain-mobile.png` });
  await follow(handover.getByRole("link", { name: "Продолжить → Ш-3" }), "Ш-3");
  const returns = await options("Ш-3", ["передача-AIN → AIN-24", "Нужен актуальный допуск AIN-21"]);
  await follow(returns.getByRole("link", { name: "передача-AIN → AIN-24" }), "AIN-24");

  await open("after", "Ш-Р", "decomposed");
  const release = await options("Ш-Р", ["Выпустить → BASELINE", "Выпуск / выпуск", "Остановить → СТОП"]);
  if (await release.getByRole("link", { name: /BASELINE|СТОП/ }).count()) fail("Конечный исход стал ссылкой");
  if (!await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)) fail("Горизонтальная прокрутка");
  return "ФТ-4: системный и декомпозированный переходы, Ш-С, повторный допуск, выпуск, клавиатура и 390 px — OK";
}
