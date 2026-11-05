#!/usr/bin/env python3
"""RUN-0089: сквозной синтетический прогон BCREQ, K (основная кнопка) против T (черновики «по тесту»), issue #454.

Правила R1 и R2 — в `preregistration.md` (закоммичено до запуска подагентов).

Использование:
    python3 experiments/issue_454/run0089/run.py prepare WORK COPIES  # промпты плеч, чек-листы, хеши
    python3 experiments/issue_454/run0089/run.py blind   WORK         # материалы слепых судей, seed 8089
    python3 experiments/issue_454/run0089/run.py score   WORK         # summary.json, вердикты R1 и R2
    python3 experiments/issue_454/run0089/run.py fixate  WORK         # runs/2026/RUN-0089/

WORK — каталог прогона (`/tmp/run88`). COPIES — вывод site_walkthrough.cjs: `{main,alt}/<шаг>.md`.
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
HERE = Path(__file__).resolve().parent
RUN = ROOT / "runs/2026/RUN-0089"
SEED = 8089
COMMON = ("Ш-0", "Ш-1", "Ш-2")
ARM = ("Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9")
SHARED = ("Ш-В", "Ш-Р", "Ш-С")
CRITICAL = ("P03", "P08", "P11", "P12", "P14")
PROCESS = tuple(f"P{n:02d}" for n in range(17))
STAGES = ("core", "work", "val", "rel")
# Pre-registration, "Провалы": every failure of the arm that stays in the kit is a fix in this PR or a backlog task.
FAIL_HANDLING = {
    "P02": "правка карточки Ш-С (указать шаг вызова); подтверждение — RUN-0090",
    "P05": "запись решения гейта: сборщик черновиков и карточки гейтов; подтверждение — RUN-0090",
    "P16": "Ш-Р v0.2 и политика на карточке: задача на промпт по R3; подтверждение — RUN-0090",
    "P14 (K, тот же Ш-В в T)": "карточка Ш-В: приложить Промпт 0 и стандарты разделов, если нет веба; подтверждение — RUN-0090",
    "S1.1": "BL-233: сверка терминов разделов 2–6 с глоссарием",
    "S1.3": "BL-233: локатор термина продукта",
    "S1.4": "BL-233: сверка со словарями; здесь нижняя граница, в чате без веба словари недоступны",
    "S3.2": "BL-233: ФТ без пункта 2.4.1 и подпункты без приёмки",
    "S3.6": "BL-233: пункт 2.4.1 без ФТ и без пометки «→ раздел 5»",
    "S8.1": "BL-233: решение по владельцу риска не доходит до таблицы 8.1",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def checklists() -> tuple[str, list[str]]:
    lines, ids = ["# Чек-листы мета-стандартов разделов 1–8", ""], []
    for path in sorted((ROOT / "standards/bcreq-sections").glob("0[1-8]-*.md")):
        section = int(path.name[:2])
        block = path.read_text(encoding="utf-8").split("## Чек-лист валидации", 1)[1].split("\n## ", 1)[0]
        items = re.findall(r"(?m)^- \[ \] (.+(?:\n {2,}.+)*)", block)
        lines += [f"## Раздел {section} ({path.name})", ""]
        for number, item in enumerate(items, 1):
            ids.append(f"S{section}.{number}")
            lines.append(f"- S{section}.{number} {' '.join(item.split())}")
        lines.append("")
    return "\n".join(lines), ids


def prepare(work: Path, copies: Path) -> int:
    hashes = {}
    for arm, button in (("K", "main"), ("T", "alt")):
        (work / arm).mkdir(parents=True, exist_ok=True)
        for step in ARM:
            shutil.copyfile(copies / button / f"{step}.md", work / arm / f"{step}.md")
        for step in SHARED:
            shutil.copyfile(copies / "main" / f"{step}.md", work / arm / f"{step}.md")
        hashes[arm] = {path.stem: sha256(path) for path in sorted((work / arm).glob("*.md"))}
    (work / "common").mkdir(exist_ok=True)
    for step in COMMON:
        shutil.copyfile(copies / "main" / f"{step}.md", work / "common" / f"{step}.md")
    hashes["common"] = {path.stem: sha256(path) for path in sorted((work / "common").glob("*.md"))}
    text, ids = checklists()
    (work / "checklists.md").write_text(text, encoding="utf-8")
    dump(work / "prompt-hashes.json", hashes)
    print(f"prompts ready; checklist items {len(ids)}; different K/T texts {sum(hashes['K'][s] != hashes['T'][s] for s in ARM)} of {len(ARM)}")
    return 0 if len(ids) == 41 else 1


PIECES = {
    "core": ("P01", "P02", "P03", "P04", "P05", "P06", "P08", "P09", "P10", "P13", "P14"),
    "work": ("P01", "P02", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P13", "P14"),
    "end": ("P02", "P05", "P08", "P11", "P12", "P13", "P14", "P15", "P16"),
}


def transcript(out: Path) -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in sorted(out.glob("[0-9][0-9]-*.md")))


def mask(body: str) -> str:
    body = re.sub(r"/tmp/run88/(?:out/)?(?:[KT]|core-[KT]|work-[KT]|val-[KT]|rel-[KT])(?=/)", "/tmp/run88/<arm>", body)
    return re.sub(r"\b(core|work|val|rel)-[KT]\b", r"\1-<arm>", body)


def pieces(work: Path, judge: Path, label: str, arm: str) -> None:
    """Addendum 1: one label's transcript cut into three parts a judge can read whole."""
    journal = (work / f"out/val-{arm}/gate-journal.md").read_text(encoding="utf-8")
    (judge / f"{label}-core.md").write_text(mask(transcript(work / "out" / f"core-{arm}")), encoding="utf-8")
    (judge / f"{label}-work.md").write_text(mask(transcript(work / "out" / f"work-{arm}")), encoding="utf-8")
    end = [f"# Стадия {stage}\n\n{transcript(work / 'out' / f'{stage}-{arm}')}" for stage in ("val", "rel")]
    (judge / f"{label}-end.md").write_text(mask("\n\n".join(end + ["# Журнал гейтов\n\n" + journal])), encoding="utf-8")


