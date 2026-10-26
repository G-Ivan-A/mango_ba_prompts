# Issue 393 work plan

Objective: implement and verify every requirement in
https://github.com/G-Ivan-A/mango_ba_prompts/issues/393 in
https://github.com/G-Ivan-A/mango_ba_prompts/pull/394.

- [x] Read the complete issue, sub-issue list, issue comments and all three PR
  feedback endpoints (all empty); inspect recent related PRs 390 and 392.
- [x] Read contributing/governance rules, taxonomy, stage contract and generator.
- [x] Confirm the prepared branch and clean starting tree; fetch upstream main
  and confirm it is already an ancestor. No Actions runs exist for this branch.
- [x] Trace the defect: missing frontmatter tags, README-based mapping, static
  counters and one-direction cascade; report navigation is independent of login.
- [x] Add regression tests and capture a failing run and browser baseline.
- [x] Add stage and operation frontmatter tags to all 14 prompts; preserve every
  prompt body and all 13 taxonomy operations. UC belongs to both core/work stages.
- [x] Generate exactly six process facets from prompt metadata and stage labels.
- [x] Implement reciprocal availability and counts from current query and other
  filters, retaining OR within a facet and AND across facets. Keep the four groups,
  BCREQ set filter and modes. Selected zero-count options remain removable.
- [x] Remove only Roadmap/Patterns/Reports menu links; preserve report routes,
  gate, logout, theme and existing direct hash routes.
- [x] Run focused tests, generator and full local validation; preserve logs in
  ci-logs and investigate actual errors before changing anything else.
- [x] Verify Chromium desktop/mobile, both cascade directions, counts, multi-select,
  search/reset, clipboard, two process blocks, report deep-link gate, logout/theme.
  Save before/after screenshots; close browser and wait for all commands.
  Both standalone Chromium and Playwright MCP on localhost passed.
- [ ] Update CHANGELOG and PR with operation audit, reproduction/test evidence,
  screenshots, assumptions and the owner's manual gh-pages deployment checklist.
- [ ] Commit useful atomic changes after local checks; push only the prepared
  issue branch, preserve history, inspect gh pr diff and confirm clean worktree.
- [ ] Recheck upstream main, latest issue/PR feedback and CI timestamps/SHA.
  Download any failed run logs to ci-logs and resolve failures if present.
  Do not enable Actions, edit workflow files, dispatch workflows or push gh-pages.
- [ ] Hand off for review using the ready PR. The issue has no project status
  field or review label; no issue-level status change will be claimed. Do not merge.

Implementation choices: `processes` is a JSON-compatible YAML inline array;
`operation` is the existing primary cognitive operation, moved to frontmatter as
the source of truth. All 14 existing primary operation assignments were audited
against each prompt and the stage contract and retained; missing tags were added.
Facet counts ignore their own selected values and honor every other filter, so
users can add alternatives within the same OR group.

Verification evidence: `ci-logs/issue-393-before-tests.log` and
`ci-logs/issue-393-before-browser.log` reproduce the defect;
`ci-logs/issue-393-validate-full-final.log` reports 64 validators, zero failures;
`ci-logs/issue-393-browser.log` records the complete Chromium pass. Logs are
ignored; screenshots, baseline hashes and reproducible scripts are committed.
