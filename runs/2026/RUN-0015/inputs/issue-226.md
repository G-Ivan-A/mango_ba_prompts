---
status: final
version: 0.1
updated: 2026-06-24
ai-generated: true
type: run-input
scope: issue-226
---

# Issue #226 input summary

Issue #226 requires a new executable L1 contract
`governance/rfc-generation-contract.md` for generating RFC documents as L3
Markdown with YAML frontmatter.

The required contract properties are:

- 100% YAML body, no Markdown prose in the contract itself.
- Runtime contract is L1 and does not embed provenance links; provenance belongs
  to `governance/contracts-registry.md`.
- Full input groups: `analytics_sources`, `report_sources`,
  `research_sources`, `existing_rfcs`, `product_docs`.
- Generated RFC frontmatter fields: `id`, `status`
  (`draft/review/canonical/deprecated`), `title`, `author`, `created`,
  `updated`, `layer`, `type`, `related_contracts`, `target_artifacts`.
- Generated RFC sections 1-8: context and motivation, problem, proposal,
  alternatives, rationale, impact, optional implementation plan, canonical
  criteria.
- Problem section uses a YAML list with stable IDs like `RFC-NNN-P1`.
- Proposal section uses a YAML rule index with stable IDs like `RFC-NNN-R1`.
- Every problem has a source; every proposal links to a problem.
- Section 6 explicitly has `requires_adr`, `requires_standard` and
  `target_artifacts`.
- Style rules require concise, unambiguous, verifiable wording, no empty
  phrases, no mixing problem/goal/solution, active subject, straight quotes for
  terms and backticks for stable IDs.
- Validation covers required sections, machine-readable problem/proposal
  structures, traceability and transition impact fields.
- Test cases must cover a real repository scenario, RFC without explicit source,
  `requires_adr=true` and `requires_standard=true`.

Explicit constraints:

- Do not modify existing RFC files.
- Do not modify `governance/rfc-process.md`.
- Do not add transition rules from RFC to ADR or RFC to standard beyond the
  impact fields.
