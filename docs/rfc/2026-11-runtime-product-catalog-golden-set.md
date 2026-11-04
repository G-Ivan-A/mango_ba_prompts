---
status: accepted
version: 0.4
updated: 2026-11-04
temperature: 0.1
owner: G-Ivan-A
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/434"
related_issues: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/427, https://github.com/G-Ivan-A/mango_ba_prompts/issues/430, https://github.com/G-Ivan-A/mango_ba_prompts/pull/431, https://github.com/G-Ivan-A/mango_ba_prompts/issues/434, https://github.com/G-Ivan-A/mango_ba_prompts/issues/442, https://github.com/G-Ivan-A/mango_ba_prompts/issues/444"
rfc-scope: multi
type: rfc
related_artifacts: "standards/bcreq-runtime-references.md, docs/taxonomy/products.json, docs/rfc/2026-11-bcreq-flow-processes-prompts.md, prompts/bcreq-products-impact-analysis-stepwise.md, experiments/issue_434/prototype/mango-products.yaml, experiments/issue_434/runtime_smoke_sim.sh, pr-ops/BACKLOG.md, pr-ops/backlog-ba-model.md, docs/hub-research-dependencies.md, standards/product-classification-contract.md, experiments/issue_434/industry_taxonomy_inventory.py, experiments/issue_442/runtime_readiness.py, experiments/issue_444/runtime_readiness.py"
---

# RFC-RT-001: Каталог продуктов и golden set по классам для `mango-ba-ai-runtime` (РТ-1, РТ-3; #434)

## Summary / BLUF

