---
status: final
version: 0.1
updated: 2026-06-24
ai-generated: true
type: validation-report
scope: rfc-generation-contract
---

# RFC generation contract test report

## Scope

Issue #226 asks for an L1 executable contract that generates RFC documents as
L3 Markdown with YAML frontmatter. The contract must be 100% YAML and must not
edit existing RFC files or `governance/rfc-process.md`.

The validation used 11 existing RFC-like documents, the BCREQ-FR contract,
`standards/executable-contract-standard.md`, `governance/rfc-process.md`,
`docs/analysis/executable-contracts-and-rfc-problems.md` and external
RFC/design-document practices.

## Local corpus observations

The 11 existing RFC-like documents showed recurring gaps that the contract must
prevent:

- inconsistent frontmatter and status fields;
- problem, goal and solution mixed inside narrative sections;
- proposals described as prose rather than a machine-readable index;
- source references present in some RFCs but not enforced per problem;
- impact sections not consistently exposing `requires_adr`,
  `requires_standard` and `target_artifacts`;
- examples and implementation notes sometimes carrying normative weight.

The new contract addresses those gaps by requiring a complete problem list,
proposal rule index, traceability checks and explicit impact fields.

## Test matrix

| Test | Input condition | Expected result | Result |
| --- | --- | --- | --- |
| `RFC-GEN-TEST-01` | Real repository issue with analytics, research and existing RFC corpus | Generated RFC schema contains frontmatter, sections 1-8, problem IDs, proposal IDs and impact fields | Pass |
| `RFC-GEN-TEST-02` | RFC without explicit source for a problem | Generation stops or returns needs-clarification; `RFC-GEN-VAL-07` fails | Pass |
| `RFC-GEN-TEST-03` | Proposal changes governance or architecture decision boundary | Section 6 has `requires_adr: true` with non-empty `adr_reason`; no ADR transition process is defined | Pass |
| `RFC-GEN-TEST-04` | Proposal changes reusable normative project rule | Section 6 has `requires_standard: true` with non-empty `standard_reason`; no RFC-to-standard transition process is defined | Pass |

## Scenario details

### `RFC-GEN-TEST-01` real repository issue

Minimal generated RFC shape for issue #226:

- frontmatter includes `id`, `status`, `title`, `author`, `created`, `updated`,
  `layer: L3`, `type: rfc`, `related_contracts`, `target_artifacts`;
- section 2 problem list uses IDs such as `RFC-226-P1` and source refs to the
  issue, analysis report, existing RFC corpus and executable-contract standard;
- section 3 proposal index uses IDs such as `RFC-226-R1` and links every rule to
  one or more problem IDs;
- section 6 impact explicitly sets `requires_adr`, `requires_standard` and
  `target_artifacts`;
- section 8 canonical criteria verify every proposal rule.

Result: pass. The contract has enough structure to generate a complete RFC
without modifying existing RFC files.

### `RFC-GEN-TEST-02` RFC without explicit source

Input condition: a requested RFC states a problem but no `analytics_sources`,
`report_sources`, `research_sources`, `existing_rfcs` or `product_docs` entry
supports it.

Expected behavior:

- `missing_required_source_policy.action` returns
  `stop_or_return_needs_clarification`;
- no RFC is created until a source is available;
- `RFC-GEN-VAL-07` fails because every problem must have non-empty
  `source_refs`.

Result: pass. The contract forbids inventing source evidence or replacing a
source with general knowledge.

### `RFC-GEN-TEST-03` `requires_adr=true`

Input condition: proposal changes architecture, ownership boundary, irreversible
governance tradeoff or decision-record responsibility.

Expected impact block:

```yaml
impact:
  requires_adr: true
  adr_reason: "Proposal changes an architecture or governance decision boundary."
  requires_standard: false
  standard_reason: "none"
  target_artifacts:
    - "docs/adr/"
```

Result: pass. The contract requires the flag and reason while explicitly
forbidding RFC-to-ADR transition process rules.

### `RFC-GEN-TEST-04` `requires_standard=true`

Input condition: proposal changes reusable normative project rules or creates a
rule that future artifacts must follow.

Expected impact block:

```yaml
impact:
  requires_adr: false
  adr_reason: "none"
  requires_standard: true
  standard_reason: "Proposal changes reusable normative project rules."
  target_artifacts:
    - "standards/"
```

Result: pass. The contract requires the flag and reason while explicitly
forbidding RFC-to-standard transition process rules.

## Validation result

The issue-specific validator
`scripts/validate_issue_226_rfc_generation_contract.py` verifies:

- the contract parses as a two-document YAML stream;
- the runtime contract has no issue/PR provenance links;
- all five required input groups exist;
- frontmatter and sections 1-8 are fully specified;
- problem/proposal ID shapes and traceability rules are defined;
- impact fields cover `requires_adr`, `requires_standard` and
  `target_artifacts`;
- edge-case test scenarios are present;
- registry, changelog, run records, README, artifact map and workflow are wired.

Status: success.
