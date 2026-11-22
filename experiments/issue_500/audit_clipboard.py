#!/usr/bin/env python3
"""Apply the prompt-purity policy to the bodies saved by browser-smoke.js."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_prompt_purity import Auditor  # noqa: E402


def main(path):
    path = Path(path).resolve()
    bodies = json.loads(path.read_text(encoding="utf-8"))
    if not bodies:
        raise ValueError("Нет тел, скопированных в браузере")
    auditor = Auditor(ROOT)
    auditor.audit_site_file(path, "abc", list(bodies), card=False)
    for finding in auditor.findings:
        print(f"{finding['where']}:{finding['line']}: {finding['rule']}: {finding['match']}")
    print(f"Буфер Chromium — {len(bodies)} тел, {len(auditor.findings)} нарушений")
    return int(bool(auditor.findings))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
