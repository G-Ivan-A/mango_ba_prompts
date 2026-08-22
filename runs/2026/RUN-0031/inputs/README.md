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

# Вход прогона RUN-0031 — провенанс

Тема: **Единая сущность обращения (сделка/тикет)**. Проработка промптов и ФТ для унифицированной сущности обращения с опорой на отраслевые модели (TM Forum) и разбор границ сделки и тикета.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`791-chat-export-1787302391232.json`](https://github.com/user-attachments/files/31336088/791-chat-export-1787302391232.json) |
| Размер, байт | 3270910 |
| SHA-256 | `00ac99aaa4c4240e940f2df970a10b28cd0495021bce8bc5f2184ac293d15814` |
| Заголовок чата в экспорте | `791` |
| Окно диалога, UTC | 2025-09-04 06:38:01 — 2025-10-22 10:13:53 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 791-chat-export-1787302391232.json \
  https://github.com/user-attachments/files/31336088/791-chat-export-1787302391232.json
sha256sum 791-chat-export-1787302391232.json
# ожидается: 00ac99aaa4c4240e940f2df970a10b28cd0495021bce8bc5f2184ac293d15814

python3 experiments/issue_309_run_stats.py 791-chat-export-1787302391232.json \
  --json /tmp/stats/791-chat-export-1787302391232.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
