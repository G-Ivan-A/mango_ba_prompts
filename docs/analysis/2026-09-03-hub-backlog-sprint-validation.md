---
status: draft
version: 0.1
updated: 2026-09-03
temperature: 0.1
ai-generated: true
type: analysis
scope: hub-backlog-validation
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/357"
hub_backlog_ref: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/pr-ops/backlog.md"
hub_backlog_version: "1.53"
hub_backlog_instruction: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/pr-ops/backlog-instruction.md"
---

# Валидация активных спринтов бэклога Хаба (2026-09-03)

> ⚠️ **Это инвентаризация фактов, а не реализация.** Документ фиксирует
> фактическое состояние каждой задачи активного бэклога Хаба
> ([`pr-ops/backlog.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/pr-ops/backlog.md),
> `version: 1.53`, `updated: 2026-09-03`) на основании проверяемых артефактов
> экосистемы. Новых гипотез не вводится, состояние задач не додумывается:
> каждая строка вердикта подкреплена абсолютной ссылкой.

## 1. Назначение и границы

Задача [issue #357](https://github.com/G-Ivan-A/mango_ba_prompts/issues/357)
требует актуализировать бэклог Хаба: проверить фактическое состояние всех
активных спринтов, удалить завершённые и обновить статусы оставшихся задач.

**Ограничение исполнения (зафиксировано честно).** Файлы
`pr-ops/backlog.md`, `pr-ops/artifact-map.md` и `CHANGELOG.md` Хаба физически
живут в репозитории
[`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab),
а issue #357 и её PR открыты в спице
[`mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts). У
исполнителя нет права записи в репозиторий Хаба (`permissions.push = false`),
поэтому здесь фиксируется:

1. полный протокол валидации с доказательствами (раздел 3);
2. исполнимая дельта правок для `pr-ops/backlog.md` Хаба (раздел 4);
3. готовые тексты записей в `CHANGELOG.md` и `pr-ops/artifact-map.md` Хаба
   (раздел 5).

Применение дельты в Хабе — отдельное действие в репозитории Хаба; см. раздел 7
«Не выполнено и вопросы».

## 2. Метод проверки

Каждая задача проверена по трём независимым источникам, а не по тексту бэклога:

| Источник факта | Как проверялся |
| --- | --- |
| Состояние issue | `GET /repos/G-Ivan-A/hybrid-Intelligence-lab/issues/{n}` — поля `state`, `state_reason` |
| Состояние PR | `GET /repos/G-Ivan-A/hybrid-Intelligence-lab/pulls/{n}` — поля `merged`, `merged_at` |
| Наличие и статус артефакта | `GET /repos/{owner}/{repo}/contents/{path}` — факт существования файла и `status` во frontmatter |
| Состояние репозиториев экосистемы | `GET /repos/G-Ivan-A/{ai-ba-playbooks,mango_ba_prompts,aether-orbis}` — `private`, `created_at`, дерево файлов |

Правила вердикта взяты из
[`pr-ops/backlog-instruction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/pr-ops/backlog-instruction.md):

- `DONE` — «merged/accepted state confirmed by issue/PR/artifact evidence»;
- спринт архивируется только когда **все** задачи `DONE` **и** итоговый артефакт
  или decision outcome имеет статус «согласовано»/«отклонено»;
- если факт не подтверждается — статус не повышается, задача помечается
  «требуется ручная проверка».

Все 70 issue/PR, на которые ссылается бэклог, проверены: все 50 issue закрыты с
`state_reason: completed`, все 20 PR имеют `merged: true`. Само по себе это **не**
основание для `DONE` — статус повышался только там, где дополнительно подтверждён
итоговый артефакт.

## 3. Протокол валидации по спринтам

### 3.1. Спринт 3 — Ремонт структуры стандартов

| ID | Статус в бэклоге | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-050 | `review` | Аналитика существует, статус артефакта `draft` | [`docs/analysis/2026-07-10-r-a-a-report-structural-desync-options.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/analysis/2026-07-10-r-a-a-report-structural-desync-options.md) (`status: draft`, v0.2); [issue #407](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407) и [issue #415](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/415) закрыты `completed` | Оставить `review` |
| B-051 | `DONE` | Решение зафиксировано в ADR-008, но ADR имеет `status: proposed` | [`docs/adr/2026-07-adr-008-standard-meta-structure.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-07-adr-008-standard-meta-structure.md) (`status: proposed`, v0.2) | `DONE`, но см. находку F-1 |
| B-052 | `DONE` | Мета-стандарт существует | [`standards/standard-meta-structure.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/standard-meta-structure.md) (`status: proposed`, v0.2); [PR #435](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/435) — issue закрыт `completed` | Подтверждён |
| B-053 | `DONE` | Миграция стандартов выполнена | [PR #452](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/452) `merged_at: 2026-07-22` | Подтверждён |
| B-054 | `TODO` | Задача отложена (`- (deferred)`), артефакта нет | Строка бэклога; артефакт стандарта стресс-тестирования процесса отсутствует | Оставить `TODO` |

**Вывод по спринту 3.** Не архивируется: B-054 в `TODO`, B-050 в `review`.

### 3.2. Спринт 4 — Post-migration границы корня Хаба

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-056 | `DONE` | Разделение выполнено: в корне Хаба есть и `ai-governance/`, и `ai-rules/` | [PR #430](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/430) `merged_at: 2026-07-16`; [`ai-rules/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/ai-rules), [`ai-governance/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/ai-governance) | Подтверждён |
| B-057 | `DONE (absorbed)` | Поглощена ADR-007 | [issue #378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) закрыт `completed` | Подтверждён |
| B-058 | `DONE (absorbed)` | Поглощена ADR-007 | [issue #378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) закрыт `completed` | Подтверждён |
| B-059 | `TODO` | Триггер не наступил | Строка бэклога `- (deferred)` | Оставить `TODO` |
| B-060 | `TODO` | Каталог [`projects-sink/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects-sink) существует, правил наполнения нет | Дерево корня Хаба | Оставить `TODO` |
| B-061 | `TODO` | Каталог [`education/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/education) существует, Learning Profile нет | Дерево корня Хаба | Оставить `TODO` |
| B-062 | `TODO` | Каталог [`frameworks/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/frameworks) существует, стандарта нет | Дерево корня Хаба | Оставить `TODO` |

**Вывод по спринту 4.** Не архивируется: четыре triggered-задачи открыты.

### 3.3. Спринт 5 — Несущие дефекты агентной модели (v0.4)

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-064 | `DONE` | Форма задачи приведена к модели; режимы — `structured`/`creative`/`hybrid` | [`.github/ISSUE_TEMPLATE/task.yml`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/.github/ISSUE_TEMPLATE/task.yml); [issue #406](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/406) закрыт `completed` | Подтверждён, см. находку F-2 |
| B-065 | `DONE` | Метод стресс-тестирования зафиксирован | [`ai-rules/adversarial-stress-testing.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/adversarial-stress-testing.md) (`status: accepted`, v1.1) | Подтверждён |
| B-066 | `DONE` | Единый OWASP-LLM чек-лист существует | [`ai-governance/agent-security-checklist.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-governance/agent-security-checklist.md) (`status: accepted`, v1.0) | Подтверждён |

**Вывод по спринту 5.** Все задачи `DONE`; два из трёх итоговых артефактов имеют
`status: accepted`, третий (`task.yml`) — исполняемая форма, чьё целевое
состояние закреплено машинным тестом
[`tools/test-operating-mode-contract.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/test-operating-mode-contract.sh).
Оба условия архивации выполнены → **спринт удаляется из активного бэклога.**

### 3.4. Спринт 6 — V2, тонкий вертикальный срез «Валидация ФТ/ТЗ»

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-067 | `DONE` | Контракт evals существует | [`standards/evals-contract-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/evals-contract-standard.md) (`status: draft`, v0.2) | Подтверждён |
| B-068 | `TODO` | Не начата, зависит от B-067 и B-070 | Строка бэклога `- (planned)` | Оставить `TODO` |
| B-069 | `TODO` | Не начата | Строка бэклога `- (planned)` | Оставить `TODO` |
| B-070 | `TODO` | Открытый вопрос наблюдаемости; в корне Хаба каталога `runs/` нет | Дерево корня Хаба | Оставить `TODO` |

**Вывод по спринту 6.** Не архивируется.

### 3.5. Спринт 7 — Триггерные входы RFC/ADR из анализа v0.4

Все восемь задач (B-071 … B-078) в статусе `TODO`, поле Issue — `- (deferred)`;
ни одна не имеет открытого issue или PR в Хабе. Проверено по списку ссылок
бэклога: номеров issue для этих строк не зарегистрировано.

**Вывод по спринту 7.** Не архивируется, изменений статусов нет.

### 3.6. Спринт 8 — Разделение Mango на два репозитория

Это тот спринт, о котором issue #357 предполагает «разделение фактически
произведено». Проверка показывает: **предположение верно лишь частично.**

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-079 | `DONE` | ADR-009 принят | [PR #429](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/429) `merged_at: 2026-07-16`; уточнение по [issue #511](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/511) | Подтверждён |
| B-080 | `DONE` | План миграции составлен | [PR #442](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/442), [PR #447](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/447) — оба `merged` | Подтверждён |
| B-081 | `TODO` | Репозиторий [`ai-ba-playbooks`](https://github.com/G-Ivan-A/ai-ba-playbooks) **создан** 2026-08-06, но содержит только `README.md`; каталогов `prompt-library/`, `patterns/`, `standards/`, `examples/`, `docs/`, `templates/` нет; GitHub Pages не настроен (`GET /repos/G-Ivan-A/ai-ba-playbooks/pages` → 404) | Единственный коммит `f972fcc` «Initial commit» от 2026-08-06 | **`ЧАСТИЧНО`** — репозиторий создан, структура архетипа B и Pages отсутствуют |
| B-082 | `TODO` | `mango_ba_prompts` **остаётся публичным** (`private: false`), каталогов `evals/`, `internal-rfc/`, `internal-docs/` нет | [Дерево `mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts): `ai-governance/`, `ai-rules/`, `docs/`, `experiments/`, `kb/`, `patterns/`, `pr-ops/`, `prompts/`, `runs/`, `scripts/`, `site/`, `standards/`, `tools/` | Оставить `TODO` — факт опровергает «разделение выполнено» |
| B-083 | `TODO` | Физическая миграция не выполнена: в `ai-ba-playbooks` нет ни одного перенесённого артефакта | Содержимое [`ai-ba-playbooks`](https://github.com/G-Ivan-A/ai-ba-playbooks) | Оставить `TODO` |
| B-084 | `TODO` | Синхронизация приватный → публичный не настроена: в `ai-ba-playbooks` нет `.github/workflows/` | Содержимое [`ai-ba-playbooks`](https://github.com/G-Ivan-A/ai-ba-playbooks) | Оставить `TODO` |

**Вывод по спринту 8.** Не архивируется. Разделение доведено до решения (ADR),
плана и создания пустого публичного репозитория; приватизация, миграция
артефактов и синхронизация — не выполнены. Единственное изменение статуса:
B-081 `TODO` → `ЧАСТИЧНО` с абсолютной ссылкой на созданный репозиторий.

### 3.7. Спринт 9 — Теоретическая основа образовательного модуля

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-085 | `review` | Модуль существует, `status: draft`; условие перевода в `reviewed` — B-086 | [`research/ai-education/retrieval/00-introduction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ai-education/retrieval/00-introduction.md) (`status: draft`, v0.3) | Оставить `review` |
| B-086 | `TODO` | Не начата | Строка бэклога `- (planned)` | Оставить `TODO` |
| B-087 | `TODO` | Не начата | Строка бэклога `- (planned)` | Оставить `TODO` |

**Вывод по спринту 9.** Не архивируется.

### 3.8. Спринт 10 — Эволюция методологии инженерных исследований

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-089 | `DONE` | Модель зрелости зафиксирована | [PR #443](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/443) `merged` | Подтверждён |
| B-090 | `DONE` | Разделение методологий внесено | [PR #464](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/464) `merged` | Подтверждён |
| B-092 | `review` | Модуль `task-processing` существует, `status: draft`; RFC-следствий нет по условию постановки | [`research/ai-education/task-processing/00-introduction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ai-education/task-processing/00-introduction.md) (`status: draft`, v0.1) | Оставить `review` |
| B-098 | `review` | Глоссарий синхронизирован и принят | [PR #518](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/518) `merged_at: 2026-08-17`; [`standards/glossary.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md) (`status: accepted`, v2.3) | **`review` → `DONE`** |
| B-093 | `review` | RFC постановки задач имеет `status: draft`; следствия `experimental` до замера B-095 | [`docs/rfc/2026-08-06-rfc-task-statement-architecture.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-08-06-rfc-task-statement-architecture.md) (`status: draft`, v0.1) | Оставить `review` |
| B-103 | `review` | ADR-011 принят | [`docs/adr/2026-08-adr-011-research-models.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-08-adr-011-research-models.md) (`status: accepted`, v0.2); [PR #516](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/516) `merged` | **`review` → `DONE`** |
| B-104 | `review` | Модели research внесены в стандарт, RRP `Validated` | [PR #524](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/524) `merged_at: 2026-08-18`; [`standards/research-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/research-standard.md) v0.3 | **`review` → `DONE`** |

**Вывод по спринту 10.** Не архивируется: B-092 и B-093 остаются в `review`,
потому что их итоговые артефакты имеют `status: draft`, а следствия RFC #470
явно удерживаются `experimental` до проспективного замера B-095.

### 3.9. Спринт 11 — Синхронизация генома HTOM

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-105 | `DONE` | RFC принят | [`docs/rfc/2026-08-21-rfc-htom-genome-structure-and-ci.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-08-21-rfc-htom-genome-structure-and-ci.md) (`status: accepted`, v0.2); [PR #532](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/532) `merged` | Подтверждён |
| B-106 | `review` | Изменения применены к геному: CI-воркфлоу генома существует | [`templates/htom/.github/workflows/validate.yml`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/.github/workflows/validate.yml); [PR #538](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/538) `merged_at: 2026-08-22`; [issue #537](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/537) закрыт `completed` | **`review` → `DONE`** |

**Вывод по спринту 11.** Обе задачи `DONE`, итоговый RFC — `accepted`
(decision outcome «согласовано»). Оба условия архивации выполнены →
**спринт удаляется из активного бэклога.**

### 3.10. Спринт 12 — Конвейер артефактов БА

| ID | Статус | Факт | Доказательство | Вердикт |
| --- | --- | --- | --- | --- |
| B-107 | `DONE` | RRP-модуль нормализации существует | [`research/ba-requirements/normalization/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/normalization); [PR #540](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/540) `merged` | Подтверждён |
| B-108 | `DONE` | RFC дорожной карты существует | [PR #542](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/542) `merged` | Подтверждён |
| B-109 | `review` | Все четыре модуля M1–M4 присутствуют в репозитории; RFC переведён в `accepted` v1.0 | [`solution-modeling/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/solution-modeling), [`artifact-rendering/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/artifact-rendering), [`feedback-and-evolution/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/feedback-and-evolution), [`orchestration/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/orchestration); [`docs/rfc/2026-08-25-rfc-ba-artifact-pipeline-rrp-roadmap.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-08-25-rfc-ba-artifact-pipeline-rrp-roadmap.md) (`status: accepted`, v1.0); [PR #546](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/546) `merged_at: 2026-08-26` | **`review` → `DONE`** |

**Вывод по спринту 12.** Все задачи `DONE`, итоговый RFC — `accepted` →
**спринт удаляется из активного бэклога.**

### 3.11. Спринт 13 — Принудительный онбординг ИИ-агентов

Все семь задач (B-110 … B-116) в статусе `todo`. Проверка подтверждает, что
описанные пробелы **всё ещё существуют**:

| Утверждение бэклога | Проверка | Результат |
| --- | --- | --- |
| Корневой `AGENTS.md` не легализован (B-110) | `GET /repos/G-Ivan-A/hybrid-Intelligence-lab/contents/AGENTS.md` → 404; в репозитории есть только черновик [`templates/agents-md-root-draft.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/agents-md-root-draft.md) из [PR #548](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/548) | Подтверждено |
| Скрипта инъекции нет (B-111) | `tools/inject-agents-md.sh` в дереве Хаба отсутствует | Подтверждено |
| Mango содержит `docs/contracts/` (B-112) | [`docs/contracts/kb-citations.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/kb-citations.md) на месте | Подтверждено |
| Aether-Orbis без шаблонов issue (B-113) | `GET /repos/G-Ivan-A/aether-orbis/contents/.github/ISSUE_TEMPLATE` → 404 | Подтверждено |

**Вывод по спринту 13.** Не архивируется; статусы менять не нужно.

### 3.12. Блок «Отложенные задачи с триггером»

B-088, B-091, B-094, B-095, B-096, B-097 — все в статусе `deferred`. Триггеры не
наступили: артефактов, на которые они должны породить изменения, в Хабе нет.
Блок остаётся без изменений.

## 4. Исполнимая дельта для `pr-ops/backlog.md` Хаба

Базовая версия: `1.53` (`updated: 2026-09-03`). Целевая: **`1.54`**.

### 4.1. Удалить целиком (архивация спринтов)

| Что удалить | Основание |
| --- | --- |
| Раздел `## Спринт 5: Несущие дефекты агентной модели (v0.4, «сейчас»)` со строками B-064, B-065, B-066 | п. 3.3 — все `DONE`, артефакты `accepted` |
| Раздел `## Спринт 11: Синхронизация генома HTOM с фактической структурой Хаба` со строками B-105, B-106 | п. 3.9 — все `DONE`, RFC `accepted` |
| Раздел `## Спринт 12: Конвейер артефактов БА — от нормализации входа к дорожной карте` со строками B-107, B-108, B-109 | п. 3.10 — все `DONE`, RFC `accepted` |

История спринтов остаётся в GitHub Issues/PR, `CHANGELOG.md` Хаба и самих
артефактах; отдельный архивный файл не создаётся — по
[`backlog-instruction.md` § «Правила архивации спринтов»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/pr-ops/backlog-instruction.md).

### 4.2. Изменить статусы

| ID | Было | Стало | Основание |
| --- | --- | --- | --- |
| B-081 | `TODO` | `ЧАСТИЧНО` | Репозиторий https://github.com/G-Ivan-A/ai-ba-playbooks создан 2026-08-06; структура архетипа B и GitHub Pages отсутствуют |
| B-098 | `review` | `DONE` | PR #518 merged; `standards/glossary.md` v2.3 `accepted` |
| B-103 | `review` | `DONE` | PR #516 merged; ADR-011 `accepted` |
| B-104 | `review` | `DONE` | PR #524 merged; `research-standard.md` v0.3 |

Строки B-098, B-103, B-104 остаются в Спринте 10, потому что спринт не
архивируется (B-092 и B-093 в `review`).

### 4.3. Изменить содержание строк (без изменения статуса)

| ID | Правка | Основание |
| --- | --- | --- |
| B-064 | Из «Краткого содержания» убрать утверждение, что `task.yml` предлагает `deep-think`: форма содержит `structured`/`creative`/`hybrid`, а `deep-think` явно запрещён тестом `tools/test-operating-mode-contract.sh`. Правка выполняется вместе с архивацией Спринта 5, поэтому в активном бэклоге строка исчезает | Находка F-2 |
| B-081 | Добавить абсолютную ссылку на созданный репозиторий и перечислить, что осталось: структура архетипа B + GitHub Pages | п. 3.6 |
| B-082 | Добавить факт: `mango_ba_prompts` на 2026-09-03 остаётся публичным (`private: false`) | п. 3.6 |

### 4.4. Обновить frontmatter `pr-ops/backlog.md`

```yaml
version: 1.54
updated: 2026-09-03
```

Из `related_issues` при архивации спринтов 5, 11 и 12 удаляются ссылки, которые
больше не используются ни одной активной строкой: `#406` (Спринт 5), `#531`,
`#537` (Спринт 11), `#539`, `#541`, `#545` (Спринт 12). Остальные ссылки
сохраняются — они цитируются оставшимися строками и блоком «Источники активного
порядка».

## 5. Записи в связанные артефакты Хаба

### 5.1. `CHANGELOG.md` Хаба — предлагаемая запись

```markdown
### Changed — Issue #357: валидация активных спринтов бэклога

- Проведена сплошная валидация `pr-ops/backlog.md` (v1.53): проверены все
  70 связанных issue/PR и итоговые артефакты каждой задачи.
- Архивированы полностью завершённые спринты 5, 11 и 12; история осталась в
  GitHub Issues/PR и в самих артефактах.
- B-098, B-103, B-104 переведены `review` → `DONE` по merged PR и принятым
  артефактам; B-081 переведён `TODO` → `ЧАСТИЧНО` (репозиторий
  `ai-ba-playbooks` создан, структура и Pages отсутствуют).
- Протокол валидации с доказательствами:
  https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/analysis/2026-09-03-hub-backlog-sprint-validation.md
```

### 5.2. `pr-ops/artifact-map.md` Хаба

Изменений в карте активных артефактов Хаба **не требуется**: архивация спринтов
не удаляет и не добавляет файлов, а все артефакты архивируемых спринтов
(`ai-rules/adversarial-stress-testing.md`, `ai-governance/agent-security-checklist.md`,
RFC генома HTOM, корпус `research/ba-requirements/`) остаются активными и уже
присутствуют в карте либо в `related_artifacts` бэклога.

## 6. Находки, требующие решения человека

| ID находки | Суть | Доказательство | Рекомендация |
| --- | --- | --- | --- |
| **F-1** | B-051/B-052 закрыты как `DONE`, но decision record ADR-008 и производный `standards/standard-meta-structure.md` остаются `status: proposed`, а не `accepted` | [ADR-008](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-07-adr-008-standard-meta-structure.md), [мета-стандарт](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/standard-meta-structure.md) | Либо перевести ADR-008 в `accepted` (human decision gate), либо понизить статус задач. Требуется ручная проверка — статус в бэклоге здесь не меняется |
| **F-2** | «Краткое содержание» B-064 утверждает, что `task.yml` предлагает `deep-think`; фактически режим отсутствует и запрещён машинным тестом | [`task.yml`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/.github/ISSUE_TEMPLATE/task.yml), [`tools/test-operating-mode-contract.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/test-operating-mode-contract.sh) L92-94, [ADR-010](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-08-adr-010-agent-autonomy-principles.md) | Расхождение снимается архивацией Спринта 5; сама задача B-064 подтверждена как выполненная (модель режимов пересмотрена ADR-010) |
| **F-3** | Постановка issue #357 исходит из того, что разделение Mango «фактически выполнено». Факты это опровергают: `mango_ba_prompts` публичен, `ai-ba-playbooks` пуст | [`private: false`](https://github.com/G-Ivan-A/mango_ba_prompts), [`ai-ba-playbooks`](https://github.com/G-Ivan-A/ai-ba-playbooks) | Спринт 8 **не** архивируется; закрыть можно только B-079/B-080 (уже `DONE`) |

## 7. Не выполнено и вопросы

1. **Правки в репозиторий Хаба не применены.** У исполнителя issue #357 нет
   права записи в
   [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab)
   (`permissions.push = false`), а PR задачи открыт в спице `mango_ba_prompts`.
   Дельта разделов 4 и 5 исполнима как есть; требуется решение Пользователя:
   применить её в Хабе самостоятельно или выдать доступ/открыть задачу в
   репозитории Хаба.
2. **F-1 требует решения человека** — статус ADR-008 не может быть изменён
   исполнителем (human decision gate).
3. Статусы задач, факт которых не подтверждается артефактом (B-050, B-085,
   B-092, B-093), сознательно **не повышены** — по контракту «запрет на
   выдумывание состояния».
