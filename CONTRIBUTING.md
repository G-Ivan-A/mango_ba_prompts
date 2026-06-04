---
status: draft
version: 0.1
updated: 2026-06-04
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

## Временный workflow промптов

До появления ADR это единственный разрешённый способ создания новых промптов в
споке. Workflow опирается на capability boundary `prompts/drafts/` и не вводит
матрицу решений или дополнительный ADR-процесс.

1. **Draft.** Создать файл в `prompts/drafts/` с именем
   `[biz-process]-[purpose].md`.
2. **Frontmatter.** Добавить обязательный frontmatter: `status: draft`,
   `version: 0.1`, `updated: {{date}}`, `temperature: 0.1`.
3. **Experimental marker.** Добавить комментарий
   `<!-- Experimental: for [task/link], no formal research yet -->`.
4. **Review issue.** Создать issue `prompt:review` с бизнес-контекстом.
5. **Canonical promotion.** После human review переместить файл в `prompts/`,
   обновить `status: canonical`, `version: 1.0`.

Минимальный черновик:

```markdown
---
status: draft
version: 0.1
updated: {{date}}
temperature: 0.1
---

<!-- Experimental: for [task/link], no formal research yet -->
```

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
