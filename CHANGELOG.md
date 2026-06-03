---
status: draft
version: 0.1
updated: 2026-06-02
ai-generated: true
---

# Changelog — mango_ba_prompts

Все значимые изменения проекта документируются здесь. Формат основан на
[Keep a Changelog](https://keepachangelog.com/ru/1.1.0/); проект придерживается
[Semantic Versioning](https://semver.org/lang/ru/).

## Unreleased

### Added — Initial repository structure based on hybrid-Intelligence-lab templates

- Инициализация спока `mango_ba_prompts` из «ДНК-шаблона» Хаба
  (`templates/spoke/`): базовый геном (governance, quick rules, навигация,
  каркасы `docs/adr/`, `docs/audit/`, база знаний `kb/glossary.md`).
- «Бесплатные» улучшения из анализа рекомендаций команд C и Q:
  fail-closed semantics в `AI_QUICK_RULES.md` и capability taxonomy в
  `AI_GOVERNANCE.md`.
- RFC стратегии миграции проекта Mango из Хаба в спок
  (`docs/analysis/migration-strategy-rfc.md`, issue #8): аудит 23 артефактов
  Хаба по полным URL, фазовая стратегия (Mermaid), edge cases, креативные
  улучшения и триггеры эволюции. Стоп-фактор: физический перенос — после
  Human Review.

### Changed

- Уточнён RFC стратегии миграции (`docs/analysis/migration-strategy-rfc.md`,
  issue #10): добавлена таблица файлов Фазы 1, чек-лист нормализации промптов,
  единый реестр research-зависимостей, корректное разделение
  `standards/GLOSSARY.md` и `standards/MANGO_CLASSIFICATION_CONTRACT.md`,
  а также правила переноса продуктовых экспериментов.
- Завершена доработка RFC (`docs/analysis/migration-strategy-rfc.md`,
  issue #12, v0.3, блоки 3–8): реестр зависимостей от исследований Хаба (§3.5),
  переписка README.md как обязательная задача Фазы 1, согласованные формулировки
  edge cases E5 (все эксперименты — часть продукта) и E6 (разделение
  глоссария и контракта классификации, §4.1), временный workflow промптов P0
  для `CONTRIBUTING.md` (§5.2) и шаблон Migration Manifest (§5.3).
- Human Review доработанного RFC миграции
  (`docs/reviews/migration-rfc-human-review-2026-06.md`, issue #13): сверка
  v0.3 против чек-листа из 11 пунктов (архитектурная целостность, операционная
  готовность, трассируемость) — все пункты пройдены; зафиксированы открытые
  вопросы Q1–Q4 на решение фаундера перед стартом Фазы 0.
- Сформирован операционный бэклог Фазы 1 миграции
  (`governance/BACKLOG.md`, issue #14): 9 атомарных задач (M-001…M-009) с
  приоритетами, зависимостями, DoD и трассировкой на разделы утверждённого RFC,
  плюс Mermaid-диаграмма критического пути. Бэклог = один файл (Anti-Inflation);
  выполнение задач не начато.

### Removed

- Удалён технический корневой `.gitkeep`, созданный только для bootstrap PR.
