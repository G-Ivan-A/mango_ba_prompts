# Issue #208 — BCREQ-1027 L3 boundary dry run

Date: 2026-06-23
Contract: `governance/bcreq-fr-generation-contract.md` v0.3
Case: BCREQ-1027 section 4.3 API artifact

## Runtime inputs checked

- `runs/bcreq-1027/metadata.yaml`
- `runs/bcreq-1027/artifacts/section-4-3-api.md`
- `kb/industry-taxonomy/registry.json`
- `kb/mango-taxonomy/registry.json`
- Local scope rules `BCREQ-FR-GEN-SCOPE-01/02` from §3 of the contract

Папки L3 `governance/rfc/` и `standards/` не загружались как runtime-входы
для этого dry run.

## Expert pass 1: Architect

Result: pass.

The contract frontmatter now integrates only L2 taxonomy registries. §2 does not
list RFC or taxonomy standards as mandatory runtime inputs. The RFC-184 source
labels remain only inside the machine-readable scope rules as provenance labels.

## Expert pass 2: BA expert

Result: pass.

The business meaning of the two scope rules is preserved in
`BCREQ-FR-GEN-SCOPE-01/02`: BCREQ-FR describes the requested change, not current
functionality; a single-user request does not justify changing functionality
already closed explicitly or alternatively.

## Expert pass 3: AI engineer

Result: pass.

The runtime input list is machine-checkable by
`scripts/validate_issue_208_bcreq_fr_l3_boundary.py`. The BCREQ-1027 dry run can
use the run metadata, the section artifact, L2 registries, and embedded scope
rules without reading `governance/rfc/` or `standards/`.
