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

# Вход прогона RUN-0051 — провенанс

Тема: **Мультивыбор в фильтре записей звонков**. Проработка ФТ на множественный выбор номеров и CRM-сущностей в фильтре записей разговоров.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`960-chat-export-1787301855482.json`](https://github.com/user-attachments/files/31336091/960-chat-export-1787301855482.json) |
| Размер, байт | 1493530 |
| SHA-256 | `78e27b0641c25f59ba8bf6b963dbff948d034786cf259594374ba023dff46b92` |
| Заголовок чата в экспорте | `960` |
| Окно диалога, UTC | 2026-02-17 11:58:58 — 2026-04-08 13:47:47 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 960-chat-export-1787301855482.json \
  https://github.com/user-attachments/files/31336091/960-chat-export-1787301855482.json
sha256sum 960-chat-export-1787301855482.json
# ожидается: 78e27b0641c25f59ba8bf6b963dbff948d034786cf259594374ba023dff46b92

python3 experiments/issue_309_run_stats.py 960-chat-export-1787301855482.json \
  --json /tmp/stats/960-chat-export-1787301855482.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
