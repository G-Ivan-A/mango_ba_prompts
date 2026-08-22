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

# Вход прогона RUN-0052 — провенанс

Тема: **AI-робот на линии**. Консультационный прогон по архитектуре AI-робота (RAG/MCP) и применимости к задаче линии поддержки.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`964-chat-export-1787302194872.json`](https://github.com/user-attachments/files/31336082/964-chat-export-1787302194872.json) |
| Размер, байт | 1247917 |
| SHA-256 | `19da73498a54cf872d36e186bbedf08366434c8d443316e34b9ad3c55505f904` |
| Заголовок чата в экспорте | `964 Задача AI робот на линию` |
| Окно диалога, UTC | 2026-02-18 08:10:14 — 2026-02-19 10:46:15 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 964-chat-export-1787302194872.json \
  https://github.com/user-attachments/files/31336082/964-chat-export-1787302194872.json
sha256sum 964-chat-export-1787302194872.json
# ожидается: 19da73498a54cf872d36e186bbedf08366434c8d443316e34b9ad3c55505f904

python3 experiments/issue_309_run_stats.py 964-chat-export-1787302194872.json \
  --json /tmp/stats/964-chat-export-1787302194872.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
