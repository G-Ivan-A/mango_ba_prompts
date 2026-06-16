---
status: proposed
version: 0.1
updated: 2026-06-16
ai-generated: true
type: adr
scope: operations-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
related_standard: "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/98"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/003-ba-ontology.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md"
---

# ADR-004: Ревизия таксономии операций и маппинг на BABOK / ISO / ГОСТ

> **Статус:** Proposed · **Дата:** 2026-06-16 · **Issue:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97> · **Стандарт-контракт:**
> <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>

> **Numbering note.** ADR-004 — трёхзначная дорожка стандартов (после
> [ADR-003](003-ba-ontology.md)). Не путать с governance-дорожкой `0001`-`0003`.
> См. [ADR-002](002-pattern-standard.md).

## Контекст

[docs/taxonomy.md](../taxonomy.md) фиксирует 13 когнитивных операций (9 базовых +
4 расширенных) и 9 процессов. Issue #97 (ФТ-2) требует:

1. провести ревизию таксономии операций на основе BABOK / IEEE / ISO;
2. **сохранить операцию `risk_analysis`** (явный запрет на её отмену);
3. разрешить «вопрос валидации/аудита» — Think Max в обсуждении предлагал ввести
   отдельную операцию `audit`;
4. обработать входные артефакты: вопросы заказчика, резюме, транскрибации, сырые
   требования;
5. сопоставить операции с 6 областями знаний (Knowledge Areas) BABOK Guide v3.

Таксономия — точка, от которой зависят имена промптов
([prompt-standard.md](../../standards/prompt-standard.md), схема
`[домен]-[операция]-[режим].md`) и поле `process_stage` паттернов. Любое
изменение здесь каскадно затрагивает 24 промпта и 7 паттернов (НФТ совместимости).
Поэтому ревизия проводится **аддитивно**: существующие 13 операций и 9 процессов
сохраняются; добавляется только §4 в таксономию (маппинг и критерии аудита),
ничего не переименовывается и не удаляется.

## Решение

### 1. Все 13 операций подтверждены, ни одна не отменяется

Ревизия по BABOK / ISO / IEEE подтвердила, что каждая из 13 операций соответствует
реальной задаче международной практики (доказательная база — ниже). В частности,
**`risk_analysis` сохраняется** (явное требование issue): в BABOK Guide v3 есть
задача «Assess Risks» в области Strategy Analysis, что прямо легитимизирует
операцию. Переименований нет — НФТ совместимости с 24 промптами соблюдена.

### 2. «Аудит» — это не новая операция, а профиль критериев верификации

**Проблема.** Предложение ввести операцию `audit` конфликтует с тремя
ограничениями issue: (а) не переименовывать/ломать существующие операции;
(б) не перегружать наименования промптов; (в) BABOK не выделяет «аудит» как
отдельную дисциплину — он различает **Verify Requirements** (требование хорошо
сформулировано) и **Validate Requirements** (требование несёт ценность).

**Решение.** Операция `validation` **уже** покрывает обе грани BABOK:

- **Verify** (верификация формы) — требование однозначно, атомарно, проверяемо,
  непротиворечиво;
- **Validate** (валидация ценности) — требование нужно, соответствует
  бизнес-цели и ограничениям.

«Аудит» формализуется не как операция, а как **именованный профиль критериев**
(audit profile) — чек-лист характеристик качества из ISO/IEC/IEEE 29148:2018 и
BABOK, который **применяют** операции `validation` (к требованиям) и `quality`
(к метрикам/документам). Профиль не вводит новый ID операции, не требует новых
имён промптов и не меняет существующие — он становится частью §4 таксономии.

**Профиль критериев аудита (audit profile).** Основан на 9 характеристиках
отдельного требования и 5 характеристиках набора из ISO/IEC/IEEE 29148:2018:

