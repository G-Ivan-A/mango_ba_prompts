---
status: draft
version: 0.2
updated: 2026-06-11
ai-generated: true
type: contract
scope: patterns
related_artifacts:
  - "docs/adr/002-pattern-standard.md"
  - "docs/adr/001-prompt-standard.md"
  - "standards/prompt-standard.md"
  - "docs/taxonomy.md"
  - "docs/ba-processes/00-index.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/52"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/63"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/64"
---

# Стандарт паттерна

> Предложен на утверждение Пользователю (issue #52). До утверждения —
> рекомендация. Нормативный словарь —
> [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**).

## Стороны и область

Контракт обязывает всех contributors и AI-агентов, создающих или изменяющих
файлы в `patterns/`. Паттерн — воспроизводимое описание способа решения
класса задач БА; его исполняемые реализации живут в `prompts/`
(см. [prompt-standard.md](prompt-standard.md)).

Архитектурное обоснование стандарта — в
[ADR-002 (pattern standard)](../docs/adr/002-pattern-standard.md).

## Обязательства

### Структура — 8 обязательных полей

1. Паттерн **ДОЛЖЕН** содержать 8 полей — как разделы документа
   `patterns/[operation-name]/README.md` (заголовки `## <поле>`), в этом
   порядке:

   | № | Поле | Содержание |
   | --- | --- | --- |
   | 1 | `purpose` | Какую задачу БА решает паттерн; когда применять и когда **не** применять. |
   | 2 | `process_stage` | Процесс (№ из [docs/taxonomy.md](../docs/taxonomy.md) §2) и когнитивные операции (§1). |
   | 3 | `context_requirements` | Обязательный входной контекст: документы, термины, ограничения. |
   | 4 | `prompt_template` | Шаблон промпта с плейсхолдерами `{{...}}`. |
   | 5 | `quality_gates` | Проверки результата до использования (чек-лист). |
   | 6 | `examples` | ≥ 1 обезличенный пример «вход → выход». |
   | 7 | `output_schema` | Структура ожидаемого результата: разделы, формат. |
   | 8 | `governance_rules` | Правила применения: review, статусы, ограничения. |

2. `prompt_template` **ДОЛЖЕН** быть универсальным (LLM-агностичным):
   без привязки к конкретной модели и без model-specific синтаксиса.
3. Frontmatter паттерна **ДОЛЖЕН** содержать `status`
   (`draft` \| `canonical` \| `archived`), `version`, `updated` —
   и **НЕ ДОЛЖЕН** содержать маппинг на промпты: связь
   паттерн ↔ промпт ведётся только в
   [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md).

### Именование и жизненный цикл

4. Директория паттерна **ДОЛЖНА** быть в kebab-case и отражать операцию или
   краткое назначение: `patterns/[operation-name]/`
   (например, `patterns/ambiguity-elicitation/`,
   `patterns/gap-analysis/`, `patterns/user-story-generation/`).
5. Директория паттерна **ДОЛЖНА** содержать `README.md`, `examples/` и
   **МОЖЕТ** содержать `related/`, если есть связанные артефакты.
6. Новый паттерн **ДОЛЖЕН** проходить issue → PR → human review;
   `canonical` присваивается после подтверждённого применения
   (зафиксированный прогон реализующего промпта в `prompts/experiments/`,
   ручной кейс БА или PR evidence).
7. Паттерн-кандидат на перенос в Хаб оценивается по критериям
   [docs/rfc-hub-integration.md](../docs/rfc-hub-integration.md) (§3).

## Критерии соответствия (DoD)

- [ ] Все 8 разделов присутствуют и непусты.
- [ ] `prompt_template` не содержит model-specific синтаксиса.
- [ ] Примеры обезличены (нет корпоративных данных и закрытых ссылок).
- [ ] Паттерн отражён в колонке «Паттерн»
      [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md).
- [ ] Директория соответствует `patterns/[operation-name]/README.md` и содержит
      каталог `examples/`.

## Обоснование

- **Поля как разделы, а не frontmatter.** Поля паттерна содержательные
  (шаблоны, примеры, чек-листы) — им место в теле документа; frontmatter
  остаётся минимальным по аналогии с
  [prompt-standard.md](prompt-standard.md).
- **Маппинг вне файла.** Один паттерн → несколько промптов (режимы
  `stepwise`/`oneshot`); хранение связи в одном реестре исключает дрейф
  при добавлении/архивации промптов.
- **Директория вместо одиночного файла.** Паттерну нужны основной текст,
  few-shot examples и иногда связанные артефакты. Directory-first layout
  сохраняет `README.md` компактным и не раздувает верхний уровень `patterns/`.
