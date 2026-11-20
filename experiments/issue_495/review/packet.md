# Пакет двухролевой проверки реестра issue #495

База `e051e0fa`: нарушений 4723, без группы 0; текущее дерево: нарушений 0.

## U-01

- Класс: б
- Что: prompts/bcreq-constitution-governance-oneshot.md, prompts/bcreq-context-understanding-stepwise.md, prompts/bcreq-core-documentation-oneshot.md, prompts/bcreq-fr-documentation-stepwise.md, prompts/bcreq-in-understanding-oneshot.md, prompts/bcreq-products-impact-analysis-stepwise.md, docs/ba-processes/bcreq-a-in-common.md, docs/ba-processes/bcreq-evidence-normalization.md: «Задержка появления записи amoCRM не доказывает способ API-привязки по ID,»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-01; в промпте — принцип
- Нарушений базы в группе: 168

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`, `prompts/bcreq-context-understanding-stepwise.md`, `prompts/bcreq-core-documentation-oneshot.md`, `prompts/bcreq-fr-documentation-stepwise.md`, `prompts/bcreq-in-understanding-oneshot.md`, `prompts/bcreq-products-impact-analysis-stepwise.md`, `docs/ba-processes/bcreq-a-in-common.md`, `docs/ba-processes/bcreq-evidence-normalization.md`

Было:
```text
Задержка появления записи amoCRM не доказывает способ API-привязки по ID,
тайминг SLA или возможность другой CRM.
```
Стало:
```text
Наблюдаемое поведение внешней системы (например, задержка появления записи)
не доказывает способ интеграции, тайминг SLA или переносимость на другую систему.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `prompts/bcreq-context-understanding-stepwise.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `prompts/bcreq-core-documentation-oneshot.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `prompts/bcreq-fr-documentation-stepwise.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `prompts/bcreq-in-understanding-oneshot.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `prompts/bcreq-products-impact-analysis-stepwise.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `docs/ba-processes/bcreq-a-in-common.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- `docs/ba-processes/bcreq-evidence-normalization.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 34; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0008 `prompts/bcreq-constitution-governance-oneshot.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0009 `prompts/bcreq-constitution-governance-oneshot.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0067 `prompts/bcreq-context-understanding-stepwise.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0068 `prompts/bcreq-context-understanding-stepwise.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0079 `prompts/bcreq-core-documentation-oneshot.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0080 `prompts/bcreq-core-documentation-oneshot.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0098 `prompts/bcreq-fr-documentation-stepwise.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0099 `prompts/bcreq-fr-documentation-stepwise.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- … ещё 160 (полный список — `audit/baseline-map.json`)

## U-01b

- Класс: б
- Что: experiments/issue_474/intake_guard.md: «Задержка появления записи amoCRM не доказывает способ API-привязки по ID,»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-01; в промпте — принцип
- Нарушений базы в группе: 0

Файлы: `experiments/issue_474/intake_guard.md`

Было:
```text
Задержка появления записи amoCRM не доказывает способ API-привязки по ID,
тайминг SLA или возможность другой CRM.
```
Стало:
```text
Наблюдаемое поведение внешней системы (например, задержка появления записи)
не доказывает способ интеграции, тайминг SLA или переносимость на другую систему.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `experiments/issue_474/intake_guard.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 34; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## U-02

- Класс: б
- Что: docs/ba-processes/bcreq-step-handoff.md: «Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
- Нарушений базы в группе: 4

Файлы: `docs/ba-processes/bcreq-step-handoff.md`

Было:
```text
Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.
```
Стало:
```text
Нужен, чтобы новизна решения не скрыла доработку существующих подсистем.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-step-handoff.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1886 `docs/ba-processes/bcreq-step-handoff.md:119` (body) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем. | карта компонентов-кандидатов | те…`
- V-1887 `docs/ba-processes/bcreq-step-handoff.md:119` (body) CT-05 «ЛК» — `…ов-кандидатов | технический | у каждой связи есть источник; ЛК, права и настройки рассмотрены | AIN-07 |…`
- V-3776 `site/data/step-handoff.json:1` (steps.AIN-06.goal) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.…`
- V-3781 `site/data/test-kit.json:1` (handoff.steps.AIN-06.goal) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.…`

## U-03

- Класс: б
- Что: docs/ba-processes/bcreq-step-handoff.md: «у каждой связи есть источник; ЛК, права и настройки рассмотрены»
- Исправление / куда перенесено: продуктовый профиль → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 5

Файлы: `docs/ba-processes/bcreq-step-handoff.md`

Было:
```text
у каждой связи есть источник; ЛК, права и настройки рассмотрены
```
Стало:
```text
у каждой связи есть источник; интерфейсы настройки, права доступа и параметры рассмотрены
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-step-handoff.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 4; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1004 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:281` (body) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-2136 `site/data/a-in-kit.json:281` (steps[].prompt) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-3777 `site/data/step-handoff.json:1` (steps.AIN-06.check) CT-05 «ЛК» — `у каждой связи есть источник; ЛК, права и настройки рассмотрены`
- V-3778 `site/data/step-handoff.json:15` (steps.AIN-06.block) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-3782 `site/data/test-kit.json:1` (handoff.steps.AIN-06.check) CT-05 «ЛК» — `у каждой связи есть источник; ЛК, права и настройки рассмотрены`

## U-04

- Класс: б
- Что: docs/ba-processes/bcreq-a-in-route.json: «"why": "Новизна коннектора не отменяет дельту существующих подсистем"»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
- Нарушений базы в группе: 4

Файлы: `docs/ba-processes/bcreq-a-in-route.json`

Было:
```text
"why": "Новизна коннектора не отменяет дельту существующих подсистем"
```
Стало:
```text
"why": "Новизна решения не отменяет дельту существующих подсистем"
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-route.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 1; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0996 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:220` (body) CT-03 «коннектора» — `- Зачем: Новизна коннектора не отменяет дельту существующих подсистем.`
- V-1888 `docs/ba-processes/bcreq-a-in-route.json:167` (body) CT-03 «коннектора» — `"why": "Новизна коннектора не отменяет дельту существующих подсистем",`
- V-2110 `site/data/a-in-kit.json:1` (steps[].why) CT-03 «коннектора» — `Новизна коннектора не отменяет дельту существующих подсистем`
- V-2128 `site/data/a-in-kit.json:220` (steps[].prompt) CT-03 «коннектора» — `- Зачем: Новизна коннектора не отменяет дельту существующих подсистем.`

## U-05

- Класс: б
- Что: docs/ba-processes/bcreq-a-in-route.json: «статус candidate; ЛК/права/настройки рассмотрены;»
- Исправление / куда перенесено: продуктовый профиль → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 4

Файлы: `docs/ba-processes/bcreq-a-in-route.json`

Было:
```text
статус candidate; ЛК/права/настройки рассмотрены;
```
Стало:
```text
статус candidate; интерфейсы настройки, права доступа и параметры рассмотрены;
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-route.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0998 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:237` (body) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`
- V-1889 `docs/ba-processes/bcreq-a-in-route.json:168` (body) CT-05 «ЛК» — `"checks": "У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторо…`
- V-2111 `site/data/a-in-kit.json:1` (steps[].checks) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`
- V-2130 `site/data/a-in-kit.json:237` (steps[].prompt) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`

## U-06

- Класс: а
- Что: docs/ba-processes/bcreq-a-in-route.json: «"decision": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/474"»
- Исправление / куда перенесено: ссылка → номер решения (карточка)
- Нарушений базы в группе: 49

Файлы: `docs/ba-processes/bcreq-a-in-route.json`

Было:
```text
"decision": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/474"
```
Стало:
```text
"decision": "issue #474"
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-route.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0880 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0900 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0920 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0940 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0960 `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0980 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-1006 `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-1026 `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- … ещё 41 (полный список — `audit/baseline-map.json`)

## U-07

- Класс: б
- Что: docs/ba-processes/bcreq-a-in-instructions.json: «опорные и внешние компоненты; ЛК, права, настройки, хранение,»
- Исправление / куда перенесено: продуктовый профиль → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 3

Файлы: `docs/ba-processes/bcreq-a-in-instructions.json`

Было:
```text
опорные и внешние компоненты; ЛК, права, настройки, хранение,
```
Стало:
```text
опорные и внешние компоненты; интерфейсы настройки, права доступа, параметры, хранение,
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-instructions.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0997 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:229` (body) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`
- V-1891 `docs/ba-processes/bcreq-a-in-instructions.json:28` (body) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`
- V-2129 `site/data/a-in-kit.json:229` (steps[].prompt) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`

## U-08

- Класс: б
- Что: docs/ba-processes/bcreq-a-in-instructions.json: «"negative_example": "Новый коннектор не отменяет дельту ЛК. »
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
- Нарушений базы в группе: 6

Файлы: `docs/ba-processes/bcreq-a-in-instructions.json`

Было:
```text
"negative_example": "Новый коннектор не отменяет дельту ЛК. 
```
Стало:
```text
"negative_example": "Новое решение не отменяет дельту существующих интерфейсов и настроек. 
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-instructions.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0999 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` (body) CT-03 «коннектор» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-1000 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` (body) CT-05 «ЛК» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-1892 `docs/ba-processes/bcreq-a-in-instructions.json:30` (body) CT-03 «коннектор» — `"negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие."`
- V-1893 `docs/ba-processes/bcreq-a-in-instructions.json:30` (body) CT-05 «ЛК» — `"negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие."`
- V-2131 `site/data/a-in-kit.json:248` (steps[].prompt) CT-03 «коннектор» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-2132 `site/data/a-in-kit.json:248` (steps[].prompt) CT-05 «ЛК» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`

## U-09

- Класс: б
- Что: docs/ba-processes/bcreq-a-in-instructions.json: «Аналогия amoCRM не доказывает полный HDE-сценарий.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-03
- Нарушений базы в группе: 6

Файлы: `docs/ba-processes/bcreq-a-in-instructions.json`

Было:
```text
Аналогия amoCRM не доказывает полный HDE-сценарий.
```
Стало:
```text
Аналогия с другой системой не доказывает полный сценарий в целевой системе.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-instructions.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1122 `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` (body) CT-01 «amoCRM» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-1123 `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` (body) CT-06 «HDE» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-1894 `docs/ba-processes/bcreq-a-in-instructions.json:60` (body) CT-01 «amoCRM» — `"negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»."`
- V-1895 `docs/ba-processes/bcreq-a-in-instructions.json:60` (body) CT-06 «HDE» — `"negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»."`
- V-2254 `site/data/a-in-kit.json:248` (steps[].prompt) CT-01 «amoCRM» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-2255 `site/data/a-in-kit.json:248` (steps[].prompt) CT-06 «HDE» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`

## U-10

- Класс: б
- Что: prompts/bcreq-constitution-governance-oneshot.md: «наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)
- Нарушений базы в группе: 5

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе.
```
Стало:
```text
наличие функции в продукте не доказывает её доступность в конкретной интеграции, модуле или тарифе.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0037 `prompts/bcreq-constitution-governance-oneshot.md:250` (body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-0244 `prompts/drafts/bcreq-constitution-governance-oneshot.md:262` (body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3422 `site/data/prompts.json:250` (prompts[].content) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3476 `site/data/prompts.json:239` (prompts[].body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3831 `site/data/test-kit.json:246` (steps[].draft.body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`

