---
status: canonical
version: 2.2
updated: 2026-08-11
temperature: 0.1
executable: false
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/ai-governance.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"
scope: mango_ba_prompts
---

# AI Governance

> **Рабочая копия стандарта Хаба.** Source of truth — [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/ai-governance.md) на `source_sha`.
> Локально файл не редактируется: расхождение устраняется следующим синком
> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.

Политический контракт AI-assisted work в `hybrid-Intelligence-lab`.

> **Слоган Хаба (зафиксирован):** «Человек задаёт смысл, AI ускоряет путь — вместе по правилам».
> Человек отвечает за смысл, цели и решения, AI ускоряет путь к ним внутри
> правил. Слоган наследуется HTOM-командами через геном
> [`templates/htom/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2/templates/htom).

Хаб является источником рекомендаций, reusable governance-практик, стандартов и
шаблонов для ecosystem repositories. Он помогает downstream-командам принимать
решения, но не является механическим блокером их работы: локальная команда может
адаптировать рекомендацию под свой риск, зрелость и контекст, если решение явно
зафиксировано.

RFC в [`docs/rfc/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc) — рекомендации и proposals. Они становятся
обязательными только после human decision и переноса нормативной части в
canonical standard, policy, template или другой active artifact. Жизненный цикл
описан в [Knowledge Lifecycle proposal](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/knowledge-lifecycle-proposal.md),
а место нового артефакта выбирается через
[Resolve Artifact Location proposal](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/rfc/resolve-artifact-location-proposal.md).

## Роли и права решений

| Роль | Ответственность |
| --- | --- |
| Пользователь | Формирует vision, priorities, publication boundaries и финальные product/governance decisions. |
| Human reviewer | Проверяет структуру, источники, риски и полезность до merge или публикации. |
| Contributor | Создаёт issues, artifacts и pull requests внутри repository model. |
| AI agent | Готовит черновики, миграции, проверки и summaries внутри scope issue и governance policy. |

AI agents могут предлагать структуру, но humans принимают финальные решения по
vision, publication, license и sensitive context.

## Политики

1. Claims, влияющие на решения, связываются с sources, experiments, issues,
   PRs или historical migration records.
2. Secrets, private client data, credentials и несанитизированные
   production-промпты не коммитятся.
3. RFC не становится обязательной политикой без human decision и продвижения в
   active normative artifact.
4. Значимые изменения governance-практики или downstream-шаблона проходят human
   review и оформляются через применимый ADR/RFC или canonical standard.

Минимальный frontmatter для активных Markdown-артефактов задан
[стандартом frontmatter](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/standards/frontmatter-standard.md). Остальные
нормативные контракты перечислены в [Standards](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/standards/README.md).

## Amendment policy (3 tier)

Политика задаёт, какая церемония нужна для правки canonical governance-артефакта
(policy, standard, template, ADR/RFC, backlog, artifact map). Обоснование —
[анализ backlog and artifact change policy](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md)
(§3.4). Tier выбирается по **максимальному** признаку изменения: если правка
попадает хотя бы под один критерий более высокого tier, применяется он.

| Tier | Что покрывает | Процесс | Переход выше |
| --- | --- | --- | --- |
| **Tier 1: Mechanical** | Исполнение уже принятого решения: typo, frontmatter update, обновление ссылок и путей, changelog-запись, validator allowlist. | RFC не нужен. Agent выполняет ripple scan затронутых ссылок, вносит правку, запускает валидаторы, оформляет PR с описанием. Human review при merge. | Обнаружено изменение смысла, путь вне accepted structure или меняется semantics валидатора → Tier 2/3. |
| **Tier 2: Limited** | Уточнение правила внутри уже принятого контракта: формулировка, пример, локальное исключение. Затрагивает один раздел и не меняет структуру артефакта. | Lightweight RFC: короткое описание изменения + rationale + список затронутых артефактов в теле PR (отдельный файл в `docs/rfc/` не обязателен). Обязателен human review. | Затронуто больше трёх active artifacts, добавляется новое поле frontmatter/status/тип артефакта, меняется routing или lifecycle → Tier 3. |
| **Tier 3: Structural** | Изменение смысла, новый раздел или каталог, изменение скелета, замена стандарта, удаление артефакта, сдвиг decision boundary. | Полный path: analysis → RFC/proposal → ADR/decision → standard/policy/template/validator → миграция. | Обхода нет: решение принимает человек. |

Правила применения:

1. Tier фиксируется в описании PR явно (`Tier 1` / `Tier 2` / `Tier 3`).
2. Сомнение между двумя tier разрешается в пользу более высокого.
3. Ни один tier не отменяет hard bans из раздела Политики и Эскалацию.
4. Обновление валидаторов входит в каждый tier, но само по себе не принимает
   governance decision.

Примеры: перенос ссылок после accepted ADR — Tier 1; добавление примера к
существующему правилу — Tier 2; введение нового типа артефакта или изменение
модели управления задачами — Tier 3.

## Обоснованное отклонение при экспертном исполнении

Экспертное исполнение действует во всех Operating Modes с разной шириной по
[Принципу 1 ADR-010](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-08-adr-010-agent-autonomy-principles.md):
Creative допускает широкое изменение способа исполнения, Structured — только
минимально необходимое, Hybrid задаёт границы по частям задачи. Обоснованное
отклонение допустимо, если:

1. не меняет цель задачи и соответствует её Operating Mode;
2. обход минимален;
3. не нарушены hard bans: secrets, private data, credentials,
   несанитизированные production-промпты, publication, license и права на
   пользовательский контент;
4. в PR, ADR/RFC или audit записаны rationale, изменённый артефакт и validation;
5. архитектурное или governance-изменение проходит human review.

Обход не отменяет политику Хаба для следующих задач, а создаёт traceable
precedent, который человек может принять, сузить или отклонить.

## Эскалация

Исчерпывающие абсолютные границы заданы как закрытый перечень из шести пунктов в
[Принципе 2 ADR-010](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-08-adr-010-agent-autonomy-principles.md).
При упоре в границу агент выполняет легальный выход из Agent Work Rules.

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу;
- изменение публикует sensitive или private information;
- нужен новый обязательный standard, но нет comparison;
- репозиторий смещается к production-code ownership;
- Creative override затрагивает hard bans, publication, license, security или
  права на пользовательский контент;
- AI agent не может проверить важное claim или migration decision.

Правила исполнения этой политики находятся в
[Agent Work Rules](../ai-rules/agent-work-rules.md).
