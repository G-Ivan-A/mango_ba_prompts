---
status: draft
version: 0.2
updated: 2026-08-21
ai-generated: true
type: contract
scope: context-loading
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
related_artifacts:
  - "AI_SESSION_HANDOVER_PROMPT.executable.md"
  - "ai-rules/agent-onboarding-protocol.md"
  - "prompts/README.executable.md"
  - "docs/ba-processes/00-index.executable.md"
  - "standards/ba-ontology.executable.md"
---

# Cascading Context Loading Standard

Стандарт фиксирует паттерн каскадной загрузки контекста для документов, где
полная human-readable версия заметно больше исполнимого слоя. Цель - загрузить
в LLM минимальный слой, достаточный для задачи, и эскалировать к полной версии
только по проверяемым условиям.

## Принцип

Контекст загружается строго по уровням:

| Уровень | Назначение | Когда загружать |
| --- | --- | --- |
| Level 1: `executable` | Минимальные инструкции, маршруты, правила и триггеры. | Всегда первым. |
| Level 2: `full` | Полный документ для человека: rationale, история, таблицы, детали. | Только если сработал `Escalation trigger`. |
| Level 3: `raw` | Исходные данные: внешние документы, PDF, первичные материалы. | Только если full-слоя недостаточно или пользователь явно просит источник. |

LLM не выбирает слой свободно. Если триггер не сработал, агент продолжает работу
на текущем уровне и не загружает более тяжёлый файл "на всякий случай".

## Naming

Парный исполнимый файл создаётся рядом с полной версией:

```text
<name>.md              # full layer
<name>.executable.md   # executable layer
```

Для `README.md` используется имя `README.executable.md` в той же директории.
Оригинальный файл не переименовывается и остаётся full-версией.

## Executable file contract

Каждый `.executable.md` должен содержать:

- frontmatter `layer: executable`;
- frontmatter `full_version: "<path-to-full>.md"`;
- ссылку на этот стандарт;
- раздел `## Escalation triggers`;
- закрытый список триггеров `TRIGGER-1`, `TRIGGER-2`, ...;
- короткий исполнимый алгоритм или навигацию, достаточную для типового запроса;
- запрет загружать full-слой при отсутствии триггера.

Минимальный каркас:

```markdown
---
status: draft
version: 0.1
updated: YYYY-MM-DD
ai-generated: true
layer: executable
full_version: "path/to/file.md"
related_standard: "standards/cascading-context-loading-standard.md"
---

# <Title> — executable layer

Load this file first. Do not load `<full_version>` unless one escalation trigger
below is true.

## Escalation triggers

- TRIGGER-1: ...
- TRIGGER-2: ...
- TRIGGER-3: ...

## Execute

...
```

## LLM Loading Contract

Каждая full-версия, для которой создан companion, должна получить предупреждение
в начале файла:

```markdown
> **LLM Loading Contract — full layer.**
> Start with [`<name>.executable.md`](<name>.executable.md). Load this full file
> only when an escalation trigger in the executable companion is true: explicit
> user request for full/rationale/history, missing required section in
> executable, need for exact wording/table/reference, or editing/validating this
> full file. Otherwise do not load this file into context.
```

Формулировка может быть локализована, но должна явно называть executable-файл и
запрещать загрузку full без триггера.

## Escalation triggers

Базовый закрытый список:

- `TRIGGER-1`: пользователь явно просит полную версию, историю, rationale,
  источники или точную цитату из full-файла.
- `TRIGGER-2`: executable-слой не содержит раздел, таблицу, правило или ссылку,
  без которых текущая задача не выполнима.
- `TRIGGER-3`: нужно редактировать, валидировать или синхронизировать сам
  full-файл.
- `TRIGGER-4`: найдено противоречие между executable-слоем, full-слоем,
  issue/PR-контекстом или стандартом, и без full-файла конфликт не разрешить.
- `TRIGGER-5`: проверка требует точного полного маппинга, реестра или таблицы, а
  не краткого маршрута.

Для конкретного файла список можно сузить или уточнить, но нельзя заменять его
расплывчатым "если нужно больше контекста".

## Selection criteria

Файл считается кандидатом на companion, если выполняется хотя бы два условия:

- частое использование агентами или пользовательскими LLM;
- full-версия содержит rationale, историю, таблицы или навигацию сверх
  исполнимой части;
- full-версия превышает примерно 3 500 токенов по текущему методу замера;
- ожидаемая экономия составляет не менее 30%;
- файл уже указан как hotspot в issue, RFC или onboarding-контракте.

## Metrics

Экономия считается как:

```text
savings_tokens = full_tokens - executable_tokens
ratio = full_tokens / executable_tokens
```

Метод подсчёта должен быть воспроизводимым. В этом репозитории используется
`scripts/kb/tokens.py`: `tiktoken:cl100k_base`, если доступен, иначе
эвристика `chars/3.3`.

## DoD

- [ ] У full-файла есть соседний `.executable.md`.
- [ ] Full-файл содержит `LLM Loading Contract`.
- [ ] Executable-файл содержит `Escalation triggers` с детерминированными
      условиями.
- [ ] Executable-файл меньше full-файла по токенам.
- [ ] Ссылки на оптимизированный документ в исполнимых промптах ведут на
      executable-слой, если полная версия не требуется.
- [ ] Изменение проверено `python3 scripts/validate_issue_125_cascading_context.py`.
