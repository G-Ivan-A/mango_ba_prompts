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

# Вход прогона RUN-0038 — провенанс

Тема: **Участники конференции в Mango Talker — раздел ФТ**. Ранняя сессия по задаче 854: раздел ФТ по участникам конференции.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`854-chat-export-1787302403660.json`](https://github.com/user-attachments/files/31336081/854-chat-export-1787302403660.json) |
| Размер, байт | 306644 |
| SHA-256 | `3b1b1b742cf86e31f3024cddf85b2d9441e2ce5e7d494e78de3b43b02bed694a` |
| Заголовок чата в экспорте | `854` |
| Окно диалога, UTC | 2025-10-20 07:15:36 — 2025-10-20 11:57:09 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 854-chat-export-1787302403660.json \
  https://github.com/user-attachments/files/31336081/854-chat-export-1787302403660.json
sha256sum 854-chat-export-1787302403660.json
# ожидается: 3b1b1b742cf86e31f3024cddf85b2d9441e2ce5e7d494e78de3b43b02bed694a

python3 experiments/issue_309_run_stats.py 854-chat-export-1787302403660.json \
  --json /tmp/stats/854-chat-export-1787302403660.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
