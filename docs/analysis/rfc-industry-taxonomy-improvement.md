---
status: draft
version: 0.1
updated: 2026-06-22
ai-generated: true
type: rfc
scope: industry-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/178"
based_on:
  - "docs/analysis/taxonomy-convergence-test.md"
  - "docs/analysis/mango-taxonomy-convergence-test.md"
  - "standards/industry-taxonomy-standard.md"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
target_artifacts:
  - "standards/industry-taxonomy-standard.md"
  - "kb/industry-taxonomy/reference-taxonomy.json"
  - "kb/industry-taxonomy/reference-taxonomy.schema.json"
  - "scripts/validate_issue_156_industry_taxonomy_registry.py"
  - "scripts/validate_issue_168_industry_reference_integrity.py"
---

# RFC: доработка Industry Taxonomy после теста на сходимость

> Это RFC для human review, а не реализация. До явного согласования фаундером
> не меняются `standards/industry-taxonomy-standard.md`, Industry registry,
> валидаторы, ADR-011 или Mango Taxonomy artifacts.

## 1. Статус путей после PR #173

Issue #178 требует использовать актуальные пути после переименования:
`kb/industry-taxonomy/` и `kb/mango-taxonomy/`. На 2026-06-22 PR #173 уже
merged в `upstream/main`, а ветка PR #179 синхронизирована с этим состоянием.

Для реализации после approval используются только текущие taxonomy directories:

| Artifact | Current path |
| --- | --- |
| Industry registry | `kb/industry-taxonomy/reference-taxonomy.json` |
| Industry schema | `kb/industry-taxonomy/reference-taxonomy.schema.json` |
| Mango registry | `kb/mango-taxonomy/mango-registry.json` |
| Industry convergence report | `docs/analysis/taxonomy-convergence-test.md` |
| Industry convergence experiment | `experiments/issue-174/` |

RFC ниже не предлагает переименование каталогов и не требует stacking поверх
другой ветки. Path refactor считается завершённой зависимостью; дальнейшие
изменения должны оставаться внутри утверждённого scope #178.

## 2. Входные факты

Локально воспроизведены оба теста:

```bash
python3 experiments/issue-174/score_convergence.py
python3 experiments/issue-176-convergence/score.py
```

