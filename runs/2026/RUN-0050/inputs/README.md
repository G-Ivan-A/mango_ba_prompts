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

# Вход прогона RUN-0050 — провенанс

Тема: **Формат по образцу в редакторе письма**. Проработка ФТ на инструмент «формат по образцу» в почтовом редакторе.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`942-chat-export-1787302178299.json`](https://github.com/user-attachments/files/31336079/942-chat-export-1787302178299.json) |
| Размер, байт | 918795 |
| SHA-256 | `8a4bc8506daf2db987117118324a0b895f6a78089bfe10df6652ea28c90725ae` |
| Заголовок чата в экспорте | `942` |
| Окно диалога, UTC | 2026-02-11 10:20:17 — 2026-02-27 14:30:36 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 942-chat-export-1787302178299.json \
  https://github.com/user-attachments/files/31336079/942-chat-export-1787302178299.json
sha256sum 942-chat-export-1787302178299.json
# ожидается: 8a4bc8506daf2db987117118324a0b895f6a78089bfe10df6652ea28c90725ae

python3 experiments/issue_309_run_stats.py 942-chat-export-1787302178299.json \
  --json /tmp/stats/942-chat-export-1787302178299.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
