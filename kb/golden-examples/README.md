# Golden Examples

`kb/golden-examples/` stores approved, repository-versioned examples that
generation contracts may use as format and style references. The lifecycle,
metadata, linking, and approval rules are defined in
[`kb/golden-examples/CONTRACT.md`](CONTRACT.md).

No real golden artifacts are created by issue #211. Until a future task adds an
approved example, contracts use the machine-readable placeholder
`status: "no-golden-standard"`.

## Structure

| Path | Purpose |
| --- | --- |
| `bcreq-fr/` | Approved BCREQ-FR golden examples. |
| `rfc/` | Approved RFC golden examples. |
| `adr/` | Approved ADR golden examples. |

Empty artifact-type directories are kept with `.gitkeep` so later tasks can add
approved examples without changing the storage contract.
