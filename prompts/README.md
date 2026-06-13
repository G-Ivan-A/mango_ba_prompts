---
status: draft
version: 0.1
updated: 2026-06-12
ai-generated: true
type: navigation
scope: prompts
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/65"
---

# Prompts — навигация по библиотеке промптов

Этот README — точка входа в `prompts/` для бизнес-аналитика Mango. Он помогает за
5 минут выбрать нужный prompt-файл, понять режим (`stepwise`, `oneshot`,
`legacy`), увидеть связь с процессами БА и понять, как давать фидбек.

Полный стандарт промптов закреплён в
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
и ADR-001:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>.

## Как быстро выбрать промпт

| Если задача | Начните с |
| --- | --- |
| Нужно собрать контекст для ФТ/ТЗ из сырого запроса | [`glossary-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-stepwise.md) |
| Нужно подготовить уточняющие вопросы заказчику | [`questions-customer-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/questions-customer-understanding-stepwise.md) |
| Нужно сформировать User Story | [`us-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-stepwise.md) или [`us-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-oneshot.md) |
| Нужно сформировать Use Case | [`uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-stepwise.md) или [`uc-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-oneshot.md) |
| Нужно написать раздел 4 ФТ | [`fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-stepwise.md) |
| Нужно проверить или перегенерировать ФТ | [`fr-validation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-stepwise.md) или [`fr-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-oneshot.md) |
| Нужно оформить ограничения и границы скоупа | [`constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/constraints-documentation-stepwise.md) |
| Нужно подготовить раздел 7 для разработки | [`technical-details-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-stepwise.md) |
| Нужно обработать ASR-расшифровку | [`asr-ingestion-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) |
| Нужно сделать резюме встречи | [`meeting-customer-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) или [`meeting-team-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md) |
| Нужно суммаризировать длинную сессию работы с LLM | [`session-debug-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) |

## Матрица промптов

В активной библиотеке сейчас 24 файла в `prompts/`. В архиве дополнительно
сохранены 6 legacy-файлов в `prompts/archive/` для истории, сравнения и аудита.

### 1. Формирование ФТ/ТЗ

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`asr-ingestion-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) | Нормализует ASR-расшифровку в читаемый вход для анализа без потери смысла. | `oneshot` | `draft` | `0.1` | `ingestion` | Формирование ФТ/ТЗ; Помощь ПО/ПМ |
| [`asr-ingestion-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-legacy.md) | Исторический итеративный вариант обработки ASR-транскрипций. | `legacy` | `draft` | `1.0` | `ingestion` | Формирование ФТ/ТЗ; Помощь ПО/ПМ |
| [`glossary-context-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-stepwise.md) | Пошагово формирует терминологию, проблему, цель и задачи для разделов 1-2 ТЗ. | `stepwise` | `draft` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US |
| [`glossary-context-understanding-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-oneshot.md) | Формирует разделы 1-2 ТЗ за один ответ при достаточном входном контексте. | `oneshot` | `draft` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Формирование UC/US |
| [`questions-customer-understanding-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/questions-customer-understanding-stepwise.md) | Пошагово нормализует сырой запрос и готовит точные уточняющие вопросы заказчику. | `stepwise` | `draft` | `0.1` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ |
| [`questions-customer-understanding-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/questions-customer-understanding-legacy.md) | Унаследованный вариант анализа запроса и подготовки вопросов заказчику. | `legacy` | `draft` | `1.0` | `understanding` | Формирование ФТ/ТЗ; Анализ тендерных ТЗ; Помощь ПО/ПМ |
| [`fr-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-stepwise.md) | Пошагово формирует раздел 4 «Функциональные требования» на основе контекста, US и UC. | `stepwise` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`fr-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-oneshot.md) | Формирует раздел 4 ФТ одним ответом при уже собранном контексте. | `oneshot` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`constraints-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/constraints-documentation-stepwise.md) | Пошагово формирует раздел 6 «Особенности реализации / Ограничения». | `stepwise` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`constraints-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/constraints-documentation-oneshot.md) | Формирует раздел 6 ограничений одним ответом. | `oneshot` | `draft` | `0.1` | `documentation` | Формирование ФТ/ТЗ |
| [`technical-details-solution-design-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-stepwise.md) | Пошагово формирует раздел 7 «Список доработок» для разработки. | `stepwise` | `draft` | `0.1` | `solution_design` | Формирование ФТ/ТЗ |
| [`technical-details-solution-design-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-oneshot.md) | Формирует раздел 7 для разработки одним ответом. | `oneshot` | `draft` | `0.1` | `solution_design` | Формирование ФТ/ТЗ |
| [`technical-details-solution-design-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/technical-details-solution-design-legacy.md) | Унаследованный вариант подготовки раздела 7 «Список доработок». | `legacy` | `draft` | `1.0` | `solution_design` | Формирование ФТ/ТЗ |

