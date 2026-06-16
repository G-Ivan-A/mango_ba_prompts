const state = {
  prompts: [],
  stats: null,
  roadmap: null,
  checks: null,
  selectedFilters: new Set(),
  query: "",
};

const nodes = {
  metrics: document.querySelector("#metrics-grid"),
  phases: document.querySelector("#phase-lane"),
  filters: document.querySelector("#filters-root"),
  promptGrid: document.querySelector("#prompt-grid"),
  resultCount: document.querySelector("#result-count"),
  search: document.querySelector("#search-input"),
  clear: document.querySelector("#clear-button"),
  checksGrid: document.querySelector("#checks-grid"),
  checksActivity: document.querySelector("#checks-activity"),
  roadmapLevels: document.querySelector("#roadmap-levels"),
  roadmapGaps: document.querySelector("#roadmap-gaps"),
  toast: document.querySelector("#toast"),
};

function el(tag, className, text) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  if (text !== undefined) {
    element.textContent = text;
  }
  return element;
}

function normalize(value) {
  return String(value || "")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/\s+/g, " ")
    .trim();
}

function selectedValues(kind) {
  const prefix = `${kind}:`;
  return [...state.selectedFilters]
    .filter((token) => token.startsWith(prefix))
    .map((token) => token.slice(prefix.length));
}

// Каскад: при выборе процессов фильтр «Операции» сужается до операций
// выбранных процессов. Возвращает null, если процессы не выбраны (доступны все).
function availableOperationIds() {
  const selectedProcesses = selectedValues("process");
  if (selectedProcesses.length === 0) {
    return null;
  }
  const ids = new Set();
  for (const process of state.promptsData.filters.processes) {
    if (selectedProcesses.includes(process.label)) {
      for (const operation of process.operations) {
        ids.add(operation);
      }
    }
  }
  return ids;
}

function promptSearchText(prompt) {
  return normalize([
    prompt.file,
    prompt.title,
    prompt.description,
    prompt.mode,
    prompt.status,
    prompt.operation.id,
    prompt.operation.label,
    prompt.processes.join(" "),
  ].join(" "));
}

// Внутри одного фильтра — ИЛИ (несколько значений), между фильтрами — И.
function visiblePrompts() {
  const query = normalize(state.query);
  const selectedProcesses = selectedValues("process");
  const selectedOperations = selectedValues("operation");
  const selectedModes = selectedValues("mode");

  return state.prompts.filter((prompt) => {
    if (query && !promptSearchText(prompt).includes(query)) {
      return false;
    }
    if (
      selectedProcesses.length > 0 &&
      !prompt.processes.some((process) => selectedProcesses.includes(process))
    ) {
      return false;
    }
    if (selectedOperations.length > 0 && !selectedOperations.includes(prompt.operation.id)) {
      return false;
    }
    if (selectedModes.length > 0 && !selectedModes.includes(prompt.mode)) {
      return false;
    }
    return true;
  });
}

function showToast(message) {
  nodes.toast.textContent = message;
  nodes.toast.dataset.visible = "true";
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    nodes.toast.dataset.visible = "false";
  }, 2200);
}

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  document.body.append(textarea);
  textarea.select();
  document.execCommand("copy");
  textarea.remove();
}

function renderMetrics() {
  const totals = state.stats.totals;
  const metrics = [
    ["Всего", totals.allPrompts],
    ["Активных", totals.activePrompts],
    ["Архив", totals.archivedPrompts],
    ["Тесты пройдены", totals.testsPassed],
    ["В работе", totals.inWork],
    ["Отложено", totals.deferred],
  ];

  nodes.metrics.replaceChildren(
    ...metrics.map(([label, value]) => {
      const tile = el("div", "metric-tile");
      tile.append(el("span", "metric-value", String(value)));
      tile.append(el("span", "metric-label", label));
      return tile;
    }),
  );
}

