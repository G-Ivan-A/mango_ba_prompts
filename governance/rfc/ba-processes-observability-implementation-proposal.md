---
id: RFC-243
status: draft
title: "RFC-243: BA process and observability implementation proposal"
author: "OpenAI Codex"
created: 2026-06-25
updated: 2026-06-25
layer: L3
type: rfc
related_contracts:
  - "governance/rfc-generation-contract.md"
  - "governance/rfc-process.md"
  - "governance/bcreq-fr-generation-contract.md"
  - "runs/CONTRACT.md"
  - "standards/executable-contract-standard.md"
target_artifacts:
  - "docs/ba-processes/00-index.md"
  - "docs/ba-processes/00-index.executable.md"
  - "standards/ba-ontology.md"
  - "governance/bcreq-fr-generation-contract.md"
  - "runs/CONTRACT.md"
  - "kb/operation-prompt-mapping/registry.json"
  - "runs/REGISTRY.md"
  - "runs/stats/by-process.md"
  - "runs/stats/by-type.md"
---

# RFC-243: BA process and observability implementation proposal

This RFC records the agreed decisions from the BA-process and observability
research chain. It is a proposal only: it does not implement standards,
contracts, prompt mappings, run metadata, or existing BA artifacts.

## 1. Context and motivation

```yaml
context:
  source_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/243"
  source_pr: "https://github.com/G-Ivan-A/mango_ba_prompts/pull/244"
  chain: "research -> rfc/adr -> standard -> artifact"
  proposal_scope: "L3 governance proposal for later standard and artifact changes"
  product_docs: "not_applicable"
  source_refs:
    - id: A3
      path: "docs/analysis/2026-06-25-runs-observability-research.md"
      signal: "Runs lack prompt-level observability, versioning, lineage, and prompt-to-rule mapping."
    - id: A4
      path: "docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md"
      signal: "BCREQ-FR is applied as a monolithic contract because L1 contracts are not linked to operation/prompt mappings."
    - id: A5
      path: "docs/analysis/2026-06-25-ba-processes-industry-analysis.md"
      source_pr: "https://github.com/G-Ivan-A/mango_ba_prompts/pull/234"
      signal: "The project model matches industry practice but needs explicit atomic/composite taxonomy, API spec, RTM, and BABOK operation alignment."
    - id: BA_PROCESS_INDEX
      path: "docs/ba-processes/00-index.md"
      signal: "Current BA process map has nine processes, thirteen operations, and prompt chains."
    - id: BA_PROCESS_EXECUTABLE
      path: "docs/ba-processes/00-index.executable.md"
      signal: "Executable companion for machine-readable process navigation."
    - id: BCREQ_FR_CONTRACT
      path: "governance/bcreq-fr-generation-contract.md"
      signal: "L1 generation contract exists but does not declare applied operations."
    - id: RUNS_CONTRACT
      path: "runs/CONTRACT.md"
      signal: "Run metadata contract exists but does not declare applied prompts or prompt lineage."
    - id: EXECUTABLE_CONTRACT_STANDARD
      path: "standards/executable-contract-standard.md"
      signal: "L1 contracts are self-contained; reusable mappings belong in L2 registries, not runtime-only L3 prose."
    - id: RFC_GENERATION_CONTRACT
      path: "governance/rfc-generation-contract.md"
      signal: "RFC artifacts must be L3 proposals with explicit problem, proposal, impact, and canonical criteria."
  permission_note:
    upstream_permission: "READ"
    fork_permission: "ADMIN"
    fork_tracking_issues:
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/7"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/8"
```

### Почему RFC, а не ADR

The artifact type is RFC, not ADR, because issue #243 asks to propose a coherent
governance and implementation path across process documentation, standards, L1
contracts, L2 registry data, and run metadata. The decision is not yet an
accepted architecture record; it is a reviewable proposal that must become
canonical before downstream implementation. An ADR would be appropriate only if
a human reviewer needs to record a final architecture choice after RFC review.

## 2. Problem

```yaml
problems:
  - id: RFC-243-P1
    title: "Research decisions are not fixed in an RFC/ADR artifact."
    source_refs:
      - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/243"
      - "docs/analysis/2026-06-25-runs-observability-research.md"
      - "docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md"
      - "docs/analysis/2026-06-25-ba-processes-industry-analysis.md"
    effect: "The chain research -> rfc/adr -> standard -> artifact is blocked."
  - id: RFC-243-P2
    title: "Atomic and composite BA artifact taxonomy is not canonical."
    source_refs:
      - "docs/analysis/2026-06-25-ba-processes-industry-analysis.md"
      - "standards/ba-ontology.md"
    effect: "API specification, RTM entry, FRD/SRS distinction, and BCREQ type semantics remain ambiguous."
  - id: RFC-243-P3
    title: "Operation hierarchy is mixed with implementation-level decomposition."
    source_refs:
      - "docs/ba-processes/00-index.md"
      - "docs/analysis/2026-06-25-ba-processes-industry-analysis.md"
    effect: "The project has useful thirteen-operation detail but lacks a first-class six-operation BABOK-compatible layer."
  - id: RFC-243-P4
    title: "Contracts cannot declare which BA operations they execute."
    source_refs:
      - "docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md"
      - "governance/bcreq-fr-generation-contract.md"
    effect: "BCREQ-FR remains a monolithic contract application instead of a traceable operation sequence."
  - id: RFC-243-P5
    title: "Runs cannot record applied prompt versions and lineage."
    source_refs:
      - "docs/analysis/2026-06-25-runs-observability-research.md"
      - "runs/CONTRACT.md"
    effect: "It is not possible to reconstruct prompt_id, version, model settings, prompt result, or previous_run_id from run metadata."
  - id: RFC-243-P6
    title: "Migration conflicts are not staged as issue-backed implementation work."
    source_refs:
      - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/243"
      - "governance/BACKLOG.md"
    effect: "Without a sprint backlog, later implementation may change standards and artifacts out of order."
```