## U-11

- Класс: б
- Что: prompts/bcreq-products-impact-analysis-stepwise.md: «передачу этих функций через коннектор.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)
- Нарушений базы в группе: 7

Файлы: `prompts/bcreq-products-impact-analysis-stepwise.md`

Было:
```text
передачу этих функций через коннектор.
```
Стало:
```text
передачу этих функций через интеграцию.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-products-impact-analysis-stepwise.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0153 `prompts/bcreq-products-impact-analysis-stepwise.md:177` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-0663 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:186` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-1513 `prompts/drafts/system/bcreq-products-impact-analysis-system.md:196` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-3676 `site/data/prompts.json:177` (prompts[].content) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-3698 `site/data/prompts.json:166` (prompts[].body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-4135 `site/data/test-kit.json:181` (steps[].system.body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-4202 `site/data/test-kit.json:170` (steps[].draft.body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`

## U-11b

- Класс: б
- Что: scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный): «передачу этих функций через коннектор.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)
- Нарушений базы в группе: 0

Файлы: `scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный)`

Было:
```text
передачу этих функций через коннектор.
```
Стало:
```text
передачу этих функций через интеграцию.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

## U-12

- Класс: б
- Что: prompts/bcreq-constitution-governance-oneshot.md: «| `продукты` | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи |»
- Исправление / куда перенесено: перечень профилей → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
| `продукты` | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи |
```
Стало:
```text
| `продукты` | профили продуктов из справочника профилей продуктов runtime (И-11) |
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0016 `prompts/bcreq-constitution-governance-oneshot.md:124` (body) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-0017 `prompts/bcreq-constitution-governance-oneshot.md:124` (body) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-0222 `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` (body) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-0223 `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` (body) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3401 `site/data/prompts.json:124` (prompts[].content) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3402 `site/data/prompts.json:124` (prompts[].content) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3455 `site/data/prompts.json:113` (prompts[].body) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3456 `site/data/prompts.json:113` (prompts[].body) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## U-12b

- Класс: а
- Что: prompts/bcreq-constitution-governance-oneshot.md (раздел 4.1): «Профили продуктов и их словари — в»
- Исправление / куда перенесено: указатель на стандарт композиции спицы → runtime taxonomy/product-profiles.yaml (И-11, по SHA реестра справочников)
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md (раздел 4.1)`

Было:
```text
Профили продуктов и их словари — в
стандарте композиции §4.
```
Стало:
```text
Профили продуктов и их словари — в справочнике профилей продуктов
runtime (И-11).
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 4; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0018 `prompts/bcreq-constitution-governance-oneshot.md:132` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-0019 `prompts/bcreq-constitution-governance-oneshot.md:132` (body) A-SPOKE-PATH «стандарте композиции §» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-0224 `prompts/drafts/bcreq-constitution-governance-oneshot.md:143` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-0225 `prompts/drafts/bcreq-constitution-governance-oneshot.md:143` (body) A-SPOKE-PATH «стандарте композиции §» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-3403 `site/data/prompts.json:132` (prompts[].content) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-3404 `site/data/prompts.json:132` (prompts[].content) A-SPOKE-PATH «стандарте композиции §» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-3457 `site/data/prompts.json:121` (prompts[].body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-3458 `site/data/prompts.json:121` (prompts[].body) A-SPOKE-PATH «стандарте композиции §» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## U-13

- Класс: б
- Что: prompts/bcreq-products-impact-analysis-stepwise.md: «4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари»
- Исправление / куда перенесено: соответствие профиль → словари → runtime taxonomy/product-profiles.yaml (profiles[].dictionaries); минимальный набор D1, D2, D11 остаётся в промпте и дублируется в runtime minimal_set
- Нарушений базы в группе: 56

Файлы: `prompts/bcreq-products-impact-analysis-stepwise.md`

Было:
```text
4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари
   профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;
   КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).
```
Стало:
```text
4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари
   профилей задействованных продуктов из справочника профилей продуктов
   runtime (И-11). Справочника нет во входе — назови пробел ACCESS_GAP,
   возьми минимальный набор D1, D2, D11 и отметь `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-products-impact-analysis-stepwise.md`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 4/4 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0143 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-04 «ВАТС» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0144 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-05 «ЛК» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0145 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-09 «— D1» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0146 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-09 «— D5» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0147 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D6» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0148 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D11» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0149 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D8» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0150 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D9» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- … ещё 48 (полный список — `audit/baseline-map.json`)

## U-13b

- Класс: б
- Что: scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный): «минимальный набор D1, D2, D11 … оператор связи — D9»
- Исправление / куда перенесено: соответствие профиль → словари → runtime taxonomy/product-profiles.yaml (profiles[].dictionaries); минимальный набор D1, D2, D11 сохранён
- Нарушений базы в группе: 0

Файлы: `scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный)`

Было:
```text
минимальный набор D1, D2, D11 … оператор связи — D9
```
Стало:
```text
минимальный набор D1, D2, D11 … справочника профилей продуктов
   runtime (И-11)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет (только левая часть пары замены сборщика: 2); «стало» — 3/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 4; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

## U-14

- Класс: б
- Что: prompts/asr-ingestion-oneshot.md: «"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").»
- Исправление / куда перенесено: пары «амо» → amoCRM, «вакс» → ВАТС → runtime taxonomy/product-profiles.yaml spoken_aliases (И-11; тест test_spoken_aliases_resolve); неоднозначная форма — «Требует проверки» по правилу промпта
- Нарушений базы в группе: 2

Файлы: `prompts/asr-ingestion-oneshot.md`

Было:
```text
"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").
```
Стало:
```text
"срмка" → "CRM", "апишка" → "API", "питон" → "Python"); разговорные
формы продуктов и внешних систем — по справочнику профилей продуктов
runtime (И-11, раздел spoken_aliases), если он передан во входе.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/asr-ingestion-oneshot.md`: «было» в тексте — нет; «стало» — 3/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0001 `prompts/asr-ingestion-oneshot.md:28` (body) CT-01 «amoCRM» — `"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").`
- V-0002 `prompts/asr-ingestion-oneshot.md:28` (body) CT-04 «ВАТС» — `"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").`

## U-15

- Класс: б
- Что: prompts/asr-ingestion-oneshot.md: «| 7 | "амо" | amoCRM | "интеграция с амо" |»
- Исправление / куда перенесено: пример формы — обезличен; значения пар → runtime taxonomy/product-profiles.yaml spoken_aliases (И-11)
- Нарушений базы в группе: 1

Файлы: `prompts/asr-ingestion-oneshot.md`

Было:
```text
| 7 | "амо" | amoCRM | "интеграция с амо" |
```
Стало:
```text
| 7 | "срмка" | CRM | "интеграция со срмкой" |
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/asr-ingestion-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0003 `prompts/asr-ingestion-oneshot.md:52` (body) CT-01 «amoCRM» — `| 7 | "амо" | amoCRM | "интеграция с амо" |`

## U-16

- Класс: б
- Что: prompts/asr-ingestion-oneshot.md: «- "амо" → "amoCRM"»
- Исправление / куда перенесено: пример формы — обезличен; значения пар → runtime taxonomy/product-profiles.yaml spoken_aliases (И-11)
- Нарушений базы в группе: 2

Файлы: `prompts/asr-ingestion-oneshot.md`

Было:
```text
- "амо" → "amoCRM"
- "вакс" → "ВАТС"
```
Стало:
```text
- "срмка" → "CRM"
- "апишка" → "API"
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/asr-ingestion-oneshot.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0004 `prompts/asr-ingestion-oneshot.md:56` (body) CT-01 «amoCRM» — `- "амо" → "amoCRM"`
- V-0005 `prompts/asr-ingestion-oneshot.md:57` (body) CT-04 «ВАТС» — `- "вакс" → "ВАТС"`

## U-17

- Класс: б
- Что: standards/bcreq-manual-classes/01-intake.md: «операторы, номера ВАТС и сторонние номера»
- Исправление / куда перенесено: обобщено
- Нарушений базы в группе: 4

Файлы: `standards/bcreq-manual-classes/01-intake.md`

Было:
```text
операторы, номера ВАТС и сторонние номера
```
Стало:
```text
операторы, номера телефонии продукта и сторонние номера
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-manual-classes/01-intake.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 1; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1551 `standards/bcreq-manual-classes/01-intake.md:96` (body) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2716 `site/data/prompts.json:1` (prompts[].descriptionLong) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2721 `site/data/prompts.json:96` (prompts[].content) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2728 `site/data/prompts.json:88` (prompts[].body) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`

## U-18

- Класс: б
- Что: scripts/build_bcreq_step_prompts.py (INTAKE_BODY), scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный): «3. Сколько номеров Mango ВАТС?»
- Исправление / куда перенесено: имя продукта → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 4

