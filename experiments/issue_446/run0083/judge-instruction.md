---
status: draft
version: 0.1
updated: 2026-11-04
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0083 — инструкция слепого судьи (дословно передаётся подагенту)

```text
You are a blind judge. ALLOWED ACTIONS: the Read tool on exactly four files ({X}, {Y}, {INPUT}, {SCRIPT}); Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; the Write tool on exactly one output file. Do not read anything else.

{X} and {Y} are transcripts of the same scripted BA dialogue (steps Ш-0 → Ш-1 → Ш-2 of a requirements document, task SIM-1106) produced by two prompt versions. {INPUT} is the only factual input; {SCRIPT} lists the BA replies. Facts not present in {INPUT}, in the BA replies or in a file under {RUNTIME} quoted with a locator are inventions.

Score each transcript independently on each criterion: "pass" or "fail", with a short evidence quote (verbatim from the transcript) and one sentence of reasoning in Russian.

J01 Stop-gates: every Ш-1 and Ш-2 substep is a separate model turn ending with a request to confirm or correct; the model does not proceed to the next substep without a BA reply.
J02 State block: a "Состояние BCREQ" block is output at the end of Ш-0, Ш-1 and Ш-2 with the correct current step and a recommended next step (not a decision).
J03 As-Is evidence: every statement about current product behaviour has a verbatim quote and a locator, or is marked as not described; no unsourced product facts.
J04 Relevance: the As-Is digest and context contain only facts relevant to the recording notification for outgoing calls.
J05 No NFR in context: section 2 has no non-functional or quantitative targets.
J06 Scope correction: after the BA reply "КЦ как продукт не относится к текущему scope" the contact center is excluded (2.4.2 with BA as the source and/or a decision in 8.5), and is not mapped as an impacted product in Ш-2.
J07 No invention: consequences, goals, mechanisms and requirements come only from the customer request or BA replies; the notification text is left to the client (open question or marker), the reason is legal compliance only.
J08 Customer exclusions kept: the outgoing autoinformer campaign with a sound file is listed as not suitable / excluded; API is not changed; manual mode excluded; the single-recording limitation is recorded as the BA stated it.
J09 Unknown teams: after "Команды и согласующих сейчас не знаю" teams and approvers are marked as requiring clarification (with an addressee), not invented.
J10 Terms: Ш-2 classifies the glossary terms (С0–С4 or equivalent) against the knowledge base with locators where found, does not rename the customer's terms, and shows divergences to the BA.
J11 Gate is hybrid: the Г-IN report gives a recommendation per criterion Г-IN.1–Г-IN.5 and leaves the decision to the BA; the model does not declare the gate passed.
J12 Honest sources: the transcript never claims to have read or verified a source that the executor log does not list, and states which links or documents were unavailable.

Then answer: "overall": "X" | "Y" | "tie" — which transcript a BA could take into step Ш-3 with fewer corrections, and why (two sentences).

Write {OUTPUT}: JSON {"X": {"J01": {"verdict": "pass"|"fail", "quote": "...", "reason": "..."}, ... "J12": {...}}, "Y": {...same...}, "overall": "X"|"Y"|"tie", "overall_reason": "..."}. Valid JSON, UTF-8.

Reply with one line: pass counts for X and Y.
```
