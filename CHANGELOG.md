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

### Removed
