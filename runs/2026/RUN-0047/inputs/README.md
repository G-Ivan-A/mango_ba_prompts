---
status: draft
version: 0.1
updated: 2026-08-22
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/309"
---

# Вход прогона RUN-0047 — провенанс

Тема: **Анализ расшифровки встречи**. Короткий прогон анализа расшифровки встречи по переданному документу.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`920-chat-export-1787302244983.json`](https://github.com/user-attachments/files/31336071/920-chat-export-1787302244983.json) |
| Размер, байт | 210115 |
| SHA-256 | `b43cb033b1421e7b64d398175f7787fa8133b0ee156cc73c672e5aae1ff9aea8` |
| Заголовок чата в экспорте | `920` |
| Окно диалога, UTC | 2026-01-23 12:36:57 — 2026-01-23 12:48:54 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 920-chat-export-1787302244983.json \
  https://github.com/user-attachments/files/31336071/920-chat-export-1787302244983.json
sha256sum 920-chat-export-1787302244983.json
# ожидается: b43cb033b1421e7b64d398175f7787fa8133b0ee156cc73c672e5aae1ff9aea8

python3 experiments/issue_309_run_stats.py 920-chat-export-1787302244983.json \
  --json /tmp/stats/920-chat-export-1787302244983.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
