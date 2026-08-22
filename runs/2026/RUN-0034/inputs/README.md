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

# Вход прогона RUN-0034 — провенанс

Тема: **Выгрузка данных речевой аналитики — финальная итерация**. Продолжение задачи 804: доведение ФТ до финальной редакции, настройки отправки и разбор замечаний.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`804_2-chat-export-1787302436487.json`](https://github.com/user-attachments/files/31336070/804_2-chat-export-1787302436487.json) |
| Размер, байт | 1939259 |
| SHA-256 | `b523ab973656a02df3bd2cec0e5977c5a0ea7f241ab730853ee13ad0028c0b90` |
| Заголовок чата в экспорте | `804 - финал` |
| Окно диалога, UTC | 2025-10-01 08:27:41 — 2025-10-06 11:28:53 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 804_2-chat-export-1787302436487.json \
  https://github.com/user-attachments/files/31336070/804_2-chat-export-1787302436487.json
sha256sum 804_2-chat-export-1787302436487.json
# ожидается: b523ab973656a02df3bd2cec0e5977c5a0ea7f241ab730853ee13ad0028c0b90

python3 experiments/issue_309_run_stats.py 804_2-chat-export-1787302436487.json \
  --json /tmp/stats/804_2-chat-export-1787302436487.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
