---
status: proposed
version: 0.1
updated: 2026-06-16
ai-generated: true
type: adr
scope: industry-standards
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
related_standard: "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/industry-standards-standard.md"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/98"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/kb-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/GLOSSARY.md"
---

# ADR-008: Стандарт отраслевых стандартов и best practices — терминология, правила применения, верификация источников

> **Статус:** Proposed · **Дата:** 2026-06-16 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97> · **Стандарт-контракт:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/industry-standards-standard.md>

> **Numbering note.** ADR-008 — трёхзначная дорожка стандартов. См.
> [ADR-002](002-pattern-standard.md).

## Контекст

Issue #97 (ФТ-6) требует предложить **стандарт отраслевых стандартов и best
practices**: терминологию, правила применения и **доказательство A/B-тестом
(с/без стандартов)**. Жёсткие ограничения issue: предоставлять **полные URL всех
источников**, **доказывать каждое предложение**, **не использовать выдуманные
источники**.

Эти ограничения не абстрактны. Список «Отраслевые стандарты (полные URL)» в самой
issue #97 содержит **как минимум три проблемных идентификатора** (проверено в
рамках этого ADR):

1. **«ГОСТ 34.602-2015»** — такой редакции не существует (есть -89 и -2020);
2. **ISO/IEC/IEEE 29148:2018** указан как `iso.org/standard/72545.html`, тогда как
   действующий номер записи — **72089**;
3. **ISO/IEC 25010:2023** указан как `iso.org/standard/78405.html`, тогда как
   действующий номер записи — **78176**.

Значит, стандарт обязан включать **правило верификации источника** и
**сверенный реестр**, иначе невыверенные ссылки (даже от Пользователя) попадают в
артефакты. Это согласуется с дисциплиной цитирования [ADR-007](007-kb-standard.md)
и реализует НФТ доказуемости.

> Примечание о роли. Режим `Creative`+`Research` даёт право предлагать решения,
> уточняющие входные данные, при обосновании. Реестр ниже **не отменяет** список
> Пользователя — он применяет правило верификации, которое Пользователь сам
> сделал обязательным, и помечает расхождения как «⚠️ проверить», приводя
> сверенный URL.

## Решение

Вводим контракт
[industry-standards-standard.md](../../standards/industry-standards-standard.md):

### 1. Терминология (выбрана оптимальная)

Опираемся на различия, уже зафиксированные в [глоссарии](../../standards/GLOSSARY.md)
(Standard / Policy / Contract / Practice / Framework / Guideline), и **расширяем**
их для **внешних** источников. Базовое различение — из терминологии ISO/IEC
Directives, Part 2 (нормативные vs информативные положения):

| Термин | Определение | Пример |
| --- | --- | --- |
| **De jure стандарт** | Утверждён органом стандартизации. | ISO/IEC/IEEE 29148, ГОСТ 34.602-2020, ISO/IEC 25010 |
| **De facto стандарт** | Принят отраслью без формального органа. | TM Forum Frameworx/ODA |
| **Best practice** | Рекомендуемый отраслью подход; информативен, не обязателен. | BABOK-техники, Anthropic Prompt Engineering Guide |
| **Framework/методология** | Связная модель понятий и процессов. | BABOK Guide v3, TM Forum ODA |
| **Нормативная ссылка** | Источник, обязательный к применению в контексте. | ГОСТ 34.602-2020 для ТЗ в РФ-контексте |
| **Информативная ссылка** | Источник для справки, не обязателен. | пояснительные руководства |

- **Иерархия приоритета (tier):** явное требование Пользователя → de jure
  стандарт → de facto стандарт → best practice → guideline.

### 2. Правила применения best practices (выбраны оптимальные)