Industry Taxonomy test (#174):

| Метрика | Результат |
| --- | --- |
| Domain | 24/25 = 96% |
| Capability | 19/25 = 76% |
| Feature | 6/10 = 60% |
| Function | 1/4 = 25% |
| function_type | 21/25 = 84% |
| Full path | 17/25 = 68% |

Mango to Industry convergence test (#176):

| Метрика | Результат |
| --- | --- |
| Exact full path | 10/27 = 37% |
| Prefix match | 17/27 = 63% |
| Domain | 22/27 = 81% |
| Capability | 18/27 = 67% |
| AI node resolves | 27/27 = 100% |
| alignment_type | 27/27 = 100% |

Текущий Industry registry содержит 372 узла: 8 domain/layer roots, 54 capability,
153 feature, 157 function. В нём есть активные дубли `id` под разными родителями,
включая `access-control`, `conversation-summaries`, `call-routing`,
`interaction-routing`, `live-monitoring`, `queue-management`,
`source-attribution` и другие. Часть дублей является техническим паттерном
"feature и function с одинаковым slug", но часть создаёт реальные competing
canonical paths.

## 3. Корневые причины

### 3.1 Critical: неоднозначные canonical nodes

Одинаковые или пересекающиеся узлы позволяют двум корректным классификаторам
выбрать разные ветки:

| Кейс | Расхождение | Причина |
| --- | --- | --- |
| #1 `Принять входящий звонок` | `accept-inbound-voice-call` vs `receive-inbound-call` | две function-синонима под одним feature |
| #7 `Распределить обращение в очередь` | `contact-center/call-routing/queue-management` vs `contact-center/interaction-routing/queue-routing` | competing routing capabilities |
| #24 `Назначить роль пользователю` | `security/information-security/access-control` vs `security/access-control` | `access-control` есть как feature и capability |
| Mango #12/#19 | `contact-center/agent-assist/conversation-summaries` vs `ai-automation/conversation-summaries` | competing AI/contact-center placement |
| Mango #22 | `security/information-security/access-control` vs `security/access-control` | тот же access-control conflict |

Это не ошибка AI-agent: все выбранные id резолвятся в registry.

### 3.2 Critical: пробелы покрытия

В registry нет точных canonical nodes для трёх функций из теста:

| Кейс | Сейчас | Нужный node |
| --- | --- | --- |
| #4 `Добавить номер в чёрный список` | ближайшие parents `voice-ucaas/cloud-pbx/call-routing-rules` или `voice-ucaas/call-routing` | number filtering / blacklist-whitelist |
| #8 `Перевести вызов с консультацией` | ближайшие parents `contact-center/agent-workspace` или `contact-center/interaction-routing` | active call transfer / consultation transfer |
| #18 `Проставить теги разговору` | `ai-automation/speech-analytics` vs `contact-center/agent-workspace` | conversation tagging under speech analytics |

### 3.3 Major: нет правил выбора при legitimate overlap

Стандарт уже содержит общие правила `primary meaning`, `platform`, `AI` и
`mapping_gap`, но не задаёт порядок выбора для таких пар:

- specific leaf vs generic parent (`working-hours-routing` vs
  `call-routing-rules`);
- contact-center system routing vs operator active-call control;
- CPaaS/API primary vs digital-channel semantics;
- UC corporate messaging vs digital team messaging;
- AI product domain vs AI-assisted contact-center feature;
- access-management as security capability vs information-security subfeature.

### 3.4 Major: `function_type` decision test недостаточно операционный

Текущий §7.2 различает `business`, `configuration` и `ui-action`, но не даёт
жёсткого теста для "view/play/status/planning" действий. В результате:

| Кейс | Эталон | AI | Нужное уточнение |
| --- | --- | --- | --- |
| #5 сменить статус присутствия | `ui-action` | `business` | влияет ли статус на routing/availability или только UI |
| #6 прослушать запись | `ui-action` | `business` | просмотр/воспроизведение existing artifact |
| #11 спланировать прогноз входящих | `configuration` | `business` | operational plan vs business outcome |
| #12 изменить статус оператора | `ui-action` | `business` | operator availability state vs UI click |

### 3.5 Separate CR: дефекты эталонных Mango mappings

Кейс #21 в Industry test и причина D в Mango test показывают не дефект Industry
standard, а недомаппленную или субоптимальную глубину в Mango registry:

- `select-dashboard-widget` должен указывать на
  `analytics/real-time-reporting/dashboard-view/select-dashboard-widget`, а не
  на `analytics/multichannel-analytics`;
- ряд Module/Function mappings в `kb/mango-taxonomy/mango-registry.json`
  остановлен на capability, хотя Industry registry уже содержит feature/function.

Это не требует изменения Mango Taxonomy Standard, но изменение Mango registry
следует согласовать отдельно, потому что issue #178 явно ограничивает scope
Industry Taxonomy.

## 4. Предлагаемые изменения

### R1 - Critical - ввести policy для неоднозначных активных id

Добавить в стандарт правило:

1. один и тот же active `id` может существовать в разных parent chains только
   если это осознанный homonym с разными определениями и полем
   `homonym_allowed: true`;
2. если два active nodes описывают один смысл, один становится canonical, второй
   получает `lifecycle_status: deprecated`, `replacement` и aliases/source_terms;
3. ambiguous aliases запрещены: alias/source term не должен silently resolve в
   несколько canonical nodes.

Validator impact:

- `scripts/validate_issue_156_industry_taxonomy_registry.py` должен находить
  duplicate active id groups без `homonym_allowed`;
- `scripts/validate_issue_168_industry_reference_integrity.py` должен явно
  проверять ambiguous alias resolution, а не перезаписывать alias последним
  найденным узлом.

### R2 - Critical - canonicalize contact-center routing

Предложенный canonical path для распределения обращений:

```text
contact-center/interaction-routing/queue-routing/assign-interaction-to-agent
```

Изменения:

- `contact-center/interaction-routing` остаётся canonical capability для
  channel-agnostic routing;
- `contact-center/call-routing` переводится в deprecated или narrowing scope
  "legacy voice-only contact-center call routing" с replacement на
  `contact-center/interaction-routing`;
- `contact-center/call-routing/queue-management/queue-management` получает
  replacement на `contact-center/interaction-routing/queue-routing/assign-interaction-to-agent`;
- стандарт получает правило: routing/assignment of any customer interaction in
  contact center uses `interaction-routing`; active operator controls use
  `agent-workspace` call-control nodes.

Ожидаемый эффект: закрывает Industry case #7 и снижает риск Mango cause A/C.

### R3 - Critical - canonicalize security access-control

Предложенный canonical path для назначения роли:

```text
security/access-control/role-management/assign-role
```

Изменения:

- `security/access-control` становится canonical capability для authentication,
  authorization, role assignment and IAM;
- `security/information-security` остаётся broader capability для audit,
  data-classification, incident management and other information security;
- `security/information-security/access-control/role-based-access-control`
  получает deprecated + replacement на
  `security/access-control/role-management/assign-role` for assign-role cases;
- для SSO/authentication требуется отдельный feature/function под
  `security/access-control`, если evidence подтверждает.

Ожидаемый эффект: закрывает Industry case #24 и Mango #22.

### R4 - Critical - добавить missing coverage nodes

Предлагаемые active nodes:

| Parent | New feature | New function(s) | Основание |
| --- | --- | --- | --- |
| `voice-ucaas/call-routing` | `number-filtering` | `add-number-to-blacklist`, `add-number-to-whitelist`, optional `remove-number-from-blacklist` | Industry case #4; evidence из чёрного/белого списка номеров |
| `contact-center/agent-workspace` | `call-control` или `call-transfer` | `transfer-call-with-consultation`, `transfer-call-without-consultation`, optional hold/conference functions | Industry case #8; active operator call control |
| `ai-automation/speech-analytics` | `conversation-tagging` | `tag-conversation`, optional `configure-ai-tagging` | Industry case #18; evidence из Speech Analytics tagging |

Boundary rules:

- blacklist/whitelist is voice call policy/routing, not security primary, unless
  source evidence is identity/access management;
- transfer with consultation is contact-center agent-workspace call control when
  operator actively transfers a live interaction; automated assignment remains
  `interaction-routing`;
- conversation tagging is `ai-automation/speech-analytics` when tags are created
  or managed as speech analytics output; manual operator-only labels can be
  `contact-center/agent-workspace` with `mapping_gap` if no canonical node exists.

Ожидаемый эффект: закрывает Industry cases #4, #8, #18.

### R5 - Major - specific-over-generic disambiguation

Добавить в §5 правило:

1. если exact specific node exists and source evidence names that behavior,
   choose it over a generic parent;
2. if two nodes are both valid, prefer the deepest canonical path whose parent
   chain preserves semantic containment;
3. if the exact node exists but gold mapping stops above it, this is a registry
   depth issue, not an AI error.

Прецеденты:

| Source | Preferred path |
| --- | --- |
| `Настроить маршрутизацию по рабочему времени` | `voice-ucaas/cloud-pbx/working-hours-schedule/working-hours-routing` |
| `Выбрать виджет дашборда` | `analytics/real-time-reporting/dashboard-view/select-dashboard-widget` |
| `Настроить интеграцию с Битрикс24` | `platform/platform-integration/crm-connectors/...` when source level is Function |

Ожидаемый эффект: закрывает Industry case #3 and documents why #21 is a Mango
registry correction.

### R6 - Major - уточнить `function_type`

Предлагаемый decision tree для §7.2:

1. If the action creates, sends, routes, transfers, tags, classifies, generates,
   authenticates, or otherwise changes customer/operator/business state, choose
   `business`.
2. If the action changes a persistent policy, route, permission, schedule,
   integration, model setting, campaign setup, forecast plan or lifecycle
   configuration, choose `configuration`.
3. If the action only navigates, opens, selects, views, listens, previews or
   plays an existing artifact without changing domain state, choose `ui-action`.
4. UI surface alone never makes a function `ui-action`; `interaction_surface`
   carries that fact separately.

Examples to add:

| Function | Proposed `function_type` | Rationale |
| --- | --- | --- |
| `play-call-recording` / listen existing recording | `ui-action` | consumes existing artifact, no domain state change |
| `select-dashboard-widget` | `ui-action` | UI selection/navigation |
| `presence-update` | `business` or `configuration` by downstream effect | not pure UI if routing/availability changes |
| `set-agent-status` | `business` or `configuration` by downstream effect | operator availability changes operational state |
| `load-forecasting` / plan forecast | `configuration` | creates operational planning artifact |

Если требуется сохранить текущий gold `ui-action` for statuses, RFC просит
фаундера явно подтвердить исключение. Без такого исключения текущий стандарт
уже ближе к AI interpretation: status changes are not pure UI.

### R7 - Minor - aliases and source terms

Для уменьшения случайных divergent choices добавить aliases/source_terms:

- `accept-inbound-voice-call` gets aliases/source terms
  `receive-inbound-call`, `answer-inbound-call`, `принять входящий вызов`;
- deprecated `receive-inbound-call` points to `accept-inbound-voice-call`;
- `number-filtering` gets source terms `blacklist`, `whitelist`,
  `black-white-list`, `чёрный список`, `белый список`;
- `call-control` / `call-transfer` gets source terms `consultation transfer`,
  `blind transfer`, `hold`, `conference`;
- `conversation-tagging` gets source terms `tagging`, `topic tagging`,
  `тегирование разговоров`.

## 5. Ожидаемый measurable effect

Текущий full path score: 17/25 = 68%.

Если R2, R3, R4, R5 and R7 делают выбор детерминированным, повторный слепой тест
должен восстановить такие cases:

| Case | Expected effect |
| --- | --- |
| #1 | synonym removal/alias policy aligns inbound call function |
| #3 | specific-over-generic rule aligns working-hours routing |
| #4 | new number-filtering node removes low-confidence nearest-parent choice |
| #7 | contact-center routing canonicalization removes competing capability |
| #8 | new active-call control/transfer node removes nearest-parent choice |
| #18 | new conversation-tagging node and AI boundary rule remove domain split |
| #24 | security access-control canonicalization removes competing branch |

Conservative expected score: `(17 + 6) / 25 = 92%` if one recovered case still
requires human judgment. Full expected score for Industry test after all seven:
`24 / 25 = 96%`. Remaining #21 is a Mango registry correction, not an Industry
Taxonomy correction.

`function_type` can improve from 21/25 only after R6 and a deliberate decision
whether the gold statuses should remain `ui-action` or be corrected.

## 6. Влияние на артефакты

| Artifact | Impact |
| --- | --- |
| `standards/industry-taxonomy-standard.md` | Add duplicate-node policy, disambiguation rules, boundary examples, `function_type` decision tree. Version should move from 0.1 to 0.2 because rules change behavior. |
| `kb/industry-taxonomy/reference-taxonomy.json` | Add missing nodes; deprecate or narrow ambiguous duplicates; add aliases/source_terms/replacement metadata. Registry version should move from 1.1.0 to 1.2.0 if non-breaking deprecations are used. |
| `kb/industry-taxonomy/reference-taxonomy.schema.json` | No required schema change if replacement metadata remains additional properties; optional schema extension can formalize `replacement`, `deprecation_reason`, `homonym_allowed`. |
| `scripts/validate_issue_156_industry_taxonomy_registry.py` | Add duplicate active id / ambiguous alias checks and required new nodes. |
| `scripts/validate_issue_168_industry_reference_integrity.py` | Make alias resolution ambiguity-safe; preserve deprecated warning behavior. |
| `standards/decisions/ADR-011-industry-taxonomy.md` | No change required. The RFC is consistent with ADR-011 hierarchy, platform layer, channel facet and alias/deprecation mechanics. |
| `standards/mango-taxonomy-standard.md` | No change proposed in this issue. Mango boundary lessons are documented but standard changes should be separate. |
| `kb/mango-taxonomy/mango-registry.json` | Separate CR unless founder explicitly approves extending #178 scope to correct #21 and depth mappings. |
| `CHANGELOG.md` | Add Issue #178 entry after approved implementation, not for RFC-only stage unless the team wants to track RFC creation separately. |

## 7. Implementation plan after approval

1. Work on the branch synced with `upstream/main` after PR #173.
2. Update Industry standard with R1-R6.
3. Update Industry reference registry with R2-R4/R7 using deprecation instead of
   removal.
4. Update validators for duplicate active ids, ambiguous aliases and new required
   canonical nodes.
5. Run local checks:

```bash
python3 scripts/validate_issue_152_industry_taxonomy_standard.py
python3 scripts/validate_issue_156_industry_taxonomy_registry.py
python3 scripts/validate_issue_168_industry_reference_integrity.py
python3 scripts/validate_issue_170_mango_registry.py
make kb-validate
python3 experiments/issue-174/score_convergence.py
python3 experiments/issue-176-convergence/score.py
```

6. Prepare repeat convergence test. Important: the current scorer replays
   already committed gold/AI outputs. A true post-fix convergence claim requires
   a fresh blind classification run against the updated standard and registry,
   then scoring the new outputs.
7. Update PR description with before/after metrics and explicitly state that
   changes are ready for repeat convergence test.

## 8. Risks

| Risk | Mitigation |
| --- | --- |
| Path refactor regression | Do not reintroduce retired taxonomy paths; keep #178 changes inside the current `kb/industry-taxonomy/` and `kb/mango-taxonomy/` directories. |
| Existing Mango registry references point to deprecated nodes | Deprecate with replacement first; update Mango registry only if approved or in a separate CR. |
| Validator becomes too strict for legitimate homonyms | Require `homonym_allowed: true` and explicit rationale, not global hard uniqueness for every slug. |
| Overfitting to the 25-case test | Rules are based on recurring patterns also seen in Mango convergence test (#176), not only individual examples. |
| `function_type` corrections conflict with current gold | Ask founder to decide status actions explicitly before changing registry data. |
| Removing nodes breaks history | Use `deprecated` and aliases/replacements; no hard removal in this issue. |

## 9. Approval request

Прошу фаундера явно согласовать:

1. Можно ли считать R1-R7 approved scope for implementation in PR #179?
2. Входит ли correction `kb/mango-taxonomy/mango-registry.json` for #21 and
   depth mappings в scope #178, или это отдельный PR?
3. Как классифицировать status-changing functions в `function_type`: keep current
   gold as `ui-action`, or correct to `business`/`configuration` when they change
   operational state?

До ответа на эти вопросы реализация стандарта и реестра должна оставаться
заблокированной.
