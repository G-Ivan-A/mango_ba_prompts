---
status: draft
version: 0.1
updated: 2026-06-02
ai-generated: true
---

# Contributing — mango_ba_prompts

Вклад в `mango_ba_prompts` сохраняет малый размер активных контрактов,
traceability и практическую полезность для hybrid human + AI work. Правила входа
наследуются от Хаба `hybrid-Intelligence-lab` и не дублируют его.

## Workflow: issue → PR → review

1. **Issue.** Начинайте с GitHub issue: context, scope, Operating Mode,
   измеримый Definition of Done.
2. **PR.** Держите изменение reviewable: одна цель, понятные ссылки, без
   unrelated restructuring. Связывайте PR с issue.
3. **Review.** Финальные решения по vision, publication и merge остаются за
   человеком согласно [AI_GOVERNANCE.md](AI_GOVERNANCE.md).

## AI-Assisted Work

AI agents следуют [AI_GOVERNANCE.md](AI_GOVERNANCE.md) и
[AI_QUICK_RULES.md](AI_QUICK_RULES.md): читают issue и последние комментарии,
сохраняют human decision rights, не публикуют sensitive data, работают внутри
requested scope и не создают `research/` в споке. Действуют capability
boundaries и fail-closed semantics: что не описано — не выполняется без human
review.

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] Изменённые файлы соответствуют целевой структуре спока.
- [ ] Значимое изменение отражено в [CHANGELOG.md](CHANGELOG.md) (`## Unreleased`).
- [ ] Решение, отклоняющееся от правила Хаба, зафиксировано как ADR в `docs/adr/`.
- [ ] Риски, допущения и фокус human review сформулированы явно.
