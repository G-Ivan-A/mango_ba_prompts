---
status: proposed
version: 0.1
updated: 2026-06-16
ai-generated: true
type: adr
scope: prompt-naming
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
related_standard: "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/98"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/007-kb-standard.md"
---

# ADR-006: Стандарт нейминга промптов (подтверждение схемы, запрет перегрузки, KB-промпты)

> **Статус:** Proposed · **Дата:** 2026-06-16 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97> · **Стандарт-контракт:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>

> **Numbering note.** ADR-006 — трёхзначная дорожка стандартов. См.
> [ADR-002](002-pattern-standard.md).

## Контекст

Схема имён промптов `[домен]-[операция]-[режим].md` уже зафиксирована в
[ADR-001](001-prompt-standard.md) и [prompt-standard.md](../../standards/prompt-standard.md).
Issue #97 (ФТ-4) требует:

1. предложить принцип нейминга промптов (Исполнитель выбирает оптимальный);
2. предложить решение для **KB-промптов**;
3. **жёстко: НЕ перегружать наименования промптов** — найти баланс между
   атомарностью и простотой (не плодить избыточные суффиксы при разделении по
   режимам);
4. доказательство — примеры для **всех 24 промптов**.

Жёсткие ограничения issue: **не менять существующие промпты** и **не создавать
новые**. Поэтому ADR-006 не трогает 24 файла, а (а) подтверждает схему,
(б) формализует правило «не перегружать» в проверяемые подправила, (в) описывает,
как KB-промпты вписываются в схему **без новой оси имени**, (г) приводит разбор
всех 24 имён как доказательство.

Дополнительная сложность: домен и операция могут быть многословными
(`technical-details`, `solution-design`), поэтому нужен явный **парс-алгоритм**
имени — его раньше не было.

## Решение

### 1. Схема подтверждена; добавлен парс-алгоритм

Имя = `[домен]-[операция]-[режим].md`. Парсинг — **справа налево**:

1. **режим** = последний сегмент, из множества `{stepwise, oneshot, legacy}`;
2. **операция** = максимальное совпадение предшествующих сегментов с операцией
   из [таксономии §1](../taxonomy.md) в kebab-форме (`solution_design` →
   `solution-design`); операция **МОЖЕТ** быть многословной;
3. **домен** = всё, что осталось слева (1-2 сегмента, kebab-case).

Этот алгоритм детерминированно разбирает и `fr-validation-stepwise`
(домен `fr`, операция `validation`), и `technical-details-solution-design-legacy`
(домен `technical-details`, операция `solution-design`).

### 2. Правило «не перегружать» — проверяемые подправила (жёсткое требование)

- **P1.** Имя **ДОЛЖНО** иметь ровно три логические части: домен, операция,
  режим. Четвёртая ось **НЕ ДОЛЖНА** появляться: запрещены суффиксы вида
  `-kb`, `-rag`, `-v2`, `-simple`, `-new`, `-final`.
- **P2.** Домену **СЛЕДУЕТ** быть ≤2 сегментов; операция — строго из таксономии;
  режим — строго из `{stepwise, oneshot, legacy}`.
- **P3.** Версия — во frontmatter (`version`), **НЕ** в имени файла; зрелость — в
  `status`, **НЕ** в имени.
- **P4.** `title` во frontmatter **НЕ СЛЕДУЕТ** перегружать аббревиатурами (кроме
  общепринятых ФТ, ТЗ, ASR, UC, US, LLM) — действующее правило
  [prompt-standard.md](../../standards/prompt-standard.md).

Антипример (грандфазер-архив): `tz-stats-generator-simple-legacy` нарушает P1
(`-generator`, `-simple` — лишние оси). Архивные промпты **не переименовываются**
(статус `archived` терминален, [prompt-standard.md](../../standards/prompt-standard.md)),
но новые так называть **НЕ ДОЛЖНО**.

### 3. KB-промпты — это не новая ось имени, а сквозная способность

**Проблема.** Добавить суффикс `-kb`/`-rag` означало бы 4-ю ось и удвоение числа
файлов (`fr-validation-stepwise` → ещё и `fr-validation-kb-stepwise`) — прямое
нарушение P1 и НФТ масштабируемости.

**Решение.** Доступ к базе знаний — **сквозная способность** (cross-cutting
capability), а не тип промпта. Любой промпт получает её через **общий блок
цитирования KB**, определённый в [ADR-007 / kb-standard](007-kb-standard.md), а не
через изменение имени. Если же *основная* задача промпта — операция над самой БЗ
(синхронизация глоссария, проверка цитат, KB-grounded research), он именуется по
обычной схеме с подходящей операцией:

| Задача над БЗ | Операция (таксономия) | Иллюстративное имя (не создаётся) |
| --- | --- | --- |
| KB-grounded исследование домена | `research` | `domain-research-stepwise` |
| Синхронизация глоссарий ↔ БЗ | `governance` | `glossary-governance-stepwise` |
| Проверка корректности цитат | `quality` | `citation-quality-oneshot` |

Так KB-функциональность масштабируется без новой оси и без перегрузки имён
(жёсткое требование ФТ-4). Имена выше — **иллюстрация принципа**, эти промпты в
рамках #97 **не создаются** (запрет issue).

### 4. Разбор всех 24 активных промптов (доказательство ФТ-4)

