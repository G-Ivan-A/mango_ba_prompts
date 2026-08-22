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

# Вход прогона RUN-0042 — провенанс

Тема: **Восстановление страниц базы знаний**. Разбор сценариев восстановления удалённых страниц базы знаний (Wiki.js/Git) и подготовка требований.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`892-chat-export-1787302153813.json`](https://github.com/user-attachments/files/31336080/892-chat-export-1787302153813.json) |
| Размер, байт | 922832 |
| SHA-256 | `0d780de8ec68739974fbd258c7b992efe14a73d2a91e1aff2a7464ac7768cb96` |
| Заголовок чата в экспорте | `892` |
| Окно диалога, UTC | 2026-03-03 14:21:48 — 2026-03-12 06:16:36 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 892-chat-export-1787302153813.json \
  https://github.com/user-attachments/files/31336080/892-chat-export-1787302153813.json
sha256sum 892-chat-export-1787302153813.json
# ожидается: 0d780de8ec68739974fbd258c7b992efe14a73d2a91e1aff2a7464ac7768cb96

python3 experiments/issue_309_run_stats.py 892-chat-export-1787302153813.json \
  --json /tmp/stats/892-chat-export-1787302153813.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
