---
status: accepted
version: 1.0
updated: 2026-06-11
ai-generated: true
type: adr
scope: creative-mode-governance
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/61"
related_prs:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/57"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/60"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/68"
---

# ADR-0003: Creative-mode governance без архитектурного долга

> **Статус:** Accepted · **Дата:** 2026-06-11 · **Issue:**
> [#61](https://github.com/G-Ivan-A/mango_ba_prompts/issues/61)

## Контекст

PR #57 решал issue #56 в режиме `Creative`: Конард исследовал международную
практику и выбрал токены режимов `stepwise` / `oneshot` / `legacy`. Решение было
применено, но ADR не создан, потому что контракты конфликтовали:

- [`CONTRIBUTING.md`](../../CONTRIBUTING.md) требовал фиксировать отклонение от
  правила Хаба как ADR в `docs/adr/`;
- issue #56 ограничивал изменения только `prompts/` и `prompts/archive/`;
- [`AI_QUICK_RULES.md`](../../ai-rules/ai-quick-rules.md) применял fail-closed ко всем
  неописанным действиям без различения `Structured` и `Creative`.

В результате архитектурное решение осталось только в PR-описании. Это создало
долг: правило, созданное для предсказуемости, помешало зафиксировать rationale.

## Практика OSS

Изучены первичные источники:

- Microsoft Semantic Kernel: вклад идёт через issues/PR, баги требуют minimal
  reproduction, а значимые решения фиксируются ADR в `docs/decisions/`.
  Источники: <https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md>,
  <https://github.com/microsoft/semantic-kernel/blob/main/docs/decisions/README.md>.
- LangChain: PR должен иметь контекст issue/discussion, автор обязан проверить
  AI-assisted changes и не отправлять bulk/unreviewed content.
  Источник: <https://docs.langchain.com/oss/python/contributing/overview>.
- DSPy: AI-assisted contributions допустимы, но автор отвечает за понимание,
  воспроизведение, тесты, описание и ownership результата.
  Источник: <https://github.com/stanfordnlp/dspy/blob/main/CONTRIBUTING.md>.

Общий вывод: автономия допустима, если есть контекст issue, воспроизводимая
проверка, reviewable PR и явное rationale. Это совместимо с Creative режимом,
но несовместимо с глобальным fail-closed для всех действий.

## Решение

1. Разделить режимы:
   - `Structured` остаётся fail-closed: если действие не описано, агент
     останавливается и просит human guidance.
   - `Creative` разрешает обоснованный обход scope или локального правила, если
     обход нужен для цели задачи и не нарушает жёсткие запреты.
2. Обязать PR фиксировать каждый обоснованный обход: какое правило обойдено,
   почему, какой артефакт создан и как проверено решение.
3. Если обход меняет architecture/governance practice, фиксировать решение как
   ADR в `docs/adr/`.
4. Зафиксировать специфику Конарда:
   - Пользователь молчит + мержит PR → молчание = согласие;
   - комментарий + ручной перезапуск задачи → итерация в той же ветке;
   - close PR → отказ от решения.
5. Переформулировать Хаб как источник рекомендаций и обмена опытом, не
   ограничитель локальных решений.
6. Завести локальный шаблон задачи
   [`docs/task-for-konard-template.md`](../task-for-konard-template.md), который
   описывает WHAT/WHY и не диктует пошаговое HOW.

## Было / Стало

| Сценарий | Было | Стало |
| :--- | :--- | :--- |
| PR #57: Creative issue разрешает менять только `prompts/` | Конард создаёт промпты, но не создаёт ADR, хотя решение по режимам архитектурно значимо. | Конард создаёт промпты и ADR в `docs/adr/`, а в PR описывает обоснованный обход ограничения `prompts/`/`prompts/archive/`. |
| RFC переноса практик в Хаб | Формулировки могли читаться как обязательный gate для спока. | RFC описывает рекомендательный маршрут; Хаб помогает обмениваться практиками, но не блокирует локальные решения. |
| Задача для Конарда | Короткая форма `Тип / Файл / Содержимое` подталкивает к инструкции как делать. | Шаблон содержит Контекст, Проблему, Story, ФТ, НФТ и Цель; Конард сам выбирает решение. |

## Примеры обоснованного обхода

- **ADR вне узкого scope.** Issue разрешает менять только промпты, но задача
  включает новое соглашение об именовании. В Creative режиме агент создаёт ADR,
  потому что без него решение останется в PR-тексте и станет долгом.
- **Локальный task template.** Issue просит обновить task.md или аналог, но в
  репозитории такого файла нет. Агент создаёт минимальный
  `docs/task-for-konard-template.md`, потому что это прямой артефакт задачи.
- **RFC clarification.** Если документ Хаба читается как ограничитель, агент
  смягчает локальный RFC и фиксирует, что передача в Хаб является отдельной
  follow-up задачей.

## Self-test на кейсе PR #57

Проверка после этого ADR:

1. Дано: issue в режиме `Creative`, цель требует архитектурного решения, а scope
   перечисляет только продуктовые файлы.
2. Ожидаемо: Конард делает основное изменение, создаёт минимальный ADR вне scope,
   описывает обоснованный обход в PR и запускает доступные проверки.
3. Acceptance: Пользователь мержит без комментариев (молчание = согласие), либо
   комментирует и вручную перезапускает задачу, либо закрывает PR.

Локальная проверка этой задачи: `python3 scripts/validate_issue_61_governance.py`.

## Последствия

**Положительные:**

- Creative режим перестаёт создавать скрытый архитектурный долг.
- Structured режим сохраняет предсказуемость и fail-closed там, где она нужна.
- PR становится единой точкой review для решений, рисков и обоснованных обходов.

**Риски и ограничения:**

- Creative обход не должен становиться оправданием широких unrelated rewrites.
- Жёсткие запреты остаются жёсткими: secrets, private data, лицензии, публикация,
  удаление файлов без разрешения, создание `research/` внутри HTOM-команды.
- Перенос этой практики в Хаб не выполняется в рамках issue #61; это отдельный
  follow-up.

## Альтернативы

- **Оставить глобальный fail-closed.** Отклонено: воспроизводит долг PR #57.
- **Всегда спрашивать Пользователя перед ADR вне scope.** Отклонено для Creative:
  тормозит задачу и перекладывает выбор решения на человека там, где issue уже
  дал агенту свободу.
- **Считать Хаб обязательным gate для спока.** Отклонено: Хаб должен помогать
  распространять практики, а не блокировать локальную работу.

## Связанные артефакты

- Issue #61: <https://github.com/G-Ivan-A/mango_ba_prompts/issues/61>
- PR #57: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/57>
- PR #60: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/60>
- AI governance: [`AI_GOVERNANCE.md`](../../ai-governance/ai-governance.md)
- Quick rules: [`AI_QUICK_RULES.md`](../../ai-rules/ai-quick-rules.md)
- Contributing: [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
- Task template: [`docs/task-for-konard-template.md`](../task-for-konard-template.md)
