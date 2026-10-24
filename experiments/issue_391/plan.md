# Issue 391 work plan

Objective: implement and verify every requirement in https://github.com/G-Ivan-A/mango_ba_prompts/issues/391 in https://github.com/G-Ivan-A/mango_ba_prompts/pull/392.

1. [x] Read complete issue and all PR comment/review types; inspect repository guidance and deployment permissions.
2. [x] Reproduce catalog/auth/process defects with focused automated checks and browser screenshots.
3. [x] Stage 1: publish only dynamically discovered BCREQ prompts; retain repository tools and archives untouched.
4. [x] Stage 2: review all five runs, all Golden Set artifacts, all fourteen prompts and existing defenses; record per-prompt added/already-covered lessons and candidate cases. Add only missing nonconflicting protections.
5. [x] Stage 3: retain exactly two process blocks with prompt copy; implement separate login, exact hash-only password via setter, failure and canonical redirect. Document operation off site.
6. [x] Run generation, focused checks, all local validators; save large logs and inspect failures. Add regression coverage through existing discovery.
7. [x] Capture before/after browser screenshots, close browser, document requirements/evidence and limitations. Never save password plaintext.
8. [x] Update CHANGELOG and PR title/body with lesson inventory, tests, screenshots, deployment status and positive issue closing reference.
9. [x] Fetch/merge upstream main, review PR source diff and generated-data contracts, commit useful changes, push only prepared source branch.
10. [ ] BLOCKED: manually deploy site contents plus .nojekyll to upstream gh-pages; verify deployed canonical URL. Authenticated push permission check returns HTTP 403. Do not change or enable Actions.
11. [x] Check latest upstream/fork CI timestamps and SHA; preserve/analyze nonpassing logs if any. Source commit 29390d5e has no Actions runs or PR checks. PR is ready, unmerged; working tree checked before final evidence commit.
12. [ ] BLOCKED: move issue to review. API returns HTTP 403; no accessible project status exists.

Known external constraint: upstream repository API reports push=false, triage=false, admin=false. Deployment to its gh-pages and issue status may require maintainer credentials. Continue all independent work.

Resource controls: no agent delegation; sequential browser/tests, finite inputs; no memory stress tests; log large outputs to ci-logs; read files above 1500 lines in chunks.

Publication evidence: authenticated dry-run push to upstream gh-pages returns HTTP 403, permission denied to konard. Review label API returns HTTP 403 (admin rights required). Canonical browser inspection: 30 old cards, no login, login.html=404. Deployment and issue review remain unfinished.

Verification: generation completed; make validate-full passed all 63 validators (0 cached, 26.58s); make validate-fast passed all 63 (60 cached, 12.60s). Chromium with the configured credential passed separate login, exact case/spacing, failure/retry, canonical redirect, dynamic BCREQ catalog, all 11 clipboard results, exactly two process blocks, other routes, theme, mobile labels, logout, report deep link and session invalidation. Playwright MCP independently checked local UI and live publication. All browser sessions were closed. Issue and PR conversation/inline/review endpoints were rechecked and remain empty.

The native goal remains unfinished because items 10 and 12 require an external permission change; passing local checks and making the PR ready do not satisfy them.
