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

# Вход прогона RUN-0044 — провенанс

Тема: **Открытие URL при ответе на звонок — валидация**. Короткая сессия валидации ФТ по задаче 908.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`908_2-chat-export-1787302303728.json`](https://github.com/user-attachments/files/31336072/908_2-chat-export-1787302303728.json) |
| Размер, байт | 162853 |
| SHA-256 | `c05adc89d622658ce3e122fe567c6a6f045c628fe6a8d35b344b8bb465697e04` |
| Заголовок чата в экспорте | `908-2` |
| Окно диалога, UTC | 2025-12-18 11:43:55 — 2025-12-18 12:39:37 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 908_2-chat-export-1787302303728.json \
  https://github.com/user-attachments/files/31336072/908_2-chat-export-1787302303728.json
sha256sum 908_2-chat-export-1787302303728.json
# ожидается: c05adc89d622658ce3e122fe567c6a6f045c628fe6a8d35b344b8bb465697e04

python3 experiments/issue_309_run_stats.py 908_2-chat-export-1787302303728.json \
  --json /tmp/stats/908_2-chat-export-1787302303728.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
