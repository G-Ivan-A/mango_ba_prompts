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

# Вход прогона RUN-0037 — провенанс

Тема: **Новый статус пресета блокировки звонков**. Разбор постановки и ФТ на новый статус пресета; в диалоге переданы объёмные документы-приложения.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`838-chat-export-1787302378596.json`](https://github.com/user-attachments/files/31336076/838-chat-export-1787302378596.json) |
| Размер, байт | 2578912 |
| SHA-256 | `40f49ef7b3d0687e70056ab64df6a355e6885863dd43e19fa589fbdc068b2a0e` |
| Заголовок чата в экспорте | `838` |
| Окно диалога, UTC | 2025-09-17 13:19:20 — 2025-10-22 14:40:18 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 838-chat-export-1787302378596.json \
  https://github.com/user-attachments/files/31336076/838-chat-export-1787302378596.json
sha256sum 838-chat-export-1787302378596.json
# ожидается: 40f49ef7b3d0687e70056ab64df6a355e6885863dd43e19fa589fbdc068b2a0e

python3 experiments/issue_309_run_stats.py 838-chat-export-1787302378596.json \
  --json /tmp/stats/838-chat-export-1787302378596.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
