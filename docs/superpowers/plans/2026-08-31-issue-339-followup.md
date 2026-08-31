# Issue 339 Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve current issue 339 and PR 342 feedback, prove the fix with regression coverage, and finalize the existing pull request.

**Architecture:** First reconstruct the requested behavior and current branch state from GitHub and repository evidence. Then validate each review item against the implementation, use a red-green regression cycle for behavioral changes, and run the repository's complete local and remote checks before updating PR 342.

**Tech Stack:** Repository-defined tooling, Git, GitHub CLI, GitHub Actions

**Spec:** GitHub issue 339 and all issue/PR 342 comments and reviews

## Global Constraints

- Work only on `issue-339-260fd9375acf`.
- Preserve unrelated user changes.
- Update existing PR 342; do not create another PR.
- Push only to `issue-339-260fd9375acf`.
- Use test-first development for every behavioral fix.

---

### Task 1: Establish Current Requirements and State

**Files:**
- Inspect: repository guidance and contribution files
- Inspect: issue 339, PR 342, all comment/review endpoints, recent commits, and branch diff
- Modify: none

**Interfaces:**
- Consumes: GitHub issue/PR data and local repository state
- Produces: verified list of unresolved requirements and failures

- [x] Confirm the checked-out branch and clean/dirty status.
- [x] Read issue 339 and every issue comment.
- [x] Read PR 342 metadata, conversation comments, inline review comments, and reviews.
- [x] Inspect recent related merged PRs and current diff for repository conventions.
- [x] List recent CI runs with timestamps and head SHAs; no runs existed before implementation.

### Task 2: Resolve Verified Feedback with Regression Coverage

**Files:**
- Modify: exact source and test paths identified in Task 1
- Test: repository-native test files identified in Task 1

**Interfaces:**
- Consumes: unresolved items and root causes from Task 1
- Produces: minimal implementation satisfying issue 339 and accepted review feedback

- [x] Write `scripts/validate_issue_339_run.py` against the three source workbooks.
- [x] Confirm RED: validator failed because the RUN-0062 report was absent.
- [x] Implement `experiments/issue_339/generate_run.py` and RUN-0062 artifacts.
- [x] Confirm exact XLS row values, six-column widths, checksums and direct links.
- [ ] Commit each independently useful correction with a clear conventional message.

### Task 3: Verify and Finalize PR 342

**Files:**
- Modify: PR 342 title/description and review threads as needed
- Inspect: complete branch diff and CI logs

**Interfaces:**
- Consumes: completed implementation and tests from Task 2
- Produces: pushed branch and review-ready PR 342

- [ ] Run all contributing-guide checks and the full local test suite, preserving large logs in files.
- [ ] Re-read the complete diff for regressions, unintended removals, and issue coverage.
- [ ] Merge the latest default branch into the feature branch if needed, resolve safely, and rerun checks.
- [ ] Commit the plan and any remaining scoped changes; confirm the working tree is clean.
- [ ] Push only `issue-339-260fd9375acf` and update PR 342 title/description with reproduction and test evidence.
- [ ] Reply to resolved inline threads using their thread endpoints and mark PR 342 ready.
- [ ] Verify fresh GitHub Actions runs correspond to the latest head SHA; download/analyze any non-passing logs before completion.
