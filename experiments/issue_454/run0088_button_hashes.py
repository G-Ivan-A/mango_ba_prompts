#!/usr/bin/env python3
"""RUN-0088: compare the texts executors received with what the kit's main buttons give now.

A button adds a service comment and a blank line above the text, so hashes in RUN records differ
from a clipboard copy (RUN-0092 recorded the copy, RUN-0088 the text). This strips that header.
Usage: run0088_button_hashes.py [copies_dir]; copies_dir comes from site_walkthrough.cjs, default /tmp/copies/main.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COPIES = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/copies/main")
INPUTS = ROOT / "runs/2026/RUN-0088/inputs"
METADATA = (ROOT / "runs/2026/RUN-0088/metadata.yaml").read_text(encoding="utf-8")

# Executors' texts: the 0.7 snapshot from Ш-6 on. T arm hashes are read from metadata.yaml, as prompts themselves live outside the repo.
used = {code: step["sha256"] for code, step in json.loads((INPUTS / "prompt-set-0.7.json").read_text(encoding="utf-8"))["steps"].items()}
t_arm = {}
for line in METADATA.splitlines():
    if "плечо T" in line:
        t_arm[line.split("step: ")[1].split(",")[0]] = line.split("sha256: ")[1].rstrip("}")

for path in sorted(COPIES.glob("*.md")):
    body = path.read_bytes().split(b"\n", 1)[1].lstrip(b"\n")
    digest = hashlib.sha256(body).hexdigest()
    code = path.stem
    print(code, digest[:8], "chain:", (used[code][:8] + (" same" if used[code] == digest else " differs")) if code in used else "-",
          "T arm:", (t_arm[code][:8] + (" same" if t_arm[code] == digest else " differs")) if code in t_arm else "-")
