---
status: draft
version: 0.1
updated: 2026-06-24
ai-generated: true
type: analysis
scope: governance
operating_mode: creative
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/225"
related_artifacts:
  - "governance/rfc-process.md"
  - "standards/artifact-naming-standard.md"
  - "standards/executable-contract-standard.md"
  - "docs/analysis/executable-contracts-and-rfc-problems.md"
---

# Исследование гипотезы цепочки артефактов

> Research-документ по issue
> [#225](https://github.com/G-Ivan-A/mango_ba_prompts/issues/225).
> Это **только анализ и предложения**: документ не создаёт RFC, ADR, standard,
> контракт или новое обязательное правило процесса.

## 1. Введение

Цель исследования - критически проверить гипотезу цепочки:

```text
research → analytics → report → rfc/adr → standard → artifact
```

и ответить, как она соотносится с текущим
[`governance/rfc-process.md`](../../governance/rfc-process.md), международными
практиками ADR/RFC/standards и уже зафиксированной моделью L1/L2/L3 из
[`standards/executable-contract-standard.md`](../../standards/executable-contract-standard.md).

Методология:

1. **Архитектор методологий**: сравнил гипотезу с ADR, RFC/PEP/KEP и standards
   lifecycle в международных проектах.
2. **BA-эксперт**: разобрал цепочку с точки зрения ролей артефактов, рисков,
   возможностей и трассируемости.
3. **AI-инженер**: сопоставил выводы с текущим RFC-процессом Mango и предложил
   улучшения без изменения действующих процессов.

Рабочая рамка проекта:

- Текущий RFC-процесс наследует цепочку Хаба
  `Observation → Research → Hypothesis → RFC → Pattern → Standard → Template → Framework → Deprecation/Archive`.
- Локальный спок уже различает L1-исполнение, L2-данные и L3-управление:
  standards/RFC/ADR/process-docs относятся к L3 и не должны становиться runtime
  входами L1 без явного переноса правил.
- Issue #225 просит не внедрять решения, а создать source-backed research с
  BPMN-диаграммами.

Ключевой вывод: гипотеза полезна как **карта трассируемости**, но её опасно
читать как жёсткую линейную трубу. Международная практика ближе к графу с
итерациями: proposal-документы собирают обратную связь, decision records
фиксируют принятое решение, standards требуют отдельного maturity-gate, а малые
изменения могут идти коротким путём.

## 2. Международные практики

### 2.1 ADR: запись решения, а не полный процесс изменения

| Источник | Наблюдение | Вывод для Mango |
| --- | --- | --- |
| Michael Nygard, [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | ADR фиксирует architecturally significant decision: контекст, решение, статус, последствия; записи короткие, нумеруются монотонно, superseded-решения сохраняются. | ADR стоит трактовать как L3 decision record: "почему и какое архитектурное решение принято", а не как универсальный proposal или стандарт. |
| ADR community, [adr.github.io](https://adr.github.io/) | ADR captures a single architectural decision, rationale, trade-offs and consequences; набор ADR образует decision log. | Один ADR - одно решение. Если документ обсуждает несколько альтернатив и собирает feedback, это ближе к RFC/proposal. |
| GitHub Engineering, [Why Write ADRs](https://github.blog/engineering/architecture-optimization/why-write-adrs/) | GitHub описывает ADR как способ документировать how and why decision was reached inside codebase, включая решения iOS/Android/mobile clients. | ADR применим для проектной памяти и onboarding, но не заменяет review/proposal-процесс. |
| GitLab, [Architecture Design Documents](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/) и [Design Decisions](https://docs.gitlab.com/charts/architecture/decisions/) | GitLab использует version-controlled design documents как основной артефакт architecture design workflow; отдельные decision docs собирают reasoning and decisions. | В зрелой практике рядом могут жить design proposal и decision log. Это поддерживает разделение RFC vs ADR, но не требует строгой последовательности. |

Практический принцип: ADR отвечает на вопрос **"какое архитектурное решение
принято и почему?"**. Он может быть результатом RFC, отчёта, production incident
или архитектурной задачи напрямую. Поэтому связь RFC → ADR полезна, но не должна
быть единственным разрешённым входом в ADR.

### 2.2 RFC/PEP/KEP: предложение, обсуждение, решение, затем реализация

| Практика | Наблюдение | Вывод для Mango |
| --- | --- | --- |
| IETF, [RFC 2026](https://datatracker.ietf.org/doc/html/rfc2026) и [About RFCs](https://www.ietf.org/process/rfcs/) | RFC-серия включает разные потоки; standards track имеет стадии и требования переходов, но не каждый RFC является Internet Standard. | RFC в Mango не должен автоматически становиться standard. Нужен явный статус и gate. |
| Rust, [RFC repository](https://github.com/rust-lang/rfcs) | RFC даёт controlled path для существенных изменений, но bug fixes и docs improvements идут обычным PR workflow. | Обязательность RFC должна зависеть от масштаба и риска, иначе процесс перегрузит малые изменения. |
| Python, [PEP 1](https://peps.python.org/pep-0001/) | PEP - design document со specification и rationale; есть обсуждение, review/resolution, accepted/final/rejected/superseded, а accepted PEP становится historical document. | Статусная модель должна отделять "proposal", "decision" и "implemented". Rejected тоже сохраняет ценность. |
| Swift, [Evolution process](https://github.com/swiftlang/swift-evolution/blob/main/process.md) | Существенное изменение проходит proposal document + open review; возможны revision loops; workgroup принимает accept/reject/revise. | Гипотеза должна разрешать циклы назад в analytics/research и повторное review, а не только движение вперёд. |
| Kubernetes, [KEP process](https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md) | KEP даёт common structure, motivation, stability milestones, graduation criteria и сохраняет проектную информацию в VCS. | Для крупных изменений полезен не только RFC, но и maturity model: критерии готовности, тест-план, graduation. |
| LLVM, [RFC Process](https://llvm.org/docs/RFCProcess.html) | Substantive changes требуют community consensus; RFC должен иметь overview, motivation, impact, open questions; после accepted работа идёт incremental PRs. | RFC должен завершаться реализационными шагами и criteria, но сама реализация не должна жить внутри RFC. |
| Linux Kernel, [Submitting patches](https://docs.kernel.org/process/submitting-patches.html) | `[RFC PATCH]` - лёгкий способ явно запросить comments на ранний draft. | Не все "RFC" одинаково тяжёлые: полезен lightweight режим для раннего feedback без формального статуса standard/proposal. |

Практический принцип: RFC-подобный артефакт отвечает на вопрос **"что предлагается
изменить, зачем, как получить feedback и кто принимает решение?"**. Он может
привести к ADR, standard, implementation PR или отказу.

### 2.3 Standards: отдельный maturity-gate

| Источник | Наблюдение | Вывод для Mango |
| --- | --- | --- |
| ISO, [Stages and resources for standards development](https://www.iso.org/stages-and-resources-for-standards-development.html) | ISO использует defined stages: Proposal, Preparatory, Committee, Enquiry, Approval, Publication; proposal stage подтверждает, что standard действительно нужен. | Standard начинается с обоснования необходимости и проходит отдельный процесс, а не возникает автоматически из ADR/RFC. |
| IEEE SA, [Developing Standards](https://standards.ieee.org/develop/) | IEEE описывает six stage life cycle и принципы direct participation, due process, broad consensus, balance, transparency, broad openness. | Для standard в Mango нужен gate шире, чем "автор RFC решил": баланс заинтересованных сторон и прозрачность. |
| W3C, [Process Document](https://www.w3.org/policies/process/) | Recommendation Track строится вокруг wide review, adequate implementation experience, consensus; путь FPWD → WD → Candidate Recommendation → Recommendation допускает regression и superseding. | Стандарт должен учитывать implementation evidence и возможность отката/пересмотра, особенно если он станет L3-правилом для будущих L1/L2. |

Практический принцип: standard отвечает на вопрос **"какое правило становится
нормативным для повторяемого создания артефактов?"**. RFC/ADR могут инициировать
standard, но не должны активировать standard напрямую.

### 2.4 Сводное сравнение с гипотезой

| Элемент гипотезы | Совпадение с практикой | Коррекция |
| --- | --- | --- |
| `research → analytics → report` | Source-backed analysis перед proposal соответствует PEP/KEP/RFC-quality bar. | Не каждый proposal требует отдельный report; для малых изменений достаточно ссылки на issue/experiment. |
| `report → rfc/adr` | Отчёт может породить proposal или decision record. | ADR может возникнуть не только после report, но и после архитектурной задачи, incident или accepted RFC. |
| `rfc ↔ adr` | GOV.UK Design System явно разделяет RFC as proposals и ADR as decision records в одном публичном репозитории: [Use RFCs and ADRs](https://github.com/alphagov/govuk-design-system-architecture/blob/main/proposals/001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions.md). | Нужны entry criteria: RFC для обсуждения изменения, ADR для фиксации принятого архитектурного решения. |
| `rfc/adr → standard` | Standards часто начинаются с proposal/need и проходят maturity stages. | Нужен отдельный standard process/gate; direct transition допустим только как initiation, не как activation. |
| `standard → artifact` | Standard как L3-правило создания артефактов согласуется с текущим executable-contract-standard. | Artifact может создаваться без отдельного standard, если это единичный продукт или draft в Creative mode. |

## 3. Анализ видения Фаундера

### 3.1 Разбор цепочки

| Переход | Что даёт | Где нужен gate | Комментарий |
| --- | --- | --- | --- |
| `research → analytics` | Перевод глобальной практики Хаба в локальный контекст проекта. | Проверка применимости к Mango. | Сильный переход: снижает риск "изобретения велосипеда". |
| `analytics → report` | Упаковка находок, аудита, статистики и evidence. | Достаточность источников и явный scope. | Не всегда нужен отдельный report: маленький сигнал может идти сразу в lightweight RFC/issue. |
| `report → rfc` | Формализация "что изменить?" и сбор feedback. | Human review; статус `proposed/in-review/accepted/rejected`. | Соответствует текущему RFC-процессу, но нужно отделять proposal от implementation. |
| `report → adr` | Фиксация архитектурного решения "как построить?" после анализа. | Решение уполномоченного human/architecture owner. | ADR не должен содержать неразрешённый список вопросов как основной payload. |
| `rfc ↔ adr` | Разделение продуктовой и архитектурной логики. | Проверка, не дублируются ли решения. | Это граф, а не pipeline: RFC может запросить ADR, ADR может выявить продуктовую неопределённость и вернуть к RFC. |
| `rfc/adr → standard` | Кодификация повторяемого правила создания артефактов. | Отдельный standard gate: need, consensus, applicability, validation. | Direct initiation допустима; direct activation рискованна. |
| `standard → artifact` | Повторяемое создание конкретных документов, контрактов, prompts, registries. | Проверка L1/L2/L3 и naming/traceability. | Artifact может быть создан и без standard, если это scoped draft или одноразовый результат. |

### 3.2 Разделение RFC vs ADR

Гипотеза в целом совпадает с международной практикой:

- **RFC**: proposal/change request, где обсуждается "что изменить?", почему это
  важно, каков impact, какие open questions и критерии принятия.
- **ADR**: decision record, где фиксируется "какое архитектурное решение принято?",
  с контекстом и последствиями.

Граница не всегда проходит по "продуктовое vs архитектурное". Например, Swift
proposal может быть одновременно продуктовым и архитектурным, а Kubernetes KEP
может содержать design details, тест-план и graduation criteria. Поэтому более
устойчивая граница для Mango:

- RFC нужен, когда **решение ещё не принято** и нужно собрать feedback/approval.
- ADR нужен, когда **архитектурное решение принято** и его нужно сохранить как
  future-context.
- Standard нужен, когда **правило должно многократно применяться** для будущих
  артефактов.

### 3.3 Риски гипотезы

| Риск | Суть | Пример из практики | Влияние на проект |
| --- | --- | --- | --- |
| R-1 | Линейное чтение цепочки скроет реальные циклы и возвраты. | Swift Evolution допускает revision loops и повторный open review. | Высокое: процесс может начать "проталкивать" плохие решения вперёд вместо возврата в analytics. |
| R-2 | Mandatory report для каждого изменения создаст governance overhead. | Rust RFC process явно выводит bug fixes/docs improvements в обычный PR workflow. | Среднее: small changes станут дорогими, пользователи будут обходить процесс. |
| R-3 | RFC и ADR начнут дублировать друг друга без entry criteria. | GOV.UK разделяет RFC/proposals и ADR/decision records, чтобы discussion и record не смешивались. | Высокое: потеряется источник истины по статусу решения. |
| R-4 | `canonical` может быть ошибочно прочитан как автоматическое approval. | Текущий `governance/rfc-process.md` уже фиксирует: повышение статуса - только по решению человека. | Высокое: proposal может стать нормой без human gate. |
| R-5 | `rfc/adr → standard` без отдельного standard gate обойдёт maturity evidence. | ISO/IEEE/W3C требуют stages, review, consensus, publication/implementation evidence. | Высокое: L3-standard начнёт управлять L1/L2 без достаточной проверки. |
| R-6 | Traceability overload: каждый artifact будет тащить полный хвост research/report/RFC/ADR. | Nygard ADR deliberately short; Linux `[RFC PATCH]` lightweight для раннего feedback. | Среднее: документы станут тяжелее источников, которые должны объяснять. |
| R-7 | "research только Hub" может заблокировать локальные discovery-задачи, если не различить global research и project analytics. | Текущий `CONTRIBUTING.md` уже запрещает `research/` в споке, но разрешает `docs/analysis/`. | Среднее: агент может останавливаться там, где нужен локальный analysis, а не новый research-каталог. |

### 3.4 Возможности гипотезы

| Возможность | Что улучшает | Оценка влияния |
| --- | --- | --- |
| O-1 | Явная карта от источника до финального artifact: легче ответить "почему создан этот документ?". | Высокое |
| O-2 | Разведение RFC/ADR снижает смешение proposal и decision record. | Высокое |
| O-3 | Отдельный standard-gate помогает не превращать каждый accepted RFC в норматив. | Высокое |
| O-4 | Возвраты к analytics/research легализуют итеративность вместо искусственной линейности. | Среднее |
| O-5 | Согласование с L1/L2/L3 предотвращает runtime-загрузку L3-документов агентом. | Высокое |
| O-6 | Единая цепочка даёт основу для будущих validators: наличие source, status, decision, implementation evidence. | Среднее |
| O-7 | Встроенная роль report/audit помогает отделить факты от proposed changes. | Среднее |

## 4. Анализ текущего RFC-процесса

### 4.1 Что уже работает

Текущий [`governance/rfc-process.md`](../../governance/rfc-process.md) содержит
несколько сильных решений:

- RFC - proposal, а не правило; обязательность возникает только после явного
  решения человека.
- Статусы `proposed → in-review → accepted → implemented` и `rejected` дают
  управляемый lifecycle.
- Есть правило обратной трассируемости: Standard ссылается на Pattern, Pattern -
  на RFC, RFC - на Research/Observation.
- Локальный спок уже различает RFC по промптам и RFC по governance/standards.
- Документ явно описывает, когда RFC нужен, а когда нет.

Это хорошо совпадает с IETF/Rust/Python/Swift-практикой: proposal и feedback не
должны автоматически менять active behavior.

### 4.2 Что не закрыто текущим процессом

| Gap | Наблюдение | Последствие |
| --- | --- | --- |
| G-1 | В upstream-цепочке Хаба нет явной роли ADR. | Архитектурные решения оказываются в `Standard` или `docs/adr/` без общей карты связи с RFC/report. |
| G-2 | `analytics` и `report` не разведены как типы project evidence. | Анализ проблем, аудит и proposal могут смешиваться в одном документе. |
| G-3 | `canonical` не описан как отдельный lifecycle state для RFC/ADR. | Есть риск читать canonical как "accepted", хотя это разные вопросы: качество формы и решение по содержанию. |
| G-4 | Нет explicit standard initiation gate. | RFC/ADR могут восприниматься как достаточное основание для создания standard без проверки повторяемости. |
| G-5 | Нет BPMN/процессной визуализации переходов и возвратов. | Новому участнику трудно увидеть, где есть human gates и где возможен откат. |

### 4.3 Улучшения процесса (предложения, не решения)

1. Добавить в будущую ревизию RFC-процесса **artifact-chain map** как граф:
   `research/analytics/report/RFC/ADR/standard/artifact`, с явными возвратами.
2. Ввести entry criteria:
   - RFC: unresolved change proposal, needs feedback/approval.
   - ADR: accepted architecture decision requiring future context.
   - Standard: repeatable rule for creating/checking artifacts.
   - Artifact: concrete output; may be created directly when no reusable rule is
     needed.
3. Развести `canonical` и `accepted`:
   - `canonical` = документ приведён к принятому формату/месту хранения;
   - `accepted` = человек принял содержание;
   - `implemented` = изменения внесены в PR/артефакт.
4. Зафиксировать rule: RFC/ADR могут **инициировать** standard, но standard
   проходит отдельный proposal/review/validation gate.
5. Для крупных RFC разрешить отдельный файл в `governance/rfc/`, а
   `governance/rfc-register.md` оставить single source of status.
6. Для lightweight feedback разрешить issue/PR label или `[RFC]`-черновик без
   перевода в формальный RFC до появления достаточного scope.

## 5. BPMN-диаграммы процессов

Диаграммы ниже записаны в Mermaid как BPMN-like представление: круги = события,
прямоугольники = задачи, ромбы = gateways, жирные переходы подразумевают human
decision gate. Это не внедряет новый процесс; это визуализация гипотезы и
предложенных уточнений.

### 5.1 Основная цепочка артефактов

```mermaid
flowchart TD
    start((Start: source signal))
    hub_research[Hub research: global practice]
    analytics[Project analytics: local problem/opportunity analysis]
    report[Report: audit, statistics, evidence package]
    decision_need{Decision or change needed?}
    product_change{What kind of decision?}
    rfc[Draft RFC: what should change?]
    adr[Draft ADR: how should architecture be built?]
    extra_research{More evidence needed?}
    review[Review and human decision gate]
    canonical[Canonical RFC/ADR record]
    reusable_rule{Repeatable rule needed?}
    standard[Draft standard: rules for future artifacts]
    artifact[Create or update artifact]
    archive((Archive / no change))
    end((End: traceable artifact or rejected proposal))

    start --> hub_research
    hub_research --> analytics
    analytics --> report
    report --> decision_need
    decision_need -- no --> archive
    decision_need -- yes --> product_change
    product_change -- product/project change --> rfc
    product_change -- architecture decision --> adr
    rfc --> extra_research
    adr --> extra_research
    extra_research -- yes --> analytics
    extra_research -- no --> review
    review -- rejected/deferred --> archive
    review -- accepted --> canonical
    canonical --> reusable_rule
    reusable_rule -- yes --> standard
    reusable_rule -- no --> artifact
    standard --> artifact
    artifact --> end
```

### 5.2 Процесс RFC

```mermaid
flowchart TD
    start((Start: research task or issue signal))
    analyze[Analyze evidence and affected artifacts]
    draft[Draft RFC: context, proposal, impact, open questions]
    triage{Is RFC the right artifact?}
    to_adr[Route to ADR if decision is already architectural]
    to_analysis[Return to analytics if evidence is insufficient]
    review[Community / founder review]
    decision{Human decision}
    rejected[Record rejected/deferred with reason]
    accepted[Mark RFC accepted]
    canonical[Canonical RFC entry + register status]
    route{Implementation route}
    adr[Create or update ADR if architecture decision is needed]
    standard[Initiate standard proposal if repeatable rule is needed]
    artifact[Implement artifact change in PR]
    end((End))

    start --> analyze --> draft --> triage
    triage -- no: architecture record --> to_adr --> end
    triage -- no: more evidence --> to_analysis --> analyze
    triage -- yes --> review --> decision
    decision -- reject/defer --> rejected --> end
    decision -- accept --> accepted --> canonical --> route
    route -- architecture implications --> adr --> end
    route -- repeatable rule --> standard --> end
    route -- concrete change --> artifact --> end
```

### 5.3 Процесс ADR

```mermaid
flowchart TD
    start((Start: architecture pressure or accepted RFC))
    context[Capture context and architecturally significant requirement]
    options[Compare options and trade-offs]
    draft[Draft ADR: context, decision, status, consequences]
    unresolved{Is product/project scope unresolved?}
    rfc[Open RFC for what should change]
    review[Architecture / founder review]
    decision{Human decision}
    superseded[Mark rejected, deprecated, or superseded]
    accepted[Mark ADR accepted]
    canonical[Canonical ADR in docs/adr]
    reusable_rule{Does decision imply repeatable artifact rules?}
    standard[Initiate standard proposal]
    artifact[Guide artifact implementation]
    end((End))

    start --> context --> options --> draft --> unresolved
    unresolved -- yes --> rfc --> end
    unresolved -- no --> review --> decision
    decision -- reject/supersede --> superseded --> end
    decision -- accept --> accepted --> canonical --> reusable_rule
    reusable_rule -- yes --> standard --> end
    reusable_rule -- no --> artifact --> end
```

### 5.4 Процесс согласования

```mermaid
flowchart TD
    start((Start: draft RFC/ADR/standard))
    intake[Register draft and source links]
    review_roles[Sequential review: methodology architect, BA expert, AI engineer]
    issues{Blocking issues found?}
    revise[Revise draft and preserve history]
    founder_gate{Founder / human decision}
    accepted[Accepted: update status and canonical record]
    rejected[Rejected: record reason and keep trace]
    deferred[Deferred: define missing evidence or owner]
    implemented[Implemented later by scoped PR]
    end((End))

    start --> intake --> review_roles --> issues
    issues -- yes --> revise --> review_roles
    issues -- no --> founder_gate
    founder_gate -- accept --> accepted --> implemented --> end
    founder_gate -- reject --> rejected --> end
    founder_gate -- defer --> deferred --> end
```

## 6. Ответы на вопросы

### 6.1 Могут ли ADR или RFC инициировать standard напрямую?

Да, **инициировать** могут. Нет, **активировать standard напрямую** не должны.

Правильная формула для Mango:

```text
accepted RFC/ADR → standard proposal → review/validation → standard
```

Обоснование:

- RFC/ADR дают rationale и decision context.
- Standard создаёт повторяемое L3-правило для будущих артефактов.
- ISO/IEEE/W3C показывают, что standard требует отдельной проверки need,
  consensus, applicability и maturity.
- Текущий `executable-contract-standard` уже защищает L1 от прямой L3-загрузки;
  поэтому standard должен быть L3 management artifact, а не shortcut в runtime.

### 6.2 Как текущий RFC-процесс соотносится с гипотезой?

Текущий процесс покрывает середину цепочки: `Research/Hypothesis → RFC →
Pattern/Standard`. Он хорошо фиксирует статус RFC и human gate, но не описывает:

- различие `analytics` vs `report`;
- роль ADR как отдельного decision record;
- переходы RFC ↔ ADR;
- standard initiation gate;
- статус `canonical` отдельно от `accepted`;
- BPMN-карту возвратов.

Следовательно, гипотеза не отменяет текущий процесс, а расширяет его в сторону
полного artifact lifecycle.

### 6.3 Какие международные практики применимы?

Применимы частично, без механического копирования:

- ADR по Nygard/ADR community - для короткой записи значимого решения и
  consequences.
- RFC/PEP/Swift/Kubernetes/LLVM - для proposal, feedback, review, accepted/rejected
  resolution и incremental implementation.
- ISO/IEEE/W3C - для maturity gate standards: proposal, review, consensus,
  publication, revision/superseding.
- Linux `[RFC PATCH]` - как пример lightweight early feedback, если формальный
  RFC слишком тяжёлый.

## 7. Дополнительные предложения

### 7.1 Предложения к будущей методологии

1. Описать artifact lifecycle как **граф**, а не цепочку.
2. Ввести decision table "какой артефакт создавать":
   - факты/исследование → `docs/analysis/*`;
   - открытое изменение → RFC;
   - принятое архитектурное решение → ADR;
   - повторяемое правило → standard;
   - конкретный результат → artifact.
3. Добавить minimal frontmatter для traceability:
   `source_signal`, `based_on`, `status`, `decision_owner`, `supersedes`.
4. Для standard добавить отдельный checklist:
   need confirmed, scope stable, affected artifacts known, validation possible,
   human approval captured.
5. Для RFC/ADR не смешивать discussion и decision:
   RFC хранит proposal and feedback; ADR хранит accepted architecture decision.

### 7.2 Нужны ли отдельные research-документы?

В рамках issue #225 отдельные research-документы **не инициированы**, потому что
ключевые вопросы закрыты на уровне, достаточном для основного отчёта. Потенциальные
следующие исследования можно создать отдельными задачами, если Фаундер захочет
углубить методологию:

| Кандидат | Скоуп | Зачем |
| --- | --- | --- |
| `docs/analysis/adr-practices-research.md` | Подробное сравнение ADR-шаблонов: Nygard, MADR, GitHub/GitLab/GOV.UK. | Нужен перед созданием локального ADR-standard. |
| `docs/analysis/rfc-vs-adr-comparison.md` | Decision table RFC vs ADR vs design doc vs proposal. | Нужен перед изменением `governance/rfc-process.md`. |
| `docs/analysis/standard-creation-process-research.md` | ISO/IEEE/W3C/OASIS-style maturity gates для локальных L3 standards. | Нужен перед созданием локального standard-creation process. |

Эти документы не создаются сейчас, чтобы не раздувать scope research-задачи и не
внедрять процессы без отдельного approval.

## 8. Заключение

Гипотеза Фаундера подтверждается как полезная методологическая основа, если читать
её не как линейный conveyor, а как граф артефактов с явными decision gates:

- `research/analytics/report` создают evidence;
- RFC обсуждает изменение и собирает решение;
- ADR фиксирует принятое архитектурное решение;
- standard кодифицирует повторяемое правило только после отдельного maturity-gate;
- artifact является конечным продуктом или конкретным результатом, но не всегда
  требует отдельного standard.

Главная рекомендация для будущей работы: расширять текущий RFC-процесс не через
новые обязательные документы для каждого случая, а через entry criteria, явные
переходы RFC ↔ ADR, отдельный standard-gate и BPMN-карту возвратов.

## Источники

Внутренние:

- Issue #225: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/225>
- RFC-процесс Mango: [`governance/rfc-process.md`](../../governance/rfc-process.md)
- Стандарт нейминга артефактов: [`standards/artifact-naming-standard.md`](../../standards/artifact-naming-standard.md)
- Стандарт исполнимых контрактов: [`standards/executable-contract-standard.md`](../../standards/executable-contract-standard.md)
- Анализ проблем контрактов и RFC: [`docs/analysis/executable-contracts-and-rfc-problems.md`](executable-contracts-and-rfc-problems.md)
- Contributing: [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

Внешние:

- Michael Nygard, Documenting Architecture Decisions: <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- ADR community: <https://adr.github.io/>
- GitHub Engineering, Why Write ADRs: <https://github.blog/engineering/architecture-optimization/why-write-adrs/>
- GitLab Architecture Design Documents: <https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/>
- GitLab Design Decisions: <https://docs.gitlab.com/charts/architecture/decisions/>
- GOV.UK Design System Architecture, Use RFCs and ADRs: <https://github.com/alphagov/govuk-design-system-architecture/blob/main/proposals/001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions.md>
- IETF RFC 2026: <https://datatracker.ietf.org/doc/html/rfc2026>
- IETF About RFCs: <https://www.ietf.org/process/rfcs/>
- Rust RFCs: <https://github.com/rust-lang/rfcs>
- Python PEP 1: <https://peps.python.org/pep-0001/>
- Swift Evolution Process: <https://github.com/swiftlang/swift-evolution/blob/main/process.md>
- Kubernetes KEP Process: <https://github.com/kubernetes/enhancements/blob/master/keps/sig-architecture/0000-kep-process/README.md>
- LLVM RFC Process: <https://llvm.org/docs/RFCProcess.html>
- Linux Kernel Submitting Patches: <https://docs.kernel.org/process/submitting-patches.html>
- ISO stages and resources for standards development: <https://www.iso.org/stages-and-resources-for-standards-development.html>
- IEEE SA Developing Standards: <https://standards.ieee.org/develop/>
- W3C Process Document: <https://www.w3.org/policies/process/>
