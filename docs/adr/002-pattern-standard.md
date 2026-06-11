---
status: accepted
version: 1.0
updated: 2026-06-11
ai-generated: true
type: adr
scope: pattern-standard
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/64"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/57"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/59"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/60"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/69"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/63"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/61"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/pattern-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md"
---

# ADR-002: Стандарт паттернов бизнес-анализа

> **Статус:** Accepted · **Дата:** 2026-06-11 · **Issue:**
> https://github.com/G-Ivan-A/mango_ba_prompts/issues/64

> **Numbering note.** Имя файла следует прямому DoD issue #64:
> `docs/adr/002-pattern-standard.md`. Уже принятый файл
> `docs/adr/0002-issue48-handover-local-enrichment.md` не переименовывается в этой
> задаче. В обсуждениях этот документ нужно называть **ADR-002 (pattern
> standard)**, чтобы не путать с историческим ADR-0002. Такой подход совместим с
> практикой экосистемы, где номер может быть стабильным идентификатором области при
> явном disambiguation:
> https://github.com/G-Ivan-A/clarify-engine-ai/blob/main/docs/ADR/README.md

## Контекст

В PR #60 создан фундамент библиотеки паттернов:
https://github.com/G-Ivan-A/mango_ba_prompts/pull/60

Уже существуют четыре опорных файла:

| Файл | Роль |
| --- | --- |
| `patterns/README.md` | Краткая навигация по каталогу паттернов: что такое паттерн, какие 8 полей обязательны, где хранится маппинг. Полный URL: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md |
| `standards/pattern-standard.md` | Операционный контракт паттерна: обязательные поля, frontmatter, lifecycle, критерии соответствия. Полный URL: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/pattern-standard.md |
| `docs/taxonomy.md` | Таксономия 13 когнитивных операций и 9 процессов БА. Полный URL: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md |
| `docs/ba-processes/00-index.md` | Единственный централизованный реестр связей процесс, операция, паттерн, промпт. Полный URL: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md |

Этого недостаточно для масштабирования библиотеки. README объясняет 8 полей, но не
фиксирует архитектурное решение: зачем паттерны отделены от промптов, как они
связаны с таксономией, как создавать новые паттерны, как версионировать изменения
и где вести связи с промптами.

Ключевое различие:

- **Паттерн** - воспроизводимая аналитическая практика бизнес-анализа. Это
  когнитивная операция или комбинация операций, которую БА мог выполнять и без
  LLM.
- **Промпт** - исполняемый артефакт для выполнения паттерна через LLM. Один
  паттерн может иметь несколько промптов: `stepwise`, `oneshot`, `legacy` или
  другие варианты, разрешённые стандартом промптов.

Связанный стандарт промптов уже зафиксировал, что маппинг паттерн <-> промпт <->
процесс не живёт во frontmatter промпта:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md