function renderPhases() {
  // Зрелость «Мультиагенты» вынесена в отдельный модуль «Проверки» (см. renderChecks).
  const phases = state.stats.phases.filter((phase) => phase.id !== "multiagents");
  nodes.phases.replaceChildren(
    ...phases.map((phase) => {
      const card = el("article", "phase-card");
      card.dataset.status = phase.status;

      const top = el("div", "phase-top");
      top.append(el("span", "phase-index", String(phase.phase)));
      top.append(el("span", "status-pill", phase.status === "current" ? "сейчас" : "план"));

      const title = el("h3", "", phase.title);
      const summary = el("p", "phase-summary", phase.summary);
      const track = el("div", "progress-track");
      const bar = el("div", "progress-bar");
      bar.style.width = `${phase.progress}%`;
      track.append(bar);

      const metrics = el("div", "phase-metrics");
      for (const metric of phase.metrics) {
        const item = el("span", "phase-metric");
        item.append(el("strong", "", String(metric.value)));
        item.append(document.createTextNode(metric.label));
        metrics.append(item);
      }

      card.append(top, title, summary, track, metrics);
      return card;
    }),
  );
}

function filterButton({ token, icon, label, count, title, unavailable }) {
  const button = el("button", "filter-button");
  button.type = "button";
  button.dataset.filterToken = token;
  button.setAttribute("aria-pressed", String(state.selectedFilters.has(token)));
  if (unavailable) {
    button.dataset.unavailable = "true";
    button.setAttribute("aria-disabled", "true");
  }
  button.title = title || label;
  button.append(el("span", "filter-icon", icon));
  button.append(el("span", "filter-label", label));
  button.append(el("span", "filter-count", String(count || 0)));
  return button;
}

function renderFilterGroup(title, items) {
  const group = el("section", "filter-group");
  const heading = el("div", "filter-title", title);
  const row = el("div", "filter-row");
  row.append(...items.map(filterButton));
  group.append(heading, row);
  return group;
}

function renderFilters() {
  const totals = state.stats.totals;
  const processes = state.promptsData.filters.processes.map((process) => ({
    token: `process:${process.label}`,
    icon: process.icon,
    label: process.label,
    count: totals.processes[process.label] || 0,
    title: `${process.label}: ${process.description}`,
  }));

  const available = availableOperationIds();
  const operations = state.promptsData.filters.operations.map((operation) => ({
    token: `operation:${operation.id}`,
    icon: operation.icon,
    label: operation.label,
    count: totals.operations[operation.id] || 0,
    title:
      available && !available.has(operation.id)
        ? `${operation.label}: недоступна для выбранных процессов`
        : `${operation.label}: ${operation.description}`,
    unavailable: Boolean(available) && !available.has(operation.id),
  }));

  const modeLabels = {
    stepwise: "Stepwise",
    oneshot: "One-shot",
    legacy: "Legacy",
  };
  const modes = state.promptsData.filters.modes.map((mode) => ({
    token: `mode:${mode}`,
    icon: state.prompts.find((prompt) => prompt.mode === mode)?.modeIcon || "•",
    label: modeLabels[mode] || mode,
    count: totals.modes[mode] || 0,
    title: mode,
  }));

  nodes.filters.replaceChildren(
    renderFilterGroup("Процессы БА", processes),
    renderFilterGroup("Операции", operations),
    renderFilterGroup("Режимы", modes),
  );
}

