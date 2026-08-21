---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/269"
related_artifacts:
  - "kb/sources/integration_amocrm/meta.json"
---

# Источники, доступные модели в прогоне

> **Зачем файл.** Разделять «модель процитировала документ» и «модель утверждает без
> источника» можно только зная, что именно было ей показано. Ниже — фактический
> перечень из экспорта чата, а не предполагаемый.

## Документ во вложении (PDF)

| Параметр | Значение |
| --- | --- |
| Имя файла | `Mango_office_integration_amoCRM.pdf` |
| Размер | 8 867 257 байт (8.5 МБ), 153 страницы |
| Статус разбора в чате | `parse_status: success` |
| Где в репозитории | **бинарник не хранится**; источник зарегистрирован в [`kb/sources/integration_amocrm/meta.json`](../../../../kb/sources/integration_amocrm/meta.json) (версия 25.08.2025) |
| Машиночитаемая БЗ | **отсутствует**: в [`kb/processed/`](../../../../kb/processed/README.md) документа нет |

Практическое следствие: ссылки модели на «п. 2.4», «п. 2.10», «п. 2.14», «п. 7, 15»
PDF **невозможно проверить средствами репозитория**. В
[`../feedback/ba-review.md`](../feedback/ba-review.md) они помечены как
непроверенные, а не как подтверждённые факты.

## Веб-источники

Модель выполнила один веб-поиск (18 результатов) и извлекла **одну** страницу
целиком. Полный список выдачи сохранён в
[`../logs/chat-transcript.md`](../logs/chat-transcript.md).

| Роль | Страница |
| --- | --- |
| Извлечена целиком (использована как источник) | [Неразобранное — API amoCRM](https://www.amocrm.ru/developers/content/crm_platform/unsorted-api) |
| Указана Заказчиком как доверенная | [Неразобранное и форма на сайт](https://www.amocrm.ru/support/starting_work/forms) |
| Прочее | 16 результатов выдачи, включая нефирменные площадки (`sipuni`, `pact.im`, `apimonster`, `amo.academy`), в текст ответа не попавшие |

Ссылки вида `[[13]]` и `[[1]]` в ответах модели — это индексы выдачи поиска
(13 = Unsorted API, 1 = support/starting_work/forms). Вне интерфейса чата они не
разрешаются: как цитаты в ТЗ они непригодны (см. дефект Д-3 в
[`../feedback/ba-review.md`](../feedback/ba-review.md)).
