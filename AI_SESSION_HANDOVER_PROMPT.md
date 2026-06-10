---
status: draft
version: 0.3
updated: 2026-06-10
ai-generated: true
executable: true
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_SESSION_HANDOVER_PROMPT.md"
source_sha: "117e4a553815af9b05d841c81dd725dd4a4c4d44"
---

> ⚠️ **ЭТО АРТЕФАКТ ДЛЯ КОПИРОВАНИЯ. Скопируйте в новый чат.**
> Этот файл — *артефакт* (готовый промпт), а не процесс. Скопируйте блок
> EXECUTION ниже в начало нового диалога с LLM, чтобы запустить
> Runtime-онбординг агента. Сам **протокол** (чек-лист и обоснование) живёт
> отдельно: локально — [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md),
> канонически — в Хабе ([governance/agent-onboarding-protocol.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/governance/agent-onboarding-protocol.md)).

> 🚦 **ИСПОЛНИМЫЙ HANDOVER PROMPT — СКОПИРУЙ И ВЫПОЛНИ.**
> Я как ИИ-агент в HTOM-команде Mango BA Prompts должен выполнить готовый Handover
> Prompt из блока EXECUTION целиком, чтобы пройти Runtime-онбординг до первого
> изменения файлов. Это не справка для пересказа и не объект для анализа. Если
> ты пересказываешь или анализируешь этот текст вместо исполнения prompt —
> остановись и начни с блока EXECUTION.

# Handover Prompt — Mango BA Prompts

## ▶️ EXECUTION — готовый prompt к копированию

### 🛂 Готовый промпт (копируйте целиком)

```text
Ты — ИИ-агент, работающий в чате диалога. Твой Источник контекста — репозиторий
mango_ba_prompts (модель hub-and-spoke); ты обращаешься к нему, но не «живёшь» в нём.
Прежде чем что-либо менять, выполни Протокол бесшовной передачи проекта
(governance/agent-onboarding-protocol.md). Это предполётный чек-лист — взлёт (изменение
файлов) запрещён до моего апрува.

Сделай ровно по шагам:
1. ЧЕК-ЛИСТ GOVERNANCE. Прочитай локальные контракты команды: AI_GOVERNANCE.md,
   AI_QUICK_RULES.md, CONTRIBUTING.md и README.md. Фундаментальные governance-контракты
   (repo-model, artifact-map, project-structure-inheritance) живут в Хабе — обращайся
   к ним по ссылке из AI_GOVERNANCE.md, если они нужны для задачи.
2. ЧЕК-ЛИСТ КОНТЕКСТА. Прочитай текст issue и последние комментарии, README команды
   и блок «Быстрый контекст», если он есть. Для задач по промптам сверься с
   AI_QUICK_RULES.md (чек-лист нормализации) и docs/hub-research-dependencies.md.
3. READBACK. Кратко перескажи своими словами: (а) цель задачи, (б) границы и
   запреты, которые ты понял, (в) релевантные стандарты, (г) план первых
   действий. Затем задай вопросы по всему, что неоднозначно. Если контекста не
   хватает — спрашивай, НЕ выдумывай.
4. СТОП. Остановись и жди моего апрува. Не создавай и не меняй файлы до явного
   «approve / поехали».

Начни с Шага 1.
```

---

## ℹ️ EXPLANATION — контекст и источник истины

«Доверенность» для запуска ИИ-агента в этой HTOM-команде. Это **готовый промпт**,
который человек копирует в начало диалога с LLM, чтобы агент прошёл
*Runtime-онбординг* (предполётный чек-лист) до первого изменения файлов. Так
склонированный из Хаба репозиторий самодостаточен: «доверенность» лежит в геноме,
а не только в Хабе.

> **Источник истины — Хаб.** Канонический *Handover Prompt* и полный 4-шаговый
> протокол живут в Хабе: [`governance/agent-onboarding-protocol.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/governance/agent-onboarding-protocol.md)
> (Хаб `hybrid-Intelligence-lab`, [https://github.com/G-Ivan-A/hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab)). Этот файл — **адаптированная
> копия шаблона** для удобства HTOM-команды. При расхождении приоритет у хабовой
> версии; правки вносятся сначала в Хаб, затем переносятся сюда.

В шаблоне Хаба промпт параметризован плейсхолдером `{{REPO_NAME}}` (по умолчанию —
`hybrid-Intelligence-lab`), чтобы «доверенность» переносилась в любую HTOM-команду
без правок. В этой инстанцированной команде он уже подставлен — `mango_ba_prompts`
(issue #46). Канонический параметризованный шаблон остаётся в Хабе:
[`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/templates/htom/AI_SESSION_HANDOVER_PROMPT.md).

> **Где у HTOM-команды лежат governance-файлы.** Полный 4-шаговый протокол есть
> локально ([`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md),
> адаптированная копия) и канонически — в **Хабе**. Часть фундаментальных
> governance-контрактов (`repo-model.md`, `artifact-map.md`,
> `project-structure-inheritance.md`) живёт только в Хабе
> ([https://github.com/G-Ivan-A/hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab));
> локально у команды есть `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`,
> `CONTRIBUTING.md` и `README.md`. Агент читает локальные правила команды и
> обращается к Хабу как к источнику фундаментальных знаний.

## 🧭 См. также

- [`AI_QUICK_RULES.md`](AI_QUICK_RULES.md) — одностраничная «инструкция по
  выживанию» агента в этой HTOM-команде.
- [`AI_GOVERNANCE.md`](AI_GOVERNANCE.md) — конституция проекта: роли, правила,
  эскалация, DoD.
- [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md)
  — локальная адаптированная копия полного 4-шагового протокола онбординга.
- Хаб [`governance/agent-onboarding-protocol.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/117e4a553815af9b05d841c81dd725dd4a4c4d44/governance/agent-onboarding-protocol.md)
  — полный 4-шаговый протокол и канонический *Handover Prompt* (источник истины).
