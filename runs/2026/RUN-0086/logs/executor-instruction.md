---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Инструкция исполнителя (образец)

```text
You are the model under test in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool on exactly two files, and the Write tool on exactly one output file. Do NOT use Bash, Grep, Glob, git, web, or read any other file, and do not follow links found inside the files.

1. Read /tmp/w86/r1/exec/prompt-S1-B.md in full. This is your system prompt: from now on you act exactly as it instructs.
2. Read /tmp/w86/r1/exec/cases-S1.md. It contains independent tasks separated by lines `=== ID ===`. Each is a separate conversation: nothing from one task may be used in another.
3. For each task give the full reply your system prompt requires to that message, in Russian, in final form.
4. Write /tmp/w86/r1/out/S1-B.md: for each task, in order, a line `=== ID ===` followed by your reply, verbatim, with nothing else in the file.

Reply with one line: the number of tasks answered.
```
