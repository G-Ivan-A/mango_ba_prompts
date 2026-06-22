---
status: draft
version: 0.1
updated: 2026-06-22
ai-generated: true
type: rfc
scope: taxonomy-extension-mechanism
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/187"
based_on:
  - "docs/analysis/taxonomy-convergence-test.md"
  - "docs/analysis/mango-taxonomy-convergence-test.md"
  - "docs/analysis/rfc-industry-taxonomy-improvement.md"
  - "docs/analysis/rfc-mango-taxonomy-improvement.md"
  - "standards/industry-taxonomy-standard.md"
  - "standards/mango-taxonomy-standard.md"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
related_rfc:
  - "docs/analysis/rfc-industry-taxonomy-improvement.md"
  - "docs/analysis/rfc-mango-taxonomy-improvement.md"
target_artifacts:
  - "docs/analysis/README.md"
  - "standards/taxonomy-extension-contract.md (proposed, not created yet)"
  - "scripts/validate_taxonomy_extension.py (proposed, not created yet)"
---

# RFC: системный механизм расширения таксономий (Industry + Mango)

> Это RFC для human review, а **не** реализация. До явного согласования
> фаундером (Иваном) не создаются новые документы (контракт расширения,
> автогенератор, обновлённый `docs/analysis/README.md`), не меняются
> `standards/industry-taxonomy-standard.md`, `standards/mango-taxonomy-standard.md`,
> Industry/Mango registries, валидаторы, ADR-011 или ADR-012. RFC только
> предлагает механизм и просит approval (см. §11).

## 1. Зачем этот RFC

Тесты на сходимость показали не отдельные дефекты, а **системную** проблему:
таксономии не успевают за продуктом. Текущий ответ — отдельный RFC на каждый
пробел — не масштабируется. Этот RFC предлагает **механизм**: какие уровни
таксономии можно расширять тактически (быстро, по правилам), а какие требуют
стратегического RFC и согласования, и как этот механизм по-разному работает для
Industry и Mango из-за разницы в источниках данных.

RFC сознательно следует прецеденту PR #179 (`rfc-industry-taxonomy-improvement.md`)
и PR #181 (`rfc-mango-taxonomy-improvement.md`): на стадии RFC PR содержит **только
сам RFC-документ**, реализация артефактов идёт отдельной веткой после approval.

## 2. Входные факты

### 2.1 Industry test на сходимость (PR #175)

Источник: `docs/analysis/taxonomy-convergence-test.md`, скоринг
`experiments/issue-174/score_convergence.py`.

| Метрика | Результат |
| --- | --- |
| Domain | 24/25 = 96% |
| Capability | 19/25 = 76% |
| Feature | 6/10 = 60% |
| Function | 1/4 = 25% |
| function_type | 21/25 = 84% |
| Full path | 17/25 = 68% |

Из разбора (см. `rfc-industry-taxonomy-improvement.md`, §3.2) **три** расхождения —
это «пробелы покрытия»: в реестре нет нужного canonical node.

| Кейс | Чего нет в реестре |
| --- | --- |
| #4 `Добавить номер в чёрный список` | number-filtering / blacklist-whitelist |
| #8 `Перевести вызов с консультацией` | active call transfer / consultation transfer |
| #18 `Проставить теги разговору` | conversation tagging под speech analytics |

Характерно: все три пробела — на уровнях **Feature/Function** (тактические), а не
на Domain/Capability.

### 2.2 Mango test на сходимость (PR #177)

Источник: `docs/analysis/mango-taxonomy-convergence-test.md`.

| Метрика | Результат |
| --- | --- |
| Exact full path | 10/27 = 37% |
| Prefix match | 17/27 = 63% |
| Domain | 22/27 = 81% |
| Capability | 18/27 = 67% |

Четыре корневые причины расхождений (§ «Причины» того же отчёта):

| Причина | Суть | Чей дефект |
| --- | --- | --- |
| A | дублирующиеся id-узлы в Industry Taxonomy | Industry registry |
| B | граница «CPaaS/API/UC ↔ digital-channels» без правила | оба стандарта |
| C | гранулярность capability: roll-up vs специфичный sibling | стандарт + реестр |
| D | реестр Mango недомаппливает глубину против §7.3 | Mango registry |

