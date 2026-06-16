#!/usr/bin/env node
// Issue #92: add "Название" (title) and "Токен" (id) columns to prompts/README.md matrix.
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const README = path.join(ROOT, "prompts", "README.md");

const OLD_HEADER =
  "| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |";
const NEW_HEADER =
  "| Файл | Название | Токен | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |";
const OLD_SEP = "| --- | --- | --- | --- | --- | --- | --- |";
const NEW_SEP = "| --- | --- | --- | --- | --- | --- | --- | --- | --- |";

async function readTitles() {
  // Read titles + ids straight from the prompt frontmatter to stay in sync.
  const dirs = ["prompts", "prompts/archive"];
  const map = new Map();
  for (const dir of dirs) {
    const names = await fs.readdir(path.join(ROOT, dir));
    for (const name of names) {
      if (!name.endsWith(".md") || name === "README.md") continue;
      const content = await fs.readFile(path.join(ROOT, dir, name), "utf8");
      const id = content.match(/^id:\s*(.+)$/m)?.[1].trim();
      const title = content
        .match(/^title:\s*(.+)$/m)?.[1]
        .trim()
        .replace(/^["']|["']$/g, "");
      if (id && title) map.set(name, { id, title });
    }
  }
  return map;
}

function isMatrixDataRow(line) {
  return /^\|\s*\[`?[^`\]]+\.md`?\]/.test(line.trim());
}

function fileFromRow(line) {
  return line.match(/\[`?([^`\]]+\.md)`?\]/)?.[1];
}

async function main() {
  const titles = await readTitles();
  const lines = (await fs.readFile(README, "utf8")).split("\n");
  let inMatrix = false;
  const out = [];
  const missing = [];

  for (const line of lines) {
    if (line.trim() === OLD_HEADER) {
      out.push(NEW_HEADER);
      inMatrix = true;
      continue;
    }
    if (inMatrix && line.trim() === OLD_SEP) {
      out.push(NEW_SEP);
      continue;
    }
    if (inMatrix && isMatrixDataRow(line)) {
      const file = fileFromRow(line);
      const meta = titles.get(file);
      if (!meta) {
        missing.push(file);
        out.push(line);
        continue;
      }
      // Insert "Название" and "Токен" cells right after the first (Файл) cell.
      const firstSep = line.indexOf("|", line.indexOf("|") + 1);
      const firstCell = line.slice(0, firstSep + 1);
      const rest = line.slice(firstSep + 1);
      out.push(`${firstCell} ${meta.title} | \`${meta.id}\` |${rest}`);
      continue;
    }
    if (inMatrix && !line.trim().startsWith("|")) {
      inMatrix = false;
    }
    out.push(line);
  }

  if (missing.length) {
    console.error("Missing metadata for:", missing);
    process.exitCode = 1;
    return;
  }
  await fs.writeFile(README, out.join("\n"), "utf8");
  console.log("prompts/README.md matrix updated");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
