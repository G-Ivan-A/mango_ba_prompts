# Issue 395 execution checklist

Objective: fully implement both tasks in
https://github.com/G-Ivan-A/mango_ba_prompts/issues/395 in
https://github.com/G-Ivan-A/mango_ba_prompts/pull/396, without merging or deploying.

- [x] Read issue and all issue/PR conversation, inline comments and reviews (empty).
- [x] Confirm prepared branch; read contributing/governance, recent related work,
  all 14 prompts, eight section standards, constitution and gate contract.
- [x] Inspect runtime README, USAGE, MAP and taxonomy against the reference catalog.
  Routing is usable; full product classification is absent (three routing classes).
- [x] Download dialogue, extract relevant lines before reading; download and extract
  approval PDF referenced by the existing process documentation.
- [x] Add failing tests and a browser baseline; preserve logs under ci-logs/.
- [x] Task 1: add identical bounded blocks to 14 prompts, preserving original bytes.
  Cover fallback, constitution availability, source circuit breakers, taxonomy
  completeness, selective retrieval, BA escalation, manual files/text and no-KB default.
- [x] Verify Task 1 before Task 2; preserve both historical byte-comparison tests.
- [x] Task 2: gated standards route/menu, eight section checklists, ten mandatory
  concepts with verified industrial sources, stage inputs/outputs and source caveats.
  Keep existing sections, styles, gate, standards and non-BCREQ prompts unchanged.
- [x] Add focused regression checks to automatic discovery; browser desktop/mobile,
  dark theme, keyboard navigation, deep link, logout, catalog/process/report smoke checks.
  Commit before/after screenshots under site/ and close browser after testing.
- [x] Record manual prompt scenario walkthroughs and trace every acceptance criterion.
- [x] Generate site data, run make validate-fast/full, inspect all failures, then
  commit atomic steps; remove only the generated root PR placeholder.
- [x] Fetch/merge upstream main, inspect gh pr diff, check no accidental removals.
- [x] Update CHANGELOG and PR title/body, reproduction, tests, screenshots, deviations,
  source findings and positive closing reference. Push only the prepared branch.
- [x] Check latest feedback, CI timestamps and head SHA on upstream and fork;
  download/analyze non-passing logs if present; do not enable/dispatch Actions or deploy.
- [x] Mark PR ready for review; verify clean worktree and no background work remains.

Scope interpretation: the two task-specific restrictions apply sequentially:
Task 1 changes only BCREQ prompt additions; Task 2 changes only site implementation.
CHANGELOG is explicitly required. Minimal regression scripts and preservation-test
updates are necessary to satisfy the requested automated/byte-level verification;
this narrow scope adjustment is documented in the PR. No standards or existing
site sections, password configuration, deployment workflows or external repos change.

Final handoff: both implementation commits are pushed; PR 396 is ready for review.
Upstream main is already included. Latest issue/PR conversations, inline comments
and reviews are empty. Upstream/fork branch run lists and PR status checks are
empty, so no remote CI success is claimed. All 66 local validators and the final
Chromium scenario pass; all browser sessions are closed.
