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

# Вход прогона RUN-0045 — провенанс

Тема: **Звуковой сигнал соединения**. Проработка требований к звуковому уведомлению при соединении.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`915-chat-export-1787302233588.json`](https://github.com/user-attachments/files/31336083/915-chat-export-1787302233588.json) |
| Размер, байт | 418450 |
| SHA-256 | `c8751e6b4741e488e81489321038de6dd23b29e119c08ed7f8a356166c720228` |
| Заголовок чата в экспорте | `915` |
| Окно диалога, UTC | 2026-01-12 14:25:13 — 2026-01-30 14:34:30 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 915-chat-export-1787302233588.json \
  https://github.com/user-attachments/files/31336083/915-chat-export-1787302233588.json
sha256sum 915-chat-export-1787302233588.json
# ожидается: c8751e6b4741e488e81489321038de6dd23b29e119c08ed7f8a356166c720228

python3 experiments/issue_309_run_stats.py 915-chat-export-1787302233588.json \
  --json /tmp/stats/915-chat-export-1787302233588.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
