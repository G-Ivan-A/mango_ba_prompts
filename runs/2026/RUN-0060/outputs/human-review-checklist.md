---
status: draft
version: 0.1
updated: 2026-08-28
ai-generated: true
type: artifact
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/335"
related_artifacts:
  - "runs/2026/RUN-0060/outputs/L4-combined-gap-report.md"
  - "docs/analysis/2026-08-28-human-review-accessibility.md"
  - "experiments/issue_335_footnote_audit.py"
  - "experiments/issue_335_human_review_checklist.py"
---

# Чек-лист Human Review: проверка сносок отчёта L4 (RUN-0060)

Проверочный вопрос для каждой сноски: **увидит ли человек, перешедший по ссылке без дополнительных знаний об API, именно тот объект, который описан в сноске?**

## 1. Условия проверки

- Спецификация: <https://api.hh.ru/openapi/specification/public>
- SHA-256: `8ea1380bf87d7351cf2f977f9918bbdd03a26a6b9c9e95eb50f3d4ae080a7576`
- Совпадает с SHA-256, закреплённым в отчёте L4: **да**
- Проиндексировано схем: 728, операций: 131
- Проверено сносок: **53**
- Инструмент: `experiments/issue_335_footnote_audit.py` (только stdlib)

Воспроизведение:

```bash
python3 experiments/issue_335_footnote_audit.py --download --json /tmp/audit.json
python3 experiments/issue_335_human_review_checklist.py --audit /tmp/audit.json \
    --out runs/2026/RUN-0060/outputs/human-review-checklist.md
```

## 2. Итог по классам проблем

| Класс | Определение | Сносок |
| --- | --- | --- |
| A | Тип A — ссылка ведёт на неверный объект | 1 |
| D | Тип D — объект не найден в документации (GAP SSOT) | 0 |
| C | Тип C — объект найден, но описан недостаточно | 14 |
| B | Тип B — ссылка верна, но объект требует дополнительной навигации | 16 |
| OK | Без замечаний — ссылка ведёт прямо на описанный объект | 22 |
| **Итого** | | **53** |

Ключевой механический факт, объясняющий большинство замечаний класса B: Redoc выводит в заголовке блока значение `title` схемы, а не её имя в `components.schemas`. Спецификация hh.ru объявляет `x-tagGroups`, поэтому раздел Schemas в Redoc не отображается и якорей на схемы не существует — правило «якорь на дочерний элемент» технически недостижимо, применяется правило 3 (явный путь навигации) плюс цитата из спецификации, закреплённой по SHA-256.

## 3. Полный чек-лист (53 сноски)

