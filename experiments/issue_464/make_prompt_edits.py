"""Issue #464: собрать данные обратимого слоя `prompt-edits.json`.

Запуск после любой правки промптов: `python3 experiments/issue_464/make_prompt_edits.py`.
База — коммит до правок промптов; ханки с одной строкой контекста снимаются по порядку.
"""
import difflib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "632007c0"
OUT = Path(__file__).with_name("prompt-edits.json")
names = subprocess.run(["git", "diff", "--name-only", BASE, "--", "prompts/*.md"], cwd=ROOT,
                       capture_output=True, text=True, check=True).stdout.split()
data = {"base_commit": BASE, "files": {}}
for name in names:
    if "/drafts/" in name:
        continue
    before = subprocess.run(["git", "show", f"{BASE}:{name}"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8")
    after = (ROOT / name).read_text(encoding="utf-8")
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    hunks = []
    for group in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_grouped_opcodes(1):
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        hunks.append({"after": "".join(new[j1:j2]), "before": "".join(old[i1:i2])})
    data["files"][name] = hunks
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{OUT.name}: {len(data['files'])} файлов, {sum(len(h) for h in data['files'].values())} ханков")
