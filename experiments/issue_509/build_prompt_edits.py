#!/usr/bin/env python3
"""Record exact #509 draft changes without rewriting any historical fixture."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = "b0caecd30968fb7e62678e78fffc43a4031d3f3f"
MERGED = "70cf31c803443f563ee852b3daf27cb972706c4b"
OUT = Path(__file__).with_name("prompt-edits.json")
spec = importlib.util.spec_from_file_location("hunks495", ROOT / "experiments/issue_495/build_prompt_edits.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def build():
    names = helper.git("diff", "--name-only", BASE, MERGED, "--", "prompts/drafts").splitlines()
    files = {}
    for name in names:
        before = helper.git("show", f"{BASE}:{name}")
        after = helper.git("show", f"{MERGED}:{name}")
        if before == after:
            continue
        for context in range(1, 8):
            hunks = helper.hunks(before, after, context)
            if hunks and helper.apply_hunks(after, hunks) == before:
                break
        else:
            raise ValueError(f"Ambiguous hunks: {name}")
        files[name] = {"sha256_before": helper.sha(before), "sha256_after": helper.sha(after), "hunks": hunks}
    return {"issue": 509, "base": BASE, "revert_order": [509, 488, 495], "files": files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build(), ensure_ascii=False, indent=1) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit("stale #509 prompt-edits.json")
    else:
        OUT.write_text(rendered)
    print("OK: exact #509 draft changes")


if __name__ == "__main__":
    main()
