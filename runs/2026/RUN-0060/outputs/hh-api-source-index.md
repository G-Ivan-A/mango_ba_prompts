---
status: draft
version: 0.1
updated: 2026-08-27
ai-generated: true
type: artifact
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/333"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/329"
related_artifacts:
  - "runs/2026/RUN-0060/outputs/L4-combined-gap-report.md"
  - "experiments/issue_333_hh_api_source_index.py"
---

# Индекс источников hh.ru API (сноски отчёта L4)

- Спецификация: <https://api.hh.ru/openapi/specification/public>
- SHA-256 спецификации: `8ea1380bf87d7351cf2f977f9918bbdd03a26a6b9c9e95eb50f3d4ae080a7576`
- Размер: 1266778 байт
- Операций в выборке: 68

Указатель порождён скриптом
[`experiments/issue_333_hh_api_source_index.py`](../../../../experiments/issue_333_hh_api_source_index.py)
и служит машинной опорой для сносок отчёта
[`L4-combined-gap-report.md`](L4-combined-gap-report.md). Отбор — разделы
спецификации, задействованные в требованиях ФТ-01…ФТ-10.

В колонке «Раздел (tag)» указан первый тег операции: часть операций объявлена
сразу в нескольких разделах, поэтому в выборку попадают и смежные разделы
(«Вакансии», «Информация о соискателе»).

Схема ссылки: `https://api.hh.ru/openapi/redoc#tag/<slug(tag)>/operation/<operationId>`.
Якорь раскрывает нужный метод в документации hh.ru непосредственно — рецензенту
не требуется искать метод вручную.

Команда воспроизведения:

```bash
python3 experiments/issue_333_hh_api_source_index.py --download \
  --tag 'Чаты' --tag 'Webhook API' \
  --tag 'Отклики/приглашения работодателя' --tag 'Переписка (отклики/приглашения) для соискателя' \
  --tag 'Менеджеры работодателя' --tag 'Информация о менеджере' \
  --tag 'Авторизация работодателя' --tag 'Авторизация приложения' \
  --tag 'Просмотр резюме' --tag 'Услуги работодателя' --tag 'Управление вакансиями' \
  --out runs/2026/RUN-0060/outputs/hh-api-source-index.md
```

