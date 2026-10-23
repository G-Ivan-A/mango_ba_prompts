#!/usr/bin/env python3
"""Negative tests for scripts/validate_issue_387_bcreq_meta_standards.py.

Each case copies the repository (without .git) into a temp dir, applies one
mutation that breaks a DoD item of issue #387 and expects the validator to
fail with the given message fragment. The unmodified copy must pass.

Usage: python3 experiments/issue_387_validator_negative.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "scripts/validate_issue_387_bcreq_meta_standards.py"
REG = "experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L"

# (name, file, old, new, expected fragment); old/new may be tuples of replacements
CASES = [
    ("checklist too long", "standards/bcreq-sections/04-non-functional-requirements.md",
     "## Чек-лист валидации\n\n", "## Чек-лист валидации\n\n" + "- [ ] x\n" * 4, "пунктов, нужно 3–7"),
    ("section heading missing", "standards/bcreq-sections/06-implementation-constraints.md",
     "## Circuit breakers", "## Предохранители", "нет секции «## Circuit breakers»"),
    ("dictionary missing", "standards/bcreq-sections/01-glossary.md", "| D7 |", "| DX |", "нет словаря D7"),
    ("short style undefined", "standards/bcreq-sections/README.md",
     "### 2.1. Короткий стиль (разделы 2, 5 L1, 6)", "### 2.1. Стиль", "короткого стиля"),
    ("only two examples", "standards/bcreq-composition-standard.md", ("### 5.3. ", "### 5.4. ", "### 5.5. "),
     ("#### 5.3. ", "#### 5.4. ", "#### 5.5. "), "примеров комбинаций 2"),
    ("ODA condition missing", "standards/bcreq-composition-standard.md", "| ODA-3 |", "| ODA |", "ODA-3"),
    ("gate role missing", "docs/contracts/bcreq-stage-gates.md", "| Заказчик [р.", "| БА [р.", "«Заказчик»"),
    ("merge missing", "standards/bcreq-prompt-architecture.md", "| М4 |", "| M4 |", "нет слияния М4"),
    ("analysis ai-generated", "docs/analysis/2026-10-23-bcreq-standards-third-opinion.md",
     "status: draft\n", "status: draft\nai-generated: true\n", "ai-generated"),
    ("rollback path missing", "docs/rfc/2026-10-bcreq-meta-standards-rfc.md",
     "Путь отката", "Откат", "Путь отката"),
    ("wrong quote line", "docs/contracts/bcreq-stage-gates.md", REG + "85)", REG + "84)", "Ч-51"),
    ("placeholder left", "standards/bcreq-sections/07-use-cases.md",
     "## Назначение\n", "## Назначение\n{{Ч-06}}\n", "плейсхолдеры"),
    ("broken anchor", "docs/rfc/2026-10-bcreq-meta-standards-rfc.md", "#50-общая-часть", "#4-recommendations",
     "якоря #4-recommendations"),
]


def run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(root / SCRIPT)], capture_output=True, text=True,
                          check=False, timeout=60)


def main() -> int:
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "repo"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns(".git", "node_modules", ".validate-cache"))
        res = run(base)
        print(f"{'ok ' if res.returncode == 0 else 'BAD'} baseline passes")
        failed += res.returncode != 0
        for name, rel, old, new, fragment in CASES:
            path = base / rel
            original = path.read_text(encoding="utf-8")
            text = original
            for o, n in zip(*((old, new) if isinstance(old, tuple) else ((old,), (new,)))):
                assert o in text, f"{name}: mutation anchor {o!r} not found in {rel}"
                text = text.replace(o, n)
            path.write_text(text, encoding="utf-8")
            res = run(base)
            ok = res.returncode == 1 and fragment in res.stdout
            print(f"{'ok ' if ok else 'BAD'} {name}" + ("" if ok else f"\n{res.stdout}"))
            failed += not ok
            path.write_text(original, encoding="utf-8")
    print("PASS" if not failed else f"FAIL: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
