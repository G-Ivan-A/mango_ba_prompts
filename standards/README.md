---
status: draft
version: 0.3
updated: 2026-11-06
ai-generated: true
type: index
scope: standards
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/265"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/387"
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
| [`bcreq-sections/`](bcreq-sections/README.md) | Мета-стандарты восьми разделов BCREQ: «необходимо и достаточно», стиль (короткий КС1–КС7, бюрократический БС1–БС5), паттерны, circuit breakers, чек-листы; словари D1–D11 для сверки глоссария. | [ADR-012](../docs/adr/2026-10-adr-012-bcreq-meta-standards.md) |
| [`bcreq-composition-standard.md`](bcreq-composition-standard.md) | Стек стандартов по разделам BCREQ, правила композиции К1–К7 для кросс-продуктовых доработок, TM Forum ODA как альтернатива (ODA-1…ODA-3), профили продуктов. | [ADR-012](../docs/adr/2026-10-adr-012-bcreq-meta-standards.md) |
| [`bcreq-prompt-architecture.md`](bcreq-prompt-architecture.md) | Архитектура промптов BCREQ: Промпт 0, шаблон шага, stepwise / oneshot, слияния М1–М4, состав набора. | [ADR-012](../docs/adr/2026-10-adr-012-bcreq-meta-standards.md) |
| [`bcreq-flow-glossary.md`](bcreq-flow-glossary.md) | Словарь потока BCREQ (BL-150): цепочка Поток → Процесс → Операция → Артефакт, шаг, гейт и его типы (`человек`, `гибрид`, `llm`, `код`), ключевые гейты, стадия, префиксы ID. Сужает `GLOSSARY.md` Хаба, не противоречит ему. | [RFC #427](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md) (DEC-427-01, поправка 0.4) |
| [`bcreq-runtime-references.md`](bcreq-runtime-references.md) | Справочники mango-ba-ai-runtime для промптов потока BCREQ (BL-154, BL-155): перечень И-1…И-10, требования ТС-1…ТС-7, закреплённый SHA — одна точка обновления, каталог продуктов runtime (И-2, BL-163), М-4 — чтение каталога промптом шага (BL-156а), заглушка З-2, задачи для runtime. | [RFC #427](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md) (DEC-427-09, DEC-427-10, поправка 0.4) |
| [`bcreq-prompt-base-standard.md`](bcreq-prompt-base-standard.md) | Базовый стандарт ручного промпта BCREQ «по тесту» (BL-151): общая часть 39 стандартов классов правилами БС-01…БС-36 с источником, справочники runtime ссылкой, типы гейтов шага. | [RFC #427](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md) (DEC-427-05, DEC-427-07, поправка 0.5) |
| [`bcreq-prompt-profiles.md`](bcreq-prompt-profiles.md) | Восемь профилей «по тесту» (BL-152): INGEST, EXTRACT, ANALYZE, ELICIT, GENERATE, VERIFY, TRANSFORM, RECORD; свои MUST-правила, каждая из 39 операций — в одном профиле. | [RFC #427](../docs/rfc/2026-11-bcreq-flow-processes-prompts.md) (DEC-427-05, DEC-427-07, поправка 0.5) |
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

## Проект потока ТТЗ

[RFC-TTZ-001](../docs/rfc/2026-11-ttz-feasibility-flow.md) (`proposed`, issue #466)
задаёт проект контракта отчётности и пробного потока оценки тендерных ТЗ.
На сайте он показан отдельным сворачиваемым подразделом после BCREQ;
индустриальная практика — третьим. Это предложение, не утверждённая норма.
Текущая онтология применяется без изменения; независимое сопоставление
внешних понятий и продуктов описано в RFC. После решения — ручная проба
BL-177, только затем нормативное оформление и автоматизация BL-178.
