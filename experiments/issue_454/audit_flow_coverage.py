#!/usr/bin/env python3
"""Issue #454: read-only per-step audit of the BCREQ flow: repository, site data, production.

Run from anywhere: python3 experiments/issue_454/audit_flow_coverage.py [--offline]
Prints a table and exits 1 on an integrity problem. A full run also writes
experiments/issue_454/audit_flow_coverage.json (facts); --offline checks the repository only and keeps that snapshot.
Touches neither gh-pages nor the password. Re-run after each deploy: the goal is met
for a step when prod_step_current is true: the production kit serves the same texts as main.
"""
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = "https://g-ivan-a.github.io/mango_ba_prompts/"
OUT = Path(__file__).with_name("audit_flow_coverage.json")
AGENT_ROUTE = {"bcreq-in-understanding-oneshot", "bcreq-core-documentation-oneshot", "bcreq-work-solution-design-oneshot"}
# Measured evidence per step: what a report in runs/ covers. Checked for existence below.
EVIDENCE = {
    "Ш-0": ["RUN-0083", "RUN-0087", "RUN-0088", "RUN-0089"], "Ш-1": ["RUN-0083", "RUN-0086", "RUN-0088", "RUN-0089"], "Ш-2": ["RUN-0083", "RUN-0088", "RUN-0089", "RUN-0092"],
    "Ш-3": ["RUN-0086", "RUN-0088", "RUN-0089"], "Ш-4": ["RUN-0088", "RUN-0089"], "Ш-5": ["RUN-0088", "RUN-0089", "RUN-0092"], "Ш-6": ["RUN-0086", "RUN-0088", "RUN-0089"], "Ш-7": ["RUN-0088", "RUN-0089"], "Ш-8": ["RUN-0088", "RUN-0089"], "Ш-9": ["RUN-0088", "RUN-0089"],
    "Ш-Р": ["RUN-0088", "RUN-0089", "RUN-0092"], "Ш-С": ["RUN-0088", "RUN-0089", "RUN-0092"],
    "Ш-В": ["RUN-0081", "RUN-0082", "RUN-0084", "RUN-0085", "RUN-0088", "RUN-0089", "RUN-0092"],
}
# Машинная база на реальных задачах: все шаги, кроме Ш-С; тексты комплекта 0.5 (kit_vs_machine_base.py).
for _code in EVIDENCE:
    if _code != "Ш-С":
        EVIDENCE[_code] += ["RUN-0090", "RUN-0091"]


