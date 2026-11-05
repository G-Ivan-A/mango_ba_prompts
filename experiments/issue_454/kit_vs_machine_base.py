#!/usr/bin/env python3
"""Какие тексты основной кнопки комплекта совпадают с машинной базой RUN-0090, RUN-0091.

База снята на коммите prompt_set.commit и записана по SHA-256 в metadata.yaml. Сравнивается
файл, который основная кнопка берёт в этой ветке (черновик при by-test, иначе опубликованный),
и файл базы на её коммите. Кнопка прода сверяется по хешам test-kit.json в upstream/gh-pages
(нужен `git fetch upstream`).
"""
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]


def show(commit, path):
    done = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
    return done.stdout if done.returncode == 0 else None


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def main():
    meta = (ROOT / "runs/2026/RUN-0090/metadata.yaml").read_text(encoding="utf-8")
    commit = re.search(r"(?m)^  commit: (\S+)$", meta).group(1)
    pins = {s: (p, d) for s, p, d in re.findall(r'step: (\S+), path: (\S+), version: "[^"]+", sha256: (\w+)', meta)}
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))
    prod_kit = json.loads(show("upstream/gh-pages", "data/test-kit.json"))
    prod_steps = {s["step"].split()[0]: s for s in prod_kit["steps"]}
    rows = []
    for step in kit["steps"]:
        code = step["step"].split()[0]
        directory = "prompts/drafts" if step["mode"] == "by-test" else "prompts"
        name = (step["draft"] if step["mode"] == "by-test" else step["published"])["file"]
        path = f"{directory}/{name}"
        current = digest((ROOT / path).read_bytes())
        pin = pins.get(code)
        prod = prod_steps.get(code)
        prod_hash = (prod["draft"] if prod["mode"] == "by-test" else prod["published"])["sha256"] if prod else None
        rows.append(
            {
                "step": code,
                "kit_mode": step["mode"],
                "kit_path": path,
                "base_path": pin[0] if pin else None,
                "same_as_base": (pin[1] == current) if pin else None,
                "prod_mode": prod["mode"] if prod else None,
                "prod_same_as_base": (pin[1] == prod_hash) if pin and prod else None,
                "pin_verified_at_commit": (digest(show(commit, pin[0])) == pin[1]) if pin else None,
            }
        )
    in_base = [r for r in rows if r["same_as_base"] is not None]
    result = {
        "base_commit": commit,
        "kit": kit["kit"]["version"],
        "steps_in_base": len(in_base),
        "same": [r["step"] for r in in_base if r["same_as_base"]],
        "different": [r["step"] for r in in_base if not r["same_as_base"]],
        "not_in_base": [r["step"] for r in rows if r["same_as_base"] is None],
        "prod_kit": prod_kit["kit"]["version"],
        "prod_same": [r["step"] for r in in_base if r["prod_same_as_base"]],
        "prod_different": [r["step"] for r in in_base if not r["prod_same_as_base"]],
        "rows": rows,
    }
    out = pathlib.Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
