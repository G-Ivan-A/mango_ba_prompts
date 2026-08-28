---
status: draft
version: 0.1
updated: 2026-08-28
ai-generated: true
type: input
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/336"
---

# Вход прогона RUN-0061 — провенанс

Тема: **задача 1090 — human review отчёта L0 в части ссылок на вики twin**. БА проверял выводы отчёта [`../../RUN-0057/outputs/L0-customer-form-with-assessment.md`](../../RUN-0057/outputs/L0-customer-form-with-assessment.md), переходя по источникам, и требовал от модели такие ссылки, по которым проверку можно выполнить быстро и однозначно.

## Источники

| Поле | Значение |
| --- | --- |
| Вложение issue | [`chat-export-1787928921525.json`](https://github.com/user-attachments/files/31558980/chat-export-1787928921525.json) |
| Размер, байт | 475614 |
| SHA-256 | `cd009dd44f0ac42d14b5169fec03182490ecf4b4d3c30ccac8b9532c5223c276` |
| Заголовок чата в экспорте | `1090` |
| Окно диалога, UTC | 2026-08-26 07:52:49 — 2026-08-28 11:27:09 |
| Проверяемый отчёт | [`runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md`](../../RUN-0057/outputs/L0-customer-form-with-assessment.md) |
| Публичная вики | <https://wiki.twin24.ai> (страницы читаются анонимно) |

## Почему исходного JSON нет в репозитории

По правилу, принятому в issue [#309](https://github.com/G-Ivan-A/mango_ba_prompts/issues/309), сырые экспорты чатов в репозитории не остаются: вход прогона описан провенансом (ссылка, размер, контрольная сумма), а все производные артефакты порождаются из него детерминированно.

## Воспроизведение

```bash
curl -L -o chat-export-1787928921525.json \
  https://github.com/user-attachments/files/31558980/chat-export-1787928921525.json
sha256sum chat-export-1787928921525.json
# ожидается: cd009dd44f0ac42d14b5169fec03182490ecf4b4d3c30ccac8b9532c5223c276

mkdir -p experiments/issue_336
python3 experiments/issue_309_run_stats.py chat-export-1787928921525.json \
  --json experiments/issue_336/stats.json
python3 scripts/chat_export_to_markdown.py chat-export-1787928921525.json \
  --output experiments/issue_336/transcript.md \
  --metrics experiments/issue_336/turn-metrics.md

python3 experiments/issue_336_link_audit.py \
  --report runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md \
  --transcript experiments/issue_336/transcript.md \
  --cache experiments/issue_336/wiki-cache \
  --json experiments/issue_336/link-audit.json --check-report-pages

python3 experiments/issue_336_fixate_run.py
```

Аудит ссылок кэширует HTML страниц вики в каталоге `--cache`, поэтому повторный запуск воспроизводит те же числа без обращения к сети. Кэш и стенограмма в репозиторий не коммитятся.

## Чего во входе нет

- нет сырого JSON-экспорта и полной стенограммы: прогон фиксирует статистику, а не содержимое переписки;
- нет копий страниц вики: в записи остаются пути страниц, HTTP-статусы, заглавия и число заголовков — см. [`../logs/link-verification.md`](../logs/link-verification.md);
- нет закрытых документов: проверялись только анонимно доступные страницы `wiki.twin24.ai`.