| Раздел (tag) | Метод | Путь | operationId | Ссылка для проверки |
| --- | --- | --- | --- | --- |
| Webhook API | `POST` | `/webhook/subscriptions` | `post-webhook-subscription` | [Подписаться на уведомления](https://api.hh.ru/openapi/redoc#tag/Webhook-API/operation/post-webhook-subscription) |
| Webhook API | `GET` | `/webhook/subscriptions` | `get-webhook-subscriptions` | [Получить список уведомлений, на которые подписан пользователь](https://api.hh.ru/openapi/redoc#tag/Webhook-API/operation/get-webhook-subscriptions) |
| Webhook API | `PUT` | `/webhook/subscriptions/{subscription_id}` | `change-webhook-subscription` | [Изменить подписку на уведомления](https://api.hh.ru/openapi/redoc#tag/Webhook-API/operation/change-webhook-subscription) |
| Webhook API | `DELETE` | `/webhook/subscriptions/{subscription_id}` | `cancel-webhook-subscription` | [Удалить подписку на уведомление](https://api.hh.ru/openapi/redoc#tag/Webhook-API/operation/cancel-webhook-subscription) |
| Авторизация приложения | `POST` | `/token` | `authorize` | [Получение access-токена](https://api.hh.ru/openapi/redoc#tag/Avtorizaciya-prilozheniya/operation/authorize) |
| Авторизация работодателя | `DELETE` | `/token` | `invalidate-token` | [Инвалидация токена](https://api.hh.ru/openapi/redoc#tag/Avtorizaciya-rabotodatelya/operation/invalidate-token) |
| Вакансии | `GET` | `/vacancies/{vacancy_id}` | `get-vacancy` | [Просмотр вакансии](https://api.hh.ru/openapi/redoc#tag/Vakansii/operation/get-vacancy) |
| Информация о менеджере | `GET` | `/employers/{employer_id}/managers/{manager_id}/vacancies/available_types` | `get-available-vacancy-types` | [Варианты публикации вакансий у текущего менеджера](https://api.hh.ru/openapi/redoc#tag/Informaciya-o-menedzhere/operation/get-available-vacancy-types) |
| Информация о соискателе | `GET` | `/me` | `get-current-user-info` | [Информация о текущем пользователе](https://api.hh.ru/openapi/redoc#tag/Informaciya-o-soiskatele/operation/get-current-user-info) |
| Менеджеры работодателя | `GET` | `/employers/{employer_id}/manager_types` | `get-employer-manager-types` | [Справочник типов и прав менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-employer-manager-types) |
| Менеджеры работодателя | `GET` | `/employers/{employer_id}/managers` | `get-employer-managers` | [Список менеджеров работодателя](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-employer-managers) |
| Менеджеры работодателя | `POST` | `/employers/{employer_id}/managers` | `add-employer-manager` | [Добавление менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/add-employer-manager) |
| Менеджеры работодателя | `PUT` | `/employers/{employer_id}/managers/{manager_id}` | `edit-employer-manager` | [Редактирование менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/edit-employer-manager) |
| Менеджеры работодателя | `GET` | `/employers/{employer_id}/managers/{manager_id}` | `get-employer-manager` | [Получение информации о менеджере](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-employer-manager) |
| Менеджеры работодателя | `DELETE` | `/employers/{employer_id}/managers/{manager_id}` | `delete-employer-manager` | [Удаление менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/delete-employer-manager) |
| Менеджеры работодателя | `GET` | `/employers/{employer_id}/managers/{manager_id}/limits/resume` | `get-employer-manager-limits` | [Дневной лимит просмотра резюме для текущего менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-employer-manager-limits) |
| Менеджеры работодателя | `GET` | `/employers/{employer_id}/managers/{manager_id}/settings` | `get-manager-settings` | [Предпочтения менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-manager-settings) |
| Менеджеры работодателя | `GET` | `/manager_accounts/mine` | `get-manager-accounts` | [Рабочие аккаунты менеджера](https://api.hh.ru/openapi/redoc#tag/Menedzhery-rabotodatelya/operation/get-manager-accounts) |
| Отклики/приглашения работодателя | `GET` | `/employers/{employer_id}/mail_templates` | `get-mail-templates` | [Список доступных шаблонов ответов соискателю](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-mail-templates) |
| Отклики/приглашения работодателя | `PUT` | `/employers/{employer_id}/mail_templates/{template_id}` | `put-mail-templates-item` | [Изменение шаблона ответа соискателю](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/put-mail-templates-item) |
| Отклики/приглашения работодателя | `GET` | `/employers/{employer_id}/managers/{manager_id}/negotiations_statistics` | `get-negotiations-statistics-manager` | [Статистика откликов для менеджера](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiations-statistics-manager) |
| Отклики/приглашения работодателя | `GET` | `/employers/{employer_id}/negotiations_statistics` | `get-negotiations-statistics-employer` | [Статистика откликов для компании](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiations-statistics-employer) |
| Отклики/приглашения работодателя | `GET` | `/message_templates/{template}` | `get-negotiation-message-templates` | [Список шаблонов ответов для отклика/приглашения](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiation-message-templates) |
| Отклики/приглашения работодателя | `POST` | `/negotiations/phone_interview` | `invite-applicant-to-vacancy` | [Пригласить соискателя на вакансию](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/invite-applicant-to-vacancy) |
| Отклики/приглашения работодателя | `POST` | `/negotiations/read` | `post-negotiations-topics-read` | [Отметить отклики прочитанными](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/post-negotiations-topics-read) |
| Отклики/приглашения работодателя | `GET` | `/negotiations/response` | `get-collection-negotiations-list` | [Список откликов/приглашений коллекции](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-collection-negotiations-list) |
| Отклики/приглашения работодателя | `PUT` | `/negotiations/{collection_name}/{nid}` | `change-negotiation-action` | [Действия по отклику/приглашению коллекции](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/change-negotiation-action) |
| Отклики/приглашения работодателя | `PUT` | `/negotiations/{id}` | `put-negotiations-collection-to-next-state` | [Действия по откликам/приглашениям](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/put-negotiations-collection-to-next-state) |
| Отклики/приглашения работодателя | `GET` | `/negotiations/{nid}/test/solution` | `get-negotiation-test-results` | [Получить результаты тестов, прикрепленных к вакансии](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiation-test-results) |
| Отклики/приглашения работодателя | `GET` | `/resumes/{resume_id}/negotiations_history` | `get-resume-negotiations-history` | [История откликов/приглашений по резюме](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-resume-negotiations-history) |
| Отклики/приглашения работодателя | `GET` | `/vacancies/{id}/preferred_negotiations_order` | `get-pref-negotiations-order` | [Просмотр предпочитаемой сортировки откликов](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-pref-negotiations-order) |
| Отклики/приглашения работодателя | `PUT` | `/vacancies/{id}/preferred_negotiations_order` | `put-pref-negotiations-order` | [Изменение предпочитаемой сортировки откликов](https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/put-pref-negotiations-order) |
| Переписка (отклики/приглашения) для соискателя | `GET` | `/negotiations` | `get-negotiations` | [Список откликов/приглашений](https://api.hh.ru/openapi/redoc#tag/Perepiska-(otklikipriglasheniya)-dlya-soiskatelya/operation/get-negotiations) |
| Переписка (отклики/приглашения) для соискателя | `GET` | `/negotiations/{id}` | `get-negotiation-item` | [Просмотр отклика/приглашения](https://api.hh.ru/openapi/redoc#tag/Perepiska-(otklikipriglasheniya)-dlya-soiskatelya/operation/get-negotiation-item) |
| Переписка (отклики/приглашения) для соискателя | `POST` | `/negotiations/{nid}/messages` | `send-negotiation-message` | [Отправка нового сообщения](https://api.hh.ru/openapi/redoc#tag/Perepiska-(otklikipriglasheniya)-dlya-soiskatelya/operation/send-negotiation-message) |
| Переписка (отклики/приглашения) для соискателя | `GET` | `/negotiations/{nid}/messages` | `get-negotiation-messages` | [Просмотр списка сообщений в отклике/приглашении](https://api.hh.ru/openapi/redoc#tag/Perepiska-(otklikipriglasheniya)-dlya-soiskatelya/operation/get-negotiation-messages) |
| Просмотр резюме | `GET` | `/resumes/{resume_id}` | `get-resume` | [Просмотр резюме](https://api.hh.ru/openapi/redoc#tag/Prosmotr-rezyume/operation/get-resume) |
| Управление вакансиями | `GET` | `/employers/{employer_id}/vacancies/active` | `get-active-vacancy-list` | [Просмотр списка опубликованных вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-active-vacancy-list) |
| Управление вакансиями | `GET` | `/employers/{employer_id}/vacancies/archived` | `get-archived-vacancies` | [Список архивных вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-archived-vacancies) |
| Управление вакансиями | `PUT` | `/employers/{employer_id}/vacancies/archived/{vacancy_id}` | `add-vacancy-to-archive` | [Архивация вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/add-vacancy-to-archive) |
| Управление вакансиями | `GET` | `/employers/{employer_id}/vacancies/hidden` | `get-hidden-vacancies` | [Список удаленных вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-hidden-vacancies) |
| Управление вакансиями | `PUT` | `/employers/{employer_id}/vacancies/hidden/{vacancy_id}` | `add-vacancy-to-hidden` | [Удаление вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/add-vacancy-to-hidden) |
| Управление вакансиями | `DELETE` | `/employers/{employer_id}/vacancies/hidden/{vacancy_id}` | `restore-vacancy-from-hidden` | [Восстановление вакансии из удаленных](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/restore-vacancy-from-hidden) |
| Управление вакансиями | `POST` | `/vacancies` | `publish-vacancy` | [Публикация вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/publish-vacancy) |
| Управление вакансиями | `PUT` | `/vacancies/{vacancy_id}` | `edit-vacancy` | [Редактирование вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/edit-vacancy) |
| Управление вакансиями | `GET` | `/vacancies/{vacancy_id}/prolongate` | `get-prolongation-vacancy-info` | [Информация о возможности продления вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-prolongation-vacancy-info) |
| Управление вакансиями | `POST` | `/vacancies/{vacancy_id}/prolongate` | `vacancy-prolongation` | [Продление вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/vacancy-prolongation) |
| Управление вакансиями | `GET` | `/vacancies/{vacancy_id}/stats` | `get-vacancy-stats` | [Статистика по вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-vacancy-stats) |
| Управление вакансиями | `GET` | `/vacancies/{vacancy_id}/upgrades` | `get-vacancy-upgrade-list` | [Список улучшений для вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-vacancy-upgrade-list) |
| Управление вакансиями | `GET` | `/vacancies/{vacancy_id}/visitors` | `get-vacancy-visitors` | [Посмотревшие вакансию](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-vacancy-visitors) |
| Управление вакансиями | `GET` | `/vacancy_conditions` | `get-vacancy-conditions` | [Условия заполнения полей при добавлении и редактировании вакансий](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-vacancy-conditions) |
| Услуги работодателя | `GET` | `/employers/{employer_id}/managers/{manager_id}/method_access` | `get-payable-api-method-access` | [Проверка доступа к платным методам](https://api.hh.ru/openapi/redoc#tag/Uslugi-rabotodatelya/operation/get-payable-api-method-access) |
| Услуги работодателя | `GET` | `/employers/{employer_id}/services/available_publications` | `get-vacancy-available-services-list` | [Получение списка доступных вариантов публикации вакансии](https://api.hh.ru/openapi/redoc#tag/Uslugi-rabotodatelya/operation/get-vacancy-available-services-list) |
| Услуги работодателя | `GET` | `/employers/{employer_id}/services/payable_api_actions/active` | `get-payable-api-actions` | [Информация по активным услугам API для платных методов](https://api.hh.ru/openapi/redoc#tag/Uslugi-rabotodatelya/operation/get-payable-api-actions) |
| Чаты | `GET` | `/common/chats` | `get-common-chat-list` | [Получить список чатов](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-common-chat-list) |
| Чаты | `GET` | `/common/chats/counters/unread` | `unread-chats-count` | [Получить количество непрочитанных чатов](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/unread-chats-count) |
| Чаты | `GET` | `/common/chats/files/conditions` | `get-common-chat-files-conditions` | [Получить свойства файлов для чатов](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-common-chat-files-conditions) |
| Чаты | `POST` | `/common/chats/files/upload_links` | `get-common-chat-files-upload-links` | [Получить ссылку для отправки файла в чат](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-common-chat-files-upload-links) |
| Чаты | `POST` | `/common/chats/without_vacancy` | `get-or-create-chat-without-vacancy-common` | [Создание чата без вакансии](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-or-create-chat-without-vacancy-common) |
| Чаты | `PUT` | `/common/chats/{chat_id}/leave` | `leave-chat` | [Покинуть чат](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/leave-chat) |
| Чаты | `PUT` | `/common/chats/{chat_id}/message/{message_id}/read` | `set-last-viewed-message` | [Установка последнего прочитанного сообщения](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/set-last-viewed-message) |
| Чаты | `GET` | `/common/chats/{chat_id}/messages` | `get-chat-messages` | [Получение списка сообщений чата](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-chat-messages) |
| Чаты | `POST` | `/common/chats/{chat_id}/messages` | `chat-message-post` | [Отправить сообщение в чат](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/chat-message-post) |
| Чаты | `PUT` | `/common/chats/{chat_id}/messages/{message_id}` | `chat-message-put` | [Изменение сообщения в чате](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/chat-message-put) |
| Чаты | `DELETE` | `/common/chats/{chat_id}/messages/{message_id}` | `chat-message-delete` | [Удаление сообщения в чате](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/chat-message-delete) |
| Чаты | `GET` | `/common/chats/{chat_id}/participants` | `get-participant-list` | [Получение списка участников чата](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/get-participant-list) |
| Чаты | `PUT` | `/common/chats/{chat_id}/participants` | `put-participant-list` | [Добавление участника в чат](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/put-participant-list) |
| Чаты | `PUT` | `/common/chats/{chat_id}/write_possibility` | `set-write-possibility-common` | [Запретить/разрешить переписку в чате соискателю](https://api.hh.ru/openapi/redoc#tag/Chaty/operation/set-write-possibility-common) |
