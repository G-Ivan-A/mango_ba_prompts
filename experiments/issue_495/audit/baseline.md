# Аудит чистоты: базовая линия (до исправлений, HEAD e051e0fa)

```
Файлов в контуре: 151; нарушений: 4895
  (a) приватные/незакреплённые ссылки: 2357
  (b) кейс-специфика: 389
  (c) неисполнимый балласт: 2149
По правилам:
  a A-PRIVATE: 1655
  a A-RELATIVE: 702
  b CT-01: 90
  b CT-02: 84
  b CT-03: 25
  b CT-04: 36
  b CT-05: 31
  b CT-06: 3
  b CT-09: 120
  c BP-01: 555
  c BP-02: 355
  c BP-03: 79
  c BP-04: 355
  c BP-06: 303
  c BP-07: 42
  c BP-08: 180
  c BP-09: 180
  c BP-10: 84
  c BP-11: 6
  c BP-12: 10
По файлам (a/b/c):
  docs/ba-processes/bcreq-a-in-common.md: 5/2/0
  docs/ba-processes/bcreq-a-in-instructions.json: 0/5/0
  docs/ba-processes/bcreq-a-in-route.json: 1/2/0
  docs/ba-processes/bcreq-evidence-normalization.md: 0/2/0
  docs/ba-processes/bcreq-step-handoff.md: 1/2/0
  prompts/AI_SESSION_HANDOVER_PROMPT.executable.md: 2/0/0
  prompts/README.executable.md: 1/0/0
  prompts/README.md: 101/0/0
  prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md: 12/0/30
  prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md: 9/0/2
  prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md: 10/2/30
  prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md: 14/15/31
  prompts/archive/a-in-v2.7.0/manifest.json: 1/0/0
  prompts/archive/constraints-documentation-oneshot.md: 1/0/2
  prompts/archive/constraints-documentation-stepwise.md: 1/0/2
  prompts/archive/fr-documentation-oneshot.md: 1/0/2
  prompts/archive/fr-documentation-stepwise.md: 1/0/2
  prompts/archive/fr-validation-legacy.md: 1/0/2
  prompts/archive/fr-validation-oneshot.md: 1/0/2
  prompts/archive/fr-validation-stepwise.md: 1/0/2
  prompts/archive/glossary-context-understanding-oneshot.md: 1/0/2
  prompts/archive/glossary-context-understanding-stepwise.md: 1/0/2
  prompts/archive/questions-customer-understanding-legacy.md: 1/0/2
  prompts/archive/questions-customer-understanding-stepwise.md: 1/0/2
  prompts/archive/technical-details-solution-design-legacy.md: 1/0/2
  prompts/archive/technical-details-solution-design-oneshot.md: 1/0/2
  prompts/archive/technical-details-solution-design-stepwise.md: 1/0/2
  prompts/archive/tz-stats-generator-simple-legacy.md: 0/0/1
  prompts/archive/uc-modeling-oneshot.md: 1/0/2
  prompts/archive/uc-modeling-stepwise.md: 1/0/2
  prompts/archive/us-modeling-oneshot.md: 1/0/2
  prompts/archive/us-modeling-stepwise.md: 1/0/2
  prompts/archive/usecase-stepwise-generator-simple-legacy.md: 0/0/1
  prompts/archive/user-story-generator-simple-legacy.md: 0/0/1
  prompts/asr-ingestion-oneshot.md: 0/5/0
  prompts/bcreq-constitution-governance-oneshot.md: 31/5/15
  prompts/bcreq-constraints-documentation-stepwise.md: 3/0/2
  prompts/bcreq-context-understanding-stepwise.md: 6/2/4
  prompts/bcreq-core-documentation-oneshot.md: 8/2/4
  prompts/bcreq-extra-risk-analysis-stepwise.md: 3/0/2
  prompts/bcreq-fr-documentation-stepwise.md: 5/2/4
  prompts/bcreq-in-understanding-oneshot.md: 10/2/4
  prompts/bcreq-nfr-documentation-stepwise.md: 3/0/2
  prompts/bcreq-orr-solution-design-stepwise.md: 5/0/2
  prompts/bcreq-products-impact-analysis-stepwise.md: 7/17/4
  prompts/bcreq-review-validation-oneshot.md: 4/0/2
  prompts/bcreq-scenarios-modeling-oneshot.md: 4/0/2
  prompts/bcreq-uc-modeling-stepwise.md: 3/0/2
  prompts/bcreq-work-solution-design-oneshot.md: 11/0/2
  prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md: 6/8/10
  prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md: 6/4/10
  prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md: 6/2/10
  prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md: 6/2/10
  prompts/drafts/bcreq-constitution-governance-oneshot.md: 37/5/49
  prompts/drafts/bcreq-constraints-documentation-stepwise.md: 10/0/33
  prompts/drafts/bcreq-context-understanding-stepwise.md: 13/2/35
  prompts/drafts/bcreq-extra-risk-analysis-stepwise.md: 10/0/33
  prompts/drafts/bcreq-fr-documentation-stepwise.md: 12/2/38
  prompts/drafts/bcreq-intake-questionnaire-stepwise.md: 11/4/35
  prompts/drafts/bcreq-nfr-documentation-stepwise.md: 10/0/34
  prompts/drafts/bcreq-orr-solution-design-stepwise.md: 12/0/33
  prompts/drafts/bcreq-products-impact-analysis-stepwise.md: 15/17/36
  prompts/drafts/bcreq-release-readiness-oneshot.md: 9/0/36
  prompts/drafts/bcreq-review-validation-oneshot.md: 11/0/30
  prompts/drafts/bcreq-scenarios-modeling-oneshot.md: 11/0/31
  prompts/drafts/bcreq-uc-modeling-stepwise.md: 11/0/35
  prompts/drafts/manifest.json: 1/0/0
  prompts/drafts/system/bcreq-context-understanding-system.md: 13/2/39
  prompts/drafts/system/bcreq-intake-questionnaire-system.md: 11/4/39
  prompts/drafts/system/bcreq-products-impact-analysis-system.md: 15/17/40
  prompts/session-debug-documentation-oneshot.md: 7/0/2
  site/data/a-in-kit.json: 144/58/240
  site/data/bcreq-flow.json: 43/0/0
  site/data/checks.json: 2/0/0
  site/data/patterns.json: 16/0/0
  site/data/process-tree.json: 42/0/0
  site/data/processes.json: 48/0/0
  site/data/prompts.json: 924/97/297
  site/data/roadmap.json: 1/0/0
  site/data/stats.json: 8/0/0
  site/data/step-handoff.json: 1/3/0
  site/data/test-kit.json: 253/56/611
  standards/bcreq-manual-classes/01-intake.md: 6/1/0
  standards/bcreq-manual-classes/02-normalize.md: 6/0/0
  standards/bcreq-manual-classes/03-ambiguity.md: 6/0/0
  standards/bcreq-manual-classes/04-questions.md: 6/0/0
  standards/bcreq-manual-classes/05-taxonomy.md: 6/0/0
  standards/bcreq-manual-classes/06-scope.md: 6/0/0
  standards/bcreq-manual-classes/07-web-evidence.md: 6/0/0
  standards/bcreq-manual-classes/08-document-evidence.md: 6/0/0
  standards/bcreq-manual-classes/09-ba-enrichment.md: 6/0/0
  standards/bcreq-manual-classes/10-source-conflicts.md: 6/0/0
  standards/bcreq-manual-classes/11-dependency-check.md: 6/0/0
  standards/bcreq-manual-classes/12-phase-assembly.md: 6/0/0
  standards/bcreq-manual-classes/13-handoff-check.md: 6/0/0
  standards/bcreq-manual-classes/14-glossary.md: 6/0/0
  standards/bcreq-manual-classes/15-business-context.md: 6/0/0
  standards/bcreq-manual-classes/16-fr-delta.md: 6/0/0
  standards/bcreq-manual-classes/17-fr-new.md: 6/0/0
  standards/bcreq-manual-classes/18-nfr.md: 6/0/0
  standards/bcreq-manual-classes/19-uc-coverage.md: 6/0/0
  standards/bcreq-manual-classes/20-gate-evidence.md: 6/0/0
  standards/bcreq-manual-classes/21-solution-l1.md: 6/0/0
  standards/bcreq-manual-classes/22-solution-l2.md: 6/0/0
  standards/bcreq-manual-classes/23-constraints.md: 6/0/0
  standards/bcreq-manual-classes/24-uc-boundaries.md: 6/0/0
  standards/bcreq-manual-classes/25-risks.md: 6/0/0
  standards/bcreq-manual-classes/26-delivery-dependencies.md: 6/0/0
  standards/bcreq-manual-classes/27-acceptance.md: 6/0/0
  standards/bcreq-manual-classes/28-independent-review.md: 6/0/0
  standards/bcreq-manual-classes/29-impact.md: 6/0/0
  standards/bcreq-manual-classes/30-targeted-edit.md: 6/0/0
  standards/bcreq-manual-classes/31-conformance.md: 6/0/0
  standards/bcreq-manual-classes/32-audience-projection.md: 6/0/0
  standards/bcreq-manual-classes/33-release-audit.md: 6/0/0
  standards/bcreq-manual-classes/34-human-record.md: 6/0/0
  standards/bcreq-manual-classes/35-baseline-handover.md: 6/0/0
  standards/bcreq-manual-classes/36-rule-bundle.md: 6/0/0
  standards/bcreq-manual-classes/37-user-story.md: 6/0/0
  standards/bcreq-manual-classes/38-requested-uc.md: 6/0/0
  standards/bcreq-manual-classes/39-manifest-alignment.md: 6/0/0
```

