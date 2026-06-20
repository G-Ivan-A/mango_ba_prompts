---
status: draft
version: 0.1
updated: 2026-06-20
ai-generated: true
type: audit
scope: mango-taxonomy
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/146"
related_artifacts:
  - "standards/decisions/ADR-011-industry-taxonomy.md"
  - "standards/decisions/ADR-012-mango-taxonomy.md"
  - "standards/product-classification-contract.md"
  - "kb/mango-product-docs/processed/"
---

# Issue #146: Mango Taxonomy validation on processed product docs

## Scope

Issue #146 asked to validate Mango Taxonomy on real processed Mango
documentation, choose the hierarchy depth, and unify terminology with Industry
Taxonomy. This audit uses only processed markdown under
`kb/mango-product-docs/processed/`; source PDFs and new KB data were not created.

Decision summary:

- Industry Taxonomy: `Domain -> Capability -> Feature -> Function`.
- Mango Taxonomy: `Product -> Service -> Module -> Function`.
- `Function` replaces the previous `Atomic Function` term in active taxonomy
  documents.
- Commercial packages, tariffs, procurement fields, industry segments and
  regional labels stay outside the hierarchy as facets.

## Sources

The validation covered 12 processed guides across the requested product spread:

| Processed guide | Product/family signal | Structural signal |
| --- | --- | --- |
| `mango-cc-manual` | Contact Center | Product manual splits into operator workspace, queue, campaign, WFM, report and settings modules; sections contain concrete user actions and settings. |
| `mango-lk-manual` | VATS / LK | Product manual exposes services such as numbers, routing, employees, groups, integrations, reports and access; modules contain settings and operations. |
| `mtalker/quick-start` | Mango Talker | Quick-start guide gives function-level user actions: call, send SMS, chat, send file. |
| `mtalker/windows-mac-working` | Mango Talker desktop | Working guide decomposes Talker into navigation, calls, statuses, chats, channels, contacts, video and settings. |
| `mtalker/windows-mac-admin` | Mango Talker admin | Admin guide shows setup functions for employees, call schemes, schedules, outgoing numbers and command-line calls. |
| `integration-bitrix24` | CRM integration | Integration guide separates setup services, CRM mapping modules, telephony actions, webhooks, analytics and message functions. |
| `sip-trunk` | SIP Trunk | Guide is structurally present as a telecom module under VATS/resource layer; text extraction is partially mojibake, so it was not used as term-count evidence. |
| `vpbx-api` | Open API / CPaaS | API guide has service/API groups, endpoint-like sections, request/response operations and function-level commands. |
| `mdialogi-api` | Dialogi API / digital channels | API guide separates Dialogi entities, channels, authorization, request types and concrete API operations. |
| `speech-analytics/rukovodstvo-polzovatelya-rechevaya-analitika` | Speech analytics / AI | Guide separates analytics service, modules for recognition, AI summaries, tagging, assistants, reports and settings. |
| `quality-managment` | Quality management | Guide explicitly uses module language and decomposes quality control into roles, scorecards, appeals, reports and review actions. |
| `wallboard` | Wallboard / real-time analytics | Guide explicitly treats Wallboard as a module and contains widget, template and indicator settings. |

## Term Evidence

The selected corpus contains enough repeated terminology to distinguish levels.
The count is intentionally simple: case-insensitive substring matching across
each selected guide's `index.md` and `sections/*.md`.

| Signal | Count | Interpretation |
| --- | ---: | --- |
| service=235 | 235 | `Service` is a useful middle layer, especially for API, integration, speech analytics and cross-product capabilities. |
| module=245 | 245 | `Module` is a strong document-level term: quality control, Wallboard, LK modules, CC modules and API groups. |
| function=371 | 371 | `Function` is a stronger and more common leaf-level term than `operation`; docs use it for concrete capabilities. |
| operation=71 | 71 | `Operation` appears, but mostly as API/user-action wording rather than a taxonomy level name. |
| settings/actions | 3329 | Settings and actions dominate the leaf-level evidence and should be captured as Function instances. |

The high settings/actions count matters because many processed sections are not
named "function" directly, but describe concrete testable behavior: configure a
webhook URL, select a widget, change an agent status, set a route, send a dialog
message, get a blacklist mode or create an outbound campaign.

## Structure Finding

The processed docs do not show one flat product list and do not stop at
`Product -> Service -> Module`. They repeatedly expose a fourth practical level:

```text
Product -> Service -> Module -> Function
```

Observed mapping:

| Mango level | Evidence pattern | Example |
| --- | --- | --- |
| Product | Public/manual boundary or product family | `mango-contact-center`, `mango-virtual-pbx`, `mango-talker`, `mango-speech-analytics` |
| Service | Functional area that can support several products | `voice-routing`, `open-api`, `crm-integrations`, `speech-analytics`, `access-control` |
| Module | Screen, API group, report, widget, integration block or operational component | `wallboard`, `quality-scorecard`, `webhooks`, `telegram-channel`, `sip-trunk` |
| Function | Concrete operation, setting, endpoint, parameter or rule | `transfer-call`, `set-agent-status`, `configure-webhook-url`, `send-dialog-message`, `select-wallboard-widget` |

`Component` is not a dominant term in the processed corpus. It appears
sporadically and is better treated as an alias or source-specific term for
module/component evidence, not as a separate canonical Mango Taxonomy level.

## Decision

ADR-011 should use `Function` as the Industry leaf level:

```text
Domain -> Capability -> Feature -> Function
```

ADR-012 should keep the two-layer Official/Internal model, but update the
internal hierarchy to four levels:

```text
Product -> Service -> Module -> Function
```

Alignment rule:

| Mango Taxonomy | Industry Taxonomy |
| --- | --- |
| Product | Domain/Capability bundle, often many-to-many |
| Service | Capability |
| Module | Feature |
| Function | Function |

This keeps symmetry without pretending that public Mango product names match
industry domains one-to-one.

## Constraints Kept

- No catalog structure was changed.
- No KB data was created or regenerated.
- Existing ADRs were updated rather than deleted.
- The validation is backed by processed docs in the repository.
- The regression check is `scripts/validate_issue_146_mango_taxonomy.py`.