## 3. Proposal

```yaml
proposal:
  RFC-243-R1:
    title: "Use RFC as the decision artifact."
    decision: "RFC-243 remains an L3 RFC draft until human review moves it to canonical, rejects it, or asks for an ADR."
    rationale: "The proposal coordinates several downstream artifacts and standards; it is not an already accepted architecture decision."
  RFC-243-R2:
    title: "Fix atomic BA artifacts as one-source/one-owner/one-check units."
    atomic_artifacts:
      - "Singular requirement"
      - "User Story"
      - "Use Case"
      - "Business Rule"
      - "Glossary term"
      - "API specification (OpenAPI/TMF Open API)"
      - "RTM entry"
    atomic_definition: "One source, one owner, one check."
  RFC-243-R3:
    title: "Fix composite BA artifacts as aggregates of atomic artifacts."
    composite_artifacts:
      - "BRD"
      - "FRD/SRS"
      - "RFP Response/Bid Requirements"
    classification:
      BCREQ-FR: "`type: frd`"
      BCREQ-SR: "`type: srs`"
    composite_definition: "Aggregation of atomics plus structure and traceability."
  RFC-243-R4:
    title: "Adopt six BABOK-compatible operations as the top-level operation layer."
    operations:
      - "Elicitation"
      - "Analysis"
      - "Documentation"
      - "Validation"
      - "Verification"
      - "Management"
    decomposition_rule: "Existing thirteen operations remain as project-specific decomposition/suboperations."
  RFC-243-R5:
    title: "Introduce an L2 operation-prompt mapping registry."
    target: "kb/operation-prompt-mapping/registry.json"
    key_edge: "operation_id -> prompt_id@version"
    minimum_fields:
      - "operation_id"
      - "prompt_id"
      - "prompt_version"
      - "source_process"
      - "artifact_scope"
      - "contract_rule_refs"
      - "owner"
  RFC-243-R6:
    title: "Add operation and prompt trace fields in later contract/run migrations."
    contract_field: "applied_operations"
    run_field: "applied_prompts"
    lineage_field: "previous_run_id"
    boundary: "Contracts reference operation IDs; runs record prompt IDs and versions used during execution."
  RFC-243-R7:
    title: "Reconcile process documentation before implementation."
    order:
      - "First reconcile docs/ba-processes/00-index.md with the industry-normal six-operation layer."
      - "Then update ontology/standards for atomic/composite artifacts."
      - "Then implement the L2 registry and L1/run metadata fields."
    reason: "The implementation proposal depends on process-model reconciliation."
  RFC-243-R8:
    title: "Use an issue-backed sprint backlog."
    backlog: "governance/BACKLOG.md#спринт-rfc-243"
    upstream_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/243"
    fork_tracking_issues:
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/7"
      - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/8"
```

## 4. Alternatives considered

```yaml
alternatives:
  - id: RFC-243-A1
    title: "Write an ADR immediately."
    outcome: "rejected_for_now"
    reason: "The work is still a proposal across several governance surfaces; an ADR would prematurely record an accepted architecture decision."
  - id: RFC-243-A2
    title: "Implement standards and contracts directly in issue #243."
    outcome: "rejected"
    reason: "Issue #243 explicitly requires documentation and a sprint proposal, not implementation of standards, contracts, runs, prompts, or existing artifacts."
  - id: RFC-243-A3
    title: "Keep operation-to-prompt mapping only in docs/ba-processes/00-index.md."
    outcome: "rejected"
    reason: "Prose is useful for navigation but cannot safely serve L1 contracts and run validators as an L2 registry."
  - id: RFC-243-A4
    title: "Embed prompt mapping directly in each L1 contract."
    outcome: "rejected"
    reason: "This duplicates prompt mappings, increases drift, and conflicts with the L1 self-contained contract plus L2 reusable-data boundary."
```

## 5. Rationale