function promptCard(prompt) {
  const card = el("article", "prompt-card");
  card.dataset.archived = String(prompt.archived);

  const head = el("div", "prompt-head");
  const titleWrap = el("div");
  titleWrap.append(el("h3", "prompt-title", prompt.title));
  const idLabel = el("span", "prompt-id", prompt.id);
  idLabel.title = "Уникальный токен промпта";
  titleWrap.append(idLabel);
  titleWrap.append(el("span", "prompt-file", prompt.sourcePath));
  const source = el("a", "source-link", "↗");
  source.href = prompt.url;
  source.target = "_blank";
  source.rel = "noreferrer";
  source.title = "Открыть файл в GitHub";
  source.setAttribute("aria-label", `Открыть ${prompt.file} в GitHub`);
  head.append(titleWrap, source);

  const description = el("p", "prompt-description", prompt.description);

  const tags = el("div", "tag-row");
  const mode = el("span", "tag", `${prompt.modeIcon} ${prompt.mode}`);
  mode.dataset.kind = "mode";
  const status = el("span", "tag", prompt.archived ? "archived" : prompt.status);
  status.dataset.kind = "status";
  const operation = el("span", "tag", `${prompt.operation.icon} ${prompt.operation.label}`);
  operation.dataset.kind = "operation";
  tags.append(mode, status, operation);
  for (const process of prompt.processes) {
    const tag = el("span", "tag", process);
    tag.dataset.kind = "process";
    tags.append(tag);
  }

  const actions = el("div", "prompt-actions");
  const copy = el("button", "copy-button");
  copy.type = "button";
  copy.dataset.copyId = prompt.id;
  copy.append(el("span", "", "⧉"));
  copy.append(el("span", "", "Копировать"));
  const checksum = el("span", "tag", prompt.contentHash.slice(0, 7));
  checksum.title = "SHA-256 prompt content";
  actions.append(copy, checksum);

  card.append(head, description, tags, actions);
  return card;
}

function renderPrompts() {
  const prompts = visiblePrompts();
  nodes.resultCount.value = `${prompts.length} из ${state.prompts.length}`;

  if (prompts.length === 0) {
    nodes.promptGrid.replaceChildren(el("div", "empty-state", "Ничего не найдено"));
    return;
  }

  nodes.promptGrid.replaceChildren(...prompts.map(promptCard));
}

function statusBar(segments) {
  const total = segments.reduce((sum, segment) => sum + segment.value, 0) || 1;
  const bar = el("div", "check-bar");
  for (const segment of segments) {
    if (segment.value <= 0) {
      continue;
    }
    const part = el("span", "check-bar-part");
    part.dataset.kind = segment.kind;
    part.style.width = `${Math.round((segment.value / total) * 100)}%`;
    part.title = `${segment.label}: ${segment.value}`;
    bar.append(part);
  }
  return bar;
}

function checkCard(title, valueNode, footNode) {
  const card = el("article", "check-card");
  card.append(el("p", "check-title", title));
  card.append(valueNode);
  if (footNode) {
    card.append(footNode);
  }
  return card;
}

function checkMetrics(items) {
  const wrap = el("div", "check-metrics");
  for (const [value, label] of items) {
    const item = el("span", "check-metric");
    item.append(el("strong", "", String(value)));
    item.append(document.createTextNode(label));
    wrap.append(item);
  }
  return wrap;
}

function renderChecks() {
  if (!state.checks) {
    return;
  }
  const checks = state.checks;
  const statuses = checks.statuses || {};

  const statusValue = el("div", "check-value-block");
  statusValue.append(
    statusBar([
      { kind: "canonical", value: statuses.canonical || 0, label: "canonical" },
      { kind: "draft", value: statuses.draft || 0, label: "draft" },
      { kind: "archived", value: statuses.archived || 0, label: "archived" },
    ]),
  );
  statusValue.append(
    checkMetrics([
      [statuses.canonical || 0, "canonical"],
      [statuses.draft || 0, "draft"],
      [statuses.archived || 0, "archived"],
    ]),
  );
  const statusCard = checkCard("Статус отладки", statusValue);

  const testsValue = el("span", "check-big", String(checks.tests.total));
  const testsFoot = checkMetrics([
    [checks.tests.coveredPrompts, "промптов с тестами"],
    [checks.tests.logs, "логов в experiments"],
  ]);
  const testsCard = checkCard("Тесты", testsValue, testsFoot);

  const feedbackValue = el("span", "check-big", String(checks.feedback.total));
  const feedbackFoot = checkMetrics([
    [checks.feedback.prompts, "промптов с feedback"],
    [checks.feedback.label, ""],
  ]);
  const feedbackCard = checkCard("Обратная связь", feedbackValue, feedbackFoot);

  nodes.checksGrid.replaceChildren(statusCard, testsCard, feedbackCard);

  if (checks.activity.length === 0) {
    nodes.checksActivity.replaceChildren(
      el("div", "empty-state", "Нет зафиксированной активности использования"),
    );
    return;
  }

  const heading = el("p", "check-activity-title", "Активность использования по процессам БА");
  const groups = el("div", "activity-grid");
  for (const group of checks.activity) {
    const card = el("article", "activity-card");
    const head = el("div", "activity-head");
    head.append(el("span", "activity-icon", group.icon));
    head.append(el("span", "activity-label", group.label));
    card.append(head);
    const list = el("ul", "activity-list");
    for (const prompt of group.prompts) {
      const row = el("li", "activity-row");
      row.append(el("span", "activity-prompt", prompt.file));
      const meta = el("span", "activity-meta");
      meta.append(el("span", "activity-chip", `тестов ${prompt.tests}`));
      if (prompt.feedback > 0) {
        const fb = el("span", "activity-chip", `feedback ${prompt.feedback}`);
        fb.dataset.kind = "feedback";
        meta.append(fb);
      }
      row.append(meta);
      list.append(row);
    }
    card.append(list);
    groups.append(card);
  }
  nodes.checksActivity.replaceChildren(heading, groups);
}

