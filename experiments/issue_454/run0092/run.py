#!/usr/bin/env python3
"""RUN-0092: подтверждение правок комплекта 0.7 после RUN-0089. Правила — logs/preregistration.md.

    python3 experiments/issue_454/run0092/run.py prepare WORK COPIES  # входы плеч, хеши, сверка с плечом T RUN-0089
    python3 experiments/issue_454/run0092/run.py blind   WORK         # материалы судьи, seed 8090
    python3 experiments/issue_454/run0092/run.py check   WORK         # механика P16, правила R3'…R6, summary.json
    python3 experiments/issue_454/run0092/run.py fixate  WORK         # runs/2026/RUN-0092/outputs

WORK — каталог прогона (/tmp/run90). COPIES — вывод site_walkthrough.cjs, {main,alt}/<шаг>.md.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "runs/2026/RUN-0092"
PRIOR = ROOT / "runs/2026/RUN-0089"
SEED = 8090
ARMS = {"rel-T": ("Ш-Р",), "rel-K": ("Ш-Р",), "val-K": ("Ш-В", "Ш-0"), "gate-in": ("Ш-2",), "gate-c1": ("Ш-5",), "sc": ("Ш-С",)}
SAME_AS_T = ("Ш-3", "Ш-4", "Ш-6", "Ш-7", "Ш-9", "Ш-В", "Ш-С")
SAME_AS_COMMON = ("Ш-0", "Ш-1")
SECTION = re.compile(r"(?m)^## Раздел (\d)\.")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sections(text: str, wanted: set[int]) -> str:
    marks = [(int(m.group(1)), m.start()) for m in SECTION.finditer(text)]
    ends = [m[1] for m in marks[1:]] + [len(text)]
    return "".join(text[start:end] for (num, start), end in zip(marks, ends) if num in wanted)


def prepare(work: Path, copies: Path) -> None:
    for step in SAME_AS_T:
        assert (work.parent / "run88/T" / f"{step}.md").read_bytes() == (copies / "main" / f"{step}.md").read_bytes(), step
    for step in SAME_AS_COMMON:
        assert (work.parent / "run88/common" / f"{step}.md").read_bytes() == (copies / "main" / f"{step}.md").read_bytes(), step
    outputs = PRIOR / "outputs"
    t_doc = (outputs / "T-document.md").read_text(encoding="utf-8")
    common = (outputs / "common-transcript.md").read_text(encoding="utf-8")
    cut = re.search(r"(?m)^## Ход \d+ — Ш-2", common).start()
    inputs = work / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    (inputs / "prior-sh0-sh1.md").write_text(common[:cut], encoding="utf-8")
    (inputs / "sections-1-4.md").write_text(sections(t_doc, {1, 2, 3, 4}), encoding="utf-8")
    (inputs / "sections-1-3.md").write_text(sections(t_doc, {1, 2, 3}), encoding="utf-8")
    for name in ("T-document.md", "K-document.md", "T-gate-journal.md", "K-gate-journal.md"):
        shutil.copy(outputs / name, inputs / name)
    for name in ("customer-materials.md", "input-pack.md"):
        shutil.copy(PRIOR / "inputs" / name, inputs / name)
    standards = inputs / "standards"
    standards.mkdir(exist_ok=True)
    for path in sorted((ROOT / "standards/bcreq-sections").glob("0[1-8]-*.md")):
        shutil.copy(path, standards / path.name)
    prompts = work / "prompts"
    prompts.mkdir(exist_ok=True)
    hashes = {}
    for step in sorted({s for steps in ARMS.values() for s in steps}):
        shutil.copy(copies / "main" / f"{step}.md", prompts / f"{step}.md")
        hashes[step] = sha(prompts / f"{step}.md")
    dump(work / "prompt-hashes.json", hashes)
    for arm in ARMS:
        (work / "out" / arm).mkdir(parents=True, exist_ok=True)
    print("prepared", hashes)


def blind(work: Path) -> None:
    labels = ["A", "B"]
    random.Random(SEED).shuffle(labels)
    key = {labels[0]: "T", labels[1]: "K"}
    judge = work / "judge"
    if judge.exists():
        shutil.rmtree(judge)
    judge.mkdir()
    dump(judge / "key.json", key)
    for label, arm in key.items():
        target = judge / f"rel-{label}"
        shutil.copytree(work / "out" / f"rel-{arm}", target)
        shutil.copy(work / "inputs" / f"{arm}-document.md", judge / f"document-{label}.md")
    for arm in ("val-K", "gate-in", "gate-c1", "sc"):
        shutil.copytree(work / "out" / arm, judge / arm)
    print("blind", key)


FORBIDDEN = {
    "[ТРЕБУЕТСЯ": re.compile(r"\[ТРЕБУЕТСЯ"),
    "Состояние BCREQ": re.compile(r"Состояние BCREQ"),
    "В-NN": re.compile(r"(?<![А-Яа-яA-Za-z-])В-\d"),
    "Р-NN": re.compile(r"(?<![А-Яа-яA-Za-z-])Р-\d"),
}
# Заголовки вне состава: пункт 2.5 и разделы по их номеру или полному названию.
OUTSIDE = {
    "2.5": re.compile(r"(?m)^#{1,6}[^\n]*\b2\.5\b"),
    "5": re.compile(r"(?m)^#{1,6}\s*(Раздел )?5[. ]"),
    "6": re.compile(r"(?m)^#{1,6}\s*(Раздел )?6[. ]"),
    "7": re.compile(r"(?m)^#{1,6}\s*(Раздел )?7[. ]"),
    "8": re.compile(r"(?m)^#{1,6}\s*(Раздел )?8[. ]"),
}
INSIDE = {n: re.compile(rf"(?m)^#{{1,6}}\s*(Раздел )?{n}[. ]") for n in "1234"}


def mechanics(path: Path, excluded: list[str], required: list[str]) -> dict:
    if not path.exists():
        return {"ok": False, "missing_file": True}
    text = path.read_text(encoding="utf-8")
    found = {name: len(rx.findall(text)) for name, rx in FORBIDDEN.items() if rx.search(text)}
    outside = [n for n in excluded if OUTSIDE[n].search(text)]
    absent = [n for n in required if not (INSIDE.get(n) or OUTSIDE[n]).search(text)]
    return {"ok": not found and not outside and not absent, "forbidden": found, "outside": outside, "absent": absent, "bytes": len(text.encode())}


def check(work: Path) -> None:
    hashes = json.loads((work / "prompt-hashes.json").read_text(encoding="utf-8"))
    for step, value in hashes.items():
        assert sha(work / "prompts" / f"{step}.md") == value, step
    mech = {}
    for arm in ("rel-T", "rel-K"):
        out = work / "out" / arm
        mech[arm] = {
            "ft": mechanics(out / "packet-ft.md", ["2.5", "5", "6", "7", "8"], list("1234")),
            "tz": mechanics(out / "packet-tz.md", ["2.5", "5", "7", "8"], list("12346")),
        }
    verdicts_path = work / "judge" / "verdicts.json"
    summary = {"prompt_hashes": hashes, "mechanical_p16": mech}
    if verdicts_path.exists():
        verdicts = json.loads(verdicts_path.read_text(encoding="utf-8"))
        key = json.loads((work / "judge" / "key.json").read_text(encoding="utf-8"))
        rel = {key[label]: verdicts[f"rel-{label}"] for label in key}
        passed = lambda block, name: block[name]["verdict"] == "pass"
        mech_ok = all(mech[f"rel-{a}"][p]["ok"] for a in "TK" for p in ("ft", "tz"))
        summary.update({
            "key": key,
            "R3": {"passed": mech_ok and all(passed(rel[a], "P16") and passed(rel[a], "P12") for a in "TK"),
                   "mechanical": mech_ok, "judge": {a: {c: rel[a][c]["verdict"] for c in ("P16", "P12")} for a in "TK"}},
            "R4": {"passed": all(passed(verdicts["val-K"], c) for c in ("P14", "P11")),
                   "judge": {c: verdicts["val-K"][c]["verdict"] for c in ("P14", "P11")}},
            "R5": {"passed": passed(verdicts["gate-in"], "P05") and passed(verdicts["gate-c1"], "P05"),
                   "judge": {g: verdicts[g]["P05"]["verdict"] for g in ("gate-in", "gate-c1")}},
            "R6": {"passed": all(passed(verdicts["sc"], c) for c in ("P02", "P15")),
                   "judge": {c: verdicts["sc"][c]["verdict"] for c in ("P02", "P15")}},
        })
    dump(work / "summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "prompt_hashes"}, ensure_ascii=False, indent=1))


def fixate(work: Path) -> None:
    out = RUN / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    for arm in ARMS:
        for path in sorted((work / "out" / arm).glob("*.md")):
            shutil.copy(path, out / f"{arm}-{path.name}")
    shutil.copy(work / "judge" / "verdicts.json", out / "judge-verdicts.json")
    shutil.copy(work / "judge" / "key.json", out / "judge-key.json")
    shutil.copy(work / "summary.json", out / "summary.json")
    print("fixated", len(list(out.iterdir())))


if __name__ == "__main__":
    command, work = sys.argv[1], Path(sys.argv[2])
    if command == "prepare":
        prepare(work, Path(sys.argv[3]))
    else:
        {"blind": blind, "check": check, "fixate": fixate}[command](work)
