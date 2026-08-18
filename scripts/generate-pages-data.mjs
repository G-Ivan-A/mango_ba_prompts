#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const SITE_DATA_DIR = path.join(ROOT, "site", "data");
const REPO_BLOB = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main";

const SOURCE_FILES = {
  promptsReadme: "prompts/README.md",
  taxonomy: "docs/taxonomy.md",
  processIndex: "docs/ba-processes/00-index.md",
  ecosystem: "docs/ba-ecosystem.md",
  patternsReadme: "patterns/README.md",
};

function isPromptAssetFile(name) {
  return name.endsWith(".md") && name !== "README.md" && !name.endsWith(".executable.md");
}

// Тестовые логи промптов и (опциональный) статический срез обратной связи.
const RUNS_DIR = "runs";
const FEEDBACK_SOURCE = "pr-ops/prompt-feedback.json";

const OPERATION_ICONS = {
  ingestion: "↓",
  understanding: "?",
  validation: "✓",
  modeling: "□",
  solution_design: "⚙",
  documentation: "¶",
  quality: "◆",
  research: "⌕",
  governance: "§",
  impact_analysis: "↗",
  reverse_requirements: "↩",
  risk_analysis: "!",
  release_readiness: "▶",
};

const MODE_ICONS = {
  stepwise: "↔",
  oneshot: "●",
  legacy: "⌁",
};

// Палитра эмодзи для процессов БА. Назначается по позиции процесса, поэтому
// дашборд и каталог остаются гибкими: при добавлении новых процессов (после
// задачи «Формализовать онтологию БА») иконка подбирается автоматически.
const PROCESS_EMOJI_PALETTE = [
  "📋",
  "✅",
  "📑",
  "🎯",
  "📊",
  "🤝",
  "📈",
  "🧭",
  "🛡️",
  "🧩",
  "🔍",
  "⚙️",
];

// Подсказка «когда использовать» по режиму запуска промпта (ФТ-2: описание
// 150-300 символов со структурой что/когда/ограничения). Режимы стабильны и не
// относятся к типам артефактов, поэтому их можно держать в коде.
const MODE_HINTS = {
  stepwise:
    "Режим stepwise подходит при средней или высокой неопределённости: БА видит промежуточный результат и подтверждает направление между шагами.",
  oneshot:
    "Режим one-shot — когда вход полный, а задача короткая: быстрый черновик или постобработка за один ответ без потери шага review.",
  legacy:
    "Режим legacy сохранён для совместимости и сравнения с историческим результатом; для новой работы выбирайте stepwise или one-shot.",
};

function processEmoji(index) {
  return PROCESS_EMOJI_PALETTE[index % PROCESS_EMOJI_PALETTE.length];
}

// Собирает развёрнутое описание карточки (что делает + контекст операции +
// когда использовать по режиму). Источники динамические, поэтому описание
// адаптируется к новым операциям и режимам.
function buildLongDescription(shortDescription, operation, mode) {
  const parts = [];
  const base = (shortDescription || "").trim();
  if (base) {
    parts.push(/[.!?]$/.test(base) ? base : `${base}.`);
  }
  if (operation?.description) {
    parts.push(operation.description.trim());
  }
  if (MODE_HINTS[mode]) {
    parts.push(MODE_HINTS[mode]);
  }
  let text = parts.join(" ").replace(/\s+/g, " ").trim();
  // Держим описание в районе 150-300 символов: не обрезаем посреди слова.
  if (text.length > 300) {
    const clipped = text.slice(0, 297);
    const lastSpace = clipped.lastIndexOf(" ");
    text = `${clipped.slice(0, lastSpace > 0 ? lastSpace : 297).trimEnd()}…`;
  }
  return text;
}

async function read(relativePath) {
  return fs.readFile(path.join(ROOT, relativePath), "utf8");
}

async function writeJson(relativePath, data) {
  const target = path.join(ROOT, relativePath);
  await fs.mkdir(path.dirname(target), { recursive: true });
  await fs.writeFile(target, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function repoUrl(relativePath) {
  return `${REPO_BLOB}/${relativePath}`;
}

function stripMarkdownInline(value) {
  return value
    .replace(/\[([^\]]+)]\([^)]+\)/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/<([^>]+)>/g, "$1")
    .replace(/&nbsp;/g, " ")
    .trim();
}

function splitMarkdownRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function isSeparatorRow(line) {
  const cells = splitMarkdownRow(line);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell));
}

function parseTables(markdown) {
  const lines = markdown.split(/\r?\n/);
  const tables = [];

  for (let index = 0; index < lines.length - 1; index += 1) {
    if (!lines[index].trim().startsWith("|") || !isSeparatorRow(lines[index + 1])) {
      continue;
    }

    const headers = splitMarkdownRow(lines[index]).map(stripMarkdownInline);
    const rows = [];
    let rowIndex = index + 2;
    while (rowIndex < lines.length && lines[rowIndex].trim().startsWith("|")) {
      const rawCells = splitMarkdownRow(lines[rowIndex]);
      if (rawCells.length === headers.length) {
        rows.push(rawCells);
      }
      rowIndex += 1;
    }

    tables.push({ headers, rows, line: index + 1 });
    index = rowIndex;
  }

  return tables;
}