def merge(work: Path) -> int:
    """Addendum 1: a criterion passes only if every piece judge that saw it passes it."""
    judge = work / "judge"
    process: dict = {"X": {}, "Y": {}}
    p00 = json.loads((judge / "p-common.json").read_text(encoding="utf-8"))["P00"]
    for label in ("X", "Y"):
        seen: dict = {"P00": [("common", p00)]}
        for piece in ("core", "work", "end"):
            scores = json.loads((judge / f"p-{label}-{piece}.json").read_text(encoding="utf-8"))
            assert set(scores) == set(PIECES[piece]), (label, piece, sorted(set(scores) ^ set(PIECES[piece])))
            for code, value in scores.items():
                seen.setdefault(code, []).append((piece, value))
        assert set(seen) == set(PROCESS), sorted(set(seen) ^ set(PROCESS))
        for code, values in seen.items():
            failed = [v for _, v in values if v["verdict"] != "pass"]
            chosen = (failed or [v for _, v in values])[0]
            process[label][code] = {**chosen, "verdict": "fail" if failed else "pass", "pieces": {name: v["verdict"] for name, v in values}}
    document = json.loads((judge / "document.json").read_text(encoding="utf-8"))
    process["overall"], process["overall_reason"] = document["overall"], document["overall_reason"]
    dump(judge / "process.json", process)
    print({label: sum(v["verdict"] == "pass" for v in process[label].values()) for label in ("X", "Y")})
    return 0


def blind(work: Path) -> int:
    order = ["K", "T"]
    random.Random(SEED).shuffle(order)
    key = {"X": order[0], "Y": order[1], "seed": SEED}
    judge = work / "judge"
    judge.mkdir(exist_ok=True)
    (judge / "common.md").write_text(mask(transcript(work / "out/in")), encoding="utf-8")
    for label in ("X", "Y"):
        arm = key[label]
        parts = [f"# Стадия {stage}\n\n{transcript(work / 'out' / f'{stage}-{arm}')}" for stage in STAGES]
        parts.append("# Журнал гейтов\n\n" + (work / f"out/val-{arm}/gate-journal.md").read_text(encoding="utf-8"))
        (judge / f"{label}-process.md").write_text(mask("\n\n".join(parts)), encoding="utf-8")
        (judge / f"{label}-document.md").write_text(mask((work / f"out/val-{arm}/document-final.md").read_text(encoding="utf-8")), encoding="utf-8")
        pieces(work, judge, label, arm)
    dump(judge / "key.json", key)
    print("blinded; sizes", {p.name: p.stat().st_size for p in sorted(judge.glob("*.md"))})
    return 0


def verdict(process: dict, document: dict, sections_present: bool) -> str:
    failed_critical = [c for c in CRITICAL if process[c]["verdict"] != "pass"]
    invented = [i for i in document["inventions"] if i.get("critical")]
    if failed_critical or invented or not sections_present:
        return "не готов"
    items = list(document["items"].values())
    passed = sum(i["verdict"] == "pass" for i in items)
    if all(process[c]["verdict"] == "pass" for c in PROCESS) and passed >= 37:
        return "готов"
    return "готов с пробелами"


