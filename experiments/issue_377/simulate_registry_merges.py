#!/usr/bin/env python3
"""Replay historical merges of `main` into PR branches (issue #377, PR #380 comment).

For every merge commit reachable from REF (default: upstream/main) the script
re-runs the merge of its two parents with `git merge-tree` and lists the files
that conflicted. For the shared registries it then replays the conflicting
file with `scripts/resolve_registry_conflicts.py` logic (union of both sides +
ordered run table) and compares the multiset of non-blank lines with the resolution the
human/agent actually committed.

Output: experiments/issue_377/registry-merge-replay.json (deterministic).

Usage: python3 experiments/issue_377/simulate_registry_merges.py [REF]
"""
from __future__ import annotations

import collections
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import resolve_registry_conflicts as rrc  # noqa: E402

OUT = ROOT / "experiments" / "issue_377" / "registry-merge-replay.json"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check)


def blob(rev: str, path: str) -> str | None:
    res = git("show", f"{rev}:{path}", check=False)
    return res.stdout if res.returncode == 0 else None


def _content(text: str) -> collections.Counter:
    """Мультимножество непустых строк: порядок блоков и число пустых строк не важны."""
    return collections.Counter(line for line in text.splitlines() if line.strip())


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "upstream/main"
    merges = git("rev-list", "--merges", "--reverse", ref).stdout.split()
    rows = []
    file_counter: collections.Counter[str] = collections.Counter()
    replay = {"resolved": 0, "same_non_blank_lines_as_committed": 0, "refused": 0}
    for sha in merges:
        p1, p2 = f"{sha}^1", f"{sha}^2"
        res = git("merge-tree", "--write-tree", "--name-only", "--no-messages", p1, p2, check=False)
        if res.returncode != 1:
            continue
        files = [f for f in res.stdout.splitlines()[1:] if f]
        file_counter.update(files)
        base = git("merge-base", p1, p2).stdout.split()[0]
        entry = {
            "merge": sha[:8],
            "date": git("log", "-1", "--format=%cs", sha).stdout.strip(),
            "subject": git("log", "-1", "--format=%s", sha).stdout.strip(),
            "conflicted_files": files,
            "registry_replay": {},
        }
        for path in files:
            if path not in rrc.REGISTRIES:
                continue
            o, b, t = blob(p1, path), blob(base, path), blob(p2, path)
            committed = blob(sha, path)
            if None in (o, b, t, committed):
                continue
            try:
                merged = rrc.resolve_text(path, o, b, t)
            except rrc.UnresolvableConflict as exc:
                replay["refused"] += 1
                entry["registry_replay"][path] = f"refused: {exc}"
                continue
            replay["resolved"] += 1
            same = _content(merged) == _content(committed)
            if same:
                replay["same_non_blank_lines_as_committed"] += 1
            entry["registry_replay"][path] = "same non-blank lines as committed" if same else "differs from committed"
        rows.append(entry)
    report = {
        "ref": ref,
        "merge_commits": len(merges),
        "merges_with_conflicts": len(rows),
        "conflicts_by_file": dict(file_counter.most_common()),
        "registry_replay": replay,
        "merges": rows,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "merges"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
