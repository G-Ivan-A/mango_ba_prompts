---
status: draft
version: 0.1
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
3. [ ] Preserve source provenance and hashes; obtain only the explicitly attached
   PDF and historical text from GitHub. Do not download Mango-hosted attachments,
   images, PDFs, archives, binaries, support/ticket or obsolete-version pages.
4. [ ] Reproduce extraction boundaries with small offline tests before implementation.
5. [ ] Crawl every reachable in-scope HTML page of the alternative documentation;
   record HTTP/redirect/error evidence, hierarchy, extraction and cross-references.
6. [ ] Verify JavaScript and CORS behavior in a real browser; distinguish observed
   accessibility from inferred LLM comprehension and update frequency.
7. [ ] Extract every page and section of the attached Contact Center PDF locally;
   compare against the pinned issue 399 map and the new map with traceable metrics.
8. [ ] Enumerate differences and denominators; distinguish structural, textual,
   version-related and unverifiable evidence. Apply the issue's 5% decision rule.
9. [ ] Publish JSON/JSONL and Markdown artifacts, extraction-tool assessment,
   combined-source principles and an explicit acceptance/evidence matrix.
10. [ ] Run focused tests and make validate-fast; run make validate-full before
    commits/pushes. Commit useful atomic steps; keep history forward-moving.
11. [ ] Fetch and merge upstream main; review full PR diff and absolute links,
    check prior features remain and generated outputs reproduce.
12. [ ] Push only issue-401-be292b53210f; update existing PR title/body, retain
    Fixes G-Ivan-A/mango_ba_prompts#401, include reproduction and verification.
13. [ ] List upstream/fork CI runs with timestamps and head SHA; download failures
    into ignored ci-logs, diagnose actual log lines, fix and verify fresh runs.
14. [ ] Mark PR 402 ready; verify clean working tree, final requirements matrix
    and review state. Never present blocked acceptance criteria as complete.

Interpretation: the ban on downloading files from websites governs the audited
Mango sites. The GitHub PDF explicitly supplied as the required reference input
is processed locally, remains ignored and is never committed. Historical chat
is context only, never a source of product facts or a published transcript.