### 2. Валидация ФТ/ТЗ и анализ тендерных ТЗ

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`fr-validation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-stepwise.md) | Пошагово проводит аудит ФТ и помогает перегенерировать требования по сырым данным. | `stepwise` | `draft` | `0.1` | `validation` | Валидация ФТ/ТЗ; Формирование ФТ/ТЗ; Анализ тендерных ТЗ |
| [`fr-validation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-oneshot.md) | Выполняет экспресс-валидацию и перегенерацию ФТ одним ответом. | `oneshot` | `draft` | `0.1` | `validation` | Валидация ФТ/ТЗ; Анализ тендерных ТЗ |
| [`fr-validation-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-legacy.md) | Унаследованный вариант анализа и валидации функциональных требований. | `legacy` | `draft` | `1.0` | `validation` | Валидация ФТ/ТЗ; Анализ тендерных ТЗ |

### 3. Формирование UC/US

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`uc-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-stepwise.md) | Пошагово формирует Use Case по Cockburn из сырого описания. | `stepwise` | `draft` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`uc-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/uc-modeling-oneshot.md) | Формирует Use Case по Cockburn одним ответом. | `oneshot` | `draft` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`us-modeling-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-stepwise.md) | Пошагово формирует User Story из сырого запроса. | `stepwise` | `draft` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |
| [`us-modeling-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/us-modeling-oneshot.md) | Формирует User Story одним ответом. | `oneshot` | `draft` | `0.1` | `modeling` | Формирование UC/US; Формирование ФТ/ТЗ |

### 4. Помощь ПО/ПМ

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`meeting-customer-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) | Пошагово формирует резюме встречи с заказчиком. | `stepwise` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |
| [`meeting-team-documentation-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md) | Пошагово формирует резюме внутренней встречи команды. | `stepwise` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |
| [`letter-customer-documentation-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/letter-customer-documentation-legacy.md) | Унаследованный промпт для сопроводительного письма заказчику. | `legacy` | `draft` | `1.0` | `documentation` | Помощь ПО/ПМ |

