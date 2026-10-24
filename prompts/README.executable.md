---
status: draft
version: 0.1
updated: 2026-10-24
ai-generated: true
type: navigation
layer: executable
full_version: "prompts/README.md"
related_standard: "../standards/cascading-context-loading-standard.md"
related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
---

# Prompts README — executable layer

Load this file first when you need to choose or route a prompt. Do not load
`prompts/README.md` unless one escalation trigger below is true.

## Escalation triggers

- TRIGGER-1: пользователь явно просит полную матрицу промптов, историю,
  explanation, feedback workflow или GitHub Pages details.
- TRIGGER-2: нужно редактировать, валидировать или синхронизировать
  `prompts/README.md`.
- TRIGGER-3: текущая задача требует точной строки полной матрицы, статуса,
  версии, `id`, title или полного списка архивных legacy-файлов.
- TRIGGER-4: быстрый выбор ниже не покрывает задачу или противоречит
  `docs/ba-processes/00-index.executable.md`.

Если ни один триггер не сработал, выбирай prompt по таблице ниже.

## Execute

### Quick prompt selection

| Задача | Начни с |
| --- | --- |
| Спецификация бизнес-требований и дизайна решения (BCREQ) | `bcreq-constitution-governance-oneshot.md` (Промпт 0), затем шаги по разделу «BCREQ: маршрутизация» в `prompts/README.md` |
| Сырой запрос, встреча, письмо, ASR -> контекст для ФТ/ТЗ | `bcreq-context-understanding-stepwise.md`; агентом — `bcreq-in-understanding-oneshot.md`; для ASR сначала `asr-ingestion-oneshot.md` |
| Затронутые продукты, команды, согласующие | `bcreq-products-impact-analysis-stepwise.md` |
| User Story или Use Case | `bcreq-scenarios-modeling-oneshot.md` (`тип: US \| UC`); UC раздела 7 — `bcreq-uc-modeling-stepwise.md` |
| Функциональные требования | `bcreq-fr-documentation-stepwise.md`; агентом — `bcreq-core-documentation-oneshot.md` |
| Нефункциональные требования | `bcreq-nfr-documentation-stepwise.md` |
| Проверка черновика требований | `bcreq-review-validation-oneshot.md` |
| Ограничения / раздел 6 | `bcreq-constraints-documentation-stepwise.md` |
| Описание решения (ОРР) / раздел 5 | `bcreq-orr-solution-design-stepwise.md`; агентом — `bcreq-work-solution-design-oneshot.md` |
| Риски, зависимости, план приёмки / раздел 8 | `bcreq-extra-risk-analysis-stepwise.md` |
| Резюме встречи | `meeting-customer-documentation-stepwise.md` или `meeting-team-documentation-stepwise.md` |
| Суммаризация длинной LLM-сессии | `session-debug-documentation-oneshot.md` |
| Статистика, release readiness | active prompt отсутствует; см. process gaps в `docs/ba-processes/00-index.executable.md` |

### Mode decision

| Mode | Используй когда |
| --- | --- |
| `stepwise` | medium/high uncertainty, нужен gate между шагами, есть риск домыслов. |
| `oneshot` | вход полный, задача короткая, цена уточнения низкая. |
| `legacy` | нужна совместимость или сравнение с историческим prompt; не выбирай как default. |

### Required checks before running a prompt

1. Проверь frontmatter: `id`, `title`, `status`, `version`, `updated`,
   `temperature`.
2. Проверь, что операция в имени файла соответствует `docs/taxonomy.md`.
3. Проверь процесс и рекомендуемый маршрут через
   `docs/ba-processes/00-index.executable.md`.
4. Не добавляй новые prompt-файлы в `prompts/` без workflow из `CONTRIBUTING.md`.
5. Для перевода prompt в `canonical` нужен минимум один зафиксированный прогон
   в `runs/YYYY/RUN-XXXX/`.

### Feedback routing

Фидбек по prompt фиксируется issue с label `prompt:feedback`. В фидбеке нужны:
prompt name, результат, что именно не так, обезличенный вход/выход при
необходимости.
