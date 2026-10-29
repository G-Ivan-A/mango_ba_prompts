---
status: review
version: 1.0
updated: 2026-10-29
temperature: 0.1
---

# Issue 401 — execution checklist

Objective: implement and verify every acceptance criterion in
https://github.com/G-Ivan-A/mango_ba_prompts/issues/401 in
https://github.com/G-Ivan-A/mango_ba_prompts/pull/402.

1. [x] Verify prepared branch, read issue and all comments, PR conversation,
   inline comments and reviews; inventory sub-issues (none returned).
2. [x] Read contributing/governance rules, prior issue 399 artifacts and merged PR.
3. [x] Preserve source provenance and hashes; obtain only the explicitly attached
   PDF and historical text from GitHub. Do not download Mango-hosted attachments,
   images, PDFs, archives, binaries, support/ticket or obsolete-version pages.
4. [x] Reproduce extraction boundaries with small offline tests before implementation.
5. [x] Crawl every reachable in-scope HTML page of the alternative documentation;
   record HTTP/redirect/error evidence, hierarchy, extraction and cross-references.
6. [x] Verify JavaScript and CORS behavior in a real browser; distinguish observed
   accessibility from inferred LLM comprehension and update frequency.
7. [x] Extract every page and section of the attached Contact Center PDF locally;
   compare against the pinned issue 399 map and the new map with traceable metrics.
8. [x] Enumerate differences and denominators; distinguish structural, textual,
   version-related and unverifiable evidence. Apply the issue's 5% decision rule.
9. [x] Publish JSON/JSONL and Markdown artifacts, extraction-tool assessment,
   combined-source principles and an explicit acceptance/evidence matrix.
10. [x] Run focused tests and make validate-fast; run make validate-full before
    commits/pushes. Commit useful atomic steps; keep history forward-moving.
11. [x] Fetch and merge upstream main; review full PR diff and absolute links,
    check prior features remain and generated outputs reproduce.
12. [x] Push only issue-401-be292b53210f; update existing PR title/body, retain
    Fixes G-Ivan-A/mango_ba_prompts#401, include reproduction and verification.
13. [x] List upstream/fork CI runs with timestamps and head SHA; download failures
    into ignored ci-logs, diagnose actual log lines, fix and verify fresh runs.
14. [x] Mark PR 402 ready; verify clean working tree, final requirements matrix
    and review state. Never present blocked acceptance criteria as complete.

Interpretation: the ban on downloading files from websites governs the audited
Mango sites. The GitHub PDF explicitly supplied as the required reference input
is processed locally, remains ignored and is never committed. Historical chat
is context only, never a source of product facts or a published transcript.

Evidence: 3533/3533 alternative pages return HTTP 200; all 590 PDF pages,
168 TOC IDs and 194 numbered sections are accounted for. Both source comparisons
exceed 5% (25.310734% / 25.087658% lexical difference); image-only semantics
and role-matrix equivalence remain explicitly unverified findings of the audit.
All seven derived comparison/provenance artifacts reproduce byte-for-byte from
recorded inputs. Sixteen offline tests check extraction and published evidence.

Local fast/full validation passes all 69 validators. The complete PR diff was
downloaded and reviewed; code/protocol changes were read separately from the
generated JSON/JSONL ledger, whose hashes, scope and operation balances are
checked by regressions. No existing product features or prompt text were removed.
Upstream main is included. Governance and Pages workflow runs passed on the
review commit; both workflows are rerun against the final head before handoff.
Final run links and exact head SHA are recorded in the PR description.

Report and full acceptance matrix:
https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-401-be292b53210f/docs/taxonomy/documentation-audit.md
