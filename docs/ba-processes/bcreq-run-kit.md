---
status: draft
version: 0.3
updated: 2026-11-04
ai-generated: true
type: process
scope: bcreq-run-kit
related_artifacts:
  - "docs/ba-processes/bcreq-manual-process.md"
  - "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
  - "docs/contracts/bcreq-stage-gates.md"
  - "standards/bcreq-lessons/lessons.json"
  - "standards/bcreq-runtime-references.md"
  - "runs/README.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/427"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/438"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/446"
---

# Комплект прогона BCREQ на новых задачах (BL-157а, BL-157б)

Комплект — то, с чем БА идёт в прогон этапа 1 на новой задаче: порядок
шагов, карточка прогона, журнал гейтов, форма обратной связи и правило
правки промптов. Состав задан
[RFC #427, раздел 9.4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#94-комплект-прогона-на-новых-задачах);
задача — BL-157 ([карточка](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/backlog-ba-model.md#bl-157-комплект-прогона-на-новых-задачах)).

**Статус: действует; A-IN — по тесту (BL-157б).** Р-15 принято, порядок
«П-П: BL-157 сначала (через BL-157а)» — [комментарий владельца к PR #439](https://github.com/G-Ivan-A/mango_ba_prompts/pull/439#issuecomment-6630337995).
Шаги A-IN (Ш-0, Ш-1, Ш-2) идут по черновикам «по тесту» (`by-test`):
синтетический прогон [RUN-0083](../../runs/2026/RUN-0083/outputs/report.md)
дал черновикам 12 из 12 критериев против 10 из 12 у v0.1 при правиле,
записанном до прогона. Остальные шаги идут по промптам `prompts/` v0.1
(`published`). Первый прогон BL-111 с комплектом на реальной задаче —
BL-157в; до него комплект проверен только синтетикой
([разбор готовности](../analysis/2026-11-04-bl-156-157-readiness-check.md)).

## 1. Порядок шагов

Процесс прогона — [ручной процесс BCREQ](bcreq-manual-process.md):
шаги потока — [раздел 0.3](bcreq-manual-process.md#03-шаги-потока),
гейты — [раздел 0.2](bcreq-manual-process.md#02-гейты-и-стадии-артефакта),
правила П-1…П-8 — [раздел 1.1](bcreq-manual-process.md#11-общие-правила-ручного-прогона).
Порядок, назначение шага и варианты «продолжить / вернуться / диалог» —
[RFC #427, раздел 5.4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#54-последовательность-шагов-этапа-1)
и [5.5](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#55-три-варианта-на-каждом-шаге).

На сайте, на странице «Процессы», эта таблица — раздел «Промпты этапа 1
для тестового прогона» (BL-157б, issue #446): у шага — режим из колонки
«Режим в тесте», кнопка копирования назначенного текста и вторая кнопка —
текст для сравнения. Данные сайт берёт из этого файла
(`scripts/generate-pages-data.mjs` → `site/data/test-kit.json`): режим
шага меняется только здесь. Полная форма раздела «Процессы» (DEC-427-12:
«зачем шаг», «варианты дальше») — BL-230 и BL-231.

| № | Шаг | Промпт для копирования | Режим в тесте | Черновик «по тесту» (BL-156) | Ключ урока (`prompts` в `lessons.json`) | Гейт после шага |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ш-0 Конституция | [`bcreq-constitution-governance-oneshot`](../../prompts/bcreq-constitution-governance-oneshot.md) | `by-test` | [`drafts/bcreq-constitution-governance-oneshot`](../../prompts/drafts/bcreq-constitution-governance-oneshot.md) | `constitution` | — |
| 2 | Ш-1 Контекст и глоссарий | [`bcreq-context-understanding-stepwise`](../../prompts/bcreq-context-understanding-stepwise.md) | `by-test` | [`drafts/bcreq-context-understanding-stepwise`](../../prompts/drafts/bcreq-context-understanding-stepwise.md) | `context` | — |
| 3 | Ш-2 Продукты и стейкхолдеры | [`bcreq-products-impact-analysis-stepwise`](../../prompts/bcreq-products-impact-analysis-stepwise.md) | `by-test` | [`drafts/bcreq-products-impact-analysis-stepwise`](../../prompts/drafts/bcreq-products-impact-analysis-stepwise.md) | `products` | Г-IN, `гибрид`, ключевой |
| 4 | Ш-3 ФТ | [`bcreq-fr-documentation-stepwise`](../../prompts/bcreq-fr-documentation-stepwise.md) | `published` | [`drafts/bcreq-fr-documentation-stepwise`](../../prompts/drafts/bcreq-fr-documentation-stepwise.md) | `fr` | — |
| 5 | Ш-4 НФТ | [`bcreq-nfr-documentation-stepwise`](../../prompts/bcreq-nfr-documentation-stepwise.md) | `published` | [`drafts/bcreq-nfr-documentation-stepwise`](../../prompts/drafts/bcreq-nfr-documentation-stepwise.md) | `nfr` | — |
| 6 | Ш-5 UC, прогон 1 | [`bcreq-uc-modeling-stepwise`](../../prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 1`) | `published` | [`drafts/bcreq-uc-modeling-stepwise`](../../prompts/drafts/bcreq-uc-modeling-stepwise.md) | `uc` | Г-С1, `человек`, ключевой |
| 7 | Ш-6 ОРР | [`bcreq-orr-solution-design-stepwise`](../../prompts/bcreq-orr-solution-design-stepwise.md) | `published` | [`drafts/bcreq-orr-solution-design-stepwise`](../../prompts/drafts/bcreq-orr-solution-design-stepwise.md) | `orr` | — |
| 8 | Ш-7 Ограничения | [`bcreq-constraints-documentation-stepwise`](../../prompts/bcreq-constraints-documentation-stepwise.md) | `published` | [`drafts/bcreq-constraints-documentation-stepwise`](../../prompts/drafts/bcreq-constraints-documentation-stepwise.md) | `constraints` | — |
| 9 | Ш-8 UC, прогон 2 | [`bcreq-uc-modeling-stepwise`](../../prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 2`) | `published` | [`drafts/bcreq-uc-modeling-stepwise`](../../prompts/drafts/bcreq-uc-modeling-stepwise.md) | `uc` | — |
| 10 | Ш-9 Риски и приёмка | [`bcreq-extra-risk-analysis-stepwise`](../../prompts/bcreq-extra-risk-analysis-stepwise.md) | `published` | [`drafts/bcreq-extra-risk-analysis-stepwise`](../../prompts/drafts/bcreq-extra-risk-analysis-stepwise.md) | `risk` | — |
| 11 | Ш-В Валидация второй ролью | [`bcreq-review-validation-oneshot`](../../prompts/bcreq-review-validation-oneshot.md) | `published` | [`drafts/bcreq-review-validation-oneshot`](../../prompts/drafts/bcreq-review-validation-oneshot.md) | `review` | Г-W, `человек`, ключевой |
| 12 | Ш-Р Выпуск | заглушка выпуска (пилот) | `by-test` (заглушка) | [заглушка Ш-Р](../../prompts/drafts/bcreq-release-readiness-oneshot.md) | нет ключа: новый — через BL-112 | Выпуск, `человек`, ключевой |
| — | Ш-С Сценарии по запросу | [`bcreq-scenarios-modeling-oneshot`](../../prompts/bcreq-scenarios-modeling-oneshot.md) | `published` | [`drafts/bcreq-scenarios-modeling-oneshot`](../../prompts/drafts/bcreq-scenarios-modeling-oneshot.md) | `scenarios` | — |

Колонка «Промпт для копирования» — опубликованные промпты v0.1 из
`prompts/`. Колонка «Черновик «по тесту»» — промпты шагов BL-156 из
`prompts/drafts/`: текст v0.1 без изменений плюс блок стандартов «по
тесту», собранный сборщиком `scripts/build_bcreq_step_prompts.py`
([отчёт BL-156](../analysis/2026-11-03-bl-156-step-prompts-report.md)).
Режим шага задаёт колонка «Режим в тесте»: `published` — текст из
«Промпт для копирования», `by-test` — из «Черновик «по тесту»». Карточка
прогона (раздел 2) ставит `prompt_set.mode: by-test`, если хоть один шаг
взят из черновика, и пишет в `prompt_ref` путь каждого шага:
`prompts/drafts/<файл>.md` для `by-test`. Измерения черновиков:

- Ш-В — golden set
  ([RUN-0080](../../runs/2026/RUN-0080/outputs/golden-set-report.md):
  55/62, как v0.1; [RUN-0082](../../runs/2026/RUN-0082/outputs/golden-set-report.md),
  три повтора: медиана 54/62, ядро 9/11 — ниже базы RUN-0079 по ядру
  (10/11), поэтому шаг остаётся `published`; правка — BL-156в);
- Ш-0, Ш-1, Ш-2 — синтетический прогон A-IN
  ([RUN-0083](../../runs/2026/RUN-0083/outputs/report.md), N = 1);
- Ш-3…Ш-9, Ш-С — не измерены, остаются `published`.

Две проверки БА в режиме `by-test` (RUN-0083, И-2 и И-3):

- черновик вдвое длиннее v0.1 (Ш-0 — 54 КБ против 35) — БА смотрит
  блок «Проверки (receipt)» ответа: если промпт или его часть попали в
  непрочитанные источники, БА вставляет текст заново;
- строка «Режим fallback: детальные стандарты недоступны» — норма, если
  в чате нет веба. БА переписывает недоступные ссылки в `notes`
  карточки и при нужде прикладывает файл стандарта в чат.

Шаг Ш-Р промпта v0.1 не имеет: черновик — заглушка выпуска (пилот).

## 2. Карточка прогона

Карточка — файл `runs/YYYY/RUN-XXXX/metadata.yaml`. Обязательные поля —
по [контракту `runs/`](../../runs/README.md#контракт-записи); поля ниже
`# BL-157` дополняют контракт и нужны, чтобы сравнивать прогоны между
собой и с golden set. Номер прогона — следующий свободный в
[реестре записей](../../runs/README.md#реестр-записей).

```yaml
run_id: RUN-XXXX
process: bcreq-stage1-<короткое имя задачи>
version: "0.1"
date: YYYY-MM-DD
author: "<БА>"
model: "<модель и версия, как в интерфейсе>"
status: draft            # после разбора: success | partial-success | works-with-edits
run_type: execution
inputs: [inputs/request.md]
outputs: [outputs/bcreq.md]
logs: [logs/gate-journal.md]
feedback: [feedback/step-feedback.md]
# BL-157: карточка прогона (RFC #427, раздел 9.4)
task:
  id: "BCREQ-<номер>"    # обезличенный: без имён клиентов и персональных данных
  title: "<суть запроса в одной фразе>"
prompt_set:
  mode: by-test          # by-test — хоть один шаг из черновика «по тесту» BL-156; published — все шаги prompts/ v0.1
  commit: <SHA коммита mango_ba_prompts, из которого скопированы промпты>
prompt_ref:              # по строке на каждый выполненный шаг
  - {step: Ш-0, path: prompts/drafts/bcreq-constitution-governance-oneshot.md, version: "0.1"}
  - {step: Ш-1, path: prompts/drafts/bcreq-context-understanding-stepwise.md, version: "0.1"}
  - {step: Ш-2, path: prompts/drafts/bcreq-products-impact-analysis-stepwise.md, version: "0.1"}
  - {step: Ш-3, path: prompts/bcreq-fr-documentation-stepwise.md, version: "0.1"}
runtime:
  repo: G-Ivan-A/mango-ba-ai-runtime
  commit: f31dcde33f0bc120244128faab98fc0162e45701   # срез реестра runtime 0.4, раздел 2
standards:               # версии стандартов «по тесту», если mode: by-test
  base: standards/bcreq-prompt-base-standard.md@0.1.3
  profiles: standards/bcreq-prompt-profiles.md@0.1.1
  runtime_references: standards/bcreq-runtime-references.md@0.4
lessons: []              # L-NN из формы обратной связи (раздел 4)
ba_reviewed: false       # true — БА прочитал результат и форму целиком
notes: []                # недоступные модели ссылки («Режим fallback»), приложенные файлы, отклонения
```

Почему эти поля:

- `task`, `model`, `prompt_set.commit`, `runtime.commit` — четыре поля
  карточки из раздела 9.4 RFC: без них прогон нельзя повторить и нельзя
  сравнить с другим прогоном.
- `prompt_ref` по шагам — тот же формат, что у
  [RUN-0079](../../runs/2026/RUN-0079/metadata.yaml) (DEC-411-02): по нему
  урок привязывается к версии промпта.
- `ba_reviewed` — признак, по которому BL-111 считает прогон
  («не меньше N прогонов с отметкой `ba_reviewed`»).
- `notes` — что модель не смогла открыть и что БА приложил сам
  (RUN-0083, И-3): без этого «Режим fallback» в ответе нельзя отличить от
  сбоя промпта.

## 3. Журнал гейтов (К-34)

Файл `runs/YYYY/RUN-XXXX/logs/gate-journal.md`. Каждое решение гейта —
строка; поля — по правилу Г3
[контракта стадий и гейтов](../contracts/bcreq-stage-gates.md#3-возвраты).
Молчание не согласие (П-5): гейт типа `человек` или `гибрид` без
записанного решения человека не пройден, следующий шаг после него не
начинается.

| `gate_id` | `gate_type` | Решение | Кто решил | `model_recommendation` | `divergence` | Причина расхождения | Время |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Г-IN | `гибрид` | дальше / доработать A-IN | БА | дальше / доработать A-IN | совпало / расходится | — | YYYY-MM-DD HH:MM |
| Г-С1 | `человек` | согласование / уточнение / отказ | Заказчик | — | — | — | |
| Г-W | `человек` | согласование / уточнение / отказ | ПО, архитектор, руководитель КК | — | — | — | |
| Выпуск | `человек` | baseline | по процессу A-RELEASE | — | — | — | |

У гейтов типа `человек` предпроверка критериев для БА — `гибрид`: если
модель дала рекомендацию, её тоже пишут в `model_recommendation`.

Переходы между шагами без гейта — вторая таблица того же файла. Она
собирает доказательства для вопроса владельца Р-16 («молчание =
согласие» на переходах): как часто БА переходит к следующему шагу без
явной записи и где это потом приводит к возврату.

| Шаг → шаг | Переход | Возврат позже к этому шагу | Комментарий |
| --- | --- | --- | --- |
| Ш-0 → Ш-1 | явный (записан в 8.5) / неявный (следующий промпт запущен без записи) | нет / да: гейт, причина | |

Журнал — вход для BL-161 (сводка К-34 по Г-IN и решение о типе гейта).

## 4. Форма обратной связи по шагу

Файл `runs/YYYY/RUN-XXXX/feedback/step-feedback.md`. Одна строка — одно
замечание, в форме «шаг → что не так → предложение» (RFC #427, раздел 9.4).

| № | Шаг | Цитата вывода модели | Что не так | Предложение | Урок | Серьёзность |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Ш-3 | «<дословно, обезличено>» | <что нарушено и почему это плохо> | <как должно быть; правило одной фразой> | L-NN или «новый» | блокирует / мешает / косметика |

Как форма идёт в
[реестр уроков](../../standards/bcreq-lessons/lessons.json):

| Поле формы | Поле `lessons.json` | Правило переноса |
| --- | --- | --- |
| Шаг | `prompts` | ключ шага из таблицы раздела 1 |
| Цитата вывода, «Что не так» | `bad`, `check` | `bad` — обезличенная цитата; `check` — вопрос, по которому дефект виден |
| Предложение | `rule`, `good` | `rule` — правило одной фразой; `good` — исправленный пример |
| Урок | `id` | L-NN — замечание подтверждает урок; «новый» — кандидат в урок |
| Файл формы | `qualitative_sources[]` | `{run: RUN-XXXX, file: runs/.../feedback/step-feedback.md, lessons: [L-NN]}` |

БА не правит `lessons.json` сам: новые уроки и связи с прогонами вносит
BL-112 по решению владельца Р-02 (ADR реестра уроков). Карточка прогона
перечисляет найденные L-NN в поле `lessons`.

## 5. Правка промптов — отдельной задачей

Промпт в ходе прогона не меняется: иначе прогон нельзя сравнить ни с
golden set, ни с другими прогонами. Если промпт мешает:

1. записать замечание в форму (раздел 4) с серьёзностью «блокирует»;
2. продолжить на том же тексте или прервать прогон со
   `status: partial-success` и причиной в `feedback/`;
3. правку промпта завести отдельной задачей пользователя (issue) со
   ссылкой на прогон и строку формы.

Промпт-инжиниринг — задачи по инициативе пользователя
([RFC #427, раздел 9.3](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собирается-из-стандартов));
публикация в `prompts/` — только не хуже базовой линии golden set
(DEC-427-11).

## 6. Состав папки прогона

```text
runs/YYYY/RUN-XXXX/
├── metadata.yaml               # карточка прогона, раздел 2
├── inputs/request.md           # обезличенный запрос и материалы
├── outputs/bcreq.md            # документ BCREQ на конец прогона
├── logs/gate-journal.md        # журнал К-34 и переходов, раздел 3
└── feedback/step-feedback.md   # форма обратной связи, раздел 4
```

Строку прогона добавить в
[реестр записей `runs/`](../../runs/README.md#реестр-записей).
