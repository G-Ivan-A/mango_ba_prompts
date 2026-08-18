---
status: draft
version: 0.1
updated: 2026-08-17
ai-generated: true
type: index
scope: standards
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/265"
---

# `standards/` — реестр стандартов спицы

Каталог содержит два разных класса файлов, и путать их дорого:

- **Рабочие копии Хаба** — норма принадлежит
  [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab).
  Локально **не редактируются**: расхождение устраняется синком
  ([`scripts/sync_from_hub.py`](../scripts/sync_from_hub.py)), а не правкой копии.
  Такой файл несёт баннер «рабочая копия» и `source_sha` во frontmatter.
- **Собственные стандарты спицы** — норма принадлежит `mango_ba_prompts`:
  промпты, прогоны, БЗ, каталог продукта Mango. Правятся здесь, через issue и PR.

Правило разграничения: собственный стандарт спицы **МОЖЕТ** сужать норму Хаба
под контекст Mango, но **НЕ ДОЛЖЕН** ей противоречить. При конфликте выигрывает
рабочая копия Хаба, а расхождение оформляется issue в Хаб (см.
[ADR-0004](../docs/adr/0004-hub-resync-2026-08.md)).

## Рабочие копии Хаба

| Файл | О чём | Носитель нормы |
| :--- | :--- | :--- |
| [`GLOSSARY.md`](GLOSSARY.md) | Canonical-словарь: Operating Mode, Task Type, Method, Абсолютные границы, Легальный выход, уровни обязательности (Policy / Standard / Contract / Guideline). | Хаб, `standards/glossary.md` |
| [`analysis-standard.md`](analysis-standard.md) | Форма и критерии готовности аналитического артефакта. | Хаб, `standards/analysis-standard.md` |
| [`research-standard.md`](research-standard.md) | Структура research-модуля и маршрутизация к Reference Research Pattern. | Хаб, `standards/research-standard.md` |
| [`evals-contract-standard.md`](evals-contract-standard.md) | Контракт evals: что считается измеримой проверкой качества. | Хаб, `standards/evals-contract-standard.md` |

Точка синка (единый `source_sha` для всех копий) —
[`.hub-profile.json`](../.hub-profile.json), поле `last_sync.hub_sha`.

## Собственные стандарты спицы

| Файл | О чём | Носитель (ADR) |
| :--- | :--- | :--- |
| [`prompt-standard.md`](prompt-standard.md) | Форма промпта: структура, режимы, формат ссылок для RAG. | [ADR-001](../docs/adr/001-prompt-standard.md) |
| [`pattern-standard.md`](pattern-standard.md) | Форма паттерна библиотеки промптов. | [ADR-002](../docs/adr/002-pattern-standard.md) |
| [`ba-ontology.md`](ba-ontology.md) · [`ba-ontology.executable.md`](ba-ontology.executable.md) | Онтология BA: операции, процессы, артефакты, исполнители, gates. | [ADR-003](../docs/adr/003-ba-ontology.md) |
| [`artifact-naming-standard.md`](artifact-naming-standard.md) | Нейминг артефактов и промптов спицы. | [ADR-005](../docs/adr/005-artifact-team-naming.md), [ADR-006](../docs/adr/006-prompt-naming.md) |
| [`kb-standard.md`](kb-standard.md) | Формат цитирования, синхронизация глоссарий ↔ БЗ, pre-RAG механизм. | [ADR-007](../docs/adr/007-kb-standard.md) |
| [`industry-standards-standard.md`](industry-standards-standard.md) | Работа с отраслевыми стандартами и best practices. | [ADR-008](../docs/adr/008-industry-standards-standard.md) |
| [`bcreq-process-standard.md`](bcreq-process-standard.md) | Многоуровневый процесс формирования BCREQ. | [ADR-009](../docs/adr/009-bcreq-formation-process.md) |
| [`pages-ux-standard.md`](pages-ux-standard.md) | UX витрины GitHub Pages. | [ADR-010](../docs/adr/010-pages-ux.md) |
| [`runs-contract-standard.md`](runs-contract-standard.md) | Контракт прогона `runs/<год>/RUN-NNNN/`. | — |
| [`cascading-context-loading-standard.md`](cascading-context-loading-standard.md) | Каскадная загрузка контекста и `.executable.md`-компаньоны. | — |
| [`experiment-log-standard.md`](experiment-log-standard.md) | Фиксация экспериментов. | — |
| [`product-classification-contract.md`](product-classification-contract.md) | Классификация функциональности продукта Mango (`Domain → Capability → Feature → Atomic Function`). | — |
| [`team-directory.md`](team-directory.md) | Справочник команд Mango. | — |

## Как добавить стандарт

1. Проверьте, нет ли нормы в [`GLOSSARY.md`](GLOSSARY.md) или в рабочей копии
   Хаба: дублировать норму нельзя (правило разграничения выше).
2. Стандарт создаётся под носителем-решением — ADR в
   [`docs/adr/`](../docs/adr/), — если решение архитектурно значимо.
3. Добавьте строку в таблицу «Собственные стандарты спицы» и в
   [`pr-ops/artifact-map.md`](../pr-ops/artifact-map.md).
4. Стандарт живёт в статусе `draft` до утверждения Пользователем.
