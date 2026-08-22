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

# Вход прогона RUN-0039 — провенанс

Тема: **Участники конференции в Mango Talker — ФТ**. Поздняя сессия по задаче 854: доработка ФТ по участникам конференции.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`854-chat-export-1787302334691.json`](https://github.com/user-attachments/files/31336087/854-chat-export-1787302334691.json) |
| Размер, байт | 455553 |
| SHA-256 | `678bb9063d28e5ad03508b4d68e67b236f18ae394a8d26c3dae1d8440f927506` |
| Заголовок чата в экспорте | `854` |
| Окно диалога, UTC | 2025-11-15 15:55:19 — 2025-11-21 10:28:51 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 854-chat-export-1787302334691.json \
  https://github.com/user-attachments/files/31336087/854-chat-export-1787302334691.json
sha256sum 854-chat-export-1787302334691.json
# ожидается: 678bb9063d28e5ad03508b4d68e67b236f18ae394a8d26c3dae1d8440f927506

python3 experiments/issue_309_run_stats.py 854-chat-export-1787302334691.json \
  --json /tmp/stats/854-chat-export-1787302334691.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
