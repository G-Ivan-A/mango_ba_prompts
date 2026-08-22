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

# Вход прогона RUN-0053 — провенанс

Тема: **Привязка звонков к сделкам и чек-листам Битрикс24**. Длинная проработка ФТ на привязку звонков к сущностям Битрикс24 и чек-листам.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`977-chat-export-1787301867394.json`](https://github.com/user-attachments/files/31336078/977-chat-export-1787301867394.json) |
| Размер, байт | 2523963 |
| SHA-256 | `a359530f43551f3bd80227d1310dc6f14a22c2767c08422f086d6eb7b4f0d820` |
| Заголовок чата в экспорте | `977` |
| Окно диалога, UTC | 2026-03-23 14:11:55 — 2026-04-07 08:21:23 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 977-chat-export-1787301867394.json \
  https://github.com/user-attachments/files/31336078/977-chat-export-1787301867394.json
sha256sum 977-chat-export-1787301867394.json
# ожидается: a359530f43551f3bd80227d1310dc6f14a22c2767c08422f086d6eb7b4f0d820

python3 experiments/issue_309_run_stats.py 977-chat-export-1787301867394.json \
  --json /tmp/stats/977-chat-export-1787301867394.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