### 5. Отладка и суммаризация сессий

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`session-debug-documentation-oneshot.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) | Суммаризирует длинную сессию работы с LLM в структурированное резюме (контекст, ключевые решения, проблемы, открытые вопросы, шаги), совместимое с `governance/session-digests.md`. | `oneshot` | `draft` | `0.1` | `documentation` | Помощь ПО/ПМ |

### 6. Архив: статистика и исторические генераторы

| Файл | Назначение | Режим | Статус | Версия | Когнитивная операция | Процесс БА |
| --- | --- | --- | --- | --- | --- | --- |
| [`tz-stats-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-legacy.md) | Архивный расширенный генератор статистики по ТЗ. | `legacy` | `archived` | `1.0` | `quality` | Статистика |
| [`tz-stats-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-simple-legacy.md) | Архивный простой генератор статистики по ТЗ. | `legacy` | `archived` | `1.0` | `quality` | Статистика |
| [`usecase-stepwise-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md) | Архивный Hub-style генератор Use Case в пошаговой логике. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`usecase-stepwise-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-simple-legacy.md) | Архивный простой генератор Use Case. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`user-story-generator-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md) | Архивный Hub-style генератор User Story из сырого запроса. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |
| [`user-story-generator-simple-legacy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-simple-legacy.md) | Архивный простой генератор User Story. | `legacy` | `archived` | `1.0` | `modeling` | Формирование UC/US |

Процессы «Визуализация UML/BPMN», «Impact Analysis» и «Risk Analysis» пока не
имеют активных рекомендуемых промптов. Это зафиксировано в центральном индексе:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>.

## Две структуры промптов

ADR-001 допускает две структуры. Новые промпты не обязаны быть одинаковыми по
заголовкам, но должны явно соответствовать одной из этих моделей.

### Структура A: Hub-style prompt

Скелет:

```markdown
# РОЛЬ
# КАК РАБОТАЕМ
# ПРАВИЛА
# ФОРМАТ ВЫВОДА
# НАЧНЕМ?
```

Когда использовать:

- промпт компактный и решает один понятный сценарий;
- не нужны длинные stop-gates и многошаговое согласование;
- промпт переносится из Хаба или готовится как переносимая hub-ready практика.

Преимущества: быстро читается, легко копируется, хорошо подходит для зрелых
role-prompting сценариев.

Ограничения: хуже выражает многошаговые проверки, согласования и сложный
workflow формирования ФТ/ТЗ.

Примеры:

- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md>

### Структура B: Mango BA workflow prompt

Скелет:

```markdown
# РОЛЬ
# ЖЕСТКИЕ ПРАВИЛА
# РЕЖИМ РАБОТЫ
# ШАГ 1
# ШАГ 2
# ФОРМАТ ВЫВОДА
# ОГРАНИЧЕНИЯ
```

Когда использовать:

- результат формируется через несколько шагов и требует подтверждений;
- есть риск домыслов, смешения бизнес-требований и реализации;
- нужно явно разделить сбор контекста, генерацию, проверку и ограничения;
- агент должен работать как workflow БА, а не как генератор одного ответа.

Преимущества: видны контрольные точки, правила, ограничения и формат результата.

Ограничения: структура длиннее и требует аккуратного выбора режима. Для коротких
зрелых prompt-assets она может быть избыточной.

Примеры:

- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/glossary-context-understanding-stepwise.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-documentation-stepwise.md>
- <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/fr-validation-oneshot.md>

## Режимы: `stepwise`, `oneshot`, `legacy`

Режим — последний токен имени файла. Он описывает способ взаимодействия агента с
пользователем, а не роль агента.

| Токен | Значение | Когда использовать | Обоснование |
| --- | --- | --- | --- |
| `stepwise` | Агент делает работу по шагам, показывает промежуточный результат и ждёт подтверждения. | Сбор контекста, ФТ/ТЗ, UC/US, валидация с уточнениями. | Близко к ReAct-подходу `thought -> act -> observe`, где следующий шаг зависит от наблюдения и обратной связи. См. <https://arxiv.org/abs/2210.03629> и <https://www.promptingguide.ai/techniques/react>. |
| `oneshot` | Агент выдаёт полный результат одним ответом без промежуточного диалога. | Достаточный вход, быстрый аудит, нормализация, постобработка ASR, низкая цена уточнений. | Соответствует one-shot prompting / one-shot learning: задача решается за один проход. См. <https://www.promptingguide.ai/techniques/fewshot>. |
| `legacy` | Исторический или унаследованный вариант, сохранённый для совместимости, сравнения или аудита. | Старый стиль, миграция из Хаба, активный черновик до замены, архивный эталон. | `legacy` — стандартный технический термин для унаследованных артефактов. |

Устаревшие токены:

- `expert` не используется как режим, потому что это роль агента, а не способ
  взаимодействия.
- `express` не используется как режим, потому что это маркетинговое слово; для
  одношагового исполнения принят технический токен `oneshot`.

Важно: `legacy` и `archived` — разные вещи. `legacy` — режим в имени файла.
`archived` — статус во frontmatter. Поэтому файл `*-legacy.md` может оставаться
активным черновиком со `status: draft`, а архивный файл должен иметь
`status: archived` и жить в `prompts/archive/`.

## Как тестировать и давать фидбек

Перед переводом промпта из `draft` в `canonical` нужен минимум один
зафиксированный прогон в `prompts/experiments/`. Для рабочей проверки лучше
сделать не меньше трёх прогонов на реальных, но обезличенных данных:

1. Типовой кейс: нормальный вход, ожидаемый результат, без пограничных условий.
2. Сложный кейс: неполный, шумный или противоречивый вход.
3. Регрессионный кейс: пример, где раньше промпт ошибался или требовал ручной
   доработки.

Фидбек создаётся через шаблон:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml>.
Такие issues получают лейбл `prompt:feedback`.

Что указать в фидбеке:

- имя prompt-файла, даже если помните его неточно;
- результат: работает, частично работает, не работает;
- что именно не так: галлюцинации, не тот формат, пропущены разделы, лишняя
  «вода», не учтён контекст;
- обезличенный фрагмент входа и выхода, если он помогает воспроизвести проблему.

Хороший фидбек:

```text
Промпт: fr-validation-stepwise.md
Результат: частично
Вход: обезличенный черновик ФТ на 12 пунктов.
Проблема: промпт сохранил 4.3 и 4.4, но пропустил противоречие между статусами
"Черновик" и "Отправлено". Ожидал отдельный дефект в отчёте валидации.
```

Плохой фидбек:

```text
Промпт плохой, результат не понравился.
```

Триаж фидбека выполняется в рамках weekly/sprint review: команда группирует
повторяющиеся проблемы, выбирает промпты для доработки, фиксирует изменения в PR
и при необходимости добавляет новый эксперимент в `prompts/experiments/`.

## Связь с таксономией и процессами БА

Таксономия задаёт 13 когнитивных операций:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>.
Операция входит в имя файла по схеме `[домен]-[операция]-[режим].md`, где
`solution_design` записывается как `solution-design`.

Индекс процессов БА задаёт 9 процессов и централизованный маппинг
«процесс -> операции -> рекомендуемые промпты»:
<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>.
Этот маппинг не дублируется во frontmatter промптов.

Пример процесса «Формирование ФТ/ТЗ»:

1. `asr-ingestion-oneshot.md` очищает расшифровку встречи.
2. `glossary-context-understanding-stepwise.md` формирует терминологию и
   бизнес-контекст.
3. `questions-customer-understanding-stepwise.md` выявляет недостающий контекст.
4. `us-modeling-stepwise.md` и `uc-modeling-stepwise.md` структурируют сценарии.
5. `fr-documentation-stepwise.md` формирует раздел 4 ФТ.
6. `constraints-documentation-stepwise.md` оформляет раздел 6.
7. `technical-details-solution-design-stepwise.md` готовит раздел 7.
8. `fr-validation-stepwise.md` проверяет полноту, непротиворечивость и
   тестируемость результата.

## Связанные документы

- Репозиторий: <https://github.com/G-Ivan-A/mango_ba_prompts>
- Таксономия 13 операций: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>
- Процессы БА и маппинг: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>
- Стандарт промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>
- ADR-001 по стандарту промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>
- Структура паттернов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md>
- Шаблон фидбека: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml>
- PR #57: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/57>
- PR #59: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/59>
- PR #60: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/60>
- Issue #61: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/61>
- Issue #62: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/62>
- Хаб `hybrid-Intelligence-lab`: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab>
- `clarify-engine-ai`: <https://github.com/G-Ivan-A/clarify-engine-ai>
- `open-ai.ru`: <https://github.com/G-Ivan-A/open-ai.ru>
