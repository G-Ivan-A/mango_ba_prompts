---
status: superseded
version: 0.2
updated: 2026-08-21
temperature: 0.1
type: protocol
layer: executable
full_version: "ai-rules/agent-onboarding-protocol_old.md"
related_standard: "../standards/cascading-context-loading-standard.md"
related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"
---

> 🗄️ **АРХИВ (superseded, issue #267).** Актуальный протокол онбординга —
> [`ai-rules/agent-onboarding-protocol.md`](agent-onboarding-protocol.md) (v1.5).
> Этот файл сохранён только для traceability: он фиксирует локальную адаптацию
> v1.2 и не должен использоваться агентами как точка входа.

# Agent Onboarding Protocol — executable layer

Load this file first. Do not load `ai-rules/agent-onboarding-protocol_old.md`
unless one escalation trigger below is true.

## Escalation triggers

- TRIGGER-1: пользователь явно просит полную версию протокола, rationale,
  threat-awareness, историю решений или ссылки на Хаб.
- TRIGGER-2: нужно редактировать, синхронизировать или валидировать
  `ai-rules/agent-onboarding-protocol_old.md`.
- TRIGGER-3: текущая задача требует точной формулировки из full-разделов
  `EXPLANATION`, `Design Rationale & History` или таблиц cross-reference.
- TRIGGER-4: есть конфликт между этим executable-слоем, full-протоколом,
  `AI_SESSION_HANDOVER_PROMPT.executable.md`, issue/PR или правилами Хаба.

Если ни один триггер не сработал, выполняй только алгоритм ниже.

## Execute

Runtime-онбординг - read-only фаза перед первым изменением файлов. Агент
ничего не пишет в репозиторий до readback и явного разрешения пользователя,
если задача не была уже явно одобрена в текущем рабочем контексте.

### Step 1 — governance checklist

Прочитай в таком порядке:

1. `README.md` - назначение проекта, актуальная структура, мост к Хабу.
2. `AI_GOVERNANCE.md` - роли, правила, operating modes, эскалация, DoD.
3. `AI_QUICK_RULES.md` - fail-closed semantics и запреты.
4. `CONTRIBUTING.md` - workflow issue -> PR -> review и локальные проверки.
5. Текст текущего issue, последние issue comments, текущий PR и PR comments.

Если документ имеет соседний `.executable.md`, начинай с executable-слоя и
читай full только по его triggers.

### Step 2 — task context checklist

Собери только проверяемый контекст:

- цель issue и Definition of Done;
- operating mode и явные запреты;
- подготовленную ветку и PR;
- релевантные standards/patterns/prompts;
- последние комментарии и review comments;
- локальный git status и существующие изменения.

Не достраивай отсутствующий контекст догадками.

### Step 3 — readback

Перед изменениями верни пользователю короткий readback:

```markdown
## Readback готовности

- Цель задачи:
- Границы и запреты:
- Релевантные стандарты:
- План первых действий:
- Открытые вопросы / неоднозначности:
- Чего не хватает в контексте:
```

Если пользователь уже дал команду "Proceed" с подготовленной веткой и PR,
readback может быть кратким рабочим обновлением, после которого исполнитель
продолжает реализацию в пределах issue.

### Step 4 — proceed only inside approved scope

После разрешения:

- меняй только файлы, необходимые для issue;
- не создавай `research/`, приватные операции, RAG/embeddings или новую
  структуру без отдельного issue;
- сохраняй full-документы как full-слой, не удаляй rationale и историю;
- добавляй проверки, если меняешь контракт;
- фиксируй результат в PR и changelog, если изменение значимое.