Причины A и D — это, по сути, **пробелы/недоведённость реестров**, то есть тот же
класс проблемы, что и в Industry: на уровне Feature/Function реестр отстаёт от
реальности продукта.

### 2.3 Вывод из фактов

Подавляющая часть «пробелов покрытия» из обоих тестов — на уровнях **Feature и
Function**. Стратегические уровни (Domain, Capability) расходятся гораздо реже
(Domain 96%/81%) и почти всегда из-за правил выбора, а не из-за отсутствия узла.
Это и есть эмпирическое основание для разделения «что автоматизировать, что
согласовывать».

## 3. Классификация уровней по автоматизируемости

Стандарты определяют четыре уровня `Domain -> Capability -> Feature -> Function`
(`standards/industry-taxonomy-standard.md`, §2.3–2.6). Предлагается разделить их
на два класса.

### 3.1 Стратегические уровни (RFC-gated): Domain, Capability

**Почему RFC.** Domain — «верхняя отраслевая область», Capability — «способность
продукта», у обоих по стандарту устойчивые границы, ownership и роль в верхне-
уровневой аналитике (industry-standard §2.3–2.4). Изменение здесь сдвигает каркас
всей таксономии и ломает сопоставимость аналитики. В обоих тестах эти уровни
почти не дают «пробелов покрытия» — значит, частые автоматические правки им и не
нужны.

**Правило.** Новый Domain или Capability, переименование/слияние/удаление
существующего, изменение границы между двумя Capability — **ТОЛЬКО через RFC** с
явным approval фаундера. Это совместимо с уже существующей практикой
(`rfc-industry-taxonomy-improvement.md`, `rfc-mango-taxonomy-improvement.md`).

### 3.2 Тактические уровни (контролируемая автоматизация): Feature, Function

**Почему можно автоматизировать.** Feature — «конкретная проверяемая возможность
внутри Capability», Function — «минимальная проверяемая единица поведения»
(industry-standard §2.5–2.6). Они листовые, локальные, не двигают каркас и именно
здесь возникает поток пробелов. Добавление листа под **существующим** одобренным
Capability — низкорисковая операция.

**Правило (контролируемая автоматизация, не «свободная»).** Новый Feature/Function
можно добавлять без отдельного RFC при выполнении **всех** условий-ворот:

1. родительский Capability уже canonical и approved (никаких новых
   Domain/Capability «по пути»);
2. узел имеет валидный `id`, `level`, `definition`, parent reference и **source
   evidence** в соответствии с разделом источников (см. §4);
3. узел проходит автоматический валидатор расширения (см. §6): нет дубля active
   `id` без `homonym_allowed`, нет ambiguous alias, схема соблюдена;
4. добавление идёт через `lifecycle_status: active` для нового узла и через
   `deprecated` + `replacement` для замен — **без hard-удаления** (как в текущих
   RFC);
5. изменение фиксируется в registry changelog / PR с ссылкой на источник.

Если хотя бы одно условие не выполнено (например, для узла нет canonical родителя,
или источник не подтверждает факт) — операция **эскалируется до RFC**
(fail-closed, в духе CONTRIBUTING «что не описано — не выполняется без human
review»).

### 3.3 Сводная матрица

| Операция | Domain | Capability | Feature | Function |
| --- | --- | --- | --- | --- |
| Добавить узел | RFC | RFC | авто\* | авто\* |
| Переименовать/слить | RFC | RFC | RFC | авто\* (с deprecate+replacement) |
| Deprecate узел | RFC | RFC | авто\* | авто\* |
| Hard-удалить | запрещено | запрещено | запрещено | запрещено |
| Изменить границу между узлами | RFC | RFC | RFC | RFC |

\* «авто» = контролируемая автоматизация при всех воротах §3.2; иначе эскалация в
RFC.

## 4. Ключевое различие: источники данных Industry vs Mango

Это центральное требование issue #187: один и тот же механизм, но **разные
контракты источников**.

### 4.1 Industry Taxonomy — открытый исследовательский источник

Допустимые источники для расширения Feature/Function:

- результаты исследований (анализ рынка, конкурентов);
- тендерные ТЗ (внешние);
- документация (различная);
- интервью с экспертами;
- отраслевые стандарты.

Характер: открытый, может включать гипотезы. Но даже здесь **каждый** новый узел
ОБЯЗАН нести `evidence_refs[]` (repo path или URL) — гипотеза без следа источника
не проходит ворота §3.2.2.