| Критерий (рус.) | 29148 | Что проверяет |
| --- | --- | --- |
| Необходимость | Necessary | требование нужно, нет «золочения» |
| Уместность | Appropriate | уровень детализации соответствует слою |
| Однозначность | Unambiguous | единственная трактовка |
| Полнота | Complete | нет TBD/пробелов (для требования и набора) |
| Атомарность | Singular | одно требование — одна мысль |
| Реализуемость | Feasible | технически и в срок выполнимо |
| Проверяемость | Verifiable | есть критерий приёмки/теста |
| Корректность | Correct | отражает реальную потребность |
| Согласованность с шаблоном | Conforming | следует стандарту оформления |
| Непротиворечивость набора | Consistent | нет конфликтов/дублей между требованиями |
| Понятность набора | Comprehensible | набор читается как целое |
| Валидируемость набора | Able to be validated | набор можно подтвердить со стейкхолдером |

Дубли — частный случай нарушения `Singular`/`Consistent`. Профиль — это вход для
состояния `validated` в жизненном цикле артефакта
([ADR-003 §6](003-ba-ontology.md)).

### 3. Обработка входных артефактов

ФТ-2 называет четыре входа. Каждый позиционирован в онтологии
([ADR-003](003-ba-ontology.md), реестр §4) и маршрутизирован через операции:

| Входной артефакт | Тип (реестр) | Точка входа | Далее (операции-потребители) |
| --- | --- | --- | --- |
| Транскрибации (ASR) | `asr-transcript-raw` (A01) | `ingestion` → `transcript-clean` (A02) | `understanding`, `documentation` |
| Сырые требования | `raw-requirement` (A05) | `understanding` | `validation`, `modeling` |
| Вопросы заказчика | `customer-questions` (A08) | `understanding` (формирует/принимает ответы) | `documentation`, `governance` |
| Резюме (встреч) | `meeting-summary` (A09) | `documentation` (производит) / вход для governance | `governance`, `understanding` |

Ключевой инвариант: **сырые входы не интерпретируются на этапе `ingestion`** —
нормализуется только форма (НФТ provability: `ingestion` не добавляет смысла,
gate «сохранность смысла» из [ADR-003 §4](003-ba-ontology.md)). Смысловая работа
начинается с `understanding`.

### 4. Маппинг 13 операций на 6 областей знаний BABOK Guide v3

Шесть KA BABOK: **BAPM** — Business Analysis Planning and Monitoring; **EC** —
Elicitation and Collaboration; **RLCM** — Requirements Life Cycle Management;
**SA** — Strategy Analysis; **RADD** — Requirements Analysis and Design Definition;
**SE** — Solution Evaluation.

| Операция | Основная KA | Доп. KA | Опорная задача BABOK |
| --- | --- | --- | --- |
| `ingestion` | EC | — | Confirm Elicitation Results |
| `understanding` | EC | SA | Conduct Elicitation; Analyze Current State |
| `validation` | RADD | RLCM | Verify Requirements; Validate Requirements |
| `modeling` | RADD | — | Specify and Model Requirements |
| `solution_design` | RADD | SA | Define Design Options; Define Solution Approach |
| `documentation` | RADD | EC | Specify and Model Requirements; Communicate BA Information |
| `quality` | RADD | SE | Verify Requirements; Measure Solution Performance |
| `research` | SA | EC | Analyze Current State |
| `governance` | RLCM | BAPM | Trace/Maintain/Prioritize/Approve; Plan BA Governance |
| `impact_analysis` | RLCM | SE | Assess Requirements Changes |
| `reverse_requirements` | SA | RADD | Analyze Current State |
| `risk_analysis` | SA | BAPM | **Assess Risks** |
| `release_readiness` | SE | RLCM | Measure Solution Performance; Recommend Actions; Approve Requirements |

Маппинг покрывает все 6 KA (НФТ трассируемости: операции → BABOK KA). Он
переносится в [docs/taxonomy.md §4](../taxonomy.md) как нормативный.

## Доказательная база

- **BABOK Guide v3** (6 KA; различие Verify vs Validate; задача Assess Risks):
  <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
  · глоссарий <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>
- **ISO/IEC/IEEE 29148:2018** (9 характеристик требования + 5 характеристик
  набора = профиль аудита): <https://www.iso.org/standard/72089.html> ·
  <https://standards.ieee.org/ieee/29148/6937/>
