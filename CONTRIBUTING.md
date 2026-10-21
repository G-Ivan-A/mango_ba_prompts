---
status: draft
version: 0.6
updated: 2026-10-20
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
   человеком согласно [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md).

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

AI agents следуют [`ai-governance/ai-governance.md`](ai-governance/ai-governance.md) и
[`ai-rules/ai-quick-rules.md`](ai-rules/ai-quick-rules.md): читают issue и последние комментарии,
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

## Проверки перед коммитом

В репозитории 25 валидаторов; каждый — регрессионный тест конкретной issue.
Запускать их по одному не нужно, есть два уровня (issue #299):

```bash
make validate-fast   # после каждой правки: перезапускаются только те валидаторы,
                     # чьи входы изменились (0.4–1.7 с)
make validate-full   # перед пушем: весь набор без кэша (~10 с), как в CI
```

Быстрый уровень определяет зависимости сам, наблюдая, что валидатор читает,
поэтому **новый валидатор не требует регистрации**: файл, подходящий под маску
`scripts/validate_issue_*.py`, `scripts/test_*.py` или `tools/validate-*.sh`,
попадает и в локальный набор, и в CI автоматически.

Кэш (`.validate-cache/`) не версионируется и полностью производный: если
что-то выглядит странно, `make validate-cache-clear` безопасен в любой момент.
Кэшируются только успешные прогоны, поэтому «зелёный кэш» не может скрыть
падение. Устройство и управление кэшем — [`tools/README.md`](tools/README.md);
разбор решения — [`docs/analysis/2026-08-22-validator-optimization.md`](docs/analysis/2026-08-22-validator-optimization.md).

## Параллельные PR: конфликты merge и номера прогонов

PR с прогоном дописывает строки в общие реестры — `CHANGELOG.md` (`## Unreleased`),
`runs/README.md` (реестр записей и таблица инструментов), иногда `.gitignore`. Когда
параллельный PR смержен первым, оставшийся получает `This branch has conflicts that
must be resolved`, хотя обе правки нужно сохранить. Реплей истории (issue #377):
60 из 183 merge-коммитов имели конфликты, 85 из них — в реестрах; скрипт ниже
разрешает 77 из 85, остальные 8 — настоящие правки одной строки
([`docs/analysis/2026-10-20-parallel-pr-merge-conflicts.md`](docs/analysis/2026-10-20-parallel-pr-merge-conflicts.md)).

Порядок для агента и человека (без согласования, ничего не ломает):

1. Номер прогона — следующий свободный с учётом `main` **и открытых PR**:
   `python3 scripts/resolve_registry_conflicts.py --next-run-id --base upstream/main`.
2. Перед финализацией PR влить `main` (`git merge upstream/main`) и при конфликте
   выполнить `make resolve-conflicts`: append-only конфликты реестров разрешаются
   объединением сторон (строки прогонов — по номеру, ссылки «Используется в» —
   объединяются, `version`/`updated` — большее значение), файлы добавляются в индекс.
3. Если скрипт сообщает о коллизии номера (каталог `runs/<год>/RUN-NNNN/` есть в
   обеих ветках): `git merge --abort`, затем
   `python3 scripts/resolve_registry_conflicts.py --renumber RUN-OLD RUN-NEW --base upstream/main`
   (переименует каталог и номер только в файлах и строках, добавленных веткой),
   закоммитить и повторить шаг 2.
4. Остальные конфликты скрипт не трогает — их разбирают вручную; после этого
   `make validate-full`. Валидатор [`scripts/validate_issue_377_merge_hygiene.py`](scripts/validate_issue_377_merge_hygiene.py)
   не пропустит маркеры конфликта, дубли номеров и служебный `.gitkeep` в корне.

## KB PDF (в репозитории не хранятся)

Опубликованная извлечённая БЗ находится в
[`mango-ba-ai-runtime/docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb).
Упоминания `kb/processed/` ниже описывают прежний процесс извлечения;
см. [`kb/processed/README.md`](kb/processed/README.md) для commit переноса.

PDF-источники БЗ **не коммитятся**: они лежат локально в `kb/sources/<slug>/` и
исключены `.gitignore` (`kb/sources/**/*.pdf`). Git LFS для них не используется
(issue #310) — в репозиторий попадает только результат извлечения
`kb/processed/<slug>/` и манифест источника `meta.json`/`source.md`.

При замене одного PDF на несколько частей обновите `meta.json`/`source.md`,
перечислите все части в порядке страниц при запуске `make kb-extract` или
workflow **KB pipeline**, затем закоммитьте регенерированный
`kb/processed/<slug>/`. Подробная инструкция и команды:
[`kb/sources/README.md`](kb/sources/README.md#как-обновлять-pdf).

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] `main` влит в ветку, конфликты реестров разрешены `make resolve-conflicts`.
- [ ] `make validate-full` проходит локально.
- [ ] Изменённые файлы соответствуют целевой структуре спока.
- [ ] Значимое изменение отражено в [CHANGELOG.md](CHANGELOG.md) (`## Unreleased`).
- [ ] Решение, отклоняющееся от правила Хаба или исходного scope, объяснено в PR.
- [ ] Архитектурное или governance-решение зафиксировано как ADR в `docs/adr/`.
- [ ] Риски, допущения и фокус human review сформулированы явно.
