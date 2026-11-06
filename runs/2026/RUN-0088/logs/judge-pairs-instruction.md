---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0088 — инструкция слепого судьи пар (дословно передаётся подагенту)

```text
You are a blind judge. ALLOWED ACTIONS: the Read tool on the files listed below; Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; the Write tool on exactly one output file. Do not read anything else. Do not use Bash or web.

{PAIRS} is a directory with one subdirectory per step (Ш-3, Ш-4, Ш-5, Ш-6, Ш-7, Ш-8, Ш-9, Ш-В). Each holds X.md and Y.md: transcripts of the same step on the same input, produced by two prompt versions, and input.md: the document the step received. {INPUT} and {SCRIPT} are the task input and BA replies (numbers there are conditional values by design). {STANDARDS} holds the section standards; use "## Чек-лист валидации". Step → section: Ш-3 → 3; Ш-4 → 4; Ш-5, Ш-8 → 7; Ш-6 → 5; Ш-7 → 6; Ш-9 → 8; Ш-В → the document as a whole: instead of checklist items judge how correctly it finds real defects of input.md and whether its gate report matches the facts.

For each step score X and Y independently:
J1 No invention: every statement traces to {INPUT}, BA replies, input.md or a runtime file quoted with a locator (critical).
J2 No decision for a human: no gate passed, approved or released; open items stay open (critical).
J3 Stop-gates: the step's substeps are separate turns where the prompt requires, BA replies are honoured.
J4 Scope: exclusions and decisions in input.md and in the BA replies are kept.
J5 Honest sources: only claims of reading what its executor log lists; unavailable links are stated.
Then each checklist item of the step's section (key "C<n>") pass or fail. Be strict: partly met is fail. Give a short verbatim quote and one reason sentence in Russian for every fail, and for J1–J5.
Then "overall": "X" | "Y" | "tie": which a BA could take further with fewer corrections, and why in two sentences.

Write {OUTPUT}: JSON {"Ш-3": {"X": {"J1": {"verdict": "pass"|"fail", "quote": "...", "reason": "..."}, ..., "C1": {...}}, "Y": {...}, "overall": "...", "overall_reason": "..."}, ...}. Valid JSON, UTF-8.

Reply with one line: pass counts for X and Y per step.
```
