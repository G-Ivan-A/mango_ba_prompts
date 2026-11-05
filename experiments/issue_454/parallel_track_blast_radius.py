#!/usr/bin/env python3
"""Issue #454: which site texts move when the synthetic track changes a source during a BA run.

Run: python3 experiments/issue_454/parallel_track_blast_radius.py
Works in a temporary git worktree, one change at a time; the main checkout and gh-pages are not touched.
Each scenario edits one source, rebuilds drafts and site data with the repository's own scripts and compares
per-step site text against the baseline build. Writes parallel_track_blast_radius.json next to itself.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("parallel_track_blast_radius.json")
MARK = "Маркер эксперимента issue-454: фраза добавлена для замера."


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout


def build(tree):
    run([sys.executable, "scripts/build_bcreq_step_prompts.py"], tree)
    run(["node", "scripts/generate-pages-data.mjs"], tree)
    return snapshot(tree)


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def snapshot(tree):
    kit = json.loads((tree / "site/data/test-kit.json").read_text(encoding="utf-8"))
    catalog = json.loads((tree / "site/data/prompts.json").read_text(encoding="utf-8"))
    bodies = {Path(p["sourcePath"]).name: p.get("body", "") for p in catalog["prompts"] if p.get("sourcePath")}
    steps = {}
    for step in kit["steps"]:
        draft, published = step.get("draft") or {}, step.get("published") or {}
        published_body = bodies.get(published.get("file"), "")
        main = draft.get("body", "") if step["mode"] == "by-test" else published_body
        card = {k: v for k, v in step.items() if k not in ("draft", "published")}
        steps[step["step"].split()[0]] = {
            "mode": step["mode"], "main_button": digest(main), "comparison_draft": digest(draft.get("body", "")),
            "published": digest(published_body), "card": digest(json.dumps(card, ensure_ascii=False, sort_keys=True)),
        }
    other = {name: digest(body) for name, body in bodies.items() if name not in {(s.get("published") or {}).get("file") for s in kit["steps"]}}
    return {"kit_version": kit["kit"]["version"], "steps": steps, "other_prompts": other}


def append(tree, relative, text=None):
    path = tree / relative
    path.write_text(path.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + (text or MARK) + "\n", encoding="utf-8")


def replace(tree, relative, old, new):
    path = tree / relative
    source = path.read_text(encoding="utf-8")
    if old not in source:
        raise SystemExit(f"{relative}: anchor not found: {old}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


def contract_file(tree, op):
    catalog = json.loads((tree / "standards/bcreq-manual-classes/catalog.json").read_text(encoding="utf-8"))
    return next(c for c in catalog["classes"] if c["id"] == op)


def edit_op_contract(tree):
    path = tree / "standards/bcreq-manual-classes/catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    op = next(c for c in data["classes"] if c["id"] == "К-24")
    op["checks"] = op["checks"] + " " + MARK
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


SCENARIOS = {
    # One published step prompt: what fixing a defect found in BA testing looks like for that step.
    "published_step_Ш-6": ("Ш-6: правка текста опубликованного промпта", lambda t: append(t, "prompts/bcreq-orr-solution-design-stepwise.md")),
    "by_test_source_Ш-1": ("Ш-1: правка источника шага в режиме by-test", lambda t: append(t, "prompts/bcreq-context-understanding-stepwise.md")),
    "operation_contract_К-24": ("К-24 (Ш-8): контракт операции в каталоге", edit_op_contract),
    "profile_VERIFY": ("Профиль VERIFY: новое правило в стандарте профилей", None),
    "base_standard": ("Базовый стандарт: новое правило", None),
    "runtime_slice": ("Срез runtime в реестре справочников", None),
    "section_standard_06": ("Мета-стандарт раздела 6", lambda t: append(t, "standards/bcreq-sections/06-implementation-constraints.md")),
    "new_module_prompt": ("Новый промпт следующего модуля (вне 13 шагов)", None),
    "shared_file_Ш-5_Ш-8": ("Общий файл Ш-5 и Ш-8", lambda t: append(t, "prompts/bcreq-uc-modeling-stepwise.md")),
    "card_text_Ш-8": ("Карточка Ш-8: текст подготовки или действий", None),
    "mode_switch_Ш-9": ("Смена режима Ш-9 на by-test", None),
}


def add_prompt(tree):
    (tree / "prompts/bcreq-next-module-experiment.md").write_text(
        "---\nid: mango-bcreq-next-module-experiment\ntitle: \"Заготовка следующего модуля\"\nstatus: draft\nversion: 0.1\n"
        "updated: 2026-11-05\ntemperature: 0.1\noperation: solution_design\nprocesses: [\"Дизайн решения и оценка\"]\n---\n\n"
        "# Заготовка\n\n" + MARK + "\n", encoding="utf-8")


def edit_rule_row(tree, relative, pattern):
    """Add the marker inside the rule cell of the first row matching pattern, so the builder carries it over."""
    path = tree / relative
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text)
    if not match:
        raise SystemExit(f"{relative}: no rule row")
    path.write_text(text[:match.end(1)] + " " + MARK + text[match.end(1):], encoding="utf-8")


def profile_edit(tree):
    edit_rule_row(tree, "standards/bcreq-prompt-profiles.md", r"(?m)^\| VE-\d\d \| (.+?) \| .+ \|$")


def base_edit(tree):
    spec = importlib.util.spec_from_file_location("builder", tree / "scripts/build_bcreq_step_prompts.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    excluded = set(builder.EXCLUDED_BASE)
    code = next(c for c in (f"БС-{n:02d}" for n in range(1, 40)) if c not in excluded)
    edit_rule_row(tree, "standards/bcreq-prompt-base-standard.md", rf"(?m)^\| {code} \| (.+) \| .+ \|$")


def slice_edit(tree):
    path = tree / "standards/bcreq-runtime-references.md"
    text = path.read_text(encoding="utf-8")
    sha = re.search(r"\b[0-9a-f]{40}\b", text).group(0)
    path.write_text(text.replace(sha, "0" * 40), encoding="utf-8")


def card_text_edit(tree):
    """Add one action to row 9 (Ш-8) of the card table the site generator reads."""
    path = tree / "docs/ba-processes/bcreq-run-kit.md"
    lines = path.read_text(encoding="utf-8").split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("| № | Этап | Зачем шаг"))
    row = next(i for i in range(start, len(lines)) if lines[i].startswith("| 9 | "))
    cells = lines[row].split(" | ")
    cells[4] = cells[4] + "; " + MARK
    lines[row] = " | ".join(cells)
    path.write_text("\n".join(lines), encoding="utf-8")


def mode_edit(tree):
    path = tree / "docs/ba-processes/bcreq-run-kit.md"
    lines = path.read_text(encoding="utf-8").split("\n")
    row = next(i for i, l in enumerate(lines) if l.startswith("|") and "Ш-9" in l and "`published`" in l)
    lines[row] = lines[row].replace("`published`", "`by-test`", 1)
    path.write_text("\n".join(lines), encoding="utf-8")


APPLY = {"profile_VERIFY": profile_edit, "base_standard": base_edit, "runtime_slice": slice_edit, "new_module_prompt": add_prompt,
         "card_text_Ш-8": card_text_edit, "mode_switch_Ш-9": mode_edit}


def compare(base, now):
    moved = {"main_button": [], "comparison_draft": [], "published": [], "card": [], "mode": []}
    for code, step in base["steps"].items():
        for key in moved:
            if now["steps"].get(code, {}).get(key) != step[key]:
                moved[key].append(code)
    other_changed = sorted(n for n in set(base["other_prompts"]) | set(now["other_prompts"]) if base["other_prompts"].get(n) != now["other_prompts"].get(n))
    return moved, other_changed


def main():
    work = Path(tempfile.mkdtemp(prefix="wt454-"))
    tree = work / "tree"
    run(["git", "worktree", "add", "--detach", "-q", str(tree), "HEAD"], ROOT)
    results = {}
    try:
        head = run(["git", "rev-parse", "HEAD"], tree).strip()
        base = build(tree)
        run(["git", "add", "-A"], tree)
        run(["git", "-c", "user.name=exp", "-c", "user.email=exp@example.invalid", "commit", "-q", "--allow-empty", "-m", "baseline"], tree)
        committed = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
        same = all(next(s for s in committed["steps"] if s["step"].split()[0] == code).get("mode") == step["mode"] for code, step in base["steps"].items())
        for name, (title, apply) in SCENARIOS.items():
            run(["git", "reset", "-q", "--hard"], tree)
            run(["git", "clean", "-qfd"], tree)
            (apply or APPLY[name])(tree)
            status = None
            try:
                now = build(tree)
                status = "built"
                moved, other = compare(base, now)
            except subprocess.CalledProcessError as error:
                status = "build_failed"
                moved, other = {}, []
                results[name] = {"title": title, "status": status, "error": (error.stderr or error.stdout)[-400:]}
                print(name, status, results[name]["error"][-200:])
                continue
            results[name] = {"title": title, "status": status, "moved": moved, "other_prompts_changed": other}
            print(name, {k: v for k, v in moved.items() if v}, "other:", other)
        facts = {"head": head, "modes_match_committed_kit": same, "baseline": base, "scenarios": results}
        OUT.write_text(json.dumps(facts, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    finally:
        run(["git", "worktree", "remove", "--force", str(tree)], ROOT)
        run(["git", "worktree", "prune"], ROOT)


if __name__ == "__main__":
    main()
