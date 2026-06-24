---
status: final
version: 0.1
updated: 2026-06-24
ai-generated: true
type: run-input
scope: rfc-generation-contract
---

# Research sources for RFC generation contract

## Local repository corpus

The contract was checked against 11 existing RFC-like documents:

1. `governance/rfc/bcreq-ft-scope-formation-rules-proposal.md`
2. `governance/rfc/prompt-improvement-bcreq-1025-proposal.md`
3. `governance/rfc/prompt-improvement-multichannel-proposal.md`
4. `governance/rfc-to-hub-001-knowledge-transfer.md`
5. `governance/rfc-to-hub-002-prompt-debugging-process.md`
6. `docs/analysis/approval-contract-test-industry-rfc.md`
7. `docs/analysis/migration-strategy-rfc.md`
8. `docs/analysis/rfc-industry-taxonomy-improvement.md`
9. `docs/analysis/rfc-mango-taxonomy-improvement.md`
10. `docs/analysis/rfc-rules-registry-system.md`
11. `docs/analysis/rfc-taxonomy-extension-mechanism.md`

Supporting local sources:

- `governance/bcreq-fr-generation-contract.md`
- `standards/executable-contract-standard.md`
- `governance/rfc-process.md`
- `docs/analysis/executable-contracts-and-rfc-problems.md`
- `runs/CONTRACT.md`

## External practices

The contract uses the following external practices as research inputs:

- IETF RFC Style Guide, RFC 7322:
  <https://datatracker.ietf.org/doc/html/rfc7322>
- RFC Editor online style guide:
  <https://www.rfc-editor.org/authors/rfc-style-guide/>
- React RFC process:
  <https://github.com/reactjs/rfcs>
- Rust RFC process and template:
  <https://rust-lang.github.io/rfcs/0002-rfc-process.html>
  and <https://github.com/rust-lang/rfcs/blob/master/0000-template.md>
- GitLab architecture design documents:
  <https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/>
- Fuchsia RFC best practices:
  <https://fuchsia.dev/fuchsia-src/contribute/governance/rfcs/best_practices>
- Kubernetes KEP template:
  <https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md>

## Findings applied

- RFC/design-doc practices consistently require clear motivation, alternatives,
  rationale, impact and future-readability.
- The local RFC corpus has inconsistent frontmatter, status naming, source
  traceability and machine-readable problem/proposal structure.
- The executable-contract standard requires L1 contracts to remain pure YAML and
  keep source/provenance out of runtime contracts.
- The contract therefore defines a complete RFC output schema and validates
  problem/proposal traceability rather than relying on examples.

