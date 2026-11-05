---
status: draft
version: 0.1
updated: 2026-11-05
ai-generated: true
type: experiment-instruction
scope: mango-only
---

# RUN-0088 — инструкция исполнителя (дословно передаётся подагенту)

Подстановки каждой стадии — в таблице под текстом. `{STAGE_RULES}` — блок
стадии из той же таблицы.

```text
You are the model under test in a controlled replay of a stepwise BA dialogue. ALLOWED ACTIONS: the Read tool on the files listed below; Read, Grep and Glob ONLY inside {RUNTIME} (the knowledge base the prompts call "runtime"); the Write tool on files inside {OUT} only. Do NOT use Bash, git, web, and do not read any other file in the repository or follow links outside {RUNTIME}. A link in a prompt to a github.com/G-Ivan-A/mango-ba-ai-runtime file maps to the same relative path inside {RUNTIME}; any other link is unavailable: say so instead of guessing its content.

Files: {PROMPTS} (the exact texts a BA copies from the site, one file per step), {INPUT} (task card, customer request, knowledge-base note), {SCRIPT} (scripted BA replies), {PRIOR} (earlier parts of the same chat or attachments, see the stage rules).

Procedure:
1. Read all listed files in full.
2. Play the dialogue turn by turn. For each step listed in the stage rules, act exactly as that step's prompt instructs, as if the prompt were your only instruction. Your input for a step is what the prompt asks for, taken from the material the stage rules make visible.
3. After each of your turns that ends with a stop-gate, a question or a stop, append the next BA reply for the current step from {SCRIPT} verbatim, then continue. Never invent BA replies; never skip a stop-gate the prompt requires; never merge substeps the prompt says to do one at a time.
4. Write one Markdown file per pass of a step into {OUT}, as soon as that pass is finished: {OUT}/<NN>-<step>.md, NN = the order of the pass. Each model turn starts with a heading "## Ход N — <step.substep> — модель", each BA reply with "## Ход N — БА" followed by the verbatim reply. Model turns contain exactly what you would have shown the BA, in Russian, nothing else (no commentary about this experiment). Repeat earlier text only if the prompt's output format requires it.
5. {STAGE_RULES}
6. At the very end write {OUT}/99-executor-log.md with the heading "## Журнал исполнителя": which files under {RUNTIME} you actually read (paths), which links you could not open, every stop outside a stop-gate, and any line "ТУПИК: <step, reason>" under the dead-end rule of {SCRIPT}.

Reply with one line: the number of model turns written.
```

| Стадия | `{PROMPTS}` | `{PRIOR}` | `{STAGE_RULES}` |
| --- | --- | --- | --- |
| E-IN | `common/Ш-0.md`, `Ш-1.md`, `Ш-2.md` | нет | Steps: Ш-0, Ш-1, Ш-2. Sections "A-IN" of the script. Your input for Ш-0 is the task card and the customer request; later steps see the whole dialogue. Stop after reply Б-2.6. |
| E-CORE-<плечо> | `<плечо>/Ш-3.md`, `Ш-4.md`, `Ш-5.md` | транскрипт E-IN | Treat {PRIOR} as the earlier part of this same chat. Steps: Ш-3, Ш-4, Ш-5, the first pass, then the return pass Ш-3, Ш-4, Ш-5 as the scripted replies order. Sections "A-CORE" of the script. Stop after reply Б-5r.5. |
| E-WORK-<плечо> | `<плечо>/Ш-6.md`, `Ш-7.md`, `Ш-8.md`, `Ш-9.md` | транскрипты E-IN и E-CORE | Treat {PRIOR} as the earlier part of this same chat. Steps: Ш-6, Ш-7, Ш-8, Ш-9, section "A-WORK" of the script. After Ш-9 act as the BA's clerk: write {OUT}/document-candidate.md: the latest version of each of sections 1–8 and of the "Состояние BCREQ" block as shown in the dialogue, copied without edits, additions or summaries (a section the dialogue never showed stays as an empty heading with the note "не выведен"). Then write {OUT}/gate-journal.md with the table of the journal form below for Г-IN and both Г-С1 decisions: decisions and deciders only from the scripted replies, model_recommendation from the model's gate report, divergence by comparing them. Journal columns: gate_id, gate_type, Решение, Кто решил, model_recommendation, divergence, Причина расхождения. |
| E-VAL-<плечо> | `<плечо>/Ш-В.md` | `document-candidate.md`, `customer-materials.md`, `gate-journal.md` (only for the clerk step) | New chat without history. Step: Ш-В only; its input is the document, the customer materials and the knowledge base. Do not read gate-journal.md before Ш-В is written. Script rows Б-В.0, Б-В.1. After Б-В.1 act as the BA's clerk: write {OUT}/document-final.md: document-candidate.md with the accepted variants applied literally (only what a variant says), rejected ones noted in 8.5, the Г-W decision, its owners and the estimate added in 8.5 exactly as Б-В.1 says. A variant that cannot be applied literally stays unapplied and goes to 8.4 as an open question. Write {OUT}/gate-journal.md: the given journal plus a row for Г-W. |
| E-REL-<плечо> | `<плечо>/Ш-Р.md`, `<плечо>/Ш-С.md` | `document-final.md`, `gate-journal.md`, `customer-materials.md` | New chat without history for each step. Step Ш-Р, script row Б-Р.0: do not declare release; the human gate stays open. Then, in another new chat that sees only sections 1, 2, 3 of document-final.md, step Ш-С, script row Б-С.0. |
