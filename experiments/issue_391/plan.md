# Issue 391 work plan

Objective: implement and verify every requirement in https://github.com/G-Ivan-A/mango_ba_prompts/issues/391 in https://github.com/G-Ivan-A/mango_ba_prompts/pull/392.

1. [x] Read complete issue and all PR comment/review types; inspect repository guidance and deployment permissions.
2. [x] Reproduce catalog/auth/process defects with focused automated checks and browser screenshots.
3. [x] Stage 1: publish only dynamically discovered BCREQ prompts; retain repository tools and archives untouched.
4. [x] Stage 2: review all five runs, all Golden Set artifacts, all fourteen prompts and existing defenses; record per-prompt added/already-covered lessons and candidate cases. Add only missing nonconflicting protections.
5. [x] Stage 3: retain exactly two process blocks with prompt copy; implement separate login, exact hash-only password via setter, failure and canonical redirect. Document operation off site.
6. [x] Run generation, focused checks, all local validators; save large logs and inspect failures. Add regression coverage through existing discovery.
7. [x] Capture before/after browser screenshots, close browser, document requirements/evidence and limitations. Never save password plaintext.
8. [ ] Update CHANGELOG and PR title/body with lesson inventory, tests, screenshots, deployment status and positive issue closing reference.
9. [ ] Fetch/merge upstream main, review complete PR diff, commit atomic useful changes, push only prepared source branch.
10. [ ] Manually deploy site contents plus .nojekyll to upstream gh-pages if permitted; do not change or enable Actions. Verify deployed canonical URL. Record exact blocked criteria if permissions prevent deployment.
11. [ ] Check latest upstream/fork CI timestamps and SHA; preserve/analyze nonpassing logs if any. Confirm clean tree and ready PR. Move issue to review if permissions permit; leave unmerged.

Known external constraint: upstream repository API reports push=false, triage=false, admin=false. Deployment to its gh-pages and issue status may require maintainer credentials. Continue all independent work.

Resource controls: no agent delegation; sequential browser/tests, finite inputs; no memory stress tests; log large outputs to ci-logs; read files above 1500 lines in chunks.

Publication evidence: authenticated dry-run push to upstream gh-pages returns HTTP 403, permission denied to konard. Review label API returns HTTP 403 (admin rights required). Canonical browser inspection: 30 old cards, no login, login.html=404. Deployment and issue review remain unfinished.
