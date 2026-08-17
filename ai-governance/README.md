---
status: canonical
version: 1.2
updated: 2026-07-16
temperature: 0.1
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/README.md"
source_sha: "3bfa4103c9efbbd59bc951814884920e406982e2"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"
scope: mango_ba_prompts
---

# AI Governance

> **Рабочая копия стандарта Хаба.** Source of truth — [`hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/ai-governance/README.md) на `source_sha`.
> Локально файл не редактируется: расхождение устраняется следующим синком
> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.

Дом политик уровня организации: ограничения государства, бизнес-правила,
информационная безопасность, внешний compliance и другие обязательства уровня
политики. Граница `ai-governance/` vs `ai-rules/` зафиксирована в
[ADR-007](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/docs/adr/2026-07-adr-007-hub-root-structure.md).

## Граница

| Сюда | Не сюда |
| --- | --- |
| Политики, compliance, внешние ограничения, ИБ, бизнес-правила уровня политики. | Правила поведения агента и быстрая синхронизация внешнего агента — они в [ai-rules/](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/3bfa4103c9efbbd59bc951814884920e406982e2/ai-rules). |
| Обязательства уровня политики. | Внешние практики AI-governance экосистемы — они в [practices/ai-governance/](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/3bfa4103c9efbbd59bc951814884920e406982e2/practices/ai-governance/README.md). |

## Содержимое

| Артефакт | Назначение |
| --- | --- |
| [ai-governance.md](ai-governance.md) | Основной policy-контракт: роли, human decision rights, ограничения и эскалация. |
| [agent-security-checklist.md](agent-security-checklist.md) | Единый risk-based checklist и трасса покрытия OWASP LLM Top 10:2025 / SAIF для agent work. |

## Статус

Policy/compliance-материал физически размещается здесь по ADR-007. Новые
политики добавляются через issue -> PR -> human review.
