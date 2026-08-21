---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: registry
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
related_artifacts:
  - "standards/runs-contract-standard.md"
---

# Runs: результаты выполнения процессов

`runs/` — единый каталог результатов выполнения процессов. Здесь хранятся
зафиксированные прогоны промптов, BA-процессов, анализов и self-test сценариев.
Маршруты и правила работы остаются в `docs/`, `prompts/`, `patterns/` и
`standards/`; результат применения этих правил записывается сюда.

## Контракт записи

Каждая запись живёт по схеме `runs/YYYY/RUN-XXXX/`.

```text
runs/
└── YYYY/
    └── RUN-XXXX/
        ├── metadata.yaml
        ├── inputs/
        ├── outputs/
        ├── feedback/
        └── logs/
```

`metadata.yaml` содержит минимальный набор полей:

| Поле | Обязательное | Значение |
| --- | --- | --- |
| `run_id` | да | Идентификатор вида `RUN-XXXX`, совпадает с именем папки. |
| `process` | да | Процесс или сценарий, который выполнялся. |
| `version` | да | Версия записи или основного результата. |
| `date` | да | Дата выполнения или фиксации результата в формате `YYYY-MM-DD`. |
| `author` | да | Автор фиксации результата: БА, человек+LLM или агент. |
| `model` | да | Использованная модель; если не записана, указывается `not-recorded`. |
| `status` | да | Состояние результата: например `draft`, `experimental`, `success`, `partial-success`, `works-with-edits`. |

Дополнительные поля разрешены: `source_paths`, `inputs`, `outputs`, `logs`,
`related_issues`, `related_artifacts`, `related_runs`.

## Назначение подкаталогов

| Подкаталог | Что хранится |
| --- | --- |
| `inputs/` | Сырой вход, выдержки БЗ, исходные данные, которые можно хранить в репозитории. |
| `outputs/` | Итоговые и промежуточные артефакты выполнения процесса. |
| `feedback/` | Комментарии ревью, обратная связь, решения по результату. |
| `logs/` | Логи эксперимента, метрики, трассировка выполнения, технические журналы. |

Если подкаталог пока пустой, он сохраняется через `.gitkeep`, чтобы структура
каждого run была одинаковой.

## Реестр перенесённых записей Phase 0

| Run | Дата | Процесс | Основной результат |
| --- | --- | --- | --- |
| [`RUN-0001`](2026/RUN-0001/metadata.yaml) | 2026-05-26 | prompt-experiment | [`tz-stats-prototype-2026-05.md`](2026/RUN-0001/outputs/tz-stats-prototype-2026-05.md) |
| [`RUN-0002`](2026/RUN-0002/metadata.yaml) | 2026-05-26 | user-story-generation | [`user-story_gen-from-raw-request_2026-05-26.md`](2026/RUN-0002/outputs/user-story_gen-from-raw-request_2026-05-26.md) |
| [`RUN-0003`](2026/RUN-0003/metadata.yaml) | 2026-05-26 | usecase-generation | [`usecase_gen-stepwise-alignment_2026-05-26.md`](2026/RUN-0003/outputs/usecase_gen-stepwise-alignment_2026-05-26.md) |
| [`RUN-0004`](2026/RUN-0004/metadata.yaml) | 2026-05-26 | prompt-audit | [`prompts-audit-2026-05-26.md`](2026/RUN-0004/outputs/prompts-audit-2026-05-26.md) |
| [`RUN-0005`](2026/RUN-0005/metadata.yaml) | 2026-05-26 | prompt-selftest | [`prompts-selftest-2026-05-26.md`](2026/RUN-0005/outputs/prompts-selftest-2026-05-26.md) |
| [`RUN-0006`](2026/RUN-0006/metadata.yaml) | 2026-06-13 | session-debug-documentation | [`session-debug-summarizer-2026-06-13.md`](2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md) |
| [`RUN-0007`](2026/RUN-0007/metadata.yaml) | 2026-06-16 | fr-generation | [`fr-generation-1027-live_2026-06-16.md`](2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md) |
| [`RUN-0008`](2026/RUN-0008/metadata.yaml) | 2026-06-16 | kb-citation-check | [`kb-citation-check-2026-06-16.md`](2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md) |
| [`RUN-0009`](2026/RUN-0009/metadata.yaml) | 2026-06-16 | industry-standards-ab-check | [`standards-applied-ab-2026-06-16.md`](2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md) |
| [`RUN-0010`](2026/RUN-0010/metadata.yaml) | 2026-06-17 | bcreq-1025-email-routing | [`2026-06-17-bcreq-1025-email-routing.md`](2026/RUN-0010/outputs/2026-06-17-bcreq-1025-email-routing.md), [`analysis-bcreq-1025-2026-06-17.md`](2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md) |
| [`RUN-0011`](2026/RUN-0011/metadata.yaml) | 2026-06-18 | multichannel-agent-workload | [`outputs/README.md`](2026/RUN-0011/outputs/README.md), [`logs/experiment-log.md`](2026/RUN-0011/logs/experiment-log.md) |
| [`RUN-0012`](2026/RUN-0012/metadata.yaml) | 2026-07-14 | bcreq-1069-restricted-api-key | [`outputs/final-artifact.md`](2026/RUN-0012/outputs/final-artifact.md), [`outputs/README.md`](2026/RUN-0012/outputs/README.md) |
| [`RUN-0013`](2026/RUN-0013/metadata.yaml) | 2026-07-24 | task-1076-vks-artifacts-bpmsoft | [`outputs/README.md`](2026/RUN-0013/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0013/outputs/final-artifact.md) |

## Валидация

Контракт проверяется локально и в CI:

```bash
python3 scripts/validate_issue_123_runs_contract.py
```
