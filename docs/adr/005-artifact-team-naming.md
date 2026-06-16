---
status: proposed
version: 0.1
updated: 2026-06-16
ai-generated: true
type: adr
scope: artifact-team-naming
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
related_standard: "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/artifact-naming-standard.md"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/98"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/team-directory.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/003-ba-ontology.md"
---

# ADR-005: Стандарт нейминга артефактов, стандартов и команд (Team Directory)

> **Статус:** Proposed · **Дата:** 2026-06-16 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97> · **Стандарт-контракт:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/artifact-naming-standard.md>

> **Numbering note.** ADR-005 — трёхзначная дорожка стандартов. См.
> [ADR-002](002-pattern-standard.md), [ADR-003](003-ba-ontology.md).

## Контекст

В репозитории нет стандарта нейминга **артефактов** (FR, TZ, US, UC, BCREQ),
**документов-стандартов** и **команд**. Issue #97 (ФТ-3) требует:

1. предложить принцип нейминга **стандартов** (документов вида
   `*-standard.md`/`*-contract.md`);
2. предложить принцип нейминга **BCREQ**;
3. ввести **справочник команд (Team Directory)** — **жёстко: только 2 команды
   BCREQ и CCMO**, с механизмом добавления новых, **без выдуманных команд**
   (`KK`, `UCaaS`, `DIG`, `AI`, `ANL`, `HW`, `SEC` — прямо запрещены);
4. доказательство — примеры для **всех типов артефактов**.

Артефакты уже формализованы в реестре из 30 типов
([ADR-003 §5](003-ba-ontology.md), [стандарт онтологии §4](../../standards/ba-ontology.md)),
но у них нет схемы человекочитаемых идентификаторов. Промпты уже именуются по
[prompt-standard.md](../../standards/prompt-standard.md). Нужна согласованная,
расширяемая (НФТ масштабируемости: 2 → 10+ команд) система имён.

**Важное замечание о терминах BCREQ и CCMO.** Это реальные коды команд,
заданные Пользователем; в репозитории и внешних источниках их расшифровка не
встречается. Чтобы не нарушать запрет на выдуманные источники, ADR **не
изобретает** их полные названия — в [Team Directory](../../standards/team-directory.md)
они помечены `⚠️ требует подтверждения` до уточнения Пользователем. Токен
`BCREQ` используется Пользователем в двух ролях: как **код команды** и как
**тип артефакта** (многоуровневое требование, ФТ-7). Стандарт разводит эти роли
через namespace-разделитель (см. §3).

## Решение

### 1. Идентификатор артефакта

Каноническая схема:

```text
[<TEAM>:]<TYPE>-<NNN>[.<под-уровень>][-v<major>]
```

| Часть | Правило | Пример |
| --- | --- | --- |
| `<TEAM>` | Код из [Team Directory](../../standards/team-directory.md). **Опционален**; ставится только когда нужно различать владельца между командами. Отделяется двоеточием. | `CCMO:` |
| `<TYPE>` | Код типа артефакта, UPPERCASE, ≤6 символов, из контролируемого списка (§4 стандарта = реестр 30 типов). | `FR`, `US`, `UC`, `TZ`, `BCREQ` |
| `<NNN>` | Порядковый номер, ≥3 цифры, ноль-паддинг. | `001` |
| `.<под-уровень>` | Иерархия для многоуровневых артефактов (BCREQ, ФТ-7). | `.2.1` |
| `-v<major>` | Опциональная мажорная версия при baseline. | `-v2` |

Примеры: `FR-001`, `US-012`, `UC-003`, `TZ-005`, `BCREQ-001.2.1`,
`CCMO:FR-014`, `BCREQ:BCREQ-007-v2`.

Принципы (обоснование — §«Доказательная база»): идентификатор **короткий**,
**сортируемый**, **трассируемый** (тип виден в имени → ребро `регулируется`
резолвится), **не перегружен** (НФТ; та же логика, что в
[prompt-standard.md](../../standards/prompt-standard.md): не дублировать в имени
то, что уже есть в реестре/frontmatter).