ADR-001 (issue #63) зафиксировал стандарт промптов как архитектурное решение:
структуры prompt-файлов, режимы `stepwise` / `oneshot` / `legacy`, frontmatter и
именование. Этот ADR на стандарт паттернов не меняет prompt-контракт, а
дополняет его слоем аналитических практик:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md

Issue #61 и PR #68 зафиксировали Creative-mode governance: если архитектурная
практика меняется, решение нужно оформлять как ADR:
https://github.com/G-Ivan-A/mango_ba_prompts/issues/61

## Практика и источники

В Хабе на 2026-06-11 найден только каркас `templates/htom/docs/adr/`, без
содержательного ADR-шаблона:
https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/templates/htom/docs/adr

Поэтому этот ADR использует локальный формат `mango_ba_prompts`: frontmatter,
`Контекст`, `Решение`, `Последствия`, `Альтернативы`, `Связанные артефакты`.
Формат совпадает с уже принятыми ADR этого репозитория:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/0003-creative-mode-governance.md

Решение опирается на международную практику pattern languages, design patterns и
prompt patterns:

| Практика | Что берём в стандарт |
| --- | --- |
| Christopher Alexander, pattern language | Паттерн описывает повторяющуюся проблему в контексте и ядро решения, которое можно применять много раз без буквального копирования. Источник: https://arl.human.cornell.edu/linked%20docs/Alexander_A_Pattern_Language.pdf |
| Gang of Four, design patterns | У паттерна должны быть стабильное имя, intent/applicability, consequences и related patterns, чтобы команда использовала общий словарь. Источник: https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610 |
| Prompt Pattern Catalog | Prompt patterns полезны как переносимые способы структурировать взаимодействие с LLM, но конкретный prompt остаётся адаптируемой реализацией. Источник: https://arxiv.org/abs/2302.11382 |

Вывод для Mango: библиотека должна строиться вокруг когнитивных операций и
процессов БА, а не вокруг отдельных prompt-файлов.

## Решение

### 1. Утвердить разделение паттерна и промпта

Паттерн описывает аналитический способ работы. Промпт реализует этот способ в
LLM. Это даёт три правила:

1. Паттерн **должен** быть LLM-агностичным.
2. Промпт **может** быть конкретной реализацией паттерна для режима работы,
   аудитории или уровня детализации.
3. Связи процесс <-> паттерн <-> промпт **должны** храниться только в
   `docs/ba-processes/00-index.md`, а не во frontmatter паттерна или промпта.

### 2. Утвердить структуру директории паттерна

Новый паттерн создаётся как директория:

```text
patterns/
└── [operation-name]/
    ├── README.md
    ├── examples/
    └── related/
```

`[operation-name]` - kebab-case slug паттерна, например
`ambiguity-elicitation`, `gap-analysis`, `user-story-generation`. Это не обязан
быть точный ID таксономии вроде `validation`; ID таксономии фиксируется внутри
поля `process_stage`.

Назначение файлов:

| Путь | Назначение | Обязательность |
| --- | --- | --- |
| `patterns/[operation-name]/README.md` | Основной документ паттерна с frontmatter и 8 обязательными разделами. | Обязателен |
| `patterns/[operation-name]/examples/` | Расширенные few-shot примеры, если они слишком велики для поля `examples`. | Обязателен как каталог, может быть пустым на `draft` |
| `patterns/[operation-name]/related/` | Связанные материалы: sanitized notes, схемы, чек-листы, если они нужны для понимания паттерна. | Опционален по содержимому |

Frontmatter паттерна минимален:

```yaml
---
status: draft
version: 0.1.0
updated: 2026-06-11
---
```

Frontmatter **не должен** содержать связи с промптами, процессами или LLM. Эти
связи ведутся в `docs/ba-processes/00-index.md`.

### 3. Зафиксировать 8 обязательных полей

Каждый `patterns/[operation-name]/README.md` содержит ровно эти 8 разделов в
указанном порядке.

| № | Поле | Назначение | Формат содержимого | Пример заполнения |
| --- | --- | --- | --- | --- |
| 1 | `purpose` | Объясняет, какую задачу БА решает паттерн, когда его применять и когда не применять. | 2-5 абзацев, включая границы применимости. | `Паттерн fr-generation преобразует утверждённые разделы 1-2, User Story и Use Case в проверяемые ФТ.` |
| 2 | `process_stage` | Связывает паттерн с процессами БА и когнитивными операциями из `docs/taxonomy.md`. | Список процессов и ID операций. | `Процессы: Формирование ФТ/ТЗ. Операции: documentation, validation.` |
| 3 | `context_requirements` | Фиксирует обязательный входной контекст. | Чек-лист входов, optional inputs, стоп-факторы. | `Нужны: глоссарий, проблема/цель/задачи, US/UC, ограничения продукта.` |
| 4 | `prompt_template` | Даёт универсальный шаблон выполнения паттерна через LLM. | Markdown-шаблон с плейсхолдерами `{{...}}`, без model-specific синтаксиса. | `Используй {{glossary}} и {{use_case}} для генерации ФТ; сначала запроси недостающий контекст.` |
| 5 | `quality_gates` | Описывает проверки качества результата до использования. | Чек-лист с pass/fail критериями. | `Все ФТ атомарны; термины соответствуют глоссарию; нет скрытых UI/API деталей.` |
| 6 | `examples` | Показывает few-shot пример входа и ожидаемого выхода. | Минимум один обезличенный пример или ссылка на файл в `examples/`. | `Вход: короткая US. Выход: 3 ФТ 4.x с критериями.` |
| 7 | `output_schema` | Фиксирует структуру результата. | Markdown-outline, таблица, JSON Schema или другой явный формат. | `## 4. Функциональные требования`, далее `4.x`, `4.x.1`, `4.x.1.1`. |
| 8 | `governance_rules` | Описывает lifecycle, review, ограничения применения и связанные риски. | Статусы, reviewer, versioning, privacy rules. | `status: canonical только после human review и проверки маппинга в реестре.` |

### 4. Связать паттерны с таксономией

Каждый паттерн соответствует одной или нескольким когнитивным операциям из
таксономии `docs/taxonomy.md`:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md

Операция фиксируется в поле `process_stage` и в реестре
`docs/ba-processes/00-index.md`:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md

| Операция таксономии | Примеры паттернов |
| --- | --- |
| `ingestion` | `asr-cleanup`, `document-intake-normalization` |
| `understanding` | `glossary-context-generation`, `ambiguity-elicitation` |
| `validation` | `fr-validation`, `consistency-check` |
| `modeling` | `use-case-modeling`, `user-story-generation` |
| `solution_design` | `technical-details-generation`, `constraints-generation` |
| `documentation` | `fr-generation`, `meeting-summary`, `customer-letter-generation` |
| `quality` | `requirements-quality-statistics`, `prompt-output-self-test` |
| `research` | `market-practice-research`, `domain-benchmarking` |
| `governance` | `pattern-readiness-review`, `taxonomy-change-review` |
| `impact_analysis` | `change-impact-map`, `dependency-impact-assessment` |
| `reverse_requirements` | `legacy-feature-reconstruction`, `behavior-to-requirements` |
| `risk_analysis` | `requirements-risk-register`, `tender-risk-scan` |
| `release_readiness` | `release-readiness-check`, `acceptance-criteria-audit` |

Примеры в таблице задают ожидаемые slug-и паттернов. Часть из них пока является
planned gap, потому что каталог `patterns/` пуст до отдельных issue и PR.

### 5. Связать паттерны с 9 процессами БА

Каждый процесс БА использует один или несколько паттернов. Маппинг ведётся в
`docs/ba-processes/00-index.md`, не в файлах паттернов и не в prompt-frontmatter.
Подробные workflow процессов описаны в карте экосистемы:
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md

| Процесс БА | Ключевые операции | Примеры паттернов | Существующие prompt-реализации |
| --- | --- | --- | --- |
| Формирование ФТ/ТЗ | `ingestion`, `understanding`, `modeling`, `documentation`, `solution_design`, `validation` | `glossary-context-generation`, `user-story-generation`, `use-case-modeling`, `fr-generation`, `fr-validation`, `constraints-generation`, `technical-details-generation` | `asr-ingestion-oneshot.md`, `glossary-context-understanding-stepwise.md`, `glossary-context-understanding-oneshot.md`, `questions-customer-understanding-stepwise.md`, `questions-customer-understanding-legacy.md`, `us-modeling-stepwise.md`, `us-modeling-oneshot.md`, `uc-modeling-stepwise.md`, `uc-modeling-oneshot.md`, `fr-documentation-stepwise.md`, `fr-documentation-oneshot.md`, `constraints-documentation-stepwise.md`, `constraints-documentation-oneshot.md`, `technical-details-solution-design-stepwise.md`, `technical-details-solution-design-oneshot.md`, `fr-validation-stepwise.md`, `fr-validation-oneshot.md`, `fr-validation-legacy.md` |
| Валидация ФТ/ТЗ | `validation`, `quality`, `risk_analysis` | `fr-validation`, `requirements-quality-check`, `requirements-risk-scan` | `fr-validation-stepwise.md`, `fr-validation-oneshot.md`, `fr-validation-legacy.md` |
| Анализ тендерных ТЗ | `ingestion`, `understanding`, `validation`, `risk_analysis`, `quality` | `tender-intake`, `tender-gap-analysis`, `tender-risk-scan`, `tender-quality-check` | `glossary-context-understanding-stepwise.md`, `glossary-context-understanding-oneshot.md`, `questions-customer-understanding-stepwise.md`, `questions-customer-understanding-legacy.md`, `fr-validation-stepwise.md`, `fr-validation-oneshot.md`, `fr-validation-legacy.md` |
| Формирование UC/US | `understanding`, `modeling`, `validation` | `use-case-modeling`, `user-story-generation`, `scenario-validation` | `uc-modeling-stepwise.md`, `uc-modeling-oneshot.md`, `us-modeling-stepwise.md`, `us-modeling-oneshot.md`, `glossary-context-understanding-stepwise.md`, `glossary-context-understanding-oneshot.md` |
| Визуализация UML/BPMN | `modeling`, `documentation`, `quality` | `process-diagram-generation`, `sequence-diagram-generation`, `diagram-quality-check` | Пока нет активных prompt-файлов |
| Помощь ПО/ПМ | `ingestion`, `understanding`, `documentation`, `governance` | `meeting-summary`, `customer-question-generation`, `customer-letter-generation`, `decision-log-generation` | `asr-ingestion-oneshot.md`, `meeting-team-documentation-stepwise.md`, `meeting-customer-documentation-stepwise.md`, `questions-customer-understanding-stepwise.md`, `questions-customer-understanding-legacy.md`, `letter-customer-documentation-legacy.md` |
| Статистика | `ingestion`, `quality`, `research` | `requirements-quality-statistics`, `tz-statistics`, `metric-research-summary` | Активного prompt-файла нет; legacy-реализации находятся в `prompts/archive/` |
| Impact Analysis | `reverse_requirements`, `impact_analysis`, `validation`, `governance` | `change-impact-map`, `legacy-feature-reconstruction`, `impact-validation`, `change-decision-log` | Пока нет активных prompt-файлов |
| Risk Analysis | `risk_analysis`, `release_readiness`, `validation`, `quality` | `requirements-risk-register`, `release-readiness-check`, `risk-validation`, `quality-risk-summary` | Пока нет активных prompt-файлов |

Полные URL существующих prompt-файлов:

- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-legacy.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/constraints-documentation-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/constraints-documentation-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-oneshot.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/questions-customer-understanding-stepwise.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/questions-customer-understanding-legacy.md
- https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/letter-customer-documentation-legacy.md

### 6. Связать паттерны с промптами через реестр

Один паттерн может реализовываться несколькими промптами.

Пример:

| Паттерн | Реализации |
| --- | --- |
| `fr-generation` | `fr-documentation-stepwise.md`, `fr-documentation-oneshot.md` |
| `fr-validation` | `fr-validation-stepwise.md`, `fr-validation-oneshot.md`, `fr-validation-legacy.md` |
| `glossary-context-generation` | `glossary-context-understanding-stepwise.md`, `glossary-context-understanding-oneshot.md` |

Маппинг фиксируется в `docs/ba-processes/00-index.md`. Он **не фиксируется**:

- во frontmatter промпта;
- во frontmatter паттерна;
- в имени prompt-файла сверх правил `standards/prompt-standard.md`.

### 7. Зафиксировать LLM-агностичность `prompt_template`

`prompt_template` в паттерне должен описывать универсальный способ выполнения
задачи. Он не должен зависеть от конкретной модели, провайдера или UI.

Разрешено:

```markdown
Используй {{glossary}}, {{business_context}} и {{use_case}}.
Сначала проверь полноту контекста. Если отсутствует обязательный вход, задай
уточняющий вопрос. Затем сформируй ФТ по схеме {{output_schema}}.
```

Не разрешено в паттерне:

```markdown
В GPT-4.1 включи режим reasoning_effort=high и используй tool call X.
```

Если нужна специфичная реализация для конкретной LLM или режима работы, создаётся
или обновляется отдельный промпт в `prompts/` по правилам
`standards/prompt-standard.md`, а паттерн не дробится. Паттерн остаётся
LLM-агностичным, а различия реализации отражаются в prompt-файле, PR-описании и
централизованном реестре.

### 8. Утвердить процесс создания нового паттерна

Новый паттерн создаётся только через issue -> PR -> human review.

1. Определить когнитивную операцию или операции из `docs/taxonomy.md`.
2. Определить процессы БА, которые используют эту операцию.
3. Выбрать kebab-case slug `patterns/[operation-name]/`.
4. Создать `patterns/[operation-name]/README.md` с frontmatter и 8 обязательными
   разделами.
5. Добавить минимум один обезличенный пример в раздел `examples` или в каталог
   `patterns/[operation-name]/examples/`.
6. Обновить `docs/ba-processes/00-index.md`: процесс <-> операция <-> паттерн.
7. Создать или обновить prompt-файлы в `prompts/`, если нужна LLM-реализация.
8. Обновить `docs/ba-processes/00-index.md`: паттерн <-> рекомендуемые промпты.
9. Запустить локальные проверки: `git diff --check` и task-specific validator, если
   он есть.

Критерии зрелости:

| Статус | Когда использовать |
| --- | --- |
| `draft` | Все 8 разделов есть, но паттерн ещё не прошёл human review или не имеет подтверждённого применения. |
| `canonical` | Паттерн прошёл review, отражён в `docs/ba-processes/00-index.md`, имеет минимум один обезличенный пример и подтверждённое применение: prompt-run, ручной кейс БА или PR evidence. |
| `archived` | Паттерн заменён, устарел или больше не рекомендован; файл сохраняется для истории, а реестр указывает замену или причину архивации. |

Паттерн считается готовым к использованию, когда:

- все 8 разделов непустые;
- `process_stage` ссылается на существующие операции таксономии;
- в реестре есть строка с процессом, паттерном и prompt-реализациями или явным
  `пока нет`;
- `quality_gates` можно проверить без дополнительных устных пояснений;
- примеры не содержат закрытых корпоративных данных.

### 9. Утвердить версионирование

Паттерны версионируются отдельно от промптов. Версия паттерна хранится во
frontmatter `patterns/[operation-name]/README.md`.

Используется semver-логика `major.minor.patch`:

| Изменение | Когда |
| --- | --- |
| `major` | Breaking change: меняется `purpose`, обязательный вход, `output_schema`, смысл когнитивной операции, maturity rule или quality gate так, что существующие prompt-реализации могут стать неверными. |
| `minor` | Backward-compatible расширение: добавлены примеры, уточнены optional inputs, добавлен процесс БА, расширен список quality gates без разрушения старого результата. |
| `patch` | Исправлены опечатки, ссылки, формулировки, неполные примеры без изменения поведения паттерна. |

Изменение паттерна не обязано автоматически менять версии всех промптов. Но при
каждом `major` или `minor` изменении паттерна PR должен проверить связанные
prompt-файлы из `docs/ba-processes/00-index.md`:

- если prompt больше не соответствует `prompt_template` или `output_schema`, prompt
  обновляется и получает свою версию по `standards/prompt-standard.md`;
- если prompt остаётся совместимым, в PR достаточно указать это в validation;
- `patch` паттерна обычно не требует изменения prompt-версий.

## Примеры

### Минимальный каркас `patterns/fr-generation/README.md`

```markdown
---
status: draft
version: 0.1.0
updated: 2026-06-11
---

# fr-generation

## purpose

Паттерн преобразует утверждённый бизнес-контекст, глоссарий, User Story и Use
Case в проверяемые функциональные требования.

## process_stage

- Процессы БА: Формирование ФТ/ТЗ.
- Когнитивные операции: `documentation`, `validation`.

## context_requirements

- Утверждённый глоссарий.
- Разделы 1-2 или эквивалентный бизнес-контекст.
- User Story и Use Case.
- Ограничения продукта.

## prompt_template

Используй {{glossary}}, {{business_context}}, {{user_story}} и {{use_case}}.
Сначала проверь полноту контекста, затем сформируй ФТ по output_schema.

## quality_gates

- Все ФТ атомарны.
- Термины соответствуют глоссарию.
- Нет скрытых UI/API деталей без источника.

## examples

См. `examples/basic-fr-generation.md`.

## output_schema

- `4.x` - родительское требование.
- `4.x.1` - детализация.
- `4.x.1.1` - атомарные условия или параметры.

## governance_rules

- `canonical` только после human review.
- Маппинг с промптами ведётся в `docs/ba-processes/00-index.md`.
```

### Пример строки реестра

```markdown
| 1 | Формирование ФТ/ТЗ | `ingestion`, `understanding`, `documentation`, `solution_design` | `glossary-context-generation`, `fr-generation`, `constraints-generation`, `technical-details-generation` | `glossary-context-understanding-*`, `fr-documentation-*`, `constraints-documentation-*`, `technical-details-solution-design-*` |
```

## Отношение к существующим документам

Выбран вариант A: ADR дополняет существующие документы, а не заменяет их.

| Документ | Роль после этого ADR |
| --- | --- |
| `docs/adr/002-pattern-standard.md` | Полное архитектурное решение: контекст, rationale, trade-offs, последствия, связь с международной практикой и экосистемой. |
| `standards/pattern-standard.md` | Нормативный операционный контракт для review: 8 полей, directory-first layout, frontmatter, lifecycle, DoD. |
| `patterns/README.md` | Короткая справка и навигация для человека, который открывает каталог паттернов. |
| `docs/ba-processes/00-index.md` | Единственный реестр связей процесс <-> операция <-> паттерн <-> prompt. |

Если между ними возникает расхождение, приоритет такой:

1. ADR фиксирует архитектурное решение и rationale.
2. `standards/pattern-standard.md` применяет решение как проверяемый контракт.
3. `patterns/README.md` кратко пересказывает контракт для навигации.
4. `docs/ba-processes/00-index.md` хранит фактические маппинги.

## Последствия

Положительные:

- Новый паттерн можно создать без дополнительных устных пояснений.
- Библиотека строится по когнитивным операциям, а не по случайным prompt-файлам.
- Prompt-файлы можно развивать независимо от паттернов, сохраняя единый реестр
  связей.
- `prompt_template` остаётся переносимым между LLM и не закрепляет локальные
  особенности провайдера.
- ADR можно передать в Хаб как локальную рекомендацию без копирования private data:
  https://github.com/G-Ivan-A/hybrid-Intelligence-lab

Риски и ограничения:

- Каталог `patterns/` пока пуст. Таблицы содержат planned pattern slug-и, которые
  должны создаваться отдельными issue и PR.
- Первые реальные паттерны потребуют обновления `docs/ba-processes/00-index.md`,
  иначе связь процесс <-> паттерн <-> prompt останется декларативной.
- Если prompt-specific требования начнут попадать в `prompt_template`, паттерны
  быстро станут зависимыми от модели. Это проверяется review и quality gates.

Что не делаем в рамках issue #64:

- Не создаём реальные паттерны в `patterns/[operation-name]/`.
- Не создаём новые prompt-файлы.
- Не меняем содержимое существующих prompt-файлов.
- Не передаём стандарт в Хаб. Передача в
  https://github.com/G-Ivan-A/hybrid-Intelligence-lab является отдельной follow-up
  задачей.

## Альтернативы

### Оставить только `patterns/README.md`

Отклонено. README хорош для навигации, но не хранит полный контекст решения,
международную практику, versioning и последствия. Новые contributors не увидят,
почему паттерны отделены от промптов.

### Хранить паттерны как отдельные markdown-файлы в `patterns/`

Отклонено для целевого стандарта. Один файл проще на старте, но плохо
масштабируется: few-shot examples, related artifacts и evidence начинают
перегружать основной текст. Directory-first layout оставляет паттерн малым и даёт
место для примеров без создания новых верхнеуровневых каталогов.

### Дублировать маппинг в frontmatter паттерна и промпта

Отклонено. Дублирование создаёт drift: один паттерн может иметь несколько
реализаций, prompt может быть archived, а процесс может получить новый
рекомендуемый prompt. Единый реестр `docs/ba-processes/00-index.md` делает review
проще и согласован с `standards/prompt-standard.md`.

### Делать отдельный паттерн под каждую LLM

Отклонено. Это смешивает аналитическую практику и исполняемую реализацию. Если
нужна специфичная LLM-реализация, меняется prompt, а не паттерн.

## Self-test

Локальная проверка этого ADR:

```bash
python3 experiments/validate_issue_64_pattern_adr.py
```

Проверка подтверждает наличие ADR, 8 обязательных полей, 13 операций
таксономии, 9 процессов БА, LLM-агностичности, versioning и ссылок на ключевые
артефакты.

## Связанные артефакты

- Issue #64: https://github.com/G-Ivan-A/mango_ba_prompts/issues/64
- PR #57: https://github.com/G-Ivan-A/mango_ba_prompts/pull/57
- PR #59: https://github.com/G-Ivan-A/mango_ba_prompts/pull/59
- PR #60: https://github.com/G-Ivan-A/mango_ba_prompts/pull/60
- PR #69: https://github.com/G-Ivan-A/mango_ba_prompts/pull/69
- Issue #63: https://github.com/G-Ivan-A/mango_ba_prompts/issues/63
- Issue #61: https://github.com/G-Ivan-A/mango_ba_prompts/issues/61
- Хаб `hybrid-Intelligence-lab`: https://github.com/G-Ivan-A/hybrid-Intelligence-lab
- Репозиторий `clarify-engine-ai`: https://github.com/G-Ivan-A/clarify-engine-ai
- Репозиторий `open-ai.ru`: https://github.com/G-Ivan-A/open-ai.ru
- Текущий репозиторий `mango_ba_prompts`: https://github.com/G-Ivan-A/mango_ba_prompts
- `docs/adr/001-prompt-standard.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md
- `patterns/README.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md
- `standards/pattern-standard.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/pattern-standard.md
- `standards/prompt-standard.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md
- `docs/taxonomy.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md
- `docs/ba-processes/00-index.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md
- `docs/ba-ecosystem.md`: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md
- GoF design patterns: https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610
- Christopher Alexander pattern language: https://arl.human.cornell.edu/linked%20docs/Alexander_A_Pattern_Language.pdf
- Prompt Pattern Catalog: https://arxiv.org/abs/2302.11382