- **ISO/IEC 25010** (модель качества для `quality`/`risk_analysis` в части NFR):
  2011 <https://www.iso.org/standard/35733.html> · 2023
  <https://www.iso.org/standard/78176.html>
- **ГОСТ 34.602-2020** (структура ТЗ — целевой документ `documentation`;
  редакция реальна, в отличие от «-2015» из issue, см.
  [ADR-003](003-ba-ontology.md)): <https://docs.cntd.ru/document/1200181804>
- **ГОСТ 34.601-90** (стадии создания АС — каркас процессов 1-2):
  <https://docs.cntd.ru/document/1200006921>

## Примеры

**Пример A. Валидация vs аудит на одном требовании.** Требование «Система должна
быстро обрабатывать звонки» проваливает audit profile сразу по `Unambiguous`
(«быстро» не определено) и `Verifiable` (нет порога). Операция `validation`
фиксирует это в `defect-report` (A20) — без введения операции `audit`.

**Пример B. risk_analysis сохранён.** В процессе 3 «Анализ тендерных ТЗ»
операция `risk_analysis` (исполнитель — человек, [ADR-003 §4](003-ba-ontology.md))
оценивает риск несоответствия продукта пунктам тендера; результат — `risk-register`
(A22). Операция не отменяется (требование issue).

**Пример C. Входной артефакт «транскрибация».** ASR-расшифровка (`asr-transcript-raw`)
→ `ingestion` → `transcript-clean` → `understanding` извлекает `task-glossary` и
`customer-questions`. Смысл не теряется, интерпретация начинается только на
`understanding`.

## Self-test

1. **Дано:** требование без критерия приёмки. **Ожидаемо:** `validation` помечает
   нарушение `Verifiable`; артефакт → `needs-clarification`. **Acceptance:**
   профиль аудита (§2) содержит критерий `Verifiable`.
2. **Дано:** запрос «удалить risk_analysis». **Ожидаемо:** отклоняется — операция
   сохранена по требованию issue. **Acceptance:** строка `risk_analysis`
   присутствует в §4-маппинге.
3. **Дано:** все 13 операций. **Ожидаемо:** каждая имеет основную KA, покрыты все
   6 KA. **Acceptance:** таблица §4.

Локально: `python3 scripts/validate_issue_97_ontology_standards.py`.

## Последствия

**Положительные:**

- Таксономия получает доказанный маппинг на BABOK KA — основа трассируемости
  (НФТ) и онбординга БА.
- Вопрос «валидация vs аудит» закрыт без инфляции числа операций и без
  перегрузки имён промптов (НФТ).
- Профиль аудита даёт операциям `validation`/`quality` явный, измеримый чек-лист
  из ISO/IEC/IEEE 29148.
- Все 24 промпта и 7 паттернов остаются валидными (изменение аддитивное).

**Отрицательные / технический долг:**

- Маппинг операция→KA — экспертная интерпретация BABOK; при появлении доступа к
  полному тексту BABOK его следует сверить и при необходимости уточнить
  (помечено как требующее подтверждения у владельца стандарта).
- Профиль аудита пока применяется вручную; автоматическая проверка критериев —
  отдельная задача (вне scope #97).

## Альтернативы (отклонены)

1. **Ввести операцию `audit`.** Отклонено: ломает совместимость, перегружает
   имена промптов, дублирует `validation` (которая уже = Verify + Validate по
   BABOK).
2. **Удалить `risk_analysis` как «дублирующую» `validation`.** Отклонено: прямой
   запрет issue; BABOK выделяет Assess Risks отдельно от верификации.
3. **Сократить 13 операций до «канонического» меньшего набора.** Отклонено:
   ломает 24 промпта и маппинг; выгода не доказана.

## Связанные артефакты

- Issue #97: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/97>
- PR #98: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/98>
- Таксономия (контракт, получает §4): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- ADR-003 (онтология): <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/003-ba-ontology.md>
- Стандарт онтологии: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/ba-ontology.md>
- Индекс процессов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>

### Международные стандарты (полные URL)

- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- BABOK Glossary: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/>
- ISO/IEC 25010:2011: <https://www.iso.org/standard/35733.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
- ГОСТ 34.601-90: <https://docs.cntd.ru/document/1200006921>
