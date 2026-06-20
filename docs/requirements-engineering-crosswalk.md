---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: reference
scope: requirements-engineering-crosswalk
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/127"
related_artifacts:
  - "standards/ba-ontology.md"
  - "docs/adr/004-operations-taxonomy.md"
  - "docs/adr/009-bcreq-formation-process.md"
  - "docs/taxonomy.md"
---

# Crosswalk: Вигерс ↔ mango operations ↔ BCREQ

Этот файл закрывает C3 issue #127: даёт справочную таблицу соответствия между
процессами Вигерса, существующими операциями mango и подпроцессами BCREQ. Таблица
является **alias-crosswalk**: она не переименовывает операции mango, не меняет
конвейер BCREQ и не вводит новые AI-специфичные подпроцессы.

## Источники

- Hub RFC `requirements-engineering-ai-era-2026.md` (С1/С2/С3, Вигерс ↔ mango):
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/requirements-engineering-ai-era-2026.md>
- Hub RFC `ai-classifications-formalization-2026-06.md` (AI-классификации,
  статус `Candidate`, подготовка синхронизации С1/С2/С3):
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/73e94c6e69995ccf9e746c19d9c18359971285f2/research/mango/ai-classifications-formalization-2026-06.md>
- ADR-004: [таксономия операций](adr/004-operations-taxonomy.md).
- ADR-009: [процесс BCREQ](adr/009-bcreq-formation-process.md).

## Правила чтения

- Колонка «Процесс Вигерса» — общий язык классической инженерии требований.
- Колонка «Операции mango» — текущие 13 операций из
  [docs/taxonomy.md](taxonomy.md); они остаются source of truth для промптов и
  паттернов.
- Колонка «Подпроцесс BCREQ» — горизонтальный конвейер П1-П6 из
  [ADR-009](adr/009-bcreq-formation-process.md).
- Если одна операция mango попадает в несколько классических процессов, это не
  конфликт: операции гранулярнее, чем модель Вигерса 4+1.

## C3: таблица соответствия

| Процесс Вигерса (RU / EN) | Операции mango (ADR-004) | Подпроцесс BCREQ (ADR-009) | Примечание |
| --- | --- | --- | --- |
| Выявление / Elicitation | `ingestion`, `understanding` | П1 | Приём, нормализация и первичное понимание контекста; смысловая интерпретация начинается после сохранения источника. |
| Анализ / Analysis | `modeling`, `research`, `impact_analysis`, `reverse_requirements` | П2, П3 | Декомпозиция, моделирование сценариев, исследование текущего состояния и восстановление требований из существующего поведения. |
| Спецификация / Specification | `documentation`, `solution_design` | П4 | Оформление требований и проектных деталей в ФТ/ТЗ/BCREQ без добавления требований без источника. |
| Проверка / Validation | `validation`, `quality` | П5 | Verify + Validate: дефекты, полнота, непротиворечивость, проверяемость и quality summary. |
| Управление / Management | `governance`, `release_readiness`, `risk_analysis` | П6 | Приоритизация, статусы, approval/baselining, readiness и owner-review для high/compliance risks. |

## Использование

- В документации или PR можно ссылаться на этот файл как на мост
  `docs/requirements-engineering-crosswalk.md`, если обсуждение идёт в терминах
  Вигерса, а реализация остаётся в терминах mango.
- Для нового BCREQ сначала выбирается маршрут по
  [docs/ba-processes/00-index.md](ba-processes/00-index.md), затем при
  необходимости указывается соответствующий процесс Вигерса из таблицы.
- Для traceability допускается хранить ссылку на строку crosswalk рядом с
  `requirement_level` и `business-rule`, но source of truth для операций остаётся
  `docs/taxonomy.md`.
