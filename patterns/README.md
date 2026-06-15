---
status: draft
version: 0.3
updated: 2026-06-15
ai-generated: true
type: navigation
---

# Patterns — паттерны бизнес-анализа

**Паттерн** — воспроизводимое описание способа решения класса задач БА.
**Промпт** (`prompts/`) — конкретная исполняемая реализация; один паттерн
может реализовываться несколькими промптами (например, `stepwise`, `oneshot` или
`legacy` режимами).

Полное архитектурное решение — [ADR-002 (pattern standard)](../docs/adr/002-pattern-standard.md).
Нормативный контракт — [standards/pattern-standard.md](../standards/pattern-standard.md).

## Навигация по MVP-паттернам

| Паттерн | Путь | Когда начинать отсюда |
| --- | --- | --- |
| [`glossary-context-generation`](glossary-context-generation/) | `patterns/glossary-context-generation/` | Нужно собрать термины, проблему, цель, задачи, Product Layer, Commercial Layer и вопросы. |
| [`asr-ingestion`](asr-ingestion/) | `patterns/asr-ingestion/` | Входом является сырая ASR-расшифровка, встреча или голосовая заметка. |
| [`user-story-generation`](user-story-generation/) | `patterns/user-story-generation/` | Нужно сформулировать роль, ценность и acceptance criteria до сценариев и ФТ. |
| [`usecase-generation`](usecase-generation/) | `patterns/usecase-generation/` | Нужно описать actor/system flow, альтернативы, исключения и postconditions. |
| [`fr-generation`](fr-generation/) | `patterns/fr-generation/` | Контекст уже собран, нужно оформить раздел 4 ФТ/ТЗ. |
| [`fr-validation`](fr-validation/) | `patterns/fr-validation/` | Нужно проверить ФТ/ТЗ на полноту, непротиворечивость, тестируемость и риски. |
| [`meeting-summary-generation`](meeting-summary-generation/) | `patterns/meeting-summary-generation/` | Нужно оформить meeting summary с decisions, questions, owners and next steps. |

## Матрица: паттерн ↔ процесс ↔ операция ↔ промпты

| Паттерн | Процесс БА | Операция | Связанные промпты |
| --- | --- | --- | --- |
| [`glossary-context-generation`](glossary-context-generation/) | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US | `understanding` | [`glossary-context-understanding-stepwise.md`](../prompts/glossary-context-understanding-stepwise.md), [`glossary-context-understanding-oneshot.md`](../prompts/glossary-context-understanding-oneshot.md) |
| [`asr-ingestion`](asr-ingestion/) | Формирование ФТ/ТЗ; Помощь ПО/ПМ | `ingestion` | [`asr-ingestion-oneshot.md`](../prompts/asr-ingestion-oneshot.md), [`asr-ingestion-legacy.md`](../prompts/asr-ingestion-legacy.md) |
| [`user-story-generation`](user-story-generation/) | Формирование UC/US; Формирование ФТ/ТЗ | `modeling` | [`us-modeling-stepwise.md`](../prompts/us-modeling-stepwise.md), [`us-modeling-oneshot.md`](../prompts/us-modeling-oneshot.md) |
| [`usecase-generation`](usecase-generation/) | Формирование UC/US; Формирование ФТ/ТЗ | `modeling` | [`uc-modeling-stepwise.md`](../prompts/uc-modeling-stepwise.md), [`uc-modeling-oneshot.md`](../prompts/uc-modeling-oneshot.md) |
| [`fr-generation`](fr-generation/) | Формирование ФТ/ТЗ | `documentation` | [`fr-documentation-stepwise.md`](../prompts/fr-documentation-stepwise.md), [`fr-documentation-oneshot.md`](../prompts/fr-documentation-oneshot.md) |
| [`fr-validation`](fr-validation/) | Валидация ФТ/ТЗ; Формирование ФТ/ТЗ; Анализ тендерных ТЗ | `validation` + quality overlay | [`fr-validation-stepwise.md`](../prompts/fr-validation-stepwise.md), [`fr-validation-oneshot.md`](../prompts/fr-validation-oneshot.md), [`fr-validation-legacy.md`](../prompts/fr-validation-legacy.md) |
| [`meeting-summary-generation`](meeting-summary-generation/) | Помощь ПО/ПМ; Формирование ФТ/ТЗ | `documentation` | [`meeting-customer-documentation-stepwise.md`](../prompts/meeting-customer-documentation-stepwise.md), [`meeting-team-documentation-stepwise.md`](../prompts/meeting-team-documentation-stepwise.md) |

