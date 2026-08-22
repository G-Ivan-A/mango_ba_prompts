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

# Вход прогона RUN-0033 — провенанс

Тема: **Выгрузка данных речевой аналитики во внешнюю систему**. Разработка и валидация ФТ на передачу результатов речевой аналитики во внешнюю систему (кейс E-Staff).

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`804-chat-export-1787302424624.json`](https://github.com/user-attachments/files/31336067/804-chat-export-1787302424624.json) |
| Размер, байт | 1951602 |
| SHA-256 | `5ab4fcbaea0efb45f2c59c37b9bb268566b8efbc50c5f13be425170bd1fe9f94` |
| Заголовок чата в экспорте | `804` |
| Окно диалога, UTC | 2025-09-12 13:44:54 — 2025-10-01 08:26:13 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 804-chat-export-1787302424624.json \
  https://github.com/user-attachments/files/31336067/804-chat-export-1787302424624.json
sha256sum 804-chat-export-1787302424624.json
# ожидается: 5ab4fcbaea0efb45f2c59c37b9bb268566b8efbc50c5f13be425170bd1fe9f94

python3 experiments/issue_309_run_stats.py 804-chat-export-1787302424624.json \
  --json /tmp/stats/804-chat-export-1787302424624.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
