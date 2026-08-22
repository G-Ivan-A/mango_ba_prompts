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

# Вход прогона RUN-0040 — провенанс

Тема: **Повторный запуск проактивного чата**. Длинная проработка правил повторного срабатывания проактивного приглашения в чат.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`872-chat-export-1787302366667.json`](https://github.com/user-attachments/files/31336075/872-chat-export-1787302366667.json) |
| Размер, байт | 2229079 |
| SHA-256 | `dd69b62776ee6a6178d77aa71cfcb9bb2afb0dc7ea09ff4ece5aaabd6c488ef4` |
| Заголовок чата в экспорте | `872` |
| Окно диалога, UTC | 2025-10-20 13:53:02 — 2025-10-28 08:52:31 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 872-chat-export-1787302366667.json \
  https://github.com/user-attachments/files/31336075/872-chat-export-1787302366667.json
sha256sum 872-chat-export-1787302366667.json
# ожидается: dd69b62776ee6a6178d77aa71cfcb9bb2afb0dc7ea09ff4ece5aaabd6c488ef4

python3 experiments/issue_309_run_stats.py 872-chat-export-1787302366667.json \
  --json /tmp/stats/872-chat-export-1787302366667.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
