---
status: draft
version: 0.1
updated: 2026-10-31
temperature: 0.1
owner: G-Ivan-A
type: audit
scope: repo
audit_target: "Репозиторий mango_ba_prompts целиком на коммите 6f6cbc47 и результаты задач #405/#407 (PR #406/#408)"
evidence_model: "Git tree 6f6cbc47 (1615 файлов), закреплённый Хаб 32b5fa52, mango-ba-ai-runtime b67410f6, история issues #1–#409 и PR, GitHub API"
verdict: "conditional — репозиторий пригоден как источник практики этапа 1 при условии решения DEC-01…DEC-10; к масштабированию без этих решений не готов"
severity_scale: "S1 блокирует согласование направления; S2 противоречие норме или SSOT; S3 устаревание; S4 косметика"
follow_up: "docs/analysis/2026-10-31-follow-up-tasks.md"
related_norm: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/audit-standard.md"
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409"
based_on: "https://github.com/G-Ivan-A/mango_ba_prompts/tree/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f"
---

# Аудит аудита репозитория: состояние, SSOT и готовность к масштабированию

Ответ на [issue #409](https://github.com/G-Ivan-A/mango_ba_prompts/issues/409):
«Я как пользователь хочу получить "чистый" репозиторий для того, чтобы
масштабировать проект». Документ проверяет сам репозиторий **и** результаты
предыдущих аналитических задач ([#405](https://github.com/G-Ivan-A/mango_ba_prompts/issues/405)
→ [PR #406](https://github.com/G-Ivan-A/mango_ba_prompts/pull/406),
[#407](https://github.com/G-Ivan-A/mango_ba_prompts/issues/407)
→ [PR #408](https://github.com/G-Ivan-A/mango_ba_prompts/pull/408)).
Это аналитический артефакт: ни один файл репозитория по его итогам не
перемещён и не изменён — по ограничению issue изменения вносятся только
отдельными задачами на основе согласованного RFC/ADR.

## Summary / BLUF

1. **Главная находка (S1): статус репозитория в экосистеме противоречит
   реальности.** Решением владельца в Хабе
   ([issue #583 Хаба](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583),
   2026-09-15) `mango_ba_prompts` объявлен **`legacy/archived`**: «Новая
   разработка в нём не ведётся… Активная задача, предполагающая изменение
   этого репозитория, в бэклоге запрещена»
   ([ops/backlog.md Хаба, раздел «Статус репозиториев экосистемы»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/ops/backlog.md#L85-L96)).
   После этой даты в репозитории создано 25 issues и слито 25 PR, а владелец
   ставит четырёхэтапную стратегию развития именно этого репозитория.
   Ни один артефакт #405/#407 этого статуса не обнаружил. Без решения
   **DEC-01** любое «видение» и «roadmap» строятся на неопределённом статусе.
2. **S1: стратегических документов нет, а действующие контракты фиксируют
   прежнюю стратегию.** В `docs/` нет видения, концепции, архитектуры и
   roadmap; их роль размазана по `README.md`, `ai-governance/ai-governance.md`
   и `docs/ba-ecosystem.md`, а формулировки прежней стратегии (issue
   [#263](https://github.com/G-Ivan-A/mango_ba_prompts/issues/263): «GitHub —
   единственная платформа», «уровни 3–4 не являются планом работ»,
   «Private», «ai-ba-playbooks») **закреплены регрессионным валидатором**
   `scripts/validate_issue_263_vision_alignment.py`. Этапы 3–4 (n8n, сервер)
   им прямо противоречат — нужна явная замена (**DEC-02**), иначе актуализация
   сломает CI.
3. **S2: сменилась идентичность соседнего репозитория.** `ai-ba-playbooks`,
   который README называет «публичной методологией», переименован в
   `mango-ba-ai-runtime` (тот же GitHub ID 1324838162) и в Хабе имеет статус
   `target` — «единственная среда исполнения MVP». Локальные документы этого
   не отражают (кроме таксономии #399).
4. **S2: SSOT этапа 2 тройной**: draft ADR-016 (39 классов, OpenCode V1),
   скомпилированный пакет Хаба `dist/execution-package-opencode` (с 2026-10-07)
   и 11 skills в `mango-ba-ai-runtime`. #405 не учёл два последних.
5. **Чистота файлов.** Каждый из 1615 файлов получил диспозицию в
   [реестре](../analysis/2026-10-31-file-disposition-register.md): 233
   актуальны, 113 требуют актуализации, 4 — переноса, 370 — исторические,
   38 — кандидаты в архив, 28 уже в архиве, 23 сгенерированы, 806 — замороженная
   статистика `runs/`.
6. **Предыдущие задачи выполнены частично.** #405 закрыл исследование клиентов,
   но не связал его с пакетами Хаба и runtime. #407 дал инвентарь и RFC, но без
   пофайловой диспозиции, с корневым размещением стратегических файлов вопреки
   практике Хаба, со ссылками на ветку форка и без учёта статуса #583. Этим PR
   RFC переписан до v0.3, ссылки форка в артефактах #407 заменены. Те же
   ссылки на временные ветки форка есть ещё в 11 активных файлах (F-19).
7. **Проверки не охватывают корпус.** Валидатор frontmatter в CI проверяет
   только корень, `ai-rules/` и `tools/`; вне этой области 183 файла с 818
   ошибками, включая все 113 файлов с запрещённым `ai-generated` (F-20).

**Вердикт: `conditional`.** Репозиторий богат проверяемой практикой этапа 1,
но к масштабированию не готов, пока владелец не примет DEC-01…DEC-10
([RFC v0.3](../rfc/2026-10-repository-modernization.md)). После решений
исполнение разбито на задачи T-01…T-09 и обращения в Хаб H-01…H-07
([реестр задач](../analysis/2026-10-31-follow-up-tasks.md)).

## Scope / Target

| Объект | Срез | Что проверялось |
| --- | --- | --- |
| `mango_ba_prompts` | [tree 6f6cbc47](https://github.com/G-Ivan-A/mango_ba_prompts/tree/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f), 1615 отслеживаемых файлов | Структура, роли, актуальность, frontmatter, связи, SSOT, соответствие Хабу |
| Хаб `hybrid-Intelligence-lab` | [tree 32b5fa52](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/32b5fa524e542af23c1a8e67c919bd66d5f4e399) | Нормы для спиц, статус репозиториев, мета-модель БА, среды исполнения, пакеты `dist/` |
| `mango-ba-ai-runtime` | [tree b67410f6](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/b67410f627801345309281faa15e7219722bfb1a) | Роль, версия, контракты, связь с этапами |
| История задач | issues #1–#409, PR #406, #408 и комментарии владельца | Эволюция требований, ожидания к #405/#407 |
| Сайт этапа 1 | https://g-ivan-a.github.io/mango_ba_prompts/ (HTTP 200; Pages из `gh-pages`, build_type `legacy`) | Связь документации с презентационным каналом |

**Вне области:** содержательная правка `runs/` (статистика, ограничение issue),
изменение действующих файлов (только по согласованному RFC/ADR), запуск LLM
и клиентов, оценка качества отдельных промптов (её выполняли #384/#397/#403).
Исключение, разрешённое issue («изменить результирующие артефакты, включая
RFC»): RFC #407 переписан до v0.3, в трёх отчётах #407 исправлены ссылки
на ветку форка.

## Method / Evidence

1. **Полный перечень файлов.** `git ls-tree -r 6f6cbc47` → генератор
   [`experiments/issue_409/build_disposition.py`](../../experiments/issue_409/build_disposition.py)
   присваивает каждому файлу одну из восьми диспозиций по правилам каталога
   и явным исключениям с обоснованием и номером задачи. Результат —
   [`disposition.json`](../../experiments/issue_409/disposition.json) и
   [реестр](../analysis/2026-10-31-file-disposition-register.md);
   согласованность проверяется `scripts/validate_issue_409_audit_artifacts.py`.
2. **Сверка с нормами Хаба** по закреплённым URL: [AGENTS.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/AGENTS.md),
   [agents-md-bootstrap-standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/agents-md-bootstrap-standard.md) (accepted 2.0),
   [htom-documentation-structure](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/htom-documentation-structure.md) (accepted 1.0),
   [product-profile](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/product-profile.md) (accepted 1.0),
   [audit-standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/audit-standard.md) (draft 0.2),
   [artifact-deprecation-standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/artifact-deprecation-standard.md) (draft 0.2),
   [rfc-structure-standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/rfc-structure-standard.md),
   [ADR-009](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/docs/adr/2026-07-adr-009-mango-repo-split.md) (proposed 0.3),
   [ADR-014 Хаба](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md) (proposed 1.0),
   [ops/backlog.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/ops/backlog.md),
   [мета-модель research/ba-requirements](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/research/ba-requirements/README.md) (draft 0.7),
   [варианты runtime ba-ai-process](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md).
3. **Проверка фактов через GitHub API** (2026-10-31): видимость и архивность
   репозиториев, переименование `ai-ba-playbooks` → `mango-ba-ai-runtime`
   (`gh api repos/G-Ivan-A/ai-ba-playbooks` возвращает
   `G-Ivan-A/mango-ba-ai-runtime`, id 1324838162, создан 2026-08-06),
   источник Pages, даты #583 Хаба (создан 2026-09-15 18:59, закрыт 19:14 UTC;
   коммит `ff97978`), счёт issues/PR после 2026-09-15.
4. **Трассировка требований** по всей истории задач (фазы Ф0–Ф6) —
   [анализ эволюции требований](../analysis/2026-10-31-requirements-evolution.md).
5. **Проверка ожиданий к #405/#407** по тексту issues и комментариям владельца
   в [PR #408](https://github.com/G-Ivan-A/mango_ba_prompts/pull/408#issuecomment-6522949478)
   и [второй коррекции](https://github.com/G-Ivan-A/mango_ba_prompts/pull/408#issuecomment-6524028597).

**Модель доказательств.** `OBSERVED` — факт из закреплённого дерева, API или
текста; `PROPOSED` — предложение этого аудита; `UNRESOLVED` — противоречие,
вынесенное на решение владельца. Аудит не выдаёт предложения за принятые
решения: принятие фиксируется только владельцем (Hub AGENTS.md, правило 7:
противоречие апеллируется, а не разрешается молча).

**Предел доказательств.** Октябрьский JSON-экспорт чата из
[комментария к PR #408](https://github.com/G-Ivan-A/mango_ba_prompts/pull/408#issuecomment-6522949478)
по-прежнему не загружен (пустая ссылка `Uploading…`). Issue #409 указывает
другой первоисточник — «эволюция требований прослеживается через историю
задач», — поэтому отсутствие JSON больше не блокирует анализ и RFC, а
фиксируется как остаточное ограничение.

## Findings / Verdict

### Реестр находок

| ID | S | Находка (`OBSERVED`) | Доказательство | Решение / задача |
| --- | --- | --- | --- | --- |
| F-01 | S1 | Хаб объявил репозиторий `legacy/archived` и запретил задачи на его изменение; фактически после 2026-09-15 создано 25 issues и слито 25 PR, владелец ставит 4 этапа развития этого репозитория. Локальные документы статус не упоминают. Карта экосистемы Хаба при этом всё ещё показывает `Active` ([ecosystem-map.md, draft 0.4 от 2026-06-12](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/docs/ecosystem-map.md)). | [backlog L85–L96](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/ops/backlog.md#L85-L96), [#583 Хаба](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583), GitHub API | DEC-01, H-01, H-02 |
| F-02 | S1 | В `docs/` нет видения, концепции, архитектуры, roadmap; правило 7 Hub AGENTS.md («read the project concept and vision») невыполнимо для исполнителя. | Дерево `docs/`; [Hub AGENTS.md L29](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/AGENTS.md#L29) | DEC-08, T-02 |
| F-03 | S1 | Четыре этапа противоречат действующим контрактам: «GitHub — единственная платформа» (`ai-governance/ai-governance.md`), «уровни 3–4 не являются планом работ» (`docs/ba-ecosystem.md` §7), запрет серверной инфраструктуры в концептуальных документах; всё закреплено валидатором #263. | `scripts/validate_issue_263_vision_alignment.py` (`REQUIRED_TEXT`, docstring) | DEC-02, T-02 |
| F-04 | S2 | `ai-ba-playbooks` переименован в `mango-ba-ai-runtime` и стал целевым runtime MVP (README v0.5, meta_model_version 0.4, маршрут A-IN → A-CORE → A-BCREQ, 11 skills). README/ai-governance/ba-ecosystem/rfc-hub-integration называют его «публичной методологией»; валидатор #263 требует строку `ai-ba-playbooks`. | GitHub API; [runtime README](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/b67410f627801345309281faa15e7219722bfb1a/README.md) | DEC-04, T-08 |
| F-05 | S2 | ADR-009 Хаба (только `proposed` 0.3) требует перевести репозиторий в Private; оба репозитория публичны, а сайт Pages — канал доставки этапа 1. README подаёт Private как свершившийся план («блокер Q1»). | [ADR-009](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/docs/adr/2026-07-adr-009-mango-repo-split.md), GitHub API | DEC-03, H-03 |
| F-06 | S2 | Три кандидата SSOT этапа 2: draft ADR-016 (39 классов), [пакет Хаба OpenCode](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/projects/ba-ai-process/dist/execution-package-opencode/README.md) (draft 0.1, `RG-BCREQ-v1`, с 2026-10-07, #652 Хаба), skills runtime. | Деревья трёх репозиториев | DEC-06, T-09 |
| F-07 | S2 | Issue #409 ставит этап 3 как «оркестрацию процессов через n8n»; Хаб: «n8n допустим как слой интеграций поверх API runner, но не вместо него»; n8n как ядро маршрута (В-6) отклонён (Г-44…Г-49); RFC серверной среды с местом n8n — B-218 (TODO). | [runtime-options L62–L71](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md#L62-L71), [backlog L700](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/ops/backlog.md#L700) | DEC-05, H-04 |
| F-08 | S2 | Нет корневого `AGENTS.md` (обязателен для архетипов A–D); в `.hub-profile.json` нет `archetype`/`environment`, `target_type: HTOM`, последний синк с Хабом 2026-08-17 (`3bfa4103`). Локальный замок корня (D1) допускает только `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md` — сам `AGENTS.md` сейчас не прошёл бы `validate-structure`. | [bootstrap-standard L14, L55](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/standards/agents-md-bootstrap-standard.md#L55), `.hub-profile.json` | DEC-07, T-01 |
| F-09 | S2 | `docs/contracts/` существует (3 файла), Хаб запрещает этот дом («agent contracts live in ai-rules/»). | [Hub AGENTS.md L35](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/AGENTS.md#L35) | T-06 |
| F-10 | S3 | Поле `ai-generated`, запрещённое Хабом, есть в 741 файле: 628 в `runs/` (статистика, не правится) и 113 вне `runs/`. Локальный валидатор проверяет только корень, `ai-rules/`, `tools/`. | [Hub AGENTS.md L37](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/AGENTS.md#L37); реестр | DEC-09, T-07 |
| F-11 | S3 | Ключевые решения этапа 1 не приняты: RFC ручного конвейера BCREQ — `draft`, ADR-015 (классы) и ADR-016 (IDE-процесс) — `draft`, ADR 003–014 — `proposed`. Принятыми остаются только 0001–0004, 001, 002. | frontmatter `docs/adr/`, `docs/rfc/` | DEC-01, T-07 |
| F-12 | S3 | KB перенесена в runtime (#361), но в репозитории остаются конвейер `scripts/kb/`, `kb/` и пять KB-валидаторов (58 файлов) — второй, расходящийся источник. | #361; реестр, T-05 | DEC-10, T-05 |
| F-13 | S3 | Карта процессов `docs/ba-processes/`, `docs/taxonomy.md`, `patterns/` описывают дофазовую модель (ТЗ/ФТ-генераторы); актуальная модель — A-IN/A-CORE/A-WORK/A-RELEASE ([RFC ручного конвейера](../rfc/2026-10-bcreq-manual-pipeline.md)). | реестр, T-04 | T-04 |
| F-14 | S3 | README и `ai-governance` утверждают «evals и golden-set отсутствуют», хотя с #373–#391 есть кандидаты Golden Set (`docs/reviews/issue-391-golden-inventory.md`) — утверждённого eval-набора нет, но формулировка устарела; валидатор #263 её закрепляет. | `README.md` L50, `ai-governance/ai-governance.md` L90 | DEC-02, T-02 |
| F-15 | S3 | Источник раздела «Дорожная карта» сайта — `docs/ba-ecosystem.md` (уровни L1–L4), а не roadmap четырёх этапов. Изменение стратегических документов не отразится на сайте без правки генератора. | `scripts/generate-pages-data.mjs`, RFC v0.2 D-01…D-08 | T-03 |
| F-16 | S4 | В корне `docs/` 7 разнородных файлов, два дома процессов (`ba-process/` и `ba-processes/`), два дома таксономии (`taxonomy.md` и `taxonomy/`), шаблон с личным именем `task-for-konard-template.md`. | дерево `docs/` | T-06 |
| F-17 | S4 | Номера ADR не уникальны в экосистеме: локальный `2026-10-adr-014-documentation-source-validation.md` и ADR-014 Хаба о наследии — разные решения с одним номером; ссылки «ADR-014» неоднозначны без префикса репозитория. | `docs/adr/`, Хаб `docs/adr/` | T-06 (ссылаться с префиксом репозитория) |
| F-18 | S3 | 14 BCREQ-промптов (`prompts/bcreq-*`, #388, 2026-10-24) названы с суффиксами `-oneshot`/`-stepwise`, тогда как ADR-016 Хаба (`proposed` 1.0, SF-7) запрещает эти имена в новых артефактах. Переименование сломало бы идентификаторы в статистике `runs/` и ссылки сайта. | [ADR-016 Хаба L70](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/32b5fa524e542af23c1a8e67c919bd66d5f4e399/docs/adr/2026-09-adr-016-skill-form-and-contract-format.md#L70) | H-06 (SF-7 — для навыков runtime; промпты этапа 1 — наследие) |
| F-19 | S3 | Активные файлы ссылаются на временные ветки форка исполнителя `konard/G-Ivan-A-mango_ba_prompts` (`issue-399-…`, `issue-401-…`): `README.md` L173, ADR-013, ADR-014, `docs/site-access.md` и 7 файлов `docs/taxonomy/` (включая 3 машинных JSON). Все цели ссылок существуют в `main`; после удаления веток форка ссылки сломаются. Генераторы JSON — исторические `experiments/issue_399/`, `experiments/issue_401/`. Записи `CHANGELOG.md` и исторические ревью — свидетельства, не правятся. | `grep -rl 'github.com/konard/G-Ivan-A-mango_ba_prompts'` по дереву 6f6cbc47: 26 файлов; правило `FORK_LINK` в `experiments/issue_409/build_disposition.py` | T-08 (README — T-02, `docs/site-access.md` — T-06) |
| F-20 | S3 | Локальный валидатор frontmatter (`tools/validate-frontmatter.sh`, правила Хаба) в CI покрывает только `FRONTMATTER_SCOPE := $(wildcard *.md) ai-rules tools`. Прогон того же валидатора по остальным каталогам (кроме `runs/` и `experiments/`) даёт 183 файла с 818 ошибками: `docs/` 75 (404; из них 21 датированный отчёт), `prompts/` 46 (192), `standards/` 31 (156), `patterns/` 15 (16), `kb/` 9 (26), `pr-ops/` 7 (24). Типы ошибок: 387 полей, не разрешённых для класса документа; 225 отсутствующих обязательных полей; 111 запрещённых `ai-generated`; 32 недопустимых статуса (24 — `archived` в `prompts/archive/`); 11 файлов без frontmatter; 48 отсутствующих разделов аудита. Все 113 файлов с `ai-generated` вне `runs/` (F-10) входят в эти 183 — без расширения области CI F-10 вернётся. Долг записан в `pr-ops/BACKLOG.md` (S-002, S-003, август 2026) с устаревшими цифрами (1 287 файлов, в основном `kb/processed/`, которого в дереве уже нет) и без решения, какие каталоги подпадают под governance-frontmatter. | [`Makefile` L146](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f/Makefile#L146); [`.github/workflows/validate.yml` L27–L28](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f/.github/workflows/validate.yml#L27-L28); прогон `./tools/validate-frontmatter.sh` по дереву 6f6cbc47; [`pr-ops/BACKLOG.md` L355–L356](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f/pr-ops/BACKLOG.md#L355-L356) | T-07 (расширение области по каталогам; датированные отчёты — явное исключение с причиной) |

### Соответствие правилам Хаба для спиц

| Правило Хаба | Состояние | Находка |
| --- | --- | --- |
| Корневой `AGENTS.md` с `archetype`/`environment` = `.hub-profile.json` | Нет файла, нет полей | F-08 |
| Концепция и видение доступны исполнителю | Нет | F-02 |
| `docs/contracts/` запрещён | Есть | F-09 |
| `ai-generated` во frontmatter запрещён | 741 файл; CI проверяет только корень, `ai-rules/`, `tools/` | F-10, F-20 |
| Ссылки из спицы на правила Хаба — абсолютные закреплённые | Соблюдается в активных концептуальных документах (валидатор #263 запрещает `../../standards/`); нарушалось в артефактах #407 (ссылки на ветку форка) — исправлено этим PR. Ссылки на ветки форка вместо `main` остаются в 11 активных файлах | F-19 |
| Новые каталоги верхнего уровня — только с decision record | Соблюдается: 9 проектных каталогов обоснованы в `.hub-profile.json` `project_specific_directories` | — |
| Аудиты в `docs/audit/YYYY-MM-DD-*.md` с обязательными разделами | Новые аудиты соблюдают; 7 старых аудитов без даты в начале имени — исторические | — |
| Жизненный цикл депрекации active → deprecated/superseded → archived | `.archive/` и `prompts/archive/` есть, но статусы не размечены единообразно | F-10, T-07 |

### SSOT: где живёт истина по каждой теме

| Тема | SSOT сейчас (`OBSERVED`) | Конфликт | Предлагаемый SSOT (`PROPOSED`) |
| --- | --- | --- | --- |
| Нормы для спиц | Хаб: `standards/`, `AGENTS.md`, `ai-governance/` | Локальные копии синка 2026-08-17 устарели | Хаб по закреплённому SHA; спица — только ссылки и локальные отклонения с обоснованием |
| Статус репозиториев экосистемы | Хаб `ops/backlog.md` (таблица статусов) | Противоречит факту (F-01) и карте экосистемы Хаба | Хаб, после решения DEC-01; в спице — ссылка из `docs/concept.md` |
| Мета-модель БА | Хаб `research/ba-requirements/` (M0–M4) + `projects/ba-ai-process/` | Локальная карта M0–M2 ↔ C01–C35 в `docs/analysis/ide-clients-stage-2/` — аналитика, не норма | Хаб; спица — практика и свидетельства в форме LG-5 («в корпусе наблюдается X, замер, коммит») |
| Процесс BCREQ этапа 1 | `docs/rfc/2026-10-bcreq-manual-pipeline.md` (draft), `standards/bcreq-manual-classes.md` и `standards/bcreq-*` | Не принят (F-11) | Принятый RFC/ADR в спице |
| Промпты | `prompts/` (+ `prompts/archive/`) | Сайт показывает выборку | `prompts/`; сайт — производное |
| Сайт | `scripts/generate-pages-data.mjs` + источники → `gh-pages` | Источник roadmap — `docs/ba-ecosystem.md` (F-15) | Генератор + `docs/roadmap.md` |
| Пакет этапа 2 | Три кандидата (F-06) | — | DEC-06 |
| Runtime и KB | `mango-ba-ai-runtime` (KB перенесена #361) | Локальный конвейер KB (F-12) | `mango-ba-ai-runtime` |
| Статистика прогонов | `runs/` + `runs/README.md` | — | `runs/` (заморожена; новые RUN дописываются) |
| Профиль спицы | `.hub-profile.json` | Нет archetype/environment | `.hub-profile.json` |
| Мост к Хабу | `docs/hub-research-dependencies.md` | Якоря на SHA 2026-08 | Он же, с обновлёнными закреплёнными SHA |
| Карта артефактов / бэклог спицы | `pr-ops/artifact-map.md`, `pr-ops/BACKLOG.md` | Не отражают #384–#409 полностью | Они же (T-06/T-07) |
| Видение, концепция, архитектура, roadmap | Отсутствуют (F-02) | — | `docs/vision.md`, `docs/concept.md`, `docs/architecture.md`, `docs/roadmap.md` (DEC-08) |

### Диспозиция файлов

Полный пофайловый перечень — в
[реестре диспозиции](../analysis/2026-10-31-file-disposition-register.md);
ниже — выводы для требований issue.

| Требование issue | Ответ аудита |
| --- | --- |
| «структура соответствует правилам для репозиториев экосистемы Хаба» | Нарушения F-08, F-09, F-10, F-16; исправимы задачами T-01, T-06, T-07 без изменения истории. |
| «файлы репозитория или актуальны или вынесены в архив» | 233 `current`; 113 `update` и 4 `relocate` — актуальная роль, устаревшее содержание или дом; 38 `archive-candidate` — вывод по стандарту депрекации; 28 уже `archived`. |
| «исторические файлы размечены» | 370 `historical` (в основном `experiments/` и датированные `docs/analysis`, `docs/report`, `docs/reviews`) размечаются правилом каталога, а не правкой каждого файла (DEC-09); 806 файлов `runs/` — `statistics`, не размечаются заново. |

### Проверка результатов задач контекста

| Задача | Ожидание пользователя | Что получено | Расхождение | Действие в этом PR |
| --- | --- | --- | --- | --- |
| [#405](https://github.com/G-Ivan-A/mango_ba_prompts/issues/405) → [PR #406](https://github.com/G-Ivan-A/mango_ba_prompts/pull/406): IDE-клиенты этапа 2 | Способ работы этапа 2 по принципам 39 классов, выбор клиента, обучение, безопасность | Полное исследование Q01–Q17, рекомендация OpenCode V1, draft ADR-016, карта M0–M2 | Не учтены уже существующий пакет Хаба `execution-package-opencode` (2026-10-07) и runtime как дом исполнения; без этого рекомендация не определяет, **где** живёт пакет (F-06). Мета-модельная карта корректна по содержанию, но не учитывает ADR-014 Хаба (практика = свидетельство). | Зафиксировано DEC-06, T-09; содержимое #405 не меняется — оно остаётся корректным исследованием. |
| [#407](https://github.com/G-Ivan-A/mango_ba_prompts/issues/407) → [PR #408](https://github.com/G-Ivan-A/mango_ba_prompts/pull/408): аудит и модернизация | (1) отделить историю от определяющих артефактов; (2) понять эволюцию требований (фазы A-IN/A-CORE вместо «валидации ФТ/ТЗ»); (3) предложить видение, концепцию, архитектуру, roadmap с обоснованием; (4) отражение на сайте; (5) архивирование ненужного; (6) не противоречить мета-модели по вектору | Инвентарь 1610 файлов, анализ октября, соответствие экосистеме, RFC v0.2 с D-01…D-08 | (1) инвентарь без пофайловой диспозиции «актуален/архив/история» — главный вопрос «чистоты» остался без ответа; (2) эволюция только за октябрь и заблокирована отсутствующим JSON; (3) предложено корневое `PRODUCT_VISION.md`/`ROADMAP.md` вопреки B-113 и практике Хаба, а локальный замок корня (`tools/validate-repository-structure.sh` L112–L130, дельта D1: в корне только `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`) такие файлы отклонит; (6) не обнаружены `legacy/archived` (#583), ADR-014 Хаба, переименование runtime, пакеты `dist/`, позиция Хаба по n8n, валидатор #263; ссылки вели на ветку форка; RFC не зарегистрирован. | Реестр диспозиции; эволюция по всей истории; RFC v0.3; ссылки форка заменены на `main` апстрима; RFC зарегистрирован в `docs/rfc/rfc-register.md`. |

### Вердикт

`conditional`. Структурные нарушения устранимы механически, но **направление**
(F-01…F-07) нельзя выбрать на стороне исполнителя: это противоречия между
постановкой владельца, решениями Хаба и действующими контрактами спицы.
По Hub AGENTS.md (правило 7) они апеллируются, а не разрешаются молча.

## Remediation / Deviation

### Решения владельца (DEC)

Полное описание вариантов, рекомендаций и последствий —
в [RFC v0.3](../rfc/2026-10-repository-modernization.md#решения-на-согласование).

| ID | Вопрос | Рекомендация (`PROPOSED`) | Находки |
| --- | --- | --- | --- |
| DEC-01 | Статус `mango_ba_prompts` в экосистеме | Гибрид: репозиторий — лаборатория практики этапа 1 (промпты, сайт, ручной конвейер BCREQ, статистика), `mango-ba-ai-runtime` — исполнение этапов 2–4; оформить решением в Хабе, заменив строку `legacy/archived` | F-01, F-11 |
| DEC-02 | Замена границ #263 | Новый ADR спицы, заменяющий формулировки #263; валидатор #263 обновляется в той же задаче | F-03, F-14 |
| DEC-03 | Видимость (ADR-009 Хаба) | Сохранить Public до принятия ADR-009; не утверждать Private в README | F-05 |
| DEC-04 | Роль `mango-ba-ai-runtime` и канал этапа 1 | Runtime — исполнение и KB; спица — источник практики и сайт; связь описывается в `docs/architecture.md` | F-04 |
| DEC-05 | Роль n8n на этапе 3 | Оболочка интеграций/интерфейса поверх API runner; «оркестрация» = управление ожиданиями и интеграциями, маршрут остаётся в runner | F-07 |
| DEC-06 | SSOT пакета этапа 2 | Пакет Хаба (`dist/execution-package-opencode`) как источник сборки, установка в runtime; ADR-016 переписывается в профиль применения | F-06 |
| DEC-07 | Архетип и среда | `archetype: B`, `environment: local` | F-08 |
| DEC-08 | Размещение четырёх документов | `docs/vision.md`, `docs/concept.md`, `docs/architecture.md`, `docs/roadmap.md` | F-02 |
| DEC-09 | Политика разметки истории | Правило каталога + блок перехода в активных документах; датированные артефакты — исторические по умолчанию | F-10, F-16 |
| DEC-10 | Вывод локального KB-конвейера | Депрекация через стандарт Хаба после проверки потребителей | F-12 |

### Задачи и обращения

После решений исполнение идёт отдельными задачами T-01…T-09 со своими
DoD, а противоречия на стороне Хаба — обращениями H-01…H-07
([реестр](../analysis/2026-10-31-follow-up-tasks.md)). Issues этим PR не
создаются: до решения DEC-01 задача на изменение этого репозитория
противоречит действующему правилу бэклога Хаба, поэтому формулировки
подготовлены к заведению после согласования RFC.

### Отклонения этого аудита

- RFC #407 переписан, а не дополнен новым RFC: issue разрешает «изменить
  результирующие артефакты, включая RFC», а две конкурирующие версии одного
  RFC создали бы второй SSOT.
- `CHANGELOG.md` не изменяется: PR не меняет поведение промптов, стандартов
  и сайта; запись появится в задачах исполнения.
- `runs/` и `site/` не изменяются.

## Related Artifacts

- [Реестр диспозиции файлов](../analysis/2026-10-31-file-disposition-register.md)
- [Анализ эволюции требований](../analysis/2026-10-31-requirements-evolution.md)
- [Предложение по стратегическим документам](../analysis/2026-10-31-strategic-documents-proposal.md)
- [Реестр задач и обращений в Хаб](../analysis/2026-10-31-follow-up-tasks.md)
- [RFC модернизации репозитория v0.3](../rfc/2026-10-repository-modernization.md)
- Контекст issue: [инвентарь #407](../analysis/2026-10-30-repository-inventory.md),
  [этап 2 #405](../analysis/2026-10-30-ide-clients-stage-2.md),
  [текущее состояние #407](../analysis/2026-10-30-repository-current-state.md),
  [соответствие экосистеме #407](../analysis/2026-10-30-ecosystem-compliance.md),
  [эволюция октября #407](../analysis/2026-10-30-october-requirements-evolution.md)
- Предшествующий аудит структуры: [2026-08-21](2026-08-21-root-structure-audit.md)
