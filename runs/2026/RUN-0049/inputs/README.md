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

# Вход прогона RUN-0049 — провенанс

Тема: **Сопоставление параметров API речевой аналитики**. Сверка параметров API речевой аналитики с описанием и подготовка требований.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`935-chat-export-1787302221867.json`](https://github.com/user-attachments/files/31336084/935-chat-export-1787302221867.json) |
| Размер, байт | 519948 |
| SHA-256 | `c126129dd49ae949ae6a73da3dbcff8de800917d65250d389facd8c14c00777f` |
| Заголовок чата в экспорте | `935` |
| Окно диалога, UTC | 2026-01-28 07:38:26 — 2026-02-11 12:11:43 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 935-chat-export-1787302221867.json \
  https://github.com/user-attachments/files/31336084/935-chat-export-1787302221867.json
sha256sum 935-chat-export-1787302221867.json
# ожидается: c126129dd49ae949ae6a73da3dbcff8de800917d65250d389facd8c14c00777f

python3 experiments/issue_309_run_stats.py 935-chat-export-1787302221867.json \
  --json /tmp/stats/935-chat-export-1787302221867.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
