const state = {
  prompts: [],
  stats: null,
  roadmap: null,
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

function promptTokens(prompt) {
  return [
    `operation:${prompt.operation.id}`,
    `mode:${prompt.mode}`,
    ...prompt.processes.map((process) => `process:${process}`),
  ];
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

function visiblePrompts() {
  const query = normalize(state.query);
  return state.prompts.filter((prompt) => {
    const matchesQuery = !query || promptSearchText(prompt).includes(query);
    const tokens = promptTokens(prompt);
    const matchesFilters =
      state.selectedFilters.size === 0 ||
      tokens.some((token) => state.selectedFilters.has(token));
    return matchesQuery && matchesFilters;
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
  nodes.phases.replaceChildren(
    ...state.stats.phases.map((phase) => {
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

function filterButton({ token, icon, label, count, title }) {
  const button = el("button", "filter-button");
  button.type = "button";
  button.dataset.filterToken = token;
  button.setAttribute("aria-pressed", String(state.selectedFilters.has(token)));
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
  const operations = state.promptsData.filters.operations.map((operation) => ({
    token: `operation:${operation.id}`,
    icon: operation.icon,
    label: operation.label,
    count: totals.operations[operation.id] || 0,
    title: `${operation.label}: ${operation.description}`,
  }));
  const processes = state.promptsData.filters.processes.map((process) => ({
    token: `process:${process.label}`,
    icon: process.icon,
    label: process.label,
    count: totals.processes[process.label] || 0,
    title: `${process.label}: ${process.description}`,
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
    renderFilterGroup("Операции", operations),
    renderFilterGroup("Процессы БА", processes),
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
    const [promptsData, stats, roadmap] = await Promise.all([
      fetch("data/prompts.json").then((response) => response.json()),
      fetch("data/stats.json").then((response) => response.json()),
      fetch("data/roadmap.json").then((response) => response.json()),
    ]);

    state.promptsData = promptsData;
    state.prompts = promptsData.prompts;
    state.stats = stats;
    state.roadmap = roadmap;

    renderMetrics();
    renderPhases();
    renderFilters();
    renderPrompts();
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
