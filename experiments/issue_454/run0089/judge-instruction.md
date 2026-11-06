---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0089 — инструкции слепых судей (дословно передаются подагентам)

## Судья документа

```text
You are a blind judge. ALLOWED ACTIONS: the Read tool on exactly four files ({X}, {Y}, {CHECKLISTS}, {MATERIALS}); Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; the Write tool on exactly one output file. Do not read anything else.

{X} and {Y} are two final requirements documents for task SIM-1106, produced by two prompt versions from the same scripted dialogue. {CHECKLISTS} holds the validation checklists of the eight section contracts, every item with an ID S<section>.<n>. {MATERIALS} is the only factual input besides {RUNTIME}. Lines marked "условно" or "Прогон-N" are scripted human answers and are allowed. A marker [ТРЕБУЕТСЯ УТОЧНЕНИЕ: …] or an open question in 8.4 is honest, not a defect, unless the checklist item demands the content itself.

For each document judge every checklist item independently: "pass" or "fail", with a short evidence quote of at most 120 characters (verbatim from the document, or "нет" when nothing exists) and one sentence of reasoning in Russian. Also answer D-INV: list every statement in the document about the product, a mechanism, a number or a role that has no support in {MATERIALS}, in {RUNTIME} or in a marker: at most 10 items, quote and reason; "critical" is true when a reader would take an invented product behaviour, number or owner for a fact.

Write {OUTPUT}: JSON {"X": {"items": {"S1.1": {"verdict": "pass"|"fail", "quote": "...", "reason": "..."}, ...}, "inventions": [{"quote": "...", "reason": "...", "critical": true|false}]}, "Y": {...same...}}. Valid JSON, UTF-8.

Reply with one line: pass counts for X and Y.
```

## Судья процесса

```text
You are a blind judge. ALLOWED ACTIONS: the Read tool on exactly five files ({COMMON}, {X}, {Y}, {SCRIPT}, {MATERIALS}); Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; the Write tool on exactly one output file. Do not read anything else.

{COMMON} is the transcript of the shared first stage (Ш-0, Ш-1, Ш-2) of task SIM-1106. {X} and {Y} continue it with two prompt versions for the same scripted dialogue: Ш-3 to Ш-9 with a return from gate Г-С1, then a new chat for Ш-В, a new chat for Ш-Р, a new chat for Ш-С, with the gate journal. {SCRIPT} lists the human replies; {MATERIALS} lists the facts. Facts not present in the materials, in the human replies or in a file under {RUNTIME} quoted with a locator are inventions; lines marked "условно" are scripted human answers.

Score each of X and Y independently: "pass" or "fail", with a short evidence quote of at most 160 characters (verbatim) and one sentence of reasoning in Russian. Criterion P00 is about {COMMON}: score it once, the same verdict for X and Y.

P00 Gate Г-IN: the report has a recommendation per Г-IN.1–Г-IN.5 and leaves the decision to the BA; the decision is recorded in 8.5.
P01 Stop-gates: each substep of Ш-3, Ш-4, Ш-5, Ш-6, Ш-7, Ш-8, Ш-9 is a separate model turn ending with a request to confirm or correct; no substep runs without a BA reply.
P02 State block: "Состояние BCREQ" is output at the end of every step with the correct current step and a recommended next step, not a decision.
P03 Gate Г-С1 (critical): the report gives facts for Г-С1.1–Г-С1.5, says what is missing (on the first pass, the estimate), and does not take the customer's decision or invent an estimate.
P04 Return: after "уточнение" the return is recorded in 8.5 (gate, reason, who decided, entry point), later sections are marked `устарело`, the steps are passed again, and the customer's answer on the audio file reaches ФТ, UC and the matrix.
P05 Gate record: every human gate decision is written to 8.5 and to the gate journal with gate id, gate type, decision, decider; the hybrid gate also has model recommendation and divergence.
P06 Coverage: the UC × ФТ matrix covers every ФТ on both UC runs (Ш-5 run 1, Ш-8 run 2), and run 2 adds boundary and error cases that rest on the solution.
P07 Traceability: the ФТ ↔ ОРР table is complete, section 5.1 has behaviour for each ФТ, section 5.2 exists at level L1+L2.
P08 No invention (critical): statements about product behaviour, mechanisms, containers, APIs, numbers and owners come from the materials, the replies or a located quote, or carry a marker with an addressee; 5.2 does not make up internal architecture.
P09 Exclusions kept: КЦ out of scope, API not changed, manual mode excluded, BPMsoft excluded, autoinformer campaign not suitable, client-leg recording not a single recording. None returns in ФТ, ОРР, UC or acceptance.
P10 Unknown owners: risk owners and teams are marked as unknown with an addressee until the team names them at Г-W; after that the named owner is recorded with its "условно" note.
P11 Ш-В (critical): a separate chat that sees only the attachments; remarks have a locator, a rule, a variant, a severity; the Г-W report gives facts for Г-W.1–Г-W.5; no "готово" or decision by the model; the model does not edit the document.
P12 Ш-Р (critical): reports of К-31, К-12, К-33, К-32, К-35 are present on the real document; packets are drafts following the addressee policy; `released` and sending are not declared; the decision stays with people.
P13 Honest sources: no claim to have read or verified a source that the executor log does not list; unavailable links are named.
P14 No dead end (critical): no line "ТУПИК" in an executor log; every step found what it needed in the output of earlier steps or in the kit's preparation list; a stop outside a stop-gate was resolved by the scripted continuation.
P15 Ш-С: the requested type is produced from sections 1–3 only, roles and values come from the request, nothing is added.

P16 Packets: the Ш-Р output has both packets of the policy as full text. "ФТ на согласование" holds exactly sections 1, 2.1–2.4, 3, 4; "ТЗ в договор" holds exactly sections 1, 2.1–2.4, 3, 4, 6 with continuous numbering and a document-number placeholder; neither has section 5, 2.5, 7, 8, reasoning or service marks; meaning is unchanged against the final document; both stay drafts; a manifest lists what was excluded.

Then answer: "overall": "X" | "Y" | "tie": which run a BA could take to release with fewer corrections, and why (two sentences).

Write {OUTPUT}: JSON {"X": {"P00": {"verdict": "pass"|"fail", "quote": "...", "reason": "..."}, ... "P16": {...}}, "Y": {...same...}, "overall": "X"|"Y"|"tie", "overall_reason": "..."}. Valid JSON, UTF-8.

Reply with one line: pass counts for X and Y.
```

