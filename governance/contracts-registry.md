# Реестр исполнимых контрактов
# Назначение: фиксировать source/provenance контрактов отдельно от runtime-контракта.
# В самом контракте указывается только contract_registry_id без гиперссылок на source/provenance.
contracts:
  - id: bcreq-fr-generation-contract
    path: "governance/bcreq-fr-generation-contract.md"
    version: 0.4
    status: active
    layer: L1
    rule_class: combat
    created: 2026-06-23
    updated: 2026-06-23
    provenance:
      issues:
        - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/196"
        - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/208"
        - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211"
        - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/215"
      prs:
        - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/202"
      rationale: "Проектная история создания, очистки L3 runtime-входов, Golden Examples lifecycle и перевода BCREQ-FR контракта в 100% YAML."
    integrates:
      - "kb/industry-taxonomy/registry.json"
      - "kb/mango-taxonomy/registry.json"
    related_artifacts:
      - "kb/golden-examples/CONTRACT.md"
      - "governance/approval-contract.md"
      - "runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md"
      - "experiments/issue-208/bcreq-1027-l3-boundary-dry-run.md"
    validated_by:
      - "scripts/validate_issue_196_bcreq_fr_contract.py"
      - "scripts/validate_issue_208_bcreq_fr_l3_boundary.py"
      - "scripts/validate_issue_211_golden_examples_contract.py"
      - "scripts/validate_issue_215_bcreq_fr_yaml_contract.py"
  - id: approval-contract
    path: "governance/approval-contract.md"
    version: 0.1
    status: needs-backfill
    layer: L1
    rule_class: combat
    created: 2026-06-23
    updated: 2026-06-23
    provenance:
      legacy_sources:
        - "Правила согласования документа.txt"
      rationale: "Legacy approval source is recorded here until stable repository provenance is backfilled."
    approved_decisions:
      - "Approval execution rules belong in L1."
      - "Contract source/provenance belongs in this registry."
    related_artifacts:
      - "governance/rfc-process.md"
      - "AI_GOVERNANCE.md"
    validated_by:
      - "scripts/validate_issue_193_approval_contract.py"
  - id: runs-contract
    path: "runs/CONTRACT.md"
    version: 0.1
    status: needs-migration
    layer: L1
    rule_class: combat
    created: 2026-06-23
    updated: 2026-06-23
    provenance:
      source_artifacts:
        - "standards/runs-contract-standard.md"
      rationale: "Existing L3 run-contract standard is the source for the data-near L1 run recording contract."
    approved_decisions:
      - "Run recording rules must be available beside run data."
      - "The data-near L1 contract must not require reading the L3 standard at runtime."
    related_artifacts:
      - "runs/README.md"
      - "runs/REGISTRY.md"
      - "runs/stats/by-type.md"
    validated_by:
      - "scripts/validate_issue_123_runs_contract.py"
      - "scripts/validate_issue_133_runs_restructure.py"
  - id: golden-examples-contract
    path: "kb/golden-examples/CONTRACT.md"
    version: 0.1
    status: active
    layer: L1
    rule_class: combat
    created: 2026-06-23
    updated: 2026-06-23
    provenance:
      issues:
        - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211"
      rationale: "Golden Examples lifecycle contract creation."
    approved_decisions:
      - "Approved examples are L2 data."
      - "The lifecycle contract for creating and verifying future examples is L1."
    related_artifacts:
      - "governance/bcreq-fr-generation-contract.md"
      - "governance/approval-contract.md"
    validated_by:
      - "scripts/validate_issue_211_golden_examples_contract.py"
