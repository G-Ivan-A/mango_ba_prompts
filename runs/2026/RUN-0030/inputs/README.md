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

# Вход прогона RUN-0030 — провенанс

Тема: **Выбор абонента 1С при входящем звонке**. Очистка ASR-расшифровки встречи, суммаризация договорённостей и разработка ФТ на выбор абонента/партнёра в связке ВАТС ↔ 1С.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`599-chat-export-1787302166886.json`](https://github.com/user-attachments/files/31336086/599-chat-export-1787302166886.json) |
| Размер, байт | 1319632 |
| SHA-256 | `5fc1909b7adfb51c9643fd8a489037063c4c79f06fb28e6c45bd4861f384ba2f` |
| Заголовок чата в экспорте | `599` |
| Окно диалога, UTC | 2026-03-02 14:42:03 — 2026-03-10 06:31:58 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 599-chat-export-1787302166886.json \
  https://github.com/user-attachments/files/31336086/599-chat-export-1787302166886.json
sha256sum 599-chat-export-1787302166886.json
# ожидается: 5fc1909b7adfb51c9643fd8a489037063c4c79f06fb28e6c45bd4861f384ba2f

python3 experiments/issue_309_run_stats.py 599-chat-export-1787302166886.json \
  --json /tmp/stats/599-chat-export-1787302166886.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
