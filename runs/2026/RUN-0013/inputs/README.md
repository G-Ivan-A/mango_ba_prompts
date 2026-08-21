---
status: draft
version: 0.1
updated: 2026-07-15
ai-generated: true
type: input
scope: runs/2026/RUN-0013
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/272"
---

# Вход прогона RUN-0013

| Файл | Что это |
| --- | --- |
| [`chat-export-1064.json`](chat-export-1064.json) | Сырой экспорт рабочего чата «1064» (437 581 байт), приложенный к issue #272. Хранится без изменений. |
| [`chat-transcript.md`](chat-transcript.md) | Читаемая стенограмма, **порождённая** из экспорта скриптом `scripts/chat_export_to_transcript.py`. |

Источник экспорта: вложение issue #272 —
<https://github.com/user-attachments/files/31298190/1064-chat-export-1787301432788.json>.

## Как воспроизвести стенограмму и метрики

```bash
python3 scripts/chat_export_to_transcript.py \
    runs/2026/RUN-0013/inputs/chat-export-1064.json \
    --transcript runs/2026/RUN-0013/inputs/chat-transcript.md \
    --metrics runs/2026/RUN-0013/logs/metrics.md
```

Скрипт детерминирован: повторный запуск даёт побайтово те же файлы. Это
проверяется валидатором `scripts/validate_issue_272_run_0013.py`, поэтому
стенограмму и метрики нельзя править вручную — правится генератор.

## Особенности формата экспорта

Разобраны опытным путём на этом файле:

- верхний уровень — список чатов, нужный чат первый;
- ветка диалога восстанавливается по цепочке `parentId` от `currentId`,
  который лежит на **верхнем** уровне объекта, а не в `chat`
  (`chat.currentId` здесь `None`);
- текст ответа модели лежит **не** в `content` (он пуст), а в элементах
  `content_list` с `phase == "answer"`; там же поля `usage` с расходом токенов.

## Что не попало в репозиторий

К отдельным репликам БА прикреплял внешние документы (руководство ЛК, PDF по
интеграции с amoCRM, скриншот окна «О программе» 1С). Сами файлы в экспорте не
содержатся — видно только их влияние на объём контекста (скачки входных токенов
до 385 343 за вызов, см. [`../logs/metrics.md`](../logs/metrics.md)). Поэтому
цитаты модели из этих документов в рамках прогона **непроверяемы** и помечены в
[`../outputs/episodes.md`](../outputs/episodes.md) как требующие проверки.
