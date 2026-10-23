"""Negative tests for check_chat_context in scripts/validate_issue_384_prompts_audit.py.

Each mutation must produce at least one error; the unmodified inputs must produce none.
Run: python3 experiments/issue_384_validator_negative.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_issue_384_prompts_audit as v  # noqa: E402

text = v.DOC.read_text(encoding="utf-8")
register = v.REGISTER.read_text(encoding="utf-8")
check = json.loads(v.QUOTE_CHECK.read_text(encoding="utf-8"))

first = re.search(r"\[р\. (\d+), (Ч-\d{2})\]", text)
cases = {
    "wrong turn": (text.replace(first.group(0), f"[р. {int(first.group(1)) + 1}, {first.group(2)}]", 1), register, check),
    "unknown id": (text.replace(first.group(0), f"[р. {first.group(1)}, Ч-99]", 1), register, check),
    "wrong line": (re.sub(r"(register\.md\?plain=1#L)(\d+)", lambda m: m.group(1) + str(int(m.group(2)) + 1), text, count=1), register, check),
    "placeholder": (text + "\n{Ч-01}\n", register, check),
    "blocked": (text + "\nBLOCKED\n", register, check),
    "no 2.14 row": (re.sub(r"^\| 2\.14 \|", "| 2.15 |", text, count=1, flags=re.M), register, check),
    "observation gap": (re.sub(r"^\| Н5 \|", "| Н50 |", text, count=1, flags=re.M), register, check),
    "check not ok": (text, register, {**check, "ok": False}),
    "check sha": (text, register, {**check, "export_sha256": "0" * 64}),
    "check rows": (text, register, {**check, "results": check["results"][:-1]}),
}
failed = False
base = v.check_chat_context(text, register, check)
print("baseline:", base or "OK")
failed |= bool(base)
for name, args in cases.items():
    errors = v.check_chat_context(*args)
    print(f"{name}: {'caught' if errors else 'MISSED'} {errors[:1]}")
    failed |= not errors
sys.exit(1 if failed else 0)
