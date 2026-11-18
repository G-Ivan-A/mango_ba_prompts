---
status: draft
updated: 2026-11-18
ai-generated: true
type: evidence
---

# Входы RUN-0095

| Вход | Что это | Где |
| --- | --- | --- |
| Issue #490 «Корректировка промптов» | Проблемы БА 1.1–1.3, 2–2.3, условия выполнения | https://github.com/G-Ivan-A/mango_ba_prompts/issues/490 |
| Выгрузка чата 1135-2 | JSON OpenWebUI-подобного формата, вложение issue, sha256 `658b1ba3daefe586380a2694919929b2b55ec1248fb56363477863acf43f5eb7` | https://github.com/user-attachments/files/35014279/chat-export-1794988207605.json |
| Метрики чата | Таблица ходов и итоги по токенам и времени | [`chat-1135-2-metrics.md`](chat-1135-2-metrics.md) |
| Постановка | Полная постановка исполнителя по шаблону задачи | [`task-statement-490.md`](task-statement-490.md) |

## Почему расшифровка чата не лежит в репозитории

Чат содержит пересказ ТЗ Заказчика (интеграция Mango Office ↔ HelpDeskEddy)
и рабочие комментарии БА. Для разбора промптов нужен не текст ТЗ, а реплики
БА о работе модели. Поэтому, как в
[BL-157в](../../../../docs/analysis/2026-11-04-bl-157v-chat-analysis.md) и
`experiments/issue_375_dump.py`, расшифровка строится локально, а в
репозиторий идут метрики, счётчики и короткие цитаты в анализе.

## Как воспроизвести

```bash
mkdir -p /tmp/chat-1135-2 && cd /tmp/chat-1135-2   # отдельный пустой каталог
curl -L -o chat.json "https://github.com/user-attachments/files/35014279/chat-export-1794988207605.json"
sha256sum chat.json   # 658b1ba3…f5eb7
cd <корень репозитория>
python3 -I scripts/chat_export_to_markdown.py /tmp/chat-1135-2/chat.json \
  --transcript /tmp/chat-1135-2/transcript.md --metrics /tmp/chat-1135-2/metrics.md
python3 -I experiments/issue_490/chat_signals.py /tmp/chat-1135-2/transcript.md
```

`metrics.md` совпадает с [`chat-1135-2-metrics.md`](chat-1135-2-metrics.md)
побайтно, вывод `chat_signals.py` — с [`../logs/chat-signals.json`](../logs/chat-signals.json).