### 4.2 Mango Taxonomy — закрытый фактологический источник

Допустимые источники — **ТОЛЬКО** официальные:

- официальная документация Mango Office (<https://www.mango-office.ru/>);
- официальные руководства пользователя;
- официальные описания продуктов.

Запрещено расширять Mango Taxonomy на основе исследований, интервью, гипотез,
конкурентного анализа. Это согласуется с действующим Mango-стандартом, который уже
требует `source refs на официальный сайт/каталог/approved public source`
(`standards/mango-taxonomy-standard.md`, §1.2/§1.3 и пример с
`https://www.mango-office.ru/products/`).

### 4.3 Контракт источника как ворота автоматизации

| Параметр | Industry | Mango |
| --- | --- | --- |
| Тип источника | research / ТЗ / docs / интервью / стандарты | только официальные Mango Office |
| Гипотезы допустимы | да (с evidence_refs) | нет |
| Обязателен `evidence_refs[]` | да | да, и домен источника ДОЛЖЕН быть `mango-office.ru` |
| Что при отсутствии источника | эскалация в RFC | узел не добавляется (fail-closed) |

Валидатор расширения (§6) проверяет домен источника для Mango-узлов: ссылка вне
`mango-office.ru` → отказ.

## 5. Предлагаемые артефакты (создаются ТОЛЬКО после approval)

> На стадии RFC ничего из перечисленного не создаётся. Это план артефактов для
> Этапа 4.

### A1 — Контракт расширения таксономии

Документ (например, `standards/taxonomy-extension-contract.md`) с нормативными
(RFC 2119) правилами §3–§4: матрица уровней, ворота автоматизации, контракт
источников Industry vs Mango, fail-closed-эскалация. Это **процессный контракт**,
он не меняет сами Industry/Mango Taxonomy Standard — ссылается на них.

### A2 — Механизм автогенерации тактических уровней

Скрипт/процедура, которая из подтверждённого источника формирует draft
Feature/Function-узлов (id, level, parent, definition, evidence_refs), прогоняет
их через валидатор (§6) и готовит PR. Стратегические узлы скрипт **не** создаёт —
при необходимости нового Domain/Capability он останавливается и требует RFC.

### A3 — Валидатор расширения

`scripts/validate_taxonomy_extension.py` (см. §6) — автоматические ворота.

### A4 — Обновление `docs/analysis/README.md`

Таблица RFC в драфте (приоритизация согласования) + сортировка документов по дате.
Предлагаемая структура — в §7. Сейчас файла `docs/analysis/README.md` нет; он
создаётся на Этапе 4 после approval.

## 6. Контроль качества: валидатор расширения

Предлагаемые проверки для `scripts/validate_taxonomy_extension.py` (переиспользуют
логику существующих валидаторов, не дублируя её):

1. **Уровень.** Новый узел только `level ∈ {feature, function}` для авто-режима;
   `domain`/`capability` → ошибка «требуется RFC».
2. **Canonical parent.** parent существует, approved, не deprecated.
3. **Уникальность id.** нет другого active узла с тем же `id` без
   `homonym_allowed: true` (как в `validate_issue_156_*` и
   `rfc-industry-taxonomy-improvement.md` R1).
4. **Alias safety.** alias/source term не резолвится в несколько canonical nodes
   (как в `validate_issue_168_*`).
5. **Source contract.** `evidence_refs[]` не пуст; для scope `mango` каждый ref —
   из `mango-office.ru`.
6. **No hard-delete.** замены идут через `deprecated` + `replacement`.
7. **Schema.** узел валиден против соответствующей `*.schema.json`.

Любой провал → узел не попадает в реестр автоматически, операция эскалируется в
RFC. Это и есть «контролируемое качество» из цели issue.

## 7. Предлагаемая структура `docs/analysis/README.md`

> Создаётся на Этапе 4. Здесь — только предлагаемый вид.

### 7.1 Таблица RFC в драфте (приоритизация согласования)

| # | RFC | Приоритет | Статус | Дата создания | Связанная проблема |
|---|-----|-----------|--------|---------------|-------------------|
| 1 | rfc-industry-taxonomy-improvement.md | P1 | на согласовании | 2026-06-22 | Industry test 68% |
| 2 | rfc-mango-taxonomy-improvement.md | P1 | на согласовании | 2026-06-22 | Mango test 37% |
| 3 | rfc-taxonomy-extension-mechanism.md | P1 | на согласовании | 2026-06-22 | Системное расширение |

Цель — нативно видеть, какие RFC согласовывать первыми.

### 7.2 Сортировка документов по дате

Остальные документы в README сортируются **по убыванию даты `updated`** (новые
сверху), чтобы самые актуальные были видны первыми. Дата берётся из frontmatter
каждого документа.

## 8. Совместимость с ADR и стандартами

| Артефакт | Влияние | Обоснование непротиворечивости |
| --- | --- | --- |
| ADR-011 (Industry) | нет изменений | механизм работает внутри иерархии Domain→Capability→Feature→Function, не меняет каркас |
| ADR-012 (Mango) | нет изменений | контракт источников лишь усиливает требование официальных источников, уже заложенное в ADR-012/стандарте |
| Industry Taxonomy Standard | нет изменений в этом issue | контракт расширения — отдельный процессный документ, ссылается на стандарт |
| Mango Taxonomy Standard | нет изменений в этом issue | то же; правило «только официальные источники» совпадает со стандартом |
| Структура каталогов | нет изменений | новые артефакты кладутся в существующие `standards/`, `scripts/`, `docs/analysis/` |

Механизм **не противоречит** уже идущим точечным RFC (#179, #181): он их обобщает.
Стратегические правки из тех RFC остаются RFC-gated; тактические пробелы (number-
filtering, conversation-tagging, depth-mappings) после approval можно закрывать уже
автоматическим путём.

## 9. Риски и минимизация

| Риск | Минимизация |
| --- | --- |
| Автогенерация замусоривает реестр слабыми узлами | жёсткие ворота §3.2 + валидатор §6; fail-closed: сомнение → RFC |
| Mango расширяется по неофициальному источнику | валидатор проверяет домен `mango-office.ru`; иначе отказ |
| «Расползание» автоматизации на Domain/Capability | валидатор запрещает авто для level ∈ {domain, capability} |
| Дубли/ambiguous alias (причина A тестов) | переиспользование проверок `validate_issue_156/168_*` |
| Hard-удаление ломает историю | только `deprecated` + `replacement`, как в текущих RFC |
| Механизм воспринят как обход human review | стратегический контроль сохранён; авто — лишь для листьев под approved parent |
| README устаревает | сортировка по `updated`-frontmatter автоматизируема скриптом |

## 10. План реализации после approval

1. Завести ветку от актуального `upstream/main`.
2. Создать `standards/taxonomy-extension-contract.md` (A1) с правилами §3–§4.
3. Реализовать `scripts/validate_taxonomy_extension.py` (A3) с проверками §6,
   переиспользуя существующие валидаторы.
4. Реализовать механизм автогенерации тактических узлов (A2).
5. Создать/обновить `docs/analysis/README.md` (A4): таблица RFC + сортировка.
6. Прогнать локальные проверки:

```bash
python3 scripts/validate_issue_152_industry_taxonomy_standard.py
python3 scripts/validate_issue_156_industry_taxonomy_registry.py
python3 scripts/validate_issue_168_industry_reference_integrity.py
python3 scripts/validate_issue_170_mango_registry.py
python3 scripts/validate_taxonomy_extension.py   # новый
make kb-validate
```

7. Обновить `CHANGELOG.md` записью issue #187.
8. Прогнать GitHub Pages / kb workflows, убедиться, что CI зелёный.

## 11. Запрос на согласование (Approval request)

Прошу фаундера явно подтвердить:

1. Принимается ли разделение уровней: **Domain/Capability — RFC-gated**,
   **Feature/Function — контролируемая автоматизация** (§3)?
2. Принимается ли контракт источников: **Industry — research/ТЗ/docs/интервью с
   `evidence_refs`**, **Mango — ТОЛЬКО `mango-office.ru`** (§4)?
3. Согласны ли ворота автоматизации и fail-closed-эскалация в RFC (§3.2)?
4. Утверждается ли набор артефактов A1–A4 (§5) как scope реализации в PR #189?
5. Утверждается ли предлагаемый вид `docs/analysis/README.md` — таблица RFC в
   драфте + сортировка по дате (§7)?

До ответа на эти вопросы реализация (создание контракта, автогенератора,
валидатора и README) остаётся **заблокированной**. Этот PR содержит только RFC.