Связь процесс -> паттерн -> prompt ведётся как source of truth в
[docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md). Эта таблица
служит навигацией для каталога.

## Структура паттерна — 8 полей

Каждый паттерн хранится в `patterns/[operation-name]/README.md` и описывается
восемью обязательными полями:

| Поле | Содержание |
| --- | --- |
| `purpose` | Какую задачу БА решает паттерн, Name/Intent и когда его не применять. |
| `process_stage` | Процесс и когнитивные операции из [docs/taxonomy.md](../docs/taxonomy.md), плюс навигация к prompt-реализациям. |
| `context_requirements` | Product Layer, Commercial Layer, правила адаптации, входы и стоп-факторы. |
| `prompt_template` | Универсальный LLM-агностичный шаблон промпта. |
| `quality_gates` | Проверки качества результата до использования. |
| `examples` | Примеры входа и ожидаемого выхода (обезличенные). |
| `output_schema` | Структура ожидаемого результата. |
| `governance_rules` | Review, статусы, ограничения применения, versioning и связь с центральным реестром. |

## Пример использования

Задача: "Сформировать ТЗ на уведомление супервизора о просроченном callback".

1. Если вход — расшифровка встречи, начните с
   [`asr-ingestion`](asr-ingestion/), чтобы отделить факты, decisions and
   questions от ASR-шума.
2. Запустите [`glossary-context-generation`](glossary-context-generation/), чтобы
   зафиксировать Product Layer = CCaaS, Commercial Layer = `client-order`,
   термины "callback", "супервизор", "SLA" и открытые вопросы.
3. Если нужен бизнес-слой, примените
   [`user-story-generation`](user-story-generation/) и
   [`usecase-generation`](usecase-generation/).
4. Сформируйте раздел 4 через [`fr-generation`](fr-generation/).
5. Проверьте результат через [`fr-validation`](fr-validation/).
6. Если нужно отправить итоги участникам, используйте
   [`meeting-summary-generation`](meeting-summary-generation/).

## Правила каталога

- `prompt_template` остаётся LLM-агностичным: без привязки к конкретной модели и
  без model-specific syntax.
- Маппинг **паттерн ↔ prompt** ведётся в
  [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md). В README
  паттернов даны навигационные ссылки на текущие prompt-реализации.
- Если нужна специфичная LLM-реализация, создаётся или обновляется отдельный
  prompt-файл в `prompts/`, а паттерн не дробится по моделям.
- Токен `quality_control`, встречавшийся в формулировках задач, не является ID
  текущей таксономии. Для `fr-validation` используется операция `validation` с
  quality overlay, чтобы не противоречить [docs/taxonomy.md](../docs/taxonomy.md).
- `asr-ingestion-stepwise.md` не указан как связанный prompt, потому что такого
  файла нет в текущей матрице [prompts/README.md](../prompts/README.md). Текущие
  реализации: `asr-ingestion-oneshot.md` и `asr-ingestion-legacy.md`.

## Связанные артефакты и полные URL

- Таксономия: [docs/taxonomy.md](../docs/taxonomy.md) —
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- Процессы БА: [docs/ba-processes/00-index.md](../docs/ba-processes/00-index.md) —
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>
- Матрица промптов: [prompts/README.md](../prompts/README.md) —
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/README.md>
- Экосистема БА: [docs/ba-ecosystem.md](../docs/ba-ecosystem.md) —
  <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md>
- ADR #002: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/70>
- Экосистема БА: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/67>
- ADR #001: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/69>
- Таксономия и базовый каталог: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/60>
- Репозиторий `mango_ba_prompts`: <https://github.com/G-Ivan-A/mango_ba_prompts>
- Хаб `hybrid-Intelligence-lab`: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab>
- `clarify-engine-ai`: <https://github.com/G-Ivan-A/clarify-engine-ai>
- `open-ai.ru`: <https://github.com/G-Ivan-A/open-ai.ru>
