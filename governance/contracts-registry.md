# Реестр исполнимых контрактов
# Назначение: фиксировать provenance контрактов отдельно от runtime-контракта.
# В самом контракте указывается только contract_registry_id без гиперссылок на provenance.
contracts:
  - id: bcreq-fr-generation-contract
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
