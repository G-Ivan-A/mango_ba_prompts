---
status: draft
version: 0.2
updated: 2026-11-03
temperature: 0.1
ai-generated: true
type: standard
scope: bcreq-flow
runtime_repo: "https://github.com/G-Ivan-A/mango-ba-ai-runtime"
runtime_sha: "5d8c201511fd730a596c9f9b4588470a7b01edc9"
related_artifacts:
  - "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
  - "standards/bcreq-flow-glossary.md"
  - "docs/ba-processes/bcreq-manual-process.md"
  - "docs/contracts/kb-citations.md"
  - "pr-ops/backlog-ba-model.md"
  - "docs/rfc/2026-11-runtime-product-catalog-golden-set.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/427"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/430"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/434"
---

# Справочники runtime для промптов потока BCREQ

> Носитель — [RFC #427](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md#8-исключения-ссылки-промптов-на-mango-ba-ai-runtime)
> (`accepted`), решения DEC-427-09 и DEC-427-10, задачи
> [BL-154](../pr-ops/backlog-ba-model.md#bl-154-справочники-runtime-перечень-требования-закреплённый-срез)
> и [BL-155](../pr-ops/backlog-ba-model.md#bl-155-заглушки-недостающих-справочников-runtime).
> Отдельный файл — по
> [поправке 0.4 RFC](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md#поправка-04-гейт-и-его-типы-issue-430)
> (issue [#430](https://github.com/G-Ivan-A/mango_ba_prompts/issues/430)):
> [базовый стандарт](bcreq-prompt-base-standard.md#34-источники-цитаты-и-справочники-runtime)
> BL-151 (решение Р-14, issue #432, PR #435) подключает этот реестр
> ссылкой, а не копией (правила БС-18…БС-22). Режим — «по тесту» до прогонов на новых задачах.
> Термины — [словарь потока](bcreq-flow-glossary.md).

Промпт ручного потока самодостаточен. Исключение — справочники
`mango-ba-ai-runtime` из раздела 2: они больше бюджета вставки или
меняются чаще промпта, нужны модели как факт или образец, а не как
правило, и имеют стабильный путь и версию (критерии раздела 8.1 RFC).
Правила исполнения в справочник не выносятся.

## 1. Закреплённый срез

| Поле | Значение |
| --- | --- |
| Репозиторий | [`G-Ivan-A/mango-ba-ai-runtime`](https://github.com/G-Ivan-A/mango-ba-ai-runtime) |
| SHA | `5d8c201511fd730a596c9f9b4588470a7b01edc9` |
| Дата коммита | 2026-11-01 |
| Проверено | 2026-11-02, клон на SHA: все пути раздела 2 со статусом «Да» или «Частично» существуют |

Это **единственная точка обновления SHA** (ТС-5). Промпты набора берут
SHA отсюда при сборке; другой SHA в ссылке на runtime — ошибка
валидатора `scripts/validate_issue_430_runtime_refs.py`.

Как обновить срез:

1. Выбрать коммит runtime, проверить пути раздела 2 и требования ТС-2,
   ТС-3 на нём.
2. Заменить SHA в таблице выше, во frontmatter (`runtime_sha`) и во всех
   ссылках раздела 2 одной правкой.
3. Пересобрать промпты набора; запись в `CHANGELOG.md`.

## 2. Перечень

Ссылка дана на закреплённый SHA. «Шаги» — шаги потока Ш- по
[процессу BCREQ, часть 0](../docs/ba-processes/bcreq-manual-process.md#0-поток-bcreq-процессы-шаги-гейты)
и разделу 9.2 RFC.

| № | Справочник | Ссылка на срезе | Есть в runtime | Решение | Шаги |
| --- | --- | --- | --- | --- | --- |
| И-1 | База знаний продуктов | [`docs/kb/MAP.json`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/docs/kb/MAP.json) → `docs/kb/maps/<id>.json` → `docs/kb/<slug>/sections/NN-*.md`; путь поиска — [`docs/kb/USAGE.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/docs/kb/USAGE.md) | Да: 25 документов в `MAP.json`, 18 каталогов документов | **Ссылка обязательна** | Ш-1, Ш-2, Ш-3, Ш-6, Ш-7 |
| И-2 | Таксономия продуктов | [`taxonomy/products.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/products.yaml) | Частично: 3 класса, уровни Domain → Capability → Feature → Atomic Function, значений ниже класса нет | Ссылка + заглушка З-1 | Ш-2 |
| И-3 | Шаблон документа BCREQ | [`templates/bcreq-skeleton.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/templates/bcreq-skeleton.md) | Да: 14 слотов, формы F-SHORT, F-APPROVAL, F-CLASSIC, F-NARRATIVE | Ссылка | Ш-0, Ш-В, Ш-Р |
| И-4 | Примеры разделов (ФТ, UC, US, НФТ, ОРР) | — | Нет (`A-FR`, `A-UC`, `A-US` вне среза) | Заглушка З-2 | Ш-3, Ш-4, Ш-5, Ш-8, Ш-С |
| И-5 | Golden set по классу продуктовой таксономии | [`golden/cases.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/golden/cases.yaml) | Частично: только contact-center, 6 синтетических кейсов, `structural_only: true` | Ссылка для contact-center + заглушка З-3 | Ш-В |
| И-6 | Доменный глоссарий | [`taxonomy/domain-glossary.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/domain-glossary.yaml) | Частично: только contact-center, 8 терминов | Ссылка для contact-center + заглушка З-4 | Ш-1 |
| И-7 | Порядок источников и уровни доверия | [`taxonomy/source-tiers.yaml`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/taxonomy/source-tiers.yaml) | Да | Ссылка в базовом стандарте (BL-151) | все шаги |
| И-8 | Чек-лист гейта G-human | [`evaluation/g-human-checklist.md`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/evaluation/g-human-checklist.md) | Да | Ссылка | Ш-В |
| И-9 | Уроки прогонов | — (здесь: `standards/bcreq-lessons/lessons.json`) | — | **Не исключение**: уроки — правила, входят в промпт (ADR-017, DEC-411-01) | — |
| И-10 | Мета-стандарты разделов | — (здесь: `standards/bcreq-sections/`) | — | **Не исключение**: правила входят в промпт через профиль GENERATE | — |

И-8 — чек-лист **ключевого** гейта: runtime сам разводит человеческий и
машинный гейт («Всё, что попало в чек-лист `G-mach`, здесь не
перепроверяется», `evaluation/g-human-checklist.md`). Типы гейтов —
[словарь потока, раздел 3](bcreq-flow-glossary.md#3-гейт-определение-типы-ключевые-гейты).

## 3. Требования к справочникам

| № | Требование | Проверка | Как проверено сейчас |
| --- | --- | --- | --- |
| ТС-1 | Ссылка закреплена по коммиту: `https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/<SHA>/…`, `tree/<SHA>/…` или raw-URL с `<SHA>`; не `main` | Валидатор: в ссылке на runtime 40-символьный SHA | `validate_issue_430_runtime_refs.py`: все ссылки этого файла; новые промпты; долг раздела 6 не растёт |
| ТС-2 | Путь стабилен и описан в `USAGE.md` или `README.md` runtime | Ссылка открывается на закреплённом SHA | Клон на SHA, 2026-11-02 (раздел 1) |
| ТС-3 | У справочника есть версия (`version` в YAML или frontmatter) и источник происхождения | Поле есть | `products.yaml`, `domain-glossary.yaml`, `cases.yaml` — `version: "1.0"`; `source-tiers.yaml` — `"0.5"`; `g-human-checklist.md` — `version: 1.0`; `MAP.json` — `schema_version` |
| ТС-4 | Справочник содержит факты и образцы, не правила исполнения | Ревью при включении в перечень | И-9, И-10 исключены по этому требованию |
| ТС-5 | Одна точка обновления SHA — раздел 1 этого файла | Один SHA во всех промптах набора | Валидатор: любой SHA runtime в репозитории вне истории совпадает с разделом 1 |
| ТС-6 | Если модель не открывает ссылки — БА прикладывает файл; промпт говорит это явно | Строка в промпте | Текст строки — раздел 5; вставка — BL-156 |
| ТС-7 | Цитата из справочника — с локатором (документ, раздел) по [контракту цитат KB](../docs/contracts/kb-citations.md) | Проверка Ш-В | Правило входит в базовый стандарт BL-151 |

## 4. Заглушки

Где справочника нет или он неполон, промпт шага содержит блок (раздел
8.4 RFC):

```text
[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]
Действуй без образца: не придумывай значения, которых нет во входе;
пометь место [ТРЕБУЕТСЯ УТОЧНЕНИЕ] и добавь вопрос в 8.4.
```

Заглушка — не ошибка прогона: в реестре прогона она пишется как
известный пробел, а не как дефект промпта. Когда справочник появляется в
runtime, строка ниже снимается, справочник получает ссылку в разделе 2,
SHA обновляется по разделу 1.

| № | Справочник | Условие заглушки | Шаги | Строка `<имя>` | Задача для runtime |
| --- | --- | --- | --- | --- | --- |
| З-1 | И-2 Таксономия продуктов | всегда для уровней Feature и Atomic Function | Ш-2 | `И-2 таксономия продуктов: уровни ниже класса не заполнены` | РТ-1 |
| З-2 | И-4 Примеры разделов | всегда | Ш-3, Ш-4, Ш-5, Ш-8, Ш-С | `И-4 примеры разделов ФТ, НФТ, UC, US, ОРР` | РТ-2 |
| З-3 | И-5 Golden set | класс задачи — `voice-ucaas` или `analytics-reporting` | Ш-В | `И-5 golden set класса <класс>` | РТ-3 |
| З-4 | И-6 Доменный глоссарий | класс задачи — `voice-ucaas` или `analytics-reporting` | Ш-1 | `И-6 доменный глоссарий класса <класс>` | РТ-4 |

Шаг выпуска Ш-Р сам по себе — заглушка промпта (пилот, раздел 9.2 RFC),
а не заглушка справочника: ему нужен только И-3. Промпт Ш-Р — в BL-156.

## 5. Строка для промпта (ТС-6)

```text
Справочники runtime закреплены на коммите <SHA из раздела 1>. Если ты не
можешь открыть ссылку, скажи об этом и попроси БА приложить файл; не
восстанавливай содержимое справочника по памяти.
```

Основание: `docs/guides/00-quick-start.md` runtime — «Если модель не
может открыть ссылку, вставьте или приложите `AGENTS.md`, …».

## 6. Задачи для репозитория runtime

Создаёт владелец в
[`mango-ba-ai-runtime`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues):
у исполнителя этой спицы нет решения о бэклоге runtime (A-08 RFC #427).
Ссылка на задачу runtime вписывается в столбец «Задача runtime» после
создания.

Готовые к копированию тела задач РТ-1 и РТ-3, задача Хаба ХАБ-1 и
механизм снятия заглушки З-1 — в
[RFC-RT-001](../docs/rfc/2026-11-runtime-product-catalog-golden-set.md)
(issue [#434](https://github.com/G-Ivan-A/mango_ba_prompts/issues/434)).
Строки РТ-1 и РТ-3 ниже расширены по нему: каталог нужен всем трём
классам, а не только `contact-center`, и живёт в отдельном файле
`taxonomy/mango-products.yaml`, а не в словаре формы `taxonomy/products.yaml`.

| № | Что нужно в runtime | Снимает заглушку | Приоритет | Почему | Задача runtime |
| --- | --- | --- | --- | --- | --- |
| РТ-1 | Закрытый каталог продуктов `taxonomy/mango-products.yaml`: все уровни Domain → Capability → Feature → Atomic Function по всей линейке (каталог спицы 2026-10-28.1, 353 узла) с классами runtime у каждого узла; проверка smoke без каталога падает. Норма привязки `c-in` — задача Хаба ХАБ-1 ([RFC-RT-001, разделы 5–6](../docs/rfc/2026-11-runtime-product-catalog-golden-set.md#5-рт-1--тело-задачи-для-mango-ba-ai-runtime-копировать-целиком)) | З-1 | P1 | `c-in` требует `atomic_function`, а каталога функций нет — модель придумывает функцию или оставляет пусто | — (создаёт владелец) |
| РТ-2 | Примеры разделов ФТ, НФТ, UC, US, ОРР (по одному эталону на раздел, с источником происхождения) | З-2 | P1 | Образцы улучшают форму вывода шагов Ш-3…Ш-8; сейчас `A-FR`, `A-UC`, `A-US` вне среза | — (создаёт владелец) |
| РТ-3 | Golden set для `voice-ucaas` и `analytics-reporting` (`golden/cases-<класс>.yaml`); у каждого случая `product_class` и `atomic_function` из каталога РТ-1; подтверждение человеком кейсов `contact-center` (`structural_only: false`) ([RFC-RT-001, раздел 7](../docs/rfc/2026-11-runtime-product-catalog-golden-set.md#7-рт-3--тело-задачи-для-mango-ba-ai-runtime-копировать-целиком)) | З-3 | P1 | Issue #427: «голден сет по каждому классу проуктовой таксономии» | — (создаёт владелец) |
| РТ-4 | Доменный глоссарий для `voice-ucaas` и `analytics-reporting` | З-4 | P2 | Термины продукта нужны глоссарию раздела 1 BCREQ (К-14) | — (создаёт владелец) |

## 7. Известный долг: ссылки на `main` в текущих промптах

На 2026-11-02 все 14 файлов `prompts/bcreq-*.md` ссылаются на runtime
через `blob/main` — нарушение ТС-1. Ссылок три:

- `mango-ba-ai-runtime/blob/main/docs/kb/README.md`;
- `mango-ba-ai-runtime/blob/main/docs/kb/MAP.json`;
- `mango-ba-ai-runtime/blob/main/taxonomy/products.yaml`.

Почему не исправлено в этом PR: замена ссылки меняет то, что модель
читает в принятых промптах, а правка `prompts/` допускается только
«не хуже базовой линии golden set» (BL-156, DEC-427-11). Промпты шагов
BL-156 собираются уже со ссылками на срез раздела 1. До этого валидатор
фиксирует долг: список файлов и ссылок на `main` не растёт, новые ссылки
на runtime — только по SHA.

## Related Artifacts

- [RFC #427, раздел 8](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md#8-исключения-ссылки-промптов-на-mango-ba-ai-runtime) — исключения, требования, заглушка
- [BL-114](../pr-ops/backlog-ba-model.md#bl-114-самодостаточность-промптов-и-справочники-в-runtime) — правило самодостаточности; перечень и требования — здесь
- [Словарь потока BCREQ](bcreq-flow-glossary.md) — термины «справочник runtime», «заглушка», типы гейтов
- [Процесс BCREQ, часть 0](../docs/ba-processes/bcreq-manual-process.md#0-поток-bcreq-процессы-шаги-гейты) — шаги потока
- [Контракт цитат KB](../docs/contracts/kb-citations.md) — ТС-7
- [RFC-RT-001](../docs/rfc/2026-11-runtime-product-catalog-golden-set.md) — тела задач РТ-1, РТ-3, ХАБ-1 и механизм снятия З-1
