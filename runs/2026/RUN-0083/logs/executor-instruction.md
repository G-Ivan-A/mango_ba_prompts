---
status: draft
version: 0.1
updated: 2026-11-04
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0083 — инструкция исполнителя (дословно передаётся подагенту)

```text
You are the model under test in a controlled replay of a stepwise BA dialogue. ALLOWED ACTIONS: the Read tool on the five files listed below; Read, Grep and Glob ONLY inside {RUNTIME} (the knowledge base the prompts call "runtime"); the Write tool on exactly one output file. Do NOT use Bash, git, web, and do not read any other file in the repository or follow links outside {RUNTIME}. A link in a prompt to a github.com/G-Ivan-A/mango-ba-ai-runtime file at commit f31dcde3 maps to the same relative path inside {RUNTIME}; any other link is unavailable — say so instead of guessing its content.

Files: {P0} (step Ш-0 system prompt), {P1} (step Ш-1 system prompt), {P2} (step Ш-2 system prompt), {INPUT} (task card, customer request, knowledge-base note), {SCRIPT} (scripted BA replies).

Procedure:
1. Read all five files in full.
2. Play the dialogue turn by turn. For each step, act exactly as that step's system prompt instructs (Ш-0, then Ш-1, then Ш-2), as if the prompt were your only instruction. Your input for Ш-0 is the task card and the customer request; for Ш-1 and Ш-2 it is everything said in the dialogue so far (your previous outputs and the BA replies) plus the customer request.
3. After each of your turns that ends with a stop-gate, a question or a stop, append the next BA reply from {SCRIPT} verbatim, then continue. Never invent BA replies; never skip a stop-gate the prompt requires; never merge substeps the prompt says to do one at a time.
4. Write {OUTPUT}: a Markdown transcript. Each model turn starts with a heading "## Ход N — <step.substep> — модель", each BA reply with "## Ход N — БА" followed by the verbatim reply. Model turns contain exactly what you would have shown the BA, in Russian, nothing else (no commentary about this experiment).
5. At the very end add "## Журнал исполнителя": which files under {RUNTIME} you actually read (paths), and which links you could not open.

Reply with one line: the number of model turns written.
```
