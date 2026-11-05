#!/usr/bin/env python3
"""Инструкции исполнителей и судей RUN-0085…0087. usage: make_instructions.py OUTDIR"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; O = Path(sys.argv[1]); O.mkdir(exist_ok=True)
REPS = ("r1", "r2", "r3")
ex = re.split(r"^---\n", (ROOT / "runs/2026/RUN-0084/logs/executor-instruction.md").read_text(encoding="utf-8"), maxsplit=2, flags=re.M)[2].strip()
jg = re.split(r"^---\n", (ROOT / "runs/2026/RUN-0084/logs/judge-instruction.md").read_text(encoding="utf-8"), maxsplit=2, flags=re.M)[2].strip()
jg = jg.replace("/tmp/gh-issue-solver-1793820870313", str(ROOT)).replace('three model outputs "Выход X", "Выход Y" and "Выход Z"', 'two model outputs "Выход X" and "Выход Y"').replace("Judge X, Y and Z", "Judge X and Y").replace("produced X, Y or Z", "produced X or Y").replace(', "Y": {same keys}, "Z": {same keys}', ', "Y": {same keys}')
E86 = """You are the model under test in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool on exactly two files, and the Write tool on exactly one output file. Do NOT use Bash, Grep, Glob, git, web, or read any other file, and do not follow links found inside the files.

1. Read {PROMPT} in full. This is your system prompt: from now on you act exactly as it instructs.
2. Read {CASES}. It contains independent tasks separated by lines `=== ID ===`. Each is a separate conversation: nothing from one task may be used in another.
3. For each task give the full reply your system prompt requires to that message, in Russian, in final form.
4. Write {OUTPUT}: for each task, in order, a line `=== ID ===` followed by your reply, verbatim, with nothing else in the file.

Reply with one line: the number of tasks answered."""
E87 = """You are the model under test in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool and the Write tool on the files named below. Do NOT use Bash, Grep, Glob, git, web, or read any other file, and do not follow links found inside the files.

1. Read {PROMPT} in full. This is your system prompt: from now on you act exactly as it instructs. Answer in Russian.
2. There are five independent conversations S1, S2, S3, S4, S5, of two turns each. For each, in order:
   a. Read {EXEC}/Sn-t1.md (the BA's first message). Write your reply to {OUT}/Sn-t1.md.
   b. Only after that write, Read {EXEC}/Sn-t2.md (the BA's next message in the same conversation). Write your reply to {OUT}/Sn-t2.md.
   Never read a turn before writing the reply to the previous one. Nothing from one conversation may be used in another. The reply file contains only your reply to the BA.

Reply with one line: the number of reply files written."""
J = """You are a blind evaluator in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool on the files named below and the Write tool on exactly one output file. You may use Bash only to run `python3 -c "import json,sys; json.load(open(sys.argv[1]))" <your output file>`. Do NOT read any other file, do not use git, Grep, Glob or web.

{CRIT}
Read {BATCH} (in consecutive parts with offset/limit if large). Each case `## ID` has the input, a reference note and two model outputs, "Выход X" and "Выход Y".
Judge X and Y independently by the same standard. Do not try to work out which prompt produced them; length and style are not criteria. Be strict but literal: fail a criterion only for an observable reason, and say the reason in "note".

Write {OUTPUT}: a JSON array, one object per case in file order: {"case": "<ID>", "X": {<criterion>: true|false|null, ..., "note": "<reason for every false; empty otherwise>"}, "Y": {same keys}}.

Reply with one line: the number of cases written."""
def w(name, tpl, **kv):
    for k, v in kv.items():
        tpl = tpl.replace("{" + k + "}", str(v))
    (O / f"{name}.txt").write_text(tpl, encoding="utf-8")
for r in REPS:
    b = Path("/tmp/w85") / r
    for a in ("A2", "A3"):
        for k in (1, 2):
            w(f"85-{r}-{a}-{k}", ex, PROMPT=b/f"exec/prompt-{a}.md", CASES=b/f"exec/cases-batch{k}.md", OUTPUT=b/f"out/{a}-batch{k}.json")
    for k in (1, 2):
        w(f"85j-{r}-{k}", jg, RULES=b/"judge/rules.md", BATCH=b/f"judge/judge-batch{k}.md", OUTPUT=b/f"judge/out-batch{k}.json")
    b = Path("/tmp/w86") / r
    for g in ("S1", "S3", "S6"):
        for a in "CB":
            w(f"86-{r}-{g}-{a}", E86, PROMPT=b/f"exec/prompt-{g}-{a}.md", CASES=b/f"exec/cases-{g}.md", OUTPUT=b/f"out/{g}-{a}.md")
        w(f"86j-{r}-{g}", J, CRIT="Read /tmp/w86/criteria.txt: the criteria G1, G2, G3, P1, P2, P3, P4 (use exactly these keys).", BATCH=b/f"judge/judge-{g}.md", OUTPUT=b/f"judge/out-{g}.json")
    b = Path("/tmp/w87") / r
    for a in "CB":
        w(f"87-{r}-{a}", E87, PROMPT=b/f"exec/prompt-{a}.md", EXEC=b/"exec", OUT=b/f"out/{a}")
    w(f"87j-{r}", J, CRIT="Each case lists its own criteria (use exactly the letter-number keys it names, plus G1).", BATCH=b/"judge/judge-SES.md", OUTPUT=b/"judge/out-SES.json")