function renderRoadmap() {
  nodes.roadmapLevels.replaceChildren(
    ...state.roadmap.levels.map((level) => {
      const card = el("article", "roadmap-card");
      card.dataset.status = level.status;
      card.append(el("span", "roadmap-number", String(level.number)));
      card.append(el("h3", "", level.title));
      card.append(el("p", "", level.howItWorks));
      card.append(el("p", "", level.exitCriteria));
      return card;
    }),
  );

  nodes.roadmapGaps.replaceChildren(
    ...state.roadmap.gaps.map((gap) => {
      const card = el("article", "gap-card");
      card.append(el("h3", "", gap.gap));
      card.append(el("p", "", gap.why));
      card.append(el("p", "", gap.nextArtifact));
      return card;
    }),
  );
}

function rerenderInteractive() {
  renderFilters();
  renderPrompts();
}

async function init() {
  try {
    const [promptsData, stats, roadmap, checks] = await Promise.all([
      fetch("data/prompts.json").then((response) => response.json()),
      fetch("data/stats.json").then((response) => response.json()),
      fetch("data/roadmap.json").then((response) => response.json()),
      fetch("data/checks.json").then((response) => response.json()),
    ]);

    state.promptsData = promptsData;
    state.prompts = promptsData.prompts;
    state.stats = stats;
    state.roadmap = roadmap;
    state.checks = checks;

    renderMetrics();
    renderPhases();
    renderFilters();
    renderPrompts();
    renderChecks();
    renderRoadmap();
  } catch (error) {
    nodes.promptGrid.replaceChildren(el("div", "empty-state", "Данные не загрузились"));
    console.error(error);
  }
}

nodes.search.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderPrompts();
});

nodes.clear.addEventListener("click", () => {
  state.query = "";
  state.selectedFilters.clear();
  nodes.search.value = "";
  rerenderInteractive();
});

nodes.filters.addEventListener("click", (event) => {
  const button = event.target.closest("[data-filter-token]");
  if (!button) {
    return;
  }
  const token = button.dataset.filterToken;
  // Недоступную (каскадно скрытую) операцию нельзя выбрать, но можно снять.
  if (button.dataset.unavailable === "true" && !state.selectedFilters.has(token)) {
    return;
  }
  if (state.selectedFilters.has(token)) {
    state.selectedFilters.delete(token);
  } else {
    state.selectedFilters.add(token);
  }
  rerenderInteractive();
});

nodes.promptGrid.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy-id]");
  if (!button) {
    return;
  }
  const prompt = state.prompts.find((item) => item.id === button.dataset.copyId);
  if (!prompt) {
    return;
  }
  try {
    await copyText(prompt.body || prompt.content);
    button.dataset.copied = "true";
    showToast(`${prompt.file} скопирован`);
    window.setTimeout(() => {
      button.dataset.copied = "false";
    }, 1400);
  } catch (error) {
    showToast("Не удалось скопировать");
  }
});

init();
