---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: registry
layer: executable
full_version: "docs/ba-processes/00-index.md"
related_standard: "../../standards/cascading-context-loading-standard.md"
related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
---

# BA Processes Index — executable layer

Load this file first when selecting a BA process, route, operation, or prompt
chain. Do not load `docs/ba-processes/00-index.md` unless one escalation trigger
below is true.

## Escalation triggers

- TRIGGER-1: пользователь явно просит полную карту процессов, detailed workflow,
  examples, Mermaid graph, Known gaps или traceability tables.
- TRIGGER-2: нужно редактировать, валидировать или синхронизировать
  `docs/ba-processes/00-index.md`.
- TRIGGER-3: задача требует точной строки центрального маппинга, полного списка
  prompt-файлов по процессу или parser-compatible структуры для Pages.
- TRIGGER-4: краткий маршрут ниже не покрывает задачу или конфликтует с
  `prompts/README.executable.md`, `docs/taxonomy.md` или стандартом онтологии.

Если ни один триггер не сработал, используй краткую карту ниже.

## Execute

### Route selection

| Если задача | Процесс | Prompt / шаг |
| --- | --- | --- |
| Сформировать ФТ/ТЗ по встрече, письму или сырому запросу | 1. Формирование ФТ/ТЗ | `asr-ingestion-oneshot.md` при ASR -> `glossary-context-understanding-stepwise.md` -> `questions-customer-understanding-stepwise.md` -> `fr-documentation-stepwise.md` |
| Проверить готовый черновик ФТ/ТЗ | 2. Валидация ФТ/ТЗ | `fr-validation-stepwise.md` |
| Разобрать внешнее тендерное ТЗ | 3. Анализ тендерных ТЗ | `glossary-context-understanding-stepwise.md` -> `questions-customer-understanding-stepwise.md` -> `fr-validation-stepwise.md`; coverage/risk вручную |
| Получить User Story или Use Case | 4. Формирование UC/US | `us-modeling-stepwise.md` или `uc-modeling-stepwise.md` |
| Нарисовать UML/BPMN/Mermaid | 5. Визуализация UML/BPMN | dedicated prompt отсутствует; вход можно взять из `uc-modeling-stepwise.md` |
| Подготовить резюме встречи, письмо, вопросы или handover | 6. Помощь ПО/ПМ | `meeting-customer-documentation-stepwise.md`, `meeting-team-documentation-stepwise.md`, `questions-customer-understanding-stepwise.md`, `session-debug-documentation-oneshot.md` |
| Посчитать статистику по корпусу ТЗ или дефектам | 7. Статистика | active prompt отсутствует; legacy только для сравнения |
| Оценить влияние изменения | 8. Impact Analysis | dedicated prompt отсутствует; опирайся на `technical-details-solution-design-stepwise.md` и `fr-validation-stepwise.md` |
| Собрать риски и readiness перед релизом | 9. Risk Analysis | dedicated prompt отсутствует; опирайся на `constraints-documentation-stepwise.md` и `fr-validation-stepwise.md`; owner review обязателен |

### Operation map

| Процесс | Основные операции |
| --- | --- |
| 1. Формирование ФТ/ТЗ | `ingestion`, `understanding`, `modeling`, `documentation`, `solution_design`, `validation` |
| 2. Валидация ФТ/ТЗ | `validation`, `quality`, `risk_analysis` |
| 3. Анализ тендерных ТЗ | `ingestion`, `understanding`, `validation`, `risk_analysis`, `quality` |
| 4. Формирование UC/US | `understanding`, `modeling`, `validation`, `documentation` |
| 5. Визуализация UML/BPMN | `modeling`, `documentation`, `quality` |
| 6. Помощь ПО/ПМ | `ingestion`, `understanding`, `documentation`, `governance` |
| 7. Статистика | `ingestion`, `quality`, `research` |
| 8. Impact Analysis | `reverse_requirements`, `impact_analysis`, `validation`, `governance` |
| 9. Risk Analysis | `risk_analysis`, `release_readiness`, `validation`, `quality` |

### Gate rules

- Не ставь `covered`, `validated`, `approved` или `released` без evidence и
  human gate, если операция относится к `человек` или `гибрид`.
- Если prompt отсутствует, не скрывай gap: пометь "Выполняется вручную" или
  "Требуется разработка промпта".
- Product Layer описывает capability/value/behavior; Commercial Layer описывает
  договорной scope, ответственность, SLA, ИБ/ПДн и клиентские обязательства.
- Research Хаба остаётся reference-only через `docs/hub-research-dependencies.md`.
