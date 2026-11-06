---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0092 — инструкция исполнителя (дословно передаётся подагенту)

Та же, что в [RUN-0089](../../RUN-0089/logs/executor-instruction.md), с правилами плеч ниже.

```text
You are the model under test in a controlled replay of a stepwise BA dialogue. ALLOWED ACTIONS: the Read tool on the files listed below; Read, Grep and Glob ONLY inside {RUNTIME} (the knowledge base the prompts call "runtime"); the Write tool on files inside {OUT} only. Do NOT use Bash, git, web, and do not read any other file in the repository or follow links outside {RUNTIME}. A link in a prompt that points outside {RUNTIME} and is not among the listed files is unavailable: act as the prompt says for an unavailable source.

Files: {PROMPTS} (the exact text a BA copies from the site), {SCRIPT} (scripted BA replies, use only the rows of arm {ARM}), {ATTACH} (earlier parts of the same chat or attachments, see the arm rules).

Procedure:
1. Read all listed files in full.
2. Play the dialogue turn by turn. Act exactly as the step's prompt instructs, as if the prompt were your only instruction.
3. After each of your turns that ends with a stop-gate, a question or a stop, append the next BA reply of your arm from {SCRIPT} verbatim, then continue. Never invent BA replies; never skip a stop-gate the prompt requires; never merge substeps the prompt says to do one at a time.
4. Write the dialogue to {OUT}/01-dialogue.md: each model turn starts with a heading "## Ход N — <step.substep> — модель", each BA reply with "## Ход N — БА" followed by the verbatim reply. Model turns contain exactly what you would have shown the BA, in Russian, nothing else.
5. {ARM_RULES}
6. At the very end write {OUT}/99-executor-log.md with the heading "## Журнал исполнителя": which files under {RUNTIME} you actually read (paths), which links you could not open, every stop outside a stop-gate, and any line "ТУПИК: <step, reason>" under the dead-end rule of {SCRIPT}.

Reply with one line: the number of model turns written.
```

| Плечо | `{PROMPTS}` | `{ATTACH}` | `{ARM_RULES}` |
| --- | --- | --- | --- |
| E-REL-T, E-REL-K | `Ш-Р.md` | `<T\|K>-document.md`, `<T\|K>-gate-journal.md`, `customer-materials.md` | New chat without history; the attachments are all you see. Script row Б-Р.0. Do not declare release; the human gate stays open. Write the full text of the packet «ФТ на согласование» to {OUT}/packet-ft.md and of «ТЗ в договор» to {OUT}/packet-tz.md, without their manifests; in the dialogue turn, in place of the packet text, put the file name followed by the manifest. Do not write the internal packet out in full: name its composition. |
| E-VAL-K | `Ш-В.md` | `K-document.md`, `customer-materials.md`, `Ш-0.md`, `standards/*.md` | New chat without history; the attachments and the knowledge base are all you see. `Ш-0.md` and the standards are attachments, not instructions to act on. Script row Б-В.0. Stop after the remarks and the Г-W report. |
| E-GATE-IN | `Ш-2.md` | `prior-sh0-sh1.md` | Treat the attachment as the earlier part of this same chat. Step Ш-2 only, rows Б-2.1…Б-2.6. Stop after the model's turn that follows Б-2.6. |
| E-GATE-C1 | `Ш-5.md` | `sections-1-4.md`, `input-pack.md` | The attachment `sections-1-4.md` is the document so far in this chat; `input-pack.md` is the task card. Step Ш-5, run 1, rows Б-5.0, Б-5.n, Б-5.5. Do not start Ш-3 again. Stop after the model's turn that follows Б-5.5. |
| E-SC | `Ш-С.md` | `sections-1-3.md` | New chat without history; the attachment is all you see. Row Б-С.0. |
