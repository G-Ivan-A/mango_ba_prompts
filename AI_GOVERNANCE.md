---
status: draft
version: 0.2
updated: 2026-06-10
ai-generated: true
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_GOVERNANCE.md"
source_sha: "117e4a553815af9b05d841c81dd725dd4a4c4d44"
---

# AI Governance — mango_ba_prompts

Операционный контракт для AI-assisted work в HTOM-команде `mango_ba_prompts`
(HTOM = Hybrid Team Operating Model: гибридная работа человека и ИИ-агентов).

Этот файл — **ядро генома** HTOM-команды: обязателен в корне (жёсткое
ограничение). Он определяет, кто принимает решения, что делает ИИ и где проходят
границы. HTOM-команда наследует правила Хаба и при конфликте ссылается на
источник истины:
[hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab)
(Хаб `hybrid-Intelligence-lab`, документ `AI_GOVERNANCE.md`). Команда не дублирует
знания Хаба, а ссылается на них.

## Роли

| Роль | Ответственность |
| --- | --- |
| Founder & PO | Vision, priorities, publication boundaries и финальные решения по проекту. |
| Human reviewer | Проверяет структуру, источники, риски и полезность до merge или публикации. |
| Contributor | Создаёт issues, artifacts и pull requests внутри модели проекта. |
| AI agent | Готовит черновики, проверки и summaries внутри scope issue и правил этого контракта. |

## Правила

1. Работа начинается с issue или явного maintainer request.
2. AI agents читают issue, последние comments, relevant files и текущий PR
   context до изменения файлов.
3. AI agents могут предлагать структуру, но humans принимают финальные решения
   по vision, publication, license и sensitive context.
4. Claims, влияющие на решения, связываются с sources, experiments, issues, PRs
   или ADR в `docs/adr/`.
5. Secrets, private client data, credentials и несанитизированные
   production-промпты не коммитятся.
6. Малые reviewable pull requests предпочтительнее широких undocumented rewrites.
7. Структура HTOM-команды не растёт «на вырост»: новый каталог создаётся только
   при доказанной операционной боли (Anti-Inflation principle Хаба).

## Capability Boundaries

Простая taxonomy границ для AI-агента — конкретная инстанциация хабовой рубрики
«Границы действий» под mango (с реальными путями репозитория). При сомнении —
действует [fail-closed semantics](AI_QUICK_RULES.md#fail-closed-semantics-критично).

**Можно делать без human review:**

- Читать файлы репозитория.
- Создавать черновики промптов в `prompts/drafts/`.
- Предлагать изменения структуры через issues.

**Требует human review:**

- Изменять существующие промпты в `prompts/`.
- Создавать новые папки.
- Обновлять `AI_GOVERNANCE.md` или `AI_QUICK_RULES.md`.

**Никогда не делать:**

- Публиковать secrets или credentials.
- Удалять файлы без явного разрешения.
- Изменять `standards/GLOSSARY.md` без согласования с Хабом.

## Эскалация

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу или правилу Хаба;
- изменение публикует sensitive или private information;
- от HTOM-команды требуют создать `research/` или иной «выключенный ген» по
  умолчанию (см. `AI_QUICK_RULES.md`): назови правило и его источник, предложи
  легитимную альтернативу, а осознанное отклонение зафиксируй как ADR в
  `docs/adr/`;
- AI agent не может проверить важное claim или migration decision.

## Operating Modes

| Mode | Когда использовать |
| --- | --- |
| Structured | По умолчанию для структуры проекта, governance и tooling. |
| Research | Для source-backed analysis (фундаментальные знания — вкладом в `research/` Хаба, а не в команду). |
| Project | Для prompt, process и knowledge-base context этой HTOM-команды. |

## Definition of Done

Для AI-assisted изменений в HTOM-команде:

- активные файлы находятся в ожидаемых каталогах;
- навигация и ссылки на Хаб обновлены;
- значимое изменение отражено в `CHANGELOG.md` (`## Unreleased`);
- структура соответствует целевой из `docs/audit/initial-state-2026-06.md`;
- PR description объясняет implementation, validation и remaining risks.
