---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
---

# Вход RUN-0083

## Что проверяется

Пригодность черновиков «по тесту» шагов A-IN (Ш-0, Ш-1, Ш-2) к тесту БА
через run kit: короткий путь к тестированию на синтетическом прогоне
(issue #446, пункт 4). Два плеча на одном и том же диалоге:

| Плечо | Тексты | Источник |
| --- | --- | --- |
| P | опубликованные v0.1 | `prompts/bcreq-constitution-governance-oneshot.md`, `prompts/bcreq-context-understanding-stepwise.md`, `prompts/bcreq-products-impact-analysis-stepwise.md` |
| T | черновики BL-156 «по тесту» на реестре 0.4 | те же имена в `prompts/drafts/` |

Полные SHA-256 шести текстов — поле `prompts` в
[`../outputs/summary.json`](../outputs/summary.json).

## Файлы

| Файл | Что внутри |
| --- | --- |
| [`input-pack.md`](input-pack.md) | Карточка задачи и запрос Заказчика SIM-1106 из сида RUN-0078, заметка о базе знаний runtime |
| [`ba-script.md`](ba-script.md) | Реплики БА по порядку: подтверждение параметров, приоритет источников, поправка scope S-56 (КЦ вне scope), S-110, S-142, «команды не знаю» |

База знаний — `G-Ivan-A/mango-ba-ai-runtime` на коммите
`f31dcde33f0bc120244128faab98fc0162e45701` (срез реестра runtime 0.4).
Исполнитель открывал её как локальный клон: ссылка промпта на файл
runtime по этому SHA — тот же относительный путь в клоне.

## Правило решения

Записано и закоммичено до запуска подагентов:
[`../logs/preregistration.md`](../logs/preregistration.md).