| ID | Класс | Правило | Локатор | Совпадение | Фрагмент |
| --- | --- | --- | --- | --- | --- |
| V-0001 | b | CT-01 | `prompts/asr-ingestion-oneshot.md:28` | `amoCRM` | "амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python"). |
| V-0002 | b | CT-04 | `prompts/asr-ingestion-oneshot.md:28` | `ВАТС` | "амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python"). |
| V-0003 | b | CT-01 | `prompts/asr-ingestion-oneshot.md:52` | `amoCRM` | \| 7 \| "амо" \| amoCRM \| "интеграция с амо" \| |
| V-0004 | b | CT-01 | `prompts/asr-ingestion-oneshot.md:56` | `amoCRM` | - "амо" → "amoCRM" |
| V-0005 | b | CT-04 | `prompts/asr-ingestion-oneshot.md:57` | `ВАТС` | - "вакс" → "ВАТС" |
| V-0006 | c | BP-01 | `prompts/bcreq-constitution-governance-oneshot.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0007 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0008 | b | CT-01 | `prompts/bcreq-constitution-governance-oneshot.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0009 | b | CT-02 | `prompts/bcreq-constitution-governance-oneshot.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0010 | c | BP-01 | `prompts/bcreq-constitution-governance-oneshot.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0011 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:99` | `mango_ba_prompts` | - [Мета-стандарты разделов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md) |
| V-0012 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:100` | `mango_ba_prompts` | - [Архитектура промптов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md) |
| V-0013 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:101` | `mango_ba_prompts` | - [Контракт стадий и гейтов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md) |
| V-0014 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:102` | `mango_ba_prompts` | - [Стандарт композиции продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md) |
| V-0015 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:120` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай: |
| V-0016 | b | CT-04 | `prompts/bcreq-constitution-governance-oneshot.md:124` | `ВАТС` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-0017 | b | CT-05 | `prompts/bcreq-constitution-governance-oneshot.md:124` | `ЛК` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-0018 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:132` | `mango_ba_prompts` | [стандарте композиции §4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-0019 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:157` | `mango_ba_prompts` | 6. Попроси ввести следующий промпт — [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) |
| V-0020 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:180` | `mango_ba_prompts` | [standards/bcreq-sections]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов). |
| V-0021 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:200` | `mango_ba_prompts` | [README §2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили). |
| V-0022 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:227` | `mango_ba_prompts` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0023 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:227` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0024 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:227` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0025 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:229` | `mango_ba_prompts` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-0026 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:229` | `RUN-0` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-0027 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:231` | `mango_ba_prompts` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-0028 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:231` | `RUN-0` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-0029 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:233` | `RUN-0` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-0030 | c | BP-12 | `prompts/bcreq-constitution-governance-oneshot.md:233` | `Категория RUN` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-0031 | c | BP-02 | `prompts/bcreq-constitution-governance-oneshot.md:243` | `#391` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0032 | c | BP-03 | `prompts/bcreq-constitution-governance-oneshot.md:243` | `issue` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0033 | c | BP-12 | `prompts/bcreq-constitution-governance-oneshot.md:243` | `ревизии Golden` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0034 | b | CT-03 | `prompts/bcreq-constitution-governance-oneshot.md:250` | `коннекторе` | …; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает… |
| V-0035 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:265` | `RUN-0` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-0036 | c | BP-04 | `prompts/bcreq-constitution-governance-oneshot.md:265` | `SC-6` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-0037 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:286` | `mango_ba_prompts` | …-intake-questionnaire-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) \|… |
| V-0038 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:287` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) \|… |
| V-0039 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:288` | `mango_ba_prompts` | …ducts-impact-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \|… |
| V-0040 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:289` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \|… |
| V-0041 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:290` | `mango_ba_prompts` | …req-nfr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-0042 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:291` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-0043 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:292` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \|… |
| V-0044 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:293` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-0045 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:294` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-0046 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:295` | `mango_ba_prompts` | …q-extra-risk-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-0047 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:296` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-0048 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:297` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \|… |
| V-0049 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:304` | `mango_ba_prompts` | [A-IN]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) (Ш-А, Ш-1, Ш-2) → |
| V-0050 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:306` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) (Ш-3…Ш-5) → |
| V-0051 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:308` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) (Ш-6…Ш-9) → |
| V-0052 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:323` | `mango_ba_prompts` | [контракта гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#3-возвраты)). |
| V-0053 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:327` | `mango_ba_prompts` | [поток CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-0054 | c | BP-01 | `prompts/bcreq-constitution-governance-oneshot.md:375` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0055 | a | A-PRIVATE | `prompts/bcreq-constitution-governance-oneshot.md:386` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0056 | c | BP-01 | `prompts/bcreq-constitution-governance-oneshot.md:479` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0057 | a | A-PRIVATE | `prompts/bcreq-constraints-documentation-stepwise.md:18` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0058 | a | A-PRIVATE | `prompts/bcreq-constraints-documentation-stepwise.md:67` | `mango_ba_prompts` | [Мета-стандарт раздела 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md). |
| V-0059 | c | BP-01 | `prompts/bcreq-constraints-documentation-stepwise.md:110` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0060 | a | A-PRIVATE | `prompts/bcreq-constraints-documentation-stepwise.md:121` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0061 | c | BP-01 | `prompts/bcreq-constraints-documentation-stepwise.md:214` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0062 | c | BP-01 | `prompts/bcreq-context-understanding-stepwise.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0063 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0064 | b | CT-01 | `prompts/bcreq-context-understanding-stepwise.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0065 | b | CT-02 | `prompts/bcreq-context-understanding-stepwise.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0066 | c | BP-01 | `prompts/bcreq-context-understanding-stepwise.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0067 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:94` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0068 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:178` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-0069 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:210` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-0070 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:215` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-0071 | c | BP-01 | `prompts/bcreq-context-understanding-stepwise.md:307` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0072 | a | A-PRIVATE | `prompts/bcreq-context-understanding-stepwise.md:318` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0073 | c | BP-01 | `prompts/bcreq-context-understanding-stepwise.md:411` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0074 | c | BP-01 | `prompts/bcreq-core-documentation-oneshot.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0075 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0076 | b | CT-01 | `prompts/bcreq-core-documentation-oneshot.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0077 | b | CT-02 | `prompts/bcreq-core-documentation-oneshot.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0078 | c | BP-01 | `prompts/bcreq-core-documentation-oneshot.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0079 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:97` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0080 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:109` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md). |
| V-0081 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:150` | `mango_ba_prompts` | [Раздел 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md); |
| V-0082 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:151` | `mango_ba_prompts` | [раздел 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md); |
| V-0083 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:152` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-0084 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:153` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-0085 | c | BP-01 | `prompts/bcreq-core-documentation-oneshot.md:208` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0086 | a | A-PRIVATE | `prompts/bcreq-core-documentation-oneshot.md:219` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0087 | c | BP-01 | `prompts/bcreq-core-documentation-oneshot.md:312` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0088 | a | A-PRIVATE | `prompts/bcreq-extra-risk-analysis-stepwise.md:18` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0089 | a | A-PRIVATE | `prompts/bcreq-extra-risk-analysis-stepwise.md:65` | `mango_ba_prompts` | [Мета-стандарт раздела 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md). |
| V-0090 | c | BP-01 | `prompts/bcreq-extra-risk-analysis-stepwise.md:110` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0091 | a | A-PRIVATE | `prompts/bcreq-extra-risk-analysis-stepwise.md:121` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0092 | c | BP-01 | `prompts/bcreq-extra-risk-analysis-stepwise.md:214` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0093 | c | BP-01 | `prompts/bcreq-fr-documentation-stepwise.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0094 | a | A-PRIVATE | `prompts/bcreq-fr-documentation-stepwise.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0095 | b | CT-01 | `prompts/bcreq-fr-documentation-stepwise.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0096 | b | CT-02 | `prompts/bcreq-fr-documentation-stepwise.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0097 | c | BP-01 | `prompts/bcreq-fr-documentation-stepwise.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0098 | a | A-PRIVATE | `prompts/bcreq-fr-documentation-stepwise.md:94` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0099 | a | A-PRIVATE | `prompts/bcreq-fr-documentation-stepwise.md:167` | `mango_ba_prompts` | [Мета-стандарт раздела 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md). |
| V-0100 | a | A-PRIVATE | `prompts/bcreq-fr-documentation-stepwise.md:175` | `mango_ba_prompts` | …BABOK — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-babok-guide-v3-что-берём… |
| V-0101 | c | BP-01 | `prompts/bcreq-fr-documentation-stepwise.md:238` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0102 | a | A-PRIVATE | `prompts/bcreq-fr-documentation-stepwise.md:249` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0103 | c | BP-01 | `prompts/bcreq-fr-documentation-stepwise.md:342` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0104 | c | BP-01 | `prompts/bcreq-in-understanding-oneshot.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0105 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0106 | b | CT-01 | `prompts/bcreq-in-understanding-oneshot.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0107 | b | CT-02 | `prompts/bcreq-in-understanding-oneshot.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0108 | c | BP-01 | `prompts/bcreq-in-understanding-oneshot.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0109 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:97` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0110 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:105` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-0111 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:162` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-0112 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:163` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-0113 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:164` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-0114 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:165` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-0115 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:180` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-0116 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:182` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-0117 | c | BP-01 | `prompts/bcreq-in-understanding-oneshot.md:237` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0118 | a | A-PRIVATE | `prompts/bcreq-in-understanding-oneshot.md:248` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0119 | c | BP-01 | `prompts/bcreq-in-understanding-oneshot.md:341` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0120 | a | A-PRIVATE | `prompts/bcreq-nfr-documentation-stepwise.md:18` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0121 | a | A-PRIVATE | `prompts/bcreq-nfr-documentation-stepwise.md:65` | `mango_ba_prompts` | [Мета-стандарт раздела 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md). |
| V-0122 | c | BP-01 | `prompts/bcreq-nfr-documentation-stepwise.md:109` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0123 | a | A-PRIVATE | `prompts/bcreq-nfr-documentation-stepwise.md:120` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0124 | c | BP-01 | `prompts/bcreq-nfr-documentation-stepwise.md:213` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0125 | a | A-PRIVATE | `prompts/bcreq-orr-solution-design-stepwise.md:20` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0126 | a | A-PRIVATE | `prompts/bcreq-orr-solution-design-stepwise.md:97` | `mango_ba_prompts` | [Мета-стандарт раздела 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-0127 | a | A-PRIVATE | `prompts/bcreq-orr-solution-design-stepwise.md:98` | `mango_ba_prompts` | [правила композиции]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции). |
| V-0128 | a | A-PRIVATE | `prompts/bcreq-orr-solution-design-stepwise.md:107` | `mango_ba_prompts` | …ктуры — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-… |
| V-0129 | c | BP-01 | `prompts/bcreq-orr-solution-design-stepwise.md:185` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0130 | a | A-PRIVATE | `prompts/bcreq-orr-solution-design-stepwise.md:196` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0131 | c | BP-01 | `prompts/bcreq-orr-solution-design-stepwise.md:289` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0132 | c | BP-01 | `prompts/bcreq-products-impact-analysis-stepwise.md:12` | `<!--` | <!-- issue-474:entry --> |
| V-0133 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:23` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0134 | b | CT-01 | `prompts/bcreq-products-impact-analysis-stepwise.md:63` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0135 | b | CT-02 | `prompts/bcreq-products-impact-analysis-stepwise.md:63` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0136 | c | BP-01 | `prompts/bcreq-products-impact-analysis-stepwise.md:85` | `<!--` | <!-- /issue-474:entry --> |
| V-0137 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:94` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0138 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:113` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-0139 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:114` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-0140 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:140` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-0141 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:140` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-0142 | b | CT-04 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0143 | b | CT-05 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0144 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0145 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0146 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0147 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0148 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:141` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0149 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:142` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0150 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:142` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0151 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:142` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0152 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:142` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0153 | b | CT-09 | `prompts/bcreq-products-impact-analysis-stepwise.md:142` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0154 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:156` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-0155 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:159` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-0156 | b | CT-03 | `prompts/bcreq-products-impact-analysis-stepwise.md:177` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-0157 | c | BP-01 | `prompts/bcreq-products-impact-analysis-stepwise.md:225` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0158 | a | A-PRIVATE | `prompts/bcreq-products-impact-analysis-stepwise.md:236` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0159 | c | BP-01 | `prompts/bcreq-products-impact-analysis-stepwise.md:329` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0160 | a | A-PRIVATE | `prompts/bcreq-review-validation-oneshot.md:21` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0161 | a | A-PRIVATE | `prompts/bcreq-review-validation-oneshot.md:65` | `mango_ba_prompts` | [Контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты); |
| V-0162 | a | A-PRIVATE | `prompts/bcreq-review-validation-oneshot.md:66` | `mango_ba_prompts` | [мета-стандарты разделов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0163 | c | BP-01 | `prompts/bcreq-review-validation-oneshot.md:126` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0164 | a | A-PRIVATE | `prompts/bcreq-review-validation-oneshot.md:137` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0165 | c | BP-01 | `prompts/bcreq-review-validation-oneshot.md:231` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0166 | a | A-PRIVATE | `prompts/bcreq-scenarios-modeling-oneshot.md:21` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0167 | a | A-PRIVATE | `prompts/bcreq-scenarios-modeling-oneshot.md:63` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md) |
| V-0168 | a | A-PRIVATE | `prompts/bcreq-scenarios-modeling-oneshot.md:65` | `mango_ba_prompts` | [архитектуры промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)). |
| V-0169 | c | BP-01 | `prompts/bcreq-scenarios-modeling-oneshot.md:104` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0170 | a | A-PRIVATE | `prompts/bcreq-scenarios-modeling-oneshot.md:115` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0171 | c | BP-01 | `prompts/bcreq-scenarios-modeling-oneshot.md:208` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0172 | a | A-PRIVATE | `prompts/bcreq-uc-modeling-stepwise.md:21` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0173 | a | A-PRIVATE | `prompts/bcreq-uc-modeling-stepwise.md:83` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-0174 | c | BP-01 | `prompts/bcreq-uc-modeling-stepwise.md:145` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0175 | a | A-PRIVATE | `prompts/bcreq-uc-modeling-stepwise.md:156` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0176 | c | BP-01 | `prompts/bcreq-uc-modeling-stepwise.md:249` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0177 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:21` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0178 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:34` | `mango_ba_prompts` | [Ш-В]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) |
| V-0179 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:82` | `mango_ba_prompts` | [Раздел 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-0180 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:83` | `mango_ba_prompts` | [раздел 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md); |
| V-0181 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:84` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-0182 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:85` | `mango_ba_prompts` | [раздел 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md); |
| V-0183 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:86` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции); |
| V-0184 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:87` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-0185 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:106` | `mango_ba_prompts` | [Ш-6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md#проверка-последовательности-и-контракта) |
| V-0186 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:108` | `mango_ba_prompts` | [Ш-8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md#проверка-покрытия-условий-контракта). |
| V-0187 | c | BP-01 | `prompts/bcreq-work-solution-design-oneshot.md:156` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0188 | a | A-PRIVATE | `prompts/bcreq-work-solution-design-oneshot.md:167` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0189 | c | BP-01 | `prompts/bcreq-work-solution-design-oneshot.md:260` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0190 | c | BP-03 | `prompts/session-debug-documentation-oneshot.md:52` | `Issue` | можно было вставить в Issue или скопировать как блок в |
| V-0191 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:58` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/session-digests.md> |
| V-0192 | c | BP-04 | `prompts/session-debug-documentation-oneshot.md:102` | `ADR-0` | - Стандарт промптов (ADR-001): |
| V-0193 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:103` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md> |
| V-0194 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:105` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/README.executable.md> |
| V-0195 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:107` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/session-digests.md> |
| V-0196 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:109` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md> |
| V-0197 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:111` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md> |
| V-0198 | a | A-PRIVATE | `prompts/session-debug-documentation-oneshot.md:112` | `mango_ba_prompts` | - Репозиторий: <https://github.com/G-Ivan-A/mango_ba_prompts> |
| V-0199 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0200 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0201 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0202 | c | BP-08 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0203 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0204 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко… |
| V-0205 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `#490` | …438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.… |
| V-0206 | c | BP-03 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» … |
| V-0207 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по… |
| V-0208 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0209 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0210 | c | BP-08 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);… |
| V-0211 | c | BP-09 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0212 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:21` | `<!--` | <!-- issue-474:entry --> |
| V-0213 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:24` | `#490` | …, формат шагов и исходный запрос без анализа. Формат шагов (#490) задаёт сайт строкой «Формат шагов: системный» или «Формат шагов: декомпозированный»;… |
| V-0214 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:34` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0215 | b | CT-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:74` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0216 | b | CT-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:74` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0217 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:96` | `<!--` | <!-- /issue-474:entry --> |
| V-0218 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:110` | `mango_ba_prompts` | - [Мета-стандарты разделов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md) |
| V-0219 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:111` | `mango_ba_prompts` | - [Архитектура промптов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md) |
| V-0220 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:112` | `mango_ba_prompts` | - [Контракт стадий и гейтов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md) |
| V-0221 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:113` | `mango_ba_prompts` | - [Стандарт композиции продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md) |
| V-0222 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:131` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай: |
| V-0223 | b | CT-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` | `ВАТС` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-0224 | b | CT-05 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:135` | `ЛК` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-0225 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:143` | `mango_ba_prompts` | [стандарте композиции §4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-0226 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:169` | `mango_ba_prompts` | [AIN-01]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md), в системном — |
| V-0227 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:170` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md). Остановись. |
| V-0228 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:192` | `mango_ba_prompts` | [standards/bcreq-sections]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов). |
| V-0229 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:212` | `mango_ba_prompts` | [README §2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили). |
| V-0230 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:239` | `mango_ba_prompts` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0231 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:239` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0232 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:239` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-0233 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:241` | `mango_ba_prompts` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-0234 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:241` | `RUN-0` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-0235 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:243` | `mango_ba_prompts` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-0236 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:243` | `RUN-0` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-0237 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` | `RUN-0` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-0238 | c | BP-12 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:245` | `Категория RUN` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-0239 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` | `#391` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0240 | c | BP-03 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` | `issue` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0241 | c | BP-12 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:255` | `ревизии Golden` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-0242 | b | CT-03 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:262` | `коннекторе` | …; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает… |
| V-0243 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` | `RUN-0` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-0244 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:277` | `SC-6` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-0245 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:298` | `mango_ba_prompts` | …eq-intake-questionnaire-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md) \|… |
| V-0246 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:299` | `mango_ba_prompts` | …q-context-understanding-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-context-understanding-system.md) \|… |
| V-0247 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:300` | `mango_ba_prompts` | …roducts-impact-analysis-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-products-impact-analysis-system.md)… |
| V-0248 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:301` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \|… |
| V-0249 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:302` | `mango_ba_prompts` | …req-nfr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-0250 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:303` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-0251 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:304` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \|… |
| V-0252 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:305` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-0253 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:306` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-0254 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:307` | `mango_ba_prompts` | …q-extra-risk-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-0255 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:308` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-0256 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:309` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \|… |
| V-0257 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:315` | `#490` | **Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из |
| V-0258 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:317` | `mango_ba_prompts` | [AIN-01…AIN-24]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md) |
| V-0259 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:334` | `mango_ba_prompts` | [контракта гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#3-возвраты)). |
| V-0260 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:338` | `mango_ba_prompts` | [поток CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-0261 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:386` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0262 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:397` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0263 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:490` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0264 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:492` | `<!--` | <!-- bl-156: by-test --> |
| V-0265 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:492` | `by-test` | <!-- bl-156: by-test --> |
| V-0266 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:493` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0267 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:493` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0268 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0269 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0270 | c | BP-09 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:495` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0271 | c | BP-07 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:497` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0272 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:498` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0273 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:498` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0274 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:499` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0275 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:500` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0276 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:501` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0277 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:502` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0278 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:513` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0279 | a | A-PRIVATE | `prompts/drafts/bcreq-constitution-governance-oneshot.md:555` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0280 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0281 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:558` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0282 | c | BP-04 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0283 | c | BP-10 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0284 | c | BP-10 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:581` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0285 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:642` | `<!--` | <!-- /bl-156: by-test --> |
| V-0286 | c | BP-06 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:642` | `by-test` | <!-- /bl-156: by-test --> |
| V-0287 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:644` | `<!--` | <!-- issue-490:handoff --> |
| V-0288 | c | BP-02 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:645` | `#490` | ## Итог шага для БА (#490) |
| V-0289 | c | BP-01 | `prompts/drafts/bcreq-constitution-governance-oneshot.md:666` | `<!--` | <!-- /issue-490:handoff --> |
| V-0290 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0291 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0292 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0293 | c | BP-08 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0294 | c | BP-02 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0295 | c | BP-02 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0296 | c | BP-03 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0297 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0298 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0299 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0300 | c | BP-08 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0301 | c | BP-09 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0302 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:27` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0303 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:76` | `mango_ba_prompts` | [Мета-стандарт раздела 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md). |
| V-0304 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:119` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0305 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:130` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0306 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:223` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0307 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:225` | `<!--` | <!-- bl-156: by-test --> |
| V-0308 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:225` | `by-test` | <!-- bl-156: by-test --> |
| V-0309 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:226` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0310 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:226` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0311 | c | BP-02 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:228` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0312 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:228` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0313 | c | BP-09 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:228` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0314 | c | BP-07 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:230` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0315 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:231` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0316 | c | BP-02 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:231` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0317 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:232` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0318 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:233` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0319 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:234` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0320 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:235` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0321 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:246` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0322 | a | A-PRIVATE | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:286` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0323 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0324 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:289` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0325 | c | BP-04 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0326 | c | BP-10 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0327 | c | BP-10 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:312` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0328 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:342` | `<!--` | <!-- /bl-156: by-test --> |
| V-0329 | c | BP-06 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:342` | `by-test` | <!-- /bl-156: by-test --> |
| V-0330 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:344` | `<!--` | <!-- issue-490:handoff --> |
| V-0331 | c | BP-02 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:345` | `#490` | ## Итог шага для БА (#490) |
| V-0332 | c | BP-01 | `prompts/drafts/bcreq-constraints-documentation-stepwise.md:366` | `<!--` | <!-- /issue-490:handoff --> |
| V-0333 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0334 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0335 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0336 | c | BP-08 | `prompts/drafts/bcreq-context-understanding-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0337 | c | BP-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0338 | c | BP-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0339 | c | BP-03 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0340 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0341 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0342 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0343 | c | BP-08 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0344 | c | BP-09 | `prompts/drafts/bcreq-context-understanding-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0345 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:21` | `<!--` | <!-- issue-474:entry --> |
| V-0346 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:32` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0347 | b | CT-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:72` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0348 | b | CT-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:72` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0349 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:94` | `<!--` | <!-- /issue-474:entry --> |
| V-0350 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:103` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0351 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:187` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-0352 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:219` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-0353 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:224` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-0354 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:316` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0355 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:327` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0356 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:420` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0357 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:422` | `<!--` | <!-- bl-156: by-test --> |
| V-0358 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:422` | `by-test` | <!-- bl-156: by-test --> |
| V-0359 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:423` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0360 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:423` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0361 | c | BP-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:425` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0362 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:425` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0363 | c | BP-09 | `prompts/drafts/bcreq-context-understanding-stepwise.md:425` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0364 | c | BP-07 | `prompts/drafts/bcreq-context-understanding-stepwise.md:427` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0365 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:428` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0366 | c | BP-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:428` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0367 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:429` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0368 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:430` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0369 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:431` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0370 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:432` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0371 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:443` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0372 | a | A-PRIVATE | `prompts/drafts/bcreq-context-understanding-stepwise.md:483` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0373 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:486` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0374 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:486` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0375 | c | BP-04 | `prompts/drafts/bcreq-context-understanding-stepwise.md:509` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0376 | c | BP-10 | `prompts/drafts/bcreq-context-understanding-stepwise.md:509` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0377 | c | BP-10 | `prompts/drafts/bcreq-context-understanding-stepwise.md:509` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0378 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:611` | `<!--` | <!-- /bl-156: by-test --> |
| V-0379 | c | BP-06 | `prompts/drafts/bcreq-context-understanding-stepwise.md:611` | `by-test` | <!-- /bl-156: by-test --> |
| V-0380 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:613` | `<!--` | <!-- issue-490:handoff --> |
| V-0381 | c | BP-02 | `prompts/drafts/bcreq-context-understanding-stepwise.md:614` | `#490` | ## Итог шага для БА (#490) |
| V-0382 | c | BP-01 | `prompts/drafts/bcreq-context-understanding-stepwise.md:635` | `<!--` | <!-- /issue-490:handoff --> |
| V-0383 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0384 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0385 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0386 | c | BP-08 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0387 | c | BP-02 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0388 | c | BP-02 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0389 | c | BP-03 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0390 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0391 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0392 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0393 | c | BP-08 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0394 | c | BP-09 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0395 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:27` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0396 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:74` | `mango_ba_prompts` | [Мета-стандарт раздела 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md). |
| V-0397 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:119` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0398 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:130` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0399 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:223` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0400 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:225` | `<!--` | <!-- bl-156: by-test --> |
| V-0401 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:225` | `by-test` | <!-- bl-156: by-test --> |
| V-0402 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:226` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0403 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:226` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0404 | c | BP-02 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:228` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0405 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:228` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0406 | c | BP-09 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:228` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0407 | c | BP-07 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:230` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0408 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:231` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0409 | c | BP-02 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:231` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0410 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:232` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0411 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:233` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0412 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:234` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0413 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:235` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0414 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:246` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0415 | a | A-PRIVATE | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:286` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0416 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0417 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:289` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0418 | c | BP-04 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:312` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0419 | c | BP-10 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:312` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0420 | c | BP-10 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:312` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0421 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:355` | `<!--` | <!-- /bl-156: by-test --> |
| V-0422 | c | BP-06 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:355` | `by-test` | <!-- /bl-156: by-test --> |
| V-0423 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:357` | `<!--` | <!-- issue-490:handoff --> |
| V-0424 | c | BP-02 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:358` | `#490` | ## Итог шага для БА (#490) |
| V-0425 | c | BP-01 | `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md:379` | `<!--` | <!-- /issue-490:handoff --> |
| V-0426 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0427 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0428 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0429 | c | BP-08 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0430 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0431 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко… |
| V-0432 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `#490` | …438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.… |
| V-0433 | c | BP-03 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» … |
| V-0434 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по… |
| V-0435 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0436 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0437 | c | BP-08 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);… |
| V-0438 | c | BP-09 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-0439 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:21` | `<!--` | <!-- issue-474:entry --> |
| V-0440 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:24` | `#490` | …тма Ш-3 проверь вход по формату шагов из «Состояния BCREQ» (#490). Декомпозированный (по умолчанию): явные AIN-21 и AIN-24/Г-IN, их task/attempt/route… |
| V-0441 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:32` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0442 | b | CT-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:72` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0443 | b | CT-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:72` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0444 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:94` | `<!--` | <!-- /issue-474:entry --> |
| V-0445 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:103` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0446 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:176` | `mango_ba_prompts` | [Мета-стандарт раздела 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md). |
| V-0447 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:184` | `mango_ba_prompts` | …BABOK — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-babok-guide-v3-что-берём… |
| V-0448 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:247` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0449 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:258` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0450 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:351` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0451 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:353` | `<!--` | <!-- bl-156: by-test --> |
| V-0452 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:353` | `by-test` | <!-- bl-156: by-test --> |
| V-0453 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:354` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0454 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:354` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0455 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:356` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0456 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:356` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0457 | c | BP-09 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:356` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0458 | c | BP-07 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:358` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0459 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:359` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0460 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:359` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0461 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:360` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0462 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:361` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0463 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:362` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0464 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:363` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0465 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:374` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0466 | a | A-PRIVATE | `prompts/drafts/bcreq-fr-documentation-stepwise.md:414` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0467 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:417` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0468 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:417` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0469 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:440` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0470 | c | BP-10 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:440` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0471 | c | BP-10 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:440` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0472 | c | BP-04 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:483` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-0473 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:488` | `<!--` | <!-- /bl-156: by-test --> |
| V-0474 | c | BP-06 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:488` | `by-test` | <!-- /bl-156: by-test --> |
| V-0475 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:490` | `<!--` | <!-- issue-490:handoff --> |
| V-0476 | c | BP-02 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:491` | `#490` | ## Итог шага для БА (#490) |
| V-0477 | c | BP-01 | `prompts/drafts/bcreq-fr-documentation-stepwise.md:512` | `<!--` | <!-- /issue-490:handoff --> |
| V-0478 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:15` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0479 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:15` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0480 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:15` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0481 | c | BP-08 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:15` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0482 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-0483 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-0484 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `#464` | …* Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-0485 | c | BP-03 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-0486 | c | BP-03 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-0487 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-0488 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-0489 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-0490 | c | BP-08 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-0491 | c | BP-09 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:17` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-0492 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:18` | `<!--` | <!-- issue-474:entry --> |
| V-0493 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:24` | `mango_ba_prompts` | [AIN-02]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md). |
| V-0494 | b | CT-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:71` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0495 | b | CT-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:71` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0496 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:93` | `<!--` | <!-- /issue-474:entry --> |
| V-0497 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:100` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-0498 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:106` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0499 | b | CT-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:147` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-0500 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:160` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-0501 | b | CT-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:177` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-0502 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:200` | `<!--` | <!-- bl-156: by-test --> |
| V-0503 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:200` | `by-test` | <!-- bl-156: by-test --> |
| V-0504 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:201` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0505 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:201` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0506 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:203` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0507 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:203` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0508 | c | BP-09 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:203` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0509 | c | BP-07 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:205` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0510 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:206` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0511 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:206` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0512 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:207` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0513 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:208` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0514 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:209` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0515 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:210` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0516 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:221` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0517 | a | A-PRIVATE | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:261` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0518 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:264` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0519 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:264` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0520 | c | BP-04 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:287` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0521 | c | BP-10 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:287` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0522 | c | BP-10 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:287` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0523 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:315` | `<!--` | <!-- /bl-156: by-test --> |
| V-0524 | c | BP-06 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:315` | `by-test` | <!-- /bl-156: by-test --> |
| V-0525 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:317` | `<!--` | <!-- issue-490:handoff --> |
| V-0526 | c | BP-02 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:318` | `#490` | ## Итог шага для БА (#490) |
| V-0527 | c | BP-01 | `prompts/drafts/bcreq-intake-questionnaire-stepwise.md:339` | `<!--` | <!-- /issue-490:handoff --> |
| V-0528 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0529 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0530 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0531 | c | BP-08 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0532 | c | BP-02 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0533 | c | BP-02 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0534 | c | BP-03 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0535 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0536 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0537 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0538 | c | BP-08 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0539 | c | BP-09 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0540 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:27` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0541 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:74` | `mango_ba_prompts` | [Мета-стандарт раздела 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md). |
| V-0542 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:118` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0543 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:129` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0544 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:222` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0545 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:224` | `<!--` | <!-- bl-156: by-test --> |
| V-0546 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:224` | `by-test` | <!-- bl-156: by-test --> |
| V-0547 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:225` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0548 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:225` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0549 | c | BP-02 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:227` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0550 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:227` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0551 | c | BP-09 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:227` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0552 | c | BP-07 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:229` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0553 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:230` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0554 | c | BP-02 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:230` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0555 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:231` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0556 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:232` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0557 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:233` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0558 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:234` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0559 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:245` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0560 | a | A-PRIVATE | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:285` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0561 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:288` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0562 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:288` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0563 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:311` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0564 | c | BP-10 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:311` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0565 | c | BP-10 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:311` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0566 | c | BP-04 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:346` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-0567 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:351` | `<!--` | <!-- /bl-156: by-test --> |
| V-0568 | c | BP-06 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:351` | `by-test` | <!-- /bl-156: by-test --> |
| V-0569 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:353` | `<!--` | <!-- issue-490:handoff --> |
| V-0570 | c | BP-02 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:354` | `#490` | ## Итог шага для БА (#490) |
| V-0571 | c | BP-01 | `prompts/drafts/bcreq-nfr-documentation-stepwise.md:375` | `<!--` | <!-- /issue-490:handoff --> |
| V-0572 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0573 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0574 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0575 | c | BP-08 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0576 | c | BP-02 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0577 | c | BP-02 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0578 | c | BP-03 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0579 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0580 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0581 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0582 | c | BP-08 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0583 | c | BP-09 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0584 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:29` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0585 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:106` | `mango_ba_prompts` | [Мета-стандарт раздела 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-0586 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:107` | `mango_ba_prompts` | [правила композиции]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции). |
| V-0587 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:116` | `mango_ba_prompts` | …ктуры — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-… |
| V-0588 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:194` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0589 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:205` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0590 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:298` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0591 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:300` | `<!--` | <!-- bl-156: by-test --> |
| V-0592 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:300` | `by-test` | <!-- bl-156: by-test --> |
| V-0593 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:301` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0594 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:301` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0595 | c | BP-02 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:303` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0596 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:303` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0597 | c | BP-09 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:303` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0598 | c | BP-07 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:305` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0599 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:306` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0600 | c | BP-02 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:306` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0601 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:307` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0602 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:308` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0603 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:309` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0604 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:310` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0605 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:321` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0606 | a | A-PRIVATE | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:361` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0607 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:364` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0608 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:364` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0609 | c | BP-04 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:387` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0610 | c | BP-10 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:387` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0611 | c | BP-10 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:387` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0612 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:424` | `<!--` | <!-- /bl-156: by-test --> |
| V-0613 | c | BP-06 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:424` | `by-test` | <!-- /bl-156: by-test --> |
| V-0614 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:426` | `<!--` | <!-- issue-490:handoff --> |
| V-0615 | c | BP-02 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:427` | `#490` | ## Итог шага для БА (#490) |
| V-0616 | c | BP-01 | `prompts/drafts/bcreq-orr-solution-design-stepwise.md:448` | `<!--` | <!-- /issue-490:handoff --> |
| V-0617 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0618 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0619 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0620 | c | BP-08 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0621 | c | BP-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0622 | c | BP-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0623 | c | BP-03 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0624 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0625 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0626 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0627 | c | BP-08 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0628 | c | BP-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0629 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:21` | `<!--` | <!-- issue-474:entry --> |
| V-0630 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:32` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-0631 | b | CT-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:72` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0632 | b | CT-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:72` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0633 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:94` | `<!--` | <!-- /issue-474:entry --> |
| V-0634 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:103` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0635 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:122` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-0636 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:123` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-0637 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:149` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-0638 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:149` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-0639 | b | CT-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0640 | b | CT-05 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0641 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0642 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0643 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0644 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0645 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:150` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-0646 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:151` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0647 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:151` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0648 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:151` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0649 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:151` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0650 | b | CT-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:151` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-0651 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:165` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-0652 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:168` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-0653 | b | CT-03 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:186` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-0654 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:234` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0655 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:245` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0656 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:338` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0657 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:340` | `<!--` | <!-- bl-156: by-test --> |
| V-0658 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:340` | `by-test` | <!-- bl-156: by-test --> |
| V-0659 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:341` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0660 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:341` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0661 | c | BP-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:343` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0662 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:343` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0663 | c | BP-09 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:343` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0664 | c | BP-07 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:345` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0665 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:346` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0666 | c | BP-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:346` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0667 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:347` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0668 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:348` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0669 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:349` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0670 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:350` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0671 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:361` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0672 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:378` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-0673 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:382` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-0674 | a | A-PRIVATE | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:408` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0675 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:411` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0676 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:411` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0677 | c | BP-04 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:434` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0678 | c | BP-10 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:434` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0679 | c | BP-10 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:434` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0680 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:522` | `<!--` | <!-- /bl-156: by-test --> |
| V-0681 | c | BP-06 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:522` | `by-test` | <!-- /bl-156: by-test --> |
| V-0682 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:524` | `<!--` | <!-- issue-490:handoff --> |
| V-0683 | c | BP-02 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:525` | `#490` | ## Итог шага для БА (#490) |
| V-0684 | c | BP-01 | `prompts/drafts/bcreq-products-impact-analysis-stepwise.md:546` | `<!--` | <!-- /issue-490:handoff --> |
| V-0685 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:15` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0686 | c | BP-01 | `prompts/drafts/bcreq-release-readiness-oneshot.md:15` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0687 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:15` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0688 | c | BP-08 | `prompts/drafts/bcreq-release-readiness-oneshot.md:15` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0689 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-0690 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «по тес… |
| V-0691 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-0692 | c | BP-03 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «… |
| V-0693 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2)… |
| V-0694 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-0695 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-0696 | c | BP-08 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, ра… |
| V-0697 | c | BP-09 | `prompts/drafts/bcreq-release-readiness-oneshot.md:17` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-0698 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:22` | `mango_ba_prompts` | ([RFC #427, раздел 9.2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)). |
| V-0699 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:22` | `#427` | ([RFC #427, раздел 9.2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)). |
| V-0700 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:24` | `BL-1` | гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16). |
| V-0701 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:24` | `RUN-0` | гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16). |
| V-0702 | c | BP-01 | `prompts/drafts/bcreq-release-readiness-oneshot.md:120` | `<!--` | <!-- bl-156: by-test --> |
| V-0703 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:120` | `by-test` | <!-- bl-156: by-test --> |
| V-0704 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:121` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0705 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:121` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0706 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:123` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0707 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:123` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0708 | c | BP-09 | `prompts/drafts/bcreq-release-readiness-oneshot.md:123` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0709 | c | BP-07 | `prompts/drafts/bcreq-release-readiness-oneshot.md:125` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0710 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:126` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0711 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:126` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0712 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:127` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0713 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:128` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0714 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:129` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0715 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:130` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0716 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:141` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0717 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:158` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-0718 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:162` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-0719 | a | A-PRIVATE | `prompts/drafts/bcreq-release-readiness-oneshot.md:188` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0720 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:191` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0721 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:191` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0722 | c | BP-04 | `prompts/drafts/bcreq-release-readiness-oneshot.md:214` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0723 | c | BP-10 | `prompts/drafts/bcreq-release-readiness-oneshot.md:214` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0724 | c | BP-10 | `prompts/drafts/bcreq-release-readiness-oneshot.md:214` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0725 | c | BP-01 | `prompts/drafts/bcreq-release-readiness-oneshot.md:289` | `<!--` | <!-- /bl-156: by-test --> |
| V-0726 | c | BP-06 | `prompts/drafts/bcreq-release-readiness-oneshot.md:289` | `by-test` | <!-- /bl-156: by-test --> |
| V-0727 | c | BP-01 | `prompts/drafts/bcreq-release-readiness-oneshot.md:291` | `<!--` | <!-- issue-490:handoff --> |
| V-0728 | c | BP-02 | `prompts/drafts/bcreq-release-readiness-oneshot.md:292` | `#490` | ## Итог шага для БА (#490) |
| V-0729 | c | BP-01 | `prompts/drafts/bcreq-release-readiness-oneshot.md:313` | `<!--` | <!-- /issue-490:handoff --> |
| V-0730 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0731 | c | BP-01 | `prompts/drafts/bcreq-review-validation-oneshot.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0732 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0733 | c | BP-08 | `prompts/drafts/bcreq-review-validation-oneshot.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0734 | c | BP-02 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0735 | c | BP-02 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0736 | c | BP-03 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0737 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0738 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0739 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0740 | c | BP-08 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0741 | c | BP-09 | `prompts/drafts/bcreq-review-validation-oneshot.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0742 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:30` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0743 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:74` | `mango_ba_prompts` | [Контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты); |
| V-0744 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:75` | `mango_ba_prompts` | [мета-стандарты разделов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0745 | c | BP-01 | `prompts/drafts/bcreq-review-validation-oneshot.md:135` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0746 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:146` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0747 | c | BP-01 | `prompts/drafts/bcreq-review-validation-oneshot.md:240` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0748 | c | BP-01 | `prompts/drafts/bcreq-review-validation-oneshot.md:242` | `<!--` | <!-- bl-156: by-test --> |
| V-0749 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:242` | `by-test` | <!-- bl-156: by-test --> |
| V-0750 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:243` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0751 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:243` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0752 | c | BP-02 | `prompts/drafts/bcreq-review-validation-oneshot.md:245` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0753 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:245` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0754 | c | BP-09 | `prompts/drafts/bcreq-review-validation-oneshot.md:245` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0755 | c | BP-07 | `prompts/drafts/bcreq-review-validation-oneshot.md:247` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0756 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:248` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0757 | c | BP-02 | `prompts/drafts/bcreq-review-validation-oneshot.md:248` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0758 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:249` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0759 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:250` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0760 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:251` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0761 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:252` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0762 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:263` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0763 | a | A-PRIVATE | `prompts/drafts/bcreq-review-validation-oneshot.md:307` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0764 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:310` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0765 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:310` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0766 | c | BP-04 | `prompts/drafts/bcreq-review-validation-oneshot.md:333` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0767 | c | BP-10 | `prompts/drafts/bcreq-review-validation-oneshot.md:333` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0768 | c | BP-10 | `prompts/drafts/bcreq-review-validation-oneshot.md:333` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0769 | c | BP-01 | `prompts/drafts/bcreq-review-validation-oneshot.md:418` | `<!--` | <!-- /bl-156: by-test --> |
| V-0770 | c | BP-06 | `prompts/drafts/bcreq-review-validation-oneshot.md:418` | `by-test` | <!-- /bl-156: by-test --> |
| V-0771 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0772 | c | BP-01 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0773 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0774 | c | BP-08 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0775 | c | BP-02 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0776 | c | BP-02 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0777 | c | BP-03 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0778 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0779 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0780 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0781 | c | BP-08 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0782 | c | BP-09 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0783 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:30` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0784 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:72` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md) |
| V-0785 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:74` | `mango_ba_prompts` | [архитектуры промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)). |
| V-0786 | c | BP-01 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:113` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0787 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:124` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0788 | c | BP-01 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:217` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0789 | c | BP-01 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:219` | `<!--` | <!-- bl-156: by-test --> |
| V-0790 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:219` | `by-test` | <!-- bl-156: by-test --> |
| V-0791 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:220` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0792 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:220` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0793 | c | BP-02 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:222` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0794 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:222` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0795 | c | BP-09 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:222` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0796 | c | BP-07 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:224` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0797 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:225` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0798 | c | BP-02 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:225` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0799 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:226` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0800 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:227` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0801 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:228` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0802 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:229` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0803 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:240` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0804 | a | A-PRIVATE | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:280` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0805 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:283` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0806 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:283` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0807 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:306` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0808 | c | BP-10 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:306` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0809 | c | BP-10 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:306` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0810 | c | BP-04 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:348` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-0811 | c | BP-01 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:353` | `<!--` | <!-- /bl-156: by-test --> |
| V-0812 | c | BP-06 | `prompts/drafts/bcreq-scenarios-modeling-oneshot.md:353` | `by-test` | <!-- /bl-156: by-test --> |
| V-0813 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0814 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0815 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0816 | c | BP-08 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-0817 | c | BP-02 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0818 | c | BP-02 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0819 | c | BP-03 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0820 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-0821 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0822 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0823 | c | BP-08 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-0824 | c | BP-09 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-0825 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:30` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-0826 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:92` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-0827 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:154` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-0828 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:165` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-0829 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:258` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-0830 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:260` | `<!--` | <!-- bl-156: by-test --> |
| V-0831 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:260` | `by-test` | <!-- bl-156: by-test --> |
| V-0832 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:261` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0833 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:261` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-0834 | c | BP-02 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:263` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0835 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:263` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0836 | c | BP-09 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:263` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-0837 | c | BP-07 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:265` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-0838 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:266` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0839 | c | BP-02 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:266` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-0840 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:267` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-0841 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:268` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-0842 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:269` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-0843 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:270` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-0844 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:281` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-0845 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:300` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-0846 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:304` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-0847 | a | A-PRIVATE | `prompts/drafts/bcreq-uc-modeling-stepwise.md:330` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-0848 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:333` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0849 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:333` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-0850 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:356` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0851 | c | BP-10 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:356` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0852 | c | BP-10 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:356` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-0853 | c | BP-04 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:398` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-0854 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:403` | `<!--` | <!-- /bl-156: by-test --> |
| V-0855 | c | BP-06 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:403` | `by-test` | <!-- /bl-156: by-test --> |
| V-0856 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:405` | `<!--` | <!-- issue-490:handoff --> |
| V-0857 | c | BP-02 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:406` | `#490` | ## Итог шага для БА (#490) |
| V-0858 | c | BP-01 | `prompts/drafts/bcreq-uc-modeling-stepwise.md:439` | `<!--` | <!-- /issue-490:handoff --> |
| V-0859 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0860 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0861 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0862 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0863 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0864 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0865 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0866 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0867 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0868 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0869 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0870 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0871 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0872 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0873 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0874 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-0875 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-0876 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-0877 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0878 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0879 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0880 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0881 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0882 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0883 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0884 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0885 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0886 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0887 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0888 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0889 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0890 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0891 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0892 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-0893 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-0894 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-0895 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0896 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0897 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0898 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0899 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0900 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0901 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0902 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0903 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0904 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0905 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0906 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0907 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0908 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0909 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0910 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-0911 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-0912 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-03-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-0913 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0914 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0915 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0916 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0917 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0918 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0919 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0920 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0921 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0922 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0923 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0924 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0925 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0926 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0927 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:265` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0928 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:268` | `<!--` | <!-- issue-490:handoff --> |
| V-0929 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:269` | `#490` | ## Итог шага для БА (#490) |
| V-0930 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-04-understanding-stepwise.md:290` | `<!--` | <!-- /issue-490:handoff --> |
| V-0931 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0932 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0933 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0934 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0935 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0936 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0937 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0938 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0939 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0940 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0941 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0942 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0943 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0944 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0945 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:265` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0946 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:268` | `<!--` | <!-- issue-490:handoff --> |
| V-0947 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:269` | `#490` | ## Итог шага для БА (#490) |
| V-0948 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-05-understanding-stepwise.md:290` | `<!--` | <!-- /issue-490:handoff --> |
| V-0949 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0950 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0951 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0952 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0953 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0954 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0955 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0956 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0957 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0958 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0959 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0960 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0961 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0962 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0963 | b | CT-03 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:220` | `коннектора` | - Зачем: Новизна коннектора не отменяет дельту существующих подсистем. |
| V-0964 | b | CT-05 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:229` | `ЛК` | … → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст… |
| V-0965 | b | CT-05 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:237` | `ЛК` | У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим… |
| V-0966 | b | CT-03 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` | `коннектор` | Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие. |
| V-0967 | b | CT-05 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:248` | `ЛК` | Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие. |
| V-0968 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0969 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-0970 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-0971 | b | CT-05 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:281` | `ЛК` | …технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта … |
| V-0972 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-06-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-0973 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0974 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0975 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0976 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0977 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0978 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0979 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0980 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0981 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-0982 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-0983 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-0984 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-0985 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0986 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-0987 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-0988 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-0989 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-0990 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-07-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-0991 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0992 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0993 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-0994 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0995 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0996 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-0997 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0998 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-0999 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1000 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1001 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1002 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1003 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1004 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1005 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1006 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1007 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1008 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-08-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1009 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1010 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1011 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1012 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1013 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1014 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1015 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1016 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1017 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1018 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1019 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1020 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1021 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1022 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1023 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1024 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1025 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1026 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-09-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1027 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1028 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1029 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1030 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1031 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1032 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1033 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1034 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1035 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1036 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1037 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1038 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1039 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1040 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1041 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1042 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1043 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1044 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-10-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1045 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1046 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1047 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1048 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1049 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1050 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1051 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1052 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1053 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1054 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1055 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1056 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1057 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1058 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1059 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1060 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1061 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1062 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-11-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1063 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1064 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1065 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1066 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1067 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1068 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1069 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1070 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1071 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1072 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1073 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1074 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1075 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1076 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1077 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` | `amoCRM` | Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет». |
| V-1078 | b | CT-06 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:248` | `HDE` | Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет». |
| V-1079 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:265` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1080 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:268` | `<!--` | <!-- issue-490:handoff --> |
| V-1081 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:269` | `#490` | ## Итог шага для БА (#490) |
| V-1082 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-12-understanding-stepwise.md:290` | `<!--` | <!-- /issue-490:handoff --> |
| V-1083 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1084 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1085 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1086 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1087 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1088 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1089 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1090 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1091 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1092 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1093 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1094 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1095 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1096 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1097 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1098 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1099 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1100 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-13-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1101 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1102 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1103 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1104 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1105 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1106 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1107 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1108 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1109 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1110 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1111 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1112 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1113 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1114 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1115 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1116 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1117 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1118 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-14-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1119 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1120 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1121 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1122 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1123 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1124 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1125 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1126 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1127 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1128 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1129 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1130 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1131 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1132 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1133 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1134 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1135 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1136 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-15-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1137 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1138 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1139 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1140 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1141 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1142 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1143 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1144 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1145 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1146 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1147 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1148 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1149 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1150 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1151 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:265` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1152 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:268` | `<!--` | <!-- issue-490:handoff --> |
| V-1153 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:269` | `#490` | ## Итог шага для БА (#490) |
| V-1154 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-16-understanding-stepwise.md:290` | `<!--` | <!-- /issue-490:handoff --> |
| V-1155 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1156 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1157 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1158 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1159 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1160 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1161 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1162 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1163 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1164 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1165 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1166 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1167 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1168 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1169 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1170 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1171 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1172 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-17-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1173 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1174 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1175 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1176 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1177 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1178 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1179 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1180 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1181 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1182 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1183 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1184 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1185 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1186 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1187 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1188 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1189 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1190 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-18-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1191 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1192 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1193 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1194 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1195 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1196 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1197 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1198 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1199 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1200 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1201 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1202 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1203 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1204 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1205 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:264` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1206 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:267` | `<!--` | <!-- issue-490:handoff --> |
| V-1207 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:268` | `#490` | ## Итог шага для БА (#490) |
| V-1208 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-19-understanding-stepwise.md:289` | `<!--` | <!-- /issue-490:handoff --> |
| V-1209 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1210 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1211 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1212 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1213 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1214 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1215 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1216 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1217 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1218 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1219 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1220 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1221 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1222 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1223 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1224 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1225 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1226 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-20-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1227 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1228 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1229 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1230 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1231 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1232 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1233 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1234 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1235 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1236 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1237 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1238 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1239 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1240 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1241 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1242 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1243 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1244 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-21-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1245 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1246 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1247 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1248 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1249 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1250 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1251 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1252 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1253 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1254 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1255 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1256 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1257 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1258 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1259 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:265` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1260 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:268` | `<!--` | <!-- issue-490:handoff --> |
| V-1261 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:269` | `#490` | ## Итог шага для БА (#490) |
| V-1262 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-22-understanding-stepwise.md:290` | `<!--` | <!-- /issue-490:handoff --> |
| V-1263 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1264 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1265 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1266 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1267 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1268 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1269 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1270 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1271 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1272 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1273 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1274 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1275 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1276 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1277 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1278 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1279 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1280 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-23-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1281 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:13` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1282 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:13` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1283 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:13` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-1284 | c | BP-08 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:17` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1285 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:17` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1286 | c | BP-09 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:17` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-1287 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:25` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1288 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:25` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1289 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:51` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1290 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:52` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1291 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:53` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1292 | a | A-PRIVATE | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:54` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1293 | b | CT-01 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:153` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1294 | b | CT-02 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:153` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1295 | c | BP-04 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:263` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-1296 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:266` | `<!--` | <!-- issue-490:handoff --> |
| V-1297 | c | BP-02 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:267` | `#490` | ## Итог шага для БА (#490) |
| V-1298 | c | BP-01 | `prompts/drafts/a-in/bcreq-ain-24-understanding-stepwise.md:288` | `<!--` | <!-- /issue-490:handoff --> |
| V-1299 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:16` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1300 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:16` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1301 | c | BP-08 | `prompts/drafts/system/bcreq-context-understanding-system.md:16` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1302 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-1303 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага … |
| V-1304 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1305 | c | BP-03 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1306 | c | BP-04 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1307 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-1308 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-1309 | c | BP-08 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-1310 | c | BP-09 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ни… |
| V-1311 | c | BP-11 | `prompts/drafts/system/bcreq-context-understanding-system.md:18` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-1312 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:22` | `<!--` | <!-- issue-490:system --> |
| V-1313 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:23` | `#490` | ## Системный формат шагов (#490) |
| V-1314 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:27` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1315 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:27` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1316 | c | BP-03 | `prompts/drafts/system/bcreq-context-understanding-system.md:27` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1317 | b | CT-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:85` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1318 | b | CT-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:85` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1319 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:107` | `<!--` | <!-- /issue-490:system --> |
| V-1320 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:113` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-1321 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:197` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-1322 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:229` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-1323 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:234` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-1324 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:326` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-1325 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:337` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md), |
| V-1326 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:430` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-1327 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:432` | `<!--` | <!-- bl-156: by-test --> |
| V-1328 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:432` | `by-test` | <!-- bl-156: by-test --> |
| V-1329 | c | BP-04 | `prompts/drafts/system/bcreq-context-understanding-system.md:433` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1330 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:433` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1331 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:435` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1332 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:435` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1333 | c | BP-09 | `prompts/drafts/system/bcreq-context-understanding-system.md:435` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1334 | c | BP-07 | `prompts/drafts/system/bcreq-context-understanding-system.md:437` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1335 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:438` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1336 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:438` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1337 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:439` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1338 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:440` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1339 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:441` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1340 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:442` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1341 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:453` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1342 | a | A-PRIVATE | `prompts/drafts/system/bcreq-context-understanding-system.md:493` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1343 | c | BP-04 | `prompts/drafts/system/bcreq-context-understanding-system.md:496` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1344 | c | BP-04 | `prompts/drafts/system/bcreq-context-understanding-system.md:496` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1345 | c | BP-04 | `prompts/drafts/system/bcreq-context-understanding-system.md:519` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1346 | c | BP-10 | `prompts/drafts/system/bcreq-context-understanding-system.md:519` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1347 | c | BP-10 | `prompts/drafts/system/bcreq-context-understanding-system.md:519` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1348 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:621` | `<!--` | <!-- /bl-156: by-test --> |
| V-1349 | c | BP-06 | `prompts/drafts/system/bcreq-context-understanding-system.md:621` | `by-test` | <!-- /bl-156: by-test --> |
| V-1350 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:623` | `<!--` | <!-- issue-490:handoff --> |
| V-1351 | c | BP-02 | `prompts/drafts/system/bcreq-context-understanding-system.md:624` | `#490` | ## Итог шага для БА (#490) |
| V-1352 | c | BP-01 | `prompts/drafts/system/bcreq-context-understanding-system.md:645` | `<!--` | <!-- /issue-490:handoff --> |
| V-1353 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:16` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1354 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:16` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1355 | c | BP-08 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:16` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1356 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-1357 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без про… |
| V-1358 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1359 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `#464` | …. Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1360 | c | BP-03 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1361 | c | BP-03 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1362 | c | BP-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1363 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): ш… |
| V-1364 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): ш… |
| V-1365 | c | BP-08 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-1366 | c | BP-09 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0… |
| V-1367 | c | BP-11 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:18` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-1368 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:22` | `<!--` | <!-- issue-490:system --> |
| V-1369 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:23` | `#490` | ## Системный формат шагов (#490) |
| V-1370 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:27` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1371 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:27` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1372 | c | BP-03 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:27` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1373 | b | CT-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:85` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1374 | b | CT-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:85` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1375 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:107` | `<!--` | <!-- /issue-490:system --> |
| V-1376 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:111` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-1377 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:117` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-1378 | b | CT-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:158` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-1379 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:171` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-1380 | b | CT-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:188` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-1381 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:211` | `<!--` | <!-- bl-156: by-test --> |
| V-1382 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:211` | `by-test` | <!-- bl-156: by-test --> |
| V-1383 | c | BP-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:212` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1384 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:212` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1385 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:214` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1386 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:214` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1387 | c | BP-09 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:214` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1388 | c | BP-07 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:216` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1389 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:217` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1390 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:217` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1391 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:218` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1392 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:219` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1393 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:220` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1394 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:221` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1395 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:232` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1396 | a | A-PRIVATE | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:272` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1397 | c | BP-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:275` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1398 | c | BP-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:275` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1399 | c | BP-04 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:298` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1400 | c | BP-10 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:298` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1401 | c | BP-10 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:298` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1402 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:326` | `<!--` | <!-- /bl-156: by-test --> |
| V-1403 | c | BP-06 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:326` | `by-test` | <!-- /bl-156: by-test --> |
| V-1404 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:328` | `<!--` | <!-- issue-490:handoff --> |
| V-1405 | c | BP-02 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:329` | `#490` | ## Итог шага для БА (#490) |
| V-1406 | c | BP-01 | `prompts/drafts/system/bcreq-intake-questionnaire-system.md:350` | `<!--` | <!-- /issue-490:handoff --> |
| V-1407 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:16` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1408 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:16` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1409 | c | BP-08 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:16` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-1410 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-1411 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага … |
| V-1412 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1413 | c | BP-03 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1414 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1415 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-1416 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-1417 | c | BP-08 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-1418 | c | BP-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ни… |
| V-1419 | c | BP-11 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:18` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-1420 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:22` | `<!--` | <!-- issue-490:system --> |
| V-1421 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:23` | `#490` | ## Системный формат шагов (#490) |
| V-1422 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:27` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1423 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:27` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1424 | c | BP-03 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:27` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-1425 | b | CT-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:85` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1426 | b | CT-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:85` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1427 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:107` | `<!--` | <!-- /issue-490:system --> |
| V-1428 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:113` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-1429 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:132` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-1430 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:133` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-1431 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:159` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-1432 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:159` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-1433 | b | CT-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1434 | b | CT-05 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1435 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1436 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1437 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1438 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1439 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:160` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1440 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:161` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1441 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:161` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1442 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:161` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1443 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:161` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1444 | b | CT-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:161` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1445 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:175` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-1446 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:178` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-1447 | b | CT-03 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:196` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-1448 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:244` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-1449 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:255` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md), |
| V-1450 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:348` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-1451 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:350` | `<!--` | <!-- bl-156: by-test --> |
| V-1452 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:350` | `by-test` | <!-- bl-156: by-test --> |
| V-1453 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:351` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1454 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:351` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1455 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:353` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1456 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:353` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1457 | c | BP-09 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:353` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1458 | c | BP-07 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:355` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1459 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:356` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1460 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:356` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1461 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:357` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1462 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:358` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1463 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:359` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1464 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:360` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1465 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:371` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1466 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:388` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-1467 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:392` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-1468 | a | A-PRIVATE | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:418` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1469 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:421` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1470 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:421` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1471 | c | BP-04 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:444` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1472 | c | BP-10 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:444` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1473 | c | BP-10 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:444` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1474 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:532` | `<!--` | <!-- /bl-156: by-test --> |
| V-1475 | c | BP-06 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:532` | `by-test` | <!-- /bl-156: by-test --> |
| V-1476 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:534` | `<!--` | <!-- issue-490:handoff --> |
| V-1477 | c | BP-02 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:535` | `#490` | ## Итог шага для БА (#490) |
| V-1478 | c | BP-01 | `prompts/drafts/system/bcreq-products-impact-analysis-system.md:556` | `<!--` | <!-- /issue-490:handoff --> |
| V-1479 | a | A-PRIVATE | `prompts/archive/constraints-documentation-oneshot.md:10` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md), [bcreq-wo… |
| V-1480 | c | BP-02 | `prompts/archive/constraints-documentation-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-constraints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/m… |
| V-1481 | c | BP-03 | `prompts/archive/constraints-documentation-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-constraints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/m… |
| V-1482 | a | A-PRIVATE | `prompts/archive/constraints-documentation-stepwise.md:10` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md), [bcreq-wo… |
| V-1483 | c | BP-02 | `prompts/archive/constraints-documentation-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-constraints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/m… |
| V-1484 | c | BP-03 | `prompts/archive/constraints-documentation-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-constraints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/m… |
| V-1485 | a | A-PRIVATE | `prompts/archive/fr-documentation-oneshot.md:10` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md), [bcreq-core-docume… |
| V-1486 | c | BP-02 | `prompts/archive/fr-documentation-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1487 | c | BP-03 | `prompts/archive/fr-documentation-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1488 | a | A-PRIVATE | `prompts/archive/fr-documentation-stepwise.md:10` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md), [bcreq-core-docume… |
| V-1489 | c | BP-02 | `prompts/archive/fr-documentation-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1490 | c | BP-03 | `prompts/archive/fr-documentation-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1491 | a | A-PRIVATE | `prompts/archive/fr-validation-legacy.md:10` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md). Файл сохранён для … |
| V-1492 | c | BP-02 | `prompts/archive/fr-validation-legacy.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1493 | c | BP-03 | `prompts/archive/fr-validation-legacy.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1494 | a | A-PRIVATE | `prompts/archive/fr-validation-oneshot.md:10` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md). Файл сохранён для … |
| V-1495 | c | BP-02 | `prompts/archive/fr-validation-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1496 | c | BP-03 | `prompts/archive/fr-validation-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1497 | a | A-PRIVATE | `prompts/archive/fr-validation-stepwise.md:10` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md). Файл сохранён для … |
| V-1498 | c | BP-02 | `prompts/archive/fr-validation-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1499 | c | BP-03 | `prompts/archive/fr-validation-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/promp… |
| V-1500 | a | A-PRIVATE | `prompts/archive/glossary-context-understanding-oneshot.md:10` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md), [bcreq-in-und… |
| V-1501 | c | BP-02 | `prompts/archive/glossary-context-understanding-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1502 | c | BP-03 | `prompts/archive/glossary-context-understanding-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1503 | a | A-PRIVATE | `prompts/archive/glossary-context-understanding-stepwise.md:10` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md), [bcreq-in-und… |
| V-1504 | c | BP-02 | `prompts/archive/glossary-context-understanding-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1505 | c | BP-03 | `prompts/archive/glossary-context-understanding-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1506 | a | A-PRIVATE | `prompts/archive/questions-customer-understanding-legacy.md:10` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md), [bcreq-in-und… |
| V-1507 | c | BP-02 | `prompts/archive/questions-customer-understanding-legacy.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1508 | c | BP-03 | `prompts/archive/questions-customer-understanding-legacy.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1509 | a | A-PRIVATE | `prompts/archive/questions-customer-understanding-stepwise.md:10` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md), [bcreq-in-und… |
| V-1510 | c | BP-02 | `prompts/archive/questions-customer-understanding-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1511 | c | BP-03 | `prompts/archive/questions-customer-understanding-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/… |
| V-1512 | a | A-PRIVATE | `prompts/archive/technical-details-solution-design-legacy.md:10` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md), [bcreq-work-sol… |
| V-1513 | c | BP-02 | `prompts/archive/technical-details-solution-design-legacy.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1514 | c | BP-03 | `prompts/archive/technical-details-solution-design-legacy.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1515 | a | A-PRIVATE | `prompts/archive/technical-details-solution-design-oneshot.md:10` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md), [bcreq-work-sol… |
| V-1516 | c | BP-02 | `prompts/archive/technical-details-solution-design-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1517 | c | BP-03 | `prompts/archive/technical-details-solution-design-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1518 | a | A-PRIVATE | `prompts/archive/technical-details-solution-design-stepwise.md:10` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md), [bcreq-work-sol… |
| V-1519 | c | BP-02 | `prompts/archive/technical-details-solution-design-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1520 | c | BP-03 | `prompts/archive/technical-details-solution-design-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr… |
| V-1521 | c | BP-01 | `prompts/archive/tz-stats-generator-simple-legacy.md:23` | `<!--` | <!-- Бизнес-задача: посчитать и накопить статистику классов Mango по ТЗ в чате без доступа к репозиторию и research Хаба. --> |
| V-1522 | a | A-PRIVATE | `prompts/archive/uc-modeling-oneshot.md:10` | `mango_ba_prompts` | …Q: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md), [bcreq-scenarios-modeli… |
| V-1523 | c | BP-02 | `prompts/archive/uc-modeling-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bc… |
| V-1524 | c | BP-03 | `prompts/archive/uc-modeling-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bc… |
| V-1525 | a | A-PRIVATE | `prompts/archive/uc-modeling-stepwise.md:10` | `mango_ba_prompts` | …Q: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md), [bcreq-scenarios-modeli… |
| V-1526 | c | BP-02 | `prompts/archive/uc-modeling-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bc… |
| V-1527 | c | BP-03 | `prompts/archive/uc-modeling-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bc… |
| V-1528 | a | A-PRIVATE | `prompts/archive/us-modeling-oneshot.md:10` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md). Файл сохранён для… |
| V-1529 | c | BP-02 | `prompts/archive/us-modeling-oneshot.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prom… |
| V-1530 | c | BP-03 | `prompts/archive/us-modeling-oneshot.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prom… |
| V-1531 | a | A-PRIVATE | `prompts/archive/us-modeling-stepwise.md:10` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md). Файл сохранён для… |
| V-1532 | c | BP-02 | `prompts/archive/us-modeling-stepwise.md:10` | `#388` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prom… |
| V-1533 | c | BP-03 | `prompts/archive/us-modeling-stepwise.md:10` | `issue` | > **Архив (issue #388).** Промпт заменён набором BCREQ: [bcreq-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prom… |
| V-1534 | c | BP-01 | `prompts/archive/usecase-stepwise-generator-simple-legacy.md:23` | `<!--` | <!-- Бизнес-задача: собрать пошаговый Use Case Mango через подтверждения пользователя без доступа к глоссарию репозитория и research-выдержкам. --> |
| V-1535 | c | BP-01 | `prompts/archive/user-story-generator-simple-legacy.md:23` | `<!--` | <!-- Бизнес-задача: превратить сырой запрос Mango в проверяемую User Story в standalone-чате без формальной research-зависимости. --> |
| V-1536 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1537 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1538 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1539 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1540 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1541 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1542 | c | BP-03 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1543 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1544 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1545 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1546 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-1547 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1548 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:27` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-1549 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:111` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-1550 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:143` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-1551 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:148` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-1552 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:240` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-1553 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:251` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-1554 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:344` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-1555 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:346` | `<!--` | <!-- bl-156: by-test --> |
| V-1556 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:346` | `by-test` | <!-- bl-156: by-test --> |
| V-1557 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:347` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1558 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:347` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1559 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:349` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1560 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:349` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1561 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:349` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1562 | c | BP-07 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:351` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1563 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:352` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1564 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:352` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1565 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:353` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1566 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:354` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1567 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:355` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1568 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:356` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1569 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:367` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1570 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:407` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1571 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:410` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1572 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:410` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1573 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:433` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1574 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:433` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1575 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:433` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1576 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:535` | `<!--` | <!-- /bl-156: by-test --> |
| V-1577 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md:535` | `by-test` | <!-- /bl-156: by-test --> |
| V-1578 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:21` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-1579 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:29` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-1580 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:86` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-1581 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:87` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-1582 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:88` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-1583 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:89` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-1584 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:104` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-1585 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:106` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-1586 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:161` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-1587 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:172` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-1588 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md:265` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-1589 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:15` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1590 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:15` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1591 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:15` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1592 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:15` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1593 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-1594 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1595 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `#464` | …* Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1596 | c | BP-03 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1597 | c | BP-03 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1598 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-1599 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-1600 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-1601 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-1602 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:17` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-1603 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:23` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-1604 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:29` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-1605 | b | CT-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:70` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-1606 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:83` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-1607 | b | CT-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:100` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-1608 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:123` | `<!--` | <!-- bl-156: by-test --> |
| V-1609 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:123` | `by-test` | <!-- bl-156: by-test --> |
| V-1610 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:124` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1611 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:124` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1612 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:126` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1613 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:126` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1614 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:126` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1615 | c | BP-07 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:128` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1616 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:129` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1617 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:129` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1618 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:130` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1619 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:131` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1620 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:132` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1621 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:133` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1622 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:144` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1623 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:184` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1624 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:187` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1625 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:187` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1626 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:210` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1627 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:210` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1628 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:210` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1629 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:238` | `<!--` | <!-- /bl-156: by-test --> |
| V-1630 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md:238` | `by-test` | <!-- /bl-156: by-test --> |
| V-1631 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:17` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1632 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:17` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1633 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:17` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1634 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:17` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-1635 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1636 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1637 | c | BP-03 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1638 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-1639 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1640 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1641 | c | BP-08 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-1642 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:19` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-1643 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:27` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-1644 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:46` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-1645 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:47` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-1646 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:73` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-1647 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:73` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-1648 | b | CT-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1649 | b | CT-05 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1650 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1651 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1652 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1653 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1654 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:74` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-1655 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:75` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1656 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:75` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1657 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:75` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1658 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:75` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1659 | b | CT-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:75` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-1660 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:89` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-1661 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:92` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-1662 | b | CT-03 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:110` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-1663 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:158` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-1664 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:169` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-1665 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:262` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-1666 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:264` | `<!--` | <!-- bl-156: by-test --> |
| V-1667 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:264` | `by-test` | <!-- bl-156: by-test --> |
| V-1668 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:265` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1669 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:265` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-1670 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:267` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1671 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:267` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1672 | c | BP-09 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:267` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-1673 | c | BP-07 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:269` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-1674 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:270` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1675 | c | BP-02 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:270` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-1676 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:271` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-1677 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:272` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-1678 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:273` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-1679 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:274` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-1680 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:285` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-1681 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:302` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-1682 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:306` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-1683 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:332` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-1684 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:335` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1685 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:335` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-1686 | c | BP-04 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:358` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1687 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:358` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1688 | c | BP-10 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:358` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-1689 | c | BP-01 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:446` | `<!--` | <!-- /bl-156: by-test --> |
| V-1690 | c | BP-06 | `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md:446` | `by-test` | <!-- /bl-156: by-test --> |
| V-1691 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1692 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:15` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1693 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1694 | b | CT-04 | `standards/bcreq-manual-classes/01-intake.md:96` | `ВАТС` | …кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк… |
| V-1695 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:141` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1696 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:142` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1697 | a | A-RELATIVE | `standards/bcreq-manual-classes/01-intake.md:143` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1698 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1699 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:15` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1700 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1701 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1702 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1703 | a | A-RELATIVE | `standards/bcreq-manual-classes/02-normalize.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1704 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1705 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:15` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1706 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1707 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:147` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1708 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:148` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1709 | a | A-RELATIVE | `standards/bcreq-manual-classes/03-ambiguity.md:149` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1710 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1711 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:15` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1712 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1713 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:149` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1714 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:150` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1715 | a | A-RELATIVE | `standards/bcreq-manual-classes/04-questions.md:151` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1716 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1717 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:15` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1718 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1719 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1720 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1721 | a | A-RELATIVE | `standards/bcreq-manual-classes/05-taxonomy.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1722 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1723 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:15` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1724 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1725 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:142` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1726 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:143` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1727 | a | A-RELATIVE | `standards/bcreq-manual-classes/06-scope.md:144` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1728 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1729 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:15` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1730 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1731 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:150` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1732 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:151` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1733 | a | A-RELATIVE | `standards/bcreq-manual-classes/07-web-evidence.md:152` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1734 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1735 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:15` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1736 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1737 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:151` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1738 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:152` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1739 | a | A-RELATIVE | `standards/bcreq-manual-classes/08-document-evidence.md:153` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1740 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1741 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:15` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1742 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1743 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:142` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1744 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:143` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1745 | a | A-RELATIVE | `standards/bcreq-manual-classes/09-ba-enrichment.md:144` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1746 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1747 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1748 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1749 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1750 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1751 | a | A-RELATIVE | `standards/bcreq-manual-classes/10-source-conflicts.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1752 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1753 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:15` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-1754 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1755 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:149` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1756 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:150` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1757 | a | A-RELATIVE | `standards/bcreq-manual-classes/11-dependency-check.md:151` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1758 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1759 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:15` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-1760 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1761 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1762 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1763 | a | A-RELATIVE | `standards/bcreq-manual-classes/12-phase-assembly.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1764 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1765 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:15` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1766 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1767 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1768 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1769 | a | A-RELATIVE | `standards/bcreq-manual-classes/13-handoff-check.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1770 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1771 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:15` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1772 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1773 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:145` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1774 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:146` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1775 | a | A-RELATIVE | `standards/bcreq-manual-classes/14-glossary.md:147` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1776 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1777 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:15` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-1778 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1779 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1780 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1781 | a | A-RELATIVE | `standards/bcreq-manual-classes/15-business-context.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1782 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-1783 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:15` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-1784 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1785 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:147` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1786 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:148` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1787 | a | A-RELATIVE | `standards/bcreq-manual-classes/16-fr-delta.md:149` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1788 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-1789 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:15` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-1790 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1791 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1792 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1793 | a | A-RELATIVE | `standards/bcreq-manual-classes/17-fr-new.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1794 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-1795 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:15` | `../../prompts/bcreq-nfr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-1796 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1797 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:147` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1798 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:148` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1799 | a | A-RELATIVE | `standards/bcreq-manual-classes/18-nfr.md:149` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1800 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-1801 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:15` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-1802 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1803 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1804 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1805 | a | A-RELATIVE | `standards/bcreq-manual-classes/19-uc-coverage.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1806 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1807 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1808 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1809 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:147` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1810 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:148` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1811 | a | A-RELATIVE | `standards/bcreq-manual-classes/20-gate-evidence.md:149` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1812 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-1813 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:15` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-1814 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1815 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:145` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1816 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:146` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1817 | a | A-RELATIVE | `standards/bcreq-manual-classes/21-solution-l1.md:147` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1818 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-1819 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:15` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-1820 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1821 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:145` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1822 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:146` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1823 | a | A-RELATIVE | `standards/bcreq-manual-classes/22-solution-l2.md:147` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1824 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-1825 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:15` | `../../prompts/bcreq-constraints-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-1826 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1827 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1828 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1829 | a | A-RELATIVE | `standards/bcreq-manual-classes/23-constraints.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1830 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-1831 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:15` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-1832 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1833 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:139` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1834 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:140` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1835 | a | A-RELATIVE | `standards/bcreq-manual-classes/24-uc-boundaries.md:141` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1836 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1837 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:15` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1838 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1839 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:151` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1840 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:152` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1841 | a | A-RELATIVE | `standards/bcreq-manual-classes/25-risks.md:153` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1842 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1843 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:15` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1844 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1845 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1846 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1847 | a | A-RELATIVE | `standards/bcreq-manual-classes/26-delivery-dependencies.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1848 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1849 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:15` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-1850 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1851 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:150` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1852 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:151` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1853 | a | A-RELATIVE | `standards/bcreq-manual-classes/27-acceptance.md:152` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1854 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1855 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1856 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1857 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:150` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1858 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:151` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1859 | a | A-RELATIVE | `standards/bcreq-manual-classes/28-independent-review.md:152` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1860 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1861 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1862 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1863 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:141` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1864 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:142` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1865 | a | A-RELATIVE | `standards/bcreq-manual-classes/29-impact.md:143` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1866 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1867 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1868 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1869 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:148` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1870 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:149` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1871 | a | A-RELATIVE | `standards/bcreq-manual-classes/30-targeted-edit.md:150` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1872 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-1873 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:15` | `../../prompts/bcreq-core-documentation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-1874 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1875 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:145` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1876 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:146` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1877 | a | A-RELATIVE | `standards/bcreq-manual-classes/31-conformance.md:147` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1878 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-1879 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:15` | `../../prompts/letter-customer-documentation-legacy.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-1880 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1881 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:141` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1882 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:142` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1883 | a | A-RELATIVE | `standards/bcreq-manual-classes/32-audience-projection.md:143` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1884 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1885 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1886 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1887 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:145` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1888 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:146` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1889 | a | A-RELATIVE | `standards/bcreq-manual-classes/33-release-audit.md:147` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1890 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1891 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:15` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1892 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1893 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:158` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1894 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:159` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1895 | a | A-RELATIVE | `standards/bcreq-manual-classes/34-human-record.md:160` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1896 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1897 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:15` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1898 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1899 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:147` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1900 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:148` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1901 | a | A-RELATIVE | `standards/bcreq-manual-classes/35-baseline-handover.md:149` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1902 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1903 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:15` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-1904 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1905 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1906 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1907 | a | A-RELATIVE | `standards/bcreq-manual-classes/36-rule-bundle.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1908 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-1909 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:15` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-1910 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1911 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:150` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1912 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:151` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1913 | a | A-RELATIVE | `standards/bcreq-manual-classes/37-user-story.md:152` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1914 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-1915 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:15` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-1916 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1917 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:150` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1918 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:151` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1919 | a | A-RELATIVE | `standards/bcreq-manual-classes/38-requested-uc.md:152` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1920 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:15` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1921 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:15` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-1922 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:25` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-1923 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:146` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-1924 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:147` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-1925 | a | A-RELATIVE | `standards/bcreq-manual-classes/39-manifest-alignment.md:148` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-1926 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-common.md:15` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-1927 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-common.md:41` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-1928 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-common.md:42` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-1929 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-common.md:43` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-1930 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-common.md:44` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-1931 | b | CT-01 | `docs/ba-processes/bcreq-a-in-common.md:143` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1932 | b | CT-02 | `docs/ba-processes/bcreq-a-in-common.md:143` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1933 | a | A-PRIVATE | `docs/ba-processes/bcreq-step-handoff.md:7 (frontmatter)` | `mango_ba_prompts` | issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/490 |
| V-1934 | b | CT-03 | `docs/ba-processes/bcreq-step-handoff.md:119` | `коннектора` | …понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем. \| карта компонентов-кандидатов \| те… |
| V-1935 | b | CT-05 | `docs/ba-processes/bcreq-step-handoff.md:119` | `ЛК` | …ов-кандидатов \| технический \| у каждой связи есть источник; ЛК, права и настройки рассмотрены \| AIN-07 \|… |
| V-1936 | b | CT-03 | `docs/ba-processes/bcreq-a-in-route.json:167` | `коннектора` | "why": "Новизна коннектора не отменяет дельту существующих подсистем", |
| V-1937 | b | CT-05 | `docs/ba-processes/bcreq-a-in-route.json:168` | `ЛК` | "checks": "У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторо… |
| V-1938 | a | A-PRIVATE | `docs/ba-processes/bcreq-a-in-route.json:724` | `mango_ba_prompts` | "decision": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/474" |
| V-1939 | b | CT-05 | `docs/ba-processes/bcreq-a-in-instructions.json:28` | `ЛК` | … → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст… |
| V-1940 | b | CT-03 | `docs/ba-processes/bcreq-a-in-instructions.json:30` | `коннектор` | "negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие." |
| V-1941 | b | CT-05 | `docs/ba-processes/bcreq-a-in-instructions.json:30` | `ЛК` | "negative_example": "Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие." |
| V-1942 | b | CT-01 | `docs/ba-processes/bcreq-a-in-instructions.json:60` | `amoCRM` | "negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»." |
| V-1943 | b | CT-06 | `docs/ba-processes/bcreq-a-in-instructions.json:60` | `HDE` | "negative_example": "Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет»." |
| V-1944 | b | CT-01 | `docs/ba-processes/bcreq-evidence-normalization.md:45` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1945 | b | CT-02 | `docs/ba-processes/bcreq-evidence-normalization.md:45` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-1946 | a | A-PRIVATE | `prompts/README.md:9 (frontmatter)` | `mango_ba_prompts` | - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/65" |
| V-1947 | a | A-PRIVATE | `prompts/README.md:26` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md> |
| V-1948 | a | A-PRIVATE | `prompts/README.md:28` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md>. |
| V-1949 | a | A-PRIVATE | `prompts/README.md:34` | `mango_ba_prompts` | …itution-governance-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) (Промпт 0), з… |
| V-1950 | a | A-PRIVATE | `prompts/README.md:35` | `mango_ba_prompts` | …ext-understanding-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) или [`bcreq-in… |
| V-1951 | a | A-PRIVATE | `prompts/README.md:36` | `mango_ba_prompts` | …s-impact-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \|… |
| V-1952 | a | A-PRIVATE | `prompts/README.md:37` | `mango_ba_prompts` | …scenarios-modeling-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) (`тип: US \\| UC`) … |
| V-1953 | a | A-PRIVATE | `prompts/README.md:38` | `mango_ba_prompts` | …-fr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) или [`bcreq-core-do… |
| V-1954 | a | A-PRIVATE | `prompts/README.md:39` | `mango_ba_prompts` | …nfr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-1955 | a | A-PRIVATE | `prompts/README.md:40` | `mango_ba_prompts` | …-review-validation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-1956 | a | A-PRIVATE | `prompts/README.md:41` | `mango_ba_prompts` | …nts-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-1957 | a | A-PRIVATE | `prompts/README.md:42` | `mango_ba_prompts` | …r-solution-design-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) или [`bcreq-work… |
| V-1958 | a | A-PRIVATE | `prompts/README.md:43` | `mango_ba_prompts` | …tra-risk-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-1959 | a | A-PRIVATE | `prompts/README.md:44` | `mango_ba_prompts` | \| Нужно обработать ASR-расшифровку \| [`asr-ingestion-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) \| |
| V-1960 | a | A-PRIVATE | `prompts/README.md:45` | `mango_ba_prompts` | …mer-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) или [`meeti… |
| V-1961 | a | A-PRIVATE | `prompts/README.md:46` | `mango_ba_prompts` | …ebug-documentation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) \|… |
| V-1962 | a | A-PRIVATE | `prompts/README.md:52` | `mango_ba_prompts` | [архитектура промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md), |
| V-1963 | a | A-PRIVATE | `prompts/README.md:53` | `mango_ba_prompts` | [композиция документа]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md), |
| V-1964 | a | A-PRIVATE | `prompts/README.md:54` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-1965 | a | A-PRIVATE | `prompts/README.md:65` | `mango_ba_prompts` | [на сайте, вкладка «Процессы»]\(https://g-ivan-a.github.io/mango_ba_prompts/#processes); |
| V-1966 | a | A-PRIVATE | `prompts/README.md:67` | `mango_ba_prompts` | [`docs/ba-processes/bcreq-manual-process.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md). |
| V-1967 | a | A-PRIVATE | `prompts/README.md:74` | `mango_ba_prompts` | …itution-governance-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) \| [`bcreq-con… |
| V-1968 | a | A-PRIVATE | `prompts/README.md:75` | `mango_ba_prompts` | …ext-understanding-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) \| [`bcreq-in-u… |
| V-1969 | a | A-PRIVATE | `prompts/README.md:76` | `mango_ba_prompts` | …s-impact-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \| A-IN \| Г-… |
| V-1970 | a | A-PRIVATE | `prompts/README.md:77` | `mango_ba_prompts` | …-fr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \| [`bcreq-core-docu… |
| V-1971 | a | A-PRIVATE | `prompts/README.md:78` | `mango_ba_prompts` | …nfr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \| A-CORE \| — \|… |
| V-1972 | a | A-PRIVATE | `prompts/README.md:79` | `mango_ba_prompts` | …bcreq-uc-modeling-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 1`) \| A-CORE \|… |
| V-1973 | a | A-PRIVATE | `prompts/README.md:80` | `mango_ba_prompts` | …r-solution-design-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \| [`bcreq-work-s… |
| V-1974 | a | A-PRIVATE | `prompts/README.md:81` | `mango_ba_prompts` | …nts-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \| A-WORK \|… |
| V-1975 | a | A-PRIVATE | `prompts/README.md:82` | `mango_ba_prompts` | …bcreq-uc-modeling-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) (`прогон: 2`) \| A-WORK \|… |
| V-1976 | a | A-PRIVATE | `prompts/README.md:83` | `mango_ba_prompts` | …tra-risk-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \| A-WORK \| — \|… |
| V-1977 | a | A-PRIVATE | `prompts/README.md:84` | `mango_ba_prompts` | …-review-validation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \| [`bcreq-review-va… |
| V-1978 | a | A-PRIVATE | `prompts/README.md:85` | `mango_ba_prompts` | …scenarios-modeling-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) (`тип: US \\| UC`) … |
| V-1979 | a | A-PRIVATE | `prompts/README.md:98` | `mango_ba_prompts` | [GitHub Pages]\(https://g-ivan-a.github.io/mango_ba_prompts/). Колонка |
| V-1980 | a | A-PRIVATE | `prompts/README.md:102` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md> |
| V-1981 | a | A-PRIVATE | `prompts/README.md:112` | `mango_ba_prompts` | …itution-governance-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md) \| BCREQ Ш-0: … |
| V-1982 | a | A-PRIVATE | `prompts/README.md:113` | `mango_ba_prompts` | …ext-understanding-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) \| BCREQ Ш-1: г… |
| V-1983 | a | A-PRIVATE | `prompts/README.md:114` | `mango_ba_prompts` | …s-impact-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \| BCREQ Ш-2… |
| V-1984 | a | A-PRIVATE | `prompts/README.md:115` | `mango_ba_prompts` | …-fr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \| BCREQ Ш-3: функци… |
| V-1985 | a | A-PRIVATE | `prompts/README.md:116` | `mango_ba_prompts` | …nfr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \| BCREQ Ш-4: нефун… |
| V-1986 | a | A-PRIVATE | `prompts/README.md:117` | `mango_ba_prompts` | …bcreq-uc-modeling-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \| BCREQ Ш-5/Ш-8: UC \| `m… |
| V-1987 | a | A-PRIVATE | `prompts/README.md:118` | `mango_ba_prompts` | …r-solution-design-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \| BCREQ Ш-6 (2.6… |
| V-1988 | a | A-PRIVATE | `prompts/README.md:119` | `mango_ba_prompts` | …nts-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \| BCREQ Ш-… |
| V-1989 | a | A-PRIVATE | `prompts/README.md:120` | `mango_ba_prompts` | …tra-risk-analysis-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \| BCREQ Ш-9 (2.1… |
| V-1990 | a | A-PRIVATE | `prompts/README.md:121` | `mango_ba_prompts` | …-review-validation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \| BCREQ Ш-В: валида… |
| V-1991 | a | A-PRIVATE | `prompts/README.md:122` | `mango_ba_prompts` | …scenarios-modeling-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \| BCREQ Ш-С (2.12/… |
| V-1992 | a | A-PRIVATE | `prompts/README.md:123` | `mango_ba_prompts` | …q-in-understanding-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) \| BCREQ A-IN: контек… |
| V-1993 | a | A-PRIVATE | `prompts/README.md:124` | `mango_ba_prompts` | …core-documentation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) \| BCREQ A-CORE: ФТ… |
| V-1994 | a | A-PRIVATE | `prompts/README.md:125` | `mango_ba_prompts` | …rk-solution-design-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) \| BCREQ A-WORK: … |
| V-1995 | a | A-PRIVATE | `prompts/README.md:131` | `mango_ba_prompts` | \| [`asr-ingestion-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-oneshot.md) \| ASR: Нормализация транскрипц… |
| V-1996 | a | A-PRIVATE | `prompts/README.md:132` | `mango_ba_prompts` | \| [`asr-ingestion-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/asr-ingestion-legacy.md) \| ASR: Обработка транскрипции (у… |
| V-1997 | a | A-PRIVATE | `prompts/README.md:148` | `mango_ba_prompts` | …mer-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-customer-documentation-stepwise.md) \| Встреча с… |
| V-1998 | a | A-PRIVATE | `prompts/README.md:149` | `mango_ba_prompts` | …eam-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/meeting-team-documentation-stepwise.md) \| Встреча коман… |
| V-1999 | a | A-PRIVATE | `prompts/README.md:150` | `mango_ba_prompts` | …tomer-documentation-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/letter-customer-documentation-legacy.md) \| Письмо клиен… |
| V-2000 | a | A-PRIVATE | `prompts/README.md:156` | `mango_ba_prompts` | …ebug-documentation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/session-debug-documentation-oneshot.md) \| Сессия LLM: С… |
| V-2001 | a | A-PRIVATE | `prompts/README.md:162` | `mango_ba_prompts` | …`tz-stats-generator-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-legacy.md) \| ТЗ: Статистика,… |
| V-2002 | a | A-PRIVATE | `prompts/README.md:163` | `mango_ba_prompts` | …ts-generator-simple-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/tz-stats-generator-simple-legacy.md) \| ТЗ: Стат… |
| V-2003 | a | A-PRIVATE | `prompts/README.md:164` | `mango_ba_prompts` | …-stepwise-generator-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md) \| Use Cas… |
| V-2004 | a | A-PRIVATE | `prompts/README.md:165` | `mango_ba_prompts` | …se-generator-simple-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-simple-legacy.md) \| … |
| V-2005 | a | A-PRIVATE | `prompts/README.md:166` | `mango_ba_prompts` | …ser-story-generator-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md) \| User Story: Г… |
| V-2006 | a | A-PRIVATE | `prompts/README.md:167` | `mango_ba_prompts` | …ry-generator-simple-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-simple-legacy.md) \| User S… |
| V-2007 | a | A-PRIVATE | `prompts/README.md:176` | `mango_ba_prompts` | …ints-documentation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/constraints-documentation-oneshot.md) \| Огранич… |
| V-2008 | a | A-PRIVATE | `prompts/README.md:177` | `mango_ba_prompts` | …nts-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/constraints-documentation-stepwise.md) \| Ограни… |
| V-2009 | a | A-PRIVATE | `prompts/README.md:178` | `mango_ba_prompts` | …[`fr-documentation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-oneshot.md) \| ФТ: Генерация за… |
| V-2010 | a | A-PRIVATE | `prompts/README.md:179` | `mango_ba_prompts` | …`fr-documentation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-stepwise.md) \| ФТ: Генерация т… |
| V-2011 | a | A-PRIVATE | `prompts/README.md:180` | `mango_ba_prompts` | \| [`fr-validation-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-legacy.md) \| ФТ: Валидация (устарев… |
| V-2012 | a | A-PRIVATE | `prompts/README.md:181` | `mango_ba_prompts` | \| [`fr-validation-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-oneshot.md) \| ФТ: Экспресс-валидац… |
| V-2013 | a | A-PRIVATE | `prompts/README.md:182` | `mango_ba_prompts` | \| [`fr-validation-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-stepwise.md) \| ФТ: Валидация и ау… |
| V-2014 | a | A-PRIVATE | `prompts/README.md:183` | `mango_ba_prompts` | …text-understanding-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-oneshot.md) \| Ко… |
| V-2015 | a | A-PRIVATE | `prompts/README.md:184` | `mango_ba_prompts` | …ext-understanding-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-stepwise.md) \| К… |
| V-2016 | a | A-PRIVATE | `prompts/README.md:185` | `mango_ba_prompts` | …tomer-understanding-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/questions-customer-understanding-legacy.md) \| В… |
| V-2017 | a | A-PRIVATE | `prompts/README.md:186` | `mango_ba_prompts` | …mer-understanding-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/questions-customer-understanding-stepwise.md) \|… |
| V-2018 | a | A-PRIVATE | `prompts/README.md:187` | `mango_ba_prompts` | …ils-solution-design-legacy.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-legacy.md) \| … |
| V-2019 | a | A-PRIVATE | `prompts/README.md:188` | `mango_ba_prompts` | …ls-solution-design-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-oneshot.md) \|… |
| V-2020 | a | A-PRIVATE | `prompts/README.md:189` | `mango_ba_prompts` | …s-solution-design-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/technical-details-solution-design-stepwise.md) … |
| V-2021 | a | A-PRIVATE | `prompts/README.md:190` | `mango_ba_prompts` | \| [`uc-modeling-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/uc-modeling-oneshot.md) \| Use Case: Моделирование … |
| V-2022 | a | A-PRIVATE | `prompts/README.md:191` | `mango_ba_prompts` | \| [`uc-modeling-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/uc-modeling-stepwise.md) \| Use Case: Моделировани… |
| V-2023 | a | A-PRIVATE | `prompts/README.md:192` | `mango_ba_prompts` | \| [`us-modeling-oneshot.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/us-modeling-oneshot.md) \| User Story: Формирование… |
| V-2024 | a | A-PRIVATE | `prompts/README.md:193` | `mango_ba_prompts` | \| [`us-modeling-stepwise.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/us-modeling-stepwise.md) \| User Story: Формирован… |
| V-2025 | a | A-PRIVATE | `prompts/README.md:197` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>. |
| V-2026 | a | A-PRIVATE | `prompts/README.md:230` | `mango_ba_prompts` | - <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/user-story-generator-legacy.md> |
| V-2027 | a | A-PRIVATE | `prompts/README.md:231` | `mango_ba_prompts` | - <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/usecase-stepwise-generator-legacy.md> |
| V-2028 | a | A-PRIVATE | `prompts/README.md:261` | `mango_ba_prompts` | - <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/glossary-context-understanding-stepwise.md> |
| V-2029 | a | A-PRIVATE | `prompts/README.md:262` | `mango_ba_prompts` | - <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-documentation-stepwise.md> |
| V-2030 | a | A-PRIVATE | `prompts/README.md:263` | `mango_ba_prompts` | - <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/fr-validation-oneshot.md> |
| V-2031 | a | A-PRIVATE | `prompts/README.md:300` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml>. |
| V-2032 | a | A-PRIVATE | `prompts/README.md:336` | `mango_ba_prompts` | [GitHub Pages]\(https://g-ivan-a.github.io/mango_ba_prompts/). Данные формируются |
| V-2033 | a | A-PRIVATE | `prompts/README.md:350` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md>. |
| V-2034 | a | A-PRIVATE | `prompts/README.md:356` | `mango_ba_prompts` | <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md>. |
| V-2035 | a | A-PRIVATE | `prompts/README.md:378` | `mango_ba_prompts` | - Репозиторий: <https://github.com/G-Ivan-A/mango_ba_prompts> |
| V-2036 | a | A-PRIVATE | `prompts/README.md:379` | `mango_ba_prompts` | - Таксономия 13 операций: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md> |
| V-2037 | a | A-PRIVATE | `prompts/README.md:380` | `mango_ba_prompts` | - Процессы БА и маппинг: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md> |
| V-2038 | a | A-PRIVATE | `prompts/README.md:381` | `mango_ba_prompts` | - Стандарт промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/prompt-standard.md> |
| V-2039 | a | A-PRIVATE | `prompts/README.md:382` | `mango_ba_prompts` | - ADR-001 по стандарту промптов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/adr/001-prompt-standard.md> |
| V-2040 | a | A-PRIVATE | `prompts/README.md:383` | `mango_ba_prompts` | - Структура паттернов: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md> |
| V-2041 | a | A-PRIVATE | `prompts/README.md:384` | `mango_ba_prompts` | - Шаблон фидбека: <https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/.github/ISSUE_TEMPLATE/prompt-feedback.yml> |
| V-2042 | a | A-PRIVATE | `prompts/README.md:385` | `mango_ba_prompts` | - PR #57: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/57> |
| V-2043 | a | A-PRIVATE | `prompts/README.md:386` | `mango_ba_prompts` | - PR #59: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/59> |
| V-2044 | a | A-PRIVATE | `prompts/README.md:387` | `mango_ba_prompts` | - PR #60: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/60> |
| V-2045 | a | A-PRIVATE | `prompts/README.md:388` | `mango_ba_prompts` | - Issue #61: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/61> |
| V-2046 | a | A-PRIVATE | `prompts/README.md:389` | `mango_ba_prompts` | - Issue #62: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/62> |
| V-2047 | a | A-PRIVATE | `prompts/README.executable.md:10 (frontmatter)` | `mango_ba_prompts` | related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125" |
| V-2048 | a | A-PRIVATE | `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md:10 (frontmatter)` | `mango_ba_prompts` | related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125" |
| V-2049 | a | A-PRIVATE | `prompts/AI_SESSION_HANDOVER_PROMPT.executable.md:35` | `mango_ba_prompts` | контекста — репозиторий mango_ba_prompts (HTOM-команда, модель hub-and-spoke); |
| V-2050 | a | A-PRIVATE | `prompts/archive/a-in-v2.7.0/manifest.json:6` | `mango_ba_prompts` | "url": "https://g-ivan-a.github.io/mango_ba_prompts/", |
| V-2051 | a | A-PRIVATE | `prompts/drafts/manifest.json:2` | `mango_ba_prompts` | "source_issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/438", |
| V-2052 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2053 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2054 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2055 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2056 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2057 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2058 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2059 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2060 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2061 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2062 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2063 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2064 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2065 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2066 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2067 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2068 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2069 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2070 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2071 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2072 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2073 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2074 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2075 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2076 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2077 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2078 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2079 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2080 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2081 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2082 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2083 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2084 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2085 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2086 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2087 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2088 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2089 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2090 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2091 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2092 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2093 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2094 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2095 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2096 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2097 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2098 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2099 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2100 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2101 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2102 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2103 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2104 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2105 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2106 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2107 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2108 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2109 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2110 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2111 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2112 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2113 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2114 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2115 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2116 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2117 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2118 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2119 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2120 | c | BP-04 | `site/data/a-in-kit.json:265 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2121 | c | BP-01 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2122 | c | BP-02 | `site/data/a-in-kit.json:269 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2123 | c | BP-01 | `site/data/a-in-kit.json:290 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2124 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2125 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2126 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2127 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2128 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2129 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2130 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2131 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2132 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2133 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2134 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2135 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2136 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2137 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2138 | c | BP-04 | `site/data/a-in-kit.json:265 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2139 | c | BP-01 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2140 | c | BP-02 | `site/data/a-in-kit.json:269 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2141 | c | BP-01 | `site/data/a-in-kit.json:290 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2142 | b | CT-03 | `site/data/a-in-kit.json:1 (steps[].why)` | `коннектора` | Новизна коннектора не отменяет дельту существующих подсистем |
| V-2143 | b | CT-05 | `site/data/a-in-kit.json:1 (steps[].checks)` | `ЛК` | У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим… |
| V-2144 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2145 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2146 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2147 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2148 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2149 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2150 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2151 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2152 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2153 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2154 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2155 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2156 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2157 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2158 | b | CT-03 | `site/data/a-in-kit.json:220 (steps[].prompt)` | `коннектора` | - Зачем: Новизна коннектора не отменяет дельту существующих подсистем. |
| V-2159 | b | CT-05 | `site/data/a-in-kit.json:229 (steps[].prompt)` | `ЛК` | … → источник. Отдельно прямые, опорные и внешние компоненты; ЛК, права, настройки, хранение, события, интерфейсы, лицензии. Определи поставку и ответст… |
| V-2160 | b | CT-05 | `site/data/a-in-kit.json:237 (steps[].prompt)` | `ЛК` | У каждой связи есть источник и статус candidate; ЛК/права/настройки рассмотрены; Отдельно определены объект поставки, ответственность сторон и зависим… |
| V-2161 | b | CT-03 | `site/data/a-in-kit.json:248 (steps[].prompt)` | `коннектор` | Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие. |
| V-2162 | b | CT-05 | `site/data/a-in-kit.json:248 (steps[].prompt)` | `ЛК` | Контрпример: Новый коннектор не отменяет дельту ЛК. Исключённый компонент с зависимостью остаётся в графе; это не само по себе противоречие. |
| V-2163 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2164 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2165 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2166 | b | CT-05 | `site/data/a-in-kit.json:281 (steps[].prompt)` | `ЛК` | …технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта … |
| V-2167 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2168 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2169 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2170 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2171 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2172 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2173 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2174 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2175 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2176 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2177 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2178 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2179 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2180 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2181 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2182 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2183 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2184 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2185 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2186 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2187 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2188 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2189 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2190 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2191 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2192 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2193 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2194 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2195 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2196 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2197 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2198 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2199 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2200 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2201 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2202 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2203 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2204 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2205 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2206 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2207 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2208 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2209 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2210 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2211 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2212 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2213 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2214 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2215 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2216 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2217 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2218 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2219 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2220 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2221 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2222 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2223 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2224 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2225 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2226 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2227 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2228 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2229 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2230 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2231 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2232 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2233 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2234 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2235 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2236 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2237 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2238 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2239 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2240 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2241 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2242 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2243 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2244 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2245 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2246 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2247 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2248 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2249 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2250 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2251 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2252 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2253 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2254 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2255 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2256 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2257 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2258 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2259 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2260 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2261 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2262 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2263 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2264 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2265 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2266 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2267 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2268 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2269 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2270 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2271 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2272 | b | CT-01 | `site/data/a-in-kit.json:248 (steps[].prompt)` | `amoCRM` | Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет». |
| V-2273 | b | CT-06 | `site/data/a-in-kit.json:248 (steps[].prompt)` | `HDE` | Контрпример: Прочитанная цитата не означает «Да» по исполнимости. Аналогия amoCRM не доказывает полный HDE-сценарий. Нет evidence — не «Нет». |
| V-2274 | c | BP-04 | `site/data/a-in-kit.json:265 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2275 | c | BP-01 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2276 | c | BP-02 | `site/data/a-in-kit.json:269 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2277 | c | BP-01 | `site/data/a-in-kit.json:290 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2278 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2279 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2280 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2281 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2282 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2283 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2284 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2285 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2286 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2287 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2288 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2289 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2290 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2291 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2292 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2293 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2294 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2295 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2296 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2297 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2298 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2299 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2300 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2301 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2302 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2303 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2304 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2305 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2306 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2307 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2308 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2309 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2310 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2311 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2312 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2313 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2314 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2315 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2316 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2317 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2318 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2319 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2320 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2321 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2322 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2323 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2324 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2325 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2326 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2327 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2328 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2329 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2330 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2331 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2332 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2333 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2334 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2335 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2336 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2337 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2338 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2339 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2340 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2341 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2342 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2343 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2344 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2345 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2346 | c | BP-04 | `site/data/a-in-kit.json:265 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2347 | c | BP-01 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2348 | c | BP-02 | `site/data/a-in-kit.json:269 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2349 | c | BP-01 | `site/data/a-in-kit.json:290 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2350 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2351 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2352 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2353 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2354 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2355 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2356 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2357 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2358 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2359 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2360 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2361 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2362 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2363 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2364 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2365 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2366 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2367 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2368 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2369 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2370 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2371 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2372 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2373 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2374 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2375 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2376 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2377 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2378 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2379 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2380 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2381 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2382 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2383 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2384 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2385 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2386 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2387 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2388 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2389 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2390 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2391 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2392 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2393 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2394 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2395 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2396 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2397 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2398 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2399 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2400 | c | BP-04 | `site/data/a-in-kit.json:264 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2401 | c | BP-01 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2402 | c | BP-02 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2403 | c | BP-01 | `site/data/a-in-kit.json:289 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2404 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2405 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2406 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2407 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2408 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2409 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2410 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2411 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2412 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2413 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2414 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2415 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2416 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2417 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2418 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2419 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2420 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2421 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2422 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2423 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2424 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2425 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2426 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2427 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2428 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2429 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2430 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2431 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2432 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2433 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2434 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2435 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2436 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2437 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2438 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2439 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2440 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2441 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2442 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2443 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2444 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2445 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2446 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2447 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2448 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2449 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2450 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2451 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2452 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2453 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2454 | c | BP-04 | `site/data/a-in-kit.json:265 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2455 | c | BP-01 | `site/data/a-in-kit.json:268 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2456 | c | BP-02 | `site/data/a-in-kit.json:269 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2457 | c | BP-01 | `site/data/a-in-kit.json:290 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2458 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2459 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2460 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2461 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2462 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2463 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2464 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2465 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2466 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2467 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2468 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2469 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2470 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2471 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2472 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2473 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2474 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2475 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2476 | a | A-PRIVATE | `site/data/a-in-kit.json:13 (steps[].prompt)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2477 | c | BP-01 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2478 | c | BP-08 | `site/data/a-in-kit.json:13 (steps[].prompt)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet --> |
| V-2479 | c | BP-08 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `Draft для` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2480 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `эффективность модели` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2481 | c | BP-09 | `site/data/a-in-kit.json:17 (steps[].prompt)` | `не измерен` | Draft для ручной проверки БА; эффективность модели не измерена. |
| V-2482 | a | A-PRIVATE | `site/data/a-in-kit.json:25 (steps[].prompt)` | `mango_ba_prompts` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2483 | c | BP-02 | `site/data/a-in-kit.json:25 (steps[].prompt)` | `#490` | Решение БА по техническому шагу (#490, [итог шага]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)): |
| V-2484 | a | A-PRIVATE | `site/data/a-in-kit.json:51 (steps[].prompt)` | `mango_ba_prompts` | - [Ш-0: полная конституция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md). |
| V-2485 | a | A-PRIVATE | `site/data/a-in-kit.json:52 (steps[].prompt)` | `mango_ba_prompts` | - [Мета-стандарты 1…8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-2486 | a | A-PRIVATE | `site/data/a-in-kit.json:53 (steps[].prompt)` | `mango_ba_prompts` | - [Маршрут и решения RFC-AIN-001]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md). |
| V-2487 | a | A-PRIVATE | `site/data/a-in-kit.json:54 (steps[].prompt)` | `mango_ba_prompts` | - [Runtime: версии и источники]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md). |
| V-2488 | b | CT-01 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2489 | b | CT-02 | `site/data/a-in-kit.json:153 (steps[].prompt)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-2490 | c | BP-04 | `site/data/a-in-kit.json:263 (steps[].prompt)` | `RUN-0` | …оречат или недоступны, модель выбирает сама (обратная связь RUN-0090) → Назвать обе нормы и остановиться. Порядок применения — §1.2. Граница: Порядок … |
| V-2491 | c | BP-01 | `site/data/a-in-kit.json:266 (steps[].prompt)` | `<!--` | <!-- issue-490:handoff --> |
| V-2492 | c | BP-02 | `site/data/a-in-kit.json:267 (steps[].prompt)` | `#490` | ## Итог шага для БА (#490) |
| V-2493 | c | BP-01 | `site/data/a-in-kit.json:288 (steps[].prompt)` | `<!--` | <!-- /issue-490:handoff --> |
| V-2494 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md |
| V-2495 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.contract.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-manual-state.md |
| V-2496 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.classes.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/README.md |
| V-2497 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/36-rule-bundle.md |
| V-2498 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/01-intake.md |
| V-2499 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/02-normalize.md |
| V-2500 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/03-ambiguity.md |
| V-2501 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/04-questions.md |
| V-2502 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/05-taxonomy.md |
| V-2503 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/06-scope.md |
| V-2504 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/07-web-evidence.md |
| V-2505 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/08-document-evidence.md |
| V-2506 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/09-ba-enrichment.md |
| V-2507 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/10-source-conflicts.md |
| V-2508 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/11-dependency-check.md |
| V-2509 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/37-user-story.md |
| V-2510 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/38-requested-uc.md |
| V-2511 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/14-glossary.md |
| V-2512 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/15-business-context.md |
| V-2513 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/34-human-record.md |
| V-2514 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/39-manifest-alignment.md |
| V-2515 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/12-phase-assembly.md |
| V-2516 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/13-handoff-check.md |
| V-2517 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/20-gate-evidence.md |
| V-2518 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/16-fr-delta.md |
| V-2519 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/17-fr-new.md |
| V-2520 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/18-nfr.md |
| V-2521 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/19-uc-coverage.md |
| V-2522 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/28-independent-review.md |
| V-2523 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/29-impact.md |
| V-2524 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/30-targeted-edit.md |
| V-2525 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/31-conformance.md |
| V-2526 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/21-solution-l1.md |
| V-2527 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/22-solution-l2.md |
| V-2528 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/23-constraints.md |
| V-2529 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/24-uc-boundaries.md |
| V-2530 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/25-risks.md |
| V-2531 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/26-delivery-dependencies.md |
| V-2532 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/27-acceptance.md |
| V-2533 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/32-audience-projection.md |
| V-2534 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/33-release-audit.md |
| V-2535 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (manual.steps[].prompt.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/35-baseline-handover.md |
| V-2536 | a | A-PRIVATE | `site/data/bcreq-flow.json:1 (approval.contract.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md |
| V-2537 | a | A-PRIVATE | `site/data/checks.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/ |
| V-2538 | a | A-PRIVATE | `site/data/checks.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/pr-ops/prompt-feedback.json |
| V-2539 | a | A-PRIVATE | `site/data/patterns.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md |
| V-2540 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/glossary-context-generation/ |
| V-2541 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2542 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2543 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/asr-ingestion/ |
| V-2544 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/user-story-generation/ |
| V-2545 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2546 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/usecase-generation/ |
| V-2547 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2548 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2549 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-generation/ |
| V-2550 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2551 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-2552 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-validation/ |
| V-2553 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2554 | a | A-PRIVATE | `site/data/patterns.json:1 (patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/meeting-summary-generation/ |
| V-2555 | a | A-PRIVATE | `site/data/process-tree.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md |
| V-2556 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2557 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2558 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2559 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2560 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2561 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2562 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md |
| V-2563 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-2564 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2565 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2566 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2567 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2568 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-2569 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2570 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2571 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2572 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2573 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2574 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2575 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2576 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2577 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2578 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2579 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2580 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2581 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2582 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2583 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2584 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2585 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2586 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2587 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2588 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2589 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2590 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2591 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2592 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2593 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-2594 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2595 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2596 | a | A-PRIVATE | `site/data/process-tree.json:1 (processes[].subprocesses[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2597 | a | A-PRIVATE | `site/data/processes.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md |
| V-2598 | a | A-PRIVATE | `site/data/processes.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md |
| V-2599 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/asr-ingestion/ |
| V-2600 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/glossary-context-generation/ |
| V-2601 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/user-story-generation/ |
| V-2602 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/usecase-generation/ |
| V-2603 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-generation/ |
| V-2604 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-validation/ |
| V-2605 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2606 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2607 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2608 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2609 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2610 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-2611 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2612 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2613 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2614 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2615 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-validation/ |
| V-2616 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2617 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/glossary-context-generation/ |
| V-2618 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-validation/ |
| V-2619 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2620 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2621 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2622 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/glossary-context-generation/ |
| V-2623 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/user-story-generation/ |
| V-2624 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/usecase-generation/ |
| V-2625 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/fr-validation/ |
| V-2626 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2627 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2628 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2629 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2630 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2631 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/usecase-generation/ |
| V-2632 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2633 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2634 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/asr-ingestion/ |
| V-2635 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/glossary-context-generation/ |
| V-2636 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].patterns[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/meeting-summary-generation/ |
| V-2637 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2638 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2639 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2640 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2641 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2642 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2643 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2644 | a | A-PRIVATE | `site/data/processes.json:1 (processes[].prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2645 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/README.md |
| V-2646 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md |
| V-2647 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md |
| V-2648 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md |
| V-2649 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json |
| V-2650 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-manual-state.md |
| V-2651 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/01-intake.md |
| V-2652 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/02-normalize.md |
| V-2653 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/03-ambiguity.md |
| V-2654 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/04-questions.md |
| V-2655 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/05-taxonomy.md |
| V-2656 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/06-scope.md |
| V-2657 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/07-web-evidence.md |
| V-2658 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/08-document-evidence.md |
| V-2659 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/09-ba-enrichment.md |
| V-2660 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/10-source-conflicts.md |
| V-2661 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/11-dependency-check.md |
| V-2662 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/12-phase-assembly.md |
| V-2663 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/13-handoff-check.md |
| V-2664 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/14-glossary.md |
| V-2665 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/15-business-context.md |
| V-2666 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/16-fr-delta.md |
| V-2667 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/17-fr-new.md |
| V-2668 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/18-nfr.md |
| V-2669 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/19-uc-coverage.md |
| V-2670 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/20-gate-evidence.md |
| V-2671 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/21-solution-l1.md |
| V-2672 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/22-solution-l2.md |
| V-2673 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/23-constraints.md |
| V-2674 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/24-uc-boundaries.md |
| V-2675 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/25-risks.md |
| V-2676 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/26-delivery-dependencies.md |
| V-2677 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/27-acceptance.md |
| V-2678 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/28-independent-review.md |
| V-2679 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/29-impact.md |
| V-2680 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/30-targeted-edit.md |
| V-2681 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/31-conformance.md |
| V-2682 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/32-audience-projection.md |
| V-2683 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/33-release-audit.md |
| V-2684 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/34-human-record.md |
| V-2685 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/35-baseline-handover.md |
| V-2686 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/36-rule-bundle.md |
| V-2687 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/37-user-story.md |
| V-2688 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/38-requested-uc.md |
| V-2689 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/39-manifest-alignment.md |
| V-2690 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md |
| V-2691 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md |
| V-2692 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md |
| V-2693 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md |
| V-2694 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-2695 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-2696 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2697 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-2698 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-2699 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2700 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2701 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md |
| V-2702 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2703 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2704 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2705 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-2706 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2707 | a | A-PRIVATE | `site/data/prompts.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-2708 | a | A-PRIVATE | `site/data/prompts.json:1 (stateContract.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-manual-state.md |
| V-2709 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/01-intake.md |
| V-2710 | b | CT-04 | `site/data/prompts.json:1 (prompts[].descriptionLong)` | `ВАТС` | …кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк… |
| V-2711 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2712 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2713 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2714 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2715 | b | CT-04 | `site/data/prompts.json:96 (prompts[].content)` | `ВАТС` | …кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк… |
| V-2716 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2717 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2718 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2719 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2720 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2721 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2722 | b | CT-04 | `site/data/prompts.json:88 (prompts[].body)` | `ВАТС` | …кета: продукты, подключённые у Заказчика, операторы, номера ВАТС и сторонние номера, объём звонков и текстовых коммуникаций в месяц, вариант (доработк… |
| V-2723 | a | A-RELATIVE | `site/data/prompts.json:133 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2724 | a | A-RELATIVE | `site/data/prompts.json:134 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2725 | a | A-RELATIVE | `site/data/prompts.json:135 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2726 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/02-normalize.md |
| V-2727 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2728 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2729 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2730 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2731 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2732 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2733 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2734 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2735 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2736 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2737 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2738 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2739 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2740 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/03-ambiguity.md |
| V-2741 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2742 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2743 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2744 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2745 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2746 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2747 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2748 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2749 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2750 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2751 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2752 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2753 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2754 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/04-questions.md |
| V-2755 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2756 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2757 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2758 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2759 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2760 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2761 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2762 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2763 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2764 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2765 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2766 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2767 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2768 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/05-taxonomy.md |
| V-2769 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2770 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2771 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2772 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2773 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2774 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2775 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2776 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2777 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2778 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2779 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2780 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2781 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2782 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/06-scope.md |
| V-2783 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2784 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2785 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2786 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2787 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2788 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2789 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2790 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2791 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2792 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2793 | a | A-RELATIVE | `site/data/prompts.json:134 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2794 | a | A-RELATIVE | `site/data/prompts.json:135 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2795 | a | A-RELATIVE | `site/data/prompts.json:136 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2796 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/07-web-evidence.md |
| V-2797 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2798 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2799 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2800 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2801 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2802 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2803 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2804 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2805 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2806 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2807 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2808 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2809 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2810 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/08-document-evidence.md |
| V-2811 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2812 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2813 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2814 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2815 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2816 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2817 | a | A-RELATIVE | `site/data/prompts.json:153 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2818 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2819 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2820 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2821 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2822 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2823 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2824 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/09-ba-enrichment.md |
| V-2825 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2826 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2827 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2828 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2829 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2830 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2831 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2832 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2833 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2834 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2835 | a | A-RELATIVE | `site/data/prompts.json:134 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2836 | a | A-RELATIVE | `site/data/prompts.json:135 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2837 | a | A-RELATIVE | `site/data/prompts.json:136 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2838 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/10-source-conflicts.md |
| V-2839 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2840 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2841 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2842 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2843 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2844 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2845 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2846 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2847 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2848 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2849 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2850 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2851 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2852 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/11-dependency-check.md |
| V-2853 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-2854 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2855 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2856 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2857 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2858 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2859 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2860 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2861 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-products-impact-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-products-impact-analysis-stepwise.md]\(../../prompts/bcreq-products-impact-analysis-stepwise.md); |
| V-2862 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2863 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2864 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2865 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2866 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/12-phase-assembly.md |
| V-2867 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-2868 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2869 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2870 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2871 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2872 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2873 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2874 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2875 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-in-understanding-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-in-understanding-oneshot.md]\(../../prompts/bcreq-in-understanding-oneshot.md); |
| V-2876 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2877 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2878 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2879 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2880 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/13-handoff-check.md |
| V-2881 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-2882 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-2883 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-2884 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2885 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2886 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2887 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2888 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-2889 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-2890 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2891 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2892 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2893 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2894 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/14-glossary.md |
| V-2895 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2896 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2897 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2898 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2899 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2900 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2901 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2902 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2903 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2904 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2905 | a | A-RELATIVE | `site/data/prompts.json:137 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2906 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2907 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2908 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/15-business-context.md |
| V-2909 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-2910 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2911 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2912 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2913 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2914 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2915 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2916 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2917 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-context-understanding-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-context-understanding-stepwise.md]\(../../prompts/bcreq-context-understanding-stepwise.md); |
| V-2918 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2919 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2920 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2921 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2922 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/16-fr-delta.md |
| V-2923 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2924 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2925 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2926 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2927 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2928 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2929 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2930 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2931 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2932 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2933 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2934 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2935 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2936 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/17-fr-new.md |
| V-2937 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-2938 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2939 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2940 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2941 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2942 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2943 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2944 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2945 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-fr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-fr-documentation-stepwise.md]\(../../prompts/bcreq-fr-documentation-stepwise.md); |
| V-2946 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2947 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2948 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2949 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2950 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/18-nfr.md |
| V-2951 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md |
| V-2952 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-2953 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-nfr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-2954 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2955 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2956 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2957 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2958 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-2959 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-nfr-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-nfr-documentation-stepwise.md]\(../../prompts/bcreq-nfr-documentation-stepwise.md); |
| V-2960 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2961 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2962 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2963 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2964 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/19-uc-coverage.md |
| V-2965 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-2966 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-2967 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-2968 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2969 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2970 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2971 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2972 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-2973 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-2974 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2975 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2976 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2977 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2978 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/20-gate-evidence.md |
| V-2979 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-2980 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2981 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2982 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2983 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2984 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2985 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2986 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2987 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-2988 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2989 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2990 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2991 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-2992 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/21-solution-l1.md |
| V-2993 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-2994 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-2995 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-2996 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-2997 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-2998 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-2999 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3000 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3001 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3002 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3003 | a | A-RELATIVE | `site/data/prompts.json:137 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3004 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3005 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3006 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/22-solution-l2.md |
| V-3007 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-3008 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3009 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3010 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3011 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3012 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3013 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3014 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3015 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-orr-solution-design-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-orr-solution-design-stepwise.md]\(../../prompts/bcreq-orr-solution-design-stepwise.md); |
| V-3016 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3017 | a | A-RELATIVE | `site/data/prompts.json:137 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3018 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3019 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3020 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/23-constraints.md |
| V-3021 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-3022 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-3023 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-constraints-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-3024 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3025 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3026 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3027 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3028 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-3029 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-constraints-documentation-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constraints-documentation-stepwise.md]\(../../prompts/bcreq-constraints-documentation-stepwise.md); |
| V-3030 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3031 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3032 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3033 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3034 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/24-uc-boundaries.md |
| V-3035 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-3036 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-3037 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-3038 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3039 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3040 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3041 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3042 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-3043 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-uc-modeling-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-uc-modeling-stepwise.md]\(../../prompts/bcreq-uc-modeling-stepwise.md); |
| V-3044 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3045 | a | A-RELATIVE | `site/data/prompts.json:131 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3046 | a | A-RELATIVE | `site/data/prompts.json:132 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3047 | a | A-RELATIVE | `site/data/prompts.json:133 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3048 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/25-risks.md |
| V-3049 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-3050 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3051 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3052 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3053 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3054 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3055 | a | A-RELATIVE | `site/data/prompts.json:153 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3056 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3057 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3058 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3059 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3060 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3061 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3062 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/26-delivery-dependencies.md |
| V-3063 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-3064 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3065 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3066 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3067 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3068 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3069 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3070 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3071 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3072 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3073 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3074 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3075 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3076 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/27-acceptance.md |
| V-3077 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-3078 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3079 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3080 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3081 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3082 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3083 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3084 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3085 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-extra-risk-analysis-stepwise.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-extra-risk-analysis-stepwise.md]\(../../prompts/bcreq-extra-risk-analysis-stepwise.md); |
| V-3086 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3087 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3088 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3089 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3090 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/28-independent-review.md |
| V-3091 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3092 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3093 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3094 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3095 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3096 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3097 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3098 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3099 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3100 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3101 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3102 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3103 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3104 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/29-impact.md |
| V-3105 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3106 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3107 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3108 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3109 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3110 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3111 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3112 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3113 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3114 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3115 | a | A-RELATIVE | `site/data/prompts.json:133 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3116 | a | A-RELATIVE | `site/data/prompts.json:134 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3117 | a | A-RELATIVE | `site/data/prompts.json:135 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3118 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/30-targeted-edit.md |
| V-3119 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3120 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3121 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3122 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3123 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3124 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3125 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3126 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3127 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3128 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3129 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3130 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3131 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3132 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/31-conformance.md |
| V-3133 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-3134 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-3135 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-core-documentation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-3136 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3137 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3138 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3139 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3140 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-3141 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-core-documentation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-core-documentation-oneshot.md]\(../../prompts/bcreq-core-documentation-oneshot.md); |
| V-3142 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3143 | a | A-RELATIVE | `site/data/prompts.json:137 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3144 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3145 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3146 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/32-audience-projection.md |
| V-3147 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/letter-customer-documentation-legacy.md |
| V-3148 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-3149 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/letter-customer-documentation-legacy.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-3150 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3151 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3152 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3153 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3154 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-3155 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/letter-customer-documentation-legacy.md` | [инвентарь]\(README.md). Текущий аналог: [letter-customer-documentation-legacy.md]\(../../prompts/letter-customer-documentation-legacy.md); |
| V-3156 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3157 | a | A-RELATIVE | `site/data/prompts.json:133 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3158 | a | A-RELATIVE | `site/data/prompts.json:134 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3159 | a | A-RELATIVE | `site/data/prompts.json:135 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3160 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/33-release-audit.md |
| V-3161 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3162 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3163 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3164 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3165 | a | A-RELATIVE | `site/data/prompts.json:145 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3166 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3167 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3168 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3169 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3170 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3171 | a | A-RELATIVE | `site/data/prompts.json:137 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3172 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3173 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3174 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/34-human-record.md |
| V-3175 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-3176 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3177 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3178 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3179 | a | A-RELATIVE | `site/data/prompts.json:158 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3180 | a | A-RELATIVE | `site/data/prompts.json:159 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3181 | a | A-RELATIVE | `site/data/prompts.json:160 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3182 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3183 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3184 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3185 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3186 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3187 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3188 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/35-baseline-handover.md |
| V-3189 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-3190 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3191 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3192 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3193 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3194 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3195 | a | A-RELATIVE | `site/data/prompts.json:149 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3196 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3197 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3198 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3199 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3200 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3201 | a | A-RELATIVE | `site/data/prompts.json:141 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3202 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/36-rule-bundle.md |
| V-3203 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-3204 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3205 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3206 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3207 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3208 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3209 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3210 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3211 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-constitution-governance-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-constitution-governance-oneshot.md]\(../../prompts/bcreq-constitution-governance-oneshot.md); |
| V-3212 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3213 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3214 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3215 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3216 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/37-user-story.md |
| V-3217 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-3218 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3219 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3220 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3221 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3222 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3223 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3224 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3225 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3226 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3227 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3228 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3229 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3230 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/38-requested-uc.md |
| V-3231 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-3232 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3233 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3234 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3235 | a | A-RELATIVE | `site/data/prompts.json:150 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3236 | a | A-RELATIVE | `site/data/prompts.json:151 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3237 | a | A-RELATIVE | `site/data/prompts.json:152 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3238 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3239 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-scenarios-modeling-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-scenarios-modeling-oneshot.md]\(../../prompts/bcreq-scenarios-modeling-oneshot.md); |
| V-3240 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3241 | a | A-RELATIVE | `site/data/prompts.json:142 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3242 | a | A-RELATIVE | `site/data/prompts.json:143 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3243 | a | A-RELATIVE | `site/data/prompts.json:144 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3244 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/39-manifest-alignment.md |
| V-3245 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].analog.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3246 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3247 | a | A-RELATIVE | `site/data/prompts.json:15 (prompts[].content)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3248 | a | A-RELATIVE | `site/data/prompts.json:25 (prompts[].content)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3249 | a | A-RELATIVE | `site/data/prompts.json:146 (prompts[].content)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3250 | a | A-RELATIVE | `site/data/prompts.json:147 (prompts[].content)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3251 | a | A-RELATIVE | `site/data/prompts.json:148 (prompts[].content)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3252 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `README.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3253 | a | A-RELATIVE | `site/data/prompts.json:7 (prompts[].body)` | `../../prompts/bcreq-review-validation-oneshot.md` | [инвентарь]\(README.md). Текущий аналог: [bcreq-review-validation-oneshot.md]\(../../prompts/bcreq-review-validation-oneshot.md); |
| V-3254 | a | A-RELATIVE | `site/data/prompts.json:17 (prompts[].body)` | `../../docs/contracts/bcreq-manual-state.md` | [контракт состояния]\(../../docs/contracts/bcreq-manual-state.md). |
| V-3255 | a | A-RELATIVE | `site/data/prompts.json:138 (prompts[].body)` | `../../docs/analysis/2026-10-29-bcreq-checkpoint.md` | Основания: [checkpoint]\(../../docs/analysis/2026-10-29-bcreq-checkpoint.md), |
| V-3256 | a | A-RELATIVE | `site/data/prompts.json:139 (prompts[].body)` | `../../docs/rfc/2026-10-bcreq-manual-pipeline.md` | [RFC и маршрут]\(../../docs/rfc/2026-10-bcreq-manual-pipeline.md), |
| V-3257 | a | A-RELATIVE | `site/data/prompts.json:140 (prompts[].body)` | `../bcreq-sections/README.md` | [мета-стандарты разделов]\(../bcreq-sections/README.md). |
| V-3258 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md |
| V-3259 | c | BP-06 | `site/data/prompts.json:2 (prompts[].content)` | `by-test` | id: mango-bcreq-context-understanding-stepwise-by-test |
| V-3260 | c | BP-06 | `site/data/prompts.json:3 (prompts[].content)` | `по тесту` | title: "BCREQ Ш-1 (2.1): контекст, глоссарий (по тесту)" |
| V-3261 | c | BP-06 | `site/data/prompts.json:12 (prompts[].content)` | `by-test` | mode: by-test |
| V-3262 | a | A-PRIVATE | `site/data/prompts.json:17 (prompts[].content)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3263 | c | BP-01 | `site/data/prompts.json:17 (prompts[].content)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3264 | c | BP-04 | `site/data/prompts.json:17 (prompts[].content)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3265 | c | BP-08 | `site/data/prompts.json:17 (prompts[].content)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3266 | c | BP-02 | `site/data/prompts.json:19 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3267 | c | BP-02 | `site/data/prompts.json:19 (prompts[].content)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3268 | c | BP-03 | `site/data/prompts.json:19 (prompts[].content)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3269 | c | BP-04 | `site/data/prompts.json:19 (prompts[].content)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3270 | c | BP-06 | `site/data/prompts.json:19 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3271 | c | BP-06 | `site/data/prompts.json:19 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3272 | c | BP-08 | `site/data/prompts.json:19 (prompts[].content)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-3273 | c | BP-09 | `site/data/prompts.json:19 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3274 | a | A-PRIVATE | `site/data/prompts.json:27 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3275 | a | A-PRIVATE | `site/data/prompts.json:111 (prompts[].content)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3276 | a | A-PRIVATE | `site/data/prompts.json:143 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-3277 | a | A-PRIVATE | `site/data/prompts.json:148 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3278 | c | BP-01 | `site/data/prompts.json:240 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3279 | a | A-PRIVATE | `site/data/prompts.json:251 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3280 | c | BP-01 | `site/data/prompts.json:344 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3281 | c | BP-01 | `site/data/prompts.json:346 (prompts[].content)` | `<!--` | <!-- bl-156: by-test --> |
| V-3282 | c | BP-06 | `site/data/prompts.json:346 (prompts[].content)` | `by-test` | <!-- bl-156: by-test --> |
| V-3283 | c | BP-04 | `site/data/prompts.json:347 (prompts[].content)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3284 | c | BP-06 | `site/data/prompts.json:347 (prompts[].content)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3285 | c | BP-02 | `site/data/prompts.json:349 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3286 | c | BP-06 | `site/data/prompts.json:349 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3287 | c | BP-09 | `site/data/prompts.json:349 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3288 | c | BP-07 | `site/data/prompts.json:351 (prompts[].content)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3289 | a | A-PRIVATE | `site/data/prompts.json:352 (prompts[].content)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3290 | c | BP-02 | `site/data/prompts.json:352 (prompts[].content)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3291 | a | A-PRIVATE | `site/data/prompts.json:353 (prompts[].content)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3292 | a | A-PRIVATE | `site/data/prompts.json:354 (prompts[].content)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3293 | a | A-PRIVATE | `site/data/prompts.json:355 (prompts[].content)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3294 | a | A-PRIVATE | `site/data/prompts.json:356 (prompts[].content)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3295 | c | BP-06 | `site/data/prompts.json:367 (prompts[].content)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3296 | a | A-PRIVATE | `site/data/prompts.json:407 (prompts[].content)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3297 | c | BP-04 | `site/data/prompts.json:410 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3298 | c | BP-04 | `site/data/prompts.json:410 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3299 | c | BP-04 | `site/data/prompts.json:433 (prompts[].content)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3300 | c | BP-10 | `site/data/prompts.json:433 (prompts[].content)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3301 | c | BP-10 | `site/data/prompts.json:433 (prompts[].content)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3302 | c | BP-01 | `site/data/prompts.json:535 (prompts[].content)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3303 | c | BP-06 | `site/data/prompts.json:535 (prompts[].content)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3304 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3305 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3306 | c | BP-04 | `site/data/prompts.json:1 (prompts[].body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3307 | c | BP-08 | `site/data/prompts.json:1 (prompts[].body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3308 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3309 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3310 | c | BP-03 | `site/data/prompts.json:3 (prompts[].body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3311 | c | BP-04 | `site/data/prompts.json:3 (prompts[].body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3312 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3313 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3314 | c | BP-08 | `site/data/prompts.json:3 (prompts[].body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-3315 | c | BP-09 | `site/data/prompts.json:3 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3316 | a | A-PRIVATE | `site/data/prompts.json:11 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3317 | a | A-PRIVATE | `site/data/prompts.json:95 (prompts[].body)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3318 | a | A-PRIVATE | `site/data/prompts.json:127 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-3319 | a | A-PRIVATE | `site/data/prompts.json:132 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3320 | c | BP-01 | `site/data/prompts.json:224 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3321 | a | A-PRIVATE | `site/data/prompts.json:235 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3322 | c | BP-01 | `site/data/prompts.json:328 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3323 | c | BP-01 | `site/data/prompts.json:330 (prompts[].body)` | `<!--` | <!-- bl-156: by-test --> |
| V-3324 | c | BP-06 | `site/data/prompts.json:330 (prompts[].body)` | `by-test` | <!-- bl-156: by-test --> |
| V-3325 | c | BP-04 | `site/data/prompts.json:331 (prompts[].body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3326 | c | BP-06 | `site/data/prompts.json:331 (prompts[].body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3327 | c | BP-02 | `site/data/prompts.json:333 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3328 | c | BP-06 | `site/data/prompts.json:333 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3329 | c | BP-09 | `site/data/prompts.json:333 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3330 | c | BP-07 | `site/data/prompts.json:335 (prompts[].body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3331 | a | A-PRIVATE | `site/data/prompts.json:336 (prompts[].body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3332 | c | BP-02 | `site/data/prompts.json:336 (prompts[].body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3333 | a | A-PRIVATE | `site/data/prompts.json:337 (prompts[].body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3334 | a | A-PRIVATE | `site/data/prompts.json:338 (prompts[].body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3335 | a | A-PRIVATE | `site/data/prompts.json:339 (prompts[].body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3336 | a | A-PRIVATE | `site/data/prompts.json:340 (prompts[].body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3337 | c | BP-06 | `site/data/prompts.json:351 (prompts[].body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3338 | a | A-PRIVATE | `site/data/prompts.json:391 (prompts[].body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3339 | c | BP-04 | `site/data/prompts.json:394 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3340 | c | BP-04 | `site/data/prompts.json:394 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3341 | c | BP-04 | `site/data/prompts.json:417 (prompts[].body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3342 | c | BP-10 | `site/data/prompts.json:417 (prompts[].body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3343 | c | BP-10 | `site/data/prompts.json:417 (prompts[].body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3344 | c | BP-01 | `site/data/prompts.json:519 (prompts[].body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3345 | c | BP-06 | `site/data/prompts.json:519 (prompts[].body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3346 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md |
| V-3347 | a | A-PRIVATE | `site/data/prompts.json:21 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3348 | a | A-PRIVATE | `site/data/prompts.json:29 (prompts[].content)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-3349 | a | A-PRIVATE | `site/data/prompts.json:86 (prompts[].content)` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-3350 | a | A-PRIVATE | `site/data/prompts.json:87 (prompts[].content)` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-3351 | a | A-PRIVATE | `site/data/prompts.json:88 (prompts[].content)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-3352 | a | A-PRIVATE | `site/data/prompts.json:89 (prompts[].content)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3353 | a | A-PRIVATE | `site/data/prompts.json:104 (prompts[].content)` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-3354 | a | A-PRIVATE | `site/data/prompts.json:106 (prompts[].content)` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-3355 | c | BP-01 | `site/data/prompts.json:161 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3356 | a | A-PRIVATE | `site/data/prompts.json:172 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3357 | c | BP-01 | `site/data/prompts.json:265 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3358 | a | A-PRIVATE | `site/data/prompts.json:10 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3359 | a | A-PRIVATE | `site/data/prompts.json:18 (prompts[].body)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-3360 | a | A-PRIVATE | `site/data/prompts.json:75 (prompts[].body)` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-3361 | a | A-PRIVATE | `site/data/prompts.json:76 (prompts[].body)` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-3362 | a | A-PRIVATE | `site/data/prompts.json:77 (prompts[].body)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-3363 | a | A-PRIVATE | `site/data/prompts.json:78 (prompts[].body)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3364 | a | A-PRIVATE | `site/data/prompts.json:93 (prompts[].body)` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-3365 | a | A-PRIVATE | `site/data/prompts.json:95 (prompts[].body)` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-3366 | c | BP-01 | `site/data/prompts.json:150 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3367 | a | A-PRIVATE | `site/data/prompts.json:161 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3368 | c | BP-01 | `site/data/prompts.json:254 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3369 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md |
| V-3370 | c | BP-06 | `site/data/prompts.json:2 (prompts[].content)` | `by-test` | id: mango-bcreq-intake-questionnaire-stepwise-by-test |
| V-3371 | c | BP-06 | `site/data/prompts.json:3 (prompts[].content)` | `по тесту` | title: "BCREQ Ш-А: анкета и согласие со стандартами (по тесту)" |
| V-3372 | c | BP-06 | `site/data/prompts.json:10 (prompts[].content)` | `by-test` | mode: by-test |
| V-3373 | a | A-PRIVATE | `site/data/prompts.json:15 (prompts[].content)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3374 | c | BP-01 | `site/data/prompts.json:15 (prompts[].content)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3375 | c | BP-04 | `site/data/prompts.json:15 (prompts[].content)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3376 | c | BP-08 | `site/data/prompts.json:15 (prompts[].content)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3377 | c | BP-02 | `site/data/prompts.json:17 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3378 | c | BP-02 | `site/data/prompts.json:17 (prompts[].content)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3379 | c | BP-02 | `site/data/prompts.json:17 (prompts[].content)` | `#464` | …* Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3380 | c | BP-03 | `site/data/prompts.json:17 (prompts[].content)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3381 | c | BP-03 | `site/data/prompts.json:17 (prompts[].content)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3382 | c | BP-04 | `site/data/prompts.json:17 (prompts[].content)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3383 | c | BP-06 | `site/data/prompts.json:17 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3384 | c | BP-06 | `site/data/prompts.json:17 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3385 | c | BP-08 | `site/data/prompts.json:17 (prompts[].content)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-3386 | c | BP-09 | `site/data/prompts.json:17 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3387 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-3388 | a | A-PRIVATE | `site/data/prompts.json:29 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3389 | b | CT-04 | `site/data/prompts.json:70 (prompts[].content)` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-3390 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].content)` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-3391 | b | CT-04 | `site/data/prompts.json:100 (prompts[].content)` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-3392 | c | BP-01 | `site/data/prompts.json:123 (prompts[].content)` | `<!--` | <!-- bl-156: by-test --> |
| V-3393 | c | BP-06 | `site/data/prompts.json:123 (prompts[].content)` | `by-test` | <!-- bl-156: by-test --> |
| V-3394 | c | BP-04 | `site/data/prompts.json:124 (prompts[].content)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3395 | c | BP-06 | `site/data/prompts.json:124 (prompts[].content)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3396 | c | BP-02 | `site/data/prompts.json:126 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3397 | c | BP-06 | `site/data/prompts.json:126 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3398 | c | BP-09 | `site/data/prompts.json:126 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3399 | c | BP-07 | `site/data/prompts.json:128 (prompts[].content)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3400 | a | A-PRIVATE | `site/data/prompts.json:129 (prompts[].content)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3401 | c | BP-02 | `site/data/prompts.json:129 (prompts[].content)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3402 | a | A-PRIVATE | `site/data/prompts.json:130 (prompts[].content)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3403 | a | A-PRIVATE | `site/data/prompts.json:131 (prompts[].content)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3404 | a | A-PRIVATE | `site/data/prompts.json:132 (prompts[].content)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3405 | a | A-PRIVATE | `site/data/prompts.json:133 (prompts[].content)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3406 | c | BP-06 | `site/data/prompts.json:144 (prompts[].content)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3407 | a | A-PRIVATE | `site/data/prompts.json:184 (prompts[].content)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3408 | c | BP-04 | `site/data/prompts.json:187 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3409 | c | BP-04 | `site/data/prompts.json:187 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3410 | c | BP-04 | `site/data/prompts.json:210 (prompts[].content)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3411 | c | BP-10 | `site/data/prompts.json:210 (prompts[].content)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3412 | c | BP-10 | `site/data/prompts.json:210 (prompts[].content)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3413 | c | BP-01 | `site/data/prompts.json:238 (prompts[].content)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3414 | c | BP-06 | `site/data/prompts.json:238 (prompts[].content)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3415 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3416 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3417 | c | BP-04 | `site/data/prompts.json:1 (prompts[].body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3418 | c | BP-08 | `site/data/prompts.json:1 (prompts[].body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3419 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3420 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3421 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#464` | …* Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3422 | c | BP-03 | `site/data/prompts.json:3 (prompts[].body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3423 | c | BP-03 | `site/data/prompts.json:3 (prompts[].body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3424 | c | BP-04 | `site/data/prompts.json:3 (prompts[].body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-3425 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3426 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3427 | c | BP-08 | `site/data/prompts.json:3 (prompts[].body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-3428 | c | BP-09 | `site/data/prompts.json:3 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-3429 | a | A-PRIVATE | `site/data/prompts.json:9 (prompts[].body)` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-3430 | a | A-PRIVATE | `site/data/prompts.json:15 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3431 | b | CT-04 | `site/data/prompts.json:56 (prompts[].body)` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-3432 | a | A-PRIVATE | `site/data/prompts.json:69 (prompts[].body)` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-3433 | b | CT-04 | `site/data/prompts.json:86 (prompts[].body)` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-3434 | c | BP-01 | `site/data/prompts.json:109 (prompts[].body)` | `<!--` | <!-- bl-156: by-test --> |
| V-3435 | c | BP-06 | `site/data/prompts.json:109 (prompts[].body)` | `by-test` | <!-- bl-156: by-test --> |
| V-3436 | c | BP-04 | `site/data/prompts.json:110 (prompts[].body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3437 | c | BP-06 | `site/data/prompts.json:110 (prompts[].body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3438 | c | BP-02 | `site/data/prompts.json:112 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3439 | c | BP-06 | `site/data/prompts.json:112 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3440 | c | BP-09 | `site/data/prompts.json:112 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3441 | c | BP-07 | `site/data/prompts.json:114 (prompts[].body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3442 | a | A-PRIVATE | `site/data/prompts.json:115 (prompts[].body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3443 | c | BP-02 | `site/data/prompts.json:115 (prompts[].body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3444 | a | A-PRIVATE | `site/data/prompts.json:116 (prompts[].body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3445 | a | A-PRIVATE | `site/data/prompts.json:117 (prompts[].body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3446 | a | A-PRIVATE | `site/data/prompts.json:118 (prompts[].body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3447 | a | A-PRIVATE | `site/data/prompts.json:119 (prompts[].body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3448 | c | BP-06 | `site/data/prompts.json:130 (prompts[].body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3449 | a | A-PRIVATE | `site/data/prompts.json:170 (prompts[].body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3450 | c | BP-04 | `site/data/prompts.json:173 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3451 | c | BP-04 | `site/data/prompts.json:173 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3452 | c | BP-04 | `site/data/prompts.json:196 (prompts[].body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3453 | c | BP-10 | `site/data/prompts.json:196 (prompts[].body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3454 | c | BP-10 | `site/data/prompts.json:196 (prompts[].body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3455 | c | BP-01 | `site/data/prompts.json:224 (prompts[].body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3456 | c | BP-06 | `site/data/prompts.json:224 (prompts[].body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3457 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md |
| V-3458 | c | BP-06 | `site/data/prompts.json:2 (prompts[].content)` | `by-test` | id: mango-bcreq-products-impact-analysis-stepwise-by-test |
| V-3459 | c | BP-06 | `site/data/prompts.json:3 (prompts[].content)` | `по тесту` | title: "BCREQ Ш-2 (2.2): продукты, стейкхолдеры (по тесту)" |
| V-3460 | c | BP-06 | `site/data/prompts.json:12 (prompts[].content)` | `by-test` | mode: by-test |
| V-3461 | a | A-PRIVATE | `site/data/prompts.json:17 (prompts[].content)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3462 | c | BP-01 | `site/data/prompts.json:17 (prompts[].content)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3463 | c | BP-04 | `site/data/prompts.json:17 (prompts[].content)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3464 | c | BP-08 | `site/data/prompts.json:17 (prompts[].content)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3465 | c | BP-02 | `site/data/prompts.json:19 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3466 | c | BP-02 | `site/data/prompts.json:19 (prompts[].content)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3467 | c | BP-03 | `site/data/prompts.json:19 (prompts[].content)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3468 | c | BP-04 | `site/data/prompts.json:19 (prompts[].content)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3469 | c | BP-06 | `site/data/prompts.json:19 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3470 | c | BP-06 | `site/data/prompts.json:19 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3471 | c | BP-08 | `site/data/prompts.json:19 (prompts[].content)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-3472 | c | BP-09 | `site/data/prompts.json:19 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3473 | a | A-PRIVATE | `site/data/prompts.json:27 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3474 | a | A-PRIVATE | `site/data/prompts.json:46 (prompts[].content)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-3475 | a | A-PRIVATE | `site/data/prompts.json:47 (prompts[].content)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3476 | b | CT-09 | `site/data/prompts.json:73 (prompts[].content)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3477 | b | CT-09 | `site/data/prompts.json:73 (prompts[].content)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3478 | b | CT-04 | `site/data/prompts.json:74 (prompts[].content)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3479 | b | CT-05 | `site/data/prompts.json:74 (prompts[].content)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3480 | b | CT-09 | `site/data/prompts.json:74 (prompts[].content)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3481 | b | CT-09 | `site/data/prompts.json:74 (prompts[].content)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3482 | b | CT-09 | `site/data/prompts.json:74 (prompts[].content)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3483 | b | CT-09 | `site/data/prompts.json:74 (prompts[].content)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3484 | b | CT-09 | `site/data/prompts.json:74 (prompts[].content)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3485 | b | CT-09 | `site/data/prompts.json:75 (prompts[].content)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3486 | b | CT-09 | `site/data/prompts.json:75 (prompts[].content)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3487 | b | CT-09 | `site/data/prompts.json:75 (prompts[].content)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3488 | b | CT-09 | `site/data/prompts.json:75 (prompts[].content)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3489 | b | CT-09 | `site/data/prompts.json:75 (prompts[].content)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3490 | a | A-PRIVATE | `site/data/prompts.json:89 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3491 | a | A-PRIVATE | `site/data/prompts.json:92 (prompts[].content)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-3492 | b | CT-03 | `site/data/prompts.json:110 (prompts[].content)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-3493 | c | BP-01 | `site/data/prompts.json:158 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3494 | a | A-PRIVATE | `site/data/prompts.json:169 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3495 | c | BP-01 | `site/data/prompts.json:262 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3496 | c | BP-01 | `site/data/prompts.json:264 (prompts[].content)` | `<!--` | <!-- bl-156: by-test --> |
| V-3497 | c | BP-06 | `site/data/prompts.json:264 (prompts[].content)` | `by-test` | <!-- bl-156: by-test --> |
| V-3498 | c | BP-04 | `site/data/prompts.json:265 (prompts[].content)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3499 | c | BP-06 | `site/data/prompts.json:265 (prompts[].content)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3500 | c | BP-02 | `site/data/prompts.json:267 (prompts[].content)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3501 | c | BP-06 | `site/data/prompts.json:267 (prompts[].content)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3502 | c | BP-09 | `site/data/prompts.json:267 (prompts[].content)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3503 | c | BP-07 | `site/data/prompts.json:269 (prompts[].content)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3504 | a | A-PRIVATE | `site/data/prompts.json:270 (prompts[].content)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3505 | c | BP-02 | `site/data/prompts.json:270 (prompts[].content)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3506 | a | A-PRIVATE | `site/data/prompts.json:271 (prompts[].content)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3507 | a | A-PRIVATE | `site/data/prompts.json:272 (prompts[].content)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3508 | a | A-PRIVATE | `site/data/prompts.json:273 (prompts[].content)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3509 | a | A-PRIVATE | `site/data/prompts.json:274 (prompts[].content)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3510 | c | BP-06 | `site/data/prompts.json:285 (prompts[].content)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3511 | c | BP-04 | `site/data/prompts.json:302 (prompts[].content)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-3512 | a | A-PRIVATE | `site/data/prompts.json:306 (prompts[].content)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-3513 | a | A-PRIVATE | `site/data/prompts.json:332 (prompts[].content)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3514 | c | BP-04 | `site/data/prompts.json:335 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3515 | c | BP-04 | `site/data/prompts.json:335 (prompts[].content)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3516 | c | BP-04 | `site/data/prompts.json:358 (prompts[].content)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3517 | c | BP-10 | `site/data/prompts.json:358 (prompts[].content)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3518 | c | BP-10 | `site/data/prompts.json:358 (prompts[].content)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3519 | c | BP-01 | `site/data/prompts.json:446 (prompts[].content)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3520 | c | BP-06 | `site/data/prompts.json:446 (prompts[].content)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3521 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3522 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3523 | c | BP-04 | `site/data/prompts.json:1 (prompts[].body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3524 | c | BP-08 | `site/data/prompts.json:1 (prompts[].body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3525 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3526 | c | BP-02 | `site/data/prompts.json:3 (prompts[].body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3527 | c | BP-03 | `site/data/prompts.json:3 (prompts[].body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3528 | c | BP-04 | `site/data/prompts.json:3 (prompts[].body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-3529 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3530 | c | BP-06 | `site/data/prompts.json:3 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3531 | c | BP-08 | `site/data/prompts.json:3 (prompts[].body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-3532 | c | BP-09 | `site/data/prompts.json:3 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-3533 | a | A-PRIVATE | `site/data/prompts.json:11 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3534 | a | A-PRIVATE | `site/data/prompts.json:30 (prompts[].body)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-3535 | a | A-PRIVATE | `site/data/prompts.json:31 (prompts[].body)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3536 | b | CT-09 | `site/data/prompts.json:57 (prompts[].body)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3537 | b | CT-09 | `site/data/prompts.json:57 (prompts[].body)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3538 | b | CT-04 | `site/data/prompts.json:58 (prompts[].body)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3539 | b | CT-05 | `site/data/prompts.json:58 (prompts[].body)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3540 | b | CT-09 | `site/data/prompts.json:58 (prompts[].body)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3541 | b | CT-09 | `site/data/prompts.json:58 (prompts[].body)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3542 | b | CT-09 | `site/data/prompts.json:58 (prompts[].body)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3543 | b | CT-09 | `site/data/prompts.json:58 (prompts[].body)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3544 | b | CT-09 | `site/data/prompts.json:58 (prompts[].body)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3545 | b | CT-09 | `site/data/prompts.json:59 (prompts[].body)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3546 | b | CT-09 | `site/data/prompts.json:59 (prompts[].body)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3547 | b | CT-09 | `site/data/prompts.json:59 (prompts[].body)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3548 | b | CT-09 | `site/data/prompts.json:59 (prompts[].body)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3549 | b | CT-09 | `site/data/prompts.json:59 (prompts[].body)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3550 | a | A-PRIVATE | `site/data/prompts.json:73 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3551 | a | A-PRIVATE | `site/data/prompts.json:76 (prompts[].body)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-3552 | b | CT-03 | `site/data/prompts.json:94 (prompts[].body)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-3553 | c | BP-01 | `site/data/prompts.json:142 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3554 | a | A-PRIVATE | `site/data/prompts.json:153 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3555 | c | BP-01 | `site/data/prompts.json:246 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3556 | c | BP-01 | `site/data/prompts.json:248 (prompts[].body)` | `<!--` | <!-- bl-156: by-test --> |
| V-3557 | c | BP-06 | `site/data/prompts.json:248 (prompts[].body)` | `by-test` | <!-- bl-156: by-test --> |
| V-3558 | c | BP-04 | `site/data/prompts.json:249 (prompts[].body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3559 | c | BP-06 | `site/data/prompts.json:249 (prompts[].body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-3560 | c | BP-02 | `site/data/prompts.json:251 (prompts[].body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3561 | c | BP-06 | `site/data/prompts.json:251 (prompts[].body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3562 | c | BP-09 | `site/data/prompts.json:251 (prompts[].body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-3563 | c | BP-07 | `site/data/prompts.json:253 (prompts[].body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-3564 | a | A-PRIVATE | `site/data/prompts.json:254 (prompts[].body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3565 | c | BP-02 | `site/data/prompts.json:254 (prompts[].body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-3566 | a | A-PRIVATE | `site/data/prompts.json:255 (prompts[].body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-3567 | a | A-PRIVATE | `site/data/prompts.json:256 (prompts[].body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-3568 | a | A-PRIVATE | `site/data/prompts.json:257 (prompts[].body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-3569 | a | A-PRIVATE | `site/data/prompts.json:258 (prompts[].body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-3570 | c | BP-06 | `site/data/prompts.json:269 (prompts[].body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-3571 | c | BP-04 | `site/data/prompts.json:286 (prompts[].body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-3572 | a | A-PRIVATE | `site/data/prompts.json:290 (prompts[].body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-3573 | a | A-PRIVATE | `site/data/prompts.json:316 (prompts[].body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-3574 | c | BP-04 | `site/data/prompts.json:319 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3575 | c | BP-04 | `site/data/prompts.json:319 (prompts[].body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-3576 | c | BP-04 | `site/data/prompts.json:342 (prompts[].body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3577 | c | BP-10 | `site/data/prompts.json:342 (prompts[].body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3578 | c | BP-10 | `site/data/prompts.json:342 (prompts[].body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-3579 | c | BP-01 | `site/data/prompts.json:430 (prompts[].body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-3580 | c | BP-06 | `site/data/prompts.json:430 (prompts[].body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-3581 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-3582 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3583 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3584 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3585 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3586 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3587 | a | A-PRIVATE | `site/data/prompts.json:99 (prompts[].content)` | `mango_ba_prompts` | - [Мета-стандарты разделов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md) |
| V-3588 | a | A-PRIVATE | `site/data/prompts.json:100 (prompts[].content)` | `mango_ba_prompts` | - [Архитектура промптов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md) |
| V-3589 | a | A-PRIVATE | `site/data/prompts.json:101 (prompts[].content)` | `mango_ba_prompts` | - [Контракт стадий и гейтов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md) |
| V-3590 | a | A-PRIVATE | `site/data/prompts.json:102 (prompts[].content)` | `mango_ba_prompts` | - [Стандарт композиции продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md) |
| V-3591 | a | A-PRIVATE | `site/data/prompts.json:120 (prompts[].content)` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай: |
| V-3592 | b | CT-04 | `site/data/prompts.json:124 (prompts[].content)` | `ВАТС` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-3593 | b | CT-05 | `site/data/prompts.json:124 (prompts[].content)` | `ЛК` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-3594 | a | A-PRIVATE | `site/data/prompts.json:132 (prompts[].content)` | `mango_ba_prompts` | [стандарте композиции §4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3595 | a | A-PRIVATE | `site/data/prompts.json:157 (prompts[].content)` | `mango_ba_prompts` | 6. Попроси ввести следующий промпт — [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) |
| V-3596 | a | A-PRIVATE | `site/data/prompts.json:180 (prompts[].content)` | `mango_ba_prompts` | [standards/bcreq-sections]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов). |
| V-3597 | a | A-PRIVATE | `site/data/prompts.json:200 (prompts[].content)` | `mango_ba_prompts` | [README §2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили). |
| V-3598 | a | A-PRIVATE | `site/data/prompts.json:227 (prompts[].content)` | `mango_ba_prompts` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3599 | c | BP-04 | `site/data/prompts.json:227 (prompts[].content)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3600 | c | BP-04 | `site/data/prompts.json:227 (prompts[].content)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3601 | a | A-PRIVATE | `site/data/prompts.json:229 (prompts[].content)` | `mango_ba_prompts` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-3602 | c | BP-04 | `site/data/prompts.json:229 (prompts[].content)` | `RUN-0` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-3603 | a | A-PRIVATE | `site/data/prompts.json:231 (prompts[].content)` | `mango_ba_prompts` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-3604 | c | BP-04 | `site/data/prompts.json:231 (prompts[].content)` | `RUN-0` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-3605 | c | BP-04 | `site/data/prompts.json:233 (prompts[].content)` | `RUN-0` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-3606 | c | BP-12 | `site/data/prompts.json:233 (prompts[].content)` | `Категория RUN` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-3607 | c | BP-02 | `site/data/prompts.json:243 (prompts[].content)` | `#391` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3608 | c | BP-03 | `site/data/prompts.json:243 (prompts[].content)` | `issue` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3609 | c | BP-12 | `site/data/prompts.json:243 (prompts[].content)` | `ревизии Golden` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3610 | b | CT-03 | `site/data/prompts.json:250 (prompts[].content)` | `коннекторе` | …; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает… |
| V-3611 | c | BP-04 | `site/data/prompts.json:265 (prompts[].content)` | `RUN-0` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-3612 | c | BP-04 | `site/data/prompts.json:265 (prompts[].content)` | `SC-6` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-3613 | a | A-PRIVATE | `site/data/prompts.json:286 (prompts[].content)` | `mango_ba_prompts` | …-intake-questionnaire-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) \|… |
| V-3614 | a | A-PRIVATE | `site/data/prompts.json:287 (prompts[].content)` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) \|… |
| V-3615 | a | A-PRIVATE | `site/data/prompts.json:288 (prompts[].content)` | `mango_ba_prompts` | …ducts-impact-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \|… |
| V-3616 | a | A-PRIVATE | `site/data/prompts.json:289 (prompts[].content)` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \|… |
| V-3617 | a | A-PRIVATE | `site/data/prompts.json:290 (prompts[].content)` | `mango_ba_prompts` | …req-nfr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-3618 | a | A-PRIVATE | `site/data/prompts.json:291 (prompts[].content)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-3619 | a | A-PRIVATE | `site/data/prompts.json:292 (prompts[].content)` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \|… |
| V-3620 | a | A-PRIVATE | `site/data/prompts.json:293 (prompts[].content)` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-3621 | a | A-PRIVATE | `site/data/prompts.json:294 (prompts[].content)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-3622 | a | A-PRIVATE | `site/data/prompts.json:295 (prompts[].content)` | `mango_ba_prompts` | …q-extra-risk-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-3623 | a | A-PRIVATE | `site/data/prompts.json:296 (prompts[].content)` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-3624 | a | A-PRIVATE | `site/data/prompts.json:297 (prompts[].content)` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \|… |
| V-3625 | a | A-PRIVATE | `site/data/prompts.json:304 (prompts[].content)` | `mango_ba_prompts` | [A-IN]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) (Ш-А, Ш-1, Ш-2) → |
| V-3626 | a | A-PRIVATE | `site/data/prompts.json:306 (prompts[].content)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) (Ш-3…Ш-5) → |
| V-3627 | a | A-PRIVATE | `site/data/prompts.json:308 (prompts[].content)` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) (Ш-6…Ш-9) → |
| V-3628 | a | A-PRIVATE | `site/data/prompts.json:323 (prompts[].content)` | `mango_ba_prompts` | [контракта гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#3-возвраты)). |
| V-3629 | a | A-PRIVATE | `site/data/prompts.json:327 (prompts[].content)` | `mango_ba_prompts` | [поток CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3630 | c | BP-01 | `site/data/prompts.json:375 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3631 | a | A-PRIVATE | `site/data/prompts.json:386 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3632 | c | BP-01 | `site/data/prompts.json:479 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3633 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3634 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3635 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3636 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3637 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3638 | a | A-PRIVATE | `site/data/prompts.json:88 (prompts[].body)` | `mango_ba_prompts` | - [Мета-стандарты разделов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md) |
| V-3639 | a | A-PRIVATE | `site/data/prompts.json:89 (prompts[].body)` | `mango_ba_prompts` | - [Архитектура промптов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md) |
| V-3640 | a | A-PRIVATE | `site/data/prompts.json:90 (prompts[].body)` | `mango_ba_prompts` | - [Контракт стадий и гейтов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md) |
| V-3641 | a | A-PRIVATE | `site/data/prompts.json:91 (prompts[].body)` | `mango_ba_prompts` | - [Стандарт композиции продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md) |
| V-3642 | a | A-PRIVATE | `site/data/prompts.json:109 (prompts[].body)` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай: |
| V-3643 | b | CT-04 | `site/data/prompts.json:113 (prompts[].body)` | `ВАТС` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-3644 | b | CT-05 | `site/data/prompts.json:113 (prompts[].body)` | `ЛК` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-3645 | a | A-PRIVATE | `site/data/prompts.json:121 (prompts[].body)` | `mango_ba_prompts` | [стандарте композиции §4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3646 | a | A-PRIVATE | `site/data/prompts.json:146 (prompts[].body)` | `mango_ba_prompts` | 6. Попроси ввести следующий промпт — [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) |
| V-3647 | a | A-PRIVATE | `site/data/prompts.json:169 (prompts[].body)` | `mango_ba_prompts` | [standards/bcreq-sections]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов). |
| V-3648 | a | A-PRIVATE | `site/data/prompts.json:189 (prompts[].body)` | `mango_ba_prompts` | [README §2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили). |
| V-3649 | a | A-PRIVATE | `site/data/prompts.json:216 (prompts[].body)` | `mango_ba_prompts` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3650 | c | BP-04 | `site/data/prompts.json:216 (prompts[].body)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3651 | c | BP-04 | `site/data/prompts.json:216 (prompts[].body)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-3652 | a | A-PRIVATE | `site/data/prompts.json:218 (prompts[].body)` | `mango_ba_prompts` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-3653 | c | BP-04 | `site/data/prompts.json:218 (prompts[].body)` | `RUN-0` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-3654 | a | A-PRIVATE | `site/data/prompts.json:220 (prompts[].body)` | `mango_ba_prompts` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-3655 | c | BP-04 | `site/data/prompts.json:220 (prompts[].body)` | `RUN-0` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-3656 | c | BP-04 | `site/data/prompts.json:222 (prompts[].body)` | `RUN-0` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-3657 | c | BP-12 | `site/data/prompts.json:222 (prompts[].body)` | `Категория RUN` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-3658 | c | BP-02 | `site/data/prompts.json:232 (prompts[].body)` | `#391` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3659 | c | BP-03 | `site/data/prompts.json:232 (prompts[].body)` | `issue` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3660 | c | BP-12 | `site/data/prompts.json:232 (prompts[].body)` | `ревизии Golden` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-3661 | b | CT-03 | `site/data/prompts.json:239 (prompts[].body)` | `коннекторе` | …; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает… |
| V-3662 | c | BP-04 | `site/data/prompts.json:254 (prompts[].body)` | `RUN-0` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-3663 | c | BP-04 | `site/data/prompts.json:254 (prompts[].body)` | `SC-6` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-3664 | a | A-PRIVATE | `site/data/prompts.json:275 (prompts[].body)` | `mango_ba_prompts` | …-intake-questionnaire-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md) \|… |
| V-3665 | a | A-PRIVATE | `site/data/prompts.json:276 (prompts[].body)` | `mango_ba_prompts` | …context-understanding-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md) \|… |
| V-3666 | a | A-PRIVATE | `site/data/prompts.json:277 (prompts[].body)` | `mango_ba_prompts` | …ducts-impact-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md) \|… |
| V-3667 | a | A-PRIVATE | `site/data/prompts.json:278 (prompts[].body)` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \|… |
| V-3668 | a | A-PRIVATE | `site/data/prompts.json:279 (prompts[].body)` | `mango_ba_prompts` | …req-nfr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-3669 | a | A-PRIVATE | `site/data/prompts.json:280 (prompts[].body)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-3670 | a | A-PRIVATE | `site/data/prompts.json:281 (prompts[].body)` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \|… |
| V-3671 | a | A-PRIVATE | `site/data/prompts.json:282 (prompts[].body)` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-3672 | a | A-PRIVATE | `site/data/prompts.json:283 (prompts[].body)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-3673 | a | A-PRIVATE | `site/data/prompts.json:284 (prompts[].body)` | `mango_ba_prompts` | …q-extra-risk-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-3674 | a | A-PRIVATE | `site/data/prompts.json:285 (prompts[].body)` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-3675 | a | A-PRIVATE | `site/data/prompts.json:286 (prompts[].body)` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \|… |
| V-3676 | a | A-PRIVATE | `site/data/prompts.json:293 (prompts[].body)` | `mango_ba_prompts` | [A-IN]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md) (Ш-А, Ш-1, Ш-2) → |
| V-3677 | a | A-PRIVATE | `site/data/prompts.json:295 (prompts[].body)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md) (Ш-3…Ш-5) → |
| V-3678 | a | A-PRIVATE | `site/data/prompts.json:297 (prompts[].body)` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md) (Ш-6…Ш-9) → |
| V-3679 | a | A-PRIVATE | `site/data/prompts.json:312 (prompts[].body)` | `mango_ba_prompts` | [контракта гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#3-возвраты)). |
| V-3680 | a | A-PRIVATE | `site/data/prompts.json:316 (prompts[].body)` | `mango_ba_prompts` | [поток CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3681 | c | BP-01 | `site/data/prompts.json:364 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3682 | a | A-PRIVATE | `site/data/prompts.json:375 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3683 | c | BP-01 | `site/data/prompts.json:468 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3684 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-3685 | a | A-PRIVATE | `site/data/prompts.json:18 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3686 | a | A-PRIVATE | `site/data/prompts.json:67 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md). |
| V-3687 | c | BP-01 | `site/data/prompts.json:110 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3688 | a | A-PRIVATE | `site/data/prompts.json:121 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3689 | c | BP-01 | `site/data/prompts.json:214 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3690 | a | A-PRIVATE | `site/data/prompts.json:7 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3691 | a | A-PRIVATE | `site/data/prompts.json:56 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md). |
| V-3692 | c | BP-01 | `site/data/prompts.json:99 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3693 | a | A-PRIVATE | `site/data/prompts.json:110 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3694 | c | BP-01 | `site/data/prompts.json:203 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3695 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-3696 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3697 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3698 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3699 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3700 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3701 | a | A-PRIVATE | `site/data/prompts.json:94 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3702 | a | A-PRIVATE | `site/data/prompts.json:178 (prompts[].content)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3703 | a | A-PRIVATE | `site/data/prompts.json:210 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-3704 | a | A-PRIVATE | `site/data/prompts.json:215 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3705 | c | BP-01 | `site/data/prompts.json:307 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3706 | a | A-PRIVATE | `site/data/prompts.json:318 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3707 | c | BP-01 | `site/data/prompts.json:411 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3708 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3709 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3710 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3711 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3712 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3713 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3714 | a | A-PRIVATE | `site/data/prompts.json:167 (prompts[].body)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-3715 | a | A-PRIVATE | `site/data/prompts.json:199 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-3716 | a | A-PRIVATE | `site/data/prompts.json:204 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3717 | c | BP-01 | `site/data/prompts.json:296 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3718 | a | A-PRIVATE | `site/data/prompts.json:307 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3719 | c | BP-01 | `site/data/prompts.json:400 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3720 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md |
| V-3721 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3722 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3723 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3724 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3725 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3726 | a | A-PRIVATE | `site/data/prompts.json:97 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3727 | a | A-PRIVATE | `site/data/prompts.json:109 (prompts[].content)` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md). |
| V-3728 | a | A-PRIVATE | `site/data/prompts.json:150 (prompts[].content)` | `mango_ba_prompts` | [Раздел 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md); |
| V-3729 | a | A-PRIVATE | `site/data/prompts.json:151 (prompts[].content)` | `mango_ba_prompts` | [раздел 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md); |
| V-3730 | a | A-PRIVATE | `site/data/prompts.json:152 (prompts[].content)` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-3731 | a | A-PRIVATE | `site/data/prompts.json:153 (prompts[].content)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3732 | c | BP-01 | `site/data/prompts.json:208 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3733 | a | A-PRIVATE | `site/data/prompts.json:219 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3734 | c | BP-01 | `site/data/prompts.json:312 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3735 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3736 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3737 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3738 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3739 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3740 | a | A-PRIVATE | `site/data/prompts.json:86 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3741 | a | A-PRIVATE | `site/data/prompts.json:98 (prompts[].body)` | `mango_ba_prompts` | [A-WORK]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md). |
| V-3742 | a | A-PRIVATE | `site/data/prompts.json:139 (prompts[].body)` | `mango_ba_prompts` | [Раздел 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md); |
| V-3743 | a | A-PRIVATE | `site/data/prompts.json:140 (prompts[].body)` | `mango_ba_prompts` | [раздел 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md); |
| V-3744 | a | A-PRIVATE | `site/data/prompts.json:141 (prompts[].body)` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-3745 | a | A-PRIVATE | `site/data/prompts.json:142 (prompts[].body)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3746 | c | BP-01 | `site/data/prompts.json:197 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3747 | a | A-PRIVATE | `site/data/prompts.json:208 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3748 | c | BP-01 | `site/data/prompts.json:301 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3749 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-3750 | a | A-PRIVATE | `site/data/prompts.json:18 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3751 | a | A-PRIVATE | `site/data/prompts.json:65 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md). |
| V-3752 | c | BP-01 | `site/data/prompts.json:110 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3753 | a | A-PRIVATE | `site/data/prompts.json:121 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3754 | c | BP-01 | `site/data/prompts.json:214 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3755 | a | A-PRIVATE | `site/data/prompts.json:7 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3756 | a | A-PRIVATE | `site/data/prompts.json:54 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md). |
| V-3757 | c | BP-01 | `site/data/prompts.json:99 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3758 | a | A-PRIVATE | `site/data/prompts.json:110 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3759 | c | BP-01 | `site/data/prompts.json:203 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3760 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-3761 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3762 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3763 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3764 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3765 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3766 | a | A-PRIVATE | `site/data/prompts.json:94 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3767 | a | A-PRIVATE | `site/data/prompts.json:167 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md). |
| V-3768 | a | A-PRIVATE | `site/data/prompts.json:175 (prompts[].content)` | `mango_ba_prompts` | …BABOK — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-babok-guide-v3-что-берём… |
| V-3769 | c | BP-01 | `site/data/prompts.json:238 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3770 | a | A-PRIVATE | `site/data/prompts.json:249 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3771 | c | BP-01 | `site/data/prompts.json:342 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3772 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3773 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3774 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3775 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3776 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3777 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3778 | a | A-PRIVATE | `site/data/prompts.json:156 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md). |
| V-3779 | a | A-PRIVATE | `site/data/prompts.json:164 (prompts[].body)` | `mango_ba_prompts` | …BABOK — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-babok-guide-v3-что-берём… |
| V-3780 | c | BP-01 | `site/data/prompts.json:227 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3781 | a | A-PRIVATE | `site/data/prompts.json:238 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3782 | c | BP-01 | `site/data/prompts.json:331 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3783 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-in-understanding-oneshot.md |
| V-3784 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3785 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3786 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3787 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3788 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3789 | a | A-PRIVATE | `site/data/prompts.json:97 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3790 | a | A-PRIVATE | `site/data/prompts.json:105 (prompts[].content)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-3791 | a | A-PRIVATE | `site/data/prompts.json:162 (prompts[].content)` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-3792 | a | A-PRIVATE | `site/data/prompts.json:163 (prompts[].content)` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-3793 | a | A-PRIVATE | `site/data/prompts.json:164 (prompts[].content)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-3794 | a | A-PRIVATE | `site/data/prompts.json:165 (prompts[].content)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3795 | a | A-PRIVATE | `site/data/prompts.json:180 (prompts[].content)` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-3796 | a | A-PRIVATE | `site/data/prompts.json:182 (prompts[].content)` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-3797 | c | BP-01 | `site/data/prompts.json:237 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3798 | a | A-PRIVATE | `site/data/prompts.json:248 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3799 | c | BP-01 | `site/data/prompts.json:341 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3800 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3801 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3802 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3803 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3804 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3805 | a | A-PRIVATE | `site/data/prompts.json:86 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3806 | a | A-PRIVATE | `site/data/prompts.json:94 (prompts[].body)` | `mango_ba_prompts` | [A-CORE]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-core-documentation-oneshot.md). |
| V-3807 | a | A-PRIVATE | `site/data/prompts.json:151 (prompts[].body)` | `mango_ba_prompts` | [Раздел 1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md); |
| V-3808 | a | A-PRIVATE | `site/data/prompts.json:152 (prompts[].body)` | `mango_ba_prompts` | [раздел 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md); |
| V-3809 | a | A-PRIVATE | `site/data/prompts.json:153 (prompts[].body)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md); |
| V-3810 | a | A-PRIVATE | `site/data/prompts.json:154 (prompts[].body)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3811 | a | A-PRIVATE | `site/data/prompts.json:169 (prompts[].body)` | `mango_ba_prompts` | [Ш-1]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md#проверка-релевантности-as-is) |
| V-3812 | a | A-PRIVATE | `site/data/prompts.json:171 (prompts[].body)` | `mango_ba_prompts` | [Ш-2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md#проверка-принадлежности-доказательства). |
| V-3813 | c | BP-01 | `site/data/prompts.json:226 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3814 | a | A-PRIVATE | `site/data/prompts.json:237 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3815 | c | BP-01 | `site/data/prompts.json:330 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3816 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md |
| V-3817 | a | A-PRIVATE | `site/data/prompts.json:18 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3818 | a | A-PRIVATE | `site/data/prompts.json:65 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md). |
| V-3819 | c | BP-01 | `site/data/prompts.json:109 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3820 | a | A-PRIVATE | `site/data/prompts.json:120 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3821 | c | BP-01 | `site/data/prompts.json:213 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3822 | a | A-PRIVATE | `site/data/prompts.json:7 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3823 | a | A-PRIVATE | `site/data/prompts.json:54 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md). |
| V-3824 | c | BP-01 | `site/data/prompts.json:98 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3825 | a | A-PRIVATE | `site/data/prompts.json:109 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3826 | c | BP-01 | `site/data/prompts.json:202 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3827 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-3828 | a | A-PRIVATE | `site/data/prompts.json:20 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3829 | a | A-PRIVATE | `site/data/prompts.json:97 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-3830 | a | A-PRIVATE | `site/data/prompts.json:98 (prompts[].content)` | `mango_ba_prompts` | [правила композиции]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции). |
| V-3831 | a | A-PRIVATE | `site/data/prompts.json:107 (prompts[].content)` | `mango_ba_prompts` | …ктуры — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-… |
| V-3832 | c | BP-01 | `site/data/prompts.json:185 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3833 | a | A-PRIVATE | `site/data/prompts.json:196 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3834 | c | BP-01 | `site/data/prompts.json:289 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3835 | a | A-PRIVATE | `site/data/prompts.json:9 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3836 | a | A-PRIVATE | `site/data/prompts.json:86 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-3837 | a | A-PRIVATE | `site/data/prompts.json:87 (prompts[].body)` | `mango_ba_prompts` | [правила композиции]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции). |
| V-3838 | a | A-PRIVATE | `site/data/prompts.json:96 (prompts[].body)` | `mango_ba_prompts` | …ктуры — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-… |
| V-3839 | c | BP-01 | `site/data/prompts.json:174 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3840 | a | A-PRIVATE | `site/data/prompts.json:185 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3841 | c | BP-01 | `site/data/prompts.json:278 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3842 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-3843 | c | BP-01 | `site/data/prompts.json:12 (prompts[].content)` | `<!--` | <!-- issue-474:entry --> |
| V-3844 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].content)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3845 | b | CT-01 | `site/data/prompts.json:63 (prompts[].content)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3846 | b | CT-02 | `site/data/prompts.json:63 (prompts[].content)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3847 | c | BP-01 | `site/data/prompts.json:85 (prompts[].content)` | `<!--` | <!-- /issue-474:entry --> |
| V-3848 | a | A-PRIVATE | `site/data/prompts.json:94 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3849 | a | A-PRIVATE | `site/data/prompts.json:113 (prompts[].content)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-3850 | a | A-PRIVATE | `site/data/prompts.json:114 (prompts[].content)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3851 | b | CT-09 | `site/data/prompts.json:140 (prompts[].content)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3852 | b | CT-09 | `site/data/prompts.json:140 (prompts[].content)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3853 | b | CT-04 | `site/data/prompts.json:141 (prompts[].content)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3854 | b | CT-05 | `site/data/prompts.json:141 (prompts[].content)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3855 | b | CT-09 | `site/data/prompts.json:141 (prompts[].content)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3856 | b | CT-09 | `site/data/prompts.json:141 (prompts[].content)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3857 | b | CT-09 | `site/data/prompts.json:141 (prompts[].content)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3858 | b | CT-09 | `site/data/prompts.json:141 (prompts[].content)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3859 | b | CT-09 | `site/data/prompts.json:141 (prompts[].content)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3860 | b | CT-09 | `site/data/prompts.json:142 (prompts[].content)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3861 | b | CT-09 | `site/data/prompts.json:142 (prompts[].content)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3862 | b | CT-09 | `site/data/prompts.json:142 (prompts[].content)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3863 | b | CT-09 | `site/data/prompts.json:142 (prompts[].content)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3864 | b | CT-09 | `site/data/prompts.json:142 (prompts[].content)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3865 | a | A-PRIVATE | `site/data/prompts.json:156 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3866 | a | A-PRIVATE | `site/data/prompts.json:159 (prompts[].content)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-3867 | b | CT-03 | `site/data/prompts.json:177 (prompts[].content)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-3868 | c | BP-01 | `site/data/prompts.json:225 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3869 | a | A-PRIVATE | `site/data/prompts.json:236 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3870 | c | BP-01 | `site/data/prompts.json:329 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3871 | c | BP-01 | `site/data/prompts.json:1 (prompts[].body)` | `<!--` | <!-- issue-474:entry --> |
| V-3872 | a | A-PRIVATE | `site/data/prompts.json:12 (prompts[].body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3873 | b | CT-01 | `site/data/prompts.json:52 (prompts[].body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3874 | b | CT-02 | `site/data/prompts.json:52 (prompts[].body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3875 | c | BP-01 | `site/data/prompts.json:74 (prompts[].body)` | `<!--` | <!-- /issue-474:entry --> |
| V-3876 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3877 | a | A-PRIVATE | `site/data/prompts.json:102 (prompts[].body)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-3878 | a | A-PRIVATE | `site/data/prompts.json:103 (prompts[].body)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-3879 | b | CT-09 | `site/data/prompts.json:129 (prompts[].body)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3880 | b | CT-09 | `site/data/prompts.json:129 (prompts[].body)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-3881 | b | CT-04 | `site/data/prompts.json:130 (prompts[].body)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3882 | b | CT-05 | `site/data/prompts.json:130 (prompts[].body)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3883 | b | CT-09 | `site/data/prompts.json:130 (prompts[].body)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3884 | b | CT-09 | `site/data/prompts.json:130 (prompts[].body)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3885 | b | CT-09 | `site/data/prompts.json:130 (prompts[].body)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3886 | b | CT-09 | `site/data/prompts.json:130 (prompts[].body)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3887 | b | CT-09 | `site/data/prompts.json:130 (prompts[].body)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-3888 | b | CT-09 | `site/data/prompts.json:131 (prompts[].body)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3889 | b | CT-09 | `site/data/prompts.json:131 (prompts[].body)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3890 | b | CT-09 | `site/data/prompts.json:131 (prompts[].body)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3891 | b | CT-09 | `site/data/prompts.json:131 (prompts[].body)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3892 | b | CT-09 | `site/data/prompts.json:131 (prompts[].body)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-3893 | a | A-PRIVATE | `site/data/prompts.json:145 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-3894 | a | A-PRIVATE | `site/data/prompts.json:148 (prompts[].body)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-3895 | b | CT-03 | `site/data/prompts.json:166 (prompts[].body)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-3896 | c | BP-01 | `site/data/prompts.json:214 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3897 | a | A-PRIVATE | `site/data/prompts.json:225 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3898 | c | BP-01 | `site/data/prompts.json:318 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3899 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-3900 | a | A-PRIVATE | `site/data/prompts.json:21 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3901 | a | A-PRIVATE | `site/data/prompts.json:65 (prompts[].content)` | `mango_ba_prompts` | [Контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты); |
| V-3902 | a | A-PRIVATE | `site/data/prompts.json:66 (prompts[].content)` | `mango_ba_prompts` | [мета-стандарты разделов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-3903 | c | BP-01 | `site/data/prompts.json:126 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3904 | a | A-PRIVATE | `site/data/prompts.json:137 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3905 | c | BP-01 | `site/data/prompts.json:231 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3906 | a | A-PRIVATE | `site/data/prompts.json:10 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3907 | a | A-PRIVATE | `site/data/prompts.json:54 (prompts[].body)` | `mango_ba_prompts` | [Контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты); |
| V-3908 | a | A-PRIVATE | `site/data/prompts.json:55 (prompts[].body)` | `mango_ba_prompts` | [мета-стандарты разделов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-3909 | c | BP-01 | `site/data/prompts.json:115 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3910 | a | A-PRIVATE | `site/data/prompts.json:126 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3911 | c | BP-01 | `site/data/prompts.json:220 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3912 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-3913 | a | A-PRIVATE | `site/data/prompts.json:21 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3914 | a | A-PRIVATE | `site/data/prompts.json:63 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md) |
| V-3915 | a | A-PRIVATE | `site/data/prompts.json:65 (prompts[].content)` | `mango_ba_prompts` | [архитектуры промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)). |
| V-3916 | c | BP-01 | `site/data/prompts.json:104 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3917 | a | A-PRIVATE | `site/data/prompts.json:115 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3918 | c | BP-01 | `site/data/prompts.json:208 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3919 | a | A-PRIVATE | `site/data/prompts.json:10 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3920 | a | A-PRIVATE | `site/data/prompts.json:52 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md) |
| V-3921 | a | A-PRIVATE | `site/data/prompts.json:54 (prompts[].body)` | `mango_ba_prompts` | [архитектуры промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)). |
| V-3922 | c | BP-01 | `site/data/prompts.json:93 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3923 | a | A-PRIVATE | `site/data/prompts.json:104 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3924 | c | BP-01 | `site/data/prompts.json:197 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3925 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-3926 | a | A-PRIVATE | `site/data/prompts.json:21 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3927 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].content)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-3928 | c | BP-01 | `site/data/prompts.json:145 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3929 | a | A-PRIVATE | `site/data/prompts.json:156 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3930 | c | BP-01 | `site/data/prompts.json:249 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3931 | a | A-PRIVATE | `site/data/prompts.json:10 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3932 | a | A-PRIVATE | `site/data/prompts.json:72 (prompts[].body)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-3933 | c | BP-01 | `site/data/prompts.json:134 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3934 | a | A-PRIVATE | `site/data/prompts.json:145 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3935 | c | BP-01 | `site/data/prompts.json:238 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3936 | a | A-PRIVATE | `site/data/prompts.json:1 (prompts[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-work-solution-design-oneshot.md |
| V-3937 | a | A-PRIVATE | `site/data/prompts.json:21 (prompts[].content)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3938 | a | A-PRIVATE | `site/data/prompts.json:34 (prompts[].content)` | `mango_ba_prompts` | [Ш-В]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) |
| V-3939 | a | A-PRIVATE | `site/data/prompts.json:82 (prompts[].content)` | `mango_ba_prompts` | [Раздел 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-3940 | a | A-PRIVATE | `site/data/prompts.json:83 (prompts[].content)` | `mango_ba_prompts` | [раздел 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md); |
| V-3941 | a | A-PRIVATE | `site/data/prompts.json:84 (prompts[].content)` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-3942 | a | A-PRIVATE | `site/data/prompts.json:85 (prompts[].content)` | `mango_ba_prompts` | [раздел 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md); |
| V-3943 | a | A-PRIVATE | `site/data/prompts.json:86 (prompts[].content)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции); |
| V-3944 | a | A-PRIVATE | `site/data/prompts.json:87 (prompts[].content)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3945 | a | A-PRIVATE | `site/data/prompts.json:106 (prompts[].content)` | `mango_ba_prompts` | [Ш-6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md#проверка-последовательности-и-контракта) |
| V-3946 | a | A-PRIVATE | `site/data/prompts.json:108 (prompts[].content)` | `mango_ba_prompts` | [Ш-8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md#проверка-покрытия-условий-контракта). |
| V-3947 | c | BP-01 | `site/data/prompts.json:156 (prompts[].content)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3948 | a | A-PRIVATE | `site/data/prompts.json:167 (prompts[].content)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3949 | c | BP-01 | `site/data/prompts.json:260 (prompts[].content)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3950 | a | A-PRIVATE | `site/data/prompts.json:10 (prompts[].body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-3951 | a | A-PRIVATE | `site/data/prompts.json:23 (prompts[].body)` | `mango_ba_prompts` | [Ш-В]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) |
| V-3952 | a | A-PRIVATE | `site/data/prompts.json:71 (prompts[].body)` | `mango_ba_prompts` | [Раздел 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-3953 | a | A-PRIVATE | `site/data/prompts.json:72 (prompts[].body)` | `mango_ba_prompts` | [раздел 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md); |
| V-3954 | a | A-PRIVATE | `site/data/prompts.json:73 (prompts[].body)` | `mango_ba_prompts` | [раздел 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md); |
| V-3955 | a | A-PRIVATE | `site/data/prompts.json:74 (prompts[].body)` | `mango_ba_prompts` | [раздел 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md); |
| V-3956 | a | A-PRIVATE | `site/data/prompts.json:75 (prompts[].body)` | `mango_ba_prompts` | [композиция]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции); |
| V-3957 | a | A-PRIVATE | `site/data/prompts.json:76 (prompts[].body)` | `mango_ba_prompts` | [контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты). |
| V-3958 | a | A-PRIVATE | `site/data/prompts.json:95 (prompts[].body)` | `mango_ba_prompts` | [Ш-6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md#проверка-последовательности-и-контракта) |
| V-3959 | a | A-PRIVATE | `site/data/prompts.json:97 (prompts[].body)` | `mango_ba_prompts` | [Ш-8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md#проверка-покрытия-условий-контракта). |
| V-3960 | c | BP-01 | `site/data/prompts.json:145 (prompts[].body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-3961 | a | A-PRIVATE | `site/data/prompts.json:156 (prompts[].body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-3962 | c | BP-01 | `site/data/prompts.json:249 (prompts[].body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-3963 | a | A-PRIVATE | `site/data/roadmap.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md |
| V-3964 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/README.md |
| V-3965 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md |
| V-3966 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/00-index.md |
| V-3967 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-ecosystem.md |
| V-3968 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/patterns/README.md |
| V-3969 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-manual-process.md |
| V-3970 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-run-kit.md |
| V-3971 | a | A-PRIVATE | `site/data/stats.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json |
| V-3972 | a | A-PRIVATE | `site/data/step-handoff.json:1 (issue)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/issues/490 |
| V-3973 | b | CT-03 | `site/data/step-handoff.json:1 (steps.AIN-06.goal)` | `коннектора` | …понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.… |
| V-3974 | b | CT-05 | `site/data/step-handoff.json:1 (steps.AIN-06.check)` | `ЛК` | у каждой связи есть источник; ЛК, права и настройки рассмотрены |
| V-3975 | b | CT-05 | `site/data/step-handoff.json:15 (steps.AIN-06.block)` | `ЛК` | …технический, можно проверить (у каждой связи есть источник; ЛК, права и настройки рассмотрены), но не обязательно. ИИ-ассистент ожидает ввода промпта … |
| V-3976 | a | A-PRIVATE | `site/data/test-kit.json:1 (sourceFiles[].url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-run-kit.md |
| V-3977 | a | A-PRIVATE | `site/data/test-kit.json:1 (kit.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-run-kit.md |
| V-3978 | b | CT-03 | `site/data/test-kit.json:1 (handoff.steps.AIN-06.goal)` | `коннектора` | …понентов как кандидатов с источниками. Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.… |
| V-3979 | b | CT-05 | `site/data/test-kit.json:1 (handoff.steps.AIN-06.check)` | `ЛК` | у каждой связи есть источник; ЛК, права и настройки рассмотрены |
| V-3980 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md |
| V-3981 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md |
| V-3982 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3983 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3984 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3985 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-3986 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-3987 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко… |
| V-3988 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#490` | …438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.… |
| V-3989 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» … |
| V-3990 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по… |
| V-3991 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-3992 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-3993 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);… |
| V-3994 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-3995 | c | BP-01 | `site/data/test-kit.json:5 (steps[].draft.body)` | `<!--` | <!-- issue-474:entry --> |
| V-3996 | c | BP-02 | `site/data/test-kit.json:8 (steps[].draft.body)` | `#490` | …, формат шагов и исходный запрос без анализа. Формат шагов (#490) задаёт сайт строкой «Формат шагов: системный» или «Формат шагов: декомпозированный»;… |
| V-3997 | a | A-PRIVATE | `site/data/test-kit.json:18 (steps[].draft.body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-3998 | b | CT-01 | `site/data/test-kit.json:58 (steps[].draft.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-3999 | b | CT-02 | `site/data/test-kit.json:58 (steps[].draft.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4000 | c | BP-01 | `site/data/test-kit.json:80 (steps[].draft.body)` | `<!--` | <!-- /issue-474:entry --> |
| V-4001 | a | A-PRIVATE | `site/data/test-kit.json:94 (steps[].draft.body)` | `mango_ba_prompts` | - [Мета-стандарты разделов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md) |
| V-4002 | a | A-PRIVATE | `site/data/test-kit.json:95 (steps[].draft.body)` | `mango_ba_prompts` | - [Архитектура промптов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md) |
| V-4003 | a | A-PRIVATE | `site/data/test-kit.json:96 (steps[].draft.body)` | `mango_ba_prompts` | - [Контракт стадий и гейтов BCREQ]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md) |
| V-4004 | a | A-PRIVATE | `site/data/test-kit.json:97 (steps[].draft.body)` | `mango_ba_prompts` | - [Стандарт композиции продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md) |
| V-4005 | a | A-PRIVATE | `site/data/test-kit.json:115 (steps[].draft.body)` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md), на Ш-0 о них не спрашивай: |
| V-4006 | b | CT-04 | `site/data/test-kit.json:119 (steps[].draft.body)` | `ВАТС` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-4007 | b | CT-05 | `site/data/test-kit.json:119 (steps[].draft.body)` | `ЛК` | \| `продукты` \| профили: ЛК, ВАТС, КЦ, РА, API, оператор связи \| из анкеты; если не ясно — вопрос БА \| |
| V-4008 | a | A-PRIVATE | `site/data/test-kit.json:127 (steps[].draft.body)` | `mango_ba_prompts` | [стандарте композиции §4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-4009 | a | A-PRIVATE | `site/data/test-kit.json:153 (steps[].draft.body)` | `mango_ba_prompts` | [AIN-01]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/a-in/bcreq-ain-01-understanding-stepwise.md), в системном — |
| V-4010 | a | A-PRIVATE | `site/data/test-kit.json:154 (steps[].draft.body)` | `mango_ba_prompts` | [Ш-А]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md). Остановись. |
| V-4011 | a | A-PRIVATE | `site/data/test-kit.json:176 (steps[].draft.body)` | `mango_ba_prompts` | [standards/bcreq-sections]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#1-восемь-разделов). |
| V-4012 | a | A-PRIVATE | `site/data/test-kit.json:196 (steps[].draft.body)` | `mango_ba_prompts` | [README §2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md#2-стили). |
| V-4013 | a | A-PRIVATE | `site/data/test-kit.json:223 (steps[].draft.body)` | `mango_ba_prompts` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-4014 | c | BP-04 | `site/data/test-kit.json:223 (steps[].draft.body)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-4015 | c | BP-04 | `site/data/test-kit.json:223 (steps[].draft.body)` | `RUN-0` | [RUN-0075]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/error-statistics.md) |
| V-4016 | a | A-PRIVATE | `site/data/test-kit.json:225 (steps[].draft.body)` | `mango_ba_prompts` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-4017 | c | BP-04 | `site/data/test-kit.json:225 (steps[].draft.body)` | `RUN-0` | [success-criteria]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/success-criteria.md), |
| V-4018 | a | A-PRIVATE | `site/data/test-kit.json:227 (steps[].draft.body)` | `mango_ba_prompts` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-4019 | c | BP-04 | `site/data/test-kit.json:227 (steps[].draft.body)` | `RUN-0` | [runtime-improvements]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/runs/2026/RUN-0075/outputs/runtime-improvements.md). |
| V-4020 | c | BP-04 | `site/data/test-kit.json:229 (steps[].draft.body)` | `RUN-0` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-4021 | c | BP-12 | `site/data/test-kit.json:229 (steps[].draft.body)` | `Категория RUN` | \| ID \| Защита \| Правило \| Категория RUN-0075 \| |
| V-4022 | c | BP-02 | `site/data/test-kit.json:239 (steps[].draft.body)` | `#391` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-4023 | c | BP-03 | `site/data/test-kit.json:239 (steps[].draft.body)` | `issue` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-4024 | c | BP-12 | `site/data/test-kit.json:239 (steps[].draft.body)` | `ревизии Golden` | #### Дополнения по ревизии Golden Set (issue #391) |
| V-4025 | b | CT-03 | `site/data/test-kit.json:246 (steps[].draft.body)` | `коннекторе` | …; наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе. «Не описано», «источник недоступен» и «явно не поддерживает… |
| V-4026 | c | BP-04 | `site/data/test-kit.json:261 (steps[].draft.body)` | `RUN-0` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-4027 | c | BP-04 | `site/data/test-kit.json:261 (steps[].draft.body)` | `SC-6` | об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65). |
| V-4028 | a | A-PRIVATE | `site/data/test-kit.json:282 (steps[].draft.body)` | `mango_ba_prompts` | …eq-intake-questionnaire-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md) \|… |
| V-4029 | a | A-PRIVATE | `site/data/test-kit.json:283 (steps[].draft.body)` | `mango_ba_prompts` | …q-context-understanding-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-context-understanding-system.md) \|… |
| V-4030 | a | A-PRIVATE | `site/data/test-kit.json:284 (steps[].draft.body)` | `mango_ba_prompts` | …roducts-impact-analysis-system]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-products-impact-analysis-system.md)… |
| V-4031 | a | A-PRIVATE | `site/data/test-kit.json:285 (steps[].draft.body)` | `mango_ba_prompts` | …creq-fr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md) \|… |
| V-4032 | a | A-PRIVATE | `site/data/test-kit.json:286 (steps[].draft.body)` | `mango_ba_prompts` | …req-nfr-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md) \|… |
| V-4033 | a | A-PRIVATE | `site/data/test-kit.json:287 (steps[].draft.body)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-4034 | a | A-PRIVATE | `site/data/test-kit.json:288 (steps[].draft.body)` | `mango_ba_prompts` | …q-orr-solution-design-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md) \|… |
| V-4035 | a | A-PRIVATE | `site/data/test-kit.json:289 (steps[].draft.body)` | `mango_ba_prompts` | …traints-documentation-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md) \|… |
| V-4036 | a | A-PRIVATE | `site/data/test-kit.json:290 (steps[].draft.body)` | `mango_ba_prompts` | … \| [bcreq-uc-modeling-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md) \|… |
| V-4037 | a | A-PRIVATE | `site/data/test-kit.json:291 (steps[].draft.body)` | `mango_ba_prompts` | …q-extra-risk-analysis-stepwise]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md) \|… |
| V-4038 | a | A-PRIVATE | `site/data/test-kit.json:292 (steps[].draft.body)` | `mango_ba_prompts` | …creq-review-validation-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md) \|… |
| V-4039 | a | A-PRIVATE | `site/data/test-kit.json:293 (steps[].draft.body)` | `mango_ba_prompts` | …req-scenarios-modeling-oneshot]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md) \|… |
| V-4040 | c | BP-02 | `site/data/test-kit.json:299 (steps[].draft.body)` | `#490` | **Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из |
| V-4041 | a | A-PRIVATE | `site/data/test-kit.json:301 (steps[].draft.body)` | `mango_ba_prompts` | [AIN-01…AIN-24]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md) |
| V-4042 | a | A-PRIVATE | `site/data/test-kit.json:318 (steps[].draft.body)` | `mango_ba_prompts` | [контракта гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#3-возвраты)). |
| V-4043 | a | A-PRIVATE | `site/data/test-kit.json:322 (steps[].draft.body)` | `mango_ba_prompts` | [поток CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-4044 | c | BP-01 | `site/data/test-kit.json:370 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4045 | a | A-PRIVATE | `site/data/test-kit.json:381 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4046 | c | BP-01 | `site/data/test-kit.json:474 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4047 | c | BP-01 | `site/data/test-kit.json:476 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4048 | c | BP-06 | `site/data/test-kit.json:476 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4049 | c | BP-04 | `site/data/test-kit.json:477 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4050 | c | BP-06 | `site/data/test-kit.json:477 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4051 | c | BP-02 | `site/data/test-kit.json:479 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4052 | c | BP-06 | `site/data/test-kit.json:479 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4053 | c | BP-09 | `site/data/test-kit.json:479 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4054 | c | BP-07 | `site/data/test-kit.json:481 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4055 | a | A-PRIVATE | `site/data/test-kit.json:482 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4056 | c | BP-02 | `site/data/test-kit.json:482 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4057 | a | A-PRIVATE | `site/data/test-kit.json:483 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4058 | a | A-PRIVATE | `site/data/test-kit.json:484 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4059 | a | A-PRIVATE | `site/data/test-kit.json:485 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4060 | a | A-PRIVATE | `site/data/test-kit.json:486 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4061 | c | BP-06 | `site/data/test-kit.json:497 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4062 | a | A-PRIVATE | `site/data/test-kit.json:539 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4063 | c | BP-04 | `site/data/test-kit.json:542 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4064 | c | BP-04 | `site/data/test-kit.json:542 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4065 | c | BP-04 | `site/data/test-kit.json:565 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4066 | c | BP-10 | `site/data/test-kit.json:565 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4067 | c | BP-10 | `site/data/test-kit.json:565 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4068 | c | BP-01 | `site/data/test-kit.json:626 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4069 | c | BP-06 | `site/data/test-kit.json:626 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4070 | c | BP-01 | `site/data/test-kit.json:628 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4071 | c | BP-02 | `site/data/test-kit.json:629 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4072 | c | BP-01 | `site/data/test-kit.json:650 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4073 | b | CT-04 | `site/data/test-kit.json:1 (steps[].prepare)` | `ВАТС` | Подключённые у Заказчика продукты, число операторов, номера ВАТС и сторонние номера, объём коммуникаций в месяц, если известны |
| V-4074 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-intake-questionnaire-system.md |
| V-4075 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.body)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4076 | c | BP-01 | `site/data/test-kit.json:1 (steps[].system.body)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4077 | c | BP-08 | `site/data/test-kit.json:1 (steps[].system.body)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4078 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-4079 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без про… |
| V-4080 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4081 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#464` | …. Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4082 | c | BP-03 | `site/data/test-kit.json:3 (steps[].system.body)` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4083 | c | BP-03 | `site/data/test-kit.json:3 (steps[].system.body)` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4084 | c | BP-04 | `site/data/test-kit.json:3 (steps[].system.body)` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4085 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): ш… |
| V-4086 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): ш… |
| V-4087 | c | BP-08 | `site/data/test-kit.json:3 (steps[].system.body)` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-4088 | c | BP-09 | `site/data/test-kit.json:3 (steps[].system.body)` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): шаг без промпта v0… |
| V-4089 | c | BP-11 | `site/data/test-kit.json:3 (steps[].system.body)` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-4090 | c | BP-01 | `site/data/test-kit.json:7 (steps[].system.body)` | `<!--` | <!-- issue-490:system --> |
| V-4091 | c | BP-02 | `site/data/test-kit.json:8 (steps[].system.body)` | `#490` | ## Системный формат шагов (#490) |
| V-4092 | a | A-PRIVATE | `site/data/test-kit.json:12 (steps[].system.body)` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4093 | c | BP-02 | `site/data/test-kit.json:12 (steps[].system.body)` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4094 | c | BP-03 | `site/data/test-kit.json:12 (steps[].system.body)` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4095 | b | CT-01 | `site/data/test-kit.json:70 (steps[].system.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4096 | b | CT-02 | `site/data/test-kit.json:70 (steps[].system.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4097 | c | BP-01 | `site/data/test-kit.json:92 (steps[].system.body)` | `<!--` | <!-- /issue-490:system --> |
| V-4098 | a | A-PRIVATE | `site/data/test-kit.json:96 (steps[].system.body)` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-4099 | a | A-PRIVATE | `site/data/test-kit.json:102 (steps[].system.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-4100 | b | CT-04 | `site/data/test-kit.json:143 (steps[].system.body)` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-4101 | a | A-PRIVATE | `site/data/test-kit.json:156 (steps[].system.body)` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-4102 | b | CT-04 | `site/data/test-kit.json:173 (steps[].system.body)` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-4103 | c | BP-01 | `site/data/test-kit.json:196 (steps[].system.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4104 | c | BP-06 | `site/data/test-kit.json:196 (steps[].system.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4105 | c | BP-04 | `site/data/test-kit.json:197 (steps[].system.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4106 | c | BP-06 | `site/data/test-kit.json:197 (steps[].system.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4107 | c | BP-02 | `site/data/test-kit.json:199 (steps[].system.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4108 | c | BP-06 | `site/data/test-kit.json:199 (steps[].system.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4109 | c | BP-09 | `site/data/test-kit.json:199 (steps[].system.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4110 | c | BP-07 | `site/data/test-kit.json:201 (steps[].system.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4111 | a | A-PRIVATE | `site/data/test-kit.json:202 (steps[].system.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4112 | c | BP-02 | `site/data/test-kit.json:202 (steps[].system.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4113 | a | A-PRIVATE | `site/data/test-kit.json:203 (steps[].system.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4114 | a | A-PRIVATE | `site/data/test-kit.json:204 (steps[].system.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4115 | a | A-PRIVATE | `site/data/test-kit.json:205 (steps[].system.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4116 | a | A-PRIVATE | `site/data/test-kit.json:206 (steps[].system.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4117 | c | BP-06 | `site/data/test-kit.json:217 (steps[].system.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4118 | a | A-PRIVATE | `site/data/test-kit.json:257 (steps[].system.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4119 | c | BP-04 | `site/data/test-kit.json:260 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4120 | c | BP-04 | `site/data/test-kit.json:260 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4121 | c | BP-04 | `site/data/test-kit.json:283 (steps[].system.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4122 | c | BP-10 | `site/data/test-kit.json:283 (steps[].system.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4123 | c | BP-10 | `site/data/test-kit.json:283 (steps[].system.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4124 | c | BP-01 | `site/data/test-kit.json:311 (steps[].system.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4125 | c | BP-06 | `site/data/test-kit.json:311 (steps[].system.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4126 | c | BP-01 | `site/data/test-kit.json:313 (steps[].system.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4127 | c | BP-02 | `site/data/test-kit.json:314 (steps[].system.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4128 | c | BP-01 | `site/data/test-kit.json:335 (steps[].system.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4129 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-intake-questionnaire-stepwise.md |
| V-4130 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4131 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4132 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4133 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4134 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-4135 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4136 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#464` | …* Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4137 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4138 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4139 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.… |
| V-4140 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-4141 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-4142 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце… |
| V-4143 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тес… |
| V-4144 | c | BP-01 | `site/data/test-kit.json:4 (steps[].draft.body)` | `<!--` | <!-- issue-474:entry --> |
| V-4145 | a | A-PRIVATE | `site/data/test-kit.json:10 (steps[].draft.body)` | `mango_ba_prompts` | [AIN-02]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/a-in/bcreq-ain-02-understanding-stepwise.md). |
| V-4146 | b | CT-01 | `site/data/test-kit.json:57 (steps[].draft.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4147 | b | CT-02 | `site/data/test-kit.json:57 (steps[].draft.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4148 | c | BP-01 | `site/data/test-kit.json:79 (steps[].draft.body)` | `<!--` | <!-- /issue-474:entry --> |
| V-4149 | a | A-PRIVATE | `site/data/test-kit.json:86 (steps[].draft.body)` | `mango_ba_prompts` | [справочника стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#1-выбор-стандартов). |
| V-4150 | a | A-PRIVATE | `site/data/test-kit.json:92 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4151 | b | CT-04 | `site/data/test-kit.json:133 (steps[].draft.body)` | `ВАТС` | 3. Сколько номеров Mango ВАТС? |
| V-4152 | a | A-PRIVATE | `site/data/test-kit.json:146 (steps[].draft.body)` | `mango_ba_prompts` | [справочнике стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md)): |
| V-4153 | b | CT-04 | `site/data/test-kit.json:163 (steps[].draft.body)` | `ВАТС` | - номера ВАТС: <…\|UNKNOWN>; сторонние номера: <…\|UNKNOWN> |
| V-4154 | c | BP-01 | `site/data/test-kit.json:186 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4155 | c | BP-06 | `site/data/test-kit.json:186 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4156 | c | BP-04 | `site/data/test-kit.json:187 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4157 | c | BP-06 | `site/data/test-kit.json:187 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4158 | c | BP-02 | `site/data/test-kit.json:189 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4159 | c | BP-06 | `site/data/test-kit.json:189 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4160 | c | BP-09 | `site/data/test-kit.json:189 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4161 | c | BP-07 | `site/data/test-kit.json:191 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4162 | a | A-PRIVATE | `site/data/test-kit.json:192 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4163 | c | BP-02 | `site/data/test-kit.json:192 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4164 | a | A-PRIVATE | `site/data/test-kit.json:193 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4165 | a | A-PRIVATE | `site/data/test-kit.json:194 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4166 | a | A-PRIVATE | `site/data/test-kit.json:195 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4167 | a | A-PRIVATE | `site/data/test-kit.json:196 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4168 | c | BP-06 | `site/data/test-kit.json:207 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4169 | a | A-PRIVATE | `site/data/test-kit.json:247 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4170 | c | BP-04 | `site/data/test-kit.json:250 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4171 | c | BP-04 | `site/data/test-kit.json:250 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4172 | c | BP-04 | `site/data/test-kit.json:273 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4173 | c | BP-10 | `site/data/test-kit.json:273 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4174 | c | BP-10 | `site/data/test-kit.json:273 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4175 | c | BP-01 | `site/data/test-kit.json:301 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4176 | c | BP-06 | `site/data/test-kit.json:301 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4177 | c | BP-01 | `site/data/test-kit.json:303 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4178 | c | BP-02 | `site/data/test-kit.json:304 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4179 | c | BP-01 | `site/data/test-kit.json:325 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4180 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-context-understanding-system.md |
| V-4181 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.body)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4182 | c | BP-01 | `site/data/test-kit.json:1 (steps[].system.body)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4183 | c | BP-08 | `site/data/test-kit.json:1 (steps[].system.body)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4184 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-4185 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага … |
| V-4186 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4187 | c | BP-03 | `site/data/test-kit.json:3 (steps[].system.body)` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4188 | c | BP-04 | `site/data/test-kit.json:3 (steps[].system.body)` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4189 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-4190 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-4191 | c | BP-08 | `site/data/test-kit.json:3 (steps[].system.body)` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4192 | c | BP-09 | `site/data/test-kit.json:3 (steps[].system.body)` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ни… |
| V-4193 | c | BP-11 | `site/data/test-kit.json:3 (steps[].system.body)` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-4194 | c | BP-01 | `site/data/test-kit.json:7 (steps[].system.body)` | `<!--` | <!-- issue-490:system --> |
| V-4195 | c | BP-02 | `site/data/test-kit.json:8 (steps[].system.body)` | `#490` | ## Системный формат шагов (#490) |
| V-4196 | a | A-PRIVATE | `site/data/test-kit.json:12 (steps[].system.body)` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4197 | c | BP-02 | `site/data/test-kit.json:12 (steps[].system.body)` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4198 | c | BP-03 | `site/data/test-kit.json:12 (steps[].system.body)` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4199 | b | CT-01 | `site/data/test-kit.json:70 (steps[].system.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4200 | b | CT-02 | `site/data/test-kit.json:70 (steps[].system.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4201 | c | BP-01 | `site/data/test-kit.json:92 (steps[].system.body)` | `<!--` | <!-- /issue-490:system --> |
| V-4202 | a | A-PRIVATE | `site/data/test-kit.json:98 (steps[].system.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-4203 | a | A-PRIVATE | `site/data/test-kit.json:182 (steps[].system.body)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-4204 | a | A-PRIVATE | `site/data/test-kit.json:214 (steps[].system.body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-4205 | a | A-PRIVATE | `site/data/test-kit.json:219 (steps[].system.body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-4206 | c | BP-01 | `site/data/test-kit.json:311 (steps[].system.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4207 | a | A-PRIVATE | `site/data/test-kit.json:322 (steps[].system.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md), |
| V-4208 | c | BP-01 | `site/data/test-kit.json:415 (steps[].system.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4209 | c | BP-01 | `site/data/test-kit.json:417 (steps[].system.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4210 | c | BP-06 | `site/data/test-kit.json:417 (steps[].system.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4211 | c | BP-04 | `site/data/test-kit.json:418 (steps[].system.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4212 | c | BP-06 | `site/data/test-kit.json:418 (steps[].system.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4213 | c | BP-02 | `site/data/test-kit.json:420 (steps[].system.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4214 | c | BP-06 | `site/data/test-kit.json:420 (steps[].system.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4215 | c | BP-09 | `site/data/test-kit.json:420 (steps[].system.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4216 | c | BP-07 | `site/data/test-kit.json:422 (steps[].system.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4217 | a | A-PRIVATE | `site/data/test-kit.json:423 (steps[].system.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4218 | c | BP-02 | `site/data/test-kit.json:423 (steps[].system.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4219 | a | A-PRIVATE | `site/data/test-kit.json:424 (steps[].system.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4220 | a | A-PRIVATE | `site/data/test-kit.json:425 (steps[].system.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4221 | a | A-PRIVATE | `site/data/test-kit.json:426 (steps[].system.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4222 | a | A-PRIVATE | `site/data/test-kit.json:427 (steps[].system.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4223 | c | BP-06 | `site/data/test-kit.json:438 (steps[].system.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4224 | a | A-PRIVATE | `site/data/test-kit.json:478 (steps[].system.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4225 | c | BP-04 | `site/data/test-kit.json:481 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4226 | c | BP-04 | `site/data/test-kit.json:481 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4227 | c | BP-04 | `site/data/test-kit.json:504 (steps[].system.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4228 | c | BP-10 | `site/data/test-kit.json:504 (steps[].system.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4229 | c | BP-10 | `site/data/test-kit.json:504 (steps[].system.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4230 | c | BP-01 | `site/data/test-kit.json:606 (steps[].system.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4231 | c | BP-06 | `site/data/test-kit.json:606 (steps[].system.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4232 | c | BP-01 | `site/data/test-kit.json:608 (steps[].system.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4233 | c | BP-02 | `site/data/test-kit.json:609 (steps[].system.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4234 | c | BP-01 | `site/data/test-kit.json:630 (steps[].system.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4235 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-context-understanding-stepwise.md |
| V-4236 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-context-understanding-stepwise.md |
| V-4237 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4238 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4239 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4240 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4241 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4242 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4243 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4244 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4245 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4246 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4247 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4248 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4249 | c | BP-01 | `site/data/test-kit.json:5 (steps[].draft.body)` | `<!--` | <!-- issue-474:entry --> |
| V-4250 | a | A-PRIVATE | `site/data/test-kit.json:16 (steps[].draft.body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-4251 | b | CT-01 | `site/data/test-kit.json:56 (steps[].draft.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4252 | b | CT-02 | `site/data/test-kit.json:56 (steps[].draft.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4253 | c | BP-01 | `site/data/test-kit.json:78 (steps[].draft.body)` | `<!--` | <!-- /issue-474:entry --> |
| V-4254 | a | A-PRIVATE | `site/data/test-kit.json:87 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4255 | a | A-PRIVATE | `site/data/test-kit.json:171 (steps[].draft.body)` | `mango_ba_prompts` | [CS]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/cs-flow-stub.md). |
| V-4256 | a | A-PRIVATE | `site/data/test-kit.json:203 (steps[].draft.body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md). |
| V-4257 | a | A-PRIVATE | `site/data/test-kit.json:208 (steps[].draft.body)` | `mango_ba_prompts` | [мета-стандарт]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-4258 | c | BP-01 | `site/data/test-kit.json:300 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4259 | a | A-PRIVATE | `site/data/test-kit.json:311 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4260 | c | BP-01 | `site/data/test-kit.json:404 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4261 | c | BP-01 | `site/data/test-kit.json:406 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4262 | c | BP-06 | `site/data/test-kit.json:406 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4263 | c | BP-04 | `site/data/test-kit.json:407 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4264 | c | BP-06 | `site/data/test-kit.json:407 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4265 | c | BP-02 | `site/data/test-kit.json:409 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4266 | c | BP-06 | `site/data/test-kit.json:409 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4267 | c | BP-09 | `site/data/test-kit.json:409 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4268 | c | BP-07 | `site/data/test-kit.json:411 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4269 | a | A-PRIVATE | `site/data/test-kit.json:412 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4270 | c | BP-02 | `site/data/test-kit.json:412 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4271 | a | A-PRIVATE | `site/data/test-kit.json:413 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4272 | a | A-PRIVATE | `site/data/test-kit.json:414 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4273 | a | A-PRIVATE | `site/data/test-kit.json:415 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4274 | a | A-PRIVATE | `site/data/test-kit.json:416 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4275 | c | BP-06 | `site/data/test-kit.json:427 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4276 | a | A-PRIVATE | `site/data/test-kit.json:467 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4277 | c | BP-04 | `site/data/test-kit.json:470 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4278 | c | BP-04 | `site/data/test-kit.json:470 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4279 | c | BP-04 | `site/data/test-kit.json:493 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4280 | c | BP-10 | `site/data/test-kit.json:493 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4281 | c | BP-10 | `site/data/test-kit.json:493 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4282 | c | BP-01 | `site/data/test-kit.json:595 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4283 | c | BP-06 | `site/data/test-kit.json:595 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4284 | c | BP-01 | `site/data/test-kit.json:597 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4285 | c | BP-02 | `site/data/test-kit.json:598 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4286 | c | BP-01 | `site/data/test-kit.json:619 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4287 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/system/bcreq-products-impact-analysis-system.md |
| V-4288 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].system.body)` | `mango_ba_prompts` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4289 | c | BP-01 | `site/data/test-kit.json:1 (steps[].system.body)` | `<!--` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4290 | c | BP-08 | `site/data/test-kit.json:1 (steps[].system.body)` | `Experimental` | <!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/490, no formal research yet --> |
| V-4291 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#490` | > **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».… |
| V-4292 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#427` | …едакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага … |
| V-4293 | c | BP-02 | `site/data/test-kit.json:3 (steps[].system.body)` | `#438` | …вует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4294 | c | BP-03 | `site/data/test-kit.json:3 (steps[].system.body)` | `issue` | … действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4295 | c | BP-04 | `site/data/test-kit.json:3 (steps[].system.body)` | `BL-1` | … (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4296 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-4297 | c | BP-06 | `site/data/test-kit.json:3 (steps[].system.body)` | `по тесту` | …): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): т… |
| V-4298 | c | BP-08 | `site/data/test-kit.json:3 (steps[].system.body)` | `Черновик BL` | … по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4299 | c | BP-09 | `site/data/test-kit.json:3 (steps[].system.body)` | `действует до ADR` | … сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черновик BL-156 (issue #438): текст шага v0.1 ни… |
| V-4300 | c | BP-11 | `site/data/test-kit.json:3 (steps[].system.body)` | `История баннер` | …истемный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования». Черн… |
| V-4301 | c | BP-01 | `site/data/test-kit.json:7 (steps[].system.body)` | `<!--` | <!-- issue-490:system --> |
| V-4302 | c | BP-02 | `site/data/test-kit.json:8 (steps[].system.body)` | `#490` | ## Системный формат шагов (#490) |
| V-4303 | a | A-PRIVATE | `site/data/test-kit.json:12 (steps[].system.body)` | `mango_ba_prompts` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4304 | c | BP-02 | `site/data/test-kit.json:12 (steps[].system.body)` | `#490` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4305 | c | BP-03 | `site/data/test-kit.json:12 (steps[].system.body)` | `issue` | ([issue #490]\(https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат на сайте: не предлагай |
| V-4306 | b | CT-01 | `site/data/test-kit.json:70 (steps[].system.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4307 | b | CT-02 | `site/data/test-kit.json:70 (steps[].system.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4308 | c | BP-01 | `site/data/test-kit.json:92 (steps[].system.body)` | `<!--` | <!-- /issue-490:system --> |
| V-4309 | a | A-PRIVATE | `site/data/test-kit.json:98 (steps[].system.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md); |
| V-4310 | a | A-PRIVATE | `site/data/test-kit.json:117 (steps[].system.body)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-4311 | a | A-PRIVATE | `site/data/test-kit.json:118 (steps[].system.body)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-4312 | b | CT-09 | `site/data/test-kit.json:144 (steps[].system.body)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-4313 | b | CT-09 | `site/data/test-kit.json:144 (steps[].system.body)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-4314 | b | CT-04 | `site/data/test-kit.json:145 (steps[].system.body)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4315 | b | CT-05 | `site/data/test-kit.json:145 (steps[].system.body)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4316 | b | CT-09 | `site/data/test-kit.json:145 (steps[].system.body)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4317 | b | CT-09 | `site/data/test-kit.json:145 (steps[].system.body)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4318 | b | CT-09 | `site/data/test-kit.json:145 (steps[].system.body)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4319 | b | CT-09 | `site/data/test-kit.json:145 (steps[].system.body)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4320 | b | CT-09 | `site/data/test-kit.json:145 (steps[].system.body)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4321 | b | CT-09 | `site/data/test-kit.json:146 (steps[].system.body)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4322 | b | CT-09 | `site/data/test-kit.json:146 (steps[].system.body)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4323 | b | CT-09 | `site/data/test-kit.json:146 (steps[].system.body)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4324 | b | CT-09 | `site/data/test-kit.json:146 (steps[].system.body)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4325 | b | CT-09 | `site/data/test-kit.json:146 (steps[].system.body)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4326 | a | A-PRIVATE | `site/data/test-kit.json:160 (steps[].system.body)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-4327 | a | A-PRIVATE | `site/data/test-kit.json:163 (steps[].system.body)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-4328 | b | CT-03 | `site/data/test-kit.json:181 (steps[].system.body)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-4329 | c | BP-01 | `site/data/test-kit.json:229 (steps[].system.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4330 | a | A-PRIVATE | `site/data/test-kit.json:240 (steps[].system.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constitution-governance-oneshot.md), |
| V-4331 | c | BP-01 | `site/data/test-kit.json:333 (steps[].system.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4332 | c | BP-01 | `site/data/test-kit.json:335 (steps[].system.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4333 | c | BP-06 | `site/data/test-kit.json:335 (steps[].system.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4334 | c | BP-04 | `site/data/test-kit.json:336 (steps[].system.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4335 | c | BP-06 | `site/data/test-kit.json:336 (steps[].system.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4336 | c | BP-02 | `site/data/test-kit.json:338 (steps[].system.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4337 | c | BP-06 | `site/data/test-kit.json:338 (steps[].system.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4338 | c | BP-09 | `site/data/test-kit.json:338 (steps[].system.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4339 | c | BP-07 | `site/data/test-kit.json:340 (steps[].system.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4340 | a | A-PRIVATE | `site/data/test-kit.json:341 (steps[].system.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4341 | c | BP-02 | `site/data/test-kit.json:341 (steps[].system.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4342 | a | A-PRIVATE | `site/data/test-kit.json:342 (steps[].system.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4343 | a | A-PRIVATE | `site/data/test-kit.json:343 (steps[].system.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4344 | a | A-PRIVATE | `site/data/test-kit.json:344 (steps[].system.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4345 | a | A-PRIVATE | `site/data/test-kit.json:345 (steps[].system.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4346 | c | BP-06 | `site/data/test-kit.json:356 (steps[].system.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4347 | c | BP-04 | `site/data/test-kit.json:373 (steps[].system.body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-4348 | a | A-PRIVATE | `site/data/test-kit.json:377 (steps[].system.body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-4349 | a | A-PRIVATE | `site/data/test-kit.json:403 (steps[].system.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4350 | c | BP-04 | `site/data/test-kit.json:406 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4351 | c | BP-04 | `site/data/test-kit.json:406 (steps[].system.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4352 | c | BP-04 | `site/data/test-kit.json:429 (steps[].system.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4353 | c | BP-10 | `site/data/test-kit.json:429 (steps[].system.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4354 | c | BP-10 | `site/data/test-kit.json:429 (steps[].system.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4355 | c | BP-01 | `site/data/test-kit.json:517 (steps[].system.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4356 | c | BP-06 | `site/data/test-kit.json:517 (steps[].system.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4357 | c | BP-01 | `site/data/test-kit.json:519 (steps[].system.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4358 | c | BP-02 | `site/data/test-kit.json:520 (steps[].system.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4359 | c | BP-01 | `site/data/test-kit.json:541 (steps[].system.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4360 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-products-impact-analysis-stepwise.md |
| V-4361 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-products-impact-analysis-stepwise.md |
| V-4362 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4363 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4364 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4365 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4366 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4367 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4368 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4369 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4370 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4371 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4372 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4373 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4374 | c | BP-01 | `site/data/test-kit.json:5 (steps[].draft.body)` | `<!--` | <!-- issue-474:entry --> |
| V-4375 | a | A-PRIVATE | `site/data/test-kit.json:16 (steps[].draft.body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-4376 | b | CT-01 | `site/data/test-kit.json:56 (steps[].draft.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4377 | b | CT-02 | `site/data/test-kit.json:56 (steps[].draft.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4378 | c | BP-01 | `site/data/test-kit.json:78 (steps[].draft.body)` | `<!--` | <!-- /issue-474:entry --> |
| V-4379 | a | A-PRIVATE | `site/data/test-kit.json:87 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4380 | a | A-PRIVATE | `site/data/test-kit.json:106 (steps[].draft.body)` | `mango_ba_prompts` | [классификация продуктов Mango]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md); |
| V-4381 | a | A-PRIVATE | `site/data/test-kit.json:107 (steps[].draft.body)` | `mango_ba_prompts` | [профили продуктов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#4-профили-продуктов). |
| V-4382 | b | CT-09 | `site/data/test-kit.json:133 (steps[].draft.body)` | `D1,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-4383 | b | CT-09 | `site/data/test-kit.json:133 (steps[].draft.body)` | `D2,` | 4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари |
| V-4384 | b | CT-04 | `site/data/test-kit.json:134 (steps[].draft.body)` | `ВАТС` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4385 | b | CT-05 | `site/data/test-kit.json:134 (steps[].draft.body)` | `ЛК` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4386 | b | CT-09 | `site/data/test-kit.json:134 (steps[].draft.body)` | `D1,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4387 | b | CT-09 | `site/data/test-kit.json:134 (steps[].draft.body)` | `D2,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4388 | b | CT-09 | `site/data/test-kit.json:134 (steps[].draft.body)` | `D11;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4389 | b | CT-09 | `site/data/test-kit.json:134 (steps[].draft.body)` | `D5,` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4390 | b | CT-09 | `site/data/test-kit.json:134 (steps[].draft.body)` | `D6;` | профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6; |
| V-4391 | b | CT-09 | `site/data/test-kit.json:135 (steps[].draft.body)` | `D6,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4392 | b | CT-09 | `site/data/test-kit.json:135 (steps[].draft.body)` | `D11;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4393 | b | CT-09 | `site/data/test-kit.json:135 (steps[].draft.body)` | `D11,` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4394 | b | CT-09 | `site/data/test-kit.json:135 (steps[].draft.body)` | `D3;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4395 | b | CT-09 | `site/data/test-kit.json:135 (steps[].draft.body)` | `D8;` | КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9). |
| V-4396 | a | A-PRIVATE | `site/data/test-kit.json:149 (steps[].draft.body)` | `mango_ba_prompts` | [мета-стандарт раздела 2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/02-business-context.md). |
| V-4397 | a | A-PRIVATE | `site/data/test-kit.json:152 (steps[].draft.body)` | `mango_ba_prompts` | [раздел 1, механизм сверки]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/01-glossary.md#механизм-сверки). |
| V-4398 | b | CT-03 | `site/data/test-kit.json:170 (steps[].draft.body)` | `коннектор` | передачу этих функций через коннектор. Неподтверждённая сторона — вопрос |
| V-4399 | c | BP-01 | `site/data/test-kit.json:218 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4400 | a | A-PRIVATE | `site/data/test-kit.json:229 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4401 | c | BP-01 | `site/data/test-kit.json:322 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4402 | c | BP-01 | `site/data/test-kit.json:324 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4403 | c | BP-06 | `site/data/test-kit.json:324 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4404 | c | BP-04 | `site/data/test-kit.json:325 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4405 | c | BP-06 | `site/data/test-kit.json:325 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4406 | c | BP-02 | `site/data/test-kit.json:327 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4407 | c | BP-06 | `site/data/test-kit.json:327 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4408 | c | BP-09 | `site/data/test-kit.json:327 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4409 | c | BP-07 | `site/data/test-kit.json:329 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4410 | a | A-PRIVATE | `site/data/test-kit.json:330 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4411 | c | BP-02 | `site/data/test-kit.json:330 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4412 | a | A-PRIVATE | `site/data/test-kit.json:331 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4413 | a | A-PRIVATE | `site/data/test-kit.json:332 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4414 | a | A-PRIVATE | `site/data/test-kit.json:333 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4415 | a | A-PRIVATE | `site/data/test-kit.json:334 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4416 | c | BP-06 | `site/data/test-kit.json:345 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4417 | c | BP-04 | `site/data/test-kit.json:362 (steps[].draft.body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-4418 | a | A-PRIVATE | `site/data/test-kit.json:366 (steps[].draft.body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-4419 | a | A-PRIVATE | `site/data/test-kit.json:392 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4420 | c | BP-04 | `site/data/test-kit.json:395 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4421 | c | BP-04 | `site/data/test-kit.json:395 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4422 | c | BP-04 | `site/data/test-kit.json:418 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4423 | c | BP-10 | `site/data/test-kit.json:418 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4424 | c | BP-10 | `site/data/test-kit.json:418 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4425 | c | BP-01 | `site/data/test-kit.json:506 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4426 | c | BP-06 | `site/data/test-kit.json:506 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4427 | c | BP-01 | `site/data/test-kit.json:508 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4428 | c | BP-02 | `site/data/test-kit.json:509 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4429 | c | BP-01 | `site/data/test-kit.json:530 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4430 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-fr-documentation-stepwise.md |
| V-4431 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-fr-documentation-stepwise.md |
| V-4432 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4433 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4434 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4435 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4436 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-4437 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в ко… |
| V-4438 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#490` | …438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.… |
| V-4439 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по тесту» … |
| V-4440 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490); блок «по… |
| V-4441 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-4442 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-4443 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов (#490);… |
| V-4444 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата … |
| V-4445 | c | BP-01 | `site/data/test-kit.json:5 (steps[].draft.body)` | `<!--` | <!-- issue-474:entry --> |
| V-4446 | c | BP-02 | `site/data/test-kit.json:8 (steps[].draft.body)` | `#490` | …тма Ш-3 проверь вход по формату шагов из «Состояния BCREQ» (#490). Декомпозированный (по умолчанию): явные AIN-21 и AIN-24/Г-IN, их task/attempt/route… |
| V-4447 | a | A-PRIVATE | `site/data/test-kit.json:16 (steps[].draft.body)` | `mango_ba_prompts` | [Полные 24 draft контракта и инструкция БА]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md). |
| V-4448 | b | CT-01 | `site/data/test-kit.json:56 (steps[].draft.body)` | `amoCRM` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4449 | b | CT-02 | `site/data/test-kit.json:56 (steps[].draft.body)` | `API-привязки` | Задержка появления записи amoCRM не доказывает способ API-привязки по ID, |
| V-4450 | c | BP-01 | `site/data/test-kit.json:78 (steps[].draft.body)` | `<!--` | <!-- /issue-474:entry --> |
| V-4451 | a | A-PRIVATE | `site/data/test-kit.json:87 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4452 | a | A-PRIVATE | `site/data/test-kit.json:160 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/03-functional-requirements.md). |
| V-4453 | a | A-PRIVATE | `site/data/test-kit.json:168 (steps[].draft.body)` | `mango_ba_prompts` | …BABOK — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#2-babok-guide-v3-что-берём… |
| V-4454 | c | BP-01 | `site/data/test-kit.json:231 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4455 | a | A-PRIVATE | `site/data/test-kit.json:242 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4456 | c | BP-01 | `site/data/test-kit.json:335 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4457 | c | BP-01 | `site/data/test-kit.json:337 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4458 | c | BP-06 | `site/data/test-kit.json:337 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4459 | c | BP-04 | `site/data/test-kit.json:338 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4460 | c | BP-06 | `site/data/test-kit.json:338 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4461 | c | BP-02 | `site/data/test-kit.json:340 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4462 | c | BP-06 | `site/data/test-kit.json:340 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4463 | c | BP-09 | `site/data/test-kit.json:340 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4464 | c | BP-07 | `site/data/test-kit.json:342 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4465 | a | A-PRIVATE | `site/data/test-kit.json:343 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4466 | c | BP-02 | `site/data/test-kit.json:343 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4467 | a | A-PRIVATE | `site/data/test-kit.json:344 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4468 | a | A-PRIVATE | `site/data/test-kit.json:345 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4469 | a | A-PRIVATE | `site/data/test-kit.json:346 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4470 | a | A-PRIVATE | `site/data/test-kit.json:347 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4471 | c | BP-06 | `site/data/test-kit.json:358 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4472 | a | A-PRIVATE | `site/data/test-kit.json:398 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4473 | c | BP-04 | `site/data/test-kit.json:401 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4474 | c | BP-04 | `site/data/test-kit.json:401 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4475 | c | BP-04 | `site/data/test-kit.json:424 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4476 | c | BP-10 | `site/data/test-kit.json:424 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4477 | c | BP-10 | `site/data/test-kit.json:424 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4478 | c | BP-04 | `site/data/test-kit.json:467 (steps[].draft.body)` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-4479 | c | BP-01 | `site/data/test-kit.json:472 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4480 | c | BP-06 | `site/data/test-kit.json:472 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4481 | c | BP-01 | `site/data/test-kit.json:474 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4482 | c | BP-02 | `site/data/test-kit.json:475 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4483 | c | BP-01 | `site/data/test-kit.json:496 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4484 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-nfr-documentation-stepwise.md |
| V-4485 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-nfr-documentation-stepwise.md |
| V-4486 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4487 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4488 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4489 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4490 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4491 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4492 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4493 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4494 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4495 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4496 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4497 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4498 | a | A-PRIVATE | `site/data/test-kit.json:11 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4499 | a | A-PRIVATE | `site/data/test-kit.json:58 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 4]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/04-non-functional-requirements.md). |
| V-4500 | c | BP-01 | `site/data/test-kit.json:102 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4501 | a | A-PRIVATE | `site/data/test-kit.json:113 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4502 | c | BP-01 | `site/data/test-kit.json:206 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4503 | c | BP-01 | `site/data/test-kit.json:208 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4504 | c | BP-06 | `site/data/test-kit.json:208 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4505 | c | BP-04 | `site/data/test-kit.json:209 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4506 | c | BP-06 | `site/data/test-kit.json:209 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4507 | c | BP-02 | `site/data/test-kit.json:211 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4508 | c | BP-06 | `site/data/test-kit.json:211 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4509 | c | BP-09 | `site/data/test-kit.json:211 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4510 | c | BP-07 | `site/data/test-kit.json:213 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4511 | a | A-PRIVATE | `site/data/test-kit.json:214 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4512 | c | BP-02 | `site/data/test-kit.json:214 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4513 | a | A-PRIVATE | `site/data/test-kit.json:215 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4514 | a | A-PRIVATE | `site/data/test-kit.json:216 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4515 | a | A-PRIVATE | `site/data/test-kit.json:217 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4516 | a | A-PRIVATE | `site/data/test-kit.json:218 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4517 | c | BP-06 | `site/data/test-kit.json:229 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4518 | a | A-PRIVATE | `site/data/test-kit.json:269 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4519 | c | BP-04 | `site/data/test-kit.json:272 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4520 | c | BP-04 | `site/data/test-kit.json:272 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4521 | c | BP-04 | `site/data/test-kit.json:295 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4522 | c | BP-10 | `site/data/test-kit.json:295 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4523 | c | BP-10 | `site/data/test-kit.json:295 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4524 | c | BP-04 | `site/data/test-kit.json:330 (steps[].draft.body)` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-4525 | c | BP-01 | `site/data/test-kit.json:335 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4526 | c | BP-06 | `site/data/test-kit.json:335 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4527 | c | BP-01 | `site/data/test-kit.json:337 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4528 | c | BP-02 | `site/data/test-kit.json:338 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4529 | c | BP-01 | `site/data/test-kit.json:359 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4530 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-4531 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-uc-modeling-stepwise.md |
| V-4532 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4533 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4534 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4535 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4536 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4537 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4538 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4539 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4540 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4541 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4542 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4543 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4544 | a | A-PRIVATE | `site/data/test-kit.json:14 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4545 | a | A-PRIVATE | `site/data/test-kit.json:76 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-4546 | c | BP-01 | `site/data/test-kit.json:138 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4547 | a | A-PRIVATE | `site/data/test-kit.json:149 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4548 | c | BP-01 | `site/data/test-kit.json:242 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4549 | c | BP-01 | `site/data/test-kit.json:244 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4550 | c | BP-06 | `site/data/test-kit.json:244 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4551 | c | BP-04 | `site/data/test-kit.json:245 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4552 | c | BP-06 | `site/data/test-kit.json:245 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4553 | c | BP-02 | `site/data/test-kit.json:247 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4554 | c | BP-06 | `site/data/test-kit.json:247 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4555 | c | BP-09 | `site/data/test-kit.json:247 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4556 | c | BP-07 | `site/data/test-kit.json:249 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4557 | a | A-PRIVATE | `site/data/test-kit.json:250 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4558 | c | BP-02 | `site/data/test-kit.json:250 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4559 | a | A-PRIVATE | `site/data/test-kit.json:251 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4560 | a | A-PRIVATE | `site/data/test-kit.json:252 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4561 | a | A-PRIVATE | `site/data/test-kit.json:253 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4562 | a | A-PRIVATE | `site/data/test-kit.json:254 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4563 | c | BP-06 | `site/data/test-kit.json:265 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4564 | c | BP-04 | `site/data/test-kit.json:284 (steps[].draft.body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-4565 | a | A-PRIVATE | `site/data/test-kit.json:288 (steps[].draft.body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-4566 | a | A-PRIVATE | `site/data/test-kit.json:314 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4567 | c | BP-04 | `site/data/test-kit.json:317 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4568 | c | BP-04 | `site/data/test-kit.json:317 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4569 | c | BP-04 | `site/data/test-kit.json:340 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4570 | c | BP-10 | `site/data/test-kit.json:340 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4571 | c | BP-10 | `site/data/test-kit.json:340 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4572 | c | BP-04 | `site/data/test-kit.json:382 (steps[].draft.body)` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-4573 | c | BP-01 | `site/data/test-kit.json:387 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4574 | c | BP-06 | `site/data/test-kit.json:387 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4575 | c | BP-01 | `site/data/test-kit.json:389 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4576 | c | BP-02 | `site/data/test-kit.json:390 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4577 | c | BP-01 | `site/data/test-kit.json:423 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4578 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-orr-solution-design-stepwise.md |
| V-4579 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-orr-solution-design-stepwise.md |
| V-4580 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4581 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4582 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4583 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4584 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4585 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4586 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4587 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4588 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4589 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4590 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4591 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4592 | a | A-PRIVATE | `site/data/test-kit.json:13 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4593 | a | A-PRIVATE | `site/data/test-kit.json:90 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 5]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/05-solution-description.md); |
| V-4594 | a | A-PRIVATE | `site/data/test-kit.json:91 (steps[].draft.body)` | `mango_ba_prompts` | [правила композиции]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-composition-standard.md#2-правила-композиции). |
| V-4595 | a | A-PRIVATE | `site/data/test-kit.json:100 (steps[].draft.body)` | `mango_ba_prompts` | …ктуры — [справочник стандартов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-industry-practice.md#3-раздел-5-выбор-между-c4-… |
| V-4596 | c | BP-01 | `site/data/test-kit.json:178 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4597 | a | A-PRIVATE | `site/data/test-kit.json:189 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4598 | c | BP-01 | `site/data/test-kit.json:282 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4599 | c | BP-01 | `site/data/test-kit.json:284 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4600 | c | BP-06 | `site/data/test-kit.json:284 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4601 | c | BP-04 | `site/data/test-kit.json:285 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4602 | c | BP-06 | `site/data/test-kit.json:285 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4603 | c | BP-02 | `site/data/test-kit.json:287 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4604 | c | BP-06 | `site/data/test-kit.json:287 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4605 | c | BP-09 | `site/data/test-kit.json:287 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4606 | c | BP-07 | `site/data/test-kit.json:289 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4607 | a | A-PRIVATE | `site/data/test-kit.json:290 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4608 | c | BP-02 | `site/data/test-kit.json:290 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4609 | a | A-PRIVATE | `site/data/test-kit.json:291 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4610 | a | A-PRIVATE | `site/data/test-kit.json:292 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4611 | a | A-PRIVATE | `site/data/test-kit.json:293 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4612 | a | A-PRIVATE | `site/data/test-kit.json:294 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4613 | c | BP-06 | `site/data/test-kit.json:305 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4614 | a | A-PRIVATE | `site/data/test-kit.json:345 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4615 | c | BP-04 | `site/data/test-kit.json:348 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4616 | c | BP-04 | `site/data/test-kit.json:348 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4617 | c | BP-04 | `site/data/test-kit.json:371 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4618 | c | BP-10 | `site/data/test-kit.json:371 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4619 | c | BP-10 | `site/data/test-kit.json:371 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4620 | c | BP-01 | `site/data/test-kit.json:408 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4621 | c | BP-06 | `site/data/test-kit.json:408 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4622 | c | BP-01 | `site/data/test-kit.json:410 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4623 | c | BP-02 | `site/data/test-kit.json:411 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4624 | c | BP-01 | `site/data/test-kit.json:432 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4625 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constraints-documentation-stepwise.md |
| V-4626 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-constraints-documentation-stepwise.md |
| V-4627 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4628 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4629 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4630 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4631 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4632 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4633 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4634 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4635 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4636 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4637 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4638 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4639 | a | A-PRIVATE | `site/data/test-kit.json:11 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4640 | a | A-PRIVATE | `site/data/test-kit.json:60 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 6]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/06-implementation-constraints.md). |
| V-4641 | c | BP-01 | `site/data/test-kit.json:103 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4642 | a | A-PRIVATE | `site/data/test-kit.json:114 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4643 | c | BP-01 | `site/data/test-kit.json:207 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4644 | c | BP-01 | `site/data/test-kit.json:209 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4645 | c | BP-06 | `site/data/test-kit.json:209 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4646 | c | BP-04 | `site/data/test-kit.json:210 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4647 | c | BP-06 | `site/data/test-kit.json:210 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4648 | c | BP-02 | `site/data/test-kit.json:212 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4649 | c | BP-06 | `site/data/test-kit.json:212 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4650 | c | BP-09 | `site/data/test-kit.json:212 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4651 | c | BP-07 | `site/data/test-kit.json:214 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4652 | a | A-PRIVATE | `site/data/test-kit.json:215 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4653 | c | BP-02 | `site/data/test-kit.json:215 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4654 | a | A-PRIVATE | `site/data/test-kit.json:216 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4655 | a | A-PRIVATE | `site/data/test-kit.json:217 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4656 | a | A-PRIVATE | `site/data/test-kit.json:218 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4657 | a | A-PRIVATE | `site/data/test-kit.json:219 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4658 | c | BP-06 | `site/data/test-kit.json:230 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4659 | a | A-PRIVATE | `site/data/test-kit.json:270 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4660 | c | BP-04 | `site/data/test-kit.json:273 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4661 | c | BP-04 | `site/data/test-kit.json:273 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4662 | c | BP-04 | `site/data/test-kit.json:296 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4663 | c | BP-10 | `site/data/test-kit.json:296 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4664 | c | BP-10 | `site/data/test-kit.json:296 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4665 | c | BP-01 | `site/data/test-kit.json:326 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4666 | c | BP-06 | `site/data/test-kit.json:326 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4667 | c | BP-01 | `site/data/test-kit.json:328 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4668 | c | BP-02 | `site/data/test-kit.json:329 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4669 | c | BP-01 | `site/data/test-kit.json:350 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4670 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-uc-modeling-stepwise.md |
| V-4671 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-uc-modeling-stepwise.md |
| V-4672 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4673 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4674 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4675 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4676 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4677 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4678 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4679 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4680 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4681 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4682 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4683 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4684 | a | A-PRIVATE | `site/data/test-kit.json:14 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4685 | a | A-PRIVATE | `site/data/test-kit.json:76 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md). |
| V-4686 | c | BP-01 | `site/data/test-kit.json:138 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4687 | a | A-PRIVATE | `site/data/test-kit.json:149 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4688 | c | BP-01 | `site/data/test-kit.json:242 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4689 | c | BP-01 | `site/data/test-kit.json:244 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4690 | c | BP-06 | `site/data/test-kit.json:244 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4691 | c | BP-04 | `site/data/test-kit.json:245 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4692 | c | BP-06 | `site/data/test-kit.json:245 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4693 | c | BP-02 | `site/data/test-kit.json:247 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4694 | c | BP-06 | `site/data/test-kit.json:247 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4695 | c | BP-09 | `site/data/test-kit.json:247 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4696 | c | BP-07 | `site/data/test-kit.json:249 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4697 | a | A-PRIVATE | `site/data/test-kit.json:250 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4698 | c | BP-02 | `site/data/test-kit.json:250 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4699 | a | A-PRIVATE | `site/data/test-kit.json:251 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4700 | a | A-PRIVATE | `site/data/test-kit.json:252 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4701 | a | A-PRIVATE | `site/data/test-kit.json:253 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4702 | a | A-PRIVATE | `site/data/test-kit.json:254 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4703 | c | BP-06 | `site/data/test-kit.json:265 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4704 | c | BP-04 | `site/data/test-kit.json:284 (steps[].draft.body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-4705 | a | A-PRIVATE | `site/data/test-kit.json:288 (steps[].draft.body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-4706 | a | A-PRIVATE | `site/data/test-kit.json:314 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4707 | c | BP-04 | `site/data/test-kit.json:317 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4708 | c | BP-04 | `site/data/test-kit.json:317 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4709 | c | BP-04 | `site/data/test-kit.json:340 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4710 | c | BP-10 | `site/data/test-kit.json:340 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4711 | c | BP-10 | `site/data/test-kit.json:340 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4712 | c | BP-04 | `site/data/test-kit.json:382 (steps[].draft.body)` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-4713 | c | BP-01 | `site/data/test-kit.json:387 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4714 | c | BP-06 | `site/data/test-kit.json:387 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4715 | c | BP-01 | `site/data/test-kit.json:389 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4716 | c | BP-02 | `site/data/test-kit.json:390 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4717 | c | BP-01 | `site/data/test-kit.json:423 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4718 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-extra-risk-analysis-stepwise.md |
| V-4719 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-extra-risk-analysis-stepwise.md |
| V-4720 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4721 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4722 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4723 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4724 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4725 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4726 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4727 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4728 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4729 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4730 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4731 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4732 | a | A-PRIVATE | `site/data/test-kit.json:11 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4733 | a | A-PRIVATE | `site/data/test-kit.json:58 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 8]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/08-supplementary.md). |
| V-4734 | c | BP-01 | `site/data/test-kit.json:103 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4735 | a | A-PRIVATE | `site/data/test-kit.json:114 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4736 | c | BP-01 | `site/data/test-kit.json:207 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4737 | c | BP-01 | `site/data/test-kit.json:209 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4738 | c | BP-06 | `site/data/test-kit.json:209 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4739 | c | BP-04 | `site/data/test-kit.json:210 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4740 | c | BP-06 | `site/data/test-kit.json:210 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4741 | c | BP-02 | `site/data/test-kit.json:212 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4742 | c | BP-06 | `site/data/test-kit.json:212 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4743 | c | BP-09 | `site/data/test-kit.json:212 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4744 | c | BP-07 | `site/data/test-kit.json:214 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4745 | a | A-PRIVATE | `site/data/test-kit.json:215 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4746 | c | BP-02 | `site/data/test-kit.json:215 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4747 | a | A-PRIVATE | `site/data/test-kit.json:216 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4748 | a | A-PRIVATE | `site/data/test-kit.json:217 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4749 | a | A-PRIVATE | `site/data/test-kit.json:218 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4750 | a | A-PRIVATE | `site/data/test-kit.json:219 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4751 | c | BP-06 | `site/data/test-kit.json:230 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4752 | a | A-PRIVATE | `site/data/test-kit.json:270 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4753 | c | BP-04 | `site/data/test-kit.json:273 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4754 | c | BP-04 | `site/data/test-kit.json:273 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4755 | c | BP-04 | `site/data/test-kit.json:296 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4756 | c | BP-10 | `site/data/test-kit.json:296 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4757 | c | BP-10 | `site/data/test-kit.json:296 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4758 | c | BP-01 | `site/data/test-kit.json:339 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4759 | c | BP-06 | `site/data/test-kit.json:339 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4760 | c | BP-01 | `site/data/test-kit.json:341 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4761 | c | BP-02 | `site/data/test-kit.json:342 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4762 | c | BP-01 | `site/data/test-kit.json:363 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4763 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-review-validation-oneshot.md |
| V-4764 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-review-validation-oneshot.md |
| V-4765 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4766 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4767 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4768 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4769 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4770 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4771 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4772 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4773 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4774 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4775 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4776 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4777 | a | A-PRIVATE | `site/data/test-kit.json:14 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4778 | a | A-PRIVATE | `site/data/test-kit.json:58 (steps[].draft.body)` | `mango_ba_prompts` | [Контракт гейтов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md#2-гейты); |
| V-4779 | a | A-PRIVATE | `site/data/test-kit.json:59 (steps[].draft.body)` | `mango_ba_prompts` | [мета-стандарты разделов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md). |
| V-4780 | c | BP-01 | `site/data/test-kit.json:119 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4781 | a | A-PRIVATE | `site/data/test-kit.json:130 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4782 | c | BP-01 | `site/data/test-kit.json:224 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4783 | c | BP-01 | `site/data/test-kit.json:226 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4784 | c | BP-06 | `site/data/test-kit.json:226 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4785 | c | BP-04 | `site/data/test-kit.json:227 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4786 | c | BP-06 | `site/data/test-kit.json:227 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4787 | c | BP-02 | `site/data/test-kit.json:229 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4788 | c | BP-06 | `site/data/test-kit.json:229 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4789 | c | BP-09 | `site/data/test-kit.json:229 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4790 | c | BP-07 | `site/data/test-kit.json:231 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4791 | a | A-PRIVATE | `site/data/test-kit.json:232 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4792 | c | BP-02 | `site/data/test-kit.json:232 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4793 | a | A-PRIVATE | `site/data/test-kit.json:233 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4794 | a | A-PRIVATE | `site/data/test-kit.json:234 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4795 | a | A-PRIVATE | `site/data/test-kit.json:235 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4796 | a | A-PRIVATE | `site/data/test-kit.json:236 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4797 | c | BP-06 | `site/data/test-kit.json:247 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4798 | a | A-PRIVATE | `site/data/test-kit.json:291 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4799 | c | BP-04 | `site/data/test-kit.json:294 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4800 | c | BP-04 | `site/data/test-kit.json:294 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4801 | c | BP-04 | `site/data/test-kit.json:317 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4802 | c | BP-10 | `site/data/test-kit.json:317 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4803 | c | BP-10 | `site/data/test-kit.json:317 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4804 | c | BP-01 | `site/data/test-kit.json:402 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4805 | c | BP-06 | `site/data/test-kit.json:402 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4806 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-release-readiness-oneshot.md |
| V-4807 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4808 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4809 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4810 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4811 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-4812 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «по тес… |
| V-4813 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-4814 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «… |
| V-4815 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2)… |
| V-4816 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-4817 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-4818 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, ра… |
| V-4819 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот,… |
| V-4820 | a | A-PRIVATE | `site/data/test-kit.json:8 (steps[].draft.body)` | `mango_ba_prompts` | ([RFC #427, раздел 9.2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)). |
| V-4821 | c | BP-02 | `site/data/test-kit.json:8 (steps[].draft.body)` | `#427` | ([RFC #427, раздел 9.2]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)). |
| V-4822 | c | BP-04 | `site/data/test-kit.json:10 (steps[].draft.body)` | `BL-1` | гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16). |
| V-4823 | c | BP-04 | `site/data/test-kit.json:10 (steps[].draft.body)` | `RUN-0` | гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16). |
| V-4824 | c | BP-01 | `site/data/test-kit.json:106 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4825 | c | BP-06 | `site/data/test-kit.json:106 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4826 | c | BP-04 | `site/data/test-kit.json:107 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4827 | c | BP-06 | `site/data/test-kit.json:107 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4828 | c | BP-02 | `site/data/test-kit.json:109 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4829 | c | BP-06 | `site/data/test-kit.json:109 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4830 | c | BP-09 | `site/data/test-kit.json:109 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4831 | c | BP-07 | `site/data/test-kit.json:111 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4832 | a | A-PRIVATE | `site/data/test-kit.json:112 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4833 | c | BP-02 | `site/data/test-kit.json:112 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4834 | a | A-PRIVATE | `site/data/test-kit.json:113 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4835 | a | A-PRIVATE | `site/data/test-kit.json:114 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4836 | a | A-PRIVATE | `site/data/test-kit.json:115 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4837 | a | A-PRIVATE | `site/data/test-kit.json:116 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4838 | c | BP-06 | `site/data/test-kit.json:127 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4839 | c | BP-04 | `site/data/test-kit.json:144 (steps[].draft.body)` | `RUN-0` | **Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5 |
| V-4840 | a | A-PRIVATE | `site/data/test-kit.json:148 (steps[].draft.body)` | `mango_ba_prompts` | [`docs/contracts/bcreq-stage-gates.md`]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/bcreq-stage-gates.md). |
| V-4841 | a | A-PRIVATE | `site/data/test-kit.json:174 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4842 | c | BP-04 | `site/data/test-kit.json:177 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4843 | c | BP-04 | `site/data/test-kit.json:177 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4844 | c | BP-04 | `site/data/test-kit.json:200 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4845 | c | BP-10 | `site/data/test-kit.json:200 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4846 | c | BP-10 | `site/data/test-kit.json:200 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4847 | c | BP-01 | `site/data/test-kit.json:275 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4848 | c | BP-06 | `site/data/test-kit.json:275 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
| V-4849 | c | BP-01 | `site/data/test-kit.json:277 (steps[].draft.body)` | `<!--` | <!-- issue-490:handoff --> |
| V-4850 | c | BP-02 | `site/data/test-kit.json:278 (steps[].draft.body)` | `#490` | ## Итог шага для БА (#490) |
| V-4851 | c | BP-01 | `site/data/test-kit.json:299 (steps[].draft.body)` | `<!--` | <!-- /issue-490:handoff --> |
| V-4852 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].published.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-scenarios-modeling-oneshot.md |
| V-4853 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.url)` | `mango_ba_prompts` | https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/drafts/bcreq-scenarios-modeling-oneshot.md |
| V-4854 | a | A-PRIVATE | `site/data/test-kit.json:1 (steps[].draft.body)` | `mango_ba_prompts` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4855 | c | BP-01 | `site/data/test-kit.json:1 (steps[].draft.body)` | `<!--` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4856 | c | BP-04 | `site/data/test-kit.json:1 (steps[].draft.body)` | `BL-1` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4857 | c | BP-08 | `site/data/test-kit.json:1 (steps[].draft.body)` | `Experimental` | <!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet --> |
| V-4858 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4859 | c | BP-02 | `site/data/test-kit.json:3 (steps[].draft.body)` | `#438` | …ует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4860 | c | BP-03 | `site/data/test-kit.json:3 (steps[].draft.body)` | `issue` | …действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4861 | c | BP-04 | `site/data/test-kit.json:3 (steps[].draft.body)` | `BL-1` | …(#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.… |
| V-4862 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4863 | c | BP-06 | `site/data/test-kit.json:3 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4864 | c | BP-08 | `site/data/test-kit.json:3 (steps[].draft.body)` | `Черновик BL` | …по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце ф… |
| V-4865 | c | BP-09 | `site/data/test-kit.json:3 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту… |
| V-4866 | a | A-PRIVATE | `site/data/test-kit.json:14 (steps[].draft.body)` | `mango_ba_prompts` | [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md); |
| V-4867 | a | A-PRIVATE | `site/data/test-kit.json:56 (steps[].draft.body)` | `mango_ba_prompts` | [Мета-стандарт раздела 7]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/07-use-cases.md) |
| V-4868 | a | A-PRIVATE | `site/data/test-kit.json:58 (steps[].draft.body)` | `mango_ba_prompts` | [архитектуры промптов]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-architecture.md)). |
| V-4869 | c | BP-01 | `site/data/test-kit.json:97 (steps[].draft.body)` | `<!--` | <!-- issue-395: runtime-fallback --> |
| V-4870 | a | A-PRIVATE | `site/data/test-kit.json:108 (steps[].draft.body)` | `mango_ba_prompts` | прочитать [Промпт 0]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md), |
| V-4871 | c | BP-01 | `site/data/test-kit.json:201 (steps[].draft.body)` | `<!--` | <!-- /issue-395: runtime-fallback --> |
| V-4872 | c | BP-01 | `site/data/test-kit.json:203 (steps[].draft.body)` | `<!--` | <!-- bl-156: by-test --> |
| V-4873 | c | BP-06 | `site/data/test-kit.json:203 (steps[].draft.body)` | `by-test` | <!-- bl-156: by-test --> |
| V-4874 | c | BP-04 | `site/data/test-kit.json:204 (steps[].draft.body)` | `BL-1` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4875 | c | BP-06 | `site/data/test-kit.json:204 (steps[].draft.body)` | `по тесту` | ## Дополнение «по тесту» (BL-156): стандарты шага |
| V-4876 | c | BP-02 | `site/data/test-kit.json:206 (steps[].draft.body)` | `#427` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4877 | c | BP-06 | `site/data/test-kit.json:206 (steps[].draft.body)` | `по тесту` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4878 | c | BP-09 | `site/data/test-kit.json:206 (steps[].draft.body)` | `действует до ADR` | > **Редакция по тесту (#427): действует до ADR обратного согласования.** |
| V-4879 | c | BP-07 | `site/data/test-kit.json:208 (steps[].draft.body)` | `сборщик` | Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по |
| V-4880 | a | A-PRIVATE | `site/data/test-kit.json:209 (steps[].draft.body)` | `mango_ba_prompts` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4881 | c | BP-02 | `site/data/test-kit.json:209 (steps[].draft.body)` | `#427` | [RFC #427, раздел 9.3]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собираетс… |
| V-4882 | a | A-PRIVATE | `site/data/test-kit.json:210 (steps[].draft.body)` | `mango_ba_prompts` | из [базового стандарта]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-base-standard.md) 0.1.3, |
| V-4883 | a | A-PRIVATE | `site/data/test-kit.json:211 (steps[].draft.body)` | `mango_ba_prompts` | [профилей]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-prompt-profiles.md) 0.1.2, |
| V-4884 | a | A-PRIVATE | `site/data/test-kit.json:212 (steps[].draft.body)` | `mango_ba_prompts` | [каталога операций]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-manual-classes/catalog.json) и |
| V-4885 | a | A-PRIVATE | `site/data/test-kit.json:213 (steps[].draft.body)` | `mango_ba_prompts` | [реестра справочников runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md) 0.5. |
| V-4886 | c | BP-06 | `site/data/test-kit.json:224 (steps[].draft.body)` | `по тесту` | …непрочитанные источники, ограничения, расхождения с блоком «по тесту»;… |
| V-4887 | a | A-PRIVATE | `site/data/test-kit.json:264 (steps[].draft.body)` | `mango_ba_prompts` | …правочник И-7 [реестра runtime]\(https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md#2-перечень); промпт **ДОЛ… |
| V-4888 | c | BP-04 | `site/data/test-kit.json:267 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4889 | c | BP-04 | `site/data/test-kit.json:267 (steps[].draft.body)` | `BL-1` | …ок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка — известный пробел, а не дефект… |
| V-4890 | c | BP-04 | `site/data/test-kit.json:290 (steps[].draft.body)` | `BL-1` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4891 | c | BP-10 | `site/data/test-kit.json:290 (steps[].draft.body)` | `Не внесены` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4892 | c | BP-10 | `site/data/test-kit.json:290 (steps[].draft.body)` | `отчёт BL` | Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1. |
| V-4893 | c | BP-04 | `site/data/test-kit.json:332 (steps[].draft.body)` | `BL-1` | [СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР; задача BL-155] |
| V-4894 | c | BP-01 | `site/data/test-kit.json:337 (steps[].draft.body)` | `<!--` | <!-- /bl-156: by-test --> |
| V-4895 | c | BP-06 | `site/data/test-kit.json:337 (steps[].draft.body)` | `by-test` | <!-- /bl-156: by-test --> |
