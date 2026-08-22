---
status: draft
version: 0.4
updated: 2026-08-21
ai-generated: true
type: registry
scope: runs
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/271"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/293"
related_artifacts:
  - "standards/runs-contract-standard.md"
  - "docs/analysis/2026-08-21-runs-type-gap-analysis.md"
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
| `run_type` | да (кроме записей до issue #293) | Тип прогона: `execution`, `statistics` или `legacy`. Если поле отсутствует, запись читается как `execution`. |

Дополнительные поля разрешены: `source_paths`, `inputs`, `outputs`, `logs`,
`feedback`, `metrics`, `related_issues`, `related_artifacts`, `related_runs`.

`metrics` — блок измеримых показателей прогона (введён
[issue #271](https://github.com/G-Ivan-A/mango_ba_prompts/issues/271), который
требует фиксировать токены, длительность, `eval`/вердикт и `success_rate`).
Заполняется, когда прогон фиксируется как эмпирические данные; при указании
токенов MUST указываться `token_method`, а при `success_rate` —
`success_rate_basis` (на чём посчитана доля). Пример —
[`2026/RUN-0018/metadata.yaml`](2026/RUN-0018/metadata.yaml).

## Типы прогонов

| `run_type` | Зачем прогон | Что кладём в `outputs/` | По чему судим об успехе | Пример |
| --- | --- | --- | --- | --- |
| `execution` | Получить рабочий артефакт. | ФТ, ТЗ, User Story, матрица UC, документ. | Качество артефакта и acceptance criteria. | [`RUN-0012`](2026/RUN-0012/metadata.yaml) — ФТ по BCREQ-1069. |
| `statistics` | Накопить данные о применении промптов и о коммуникации «пользователь ↔ ИИ». | Замеры, классификации, A/B-сравнения, таксономии. | Значимость выборки, покрытие типов запросов, выявленные паттерны. | [`RUN-0009`](2026/RUN-0009/metadata.yaml) — A/B применения отраслевых стандартов. |
| `legacy` | Запись, тип которой не восстанавливается. | — | Не участвует в статистической выборке. | — |

### Как выбрать тип

Тип берётся из **формулировки цели в постановке задачи** (issue), а не из состава
файлов прогона:

| Формулировка цели | Тип |
| --- | --- |
| «Зафиксировать прогон», «собрать эмпирические данные», «накопить статистику для анализа» | `statistics` |
| «Выполнить процесс», «сформировать ФТ/ТЗ/документ», «получить артефакт» | `execution` |

Наличие ФТ или матрицы UC в `outputs/` не делает прогон `execution` — в
статистическом прогоне артефакт является следствием успешной коммуникации, а не
целью задачи. Полный критерий и разбор пограничных случаев —
[`standards/runs-contract-standard.md`](../standards/runs-contract-standard.md#критерий-выбора-типа-прогона).

Метрики двух типов не смешиваются: выборка для решения о промптах собирается из
прогонов одного `run_type`. Если из прогона-исполнения извлекаются данные для
статистики, они фиксируются отдельным прогоном с `run_type: statistics` и
ссылкой `related_runs`.

## Границы прогона

Прогоны **не инициируют** изменения рабочих артефактов:

- прогон создаёт файлы только внутри `runs/YYYY/RUN-XXXX/`;
- прогон не изменяет `prompts/`, `kb/`, `site/data/`, `patterns/`;
- ссылки на промпты и стандарты допустимы только как трассировка в
  `related_artifacts`;
- изменения промптов, стандартов и веб-каталога инициирует Пользователь
  отдельными задачами на основе накопленной статистики.

## Назначение подкаталогов

| Подкаталог | Что хранится |
| --- | --- |
| `inputs/` | Сырой вход, выдержки БЗ, исходные данные, которые можно хранить в репозитории. |
| `outputs/` | Итоговые и промежуточные артефакты выполнения процесса. |
| `feedback/` | Комментарии ревью, обратная связь, решения по результату. |
| `logs/` | Логи эксперимента, метрики, трассировка выполнения, технические журналы. |

Если подкаталог пока пустой, он сохраняется через `.gitkeep`, чтобы структура
каждого run была одинаковой.

## Реестр записей

`RUN-0001`–`RUN-0012` перенесены в рамках Phase 0 (issue #123); последующие записи
создаются сразу по контракту.

| Run | Дата | `run_type` | Процесс | Основной результат |
| --- | --- | --- | --- | --- |
| [`RUN-0001`](2026/RUN-0001/metadata.yaml) | 2026-05-26 | `execution` | prompt-experiment | [`tz-stats-prototype-2026-05.md`](2026/RUN-0001/outputs/tz-stats-prototype-2026-05.md) |
| [`RUN-0002`](2026/RUN-0002/metadata.yaml) | 2026-05-26 | `execution` | user-story-generation | [`user-story_gen-from-raw-request_2026-05-26.md`](2026/RUN-0002/outputs/user-story_gen-from-raw-request_2026-05-26.md) |
| [`RUN-0003`](2026/RUN-0003/metadata.yaml) | 2026-05-26 | `execution` | usecase-generation | [`usecase_gen-stepwise-alignment_2026-05-26.md`](2026/RUN-0003/outputs/usecase_gen-stepwise-alignment_2026-05-26.md) |
| [`RUN-0004`](2026/RUN-0004/metadata.yaml) | 2026-05-26 | `statistics` | prompt-audit | [`prompts-audit-2026-05-26.md`](2026/RUN-0004/outputs/prompts-audit-2026-05-26.md) |
| [`RUN-0005`](2026/RUN-0005/metadata.yaml) | 2026-05-26 | `statistics` | prompt-selftest | [`prompts-selftest-2026-05-26.md`](2026/RUN-0005/outputs/prompts-selftest-2026-05-26.md) |
| [`RUN-0006`](2026/RUN-0006/metadata.yaml) | 2026-06-13 | `execution` | session-debug-documentation | [`session-debug-summarizer-2026-06-13.md`](2026/RUN-0006/outputs/session-debug-summarizer-2026-06-13.md) |
| [`RUN-0007`](2026/RUN-0007/metadata.yaml) | 2026-06-16 | `execution` | fr-generation | [`fr-generation-1027-live_2026-06-16.md`](2026/RUN-0007/outputs/fr-generation-1027-live_2026-06-16.md) |
| [`RUN-0008`](2026/RUN-0008/metadata.yaml) | 2026-06-16 | `statistics` | kb-citation-check | [`kb-citation-check-2026-06-16.md`](2026/RUN-0008/outputs/kb-citation-check-2026-06-16.md) |
| [`RUN-0009`](2026/RUN-0009/metadata.yaml) | 2026-06-16 | `statistics` | industry-standards-ab-check | [`standards-applied-ab-2026-06-16.md`](2026/RUN-0009/outputs/standards-applied-ab-2026-06-16.md) |
| [`RUN-0010`](2026/RUN-0010/metadata.yaml) | 2026-06-17 | `statistics` | bcreq-1025-email-routing | [`2026-06-17-bcreq-1025-email-routing.md`](2026/RUN-0010/outputs/2026-06-17-bcreq-1025-email-routing.md), [`analysis-bcreq-1025-2026-06-17.md`](2026/RUN-0010/outputs/analysis-bcreq-1025-2026-06-17.md) |
| [`RUN-0011`](2026/RUN-0011/metadata.yaml) | 2026-06-18 | `execution` | multichannel-agent-workload | [`outputs/README.md`](2026/RUN-0011/outputs/README.md), [`logs/experiment-log.md`](2026/RUN-0011/logs/experiment-log.md) |
| [`RUN-0012`](2026/RUN-0012/metadata.yaml) | 2026-07-14 | `execution` | bcreq-1069-restricted-api-key | [`outputs/final-artifact.md`](2026/RUN-0012/outputs/final-artifact.md), [`outputs/README.md`](2026/RUN-0012/outputs/README.md) |
| [`RUN-0013`](2026/RUN-0013/metadata.yaml) | 2026-07-31 | `statistics` | bcreq-1059-multichannel-slots-limits | [`outputs/final-artifact.md`](2026/RUN-0013/outputs/final-artifact.md), [`outputs/README.md`](2026/RUN-0013/outputs/README.md) |
| [`RUN-0014`](2026/RUN-0014/metadata.yaml) | 2026-07-24 | `statistics` | task-1075-amocrm-deal-on-call | [`outputs/README.md`](2026/RUN-0014/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0014/outputs/final-artifact.md), [`feedback/ba-review.md`](2026/RUN-0014/feedback/ba-review.md) |
| [`RUN-0015`](2026/RUN-0015/metadata.yaml) | 2026-08-21 | `statistics` | fr-validation-57204-ivr-scheme-amocrm-rule | [`outputs/README.md`](2026/RUN-0015/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0015/outputs/quality-findings.md), [`outputs/final-artifact.md`](2026/RUN-0015/outputs/final-artifact.md), [`logs/metrics.md`](2026/RUN-0015/logs/metrics.md) |
| [`RUN-0017`](2026/RUN-0017/metadata.yaml) | 2026-07-24 | `statistics` | task-1076-vks-artifacts-bpmsoft | [`outputs/README.md`](2026/RUN-0017/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0017/outputs/final-artifact.md) |
| [`RUN-0018`](2026/RUN-0018/metadata.yaml) | 2026-07-21 | `statistics` | fr-validation-1079-messenger-id-search | [`outputs/README.md`](2026/RUN-0018/outputs/README.md), [`feedback/review-notes.md`](2026/RUN-0018/feedback/review-notes.md), [`logs/metrics.md`](2026/RUN-0018/logs/metrics.md) |
| [`RUN-0020`](2026/RUN-0020/metadata.yaml) | 2026-07-10 | `statistics` | task-1065-context-and-questions-a7a | [`outputs/README.md`](2026/RUN-0020/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0020/outputs/quality-findings.md), [`outputs/final-artifact.md`](2026/RUN-0020/outputs/final-artifact.md) |
| [`RUN-0021`](2026/RUN-0021/metadata.yaml) | 2026-07-10 | `statistics` | fr-drafting-975-ineffective-call-parameters | [`outputs/README.md`](2026/RUN-0021/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0021/outputs/final-artifact.md), [`feedback/review-notes.md`](2026/RUN-0021/feedback/review-notes.md), [`logs/metrics.md`](2026/RUN-0021/logs/metrics.md) |
| [`RUN-0022`](2026/RUN-0022/metadata.yaml) | 2026-08-21 | `statistics` | fr-validation-765-headhunter-channel | [`outputs/README.md`](2026/RUN-0022/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0022/outputs/quality-findings.md), [`logs/metrics.md`](2026/RUN-0022/logs/metrics.md) |
| [`RUN-0023`](2026/RUN-0023/metadata.yaml) | 2026-05-25 | `statistics` | task-59295-fr-validation-email-forward | [`outputs/README.md`](2026/RUN-0023/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0023/outputs/quality-findings.md), [`outputs/final-artifact.md`](2026/RUN-0023/outputs/final-artifact.md) |
| [`RUN-0024`](2026/RUN-0024/metadata.yaml) | 2026-05-25 | `statistics` | task-1020-okdesk-mango-integration-questions | [`outputs/README.md`](2026/RUN-0024/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0024/outputs/quality-findings.md), [`logs/grounding-check.md`](2026/RUN-0024/logs/grounding-check.md) |
| [`RUN-0025`](2026/RUN-0025/metadata.yaml) | 2026-05-12 | `statistics` | fr-validation-997-ivr-scheme-incoming-call-rules | [`outputs/README.md`](2026/RUN-0025/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0025/outputs/final-artifact.md), [`feedback/review-notes.md`](2026/RUN-0025/feedback/review-notes.md), [`logs/metrics.md`](2026/RUN-0025/logs/metrics.md) |
| [`RUN-0026`](2026/RUN-0026/metadata.yaml) | 2026-05-04 | `statistics` | task-1007-amocrm-outbound-campaign-funnel-stage-fr | [`outputs/README.md`](2026/RUN-0026/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0026/outputs/quality-findings.md), [`logs/grounding-check.md`](2026/RUN-0026/logs/grounding-check.md) |
| [`RUN-0027`](2026/RUN-0027/metadata.yaml) | 2026-04-10 | `statistics` | fr-analysis-978-email-signature-in-lk | [`outputs/README.md`](2026/RUN-0027/outputs/README.md), [`outputs/final-artifact.md`](2026/RUN-0027/outputs/final-artifact.md), [`feedback/review-notes.md`](2026/RUN-0027/feedback/review-notes.md), [`logs/grounding-check.md`](2026/RUN-0027/logs/grounding-check.md) |
| [`RUN-0028`](2026/RUN-0028/metadata.yaml) | 2026-07-01 | `statistics` | fr-validation-1040-speech-analytics-direction-filter | [`outputs/README.md`](2026/RUN-0028/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0028/outputs/quality-findings.md), [`feedback/review-notes.md`](2026/RUN-0028/feedback/review-notes.md) |
| [`RUN-0029`](2026/RUN-0029/metadata.yaml) | 2026-08-21 | `statistics` | fr-drafting-58093-amocrm-deal-card-new-tab | [`outputs/README.md`](2026/RUN-0029/outputs/README.md), [`outputs/quality-findings.md`](2026/RUN-0029/outputs/quality-findings.md), [`logs/metrics.md`](2026/RUN-0029/logs/metrics.md) |

## Локальные инструменты воспроизводимости

Часть входов прогона (например, экспорт истории чата в JSON) не читается глазами
и разворачивается в markdown скриптом. Такие конвертеры — **локальные
инструменты воспроизводимости, а не рабочие артефакты прогона**:

| Инструмент | Назначение |
| --- | --- |
| [`scripts/chat_export_to_markdown.py`](../scripts/chat_export_to_markdown.py) | Разворачивает экспорт чата (JSON) в линейный транскрипт и таблицу метрик по репликам. Используется в [`RUN-0015`](2026/RUN-0015/inputs/README.md), [`RUN-0017`](2026/RUN-0017/inputs/README.md), [`RUN-0020`](2026/RUN-0020/inputs/README.md), [`RUN-0021`](2026/RUN-0021/inputs/README.md), [`RUN-0022`](2026/RUN-0022/inputs/README.md), [`RUN-0023`](2026/RUN-0023/inputs/README.md), [`RUN-0024`](2026/RUN-0024/inputs/README.md), [`RUN-0025`](2026/RUN-0025/inputs/README.md), [`RUN-0026`](2026/RUN-0026/inputs/README.md), [`RUN-0027`](2026/RUN-0027/inputs/README.md) [`RUN-0028`](2026/RUN-0028/inputs/README.md) и [`RUN-0029`](2026/RUN-0029/inputs/README.md). |
| [`experiments/chat_export_probe.py`](../experiments/chat_export_probe.py) | Разведочный скрипт: печатает структуру незнакомого экспорта чата перед конвертацией. |
| [`experiments/parse_qwen_chat_export.py`](../experiments/parse_qwen_chat_export.py) | Считает токены (`tiktoken:cl100k_base`), длительности и метрики по эпизодам из выгрузки чата Qwen. Используется в [`RUN-0018`](2026/RUN-0018/logs/metrics.md) и [`RUN-0021`](2026/RUN-0021/logs/metrics.md). |
| [`experiments/chat_export_usage_metrics.py`](../experiments/chat_export_usage_metrics.py) | Считает токены по нативным полям `usage` провайдера (без оценки токенизатором), латентности и длительности по эпизодам. Используется в [`RUN-0028`](2026/RUN-0028/logs/metrics.md). |
| [`experiments/parse_765_chat_export.py`](../experiments/parse_765_chat_export.py) | Считает метрики по эпизодам (токены провайдера, время генерации, активное время) из выгрузки чата задачи 765. Используется в [`RUN-0022`](2026/RUN-0022/logs/metrics.md). |
| [`experiments/parse_58093_chat_export.py`](../experiments/parse_58093_chat_export.py) | Считает метрики по эпизодам (токены провайдера, время генерации, активное время) из выгрузки чата задачи 58093. Используется в [`RUN-0029`](2026/RUN-0029/logs/metrics.md). |
| [`experiments/okdesk_citation_grounding_probe.py`](../experiments/okdesk_citation_grounding_probe.py) | Извлекает результаты веб-инструмента (`content_list[*].extra.tool_result`) из экспорта чата и считает вхождения контрольных терминов — проверка заземления сносок. Используется в [`RUN-0024`](2026/RUN-0024/logs/grounding-check.md). |
| [`experiments/amocrm_widget_grounding_probe.py`](../experiments/amocrm_widget_grounding_probe.py) | Печатает нумерацию документов поисковой выдачи (`[[N]]`), метрики извлечения страниц (`extract_page_success`) и вхождения контрольных терминов из экспорта чата — проверка заземления сносок. Используется в [`RUN-0026`](2026/RUN-0026/logs/grounding-check.md). |
| [`experiments/signature_citation_grounding_probe.py`](../experiments/signature_citation_grounding_probe.py) | Проверяет заземление сносок валидации НФТ на реально полученную выдачу веб-инструмента (`web_search`, `web_extractor`) из экспорта чата задачи 978. Используется в [`RUN-0027`](2026/RUN-0027/logs/grounding-check.md). |

Правила обращения с ними:

- запускаются **вручную**, локально, командой вида
  `python3 scripts/chat_export_to_markdown.py <export.json> ...`;
- **не** вызываются из GitHub Actions и не входят в CI, поэтому остаются
  работоспособными при отключённых Actions (в том числе в приватном репозитории);
- требуют только стандартной библиотеки Python 3 — внешних зависимостей нет;
- по статусу аналогичны [`scripts/sync_from_hub.py`](../scripts/sync_from_hub.py)
  и [`scripts/generate-pages-data.mjs`](../scripts/generate-pages-data.mjs):
  инструменты для работы с репозиторием, а не содержимое прогона;
- границы прогона не нарушают: ничего не пишут в `prompts/`, `kb/`, `patterns/`
  и `site/data/`, вывод кладут только внутрь `runs/YYYY/RUN-XXXX/`.

## Валидация

Контракт проверяется локально и в CI:

```bash
python3 scripts/validate_issue_123_runs_contract.py
```