### 2. Нейминг документов-стандартов

| Вид документа | Каталог | Схема имени | Пример |
| --- | --- | --- | --- |
| Контракт-правило | `standards/` | `<scope>-standard.md` | `prompt-standard.md`, `ba-ontology.md` |
| Контракт, привязанный к внешнему источнику | `standards/` | `<scope>-contract.md` | `product-classification-contract.md` |
| Справочник/реестр | `standards/` | `<scope>-directory.md` / `GLOSSARY.md` | `team-directory.md` |
| ADR (дорожка стандартов) | `docs/adr/` | `<NNN>-<kebab-slug>.md` | `005-artifact-team-naming.md` |
| ADR (governance-дорожка) | `docs/adr/` | `<NNNN>-<kebab-slug>.md` | `0003-creative-mode-governance.md` |

`<scope>` — kebab-case, совпадает с полем `scope` во frontmatter. Заголовок
документа: `# Стандарт <чего>` или `# <Name> Contract`. Это кодифицирует уже
сложившуюся практику (никаких переименований существующих файлов).

### 3. Нейминг BCREQ и разведение ролей токена

`BCREQ` — тип артефакта «многоуровневое бизнес-/коммерческое требование»
(см. [ADR-009](009-bcreq-formation-process.md)). Идентификатор уровня:

```text
BCREQ-<NNN>            ← корневой документ (уровень 0)
BCREQ-<NNN>.<k>        ← подтребование уровня 1
BCREQ-<NNN>.<k>.<m>    ← уровень 2 …
```

Пример: `BCREQ-014`, `BCREQ-014.3`, `BCREQ-014.3.2`. Иерархическая нумерация
напрямую поддерживает многоуровневый процесс ФТ-7 и состояние
`needs-clarification` для незавершённых под-уровней.

Когда нужно одновременно указать команду-владельца и тип BCREQ, namespace-форма
снимает коллизию токена: `BCREQ:BCREQ-014` = артефакт типа BCREQ, принадлежащий
команде BCREQ; `CCMO:BCREQ-014` = BCREQ, принадлежащий команде CCMO.

### 4. Справочник команд (Team Directory)

Полный реестр — в [standards/team-directory.md](../../standards/team-directory.md).
Жёсткие требования issue выполнены буквально:

- **Ровно 2 команды:** `BCREQ`, `CCMO`. Полные названия — `⚠️ требует
  подтверждения` (не выдуманы).
- **Механизм расширения** (НФТ: 2 → 10+): добавление команды = issue → PR →
  human review; код UPPERCASE, уникальный, ≤6 символов, не из запрещённого
  списка.
- **Запрещённые (выдуманные) коды** зафиксированы явно как отклонённые и **не
  добавляются**: `KK`, `UCaaS`, `DIG`, `AI`, `ANL`, `HW`, `SEC`. Они были
  предложены в обсуждении (Think Max) как производные от доменов классификации,
  но не являются реальными командами (требование Пользователя).

### 5. Примеры для всех типов артефактов (доказательство ФТ-3)

Полная таблица «тип → код → пример ID» для всех 30 типов реестра ведётся в
[стандарте нейминга, §«Каталог кодов типов»](../../standards/artifact-naming-standard.md).
Репрезентативная выборка:

| Тип (реестр) | Код | Пример ID | Пример с командой |
| --- | --- | --- | --- |
| `fr-section` (A15) | `FR` | `FR-001` | `CCMO:FR-001` |
| `tz-contract` (A19) | `TZ` | `TZ-005` | `CCMO:TZ-005` |
| `user-story` (A11) | `US` | `US-012` | `BCREQ:US-012` |
| `use-case` (A13) | `UC` | `UC-003` | `BCREQ:UC-003` |
| `bcreq` (A30) | `BCREQ` | `BCREQ-014.3` | `BCREQ:BCREQ-014.3` |
| `risk-register` (A22) | `RISK` | `RISK-002` | `CCMO:RISK-002` |
| `acceptance-criteria` (A12) | `AC` | `AC-031` | — |
| `defect-report` (A20) | `DEF` | `DEF-007` | — |

