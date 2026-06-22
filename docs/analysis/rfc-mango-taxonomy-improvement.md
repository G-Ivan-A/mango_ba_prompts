---
status: draft
version: 0.1
updated: 2026-06-22
ai-generated: true
type: rfc
scope: mango-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/181"
based_on:
  - "docs/analysis/mango-taxonomy-convergence-test.md"
  - "standards/mango-taxonomy-standard.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "kb/mango-taxonomy/mango-registry.json"
  - "kb/industry-taxonomy/reference-taxonomy.json"
related_rfc:
  - "docs/analysis/rfc-industry-taxonomy-improvement.md"
target_artifacts:
  - "standards/mango-taxonomy-standard.md"
  - "kb/mango-taxonomy/mango-registry.json"
  - "scripts/validate_issue_170_mango_registry.py"
  - "scripts/validate_issue_154_mango_taxonomy_standard.py"
---

# RFC: доработка Mango Taxonomy после теста на сходимость

> Это RFC для human review, а **не** реализация. До явного согласования
> фаундером (Иваном) не меняются `standards/mango-taxonomy-standard.md`, Mango
> registry, валидаторы или ADR-012. Industry Taxonomy Standard, Industry registry
> и структура каталогов не меняются в рамках issue #181 ни при каких условиях.

## 1. Статус путей после PR #173

