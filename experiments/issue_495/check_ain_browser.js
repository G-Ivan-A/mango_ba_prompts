// Playwright MCP browser_run_code_unsafe snippet. Serve the archived main site
// under /site/ and the PR site under /after/ with python3 -m http.server 8137.
async (page) => {
  const results = [];
  await page.setViewportSize({ width: 1040, height: 760 });

  for (const [path, version, purpose, hasPrivateUrl] of [
    ["site", "2.9.1", "Новизна коннектора", true],
    ["after", "2.9.2", "Новизна решения", false],
  ]) {
    await page.goto(`http://127.0.0.1:8137/${path}/#processes?ain=AIN-06`);
    const card = page.locator('[data-ain-step="AIN-06"]');
    const info = card.locator(".testkit-step-info");
    await info.waitFor({ state: "visible" });

    if (await page.locator("[data-ain-step]").count() !== 24) throw new Error("Expected 24 A-IN steps");
    if (!(await page.locator(".topbar").innerText()).includes(`v${version}`)) throw new Error("Unexpected site version");
    if (!(await info.innerText()).includes(purpose)) throw new Error("Unexpected AIN-06 purpose");

    await page.evaluate(() => {
      navigator.clipboard.writeText = async (value) => { window.copiedPrompt = value; };
    });
    await card.getByRole("button", { name: /Скопировать промпт шага AIN-06/ }).click();
    await page.waitForFunction(() => typeof window.copiedPrompt === "string");

    const copied = await page.evaluate(async () => {
      const kit = await (await fetch("data/a-in-kit.json")).json();
      const step = kit.steps.find(({ id }) => id === "AIN-06");
      // The UI prefixes the required #95/#448 copy identifier before the prompt.
      const prefix = `<!-- mango-bcreq-ain-06-stepwise · AIN-06 ${step.name} -->\n\n`;
      const body = window.copiedPrompt.startsWith(prefix) ? window.copiedPrompt.slice(prefix.length) : "";
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(body));
      const sha = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
      return {
        identical: body === step.prompt && sha === step.promptSha256,
        hasAccessGap: body.includes("ACCESS_GAP"),
        hasPrivateUrl: body.includes("github.com/G-Ivan-A/mango_ba_prompts"),
        sha,
      };
    });
    if (!copied.identical || !copied.hasAccessGap || copied.hasPrivateUrl !== hasPrivateUrl) {
      throw new Error(JSON.stringify(copied));
    }
    results.push({ version, purpose, ...copied });
  }
  return results;
}
