// Playwright MCP browser_run_code_unsafe. Serve the two site trees under base first.
async (page, { base = "http://127.0.0.1:8137", output = "/tmp/mango-500-preview" } = {}) => {
  const clipboard = {};
  const ain = "mango-bcreq-ain-01-stepwise";
  const system = "mango-bcreq-context-understanding-system";
  const comparison = "mango-bcreq-context-understanding-stepwise";
  const history = "mango-bcreq-context-understanding-stepwise-by-test-site-v2p7p0";
  const process = (step, track) => `#processes?${new URLSearchParams({ step, track })}`;
  const edition = (id) => `#catalog?edition=${id}`;
  const stepCard = (step) => page.locator(`[id="bcreq-testkit-${step}"]`);
  const catalogCard = (id) => page.locator(`[id="catalog-edition-${id}"]`);
  const track = (id) => page.locator(`[data-step-format="${id}"]`);

  function equal(actual, expected, label) {
    if (actual !== expected) throw new Error(label);
  }

  function has(actual, value, label) {
    if (!actual?.includes(value)) throw new Error(label);
  }

  async function open(tree, hash, label) {
    await page.goto(`${base}/${tree}/site/?case=${label}${hash}`);
    await page.locator("#prompt-grid .prompt-card").first().waitFor({ state: "attached" });
  }

  async function screenshot(name, card) {
    if (card) await card.scrollIntoViewIfNeeded();
    await page.screenshot({ path: `${output}/${name}.png`, animations: "disabled" });
  }

  async function focused(card) {
    await card.and(page.locator(":focus")).waitFor();
  }

  async function activate(link) {
    await link.focus();
    await page.keyboard.press("Enter");
  }

  async function copy(name, card, button, prefix, expected) {
    await activate(card.locator(button));
    const value = await page.evaluate(() => navigator.clipboard.readText());
    equal(value.slice(0, prefix.length), prefix, `${name}: точный префикс копирования`);
    equal(value.slice(prefix.length), expected, `${name}: байты скопированного тела`);
    clipboard[name] = value.slice(prefix.length);
  }

  await page.context().grantPermissions(["clipboard-read", "clipboard-write"], { origin: base });
  await page.route(/^https?:\/\//, (route) => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.emulateMedia({ colorScheme: "light", reducedMotion: "reduce" });

  await open("before", "#catalog", "before-ain");
  await page.locator("#search-input").fill(ain);
  await page.getByText("Ничего не найдено", { exact: true }).waitFor();
  await screenshot("before-catalog-ain01");
  await open("before", "#catalog", "before-system");
  await page.locator('[data-filter-token="format:system"]').click();
  await page.locator("#search-input").fill("bcreq-context-understanding-stepwise");
  await page.locator(".prompt-card[data-archived=true]").first().waitFor();
  equal(await page.locator(".prompt-card[data-archived=false]").count(), 0, "база: системный поиск показывает архив");
  await screenshot("before-catalog-system");
  await open("before", "#processes?ain=AIN-01", "before-ain-step");
  await screenshot("before-processes-ain01", page.locator('[data-ain-step="AIN-01"]'));
  await open("before", "#processes?track=system", "before-system-step");
  await screenshot("before-processes-system", page.locator(".testkit-step").filter({
    has: page.getByRole("heading", { name: /^Ш-1 / }),
  }));

  await open("after", "#catalog", "default");
  equal(await page.locator(".prompt-card").count(), 39, "39 классов видны по умолчанию");
  const [catalog, testKit, ainKit] = await page.evaluate(() => Promise.all(
    ["prompts", "test-kit", "a-in-kit"].map((name) => fetch(`data/${name}.json`).then((response) => response.json())),
  ));
  const stepData = (code) => testKit.steps.find(({ step }) => step.startsWith(`${code} `));
  const publishedBody = (id) => catalog.prompts.find((prompt) => prompt.id === id).body;

  await open("after", process("AIN-01", "decomposed"), "after-ain");
  const ainCard = stepCard("AIN-01");
  await focused(ainCard);
  await screenshot("after-processes-ain01", ainCard);
  const ainStep = ainKit.steps[0];
  await copy("AIN-01 / Процессы", ainCard, ".testkit-copy", `<!-- ${ain} · ${ainStep.id} ${ainStep.name} -->\n\n`, ainStep.prompt);

  await page.context().setOffline(true);
  try {
    await activate(ainCard.locator(".bcreq-step-prompt a"));
    await focused(catalogCard(ain));
    equal(await page.locator(".prompt-card").count(), 1, "открывается точная карточка AIN-01");
    await screenshot("after-catalog-ain01", catalogCard(ain));
    await copy("AIN-01 / Каталог", catalogCard(ain), ".copy-button", `<!-- ${ain} -->\n\n`, ainStep.prompt);
    await activate(catalogCard(ain).getByRole("link", { name: /^AIN-01 ·/ }));
    await focused(ainCard);
    await activate(ainCard.getByRole("link", { name: "К-36", exact: true }));
    const classCard = page.locator(".prompt-card").filter({ hasText: "класс К-36" });
    await activate(classCard.getByRole("link", { name: "Ш-0", exact: true }));
    await focused(stepCard("Ш-0"));
    await activate(stepCard("Ш-0").getByRole("link", { name: "К-36", exact: true }));
    await activate(classCard.getByRole("link", { name: "AIN-01", exact: true }));
    await focused(ainCard);
    await activate(track("system"));
    await focused(stepCard("Ш-0"));
    await activate(track("decomposed"));
    await focused(ainCard);
  } finally {
    await page.context().setOffline(false);
  }

  await open("after", process("Ш-1", "system"), "after-system");
  const systemCard = stepCard("Ш-1");
  const systemStep = stepData("Ш-1");
  await focused(systemCard);
  equal(await systemCard.locator(".testkit-edition-status").textContent(), "draft · v0.3", "статус действующего Ш-1");
  has(await systemCard.locator(".testkit-edition-source").getAttribute("href"), systemStep.system.sourcePath, "системный файл");
  await screenshot("after-processes-system", systemCard);
  await copy("Ш-1 / Процессы", systemCard, ".testkit-copy", `<!-- ${system} · ${systemStep.step} -->\n\n`, systemStep.system.body);
  await activate(systemCard.locator(".bcreq-step-prompt a"));
  await focused(catalogCard(system));
  equal(await page.locator(".prompt-card[data-archived=true]").count(), 0, "архив закрыт при открытии рабочего Ш-1");
  equal(await catalogCard(system).locator(".working-prompt-path").textContent(), systemStep.system.sourcePath, "точный рабочий путь");
  await screenshot("after-catalog-system", catalogCard(system));
  await copy("Ш-1 / Каталог", catalogCard(system), ".copy-button", `<!-- ${system} -->\n\n`, systemStep.system.body);

  await page.setViewportSize({ width: 390, height: 844 });
  await activate(catalogCard(system).getByRole("link", { name: /^Ш-1 ·/ }));
  await focused(systemCard);
  await activate(systemCard.locator('[data-testkit-edition="published"]'));
  equal(await systemCard.locator(".testkit-edition-status").textContent(), "draft · v0.6", "статус и версия редакции сравнения");
  await copy("Ш-1 v0.6 / Процессы", systemCard, ".testkit-copy", `<!-- ${comparison} · ${systemStep.step} -->\n\n`, publishedBody(comparison));
  await activate(systemCard.locator(".bcreq-step-prompt a"));
  await focused(catalogCard(comparison));
  equal(await catalogCard(comparison).locator(".working-prompt-path").textContent(), systemStep.published.sourcePath, "не архив при совпадении имён");
  await activate(catalogCard(comparison).getByRole("link", { name: /^Ш-1 ·/ }));
  await focused(systemCard);
  equal(await systemCard.locator('[data-testkit-edition="published"]').getAttribute("aria-pressed"), "true", "выбор сохранён при возврате");
  await activate(track("decomposed"));
  await focused(stepCard("Ш-0"));
  await activate(track("system"));
  await focused(systemCard);
  equal(await systemCard.locator('[data-testkit-edition="published"]').getAttribute("aria-pressed"), "true", "выбор сохранён после переключения формата");

  const uc = "mango-bcreq-uc-modeling-stepwise-by-test";
  await open("after", edition(uc), "uc");
  await focused(catalogCard(uc));
  equal(await catalogCard(uc).count(), 1, "одна редакция UC");
  for (const code of ["Ш-5", "Ш-8"]) {
    equal(await catalogCard(uc).getByRole("link", { name: new RegExp(`^${code} ·`) }).count(), 2, `оба формата ${code}`);
  }
  await activate(catalogCard(uc).getByRole("link", { name: /^Ш-8 · системный ·/ }));
  await focused(stepCard("Ш-8"));
  await activate(track("decomposed"));
  await focused(stepCard("Ш-8"));
  equal(await track("decomposed").getAttribute("aria-current"), "true", "формат общего шага переключён");

  await open("after", process("Ш-0", "system"), "constit");
  const start = stepData("Ш-0");
  await copy("Ш-0 / Процессы", stepCard("Ш-0"), ".testkit-copy", `<!-- ${start.draft.id} · ${start.step} -->\n\n`,
    `${start.draft.body.trimEnd()}\n\nФормат шагов: системный\n`);
  for (const code of ["Ш-В", "Ш-С"]) {
    await open("after", process(code, "decomposed"), code);
    const step = stepData(code);
    await focused(stepCard(code));
    await copy(`${code} / Процессы`, stepCard(code), ".testkit-copy", `<!-- ${step.published.id} · ${step.step} -->\n\n`,
      `${publishedBody(step.published.id).trimEnd()}\n\n${step.handoffBlock}`);
  }

  await open("after", `#prompt=${history}`, "old-archive");
  equal(await page.locator(".prompt-card[data-archived=true]").count(), 1, "старая архивная закладка");
  await open("after", "#processes?ain=AIN-01", "old-ain");
  await focused(ainCard);
  await open("after", "#processes?step=36", "old-pilot");
  await focused(page.locator("#bcreq-step-36"));
  equal(await page.locator("#bcreq-steps > li").count(), 39, "полный процесс 39 классов");
  const download = page.waitForEvent("download");
  await page.evaluate((bodies) => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([JSON.stringify(bodies)], { type: "application/json" }));
    link.download = "clipboard-bodies.json";
    link.click();
  }, clipboard);
  await (await download).saveAs(`${output}/clipboard-bodies.json`);
  return `Фокус, переходы и копирование в Chromium пройдены. Проверено тел: ${Object.keys(clipboard).length}.`;
}