[PR #431](https://github.com/G-Ivan-A/mango_ba_prompts/pull/431) оставил
владельцу шаг: «создать задачи РТ-1…РТ-4 в `mango-ba-ai-runtime`… Самые
ценные — РТ-1 (каталог функций для `c-in`) и РТ-3 (golden set по классам
продукта, требование issue #427). Без них BL-156 выйдет с заглушками».
Этот RFC — готовая к копированию постановка этих задач. Он проверен на
runtime `5d8c201511fd730a596c9f9b4588470a7b01edc9`, на каталоге спицы
`docs/taxonomy/products.json` 2026-10-28.1 и на Хабе
`c06075d0b45da70cb68e2df3851b861b5ec3aed1`.

Главное:

1. **Заглушка таксономии подтверждена.** В runtime нет ни одного
   значения ниже продуктового класса. `c-in.products[].atomic_function` —
   свободная строка. Ни одна из шести функций, которые названы в эталонах
   `golden/*.md`, не существует в каталоге продуктов (раздел 1).
2. **ССОТ значений — каталог спицы.** Это `docs/taxonomy/products.json`
   v2026-10-28.1: 353 узла, 152 атомарные функции, вся продуктовая линейка.
   **Форма — Хаб**: там уже есть файл `taxonomy/mango-products.yaml` и
   полная цепочка в `c-in`. **Нормативная часть** правится только задачей
   в Хабе и новой компиляцией (правило 13 `AGENTS.md` runtime).
3. **РТ-1 разделён на две задачи.**
   - **РТ-1** (runtime, данные) кладёт закрытый каталог
     `taxonomy/mango-products.yaml` со всеми 353 узлами. Каталог
     записывается в манифест как копия, по прецеденту базы знаний.
     Проверки `tests/runtime-smoke.sh` падают, если каталога нет или
     эталон ссылается на функцию вне каталога.
   - **ХАБ-1** (Хаб, норма) превращает `atomic_function` в ссылку на
     id каталога и добавляет каталог в `G-mach`.
4. **РТ-3** вводит golden set на каждый класс. Это файлы
   `golden/cases-<класс>.yaml`. У каждого случая обязательны поля
   `product_class` и `atomic_function` из каталога. Минимальный состав
   задан по классу. Есть подтверждение человеком и источник отбора.
5. **Механизм против заглушки** — шесть звеньев М-1…М-6 (раздел 4). Каждое
   звено fail-closed. Промпт читает каталог по SHA из реестра спицы.
   Пока звено не выполнено, промпт явно ставит заглушку З-1, а не
   угадывает значение.
6. **Решение владельца Р-17 принято** ([комментарий владельца](https://github.com/G-Ivan-A/mango_ba_prompts/pull/437#issuecomment-6605372609),
   2026-11-03). 74 узла с портала переведены из `added-for-review` в
   `lifecycle: accepted`, каталог 2026-10-28.1 получил `status: accepted`.
   Условие по таксономии для запуска РТ-1 в runtime выполнено.
7. **Происхождение таксономии проверено (версия 0.2, комментарий
   владельца к PR #437).** Таксономия Mango разработана в Хабе, в
   `research/mango/2026-05-22-classification.md` v3.0. Каталог спицы
   построен из этого файла: 279 из 353 узлов имеют `origin: inherited`.
   В том же файле есть индустриальный слой: TM Forum, UNSPSC, ОКПД 2 и
   ГОСТ/НПА для 42 строк классов. Каталог связан с ним только номером
   строки `row`. Ни каталог, ни runtime индустриальных полей не хранят.
   Сопоставление нужно будущему потоку оценки тендерного ТЗ. По указанию
   владельца для него заведена только задача BL-164 в бэклоге спицы
   (подраздел 3.1). РТ-1 и РТ-3 этим не меняются.
8. **Поправка 0.3 (issue [#442](https://github.com/G-Ivan-A/mango_ba_prompts/issues/442)):
   М-1…М-3 исполнены.** РТ-1 слита в runtime
   ([PR #16](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/16), `2db0ef51`),
   ХАБ-1 слита в Хаб ([PR #720](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/720)).
   BL-163 перевёл реестр справочников на этот срез: И-2 — «Да», З-1 снята.
   Копия каталога в runtime старше решения Р-17 (74 узла — ещё
   `added-for-review`), id и связи совпадают со спицей. Обновление копии —
   задача РТ-6 (раздел 12). RFC — `accepted`: PR #437 слит (шаг 1 раздела 11).

## 0. Тип и дом артефакта

**Тип — RFC спицы с готовыми к копированию телами задач.** Каждое тело
написано по
[шаблону задачи](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/task-for-konard-template.md).
**Дом — `docs/rfc/` этой спицы**, запись `RFC-RT-001` в
[реестре RFC](rfc-register.md), раздел «Задачи для runtime».

Почему так, а не иначе:

| Вариант | Почему отвергнут или принят |
| --- | --- |
| Сразу issue в `mango-ba-ai-runtime` | У исполнителя спицы нет решения о бэклоге runtime: «создаёт владелец… (A-08 RFC #427)» ([реестр справочников, раздел 6](../../standards/bcreq-runtime-references.md#6-задачи-для-репозитория-runtime)). Issue без решения владельца — обход его полномочий |
| Файл предложения в runtime | Нормативное содержание runtime правится только компиляцией (правило 13 `AGENTS.md`); предложение — не справочник (ТС-4) |
| Раздел реестра `standards/bcreq-runtime-references.md` | Реестр — перечень справочников и ссылок (факты, ТС-4); спецификация на три репозитория раздует его и смешает назначение. Реестр получает ссылку на этот RFC |
| Задача только в Хабе | Значения каталога принадлежат спице («каталог значений принадлежит споку и расширяется в споке», `taxonomy/products.yaml` runtime, строка 3); Хаб владеет формой. Нужны оба |
| **RFC спицы** | **Принят.** У решения есть статус, владелец и журнал ([процесс RFC](rfc-process.md)). Тела задач копируются в runtime и Хаб без правки. Обоснование, проверки и риски остаются рядом |

Все ссылки в телах задач — полные URL. Задача запускается из runtime и
читает эту спицу. Ссылки на runtime закреплены по SHA (ТС-1), ссылки на
каталог спицы — по коммиту каталога `e3597fd74da9c4f631ca46697c643462e2cf0b85`.

## 1. Проверенное текущее состояние

Каждая строка проверена клоном на указанном коммите 2026-11-03. Логи —
в `experiments/issue_434/`.

| № | Факт | Источник | Как проверено |
| --- | --- | --- | --- |
| Ф-1 | Словарь продуктов runtime содержит форму уровней и три класса, значений ниже класса нет | [`taxonomy/products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/products.yaml), строки 9–18 | Чтение файла |
| Ф-2 | `binding_level: Atomic Function` — связь только с Domain считается неполной разметкой (PT-3) | там же, строка 14 | Чтение файла |
| Ф-3 | `c-in.products[]` требует `atomic_function`, значение — «string (мин. длина `1`)», без словаря | [`contracts/c-in.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/contracts/c-in.md), строки 42–50 | Чтение файла |
| Ф-4 | Правило 1 «значение вне закрытого словаря — отказ» перечисляет класс артефакта, процесс, операцию, слот, класс формата и профиль — функции продукта в перечне нет | [`AGENTS.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/AGENTS.md), строки 44–47 | Чтение файла |
| Ф-5 | Нормативное содержание runtime не правится в runtime, только задачей в Хабе и компиляцией | там же, правило 13, строки 94–95 | Чтение файла |
| Ф-6 | Golden set один: `product_class: contact-center`, `structural_only: true`, 2 положительных и 4 отрицательных синтетических случая, `confirmed_by: none`; поля `atomic_function` в индексе нет | [`golden/cases.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/golden/cases.yaml) | Чтение файла |
| Ф-7 | Функции эталонов названы только в markdown: `queue-callback-offer`, `handling-report-export`, `callback-offer`, `queue-capacity-limit`, `group-report-threshold`, `after-hours-greeting`; ни одной нет в каталоге спицы | [`golden/gs-cc-01-queue-overflow.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/golden/gs-cc-01-queue-overflow.md), строка 31, и ещё пять файлов `golden/` | `experiments/issue_434/golden-af-vs-catalog.log` |
| Ф-8 | Отрицательный эталон NEG-03 объявляет класс `analytics-reporting` внутри набора `contact-center` | [`golden/gs-cc-neg-03-sla-vs-aht.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/golden/gs-cc-neg-03-sla-vs-aht.md), строка 25 | Чтение файла |
| Ф-9 | Все 11 навыков и маршрут — только для `contact-center`; классы `voice-ucaas`, `analytics-reporting` — `in_slice: false` | [`skills/`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/5d8c201511fd730a596c9f9b4588470a7b01edc9/skills), [`routes/rg-bcreq-v1.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/routes/rg-bcreq-v1.yaml), строка 8 | Чтение файлов |
| Ф-10 | Машинный гейт `G-mach` читает семь словарей; каталога функций среди них нет; `check_golden` проверяет только `golden/cases.yaml` | [`evaluation/validate-package.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/evaluation/validate-package.md), разделы `check_taxonomies`, `check_golden` | Чтение файла |
| Ф-11 | Пакет runtime скомпилирован из Хаба `dbf3baa9` (2026-09-19); форма Хаба с каталогом `taxonomy/mango-products.yaml` и полной цепочкой в `c-in` появилась позже — `90c7f1ef` (2026-09-23), на 27 коммитов позже | `compilation-manifest.yaml` runtime, строка 10; история Хаба | `experiments/issue_434/hub-product-form-vs-runtime.log` |
| Ф-12 | Каталог Хаба `mango-products.yaml` v3.0 (98 записей функций, 97 уникальных id) целиком входит в каталог спицы; спица добавляет 74 узла с портала (`origin: portal-update`, по Р-17 — `lifecycle: accepted`) | Хаб `c06075d0`, `projects/ba-ai-process/dist/execution-package-gigacode-cli/taxonomy/mango-products.yaml` | `experiments/issue_434/hub-snapshot-vs-spoke-catalog.log` |
| Ф-13 | Каталог спицы: 353 узла (Domain 7, Capability 43, Feature 151, Atomic Function 152), статус `accepted` (Р-17), `runtime_compatibility` сопоставляет три класса runtime доменам | [`docs/taxonomy/products.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/e3597fd74da9c4f631ca46697c643462e2cf0b85/docs/taxonomy/products.json) | `experiments/issue_434/catalog-stats.json` |
| Ф-14 | Текущий промпт спицы считает таксономию runtime «определённой», только если это каталог по всей продуктовой линейке с цепочкой до Atomic Function; иначе — «[ТРЕБУЕТСЯ УТОЧНЕНИЕ]» | [`prompts/bcreq-products-impact-analysis-stepwise.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md), раздел «Полнота таксономии и класс поиска» | Чтение файла |
| Ф-15 | Манифест runtime уже содержит копию из спицы с `source_commit` — базу знаний (`docs/kb`); правки данных runtime вне компиляции уже были (`3df40fd`, `0a13425` и откат `b67410f`) | `compilation-manifest.yaml` runtime, раздел `copied`; история runtime | `git log` клона runtime |
| Ф-16 | Каталог спицы построен из классификации Хаба v3.0: `source_urls` ведёт на `2026-05-22-classification.md` по коммиту `cd5d6e4b`; 279 узлов `origin: inherited`, 74 — `portal-update`; до Хаба `c06075d0` файл не менялся | [`2026-05-22-classification.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-22-classification.md), каталог спицы, ключ `source_urls` | `experiments/issue_434/industry-taxonomy-inventory.log` |
| Ф-17 | Индустриальный слой — в том же файле Хаба: «одно требование получает четыре ключа классификации» (Mango, TM Forum, UNSPSC/ОКПД 2, ГОСТ/НПА); международная таблица — 42 строки, 39 разных кодов UNSPSC; российская таблица — 42 строки; поля «Рабочей таксономии для входящих требований» | там же, строка 75, разделы «Сравнительная таблица международной классификации», «Рабочая таксономия для входящих требований» | `experiments/issue_434/industry-taxonomy-inventory.log` |
| Ф-18 | Связь каталога с индустриальным слоем — только поле `row` у 42 из 43 Capability; у `report-builder` его нет; полей TM Forum, UNSPSC, ОКПД 2 в узлах каталога нет; в runtime нет ни одного упоминания TM Forum, UNSPSC, ОКПД | каталог спицы; клон runtime `5d8c201` | `experiments/issue_434/industry-taxonomy-inventory.log` |
| Ф-19 | Сравнение с внешними продуктами на уровне функций есть только в черновике Хаба: у функции ≥2 `international_sources` (Genesys — 29, TM Forum SID — 21, Amazon Connect — 20, Cisco UCCE — 14); из 54 функций 17 есть в каталоге спицы | [`2026-05-27-capability-decomposition.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-27-capability-decomposition.md), `status: draft` | `experiments/issue_434/industry-taxonomy-inventory.log` |
| Ф-20 | Поток оценки тендерного ТЗ в runtime объявлен, но вне среза: `P-08 tender-tz-assessment`, `in_slice: false`; в спице — BL-133, `deferred (triggered)` | [`taxonomy/processes.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/processes.yaml), строка 50; [BL-133](../../pr-ops/backlog-ba-model.md#bl-133-процесс-оценки-тз-заказчика) | Чтение файлов |

Числа каталога по классам runtime (узел относится к классу, если среди
его предков есть Domain класса из `runtime_compatibility`):

| Класс runtime | Domain каталога | Capability | Feature | Atomic Function | из них `retained` / `accepted` |
| --- | --- | --- | --- | --- | --- |
| `contact-center` | `contact-center` | 17 | 59 | 66 | 33 / 33 |
| `voice-ucaas` | `voice-ucaas` | 16 | 54 | 51 | 39 / 12 |
| `analytics-reporting` | `analytics` | 12 | 35 | 28 | 20 / 8 |
| вне классов runtime | `digital-channels`, `ai-automation`, `hardware`, `security` | 10 | 39 | 39 | — |

16 функций относятся сразу к трём классам: их Capability имеет нескольких
родителей. Поэтому сумма по строкам больше 152. Все 353 узла имеют
`availability: not-established-by-taxonomy`: каталог не утверждает, что
функция доступна клиенту.

## 2. Обоснование и связь с BL-156

[BL-156](../../pr-ops/backlog-ba-model.md#bl-156-промпты-шагов-потока-из-стандартов-по-тесту)
собирает промпты шагов потока. В `prompts/` допускается только редакция
«не хуже базовой линии golden set» (DEC-427-11). Промпт шага ссылается на
справочники runtime по
[реестру](../../standards/bcreq-runtime-references.md). Если справочника
нет, промпт получает блок заглушки (раздел 4 реестра). Без РТ-1 и РТ-3
заглушки неизбежны по трём причинам:

1. **Шаг Ш-2 (продуктовая принадлежность) без каталога не может дать
   правильного результата.**
   - `c-in` требует `atomic_function` (Ф-3), а значений нет (Ф-1).
   - У модели два выхода. Она может придумать функцию: именно так
     появились шесть функций эталонов, которых нет в каталоге (Ф-7). Или
     она оставит пробел: это заглушка З-1.
   - Промпт обязан выбрать второй выход (Ф-14). Значит, каждый документ
     BCREQ получит «Продуктовая принадлежность: [ТРЕБУЕТСЯ УТОЧНЕНИЕ]».
   - PT-3 считает такую разметку неполной (Ф-2).
2. **Шаг Ш-В (проверка) без golden set класса не имеет базовой линии.**
   - Для `voice-ucaas` и `analytics-reporting` эталонов нет (Ф-6).
   - Правило «не хуже базовой линии golden set» для этих классов
     непроверяемо. Промпт либо не вводится, либо вводится с заглушкой З-3.
   - Для `contact-center` эталоны есть, но они `structural_only`:
     «расхождение по содержанию отказом не является». Содержание
     документа ими не проверяется.
3. **Заглушка — не временная мера, если её никто не снимает.**
   - Реестр говорит: «Когда справочник появляется в runtime, строка
     ниже снимается».
   - Справочник не появится сам. Нужны задачи в runtime и Хабе и решение
     владельца по каталогу в статусе `review`.

Нарушение принципа качества здесь конкретное. Документ выходит без
обязательного по PT-3 уровня разметки, а проверка промпта не имеет
эталона для двух классов из трёх.

## 3. ССОТ и разделение ответственности

| Что | ССОТ | Почему | Кто правит |
| --- | --- | --- | --- |
| Значения уровней Domain…Atomic Function | Каталог спицы [`docs/taxonomy/products.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/e3597fd74da9c4f631ca46697c643462e2cf0b85/docs/taxonomy/products.json) | Runtime прямо отдаёт значения спице (Ф-1, строка 3); каталог спицы — надмножество снимка Хаба (Ф-12) | Спица (PR в `mango_ba_prompts`) |
| Форма записи каталога и правило привязки в `c-in` | Хаб (`ba-meta-model/product-taxonomy`, пакет `dist/…/taxonomy/products.yaml` v2.0) | Хаб уже ввёл `catalog: taxonomy/mango-products.yaml` и цепочку в `c-in` (Ф-11); норма runtime — компиляция Хаба (Ф-5) | Хаб (задача ХАБ-1) |
| Копия каталога в runtime | `taxonomy/mango-products.yaml` runtime | Модель читает runtime без доступа к Хабу и спице («`hub_access_required_at_runtime: false`», манифест) | Runtime (задача РТ-1), запись `copied` в манифесте |
| Эталоны по классам | `golden/` runtime | Эталон — «обязательный элемент машинного гейта» (`golden/cases.yaml`) | Runtime (задача РТ-3); правило проверки — Хаб (ХАБ-1, пункт 5) |
| Какой SHA runtime читает промпт | [Реестр справочников, раздел 1](../../standards/bcreq-runtime-references.md#1-закреплённый-срез) | ТС-5: «единственная точка обновления SHA» | Спица (BL-163) |
| Исток значений (исследование) | Хаб, [`research/mango/2026-05-22-classification.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-22-classification.md) v3.0 | Из него унаследованы 279 узлов каталога (Ф-16); спица добавила 74 узла с портала | Не правится ради runtime: значения для runtime берутся из каталога спицы |
| Индустриальный слой: TM Forum, UNSPSC, ОКПД 2, ГОСТ/НПА | Тот же файл Хаба, таблицы по номеру строки (Ф-17) | В каталоге и runtime этих полей нет (Ф-18); слой нужен потоку оценки тендерного ТЗ, а не РТ-1 и РТ-3 | Решает BL-164 по триггеру (подраздел 3.1) |

Имя файла `taxonomy/mango-products.yaml` взято из Хаба (Ф-11), а не
придумано. Так следующая компиляция Хаба заменит файл, а не создаст
второй.

### 3.1. Происхождение таксономии и индустриальный слой

Владелец попросил проверить три вещи
([комментарий к PR #437](https://github.com/G-Ivan-A/mango_ba_prompts/pull/437)):

1. что таксономия Mango разработана в
   `research/mango/2026-05-22-classification.md` Хаба;
2. что она правильно используется в спице и в runtime;
3. что рядом с ней есть индустриальная таксономия.

Цель индустриальной таксономии — в будущем потоке тендерного ТЗ
сопоставлять таксономию Mango с рыночной, чтобы сравнивать функции с
внешними продуктами. Скрипт проверки —
`experiments/issue_434/industry_taxonomy_inventory.py`, лог —
`experiments/issue_434/industry-taxonomy-inventory.log`.

**Что подтверждено.**

| № | Проверка | Результат | Факт |
| --- | --- | --- | --- |
| П-1 | Таксономия Mango разработана в `2026-05-22-classification.md` | Да. Это версия 3.0 с уровнями `Domain → Capability → Feature → Atomic Function` и 7 доменами. Каталог спицы ссылается на неё по коммиту `cd5d6e4b`, файл с тех пор не менялся | Ф-16 |
| П-2 | Каталог спицы использует таксономию Хаба корректно | Да. 279 узлов унаследованы, 74 добавлены с портала и приняты владельцем (`accepted`, Р-17). ССОТ значений для runtime — каталог спицы (раздел 3) | Ф-12, Ф-13, Ф-16 |
| П-3 | Runtime использует таксономию корректно | Нет, пока нет РТ-1. В runtime только три класса и свободная строка `atomic_function` | Ф-1, Ф-3, Ф-7 |
| П-4 | Есть индустриальная таксономия | Да, в том же файле Хаба, отдельного файла нет. Ключи TM Forum, UNSPSC, ОКПД 2 и ГОСТ/НПА заданы для 42 классов. Есть закупочный слой Commercial Layer. Отраслевая вертикаль R2.7 отложена: «вертикаль описывает контекст применения, а не продуктовый класс» | Ф-17 |
| П-5 | Индустриальный слой связан с каталогом | Частично. Связь только через `row` Capability (42 из 43). Полей слоя нет ни в каталоге, ни в runtime | Ф-18 |
| П-6 | Есть основа для сравнения с внешними продуктами | Частично. Внешние продукты названы только у функций черновика декомпозиции (Genesys, Amazon Connect, Cisco UCCE); 17 из 54 функций есть в каталоге | Ф-19 |

**Что ещё проверено в документах Хаба и спицы.**

- [`2026-05-22-requirements-flow.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-22-requirements-flow.md)
  (поток анализа ТЗ), FR-06: «классифицировать требования по рабочей
  таксономии MANGO OFFICE из `2026-05-22-classification.md`: product
  family, Mango status, Mango product, TM Forum domain/capability,
  UNSPSC, ОКПД 2, standards overlay и compliance trigger». BPR-10:
  «хранить benchmark конкурентов как отдельный источник evidence с датой
  среза, ссылкой, продуктом конкурента, capability и уровнем уверенности».
  Это и есть сценарий владельца для тендерного ТЗ.
- [`2026-05-26-taxonomy-concept.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-26-taxonomy-concept.md)
  (`status: draft`) называет назначение таксономии: «функции конкурентов
  и best-practice capabilities». Про UNSPSC и ОКПД 2 он говорит: «Не
  делать закупочный код главным ключом taxonomy: он слишком грубый для
  продуктового анализа». Предлагаемое поле — `tm_forum_mapping`.
- Классификация, рекомендация 8: «Заполнять продуктовый ключ (`Domain →
  Capability → Feature → Atomic Function`) и закупочный слой (`Commercial
  Layer`) независимо». Поэтому индустриальный слой не вносится в
  РТ-1. Узлы каталога в runtime сохраняют id без изменений (раздел 5,
  ФТ), значит слой можно присоединить позже по id Capability.
- В спице TM Forum используется в другой роли — как альтернативный
  стандарт описания решения
  ([`standards/bcreq-composition-standard.md`](../../standards/bcreq-composition-standard.md),
  раздел 3). Это не продуктовая таксономия, и BL-164 её не меняет. Термины
  отрасли (UCaaS, Outbound Campaign, ACD) есть в
  [`standards/product-classification-contract.md`](../../standards/product-classification-contract.md)
  как словарь, без кодов по узлам.
- [`docs/hub-research-dependencies.md`](../hub-research-dependencies.md)
  ведёт `#classification`, `#classification-tz`, `#taxonomy-concept`,
  `#capability-decomposition` на старые пути Хаба по коммиту `038868dd`
  (до переименования в `2026-05-22-…`). Ссылки закреплены по SHA и
  открываются. Содержание классификации на `038868dd` и `cd5d6e4b`
  отличается только метаданными и путями ссылок (16 строк diff). Среди
  потребителей `#classification` указан `prompts/tz-stats-generator.md`,
  которого в спице нет. Обновление — шаг 10 раздела 11.

**Предложение по индустриальной таксономии (по указанию владельца —
только задача в бэклоге).** Заведена
[BL-164](../../pr-ops/backlog-ba-model.md#bl-164-индустриальная-таксономия-для-оценки-тендерного-тз),
`deferred (triggered)`. Триггер — старт BL-133 или включение `P-08` в
срез runtime. До триггера ничего не строится: потребителя нет (Ф-20).

Рассмотренные альтернативы:

| Вариант | Решение | Почему |
| --- | --- | --- |
| Только задача BL-164 в бэклоге спицы | **Принят** | Указание владельца. Потребителя пока нет (Ф-20), а знание не теряется: карточка ссылается на источники и ключ связи `row` |
| Добавить поля TM Forum, UNSPSC, ОКПД 2 в узлы `products.json` сейчас | Отвергнут | Смешивает продуктовый и закупочный ключи (рекомендация 8 классификации); каталог в статусе `review` (Р-17); раздувает РТ-1 |
| Перенести слой в РТ-1 или завести РТ-5 в runtime | Отвергнут сейчас | `P-08` вне среза, навыков нет; правило runtime читать «только то, что читается в исполнении» (EP-C4) |
| Задача в Хабе вместо спицы | Отвергнут | Значения каталога принадлежат спице (раздел 3); Хаб правит форму, когда спица даст данные |
| Ничего не заводить | Отвергнут | Связь держится на одном поле `row`, а 43-я Capability его не имеет; без задачи это знание теряется |

## 4. Механизм снятия заглушки таксономии (критично)

**Явный пункт.** Задача РТ-1 обязывает runtime зафиксировать актуальную
продуктовую таксономию Mango в файле `taxonomy/mango-products.yaml`:
весь каталог 2026-10-28.1, без отбора. Без этого файла РТ-1 не закрыта
(«Готово, когда», раздел 5).

Гарантия — цепочка из шести звеньев. Каждое звено ломается громко:
отказ, падение проверки или явная заглушка, но не тихое угадывание.

| № | Звено | Где | Что гарантирует | Как ломается |
| --- | --- | --- | --- | --- |
| М-1 | Файл `taxonomy/mango-products.yaml`: `vocabulary: mango-products`, `closed: true`, 353 узла с `id`, `level`, `parents`, `classes`, `lifecycle` | runtime, РТ-1 | Значения есть и читаются моделью по ссылке | — |
| М-2 | Проверки `tests/runtime-smoke.sh`: файл есть, `closed: true`, каждый `atomic_function` в `golden/cases*.yaml` — id функции каталога | runtime, РТ-1 и РТ-3 | Каталог нельзя удалить или подменить незаметно; эталон не может ссылаться на выдуманную функцию | CI runtime красный. Проверено симуляцией: 4 сценария, `experiments/issue_434/runtime-smoke-sim.log` |
| М-3 | Строка И-2 реестра → «Да», ссылка на `taxonomy/mango-products.yaml` по SHA; строка З-1 снимается | спица, BL-163 — исполнено 2026-11-04 (issue #442, раздел 12) | Промпт читает каталог, а не `products.yaml`-форму | Валидатор реестра: ссылка только по SHA раздела 1 |
| М-4 | Инструкция чтения в промпте шага Ш-2 (ниже) | спица, BL-156 | Модель выбирает id из каталога и не изобретает функцию | Нет id → «[ТРЕБУЕТСЯ УТОЧНЕНИЕ]» и вопрос БА |
| М-5 | `c-in.products[].atomic_function` — id узла `level: function` каталога; `product_class` ∈ `classes` узла; правило 1 `AGENTS.md` распространено на каталог | Хаб → runtime, ХАБ-1 | Вход с выдуманной функцией отклоняется на узле n1 | Отказ навыка нормализации по `C-IN` |
| М-6 | `check_taxonomies` читает каталог: уникальные id, родитель на уровень выше, `closed: true` | Хаб → runtime, ХАБ-1 | Машинный гейт видит каталог как словарь | `G-mach: пакет отвергнут` |

М-1 и М-2 снимают заглушку для чтения промптами сразу после слияния РТ-1.
М-5 и М-6 делают каталог нормой исполнения runtime. Это отдельный цикл
компиляции, и он не блокирует промпты.

**Как промпт читает каталог (текст для промпта шага Ш-2, BL-156).** Это
образец, а не нормативный текст стандарта. В промпт он попадает через
BL-156 «по тесту» (Р-14 принято, issue #432). Механизм опирается на
правила [базового стандарта](../../standards/bcreq-prompt-base-standard.md#34-источники-цитаты-и-справочники-runtime)
BL-151: БС-19 (SHA — только в разделе 1 реестра) и БС-21 (блок заглушки —
из раздела 4 реестра). Поэтому М-3 снимает заглушку во всех промптах
одной правкой реестра.

```text
Таксономия продуктов: https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/<SHA реестра>/taxonomy/mango-products.yaml
1. Возьми продуктовый класс задачи из входа БА (contact-center,
   voice-ucaas или analytics-reporting). Класс не выводится из текста.
2. Отбери узлы, у которых в `classes` есть этот класс.
3. Пройди цепочку: domain → capability → feature → function по полю
   `parents`. Для каждого затронутого продукта выбери id узла
   `level: function` и приведи цепочку целиком.
4. Если подходящей функции нет или подходят две, не выбирай сам: выведи
   «Продуктовая принадлежность: [ТРЕБУЕТСЯ УТОЧНЕНИЕ]», подтверждённые
   уровни и вопрос БА.
5. Узлы с `lifecycle: retained` и `lifecycle: accepted` равноправны:
   оба утверждены владельцем (Р-17). В копии runtime до задачи РТ-6
   узлы с портала помечены `added-for-review`: читай их как `accepted`.
6. Каталог не утверждает доступность функции клиенту
   (`availability: not-established-by-taxonomy`): доступность — только
   из источника задачи или БЗ.
```

Шаг 6 не придуман. Его основание — поле `availability` в каждом узле
каталога (Ф-13). Если модель не открывает ссылку, действует ТС-6: БА
прикладывает файл.

## 5. РТ-1 — тело задачи для `mango-ba-ai-runtime` (копировать целиком)

Заголовок: `РТ-1. Каталог продуктов Mango taxonomy/mango-products.yaml (снятие заглушки З-1)`

````markdown
## Контекст задачи

- Полный URL постановки: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-runtime-product-catalog-golden-set.md (RFC-RT-001, раздел 5)
- Полные URL связанных PR/issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/434, https://github.com/G-Ivan-A/mango_ba_prompts/pull/431, https://github.com/G-Ivan-A/mango_ba_prompts/issues/427
- Полные URL связанных репозиториев: https://github.com/G-Ivan-A/mango_ba_prompts (ССОТ значений каталога), https://github.com/G-Ivan-A/hybrid-Intelligence-lab (ССОТ формы, задача ХАБ-1)
- Важные решения, которые уже приняты:
  - каталог значений принадлежит спице: «каталог значений принадлежит споку и расширяется в споке» (https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/products.yaml, строка 3);
  - решение владельца Р-17 (https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/BACKLOG.md): каталог 2026-10-28.1 (`status: accepted`) переносится целиком, `lifecycle` сохраняется, 74 узла с портала приняты (`accepted`);
  - нормативное содержание runtime не правится в runtime (правило 13 AGENTS.md) — норма идёт задачей ХАБ-1.
- Что нельзя считать известным из предыдущих задач: значения уровней ниже класса — их в runtime нет; функции в `golden/*.md` (`queue-callback-offer` и др.) — выдуманы, в каталоге их нет.

## Решаемая проблема

`contracts/c-in.md` требует `atomic_function`, но словаря функций в runtime нет (https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/contracts/c-in.md, строки 42–50). Модель придумывает функцию или оставляет пусто; промпты спицы ставят заглушку З-1 (https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md, раздел 4). Каталог существует в спице: https://github.com/G-Ivan-A/mango_ba_prompts/blob/e3597fd74da9c4f631ca46697c643462e2cf0b85/docs/taxonomy/products.json (353 узла, 152 функции, статус `accepted`).

## Story

**Как есть:**

- Кто действует: БА запускает промпт BCREQ, модель читает runtime.
- Что происходит сейчас: `taxonomy/products.yaml` даёт три класса и форму уровней без значений.
- Где возникает ошибка, блокировка или долг: шаг продуктовой принадлежности выдаёт «[ТРЕБУЕТСЯ УТОЧНЕНИЕ]» или выдуманный id; PT-3 считает разметку неполной.

**Как должно быть:**

- Кто действует: та же модель по ссылке на runtime.
- Какой результат должен быть доступен после решения: закрытый каталог `taxonomy/mango-products.yaml` со всеми узлами продуктовой линейки и цепочкой Domain → Capability → Feature → Atomic Function.
- Как Пользователь принимает или возвращает решение на доработку: сверяет числа в PR с каталогом спицы и прогоняет `sh tests/runtime-smoke.sh`.

## ФТ

- [ ] Файл `taxonomy/mango-products.yaml` содержит заголовок: `vocabulary: mango-products`, `closed: true`, `version`, `catalog_version: "2026-10-28.1"`, `catalog_status`, `source` (URL каталога спицы по коммиту), `source_commit`, `source_sha256`, `class_domains` (три класса runtime → домены каталога из `runtime_compatibility`).
- [ ] Все 353 узла каталога перенесены без отбора и без изменения id, имени и связей: `id`, `level` (`domain` | `capability` | `feature` | `function`), `name`, `parents`, `classes`, `lifecycle`; если есть в источнике — `params`, `locator`, `legacy_id`, `binding_basis`.
- [ ] `classes` узла — классы runtime, к доменам которых узел относится через предков; для 39 функций доменов `digital-channels`, `ai-automation`, `hardware`, `security` — пустой список (класса runtime нет).
- [ ] Числа совпадают с каталогом: Domain 7, Capability 43, Feature 151, Atomic Function 152; функций класса `contact-center` — 66, `voice-ucaas` — 51, `analytics-reporting` — 28; id уникальны.
- [ ] `compilation-manifest.yaml`, раздел `copied`: запись по образцу базы знаний — `what`, `from` (URL каталога спицы), `source_commit`, `to: taxonomy/mango-products.yaml`, `note` (копия без изменения смысла; правило привязки — задача Хаба).
- [ ] `README.md`, раздел «Состав», и `docs/guides/` (шаг объявления продуктов) называют файл и говорят: значение `atomic_function` берётся из него по id.
- [ ] `tests/runtime-smoke.sh` перед итоговой проверкой:
  ```sh
  require_file taxonomy/mango-products.yaml
  require_text taxonomy/mango-products.yaml '^closed: true$' 'product catalog is closed'
  for af in $(grep -hEo 'atomic_function: *"?[a-z0-9/-]+' "$ROOT"/golden/cases*.yaml | sed 's/.*: *"\{0,1\}//'); do
    if grep -Fq "{id: \"$af\", level: function," "$ROOT/taxonomy/mango-products.yaml" 2>/dev/null; then pass "golden atomic_function $af is in catalog"; else fail "golden atomic_function $af is in catalog"; fi
  done
  ```
  (цикл не находит значений, пока РТ-3 не добавит поле; тогда он становится проверкой РТ-3).

## НФТ

- [ ] Без файлов `.py`/`.json` вне разрешённых каталогов (правило `tests/runtime-smoke.sh`); каталог — YAML.
- [ ] Каталог не содержит правил исполнения (ТС-4 спицы): правило привязки — в `contracts/c-in.md` после ХАБ-1, не в каталоге.
- [ ] Форма строки узла позволяет проверку одной командой `grep` (одна строка — один узел); образец: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_434/prototype/mango-products.yaml, генератор: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_434/compile_catalog_prototype.py.
- [ ] Ни `AGENTS.md`, ни `contracts/`, ни `skills/`, ни `evaluation/` не правятся (правило 13).
- [ ] Пути Хаба, запрещённые во время выполнения (`evaluation/validate-package.md`), в каталог не попадают; URL спицы допустим только в ключах провенанса (`source:`).

## Цель

В runtime есть закрытый каталог продуктов Mango по всей линейке, промпты читают его по SHA, а smoke-проверка падает без него.

Definition of Done:

- `sh tests/runtime-smoke.sh` — `runtime smoke test passed`; удаление `taxonomy/mango-products.yaml` даёт падение (проверить и привести вывод в PR);
- числа ФТ сверены командой и приведены в PR;
- запись манифеста и строка README есть;
- в PR — ссылка на задачу ХАБ-1 (норма) и SHA коммита слияния для реестра спицы (BL-163).

## Operating Mode

- `Structured`: значения и связи каталога не меняются; отбор, переименование и «улучшение» узлов запрещены; расхождение с каталогом — вопрос в PR.

## Специфика работы с Конардом

- **молчание = согласие:** если Пользователь мержит PR без комментариев, решения приняты;
- **комментарий + ручной перезапуск:** доработка в том же PR;
- **close:** закрытие PR означает отказ от решения;
- draft PR используется как место отложенной проверки до acceptance.

## Обоснованные обходы

- Правка runtime вне компиляции Хаба. Обходится порядок «сначала Хаб, затем компиляция» для **данных**: каталог — копия значений спицы, как `docs/kb` (раздел `copied` манифеста, `source_commit`). Норма (`c-in`, `AGENTS.md`, `G-mach`) не правится — она в ХАБ-1. Без обхода промпты ждут цикла компиляции Хаба, а BL-156 выходит с заглушкой З-1.
````

## 6. ХАБ-1 — тело задачи для `hybrid-Intelligence-lab` (норма привязки)

Заголовок: `ХАБ-1. Привязка c-in.atomic_function к каталогу продуктов и компиляция в mango-ba-ai-runtime`

````markdown
## Контекст задачи

- Полный URL постановки: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-runtime-product-catalog-golden-set.md (RFC-RT-001, раздел 6)
- Полные URL связанных PR/issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/434; задача РТ-1 в https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues
- Полные URL связанных репозиториев: https://github.com/G-Ivan-A/mango-ba-ai-runtime (цель компиляции, срез 5d8c201511fd730a596c9f9b4588470a7b01edc9), https://github.com/G-Ivan-A/mango_ba_prompts (ССОТ значений)
- Важные решения, которые уже приняты: форма каталога уже есть в Хабе — `catalog: taxonomy/mango-products.yaml` и цепочка `domain/capability/feature/atomic_function` в `c-in` (коммит 90c7f1ef9d2b75dff144d17531302438548893e0); runtime скомпилирован раньше — `hub_commit: dbf3baa96d3585150974212254af81bcf7b03150`.
- Что нельзя считать известным из предыдущих задач: что снимок Хаба `mango-products.yaml` v3.0 полон — в нём 98 записей функций (97 уникальных id: `callback-scheduling` дважды), каталог спицы — 152 функции.

## Решаемая проблема

В runtime `atomic_function` — свободная строка (https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/contracts/c-in.md, строка 50), а правило 1 AGENTS.md не распространяется на функцию продукта. После РТ-1 каталог в runtime есть, но норма его не требует: вход с выдуманной функцией проходит G-mach.

## Story

**Как есть:** вход `c-in` с любой непустой строкой в `atomic_function` принимается; G-mach не читает каталог.

**Как должно быть:** функция вне каталога или функция чужого класса — отказ на n1 с описанием непокрытого случая; G-mach проверяет каталог как закрытый словарь. Пользователь принимает по отчёту G-mach и отрицательному эталону РТ-3.

## ФТ

- [ ] `taxonomy/products.yaml`: ключ `catalog: taxonomy/mango-products.yaml` и `class_domains` (класс runtime → домен каталога).
- [ ] `contracts/c-in.md`: `atomic_function` — id узла `level: function` из `taxonomy/mango-products.yaml`; `product_class` ∈ `classes` этого узла.
- [ ] `AGENTS.md`, правило 1: в перечень закрытых значений добавлена функция продукта (каталог `taxonomy/mango-products.yaml`).
- [ ] `evaluation/validate-package.md`, `check_taxonomies`: каталог читается; `closed: true`; id уникальны; каждый `parents` ссылается на узел уровнем выше; у функции без класса runtime `classes: []` явно.
- [ ] `evaluation/validate-package.md`, `check_golden`: у каждого случая есть `product_class`, `atomic_function` — id функции каталога того же класса; набор `golden/cases-<класс>.yaml` проверяется для каждого класса, где он есть (форма — РТ-3).
- [ ] Навык нормализации (`transcript-normalization-*`, шаг `check-schema`) отказывает при функции вне каталога.
- [ ] Компиляция в runtime: `compilation-manifest.yaml` — новый `hub_commit`, `compiled_at`; каталог переходит из `copied` спицы в цепочку Хаба только если Хаб принимает каталог спицы как источник (иначе остаётся копией спицы — ССОТ значений не меняется).

## НФТ

- [ ] Ни один артефакт времени выполнения не ссылается на Хаб (контракт 2 манифеста).
- [ ] Совместимость: поле `product_class` в `c-in` сохраняется (три класса), полная цепочка Хаба `domain/capability/feature` вводится отдельным решением — не в этой задаче.
- [ ] Отрицательный эталон РТ-3 «функция вне каталога» проходит как `refused`.

## Цель

Каталог продуктов — закрытый словарь нормы runtime: выдуманная функция останавливает маршрут, G-mach проверяет каталог и эталоны по классам.

## Operating Mode

- `Structured`.

## Специфика работы с Конардом

- **молчание = согласие**; **комментарий + ручной перезапуск**; **close** — отказ; draft PR — отложенная проверка.

## Обоснованные обходы

- Нет.
````

## 7. РТ-3 — тело задачи для `mango-ba-ai-runtime` (копировать целиком)

Заголовок: `РТ-3. Golden set по классам продуктовой таксономии (снятие заглушки З-3)`

Требование: issue
[#427](https://github.com/G-Ivan-A/mango_ba_prompts/issues/427) —
«голден сет по каждому классу проуктовой таксономии». Задача —
[РТ-3 реестра справочников](../../standards/bcreq-runtime-references.md#6-задачи-для-репозитория-runtime).

````markdown
## Контекст задачи

- Полный URL постановки: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-runtime-product-catalog-golden-set.md (RFC-RT-001, раздел 7)
- Полные URL связанных PR/issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/427 (требование: «голден сет по каждому классу проуктовой таксономии»), https://github.com/G-Ivan-A/mango_ba_prompts/pull/431, https://github.com/G-Ivan-A/mango_ba_prompts/issues/434
- Полные URL связанных репозиториев: https://github.com/G-Ivan-A/mango_ba_prompts (кандидаты эталонов из прогонов: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0074/outputs/golden-set-candidates.json)
- Важные решения, которые уже приняты: РТ-1 слита (каталог `taxonomy/mango-products.yaml`); РТ-4 слита для класса набора (пары `confusable_with` нужны отрицательным случаям, правило EP-G7).
- Что нельзя считать известным из предыдущих задач: функции в `golden/*.md` (`queue-callback-offer` и др.) — их нет в каталоге; эталоны `contact-center` подтверждены человеком — нет, `confirmed_by: none`.

## Решаемая проблема

Golden set один и только для `contact-center`, синтетический и `structural_only: true` (https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/golden/cases.yaml). Для `voice-ucaas` и `analytics-reporting` эталонов нет: правило спицы «не хуже базовой линии golden set» для этих классов непроверяемо, промпты получают заглушку З-3. Индекс не связывает случай с функцией продукта: функция названа только в markdown и выдумана.

## Story

**Как есть:** G-mach и промпты спицы сверяют вывод с шестью синтетическими случаями одного класса; содержание не проверяется.

**Как должно быть:** у каждого класса таксономии свой набор эталонов; каждый случай привязан к функции каталога; эталоны `contact-center` подтверждены человеком и проверяют содержание. Пользователь принимает по таблице покрытия в PR.

## ФТ

- [ ] Набор на класс — файл `golden/cases-<класс>.yaml` для `voice-ucaas` и `analytics-reporting`; `golden/cases.yaml` остаётся набором `contact-center` (ссылки на него не ломаются).
- [ ] Заголовок набора: `golden_set`, `version`, `product_class` (класс файла), `catalog_version` (версия `taxonomy/mango-products.yaml`), `structural_only`.
- [ ] Каждый случай, кроме существующих полей, имеет:
  - `product_class` — равен классу набора;
  - `atomic_function` — id узла `level: function` каталога, в `classes` которого есть `product_class`;
  - `origin` (`synthetic` | `run-observed`) и `confirmed_by` (`none` | `user`); для `run-observed` — `source` (прогон, инцидент, реплика).
- [ ] Минимальный состав набора: 2 положительных случая (разные профили продукта, если класс их допускает); по отрицательному случаю на каждую пару `confusable_with` словаря класса (EP-G7); 1 отрицательный случай «функция вне каталога или чужого класса» — `expect.outcome: refused` с причиной из правила 1 AGENTS.md.
- [ ] `contact-center`: шесть существующих случаев получают `product_class` и `atomic_function` из каталога (выдуманные значения в markdown заменены id каталога); NEG-03 — класс `contact-center` или перенос в набор `analytics-reporting` с обоснованием; подтверждение человеком — `confirmed_by: user` и `structural_only: false` только для подтверждённых случаев.
- [ ] Markdown-эталон на случай: `golden/gs-vu-*.md`, `golden/gs-ar-*.md` по образцу `golden/gs-cc-*.md`, с реестром продуктов (маркер, класс, id функции).
- [ ] `tests/runtime-smoke.sh`: цикл РТ-1 проверяет `atomic_function` всех `golden/cases*.yaml`; новые файлы эталонов существуют.

Образец случая:

```yaml
golden_set: mvp-bcreq-voice-ucaas
version: "0.1"
product_class: voice-ucaas
catalog_version: "2026-10-28.1"
structural_only: true          # до подтверждения человеком
cases:
  - id: GS-VU-01
    kind: positive
    file: golden/gs-vu-01-<slug>.md
    origin: synthetic
    confirmed_by: none
    product_class: voice-ucaas
    atomic_function: <id узла level: function из taxonomy/mango-products.yaml>
    artifact_class: A-BCREQ
    format_class: <F-…>
    projection: <V-…>
    product_profile: <P-…>
    expect:
      outcome: completed
      slots_present_all: true
      filled: [...]
      empty_with_reason: {...}
      trace_nonempty: true
```

## НФТ

- [ ] Ни одной выдуманной функции: smoke-проверка РТ-1 зелёная.
- [ ] Эталон не утверждает доступность функции клиенту (`availability` каталога — `not-established-by-taxonomy`).
- [ ] Набор класса вне среза маршрута (`in_slice: false`) используется промптами спицы и структурной сверкой; G-mach не отвергает пакет из-за отсутствия навыков класса — решение о поведении маршрута фиксируется в PR.
- [ ] Без `.py`/`.json`; правило проверки `check_golden` не правится в runtime — оно в задаче Хаба ХАБ-1.

## Цель

Для каждого из трёх классов `taxonomy/products.yaml` есть набор эталонов, привязанный к функциям каталога; `contact-center` проверяет содержание после подтверждения человеком.

Definition of Done: таблица покрытия в PR (класс × положительные × отрицательные × подтверждённые), `sh tests/runtime-smoke.sh` зелёный, ссылки на кандидатов из прогонов спицы для `run-observed`.

## Operating Mode

- `Creative`: выбор функций и сценариев эталонов — исполнителя, с обоснованием в PR; подтверждение человеком не выводится из текста.

## Специфика работы с Конардом

- **молчание = согласие**; **комментарий + ручной перезапуск**; **close** — отказ; draft PR — отложенная проверка.

## Обоснованные обходы

- Правка данных `golden/` до ХАБ-1: эталоны — данные пакета; правило их проверки (`check_golden`) меняет только Хаб.
````

### 7.1. Структура данных по классам

| Класс | Файл | Минимум положительных | Минимум отрицательных | Условие старта | Кандидаты |
| --- | --- | --- | --- | --- | --- |
| `contact-center` | `golden/cases.yaml` | 2 (есть, синтетические) | 4 пары глоссария (есть) + 1 «функция вне каталога» | РТ-1 | 1 случай `product: cc` с `confirmed_by: user` в RUN-0074 |
| `voice-ucaas` | `golden/cases-voice-ucaas.yaml` | 2 | по паре глоссария + 1 «функция вне каталога» | РТ-1, РТ-4 для класса | нет подтверждённых; функций в каталоге — 51 |
| `analytics-reporting` | `golden/cases-analytics-reporting.yaml` | 2 | по паре глоссария + 1 «функция вне каталога» | РТ-1, РТ-4 для класса | нет подтверждённых; функций в каталоге — 28 |

Кандидаты прогонов. В
[`runs/2026/RUN-0074/outputs/golden-set-candidates.json`](../../runs/2026/RUN-0074/outputs/golden-set-candidates.json)
46 случаев, из них 30 с `confirmed_by: user`. Поле `product` там имеет
значения `lk`, `cross`, `cc`, а не классы runtime. Значит, каждому
кандидату перед переносом нужно сопоставить класс и функцию каталога, и
это решение человека — гейт типа `человек`
(`experiments/issue_434/run0074-seed-counts.log`).

## 8. Связанные задачи спицы и решение владельца

| ID | Что | Где | Статус |
| --- | --- | --- | --- |
| Р-17 | Принять каталог `docs/taxonomy/products.json` 2026-10-28.1 целиком как таксономию runtime; 74 узла с портала — из `added-for-review` в `accepted` | [BACKLOG, раздел 2](../../pr-ops/BACKLOG.md), [комментарий владельца](https://github.com/G-Ivan-A/mango_ba_prompts/pull/437#issuecomment-6605372609) | принято 2026-11-03 |
| BL-163 | Реестр справочников на каталог runtime: SHA, И-2 → «Да», снятие З-1, тест клона | [Карточка](../../pr-ops/backlog-ba-model.md#bl-163-реестр-справочников-на-каталог-продуктов-runtime) | DONE: issue [#442](https://github.com/G-Ivan-A/mango_ba_prompts/issues/442), PR [#443](https://github.com/G-Ivan-A/mango_ba_prompts/pull/443) слит 2026-11-04 |
| BL-164 | Индустриальная таксономия для оценки тендерного ТЗ: сопоставление каталога Mango с TM Forum, UNSPSC, ОКПД 2 и функциями внешних продуктов (подраздел 3.1) | [Карточка](../../pr-ops/backlog-ba-model.md#bl-164-индустриальная-таксономия-для-оценки-тендерного-тз) | deferred (triggered): старт BL-133 или `P-08` в срезе |
| BL-165, BL-166 | Human Review кейсов `contact-center` и маппинг кандидатов RUN-0074 (решения владельца в issue #444) | [Раздел 13.4](#134-задачи-бэклога-из-решений-владельца) | deferred (triggered) |

Почему Р-17 понадобилось (до решения 2026-11-03):

- каталог был в статусе `review`;
- у класса `contact-center` 33 из 66 функций были `added-for-review`;
- перенос только `retained` уменьшит класс вдвое, а перенос всего каталога
  делает ревью-узлы нормой runtime.

Владелец выбрал перенос целиком и принял 74 узла с портала
(`lifecycle: accepted`, каталог `status: accepted`).

## 9. Риски, допущения, открытые вопросы

| № | Тип | Что | Как учтено |
| --- | --- | --- | --- |
| R-1 | Риск | Коллизия терминов: в `products.yaml` уровень Capability называется «Класс», а «продуктовый класс» runtime — уровень Domain | Тела задач говорят «продуктовый класс» только о трёх `classes`, уровни называют по `id` (Domain, Capability…) |
| R-2 | Риск | Каталог `review` меняется → копия в runtime стареет | `source_commit` и `source_sha256` в заголовке; смена каталога спицы — новая версия РТ-1-копии и шаг 1 реестра. **Сработал 2026-11-04**: PR #440 (Р-17) слит после РТ-1, копия на `7f920e2` — правило чтения и РТ-6 (раздел 12) |
| R-3 | Открыто | 39 функций доменов `digital-channels`, `ai-automation`, `hardware`, `security` не имеют класса runtime: в `c-in` их нельзя объявить | Каталог переносит их с `classes: []`; расширение классов — отдельное решение Хаба (не в ХАБ-1) |
| R-4 | Открыто | Поведение маршрута для класса `in_slice: false`, когда эталоны есть | Решение — в PR РТ-3 (НФТ) |
| R-5 | Риск | Golden set Хаба тоже классовый, без функций | ХАБ-1 правит `check_golden`; РТ-3 даёт данные |
| R-6 | Допущение | «Действиям по P-14» в issue #434 читается как цепочка следующих шагов PR #431: шаг 3 (РТ-1…РТ-4) идёт параллельно Р-14 → BL-151/152 | Р-14 принято, BL-151/152 — `review` (issue #432, PR #435); образец текста промпта входит в BL-156 «по тесту» |
| R-7 | Риск | Снимок Хаба содержит повтор id: функция `callback-scheduling`, Feature `audit-logging` и `incident-management` (`experiments/issue_434/hub-snapshot-vs-spoke-catalog.log`) | Каталог спицы использует путь-id (`callback/function/callback-scheduling`), повторов нет — проверено (353 уникальных id) |
| R-8 | Допущение | Задачи РТ-2 и РТ-4 в этом RFC не детализированы: issue просит РТ-1 и РТ-3 | РТ-4 — предусловие РТ-3; её строка в реестре остаётся |
| R-9 | Допущение | Индустриальный слой (TM Forum, UNSPSC, ОКПД 2, ГОСТ/НПА, внешние продукты) не входит в РТ-1, РТ-3 и ХАБ-1 | РТ-1 переносит id без изменений, поэтому слой присоединяется позже по id Capability; решение — BL-164 (подраздел 3.1) |
| R-10 | Риск | Связь с индустриальным слоем держится на поле `row`: его нет у `report-builder`, а номера строк могут смениться при новой версии классификации | BL-164 проверяет `row` всех Capability на новой версии классификации до сопоставления |
| R-11 | Риск | `docs/hub-research-dependencies.md` ведёт на старые пути Хаба (`038868dd`) и на несуществующий потребитель `prompts/tz-stats-generator.md` | Ссылки по SHA открываются, содержание не отличается по существу (подраздел 3.1); обновление — шаг 10 раздела 11 |

## 10. Обоснованные обходы

1. **Данные в runtime до нормы Хаба (РТ-1 отдельно от ХАБ-1).**
   - Что обойдено: порядок «сначала Хаб, затем компиляция» для
     данных.
   - Почему: иначе промпты ждут цикла компиляции Хаба, а BL-156
     выходит с заглушкой З-1.
   - Почему допустимо: по Ф-15 копия из спицы уже есть в манифесте.
     Норма не правится.
2. **Инициированы новые ID: ХАБ-1, Р-17, BL-163, BL-164.** Issue даёт право
   «инициировать допонительные связанные задачи». Без ХАБ-1 каталог не
   станет нормой. Без Р-17 решение о статусе `review` принял бы
   исполнитель. Без BL-163 заглушка З-1 не снимется в промптах. BL-164
   заведена по комментарию владельца к PR #437, чтобы не потерять
   индустриальную таксономию.
3. **Прототип вместо файла в runtime.** Файл
   `experiments/issue_434/prototype/mango-products.yaml` — образец формы
   для исполнителя РТ-1. В runtime он не кладётся: это решение владельца
   (A-08).

## 11. Рекомендуемые следующие шаги (после согласования)

1. **Исполнено (PR #437 слит; RFC-RT-001 → `accepted` в поправке 0.3).** Было: владелец: ревью и слияние PR #437; RFC-RT-001 → `accepted`.
   Почему: тела задач копируются с `blob/main`; до слияния ссылки ведут
   на ветку.
2. **Исполнено (Р-17 принято 2026-11-03, PR #440).** Было: владелец: решение Р-17. Почему: от него зависит состав каталога.
   Без решения половина функций `contact-center` либо выпадает, либо
   входит в норму без согласия.
3. **Исполнено (runtime #15/PR #16 и Хаб #719/PR #720 слиты 2026-11-04; ссылки — в реестре, раздел 6).** Было: владелец: создать РТ-1 в `mango-ba-ai-runtime` и ХАБ-1 в
   `hybrid-Intelligence-lab` (разделы 5, 6); ссылки вписать в реестр,
   раздел 6.** Почему: РТ-1 снимает З-1 для промптов сразу, ХАБ-1 делает
   каталог нормой. Задачи независимы, их можно вести параллельно.
4. **Исполнено: BL-163 после слияния РТ-1 (issue #442, PR #443, раздел 12).** Почему: промпт видит каталог только
   через SHA реестра (ТС-5). Строка З-1 снимается, И-2 → «Да».
   - 4а. **Владелец: создать РТ-6 в `mango-ba-ai-runtime` (раздел 12.3).**
     Почему: копия каталога старше Р-17, промпт держит правило чтения
     `added-for-review` как `accepted` (реестр, раздел 2.1).
   - 4а, 4б. **Исполнено (runtime PR #21 слит 2026-11-04, `f31dcde3`; реестр 0.4, раздел 13).** Было: РТ-6; новый срез реестра после РТ-6 и после слияния runtime PR #17
     (компиляция ХАБ-1: М-5, М-6; PR #17 закрыт, логика перенесена в PR #21). Почему: ТС-5 — одна точка SHA;
     срез должен включать и обновлённую копию, и норму привязки `c-in`.
   - 4в. **Исполнено (PR #439 слит; черновики пересобраны на реестре 0.4 в issue #444).** Было: PR [#439](https://github.com/G-Ivan-A/mango_ba_prompts/pull/439)
     (BL-156, BL-157) — пересобрать на реестре 0.3. Почему: черновики
     #439 закреплены на `5d8c201` и держат З-1 у Ш-2. Поверх этого PR
     валидатор ТС-5 даёт 62 ошибки, а сборщик падает на таблице снятых
     заглушек. Правка сборщика в одну строку (читать заглушки до «Снятые
     заглушки.») и пересборка снимают обе ошибки. Остаётся решение #439 по
     замеру RUN-0080: он снят на текстах реестра 0.2
     ([`experiments/issue_442/pr439-on-top.log`](../../experiments/issue_442/pr439-on-top.log)).
5. **Исполнено (runtime PR #21).** РТ-4 (глоссарии `voice-ucaas`, `analytics-reporting`). Почему:
   без пар `confusable_with` отрицательные случаи РТ-3 не по EP-G7.
6. **Исполнено структурно (runtime PR #21, `structural_only: true`).** РТ-3 (раздел 7). Почему: базовая линия «не хуже golden set» для
   трёх классов. Сначала нужно подтверждение `contact-center` человеком — задача BL-165 (раздел 13.4).
7. **Этап BL-156а исполнен (issue #444, раздел 13); BL-156б — после замера с повторами.** BL-156 после Р-15 (Р-14 принято в issue #432): промпт Ш-2 читает
   каталог по разделу 4.
   Почему: тогда BL-156 выйдет без заглушек З-1 и З-3.
8. **BL-157 — прогон на новых задачах** с отчётом по функциям каталога (BL-157а `DONE`; BL-157б — после BL-156а и BL-111).
   Почему: это доказательная база для снятия «по тесту» (BL-158).
9. **BL-164 держать `deferred (triggered)` до старта BL-133 или
   включения `P-08` в срез runtime; при старте — до оценки первого
   тендерного ТЗ.** Почему: потребитель индустриального слоя — оценка
   тендерного ТЗ (FR-06, BPR-10 потока требований Хаба). Сейчас его нет
   (Ф-20). Раньше времени слой раздует каталог и РТ-1. Позже — оценка
   ТЗ останется без сравнения с внешними продуктами.
10. **Обновить `docs/hub-research-dependencies.md`:** якоря
    `#classification`, `#classification-tz`, `#taxonomy-concept`,
    `#capability-decomposition` перевести на пути `2026-05-…` по
    закреплённому SHA Хаба, убрать несуществующий потребитель
    `prompts/tz-stats-generator.md`. Почему: ссылки работают, но ведут на
    старые пути. Исполнитель BL-164 и BL-133 должен попадать в текущий
    файл Хаба. Шаг не срочный, его можно сделать в любой задаче
    обслуживания или первым шагом BL-164.

РТ-2 (образцы разделов) остаётся строкой реестра. Её детализация — по
этому же шаблону, когда владелец решит, что `A-FR`, `A-UC`, `A-US`
входят в срез.

## 12. Поправка 0.3: исполнение BL-163 (issue #442)

Issue [#442](https://github.com/G-Ivan-A/mango_ba_prompts/issues/442)
запускает шаг 4 раздела 11 после проверки готовности. Постановка с
граничными случаями — [`experiments/issue_442/task-statement.md`](../../experiments/issue_442/task-statement.md).

### 12.1. Проверка готовности (2026-11-04)

| № | Условие | Факт | Итог |
| --- | --- | --- | --- |
| Г-1 | РТ-1 слита в runtime | [runtime PR #16](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/16) слит 2026-11-04T09:55Z, коммит `2db0ef5106883b01b096fe8c4af50334899e9fe0` — `main` runtime; issue [#15](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/15) закрыта | Да |
| Г-2 | Каталог на этом SHA: `closed: true`, 353 узла | [`taxonomy/mango-products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/2db0ef5106883b01b096fe8c4af50334899e9fe0/taxonomy/mango-products.yaml): 353 узла, Domain 7, Capability 43, Feature 151, Atomic Function 152 | Да |
| Г-3 | `source_sha256` копии = каталог спицы на `source_commit` | `c5ff76c3…` = sha256 `docs/taxonomy/products.json` на `7f920e2` | Да |
| Г-4 | id, уровни и родители копии = текущий каталог спицы | 353 из 353 совпадают | Да |
| Г-5 | Пути раздела 2 реестра есть на SHA (ТС-2), версии (ТС-3) | Все 9 путей есть; кроме каталога, файлы не менялись с `5d8c201` | Да |
| Г-6 | Решение Р-17 | Принято 2026-11-03, записано PR #440 (слит 2026-11-04T10:25Z) | Да |
| Г-7 | ХАБ-1 (норма привязки) | Хаб [PR #720](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/720) слит; компиляция в runtime — [PR #17](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/17), открыт | Не блокирует: М-5 и М-6 не нужны промптам (раздел 4) |
| Г-8 | Копия совпадает со спицей по `lifecycle` и статусу | Копия: 74 узла `added-for-review`, `catalog_status: review`; спица после PR #440: `accepted` | **Нет** — расхождение R-2, не блокирует (ниже) |

Лог проверки — [`experiments/issue_442/runtime-readiness.log`](../../experiments/issue_442/runtime-readiness.log),
снимок PR и issue — [`experiments/issue_442/cross-repo-state.log`](../../experiments/issue_442/cross-repo-state.log).

Почему Г-8 не блокирует BL-163: промпт связывает требование с функцией
по id (раздел 4, шаги 2–4), а id, уровни и родители совпадают. Различие —
только пометка `lifecycle`, а Р-17 приняло все 74 узла. Поэтому реестр
переходит на срез с правилом чтения (реестр, раздел 2.1; шаг 5 текста
раздела 4). Ждать обновления копии — значит держать З-1 во всех промптах
ради метаданных, которые уже решены владельцем.

### 12.2. Что исполнено

- Реестр [`standards/bcreq-runtime-references.md`](../../standards/bcreq-runtime-references.md)
  0.3: SHA `2db0ef51` в разделе 1 и во всех ссылках раздела 2; И-2 — «Да»
  со ссылкой на каталог; раздел 2.1 — сверка копии и правило чтения;
  З-1 перенесена в снятые заглушки (id не переиспользуется); строка РТ-1
  ведёт на задачу и PR runtime; новая строка РТ-6.
- Тест клона `scripts/validate_issue_430_runtime_refs.py`: каталог есть,
  `closed: true`, число узлов, id, уровни и родители совпадают с каталогом
  спицы, `source_sha256` совпадает с каталогом спицы на `source_commit`.
  Мутационная проверка (17 порч реестра, RFC и копии каталога — все
  ловятся): [`experiments/issue_442/mutation-check.log`](../../experiments/issue_442/mutation-check.log).
- Runtime [PR #17](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/17)
  (компиляция ХАБ-1, открыт, на ревью; голова `8098487`) на 2026-11-04 не меняет
  `taxonomy/mango-products.yaml`, но меняет `contracts/c-in.md`, `golden/*`,
  `taxonomy/products.yaml`, `evaluation/*` и добавляет отрицательный случай
  `gs-cc-neg-05` (функция вне каталога). После слияния нужен новый срез
  реестра: факты И-5 (golden set) и М-5/М-6 надо перепроверить (шаг 4б
  раздела 11). В PR попали байткод-файлы `tests/__pycache__/*.pyc` —
  замечание для ревью runtime, на спицу не влияет.
- Остаётся в BL-156: промпт Ш-2 ссылается на каталог (последний пункт
  «Готово, когда» BL-163). Правка `prompts/` — только «не хуже базовой
  линии golden set» (DEC-427-11).

### 12.3. РТ-6 — тело задачи для `mango-ba-ai-runtime` (копировать целиком)

Почему id РТ-6, а не РТ-5: РТ-5 уже занят альтернативой «слой в runtime»
для индустриального слоя (раздел 3.1, карточка BL-164), а в Хабе есть
правило `PT-5` (латиница), которое легко спутать с РТ-5. Номер РТ-5 не
используется для другой задачи.

Заголовок: `РТ-6. Обновить копию каталога продуктов до решения Р-17 (lifecycle accepted)`

````markdown
## Контекст задачи

- Полный URL постановки: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-runtime-product-catalog-golden-set.md (RFC-RT-001, раздел 12.3)
- Полные URL связанных PR/issue: https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/16, https://github.com/G-Ivan-A/mango_ba_prompts/pull/440, https://github.com/G-Ivan-A/mango_ba_prompts/issues/442
- Полные URL связанных репозиториев: https://github.com/G-Ivan-A/mango_ba_prompts (ССОТ значений каталога)
- Важные решения, которые уже приняты:
  - решение владельца Р-17: 74 узла с портала приняты, `lifecycle: accepted`, каталог `status: accepted` (https://github.com/G-Ivan-A/mango_ba_prompts/pull/437#issuecomment-6605372609);
  - копия каталога — данные, а не норма: правится в runtime по прецеденту РТ-1 (раздел `copied` манифеста).
- Что нельзя считать известным из предыдущих задач: что id или связи узлов менялись — не менялись (сверка 353 из 353).

## Решаемая проблема

Копия `taxonomy/mango-products.yaml` (https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/2db0ef5106883b01b096fe8c4af50334899e9fe0/taxonomy/mango-products.yaml) снята с коммита каталога спицы `7f920e2e967ad1331e027fef885ea68ecef7070f` до решения Р-17. В спице каталог уже `accepted` (https://github.com/G-Ivan-A/mango_ba_prompts/blob/e3597fd74da9c4f631ca46697c643462e2cf0b85/docs/taxonomy/products.json). Модель читает у принятых узлов `added-for-review`.

## Story

**Как есть:**

- Кто действует: модель читает каталог runtime по SHA реестра спицы.
- Что происходит сейчас: 74 узла — `lifecycle: added-for-review`, `catalog_status: review`.
- Где возникает ошибка, блокировка или долг: промпт спицы держит отдельное правило чтения для этих узлов (реестр спицы, раздел 2.1).

**Как должно быть:**

- Кто действует: та же модель.
- Какой результат должен быть доступен после решения: копия совпадает с каталогом спицы, включая `lifecycle` и статус.
- Как Пользователь принимает или возвращает решение на доработку: сверяет `source_sha256` с каталогом спицы и прогоняет `sh tests/runtime-smoke.sh`.

## ФТ

- [ ] `source`, `source_commit`, `source_sha256` указывают на коммит каталога спицы `e3597fd74da9c4f631ca46697c643462e2cf0b85` (или более поздний коммит каталога в `main` спицы на дату задачи).
- [ ] `catalog_status: "accepted"`; у 74 узлов с портала `lifecycle: accepted`; узлов `added-for-review` нет.
- [ ] id, `level`, `name`, `parents`, `classes`, `params` всех 353 узлов не меняются.
- [ ] Запись `copied` манифеста получает новый `source_commit`.
- [ ] Комментарий-шапка файла описывает `accepted` вместо `added-for-review`.

## НФТ

- [ ] Правка только данных: `AGENTS.md`, `contracts/`, `skills/`, `evaluation/` не правятся (правило 13).
- [ ] Одна строка — один узел (проверка `grep`).
- [ ] Проверки `tests/test_product_catalog.py` и `tests/runtime-smoke.sh` зелёные.

## Цель

Копия каталога runtime совпадает с каталогом спицы после Р-17.

Definition of Done:

- `sh tests/runtime-smoke.sh` — `runtime smoke test passed`;
- в PR — sha256 каталога спицы на новом `source_commit` и число узлов по `lifecycle`;
- в PR — SHA коммита слияния для реестра спицы (новый срез раздела 1).

## Operating Mode

- `Structured`: меняются только `lifecycle`, статус и провенанс; расхождение id или связей — вопрос в PR, не правка.

## Специфика работы с Конардом

- **молчание = согласие:** если Пользователь мержит PR без комментариев, решения приняты;
- **комментарий + ручной перезапуск:** доработка в том же PR;
- **close:** закрытие PR означает отказ от решения;
- draft PR используется как место отложенной проверки до acceptance.

## Обоснованные обходы

- Нет: задача повторяет порядок РТ-1 для данных.
````

После слияния РТ-6 спица обновляет срез реестра (раздел 1) и снимает
правило чтения раздела 2.1. Шаги после согласования — раздел 11, пункты
4а и 4б.

## 13. Поправка 0.4: исполнение BL-156а (issue #444)

Issue [#444](https://github.com/G-Ivan-A/mango_ba_prompts/issues/444)
продолжает BL-156 и BL-157 после слияния
[PR #439](https://github.com/G-Ivan-A/mango_ba_prompts/pull/439). Постановка
с граничными случаями —
[`experiments/issue_444/task-statement.md`](../../experiments/issue_444/task-statement.md),
разбор готовности —
[`docs/analysis/2026-11-04-bl-156-readiness-check-444.md`](../analysis/2026-11-04-bl-156-readiness-check-444.md).

### 13.1. Проверка готовности (2026-11-04)

| № | Условие | Факт | Итог |
| --- | --- | --- | --- |
| Г-9 | РТ-3, РТ-4, РТ-6 и компиляция ХАБ-1 слиты в runtime | [runtime PR #21](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/21) слит 2026-11-04T14:55Z, `f31dcde33f0bc120244128faab98fc0162e45701` — `main` runtime; issue [#20](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/20) закрыта | Да |
| Г-10 | Пути и версии реестра есть на SHA (ТС-2, ТС-3) | 13 путей и 11 версий на `f31dcde3`; база знаний `docs/kb` не менялась с `2db0ef51` | Да |
| Г-11 | Копия каталога = каталог спицы, `lifecycle` без дрейфа | [`taxonomy/mango-products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/f31dcde33f0bc120244128faab98fc0162e45701/taxonomy/mango-products.yaml): 353 узла, id, уровни и родители совпадают, `catalog_status: accepted`; расхождение Г-8 снято РТ-6 | Да |
| Г-12 | Golden set трёх классов в строгой форме (функция кейса — id каталога класса) | `contact-center` 7 кейсов (2 положительных, 5 отрицательных), `voice-ucaas` 6, `analytics-reporting` 5; везде `structural_only: true`, `confirmed_by: none`; функция вне каталога — только в `declared_function` | Да, с оговоркой: смысл кейсов человек не проверял (BL-165) |
| Г-13 | Глоссарии трёх классов с парами `confusable_with` (РТ-4) | 8, 6 и 4 пары; узлы `catalog` есть в каталоге | Да |
| Г-14 | PR #439 слит, черновики BL-156 — в `main` спицы | слит 2026-11-04T13:36Z | Да |

Лог — [`experiments/issue_444/runtime-readiness.log`](../../experiments/issue_444/runtime-readiness.log),
снимок трёх репозиториев — [`experiments/issue_444/cross-repo-state.log`](../../experiments/issue_444/cross-repo-state.log).

### 13.2. Решение по PR #17 и сверка с комментарием к PR #21

Решение владельца в issue #444: принять строгий вариант PR #21 — функция
кейса строго равна id каталога, без исключений и магических маркеров;
PR #17 остаётся закрытым, его логика в поток не интегрируется.

Кажущееся расхождение. В [комментарии к runtime PR #21](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/21#issuecomment-6633420940)
(2026-11-04T14:36Z) владелец просил «взять из PR #17 ту логику и
проверки, которых нет в текущем PR #21, и реализовать их прямо здесь».
Issue #444 говорит, что логика #17 «не интегрируется». Сверка по коммитам
runtime показывает, что речь о разных частях #17:

| Часть PR #17 | Где в PR #21 | Итог |
| --- | --- | --- |
| Норма PT-5 в `contracts/c-in.md`: функция продукта на входе — id каталога класса | `09cc684` | перенесено |
| Проверки `check_taxonomies` 6–11 и `check_golden` 2–8 в `evaluation/validate-package.md` | `09cc684`, `23d2a4b` | перенесено |
| Тесты привязки к каталогу (прокси G-mach) | `449d772`, `tests/test_catalog_binding.py` | перенесено |
| Байткод `tests/__pycache__/*.pyc` в индексе | `11fad36` убирает его и дополняет `.gitignore` | снято |
| Форма отказа по каталогу: `atomic_function: queue-callback-offer   # намеренно вне каталога` и `grep -v` по этому комментарию в `tests/runtime-smoke.sh` | не перенесено: в PR #21 `atomic_function` — всегда id каталога, объявленная функция вне каталога — в поле `declared_function` | **отвергнуто** |

Вывод: комментарий к PR #21 исполнен (проверки и норма перенесены), а
решение issue #444 отвергает только форму #17 — маркер-исключение в
комментарии. Расхождения нет. Спица не меняет ничего в runtime: строгая
форма уже в `main` (`f31dcde3`).

### 13.3. Что исполнено

- Реестр [`standards/bcreq-runtime-references.md`](../../standards/bcreq-runtime-references.md)
  0.4 на `f31dcde3`: И-5 (golden set трёх классов) и И-6 (глоссарии) —
  «Да»; З-3 и З-4 перенесены в снятые заглушки; раздел 2.1 снят (РТ-6);
  раздел 2.2 — звено М-4: каталог для раздела 2.2 BCREQ (анализ влияния
  на продукты).
- 11 черновиков BL-156 в `prompts/drafts/` пересобраны на реестре 0.4,
  черновик Ш-2 читает каталог по звену М-4 (раздел 4).
- 14 промптов v0.1 в `prompts/` ссылаются на runtime по SHA (долг ТС-1
  раздела 7 реестра закрыт).
- Golden set Ш-В [RUN-0081](../../runs/2026/RUN-0081/outputs/golden-set-report.md):
  A с типом гейта — 56/62, ядро 9/11 против 10/11 RUN-0079. По DEC-427-11
  тип гейта в `prompts/` не опубликован (этап BL-156б), ссылки по SHA
  остаются.

### 13.4. Задачи бэклога из решений владельца

| ID | Что | Где | Статус |
| --- | --- | --- | --- |
| BL-165 | Human Review кейсов `contact-center` golden set runtime (решение issue #444: отложено) | [Карточка](../../pr-ops/backlog-ba-model.md#bl-165-human-review-кейсов-contact-center-в-golden-set-runtime) | deferred (triggered) |
| BL-166 | Маппинг 46 кандидатов RUN-0074 на классы и функции каталога (подраздел 7.1) | [Карточка](../../pr-ops/backlog-ba-model.md#bl-166-маппинг-кандидатов-run-0074-на-классы-и-функции-каталога) | deferred (triggered) |
| BL-156б | Публикация черновиков и типа гейта после замера с повторами | [Карточка BL-156](../../pr-ops/backlog-ba-model.md#bl-156б-публикация-промптов-по-тесту-и-типа-гейта) | deferred (triggered) |

## Related Artifacts

- [Реестр справочников runtime](../../standards/bcreq-runtime-references.md) — И-2, З-1 (снята), З-3, РТ-1…РТ-4, РТ-6
- [Проверка готовности BL-156а](../../experiments/issue_444/runtime_readiness.py) — [лог](../../experiments/issue_444/runtime-readiness.log), [постановка](../../experiments/issue_444/task-statement.md), раздел 13
- [Проверка готовности BL-163](../../experiments/issue_442/runtime_readiness.py) — [лог](../../experiments/issue_442/runtime-readiness.log), [постановка](../../experiments/issue_442/task-statement.md)
- [RFC #427, раздел 8](2026-11-bcreq-flow-processes-prompts.md) — исключения, требования, заглушка
- [Каталог продуктов спицы](../taxonomy/products.json) — ССОТ значений
- [Прототип каталога runtime](../../experiments/issue_434/prototype/mango-products.yaml) и [генератор](../../experiments/issue_434/compile_catalog_prototype.py)
- [Симуляция проверок М-2](../../experiments/issue_434/runtime_smoke_sim.sh) — [лог](../../experiments/issue_434/runtime-smoke-sim.log)
- [Валидатор постановки](../../scripts/validate_issue_434_runtime_tasks.py)
- [Классификация Хаба v3.0](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-22-classification.md) — исток таксономии Mango и индустриальный слой (подраздел 3.1)
- [Декомпозиция функций Хаба](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-27-capability-decomposition.md), [концепция таксономии](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-26-taxonomy-concept.md), [поток требований](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/c06075d0b45da70cb68e2df3851b861b5ec3aed1/research/mango/2026-05-22-requirements-flow.md) — черновики и требования для BL-164
- [Инвентаризация индустриального слоя](../../experiments/issue_434/industry_taxonomy_inventory.py) — [лог](../../experiments/issue_434/industry-taxonomy-inventory.log)
- [BL-164](../../pr-ops/backlog-ba-model.md#bl-164-индустриальная-таксономия-для-оценки-тендерного-тз) — задача по индустриальной таксономии
