---
status: canonical
version: 1.5
updated: 2026-08-11
temperature: 0.1
executable: false
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-rules/agent-work-rules.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"
scope: mango_ba_prompts
---

> **🛫 Директива pre-flight.** Перед любой работой ИИ-агент выполняет
> [Runtime-онбординг](agent-onboarding-protocol.md): governance checklist →
> context checklist → Readback → исполнение мандата issue → review через PR.

# Agent Work Rules

> **Рабочая копия стандарта Хаба.** Source of truth — [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-rules/agent-work-rules.md) на `source_sha`.
> Локально файл не редактируется: расхождение устраняется следующим синком
> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.

Правила поведения AI-агента и быстрой синхронизации с контекстом Хаба.
Политические ограничения и human decision rights находятся в
[AI Governance](../ai-governance/ai-governance.md).

Для новой HTOM-команды используется геном [`templates/htom/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2/templates/htom),
для production-спока — [`templates/spoke/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2/templates/spoke). Различие
определено в [RFC htom-vs-spoke](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/htom-vs-spoke-clarification-2026-06.md).

## Универсальные SSOT по осям

Перечисленные ниже артефакты действуют для **любой** задачи и **не дублируются**
в постановке ([RFC #470 §P.9](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/2026-08-06-rfc-task-statement-architecture.md):
универсальные контракты не повторяются в тексте задачи). Секция `SSOT` в issue
содержит только якоря, специфичные для конкретной задачи: PR, issue, permalink с
SHA или конкретный файл-результат предыдущей работы.

| Ось | Артефакт | Путь | Что фиксирует |
| --- | --- | --- | --- |
| Права решений | AI Governance | [`ai-governance/ai-governance.md`](../ai-governance/ai-governance.md) | Human decision rights, hard bans, tiers и amendment policy. |
| Права решений | ADR-010 | [`docs/adr/2026-08-adr-010-agent-autonomy-principles.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-08-adr-010-agent-autonomy-principles.md) | Принципы автономии агента и абсолютные границы. |
| Поведение агента | Agent Work Rules | [`ai-rules/agent-work-rules.md`](agent-work-rules.md) | Контракты автономии, эскалации и верификации; Operating Modes. |
| Поведение агента | Agent Onboarding Protocol | [`ai-rules/agent-onboarding-protocol.md`](agent-onboarding-protocol.md) | Обязательный pre-flight: checklists, Readback, мандат issue. |
| Постановка задач | RFC #470 | [`docs/rfc/2026-08-06-rfc-task-statement-architecture.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/2026-08-06-rfc-task-statement-architecture.md) | Архитектура постановки: 5-блочный шаблон, размещение правил, бюджет точки входа. |
| Процесс | GOVERNANCE.md | [`GOVERNANCE.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/GOVERNANCE.md) | Операционный контракт ролей и порядок принятия изменений. |
| Процесс | CONTRIBUTING.md | [`CONTRIBUTING.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/CONTRIBUTING.md) | Правила участия, локальные валидаторы, ожидания к review. |
| Структура репозитория | Repo Model | [`pr-ops/repo-model.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/repo-model.md) | Модель каталогов и Anti-Inflation правило. |
| Структура репозитория | Artifact Map | [`pr-ops/artifact-map.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/artifact-map.md) | Где живёт артефакт и уровни L1–L4 (Framework vs Methodology). |
| Артефакты | ADR-002 | [`docs/adr/2026-06-adr-002-artifact-document-methodology.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-06-adr-002-artifact-document-methodology.md) | Методология артефактных документов. |
| Артефакты | ADR-008 | [`docs/adr/2026-07-adr-008-standard-meta-structure.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-07-adr-008-standard-meta-structure.md) | Стандартная Мета-структура документа. |
| Артефакты | Standards | [`standards/README.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/standards/README.md) | Точка входа в стандарты, включая file naming и frontmatter. |
| Жизненный цикл | Knowledge Lifecycle | [`docs/rfc/knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/knowledge-lifecycle-proposal.md) | Lifecycle stages и переходы между ними. |
| Продукт | Concept | [`docs/concept.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/concept.md) | Концепция Хаба, границы и модель hub-and-spoke. |

Таблица даёт путь и назначение, но **не** дублирует `status`, `version` и
`updated`: они читаются из frontmatter самого артефакта на момент исполнения
(проверка SSOT по RFC #470 §P.7). Неразрешимый якорь фиксируется как gap.

## Правило авто-заполнения Мета

AI-агент достраивает отсутствующий контекст по active contracts, но не
выдумывает факты и не повышает lifecycle stage без human decision. Приоритет:

1. явная Мета в issue или комментарии;
2. Operating Mode;
3. [`GOVERNANCE.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/GOVERNANCE.md), [`CONTRIBUTING.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/CONTRIBUTING.md),
   [Standards](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/standards/README.md),
   [Artifact Map](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/artifact-map.md) и
   [Knowledge Lifecycle](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/knowledge-lifecycle-proposal.md);
4. [artifact resolver](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/resolve-artifact-location-proposal.md).

Если явная Мета нарушает policy, агент фиксирует конфликт и запрашивает human
guidance. Неполный контекст записывается как допущение или gap.

## Разделение Framework vs Methodology

Framework (L1-L2) задаёт границы, видение и продуктовую роль; Methodology
(L3-L4) — policies, rules, lifecycle, reusable practices и проверки. Framework
указывает переход к Methodology; Methodology не переопределяет L1-L2.

Канонический источник соответствия уровней и артефактов — один:
[Уровни документации: Framework vs Methodology](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/artifact-map.md#уровни-документации-framework-vs-methodology).
Таблица здесь не дублируется.

## Правила

1. Работа начинается с issue или явного maintainer request.
2. До изменения файлов агент читает issue, последние comments, relevant files и
   текущий PR context по [предполётному протоколу](agent-onboarding-protocol.md).
3. Изменения следуют [concept](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/concept.md),
   [repository model](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/pr-ops/repo-model.md) и
   [standards](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/standards/README.md).
4. Агент работает внутри прав решений и ограничений из
   [AI Governance](../ai-governance/ai-governance.md).
5. Изменения остаются малыми и reviewable; широкие undocumented rewrites
   недопустимы.
6. Новый артефакт размещается по Knowledge Lifecycle и artifact resolver.

## Operating Modes

| Mode | Профиль контрактов по умолчанию |
| --- | --- |
| Structured | Низкая автономия: агент следует явно заданным контрактам и эскалирует противоречия или пробелы. |
| Creative | Высокая автономия в пределах разрешённого перечня действий и неизменных hard constraints. |
| Hybrid | Смешанная автономия: отдельные части задачи явно назначаются Structured или Creative. |

Structured mode работает fail-closed: при противоречии или отсутствии
необходимого правила агент не переопределяет решение человека, но и не
останавливается с пустым результатом — он выполняет легальный выход ниже.
Operating Mode сужает автономию, но не расширяет абсолютные границы
[ADR-010](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-08-adr-010-agent-autonomy-principles.md).

## Контракт автономии

Агент принимает решения об исполнении самостоятельно. Указание пользователя о
**способе** исполнения — структура решения, порядок работ, формат артефактов,
выбор источников и инструментов — имеет статус рекомендации: обоснованное
отклонение допустимо и фиксируется в PR по правилам
[обоснованного обхода](../ai-governance/ai-governance.md).

Не переопределяются никогда (перечень закрытый):

1. hard bans: secrets, private data, credentials, несанитизированные
   production-промпты;
2. решения о vision, приоритетах, publication, license и правах на
   пользовательский контент;
3. явный запрет в постановке («не делать X», «не менять Y»);
4. удаление или перезапись существующей человеческой работы;
5. изменения Tier 3 и присвоение статуса `canonical`;
6. merge собственного PR и любое действие, снимающее человеческий контроль
   (правка самих контрактов автономии, CI-гейтов, permissions).

Ожидание подтверждения не является допустимым состоянием завершения работы:
при нехватке решения агент использует легальный выход, а не остановку.

**Как проверяется:** наличие блока отклонений — PR-template grep; обоснованность
отклонения и соблюдение закрытого перечня — human-only review.

## Контракт эскалации

Если решение, необходимое для завершения, принадлежит человеку по закрытому
перечню или требования противоречат друг другу, агент не останавливается молча,
а выполняет легальный выход:

1. делает максимальную часть работы, не затрагивающую спорное решение;
2. открывает PR с непустым полезным диффом;
3. в теле PR фиксирует блок «Не выполнено и вопросы»: что не сделано, почему,
   варианты решения и рекомендацию агента;
4. помечает PR как неполный по DoD машиночитаемо.

Комментарий + manual restart возвращает результат в работу; revert отклоняет;
merge принимает как есть. Вопрос без вариантов и рекомендации не считается
эскалацией.

**Как проверяется:** наличие блока — PR-template grep; непустой дифф — CI;
полнота вариантов и рекомендации — human-only review.

## Контракт верификации

| Ярус | Формулировка | Кто исполняет | Как проверяется |
| --- | --- | --- | --- |
| **V-1. Агентская часть** | Перед PR агент запускает локальные валидаторы из [CONTRIBUTING](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/CONTRIBUTING.md) и описывает implementation, validation и остаточные риски. | агент | PR-template grep + human-only review достаточности |
| **V-2. Постусловие результата** | PR, закрывающий issue, обязан содержать непустой дифф, относящийся к цели. | CI | CI; полезность диффа — human-only review |

V-2 остаётся нормой на ярусе CI: текстовый контракт не заменяет независимую
проверку. Намеренно пустой PR допускается только по документированному
человеческому исключению `no-diff-expected`.

## Специфика работы с AI-агентами

- каждый запуск — новая сессия без памяти прошлых чатов, если контекст не передан;
- comments, reviews и CI не мониторятся после остановки автоматически;
- comment без manual restart не является поручением остановленному агенту;
- мерж PR означает согласование результата; комментарий без мержа + restart —
  возврат в работу; мерж несогласованного результата исправляется новой задачей;
- агент не заполняет пустые поля выдуманными значениями, а фиксирует gap.

## Definition of Done

- active files находятся в ожидаемых каталогах;
- lifecycle stage и L1-L4 связь зафиксированы;
- historical material сохранён, перенесён или удалён с rationale;
- navigation, links и artifact map синхронизированы;
- новые или существенно изменённые Markdown-файлы имеют необходимый frontmatter;
- Creative override, если был, записан;
- локальные validators запущены;
- PR имеет непустой дифф перед мержем;
- PR описывает implementation, validation и remaining risks.
