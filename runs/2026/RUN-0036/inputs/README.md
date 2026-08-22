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

# Вход прогона RUN-0036 — провенанс

Тема: **Текст согласия на обработку персональных данных**. Проработка и валидация ФТ на настраиваемый текст согласия.

## Источник

| Поле | Значение |
| --- | --- |
| Вложение issue | [`817-chat-export-1787302455834.json`](https://github.com/user-attachments/files/31336069/817-chat-export-1787302455834.json) |
| Размер, байт | 463786 |
| SHA-256 | `76db5d52bca4372a73c9bc3c99bdd24558190cf446b5db04bae654a4346ca13d` |
| Заголовок чата в экспорте | `817` |
| Окно диалога, UTC | 2025-09-09 07:41:17 — 2025-09-09 13:29:05 |

## Почему исходного JSON нет в репозитории

Задача [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309) требует зафиксировать прогоны как **статистику применения промптов** и удалить исходные JSON-файлы из репозитория. Поэтому вход прогона описан провенансом, а не копией сырых данных: файл однозначно идентифицируется ссылкой и контрольной суммой, а все производные артефакты прогона порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o 817-chat-export-1787302455834.json \
  https://github.com/user-attachments/files/31336069/817-chat-export-1787302455834.json
sha256sum 817-chat-export-1787302455834.json
# ожидается: 76db5d52bca4372a73c9bc3c99bdd24558190cf446b5db04bae654a4346ca13d

python3 experiments/issue_309_run_stats.py 817-chat-export-1787302455834.json \
  --json /tmp/stats/817-chat-export-1787302455834.json
python3 experiments/issue_309_fixate_runs.py --stats-dir /tmp/stats
```

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет вложений диалога (документы, расшифровки): в записи остаются только их имена и количество обращений — см. [`../outputs/prompt-usage.md`](../outputs/prompt-usage.md).
