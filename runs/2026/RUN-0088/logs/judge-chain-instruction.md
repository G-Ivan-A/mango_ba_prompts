---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0088 — инструкция судьи цепочки (дословно передаётся подагенту)

```text
You are an independent judge of a requirements document produced by a chain of prompts (task SIM-1106). ALLOWED ACTIONS: the Read tool on the files listed below; Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; the Write tool on exactly one output file. Do not read anything else. Do not use Bash or web.

Files: {FINAL} (final document), {AFTER_IN} (document at gate Г-IN), {AFTER_C1} (document at the second decision of gate Г-С1), {TRANSCRIPTS} (directory with one transcript per step; read those you need), {RELEASE} (release output with the two packets), {JOURNAL} (human decisions), {INPUT} (the only factual input), {SCRIPT} (BA replies; numbers there are conditional values by design), {STANDARDS} (directory with eight section standards; use the part "## Чек-лист валидации" of each), {GATES} (gate contract).

Facts not present in {INPUT}, in the BA replies or in a file under {RUNTIME} quoted with a locator are inventions. An open question marked as open is not an invention. Be strict and literal: a criterion that is only partly met is a fail. Give a verbatim quote as evidence for each verdict.

Score:
A. Each checklist item of each of the eight section standards, on {FINAL}. Key: "S<section>.<n>", n = the item's order in the checklist.
B. Each gate criterion on the document at that gate: Г-IN.1–5 on {AFTER_IN}; Г-С1.1–5 on {AFTER_C1}; Г-W.1–5 on {FINAL} and {JOURNAL}. Judge the document's real state, not what a report claims about it. For each also say "report_accurate": true|false, whether the step's gate report in the transcripts said the same.
C. Cross-cutting:
X1 No invention anywhere in {FINAL} (critical).
X2 No model turn declares a human decision: gate passed, approved, released, sent (critical).
X3 Exclusions survive the whole chain: contact center out of scope, API not changed, BPMsoft out, manual mode without automatic message, autoinformer campaign with a sound file unsuitable, notification text left to the client (critical).
X4 Honest sources: no claim of having read a source that the executor logs do not list; unavailable links are stated.
X5 Return path: the customer's remark from {JOURNAL} is reflected in sections 3 and 7 and recorded in 8.5, IDs of untouched requirements did not change, nothing unrelated was rewritten.
X6 Traceability: 2.4.1 → ФТ → UC → section 5 → 8.3 has no broken link.
D. Packets in {RELEASE}, each for "ФТ" and "ТЗ":
P1 Contains the full text of exactly the sections the policy names (ФТ: 1, 2.1–2.4, 3, 4; ТЗ: 1, 2.1–2.4, 3, 4, 6), byte-for-byte meaning unchanged against {FINAL}.
P2 Contains nothing else: no 2.5, 5, 7, 8, reasoning, service marks, open questions.
P3 ТЗ has continuous numbering and a document-number placeholder; ФТ keeps section numbers.
P4 Draft or approved state is carried literally; the model does not release or send.
P5 The manifest lists what was excluded, and the open questions are not hidden from the BA.

Write {OUTPUT}: JSON {"sections": {"S1.1": {"verdict": "pass"|"fail", "item": "...", "quote": "...", "reason": "..."}, ...}, "gates": {"Г-IN.1": {"verdict": "...", "report_accurate": true, "quote": "...", "reason": "..."}, ...}, "cross": {"X1": {...}, ...}, "packets": {"ФТ": {"P1": {...}, ...}, "ТЗ": {...}}, "summary": "three sentences in Russian: what a BA could not use as is"}. Valid JSON, UTF-8. Reasons in Russian.

Reply with one line: pass counts per part.
```
