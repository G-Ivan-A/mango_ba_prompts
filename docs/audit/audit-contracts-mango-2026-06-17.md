---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: audit
scope: governance
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/audit/audit-hub-2026-06-17.md"
  - "pr-ops/sync-matrix-2026-06-17.md"
  - "docs/rfc/rfc-process.md"
  - "pr-ops/artifact-map.md"
---

# Аудит контрактов mango_ba_prompts (2026-06-17)

> **Повод.** Задача [#105](https://github.com/G-Ivan-A/mango_ba_prompts/issues/105) —
> синхронизация контрактов `mango_ba_prompts` со стратегическим Хабом
> [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab).
> Этот документ закрывает **ФТ-1**: фиксирует полный список контрактов спока после
> PR #98 и для каждого определяет, локальный он или потенциально глобальный,
> отличается ли от Хаба и нужна ли синхронизация. Результаты сводятся в
> [`pr-ops/sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md); аудит самого
> Хаба — в [`docs/audit/audit-hub-2026-06-17.md`](audit-hub-2026-06-17.md).
>
> **Важно (разделение задач).** Этот аудит — про **контент и процессы** (ADR,
> стандарты, governance). Физическая структура репозитория (директории,
> переименования, dev/prod) — отдельная задача (Migration Plan, Хаб PR #244).
> Здесь структура не меняется.

## Метод

1. Перечислены **все** активные контракты спока: ADR #003–#010 (серия PR #98),
   стандарты в `standards/`, governance-документы в корне и `governance/`.
2. Для каждого контракта зафиксированы: описание, тип, область применения
   (локальный / глобальный / частично), отличие от Хаба (да / нет / неизвестно),
   потребность в синхронизации (да / нет / частично) и обоснование.
3. Колонка «Отличается от Хаба» опирается на
   [`audit-hub-2026-06-17.md`](audit-hub-2026-06-17.md): если в Хабе нет аналога —
   «нет аналога»; если есть — отмечено, в чём вероятное расхождение.

**Условные обозначения области применения.**
- **Локальный** — имеет смысл только внутри Mango (привязан к продукту,
  конкретным числам, реестрам, командам).
- **Глобальный** — модель/правило переносимо в другие БА-проекты без Mango-специфики.
- **Частично** — универсальный каркас + локальное наполнение.

---

## 1. ADR #003–#010 (онтология БА и стандарты, PR #98)

> Нумерация ADR в репозитории двойная: трёхзначная серия (`003`–`010`) — это
> онтология БА из PR #98 (предмет этого аудита); четырёхзначная (`0001`–`0003`) —
> hub-sync серия (PR #208 и др.), вне scope ФТ-1.

| ADR | Тема | Тип | Область | Отличается от Хаба | Синхронизация | Обоснование |
| --- | --- | --- | --- | --- | --- | --- |
| [#003](../adr/003-ba-ontology.md) | Онтология БА (Артефакт↔Процесс↔Операция), граф, 8 состояний ЖЦ | ADR | Глобальный (модель) + локальный (реестр 30 артефактов) | Нет аналога в Хабе | **Передача знаний** | Уникальная практика Mango; кандидат на RFC в Хаб (ФТ-5). |
| [#004](../adr/004-operations-taxonomy.md) | Таксономия 13 операций, маппинг BABOK/ISO 29148, профиль аудита | ADR | Глобальный | Нет аналога; пересекается с PR #246 (методологии) | **Частично** (свериться с PR #246) | Маппинг на BABOK универсален; уникальный набор 13 операций — кандидат на передачу знаний. |
| [#005](../adr/005-artifact-team-naming.md) | Нейминг артефактов/документов + Team Directory | ADR | Частично (схема глобальна, реестр кодов и команды локальны) | Да — Хаб: [`standards/file-naming.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/file-naming.md) (про файлы), Mango — про ID артефактов | **Частично** (свериться с file-naming) | Разные предметы: file-naming Хаба — про имена файлов, ADR #005 — про ID артефактов БА. Сверить нейминг файлов-стандартов. |
| [#006](../adr/006-prompt-naming.md) | Нейминг промптов `[домен]-[операция]-[режим].md` | ADR | Глобальный | Нет прямого аналога; родственно `file-naming.md` | **Нет** (локальная конвенция промптов) | Схема промптов специфична для библиотеки промптов; в Хабе нет реестра промптов БА. |
| [#007](../adr/007-kb-standard.md) | Стандарт БЗ (pre-RAG), формат цитирования, синхронизация с глоссарием | ADR | Глобальный (формат) + локальный (структура `kb/`) | Частично — пересекается с PR #242 (Research Memory) и `external-knowledge-integration.md` | **Частично** (свериться с PR #242) | Формат цитирования и pre-RAG универсальны; модель Knowledge Object из Хаба может обогатить ADR #007 — кандидат на RFC. |
| [#008](../adr/008-industry-standards-standard.md) | Отраслевые стандарты: терминология, верификация источников, реестр | ADR | Глобальный (правила) + локальный (реестр источников) | Частично — Хаб: `external-knowledge-integration.md`, `research-memory` (Tier 1) | **Частично** (свериться) | Tier-1/Tier-2 модель Хаба и реестр Mango концептуально совместимы; согласовать терминологию tier. |
| [#009](../adr/009-bcreq-formation-process.md) | Процесс формирования BCREQ: 6 подпроцессов, 3 human gate | ADR | Частично (каркас глобален, числа/операции локальны) | Нет аналога в Хабе | **Передача знаний** | Уникальная практика Mango; кандидат на RFC в Хаб (ФТ-5). |
| [#010](../adr/010-pages-ux.md) | UX GitHub Pages: дерево процессов, только узлы с промптами | ADR | Частично (архитектура данные/отображение глобальна) | Нет аналога в Хабе | **Передача знаний** | Уникальная практика Mango; кандидат на RFC в Хаб (ФТ-5). |

**Примечание по ADR #001/#002.** [`001-prompt-standard.md`](../adr/001-prompt-standard.md)
и [`002-pattern-standard.md`](../adr/002-pattern-standard.md) формализуют
стандарты промптов и паттернов (носители — `standards/prompt-standard.md`,
`standards/pattern-standard.md`). Не входят в перечень ФТ-1 (#003–#010), но
учтены в разделе 2 через свои стандарты-носители.

---

## 2. Стандарты (`standards/`)

| Стандарт | Носитель ADR | Тип | Область | Отличается от Хаба | Синхронизация | Обоснование |
| --- | --- | --- | --- | --- | --- | --- |
| [`ba-ontology.md`](../../standards/ba-ontology.md) | #003 | контракт-правило | Глобальный + локальный реестр | Нет аналога | **Передача знаний** | Носитель уникальной онтологии. |
| [`artifact-naming-standard.md`](../../standards/artifact-naming-standard.md) | #005 | контракт-правило | Частично | Да — Хаб `file-naming.md` (другой предмет) | **Частично** | Сверить нейминг файлов-стандартов (`*-standard.md`) с Хабом. |
| [`product-classification-contract.md`](../../standards/product-classification-contract.md) | — | контракт (внешний источник) | **Локальный** (явно: «только Mango») | Нет аналога | **Нет** | Иерархия Domain→Capability→Feature→Atomic Function привязана к продукту Mango. |
| [`kb-standard.md`](../../standards/kb-standard.md) | #007 | контракт-правило | Глобальный + локальный | Частично — PR #242 (Research Memory) | **Частично** | См. ADR #007. |
| [`industry-standards-standard.md`](../../standards/industry-standards-standard.md) | #008 | контракт-правило | Глобальный + локальный реестр | Частично — `external-knowledge-integration.md` | **Частично** | Согласовать tier-модель с Хабом. |
| [`bcreq-process-standard.md`](../../standards/bcreq-process-standard.md) | #009 | процесс | Частично | Нет аналога | **Передача знаний** | Носитель уникального процесса BCREQ. |
| [`pages-ux-standard.md`](../../standards/pages-ux-standard.md) | #010 | UX-стандарт | Частично | Нет аналога | **Передача знаний** | Носитель уникального UX. |
| [`prompt-standard.md`](../../standards/prompt-standard.md) | #001 | контракт-правило | Глобальный | Частично — Хаб `executable-contract-standard.md` (про `executable: true`) | **Частично** (свериться) | Frontmatter и ЖЦ промптов универсальны; сверить с моделью исполнимых контрактов Хаба. |
| [`pattern-standard.md`](../../standards/pattern-standard.md) | #002 | контракт-правило | Глобальный | Частично — Хаб `executable-documentation-standard.md` (атомизация практик) | **Частично** (свериться) | 8 полей паттерна универсальны; сверить с graph-of-practices Хаба. |
| [`GLOSSARY.md`](../../standards/GLOSSARY.md) | — | глоссарий (копия Хаба) | Глобальный (артефакт Хаба) | Да — копия Хаба `standards/glossary.md` v1.0, Хаб уже 56+ терминов | **Да** (Smart Sync из Хаба) | Источник истины — Хаб; локальная копия синхронизируется явным действием. |
| [`experiment-log-standard.md`](../../standards/experiment-log-standard.md) | — | правило фиксации | **Локальный** | Нет аналога | **Нет** | Двухуровневая фиксация прогонов промптов специфична для операционной модели Mango. |
| [`team-directory.md`](../../standards/team-directory.md) | #005 | реестр | **Локальный** | Нет аналога | **Нет** | Реестр из ровно 2 команд (BCREQ, CCMO) — оргструктура Mango. |

---

## 3. Governance и корневые контракты

| Документ | Тип | Область | Отличается от Хаба | Синхронизация | Обоснование |
| --- | --- | --- | --- | --- | --- |
| [`AI_GOVERNANCE.md`](../../AI_GOVERNANCE.md) | контракт/политика | Локальный (наследует Хаб) | Да — Хаб `AI_GOVERNANCE.md` canonical, локальная адаптация под Mango | **Частично** (осознанная адаптация) | Локализует роли/границы под структуру Mango; синхронизируется как HTOM-контракт через Smart Sync. |
| [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | политика/guideline | Локальный | Да — Хаб `CONTRIBUTING.md` | **Частично** | Workflow вклада адаптирован; «Временный workflow промптов» — локальный. |
| [`AI_QUICK_RULES.md`](../../AI_QUICK_RULES.md) | исполнимые правила | Локальный | Да — HTOM-геном Хаба | **Частично** (Smart Sync) | Короткая инструкция агента; часть HTOM-генома. |
| [`AI_SESSION_HANDOVER_PROMPT.md`](../../AI_SESSION_HANDOVER_PROMPT.md) | исполнимый контракт | Локальный | Да — Хаб `session-handover-standard.md` + геном | **Частично** (Smart Sync) | Передача контекста; синхронизирован в issue #72. |
| [`pr-ops/artifact-map.md`](../../pr-ops/artifact-map.md) | навигация | Локальный (адаптация Хаба) | Да — Хаб `pr-ops/artifact-map.md` | **Частично** (Smart Sync) | Уже синхронизирован (см. `source_hub` в frontmatter). |
| [`.archive/ai-rules/agent-onboarding-protocol_old.md`](../../.archive/ai-rules/agent-onboarding-protocol_old.md) | исполнимый контракт | Локальный | Да — Хаб одноимённый эталон | **Частично** (Smart Sync) | Эталон исполнимого контракта Хаба, адаптирован. |
| [`standards/prompt-debugging-process.md`](../../standards/prompt-debugging-process.md) | процесс | **Локальный** | Нет аналога | **Передача знаний** | Создан в issue #101; уникальный — кандидат на RFC в Хаб (ФТ-4/ФТ-5). |
| [`docs/rfc/rfc-register.md`](../rfc/rfc-register.md) | реестр | Локальный | Частично — Хаб `knowledge-lifecycle-proposal.md` (lifecycle) | **Частично** (интеграция) | Реестр RFC привязывается к lifecycle Хаба (см. `rfc-process.md`). |
| [`docs/audit/audit-contracts-2026-06-17.md`](audit-contracts-2026-06-17.md) | аудит | Локальный | — | **Нет** | Аудит по issue #101 (отладка промптов), исторический. |
| [`pr-ops/BACKLOG.md`](../../pr-ops/BACKLOG.md) | трекер | Локальный | Да — Хаб `governance/backlog.md` | **Частично** (Smart Sync) | Локальные открытые вопросы; формат из Хаба. |
| [`pr-ops/migration-manifest.md`](../../pr-ops/migration-manifest.md), [`migration-phase1-issues.md`](../../pr-ops/migration-phase1-issues.md), [`migration-issues-registry.md`](../../pr-ops/migration-issues-registry.md) | миграция | Локальный | — | **Нет** | Снимки миграции из Хаба; исторический контекст. |
| [`pr-ops/session-digests.md`](../../pr-ops/session-digests.md) | журнал | Локальный | Да — механизм из Хаба | **Частично** (Smart Sync) | Механизм session-digest синхронизирован из Хаба. |
| [`.hub-profile.json`](../../.hub-profile.json) | профиль синхронизации | Локальный | Да — формат Smart Sync Хаба (PR #208) | **Частично** | Профиль для Smart Sync; обязан соответствовать формату Хаба. |

---

## 4. Сводка

| Категория | Кол-во | Что делать |
| --- | --- | --- |
| **Локальные (не синхронизировать)** | product-classification-contract, experiment-log-standard, team-directory, audit-* | Оставить локальными; не дублировать в Хаб. |
| **Передача знаний → Хаб (ФТ-5)** | ADR #003 (онтология), #009 (BCREQ), #010 (Pages UX), prompt-debugging-process | Подготовить документы передачи знаний + RFC в Хаб. |
| **Частичная сверка с Хабом** | ADR #004, #005, #007, #008, prompt-standard, pattern-standard, industry-standards | Сверить, при расхождении — **RFC, не прямая правка**. |
| **Smart Sync из Хаба** | GLOSSARY, AI_GOVERNANCE, CONTRIBUTING, artifact-map, AI_QUICK_RULES, handover, BACKLOG, session-digests, .hub-profile | Источник истины — Хаб; обновлять осознанным Smart Sync. |
| **Интеграция процесса Хаба** | rfc-register → lifecycle Хаба | См. [`rfc-process.md`](../rfc/rfc-process.md). |

## 5. Вывод

После PR #98 спок имеет **8 ADR онтологии** (#003–#010), **12 стандартов** и
**13 governance-контрактов**. Три класса контрактов:

1. **Уникальные практики Mango** (онтология БА, таксономия операций, процесс
   BCREQ, UX GitHub Pages, процесс отладки промптов) — в Хабе аналогов нет; они
   составляют **обратный поток знаний** (спок → Хаб, ФТ-5).
2. **Контракты, пересекающиеся с RFC Хаба** (БЗ ↔ Research Memory, отраслевые
   стандарты ↔ external-knowledge, нейминг ↔ file-naming, промпты/паттерны ↔
   executable-* ) — требуют **сверки и, при расхождении, RFC** (не прямой правки).
3. **Контракты, синхронизируемые из Хаба** (глоссарий, governance-геном) —
   источник истины Хаб, обновляются Smart Sync.

Ни один контракт не требует немедленной правки в рамках этой задачи: расхождения
оформляются как RFC (см. [`rfc-process.md`](../rfc/rfc-process.md) и
[`sync-matrix-2026-06-17.md`](../../pr-ops/sync-matrix-2026-06-17.md)).
