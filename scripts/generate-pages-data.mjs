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
};

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

  const processes = (processTable?.rows || []).map((row) => {
    const id = Number(stripMarkdownInline(row[0]));
    return {
      id,
      label: stripMarkdownInline(row[1]),
      description: stripMarkdownInline(row[2]),
      operations: parseCodes(row[3]),
      icon: String(id),
    };
  });

  return { operations, processes };
}

function parsePromptMatrix(markdown) {
  const matrixTables = parseTables(markdown).filter(
    (table) => table.headers[0] === "Файл" && table.headers[1] === "Назначение",
  );
  const metadataByFile = new Map();

  for (const table of matrixTables) {
    for (const row of table.rows) {
      const file = extractFilename(row[0]);
      if (!file.endsWith(".md")) {
        continue;
      }
      metadataByFile.set(file, {
        file,
        description: stripMarkdownInline(row[1]),
        mode: stripMarkdownInline(row[2]),
        status: stripMarkdownInline(row[3]),
        version: stripMarkdownInline(row[4]),
        operationId: stripMarkdownInline(row[5]).replace(/-/g, "_"),
        processes: row[6]
          .split(";")
          .map(stripMarkdownInline)
          .filter(Boolean),
      });
    }
  }

  return metadataByFile;
}

function parseProcessIndex(markdown) {
  const table = parseTables(markdown).find(
    (candidate) => candidate.headers[0] === "№" && candidate.headers[1] === "Процесс",
  );
  return (table?.rows || []).map((row) => ({
    id: Number(stripMarkdownInline(row[0])),
    label: stripMarkdownInline(row[1]),
    operations: parseCodes(row[2]),
    pattern: stripMarkdownInline(row[3]),
    recommendedPrompts: parseCodes(row[4]),
  }));
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
    .filter((name) => name.endsWith(".md") && name !== "README.md")
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

async function main() {
  const [promptsReadme, taxonomyMarkdown, processIndexMarkdown, ecosystemMarkdown] =
    await Promise.all([
      read(SOURCE_FILES.promptsReadme),
      read(SOURCE_FILES.taxonomy),
      read(SOURCE_FILES.processIndex),
      read(SOURCE_FILES.ecosystem),
    ]);

  const taxonomy = parseTaxonomy(taxonomyMarkdown);
  const promptMetadata = parsePromptMatrix(promptsReadme);
  const processIndex = parseProcessIndex(processIndexMarkdown);
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

    prompts.push({
      id: basename.replace(/\.md$/, ""),
      file: basename,
      title: basename.replace(/\.md$/, ""),
      sourcePath: file.relativePath,
      url: repoUrl(file.relativePath),
      archived: file.archived,
      description: metadata?.description || "Описание отсутствует в prompts/README.md.",
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
      })),
      frontmatter,
      content,
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

  await fs.mkdir(SITE_DATA_DIR, { recursive: true });
  await writeJson("site/data/prompts.json", promptsData);
  await writeJson("site/data/stats.json", makeStats(prompts, taxonomy, processIndex, roadmap));
  await writeJson("site/data/roadmap.json", roadmapData);

  console.log(`Generated ${prompts.length} prompts`);
  console.log(`Generated ${taxonomy.operations.length} operations and ${taxonomy.processes.length} processes`);
  console.log(`Generated ${roadmap.levels.length} roadmap levels and ${roadmap.gaps.length} gaps`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
