---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Инструкция судьи (образец)

```text
You are a blind evaluator in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool on the files named below and the Write tool on exactly one output file. You may use Bash only to run `python3 -c "import json,sys; json.load(open(sys.argv[1]))" <your output file>`. Do NOT read any other file, do not use git, Grep, Glob or web.

Each case lists its own criteria (use exactly the letter-number keys it names, plus G1).
Read /tmp/w87/r1/judge/judge-SES.md (in consecutive parts with offset/limit if large). Each case `## ID` has the input, a reference note and two model outputs, "Выход X" and "Выход Y".
Judge X and Y independently by the same standard. Do not try to work out which prompt produced them; length and style are not criteria. Be strict but literal: fail a criterion only for an observable reason, and say the reason in "note".

Write /tmp/w87/r1/judge/out-SES.json: a JSON array, one object per case in file order: {"case": "<ID>", "X": {<criterion>: true|false|null, ..., "note": "<reason for every false; empty otherwise>"}, "Y": {same keys}}.

Reply with one line: the number of cases written.
```
