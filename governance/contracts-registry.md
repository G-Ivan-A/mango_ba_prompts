---
status: draft
version: 0.1
updated: 2026-06-23
ai-generated: true
type: registry
layer: L2
rule_class: data
scope: contract-provenance
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/212"
related_artifacts:
  - "standards/executable-contract-standard.md"
---

# Реестр source/provenance контрактов

Этот L2-реестр хранит source/provenance и управленческую трассировку
контрактов. L1-контракт содержит только `contract_registry_id`; прямые
гиперссылки на L3-артефакты, `source_hub`, `source_sha`, `source_attachments`,
`depends_on` и `related_artifacts` в L1 не допускаются.

```yaml
contracts_registry:
  - contract_registry_id: CONTRACT-BCREQ-FR-GEN
    contract_path: governance/bcreq-fr-generation-contract.md
    contract_layer: L1
    rule_class: combat
    registry_status: active
    source_provenance:
      - kind: issue
        ref: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/196"
        rationale: "Initial BCREQ-FR generation contract creation."
      - kind: issue
        ref: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/208"
        rationale: "L3 runtime input boundary correction."
    approved_decisions:
      - "Accepted runtime rules must be embedded locally in L1."
      - "Taxonomy registries are L2 runtime inputs."
      - "L3 sources are provenance, not runtime inputs."
    rationale: "BCREQ-FR generation is the canonical L1 generation contract example."

  - contract_registry_id: CONTRACT-APPROVAL
    contract_path: governance/approval-contract.md
    contract_layer: L1
    rule_class: combat
    registry_status: needs-backfill
    source_provenance:
      - kind: legacy-source
        ref: "Правила согласования документа.txt"
        rationale: "Legacy source name is recorded here until stable repository provenance is backfilled."
    approved_decisions:
      - "Approval execution rules belong in L1."
      - "Source attachment provenance belongs in this registry."
    rationale: "Approval workflow is executable, while its origin evidence is governance data."

  - contract_registry_id: CONTRACT-RUNS
    contract_path: runs/CONTRACT.md
    contract_layer: L1
    rule_class: combat
    registry_status: needs-migration
    source_provenance:
      - kind: repository-artifact
        ref: standards/runs-contract-standard.md
        rationale: "Existing L3 run-contract standard used to design the data-near L1 contract."
    approved_decisions:
      - "Run recording rules must be available beside run data."
      - "The data-near L1 contract must not require reading the L3 standard at runtime."
    rationale: "Run evidence creation is a runtime workflow controlled by a data-near contract."

  - contract_registry_id: CONTRACT-GOLDEN-EXAMPLES
    contract_path: kb/golden-examples/CONTRACT.md
    contract_layer: L1
    rule_class: combat
    registry_status: active
    source_provenance:
      - kind: issue
        ref: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211"
        rationale: "Golden Examples lifecycle contract creation."
    approved_decisions:
      - "Approved examples are L2 data."
      - "The lifecycle contract for creating and verifying future examples is L1."
    rationale: "Golden Examples need executable lifecycle rules while the approved examples remain data."
```

## Правила обновления

- При создании или миграции L1-контракта добавляйте запись с уникальным
  `contract_registry_id`.
- Не переносите source/provenance обратно в L1-контракт.
- Если источник пока нестабилен или исторический, ставьте `registry_status:
  needs-backfill` и фиксируйте, что именно нужно восстановить.