Issue #181 требует использовать актуальные пути после переименования каталогов
(PR #173, уже merged в `upstream/main`):

| Artifact | Старый путь (в отчёте теста встречается) | Актуальный путь |
| --- | --- | --- |
| Mango registry | `kb/mango/...` | `kb/mango-taxonomy/mango-registry.json` |
| Industry registry | `kb/industry/...` | `kb/industry-taxonomy/reference-taxonomy.json` |
| Mango convergence report | — | `docs/analysis/mango-taxonomy-convergence-test.md` |
| Mango convergence experiment | — | `experiments/issue-176-convergence/` |

Отчёт теста (`docs/analysis/mango-taxonomy-convergence-test.md`) и его артефакты
уже используют актуальные пути; устаревшие `kb/mango/` / `kb/industry/` в текущей
ветке не встречаются. Этот RFC не предлагает переименование каталогов и не
требует stacking поверх другой ветки.

## 2. Входные факты

Тест локально воспроизведён из корня репозитория:

```bash
python3 experiments/issue-176-convergence/score.py
```

Результат Mango → Industry convergence test (#176), совпадает с отчётом:

| Метрика | Результат | Порог ДоД |
| --- | --- | --- |
| Exact full path (формула ДоД) | **10/27 = 37%** | ≥ 80% |
| Prefix match | 17/27 = 63% | ≥ 80% |
| Domain | 22/27 = 81% | ≥ 80% |
| Capability | 18/27 = 67% | — |
| Feature | 1/8 = 12% | — |
| Function | 0/1 = 0% | — |
| AI node resolves в reference taxonomy | 27/27 = 100% | — |
| alignment_type | 27/27 = 100% | — |

Структурные факты, проверенные напрямую по реестрам:

- Mango registry (`taxonomy.version 1.0.0`) содержит 271 entity всех 5 уровней.
- Industry registry (`version 1.1.0`) содержит дубли одинаковых `id` под разными
  родителями. Подтверждены резолвером (`score.py`) и прямой проверкой:

  | Дублированный `id` | Ветка A | Ветка B |
  | --- | --- | --- |
  | `conversation-summaries` | `contact-center/agent-assist/conversation-summaries` | `ai-automation/conversation-summaries` |
  | `access-control` | `security/information-security/access-control` | `security/access-control` |
  | `call-routing` | `voice-ucaas/call-routing` | `contact-center/call-routing` |
  | `live-monitoring` | `contact-center/supervisor-assist/live-monitoring` | `contact-center/supervisor-workspace/live-monitoring` |
  | `interaction-routing` | `…/inbound-handling/interaction-routing` | `contact-center/interaction-routing` |
  | `device-provisioning` | `hardware/telephony-equipment/sip-phones/device-provisioning` | `hardware/device-management/device-provisioning` |

- Эталонные primary-маппинги в Mango registry для ряда Module/Function останавливаются
  на capability, хотя §7.3 стандарта рекомендует глубину `+ feature` (Module) и
  `+ feature + function` (Function). Подтверждено для `cc-supervisor-monitoring-module`,
  `vats-voicemail-management-module`, `bitrix24-connector-module`,
  `run-voice-robot-dialog` и др.

## 3. Корневые причины (по отчёту теста)

Отчёт классифицирует 17 несовпадений в 4 воспроизводимые причины. Ключевой факт
из отчёта: **ни одно расхождение не является галлюцинацией** — агент 27/27 раз
выбирал реально существующий узел по защитимой логике (резолвимость 100%).

| Причина | Кейсы | Кол-во | Чей дефект | Где чинить в рамках #181 |
| --- | --- | :---: | --- | --- |
| **A.** Дубли id-узлов Industry + нет правила выбора ветки | #12, #15, #19, #22 | 4 | Industry registry + оба стандарта | Mango standard: disambiguation rule (выбор ветки). Дедуп самих узлов — Industry scope (#178). |
| **B.** Нет boundary-правила «CPaaS/API/UC ↔ digital-channels» | #10, #18, #24 | 3 | Mango/Industry стандарты | Mango standard: явное boundary-правило для маппинга. |
| **C.** Гранулярность capability + возможная ошибка наследования (#17) | #11, #16, #17 | 3 | Стандарт + Mango registry | Mango standard: roll-up rule. Mango registry: ревизия #17. |
| **D.** Mango registry мельче §7.3 по глубине | #8, #20, #21, #23, #25, #26, #27 | 7 | Mango registry | Mango registry: доуглубить `maps_to` до §7.3. |

### 3.1 Что находится внутри scope #181, а что — нет

Issue #181 запрещает менять Industry Taxonomy Standard и Industry registry. Это
разделяет работу так:

- **Внутри scope #181 (Mango-сторона):**
  - правила выбора и boundary-rules в **Mango** standard (это не меняет Industry
    standard — это инструкция «как Mango выбирает Industry-узел при маппинге»);
  - доуглубление `maps_to` и ревизия конкретных эталонов в **Mango** registry;
  - валидаторы Mango.
- **Вне scope #181 (Industry-сторона, issue #178 / PR #179):**
  - физический дедуп дублированных `id` (`conversation-summaries`,
    `access-control`, `call-routing`, …) в `reference-taxonomy.json`;
  - правила homonym/deprecation в Industry standard.

> **Важное следствие.** Полное закрытие причины A требует Industry-side дедупа,
> который вне scope #181. Но Mango может **детерминировать выбор** при текущих
> дублях через disambiguation-правило в своём стандарте — этого достаточно, чтобы
> Mango registry (эталон) и дисциплинированный агент сходились. Подробно — §4.1.

## 4. Предлагаемые изменения

Приоритеты: **P1** (Critical) закрывают наибольшую долю расхождений и/или
дефекты данных; **P2** (Major) — правила выбора; **P3** — повторный тест.

### R1 — P1 — Mango registry: доуглубить `maps_to` до §7.3 (причина D)

**Адресует:** причину D (7 кейсов: #8, #20, #21, #23, #25, #26, #27) — самый
крупный одиночный блок расхождений.

Эталонные primary-маппинги Module/Function в `kb/mango-taxonomy/mango-registry.json`
систематически мельче рекомендации §7.3. Во всех 7 случаях путь агента **содержит
эталон как префикс** и резолвится в Industry registry — агент оказался
дисциплинированнее эталона.

Предлагается для каждого из 7 кейсов (и для всех аналогичных Module/Function в
реестре, выявленных сплошной проверкой) либо доуглубить `industry_ref` до
канонического узла, либо, если канонического узла нет, явно проставить
`mapping_gap` (§7.5):

| # | Level | Эталон сейчас | Предлагаемый канонический путь | §7.3 цель |
| --- | --- | --- | --- | --- |
| 20 | module | `platform/platform-integration` | `…/crm-connectors` | feature |
| 21 | function | `ai-automation/voice-bot` | `…/voice-dialog-orchestration/voice-dialog-flow` | feature+function |
| 23 | function | `voice-ucaas/unified-communications` | `…/softphone` (или `mapping_gap`, если нет function-узла) | feature+function |
| 25 | function | `platform/open-api/webhooks` | `…/webhook-subscription` | feature+function |
| 26 | function | `analytics/call-tracking` | `…/source-attribution/source-attribution` | feature+function |
| 27 | function | `contact-center/agent-workspace` | `…/agent-desktop/interaction-handling` | feature+function |
| 8 | service | `voice-ucaas/ivr-voice-menu` | для service §7.3 рекомендует только capability — здесь эталон **корректен**; углубление агента до `…/ivr-scenarios` допустимо, но не требуется. Возможный шаг: пометить как acceptable-deeper. |

**Обязательное правило при реализации:** глубина проставляется только для реально
существующих в `reference-taxonomy.json` узлов. Если узел отсутствует — `mapping_gap`,
а не выдуманный slug (§1.4 запрещает создавать Industry slug из Mango label).

**Ожидаемый эффект:** при доуглублении эталона до пути, который выбирает
дисциплинированный агент, эти 6–7 кейсов из расхождений переходят в exact-match.
Чистый эффект на строгую метрику: +6…+7 (37% → ~63%).

### R2 — P1 — Mango standard: disambiguation rule для дублированных Industry-узлов (причина A)

**Адресует:** причину A (4 кейса: #12, #15, #19, #22).

Пока Industry registry содержит один и тот же `id` под двумя родителями, два
корректных классификатора расходятся. Дедуп самих узлов — Industry scope (#178),
но Mango должна детерминировать выбор ветки **на своей стороне**. Предлагается
добавить в §7 Mango standard правило выбора канонической ветки:

1. Если требуемый смысл резолвится в **несколько** Industry-узлов с одинаковым
   `id` под разными родителями — выбирается ветка, чей **parent chain семантически
   ближе к назначению Mango-сущности** (по `description`/`cluster`/`function_type`),
   а не первый/короткий путь.
2. Для повторяющихся пар фиксируются явные prescriptive-выборы (таблица ниже),
   чтобы эталон и агент совпадали детерминированно:

   | Дублированный смысл | Канонический выбор для Mango-маппинга | Прецедент |
   | --- | --- | --- |
   | AI-конспекты разговоров (contact-center agent-assist) | `contact-center/agent-assist/conversation-summaries` | #12, #19 — эталон |
   | Управление доступом/ролями в ИБ-контуре | `security/information-security/access-control` | #15, #22 — эталон |

3. После Industry-side дедупа (#178) это правило ссылается на canonical-узел и
   срабатывает автоматически (alias deprecated-ветки → canonical).

> Правило живёт в **Mango** standard и описывает только то, *как Mango выбирает*
> Industry-узел при маппинге. Оно **не** изменяет Industry standard и не создаёт
> Industry-узлов.

**Ожидаемый эффект:** закрывает #12, #15, #19, #22 (после согласования
канонического выбора). До Industry-дедупа правило держит эталон и агента на одной
ветке; после дедупа становится автоматическим.

### R3 — P2 — Mango standard: boundary-правило «CPaaS/API/UC ↔ digital-channels» (причина B)

**Адресует:** причину B (3 кейса: #10, #18, #24).

Стандарт даёт правило только для **Mango-кластера** Talker, но не для выбора
**Industry**-домена при программных/корпоративных коммуникациях. Предлагается
добавить в §7 явный boundary-критерий:

1. **API/CPaaS vs digital-channel.** Если Mango-сущность — это программный
   интерфейс отправки/приёма сообщений (Dialog API, webhooks, programmable
   messaging), её primary Industry-маппинг = `platform/cpaas/...`
   (`programmable-messaging`), **не** `digital-channels/omnichannel-messaging`.
   Признак: `interaction_surface: api|webhook` и evidence об API/программном
   контракте. Закрывает #10, #24.
2. **UC corporate-messaging vs digital team-messaging.** Если сущность —
   корпоративный мессенджер/файлообмен внутри Mango Talker (UC-клиент), её primary
   Industry-маппинг = `voice-ucaas/unified-communications/corporate-messaging`,
   **не** `digital-channels/team-messaging`. Закрывает #18.
3. Критерий формулируется однозначно (по surface + evidence), чтобы не зависеть
   от чтения свободного описания.

**Ожидаемый эффект:** закрывает #10, #18, #24 (3 кейса).

### R4 — P2 — Mango standard + registry: правило гранулярности + ревизия #17 (причина C)

**Адресует:** причину C (3 кейса: #11, #16, #17).

1. **Roll-up rule (standard).** Добавить правило: когда сущность относится к
   capability, у которого есть и зонтичный родитель, и специфичный sibling,
   выбор делается по доминирующему смыслу evidence; при равной валидности
   предпочитается узел, чей parent chain сохраняет семантическое containment.
   Документирует законность judgment-calls #11 (видео Talker: UC-зонтик vs
   `video-conferencing`) и #16 (voicemail: `call-recording` vs
   `cloud-pbx/voicemail`).
2. **Ревизия эталона #17 (registry).** `cc-supervisor-monitoring-module` сейчас
   наследует `workforce-management` от родительского сервиса
   `cc-supervisor-wfm-service`. Отчёт указывает, что выбор агента
   `supervisor-assist/live-monitoring` **семантически точнее** («контроль и
   прослушивание операторов» — это supervisor-assist, не WFM). Предлагается
   проверить и, при подтверждении, исправить эталон в Mango registry на
   `contact-center/supervisor-assist/live-monitoring`.

   > ⚠️ `live-monitoring` сам является дублированным Industry-узлом (см. §2:
   > `supervisor-assist/live-monitoring` vs `supervisor-workspace/live-monitoring`).
   > Поэтому ревизия #17 должна применять disambiguation-правило R2.

**Ожидаемый эффект:** документирует #11, #16 как законные judgment-calls (и/или
выравнивает эталон по согласованному roll-up-правилу); исправляет #17, если
ревизия подтвердит ошибку наследования.

### R5 — P3 — повторный тест и фиксация v1.0

После реализации R1–R4 — **свежий слепой прогон** теста против обновлённого
стандарта и реестра (не реплей уже зафиксированных AI-выходов), затем подсчёт
`score.py`. Фиксировать Mango Taxonomy v1.0 только при достижении порога.

## 5. Ожидаемый measurable effect

Текущий exact full path: 10/27 = 37%.

| Причина | R | Кейсы | Эффект на exact-match |
| --- | --- | --- | --- |
| D | R1 | #8, #20, #21, #23, #25, #26, #27 | +6…+7 |
| A | R2 | #12, #15, #19, #22 | +4 |
| B | R3 | #10, #18, #24 | +3 |
| C | R4 | #11, #16, #17 | +2…+3 |

Консервативная оценка: при срабатывании R1 (+6), R2 (+4), R3 (+3) и частично R4
(+2): `(10 + 15) / 27 = 93%`. Даже если 2–3 кейса останутся как законные
judgment-calls, требующие human review, ожидаемый результат **≥ 80%** по строгой
формуле — порог ДоД достигается.

> ⚠️ **Честная оговорка о методе (как в Industry RFC).** Текущий `score.py`
> сравнивает уже зафиксированные gold/AI-выходы. Истинное пост-фикс утверждение о
> сходимости требует нового слепого прогона классификации против обновлённых
> стандарта и реестра, затем подсчёта новых выходов. R5 это учитывает.

## 6. Влияние на артефакты

| Artifact | Impact |
| --- | --- |
| `standards/mango-taxonomy-standard.md` | Добавить disambiguation rule (R2), boundary rule (R3), roll-up rule (R4). Версия → 0.3 (правила меняют поведение маппинга). |
| `kb/mango-taxonomy/mango-registry.json` | Доуглубить `maps_to` Module/Function до §7.3 (R1); ревизия эталона #17 (R4). `taxonomy.version` → 1.1.0 (non-breaking уточнения) или 2.0.0, если #17 меняет canonical mapping. |
| `scripts/validate_issue_170_mango_registry.py` | Опционально: проверка глубины `maps_to` против §7.3 (warning, если мельче без `mapping_gap`). |
| `scripts/validate_issue_154_mango_taxonomy_standard.py` | Без обязательных изменений; при добавлении новых normative-секций обновить контракт проверки. |
| `standards/decisions/ADR-012-mango-taxonomy.md` | **Без изменений.** RFC не противоречит ADR-012 (см. §8). Приоритет ADR-011 над ADR-012 сохраняется. |
| `standards/industry-taxonomy-standard.md` | **Без изменений** (отдельная задача #178). |
| `kb/industry-taxonomy/reference-taxonomy.json` | **Без изменений** в рамках #181. Дедуп дублей — Industry scope. |
| `CHANGELOG.md` | Запись по #181 добавляется после approved-реализации. |

## 7. Зависимость от Industry Reference Data (обязательно по ДоД п.10)

Mango registry содержит `maps_to.industry_alignment[].industry_ref`, ссылающийся
на `kb/industry-taxonomy/reference-taxonomy.json`. Параллельная задача #178
(PR #179) предлагает дедуплицировать дублированные Industry-узлы через
`deprecated` + `replacement` + alias.

**Какие изменения Industry потребуют синхронизации Mango:**

| Industry-изменение (#178) | Эффект на Mango registry | Действие синхронизации |
| --- | --- | --- |
| `access-control` дедуп: одна ветка canonical, вторая deprecated | Mango #15/#22 ссылаются на `security/information-security/access-control`. Если canonical станет `security/access-control` — Mango ref надо обновить на canonical. | Сверить выбранный Industry canonical с R2-таблицей; обновить Mango ref. |
| `conversation-summaries` дедуп | Mango #12/#19 → `contact-center/agent-assist/conversation-summaries`. | Подтвердить, что Industry оставил эту ветку canonical; иначе обновить. |
| `call-routing` / `live-monitoring` / `interaction-routing` дедуп | Затрагивает #17 (R4) и потенциально другие записи реестра. | После дедупа повторно прогнать R4-ревизию. |
| Новые Industry feature/function узлы (R4 в Industry RFC) | Может появиться канонический узел там, где Mango стоит `mapping_gap`. | Заменить `mapping_gap` на реальный ref. |

**План синхронизации:**

1. R2/R3/R4 в этом RFC намеренно выбирают ветки, **совпадающие с эталоном теста**
   и с предложениями Industry RFC (PR #179) — чтобы минимизировать рассинхрон.
2. После merge Industry-изменений (#178) — повторить проверку: все ли Mango
   `industry_ref` резолвятся в **не-deprecated** canonical-узлы.
3. Если после Industry-дедупа какие-то Mango ref указывают на deprecated-ветку —
   это **отдельная задача синхронизации** (не в scope #181), как требует issue.
4. Порядок предпочтителен: сначала Industry (#178/#179), затем Mango (#181) —
   тогда Mango сразу маппится на финальные canonical-узлы. Если Mango реализуется
   первым, Industry-deprecation должен сохранять alias, чтобы Mango ref не ломались.

## 8. Непротиворечивость ADR-012 и ADR-011 (самопроверка)

- **Приоритет источников.** ADR-012 фиксирует: «ADR-011 имеет приоритет над
  ADR-012… по форме `industry_ref`». R2/R3/R4 выбирают существующие
  canonical-узлы Industry и **не** создают Industry slug из Mango label (§1.4) —
  значит, не инвертируют приоритет.
- **Двухслойная модель.** Изменения касаются только Mango Internal Layer
  (`maps_to` глубина) и правил маппинга, не трогая Official/Internal разделение и
  иерархию `Product → Service → Module → Function`.
- **`alignment_type`.** Тест показал 100% совпадение `alignment_type`; RFC его не
  меняет.
- **mapping_gap.** R1 явно использует §7.5 mapping_gap там, где канонического
  Industry-узла нет — это уже согласованный механизм ADR-012/стандарта.

Вывод: RFC не требует изменений ADR-012 и не противоречит ADR-011. Изменение
ADR-012 запрашивается **только** если фаундер решит, что ревизия #17 (R4) меняет
canonical-решение уровня ADR (по умолчанию — нет, это registry-correction).

## 9. Риски

| Risk | Mitigation |
| --- | --- |
| Дедуп Industry (#178) выберет другую canonical-ветку, чем R2 | R2-таблица выбрана по эталону теста; синхронизация по §7 после merge #178. |
| Доуглубление эталона = оверфит под конкретный AI-выход | Углубляем только до **существующих** canonical-узлов и только там, где §7.3 это рекомендует; путь агента уже был префикс-совместим с эталоном. |
| Ревизия #17 поломает наследование capability в реестре | Менять только запись #17 после подтверждения evidence; не трогать родительский `cc-supervisor-wfm-service`. |
| Mango ref укажет на deprecated Industry-узел | Industry-deprecation сохраняет alias; пост-merge проверка резолвимости (§7, п.2). |
| Реплей-метод завысит/занизит пост-фикс сходимость | R5 требует свежий слепой прогон, а не реплей. |
| Изменение версий ломает downstream | Использовать non-breaking версии (standard 0.3, registry 1.1.0) если #17 не меняет canonical; иначе явно поднять major и отметить в CHANGELOG. |

## 10. План реализации после approval

1. Работать на ветке `issue-181-...`, синхронизированной с `upstream/main`.
2. Обновить Mango standard: R2 (disambiguation), R3 (boundary), R4 (roll-up).
3. Обновить Mango registry: R1 (глубина §7.3), R4 (ревизия #17), `mapping_gap`
   где нет канонического узла.
4. Обновить валидатор Mango (опционально: depth-check).
5. Локальные проверки:

```bash
python3 scripts/validate_issue_154_mango_taxonomy_standard.py
python3 scripts/validate_issue_170_mango_registry.py
make kb-validate
python3 experiments/issue-176-convergence/score.py
```

6. Подготовить повторный convergence test (R5): свежий слепой прогон против
   обновлённых артефактов, затем `score.py` по новым выходам.
7. Обновить CHANGELOG.md и описание PR: before/after метрики + явная пометка, что
   изменения готовы к повторному тесту.
8. После merge Industry (#178) — проверить резолвимость Mango ref; при
   необходимости — отдельная задача синхронизации.

## 11. Approval request (Этап 3)

Прошу фаундера явно согласовать перед реализацией:

1. Принять R1–R5 как approved scope для реализации в PR #183?
2. **Канонический выбор веток (R2):** подтвердить
   `contact-center/agent-assist/conversation-summaries` (#12/#19) и
   `security/information-security/access-control` (#15/#22) как canonical для
   Mango-маппинга — или указать другой?
3. **Ревизия #17 (R4):** менять ли эталон `cc-supervisor-monitoring-module` с
   `workforce-management` на `contact-center/supervisor-assist/live-monitoring`?
   Если да — считается ли это registry-correction (без ADR-012) или требует
   обновления ADR-012?
4. **Порядок с Industry (#178):** реализовывать Mango до или после Industry-дедупа?
   (Рекомендация RFC — после, §7 п.4.)
5. **Версионирование:** standard → 0.3, registry → 1.1.0 (non-breaking) — или
   поднять major, если #17 трактуется как breaking?

До явных ответов на эти вопросы реализация стандарта и реестра остаётся
**заблокированной** (Этап 4 не начинается).
