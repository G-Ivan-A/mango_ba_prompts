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

# Вход прогона RUN-0054 — провенанс

Тема: **Подмена номера — уточняющие вопросы**. Короткий прогон элицитации: формулирование уточняющих вопросов по задаче подмены номера.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`980-chat-export-1787301841993.json`](https://github.com/user-attachments/files/31336089/980-chat-export-1787301841993.json) |
| Размер, байт | 196619 |
| SHA-256 | `fd1d6d7b8c1cb6f479de61ccc0058ea1f80a45483fdd9ef836ccd58869653ee4` |
| Заголовок чата в экспорте | `980` |
| Окно диалога, UTC | 2026-04-08 16:12:47 — 2026-04-08 16:39:31 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 980-chat-export-1787301841993.json \
  https://github.com/user-attachments/files/31336089/980-chat-export-1787301841993.json
sha256sum 980-chat-export-1787301841993.json
# ожидается: fd1d6d7b8c1cb6f479de61ccc0058ea1f80a45483fdd9ef836ccd58869653ee4

python3 experiments/issue_309_run_stats.py 980-chat-export-1787301841993.json \
  --json /tmp/stats/980-chat-export-1787301841993.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
