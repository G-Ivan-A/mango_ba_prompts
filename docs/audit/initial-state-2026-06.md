---
status: draft
version: 0.1
updated: 2026-06-02
ai-generated: true
type: audit
scope: mango_ba_prompts-bootstrap
based_on: "hybrid-Intelligence-lab/templates/spoke/"
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/4"
---

# Аудит и план миграции `mango_ba_prompts` (2026-06)

> ⚠️ **Это RFC-отчёт на Human Review, а не реализация.** В рамках issue #4
> действует стоп-фактор: физическое создание governance-файлов и перенос
> промптов **не выполняется** до утверждения этого плана человеком. Документ
> фиксирует аудит, предлагает точный список файлов из «ДНК-шаблона» Хаба и
> описывает пошаговый план миграции с нормализацией.

**Operating Mode**: `Project` — фокус на практической применимости для этого
конкретного репозитория, без усложнения структуры «ради красоты»
(Anti-Inflation principle Хаба).

**Источник стандартов (Хаб)**:
[`hybrid-Intelligence-lab/templates/spoke/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/templates/spoke)

---

## 1. Аудит текущего состояния

### 1.1. Что лежит в репозитории сейчас

| Путь | Что это | Замечание |
| :--- | :--- | :--- |
| `README.md` | Дословная копия `projects/mango/README.md` из Хаба | frontmatter `status: canonical, version: 1.3`; написан под **монорепо** Хаба, а не под standalone-спок |
| `.gitkeep` | Авто-плейсхолдер для создания PR | Технический файл, удаляется при первом реальном коммите структуры |

Полная проверка дерева на ветке `main`:

```text
mango_ba_prompts/
├── README.md      # «чужой» README из монорепо Хаба
└── (.gitkeep)     # авто-генерируется для PR, не часть структуры
```

Промпты, на которые ссылается README (раздел «Готовые prompt assets» и
«Связанные артефакты»), **физически отсутствуют** в этом репозитории — они
живут в Хабе в `projects/mango/prompts/`. То есть репозиторий — это **пустой
спок с README от монорепо**: навигация описывает структуру, которой здесь нет.

### 1.2. Целевая структура «Гибридного минимума» (Хаб → `templates/spoke/`)

Фактический «ДНК-шаблон» спока в Хабе:

```text
templates/spoke/
├── README.md
├── AI_GOVERNANCE.md
├── AI_QUICK_RULES.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── init.sh                                   # одноразовый инициализатор плейсхолдеров
├── docs/
│   ├── adr/.gitkeep
│   └── audit/.gitkeep
├── .github/ISSUE_TEMPLATE/task.md
└── tools/validate-repository-structure.sh    # валидатор + negative-check на research/
```

### 1.3. Сверка с минимальным набором из issue #4

Issue называет ориентировочный минимум; фактические имена в Хабе отличаются.
Фиксирую расхождения, чтобы план опирался на **реальный** шаблон, а не на память:

| Названо в issue #4 | Факт в `templates/spoke/` | Решение |
| :--- | :--- | :--- |
| `README.md` | `README.md` ✅ | Взять из шаблона |
| `AI_GOVERNANCE.md` | `AI_GOVERNANCE.md` ✅ | Взять из шаблона (жёсткое требование Хаба — обязателен в корне) |
| `governance/PROJECT_CONTRACT.md` | ❌ нет такого файла | Роль «контракта проекта» выполняет `AI_GOVERNANCE.md`. Папка `governance/` в шаблоне **не предусмотрена** — не создаём (Anti-Inflation) |
| `tools/validate-structure.sh` | `tools/validate-repository-structure.sh` | Использовать **точное** имя из Хаба |
| `docs/adr/.gitkeep` | `docs/adr/.gitkeep` ✅ | Взять из шаблона |
| — | `AI_QUICK_RULES.md` | Добавить: одностраничные правила для агента (нормализация промптов сверяется с ним) |
| — | `CONTRIBUTING.md`, `CHANGELOG.md` | Добавить: входят в обязательный набор валидатора |
| — | `docs/audit/.gitkeep` | Уже фактически занимаем этим аудитом |
| — | `.github/ISSUE_TEMPLATE/task.md` | Добавить: единый язык постановки задач |

### 1.4. Выявленные «разрывы» (gaps)

| # | Разрыв | Влияние | Подтверждение |
| :--- | :--- | :--- | :--- |
| G1 | Нет `AI_GOVERNANCE.md` в корне | Нарушено жёсткое ограничение Хаба | `validate-repository-structure.sh` → FAIL |
| G2 | Нет `AI_QUICK_RULES.md` | Агент не знает правил спока (что нельзя, как звать человека) | отсутствует файл |
| G3 | Нет `CONTRIBUTING.md`, `CHANGELOG.md` | Нет описанного workflow и журнала изменений | FAIL валидатора |
| G4 | Нет `tools/validate-repository-structure.sh` | Нет «иммунной системы» структуры | FAIL валидатора |
| G5 | Нет `docs/adr/`, `docs/audit/`, `.github/ISSUE_TEMPLATE/` | Негде фиксировать решения и задачи | FAIL валидатора |
| G6 | `README.md` — копия монорепо | Битые относительные ссылки (`../../standards/...`, `../../governance/...`), описывает несуществующие здесь папки | ссылки ведут «вверх» за пределы репозитория |
| G7 | Промпты отсутствуют физически | README обещает 6 prompt assets, которых нет | см. п. 1.1 |
| G8 | У промптов в Хабе нет полей нормализации | В frontmatter нет `temperature`; ссылки указывают на hub-пути `research/mango/classification.md` | проверено по `projects/mango/prompts/*` |

---

## 2. Предложение: инициализация базовой структуры

**Точный список файлов для добавления первыми** (минимальный «правильный геном»,
все — из `templates/spoke/` Хаба; трассируемость в колонке «Источник»):

| # | Файл в споке | Источник (Хаб) | Назначение |
| :--- | :--- | :--- | :--- |
| 1 | `AI_GOVERNANCE.md` | `templates/spoke/AI_GOVERNANCE.md` | Конституция проекта: роли, правила, эскалация, DoD. **Обязателен** (жёсткое ограничение) |
| 2 | `AI_QUICK_RULES.md` | `templates/spoke/AI_QUICK_RULES.md` | Одностраничная инструкция агенту; база для чек-листа нормализации промптов |
| 3 | `README.md` (перезапись) | `templates/spoke/README.md` | Корректный spoke-README со ссылками на Хаб; заменяет «чужую» копию монорепо |
| 4 | `CONTRIBUTING.md` | `templates/spoke/CONTRIBUTING.md` | Workflow вклада: issue → PR → review |
| 5 | `CHANGELOG.md` | `templates/spoke/CHANGELOG.md` | Журнал значимых изменений |
| 6 | `tools/validate-repository-structure.sh` | `templates/spoke/tools/validate-repository-structure.sh` | Валидатор структуры + negative-check на `research/` |
| 7 | `docs/adr/.gitkeep` | `templates/spoke/docs/adr/.gitkeep` | Точка для Architecture Decision Records |
| 8 | `docs/audit/.gitkeep` | `templates/spoke/docs/audit/.gitkeep` | Точка для аудитов (этот файл — первый реальный аудит) |
| 9 | `.github/ISSUE_TEMPLATE/task.md` | `templates/spoke/.github/ISSUE_TEMPLATE/task.md` | Единый шаблон постановки задач |
| 10 | `init.sh` (временно) | `templates/spoke/init.sh` | Заменяет плейсхолдеры `{{project_name}}`, `{{hub_url}}`, `{{date}}` и **самоудаляется** |

Значения для `init.sh`:

- `project_name` = `mango_ba_prompts`
- `project_description` = «Prompt assets и knowledge base бизнес-аналитика Mango Office (spoke Хаба).»
- `hub_url` = `https://github.com/G-Ivan-A/hybrid-Intelligence-lab`

### ⚠️ Negative Check (обязательно)

- **`research/` не создаём.** Прямого, обоснованного и одобренного человеком
  операционного повода нет. Фундаментальные знания (`research/mango/...`)
  остаются в Хабе, спок ссылается на них (см. `AI_QUICK_RULES.md`). Если повод
  появится — он оформляется как ADR в `docs/adr/`, а не явочным порядком.
- **`governance/PROJECT_CONTRACT.md` не создаём.** В «ДНК-шаблоне» такого файла
  нет; его роль уже исполняет `AI_GOVERNANCE.md`. Отдельная папка `governance/`
  была бы ростом «на вырост».
- Папки `prompts/`, `kb/`, `experiments/`, `decisions/` создаём **только**
  вместе с реальным переносом артефактов (см. план миграции), а не заранее.

---

## 3. План миграции промптов (пошагово)

Контекст: prompt assets и связанные артефакты живут в Хабе в
`projects/mango/`. Цель — перенести их в этот standalone-спок без потери
контекста и привести к правилам спока.

**Артефакты-источники в Хабе (`projects/mango/`):**

- `prompts/` — 6 файлов: `tz-stats-generator_{exp,simple}`,
  `user-story-generator_{exp,simple}`, `usecase-stepwise-generator_{exp,simple}`
  (все `-2026-05.md`).
- `standards/classification-glossary.md` — активный Mango-only глоссарий.
- `experiments/` — аудит и self-test промптов (`prompts-audit-2026-05-26.md`,
  `prompts-selftest-2026-05-26.md`) + прототипы.

### Шаг 0 — Утверждение (Human Review)
Утвердить этот план. **Блокирует** все последующие шаги (стоп-фактор issue #4).

### Шаг 1 — Базовый геном (Предложение из §2)
Инициализировать спок из `templates/spoke/` (файлы 1–10), запустить `init.sh`,
убедиться, что `./tools/validate-repository-structure.sh` проходит (exit 0).
Отметить изменение в `CHANGELOG.md` → `## Unreleased`.
**Оценка трудозатрат: ~0.5 дня.**

### Шаг 2 — Перенос глоссария
Скопировать `standards/classification-glossary.md` → `kb/glossary.md` (создать
`kb/` именно сейчас, под реальный артефакт). Зафиксировать решение «свести
Mango-only стандарты в `kb/`» как ADR в `docs/adr/`.
**Оценка: ~0.5 дня.**

### Шаг 3 — Перенос промптов + нормализация
Скопировать 6 промптов в `prompts/` (создать папку под реальный перенос) и
**нормализовать** каждый по чек-листу из `AI_QUICK_RULES.md` / `AI_GOVERNANCE.md`:

**Чек-лист нормализации (на промпт):**
- [ ] Frontmatter валиден (`status`, `version`, `updated`, `ai-generated`, `type`, `variant`, `scope`).
- [ ] Добавлено поле **`temperature`** (сейчас отсутствует во всех промптах Хаба).
- [ ] Есть явный раздел **«ФОРМАТ ВЫВОДА»** (у `*_exp`-вариантов местами свёрнут — выровнять).
- [ ] **Ссылки на глоссарий** ведут на `kb/glossary.md` спока, а не на hub-путь
      `research/mango/classification.md` (вариант `_exp` сейчас ссылается на Хаб
      — заменить на относительную ссылку спока или явный hub-URL).
- [ ] `based_on`-ссылки на `projects/mango/experiments/...` либо переносятся в
      спок, либо переписываются на абсолютный hub-URL (не оставлять битые
      относительные пути).
- [ ] Прогон self-test по сценарию `experiments/prompts-selftest-2026-05-26.md`.

**Оценка: ~1.5–2 дня** (6 промптов × нормализация + прогон).

### Шаг 4 — Перенос истории экспериментов (опционально, по необходимости)
Перенести `experiments/prompts-audit-*` и `prompts-selftest-*` в `experiments/`
спока, если потребуется воспроизводимость нормализации. Иначе — оставить в Хабе
и сослаться. Решение зафиксировать в PR/ADR.
**Оценка: ~0.5 дня.**

### Шаг 5 — Чистка и сверка
Удалить технический `.gitkeep` из корня; убедиться, что README спока больше не
ссылается на несуществующие/hub-относительные пути; финальный прогон валидатора;
запись в `CHANGELOG.md`.
**Оценка: ~0.5 дня.**

**Итого по миграции: ~3.5–4.5 дня** (без учёта review-итераций).

---

## 4. Черновик бэклога (issues для старта миграции)

> Создаются **после** утверждения плана (Human Review). Ниже — драфты.

### Issue A — «Инициализация спока из ДНК-шаблона Хаба»
- **Labels**: `bootstrap`, `priority:P1`
- **Scope**: Шаги 1 настоящего плана — добавить файлы 1–10 из `templates/spoke/`,
  прогнать `init.sh`, перезаписать «чужой» README, добиться зелёного валидатора.
- **DoD**: `./tools/validate-repository-structure.sh` → exit 0; `AI_GOVERNANCE.md`
  в корне; запись в `CHANGELOG.md`; в репозитории нет незаменённых `{{...}}`.

### Issue B — «Миграция и нормализация промптов Mango»
- **Labels**: `migration`, `priority:P1`
- **Scope**: Шаги 2–3 — перенести глоссарий в `kb/glossary.md`, перенести 6
  промптов в `prompts/`, нормализовать по чек-листу §3 (frontmatter,
  `temperature`, формат вывода, ссылки на `kb/glossary.md`).
- **DoD**: все 6 промптов проходят чек-лист нормализации; ссылки не битые;
  self-test пройден; решение по `kb/` зафиксировано как ADR.

### Issue C — (опционально) «Добавление валидатора frontmatter промптов»
- **Labels**: `tooling`, `priority:P2`
- **Scope**: перенести/адаптировать `tools/validate-frontmatter.sh` из Хаба для
  проверки обязательных полей промптов (включая `temperature`) в CI.
- **DoD**: скрипт ловит промпт без `temperature`/битой ссылки на глоссарий;
  подключён к локальной проверке.

---

## 5. Запрос Human Review

Прошу **утвердить или скорректировать**:

1. Список файлов §2 (10 позиций из `templates/spoke/`) и значения для `init.sh`.
2. Решение **не создавать** `research/` и `governance/PROJECT_CONTRACT.md`
   (Negative Check §2).
3. План миграции §3 и оценки трудозатрат.
4. Драфты issues §4 (создавать ли C — валидатор frontmatter).

После аппрува issue #4 переводится в `done`, а работа продолжается по issues A/B
(и C при необходимости). До аппрува физическая инициализация структуры и перенос
промптов **не выполняются**.

---

## Связанные артефакты

- Issue: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/4>
- Хаб, шаблон спока: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/templates/spoke>
- Хаб, исходные промпты: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/mango/prompts>
- Хаб, RFC инициализации проектов: `governance/proposals/rfc-two-cases-of-project-initialization.md`
