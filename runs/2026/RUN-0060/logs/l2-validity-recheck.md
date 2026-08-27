---
status: draft
version: 0.1
updated: 2026-08-27
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/333"
related_artifacts:
  - "runs/2026/RUN-0058/outputs/L2-gap-matrix.md"
  - "runs/2026/RUN-0060/outputs/L4-combined-gap-report.md"
---

# Перепроверка выводов L2 (RUN-0058) по спецификации от 2026-08-27

Постановка #333 требует: «Если сформулировано корректно, оставить, если
ошибки — скорректировать». Ниже — протокол проверки: что подтверждено дословно
и что исправлено. Итоговые формулировки перенесены в
[отчёт L4](../outputs/L4-combined-gap-report.md), раздел 15.

## Подтверждено дословно (перенесено в L4 без изменений)

| # | Вывод L2 | Чем подтверждён в спецификации |
| --- | --- | --- |
| 1 | 14 операций раздела «Чаты» | Раздел `Чаты` индекса источников |
| 2 | GAP-R1: события только участникам чата, доступа на уровне работодателя нет | `WebhookActionChatCreated`, `WebhookActionChatMessageCreated`, `404` у `get-participant-list` / `get-chat-messages`, отсутствие тега «Чаты на уровне работодателя» |
| 3 | GAP-R3: событие сообщения не несёт вакансию, резюме и текст | `WebhookPayloadChatMessageCreated` |
| 4 | GAP-R4: нет сортировки и фильтра «изменённые с»; `page` 0…50, `per_page` 1…20 | Параметры `get-common-chat-list` |
| 5 | GAP-R5: фильтр по вакансиям — строка вида `[1,2,3]`, не более 100 идентификаторов | `filter_with_vacancy_ids` |
| 6 | GAP-R6: `file_upload_ids` `maxItems: 1`; пример условий — 20 971 520 байт, JPEG/PNG | `ChatsCommonMessagePostFileUploadIds`, пример условий загрузки |
| 7 | GAP-R8: смена статуса отклика — отдельное действие | `change-negotiation-action`, `put-negotiations-collection-to-next-state` |
| 8 | M2 / Путь 4: `vacancies_only_mine` по умолчанию `false`; событие отклика несёт `chat_id`, `vacancy_id`, `resume_id`, `topic_id`, `employer_id` | `WebhookActionVacancyOnlyMineSettings`, `WebhookPayloadNewResponseOrInvitationVacancy` |
| 9 | Ограничения вебхуков: 5 секунд на ответ, повторы, один URL на пользователя в приложении, удаление подписок при отзыве доступа, «не являются средствами гарантированной доставки» | Описание `post-webhook-subscription` |
| 10 | `write_message_state` / `send_file_state` читаются заранее | `ChatsCommonChatState` |
| 11 | `text` до 20 000 символов, `idempotency_key` UUID, признак `is_automated` | `ChatsCommonMessagePostText` |
| 12 | Менеджерский контекст: `get-manager-accounts`, заголовок `X-Manager-Account-Id` | Раздел «Менеджеры работодателя» |

## Исправлено

| # | Где | Было в L2 | Стало в L4 | Влияние на вердикт |
| --- | --- | --- | --- | --- |
| 1 | ФТ-05 | «`filter_has_text_message` — только чаты, в которых есть хотя бы одно текстовое сообщение» | «Фильтр по чатам с активными переписками. Доступно только для работодателя»; тип `SIMPLE` — «сообщение с текстом **либо вложениями**» | **Да → Частично**, новый **GAP-R11** |
| 2 | ФТ-04 | `vacancy_id` и `last_message` отнесены к `ChatsCommonChatBasic` | Поля приходят из inline-ветви `allOf` схемы `ChatsCommonChatItems`; `vacancy_id` есть и в `ChatsCommonMessagesResponse` | Вердикт не меняется |
| 3 | ФТ-05, ФТ-06 | Поле типа сообщения называется то `type`, то `message_type` | `ChatsCommonMessage.type` и `WebhookPayloadChatMessageCreated.message_type` — разные поля разных схем | Вердикт не меняется, важно для маппинга |
| 4 | ФТ-06 | Пример условий загрузки — `ChatsCommonFilesConditionsResponse` | Пример называется `ChatsCommonFilesConditions` | Вердикт не меняется |
| 5 | ФТ-08 | GAP-R7 обоснован внешней документацией | Обоснован описанием `get-resume`: платный доступ, `can_view_full_info`, `contact_view_status: NONE` | Вердикт не меняется, разрыв стал проверяемым по ссылке |
| 6 | Метаданные | SHA-256 `4349900b…6383d` | `8ea1380b…a7576`, 1 266 778 байт, 2026-08-27 | Потребовало сплошной перепроверки |

## Добавлено сверх L2

- **GAP-R11** (Medium, ФТ-05) — семантика `filter_has_text_message` и типа
  `SIMPLE`; порождает риск **R8**.
- **GAP-R12** (Medium, ФТ-09) — приоритет ключей сопоставления с Адресной
  книгой; в L2 присутствовал как замечание без номера.
- Разбор ФТ-09 и ФТ-10 по подпунктам (`§4.9.1`–`§4.9.3`, `§4.10.1`–`§4.10.3`):
  в L2 эти ФТ оценивались целиком.
- Тип чата `NEGOTIATION` / `SUPPORT` / `BOT` / `COMMON` — в область канала
  попадает только `NEGOTIATION`.
- Жизненный цикл подписки на вебхуки с внешним переходом «подписка удалена
  без действий интеграции» и сторожевой проверкой `get-webhook-subscriptions`.

## Проверка RUN-0059

Имена полей hh.ru в матрице маппинга (§4.3 спайка) не совпадают со
спецификацией: `items[].text` → `items[].payload.text`, `items[].created_at` →
`items[].creation_time`, `items[].participant.role` →
`items[].sender_display_info.role`; не учтены `payload.attachments[]` и
`payload.moved_participant`. Логика маппинга и архитектурная рекомендация
(вариант A) верны и не меняются.
