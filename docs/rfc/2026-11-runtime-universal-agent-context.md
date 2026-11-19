---
status: proposed
version: 0.1
updated: 2026-11-19
temperature: 0.1
owner: G-Ivan-A
source: "https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25"
related_issues: "https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25, https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/26, https://github.com/G-Ivan-A/mango_ba_prompts/issues/492, https://github.com/G-Ivan-A/mango_ba_prompts/pull/493, https://github.com/G-Ivan-A/mango_ba_prompts/issues/417"
rfc-scope: multi
type: rfc
related_artifacts: "docs/contracts/ssot-stage1-handoff-manifest.md, docs/contracts/ssot-stage1-handoff-manifest.json, experiments/issue_492/runtime-deps.md, docs/audit/2026-11-18-runtime-dependencies-ssot-handoff.md, docs/adr/2026-10-adr-016-ide-client-process.md, docs/rfc/2026-11-runtime-product-catalog-golden-set.md, pr-ops/backlog-ba-model.md, pr-ops/BACKLOG.md, scripts/validate_issue_rt25_agent_context.py"
---

# RFC-RT-002: Универсальный агентный контекст runtime (OpenCode-first)

## Summary / BLUF

Задача — [runtime #25](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25),
вход — манифест передачи SSOT этапа 1 ([#492](https://github.com/G-Ivan-A/mango_ba_prompts/issues/492),
PR #493 слит, `7611c041`). Это анализ и RFC `proposed`. Runtime не
перестраивается: ни один файл не удалён и не перемещён, тексты промптов и
навыков не написаны, SHA реестра не поднят. Аудит воспроизводится скриптом
[`tests/agent_context_audit.py`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/490188ef90e3f3a6fd600f6988cc3c1f5d6d84b4/tests/agent_context_audit.py)
в PR runtime #26, его лог —
[`tests/agent_context_audit.log`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/490188ef90e3f3a6fd600f6988cc3c1f5d6d84b4/tests/agent_context_audit.log)
(версия скрипта 0.3, далее «лог, раздел N»).

| Гипотеза владельца | Вердикт | Главный факт |
| --- | --- | --- |
| Г1. IDE-пакеты (GigaCode, Cline и др.) устарели и избыточны | **Подтверждена, уже исполнена** | Срез GigaCode удалён в `a4b1377` (2026-09-26) и записан в `discarded` манифеста компиляции; в рабочем дереве ни одного из 17 маркеров клиентов, кроме `AGENTS.md` (лог, раздел 3). Уточнение: раскладка `.agents/skills/<имя>/SKILL.md` удалена вместе со срезом, но сегодня это не пакет GigaCode, а межклиентское соглашение Agent Skills |
| Г2. Единая структура (`AGENTS.md`, `skills/`, `agents/`) применима к разным клиентам | **Подтверждена частично** | `AGENTS.md` читают нативно 8 из 9 проверенных клиентов, включая OpenCode; исключение — Gemini CLI, Claude Code — только без `CLAUDE.md`. Плоский `skills/<имя>.md` в корне **не находит ни один** клиент по умолчанию. Все 11 навыков проходят требования `<имя>/SKILL.md` без правки текста (лог, раздел 4). `agents/` не нужен |
| Г3. В репозитории есть иная устаревшая информация | **Подтверждена** | README — пакет 0.5 и метамодель 0.4 при манифесте 0.7 и 0.5; навигация БЗ в `AGENTS.md` не знает `MAP.json` и `sections_toc`; маркера `ACCESS_GAP` нет; «задачей Хаба» в защищённом `taxonomy/artifacts.yaml` (лог, разделы 4–5) |

Что RFC предлагает (решения Р-RT-1…Р-RT-9, раздел 9):

1. Корневой `AGENTS.md` остаётся единым входом. Его дополняют маркером
   `ACCESS_GAP`, маршрутом навигации README → MAP → `sections_toc` → разделы и
   ссылкой на каталог навыков. Правка идёт каналом компиляции
   `ba-ai-metamodel`, как ХАБ-1 и B-248.
2. Навыки остаются в `skills/<имя>.md` — это защищённый путь и SSOT. Рядом
   появляется **генерируемое побайтное зеркало** `.agents/skills/<имя>/SKILL.md`
   со сверкой sha256. Его находят OpenCode V1 и V2, Codex, Cursor, Copilot,
   Gemini CLI, Qwen и GigaCode на GitVerse.
3. `agents/` не вводится, пока не сработает триггер BL-132 или ADR-016.
   Адаптеров под клиентов сейчас не нужно ни одного; для клиентов вне
   OpenCode-first описаны указатели.
4. SSOT этапа 1 (133 артефакта) принимается в каталог с сохранением путей
   источника. Тогда 416 внутренних ссылок работают на побайтной копии.
   334 ссылки на файлы вне передачи не переписываются: они фиксируются картой
   ссылок в журнале передач. Так снимается противоречие правил 1, 2, 4 и
   правила 5 политики синхронизации.
5. Защищённые пути не трогаются. Правка `AGENTS.md` и README допустима только
   потому, что их потребители читают закреплённый SHA. Это проверяется
   валидаторами спицы на SHA реестра.

**Рекомендация: принять RFC и слить PR runtime #26 и PR спицы.** Производство
контекста и приём SSOT начинаются после решений Р-RT, отдельными задачами.

## 1. Постановка и границы

Режим `Creative`; постановка дополнена по стандарту выставления задач.

**Цель.** Один агентный контекст runtime для любого клиента, OpenCode — первый.
Внешние контракты этапа 1 не ломаются, и есть план безопасной миграции.

**Входы.** Runtime на `90f08233` (main до задачи) и на SHA реестра `68ad8fcf`.
Манифест передачи [`ssot-stage1-handoff-manifest.json`](../contracts/ssot-stage1-handoff-manifest.json)
и таблица защищённых путей [`runtime-deps.md`](../../experiments/issue_492/runtime-deps.md)
закреплены sha256 в скрипте аудита. Документация клиентов прочитана
2026-11-19 по первоисточникам (раздел 3).

**Выходы.** RFC, скрипт аудита, лог и сторожа в runtime, запись в реестре,
карточки бэклога, валидатор `scripts/validate_issue_rt25_agent_context.py`.

**Вне границ (раздел 5 задачи).** Изменение структуры runtime, удаление файлов,
тексты промптов и навыков, подъём SHA реестра, деплой, модельные прогоны.
Аудит сам проверяет, что ни один защищённый путь не изменён (лог, раздел 2).

**Граничные случаи и их разрешение.**

| № | Случай | Разрешение |
| --- | --- | --- |
| ГК-1 | Элемент выглядит устаревшим, но его читает потребитель этапа 1 | Защищён. Пример — `taxonomy/artifacts.yaml:2` («задачей Хаба», Г3): правка только вместе с подъёмом SHA реестра (раздел 6) |
| ГК-2 | Клиент не читает `AGENTS.md` | Тонкий адаптер-указатель без копии содержания (раздел 4.4): Gemini CLI — `context.fileName`, Claude Code при наличии `CLAUDE.md` — импорт `@AGENTS.md` |
| ГК-3 | ФТ-2 требует правки `AGENTS.md`, а это защищённый путь ФТ-4 | У `AGENTS.md` и `README.md` единственный тип ссылки — «SHA (иной срез)», то есть закреплённый коммит. Правка на main не меняет байты на закреплённом SHA. Пути, которые читаются с `main` или из клона (`/`, `docs/kb/MAP.json`, `docs/kb/README.md`, `docs/kb/USAGE.md`, `taxonomy/products.yaml`, `taxonomy/mango-products.yaml`, `golden/cases.yaml`), не правятся вовсе |
| ГК-4 | Побайтная копия SSOT нарушает smoke runtime: 7 файлов `.json`, 1 файл со словом среды | Каталог SSOT исключается из проверок слов и расширений, как `docs/kb` (Р-RT-4). Слово `tools/validate` в `golden-set-bcreq-stage1.md` — ссылка на валидатор спицы, а не срез среды |
| ГК-5 | Правило 5 политики (переписать ссылки) противоречит правилам 1, 2, 4 (побайтно, без правок, равенство sha256) | Карта ссылок в журнале передач, без переписывания (Р-RT-7) |
| ГК-6 | Сценарного навыка «оценка ТТЗ» нет в манифесте: артефактов ТТЗ в 133 нет | Навык ждёт новой закреплённой передачи с артефактами ТТЗ. Это не пробел этого RFC (раздел 4.2) |
| ГК-7 | Зеркало навыков дублирует содержание | Зеркало генерируется, не правится руками и сверяется по sha256 с `skills/`. Источник один, копия — вид, а не второй источник (Р-RT-3) |
| ГК-8 | В репозиторий попадают клиентские данные | Аудит читает только пути, версии и хэши. Манифест запрещает `runs/`, `kb/`, `inputs/`, `attachments/` |
| ГК-9 | Источник недоступен или платный | Помечается `UNVERIFIED` или `ACCESS_GAP` (раздел 3), вывод на нём не строится |

## 2. Аудит As-Is (ФТ-1)

### 2.1. Инвентаризация

Лог, раздел 1: 7008 отслеживаемых файлов на `567d3783` (из них 6931 в
`docs/kb`). Таблица ниже — сокращение. Хэш дерева и байты по каждому элементу
есть в логе.

| Элемент | Назначение | Потребитель | Актуальность к SSOT | Дублирование |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | системный промпт маршрута RG-BCREQ-v1, единый вход модели | модель; валидатор спицы (SHA иного среза) | 0.7 от 2026-11-17; нет `ACCESS_GAP`, навигация БЗ устарела (Г3) | нет |
| `README.md` | вход человека | человек; валидатор (SHA иного среза) | 0.5 и метамодель 0.4 при манифесте 0.7 и 0.5 (Г3) | частично повторяет `AGENTS.md` (состав каталогов) |
| `compilation-manifest.yaml` | происхождение пакета: copied / transformed / discarded; канал обратной связи | человек; `tests/test_source_pin.py` | актуален (0.7) | нет |
| `skills/` (11) | навыки узлов маршрута | модель; валидатор (SHA иного среза) | 10 навыков — слой `meta_model` 0.3 (`60c224b3`), 1 — 0.5 (`657abccc`), манифест 0.5 (Г3, за пределами этой задачи) | нет |
| `contracts/` (5) | контракты C-IN, C-CORE, C-QUEST, C-OUT-BCREQ, C-RK | модель; валидатор | 4 из 5 с `updated` раньше компиляции 2026-11-04 | нет |
| `routes/`, `templates/`, `golden/`, `evaluation/`, `taxonomy/` | маршрут, скелеты, Golden Set, гейты, словари | модель; валидатор, сайт этапа 1 | защищены (ФТ-4) | нет |
| `docs/kb` | база знаний ST-5-LOCAL | модель; валидатор, сайт этапа 1 | защищена; `MAP.json`, `README.md`, `USAGE.md` читаются с `main` | нет |
| `docs/guides` | инструкции пользователя | человек | без версий во frontmatter | нет |
| `tests/`, `.github/` | smoke, unittest, этот аудит | CI | актуальны | нет |
| IDE-пакеты | — | — | **отсутствуют** (2.2) | — |
| `agents/` | — | — | **отсутствует** | — |

### 2.2. Г1: IDE-специфичные пакеты

- Ни одного из маркеров `CLAUDE.md`, `.claude`, `GEMINI.md`, `.gemini`,
  `.opencode`, `opencode.json(c)`, `.agents`, `.hub-profile.json`,
  `.clinerules`, `.cursor`, `.cursorrules`, `.windsurf(rules)`,
  `.github/copilot-instructions.md`, `.github/instructions`, `.qwen`,
  `.gigacode`, `QWEN.md` в рабочем дереве нет (лог, раздел 3).
- Срез GigaCode удалён коммитом
  [`a4b1377`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/commit/a4b13770336e27c8a3211d4707b301d69618dbd5)
  «restructure runtime as environment-neutral repository for model chats»:
  “drop GigaCode slice: .hub-profile.json, tools/, runs/, experiments/”.
  Манифест компиляции, раздел `discarded`: “срез под конкретную среду
  исполнения (.hub-profile.json, .agents/skills/, tools/, runs/, experiments/)”.
- Возврат среза сторожит `tests/runtime-smoke.sh`: `.agents`, `.hub-profile.json`,
  `tools`, `runs`, `experiments` должны отсутствовать. Новый сторож
  `test_no_client_package_without_decision` не пропустит пакет клиента без решения.
- Упоминания клиентов вне `docs/kb` есть только в `tests/` (сторожа и аудит).
  36 упоминаний в `docs/kb` — продуктовая база знаний, а не конфигурация клиента.

**Вердикт:** подтверждена. Пакеты не просто устарели — их уже нет, вывод
исполнен (раздел 7). Уточнение к гипотезе: из удалённого `.hub-profile.json` и
`tools/` действительно привязаны к среде. А раскладка
`.agents/skills/<имя>/SKILL.md` с 2026 года — общий путь спецификации Agent
Skills: “The `.agents/skills/` paths have emerged as a widely-adopted
convention for cross-client skill sharing”
([agentskills.io, adding-skills-support](https://agentskills.io/client-implementation/adding-skills-support)).
Это основание Р-RT-3.

### 2.3. Г2: единый вход и каталоги

- `AGENTS.md` — 12 070 байт, ниже предела Codex `project_doc_max_bytes` 32 KiB.
  Есть запрет имитации чтения (`unverified`) и правило цитирования «локатор +
  дословная цитата». Нет маркера `ACCESS_GAP` и маршрута README → MAP →
  `sections_toc` (лог, раздел 4).
- 11 навыков в плоской раскладке `skills/<имя>.md`. У каждого есть `version`,
  `compiled_from.source_commit`, `derived_from`, `compiled_at` — версия и
  происхождение уже есть.
- Совместимость с `<имя>/SKILL.md` (лог, раздел 4): у всех 11 `name` равен имени
  файла и проходит шаблон `[a-z0-9]+(-[a-z0-9]+)*`, `description` — от 149 до
  226 символов, длина — от 71 до 94 строк. **Пригодны без правки текста:
  11 из 11.** Сторож — `test_skills_fit_agent_skills_mirror`.
- Плоский `skills/` в корне не находит ни один проверенный клиент (раздел 3).
  OpenCode V2 найдёт его только с `"skills": ["./skills"]` в `opencode.json`.
  OpenCode V1, который ADR-016 называет предпочтительным профилем, плоскую
  форму не поддерживает вовсе.

**Вердикт:** подтверждена частично. Единый `AGENTS.md` применим уже сейчас,
каталог навыков — после зеркала или переноса (Р-RT-3). `agents/` не нужен
(раздел 4.3).

### 2.4. Г3: иная устаревшая информация

| Находка | Где | Почему устарело | Как исправлять |
| --- | --- | --- | --- |
| Версия пакета и метамодели | `README.md`: «MVP BCREQ 0.5», `meta_model_version: 0.4` | манифест компиляции 0.7, метамодель 0.5 | задача runtime по образцу РТ-7 (Р-RT-2) |
| Навигация БЗ | `AGENTS.md`: только `index.md → sections/` | README базы и `docs/kb/USAGE.md` после РТ-7 (`105b275`) ведут MAP.json → `sections_toc` → разделы | канал компиляции (Р-RT-2) |
| Нет `ACCESS_GAP` | `AGENTS.md` | ФТ-2 требует явного маркера недоступности | канал компиляции (Р-RT-2) |
| «Задачей Хаба» | `taxonomy/artifacts.yaml:2` | источник модели — `ba-ai-metamodel` с `3ec1a6a` (B-248) | защищённый каталог: только с подъёмом SHA реестра (ГК-1) |
| «До выноса — Хаб» | `AGENTS.md:14`, `evaluation/validate-package.md` (4 строки) | исторические пояснения, не устаревшие нормы | не править |
| Слой `meta_model` 0.3 у 10 навыков | `skills/*.md` | манифест 0.5 | перекомпиляция — задача `ba-ai-metamodel`, вне этого RFC |
| `updated` раньше компиляции | 4 контракта, `evaluation/g-human-checklist.md` (гейт типа `человек`), 2 шаблона `templates/` | не перевыпущены после 2026-11-04 | сигнал, а не дефект: содержание могло не меняться; проверка — при перекомпиляции |

**Вердикт:** подтверждена.

## 3. Индустриальные источники и матрица совместимости клиентов

Все факты сняты 2026-11-19 с первоисточников. Цитаты дословные.

- **AGENTS.md** ([agents.md](https://agents.md/)): “AGENTS.md is just standard
  Markdown”; “The closest AGENTS.md to the edited file wins”. Стандарт ведёт
  Agentic AI Foundation (Linux Foundation).
- **Agent Skills** ([agentskills.io/specification](https://agentskills.io/specification)):
  “A skill is a directory containing, at minimum, a `SKILL.md` file”.
  - `name`: “Must be 1-64 characters”, “Must match the parent directory name”.
  - `description`: “Must be 1-1024 characters”.
  - “Keep your main `SKILL.md` under 500 lines”.
  - Прогрессивная загрузка: метаданные → инструкции → ресурсы.
- **OpenCode.** Репозиторий [anomalyco/opencode](https://github.com/anomalyco/opencode);
  выпуски v2.3.2 (2026-11-18) и v1.19.6 (2026-11-17). Документация описывает V2.
  - [rules](https://opencode.ai/docs/rules/): AGENTS.md ищется от рабочего
    каталога до корня проекта, вложенные файлы подгружаются; “OpenCode
    combines the files and does not resolve conflicts between them”.
    Резерв — `CLAUDE.md`.
  - [skills](https://opencode.ai/docs/skills/): пути `.opencode/skills`,
    `.claude/skills`, `.agents/skills`; “Markdown files must be at the source
    root”; дополнительные каталоги — массивом `skills` в `opencode.json`.
  - [V1 skills](https://github.com/anomalyco/opencode/blob/dev/services/site/src/docs/v1/content/skills.mdx):
    `name` и `description` обязательны, `name` совпадает с каталогом,
    поддерживается только `<имя>/SKILL.md`.
  - [agents](https://opencode.ai/docs/agents/): `.opencode/agents/<имя>.md`,
    режимы `primary`, `subagent`, `all`.
  - `/init` — “guided AGENTS.md setup”
    ([command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/plugin/command.ts)).

| Клиент | Читает `AGENTS.md` | Пути навыков проекта | Адаптер при раскладке Р-RT-3 B | `/init` пишет | Источник |
| --- | --- | --- | --- | --- | --- |
| OpenCode V2 | да, до корня, с вложенными | `.opencode/skills`, `.claude/skills`, `.agents/skills` | не нужен | `AGENTS.md` | [rules](https://opencode.ai/docs/rules/), [skills](https://opencode.ai/docs/skills/) |
| OpenCode V1 | да | только `<имя>/SKILL.md` | не нужен | `AGENTS.md` | [v1 skills.mdx](https://github.com/anomalyco/opencode/blob/dev/services/site/src/docs/v1/content/skills.mdx) |
| GigaCode на GitVerse | да: “Файл `AGENTS.md` в корне репозитория — это то, что он читает всегда” | `.agents/skills` | не нужен (агенты — `.opencode/agent`) | `AGENTS.md` | [repository-setup](https://gitverse.ru/docs/ai/ai-development/repository-setup), [skills](https://gitverse.ru/docs/ai/ai-development/skills), [agents](https://gitverse.ru/docs/ai/ai-development/agents) |
| Codex | да, предел 32 KiB | `.agents/skills` | не нужен | `AGENTS.md`, существующий не меняет | [agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [skills](https://learn.chatgpt.com/docs/build-skills) |
| Cursor | да, корень и подкаталоги | `.agents`, `.cursor`, `.claude`, `.codex` | не нужен | — | [rules](https://cursor.com/docs/context/rules), [skills](https://cursor.com/docs/context/skills) |
| GitHub Copilot | да: “the nearest `AGENTS.md` file … will take precedence” | `.github`, `.claude`, `.agents` | не нужен | — | [repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions), [skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Qwen Code | да, по умолчанию `QWEN.md` и `AGENTS.md` | `.qwen`, `.agents` | не нужен | `QWEN.md` | [memory-constants.ts](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/utils/memory-constants.ts), [skills.md](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/skills.md) |
| Gemini CLI | **нет**, по умолчанию `GEMINI.md`; `AGENTS.md` — через `context.fileName` | `.gemini`, `.agents` | указатель `.gemini/settings.json` (ГК-2) | `GEMINI.md` | [gemini-md](https://geminicli.com/docs/cli/gemini-md/), [memoryTool.ts](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/tools/memoryTool.ts) |
| Claude Code | да, только если нет `CLAUDE.md` (v2.1.277+) | только `.claude/skills` | зеркало `.claude/skills` — только по решению | `CLAUDE.md` | [memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills) |
| Cline | да | `.cline/skills`, `.clinerules/skills`, `.claude/skills` | зеркало — только по решению | — | [rules](https://docs.cline.bot/customization/cline-rules), [skills](https://docs.cline.bot/customization/skills) |
| GigaCode IDE и CLI | `ACCESS_GAP`: публичной документации о файлах контекста нет | `ACCESS_GAP` | не определяется | `ACCESS_GAP` | [ai-assistant-gigacode](https://gitverse.ru/docs/ai/ai-assistant-gigacode) молчит |
| Kilo, Roo | да, по списку agents.md | `UNVERIFIED` | `UNVERIFIED` | `UNVERIFIED` | [agents.md](https://agents.md/) |

Непроверенное:

- Движок GigaCode на GitVerse как OpenCode V1 — **вывод**, сделанный по
  каталогу `.opencode/agent`, а не факт.
- Замена Gemini CLI на Antigravity CLI для бесплатного тарифа — пересказ
  инструмента чтения, дословной цитаты нет.
- Какие поверхности Copilot читают `AGENTS.md` — `UNVERIFIED`.
- Cline, Kilo, Qwen и GigaCode не входят в список внедривших Agent Skills
  ([clients.jsx](https://github.com/agentskills/agentskills/blob/main/docs/snippets/clients.jsx)).

## 4. Целевая архитектура (ФТ-2)

```text
AGENTS.md                          единый вход (защищён; правка — Р-RT-2)
skills/<имя>.md                    SSOT навыков (защищён, не перемещается)
.agents/skills/<имя>/SKILL.md      генерируемое побайтное зеркало (Р-RT-3 B)
ssot/mango_ba_prompts/<путь>       закреплённая копия SSOT этапа 1 (Р-RT-6)
ssot/mango_ba_prompts/TRANSFERS.md журнал передач и карта ссылок (Р-RT-7)
contracts/ routes/ taxonomy/ templates/ golden/ evaluation/ docs/   без изменений
```

Имена `ssot/…` и `TRANSFERS.md` — предложение, их выбирает Р-RT-6.

### 4.1. `AGENTS.md`: требования, а не текст

Текст `AGENTS.md` — нормативное содержание. Его производит канал компиляции
(Р-RT-2), а не этот RFC. Требования к следующей версии:

1. **Роль** — сохраняется: системный промпт маршрута RG-BCREQ-v1.
2. **Provenance и цитирование** — сохраняются: «локатор + дословная цитата»,
   запрет имитации чтения. Добавляется ссылка на журнал передач SSOT как
   источник версии и sha256 перенесённых норм.
3. **`ACCESS_GAP`** — новый явный маркер. Источник недоступен, платный или
   ссылка ведёт за пределы runtime (карта ссылок, Р-RT-7) → модель пишет
   `ACCESS_GAP: <что> — <почему>` и не выводит содержание. Отличие от
   `unverified`: тот помечает непроверенное утверждение, а `ACCESS_GAP` —
   недоступный источник.
4. **Навигация БЗ** — README базы → `MAP.json` → `sections_toc`
   (`maps/<doc>.toc.tsv`) → целевые разделы → `retrieval_if_insufficient`.
   Это маршрут `docs/kb/USAGE.md` после РТ-7. Сейчас `AGENTS.md` расходится с ним (Г3).
5. **Каталог навыков** — путь к `skills/` как SSOT и к зеркалу, правило
   «навык открывается на своём узле» без изменений.
6. **Размер** — не больше 32 KiB, предел Codex. Сейчас 12 070 байт.

### 4.2. Каталог `skills/`

- **Навыки маршрута** — 11 существующих. Версия и происхождение уже есть
  (`version`, `compiled_from`, `derived_from`, `compiled_at`). Этот RFC их
  не меняет.
- **Сценарные навыки** — потребители перенесённого SSOT. Кандидаты на
  производство после приёма SSOT и Р-RT-8:
  - исполнение A-IN по маршруту `bcreq-a-in-route.json` и 24 контрактам AIN;
  - исполнение шагов потока BCREQ по базовому стандарту и каталогу операций;
  - оценка ТТЗ — после новой передачи с артефактами ТТЗ (ГК-6).
- **Обязательные поля сценарного навыка.** `name` равен каталогу, длина
  1–64; `description` — 1–1024 символа; `version`; `source_transfer` — запись
  журнала передач; `source_commit` спицы; sha256 каждого перенесённого
  артефакта, на который ссылается навык. Это продолжение полей `compiled_from`
  навыков маршрута.

### 4.3. `agents/`: не вводится

Отдельный агент в OpenCode нужен только для другой роли или другого набора
разрешений (`.opencode/agents/<имя>.md`, режимы `primary`, `subagent`, `all`).
В маршруте RG-BCREQ-v1 одна роль. Гейты `G-mach` и `G-human` (гейт типа `человек`) описаны
промптами `evaluation/`, отдельный субагент им не нужен. Кандидат на агента
один — независимый рецензент ADR-016 с иными правами. Он появится, когда
BL-132 закрепит версию OpenCode и проверит P01–P08. Это триггер Р-RT-5.

### 4.4. Тонкие адаптеры

| Клиент | Нужен ли | Что именно | Обоснование |
| --- | --- | --- | --- |
| OpenCode V1, V2 | нет | — | читает `AGENTS.md` и `.agents/skills` нативно |
| GigaCode на GitVerse, Codex, Cursor, Copilot, Qwen | нет | — | то же |
| Gemini CLI | только при использовании | `.gemini/settings.json` с `context.fileName: ["AGENTS.md"]` | не читает `AGENTS.md` по умолчанию (ГК-2); файл `.json` требует поправки smoke |
| Claude Code | только при использовании | `CLAUDE.md` с одной строкой `@AGENTS.md`, если `CLAUDE.md` нужен; иначе ничего. Навыки — зеркало в `.claude/skills` | навыки читает только из `.claude/skills` |
| Cline | только при использовании | зеркало в `.claude/skills` (общее с Claude Code) | `.agents/skills` не в списке путей |

Адаптер — указатель или генерируемое зеркало, а не второй пакет. Ни один
адаптер не вводится без решения владельца по конкретному клиенту.

## 5. Приём SSOT этапа 1 (ФТ-3)

**Что принимается.** 133 артефакта манифеста на `source_commit` `7dea8f71`.
По карточкам переноса: BL-185 — 38, BL-186 — 31, BL-187 — 62, BL-188 — 2.
24 контракта AIN (`prompts/drafts/a-in/`). sha256 совпадает у 133 из 133 — пересчитано по клону спицы
(лог, раздел 6).

**Куда.** Каталог с сохранением путей источника, например
`ssot/mango_ba_prompts/docs/ba-processes/…` (Р-RT-6). Сохранение путей
оставляет рабочими **416 внутренних ссылок** между перенесёнными файлами
без единой правки байтов.

**Как.**

1. Побайтная копия, закреплённая на `source_commit` (правило 1).
2. Копия манифеста передачи рядом и запись в журнале передач. Поля записи:
   номер передачи, `source_commit`, sha256 манифеста, число артефактов,
   карточка BL, коммит runtime.
3. Сторож runtime: sha256 каждого файла равен значению манифеста (правило 4).
   Локальные правки ловит этот же сторож (правило 2).
4. Обновление — только новой передачей с новым манифестом (правило 3).
5. Все четыре карточки принимаются **одной передачей**. Ссылки между ними
   взаимные: BL-187 → BL-185 — 92, BL-188 → BL-187 — 15, BL-187 → BL-188 — 10,
   остальные пары — от 1 до 6 (подсчёт по `source_commit`). При приёме по
   карточкам любой порядок оставляет ссылки битыми между коммитами. Карточки
   BL-185…BL-188 остаются чек-листами приёмки внутри одной передачи.

**Ссылки (Р-RT-7).** В 126 перенесённых `.md` (лог, раздел 6):

- 805 абсолютных и якорных ссылок;
- 416 ссылок внутри передачи;
- **334 ссылки на существующие файлы спицы вне передачи**, в 64 файлах.
  По каталогу цели: `docs` 214, `runs` 49, `standards` 31, `experiments` 17,
  `pr-ops` 8, `scripts` 6, `prompts` 5, `site` 2, `tools` 1, `README.md` 1.

Правило 5 политики велит их переписать, но тогда файл перестаёт быть
побайтной копией, и правила 1, 2, 4 нарушаются. Прецедент
`scripts/sync_from_hub.py` переписывает ссылки, но и не обещает побайтности.

Рекомендация — **вариант 7а**:

- байты не трогаются;
- в журнале передач — карта ссылок «файл → ссылка → permalink спицы на
  `source_commit`»;
- `AGENTS.md` велит модели на ссылке вне runtime ставить `ACCESS_GAP` или
  брать permalink из карты.

Нормативные цели (класс (б) по #492) не попадают в карту. Они входят в
следующую передачу, поэтому требование «нормативные ссылки для внешнего
чтения ведут только на runtime» выполняется. Классификация 334 ссылок на (а)
и (б) — первый шаг задачи приёма. Она переиспользует правила А-0…А-6 и
Б-1…Б-7 из `classify_prompt_links.py`.

**Вариант 7б** — переписывание по правилу 5 с двумя sha256 в журнале
(источник и runtime). Он отвергается: проверка «равенство sha256 манифесту»
перестаёт быть простой, а локальная правка становится неотличима от
переписывания.

**Совместимость со smoke runtime.** Копия как есть нарушает две проверки
(лог, раздел 6):

- 7 файлов `.json` — `bcreq-a-in-route.json`, `bcreq-a-in-instructions.json`,
  `catalog.json`, `lessons.json`, `coverage.json`, два `manifest.json`;
- 1 срабатывание слов среды.

Запретов внешних баз и битых ссылок формы `contracts|skills|…/x.md` нет.
Решение — Р-RT-4.

## 6. Обратная совместимость (ФТ-4)

- Каталоги `docs/kb`, `taxonomy/`, `templates/`, `golden/`, `evaluation/` и
  26 защищённых путей #492 не меняются. Этот PR — 0 изменений относительно
  `90f08233` (лог, раздел 2, дайджесты каталогов). Сторож
  `test_protected_paths_exist` не даст их переместить.
- Различие типов потребителей определяет, что можно делать дальше (ГК-3):
  - пути, читаемые с `main`, из клона или как корень, неизменны до отдельного
    плана миграции;
  - пути, читаемые по закреплённому SHA, можно править на main — закреплённые
    ссылки продолжают работать.
- Между SHA реестра `68ad8fcf` и main уже есть одно расхождение —
  `evaluation/validate-package.md`. Его потребитель — валидатор по «SHA (иной
  срез)», а не по SHA реестра, поэтому ничего не ломается. Это расхождение
  будет учтено при следующем подъёме SHA.
- Подъём SHA реестра — отдельный контролируемый шаг спицы, не в этом RFC. На
  нём же правится «задачей Хаба» в `taxonomy/artifacts.yaml` (ГК-1).
- Перемещение `skills/` (вариант Р-RT-3 C) — только отдельным планом миграции.
  Генератор сайта и промпты спицы должны правиться синхронно с ним.

## 7. Вывод legacy из эксплуатации (ФТ-5)

Действующих IDE-пакетов нет: вывод исполнен в `a4b1377`. Ниже — соответствие
«удалено → чем заменено». Это и есть tombstone. Его носители:

- раздел `discarded` манифеста компиляции;
- коммит `a4b1377`;
- история git до него ([`6d8b5e9`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/6d8b5e9c07178f7ec7abae13fcafade9d18ac070)).

Информация не потеряна: удалённые файлы читаются на этом SHA.

| Удалено в `a4b1377` | Чем заменено | Потеря информации |
| --- | --- | --- |
| `.agents/skills/<имя>/SKILL.md` (11) | `skills/<имя>.md` — переименование git; 5 из 11 без правок, у 6 правки от 2 до 8 строк | нет |
| `contracts/*.schema.json` (5) | `contracts/*.md`: «имя до точки и структура полей сохранены из JSON Schema версии 0.4» (`transformed`) | нет; схемы — в истории |
| `tools/validate-package.py`, `.sh` | `evaluation/validate-package.md`: «порядок проверок сохранён» | исполняемая проверка стала промптом, решение `a4b1377` |
| `.hub-profile.json` | раздел `deployment` манифеста компиляции | нет |
| `docs/guides/01-repository-setup.md`, `04-running-tasks.md` | `docs/guides/00-quick-start.md` | инструкции под GigaCode, по назначению устарели |
| `experiments/source-audit/*`, `runs/.gitkeep` | — (материал получения правил, `discarded`) | в истории |

Срок и условие удаления: удалять нечего. Если Р-RT-3 B принят, `.agents/skills/`
возвращается **как зеркало**, а не как срез среды. Тогда запись `discarded`
уточняется при следующей компиляции: срезом остаются `.hub-profile.json`,
`tools/`, `runs/`, `experiments/`.

## 8. Миграция, валидация и откат (ФТ-6)

Оценки трудозатрат — **гипотезы**. Они не измерены и даны в
человеко-днях исполнителя с доступом к обоим репозиториям.

| Этап | После решения | Что делается | Где | Оценка (гипотеза) | Откат |
| --- | --- | --- | --- | --- | --- |
| Э0 | — | принять RFC, слить PR runtime #26 и PR спицы | обе | 0 | revert PR |
| Э1 | Р-RT-3, Р-RT-4 | генератор зеркала `.agents/skills/` в `tests/`, сторож sha256 зеркала, поправка smoke | runtime | 0,5 | revert; зеркало генерируемое, удаляется без потерь |
| Э2 | Р-RT-2 | `AGENTS.md`: `ACCESS_GAP`, навигация, ссылка на навыки — компиляция `ba-ai-metamodel`; README — задача runtime | `ba-ai-metamodel`, runtime | 0,5–1 | revert; потребители читают закреплённый SHA |
| Э3 | Р-RT-6, Р-RT-7 | классификация 334 ссылок, приём BL-185…BL-188 одной передачей, журнал передач и карта ссылок, сторож sha256 | runtime | 2–3 | revert коммита передачи; спица не меняется |
| Э4 | Р-RT-8, BL-132 | smoke инициализации в закреплённой версии OpenCode | runtime, отчёт в спице | 0,5 | не меняет файлов |
| Э5 | Р-RT-8 | сценарные навыки (BL-131) | runtime | вне RFC: BL-131 | revert |
| Э6 | отдельно | подъём SHA реестра и правка ссылок промптов (BL-190) | спица | вне RFC | revert строки реестра |

**Валидация на каждом этапе.**

- runtime: `tests/runtime-smoke.sh`, `python3 -m unittest discover -s tests`,
  `tests/agent_context_audit.py --base <SHA до этапа>` — 0 изменений в
  защищённых каталогах;
- спица: `validate_issue_430_runtime_refs.py` и
  `validate_issue_434_runtime_tasks.py` с `RUNTIME_CLONE` на SHA реестра
  (закреплённые ссылки целы) и на кандидате для подъёма;
  `node scripts/generate-pages-data.mjs` — без изменений, кроме `generatedAt`;
  `make validate-full`.

Базовая линия этой задачи — раздел «Проверки» ниже.

**Smoke OpenCode (Э4).** Дешёвый шаг без модельного прогона маршрута:

- клиент запускается в клоне runtime на закреплённой версии;
- проверяется, что `AGENTS.md` загружен и 11 навыков видны в списке со своими
  `description` (V2: ID по пути; V1: `name` равен каталогу).

Точная команда вывода списка навыков без обращения к модели —
`UNVERIFIED`, её фиксирует BL-132. Если такой команды нет, достаточно одного
короткого запроса «перечисли навыки». Это не прогон маршрута.

## 9. Решения на согласование

| № | Вопрос | Рекомендация | Почему | Если промолчать |
| --- | --- | --- | --- | --- |
| Р-RT-1 | Принять RFC; место RFC — реестр спицы, аудит — `tests/` runtime | **Принять** | Прецедент RFC-RT-001. Runtime не хранит организационных материалов (`discarded`), а задача запрещает менять его структуру | принято при слиянии PR |
| Р-RT-2 | Канал правки `AGENTS.md` и README | **`AGENTS.md` — компиляция `ba-ai-metamodel`; README — задача runtime** | `feedback` манифеста компиляции: «правка нормативного содержания в спутнике — дефект процесса». Прецеденты: `AGENTS.md` — ХАБ-1 (`09cc684`) и B-248 (`3ec1a6a`); README — РТ-7 (`105b275`) | Г3 остаётся, `ACCESS_GAP` нет |
| Р-RT-3 | Раскладка навыков: A — `opencode.json` с `"skills": ["./skills"]`; B — зеркало `.agents/skills/<имя>/SKILL.md`; C — перенос | **B** | B работает в OpenCode V1 и V2, на GitVerse и в 5 других клиентах; 11 из 11 навыков пригодны без правки. A — только OpenCode V2, это файл `.json`. C ломает защищённый путь. Симлинки ненадёжны на Windows, а пилот Хаба — Windows 10/11 | навыки видны только по явной ссылке из `AGENTS.md` |
| Р-RT-4 | Поправка `tests/runtime-smoke.sh` | **Разрешить** `.agents/skills/` как зеркало и каталог SSOT; каталог SSOT исключить из проверок слов и расширений, как `docs/kb` | Без поправки зеркало и приём SSOT невозможны (ГК-4). Сторожа среза (`.hub-profile.json`, `tools`, `runs`, `experiments`) остаются | Э1 и Э3 заблокированы |
| Р-RT-5 | Каталог агентов | **Не вводить**; триггер — BL-132 или рецензент ADR-016 | Одна роль маршрута; агент нужен только для другой роли или прав | не вводится |
| Р-RT-6 | Каталог приёма SSOT | **`ssot/mango_ba_prompts/` с путями источника** и журналом передач | 416 внутренних ссылок работают без правки байтов; имя показывает источник | BL-185…BL-188 без места |
| Р-RT-7 | Ссылки вне передачи (334) | **7а: карта ссылок**, нормативные цели — следующей передачей; правило 5 политики #492 уточнить в манифесте 0.2 | Сохраняет правила 1, 2, 4 и требование ФТ-3 о нормативных ссылках | противоречие политики остаётся у исполнителя BL-185 |
| Р-RT-8 | Связь с BL-131 (Р-06) и версией OpenCode (BL-132) | **Runtime — единственный источник контекста этапа 2.** Пакет Хаба (Спринт 28) ссылается на runtime по SHA; Р-06 решает владелец | Два пакета разойдутся — довод BL-131. Раскладка B не зависит от выбора V1 или V2 | BL-131 без источника |
| Р-RT-9 | Адаптеры под клиентов | **Не вводить сейчас**; по решению на клиента — указатели раздела 4.4 | OpenCode-first адаптеров не требует | не вводятся |

## 10. Движение по бэклогу

Таблица ведётся в [`pr-ops/BACKLOG.md`](../../pr-ops/BACKLOG.md), блок
«Движение по цепочке (runtime #25)». Кратко:

- **Предыдущий шаг.** BL-184 → `DONE`: PR #493 слит (`7611c041`), RFC-задача
  runtime — [#25](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25).
- **Текущий шаг.** BL-191 (этот RFC) — `review` до слияния PR.
- **Открывает.**
  - BL-192 — производство универсального контекста (Э1, Э2, Э4), `deferred
    (triggered)`, триггер — решения Р-RT-2…Р-RT-4.
  - BL-185…BL-188 остаются `TODO`; их вход — Р-RT-6 и Р-RT-7.
  - BL-189, BL-190, BL-131 и BL-132 не меняют статуса; сценарные навыки идут
    в BL-131 (Р-RT-8), версию OpenCode закрепляет BL-132.
- **Миграция защищённых путей** (вариант C, подъём SHA) — отдельная
  согласованная задача, не открывается без решения.

## 11. Пределы

- Документация клиентов меняется быстро: последние выпуски линий OpenCode
  V1 (v1.19.6) и V2 (v2.3.2) вышли 17 и 18 ноября 2026. Матрица верна на 2026-11-19. Перед Э4 её надо
  перепроверить на закреплённой версии.
- Поведение GigaCode IDE и CLI — `ACCESS_GAP`; Kilo и Roo — `UNVERIFIED`.
- Оценки — гипотезы, без замеров.
- Классификация 334 ссылок на (а) и (б) не сделана — это первый шаг Э3.
- Аудит статический, модельных прогонов не было.

## Проверки

| Проверка | Где | Результат |
| --- | --- | --- |
| `tests/agent_context_audit.py --base 90f0823 --deps … --handoff … --stage1-repo …` | runtime | встроенные сводки совпали с клоном спицы; 0 изменений защищённых каталогов |
| `python3 -m unittest discover -s tests`; `tests/runtime-smoke.sh` | runtime | 52 теста OK; smoke passed |
| `validate_issue_430_runtime_refs.py`, `validate_issue_434_runtime_tasks.py`, `validate_issue_492_ssot_handoff.py` с `RUNTIME_CLONE` на `68ad8fcf` | спица | 73 теста OK, 1 пропущен (нет `HUB_CLONE`) |
| `node scripts/generate-pages-data.mjs` | спица | код 0; изменился только `generatedAt` |
| `scripts/validate_issue_rt25_agent_context.py`, `make validate-full` | спица | 0 провалов |

## Operating Mode

- `Creative`: режим задан issue runtime #25. Статус `accepted` ставит только владелец.

## Специфика работы с Конардом

- **молчание = согласие:** если Пользователь мержит PR без комментариев, решения приняты;
- **комментарий + ручной перезапуск:** доработка в том же PR;
- **close:** закрытие PR означает отказ от решения;
- draft PR используется как место отложенной проверки до acceptance.

## Обоснованные обходы

- RFC лежит в спице, а не в runtime. Задача запрещает менять структуру runtime,
  а runtime не хранит организационных материалов. Прецедент — RFC-RT-001.
- В runtime добавлены только файлы в существующий каталог `tests/`: скрипт,
  лог, сторожа. Структура не изменена, smoke проходит.

## Related Artifacts

- [Runtime #25](https://github.com/G-Ivan-A/mango-ba-ai-runtime/issues/25), [PR runtime #26](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/26)
- [Скрипт аудита](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/490188ef90e3f3a6fd600f6988cc3c1f5d6d84b4/tests/agent_context_audit.py), [лог](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/490188ef90e3f3a6fd600f6988cc3c1f5d6d84b4/tests/agent_context_audit.log), [сторожа](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/490188ef90e3f3a6fd600f6988cc3c1f5d6d84b4/tests/test_agent_context_audit.py)
- [Манифест передачи SSOT](../contracts/ssot-stage1-handoff-manifest.md), [аудит #492](../audit/2026-11-18-runtime-dependencies-ssot-handoff.md), [защищённые пути](../../experiments/issue_492/runtime-deps.md)
- [RFC-RT-001](2026-11-runtime-product-catalog-golden-set.md), [ADR-016](../adr/2026-10-adr-016-ide-client-process.md)
- [BL-131](../../pr-ops/backlog-ba-model.md#bl-131-пакет-этапа-2-для-opencode-из-одного-источника), [BL-132](../../pr-ops/backlog-ba-model.md#bl-132-квалификация-закреплённой-версии-opencode-по-p01p08), [BL-184](../../pr-ops/backlog-ba-model.md#bl-184-аудит-зависимостей-от-runtime-и-манифест-передачи-ssot-этапа-1), [BL-191](../../pr-ops/backlog-ba-model.md#bl-191-rfc-универсального-агентного-контекста-runtime), [BL-192](../../pr-ops/backlog-ba-model.md#bl-192-производство-универсального-агентного-контекста-runtime)
- [Валидатор](../../scripts/validate_issue_rt25_agent_context.py)
