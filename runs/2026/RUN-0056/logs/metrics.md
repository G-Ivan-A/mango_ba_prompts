---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/315"
---

# Метрики прогона RUN-0056 — обоснование чисел

| Метрика | Значение | Как получено |
| --- | --- | --- |
| `verdict` | `works-with-edits` | Совпадает с вердиктом [`experiment-log.md`](experiment-log.md). |
| `success_rate` | 0.7 | Доля требований ФТ с полностью обоснованным вердиктом покрытия: 7 из 10 (ФТ-01, ФТ-02, ФТ-03, ФТ-05, ФТ-07, ФТ-08, ФТ-09). Частичные — ФТ-04, ФТ-06, ФТ-10: их вердикт ограничен недоступностью источников. |
| `success_rate_basis` | см. `metadata.yaml` | База — требования ФТ, а не утверждения об API. Иная база даст иное число. |
| `sources_studied` | 15 | 1 ФТ + 12 документов `hhru/api` (перечень в [`../inputs/README.md`](../inputs/README.md)) + 2 группы источников БЗ Mango (LK, CC). |
| `hh_api_docs_read` | 12 | Пересчёт файлов `hhru/api`, прочитанных целиком. |
| `kb_sections_read` | 6 | Разделы БЗ, использованные как источник фактов в выводе. |
| `requirements_assessed` | 10 | ФТ-01…ФТ-10. |
| `critical_gaps` | 7 | Число маркеров `⚠️ КРИТИЧЕСКИЙ GAP` в [`../outputs/L2-gap-matrix.md`](../outputs/L2-gap-matrix.md): GAP-1…GAP-7. |
| `duration_active_s` | 10800 | Оценка активного времени работы исполнителя; `measured: false`. |
| `token_method` | `not-recorded` | Токены провайдера в среде прогона не фиксировались; поле оставлено явным, а не выдуманным. |

Не измерялось и потому не приводится: число итераций диалога, календарная длительность, объём правок БА (приёмка не выполнена).
