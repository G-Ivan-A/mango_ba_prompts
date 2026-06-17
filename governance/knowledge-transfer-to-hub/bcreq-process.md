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
  - "docs/adr/009-bcreq-formation-process.md"
  - "standards/bcreq-process-standard.md"
  - "governance/rfc-to-hub-001-knowledge-transfer.md"
---

# Передача знаний: процесс формирования BCREQ (бизнес- и системных требований)

## Название практики

Многоуровневый процесс формирования требований (BCREQ) с **горизонтальным
конвейером** подпроцессов и **вертикальной иерархией** детализации, со встроенными
**человеческими воротами** (human gates) и механизмом `needs-clarification`.

## Описание (что, как, зачем)

- **Что.** Процесс из 6 последовательных подпроцессов (П1–П6), разворачивающих
  бизнес-контекст в проверенные требования, с тремя обязательными точками решения
  человека (G1/G2/G3) между этапами.
- **Как.** [ADR #009](../../docs/adr/009-bcreq-formation-process.md) и стандарт
  [`standards/bcreq-process-standard.md`](../../standards/bcreq-process-standard.md)
  задают: вертикаль (нотация с точками — иерархия детализации требований) и
  горизонталь (П1→П6). На воротах G1/G2/G3 человек подтверждает переход; неполнота
  явно помечается состоянием `needs-clarification` (связь с онтологией,
  [`ba-ontology.md`](ba-ontology.md)).
- **Зачем.** Делает превращение «контекст → требования» воспроизводимым, с явным
  human-in-the-loop и без «тихого» проскакивания неполных мест.

## Обоснование (почему полезно другим проектам)

Каркас «конвейер + ворота человека + явная пометка неполноты» переиспользуем за
пределами требований — это общий паттерн для любого многоэтапного процесса
производства знаний с участием человека. Он прямо реализует принцип Хаба
**«финальные решения за человеком»** (`AI_GOVERNANCE.md`) и правило «молчание =
согласие лишь с текущим состоянием» из
[`knowledge-lifecycle-proposal.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/governance/rfc/knowledge-lifecycle-proposal.md):
ворота G1/G2/G3 — это и есть точки, где молчание не повышает статус.

## Примеры использования

- **Производство требований БА:** контекст заказчика → (П1–П6 с G1/G2/G3) →
  проверенный набор бизнес- и системных требований.
- **Шаблон для других пайплайнов:** структуру «этап → ворота человека → этап»
  можно применить к RFC-конвейеру самого Хаба (Hypothesis → RFC → Pattern с
  явными воротами).
- **Обработка неполноты:** `needs-clarification` не блокирует процесс, а
  фиксирует partial baseline для возврата.

## Что обобщить перед переносом (критерий C2)

Передавать **мета-паттерн** (конвейер этапов + типизированные human gates +
состояние неполноты), а конкретные П1–П6 — как референс-реализацию для BA-домена.
Сопоставить ворота с уже существующими в Хабе точками решения человека, чтобы не
вводить параллельную терминологию.

## Ссылки

- ADR-носитель: [`docs/adr/009-bcreq-formation-process.md`](../../docs/adr/009-bcreq-formation-process.md)
- Стандарт: [`standards/bcreq-process-standard.md`](../../standards/bcreq-process-standard.md)
- Umbrella-RFC: [`rfc-to-hub-001-knowledge-transfer.md`](../rfc-to-hub-001-knowledge-transfer.md)
- Контракт Хаба (родственный): [`AI_GOVERNANCE.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/6ddffdfff693d8279792cd1e9c4c5d94ee0dffcf/AI_GOVERNANCE.md)
