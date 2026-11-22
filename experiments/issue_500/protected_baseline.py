#!/usr/bin/env python3
"""Record and verify protected markers at the post-#497 revision."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "e89a6dea73ddeb27aa824cc2ca8c64fcf4d5ef3c"
OUT = HERE / "protected-baseline.json"
POLICY = "standards/bcreq-prompt-purity.json"
MARKERS = (
    "Итог шага", "На согласование БА", "Проверки (receipt)", "Состояние BCREQ",
    "ACCESS_GAP", "[ТРЕБУЕТСЯ УТОЧНЕНИЕ]",
)
RULE = re.compile(r"(?<![\w-])(?:Р-?\d+|АД-\d+|БС-?\d+|КС-?\d+)(?!\w)")
END = re.compile(r"КОНЕЦ AIN-\d{2} (?:<[^>\n]+>|v?\d+(?:\.\d+)*)")


def read_json(root, relative):
    return json.loads((root / relative).read_text(encoding="utf-8"))


def counts(text):
    result = Counter(RULE.findall(text))
    result.update(END.findall(text))
    result.update({marker: text.count(marker) for marker in MARKERS if marker in text})
    return dict(result)


def snapshot(root):
    policy = read_json(root, POLICY)
    sources = {}
    for scope in ("prompt_texts", "archive_texts", "ssot_texts"):
        config = policy["contour"].get(scope, {})
        for pattern in config.get("globs", []):
            for candidate in root.glob(pattern):
                relative = candidate.relative_to(root).as_posix()
                if relative not in config.get("exclude", []):
                    sources[relative] = counts(candidate.read_text(encoding="utf-8"))

    projections = {}
    for prompt in read_json(root, "site/data/prompts.json")["prompts"]:
        for field in ("body", "content"):
            projections[f"prompts.json:{prompt['id']}:{field}"] = counts(prompt[field])
    for step in read_json(root, "site/data/test-kit.json")["steps"]:
        code = step["step"].split()[0]
        for kind in ("draft", "system"):
            if step[kind]:
                projections[f"test-kit.json:{code}:{kind}:{step[kind]['id']}"] = counts(step[kind]["body"])
        if step["handoffBlock"]:
            projections[f"test-kit.json:{code}:handoffBlock"] = counts(step["handoffBlock"])
    for step in read_json(root, "site/data/a-in-kit.json")["steps"]:
        projections[f"a-in-kit.json:{step['id']}"] = counts(step["prompt"])
    for code, step in read_json(root, "site/data/step-handoff.json")["steps"].items():
        projections[f"step-handoff.json:{code}"] = counts(step["block"])
    return {
        "base": BASE,
        "policy_ids": sorted(rule["id"] for group in ("case_tokens", "ballast_patterns") for rule in policy[group]),
        "sources": sources,
        "projections": projections,
    }


def regressions(base, current):
    errors = []
    for rule in sorted(set(base["policy_ids"]) - set(current["policy_ids"])):
        errors.append(f"{POLICY}: отсутствует {rule}")
    for section in ("sources", "projections"):
        for key, before in base[section].items():
            after = current[section].get(key)
            if after is None:
                errors.append(f"{key}: редакция отсутствует")
                continue
            for marker, minimum in before.items():
                if after.get(marker, 0) < minimum:
                    errors.append(f"{key}: {marker}: {after.get(marker, 0)} < {minimum}")
    return errors


def reference_snapshot():
    with tempfile.TemporaryDirectory(prefix="bl231-baseline-") as tmp:
        paths = [
            "prompts", "standards/bcreq-manual-classes", POLICY,
            "site/data", "docs/ba-processes",
        ]
        with subprocess.Popen(["git", "archive", BASE, *paths], cwd=ROOT, stdout=subprocess.PIPE) as archive:
            subprocess.run(["tar", "-x", "-C", tmp], stdin=archive.stdout, check=True)
            if archive.wait():
                raise SystemExit("git archive завершился с ошибкой")
        return snapshot(Path(tmp))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    reference = reference_snapshot()
    serialized = json.dumps(reference, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    if not args.check:
        OUT.write_text(serialized, encoding="utf-8")
        return
    if OUT.read_text(encoding="utf-8") != serialized:
        raise SystemExit(f"{OUT.name} отличается от закреплённого среза {BASE}")
    errors = regressions(reference, snapshot(ROOT))
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK post-#497: {len(reference['sources'])} исходников, "
          f"{len(reference['projections'])} проекций, {len(reference['policy_ids'])} CT/BP")


if __name__ == "__main__":
    main()
