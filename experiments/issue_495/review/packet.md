# Пакет двухролевой проверки реестра issue #495

База `e051e0fa`: нарушений 4542, без группы 0; текущее дерево: нарушений 0.

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
- V-0064 `prompts/bcreq-context-understanding-stepwise.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0065 `prompts/bcreq-context-understanding-stepwise.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0076 `prompts/bcreq-core-documentation-oneshot.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0077 `prompts/bcreq-core-documentation-oneshot.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0095 `prompts/bcreq-fr-documentation-stepwise.md:63` (body) CT-01 «amoCRM» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
- V-0096 `prompts/bcreq-fr-documentation-stepwise.md:63` (body) CT-02 «API-привязки» — `Задержка появления записи amoCRM не доказывает способ API-привязки по ID,`
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
- V-1798 `docs/ba-processes/bcreq-step-handoff.md:119` (body) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем. | карта компонентов-кандидатов | те…`
- V-1799 `docs/ba-processes/bcreq-step-handoff.md:119` (body) CT-05 «ЛК» — `…ов-кандидатов | технический | у каждой связи есть источник; ЛК, права и настройки рассмотрены | AIN-07 |…`
- V-3632 `site/data/step-handoff.json:1` (steps.AIN-06.goal) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.…`
- V-3637 `site/data/test-kit.json:1` (handoff.steps.AIN-06.goal) CT-03 «коннектора» — `…понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.…`

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
- V-0959 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:281` (body) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-2036 `site/data/a-in-kit.json:281` (steps[].prompt) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-3633 `site/data/step-handoff.json:1` (steps.AIN-06.check) CT-05 «ЛК» — `у каждой связи есть источник; ЛК, права и настройки рассмотрены`
- V-3634 `site/data/step-handoff.json:15` (steps.AIN-06.block) CT-05 «ЛК» — `…технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта …`
- V-3638 `site/data/test-kit.json:1` (handoff.steps.AIN-06.check) CT-05 «ЛК» — `у каждой связи есть источник; ЛК, права и настройки рассмотрены`

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
- V-0951 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:220` (body) CT-03 «коннектора» — `- Зачем: Новизна коннектора не отменяет дельту существующих подсистем.`
- V-1800 `docs/ba-processes/bcreq-a-in-route.json:167` (body) CT-03 «коннектора» — `"why": "Новизна коннектора не отменяет дельту существующих подсистем",`
- V-2012 `site/data/a-in-kit.json:1` (steps[].why) CT-03 «коннектора» — `Новизна коннектора не отменяет дельту существующих подсистем`
- V-2028 `site/data/a-in-kit.json:220` (steps[].prompt) CT-03 «коннектора» — `- Зачем: Новизна коннектора не отменяет дельту существующих подсистем.`

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
- V-0953 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:237` (body) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`
- V-1801 `docs/ba-processes/bcreq-a-in-route.json:168` (body) CT-05 «ЛК» — `"checks": "У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторо…`
- V-2013 `site/data/a-in-kit.json:1` (steps[].checks) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`
- V-2030 `site/data/a-in-kit.json:237` (steps[].prompt) CT-05 «ЛК» — `У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим…`

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
- V-0847 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0865 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0883 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0901 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0919 `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0937 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0961 `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
- V-0979 `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:13` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->`
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
- V-0952 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:229` (body) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`
- V-1803 `docs/ba-processes/bcreq-a-in-instructions.json:28` (body) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`
- V-2029 `site/data/a-in-kit.json:229` (steps[].prompt) CT-05 «ЛК» — `… → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст…`

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
- V-0954 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` (body) CT-03 «коннектор» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-0955 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` (body) CT-05 «ЛК» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-1804 `docs/ba-processes/bcreq-a-in-instructions.json:30` (body) CT-03 «коннектор» — `"negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие."`
- V-1805 `docs/ba-processes/bcreq-a-in-instructions.json:30` (body) CT-05 «ЛК» — `"negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие."`
- V-2031 `site/data/a-in-kit.json:248` (steps[].prompt) CT-03 «коннектор» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`
- V-2032 `site/data/a-in-kit.json:248` (steps[].prompt) CT-05 «ЛК» — `Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие.`

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
- V-1065 `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` (body) CT-01 «amoCRM» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-1066 `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` (body) CT-06 «HDE» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-1806 `docs/ba-processes/bcreq-a-in-instructions.json:60` (body) CT-01 «amoCRM» — `"negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»."`
- V-1807 `docs/ba-processes/bcreq-a-in-instructions.json:60` (body) CT-06 «HDE» — `"negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»."`
- V-2142 `site/data/a-in-kit.json:248` (steps[].prompt) CT-01 «amoCRM» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`
- V-2143 `site/data/a-in-kit.json:248` (steps[].prompt) CT-06 «HDE» — `Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет».`

## U-10

- Класс: б
- Что: prompts/bcreq-constitution-governance-oneshot.md: «наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
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
- V-0034 `prompts/bcreq-constitution-governance-oneshot.md:250` (body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-0236 `prompts/drafts/bcreq-constitution-governance-oneshot.md:262` (body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3281 `site/data/prompts.json:250` (prompts[].content) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3332 `site/data/prompts.json:239` (prompts[].body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`
- V-3684 `site/data/test-kit.json:246` (steps[].draft.body) CT-03 «коннекторе» — `…; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает…`