| # | Файл | Домен | Операция | Режим |
| --- | --- | --- | --- | --- |
| 1 | `asr-ingestion-oneshot` | asr | ingestion | oneshot |
| 2 | `asr-ingestion-legacy` | asr | ingestion | legacy |
| 3 | `glossary-context-understanding-stepwise` | glossary-context | understanding | stepwise |
| 4 | `glossary-context-understanding-oneshot` | glossary-context | understanding | oneshot |
| 5 | `questions-customer-understanding-stepwise` | questions-customer | understanding | stepwise |
| 6 | `questions-customer-understanding-legacy` | questions-customer | understanding | legacy |
| 7 | `fr-documentation-stepwise` | fr | documentation | stepwise |
| 8 | `fr-documentation-oneshot` | fr | documentation | oneshot |
| 9 | `constraints-documentation-stepwise` | constraints | documentation | stepwise |
| 10 | `constraints-documentation-oneshot` | constraints | documentation | oneshot |
| 11 | `technical-details-solution-design-stepwise` | technical-details | solution-design | stepwise |
| 12 | `technical-details-solution-design-oneshot` | technical-details | solution-design | oneshot |
| 13 | `technical-details-solution-design-legacy` | technical-details | solution-design | legacy |
| 14 | `fr-validation-stepwise` | fr | validation | stepwise |
| 15 | `fr-validation-oneshot` | fr | validation | oneshot |
| 16 | `fr-validation-legacy` | fr | validation | legacy |
| 17 | `uc-modeling-stepwise` | uc | modeling | stepwise |
| 18 | `uc-modeling-oneshot` | uc | modeling | oneshot |
| 19 | `us-modeling-stepwise` | us | modeling | stepwise |
| 20 | `us-modeling-oneshot` | us | modeling | oneshot |
| 21 | `meeting-customer-documentation-stepwise` | meeting-customer | documentation | stepwise |
| 22 | `meeting-team-documentation-stepwise` | meeting-team | documentation | stepwise |
| 23 | `letter-customer-documentation-legacy` | letter-customer | documentation | legacy |
| 24 | `session-debug-documentation-oneshot` | session-debug | documentation | oneshot |

Все 24 имени детерминированно разбираются парс-алгоритмом §1, операция каждого —
из таксономии, режим — из разрешённого множества. Перегрузки нет.

Архив (6, грандфазер, не переименовываются): `tz-stats-generator-legacy`,
`tz-stats-generator-simple-legacy`, `usecase-stepwise-generator-legacy`,
`usecase-stepwise-generator-simple-legacy`, `user-story-generator-legacy`,
`user-story-generator-simple-legacy` — нарушают P1 (`-generator`/`-simple`),
поэтому архивированы и служат антипримером.

## Доказательная база

- **Внутренний контракт** [prompt-standard.md](../../standards/prompt-standard.md)
  и [ADR-001](001-prompt-standard.md) — источник схемы; ADR-006 её подтверждает
  и уточняет.
- **Режимы stepwise/oneshot/legacy** обоснованы в ADR-001 ссылкой на ReAct
  (reasoning+acting): <https://arxiv.org/abs/2210.03629>.
- **Принцип минимальной перегрузки имён** согласован с практикой именования
  требований в ISO/IEC/IEEE 29148 (короткий стабильный идентификатор):
  <https://www.iso.org/standard/72089.html>.

## Self-test

1. **Дано:** `technical-details-solution-design-legacy`. **Ожидаемо:** парсится
   как (technical-details, solution-design, legacy). **Acceptance:** алгоритм §1.
2. **Дано:** предложение назвать промпт `fr-validation-kb-stepwise`. **Ожидаемо:**
   отклонено по P1 (4-я ось). **Acceptance:** KB — через общий блок (§3).
3. **Дано:** 24 активных промпта. **Ожидаемо:** все парсятся, операция из
   таксономии. **Acceptance:** таблица §4.

Локально: `python3 scripts/validate_issue_97_ontology_standards.py`.

## Последствия

**Положительные:**

- Схема имён получает детерминированный парс-алгоритм (важно для GitHub Pages и
  RAG-индексации).
- Жёсткое требование «не перегружать» стало проверяемым (P1-P4).
- KB-функциональность масштабируется без новой оси имени и без новых файлов.
- 24 промпта подтверждены валидными; ничего не переименовано (НФТ совместимости).

**Отрицательные / технический долг:**

- Парс-алгоритм опирается на актуальность списка операций в таксономии; при
  добавлении операции его нужно учитывать (отражено в правилах эволюции
  таксономии).
- Архивные имена остаются «грязными» (грандфазер) — это сознательный компромисс.

## Альтернативы (отклонены)

1. **Ввести суффикс `-kb`/`-rag`.** Отклонено: 4-я ось, перегрузка, удвоение
   файлов (нарушает жёсткое требование и НФТ).
2. **Кодировать режим в frontmatter, убрать из имени.** Отклонено: режим —
   ключевой различитель в листинге GitHub Pages; имя должно его нести.
3. **Переименовать архивные промпты под стандарт.** Отклонено: `archived`
   терминален; переименование ломает ссылки и историю без выгоды.

## Связанные артефакты

- Issue #97: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97>
- PR #98: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/98>
- Стандарт промпта (контракт, получает подраздел KB): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
- ADR-001 (стандарт промптов): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>
- ADR-007 (KB-стандарт, общий блок цитирования): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/007-kb-standard.md>
- Таксономия: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>

### Внешние источники (полные URL)

- ReAct (режимы рассуждения): <https://arxiv.org/abs/2210.03629>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