## Доказательная база

- **ISO/IEC/IEEE 29148:2018** — требует уникальной идентификации требований для
  трассируемости (unique identifier per requirement):
  <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- **BABOK Guide v3 (RLCM — Trace Requirements)** — идентификатор как основа
  traceability: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- **ГОСТ 34.602-2020** — структура и обозначение разделов ТЗ (тип `TZ`):
  <https://docs.cntd.ru/document/1200181804>
- **Внутренний прецедент** — схема имён промптов `[домен]-[операция]-[режим]`
  ([prompt-standard.md](../../standards/prompt-standard.md)) и принцип «не
  перегружать имена» переиспользованы для артефактов.

## Примеры

**Пример A. Трассируемость через ID.** `US-012` → `FR-001` → `TZ-005`:
по идентификаторам строится `traceability-matrix` (A27) без чтения тел
документов (ребро `трассируется`, [ADR-003](003-ba-ontology.md)).

**Пример B. Добавление команды.** Реальная команда «PLATFORM» добавляется PR-ом:
строка в [team-directory.md](../../standards/team-directory.md), код
`PLAT` (≤6, uppercase, не из запрета) → артефакты `PLAT:FR-001`. Масштаб 2 → 10+
не ломает существующие ID (НФТ).

**Пример C. Запрет выдуманных команд.** Попытка добавить `AI` отклоняется
валидатором: код в списке запрещённых.

## Self-test

1. **Дано:** ID `CCMO:FR-001`. **Ожидаемо:** команда CCMO существует в
   directory, тип FR — в реестре. **Acceptance:** обе проверки проходят.
2. **Дано:** попытка завести команду `HW`. **Ожидаемо:** отклонено (запрещённый
   код). **Acceptance:** `HW` в списке §4.
3. **Дано:** BCREQ с под-уровнями. **Ожидаемо:** `BCREQ-014.3.2` валиден.
   **Acceptance:** схема §3.

Локально: `python3 scripts/validate_issue_97_ontology_standards.py`.

## Последствия

**Положительные:**

- Единые, сортируемые, трассируемые идентификаторы для 30 типов артефактов.
- Team Directory выполняет жёсткое требование (2 команды, расширяемость, без
  выдуманных) и масштабируется до 10+.
- Имена не перегружены (НФТ); команда — опциональный facet.
- Роли токена `BCREQ` разведены без фабрикации значений.

**Отрицательные / технический долг:**

- Полные названия BCREQ/CCMO не подтверждены (`⚠️ требует подтверждения`).
- Сквозная нумерация `<NNN>` требует владельца счётчика на команду — пока
  ведётся вручную (вне scope #97).

## Альтернативы (отклонены)

1. **Обязательный префикс команды в каждом ID.** Отклонено: перегружает имена
   при единственном владельце (НФТ — баланс атомарности и простоты).
2. **UUID/хэш как ID.** Отклонено: нечитаемо, не сортируемо, ломает традицию
   `FR-001`.
3. **Изобрести расшифровки BCREQ/CCMO и добавить домены как команды.** Отклонено:
   нарушает запрет на выдуманные команды/источники.

## Связанные артефакты

- Issue #97: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97>
- PR #98: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/98>
- Стандарт нейминга артефактов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/artifact-naming-standard.md>
- Team Directory: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/team-directory.md>
- ADR-003 (онтология, реестр артефактов): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/003-ba-ontology.md>
- ADR-009 (процесс BCREQ): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/009-bcreq-formation-process.md>
- Стандарт промпта (прецедент именования): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>

### Международные стандарты (полные URL)

- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
