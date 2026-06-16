---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: contract
scope: industry-standards
related_artifacts:
  - "docs/adr/008-industry-standards-standard.md"
  - "standards/kb-standard.md"
  - "standards/GLOSSARY.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/97"
---

# Стандарт отраслевых стандартов и best practices

> Контракт-носитель [ADR-008](../docs/adr/008-industry-standards-standard.md).
> Нормативный словарь [RFC 2119](https://www.rfc-editor.org/info/bcp14)
> (**ДОЛЖНО** / **СЛЕДУЕТ** / **МОЖНО**). Версия `draft` до утверждения
> Пользователем (issue #97).

## Стороны и область

Контракт обязывает всех, кто ссылается на внешние стандарты и best practices в
артефактах, промптах и ADR. Термины уровня обязательности (Standard, Policy,
Practice, Guideline …) — в [GLOSSARY.md](GLOSSARY.md); здесь — различение
**внешних** источников и правила их применения.

## 1. Терминология

| Термин | Определение | Нормативность |
| --- | --- | --- |
| De jure стандарт | Утверждён органом стандартизации (ISO/IEC/IEEE, ГОСТ). | нормативный в своём контексте |
| De facto стандарт | Принят отраслью без формального органа (TM Forum). | по договорённости |
| Best practice | Рекомендуемый подход; не обязателен. | информативный |
| Framework/методология | Связная модель понятий и процессов (BABOK, ODA). | информативный/нормативный |
| Нормативная ссылка | Обязательна к применению в данном контексте. | нормативный |
| Информативная ссылка | Для справки. | информативный |

Различение «нормативное/информативное» — по ISO/IEC Directives, Part 2:
<https://www.iso.org/sites/directives/current/part2/index.xhtml>.

## 2. Правила применения

- **Правило И1 (верификация).** Источник **ДОЛЖЕН** быть проверен на
  существование (документ, редакция/год, полный URL) до цитирования; чек-лист —
  [KB: source-backed-analysis](../kb/practices/source-backed-analysis.md#чек-лист-проверки-источника).
- **Правило И2 (полный URL).** Каждая ссылка — **полным URL**.
- **Правило И3 (приоритет).** При конфликте применяется верхний tier: явное
  требование Пользователя → de jure → de facto → best practice → guideline;
  решение фиксируется ADR.
- **Правило И4 (локализация).** ГОСТ — РФ-контекст ТЗ; ISO/IEEE — международный;
  best practice — где нет обязательного стандарта.
- **Правило И5 (маркировка).** Ссылка помечается «нормативная» или
  «информативная».
- **Правило И6 (реестр).** Допускаются только источники из §3; новый — через
  issue/PR с подтверждённым URL.

## 3. Сверенный реестр источников

> Колонка «В issue #97» приведена для прослеживаемости. «⚠️ проверить» = указанный
> в issue идентификатор не сошёлся со сверенным; молча не заменяем — приводим оба.

| Источник | Tier | Норм/Инф | Сверенный URL | В issue #97 |
| --- | --- | --- | --- | --- |
| ISO/IEC/IEEE 29148:2018 | de jure | нормативный | <https://www.iso.org/standard/72089.html> · <https://standards.ieee.org/ieee/29148/6937/> | ⚠️ проверить: `iso.org/standard/72545.html` (действ. 72089); `ieee/29148/4378` |
| ISO/IEC 25010:2023 | de jure | нормативный | <https://www.iso.org/standard/78176.html> | ⚠️ проверить: `iso.org/standard/78405.html` (действ. 78176) |
| ГОСТ 34.602-2020 | de jure | нормативный (РФ) | <https://docs.cntd.ru/document/1200181804> | ⚠️ проверить: «ГОСТ 34.602-**2015**» (`1200124556`) — **редакции -2015 нет**; есть -89 и -2020 |
| ГОСТ 34.602-89 (истор.) | de jure | информативный | <https://standards.narod.ru/gosts/gost34/34-602-89.htm> | — |
| BABOK Guide v3 | framework/best practice | информативный | <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/> | `iiba.org/career-resources/a-body-of-knowledge` (вероятный редирект) |
| TM Forum Frameworx / ODA | de facto | информативный | <https://www.tmforum.org/oda/> · <https://www.tmforum.org/open-digital-architecture/> | `tmforum.org/oda/` |
| Anthropic Prompt Engineering Guide | best practice | информативный | <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview> | то же |
| ISO/IEC Directives, Part 2 | de jure | нормативный (терминология) | <https://www.iso.org/sites/directives/current/part2/index.xhtml> | — |

## Критерии соответствия (DoD)

- [ ] Каждая внешняя ссылка проверена (И1) и приведена полным URL (И2).
- [ ] Ссылка помечена нормативная/информативная (И5) и есть в реестре §3 (И6).
- [ ] Конфликты разрешены по tier (И3) и зафиксированы ADR.
- [ ] Расхождения с issue помечены «⚠️ проверить», а не заменены молча.
- [ ] `python3 scripts/validate_issue_97_ontology_standards.py` проходит.

## Источники

- ADR-008 (носитель): [docs/adr/008-industry-standards-standard.md](../docs/adr/008-industry-standards-standard.md)
- ISO/IEC Directives, Part 2: <https://www.iso.org/sites/directives/current/part2/index.xhtml>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
- ISO/IEC 25010:2023: <https://www.iso.org/standard/78176.html>
- ГОСТ 34.602-2020: <https://docs.cntd.ru/document/1200181804>
- BABOK Guide v3: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- TM Forum ODA: <https://www.tmforum.org/oda/>
- Anthropic Prompt Engineering Guide: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>
- RFC 2119 / BCP 14: <https://www.rfc-editor.org/info/bcp14>
