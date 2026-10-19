---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/373"
---

# Вход прогона RUN-0073 — провенанс

Тема: **задача 1123 — генерация BCREQ-ФТ «Сервис-коннектор ВАТС MANGO OFFICE → CallMentor»**. БА шаблоном-промптом (реплика 0) запустил посекционную генерацию документа (разделы 1–7 и реестр открытых вопросов) и в течение трёх дней правил ответы двух моделей. Прогон фиксирует диалог ради статистики ошибок ИИ и золотых наборов для промптов, правил и навыков генерации BCREQ-ФТ.

## Источники

| Поле | Значение |
| --- | --- |
| Вложение issue | [`chat-export-1123.json`](https://github.com/user-attachments/files/33662573/chat-export-1123.json) |
| Размер, байт | 1672643 |
| SHA-256 | `318212fec8f2c3c4078bea71d32bb4607d74766961e64722e3c82cf875b01c27` |
| Заголовок чата в экспорте | `1123` |
| Окно диалога, UTC | 2026-10-16 09:10:17 — 2026-10-19 10:56:30 |
| Реплик в линейной ветке | 106 (53 БА, 53 модели) |
| Модели | qwen3.7-plus, qwen3.8-max |
| SSOT продуктовой принадлежности | [mango-ba-ai-runtime @ `91406e4`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/91406e430aeb70dabf20548eee0ea95127f42690): `taxonomy/products.yaml`, `AGENTS.md`, `golden/cases.yaml`, `docs/kb` |

## Вложения внутри диалога

Перечислены только имена файлов: ссылки на вложения в экспорте содержат подписанные токены CDN и в репозиторий не переносятся.

| Файл | Реплика | Что это |
| --- | --- | --- |
| `-5344018727864835633_121 (1).jpg` | 6 | изображение; в тексте реплики БА назвал его «файл конкурентов» |
| `Модуль ЦОВ Робот Фил 2,0_manual_v7.26.28.pdf` | 102 | руководство Робота Фил 2.0 — БА передал предложение коллег закрыть кейс «роботом-администратором» без доработки; в КБ runtime есть разбор того же руководства `docs/kb/cov-robot-fil` |

## Почему исходного JSON нет в репозитории

По правилу, принятому в issue [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309), сырые экспорты чатов в репозитории не остаются: вход прогона описан провенансом (ссылка, размер, контрольная сумма), а все производные артефакты порождаются из него детерминированно. Цитаты в записи — дословные фрагменты экспорта, каждая сверена с ним ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

## Воспроизведение

Экспорт — недоверенные данные: он скачивается в отдельный пустой каталог, а скрипты, которые его читают, запускаются из репозитория с `python3 -I`.

```bash
mkdir -p /tmp/dl373
curl -L -o /tmp/dl373/chat-export-1123.json \
  https://github.com/user-attachments/files/33662573/chat-export-1123.json
sha256sum /tmp/dl373/chat-export-1123.json
# ожидается: 318212fec8f2c3c4078bea71d32bb4607d74766961e64722e3c82cf875b01c27

mkdir -p experiments/issue_373
python3 -I experiments/issue_309_run_stats.py /tmp/dl373/chat-export-1123.json \
  --json experiments/issue_373/stats.json
python3 -I scripts/chat_export_to_markdown.py /tmp/dl373/chat-export-1123.json \
  --transcript experiments/issue_373/transcript.md \
  --metrics experiments/issue_373/turn-metrics.md

python3 -I experiments/issue_373_verify_quotes.py /tmp/dl373/chat-export-1123.json
python3 -I experiments/issue_373_golden_set.py
```

В репозитории остаются `experiments/issue_373/stats.json` и `experiments/issue_373/quote-check.json` (числа и контрольные суммы без текста переписки и без ссылок на вложения): по ним генератор и валидатор `scripts/validate_issue_373_run.py` воспроизводят запись без исходного экспорта. Стенограмма в репозиторий не коммитится.

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику и дословные цитаты, а не всю переписку;
- нет итогового документа BCREQ-ФТ: последняя редакция БА (реплика 104) — промежуточная, приёмки документа в экспорте нет;
- нет содержимого изображения из реплики 6 и текста PDF Робота Фил: при фиксации они не открывались, утверждения о Роботе Фил сверены с КБ runtime.
