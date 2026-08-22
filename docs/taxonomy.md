---
status: draft
version: 0.1
updated: 2026-06-11
ai-generated: true
type: taxonomy
scope: repo-wide
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/52"
---

# Таксономия: когнитивные операции и процессы БА

Таксономия — единая система координат репозитория. Она отвечает на два вопроса:

1. **Какую когнитивную операцию** выполняет промпт или паттерн
   (13 операций, см. §1).
2. **В каком процессе БА** эта операция применяется (9 процессов, см. §2).

Таксономия используется в трёх местах:

- **Именование промптов** — схема `[домен]-[операция]-[режим].md`
  (см. [Стандарт промпта](../standards/prompt-standard.md)) берёт операцию
  из §1.
- **Поле `process_stage` паттерна** (см.
  [Стандарт паттерна](../standards/pattern-standard.md)) ссылается на
  операции из §1.
- **Маппинг процесс ↔ паттерн ↔ промпт** ведётся централизованно в
  [docs/ba-processes/00-index.md](ba-processes/00-index.md) — не во
  frontmatter файлов.

## 1. Когнитивные операции (13)

Операция — атомарный тип мыслительной работы БА, который можно поручить
промпту. Девять операций базовые (унаследованы из практики Mango в Хабе),
четыре добавлены для покрытия процессов Impact/Risk Analysis и
release-цикла.

### 1.1. Базовые операции (9)

| ID | Операция | Что делает | Пример артефакта |
| --- | --- | --- | --- |
| `ingestion` | Приём данных | Превращает сырой вход (ASR-расшифровка, письмо, заметки, тендерное ТЗ) в форму, пригодную для анализа. | Очищенная расшифровка встречи |
| `understanding` | Понимание контекста | Извлекает термины, цели, неявные допущения; формирует уточняющие вопросы. | Глоссарий задачи, список вопросов заказчику |
| `validation` | Валидация | Проверяет артефакт на полноту, непротиворечивость, тестируемость, соответствие стандартам. | Отчёт о дефектах ФТ |
| `modeling` | Моделирование | Структурирует требования в формальные модели: Use Case, User Story, диаграммы UML/BPMN. | Use Case по Cockburn |
| `solution_design` | Проектирование решения | Прорабатывает системно-технические требования и варианты реализации. | Раздел системно-технических требований |
| `documentation` | Документирование | Оформляет результаты анализа в целевые документы: ФТ, ТЗ, резюме встреч, письма. | Черновик ФТ |
| `quality` | Контроль качества | Оценивает качество артефактов и самих промптов; собирает метрики и статистику. | ТЗ-статистика, отчёт self-test |
| `research` | Исследование | Изучает предметную область, рынок, практики; производит знание для решений. | Аналитическая записка |
| `governance` | Управление процессом | Поддерживает правила, статусы, жизненный цикл артефактов и задач. | Чек-лист статусов, бэклог |

### 1.2. Расширенные операции (4)

| ID | Операция | Что делает | Пример артефакта |
| --- | --- | --- | --- |
| `impact_analysis` | Анализ влияния | Оценивает влияние изменения на существующие требования, функции и интеграции продукта. | Карта затронутых функций |
| `reverse_requirements` | Обратные требования | Восстанавливает требования из существующей системы, кода или наблюдаемого поведения. | Реконструированное ФТ legacy-функции |
| `risk_analysis` | Анализ рисков | Выявляет и оценивает риски требований и решений; предлагает митигации. | Реестр рисков с приоритетами |
| `release_readiness` | Готовность к релизу | Проверяет полноту требований, критериев приёмки и чек-листов перед релизом. | Release-readiness чек-лист |

## 2. Процессы БА (9)

Процесс — повторяемый рабочий сценарий бизнес-аналитика Mango. Один процесс
обычно задействует несколько когнитивных операций.

