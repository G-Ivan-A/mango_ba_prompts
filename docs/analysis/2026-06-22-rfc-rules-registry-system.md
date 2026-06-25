---
status: proposed
version: 0.1
updated: 2026-06-22
issue: 186
ai-generated: true
---

# RFC: Rules Registry System для управления правилами создания артефактов

## 1. Статус RFC

Этот документ является предложением по issue
[#186](https://github.com/G-Ivan-A/mango_ba_prompts/issues/186), а не
внедрением новой системы правил.

До явного решения основателя:

- не создаются machine-readable реестры правил;
- не изменяются активные промпты;
- не изменяются стандарты и process maps как обязательные контракты;
- предложенные ниже поля, lifecycle и AI-agent contract не считаются
  действующими правилами проекта.

Текущий PR закрывает только Stage 1-2 из issue #186: анализ существующих
правил и RFC-предложение. Stage 4 должен начаться только после явного
founder approval.

## 2. Задача

В проекте уже есть много правил, влияющих на создание артефактов: hard rules в
промптах, RFC-предложения, стандарты, ADR, process maps, pattern contracts,
AI governance и выводы из convergence tests. Эти правила помогают, но сейчас
они распределены по разным типам документов и не имеют единого машинного
контракта:

- AI-агенту трудно понять, какие правила активны именно для текущего процесса,
  операции и типа артефакта;
- предлагаемые правила в RFC могут выглядеть рядом с действующими правилами,
  хотя ещё не меняют поведение;
- отладка качества артефакта часто требует вручную искать, какое правило было
  применено, пропущено или конфликтовало с другим правилом;
- при эволюции промптов нет единого места, где видно lifecycle правила:
  proposal, approval, activation, deprecation, replacement.

Цель RFC: предложить системный механизм Rules Registry, который переводит
правила создания артефактов из scattered knowledge в управляемую систему с
traceability, lifecycle и process bindings.

## 3. Что было проанализировано

### 3.1. RFC с атомарными prompt-правилами

Файл
[`governance/rfc/bcreq-ft-scope-formation-rules-proposal.md`](../../governance/rfc/bcreq-ft-scope-formation-rules-proposal.md)
уже задаёт хороший локальный формат атомарных правил:

- `RFC-184-S1`: ФТ описывает доработку, а не текущую функциональность;
- `RFC-184-S2`: один пользовательский запрос не является достаточным
  основанием менять функциональность, уже закрытую текущей или альтернативной
  реализацией.

Сильные стороны этого подхода:

- у каждого правила есть ID;
- указаны prompt impact, rationale, риск, тип изменения и приоритет;
- явно сказано, что RFC не меняет промпты до отдельного решения.

Ограничение: правила живут в Markdown RFC и в
[`governance/rfc-register.md`](../../governance/rfc-register.md), но не в
машиночитаемом реестре, который агент может использовать как runtime contract.

### 3.2. Prompt hard rules

Промпты
[`prompts/fr-documentation-oneshot.md`](../../prompts/fr-documentation-oneshot.md),
[`prompts/fr-documentation-stepwise.md`](../../prompts/fr-documentation-stepwise.md),
[`prompts/glossary-context-understanding-oneshot.md`](../../prompts/glossary-context-understanding-oneshot.md)
и
[`prompts/glossary-context-understanding-stepwise.md`](../../prompts/glossary-context-understanding-stepwise.md)
содержат действующие правила генерации артефактов:

- иерархия ФТ `4.x / 4.x.1 / 4.x.1.1`;
- бизнес-уровень без API/DB/UI/алгоритмов;
- нормализация стиля;
- защита scope;
- запрет добавлять функциональность вне переданного контекста;
- разделение глоссария и бизнес-контекста.

Ограничение: эти правила встроены в текст промпта. У них нет стабильных ID,
статуса, владельца, lifecycle, связей с RFC и отдельной отладочной записи
применения.

### 3.3. Process maps

[`docs/ba-processes/00-index.md`](../ba-processes/00-index.md) уже является
центральным маппингом process -> operations -> patterns -> prompts. Например,
для процесса формирования ФТ/ТЗ он связывает операции с glossary/context и
FR-generation prompts.

Сильная сторона: это естественная точка, где агент узнаёт, какой процесс и
какие промпты применимы.

Ограничение: в process map пока нет формальной связи process/operation ->
rule set. Агент видит prompts, но не видит отдельный набор обязательных правил
для типа артефакта.

### 3.4. Standards, ADR и pattern contracts

[`standards/bcreq-process-standard.md`](../../standards/bcreq-process-standard.md)
и
[`docs/adr/009-bcreq-formation-process.md`](../adr/009-bcreq-formation-process.md)
содержат правила B1-B8 для BCREQ-процесса: фрактальность, шесть подпроцессов,
human gates, traceability и правила обработки incomplete subprocesses.

[`standards/prompt-standard.md`](../../standards/prompt-standard.md) описывает
контракт prompt assets, lifecycle и frontmatter.

[`standards/pattern-standard.md`](../../standards/pattern-standard.md) требует
для паттернов секции `quality_gates` и `governance_rules`.

Сильная сторона: стандарты уже задают обязательные контракты и частично
структурированные правила.

Ограничение: правила распределены по стандартам и ADR, но нет единого
cross-standard registry, где видно, какие правила применимы к конкретному
артефакту и какая версия правила активна.

### 3.5. Convergence reports

Отчёты
[`docs/analysis/2026-06-22-taxonomy-convergence-test.md`](2026-06-22-taxonomy-convergence-test.md) и
[`docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md`](2026-06-22-mango-taxonomy-convergence-test.md)
показывают повторяемую проблему: AI-агент не галлюцинирует, но расходится в
классификации из-за missing boundary rules, неоднозначных узлов, разной
гранулярности и неполного decision tree.

Это важный сигнал для Rules Registry: правила должны не только описывать
идеальное поведение, но и поддерживать отладку:

- какое правило должно было снять неоднозначность;
- какое правило отсутствовало;
- какой конфликт правил повлиял на результат;
- какая правка правила улучшила сходимость.

### 3.6. Governance and RFC process

[`AI_GOVERNANCE.md`](../../AI_GOVERNANCE.md),
[`AI_QUICK_RULES.md`](../../AI_QUICK_RULES.md),
[`CONTRIBUTING.md`](../../CONTRIBUTING.md) и
[`governance/rfc-process.md`](../../governance/rfc-process.md) задают важные
мета-правила:

- агент читает issue, комментарии и релевантные файлы до изменений;
- человек сохраняет право финального решения;
- RFC является предложением, а не правилом;
- молчание не повышает статус proposal до accepted/implemented;
- значимые изменения фиксируются в `CHANGELOG.md`.

Rules Registry должен наследовать эти ограничения. Иначе registry сам станет
обходом governance.

## 4. Вывод Stage 1

В проекте уже есть proto-registry из нескольких слоёв:

| Слой | Где живёт сейчас | Проблема |
| --- | --- | --- |
| Governance hard rules | `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md` | Не связаны машинно с artifact generation rules |
| RFC rule proposals | `governance/rfc/*.md`, `governance/rfc-register.md` | Есть ID и rationale, но нет runtime registry |
| Prompt hard rules | `prompts/*.md` | Действуют, но не имеют отдельного ID/lifecycle |
| Process bindings | `docs/ba-processes/00-index.md` | Есть process -> prompt, нет process -> rule set |
| Standards/ADR rules | `standards/`, `docs/adr/` | Нормативны, но не сведены в общий rule graph |
| Pattern checks | `patterns/*/README.md` + pattern standard | Локальны для паттерна, не атомизированы |
| Test-derived rules | `docs/analysis/*convergence-test.md` | Выявляют gaps, но не создают управляемое rule backlog |

Следовательно, проблема issue #186 реальна: правила существуют, но управление
ими не является отдельной системой.

## 5. Предлагаемое решение

Создать после approval систему Rules Registry с четырьмя слоями:

1. **Atomic rules registry**: machine-readable источник правил с ID, статусом,
   версией, областью применения, текстом правила, rationale и validation.
2. **Process/operation bindings**: явная связь process/operation/artifact_type
   с набором применимых правил.
3. **AI-agent contract**: порядок загрузки, применения, логирования и
   разрешения конфликтов правил.
4. **Lifecycle and debug loop**: proposal -> approval -> active rule -> usage
   evidence -> update/deprecate/replacement.

## 6. Atomic Rule Model

Предлагаемый минимальный контракт правила:

| Поле | Назначение |
| --- | --- |
| `id` | Стабильный человеко- и машинно-читаемый ID правила |
| `title` | Короткое название |
| `status` | `proposed`, `accepted`, `active`, `deprecated`, `rejected` |
| `version` | Версия правила |
| `owner` | Роль или область ответственности |
| `source` | Issue/RFC/ADR/standard/prompt/test, откуда появилось правило |
| `scope` | Процессы, операции, artifact types, prompts, standards |
| `severity` | `hard`, `default`, `advisory` |
| `priority` | Порядок применения внутри scope |
| `rule` | Краткая формулировка правила |
| `must` | Что агент обязан сделать |
| `must_not` | Что агенту запрещено делать |
| `rationale` | Почему правило нужно |
| `risks` | Что может пойти не так |
| `validation` | Проверяемые критерии применения |
| `debug` | Что логировать при применении/пропуске/конфликте |
| `relations` | `depends_on`, `conflicts_with`, `supersedes`, `superseded_by` |
| `approval` | Кто и когда перевёл правило в активный статус |

Пример ниже является иллюстрацией RFC, а не предлагаемым к коммиту registry
entry:

```yaml
id: RFC-184-S1
title: "ФТ описывает доработку, а не текущую функциональность"
status: proposed
version: "0.1"
owner: "BA governance"
source:
  issue: 184
  rfc: "governance/rfc/bcreq-ft-scope-formation-rules-proposal.md"
scope:
  processes:
    - bcreq-formation
  artifact_types:
    - functional-requirements
  prompts:
    - prompts/fr-documentation-stepwise.md
    - prompts/fr-documentation-oneshot.md
severity: hard
priority: 100
rule: "ФТ должен описывать целевую доработку, а не пересказывать текущую функциональность."
must:
  - "Отделять целевое изменение от As-Is контекста."
  - "Оставлять текущие настройки только как зависимости или ограничения."
must_not:
  - "Добавлять требования к уже существующей функциональности без явного изменения."
validation:
  - "Каждый пункт ФТ связан с изменением, зависимостью или ограничением."
debug:
  log_when:
    - applied
    - skipped
    - conflict
```

## 7. Registry Files: proposal

После approval возможна такая структура:

```text
governance/rules/
  README.md
  schema.yaml
  registry.yaml
  process-bindings.yaml
  lifecycle.md
  ai-agent-contract.md
```

Альтернатива: хранить machine-readable registry в `kb/` как knowledge asset,
а governance contract оставить в `governance/rules/`. Этот RFC предлагает
использовать `governance/rules/`, потому что речь идёт о правилах создания
артефактов и поведении AI-агентов, а не о доменной справочной базе.

Важно: этот PR не создаёт указанную структуру. Она приведена как design target
для Stage 4.

## 8. Process and Operation Bindings

Rules Registry должен отвечать на вопрос: какие правила действуют для текущей
работы агента?

Предлагаемый binding context:

```yaml
process_id: bcreq-formation
operation_id: fr-generation
artifact_type: functional-requirements
prompt_ids:
  - fr-documentation-stepwise
required_rules:
  - RFC-184-S1
  - RFC-184-S2
optional_rules: []
debug_required: true
```

Binding может быть отдельным файлом `process-bindings.yaml` или расширением
существующего `docs/ba-processes/00-index.md`. RFC предлагает начать с
отдельного machine-readable файла, чтобы не ломать текущий Markdown map и дать
валидатору простой объект проверки.

## 9. AI-Agent Contract

После внедрения registry AI-агент должен работать по такому контракту:

1. Определить context: issue, process, operation, artifact_type, prompt/pattern.
2. Загрузить process binding для этого context.
3. Загрузить только правила со статусом `active` или явно разрешённым статусом
   для текущего review mode.
4. Применить правила в порядке `severity -> priority -> specificity`.
5. Перед созданием артефакта проверить `must` и `must_not`.
6. После создания артефакта выполнить validation checklist.
7. Зафиксировать debug summary: applied rules, skipped rules, conflicts,
   uncertain rules, source evidence.
8. При конфликте hard rules не выбирать молча, а остановиться и запросить
   human decision или создать RFC/issue.
9. Не применять proposed/rejected/deprecated rules как обязательные.

Debug summary не должен засорять каждый пользовательский артефакт. Он должен
жить в run logs, PR description или отдельном evidence artifact, если процесс
требует traceability.

## 10. Conflict Resolution

Предлагаемый порядок приоритета:

1. Hard restrictions из `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`,
   `CONTRIBUTING.md` и явных user instructions.
2. Accepted/active standards и ADR.
3. Active rules из Rules Registry.
4. Process/operation bindings.
5. Prompt-local instructions.
6. Proposed RFC rules как advisory context, если founder явно не попросил
   тестировать их в экспериментальном режиме.

Если правило из нижнего слоя конфликтует с верхним, применяется верхний слой.
Если конфликт остаётся внутри одного слоя, агент должен остановиться и
запросить human review.

## 11. Lifecycle

Предлагаемый lifecycle правила:

1. **Signal**: проблема найдена в issue, PR review, run feedback, convergence
   test, CI, production-like artifact review.
2. **Rule proposal**: создаётся RFC или секция RFC с атомарным правилом.
3. **Review**: основатель/ревьюер принимает, отклоняет или просит переработать.
4. **Activation**: после approval правило попадает в registry со статусом
   `active` и ссылкой на решение.
5. **Binding**: правило связывается с process/operation/artifact_type.
6. **Implementation**: если нужно, обновляются prompts, standards, validators.
7. **Evidence**: последующие runs фиксируют применение правила.
8. **Evolution**: правило меняется только через новую proposal/review запись.
9. **Deprecation**: устаревшее правило не удаляется сразу, а получает
   `deprecated` и ссылку на replacement.

Этот lifecycle совместим с текущим
[`governance/rfc-process.md`](../../governance/rfc-process.md): RFC не становится
правилом без явного human decision.

## 12. Seed Rules for Stage 4

После approval можно начать с малого seed set:

| Источник | Кандидаты |
| --- | --- |
| Issue #184 RFC | `RFC-184-S1`, `RFC-184-S2` |
| BCREQ standard/ADR | `B1`-`B8` как rules для bcreq process |
| Prompt standard | prompt frontmatter/lifecycle rules |
| Pattern standard | required sections, `quality_gates`, `governance_rules` |
| Taxonomy convergence RFCs | boundary/disambiguation rules после отдельного approval |

Важно: proposed RFC rules не должны автоматически становиться active. При
миграции seed set нужно сохранить исходные статусы и approval evidence.

## 13. Validation

Stage 4 должен добавить validator, который проверяет:

- registry соответствует schema;
- ID уникальны;
- `source` ссылки существуют;
- `status` входит в допустимый enum;
- `process-bindings` ссылаются только на существующие rules;
- active bindings не используют rejected/deprecated rules;
- prompts/standards, указанные в scope, существуют;
- lifecycle transitions не обходят approval evidence;
- proposed rules не попадают в active runtime set.

Для текущего RFC validator не добавляется, потому что это уже было бы
реализацией Stage 4.

## 14. Риски и ограничения

| Риск | Митигация |
| --- | --- |
| Registry продублирует RFC register | RFC register остаётся списком решений; registry хранит runtime rules |
| Система станет слишком тяжёлой | Начать с малого seed set и одной process binding области |
| Агент начнёт применять proposed rules | Строгий status filter: обязательны только active rules |
| Правила устареют | Validation + lifecycle + deprecation вместо silent edits |
| Конфликты правил будут скрыты | Debug summary и hard stop при unresolved hard conflict |
| Markdown и YAML начнут расходиться | YAML хранит runtime contract, Markdown хранит rationale и human-readable RFC |
| Scope rules станут слишком абстрактными | Привязывать правила к process/operation/artifact_type и validation checklist |

## 15. Stage 4 Implementation Plan after approval

Если основатель одобрит RFC, следующая итерация может быть такой:

1. Создать `governance/rules/schema.yaml`.
2. Создать `governance/rules/registry.yaml` с минимальным seed set и сохранёнными
   статусами.
3. Создать `governance/rules/process-bindings.yaml` для bcreq/fr-generation.
4. Создать `governance/rules/ai-agent-contract.md`.
5. Создать `governance/rules/lifecycle.md`.
6. Добавить validator script и подключить его к существующим локальным/CI
   проверкам.
7. Только после этого обновлять prompts/standards, если approval явно включает
   изменение их поведения.
8. Обновить `CHANGELOG.md` и PR description с evidence.

## 16. Вопросы на approval

Для перехода к Stage 4 нужно явное решение по вопросам:

1. Одобряется ли сама идея Rules Registry как отдельного governance слоя?
2. Подтверждается ли путь `governance/rules/` для registry, schema, bindings и
   AI-agent contract?
3. Нужен ли отдельный `process-bindings.yaml`, или binding нужно встроить в
   `docs/ba-processes/00-index.md`?
4. Какие seed rules разрешено мигрировать первыми: только `RFC-184-S1/S2`, или
   также BCREQ `B1`-`B8`, prompt standard и pattern standard?
5. Какие статусы должны получить seed rules при миграции: сохранить текущие
   `proposed`/`accepted`, или явно активировать выбранные правила?
6. Где хранить debug evidence применения правил: в `runs/`, PR description,
   отдельном governance log или комбинации этих вариантов?
7. Продолжать Stage 4 в PR #188 после approval или открыть отдельный follow-up
   PR для реализации?

## 17. Recommendation

Рекомендуется одобрить Rules Registry как отдельный governance/runtime слой, но
начать Stage 4 с минимального объёма:

- `governance/rules/schema.yaml`;
- `governance/rules/registry.yaml`;
- `governance/rules/process-bindings.yaml`;
- `governance/rules/ai-agent-contract.md`;
- validator;
- seed только для BCREQ/FR scope.

Это даст проверяемую пользу на самом проблемном участке, не превращая registry
в большой теоретический стандарт до появления evidence.
