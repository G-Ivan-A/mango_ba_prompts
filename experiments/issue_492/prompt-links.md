# Классификация ссылок промптов на mango_ba_prompts (issue #492, ФТ-2)

Сгенерировано `experiments/issue_492/classify_prompt_links.py`; не править вручную.
Тексты промптов не менялись: это инвентаризация, решения и задачи.

- Коммит спицы: `786f8f3d67c5a8d08ceb8abfad891dda9cf2f2f2`; SHA реестра: `68ad8fcffd47439fc3051852d9a2fbbe23815855`; main runtime: `90f082330015634f3a0632cdd31ebfe1c15fd7ae`.
- Файлов промптов: 90, со ссылками на спицу: 79; вхождений: 543; целей: 54; относительных ссылок: 0.
- Класс (а): 225 вхождений; класс (б): 318 вхождений, 25 целей.

## 1. Правила классификации (порядок применения)

| Правило | Класс | Условие | Обоснование | Вхождений |
| --- | --- | --- | --- | --- |
| А-0 | (а) | ссылка во frontmatter | Метаданные файла (related_issue и т. п.): модель их не исполняет. | 2 |
| А-1 | (а) | ссылка в HTML-комментарии | Служебная пометка (Experimental, маркер сборки): не инструкция модели. | 43 |
| А-2 | (а) | цель — issue или PR | Трассировка решения владельца; правило уже записано в тексте промпта. | 3 |
| А-3 | (а) | служебный промпт вне потока BCREQ | Промпт обслуживания сессий спицы: результат сохраняется в pr-ops спицы, обязательная структура вывода перечислена в самом тексте. | 7 |
| А-4 | (а) | абзац происхождения встроенного текста | Указывает, из чего собран или чем заменён текст; правила перенесены дословно, модели не нужно открывать источник. | 132 |
| А-5 | (а) | цель — RFC, ADR, pr-ops, runs, архив, issue-шаблоны, анализ | Документ управления и истории решений; норма для исполнения в нём не вынесена (RFC #427, раздел 8.1: правила исполнения в справочник не выносятся). | 1 |
| Б-1 | (б) | цель — конституция Ш-0 | Шаги требуют «Прочитай полную конституцию из Ш-0»: Р1…Р7, АД, АП, КС, БС и гейты действуют на каждом шаге. | 85 |
| Б-2 | (б) | цель — RFC-AIN-001 | Общий контракт A-IN: «приоритет у принятого RFC-AIN-001 и этого контракта». | 24 |
| А-6 | (а) | цель — другой промпт набора без якоря | Навигация: модель называет следующий промпт, текст промпта вводит БА. | 37 |
| Б-3 | (б) | цель — правило другого промпта по якорю | Шаг ссылается на конкретное правило другого шага как на действующую норму. | 6 |
| Б-4 | (б) | цель — реестр справочников runtime | БС-18 «промпт ДОЛЖЕН ссылаться» на И-7; AIN «Runtime: версии и источники». | 43 |
| Б-5 | (б) | цель — стандарт в standards/ | Мета-стандарт или стандарт, по которому модель строит вывод шага. | 104 |
| Б-6 | (б) | цель — контракт в docs/contracts/ | Контракт гейтов и возвратов, по которому шаг принимает решение. | 15 |
| Б-7 | (б) | цель — процесс в docs/ba-processes/ | Процессный SSOT (итог шага, исполнение A-IN, поток CS), читаемый шагом. | 41 |

## 2. Свод по группам промптов

| Группа | (а) | (б) |
| --- | --- | --- |
| AIN v0.3 | 24 | 120 |
| v0.1 (14 промптов) | 23 | 80 |
| архив 2.7.0 | 19 | 26 |
| архив до BCREQ | 31 | 0 |
| системный формат | 21 | 18 |
| служебные промпты | 9 | 0 |
| черновики Ш-ХХ | 98 | 74 |

## 3. Цели класса (б): решение

| Цель | Вхождений (б/всего) | Промптов | Есть в runtime | Решение | Карточка | Примечание |
| --- | --- | --- | --- | --- | --- | --- |
| `prompts/bcreq-constitution-governance-oneshot.md` | 80/80 | 54 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `standards/bcreq-runtime-references.md` | 43/62 | 43 | `docs/kb/MAP.json`, `docs/kb/USAGE.md`, `evaluation/g-human-checklist.md`, `golden/cases-analytics-reporting.yaml`, `golden/cases-voice-ucaas.yaml`, `golden/cases.yaml`, `taxonomy/domain-glossary-analytics-reporting.yaml`, `taxonomy/domain-glossary-voice-ucaas.yaml`, `taxonomy/domain-glossary.yaml`, `taxonomy/mango-products.yaml`, `taxonomy/products.yaml`, `taxonomy/source-tiers.yaml`, `templates/bcreq-skeleton.md` | кандидат на замену ссылки: справочники реестра есть в runtime на SHA реестра | BL-190 | Нормативная функция реестра для модели — указать справочники И-1…И-8 на закреплённом SHA; сами справочники есть в runtime (БС-18 → И-7 `taxonomy/source-tiers.yaml`). Замена: прямые закреплённые ссылки на справочники runtime; реестр остаётся governance-индексом спицы и входит в манифест ФТ-3. |
| `standards/bcreq-sections/README.md` | 32/32 | 28 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | В runtime есть шаблон документа `templates/bcreq-skeleton.md` (И-3), но не мета-стандарты разделов. |
| `docs/ba-processes/bcreq-step-handoff.md` | 24/24 | 24 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-186 | — |
| `docs/rfc/2026-11-a-in-decomposition.md` | 24/24 | 24 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-186 | — |
| `docs/contracts/bcreq-stage-gates.md` | 15/15 | 13 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-188 | В runtime есть только чек-лист G-human `evaluation/g-human-checklist.md` (И-8); гейты Г-IN/Г-W и возвраты — нет. |
| `standards/bcreq-composition-standard.md` | 13/13 | 11 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `docs/ba-processes/bcreq-a-in-execution.md` | 11/11 | 10 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-186 | — |
| `standards/bcreq-industry-practice.md` | 10/10 | 7 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/01-glossary.md` | 10/10 | 10 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/02-business-context.md` | 10/10 | 10 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `prompts/bcreq-context-understanding-stepwise.md` | 2/7 | 7 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `prompts/bcreq-uc-modeling-stepwise.md` | 1/7 | 5 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `docs/ba-processes/cs-flow-stub.md` | 6/6 | 6 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-188 | — |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 1/6 | 6 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `standards/bcreq-sections/07-use-cases.md` | 6/6 | 6 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 5/5 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `standards/bcreq-prompt-architecture.md` | 4/4 | 4 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/product-classification-contract.md` | 4/4 | 4 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | В runtime есть значения таксономии `taxonomy/mango-products.yaml` (И-2), но не правила классификации. |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 2/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-185 | — |
| `standards/bcreq-sections/03-functional-requirements.md` | 3/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/04-non-functional-requirements.md` | 3/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/05-solution-description.md` | 3/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/06-implementation-constraints.md` | 3/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |
| `standards/bcreq-sections/08-supplementary.md` | 3/3 | 3 | нет | нет в runtime: задача в бэклог на перенос закреплённой копией | BL-187 | — |

## 4. Цели только класса (а): обоснование

| Цель | Вхождений | Правила |
| --- | --- | --- |
| `issues/*` | 48 | А-0 ×2, А-1 ×43, А-2 ×3 |
| `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 20 | А-4 ×19, А-5 ×1 |
| `standards/bcreq-manual-classes/catalog.json` | 19 | А-4 ×19 |
| `standards/bcreq-prompt-base-standard.md` | 19 | А-4 ×19 |
| `standards/bcreq-prompt-profiles.md` | 19 | А-4 ×19 |
| `prompts/bcreq-work-solution-design-oneshot.md` | 7 | А-4 ×5, А-6 ×2 |
| `prompts/bcreq-review-validation-oneshot.md` | 6 | А-4 ×3, А-6 ×3 |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 6 | А-4 ×4, А-6 ×2 |
| `prompts/bcreq-core-documentation-oneshot.md` | 5 | А-4 ×2, А-6 ×3 |
| `prompts/bcreq-in-understanding-oneshot.md` | 5 | А-4 ×4, А-6 ×1 |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 4 | А-4 ×2, А-6 ×2 |
| `prompts/bcreq-fr-documentation-stepwise.md` | 4 | А-4 ×2, А-6 ×2 |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 4 | А-6 ×4 |
| `pr-ops/session-digests.md` | 2 | А-3 ×2 |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 2 | А-6 ×2 |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 2 | А-6 ×2 |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 2 | А-6 ×2 |
| `runs/2026/RUN-0075/outputs/error-statistics.md` | 2 | А-4 ×2 |
| `runs/2026/RUN-0075/outputs/runtime-improvements.md` | 2 | А-4 ×2 |
| `runs/2026/RUN-0075/outputs/success-criteria.md` | 2 | А-4 ×2 |
| `(корень)` | 1 | А-3 ×1 |
| `docs/adr/001-prompt-standard.md` | 1 | А-3 ×1 |
| `docs/ba-ecosystem.md` | 1 | А-3 ×1 |
| `docs/taxonomy.md` | 1 | А-3 ×1 |
| `prompts/README.executable.md` | 1 | А-3 ×1 |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 1 | А-6 ×1 |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 1 | А-6 ×1 |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 1 | А-6 ×1 |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 1 | А-6 ×1 |

## 5. Заглушки реестра справочников (ФТ-4)

| Заглушка | Справочник | Шаги | Задача runtime | Карточка |
| --- | --- | --- | --- | --- |
| З-2 | И-4 Примеры разделов | Ш-3, Ш-4, Ш-5, Ш-8, Ш-С | РТ-2 | BL-189 |

## 6. Карточки бэклога

| Карточка | Содержание |
| --- | --- |
| BL-185 | Конституция Ш-0 и промпты набора этапа 1 в runtime |
| BL-186 | Маршрут A-IN, контракты AIN и итог шага в runtime |
| BL-187 | Стандарты исполнения шагов в runtime |
| BL-188 | Контракт гейтов и поток CS в runtime |
| BL-189 | Примеры разделов И-4 (РТ-2, заглушка З-2) |
| BL-190 | Замена ссылок (б) в текстах промптов на runtime |

## 7. Все вхождения

| Промпт | Строка | Группа | Цель | Якорь | Правило | Класс |
| --- | --- | --- | --- | --- | --- | --- |
| `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md` | 10 | служебные промпты | `issues/*` | — | А-0 | (а) |
| `prompts/README.executable.md` | 10 | служебные промпты | `issues/*` | — | А-0 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 17 | архив 2.7.0 | `issues/*` | — | А-1 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 27 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 111 | архив 2.7.0 | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 143 | архив 2.7.0 | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 148 | архив 2.7.0 | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 251 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 352 | архив 2.7.0 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 353 | архив 2.7.0 | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 354 | архив 2.7.0 | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 355 | архив 2.7.0 | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 356 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 407 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 21 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 29 | архив 2.7.0 | `prompts/bcreq-core-documentation-oneshot.md` | — | А-6 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 86 | архив 2.7.0 | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 87 | архив 2.7.0 | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 88 | архив 2.7.0 | `standards/bcreq-composition-standard.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 89 | архив 2.7.0 | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 104 | архив 2.7.0 | `prompts/bcreq-context-understanding-stepwise.md` | проверка-релевантности-as-is | Б-3 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 106 | архив 2.7.0 | `prompts/bcreq-products-impact-analysis-stepwise.md` | проверка-принадлежности-доказательства | Б-3 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 172 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 15 | архив 2.7.0 | `issues/*` | — | А-1 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 23 | архив 2.7.0 | `standards/bcreq-industry-practice.md` | 1-выбор-стандартов | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 29 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 83 | архив 2.7.0 | `standards/bcreq-industry-practice.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 129 | архив 2.7.0 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 130 | архив 2.7.0 | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 131 | архив 2.7.0 | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 132 | архив 2.7.0 | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 133 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 184 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 17 | архив 2.7.0 | `issues/*` | — | А-1 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 27 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 46 | архив 2.7.0 | `standards/product-classification-contract.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 47 | архив 2.7.0 | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 89 | архив 2.7.0 | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 92 | архив 2.7.0 | `standards/bcreq-sections/01-glossary.md` | механизм-сверки | Б-5 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 169 | архив 2.7.0 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 270 | архив 2.7.0 | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 271 | архив 2.7.0 | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 272 | архив 2.7.0 | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 273 | архив 2.7.0 | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 274 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 306 | архив 2.7.0 | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 332 | архив 2.7.0 | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/archive/constraints-documentation-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-constraints-documentation-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/constraints-documentation-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/constraints-documentation-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-constraints-documentation-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/constraints-documentation-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/fr-documentation-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-fr-documentation-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/fr-documentation-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-core-documentation-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/fr-documentation-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-fr-documentation-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/fr-documentation-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-core-documentation-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/fr-validation-legacy.md` | 10 | архив до BCREQ | `prompts/bcreq-review-validation-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/fr-validation-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-review-validation-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/fr-validation-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-review-validation-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/glossary-context-understanding-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-context-understanding-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/glossary-context-understanding-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-in-understanding-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/glossary-context-understanding-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-context-understanding-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/glossary-context-understanding-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-in-understanding-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/questions-customer-understanding-legacy.md` | 10 | архив до BCREQ | `prompts/bcreq-context-understanding-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/questions-customer-understanding-legacy.md` | 10 | архив до BCREQ | `prompts/bcreq-in-understanding-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/questions-customer-understanding-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-context-understanding-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/questions-customer-understanding-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-in-understanding-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-legacy.md` | 10 | архив до BCREQ | `prompts/bcreq-orr-solution-design-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-legacy.md` | 10 | архив до BCREQ | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-orr-solution-design-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-orr-solution-design-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/technical-details-solution-design-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/uc-modeling-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/uc-modeling-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/uc-modeling-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-4 | (а) |
| `prompts/archive/uc-modeling-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/us-modeling-oneshot.md` | 10 | архив до BCREQ | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-4 | (а) |
| `prompts/archive/us-modeling-stepwise.md` | 10 | архив до BCREQ | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-4 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 99 | v0.1 (14 промптов) | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 100 | v0.1 (14 промптов) | `standards/bcreq-prompt-architecture.md` | — | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 101 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 102 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | — | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 120 | v0.1 (14 промптов) | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 132 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 157 | v0.1 (14 промптов) | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 180 | v0.1 (14 промптов) | `standards/bcreq-sections/README.md` | 1-восемь-разделов | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 200 | v0.1 (14 промптов) | `standards/bcreq-sections/README.md` | 2-стили | Б-5 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 227 | v0.1 (14 промптов) | `runs/2026/RUN-0075/outputs/error-statistics.md` | — | А-4 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 229 | v0.1 (14 промптов) | `runs/2026/RUN-0075/outputs/success-criteria.md` | — | А-4 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 231 | v0.1 (14 промптов) | `runs/2026/RUN-0075/outputs/runtime-improvements.md` | — | А-4 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 286 | v0.1 (14 промптов) | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 287 | v0.1 (14 промптов) | `prompts/bcreq-context-understanding-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 288 | v0.1 (14 промптов) | `prompts/bcreq-products-impact-analysis-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 289 | v0.1 (14 промптов) | `prompts/bcreq-fr-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 290 | v0.1 (14 промптов) | `prompts/bcreq-nfr-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 291 | v0.1 (14 промптов) | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 292 | v0.1 (14 промптов) | `prompts/bcreq-orr-solution-design-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 293 | v0.1 (14 промптов) | `prompts/bcreq-constraints-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 294 | v0.1 (14 промптов) | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 295 | v0.1 (14 промптов) | `prompts/bcreq-extra-risk-analysis-stepwise.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 296 | v0.1 (14 промптов) | `prompts/bcreq-review-validation-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 297 | v0.1 (14 промптов) | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 304 | v0.1 (14 промптов) | `prompts/bcreq-in-understanding-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 306 | v0.1 (14 промптов) | `prompts/bcreq-core-documentation-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 308 | v0.1 (14 промптов) | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 323 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | 3-возвраты | Б-6 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 327 | v0.1 (14 промптов) | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 386 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 18 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 67 | v0.1 (14 промптов) | `standards/bcreq-sections/06-implementation-constraints.md` | — | Б-5 | (б) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 121 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 94 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 178 | v0.1 (14 промптов) | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 210 | v0.1 (14 промптов) | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 215 | v0.1 (14 промптов) | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/bcreq-context-understanding-stepwise.md` | 318 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 97 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 109 | v0.1 (14 промптов) | `prompts/bcreq-work-solution-design-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-core-documentation-oneshot.md` | 150 | v0.1 (14 промптов) | `standards/bcreq-sections/03-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 151 | v0.1 (14 промптов) | `standards/bcreq-sections/04-non-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 152 | v0.1 (14 промптов) | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 153 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/bcreq-core-documentation-oneshot.md` | 219 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 18 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 65 | v0.1 (14 промптов) | `standards/bcreq-sections/08-supplementary.md` | — | Б-5 | (б) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 121 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 94 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 167 | v0.1 (14 промптов) | `standards/bcreq-sections/03-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 175 | v0.1 (14 промптов) | `standards/bcreq-industry-practice.md` | 2-babok-guide-v3-что-берём-по-пунктам | Б-5 | (б) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 249 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 97 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 105 | v0.1 (14 промптов) | `prompts/bcreq-core-documentation-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-in-understanding-oneshot.md` | 162 | v0.1 (14 промптов) | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 163 | v0.1 (14 промптов) | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 164 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | — | Б-5 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 165 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 180 | v0.1 (14 промптов) | `prompts/bcreq-context-understanding-stepwise.md` | проверка-релевантности-as-is | Б-3 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 182 | v0.1 (14 промптов) | `prompts/bcreq-products-impact-analysis-stepwise.md` | проверка-принадлежности-доказательства | Б-3 | (б) |
| `prompts/bcreq-in-understanding-oneshot.md` | 248 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 18 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 65 | v0.1 (14 промптов) | `standards/bcreq-sections/04-non-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 120 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 20 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 97 | v0.1 (14 промптов) | `standards/bcreq-sections/05-solution-description.md` | — | Б-5 | (б) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 98 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | 2-правила-композиции | Б-5 | (б) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 107 | v0.1 (14 промптов) | `standards/bcreq-industry-practice.md` | 3-раздел-5-выбор-между-c4-и-tm-forum-oda | Б-5 | (б) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 196 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 23 | v0.1 (14 промптов) | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 94 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 113 | v0.1 (14 промптов) | `standards/product-classification-contract.md` | — | Б-5 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 114 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 156 | v0.1 (14 промптов) | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 159 | v0.1 (14 промптов) | `standards/bcreq-sections/01-glossary.md` | механизм-сверки | Б-5 | (б) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 236 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-review-validation-oneshot.md` | 21 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-review-validation-oneshot.md` | 65 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/bcreq-review-validation-oneshot.md` | 66 | v0.1 (14 промптов) | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/bcreq-review-validation-oneshot.md` | 137 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 21 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 63 | v0.1 (14 промптов) | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 65 | v0.1 (14 промптов) | `standards/bcreq-prompt-architecture.md` | — | Б-5 | (б) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 115 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 21 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 83 | v0.1 (14 промптов) | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 156 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 21 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 34 | v0.1 (14 промптов) | `prompts/bcreq-review-validation-oneshot.md` | — | А-6 | (а) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 82 | v0.1 (14 промптов) | `standards/bcreq-sections/05-solution-description.md` | — | Б-5 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 83 | v0.1 (14 промптов) | `standards/bcreq-sections/06-implementation-constraints.md` | — | Б-5 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 84 | v0.1 (14 промптов) | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 85 | v0.1 (14 промптов) | `standards/bcreq-sections/08-supplementary.md` | — | Б-5 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 86 | v0.1 (14 промптов) | `standards/bcreq-composition-standard.md` | 2-правила-композиции | Б-5 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 87 | v0.1 (14 промптов) | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 106 | v0.1 (14 промптов) | `prompts/bcreq-orr-solution-design-stepwise.md` | проверка-последовательности-и-контракта | Б-3 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 108 | v0.1 (14 промптов) | `prompts/bcreq-uc-modeling-stepwise.md` | проверка-покрытия-условий-контракта | Б-3 | (б) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 167 | v0.1 (14 промптов) | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 13 | AIN v0.3 | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 25 | AIN v0.3 | `docs/ba-processes/bcreq-step-handoff.md` | — | Б-7 | (б) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 51 | AIN v0.3 | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 52 | AIN v0.3 | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 53 | AIN v0.3 | `docs/rfc/2026-11-a-in-decomposition.md` | — | Б-2 | (б) |
| `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md` | 54 | AIN v0.3 | `standards/bcreq-runtime-references.md` | — | Б-4 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 34 | черновики Ш-ХХ | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 110 | черновики Ш-ХХ | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 111 | черновики Ш-ХХ | `standards/bcreq-prompt-architecture.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 112 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 113 | черновики Ш-ХХ | `standards/bcreq-composition-standard.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 131 | черновики Ш-ХХ | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 143 | черновики Ш-ХХ | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 169 | черновики Ш-ХХ | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 170 | черновики Ш-ХХ | `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 192 | черновики Ш-ХХ | `standards/bcreq-sections/README.md` | 1-восемь-разделов | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 212 | черновики Ш-ХХ | `standards/bcreq-sections/README.md` | 2-стили | Б-5 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 239 | черновики Ш-ХХ | `runs/2026/RUN-0075/outputs/error-statistics.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 241 | черновики Ш-ХХ | `runs/2026/RUN-0075/outputs/success-criteria.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 243 | черновики Ш-ХХ | `runs/2026/RUN-0075/outputs/runtime-improvements.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 298 | черновики Ш-ХХ | `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 299 | черновики Ш-ХХ | `prompts/drafts/system/bcreq-context-understanding-system.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 300 | черновики Ш-ХХ | `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 301 | черновики Ш-ХХ | `prompts/bcreq-fr-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 302 | черновики Ш-ХХ | `prompts/bcreq-nfr-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 303 | черновики Ш-ХХ | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 304 | черновики Ш-ХХ | `prompts/bcreq-orr-solution-design-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 305 | черновики Ш-ХХ | `prompts/bcreq-constraints-documentation-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 306 | черновики Ш-ХХ | `prompts/bcreq-uc-modeling-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 307 | черновики Ш-ХХ | `prompts/bcreq-extra-risk-analysis-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 308 | черновики Ш-ХХ | `prompts/bcreq-review-validation-oneshot.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 309 | черновики Ш-ХХ | `prompts/bcreq-scenarios-modeling-oneshot.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 317 | черновики Ш-ХХ | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 334 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | 3-возвраты | Б-6 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 338 | черновики Ш-ХХ | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 397 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 498 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 499 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 500 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 501 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 502 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 555 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 27 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 76 | черновики Ш-ХХ | `standards/bcreq-sections/06-implementation-constraints.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 130 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 231 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 232 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 233 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 234 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 235 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 286 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 32 | черновики Ш-ХХ | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 103 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 187 | черновики Ш-ХХ | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 219 | черновики Ш-ХХ | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 224 | черновики Ш-ХХ | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 327 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 428 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 429 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 430 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 431 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 432 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 483 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 27 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 74 | черновики Ш-ХХ | `standards/bcreq-sections/08-supplementary.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 130 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 231 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 232 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 233 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 234 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 235 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 286 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 32 | черновики Ш-ХХ | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 103 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 176 | черновики Ш-ХХ | `standards/bcreq-sections/03-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 184 | черновики Ш-ХХ | `standards/bcreq-industry-practice.md` | 2-babok-guide-v3-что-берём-по-пунктам | Б-5 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 258 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 359 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 360 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 361 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 362 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 363 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 414 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 15 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 24 | черновики Ш-ХХ | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md` | — | А-6 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 100 | черновики Ш-ХХ | `standards/bcreq-industry-practice.md` | 1-выбор-стандартов | Б-5 | (б) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 106 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 160 | черновики Ш-ХХ | `standards/bcreq-industry-practice.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 206 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 207 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 208 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 209 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 210 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 261 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 27 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 74 | черновики Ш-ХХ | `standards/bcreq-sections/04-non-functional-requirements.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 129 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 230 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 231 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 232 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 233 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 234 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 285 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 29 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 106 | черновики Ш-ХХ | `standards/bcreq-sections/05-solution-description.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 107 | черновики Ш-ХХ | `standards/bcreq-composition-standard.md` | 2-правила-композиции | Б-5 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 116 | черновики Ш-ХХ | `standards/bcreq-industry-practice.md` | 3-раздел-5-выбор-между-c4-и-tm-forum-oda | Б-5 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 205 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 306 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 307 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 308 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 309 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 310 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 361 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 32 | черновики Ш-ХХ | `docs/ba-processes/bcreq-a-in-execution.md` | — | Б-7 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 103 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 122 | черновики Ш-ХХ | `standards/product-classification-contract.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 123 | черновики Ш-ХХ | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 165 | черновики Ш-ХХ | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 168 | черновики Ш-ХХ | `standards/bcreq-sections/01-glossary.md` | механизм-сверки | Б-5 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 245 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 346 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 347 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 348 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 349 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 350 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 382 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 408 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 15 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 22 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 92-состав | А-5 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 126 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 127 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 128 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 129 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 130 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 162 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 188 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 30 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 74 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | 2-гейты | Б-6 | (б) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 75 | черновики Ш-ХХ | `standards/bcreq-sections/README.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 146 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 248 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 249 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 250 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 251 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 252 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 307 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 30 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 72 | черновики Ш-ХХ | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 74 | черновики Ш-ХХ | `standards/bcreq-prompt-architecture.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 124 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 225 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 226 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 227 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 228 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 229 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 280 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 17 | черновики Ш-ХХ | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 30 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 92 | черновики Ш-ХХ | `standards/bcreq-sections/07-use-cases.md` | — | Б-5 | (б) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 165 | черновики Ш-ХХ | `prompts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 266 | черновики Ш-ХХ | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 267 | черновики Ш-ХХ | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 268 | черновики Ш-ХХ | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 269 | черновики Ш-ХХ | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 270 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 304 | черновики Ш-ХХ | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 330 | черновики Ш-ХХ | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 16 | системный формат | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 27 | системный формат | `issues/*` | — | А-2 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 113 | системный формат | `prompts/drafts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 197 | системный формат | `docs/ba-processes/cs-flow-stub.md` | — | Б-7 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 229 | системный формат | `standards/bcreq-sections/01-glossary.md` | — | Б-5 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 234 | системный формат | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 337 | системный формат | `prompts/drafts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 438 | системный формат | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 439 | системный формат | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 440 | системный формат | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 441 | системный формат | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 442 | системный формат | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 493 | системный формат | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 16 | системный формат | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 27 | системный формат | `issues/*` | — | А-2 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 111 | системный формат | `standards/bcreq-industry-practice.md` | 1-выбор-стандартов | Б-5 | (б) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 117 | системный формат | `prompts/drafts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 171 | системный формат | `standards/bcreq-industry-practice.md` | — | Б-5 | (б) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 217 | системный формат | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 218 | системный формат | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 219 | системный формат | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 220 | системный формат | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 221 | системный формат | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 272 | системный формат | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 16 | системный формат | `issues/*` | — | А-1 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 27 | системный формат | `issues/*` | — | А-2 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 113 | системный формат | `prompts/drafts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 132 | системный формат | `standards/product-classification-contract.md` | — | Б-5 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 133 | системный формат | `standards/bcreq-composition-standard.md` | 4-профили-продуктов | Б-5 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 175 | системный формат | `standards/bcreq-sections/02-business-context.md` | — | Б-5 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 178 | системный формат | `standards/bcreq-sections/01-glossary.md` | механизм-сверки | Б-5 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 255 | системный формат | `prompts/drafts/bcreq-constitution-governance-oneshot.md` | — | Б-1 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 356 | системный формат | `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 93-как-промпт-собирается-из-стандартов | А-4 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 357 | системный формат | `standards/bcreq-prompt-base-standard.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 358 | системный формат | `standards/bcreq-prompt-profiles.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 359 | системный формат | `standards/bcreq-manual-classes/catalog.json` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 360 | системный формат | `standards/bcreq-runtime-references.md` | — | А-4 | (а) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 392 | системный формат | `docs/contracts/bcreq-stage-gates.md` | — | Б-6 | (б) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 418 | системный формат | `standards/bcreq-runtime-references.md` | 2-перечень | Б-4 | (б) |
| `prompts/session-debug-documentation-oneshot.md` | 58 | служебные промпты | `pr-ops/session-digests.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 103 | служебные промпты | `docs/adr/001-prompt-standard.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 105 | служебные промпты | `prompts/README.executable.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 107 | служебные промпты | `pr-ops/session-digests.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 109 | служебные промпты | `docs/taxonomy.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 111 | служебные промпты | `docs/ba-ecosystem.md` | — | А-3 | (а) |
| `prompts/session-debug-documentation-oneshot.md` | 112 | служебные промпты | `(корень)` | — | А-3 | (а) |
