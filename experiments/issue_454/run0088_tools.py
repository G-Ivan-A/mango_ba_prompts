#!/usr/bin/env python3
"""RUN-0088 helper: snapshot the exact site texts, assemble the BA's document from step blocks, compute mechanical checks.

  python3 experiments/issue_454/run0088_tools.py prepare         # write /tmp/run0088/prompts, inputs/prompt-set.json
  python3 experiments/issue_454/run0088_tools.py assemble LABEL  # overlay outputs/steps/LABEL/blocks.md on the current document
  python3 experiments/issue_454/run0088_tools.py checks          # outputs/mechanical-checks.json

The assembler plays the BA's copying: earlier blocks stay byte-identical unless a step or the BA editor returns them.
It runs no model and judges nothing.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "runs/2026/RUN-0088"
SNAP = Path("/tmp/run0088/prompts")
DOC = RUN / "outputs/document"
ORDER = ["1", "2", "2.5", "3", "4", "5", "6", "7", "8.1", "8.2", "8.3", "8.4", "8.5", "state"]
PAIRED = ["Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В"]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prepare():
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
    site = json.loads((ROOT / "site/data/prompts.json").read_text(encoding="utf-8"))
    by_file = {Path(p["sourcePath"]).name: p for p in site["prompts"] if p.get("sourcePath")}
    SNAP.mkdir(parents=True, exist_ok=True)
    rows = []
    for step in kit["steps"]:
        code = step["step"].split()[0]
        published = step.get("published")
        text = step["draft"]["body"] if step["mode"] == "by-test" else by_file[published["file"]]["body"]
        (SNAP / f"{code}-assigned.md").write_text(text, encoding="utf-8")
        row = {"step": code, "mode": step["mode"], "assigned_sha256": sha(text), "assigned_bytes": len(text.encode("utf-8")),
               "card_sha256": (step["draft"] if step["mode"] == "by-test" else published)["sha256"]}
        if code in PAIRED:
            (SNAP / f"{code}-draft.md").write_text(step["draft"]["body"], encoding="utf-8")
            row["draft_sha256"] = sha(step["draft"]["body"])
        rows.append(row)
    (RUN / "inputs/prompt-set.json").write_text(json.dumps({"kit": kit["kit"]["version"], "steps": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(rows), "steps;", len(PAIRED), "paired drafts")


def read_blocks(path):
    text = path.read_text(encoding="utf-8")
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"<!-- block:([\w.\-]+) -->\n(.*?)\n<!-- /block -->", text, re.S)}


def load_current():
    path = DOC / "current.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def render(blocks):
    parts = ["# Документ BCREQ SIM-1106 (как его ведёт БА)", ""]
    for key in ORDER:
        if key in blocks:
            parts += [f"<!-- block:{key} -->", blocks[key], "<!-- /block -->", ""]
    return "\n".join(parts)


def assemble(label):
    current = load_current()
    new = read_blocks(RUN / "outputs/steps" / label / "blocks.md")
    unknown = sorted(set(new) - set(ORDER))
    changed = sorted(k for k in new if k in ORDER and current.get(k) != new[k])
    current.update({k: v for k, v in new.items() if k in ORDER})
    (DOC / "current.json").write_text(json.dumps(current, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    (DOC / f"after-{label}.md").write_text(render(current), encoding="utf-8")
    print(label, "changed:", changed, "ignored:", unknown, "bytes:", len(render(current).encode("utf-8")))


def sentences(text):
    plain = re.sub(r"[`*|#>]", " ", text)
    return [s for s in re.split(r"(?<=[.!?])\s+|\n", plain) if s.strip()]


def checks():
    doc = load_current()
    words = lambda t: len(re.findall(r"\S+", t))
    fr = sorted(set(re.findall(r"ФТ-\d+", doc.get("3", ""))))
    uc_text = doc.get("7", "")
    uncovered = [f for f in fr if f not in uc_text]
    design = doc.get("5", "")
    accept = doc.get("8.3", "")
    result = {
        "blocks_present": [k for k in ORDER if k in doc], "blocks_missing": [k for k in ORDER if k not in doc],
        "words": {k: words(doc[k]) for k in doc},
        "budgets": {"section_2_le_250": words(doc.get("2", "")) <= 250, "section_5_le_900": words(design) <= 900, "section_6_le_250": words(doc.get("6", "")) <= 250},
        "sentences_over_20_words": {k: sum(1 for s in sentences(doc[k]) if words(s) > 20) for k in ["1", "2", "3", "4", "5", "6", "7"] if k in doc},
        "fr_ids": fr, "fr_without_uc": uncovered, "fr_without_design": [f for f in fr if f not in design], "fr_without_acceptance": [f for f in fr if f not in accept],
    }
    (RUN / "outputs/mechanical-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    {"prepare": prepare, "checks": checks}.get(sys.argv[1], lambda: assemble(sys.argv[2]))()
