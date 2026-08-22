---
status: draft
version: 0.1
updated: 2026-08-21
ai-generated: true
type: step
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/281"
---

# Эпизод 2 (реплики 2–3) — ad-hoc-промпт eTOM/ODA, первый перечень ФТ 4.1–4.6

## Что происходило

| Реплика | Содержание |
| --- | --- |
| 2 (user) | Ad-hoc-промпт «команда сертифицированных БА… eTOM… ODA Capability Map», правила формулировок (через результат, без реализации/API), контракт из 3 шагов. |
| 3 (assistant) | Сразу выдан проект ФТ уровня 4.x (4.1–4.6), без уточняющих вопросов. |

## Что зафиксировано

- Использован ad-hoc-промпт, а не `prompts/fr-documentation-stepwise.md`
  (см. [`../prompts-chain.md`](../prompts-chain.md)).
- Шаг «уточняющие вопросы» из собственного контракта промпта пропущен.

## Вердикт эпизода

**works-with-edits** — перечень принят как основа, но требует доработки.
