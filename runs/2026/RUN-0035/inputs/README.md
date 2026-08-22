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

# Вход прогона RUN-0035 — провенанс

Тема: **Рекомендации по базе знаний ELMA**. Одноэпизодный прогон: генерация раздела ФТ по работе с базой знаний.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`806-chat-export-1787302469723.json`](https://github.com/user-attachments/files/31336068/806-chat-export-1787302469723.json) |
| Размер, байт | 40489 |
| SHA-256 | `bda19e898af61287d1b90532ea569de993b188c62cbc2558b25f48333d3ba62a` |
| Заголовок чата в экспорте | `806` |
| Окно диалога, UTC | 2025-08-11 14:20:51 — 2025-08-11 14:20:51 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 806-chat-export-1787302469723.json \
  https://github.com/user-attachments/files/31336068/806-chat-export-1787302469723.json
sha256sum 806-chat-export-1787302469723.json
# ожидается: bda19e898af61287d1b90532ea569de993b188c62cbc2558b25f48333d3ba62a

python3 experiments/issue_309_run_stats.py 806-chat-export-1787302469723.json \
  --json /tmp/stats/806-chat-export-1787302469723.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