function parseFrontmatter(content) {
  if (!content.startsWith("---\n")) {
    return {};
  }
  const end = content.indexOf("\n---", 4);
  if (end === -1) {
    return {};
  }
  const frontmatter = {};
  for (const line of content.slice(4, end).split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) {
      continue;
    }
    const key = match[1];
    let value = match[2].trim();
    value = value.replace(/^["']|["']$/g, "");
    if (value === "true") {
      frontmatter[key] = true;
    } else if (value === "false") {
      frontmatter[key] = false;
    } else {
      frontmatter[key] = value;
    }
  }
  return frontmatter;
}

function stripFrontmatter(content) {
  // Remove the leading YAML frontmatter block and the legacy EXPERIMENTAL
  // marker so the copied prompt is clean text without metadata noise.
  let body = content;
  if (body.startsWith("---\n")) {
    const end = body.indexOf("\n---", 4);
    if (end !== -1) {
      body = body.slice(end + 4);
    }
  }
  body = body.replace(/^\s*<!--\s*EXPERIMENTAL[^>]*-->\s*\n/m, "");
  return body.replace(/^\s+/, "").replace(/\s+$/, "") + "\n";
}

function parseCodes(value) {
  const codes = [...value.matchAll(/`([^`]+)`/g)].map((match) => match[1]);
  if (codes.length > 0) {
    return codes.map((code) => code.replace(/-/g, "_"));
  }
  return stripMarkdownInline(value)
    .split(",")
    .map((item) => item.trim().replace(/-/g, "_"))
    .filter(Boolean);
}

function extractFilename(cell) {
  const codeMatch = cell.match(/`([^`]+\.md)`/);
  if (codeMatch) {
    return codeMatch[1];
  }
  const linkMatch = cell.match(/\[([^\]]+\.md)]/);
  return linkMatch ? linkMatch[1] : stripMarkdownInline(cell);
}

function modeFromFilename(file) {
  const match = file.match(/-(stepwise|oneshot|legacy)\.md$/);
  return match ? match[1] : "unknown";
}

function operationFromFilename(file, operationIds) {
  const slug = file.replace(/\.md$/, "").replace(/-(stepwise|oneshot|legacy)$/, "");
  const normalizedSlug = slug.replace(/-/g, "_");
  const sortedIds = [...operationIds].sort((left, right) => right.length - left.length);
  return sortedIds.find((id) => normalizedSlug.endsWith(id)) || "unknown";
}

function parseTaxonomy(markdown) {
  const tables = parseTables(markdown);
  const operationTables = tables.filter(
    (table) => table.headers[0] === "ID" && table.headers[1] === "Операция",
  );
  const processTable = tables.find(
    (table) => table.headers[0] === "№" && table.headers[1] === "Процесс",
  );

  const operations = operationTables.flatMap((table) => table.rows).map((row) => {
    const id = stripMarkdownInline(row[0]).replace(/-/g, "_");
    return {
      id,
      label: stripMarkdownInline(row[1]),
      description: stripMarkdownInline(row[2]),
      example: stripMarkdownInline(row[3]),
      icon: OPERATION_ICONS[id] || "•",
    };
  });

  const processes = (processTable?.rows || []).map((row, index) => {
    const id = Number(stripMarkdownInline(row[0]));
    return {
      id,
      label: stripMarkdownInline(row[1]),
      description: stripMarkdownInline(row[2]),
      operations: parseCodes(row[3]),
      icon: String(id),
      emoji: processEmoji(index),
    };
  });

  return { operations, processes };
}

function parsePromptMatrix(markdown) {
  const matrixTables = parseTables(markdown).filter(
    (table) => table.headers.includes("Файл") && table.headers.includes("Назначение"),
  );
  const metadataByFile = new Map();

  for (const table of matrixTables) {
    const col = (name) => table.headers.indexOf(name);
    const idx = {
      file: col("Файл"),
      title: col("Название"),
      token: col("Токен"),
      description: col("Назначение"),
      mode: col("Режим"),
      status: col("Статус"),
      version: col("Версия"),
      operation: col("Когнитивная операция"),
      processes: col("Процесс БА"),
    };
    const cell = (row, index) => (index >= 0 ? stripMarkdownInline(row[index]) : "");

    for (const row of table.rows) {
      const file = extractFilename(row[idx.file]);
      if (!file.endsWith(".md")) {
        continue;
      }
      metadataByFile.set(file, {
        file,
        title: cell(row, idx.title),
        token: cell(row, idx.token),
        description: cell(row, idx.description),
        mode: cell(row, idx.mode),
        status: cell(row, idx.status),
        version: cell(row, idx.version),
        operationId: cell(row, idx.operation).replace(/-/g, "_"),
        processes:
          idx.processes >= 0
            ? row[idx.processes].split(";").map(stripMarkdownInline).filter(Boolean)
            : [],
      });
    }
  }

  return metadataByFile;
}

// Извлекает имена файлов промптов (`*.md`) из ячейки центрального маппинга.
function extractPromptFilenames(cell) {
  const codes = [...cell.matchAll(/`([^`]+\.md)`/g)].map((match) => match[1]);
  const links = [...cell.matchAll(/\[`?([^\]`]+\.md)`?\]/g)].map((match) => match[1]);
  const names = [...codes, ...links].map((name) => name.replace(/^archive\//, ""));
  return [...new Set(names)];
}

// Извлекает slug паттернов (`patterns/<slug>/`) из ячейки.
function extractPatternSlugs(cell) {
  const slugs = [...cell.matchAll(/patterns\/([a-z0-9-]+)\//g)].map((match) => match[1]);
  return [...new Set(slugs)];
}

// Извлекает slug паттерна из ячейки-имени (`[`slug`](slug/)`), где префикса
// `patterns/` нет: сперва из ссылки `](slug/)`, затем из кода в backticks.
function extractPatternSlug(cell) {
  const fromPatternsPath = extractPatternSlugs(cell)[0];
  if (fromPatternsPath) {
    return fromPatternsPath;
  }
  const linkMatch = cell.match(/]\(([a-z0-9-]+)\/?\)/);
  if (linkMatch) {
    return linkMatch[1];
  }
  const codeMatch = cell.match(/`([a-z0-9-]+)`/);
  return codeMatch ? codeMatch[1] : "";
}

function parseProcessIndex(markdown) {
  const table = parseTables(markdown).find(
    (candidate) => candidate.headers[0] === "№" && candidate.headers[1] === "Процесс",
  );
  const gapsTable = parseTables(markdown).find(
    (candidate) => candidate.headers[0] === "Gap" && candidate.headers[1] === "Процессы",
  );

  const processes = (table?.rows || []).map((row) => ({
    id: Number(stripMarkdownInline(row[0])),
    label: stripMarkdownInline(row[1]),
    operations: parseCodes(row[2]),
    pattern: stripMarkdownInline(row[3]),
    patternSlugs: extractPatternSlugs(row[3]),
    recommendedPrompts: parseCodes(row[4]),
    promptFiles: extractPromptFilenames(row[4]),
  }));

  const gaps = (gapsTable?.rows || []).map((row, index) => ({
    id: `process-gap-${index + 1}`,
    gap: stripMarkdownInline(row[0]),
    processes: stripMarkdownInline(row[1])
      .split(/[,;]/)
      .map((value) => value.trim())
      .filter(Boolean),
    status: stripMarkdownInline(row[2]),
    nextArtifact: stripMarkdownInline(row[3]),
  }));

  return { processes, gaps };
}

// Активные prompt-файлы, на которые ссылается ячейка «Промпты» детальной карты.
// Архивные ссылки (`prompts/archive/...`) исключаются: `[^)/]+` обрывается на `/`.
function parseActivePromptLinks(cell) {
  const files = [];
  const seen = new Set();
  for (const match of cell.matchAll(/\((?:\.\.\/)+prompts\/([^)/]+\.md)\)/g)) {
    const file = match[1];
    if (!seen.has(file)) {
      seen.add(file);
      files.push(file);
    }
  }
  return files;
}

// Тип подпроцесса по ячейке «Промпты»:
//   direct  — шаг исполняется активным промптом;
//   support — ручной шаг, опирающийся на активный промпт («Выполняется вручную ...»);
//   gap     — промпта нет, нужен новый («Требуется разработка промпта»);
//   archive — только legacy-ссылка в prompts/archive/;
//   manual  — ручной шаг без промпта.
// hasPrompts (для жёсткого требования ФТ-8) истинно только для direct и support.
function subprocessKind(cell, activeCount) {
  const manual = /Выполняется вручную/i.test(cell);
  if (activeCount > 0) {
    return manual ? "support" : "direct";
  }
  if (/Требуется разработка промпта/i.test(cell)) {
    return "gap";
  }
  if (/prompts\/archive\//.test(cell)) {
    return "archive";
  }
  return "manual";
}

// Дерево «процесс -> подпроцессы» из раздела «Детальная карта» 00-index.md.
// Возвращает полный список (НФТ прослеживаемости) с флагом hasPrompts у каждого
// подпроцесса; фильтрация «только с промптами» — жёсткое требование ФТ-8 — делается
// на слое рендера, а сводные счётчики и useTree вычисляются здесь.
function parseProcessTree(markdown, processIndex) {
  const lines = markdown.split(/\r?\n/);
  const indexById = new Map(processIndex.map((process) => [process.id, process]));
  const processes = [];
  let totalSubprocesses = 0;
  let shownSubprocesses = 0;

  for (let i = 0; i < lines.length; i += 1) {
    const heading = lines[i].match(/^###\s+(\d+)\.\s+(.+?)\s*$/);
    if (!heading) {
      continue;
    }
    const id = Number(heading[1]);
    const label = stripMarkdownInline(heading[2]);
    const subprocesses = [];

    for (let j = i + 1; j < lines.length; j += 1) {
      if (/^#{2,3}\s/.test(lines[j])) {
        break; // следующий раздел — таблицы шагов больше нет
      }
      if (!lines[j].trim().startsWith("|") || !isSeparatorRow(lines[j + 1] || "")) {
        continue;
      }
      const headers = splitMarkdownRow(lines[j]).map(stripMarkdownInline);
      if (headers[0] !== "Шаг") {
        continue; // не таблица шагов
      }
      const stepCol = headers.indexOf("Шаг");
      const opCol = headers.indexOf("Операция");
      const promptCol = headers.findIndex((header) => header.startsWith("Промпт"));
      let k = j + 2;
      let order = 0;
      while (k < lines.length && lines[k].trim().startsWith("|")) {
        const cells = splitMarkdownRow(lines[k]);
        if (cells.length === headers.length) {
          const promptCell = promptCol >= 0 ? cells[promptCol] : "";
          const files = parseActivePromptLinks(promptCell);
          const opCell = opCol >= 0 ? cells[opCol] : "";
          const operation = (opCell.match(/`([^`]+)`/)?.[1] || stripMarkdownInline(opCell)).replace(
            /-/g,
            "_",
          );
          order += 1;
          subprocesses.push({
            order,
            step: stripMarkdownInline(cells[stepCol] || ""),
            operation,
            operationIcon: OPERATION_ICONS[operation] || "•",
            kind: subprocessKind(promptCell, files.length),
            hasPrompts: files.length > 0,
            prompts: files.map((file) => ({ file, url: repoUrl(`prompts/${file}`) })),
          });
        }
        k += 1;
      }
      break; // только первая таблица шагов под заголовком процесса
    }

    if (subprocesses.length === 0) {
      continue;
    }
    const shown = subprocesses.filter((subprocess) => subprocess.hasPrompts).length;
    totalSubprocesses += subprocesses.length;
    shownSubprocesses += shown;
    const indexed = indexById.get(id);
    processes.push({
      id,
      label,
      icon: String(id),
      operations: indexed?.operations || [],
      recommendedPrompts: indexed?.recommendedPrompts || [],
      subprocessTotal: subprocesses.length,
      subprocessShown: shown,
      subprocesses,
    });
  }

  return {
    treeThreshold: 20,
    totalProcesses: processes.length,
    shownProcesses: processes.filter((process) => process.subprocessShown > 0).length,
    totalSubprocesses,
    shownSubprocesses,
    useTree: shownSubprocesses > 20,
    processes,
  };
}

// Парсит навигационную матрицу паттернов patterns/README.md.
function parsePatterns(markdown) {
  const tables = parseTables(markdown);
  const navTable = tables.find(
    (table) => table.headers[0] === "Паттерн" && table.headers[1] === "Путь",
  );
  const matrixTable = tables.find(
    (table) => table.headers[0] === "Паттерн" && table.headers[1] === "Процесс БА",
  );

  const whenBySlug = new Map();
  for (const row of navTable?.rows || []) {
    const slug = extractPatternSlug(row[0]) || extractPatternSlugs(row[1])[0];
    if (slug) {
      whenBySlug.set(slug, stripMarkdownInline(row[2]));
    }
  }

  const patterns = [];
  for (const row of matrixTable?.rows || []) {
    const slug = extractPatternSlug(row[0]);
    if (!slug) {
      continue;
    }
    patterns.push({
      slug,
      path: `patterns/${slug}/`,
      url: repoUrl(`patterns/${slug}/`),
      whenToStart: whenBySlug.get(slug) || "",
      processes: stripMarkdownInline(row[1])
        .split(/[;]/)
        .map((value) => value.trim())
        .filter(Boolean),
      operation: stripMarkdownInline(row[2]),
      promptFiles: extractPromptFilenames(row[3]),
    });
  }

  return patterns;
}

function parseRoadmap(markdown) {
  const tables = parseTables(markdown);
  const levelsTable = tables.find(
    (table) => table.headers[0] === "Уровень" && table.headers[1] === "Как работает",
  );
  const gapsTable = tables.find(
    (table) => table.headers[0] === "Gap" && table.headers[1] === "Почему важен",
  );

  const levels = (levelsTable?.rows || []).map((row) => {
    const title = stripMarkdownInline(row[0]);
    const match = title.match(/^(\d+)\.\s*(.+)$/);
    const number = match ? Number(match[1]) : 0;
    return {
      id: `level-${number}`,
      number,
      title: match ? match[2] : title,
      howItWorks: stripMarkdownInline(row[1]),
      baRole: stripMarkdownInline(row[2]),
      exitCriteria: stripMarkdownInline(row[3]),
      status: number === 1 ? "current" : "planned",
    };
  });

  const gaps = (gapsTable?.rows || []).map((row, index) => ({
    id: `gap-${index + 1}`,
    gap: stripMarkdownInline(row[0]),
    why: stripMarkdownInline(row[1]),
    nextArtifact: stripMarkdownInline(row[2]),
  }));

  return { levels, gaps };
}

async function listPromptFiles() {
  const activeNames = await fs.readdir(path.join(ROOT, "prompts"));
  const archiveNames = await fs.readdir(path.join(ROOT, "prompts", "archive"));
  const active = activeNames
    .filter(isPromptAssetFile)
    .map((name) => ({ relativePath: `prompts/${name}`, archived: false }));
  const archived = archiveNames
    .filter((name) => name.endsWith(".md"))
    .map((name) => ({ relativePath: `prompts/archive/${name}`, archived: true }));
  return [...active, ...archived].sort((left, right) => {
    if (left.archived !== right.archived) {
      return left.archived ? 1 : -1;
    }
    return left.relativePath.localeCompare(right.relativePath, "ru");
  });
}

function countBy(items, selector) {
  return items.reduce((counts, item) => {
    const value = selector(item);
    if (Array.isArray(value)) {
      for (const nested of value) {
        counts[nested] = (counts[nested] || 0) + 1;
      }
    } else {
      counts[value] = (counts[value] || 0) + 1;
    }
    return counts;
  }, {});
}

function makeStats(prompts, taxonomy, processIndex, roadmap) {
  const activePrompts = prompts.filter((prompt) => !prompt.archived);
  const archivedPrompts = prompts.filter((prompt) => prompt.archived);
  const canonicalPrompts = activePrompts.filter((prompt) => prompt.status === "canonical");
  const draftPrompts = activePrompts.filter((prompt) => prompt.status === "draft");

  const totals = {
    allPrompts: prompts.length,
    activePrompts: activePrompts.length,
    archivedPrompts: archivedPrompts.length,
    testsPassed: canonicalPrompts.length,
    inWork: draftPrompts.length,
    deferred: archivedPrompts.length,
    modes: countBy(prompts, (prompt) => prompt.mode),
    statuses: countBy(prompts, (prompt) => prompt.status),
    operations: countBy(prompts, (prompt) => prompt.operation.id),
    processes: countBy(prompts, (prompt) => prompt.processes),
  };

  const phases = [
    {
      id: "prompts",
      phase: 1,
      title: "Промпты",
      status: "current",
      progress: prompts.length === 0 ? 0 : Math.round((activePrompts.length / prompts.length) * 100),
      levelIds: ["level-1"],
      summary: "Ручной выбор prompt-файла, копирование в AI-чат и human review результата.",
      metrics: [
        { label: "активных", value: activePrompts.length },
        { label: "проверено", value: canonicalPrompts.length },
        { label: "в работе", value: draftPrompts.length },
      ],
    },
    {
      id: "agents",
      phase: 2,
      title: "Агенты",
      status: "planned",
      progress: 0,
      levelIds: ["level-2", "level-3"],
      summary: "Системный prompt, БЗ/RAG и агентный workflow поверх текущей библиотеки.",
      metrics: [
        { label: "основа", value: processIndex.length },
        { label: "операций", value: taxonomy.operations.length },
        { label: "gaps", value: roadmap.gaps.length },
      ],
    },
    {
      id: "multiagents",
      phase: 3,
      title: "Мультиагенты",
      status: "planned",
      progress: 0,
      levelIds: ["level-4"],
      summary: "Несколько ролей: BA orchestrator, evidence, documentation, risk и reviewer.",
      metrics: [
        { label: "уровень", value: 4 },
        { label: "human gates", value: "on" },
        { label: "статус", value: "план" },
      ],
    },
  ];

  return {
    generatedAt: new Date().toISOString(),
    sourceFiles: Object.values(SOURCE_FILES).map((relativePath) => ({
      path: relativePath,
      url: repoUrl(relativePath),
    })),
    totals,
    taxonomy: {
      operations: taxonomy.operations.length,
      processes: taxonomy.processes.length,
    },
    processIndex,
    phases,
  };
}

function normalizeForMatch(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[_\s]+/g, "-")
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/-+/g, "-");
}

// Набор «топиков» промпта для сопоставления с тестовыми логами runs/.
function promptSearchTerms(prompt) {
  const stem = prompt.file
    .replace(/\.md$/, "")
    .replace(/-(stepwise|oneshot|legacy|simple)$/g, "")
    .replace(/-generator$/g, "");
  const normalizedStem = normalizeForMatch(stem);
  const words = normalizedStem.split("-").filter(Boolean);
  const core = words.slice(0, 2).join("-");
  const terms = new Set([normalizedStem, core].filter(Boolean));
  // Устойчивые сокращения предметной области БА.
  if (words[0] === "us" || normalizedStem.startsWith("user-story")) {
    terms.add("user-story");
  }
  if (words[0] === "uc" || normalizedStem.startsWith("usecase")) {
    terms.add("usecase");
  }
  if (normalizedStem.startsWith("tz-stats")) {
    terms.add("tz-stats");
  }
  return [...terms];
}

async function walkMarkdown(relativeDir) {
  let entries = [];
  try {
    entries = await fs.readdir(path.join(ROOT, relativeDir), { withFileTypes: true });
  } catch {
    return [];
  }

  const files = [];
  for (const entry of entries) {
    const relativePath = `${relativeDir}/${entry.name}`;
    if (entry.isDirectory()) {
      files.push(...(await walkMarkdown(relativePath)));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(relativePath);
    }
  }
  return files;
}

async function loadExperiments() {
  const experiments = [];
  const files = (await walkMarkdown(RUNS_DIR)).filter((file) => /\/(outputs|logs)\//.test(file));
  for (const file of files) {
    const content = await read(file);
    experiments.push({ name: file, normalized: normalizeForMatch(content) });
  }
  return experiments;
}

async function loadFeedback() {
  try {
    const parsed = JSON.parse(await read(FEEDBACK_SOURCE));
    return Array.isArray(parsed.entries) ? parsed.entries : [];
  } catch {
    return [];
  }
}

function makeChecks(prompts, processes, experiments, feedbackEntries) {
  const statuses = { draft: 0, canonical: 0, archived: 0 };
  for (const prompt of prompts) {
    if (prompt.archived) {
      statuses.archived += 1;
    } else {
      statuses[prompt.status] = (statuses[prompt.status] || 0) + 1;
    }
  }

  const feedbackByPrompt = new Map();
  for (const entry of feedbackEntries) {
    const id = entry.prompt || entry.id;
    if (!id) {
      continue;
    }
    if (!feedbackByPrompt.has(id)) {
      feedbackByPrompt.set(id, []);
    }
    feedbackByPrompt.get(id).push(entry);
  }

  const perPrompt = prompts.map((prompt) => {
    const terms = promptSearchTerms(prompt);
    const testFiles = experiments
      .filter((experiment) => terms.some((term) => experiment.normalized.includes(term)))
      .map((experiment) => experiment.name);
    const feedback = feedbackByPrompt.get(prompt.id) || [];
    return {
      id: prompt.id,
      file: prompt.file,
      status: prompt.archived ? "archived" : prompt.status,
      operation: prompt.operation.id,
      processes: prompt.processes,
      tests: testFiles.length,
      testFiles,
      feedback: feedback.length,
      feedbackIssues: feedback,
      usage: testFiles.length + feedback.length,
    };
  });

  const byUsage = (left, right) => right.usage - left.usage || left.id.localeCompare(right.id);

  // Показатели проверок по процессам (ФТ-3). Считаются динамически из processes
  // во frontmatter промптов плюс бакет «Прочее» для промптов без процесса.
  const OTHER_LABEL = "Прочее";
  const checkedByLabel = new Map();
  const promptsByLabel = new Map();
  for (const process of processes) {
    checkedByLabel.set(process.label, 0);
    promptsByLabel.set(process.label, 0);
  }
  for (const prompt of perPrompt) {
    const labels = prompt.processes.length > 0 ? prompt.processes : [OTHER_LABEL];
    for (const label of labels) {
      if (!checkedByLabel.has(label)) {
        checkedByLabel.set(label, 0);
        promptsByLabel.set(label, 0);
      }
      checkedByLabel.set(label, checkedByLabel.get(label) + prompt.tests);
      promptsByLabel.set(label, promptsByLabel.get(label) + (prompt.tests > 0 ? 1 : 0));
    }
  }
  const emojiByLabel = new Map(processes.map((process) => [process.label, process.emoji]));
  const byProcess = [...checkedByLabel.entries()]
    .map(([label, checks]) => ({
      label,
      emoji: emojiByLabel.get(label) || "🗂️",
      checks,
      coveredPrompts: promptsByLabel.get(label) || 0,
    }))
    .sort((left, right) => right.checks - left.checks || left.label.localeCompare(right.label, "ru"));

  const coveredPrompts = perPrompt.filter((prompt) => prompt.tests > 0).length;
  const testsPassed = {
    covered: coveredPrompts,
    total: perPrompt.length,
    percent: perPrompt.length === 0 ? 0 : Math.round((coveredPrompts / perPrompt.length) * 100),
  };

  const activity = processes
    .map((process) => ({
      id: process.id,
      label: process.label,
      icon: process.icon,
      prompts: perPrompt
        .filter((prompt) => prompt.processes.includes(process.label) && prompt.usage > 0)
        .sort(byUsage)
        .slice(0, 4)
        .map((prompt) => ({
          id: prompt.id,
          file: prompt.file,
          tests: prompt.tests,
          feedback: prompt.feedback,
          usage: prompt.usage,
        })),
    }))
    .filter((group) => group.prompts.length > 0);

  return {
    generatedAt: new Date().toISOString(),
    sourceFiles: [
      { path: `${RUNS_DIR}/`, url: repoUrl(`${RUNS_DIR}/`) },
      { path: FEEDBACK_SOURCE, url: repoUrl(FEEDBACK_SOURCE) },
    ],
    statuses,
    tests: {
      logs: experiments.length,
      total: perPrompt.reduce((sum, prompt) => sum + prompt.tests, 0),
      coveredPrompts: perPrompt.filter((prompt) => prompt.tests > 0).length,
    },
    feedback: {
      label: "prompt:feedback",
      total: perPrompt.reduce((sum, prompt) => sum + prompt.feedback, 0),
      prompts: perPrompt.filter((prompt) => prompt.feedback > 0).length,
    },
    totalChecked: perPrompt.reduce((sum, prompt) => sum + prompt.tests, 0),
    testsPassed,
    byProcess,
    activity,
    prompts: perPrompt.sort(byUsage),
  };
}

function promptSummary(prompt) {
  return {
    id: prompt.id,
    file: prompt.file,
    title: prompt.title,
    url: prompt.url,
    mode: prompt.mode,
    modeIcon: prompt.modeIcon,
    status: prompt.archived ? "archived" : prompt.status,
    archived: prompt.archived,
  };
}

// Карта процессов БА (страница «Процессы»): описание, операции, паттерны,
// связанные промпты, known gaps и показатели проверок. Источники динамические.
function makeProcesses(taxonomyProcesses, processIndexData, prompts, patternsList, checks) {
  const promptByFile = new Map(prompts.map((prompt) => [prompt.file, prompt]));
  const indexById = new Map(processIndexData.processes.map((process) => [process.id, process]));
  const checksByLabel = new Map((checks.byProcess || []).map((entry) => [entry.label, entry]));
  const patternBySlug = new Map(patternsList.map((pattern) => [pattern.slug, pattern]));

  const processes = taxonomyProcesses.map((process) => {
    const indexEntry = indexById.get(process.id) || {};
    const operations = (process.operations || []).map((operationId) => operationId);
    const promptFiles = indexEntry.promptFiles || [];
    const linkedPrompts = promptFiles
      .map((file) => promptByFile.get(file))
      .filter(Boolean)
      .map(promptSummary);
    const patternSlugs = indexEntry.patternSlugs || [];
    const patterns = patternSlugs
      .map((slug) => patternBySlug.get(slug))
      .filter(Boolean)
      .map((pattern) => ({ slug: pattern.slug, path: pattern.path, url: pattern.url }));
    const gaps = processIndexData.gaps.filter((gap) => gap.processes.includes(process.label));
    const checkStats = checksByLabel.get(process.label) || { checks: 0, coveredPrompts: 0 };

    return {
      id: process.id,
      label: process.label,
      emoji: process.emoji,
      description: process.description,
      operations,
      pattern: indexEntry.pattern || "",
      patterns,
      prompts: linkedPrompts,
      gaps: gaps.map((gap) => ({ gap: gap.gap, status: gap.status, nextArtifact: gap.nextArtifact })),
      checks: checkStats.checks,
      coveredPrompts: checkStats.coveredPrompts,
    };
  });

  return {
    generatedAt: new Date().toISOString(),
    sourceFiles: [
      { path: SOURCE_FILES.processIndex, url: repoUrl(SOURCE_FILES.processIndex) },
      { path: SOURCE_FILES.taxonomy, url: repoUrl(SOURCE_FILES.taxonomy) },
    ],
    processes,
    gaps: processIndexData.gaps,
  };
}

// Библиотека паттернов (страница «Паттерны»).
function makePatterns(patternsList, prompts, operationsById) {
  const promptByFile = new Map(prompts.map((prompt) => [prompt.file, prompt]));
  const patterns = patternsList.map((pattern) => {
    const operationId = pattern.operation.split(/\s|\+/)[0].replace(/-/g, "_");
    const operation = operationsById.get(operationId);
    return {
      slug: pattern.slug,
      path: pattern.path,
      url: pattern.url,
      whenToStart: pattern.whenToStart,
      processes: pattern.processes,
      operation: pattern.operation,
      operationIcon: operation?.icon || "•",
      prompts: pattern.promptFiles
        .map((file) => promptByFile.get(file))
        .filter(Boolean)
        .map(promptSummary),
    };
  });

  return {
    generatedAt: new Date().toISOString(),
    sourceFiles: [{ path: SOURCE_FILES.patternsReadme, url: repoUrl(SOURCE_FILES.patternsReadme) }],
    patterns,
  };
}

async function main() {
  const [promptsReadme, taxonomyMarkdown, processIndexMarkdown, ecosystemMarkdown, patternsReadme] =
    await Promise.all([
      read(SOURCE_FILES.promptsReadme),
      read(SOURCE_FILES.taxonomy),
      read(SOURCE_FILES.processIndex),
      read(SOURCE_FILES.ecosystem),
      read(SOURCE_FILES.patternsReadme),
    ]);

  const taxonomy = parseTaxonomy(taxonomyMarkdown);
  const promptMetadata = parsePromptMatrix(promptsReadme);
  const processIndexData = parseProcessIndex(processIndexMarkdown);
  const processIndex = processIndexData.processes;
  const processTree = parseProcessTree(processIndexMarkdown, processIndex);
  const patternsList = parsePatterns(patternsReadme);
  const roadmap = parseRoadmap(ecosystemMarkdown);
  const promptFiles = await listPromptFiles();
  const operationIds = taxonomy.operations.map((operation) => operation.id);
  const operationsById = new Map(taxonomy.operations.map((operation) => [operation.id, operation]));
  const processesByLabel = new Map(taxonomy.processes.map((process) => [process.label, process]));

  const prompts = [];
  for (const file of promptFiles) {
    const content = await read(file.relativePath);
    const frontmatter = parseFrontmatter(content);
    const basename = path.basename(file.relativePath);
    const metadata = promptMetadata.get(basename);
    const operationId =
      metadata?.operationId || operationFromFilename(basename, operationIds);
    const operation = operationsById.get(operationId) || {
      id: operationId,
      label: operationId,
      description: "",
      icon: "•",
    };
    const processes = metadata?.processes || [];
    const processDetails = processes.map((label) => processesByLabel.get(label)).filter(Boolean);
    const mode = metadata?.mode || modeFromFilename(basename);
    const contentHash = crypto.createHash("sha256").update(content).digest("hex");

    const slug = basename.replace(/\.md$/, "");
    prompts.push({
      id: frontmatter.id || `mango-${slug}`,
      file: basename,
      title: frontmatter.title || slug,
      sourcePath: file.relativePath,
      url: repoUrl(file.relativePath),
      archived: file.archived,
      description: metadata?.description || "Описание отсутствует в prompts/README.md.",
      descriptionLong: buildLongDescription(
        metadata?.description || "Описание отсутствует в prompts/README.md.",
        operation,
        mode,
      ),
      mode,
      modeIcon: MODE_ICONS[mode] || "•",
      status: frontmatter.status || metadata?.status || "unknown",
      version: frontmatter.version || metadata?.version || "unknown",
      updated: frontmatter.updated || "",
      temperature: frontmatter.temperature || "",
      operation: {
        id: operation.id,
        label: operation.label,
        description: operation.description,
        icon: operation.icon,
      },
      processes,
      processDetails: processDetails.map((process) => ({
        id: process.id,
        label: process.label,
        icon: process.icon,
        emoji: process.emoji,
      })),
      frontmatter,
      content,
      body: stripFrontmatter(content),
      contentHash,
      lineCount: content.split(/\r?\n/).length,
    });
  }

  const filters = {
    operations: taxonomy.operations,
    processes: taxonomy.processes,
    modes: ["stepwise", "oneshot", "legacy"],
    statuses: [...new Set(prompts.map((prompt) => prompt.status))].sort(),
  };

  const promptsData = {
    generatedAt: new Date().toISOString(),
    sourceFiles: [
      { path: SOURCE_FILES.promptsReadme, url: repoUrl(SOURCE_FILES.promptsReadme) },
      { path: SOURCE_FILES.taxonomy, url: repoUrl(SOURCE_FILES.taxonomy) },
      { path: SOURCE_FILES.processIndex, url: repoUrl(SOURCE_FILES.processIndex) },
      ...promptFiles.map((file) => ({ path: file.relativePath, url: repoUrl(file.relativePath) })),
    ],
    filters,
    prompts,
  };

  const roadmapData = {
    generatedAt: new Date().toISOString(),
    sourceFiles: [{ path: SOURCE_FILES.ecosystem, url: repoUrl(SOURCE_FILES.ecosystem) }],
    levels: roadmap.levels,
    gaps: roadmap.gaps,
  };

  const processTreeData = {
    generatedAt: new Date().toISOString(),
    sourceFiles: [
      { path: SOURCE_FILES.processIndex, url: repoUrl(SOURCE_FILES.processIndex) },
    ],
    ...processTree,
  };

  const experiments = await loadExperiments();
  const feedbackEntries = await loadFeedback();
  const checksData = makeChecks(prompts, taxonomy.processes, experiments, feedbackEntries);

  await fs.mkdir(SITE_DATA_DIR, { recursive: true });
  await writeJson("site/data/prompts.json", promptsData);
  await writeJson("site/data/stats.json", makeStats(prompts, taxonomy, processIndex, roadmap));
  await writeJson("site/data/roadmap.json", roadmapData);
  await writeJson("site/data/checks.json", checksData);
  await writeJson("site/data/process-tree.json", processTreeData);
  const processesData = makeProcesses(
    taxonomy.processes,
    processIndexData,
    prompts,
    patternsList,
    checksData,
  );
  const patternsData = makePatterns(patternsList, prompts, operationsById);
  await writeJson("site/data/processes.json", processesData);
  await writeJson("site/data/patterns.json", patternsData);

  console.log(`Generated ${prompts.length} prompts`);
  console.log(
    `Generated ${processesData.processes.length} process cards and ${patternsData.patterns.length} patterns`,
  );
  console.log(`Generated ${taxonomy.operations.length} operations and ${taxonomy.processes.length} processes`);
  console.log(`Generated ${roadmap.levels.length} roadmap levels and ${roadmap.gaps.length} gaps`);
  console.log(
    `Generated process tree: ${processTree.shownSubprocesses}/${processTree.totalSubprocesses} subprocesses with prompts in ${processTree.shownProcesses}/${processTree.totalProcesses} processes (useTree=${processTree.useTree})`,
  );
  console.log(
    `Generated checks: ${checksData.tests.total} prompt tests in ${experiments.length} logs, ${checksData.feedback.total} feedback items`,
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
