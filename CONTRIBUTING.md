---
status: draft
version: 0.4
updated: 2026-08-21
temperature: 0.1
---

# Contributing — mango_ba_prompts

Вклад в `mango_ba_prompts` сохраняет малый размер активных контрактов,
traceability и практическую полезность для hybrid human + AI work. Правила входа
наследуются от Хаба `hybrid-Intelligence-lab` и не дублируют его.

## Workflow: issue → PR → review

1. **Issue.** Начинайте с GitHub issue: context, решаемая проблема, Story,
   ФТ/НФТ, цель, scope, Operating Mode и измеримый Definition of Done. Для задач
   Конарда используйте [`docs/task-for-konard-template.md`](docs/task-for-konard-template.md).
2. **PR.** Держите изменение reviewable: одна цель, понятные ссылки, без
   unrelated restructuring. Связывайте PR с issue. В Creative режиме PR может
   содержать файлы вне исходного scope, если они нужны для цели задачи и
   обоснованный обход описан в PR.
3. **Review.** Финальные решения по vision, publication и merge остаются за
   человеком согласно [AI_GOVERNANCE.md](AI_GOVERNANCE.md).

## Review loop с Конардом

PR Конарда считается итерируемым черновиком до merge:

- **молчание = согласие:** если Пользователь мержит PR без комментариев, решения,
  включая обоснованные обходы scope, приняты;
- **комментарий + ручной перезапуск:** если Пользователь оставляет комментарий и
  вручную перезапускает задачу, Конард дорабатывает тот же PR новыми коммитами;
- **close:** закрытие PR означает полный отказ от решения.

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
сохраняют права решения за Пользователем и не публикуют sensitive data.
Отдельное hard rule: AI agents не создают `research/` в споке.

- В Structured режиме действуют capability boundaries и fail-closed semantics:
  что не описано — не выполняется без human review.
- В Creative режиме агент может создать ADR/RFC/шаблон/проверку вне requested
  scope, если это нужно для цели задачи. Такой обоснованный обход фиксируется в
  PR: какое правило обойдено, почему, какой файл создан и как проверено решение.
- При создании дайджеста сессии, если в нём есть открытые вопросы, Исполнитель
  добавляет их в [`pr-ops/BACKLOG.md`](pr-ops/BACKLOG.md#5-открытые-вопросы),
  если они ещё не добавлены. Это сохраняет единый трекер вопросов вместо
  разрозненных таблиц.

## KB PDF and Git LFS

PDF-источники БЗ хранятся только в `kb/sources/<slug>/` и отслеживаются через
Git LFS (`*.pdf` в `.gitattributes`). Загружайте и заменяйте такие файлы через
Codespace или локальный Git с `git lfs`, не через веб-интерфейс GitHub.

При замене одного PDF на несколько частей обновите `meta.json`/`source.md`,
перечислите все части в порядке страниц при запуске `make kb-extract` или
workflow **KB pipeline**, затем закоммитьте регенерированный
`kb/processed/<slug>/`. Подробная инструкция и команды:
[`kb/sources/README.md`](kb/sources/README.md#как-обновлять-pdf-через-git-lfs).

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] Изменённые файлы соответствуют целевой структуре спока.
- [ ] Значимое изменение отражено в [CHANGELOG.md](CHANGELOG.md) (`## Unreleased`).
- [ ] Решение, отклоняющееся от правила Хаба или исходного scope, объяснено в PR.
- [ ] Архитектурное или governance-решение зафиксировано как ADR в `docs/adr/`.
- [ ] Риски, допущения и фокус human review сформулированы явно.
