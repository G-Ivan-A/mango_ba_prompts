---
status: draft
version: 0.1
updated: 2026-06-22
ai-generated: true
type: input
scope: mango-only
related_artifacts:
  - "kb/mango-taxonomy/registry.json"
  - "kb/industry-taxonomy/registry.json"
  - "kb/mango-product-docs/processed/mtalker/android-user-guide/index.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/180"
---

# Вход 3 — Выдержки из базы знаний (БЗ)

Опорные узлы таксономий и разделы продуктовой документации, использованные при
формировании нового ФТ. Цитирование выполнено по стандартам
[`standards/kb-standard.md`](../../../../standards/kb-standard.md),
[`standards/mango-taxonomy-standard.md`](../../../../standards/mango-taxonomy-standard.md),
[`standards/industry-taxonomy-standard.md`](../../../../standards/industry-taxonomy-standard.md).

## 1. Industry Taxonomy (`kb/industry-taxonomy/registry.json`)

Модель: `Domain → Capability → Feature → Function`.

| Узел | Уровень | Назначение |
| --- | --- | --- |
| `voice-ucaas` | domain | Голос и унифицированные коммуникации (UCaaS). |
| `voice-ucaas.unified-communications` | capability | Первичное соответствие продукта Mango Talker. |
| `voice-ucaas.video-conferencing` | capability | Видеоконференции: «Video meetings, recording, and screen sharing». Опорная capability для нового решения (групповой звонок на основе ВКС). |
| `voice-ucaas.video-conferencing.video-meetings` | feature | Видеовстречи (групповой звонок). |

## 2. Mango Taxonomy (`kb/mango-taxonomy/registry.json`)

Кластер `mango-talker`.

| Узел | Уровень | name_ru | Релевантность |
| --- | --- | --- | --- |
| `mango-talker` | product | Mango Talker | Продуктовый кластер (софтфон, чаты, видео, контакты). primary → `voice-ucaas.unified-communications`. |
| `talker-video-meeting-service` | service | Видео и конференции Talker | Сервис видеозвонков, аудиоконференций и конференц-комнат. facets: `channel_kind=video`, `synchronicity=sync`. Опорный сервис решения. |
| `talker-video-meeting-module` | module | Видео и конференции | Модуль инициации/проведения конференций. |
| `join-talker-conference-room` | function | Присоединиться к конференции Talker | Базовая функция подключения к конференции (в т.ч. переподключение по ссылке). |
| `talker-contact-history-service` | service | Контакты и история Talker | Карточки контактов, история вызовов, быстрые действия из журнала. Опора для «ссылки переподключения в истории». |
| `talker-favorites-groups-module` | module | Избранное и группы контактов | Опора для «личных групп пользователей в адресной книге». |

## 3. Продуктовая документация (`kb/mango-product-docs/processed/mtalker/`)

Документ: **Mango Talker для Android — Руководство пользователя**, версия от
23.08.2024 (код цитирования `MTALKER-MOB`). Формат цитаты проекта (issue #109):
`[<Документ>, §<Раздел>, с.<Страница>]`.

| § | Раздел | Стр. | Используется для |
| --- | --- | --- | --- |
| §14 | Как начать групповой видеозвонок | 10–11 | Инициация группового звонка (видео), приглашение сотрудников. |
| §37 | Конференции | — | Раздел «Встречи/Конференции» как точка входа. |
| §41 | Как создать новую видео конференцию и поделиться ссылкой | 20 | As-Is сценарий «Создать ссылку» (от которого отказываемся как от основного). |
| §42 | Как присоединиться к конференции по ссылке | 20 | Переподключение к конференции по ссылке. |
| §43 | Поиск комнаты конференции | — | Поиск участника/комнаты. |
| §62 | Описание прав участников | 27–28 | Роли «участник/администратор» (контекст управления). |
| §63 | Отображение списка участников | 28 | Просмотр списка участников. |
| §64 | Добавить участника | 28 | Добавление участника. |
| §71 | Удалить участника | 29–30 | Удаление участника инициатором. |

> Примечание. As-Is документация описывает инициацию группового видеозвонка через
> создание общего чата (§14). В рамках решения issue #180 чаты МТ отключены
> политикой Компании (см. вход 1, §3), поэтому ФТ задаёт **новую** точку входа —
> элемент «Начать групповой звонок (с возможностью видео подключения)» в разделе
> «Встречи» — без зависимости от функционала чатов.
