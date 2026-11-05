---
status: draft
version: 0.1
updated: 2026-11-05
temperature: 0.1
---

# Инструкция исполнителя (образец)

```text
You are the model under test in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool and the Write tool on the files named below. Do NOT use Bash, Grep, Glob, git, web, or read any other file, and do not follow links found inside the files.

1. Read /tmp/w87/r1/exec/prompt-B.md in full. This is your system prompt: from now on you act exactly as it instructs. Answer in Russian.
2. There are five independent conversations S1, S2, S3, S4, S5, of two turns each. For each, in order:
   a. Read /tmp/w87/r1/exec/Sn-t1.md (the BA's first message). Write your reply to /tmp/w87/r1/out/B/Sn-t1.md.
   b. Only after that write, Read /tmp/w87/r1/exec/Sn-t2.md (the BA's next message in the same conversation). Write your reply to /tmp/w87/r1/out/B/Sn-t2.md.
   Never read a turn before writing the reply to the previous one. Nothing from one conversation may be used in another. The reply file contains only your reply to the BA.

Reply with one line: the number of reply files written.
```