| № | Раздел | Сноска | Что описывает сноска | Что видно по ссылке | Класс | Рекомендация |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2.3 | `^1` | `POST /token` (`authorize`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 2 | 2.3 | `^2` | `DELETE /token` (`invalidate-token`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 3 | 2.3 | `^3` | `GET /manager_accounts/mine` (`get-manager-accounts`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 4 | 3.3 | `^1` | `DELETE /webhook/subscriptions/{subscription_id}` (`cancel-webhook-subscription`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 5 | 3.3 | `^2` | `GET /webhook/subscriptions` (`get-webhook-subscriptions`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 6 | 3.3 | `^3` | `POST /webhook/subscriptions` (`post-webhook-subscription`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 7 | 4.3 | `^1` | `POST /common/chats/{chat_id}/messages` (`chat-message-post`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 8 | 5.3 | `^1` | `GET /common/chats` (`get-common-chat-list`): параметры `page`, `per_page`, `filter_unread`, `filter_has_text_message`, `vacancy_status`, `filter_with_vacancy_ids`; схемы ответа `ChatsCommonChatItems`, `ChatsCommonChatBasic` | Redoc печатает `title` схемы, а не её имя: `ChatsCommonChatBasic` отображается как «Базовая информация о чате»; `ChatsCommonChatItems` отображается как «Список чатов» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-common-chat-list` → блок с заголовком «Базовая информация о чате», «Список чатов» |
| 9 | 5.3 | `^2` | Callback `onData`, схемы `WebhookSendObjectBaseUser`, `WebhookPayloadChatMessageCreated` (раздел Callbacks метода `post-webhook-subscription`) | Redoc печатает `title` схемы, а не её имя: `WebhookPayloadChatMessageCreated` отображается как «CHAT_MESSAGE_CREATED»; `WebhookSendObjectBaseUser` отображается как «Сообщение о событии на уровне менеджера» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «CHAT_MESSAGE_CREATED», «Сообщение о событии на уровне менеджера» |
| 10 | 5.3 | `^3` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 11 | 6.3 | `^1` | Callback `onData` → `WebhookPayloadChatMessageCreated` (поля `role`, `message_type`) | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookPayloadChatMessageCreated` отображается как «CHAT_MESSAGE_CREATED» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «CHAT_MESSAGE_CREATED» |
| 12 | 6.3 | `^2` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`), схемы `ChatsCommonMessage`, `ChatsCommonSenderDisplayInfo`, `chat_states.write_message_state` | Redoc печатает `title` схемы, а не её имя: `ChatsCommonMessage` отображается как «Информация о сообщении»; `ChatsCommonSenderDisplayInfo` отображается как «Отображаемая информация об отправителе сообщения»; сноска не называет схему-владельца для `chat_states.write_message_state`: на странице операции поле приходится искать вручную | C | правило 3: указать путь навигации — раздел «Chaty» → операция `get-chat-messages` → блок с заголовком «Информация о сообщении», «Отображаемая информация об отправителе сообщения»; поле `chat_states.write_message_state` объявлено только в `components.schemas.ChatsCommonChatState` (строка 5895 спецификации) — процитировать эту схему |
| 13 | 6.3 | `^3` | `POST /webhook/subscriptions` (`post-webhook-subscription`), перечень `actions`: `NEW_NEGOTIATION_VACANCY`, `NEW_RESPONSE_OR_INVITATION_VACANCY`, `CHAT_CREATED`, `CHAT_MESSAGE_CREATED` | сноска не называет схему-владельца для `actions`: на странице операции поле приходится искать вручную | C | поле `actions` объявлено в 6 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 14 | 6.3 | `^4` | `GET /common/chats` (`get-common-chat-list`), схема `ChatsCommonChatBasic`: поля `type` (`NEGOTIATION`…), `block_reason` | Redoc печатает `title` схемы, а не её имя: `ChatsCommonChatBasic` отображается как «Базовая информация о чате» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-common-chat-list` → блок с заголовком «Базовая информация о чате» |
| 15 | 6.3 | `^5` | `GET /common/chats` (`get-common-chat-list`), параметр `filter_has_text_message` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 16 | 6.3 | `^6` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`), параметры `start_message_id`, `limit`, `order`, поле `has_more` | сноска не называет схему-владельца для `has_more`: на странице операции поле приходится искать вручную | C | поле `has_more` объявлено только в `components.schemas.ChatsCommonMessageItems` (строка 5934 спецификации) — процитировать эту схему |
| 17 | 7.3 | `^1` | `POST /common/chats/{chat_id}/messages` (`chat-message-post`), схемы `ChatsCommonMessagePostText` (`text`, `idempotency_key`, `is_automated`), `ChatsCommonMessagePostFileUploadIds` (`file_upload_ids`, `maxItems: 1`) | Redoc печатает `title` схемы, а не её имя: `ChatsCommonMessagePostFileUploadIds` отображается как «Идентификаторы загруженных файлов»; `ChatsCommonMessagePostText` отображается как «Текст сообщения» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `chat-message-post` → блок с заголовком «Идентификаторы загруженных файлов», «Текст сообщения» |
| 18 | 7.3 | `^2` | `POST /common/chats/files/upload_links` (`get-common-chat-files-upload-links`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 19 | 7.3 | `^3` | `GET /common/chats/files/conditions` (`get-common-chat-files-conditions`), пример `ChatsCommonFilesConditions` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 20 | 7.3 | `^4` | `PUT /negotiations/{collection_name}/{nid}` (`change-negotiation-action`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 21 | 7.3 | `^5` | `PUT /negotiations/{id}` (`put-negotiations-collection-to-next-state`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 22 | 7.3 | `^6` | Схема `WebhookActionChatMessageCreated` (описание условия доставки) | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookActionChatMessageCreated` отображается как «Подписка на CHAT_MESSAGE_CREATED» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «Подписка на CHAT_MESSAGE_CREATED» |
| 23 | 7.3 | `^7` | `POST /webhook/subscriptions` (`post-webhook-subscription`): описание метода (5 секунд, повторы, блокировка, «не являются средствами гарантированной доставки») и раздел `callbacks` (`security: null`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 24 | 7.3 | `^8` | `GET /common/chats` (`get-common-chat-list`), параметры `page` (0…50), `per_page` (1…20) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 25 | 7.3 | `^9` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`), схемы `ChatsCommonChatState`, `ChatsCommonMessage` (поле `type`) | Redoc печатает `title` схемы, а не её имя: `ChatsCommonChatState` отображается как «Состояние чата»; `ChatsCommonMessage` отображается как «Информация о сообщении» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-chat-messages` → блок с заголовком «Информация о сообщении», «Состояние чата» |
| 26 | 7.3 | `^10` | Схема `WebhookPayloadChatMessageCreated` (поле `message_type`) | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookPayloadChatMessageCreated` отображается как «CHAT_MESSAGE_CREATED» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «CHAT_MESSAGE_CREATED» |
| 27 | 7.3 | `^11` | `GET /negotiations/response` (`get-collection-negotiations-list`), поля `actions[].url`, `actions[].arguments` | сноска не называет схему-владельца для `actions[].arguments`, `actions[].url`: на странице операции поле приходится искать вручную | C | поле `actions[].arguments` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно; поле `actions[].url` объявлено в 41 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 28 | 8.3 | `^1` | `GET /common/chats` (`get-common-chat-list`), поле `type` = `NEGOTIATION` | сноска не называет схему-владельца для `type`: на странице операции поле приходится искать вручную | C | поле `type` объявлено в 73 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 29 | 8.3 | `^2` | `GET /common/chats/{chat_id}/participants` (`get-participant-list`), схема `ChatsCommonParticipant` (`role`, `resume_id`, `last_viewed_message_id`) | Redoc печатает `title` схемы, а не её имя: `ChatsCommonParticipant` отображается как «Участник чата» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-participant-list` → блок с заголовком «Участник чата» |
| 30 | 8.3 | `^3` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`), схема `ChatsCommonSenderDisplayInfo` (`name`, `icon`, `role`) | Redoc печатает `title` схемы, а не её имя: `ChatsCommonSenderDisplayInfo` отображается как «Отображаемая информация об отправителе сообщения» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-chat-messages` → блок с заголовком «Отображаемая информация об отправителе сообщения» |
| 31 | 8.3 | `^4` | Схемы `WebhookActionChatCreated` («является участником»), `WebhookActionChatMessageCreated` («является активным участником») | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookActionChatCreated` отображается как «Подписка на CHAT_CREATED»; `WebhookActionChatMessageCreated` отображается как «Подписка на CHAT_MESSAGE_CREATED» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «Подписка на CHAT_CREATED», «Подписка на CHAT_MESSAGE_CREATED» |
| 32 | 8.3 | `^5` | `POST /common/chats/{chat_id}/messages` (`chat-message-post`), поле `is_automated` | сноска не называет схему-владельца для `is_automated`: на странице операции поле приходится искать вручную | C | поле `is_automated` объявлено только в `components.schemas.ChatsCommonMessagePostText` (строка 5851 спецификации) — процитировать эту схему |
| 33 | 9.3 | `^1` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`): `start_message_id`, `limit` (1…50), `order` (`prev`/`next`), `has_more`, `creation_time`, `sender_display_info` | сноска не называет схему-владельца для `creation_time`, `has_more`, `sender_display_info`: на странице операции поле приходится искать вручную | C | поле `creation_time` объявлено в 6 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно; поле `has_more` объявлено только в `components.schemas.ChatsCommonMessageItems` (строка 5934 спецификации) — процитировать эту схему; поле `sender_display_info` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 34 | 9.3 | `^2` | `GET /vacancies/{vacancy_id}` (`get-vacancy`), поля `name`, `alternate_url` | сноска не называет схему-владельца для `alternate_url`: на странице операции поле приходится искать вручную | C | поле `alternate_url` объявлено в 12 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 35 | 9.3 | `^3` | Схема `WebhookPayloadNewResponseOrInvitationVacancy` (`chat_id`, `vacancy_id`, `resume_id`, `topic_id`, `employer_id`, `response_date`) | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookPayloadNewResponseOrInvitationVacancy` отображается как «NEW_RESPONSE_OR_INVITATION_VACANCY» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «NEW_RESPONSE_OR_INVITATION_VACANCY» |
| 36 | 9.3 | `^4` | `GET /common/chats` (`get-common-chat-list`), связка `id` (string) ↔ `vacancy_id` | сноска не называет схему-владельца для `id`: на странице операции поле приходится искать вручную | C | поле `id` объявлено в 152 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 37 | 9.3 | `^5` | `GET /resumes/{resume_id}` (`get-resume`): описание метода (платный доступ, `can_view_full_info`, `contact_view_status`), поле `alternate_url` | сноска не называет схему-владельца для `alternate_url`, `can_view_full_info`, `contact_view_status`: на странице операции поле приходится искать вручную | C | поле `alternate_url` объявлено в 12 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно; поле `can_view_full_info` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно; поле `contact_view_status` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 38 | 9.3 | `^6` | `GET /common/chats/{chat_id}/participants` (`get-participant-list`), поле `resume_id` у роли `APPLICANT` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 39 | 9.3 | `^7` | Раздел «Просмотр резюме с контактами» (ссылка из описания `get-resume`) | якорь указывает на подраздел тега, а не на операцию | A | заменить якорь на `#tag/<tag>/operation/<operationId>` |
| 40 | 9.3 | `^8` | `GET /negotiations/response` (`get-collection-negotiations-list`), схема `NegotiationsObjectsTopicItemCommon` (`chat_id` как `number`) | Redoc печатает `title` схемы, а не её имя: `NegotiationsObjectsTopicItemCommon` отображается как «Общая информация об отклике/приглашении»; сноска не называет схему-владельца для `number`: на странице операции поле приходится искать вручную | C | правило 3: указать путь навигации — раздел «Otklikipriglasheniya-rabotodatelya» → операция `get-collection-negotiations-list` → блок с заголовком «Общая информация об отклике/приглашении»; поле `number` объявлено в 5 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 41 | 10.3 | `^1` | `GET /common/chats/{chat_id}/participants` (`get-participant-list`), поле `resume_id`, роль `APPLICANT` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 42 | 10.3 | `^2` | `GET /resumes/{resume_id}` (`get-resume`): `can_view_full_info`, `contact_view_status` | сноска не называет схему-владельца для `can_view_full_info`, `contact_view_status`: на странице операции поле приходится искать вручную | C | поле `can_view_full_info` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно; поле `contact_view_status` объявлено в 2 схемах спецификации и ни в одной из названных в сноске — указать схему-владельца явно |
| 43 | 10.3 | `^3` | Схема `WebhookPayloadNewResponseOrInvitationVacancy`, поле `resume_id` | на странице операции нет заголовка с именем схемы: схема раскрывается только внутри блока Callbacks/Responses; Redoc печатает `title` схемы, а не её имя: `WebhookPayloadNewResponseOrInvitationVacancy` отображается как «NEW_RESPONSE_OR_INVITATION_VACANCY» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «NEW_RESPONSE_OR_INVITATION_VACANCY» |
| 44 | 11.3 | `^1` | `GET /common/chats` (`get-common-chat-list`), схемы `ChatsCommonChatBasic` / `ChatsCommonChatItems` | Redoc печатает `title` схемы, а не её имя: `ChatsCommonChatBasic` отображается как «Базовая информация о чате»; `ChatsCommonChatItems` отображается как «Список чатов» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-common-chat-list` → блок с заголовком «Базовая информация о чате», «Список чатов» |
| 45 | 11.3 | `^2` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`), схема `ChatsCommonMessage` (`payload.text`, `payload.attachments`, `viewed_by_opponent`, `type`) | Redoc печатает `title` схемы, а не её имя: `ChatsCommonMessage` отображается как «Информация о сообщении» | B | правило 3: указать путь навигации — раздел «Chaty» → операция `get-chat-messages` → блок с заголовком «Информация о сообщении» |
| 46 | 12.5 | `^1` | `POST /webhook/subscriptions` (`post-webhook-subscription`), схемы `WebhookActionChatCreated`, `WebhookActionChatMessageCreated`, `WebhookActionVacancyOnlyMineSettings.vacancies_only_mine` | Redoc печатает `title` схемы, а не её имя: `WebhookActionChatCreated` отображается как «Подписка на CHAT_CREATED»; `WebhookActionChatMessageCreated` отображается как «Подписка на CHAT_MESSAGE_CREATED»; `WebhookActionVacancyOnlyMineSettings` отображается как «Настройка на подписку только на мои вакансии» | B | правило 3: указать путь навигации — раздел «Webhook-API» → операция `post-webhook-subscription` → блок с заголовком «Настройка на подписку только на мои вакансии», «Подписка на CHAT_CREATED», «Подписка на CHAT_MESSAGE_CREATED» |
| 47 | 12.5 | `^2` | `GET /common/chats/{chat_id}/participants` (`get-participant-list`), ответ `404` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 48 | 12.5 | `^3` | `PUT /common/chats/{chat_id}/participants` (`put-participant-list`), тело `{"id": …}`, ответы `204` / `404` | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 49 | 12.5 | `^4` | `GET /common/chats/{chat_id}/messages` (`get-chat-messages`): `404`, типы `PARTICIPANT_JOINED` / `PARTICIPANT_LEFT`, `write_message_state` | сноска не называет схему-владельца для `write_message_state`: на странице операции поле приходится искать вручную | C | поле `write_message_state` объявлено только в `components.schemas.ChatsCommonChatState` (строка 5895 спецификации) — процитировать эту схему |
| 50 | 12.5 | `^5` | `POST /common/chats/{chat_id}/messages` (`chat-message-post`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 51 | 12.5 | `^6` | `GET /manager_accounts/mine` (`get-manager-accounts`), заголовок `X-Manager-Account-Id` | сноска не называет схему-владельца для `X-Manager-Account-Id`: на странице операции поле приходится искать вручную | C | поле `X-Manager-Account-Id` отсутствует в структурах спецификации — пометить как GAP SSOT |
| 52 | 12.5 | `^7` | `POST /webhook/subscriptions` (`post-webhook-subscription`), описание: удаление подписок при отзыве доступа, очередь на блокировку | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |
| 53 | 12.5 | `^8` | `GET /negotiations/response` (`get-collection-negotiations-list`) | описанный объект виден на странице ссылки без дополнительных шагов | OK | исправление не требуется |

## 4. Выводы для стандарта

1. Ссылка на операцию Redoc проверяема машинно: `operationId` обязан присутствовать в спецификации с зафиксированным SHA-256.
2. Ссылка на схему в Redoc непроверяема и человеку не помогает: у схем нет якорей. Сноска, описывающая схему, обязана содержать путь навигации и цитату `components.schemas.<Имя>` со строкой спецификации.
3. Имя схемы нельзя использовать как ориентир для человека: в интерфейсе видно `title`. Сноска обязана приводить отображаемый заголовок.
4. Поле, отсутствующее в структурах спецификации (например `X-Manager-Account-Id`, упомянутый только в текстовых описаниях), фиксируется как GAP SSOT, а не как проверенный факт.

