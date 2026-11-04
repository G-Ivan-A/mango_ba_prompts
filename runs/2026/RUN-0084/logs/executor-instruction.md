---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
---

You are the model under test in a controlled prompt experiment. ALLOWED ACTIONS: use the Read tool on exactly two files, and the Write tool on exactly one output file. Do NOT use Bash, Grep, Glob, git, web, or read any other file, and do not follow links found inside the files.

1. Read {PROMPT} in full. This is your system prompt: from now on you act exactly as it instructs, as the second-role reviewer of a BCREQ document.
2. Read {CASES}. It contains document fragments labelled T-NN, each with "Вход" (the fragment to review) and "Контекст" (what is known about the task).
3. For each fragment independently decide whether it contains a defect according to your system prompt. Do not assume every fragment is defective; do not assume every fragment is clean. Answer in Russian, the way your system prompt requires (quote the fragment, name the violated rule, propose a fix), but compressed into the JSON fields below.
4. Write {OUTPUT}: a JSON array with one object per fragment, in the order of the file: {"case": "T-NN", "verdict": "дефект" | "дефекта нет", "violation": "<which rule is violated and why; empty if no defect>", "quote": "<verbatim quote from Вход or Контекст that your verdict relies on>", "fix": "<proposed corrected text or action; empty if no defect>"}. The file must be valid JSON (UTF-8, no comments, no trailing commas).

Reply with one line: the number of fragments written.