| № | Процесс | Что включает | Ключевые операции |
| --- | --- | --- | --- |
| 1 | Формирование ФТ/ТЗ | От сырого запроса (встреча, письмо, идея) до черновика ФТ/ТЗ. | `ingestion`, `understanding`, `documentation`, `solution_design` |
| 2 | Валидация ФТ/ТЗ | Проверка готовых ФТ/ТЗ на полноту, непротиворечивость, тестируемость. | `validation`, `quality` |
| 3 | Анализ тендерных ТЗ | Разбор внешнего тендерного ТЗ: соответствие продукту, объём доработок. | `ingestion`, `understanding`, `validation`, `risk_analysis` |
| 4 | Формирование UC/US | Преобразование требований в Use Case и User Story. | `modeling`, `understanding` |
| 5 | Визуализация UML/BPMN | Построение диаграмм процессов и взаимодействий. | `modeling`, `documentation` |
| 6 | Помощь ПО/ПМ | Резюме встреч, письма заказчику, уточняющие вопросы, подготовка коммуникаций. | `understanding`, `documentation` |
| 7 | Статистика | Сбор и агрегация статистики по ТЗ и артефактам анализа. | `quality`, `ingestion` |
| 8 | Impact Analysis | Оценка влияния изменений на продукт и связанные требования. | `impact_analysis`, `reverse_requirements` |
| 9 | Risk Analysis | Систематическая оценка рисков требований и готовности к релизу. | `risk_analysis`, `release_readiness`, `validation` |

## 3. Правила эволюции таксономии

- Новая операция или процесс добавляется через issue → PR → human review;
  решение — за Пользователем ([AI_GOVERNANCE.md](../ai-governance/ai-governance.md)).
- Переименование операции требует синхронного обновления имён промптов,
  использующих её, и маппинга в
  [docs/ba-processes/00-index.md](ba-processes/00-index.md).
- Операции в именах файлов записываются в kebab-case
  (`solution_design` → `solution-design`).

## 4. Соответствие BABOK / ISO / ГОСТ и профиль аудита

Раздел добавлен по [ADR-004](adr/004-operations-taxonomy.md) (issue #97, ФТ-2)
**аддитивно**: 13 операций и 9 процессов §1-2 не меняются. Здесь фиксируется
маппинг операций на области знаний BABOK Guide v3 и профиль критериев аудита.

### 4.1. Маппинг операций на 6 областей знаний BABOK Guide v3

Области знаний (Knowledge Areas): **BAPM** — Business Analysis Planning and
Monitoring; **EC** — Elicitation and Collaboration; **RLCM** — Requirements Life
Cycle Management; **SA** — Strategy Analysis; **RADD** — Requirements Analysis and
Design Definition; **SE** — Solution Evaluation.

| Операция | Основная KA | Доп. KA |
| --- | --- | --- |
| `ingestion` | EC | — |
| `understanding` | EC | SA |
| `validation` | RADD | RLCM |
| `modeling` | RADD | — |
| `solution_design` | RADD | SA |
| `documentation` | RADD | EC |
| `quality` | RADD | SE |
| `research` | SA | EC |
| `governance` | RLCM | BAPM |
| `impact_analysis` | RLCM | SE |
| `reverse_requirements` | SA | RADD |
| `risk_analysis` | SA | BAPM |
| `release_readiness` | SE | RLCM |

### 4.2. Профиль критериев аудита (для `validation` и `quality`)

«Аудит» — **не отдельная операция**, а именованный чек-лист характеристик
качества из ISO/IEC/IEEE 29148:2018, который применяют операции `validation`
(к требованиям) и `quality` (к документам/метрикам). Операция `validation`
по BABOK покрывает обе грани: **Verify** (форма) и **Validate** (ценность).

9 характеристик отдельного требования: Necessary, Appropriate, Unambiguous,
Complete, Singular, Feasible, Verifiable, Correct, Conforming. 5 характеристик
набора: Complete, Consistent, Feasible, Comprehensible, Able to be validated.
Прохождение профиля = условие перехода артефакта в состояние `validated`
(см. [стандарт онтологии](../standards/ba-ontology.md), §5).

### 4.3. Соответствие стандартам (полные URL)

- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
- ISO/IEC 25010:2011: <https://www.iso.org/standard/35733.html> · 2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020 (структура ТЗ): <https://docs.cntd.ru/document/1200181804>
- ГОСТ 34.601-90 (стадии создания АС): <https://docs.cntd.ru/document/1200006921>

## Связанные артефакты

- [docs/ba-processes/00-index.md](ba-processes/00-index.md) — маппинг
  процесс ↔ операции ↔ промпты.
- [standards/prompt-standard.md](../standards/prompt-standard.md) — контракт
  промпта (именование, frontmatter).
- [standards/pattern-standard.md](../standards/pattern-standard.md) — контракт
  паттерна (8 полей).
- [docs/rfc-hub-integration.md](rfc-hub-integration.md) — стратегия переноса
  практик в Хаб.
