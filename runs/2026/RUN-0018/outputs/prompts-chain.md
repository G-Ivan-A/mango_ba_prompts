---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: artifact
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/271"
related_artifacts:
  - "prompts/fr-validation-stepwise.md"
  - "standards/experiment-log-standard.md"
---

# Маршрут промптов прогона 1079

## Один промпт, восемь эпизодов

В отличие от [RUN-0012](../../RUN-0012/outputs/prompts-chain.md) (цепочка из шести
разных промптов) здесь запускался **ровно один** промпт:

| Поле | Значение |
| --- | --- |
| Файл | [`prompts/fr-validation-stepwise.md`](../../../../prompts/fr-validation-stepwise.md) |
| `id` | `mango-fr-validation-stepwise` |
| `version` / `status` | 0.1 / draft |
| `temperature` | 0.1 |
| Модель | `qwen3.7-plus`, `thinking_enabled: true`, `auto_search: true` |

**Промпт не изменялся в ходе прогона.** Текст, вставленный БА в чат (Эпизод 1),
сверен с файлом репозитория побайтово (`difflib` → идентичны). Это делает прогон
валидным свидетельством именно для версии v0.1.

## Раскладка по эпизодам

| Эпизод | Шаг промпта | Что запрашивал БА | Результат | Файл разбора |
| --- | --- | --- | --- | --- |
| 1 | ШАГ 1 | инициализация | вопрос о стратегии А/Б | [step-1](steps/step-1-init-strategy.md) |
| 2 | ШАГ 2 | ФТ v1.0 + стратегия Б | Отчёт аудитора (Блок А/Б) | [step-2](steps/step-2-audit-report.md) |
| 3 | ШАГ 3 | перестроить иерархию Раздела 4 | ФТ v1.1 | [step-3](steps/step-3-fr-v1.1.md) |
| 4 | вне шагов | проверка факта по документации | условные 4.3.4 / 4.4.3 | [step-4](steps/step-4-check-multiple-ids.md) |
| 5 | вне шагов | проверка противоречия 6.1.4 ↔ 4.3.3 | «противоречия нет» + микро-правка | [step-5](steps/step-5-contradiction-check.md) |
| 6 | вне шагов | проверка термина по документации | замена термина (**ошибочная**) | [step-6](steps/step-6-terminology-check.md) |
| 7 | ШАГ 2 + ШАГ 3 | вычитка на грамматику/дубли/полноту | ФТ v1.2 | [step-7](steps/step-7-proofreading-v1.2.md) |
| 8 | ШАГ 3 | п. 6.1.5 → ограничение | ФТ v1.3 | [step-8](steps/step-8-constraint-v1.3.md) |

## Наблюдение о покрытии промпта

Промпт описывает три шага, но **половина прогона (эпизоды 4–6) прошла вне его
модели**: БА использовал модель как справочную службу по документации КЦ — режим,
которого в промпте нет вовсе. Именно в этих трёх эпизодах сосредоточены все
подтверждённые галлюцинации прогона (см.
[`../feedback/review-notes.md`](../feedback/review-notes.md)).

**Вывод для библиотеки промптов:** `fr-validation-stepwise` покрывает аудит и
перегенерацию, но не покрывает верификацию фактов и не запрещает недоказуемые
ссылки. Предложение по правке — раздел «Предложения по промптам» в
[`../logs/experiment-log.md`](../logs/experiment-log.md).
