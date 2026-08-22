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

# Вход прогона RUN-0046 — провенанс

Тема: **Обязательные теги тематик звонка**. Длинная проработка правил обязательного проставления тематик и их выгрузки в отчёты.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`918-chat-export-1787302206030.json`](https://github.com/user-attachments/files/31336077/918-chat-export-1787302206030.json) |
| Размер, байт | 1586933 |
| SHA-256 | `8160af678d10cb3be02ee49f0e191fb222b4d87eaa7ac4b37739d91d7963e0c4` |
| Заголовок чата в экспорте | `918` |
| Окно диалога, UTC | 2026-01-21 07:30:44 — 2026-02-18 11:41:09 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 918-chat-export-1787302206030.json \
  https://github.com/user-attachments/files/31336077/918-chat-export-1787302206030.json
sha256sum 918-chat-export-1787302206030.json
# ожидается: 8160af678d10cb3be02ee49f0e191fb222b4d87eaa7ac4b37739d91d7963e0c4

python3 experiments/issue_309_run_stats.py 918-chat-export-1787302206030.json \
  --json /tmp/stats/918-chat-export-1787302206030.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
