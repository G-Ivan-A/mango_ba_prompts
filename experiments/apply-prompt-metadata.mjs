#!/usr/bin/env node
// Issue #92: add `id` + `title` frontmatter to all prompts, drop EXPERIMENTAL marker.
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");

const EXPERIMENTAL = "<!-- EXPERIMENTAL: DO NOT USE IN PRODUCTION -->\n";

// Human-readable Russian titles (2-5 words). Common abbreviations allowed:
// ФТ, ТЗ, ASR, UC, US, LLM. Mode is hinted to keep titles distinct per family.
const TITLES = {
  // Формирование ФТ/ТЗ
  "asr-ingestion-oneshot.md": "ASR: Нормализация транскрипции",
  "asr-ingestion-legacy.md": "ASR: Обработка транскрипции (устаревший)",
  "glossary-context-understanding-stepwise.md": "Контекст: Терминология и цели",
  "glossary-context-understanding-oneshot.md": "Контекст: Терминология за один ответ",
  "questions-customer-understanding-stepwise.md": "Вопросы: Выявление потребностей",
  "questions-customer-understanding-legacy.md": "Вопросы: Подготовка заказчику (устаревший)",
  "fr-documentation-stepwise.md": "ФТ: Генерация требований",
  "fr-documentation-oneshot.md": "ФТ: Генерация за один ответ",
  "constraints-documentation-stepwise.md": "Ограничения: Документирование",
  "constraints-documentation-oneshot.md": "Ограничения: За один ответ",
  "technical-details-solution-design-stepwise.md": "Технические детали: Проектирование",
  "technical-details-solution-design-oneshot.md": "Технические детали: За один ответ",
  "technical-details-solution-design-legacy.md": "Технические детали: Доработки (устаревший)",
  // Валидация ФТ/ТЗ
  "fr-validation-stepwise.md": "ФТ: Валидация и аудит",
  "fr-validation-oneshot.md": "ФТ: Экспресс-валидация",
  "fr-validation-legacy.md": "ФТ: Валидация (устаревший)",
  // Формирование UC/US
  "uc-modeling-stepwise.md": "Use Case: Моделирование",
  "uc-modeling-oneshot.md": "Use Case: Моделирование за один ответ",
  "us-modeling-stepwise.md": "User Story: Формирование",
  "us-modeling-oneshot.md": "User Story: Формирование за один ответ",
  // Помощь ПО/ПМ
  "meeting-customer-documentation-stepwise.md": "Встреча с клиентом: Резюме",
  "meeting-team-documentation-stepwise.md": "Встреча команды: Резюме",
  "letter-customer-documentation-legacy.md": "Письмо клиенту: Сопровождение (устаревший)",
  // Отладка и суммаризация сессий
  "session-debug-documentation-oneshot.md": "Сессия LLM: Суммаризация",
  // Архив
  "tz-stats-generator-legacy.md": "ТЗ: Статистика, расширенный (архив)",
  "tz-stats-generator-simple-legacy.md": "ТЗ: Статистика, простой (архив)",
  "usecase-stepwise-generator-legacy.md": "Use Case: Генератор (архив)",
  "usecase-stepwise-generator-simple-legacy.md": "Use Case: Генератор, простой (архив)",
  "user-story-generator-legacy.md": "User Story: Генератор (архив)",
  "user-story-generator-simple-legacy.md": "User Story: Генератор, простой (архив)",
};

async function listPromptFiles() {
  const active = (await fs.readdir(path.join(ROOT, "prompts")))
    .filter((name) => name.endsWith(".md") && name !== "README.md")
    .map((name) => `prompts/${name}`);
  const archived = (await fs.readdir(path.join(ROOT, "prompts", "archive")))
    .filter((name) => name.endsWith(".md"))
    .map((name) => `prompts/archive/${name}`);
  return [...active, ...archived];
}

function applyMetadata(content, basename) {
  if (!content.startsWith("---\n")) {
    throw new Error(`${basename}: no frontmatter`);
  }
  const id = `mango-${basename.replace(/\.md$/, "")}`;
  const title = TITLES[basename];
  if (!title) {
    throw new Error(`${basename}: no title mapping`);
  }

  let body = content;
  // Drop the EXPERIMENTAL marker line if present (keeps the blank line after it
  // as the separator between frontmatter and body).
  body = body.replace(`---\n${EXPERIMENTAL}`, "---\n");

  // Insert id + title right after the opening fence, ahead of existing fields.
  // Skip if already present (idempotent).
  if (!/^id:\s/m.test(body.split("\n---", 1)[0])) {
    body = body.replace(
      /^---\n/,
      `---\nid: ${id}\ntitle: "${title}"\n`,
    );
  }
  return body;
}

async function main() {
  const files = await listPromptFiles();
  let changed = 0;
  for (const relative of files) {
    const abs = path.join(ROOT, relative);
    const basename = path.basename(relative);
    const content = await fs.readFile(abs, "utf8");
    const next = applyMetadata(content, basename);
    if (next !== content) {
      await fs.writeFile(abs, next, "utf8");
      changed += 1;
      console.log(`updated ${relative}`);
    }
  }
  console.log(`Done: ${changed}/${files.length} files updated`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
