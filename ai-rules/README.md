---
status: canonical
version: 1.2
updated: 2026-07-16
temperature: 0.1
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-rules/README.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"
scope: mango_ba_prompts
---

# AI Rules

> **Рабочая копия стандарта Хаба.** Source of truth — [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-rules/README.md) на `source_sha`.
> Локально файл не редактируется: расхождение устраняется следующим синком
> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.

Дом правил поведения AI-агента и быстрой синхронизации внешнего агента:
onboarding-протокол и операционные инструкции агента. Граница `ai-rules/` vs
`ai-governance/` зафиксирована в
[ADR-007](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-07-adr-007-hub-root-structure.md).

## Содержимое

| Артефакт | Назначение |
| --- | --- |
| [agent-work-rules.md](agent-work-rules.md) | Основной контракт поведения агента: pre-flight, operating modes и Definition of Done. |
| [agent-onboarding-protocol.md](agent-onboarding-protocol.md) | Протокол онбординга и синхронизации AI-агента. |
| [adversarial-stress-testing.md](adversarial-stress-testing.md) | Повторяемая процедура проверки гипотез и решений попыткой опровержения. |

## Граница

| Сюда | Не сюда |
| --- | --- |
| Правила поведения агента, onboarding, быстрая синхронизация. | Политики уровня организации, compliance, ИБ — они в [ai-governance/](../ai-governance/README.md). |
