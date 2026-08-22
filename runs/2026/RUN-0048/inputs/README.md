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

# Вход прогона RUN-0048 — провенанс

Тема: **Два поля комментария и тегов в amoCRM**. Проработка ФТ на раздельные поля комментария и тегов при записи звонка в amoCRM.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`930-chat-export-1787301829163.json`](https://github.com/user-attachments/files/31336085/930-chat-export-1787301829163.json) |
| Размер, байт | 751227 |
| SHA-256 | `55bd03ec6980cef1fba8fa7770c6a549297247b83e5a5386b22eb85af435718d` |
| Заголовок чата в экспорте | `930` |
| Окно диалога, UTC | 2026-04-14 14:26:00 — 2026-04-20 13:47:15 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 930-chat-export-1787301829163.json \
  https://github.com/user-attachments/files/31336085/930-chat-export-1787301829163.json
sha256sum 930-chat-export-1787301829163.json
# ожидается: 55bd03ec6980cef1fba8fa7770c6a549297247b83e5a5386b22eb85af435718d

python3 experiments/issue_309_run_stats.py 930-chat-export-1787301829163.json \
  --json /tmp/stats/930-chat-export-1787301829163.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
