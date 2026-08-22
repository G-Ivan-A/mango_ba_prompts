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

# Вход прогона RUN-0043 — провенанс

Тема: **Открытие URL при ответе на звонок**. Проработка ФТ на открытие внешней ссылки в момент ответа на звонок.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`908-chat-export-1787302322682.json`](https://github.com/user-attachments/files/31336090/908-chat-export-1787302322682.json) |
| Размер, байт | 313668 |
| SHA-256 | `cb4b7c284bfb187b41c3e7dc6a896e2d534f2d24f72175024f705e6461ac5121` |
| Заголовок чата в экспорте | `908` |
| Окно диалога, UTC | 2025-12-11 12:50:26 — 2025-12-18 11:42:10 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 908-chat-export-1787302322682.json \
  https://github.com/user-attachments/files/31336090/908-chat-export-1787302322682.json
sha256sum 908-chat-export-1787302322682.json
# ожидается: cb4b7c284bfb187b41c3e7dc6a896e2d534f2d24f72175024f705e6461ac5121

python3 experiments/issue_309_run_stats.py 908-chat-export-1787302322682.json \
  --json /tmp/stats/908-chat-export-1787302322682.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
