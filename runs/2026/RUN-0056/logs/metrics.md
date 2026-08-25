---
status: draft
version: 0.1
updated: 2026-08-25
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/317"
related_artifacts:
  - "standards/kb-standard.md"
  - "standards/runs-contract-standard.md"
---

# Метрики RUN-0056

Все числа взяты из `meta.json` соответствующих разделов БЗ (поля
`section_count`, `page_count`, `tokens_total`, `image_count`, `table_count`,
`verification.*`), метод подсчёта токенов — `tiktoken:cl100k_base`.

| Раздел БЗ | Стр. | Разделов | Токенов | Изобр. | Табл. | Крит. токенов сверено | Не подтверждено |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mango-cc-manual` | 614 | 139 | 425 137 | 1774 | 527 | 1088 | 2 |
| `mango-lk-manual` | 565 | 351 | 310 345 | 1540 | 54 | 1505 | 0 |
| `mdialogi-api` | 96 | 70 | 50 413 | 13 | 161 | 1591 | 0 |
| `cov-robot-fil` | 195 | 75 | 96 376 | 455 | 41 | 515 | 0 |
| `mtalker/windows-mac-working` | 128 | 143 | 102 173 | 362 | 5 | 808 | 0 |
| `mtalker/android-user-guide` | 66 | 99 | 47 293 | 146 | 5 | 313 | 0 |
| **Итого** | **1664** | **877** | **1 031 737** | **4290** | **793** | **5820** | **2** |

Доля подтверждённых критических токенов: 5818 / 5820 = 0.9997.

Токены диалога исполнителя не фиксировались: прогон выполнялся как серия
запусков детерминированных скриптов, метрика провайдера для него не собиралась.