def score(work: Path) -> int:
    key = json.loads((work / "judge/key.json").read_text(encoding="utf-8"))
    process = json.loads((work / "judge/process.json").read_text(encoding="utf-8"))
    document = json.loads((work / "judge/document.json").read_text(encoding="utf-8"))
    _, ids = checklists()
    hashes = json.loads((work / "prompt-hashes.json").read_text(encoding="utf-8"))
    for arm in ("K", "T", "common"):
        for step, value in hashes[arm].items():
            assert sha256(work / arm / f"{step}.md") == value, (arm, step)
    summary = {"judge_seed": SEED, "key": key, "arms": {}, "overall": {"winner": key.get(process.get("overall"), process.get("overall")), "reason": process.get("overall_reason", "")}, "prompts": hashes}
    for label in ("X", "Y"):
        arm, proc, doc = key[label], process[label], document[label]
        assert set(doc["items"]) == set(ids), sorted(set(ids) ^ set(doc["items"]))
        final = (work / f"out/val-{arm}/document-final.md").read_text(encoding="utf-8")
        present = {n: bool(re.search(rf"(?m)^#+ .*Раздел {n}\b|^#+ *{n}[.\s]", final)) for n in range(1, 9)}
        passed_process = sum(proc[c]["verdict"] == "pass" for c in PROCESS)
        passed_items = sum(i["verdict"] == "pass" for i in doc["items"].values())
        by_section = {}
        for item, value in doc["items"].items():
            section = item[1:].split(".")[0]
            by_section.setdefault(section, [0, 0])
            by_section[section][0] += value["verdict"] == "pass"
            by_section[section][1] += 1
        summary["arms"][arm] = {
            "process_passed": passed_process, "process_failed": [c for c in PROCESS if proc[c]["verdict"] != "pass"],
            "items_passed": passed_items, "items_total": len(ids),
            "items_failed": [i for i, v in doc["items"].items() if v["verdict"] != "pass"],
            "by_section": by_section, "sections_present": present,
            "inventions": len(doc["inventions"]), "critical_inventions": sum(bool(i.get("critical")) for i in doc["inventions"]),
            "R1": verdict(proc, doc, all(present.values())), "total": passed_process + passed_items,
        }
    k, t = summary["arms"]["K"], summary["arms"]["T"]
    summary["R2"] = {"t_not_worse": t["total"] >= k["total"], "t_r1_not_failed": t["R1"] != "не готов", "by_test": t["total"] >= k["total"] and t["R1"] != "не готов"}
    summary["R3"] = {"assembles": all(proc["P16"]["verdict"] == "pass" for proc in (process["X"], process["Y"]))}
    summary["fail_handling"] = FAIL_HANDLING
    dump(work / "summary.json", summary)
    print(json.dumps({"arms": summary["arms"], "R2": summary["R2"], "R3": summary["R3"], "overall": summary["overall"]}, ensure_ascii=False))
    return 0


def fixate(work: Path) -> int:
    for sub in ("inputs", "outputs", "logs", "feedback"):
        (RUN / sub).mkdir(parents=True, exist_ok=True)
    links = {
        "input-pack.md": {"](../../../runs/2026/RUN-0078/": "](../../RUN-0078/"},
        "judge-instruction.md": {"](run.py)": "](../../../../experiments/issue_454/run0089/run.py)"},
        "preregistration.md": {"](input-pack.md)": "](../inputs/input-pack.md)", "](customer-materials.md)": "](../inputs/customer-materials.md)",
                               "](ba-script.md)": "](../inputs/ba-script.md)"},
    }
    for sub, names in (("inputs", ("input-pack.md", "customer-materials.md", "ba-script.md")),
                       ("logs", ("executor-instruction.md", "judge-instruction.md", "preregistration.md"))):
        for name in names:
            body = (HERE / name).read_text(encoding="utf-8")
            for old, new in links.get(name, {}).items():
                assert old in body, (name, old)
                body = body.replace(old, new)
            (RUN / sub / name).write_text(body, encoding="utf-8")
    (RUN / "outputs/common-transcript.md").write_text(transcript(work / "out/in"), encoding="utf-8")
    for arm in ("K", "T"):
        parts = [f"# Стадия {stage}\n\n{transcript(work / 'out' / f'{stage}-{arm}')}" for stage in STAGES]
        (RUN / f"outputs/{arm}-transcript.md").write_text("\n\n".join(parts), encoding="utf-8")
        shutil.copyfile(work / f"out/val-{arm}/document-final.md", RUN / f"outputs/{arm}-document.md")
        shutil.copyfile(work / f"out/val-{arm}/gate-journal.md", RUN / f"outputs/{arm}-gate-journal.md")
    for name, target in (("judge/process.json", "judge-process.json"), ("judge/document.json", "judge-document.json"),
                         ("judge/key.json", "judge-key.json"), ("summary.json", "summary.json"), ("checklists.md", "checklists.md")):
        shutil.copyfile(work / name, RUN / "outputs" / target)
    print(f"fixated into {RUN.relative_to(ROOT)}")
    return 0


def main() -> int:
    command, work = sys.argv[1], Path(sys.argv[2]).resolve()
    if command == "prepare":
        return prepare(work, Path(sys.argv[3]).resolve())
    return {"blind": blind, "merge": merge, "score": score, "fixate": fixate}[command](work)


if __name__ == "__main__":
    raise SystemExit(main())