```yaml
rationale:
  source_traceability:
    - "A3 supports RFC-243-R5 and RFC-243-R6: prompt observability requires prompt IDs, prompt versions, and lineage in runs."
    - "A4 supports RFC-243-R5 and RFC-243-R6: contract application needs an operation layer before prompt-level execution can be audited."
    - "PR #234 / A5 supports RFC-243-R2, RFC-243-R3, and RFC-243-R4: industry practice separates atomic artifacts, composite documents, and top-level BA operations."
  boundary_rules:
    - "RFC-243 is L3 governance and does not implement L1/L2 artifacts."
    - "L2 registry data is the right home for operation_id -> prompt_id@version because it is reusable by contracts, runs, and validators."
    - "L1 contracts should reference applied_operations, while runs should record applied_prompts with concrete prompt versions."
  migration_order:
    - "The process index must be reconciled before generated contracts can safely reference operation IDs."
    - "The artifact ontology must define atomic/composite/API/RTM semantics before BCREQ-FR and BCREQ-SR type fields can be migrated."
    - "Run observability should follow the registry and contract-field changes so validators can check real references."
```

## 6. Impact

```yaml
impact:
  requires_adr: false
  adr_reason: "This RFC is the reviewable proposal. No irreversible architecture decision is accepted in this PR."
  requires_standard: true
  standard_reason: "Later implementation will need normative updates to BA ontology, process documentation, contract fields, and run metadata rules."
  target_artifacts:
    - "docs/ba-processes/00-index.md"
    - "docs/ba-processes/00-index.executable.md"
    - "standards/ba-ontology.md"
    - "governance/bcreq-fr-generation-contract.md"
    - "runs/CONTRACT.md"
    - "kb/operation-prompt-mapping/registry.json"
    - "runs/REGISTRY.md"
    - "runs/stats/by-process.md"
    - "runs/stats/by-type.md"
  conflicts:
    - id: RFC-243-C1
      description: "`type: contract` is overloaded in some L3-adjacent artifacts and must not be reused for BCREQ-FR/BCREQ-SR document type classification."
      migration: "Audit and migrate metadata only in dedicated implementation issues."
    - id: RFC-243-C2
      description: "Existing thirteen operations are valuable detail but not the canonical top-level operation set."
      migration: "Preserve them as suboperations when adding the six-operation layer."
    - id: RFC-243-C3
      description: "Current runs do not contain prompt lineage."
      migration: "Add new optional fields first; backfill only when evidence exists."
  non_implementation_guards:
    - "This RFC does not implement kb/operation-prompt-mapping/registry.json."
    - "This RFC does not change standards/ba-ontology.md."
    - "This RFC does not change governance/bcreq-fr-generation-contract.md."
    - "This RFC does not change runs/CONTRACT.md."
```

## 7. Implementation plan

```yaml
implementation_plan:
  status: "proposal_only"
  waves:
    - wave: 0
      title: "Decision gate"
      tasks:
        - title: "decision: зафиксировать RFC-243 governance proposal"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
          type: "decision"
          priority: "P1"
          dependency_mode: "independent"
    - wave: 1
      title: "Process and taxonomy reconciliation"
      tasks:
        - title: "implementation: сверить 00-index.md с BABOK-операциями"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"
          type: "implementation"
          priority: "P1"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
        - title: "implementation: обновить БА-онтологию для atomic-composite taxonomy"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4"
          type: "implementation"
          priority: "P1"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"
    - wave: 2
      title: "Mapping and execution metadata"
      tasks:
        - title: "implementation: создать L2-реестр operation-prompt mapping"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"
          type: "implementation"
          priority: "P1"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/1"
        - title: "implementation: добавить applied_operations в generation contracts"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5"
          type: "implementation"
          priority: "P1"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/3"
        - title: "implementation: добавить applied_prompts и lineage в runs contract"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6"
          type: "implementation"
          priority: "P1"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/2"
    - wave: 3
      title: "Validation and domain follow-up"
      tasks:
        - title: "implementation: обновить валидаторы и статистику под трассируемость"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/7"
          type: "implementation"
          priority: "P2"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/5"
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/6"
        - title: "research: оценить eTOM/SID как доменные БА-артефакты"
          issue: "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/8"
          type: "research"
          priority: "P3"
          dependency_mode: "dependent"
          depends_on:
            - "https://github.com/konard/G-Ivan-A-mango_ba_prompts/issues/4"
  note: "The fork issue URLs are used because the current GitHub token cannot create upstream issues or labels."
```

## 8. Canonical criteria

```yaml
canonical_criteria:
  - id: RFC-243-CC1
    criterion: "A human reviewer accepts RFC as the correct artifact type or explicitly requests ADR conversion."
  - id: RFC-243-CC2
    criterion: "Atomic and composite artifact decisions are accepted without changing standards in this PR."
  - id: RFC-243-CC3
    criterion: "The six-operation BABOK layer and thirteen-operation decomposition rule are accepted."
  - id: RFC-243-CC4
    criterion: "The operation_id -> prompt_id@version L2 registry is accepted as a future implementation target."
  - id: RFC-243-CC5
    criterion: "`applied_operations` for contracts and `applied_prompts` for runs are accepted as future migration fields."
  - id: RFC-243-CC6
    criterion: "The sprint backlog is accepted as the implementation sequence, with upstream issues recreated if maintainers require upstream tracking."
```