## U-11

- Класс: б
- Что: prompts/bcreq-products-impact-analysis-stepwise.md: «передачу этих функций через коннектор.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
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
- V-0150 `prompts/bcreq-products-impact-analysis-stepwise.md:177` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-0641 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:186` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-1429 `prompts/drafts/system/bcreq-products-impact-analysis-system.md:196` (body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-3532 `site/data/prompts.json:177` (prompts[].content) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-3554 `site/data/prompts.json:166` (prompts[].body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-3981 `site/data/test-kit.json:181` (steps[].system.body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`
- V-4045 `site/data/test-kit.json:170` (steps[].draft.body) CT-03 «коннектор» — `передачу этих функций через коннектор. Неподтверждённая сторона — вопрос`

## U-11b

- Класс: б
- Что: scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный): «передачу этих функций через коннектор.»
- Исправление / куда перенесено: кейс → runtime golden/prompt-regressions.yaml PR-02
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
- V-0217 `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` (body) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-0218 `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` (body) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3263 `site/data/prompts.json:124` (prompts[].content) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3264 `site/data/prompts.json:124` (prompts[].content) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3314 `site/data/prompts.json:113` (prompts[].body) CT-04 «ВАТС» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
- V-3315 `site/data/prompts.json:113` (prompts[].body) CT-05 «ЛК» — `| 'продукты' | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи | из анкеты; если не ясно — вопрос БА |`
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
- V-0140 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-04 «ВАТС» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0141 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-05 «ЛК» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0142 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-09 «— D1» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0143 `prompts/bcreq-products-impact-analysis-stepwise.md:141` (body) CT-09 «— D5» — `профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;`
- V-0144 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D6» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0145 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D11» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0146 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D8» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
- V-0147 `prompts/bcreq-products-impact-analysis-stepwise.md:142` (body) CT-09 «— D9» — `КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).`
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
- V-1464 `standards/bcreq-manual-classes/01-intake.md:96` (body) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2580 `site/data/prompts.json:1` (prompts[].descriptionLong) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2585 `site/data/prompts.json:96` (prompts[].content) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`
- V-2592 `site/data/prompts.json:88` (prompts[].body) CT-04 «ВАТС» — `…кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк…`

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
- V-0493 `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:147` (body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-1366 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:158` (body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-3759 `site/data/test-kit.json:143` (steps[].system.body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`
- V-3810 `site/data/test-kit.json:133` (steps[].draft.body) CT-04 «ВАТС» — `3. Сколько номеров Mango ВАТС?`

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
- V-0495 `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:177` (body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-1368 `prompts/drafts/system/bcreq-intake-questionnaire-system.md:188` (body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-3761 `site/data/test-kit.json:173` (steps[].system.body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`
- V-3812 `site/data/test-kit.json:163` (steps[].draft.body) CT-04 «ВАТС» — `- номера ВАТС: <…|UNKNOWN>; сторонние номера: <…|UNKNOWN>`

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
- V-3732 `site/data/test-kit.json:1` (steps[].prepare) CT-04 «ВАТС» — `Подключённые у Заказчика продукты, число операторов, номера ВАТС и сторонние номера, объём коммуникаций в месяц, если известны`

## D-01

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «Защиты выведены из 168 инцидентов прогона»
- Исправление / куда перенесено: происхождение (RUN-0075, success-criteria, runtime-improvements) → репозиторий runs/2026/RUN-0075
- Нарушений базы в группе: 15

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
- V-0022 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0023 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) BP-04 «RUN-0» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0024 `prompts/bcreq-constitution-governance-oneshot.md:227` (body) BP-04 «RUN-0» — `[RUN-0075](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md)`
- V-0025 `prompts/bcreq-constitution-governance-oneshot.md:229` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[success-criteria](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md),`
- V-0026 `prompts/bcreq-constitution-governance-oneshot.md:229` (body) BP-04 «RUN-0» — `[success-criteria](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md),`
- V-0027 `prompts/bcreq-constitution-governance-oneshot.md:231` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[runtime-improvements](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md).`
- V-0028 `prompts/bcreq-constitution-governance-oneshot.md:231` (body) BP-04 «RUN-0» — `[runtime-improvements](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md).`
- V-0229 `prompts/drafts/bcreq-constitution-governance-oneshot.md:243` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[runtime-improvements](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md).`
- … ещё 7 (полный список — `audit/baseline-map.json`)

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
- V-0029 `prompts/bcreq-constitution-governance-oneshot.md:233` (body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0030 `prompts/bcreq-constitution-governance-oneshot.md:233` (body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0231 `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` (body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-0232 `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` (body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3276 `site/data/prompts.json:233` (prompts[].content) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3277 `site/data/prompts.json:233` (prompts[].content) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3327 `site/data/prompts.json:222` (prompts[].body) BP-04 «RUN-0» — `| ID | Защита | Правило | Категория RUN-0075 |`
- V-3328 `site/data/prompts.json:222` (prompts[].body) BP-12 «Категория RUN» — `| ID | Защита | Правило | Категория RUN-0075 |`
- … ещё 2 (полный список — `audit/baseline-map.json`)

## D-03

- Класс: в
- Что: prompts/bcreq-constitution-governance-oneshot.md: «#### Дополнения по ревизии Golden Set (issue #391)»
- Исправление / куда перенесено: происхождение (issue #391, кандидаты Golden Set) → карточка Ш-0 и issue #391
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
- V-0031 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0032 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0033 `prompts/bcreq-constitution-governance-oneshot.md:243` (body) BP-12 «ревизии Golden» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0233 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0234 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-0235 `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` (body) BP-12 «ревизии Golden» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-3278 `site/data/prompts.json:243` (prompts[].content) BP-02 «#391» — `#### Дополнения по ревизии Golden Set (issue #391)`
- V-3279 `site/data/prompts.json:243` (prompts[].content) BP-03 «issue» — `#### Дополнения по ревизии Golden Set (issue #391)`
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
- V-0035 `prompts/bcreq-constitution-governance-oneshot.md:265` (body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0036 `prompts/bcreq-constitution-governance-oneshot.md:265` (body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0237 `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` (body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-0238 `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` (body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3282 `site/data/prompts.json:265` (prompts[].content) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3283 `site/data/prompts.json:265` (prompts[].content) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3333 `site/data/prompts.json:254` (prompts[].body) BP-04 «RUN-0» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
- V-3334 `site/data/prompts.json:254` (prompts[].body) BP-04 «SC-6» — `об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).`
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
- V-0063 `prompts/bcreq-context-understanding-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0075 `prompts/bcreq-core-documentation-oneshot.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0094 `prompts/bcreq-fr-documentation-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0105 `prompts/bcreq-in-understanding-oneshot.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0133 `prompts/bcreq-products-impact-analysis-stepwise.md:23` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0208 `prompts/drafts/bcreq-constitution-governance-oneshot.md:34` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- V-0340 `prompts/drafts/bcreq-context-understanding-stepwise.md:32` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Полные 24 draft контракта и инструкция БА](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md).`
- … ещё 18 (полный список — `audit/baseline-map.json`)

## D-06

- Класс: в
- Что: prompts/session-debug-documentation-oneshot.md: «можно было вставить в Issue или скопировать как блок в»
- Исправление / куда перенесено: имя файла репозитория → репозиторий pr-ops/session-digests.md
- Нарушений базы в группе: 1

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
- V-0184 `prompts/session-debug-documentation-oneshot.md:52` (body) BP-03 «Issue» — `можно было вставить в Issue или скопировать как блок в`

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
- V-0186 `prompts/session-debug-documentation-oneshot.md:102` (body) BP-04 «ADR-0» — `- Стандарт промптов (ADR-001):`

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
- V-0853 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0854 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0871 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0872 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0889 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0890 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0907 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- V-0908 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` (body) BP-02 «#490» — `Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):`
- … ещё 89 (полный список — `audit/baseline-map.json`)

## D-10

- Класс: а
- Что: docs/ba-processes/bcreq-a-in-common.md: «Источники:»
- Исправление / куда перенесено: 4 приватные ссылки → Ш-0 во входе; контракты runtime — задачи BL-241, BL-242
- Нарушений базы в группе: 196

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
- V-0855 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:51` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).`
- V-0856 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:52` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).`
- V-0857 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:53` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).`
- V-0858 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:54` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Runtime: версии и источники](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md).`
- V-0873 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:51` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).`
- V-0874 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:52` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).`
- V-0875 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:53` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).`
- V-0876 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:54` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Runtime: версии и источники](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md).`
- … ещё 188 (полный список — `audit/baseline-map.json`)

## D-11

- Класс: в
- Что: Баннер архива «(issue #388)» в 25 файлах архива
- Исправление / куда перенесено: > **Архив.** Промпт заменён
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
- V-1797 `docs/ba-processes/bcreq-step-handoff.md:7` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/490`
- V-1919 `prompts/README.executable.md:10` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"`
- V-1920 `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md:10` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"`

## D-13

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (»
- Исправление / куда перенесено: frontmatter карточки, манифест сборки
- Нарушений базы в группе: 72

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.
```
Стало:
```text
— (баннер удалён; режим — поле `mode: by-test` frontmatter)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 2

Локаторы базы (выборка):
- V-0288 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-02 «#427» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту…`
- V-0289 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-02 «#438» — `…ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-0290 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-03 «issue» — `…действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-0291 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-04 «BL-1» — `…(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-0292 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту…`
- V-0293 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту…`
- V-0294 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-08 «Черновик BL» — `…по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф…`
- V-0295 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` (body) BP-09 «действует до ADR» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту…`
- … ещё 64 (полный список — `audit/baseline-map.json`)

## D-14

- Класс: в
- Что: scripts/build_bcreq_step_prompts.py: «<!-- bl-156: by-test --> ## Дополнение «по тесту» (BL-156): стандарты шага … Блок собран с»
- Исправление / куда перенесено: версии стандартов — prompts/drafts/manifest.json
- Нарушений базы в группе: 111

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
<!-- bl-156: by-test --> ## Дополнение «по тесту» (BL-156): стандарты шага … Блок собран сборщиком … из [базового стандарта](…) … [реестра справочников runtime](…)
```
Стало:
```text
## Стандарты шага / Правила базового стандарта, профилей шага и контракты операций — с номером правила.
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 0/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0265 `prompts/drafts/bcreq-constitution-governance-oneshot.md:497` (body) BP-07 «сборщик» — `Блок собран сборщиком 'scripts/build_bcreq_step_prompts.py' по`
- V-0268 `prompts/drafts/bcreq-constitution-governance-oneshot.md:499` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `из [базового стандарта](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3,`
- V-0271 `prompts/drafts/bcreq-constitution-governance-oneshot.md:502` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[реестра справочников runtime](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5.`
- V-0308 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:230` (body) BP-07 «сборщик» — `Блок собран сборщиком 'scripts/build_bcreq_step_prompts.py' по`
- V-0311 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:232` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `из [базового стандарта](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3,`
- V-0314 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:235` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[реестра справочников runtime](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5.`
- V-0358 `prompts/drafts/bcreq-context-understanding-stepwise.md:427` (body) BP-07 «сборщик» — `Блок собран сборщиком 'scripts/build_bcreq_step_prompts.py' по`
- V-0361 `prompts/drafts/bcreq-context-understanding-stepwise.md:429` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `из [базового стандарта](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3,`
- … ещё 103 (полный список — `audit/baseline-map.json`)

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
- Исправление / куда перенесено: prompts/drafts/manifest.json → excluded_base_rules
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
- V-0276 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0277 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0278 `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` (body) BP-10 «отчёт BL» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0319 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0320 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0321 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` (body) BP-10 «отчёт BL» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0369 `prompts/drafts/bcreq-context-understanding-stepwise.md:509` (body) BP-04 «BL-1» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- V-0370 `prompts/drafts/bcreq-context-understanding-stepwise.md:509` (body) BP-10 «Не внесены» — `Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.`
- … ещё 91 (полный список — `audit/baseline-map.json`)

## D-17

- Класс: а, в
- Что: scripts/build_bcreq_step_prompts.py: «**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3: »
- Исправление / куда перенесено: контракт гейтов → runtime (BL-241)
- Нарушений базы в группе: 9

Файлы: `scripts/build_bcreq_step_prompts.py`

Было:
```text
**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3: [`docs/contracts/bcreq-stage-gates.md`](…).
```
Стало:
```text
**Запись решения гейта (К-34).** … неполна (стандарт гейтов, правило Г3).
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_step_prompts.py`: «было» в тексте — нет; «стало» — 2/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 5; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 1

Локаторы базы (выборка):
- V-0660 `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:378` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-0705 `prompts/drafts/bcreq-release-readiness-oneshot.md:158` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-0833 `prompts/drafts/bcreq-uc-modeling-stepwise.md:300` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-1448 `prompts/drafts/system/bcreq-products-impact-analysis-system.md:388` (body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-4000 `site/data/test-kit.json:373` (steps[].system.body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-4064 `site/data/test-kit.json:362` (steps[].draft.body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-4211 `site/data/test-kit.json:284` (steps[].draft.body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- V-4351 `site/data/test-kit.json:284` (steps[].draft.body) BP-04 «RUN-0» — `**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5`
- … ещё 1 (полный список — `audit/baseline-map.json`)

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
- V-0193 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0194 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-01 «<!--» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0195 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-04 «BL-1» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0196 `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` (body) BP-08 «Experimental» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0284 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0285 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-01 «<!--» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0286 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-04 «BL-1» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- V-0287 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` (body) BP-08 «Experimental» — `<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->`
- … ещё 226 (полный список — `audit/baseline-map.json`)

## D-19

- Класс: в
- Что: standards/bcreq-prompt-base-standard.md: «БС-21: … блок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 —»
- Исправление / куда перенесено: колонка «Источник» стандарта, реестр справочников раздел 4
- Нарушений базы в группе: 32

Файлы: `standards/bcreq-prompt-base-standard.md`

Было:
```text
БС-21: … блок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка …
```
Стало:
```text
БС-21: … блок заглушки раздела 4 реестра; заглушка … (история заглушек — колонка «Источник»)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-prompt-base-standard.md`: «было» в тексте — нет; «стало» — 1/2 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 17; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 3

Локаторы базы (выборка):
- V-0274 `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0275 `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0317 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0318 `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0367 `prompts/drafts/bcreq-context-understanding-stepwise.md:486` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0368 `prompts/drafts/bcreq-context-understanding-stepwise.md:486` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0410 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- V-0411 `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` (body) BP-04 «BL-1» — `…ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект…`
- … ещё 24 (полный список — `audit/baseline-map.json`)

## D-20

- Класс: в
- Что: standards/bcreq-runtime-references.md: «[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]»
- Исправление / куда перенесено: RFC #427, раздел 8.4; pr-ops/BACKLOG.md BL-155
- Нарушений базы в группе: 0

Файлы: `standards/bcreq-runtime-references.md`

Было:
```text
[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]
```
Стало:
```text
[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>]
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `standards/bcreq-runtime-references.md`: «было» в тексте — нет; «стало» — 1/1 фрагментов
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

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
- V-0861 `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0879 `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0897 `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0915 `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:265` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0933 `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:265` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0956 `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:264` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0975 `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:263` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- V-0993 `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:264` (body) BP-04 «RUN-0» — `…оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок …`
- … ещё 40 (полный список — `audit/baseline-map.json`)

## D-22

- Класс: в
- Что: scripts/build_bcreq_system_track.py: «> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архив»
- Исправление / куда перенесено: архив prompts/archive/a-in-v2.7.0 (историческая сущность)
- Нарушений базы в группе: 35

Файлы: `scripts/build_bcreq_system_track.py`

Было:
```text
> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архивный блок «Дополнение «по тесту» (BL-156)»
```
Стало:
```text
— (баннер удалён; архивный блок заменён текущим блоком «Стандарты шага»)
```

Сверка текущего дерева (машинная, по фрагментам ≥ 8 символов; описательные «стало» — проверять вручную):
- `scripts/build_bcreq_system_track.py`: «было» в тексте — нет; «стало» — удаление
- Собранные черновики и данные сайта (90 единиц): фрагментов «было» — 0; единиц с «стало» — 0; архивных карточек 2.7.0 с «было» (только проекция, п.14) — 0

Локаторы базы (выборка):
- V-1290 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-02 «#490» — `> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».…`
- V-1291 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-02 «#427» — `…едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага …`
- V-1292 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-02 «#438» — `…вует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-1293 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-03 «issue» — `… действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-1294 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-04 «BL-1» — `… (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.…`
- V-1295 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-06 «по тесту» — `…): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т…`
- V-1296 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-06 «по тесту» — `…): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т…`
- V-1297 `prompts/drafts/system/bcreq-context-understanding-system.md:18` (body) BP-08 «Черновик BL» — `… по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф…`
- … ещё 27 (полный список — `audit/baseline-map.json`)

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

## M-01

- Класс: а
- Что: Ручные исходники промптов и ССОТ: ссылки на спицу (абсолютные и относительные) → подпись ссылки
- Исправление / куда перенесено: experiments/issue_495/clean_sources.py → prompt_purity.project (delink)
- Нарушений базы в группе: 335

Локаторы базы (выборка):
- V-0011 `prompts/bcreq-constitution-governance-oneshot.md:99` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Мета-стандарты разделов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md)`
- V-0012 `prompts/bcreq-constitution-governance-oneshot.md:100` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Архитектура промптов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)`
- V-0013 `prompts/bcreq-constitution-governance-oneshot.md:101` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Контракт стадий и гейтов BCREQ](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md)`
- V-0014 `prompts/bcreq-constitution-governance-oneshot.md:102` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- [Стандарт композиции продуктов](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md)`
- V-0015 `prompts/bcreq-constitution-governance-oneshot.md:120` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай:`
- V-0018 `prompts/bcreq-constitution-governance-oneshot.md:132` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[стандарте композиции §4](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов).`
- V-0019 `prompts/bcreq-constitution-governance-oneshot.md:157` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `6. Попроси ввести следующий промпт — [Ш-А](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md)`
- V-0020 `prompts/bcreq-constitution-governance-oneshot.md:180` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `[standards/bcreq-sections](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов).`
- … ещё 327 (полный список — `audit/baseline-map.json`)

Файлов группы: 54; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-02

- Класс: в
- Что: Ручные исходники: служебные HTML-комментарии удалены
- Исправление / куда перенесено: experiments/issue_495/clean_sources.py → prompt_purity.project (strip_comments)
- Нарушений базы в группе: 58

Локаторы базы (выборка):
- V-0006 `prompts/bcreq-constitution-governance-oneshot.md:12` (body) BP-01 «<!--» — `<!-- issue-474:entry -->`
- V-0010 `prompts/bcreq-constitution-governance-oneshot.md:85` (body) BP-01 «<!--» — `<!-- /issue-474:entry -->`
- V-0054 `prompts/bcreq-constitution-governance-oneshot.md:375` (body) BP-01 «<!--» — `<!-- issue-395: runtime-fallback -->`
- V-0056 `prompts/bcreq-constitution-governance-oneshot.md:479` (body) BP-01 «<!--» — `<!-- /issue-395: runtime-fallback -->`
- V-0059 `prompts/bcreq-constraints-documentation-stepwise.md:110` (body) BP-01 «<!--» — `<!-- issue-395: runtime-fallback -->`
- V-0061 `prompts/bcreq-constraints-documentation-stepwise.md:214` (body) BP-01 «<!--» — `<!-- /issue-395: runtime-fallback -->`
- V-0062 `prompts/bcreq-context-understanding-stepwise.md:12` (body) BP-01 «<!--» — `<!-- issue-474:entry -->`
- V-0066 `prompts/bcreq-context-understanding-stepwise.md:85` (body) BP-01 «<!--» — `<!-- /issue-474:entry -->`
- … ещё 50 (полный список — `audit/baseline-map.json`)

Файлов группы: 21; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-03

- Класс: а
- Что: Архив 2.7.0 и прежних редакций: ссылки на спицу → подпись; хэши оригинала — в манифесте архива
- Исправление / куда перенесено: clean_sources.py; prompts/archive/a-in-v2.7.0/manifest.json
- Нарушений базы в группе: 76

Локаторы базы (выборка):
- V-1696 `prompts/archive/constraints-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1697 `prompts/archive/constraints-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1698 `prompts/archive/constraints-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1699 `prompts/archive/constraints-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…н набором BCREQ: [bcreq-constraints-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documenta…`
- V-1700 `prompts/archive/fr-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1701 `prompts/archive/fr-documentation-oneshot.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1702 `prompts/archive/fr-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- V-1703 `prompts/archive/fr-documentation-stepwise.md:10` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…пт заменён набором BCREQ: [bcreq-fr-documentation-stepwise](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-step…`
- … ещё 68 (полный список — `audit/baseline-map.json`)

Файлов группы: 22; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## M-04

- Класс: а
- Что: Служебные файлы рядом с промптами (README, манифесты, каталог): ссылки на спицу → пути от корня
- Исправление / куда перенесено: ручная правка + сборщики манифестов
- Нарушений базы в группе: 109

Локаторы базы (выборка):
- V-1810 `prompts/README.md:9` (frontmatter) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `- "https://github.com/G-Ivan-A/mango_ba_prompts/issues/65"`
- V-1811 `prompts/README.md:26` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md>`
- V-1812 `prompts/README.md:28` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `<https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>.`
- V-1813 `prompts/README.md:34` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…ения (BCREQ) | ['bcreq-constitution-governance-oneshot.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governan…`
- V-1814 `prompts/README.md:35` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…осы заказчику | ['bcreq-context-understanding-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding…`
- V-1815 `prompts/README.md:35` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…осы заказчику | ['bcreq-context-understanding-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding…`
- V-1816 `prompts/README.md:36` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `… и команды | ['bcreq-products-impact-analysis-stepwise.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analy…`
- V-1817 `prompts/README.md:37` (body) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `…tory или Use Case | ['bcreq-scenarios-modeling-oneshot.md'](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-on…`
- … ещё 101 (полный список — `audit/baseline-map.json`)

Файлов группы: 1; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-01

- Класс: а, б, в
- Что: Черновики, A-IN и системный трек (`prompts/drafts/**`): пересборка из чистых ССОТ и сборщиков
- Исправление / куда перенесено: сборщики bcreq_handoff, build_bcreq_a_in, build_bcreq_step_prompts, build_bcreq_system_track (проекция стандартов)
- Нарушений базы в группе: 622

Локаторы базы (выборка):
- V-0197 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#427» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0198 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#438» — `…ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко…`
- V-0199 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-02 «#490» — `…438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.…`
- V-0200 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-03 «issue» — `…действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» …`
- V-0201 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-04 «BL-1» — `…(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по…`
- V-0202 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0203 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-06 «по тесту» — `> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата …`
- V-0204 `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` (body) BP-08 «Черновик BL» — `…по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);…`
- … ещё 614 (полный список — `audit/baseline-map.json`)

Файлов группы: 41; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-02

- Класс: а
- Что: Данные сайта: поля url/путь → путь от корня, ссылку строит интерфейс
- Исправление / куда перенесено: A-01: scripts/generate-pages-data.mjs (repoUrl), site/app.js (repoHref)
- Нарушений базы в группе: 352

Локаторы базы (выборка):
- V-2364 `site/data/bcreq-flow.json:1` (sourceFiles[].url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md`
- V-2365 `site/data/bcreq-flow.json:1` (manual.contract.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-manual-state.md`
- V-2366 `site/data/bcreq-flow.json:1` (manual.classes.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/README.md`
- V-2367 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/36-rule-bundle.md`
- V-2368 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/01-intake.md`
- V-2369 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/02-normalize.md`
- V-2370 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/03-ambiguity.md`
- V-2371 `site/data/bcreq-flow.json:1` (manual.steps[].prompt.url) A-PRIVATE «https://github.com/G-Ivan-A/mango_ba_prompts» — `https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/04-questions.md`
- … ещё 344 (полный список — `audit/baseline-map.json`)

Файлов группы: 10; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

## G-03

- Класс: а, б, в
- Что: Данные сайта: тела промптов и поля карточек — копия очищенных источников
- Исправление / куда перенесено: node scripts/generate-pages-data.mjs
- Нарушений базы в группе: 1631

Локаторы базы (выборка):
- V-1925 `site/data/a-in-kit.json:17` (steps[].prompt) BP-08 «Draft для» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-1926 `site/data/a-in-kit.json:17` (steps[].prompt) BP-09 «эффективность модели» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-1927 `site/data/a-in-kit.json:17` (steps[].prompt) BP-09 «не измерен» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-1937 `site/data/a-in-kit.json:266` (steps[].prompt) BP-01 «<!--» — `<!-- issue-490:handoff -->`
- V-1938 `site/data/a-in-kit.json:267` (steps[].prompt) BP-02 «#490» — `## Итог шага для БА (#490)`
- V-1939 `site/data/a-in-kit.json:288` (steps[].prompt) BP-01 «<!--» — `<!-- /issue-490:handoff -->`
- V-1943 `site/data/a-in-kit.json:17` (steps[].prompt) BP-08 «Draft для» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- V-1944 `site/data/a-in-kit.json:17` (steps[].prompt) BP-09 «эффективность модели» — `Draft для ручной проверки БА; эффективность модели не измерена.`
- … ещё 1623 (полный список — `audit/baseline-map.json`)

Файлов группы: 3; удалено из дерева: 0; нарушений в текущих версиях этих файлов: 0.