## Поправка 1 (до запуска судей): судья процесса разрезан по размеру

Вход одного судьи процесса — 2,1 МБ, в один контекст не помещается. Поэтому вместо одного судьи работают семь на
те же критерии и формулировки: P00 — отдельный судья на `common.md`; по три судьи на метку: `core` (Ш-3, Ш-4, Ш-5 и
возврат), `work` (Ш-6…Ш-9), `end` (Ш-В, Ш-Р, Ш-С, журнал гейтов). Судья видит одну метку и одну часть. Критерий
проходит, только если его прошли все судьи, которым он назначен (`run.py merge`). Назначение критериев — `PIECES` в
[`run.py`](run.py). Вопрос `overall` не влияет на правила и передан судье документов: он видит оба документа.

Судья документов получает дополнительно: «Then answer: "overall": "X" | "Y" | "tie": which document a BA could take to
release with fewer corrections, and why (two sentences). Add the keys "overall" and "overall_reason" to the JSON.»

```text
You are a blind judge. ALLOWED ACTIONS: the Read tool on exactly three files ({PART}, {SCRIPT}, {MATERIALS}); Read, Grep and Glob inside {RUNTIME} only to verify a quote or a locator; Grep on {PART}; the Write tool on exactly one output file. Do not read anything else. Read {PART} completely, in consecutive ranges of 400 lines. After each range append your interim notes to {OUTPUT}.notes so a context reset loses nothing.

{PART} is part of the transcript of one run on task SIM-1106: {PART_DESCRIPTION}. It starts after earlier steps you do not see: do not fail a criterion for what happened outside this part, judge the part you see. {SCRIPT} lists the human replies; {MATERIALS} lists the facts. Facts not present in the materials, in the human replies or in a file under {RUNTIME} quoted with a locator are inventions; lines marked "условно" are scripted human answers. Links outside {RUNTIME} were unavailable to the executor by the conditions of the run, and that alone is not a defect of a step.

Score only these criteria: {CRITERIA}. For a criterion that mentions a step outside this part, apply it to the steps in this part. Each gets "pass" or "fail", a short evidence quote of at most 160 characters (verbatim) and one sentence of reasoning in Russian.

{CRITERIA_TEXT}

Write {OUTPUT}: JSON {"P01": {"verdict": "pass"|"fail", "quote": "...", "reason": "..."}, ...}. Valid JSON, UTF-8.

Reply with one line: pass count.
```
