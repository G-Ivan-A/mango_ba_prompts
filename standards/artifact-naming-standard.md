---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: contract
scope: artifact-naming
related_artifacts:
  - "docs/adr/005-artifact-team-naming.md"
  - "standards/team-directory.md"
  - "standards/ba-ontology.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
---

# Стандарт нейминга артефактов

> Контракт-носитель [ADR-005](../docs/adr/005-artifact-team-naming.md). Нормативный
> словарь [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**). Версия `draft` до утверждения
> Пользователем (issue #97).

## Стороны и область

Контракт обязывает всех, кто создаёт идентификаторы аналитических артефактов
(FR, TZ, US, UC, BCREQ и др. из реестра 30 типов
[ba-ontology.md §4](ba-ontology.md)). Имена промптов регулируются отдельно
([prompt-standard.md](prompt-standard.md)), имена документов-стандартов — §3 ниже.

## 1. Схема идентификатора артефакта

```text
[<TEAM>:]<TYPE>-<NNN>[.<под-уровень>][-v<major>]
```

- **Правило N1.** `<TYPE>` **ДОЛЖЕН** быть кодом из каталога §2 (UPPERCASE,
  ≤6 символов).
- **Правило N2.** `<NNN>` **ДОЛЖЕН** быть числом ≥3 цифр с ноль-паддингом
  (`001`), уникальным в пределах пары `(<TEAM>, <TYPE>)`.
- **Правило N3.** `<TEAM>` **МОЖНО** опускать при единственном владельце; если
  указан — **ДОЛЖЕН** быть кодом из [team-directory.md](team-directory.md) и
  отделяться двоеточием.
- **Правило N4.** `.<под-уровень>` **СЛЕДУЕТ** использовать только для
  иерархических артефактов (BCREQ); формат — точечная нотация (`.2.1`).
- **Правило N5.** Идентификатор **НЕ ДОЛЖЕН** перегружаться: не дублировать в нём
  то, что уже выражено типом/реестром/frontmatter (баланс атомарности и
  простоты — НФТ).

## 2. Каталог кодов типов (все 30 типов реестра)

Коды соответствуют реестру артефактов [ba-ontology.md §4](ba-ontology.md)
(A01-A30). Колонка «Пример ID» — доказательство ФТ-3 «примеры для всех типов
артефактов».

| Реестр | Тип | Код | Пример ID | Пример с командой |
| --- | --- | --- | --- | --- |
| A01 | `asr-transcript-raw` | `ASR` | `ASR-001` | `CCMO:ASR-001` |
| A02 | `transcript-clean` | `TRN` | `TRN-001` | `CCMO:TRN-001` |
| A03 | `customer-letter` | `LET` | `LET-001` | `CCMO:LET-001` |
| A04 | `meeting-notes` | `NOTE` | `NOTE-001` | `BCREQ:NOTE-001` |
| A05 | `raw-requirement` | `RREQ` | `RREQ-001` | `BCREQ:RREQ-001` |
| A06 | `tender-spec-external` | `TND` | `TND-001` | `CCMO:TND-001` |
| A07 | `task-glossary` | `GLO` | `GLO-001` | `BCREQ:GLO-001` |
| A08 | `customer-questions` | `QST` | `QST-001` | `BCREQ:QST-001` |
| A09 | `meeting-summary` | `SUM` | `SUM-001` | `CCMO:SUM-001` |
| A10 | `business-alignment-pack` | `BAP` | `BAP-001` | `CCMO:BAP-001` |
| A11 | `user-story` | `US` | `US-012` | `BCREQ:US-012` |
| A12 | `acceptance-criteria` | `AC` | `AC-031` | `BCREQ:AC-031` |
| A13 | `use-case` | `UC` | `UC-003` | `BCREQ:UC-003` |
| A14 | `uml-bpmn-diagram` | `DGM` | `DGM-004` | `BCREQ:DGM-004` |
| A15 | `fr-section` | `FR` | `FR-001` | `CCMO:FR-001` |
| A16 | `constraints-section` | `CON` | `CON-002` | `CCMO:CON-002` |
| A17 | `technical-details-section` | `TECH` | `TECH-007` | `CCMO:TECH-007` |
| A18 | `feature-spec-kk` | `FSPEC` | `FSPEC-009` | `CCMO:FSPEC-009` |
| A19 | `tz-contract` | `TZ` | `TZ-005` | `CCMO:TZ-005` |
| A20 | `defect-report` | `DEF` | `DEF-007` | `CCMO:DEF-007` |
| A21 | `quality-summary` | `QS` | `QS-003` | `CCMO:QS-003` |
| A22 | `risk-register` | `RISK` | `RISK-002` | `CCMO:RISK-002` |
| A23 | `impact-map` | `IMP` | `IMP-006` | `CCMO:IMP-006` |
| A24 | `reverse-requirements` | `RREV` | `RREV-001` | `CCMO:RREV-001` |
| A25 | `release-readiness-checklist` | `RRC` | `RRC-001` | `CCMO:RRC-001` |
| A26 | `coverage-matrix` | `COV` | `COV-002` | `CCMO:COV-002` |
| A27 | `traceability-matrix` | `TRC` | `TRC-001` | `BCREQ:TRC-001` |
| A28 | `analysis-note` | `AN` | `AN-010` | `BCREQ:AN-010` |
| A29 | `status-backlog` | `BKL` | `BKL-001` | `BCREQ:BKL-001` |
| A30 | `bcreq` | `BCREQ` | `BCREQ-014.3` | `BCREQ:BCREQ-014.3` |

- **Правило N6.** Новый тип артефакта = новая строка в
  [ba-ontology.md §4](ba-ontology.md) **и** новый код здесь (уникальный,
  ≤6 символов).

## 3. Нейминг документов-стандартов

| Вид | Каталог | Схема | Пример |
| --- | --- | --- | --- |
| Контракт-правило | `standards/` | `<scope>-standard.md` | `prompt-standard.md` |
| Контракт от внешнего источника | `standards/` | `<scope>-contract.md` | `product-classification-contract.md` |
| Справочник/реестр | `standards/` | `<scope>-directory.md` | `team-directory.md` |
| ADR (стандарты) | `docs/adr/` | `<NNN>-<kebab-slug>.md` | `005-artifact-team-naming.md` |
| ADR (governance) | `docs/adr/` | `<NNNN>-<kebab-slug>.md` | `0003-creative-mode-governance.md` |

- **Правило N7.** `<scope>` **ДОЛЖЕН** совпадать с полем `scope` во frontmatter
  документа.

## 4. Нейминг BCREQ (многоуровневый)

```text
BCREQ-<NNN>            ← корень (уровень 0)
BCREQ-<NNN>.<k>        ← уровень 1
BCREQ-<NNN>.<k>.<m>    ← уровень 2 …
```

- **Правило N8.** Под-уровень **ДОЛЖЕН** ссылаться на существующий родитель;
  незавершённый под-уровень помечается состоянием `needs-clarification`
  ([ba-ontology.md §5](ba-ontology.md), ФТ-7).

## Критерии соответствия (DoD)

- [ ] ID матчит `[<TEAM>:]<TYPE>-<NNN>[.<под>][-v<major>]`.
- [ ] `<TYPE>` есть в каталоге §2; `<TEAM>` (если есть) — в team-directory.
- [ ] Все 30 типов реестра имеют код и пример (§2).
- [ ] Имя не перегружено (N5).
- [ ] `python3 scripts/validate_issue_97_ontology_standards.py` проходит.

## Источники

- ISO/IEC/IEEE 29148:2018 (unique requirement identifier, traceability):
  <https://www.iso.org/standard/72089.html>
- BABOK Guide v3 (RLCM — Trace Requirements):
  <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ГОСТ 34.602-2020 (структура ТЗ): <https://docs.cntd.ru/document/1200181804>