def fetch(path):
    try:
        with urllib.request.urlopen(PROD + path, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def front(text, key):
    found = re.search(rf"(?m)^{key}: *\"?([^\"\n]+)\"?$", text.split("\n---", 1)[0])
    return found.group(1).strip() if found else None


def text_ids(step):
    """What a kit card serves: the hashes of its assigned and comparison texts, and its mode."""
    return (step["mode"], (step.get("published") or {}).get("sha256"), (step.get("draft") or {}).get("sha256"))


def active_stubs(text):
    """Stub codes a draft really carries: the base-standard rule БС-21 only lists them all."""
    return sorted({code for line in text.splitlines() if "БС-21" not in line for code in re.findall(r"З-\d", line)})


def main():
    offline = "--offline" in sys.argv
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "site/data/prompts.json").read_text(encoding="utf-8"))
    by_file = {Path(p["sourcePath"]).name: p for p in catalog["prompts"] if p.get("sourcePath")}
    registry = (ROOT / "standards/bcreq-runtime-references.md").read_text(encoding="utf-8")
    slice_sha = re.search(r"\b[0-9a-f]{40}\b", registry).group(0)
    prod_kit = prod_prompts = None
    if not offline:
        raw = fetch("data/test-kit.json")
        prod_kit = json.loads(raw) if raw else None
        prod_prompts = {Path(p["sourcePath"]).name: p for p in json.loads(fetch("data/prompts.json"))["prompts"] if p.get("sourcePath")}
    rows = []
    for step in kit["steps"]:
        published, draft = step.get("published"), step.get("draft")
        name = (published or draft)["file"]
        file_path = ROOT / "prompts" / name
        draft_path = ROOT / draft["sourcePath"] if draft else None
        draft_text = draft_path.read_text(encoding="utf-8") if draft_path else ""
        item = by_file.get(name)
        code = step["step"].split()[0]
        prod_item = (prod_prompts or {}).get(name)
        prod_step = next((s for s in (prod_kit or {}).get("steps", []) if s["step"] == step["step"]), None)
        rows.append({
            "step": code, "title": step["step"], "group": step["group"], "gate": step["gate"], "mode": step["mode"], "file": name,
            "main_published_exists": file_path.is_file(),
            "main_version": published["version"] if published else None,
            "published_sha_ok": bool(published) and sha(file_path) == published["sha256"],
            "catalog_has_text": bool(item and item.get("body")),
            "catalog_archived": bool(item and item.get("archived")),
            "draft_on_site": bool(draft and draft.get("body")),
            "draft_version": front(draft_text, "version"),
            "draft_based_on_current": (not published) or bool(draft) and draft.get("basedOnSha256") == published["sha256"],
            "draft_sha_ok": bool(draft) and sha(draft_path) == draft["sha256"],
            "draft_runtime_is_registry_slice": front(draft_text, "runtime_sha") == slice_sha,
            "active_stubs": active_stubs(draft_text),
            "evidence": [r for r in EVIDENCE.get(code, []) if (ROOT / "runs/2026" / r).is_dir()],
            "prod_version": str(prod_item["version"]) if prod_item else None,
            "prod_text_same_as_main": bool(prod_item and item and prod_item.get("body") == item.get("body")),
            "prod_kit": bool(prod_kit),
            "prod_step_current": bool(prod_step) and text_ids(prod_step) == text_ids(step)
            and (not published or bool(prod_item and item and prod_item.get("body") == item.get("body"))),
        })
    files = {r["file"] for r in rows}
    facts = {
        "runtime_slice": slice_sha,
        "kit_version": kit["kit"]["version"],
        "counts": kit["counts"],
        "steps": rows,
        "unique_prompt_files": len(files),
        "agent_route_excluded": sorted(Path(p["sourcePath"]).stem for p in catalog["prompts"]
                                       if p.get("sourcePath") and Path(p["sourcePath"]).stem in AGENT_ROUTE),
        "catalog_step_prompts_marked_archive": sum(1 for p in catalog["prompts"] if p.get("archived")),
        "prod": None if offline else {
            "kit_available": bool(prod_kit),
            "prompts": len(prod_prompts),
            "steps_current": sum(1 for r in rows if r["prod_step_current"]),
            "steps_total": len(rows),
            "catalog_texts_same_as_main": sum(1 for r in rows if r["prod_text_same_as_main"]),
        },
    }
    if not offline:
        OUT.write_text(json.dumps(facts, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"slice {slice_sha}; kit {facts['kit_version']}; {kit['counts']}; files {len(files)}; archive {facts['catalog_step_prompts_marked_archive']}")
    print("step | mode | main | prod | same_text | archived | draft | stubs | evidence")
    for r in rows:
        print(" | ".join(str(x) for x in (r["step"], r["mode"], r["main_version"], r["prod_version"], r["prod_text_same_as_main"],
                                         r["catalog_archived"], r["draft_on_site"], ",".join(r["active_stubs"]) or "-",
                                         ",".join(r["evidence"]) or "-")))
    print("prod:", facts["prod"])
    bad = [r["step"] for r in rows if not (r["draft_sha_ok"] and r["draft_based_on_current"] and r["draft_runtime_is_registry_slice"]
                                           and (r["published_sha_ok"] or r["main_version"] is None))]
    print("integrity problems:", bad or "none")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