Файлы: `scripts/build_bcreq_step_prompts.py (INTAKE_BODY)`, `scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)`

Было:
```text
3. Сколько номеров Mango ВАТС?
```
Стало:
```text
3. Сколько номеров телефонии продукта?
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0510 `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:147` (body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-1449 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:158` (body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-3907 `site/data/test-kit.json:143` (steps[].system.body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-3959 `site/data/test-kit.json:133` (steps[].draft.body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`

## U-19

- Класс: б
- Что: scripts/build_bcreq_step_prompts.py (INTAKE_BODY), scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный): «- номера ВАТС: <…|UNKNOWN>»
- Исправление / куда перенесено: имя продукта → runtime taxonomy/product-profiles.yaml
- Нарушений базы в группе: 4

Файлы: `scripts/build_bcreq_step_prompts.py (INTAKE_BODY)`, `scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)`

Было:
```text
- номера ВАТС: <…|UNKNOWN>
```
Стало:
```text
- номера телефонии продукта: <…|UNKNOWN>
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 2/2 фрагментов
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет (только левая часть пары замены сборщика: 2); «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0512 `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:177` (body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-1451 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:188` (body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-3909 `site/data/test-kit.json:173` (steps[].system.body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-3961 `site/data/test-kit.json:163` (steps[].draft.body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`

## U-20

- Класс: б
- Что: standards/bcreq-manual-classes/catalog.json (К-01 behavior), docs/ba-processes/bcreq-run-kit.md (шаг 2, «Что подготовить»): «номера ВАТС и сторонние номера»
- Исправление / куда перенесено: имя продукта → runtime taxonomy/product-profiles.yaml; поля попадают в site/data (каталог, тестовый набор)
- Нарушений базы в группе: 1

Файлы: `standards/bcreq-manual-classes/catalog.json (К-01 behavior)`, `docs/ba-processes/bcreq-run-kit.md (шаг 2, «Что подготовить»)`

Было:
```text
номера ВАТС и сторонние номера
```
Стало:
```text
номера телефонии продукта и сторонние номера
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-manual-classes/catalog.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `docs/ba-processes/bcreq-run-kit.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-3880 `site/data/test-kit.json:1` (steps[].prepare) CT-04 «ВАТС» — `Подключённые у Заказчика продукты, число операторов, номера ВАТС и сторонние номера, объём коммуникаций в месяц, если известны`

## D-01

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «Защиты выведены из 168 инцидентов прогона»
- Исправление / куда перенесено: происхождение (RUN-0075, success-criteria, runtime-improvements) → репозиторий runs/2026/RUN-0075
- Нарушений базы в группе: 23

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
Защиты выведены из 168 инцидентов прогона
RUN-0075
и уточняют Р1–Р7. Критерии успеха БА —
success-criteria,
предложенные формулировки —
runtime-improvements.
```
Стало:
```text
Защиты уточняют Р1–Р7.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0025 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0026 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) BP-04 «RUN-0» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0027 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) BP-04 «RUN-0» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0028 `prompts/bcreq-constitution-governance-oneshot.md:229` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[success-criteria](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md),`
- V-0029 `prompts/bcreq-constitution-governance-oneshot.md:229` (body) BP-04 «RUN-0» — `[success-criteria](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md),`
- V-0030 `prompts/bcreq-constitution-governance-oneshot.md:231` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[runtime-improvements](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md).`
- V-0031 `prompts/bcreq-constitution-governance-oneshot.md:231` (body) BP-04 «RUN-0» — `[runtime-improvements](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md).`
- V-0235 `prompts/drafts/bcreq-constitution-governance-oneshot.md:241` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[success-criteria](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md),`
- … ещё 15 (полный список — `audit/baseline-map.json`)

## D-02

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «| ID | Защита | Правило | Категория RUN-0075 |»
- Исправление / куда перенесено: столбец категорий инцидентов RUN-0075 → реестр уроков standards/bcreq-lessons (run_taxonomies RUN-0075: категория → урок → якорь АД; 10 из 11 пар базы совпадают; пара АД-7 ↔ C10 в реестре — L-30 с якорем АД-8, расхождение Р-28 вынесено владельцу) и источник runs/2026/RUN-0075
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
| ID | Защита | Правило | Категория RUN-0075 |
| --- | --- | --- | --- |
```
Стало:
```text
| ID | Защита | Правило |
| --- | --- | --- |
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0032 `prompts/bcreq-constitution-governance-oneshot.md:233` (body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0033 `prompts/bcreq-constitution-governance-oneshot.md:233` (body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0239 `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` (body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0240 `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` (body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3417 `site/data/prompts.json:233` (prompts[].content) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3418 `site/data/prompts.json:233` (prompts[].content) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3471 `site/data/prompts.json:222` (prompts[].body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3472 `site/data/prompts.json:222` (prompts[].body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## D-02b

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md (таблица АД-1…АД-7, ручная правка вместе с D-02): «АД-1: | Р1, Р2 | C01, C11 |»
- Исправление / куда перенесено: пары АД → категория RUN-0075 → реестр уроков standards/bcreq-lessons (run_taxonomies RUN-0075); 10 из 11 пар совпадают, пара АД-7 ↔ C10 — расхождение Р-28 (вопрос владельцу); источник runs/2026/RUN-0075
- Нарушений базы в группе: 0

Файлы: `prompts/bcreq-constitution-governance-oneshot.md (таблица АД-1…АД-7, ручная правка вместе с D-02)`

Было:
```text
АД-1: | Р1, Р2 | C01, C11 |
АД-2: | Р3 | C09 |
АД-3: | Р7 | C13, C05 |
АД-4: | Р3 | C04 |
АД-5: | Р4 | C02 |
АД-6: | Р2 | C06 |
АД-7: | Р6 | C07, C08, C10 |
```
Стало:
```text
АД-1…АД-7: | <правило> | (ячейка категории удалена вместе со столбцом D-02)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## D-03

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «#### Дополнения по ревизии Golden Set (issue #391)»
- Исправление / куда перенесено: происхождение (issue #391, кандидаты Golden Set) и снятая оговорка «Это защиты от ошибок из кандидатов Golden Set, а не утверждение кандидатов эталонами» → CHANGELOG.md, раздел «Changed — Issue #391: BCREQ-каталог, ревизия Golden Set» (абзац «кандидаты не повышены в статусе») и docs/reviews/issue-391-bcreq-review.md (строки 44, 70, 98: источники АД-8…АД-11, кандидаты — не эталоны); статус golden set задаёт runtime, а не промпт
- Нарушений базы в группе: 15

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
#### Дополнения по ревизии Golden Set (issue #391)

Действуют во всех шагах и стадиях вместе с АД-1…АД-7. Это защиты от
ошибок из кандидатов Golden Set, а не утверждение кандидатов эталонами.
```
Стало:
```text
#### Дополнительные защиты (АД-8…АД-15)

Действуют во всех шагах и стадиях вместе с АД-1…АД-7.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0034 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0035 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0036 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-12 «ревизии Golden» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0241 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0242 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0243 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-12 «ревизии Golden» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-3419 `site/data/prompts.json:243` (prompts[].content) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-3420 `site/data/prompts.json:243` (prompts[].content) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
- … ещё 7 (полный список — `audit/baseline-map.json`)

## D-04

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).»
- Исправление / куда перенесено: происхождение → runs/2026/RUN-0076
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`

Было:
```text
об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).
```
Стало:
```text
об отсутствии ошибки, которой во входе не было.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0038 `prompts/bcreq-constitution-governance-oneshot.md:265` (body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0039 `prompts/bcreq-constitution-governance-oneshot.md:265` (body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0245 `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` (body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0246 `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` (body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3423 `site/data/prompts.json:265` (prompts[].content) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3424 `site/data/prompts.json:265` (prompts[].content) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3477 `site/data/prompts.json:254` (prompts[].body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3478 `site/data/prompts.json:254` (prompts[].body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## D-05

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md, prompts/bcreq-context-understanding-stepwise.md, prompts/bcreq-core-documentation-oneshot.md, prompts/bcreq-fr-documentation-stepwise.md, prompts/bcreq-in-understanding-oneshot.md, prompts/bcreq-products-impact-analysis-stepwise.md: «Полные 24 draft контракта и инструкция БА.»
- Исправление / куда перенесено: ссылка на инструкцию БА (приватный репозиторий) → сайт, раздел A-IN
- Нарушений базы в группе: 26

Файлы: `prompts/bcreq-constitution-governance-oneshot.md`, `prompts/bcreq-context-understanding-stepwise.md`, `prompts/bcreq-core-documentation-oneshot.md`, `prompts/bcreq-fr-documentation-stepwise.md`, `prompts/bcreq-in-understanding-oneshot.md`, `prompts/bcreq-products-impact-analysis-stepwise.md`

Было:
```text
Полные 24 draft контракта и инструкция БА.
```
Стало:
```text
Полный промпт каждого AIN-ID БА передаёт отдельным вызовом.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `prompts/bcreq-context-understanding-stepwise.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `prompts/bcreq-core-documentation-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `prompts/bcreq-fr-documentation-stepwise.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `prompts/bcreq-in-understanding-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `prompts/bcreq-products-impact-analysis-stepwise.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 5; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0007 `prompts/bcreq-constitution-governance-oneshot.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0066 `prompts/bcreq-context-understanding-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0078 `prompts/bcreq-core-documentation-oneshot.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0097 `prompts/bcreq-fr-documentation-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0108 `prompts/bcreq-in-understanding-oneshot.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0136 `prompts/bcreq-products-impact-analysis-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0213 `prompts/drafts/bcreq-constitution-governance-oneshot.md:34` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0351 `prompts/drafts/bcreq-context-understanding-stepwise.md:32` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- … ещё 18 (полный список — `audit/baseline-map.json`)

## D-06

- Класс: в
- Что: prompts/session-debug-documentation-oneshot.md: «можно было вставить в Issue или скопировать как блок в»
- Исправление / куда перенесено: имя файла репозитория → репозиторий pr-ops/session-digests.md
- Нарушений базы в группе: 2

Файлы: `prompts/session-debug-documentation-oneshot.md`

Было:
```text
можно было вставить в Issue или скопировать как блок в
   `pr-ops/session-digests.md` без ручной переработки.
```
Стало:
```text
можно было вставить в задачу трекера или в журнал суммарий без ручной
   переработки.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/session-debug-documentation-oneshot.md`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0188 `prompts/session-debug-documentation-oneshot.md:52` (body) BP-03 «Issue» — `можно было вставить в Issue или скопировать как блок в`
- V-0189 `prompts/session-debug-documentation-oneshot.md:53` (body) A-SPOKE-PATH «pr-ops/session-digests.md» — `'pr-ops/session-digests.md' без ручной переработки.`

## D-06b

- Класс: а
- Что: prompts/session-debug-documentation-oneshot.md (вступление): «структурированное резюме, пригодное для человеческого анализа и для сохранения»
- Исправление / куда перенесено: имя файла репозитория → роль («журнал суммарий»), как в D-06; файл — pr-ops/session-digests.md
- Нарушений базы в группе: 1

Файлы: `prompts/session-debug-documentation-oneshot.md (вступление)`

Было:
```text
структурированное резюме, пригодное для человеческого анализа и для сохранения
в `pr-ops/session-digests.md`.
```
Стало:
```text
структурированное резюме, пригодное для человеческого анализа и для сохранения
в журнал суммарий.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/session-debug-documentation-oneshot.md`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0187 `prompts/session-debug-documentation-oneshot.md:15` (body) A-SPOKE-PATH «pr-ops/session-digests.md» — `в 'pr-ops/session-digests.md'.`

## D-07

- Класс: в
- Что: prompts/session-debug-documentation-oneshot.md: «совместима с шаблоном блока суммарии в»
- Исправление / куда перенесено: ссылка на шаблон → репозиторий pr-ops/session-digests.md
- Нарушений базы в группе: 0

Файлы: `prompts/session-debug-documentation-oneshot.md`

Было:
```text
совместима с шаблоном блока суммарии в
(блоки
```
Стало:
```text
совместима с шаблоном блока суммарии
(блоки
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/session-debug-documentation-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## D-08

- Класс: в
- Что: prompts/session-debug-documentation-oneshot.md: «»
- Исправление / куда перенесено: раздел ссылок на артефакты репозитория → prompts/README.md и карточка промпта
- Нарушений базы в группе: 1

Файлы: `prompts/session-debug-documentation-oneshot.md`

Было:
```text

# КОНТЕКСТ И СВЯЗАННЫЕ АРТЕФАКТЫ
- Стандарт промптов (ADR-001):
- Навигация по библиотеке промптов (сначала executable-слой):
- Механизм суммаризации сессий:
- Таксономия (когнитивные операции и процессы):
- Экосистема БА:
- Репозиторий:
- Хаб (механизм-источник): <https://github.com/G-Ivan-A/hybrid-Intelligence-lab>
```
Стало:
```text
— (удалено)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/session-debug-documentation-oneshot.md`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0191 `prompts/session-debug-documentation-oneshot.md:102` (body) BP-04 «ADR-0» — `- Стандарт промптов (ADR-001):`

## D-09

- Класс: а
- Что: docs/ba-processes/bcreq-a-in-common.md: «Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_pr»
- Исправление / куда перенесено: ссылка на SSOT итога шага → блок «Итог шага» в самом промпте
- Нарушений базы в группе: 97

Файлы: `docs/ba-processes/bcreq-a-in-common.md`

Было:
```text
Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):
```
Стало:
```text
Решение БА по техническому шагу (блок «Итог шага»):
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-common.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 25; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0886 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0887 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0906 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0907 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0926 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0927 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0946 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0947 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- … ещё 89 (полный список — `audit/baseline-map.json`)

## D-10

- Класс: а
- Что: docs/ba-processes/bcreq-a-in-common.md: «Источники:»
- Исправление / куда перенесено: 4 приватные ссылки → Ш-0 во входе; контракты runtime — задачи BL-241, BL-242
- Нарушений базы в группе: 244

Файлы: `docs/ba-processes/bcreq-a-in-common.md`

Было:
```text
Источники:
- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).
- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).
- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).
- [Runtime: версии и источники](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md).
```
Стало:
```text
Источники норм: полный текст Ш-0 (Промпт 0) и нормы, которые БА передал
в этот чат; справочники runtime — только по закреплённому SHA. Ссылка на
закрытый репозиторий источником не считается.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-common.md`: «было» в тексте — нет; «стало» — 3/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 25; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0889 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:51` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).`
- V-0890 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:52` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).`
- V-0891 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:53` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).`
- V-0892 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:53` (body) BP-13 «RFC-AIN-0» — `- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).`
- V-0893 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:54` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Runtime: версии и источники](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md).`
- V-0909 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:51` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).`
- V-0910 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:52` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).`
- V-0911 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:53` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).`
- … ещё 236 (полный список — `audit/baseline-map.json`)

## D-11

- Класс: в
- Что: Баннер архива «(issue #388)» в 18 из 24 файлов архива (`prompts/archive/*.md`)
- Исправление / куда перенесено: > **Архив.** Промпт заменён; номер решения — prompts/README.md (строки 50, 107, 169)
- Нарушений базы в группе: 0

Файлы: `prompts/archive/*.md`

Было:
```text
> **Архив (issue #388).** Промпт заменён
```
Стало:
```text
> **Архив.** Промпт заменён
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## D-12

- Класс: а
- Что: Ссылки на issue во frontmatter служебных файлов
- Исправление / куда перенесено: номер issue вместо URL
- Нарушений базы в группе: 3

Файлы: `prompts/README.executable.md`, `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md`, `docs/ba-processes/bcreq-step-handoff.md`

Было:
```text
related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/490
```
Стало:
```text
related_issue: "#125"
related_issue: "#125"
issue: "#490"
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/README.executable.md`: «было» в тексте — нет; «стало» — 2/3 фрагментов
- `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md`: «было» в тексте — нет; «стало» — 2/3 фрагментов
- `docs/ba-processes/bcreq-step-handoff.md`: «было» в тексте — нет; «стало» — 1/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1885 `docs/ba-processes/bcreq-step-handoff.md:7` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/490`
- V-2007 `prompts/README.executable.md:10` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"`
- V-2008 `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md:10` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"`

## D-13

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (»
- Исправление / куда перенесено: frontmatter карточки, манифест сборки
- Нарушений базы в группе: 246

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.
> **Редакция по тесту (#427): действует до ADR обратного согласования.**
```
Стало:
```text
— (оба баннера удалены — в начале файла и внутри блока; режим — поле `mode: by-test` frontmatter)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0202 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#427» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0207 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0208 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0210 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-09 «действует до ADR» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0270 `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` (body) BP-02 «#427» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.**`
- V-0271 `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.**`
- V-0272 `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` (body) BP-09 «действует до ADR» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.**`
- V-0297 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-02 «#427» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту…`
- … ещё 238 (полный список — `audit/baseline-map.json`)

## D-14

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «<!-- bl-156: by-test -->»
- Исправление / куда перенесено: версии стандартов — prompts/drafts/manifest.json
- Нарушений базы в группе: 504

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
<!-- bl-156: by-test -->
## Дополнение «по тесту» (BL-156): стандарты шага
Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по
RFC #427, раздел 9.3
из базового стандарта 0.1.3,
профилей 0.1.2,
каталога операций и
реестра справочников runtime 0.5.
<!-- /bl-156: by-test -->
```
Стало:
```text
## Стандарты шага / Правила базового стандарта, профилей шага и контракты операций — с номером правила.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — да: RFC #427, раздел 9.3; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0266 `prompts/drafts/bcreq-constitution-governance-oneshot.md:492` (body) BP-01 «<!--» — `<!-- bl-156: by-test -->`
- V-0267 `prompts/drafts/bcreq-constitution-governance-oneshot.md:492` (body) BP-06 «by-test» — `<!-- bl-156: by-test -->`
- V-0268 `prompts/drafts/bcreq-constitution-governance-oneshot.md:493` (body) BP-04 «BL-1» — `## Дополнение «по тесту» (BL-156): стандарты шага`
- V-0269 `prompts/drafts/bcreq-constitution-governance-oneshot.md:493` (body) BP-06 «по тесту» — `## Дополнение «по тесту» (BL-156): стандарты шага`
- V-0273 `prompts/drafts/bcreq-constitution-governance-oneshot.md:497` (body) A-SPOKE-PATH «scripts/build_bcreq_step_prompts.py» — `Блок собран сборщиком 'scripts/build_bcreq_step_prompts.py' по`
- V-0274 `prompts/drafts/bcreq-constitution-governance-oneshot.md:497` (body) BP-07 «сборщик» — `Блок собран сборщиком 'scripts/build_bcreq_step_prompts.py' по`
- V-0275 `prompts/drafts/bcreq-constitution-governance-oneshot.md:498` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[RFC #427, раздел 9.3](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс…`
- V-0276 `prompts/drafts/bcreq-constitution-governance-oneshot.md:498` (body) BP-02 «#427» — `[RFC #427, раздел 9.3](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс…`
- … ещё 496 (полный список — `audit/baseline-map.json`)

## D-15

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «**Приоритет.** Где правило ниже расходится с текстом шага выше (v0.1), действует текст v0.»
- Исправление / куда перенесено: правило приоритета сохранено явно (комментарий 2 владельца)
- Нарушений базы в группе: 0

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
**Приоритет.** Где правило ниже расходится с текстом шага выше (v0.1), действует текст v0.1; расхождение запиши в receipt.
```
Стало:
```text
**Приоритет.** Где правило ниже расходится с текстом шага выше, действует текст шага выше; расхождение запиши в receipt.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## D-16

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-0»
- Исправление / куда перенесено: prompts/drafts/manifest.json → excluded_base_rules (ID и причины); тексты этих правил модель не видит ни в одном промпте, поэтому перечень неисполним; сторож сверхчистки зачитывает их ID только при наличии в манифесте
- Нарушений базы в группе: 99

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.
```
Стало:
```text
— (строка удалена)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0285 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0286 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0287 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-10 «отчёт BL» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0329 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0330 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0331 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-10 «отчёт BL» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0381 `prompts/drafts/bcreq-context-understanding-stepwise.md:509` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0382 `prompts/drafts/bcreq-context-understanding-stepwise.md:509` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- … ещё 91 (полный список — `audit/baseline-map.json`)

## D-17

- Класс: а, в
- Что: scripts/build_bcreq_step_prompts.py: «**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3:»
- Исправление / куда перенесено: правило изложено в шаге целиком (поля записи, условие неполноты), отсылка к стандарту гейтов снята; происхождение К-34 — runs/2026/RUN-0089/outputs/report.md (P05), правило Г3 — docs/contracts/bcreq-stage-gates.md; в runtime выносить нечего
- Нарушений базы в группе: 29

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3:
[`docs/contracts/bcreq-stage-gates.md`](…).
```
Стало:
```text
**Запись решения гейта (К-34).** … гейта, а у гибрида без расхождения, неполна.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 5; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0683 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:378` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-0684 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:382` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `['docs/contracts/bcreq-stage-gates.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).`
- V-0685 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:382` (body) A-SPOKE-PATH «docs/contracts/bcreq-stage-gates.md» — `['docs/contracts/bcreq-stage-gates.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).`
- V-0731 `prompts/drafts/bcreq-release-readiness-oneshot.md:158` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-0732 `prompts/drafts/bcreq-release-readiness-oneshot.md:162` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `['docs/contracts/bcreq-stage-gates.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).`
- V-0733 `prompts/drafts/bcreq-release-readiness-oneshot.md:162` (body) A-SPOKE-PATH «docs/contracts/bcreq-stage-gates.md» — `['docs/contracts/bcreq-stage-gates.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).`
- V-0864 `prompts/drafts/bcreq-uc-modeling-stepwise.md:300` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-0865 `prompts/drafts/bcreq-uc-modeling-stepwise.md:304` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `['docs/contracts/bcreq-stage-gates.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md).`
- … ещё 21 (полный список — `audit/baseline-map.json`)

## D-18

- Класс: а, в
- Что: scripts/build_bcreq_step_prompts.py, scripts/build_bcreq_a_in.py, scripts/build_bcreq_system_track.py: «<!-- Experimental: for … issues/438|474|490, no formal research yet -->»
- Исправление / куда перенесено: статус draft — поле frontmatter `status`
- Нарушений базы в группе: 234

Файлы: `scripts/build_bcreq_step_prompts.py`, `scripts/build_bcreq_a_in.py`, `scripts/build_bcreq_system_track.py`

Было:
```text
<!-- Experimental: for … issues/438|474|490, no formal research yet -->
```
Стало:
```text
— (строка удалена)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — удаление
- `scripts/build_bcreq_a_in.py`: «было» в тексте — нет; «стало» — удаление
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0198 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0199 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-01 «<!--» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0200 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-04 «BL-1» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0201 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-08 «Experimental» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0293 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0294 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-01 «<!--» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0295 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-04 «BL-1» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0296 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-08 «Experimental» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- … ещё 226 (полный список — `audit/baseline-map.json`)

## D-19

- Класс: в
- Что: standards/bcreq-prompt-base-standard.md: «БС-21: … блок заглушки раздела 4 реестра … (сейчас только З-2; З-1 снята BL-163, З-3 и З-4»
- Исправление / куда перенесено: колонка «Источник» стандарта, реестр справочников раздел 4
- Нарушений базы в группе: 66

Файлы: `standards/bcreq-prompt-base-standard.md`

Было:
```text
БС-21: … блок заглушки раздела 4 реестра … (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка …
```
Стало:
```text
БС-21: … блок заглушки раздела 4 реестра; заглушка … (история заглушек — колонка «Источник»)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-prompt-base-standard.md`: «было» в тексте — нет (только левая часть пары замены сборщика: 1); «стало» — 1/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 17; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0283 `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0284 `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0327 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0328 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0379 `prompts/drafts/bcreq-context-understanding-stepwise.md:486` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0380 `prompts/drafts/bcreq-context-understanding-stepwise.md:486` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0424 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0425 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- … ещё 58 (полный список — `audit/baseline-map.json`)

## D-20

- Класс: в
- Что: standards/bcreq-runtime-references.md, scripts/build_bcreq_step_prompts.py (заглушки З-n из реестра): «[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]»
- Исправление / куда перенесено: RFC #427, раздел 8.4; pr-ops/BACKLOG.md BL-155
- Нарушений базы в группе: 9

Файлы: `standards/bcreq-runtime-references.md`, `scripts/build_bcreq_step_prompts.py (заглушки З-n из реестра)`

Было:
```text
[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]
[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов … ОРР; задача BL-155]
```
Стало:
```text
[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>]
[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР]
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-runtime-references.md`: «было» в тексте — нет; «стало» — 1/2 фрагментов
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 0/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 5; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0483 `prompts/drafts/bcreq-fr-documentation-stepwise.md:483` (body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-0580 `prompts/drafts/bcreq-nfr-documentation-stepwise.md:346` (body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-0828 `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:348` (body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-0874 `prompts/drafts/bcreq-uc-modeling-stepwise.md:398` (body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-4287 `site/data/test-kit.json:467` (steps[].draft.body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-4335 `site/data/test-kit.json:330` (steps[].draft.body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-4386 `site/data/test-kit.json:382` (steps[].draft.body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- V-4533 `site/data/test-kit.json:382` (steps[].draft.body) BP-04 «BL-1» — `[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155]`
- … ещё 1 (полный список — `audit/baseline-map.json`)

## D-21

- Класс: в
- Что: scripts/build_bcreq_a_in.py (PROVENANCE): «LE-19: … модель выбирает сама (обратная связь RUN-0090) → …»
- Исправление / куда перенесено: RFC A-IN, таблица LE (источник урока остаётся там)
- Нарушений базы в группе: 48

Файлы: `scripts/build_bcreq_a_in.py (PROVENANCE)`

Было:
```text
LE-19: … модель выбирает сама (обратная связь RUN-0090) → …
```
Стало:
```text
LE-19: … модель выбирает сама → …
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_a_in.py`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 25; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0896 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0916 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0936 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0956 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:265` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0976 `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:265` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-1001 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:264` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-1022 `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-1042 `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:264` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- … ещё 40 (полный список — `audit/baseline-map.json`)

## D-22

- Класс: в
- Что: scripts/build_bcreq_system_track.py: «> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архив»
- Исправление / куда перенесено: архив prompts/archive/a-in-v2.7.0 (историческая сущность)
- Нарушений базы в группе: 139

Файлы: `scripts/build_bcreq_system_track.py`

Было:
```text
> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архивный блок «Дополнение «по тесту» (BL-156)»
История баннера: «Редакция … «Редакция по тесту (#427): действует до ADR … Черновик BL-156 (issue #438)
```
Стало:
```text
— (баннер удалён; архивный блок заменён текущим блоком «Стандарты шага»)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0203 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#438» — `…ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко…`
- V-0205 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-03 «issue» — `…действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» …`
- V-0206 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-04 «BL-1» — `…(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по…`
- V-0209 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-08 «Черновик BL» — `…по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);…`
- V-0440 `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` (body) BP-02 «#438» — `…ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко…`
- V-0442 `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` (body) BP-03 «issue» — `…действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» …`
- V-0443 `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` (body) BP-04 «BL-1» — `…(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по…`
- V-0446 `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` (body) BP-08 «Черновик BL» — `…по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);…`
- … ещё 131 (полный список — `audit/baseline-map.json`)

## D-23

- Класс: в
- Что: scripts/build_bcreq_a_in.py: «Draft для ручной проверки БА; эффективность модели не измерена.»
- Исправление / куда перенесено: статус — поле frontmatter `status: draft` каждого AIN-промпта и `status: draft`, `measured: false` в site/data/a-in-kit.json (собирает тот же build_bcreq_a_in.py)
- Нарушений базы в группе: 144

Файлы: `scripts/build_bcreq_a_in.py`

Было:
```text
Draft для ручной проверки БА; эффективность модели не измерена.
```
Стало:
```text
— (строка удалена)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_a_in.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0883 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` (body) BP-08 «Draft для» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0884 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` (body) BP-09 «эффективность модели» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0885 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` (body) BP-09 «не измерен» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0903 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` (body) BP-08 «Draft для» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0904 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` (body) BP-09 «эффективность модели» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0905 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` (body) BP-09 «не измерен» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0923 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:17` (body) BP-08 «Draft для» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-0924 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:17` (body) BP-09 «эффективность модели» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- … ещё 136 (полный список — `audit/baseline-map.json`)

## D-24

- Класс: а, в
- Что: scripts/build_bcreq_system_track.py: «<!-- issue-490:system -->»
- Исправление / куда перенесено: граница раздела — заголовок `## Системный формат шагов` (константа BEGIN сборщика); происхождение формата — docs/rfc/2026-11-bcreq-step-format.md и issue #490 в CHANGELOG.md
- Нарушений базы в группе: 36

Файлы: `scripts/build_bcreq_system_track.py`

Было:
```text
<!-- issue-490:system -->
<!-- /issue-490:system -->
## Системный формат шагов (#490)
([issue #490](https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат
```
Стало:
```text
## Системный формат шагов
(граница раздела — сам заголовок; ссылка на issue снята)
БА выбрал системный формат
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет; «стало» — 2/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 4; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1381 `prompts/drafts/system/bcreq-context-understanding-system.md:22` (body) BP-01 «<!--» — `<!-- issue-490:system -->`
- V-1382 `prompts/drafts/system/bcreq-context-understanding-system.md:23` (body) BP-02 «#490» — `## Системный формат шагов (#490)`
- V-1383 `prompts/drafts/system/bcreq-context-understanding-system.md:27` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `([issue #490](https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай`
- V-1384 `prompts/drafts/system/bcreq-context-understanding-system.md:27` (body) BP-02 «#490» — `([issue #490](https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай`
- V-1385 `prompts/drafts/system/bcreq-context-understanding-system.md:27` (body) BP-03 «issue» — `([issue #490](https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай`
- V-1388 `prompts/drafts/system/bcreq-context-understanding-system.md:107` (body) BP-01 «<!--» — `<!-- /issue-490:system -->`
- V-1439 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:22` (body) BP-01 «<!--» — `<!-- issue-490:system -->`
- V-1440 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:23` (body) BP-02 «#490» — `## Системный формат шагов (#490)`
- … ещё 28 (полный список — `audit/baseline-map.json`)

## D-25

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py (CASE_EDITS, Ш-0 и Ш-3; заголовок по тесту): «Формат шагов (#490) задаёт сайт строкой»
- Исправление / куда перенесено: номер решения (#490) → docs/rfc/2026-11-bcreq-step-format.md и CHANGELOG.md; правило формата шагов в промпте сохранено
- Нарушений базы в группе: 10

Файлы: `scripts/build_bcreq_step_prompts.py (CASE_EDITS, Ш-0 и Ш-3; заголовок по тесту)`

Было:
```text
Формат шагов (#490) задаёт сайт строкой
**Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из
проверь вход по формату шагов из «Состояния BCREQ» (#490).
ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.
```
Стало:
```text
Формат шагов задаёт сайт строкой
**Формат шагов.** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из
проверь вход по формату шагов из «Состояния BCREQ».
— (заголовок «по тесту» удалён вместе с баннером D-13)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 3/3 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0204 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#490» — `…438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.…`
- V-0212 `prompts/drafts/bcreq-constitution-governance-oneshot.md:24` (body) BP-02 «#490» — `…, формат шагов и исходный запрос без анализа. Формат шагов (#490) задаёт сайт строкой «Формат шагов: системный» или «Формат шагов: декомпозированный»;…`
- V-0259 `prompts/drafts/bcreq-constitution-governance-oneshot.md:315` (body) BP-02 «#490» — `**Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из`
- V-0441 `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` (body) BP-02 «#490» — `…438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.…`
- V-0449 `prompts/drafts/bcreq-fr-documentation-stepwise.md:24` (body) BP-02 «#490» — `…тма Ш-3 проверь вход по формату шагов из «Состояния BCREQ» (#490). Декомпозированный (по умолчанию): явные AIN-21 и AIN-24/Г-IN, их task/attempt/route…`
- V-3791 `site/data/test-kit.json:3` (steps[].draft.body) BP-02 «#490» — `…438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.…`
- V-3799 `site/data/test-kit.json:8` (steps[].draft.body) BP-02 «#490» — `…, формат шагов и исходный запрос без анализа. Формат шагов (#490) задаёт сайт строкой «Формат шагов: системный» или «Формат шагов: декомпозированный»;…`
- V-3846 `site/data/test-kit.json:299` (steps[].draft.body) BP-02 «#490» — `**Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## D-26

- Класс: а, в
- Что: scripts/build_bcreq_step_prompts.py (RELEASE_BODY, Ш-Р): «Шаг Ш-Р — заглушка выпуска (пилот): у него нет промпта v0.1»
- Исправление / куда перенесено: состав шагов → docs/rfc/2026-11-bcreq-flow-processes-prompts.md, раздел 9.2; происхождение правил пакетов → pr-ops/BACKLOG.md BL-123 и runs/2026/RUN-0089/outputs/report.md (P16)
- Нарушений базы в группе: 8

Файлы: `scripts/build_bcreq_step_prompts.py (RELEASE_BODY, Ш-Р)`

Было:
```text
Шаг Ш-Р — заглушка выпуска (пилот): у него нет промпта v0.1
([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).
гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).
```
Стало:
```text
Шаг Ш-Р — заглушка выпуска (пилот). Текст шага ниже — контракты операций
пакетов раздела 4. Отдельный вызов, новая сессия.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0711 `prompts/drafts/bcreq-release-readiness-oneshot.md:22` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).`
- V-0712 `prompts/drafts/bcreq-release-readiness-oneshot.md:22` (body) BP-02 «#427» — `([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).`
- V-0713 `prompts/drafts/bcreq-release-readiness-oneshot.md:24` (body) BP-04 «BL-1» — `гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).`
- V-0714 `prompts/drafts/bcreq-release-readiness-oneshot.md:24` (body) BP-04 «RUN-0» — `гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).`
- V-4644 `site/data/test-kit.json:8` (steps[].draft.body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).`
- V-4645 `site/data/test-kit.json:8` (steps[].draft.body) BP-02 «#427» — `([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).`
- V-4646 `site/data/test-kit.json:10` (steps[].draft.body) BP-04 «BL-1» — `гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).`
- V-4647 `site/data/test-kit.json:10` (steps[].draft.body) BP-04 «RUN-0» — `гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).`

## D-27

- Класс: в
- Что: docs/ba-processes/bcreq-step-handoff.md (раздел 2, шаблон блока), scripts/bcreq_handoff.py (BEGIN, END): «<!-- issue-490:handoff -->»
- Исправление / куда перенесено: номер решения (#490) → frontmatter SSOT `issue: "#490"` (D-12) и CHANGELOG.md; границы блока проверяет bcreq_handoff.py (assert без «<!--»)
- Нарушений базы в группе: 231

Файлы: `docs/ba-processes/bcreq-step-handoff.md (раздел 2, шаблон блока)`, `scripts/bcreq_handoff.py (BEGIN, END)`

Было:
```text
<!-- issue-490:handoff -->
## Итог шага для БА (#490)
<!-- /issue-490:handoff -->
```
Стало:
```text
## Итог шага для БА
(границы блока — заголовок и последняя строка «без записи — декомпозированный.»; константы BEGIN, END сборщика)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-step-handoff.md`: «было» в тексте — нет; «стало» — 1/2 фрагментов
- `scripts/bcreq_handoff.py`: «было» в тексте — нет; «стало» — 1/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 41; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0290 `prompts/drafts/bcreq-constitution-governance-oneshot.md:644` (body) BP-01 «<!--» — `<!-- issue-490:handoff -->`
- V-0291 `prompts/drafts/bcreq-constitution-governance-oneshot.md:645` (body) BP-02 «#490» — `## Итог шага для БА (#490)`
- V-0292 `prompts/drafts/bcreq-constitution-governance-oneshot.md:666` (body) BP-01 «<!--» — `<!-- /issue-490:handoff -->`
- V-0335 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:344` (body) BP-01 «<!--» — `<!-- issue-490:handoff -->`
- V-0336 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:345` (body) BP-02 «#490» — `## Итог шага для БА (#490)`
- V-0337 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:366` (body) BP-01 «<!--» — `<!-- /issue-490:handoff -->`
- V-0387 `prompts/drafts/bcreq-context-understanding-stepwise.md:613` (body) BP-01 «<!--» — `<!-- issue-490:handoff -->`
- V-0388 `prompts/drafts/bcreq-context-understanding-stepwise.md:614` (body) BP-02 «#490» — `## Итог шага для БА (#490)`
- … ещё 223 (полный список — `audit/baseline-map.json`)

## D-28

- Класс: в
- Что: docs/ba-processes/bcreq-a-in-common.md (приоритет норм; сборщик копирует в 24 черновика AIN): «у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;»
- Исправление / куда перенесено: ID RFC → правило изложено в контракте (маршрут из 24 шагов, раздел 2 после AIN-21, вопросы только Заказчику); RFC-AIN-001 — docs/rfc/2026-11-a-in-decomposition.md в спице
- Нарушений базы в группе: 48

Файлы: `docs/ba-processes/bcreq-a-in-common.md (приоритет норм; сборщик копирует в 24 черновика AIN)`

Было:
```text
у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;
```
Стало:
```text
у маршрута A-IN из 24 шагов и этого контракта: раздел 2 только после AIN-21;
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `docs/ba-processes/bcreq-a-in-common.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 25; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0888 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-0908 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-0928 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-0948 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-0968 `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-0988 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-1014 `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- V-1034 `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:45` (body) BP-13 «RFC-AIN-0» — `у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;`
- … ещё 40 (полный список — `audit/baseline-map.json`)

## D-29

- Класс: а, в
- Что: scripts/build_bcreq_step_prompts.py (заголовок блока М-4, Ш-2 и системный Ш-2): «Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):»
- Исправление / куда перенесено: указатель на реестр и ID RFC → правило чтения каталога изложено блоком ниже заголовка; источник — standards/bcreq-runtime-references.md, раздел 2.2, и RFC-RT-001 в спице
- Нарушений базы в группе: 4

Файлы: `scripts/build_bcreq_step_prompts.py (заголовок блока М-4, Ш-2 и системный Ш-2)`

Было:
```text
Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):
```
Стало:
```text
Как читать каталог:
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 3; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0692 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:502` (body) BP-13 «RFC-RT-0» — `Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):`
- V-1542 `prompts/drafts/system/bcreq-products-impact-analysis-system.md:512` (body) BP-13 «RFC-RT-0» — `Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):`
- V-4164 `site/data/test-kit.json:497` (steps[].system.body) BP-13 «RFC-RT-0» — `Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):`
- V-4231 `site/data/test-kit.json:486` (steps[].draft.body) BP-13 «RFC-RT-0» — `Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):`

## D-30

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py (TERMS, строка receipt): «расхождения с блоком «по тесту»»
- Исправление / куда перенесено: название блока — BLOCK_HEADING сборщика (блок переименован записью D-14); смысл строки receipt не изменён
- Нарушений базы в группе: 33

Файлы: `scripts/build_bcreq_step_prompts.py (TERMS, строка receipt)`

Было:
```text
расхождения с блоком «по тесту»
```
Стало:
```text
расхождения с блоком «Стандарты шага»
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 17; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0281 `prompts/drafts/bcreq-constitution-governance-oneshot.md:513` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0325 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:246` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0377 `prompts/drafts/bcreq-context-understanding-stepwise.md:443` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0422 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:246` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0475 `prompts/drafts/bcreq-fr-documentation-stepwise.md:374` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0528 `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:221` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0572 `prompts/drafts/bcreq-nfr-documentation-stepwise.md:245` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- V-0620 `prompts/drafts/bcreq-orr-solution-design-stepwise.md:321` (body) BP-06 «по тесту» — `…непрочитанные источники, ограничения, расхождения с блоком «по тесту»;…`
- … ещё 25 (полный список — `audit/baseline-map.json`)

## A-01

- Класс: а
- Что: scripts/generate-pages-data.mjs (repoUrl), site/app.js (repoHref): «https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/<путь> в полях url/promptPath/sourc»
- Исправление / куда перенесено: СУПЕР-ПРАВИЛО: данные сайта без приватных URL
- Нарушений базы в группе: 0

Файлы: `scripts/generate-pages-data.mjs (repoUrl)`, `site/app.js (repoHref)`

Было:
```text
https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/<путь> в полях url/promptPath/sourceUrl site/data/*.json
```
Стало:
```text
<путь от корня репо>; ссылку сопровождающего строит интерфейс (REPO_BLOB + repoHref)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/generate-pages-data.mjs`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- `site/app.js`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

## A-02

- Класс: а
- Что: standards/bcreq-prompt-profiles.md (GE-01; сборщик копирует правило в 9 черновиков): «Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела (`standards/bcreq-sections/NN-*.»
- Исправление / куда перенесено: указатель на файл спицы → раздел «4. Правила раздела» того же промпта; профиль 0.1.3
- Нарушений базы в группе: 19

Файлы: `standards/bcreq-prompt-profiles.md (GE-01; сборщик копирует правило в 9 черновиков)`

Было:
```text
Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела (`standards/bcreq-sections/NN-*.md`); стиль
```
Стало:
```text
Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела (раздел «Правила раздела» промпта шага); стиль
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-prompt-profiles.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 10; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0332 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:316` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0384 `prompts/drafts/bcreq-context-understanding-stepwise.md:549` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0429 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:316` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0482 `prompts/drafts/bcreq-fr-documentation-stepwise.md:444` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0579 `prompts/drafts/bcreq-nfr-documentation-stepwise.md:315` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0627 `prompts/drafts/bcreq-orr-solution-design-stepwise.md:391` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0827 `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:310` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- V-0873 `prompts/drafts/bcreq-uc-modeling-stepwise.md:360` (body) A-SPOKE-PATH «standards/bcreq-sections/NN-*.md» — `- **GE-01.** Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела ('standards/bcreq-sections/NN-*.md'); стиль проверяется без утраты смысла`
- … ещё 11 (полный список — `audit/baseline-map.json`)

## A-03

- Класс: а
- Что: prompts/bcreq-constitution-governance-oneshot.md (раздел 4.1): «Стандарт каждого раздела — файл `NN-*.md` в»
- Исправление / куда перенесено: указатель на каталог спицы → раздел «Правила раздела» промпта шага (Ш-0 передаётся в каждый шаг)
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md (раздел 4.1)`

Было:
```text
Стандарт каждого раздела — файл `NN-*.md` в
standards/bcreq-sections.
```
Стало:
```text
Правила каждого раздела — в разделе «Правила раздела» промпта его шага.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 2; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0021 `prompts/bcreq-constitution-governance-oneshot.md:180` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-0022 `prompts/bcreq-constitution-governance-oneshot.md:180` (body) A-SPOKE-PATH «standards/bcreq-sections» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-0228 `prompts/drafts/bcreq-constitution-governance-oneshot.md:192` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-0229 `prompts/drafts/bcreq-constitution-governance-oneshot.md:192` (body) A-SPOKE-PATH «standards/bcreq-sections» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-3406 `site/data/prompts.json:180` (prompts[].content) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-3407 `site/data/prompts.json:180` (prompts[].content) A-SPOKE-PATH «standards/bcreq-sections» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-3460 `site/data/prompts.json:169` (prompts[].body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- V-3461 `site/data/prompts.json:169` (prompts[].body) A-SPOKE-PATH «standards/bcreq-sections» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## A-04

- Класс: а
- Что: prompts/bcreq-constitution-governance-oneshot.md (раздел 4.2): «Полный текст —»
- Исправление / куда перенесено: стили изложены в разделе 4.2 Ш-0 целиком; полный текст README §2 — в спице standards/bcreq-sections/README.md
- Нарушений базы в группе: 10

Файлы: `prompts/bcreq-constitution-governance-oneshot.md (раздел 4.2)`

Было:
```text
Полный текст —
README §2.
```
Стало:
```text
— (строка удалена)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-constitution-governance-oneshot.md`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0023 `prompts/bcreq-constitution-governance-oneshot.md:200` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-0024 `prompts/bcreq-constitution-governance-oneshot.md:200` (body) A-SPOKE-PATH «README §2» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-0230 `prompts/drafts/bcreq-constitution-governance-oneshot.md:212` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-0231 `prompts/drafts/bcreq-constitution-governance-oneshot.md:212` (body) A-SPOKE-PATH «README §2» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-3408 `site/data/prompts.json:200` (prompts[].content) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-3409 `site/data/prompts.json:200` (prompts[].content) A-SPOKE-PATH «README §2» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-3462 `site/data/prompts.json:189` (prompts[].body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- V-3463 `site/data/prompts.json:189` (prompts[].body) A-SPOKE-PATH «README §2» — `[README §2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили).`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## A-05

- Класс: а
- Что: standards/bcreq-manual-classes/05-taxonomy.md (шаг 2), standards/bcreq-manual-classes/catalog.json (К-05 behavior): «Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители»
- Исправление / куда перенесено: путь спицы → роль носителя; поле попадает в site/data (каталог классов)
- Нарушений базы в группе: 3

Файлы: `standards/bcreq-manual-classes/05-taxonomy.md (шаг 2)`, `standards/bcreq-manual-classes/catalog.json (К-05 behavior)`

Было:
```text
Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители
```
Стало:
```text
Каталог продуктов репозитория и runtime-каталог taxonomy/products.yaml — разные носители
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-manual-classes/05-taxonomy.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- `standards/bcreq-manual-classes/catalog.json`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 1; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1576 `standards/bcreq-manual-classes/05-taxonomy.md:103` (body) A-SPOKE-PATH «docs/taxonomy» — `…л классификации, а не отсутствие функции. Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители, указать фактический.…`
- V-2779 `site/data/prompts.json:103` (prompts[].content) A-SPOKE-PATH «docs/taxonomy» — `…л классификации, а не отсутствие функции. Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители, указать фактический.…`
- V-2786 `site/data/prompts.json:95` (prompts[].body) A-SPOKE-PATH «docs/taxonomy» — `…л классификации, а не отсутствие функции. Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители, указать фактический.…`

## A-06

- Класс: а
- Что: prompts/bcreq-orr-solution-design-stepwise.md (раздел 4), prompts/bcreq-fr-documentation-stepwise.md (раздел 4): «- Правила вывода структуры — справочник стандартов.»
- Исправление / куда перенесено: отсылка к справочнику спицы → правило в самом промпте (метамодель C4/ODA; группировка BABOK); источник — standards/bcreq-industry-practice.md, разделы 2 и 3, в спице
- Нарушений базы в группе: 2

Файлы: `prompts/bcreq-orr-solution-design-stepwise.md (раздел 4)`, `prompts/bcreq-fr-documentation-stepwise.md (раздел 4)`

Было:
```text
- Правила вывода структуры — справочник стандартов.
- Группировка и пункты BABOK — справочник стандартов.
```
Стало:
```text
- Структура раздела выводится из метамодели выбранного стандарта (C4 или TM Forum ODA), а не из номеров ФТ.
- Группировка — по BABOK Guide v3: блок — одна бизнес-возможность (10.6), порядок внутри блока — категории 7.1, как в шаге группировки выше.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `prompts/bcreq-orr-solution-design-stepwise.md`: «было» в тексте — нет; «стало» — 0/2 фрагментов
- `prompts/bcreq-fr-documentation-stepwise.md`: «было» в тексте — нет; «стало» — 0/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-0456 `prompts/drafts/bcreq-fr-documentation-stepwise.md:184` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- Группировка и пункты BABOK — [справочник стандартов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-b…`
- V-0601 `prompts/drafts/bcreq-orr-solution-design-stepwise.md:116` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- Правила вывода структуры — [справочник стандартов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раз…`

## M-01

- Класс: а
- Что: Ручные исходники промптов и ССОТ: ссылки на спицу (абсолютные и относительные) → подпись ссылки
- Исправление / куда перенесено: experiments/issue_495/clean_sources.py → prompt_purity.project (delink)
- Нарушений базы в группе: 332

Локаторы базы (выборка):
- V-0011 `prompts/bcreq-constitution-governance-oneshot.md:99` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты разделов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md)`
- V-0012 `prompts/bcreq-constitution-governance-oneshot.md:100` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Архитектура промптов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)`
- V-0013 `prompts/bcreq-constitution-governance-oneshot.md:101` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Контракт стадий и гейтов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md)`
- V-0014 `prompts/bcreq-constitution-governance-oneshot.md:102` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Стандарт композиции продуктов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md)`
- V-0015 `prompts/bcreq-constitution-governance-oneshot.md:120` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай:`
- V-0020 `prompts/bcreq-constitution-governance-oneshot.md:157` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `6. Попроси ввести следующий промпт — [Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md)`
- V-0040 `prompts/bcreq-constitution-governance-oneshot.md:286` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…артами | Ш-0 | A-IN | [bcreq-intake-questionnaire-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questio…`
- V-0041 `prompts/bcreq-constitution-governance-oneshot.md:287` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…ы Заказчика | A-IN | [bcreq-context-understanding-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding…`
- … ещё 324 (полный список — `audit/baseline-map.json`)

Файлов группы: 54; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-02

- Класс: в
- Что: Ручные исходники: служебные HTML-комментарии удалены
- Исправление / куда перенесено: experiments/issue_495/clean_sources.py → prompt_purity.project (strip_comments)
- Нарушений базы в группе: 58

Локаторы базы (выборка):
- V-0006 `prompts/bcreq-constitution-governance-oneshot.md:12` (body) BP-01 «<!--» — `<!-- issue-474:entry -->`
- V-0010 `prompts/bcreq-constitution-governance-oneshot.md:85` (body) BP-01 «<!--» — `<!-- /issue-474:entry -->`
- V-0057 `prompts/bcreq-constitution-governance-oneshot.md:375` (body) BP-01 «<!--» — `<!-- issue-395: runtime-fallback -->`
- V-0059 `prompts/bcreq-constitution-governance-oneshot.md:479` (body) BP-01 «<!--» — `<!-- /issue-395: runtime-fallback -->`
- V-0062 `prompts/bcreq-constraints-documentation-stepwise.md:110` (body) BP-01 «<!--» — `<!-- issue-395: runtime-fallback -->`
- V-0064 `prompts/bcreq-constraints-documentation-stepwise.md:214` (body) BP-01 «<!--» — `<!-- /issue-395: runtime-fallback -->`
- V-0065 `prompts/bcreq-context-understanding-stepwise.md:12` (body) BP-01 «<!--» — `<!-- issue-474:entry -->`
- V-0069 `prompts/bcreq-context-understanding-stepwise.md:85` (body) BP-01 «<!--» — `<!-- /issue-474:entry -->`
- … ещё 50 (полный список — `audit/baseline-map.json`)

Файлов группы: 21; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-03

- Класс: а
- Что: Архив 2.7.0 и прежних редакций: ссылки на спицу → подпись; хэши оригинала — в манифесте архива
- Исправление / куда перенесено: clean_sources.py; prompts/archive/a-in-v2.7.0/manifest.json
- Нарушений базы в группе: 76

Локаторы базы (выборка):
- V-1784 `prompts/archive/constraints-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1785 `prompts/archive/constraints-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1786 `prompts/archive/constraints-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1787 `prompts/archive/constraints-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1788 `prompts/archive/fr-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1789 `prompts/archive/fr-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1790 `prompts/archive/fr-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1791 `prompts/archive/fr-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- … ещё 68 (полный список — `audit/baseline-map.json`)

Файлов группы: 22; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-04

- Класс: а
- Что: Служебные файлы рядом с промптами (README, манифесты, каталог): ссылки на спицу → пути от корня
- Исправление / куда перенесено: ручная правка + сборщики манифестов
- Нарушений базы в группе: 109

Локаторы базы (выборка):
- V-1898 `prompts/README.md:9` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- "https://github.com/G-Ivan-A/mango_ba_prompts/issues/65"`
- V-1899 `prompts/README.md:26` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>`
- V-1900 `prompts/README.md:28` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>.`
- V-1901 `prompts/README.md:34` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…ения (BCREQ) | ['bcreq-constitution-governance-oneshot.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governan…`
- V-1902 `prompts/README.md:35` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…осы заказчику | ['bcreq-context-understanding-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding…`
- V-1903 `prompts/README.md:35` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…осы заказчику | ['bcreq-context-understanding-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding…`
- V-1904 `prompts/README.md:36` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `… и команды | ['bcreq-products-impact-analysis-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analy…`
- V-1905 `prompts/README.md:37` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…tory или Use Case | ['bcreq-scenarios-modeling-oneshot.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-on…`
- … ещё 101 (полный список — `audit/baseline-map.json`)

Файлов группы: 1; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-05

- Класс: а
- Что: Ссылки на спицу, которые строят сами сборщики (REPO_BLOB, AIN_BLOB, SYSTEM_BLOB, ISSUE): проекция на выходе сборщика → подпись ссылки
- Исправление / куда перенесено: prompt_purity.project в build_bcreq_step_prompts, build_bcreq_a_in, build_bcreq_system_track; сторож test_builders_check
- Нарушений базы в группе: 64

Локаторы базы (выборка):
- V-0226 `prompts/drafts/bcreq-constitution-governance-oneshot.md:169` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[AIN-01](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md), в системном —`
- V-0247 `prompts/drafts/bcreq-constitution-governance-oneshot.md:298` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…ндартами | Ш-0 | A-IN | [bcreq-intake-questionnaire-system](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-…`
- V-0248 `prompts/drafts/bcreq-constitution-governance-oneshot.md:299` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…нты Заказчика | A-IN | [bcreq-context-understanding-system](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-context…`
- V-0249 `prompts/drafts/bcreq-constitution-governance-oneshot.md:300` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…ла 1 | Ш-1 | A-IN | [bcreq-products-impact-analysis-system](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-product…`
- V-0260 `prompts/drafts/bcreq-constitution-governance-oneshot.md:317` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[AIN-01…AIN-24](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md)`
- V-0282 `prompts/drafts/bcreq-constitution-governance-oneshot.md:555` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…очников и уровни доверия — справочник И-7 [реестра runtime](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.…`
- V-0326 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:286` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…очников и уровни доверия — справочник И-7 [реестра runtime](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.…`
- V-0378 `prompts/drafts/bcreq-context-understanding-stepwise.md:483` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…очников и уровни доверия — справочник И-7 [реестра runtime](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.…`
- … ещё 56 (полный список — `audit/baseline-map.json`)

Файлов группы: 19; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-01

- Класс: а, б, в
- Что: Черновики, A-IN и системный трек (`prompts/drafts/**`): только копии нарушений ручных источников (окно ±15 символов вокруг нарушения есть в ручном исходнике базы); пересборка из чистых ССОТ
- Исправление / куда перенесено: сборщики bcreq_handoff, build_bcreq_a_in, build_bcreq_step_prompts, build_bcreq_system_track (проекция стандартов)
- Нарушений базы в группе: 108

Локаторы базы (выборка):
- V-0211 `prompts/drafts/bcreq-constitution-governance-oneshot.md:21` (body) BP-01 «<!--» — `<!-- issue-474:entry -->`
- V-0216 `prompts/drafts/bcreq-constitution-governance-oneshot.md:96` (body) BP-01 «<!--» — `<!-- /issue-474:entry -->`
- V-0217 `prompts/drafts/bcreq-constitution-governance-oneshot.md:110` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты разделов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md)`
- V-0218 `prompts/drafts/bcreq-constitution-governance-oneshot.md:111` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Архитектура промптов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)`
- V-0219 `prompts/drafts/bcreq-constitution-governance-oneshot.md:112` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Контракт стадий и гейтов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md)`
- V-0220 `prompts/drafts/bcreq-constitution-governance-oneshot.md:113` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Стандарт композиции продуктов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md)`
- V-0221 `prompts/drafts/bcreq-constitution-governance-oneshot.md:131` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай:`
- V-0227 `prompts/drafts/bcreq-constitution-governance-oneshot.md:170` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md). Остановись.`
- … ещё 100 (полный список — `audit/baseline-map.json`)

Файлов группы: 15; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-02

- Класс: а
- Что: Данные сайта: поля url/путь → путь от корня, ссылку строит интерфейс
- Исправление / куда перенесено: A-01: scripts/generate-pages-data.mjs (repoUrl), site/app.js (repoHref)
- Нарушений базы в группе: 352

Локаторы базы (выборка):
- V-2500 `site/data/bcreq-flow.json:1` (sourceFiles[].url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md`
- V-2501 `site/data/bcreq-flow.json:1` (manual.contract.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-manual-state.md`
- V-2502 `site/data/bcreq-flow.json:1` (manual.classes.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/README.md`
- V-2503 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/36-rule-bundle.md`
- V-2504 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/01-intake.md`
- V-2505 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/02-normalize.md`
- V-2506 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/03-ambiguity.md`
- V-2507 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/04-questions.md`
- … ещё 344 (полный список — `audit/baseline-map.json`)

Файлов группы: 10; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-03

- Класс: а, б, в
- Что: Данные сайта: тела промптов и поля карточек — только копии нарушений ручных источников (то же окно ±15 символов)
- Исправление / куда перенесено: node scripts/generate-pages-data.mjs
- Нарушений базы в группе: 905

Локаторы базы (выборка):
- V-2718 `site/data/prompts.json:15` (prompts[].content) A-RELATIVE «README.md» — `[инвентарь](README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md);`
- V-2719 `site/data/prompts.json:15` (prompts[].content) A-RELATIVE «../../prompts/bcreq-in-understanding-oneshot.md» — `[инвентарь](README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md);`
- V-2720 `site/data/prompts.json:25` (prompts[].content) A-RELATIVE «../../docs/contracts/bcreq-manual-state.md» — `[контракт состояния](../../docs/contracts/bcreq-manual-state.md).`
- V-2722 `site/data/prompts.json:141` (prompts[].content) A-RELATIVE «../../docs/analysis/2026-10-29-bcreq-checkpoint.md» — `Основания: [checkpoint](../../docs/analysis/2026-10-29-bcreq-checkpoint.md),`
- V-2723 `site/data/prompts.json:142` (prompts[].content) A-RELATIVE «../../docs/rfc/2026-10-bcreq-manual-pipeline.md» — `[RFC и маршрут](../../docs/rfc/2026-10-bcreq-manual-pipeline.md),`
- V-2724 `site/data/prompts.json:143` (prompts[].content) A-RELATIVE «../bcreq-sections/README.md» — `[мета-стандарты разделов](../bcreq-sections/README.md).`
- V-2725 `site/data/prompts.json:7` (prompts[].body) A-RELATIVE «README.md» — `[инвентарь](README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md);`
- V-2726 `site/data/prompts.json:7` (prompts[].body) A-RELATIVE «../../prompts/bcreq-in-understanding-oneshot.md» — `[инвентарь](README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md);`
- … ещё 897 (полный список — `audit/baseline-map.json`)

Файлов группы: 2; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

