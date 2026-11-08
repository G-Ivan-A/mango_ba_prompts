---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: index
scope: ba-processes
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/123"
---

# docs/ba-processes

`docs/ba-processes/` хранит карту процессов БА: какие промпты, операции и
паттерны использовать для типовых задач. Это не место хранения результатов
выполнения.

Результаты реальных прогонов, экспериментов, self-test и анализов фиксируются в
[`runs/`](../../runs/README.md). Центральный маппинг процессов остаётся в
[`00-index.md`](00-index.md).


[A-IN: 24 отдельных вызова](bcreq-a-in-execution.md) — действующая draft
реализация принятого RFC-AIN-001 (#474), с допуском БА до раздела 2,
вопросами Заказчику и отдельным handover. Полные тексты генерируются из
route/instructions/common; измерение поведения LLM — отдельный BL-175.
