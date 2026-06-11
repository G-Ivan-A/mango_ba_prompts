---
status: draft
version: 0.2
updated: 2026-06-11
ai-generated: true
type: navigation
---

# Patterns — паттерны бизнес-анализа

**Паттерн** — воспроизводимое описание способа решения класса задач БА.
**Промпт** (`prompts/`) — конкретная исполняемая реализация; один паттерн
может реализовываться несколькими промптами (например, `stepwise` и
`oneshot` режимами).

Полное архитектурное решение — [ADR-002 (pattern standard)](../docs/adr/002-pattern-standard.md).

## Структура паттерна — 8 полей

Каждый паттерн хранится в `patterns/[operation-name]/README.md` и описывается
восемью обязательными полями (нормативный контракт —
[standards/pattern-standard.md](../standards/pattern-standard.md)):

| Поле | Содержание |
| --- | --- |
| `purpose` | Какую задачу БА решает паттерн и когда его применять. |
| `process_stage` | Процесс и когнитивные операции из [docs/taxonomy.md](../docs/taxonomy.md). |
| `context_requirements` | Какой входной контекст обязателен (документы, термины, ограничения). |
| `prompt_template` | Универсальный (LLM-агностичный) шаблон промпта. |
| `quality_gates` | Проверки качества результата до использования. |
| `examples` | Примеры входа и ожидаемого выхода (обезличенные). |
| `output_schema` | Структура ожидаемого результата (разделы, формат). |
| `governance_rules` | Правила жизненного цикла: review, статусы, ограничения применения. |

## Структура директории

```text
patterns/
└── [operation-name]/
    ├── README.md
    ├── examples/
    └── related/
```

`[operation-name]` — kebab-case slug паттерна, например
`ambiguity-elicitation`, `gap-analysis`, `user-story-generation`.

## Правила каталога

- Маппинг **паттерн ↔ промпт** ведётся только в
  [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md) —
  не во frontmatter паттернов или промптов.
- `prompt_template` пока универсальный: без привязки к конкретной LLM
  и без специализированных вариантов под модели.
- Если нужна специфичная LLM-реализация, создаётся или обновляется отдельный
  prompt-файл в `prompts/`, а паттерн не дробится.
- Сейчас каталог пуст: паттерны создаются отдельными задачами
  (issue → PR → review) после утверждения фундамента
  (issue [#52](https://github.com/G-Ivan-A/mango_ba_prompts/issues/52),
  ADR [#64](https://github.com/G-Ivan-A/mango_ba_prompts/issues/64)).
