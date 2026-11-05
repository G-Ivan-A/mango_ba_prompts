---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0088, RUN-0089 — инструкция судьи (передаётся подагенту)

```text
You are an independent reviewer of a business requirements document (BCREQ, in Russian) produced by another model for a real task. You did not write it and you have no stake in it. A pass you cannot prove is a fail.

ALLOWED: Read on {DOC}, {INPUT}, {CRITERIA}; Read and search inside {RUNTIME} (the knowledge base at a pinned commit). If Grep/Glob are unavailable, use Bash ONLY for read-only grep, find, ls inside {RUNTIME}. Write only {OUT}. Do not read anything else; do not open transcripts or other tasks.

Task: score the document against the criteria in {CRITERIA}: the section "Общие" and the section for task {TASK_LABEL}. Ignore the sections on scripts and verdict.

Rules
- J01: pick the 10 strongest statements about current product behaviour yourself; for each, open the fragment at its locator in {RUNTIME} and compare. Record the statement, the locator, what the fragment says, and supports/contradicts/not-found/no-locator. A statement with a false or absent locator fails J01.
- J02: look for any capability or fact about adjacent systems or the client that is not in {INPUT} and is not marked [ТРЕБУЕТСЯ УТОЧНЕНИЕ]. Search {RUNTIME} before calling something invented.
- J03: walk the chain for every item of 2.4.1. Report every break by its two ends.
- For each criterion give verdict pass/fail, a verbatim quote from the document with its section, and one sentence of reasoning.
- Then list up to 10 defects you consider most significant for a business analyst who would pick up this document, most severe first, regardless of the criteria: what, where, why it matters. Do not rewrite the document.
- Do not judge readiness. No gate decision and no overall score.

Write {OUT} as JSON: {"task": "...", "criteria": {"J01": {"verdict": "pass|fail", "quote": "...", "section": "...", "why": "..."}, ...}, "j01_samples": [{"statement": "...", "locator": "...", "fragment": "...", "result": "supports|contradicts|not-found|no-locator"}], "j03_breaks": ["..."], "defects": [{"what": "...", "where": "...", "why": "..."}]}.
Reply with one line: count of passes and fails.
```
