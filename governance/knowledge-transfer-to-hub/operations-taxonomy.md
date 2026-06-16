---
status: draft
version: 0.1
updated: 2026-06-16
ai-generated: true
type: knowledge-transfer
scope: strategic
target_repo: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
source_spoke: "https://github.com/G-Ivan-A/mango_ba_prompts"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/105"
related_artifacts:
  - "docs/adr/004-operations-taxonomy.md"
  - "governance/rfc-to-hub-001-knowledge-transfer.md"
---

# Передача знаний: таксономия когнитивных операций БА

## Название практики

Таксономия из **13 когнитивных операций** бизнес-анализа с маппингом на внешние
методологические стандарты (BABOK Knowledge Areas, ISO/IEC/IEEE 29148) и
профилем аудита для каждой операции.

## Описание (что, как, зачем)

- **Что.** Замкнутый набор атомарных действий аналитика (например: извлечение,
  классификация, моделирование, верификация, формализация требований и т.д.),
  каждое из которых — узел онтологии ([`ba-ontology.md`](ba-ontology.md)) и точка
  привязки промптов.
- **Как.** Зафиксировано в [ADR #004](../../docs/adr/004-operations-taxonomy.md):
  каждая операция сопоставлена с областями знаний BABOK и пунктами ISO 29148,
  снабжена профилем аудита (как проверять качество результата операции).
- **Зачем.** Превращает «промпт для БА» в «промпт для конкретной операции с
  известным методологическим основанием» — снимает произвол в наборе действий и
  даёт критерии приёмки.

## Обоснование (почему полезно другим проектам)

Хаб ведёт RFC
[`methodology-research-and-proposals.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/methodology-research-and-proposals.md)
(PR #246) — площадку для методологического маппинга. Таксономия Mango — готовый,
проверенный на практике вклад: общий язык операций для всех BA-команд экосистемы
и мост к внешним стандартам (BABOK/ISO), который Хаб может принять как Base
Registry, а споки — расширять (паттерн Base Registry / Local Extension из
[`external-knowledge-integration.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/external-knowledge-integration.md)).

## Примеры использования

- **Каталог промптов:** каждый промпт указывает свою операцию → автоматическая
  группировка и поиск «чем закрыть операцию X».
- **Аудит качества:** профиль аудита операции = чек-лист приёмки её результата.
- **Сверка с Хабом:** RFC-SYNC-004 предлагает согласовать 13 операций ↔ Knowledge
  Areas BABOK Хаба (см. [`sync-matrix-2026-06-17.md`](../sync-matrix-2026-06-17.md)).

## Что обобщить перед переносом (критерий C2)

Передавать как **маппинг-таблицу** (операция → BABOK/ISO → профиль аудита), а не
как жёсткий список из 13: другие домены могут иметь иной набор. Ценность для Хаба —
*метод сопоставления* операций с внешними стандартами + конкретная BA-таблица как
референс. Согласовать с RFC-SYNC-004, чтобы перенос и сверка не противоречили.

## Ссылки

- ADR-носитель: [`docs/adr/004-operations-taxonomy.md`](../../docs/adr/004-operations-taxonomy.md)
- Онтология (контекст): [`ba-ontology.md`](ba-ontology.md)
- Umbrella-RFC: [`rfc-to-hub-001-knowledge-transfer.md`](../rfc-to-hub-001-knowledge-transfer.md)
- Связанный RFC сверки: RFC-SYNC-004 в [`rfc-register.md`](../rfc-register.md)
- RFC Хаба: [`methodology-research-and-proposals.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/methodology-research-and-proposals.md)
