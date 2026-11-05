---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0088 — инструкция исполнителя (дословно передаётся подагенту)

```text
You are the model under test in a controlled replay of one step of a BA's chat-based requirements workflow. ALLOWED ACTIONS: the Read tool on the files listed below; Read, Grep and Glob ONLY inside {RUNTIME} (the knowledge base the prompts call "runtime"); the Write tool on exactly two output files. Do NOT use Bash, git, web, and do not read any other file in the repository or follow links outside {RUNTIME}. A link in a prompt to a github.com/G-Ivan-A/mango-ba-ai-runtime file at commit 68ad8fcf maps to the same relative path inside {RUNTIME}; ANY other link, including links to standards in mango_ba_prompts, is unavailable: say so as the prompt instructs for an unavailable source, never guess its content.

Files: {PROMPT} (the prompt the BA pasted: your only instruction), {INPUT} (task card, customer request, knowledge-base note), {DOC} (the document as the BA keeps it so far, including the last state block; may not exist at the first step), {JOURNAL} (gate decisions the BA recorded; may not exist yet), {SCRIPT} (scripted BA replies; use only the section "{SECTION}").

Procedure:
1. Read all the files in full.
2. Play the step turn by turn, acting exactly as {PROMPT} instructs. The first BA message consists of {PROMPT}, the customer request, {DOC}, {JOURNAL} and any "first message" text given in the section "{SECTION}" of {SCRIPT}.
3. After each of your turns that ends with a stop-gate, a question or a stop, append the next BA reply from that section verbatim, then continue; follow the rule "нет ответа" in {SCRIPT}. Never invent BA replies; never skip a stop-gate the prompt requires; never merge substeps the prompt says to do one at a time. You are not the BA: gate decisions are not yours.
4. Write {TRANSCRIPT}: a Markdown transcript. Each model turn starts with a heading "## Ход N — <step.substep> — модель", each BA reply with "## Ход N — БА" followed by the verbatim reply. Model turns contain exactly what you would have shown the BA, in Russian, nothing else (no commentary about this experiment). At the very end add "## Журнал исполнителя" with three lists: (a) files under {RUNTIME} you actually read; (b) links you could not open; (c) "Чего не хватило": every point where the prompt required data, a parameter, a document or an instruction that neither {PROMPT}, {INPUT}, {DOC}, {JOURNAL} nor the BA replies gave, one line each, or "нет".
5. Write {BLOCKS}: the final text of every document block this step produced or changed, copied verbatim from your last version in the transcript, each wrapped exactly as:
<!-- block:KEY -->
text
<!-- /block -->
KEY is one of 1, 2, 2.5, 3, 4, 5, 6, 7, 8.1, 8.2, 8.3, 8.4, 8.5, state. "state" is the state block "Состояние BCREQ". 8.4 and 8.5 are written whole, as updated, whenever you changed them. Do not improve or add anything while copying. Blocks you did not change are not written.

Reply with one line: the number of model turns written.
```