- **И1 (верификация).** Перед ссылкой источник **ДОЛЖЕН** быть проверен на
  существование (документ, редакция/год, полный URL) — чек-лист
  [KB: source-backed-analysis](../../kb/practices/source-backed-analysis.md#чек-лист-проверки-источника).
  Несуществующий — не цитируется (правило C4 [ADR-007](007-kb-standard.md)).
- **И2 (полный URL).** Каждая ссылка — **полным URL** (жёсткое требование issue).
- **И3 (приоритет/конфликт).** При конфликте источников применяется верхний tier
  (§1); решение фиксируется ADR (модель «молчание = согласие»).
- **И4 (применимость/локализация).** ГОСТ — для РФ-контекста ТЗ; ISO/IEEE — для
  международного; best practice — где нет обязательного стандарта.
- **И5 (нормативное vs информативное).** Каждая ссылка помечается как
  нормативная (обязательна) или информативная (справочна).
- **И6 (реестр).** Используется только сверенный реестр §3 контракта; новая
  ссылка добавляется через issue/PR с подтверждённым URL.

### 3. Сверенный реестр (реконсиляция списка issue #97)

Полный реестр с пометками «нормативный/информативный», tier и сверенными URL — в
[industry-standards-standard.md §3](../../standards/industry-standards-standard.md).
Расхождения со списком issue помечены «⚠️ проверить» и сопровождены сверенным URL
(а не молчаливо заменены).

## Доказательная база

- **Терминология нормативное/информативное** — ISO/IEC Directives, Part 2:
  <https://www.iso.org/sites/directives/current/part2/index.xhtml>
- **Качество требований (для A/B)** — ISO/IEC/IEEE 29148:2018:
  <https://www.iso.org/standard/72089.html> (сверено; в issue ошибочно 72545).
- **BABOK Guide v3** (techniques как best practices):
  <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- **Anthropic Prompt Engineering Guide** (best practice для промптов):
  <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
- **A/B-эксперимент (ФТ-6):**
  [`runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md`](../../runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md)
  — формирование/проверка FR с применением стандартов и без.

## Примеры

**A. Нормативная ссылка (РФ-контекст):** структура ТЗ → [ГОСТ 34.602-2020](https://docs.cntd.ru/document/1200181804) (tier: de jure, нормативная).

**B. Best practice (информативная):** структура промпта → [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) (tier: best practice, информативная).

**C. Разрешение конфликта:** если best practice противоречит de jure стандарту в
обязательном контексте — применяется стандарт (И3); исключение фиксируется ADR.

## Self-test

1. **Дано:** ссылка «ГОСТ 34.602-2015». **Ожидаемо:** отклонена И1 (редакции нет),
   предложена -2020. **Acceptance:** реестр §3.
2. **Дано:** best practice vs de jure стандарт в обязательном контексте.
   **Ожидаемо:** применён стандарт (И3). **Acceptance:** §2.
3. **Дано:** FR без применения 29148. **Ожидаемо:** A/B показывает пропуск
   дефектов. **Acceptance:** эксперимент.

Локально: `python3 scripts/validate_issue_97_ontology_standards.py`.

## Последствия

**Положительные:**

- Правило верификации ловит невыверенные ссылки (доказано на самом списке issue) —
  НФТ доказуемости.
- Единая терминология и tier снимают споры о приоритете источников.
- Сверенный реестр — единая точка истины с полными URL.

**Отрицательные / технический долг:**

- Реестр нужно поддерживать при выходе новых редакций стандартов.
- Пометки «⚠️ проверить» по списку issue требуют подтверждения Пользователя
  (намеренно не «исправлены молча»).

## Альтернативы (отклонены)

1. **Брать URL из issue как есть.** Отклонено: содержит несуществующую редакцию и
   неверные номера записей ISO — нарушит «не использовать выдуманные источники».
2. **Молча заменить URL Пользователя.** Отклонено: непрозрачно; вместо этого —
   пометка «⚠️ проверить» + сверенный URL (уважение к роли Пользователя).
3. **Не вводить терминологию, ссылаться свободно.** Отклонено: нарушает ФТ-6 и
   делает приоритеты источников неоднозначными.

## Связанные артефакты

- Issue #97: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97>
- PR #98: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/98>
- Контракт (терминология, правила, реестр): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/industry-standards-standard.md>
- ADR-007 (дисциплина цитирования, правило C4): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/007-kb-standard.md>
- Таксономия (audit-профиль 29148): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- A/B-эксперимент: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md>

### Международные стандарты (полные URL, сверено)

- ISO/IEC Directives, Part 2: <https://www.iso.org/sites/directives/current/part2/index.xhtml>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- TM Forum ODA / Frameworx: <https://www.tmforum.org/oda/>
- Anthropic Prompt Engineering Guide: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
