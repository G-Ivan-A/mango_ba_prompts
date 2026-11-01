"""Проверка внешних цитат бэклога issue #418 через gh.

Цитаты из репозитория проверяет scripts/validate_issue_418_backlog.py.
Здесь — источники вне репозитория: файлы Хаба и PR #419 на закреплённом
коммите (ищется в разделе по якорю), тела issue и PR.

    python3 experiments/issue_418/check_external_quotes.py
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("v", ROOT / "scripts/validate_issue_418_backlog.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

BLOB = re.compile(r"^https://github\.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/([^#]+)(?:#(.*))?$")
ISSUE = re.compile(r"^https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)")
CACHE = {}


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def fetch_blob(repo, sha, path):
    key = (repo, sha, path)
    if key not in CACHE:
        CACHE[key] = gh("api", "-H", "Accept: application/vnd.github.raw",
                        f"repos/{repo}/contents/{path}?ref={sha}")
    return CACHE[key]


def fetch_thread(repo, kind, number):
    key = (repo, kind, number)
    if key not in CACHE:
        data = json.loads(gh("issue" if kind == "issues" else "pr", "view", number,
                             "--repo", repo, "--json", "body,comments"))
        CACHE[key] = data["body"] + "\n" + "\n".join(c["body"] for c in data["comments"])
    return CACHE[key]


def main():
    checked = failed = 0
    tmp = Path(tempfile.mkdtemp())
    for path in v.CARD_FILES:
        for task, chunks in v.cards(path).items():
            for line in v.source_lines(chunks[0]):
                links = v.LINK_RE.findall(line)
                quote = v.QUOTE_RE.findall(line)
                if not links or not quote:
                    continue
                url, quote = links[0][1], quote[0]
                blob, issue = BLOB.match(url), ISSUE.match(url)
                if blob:
                    repo, sha, file, anchor = blob.groups()
                    local = tmp / f"{sha[:8]}-{Path(file).name}"
                    local.write_text(fetch_blob(repo, sha, file), encoding="utf-8")
                    haystack = v.section(local, anchor) if anchor else v.text(local)
                    where = f"{repo}@{sha[:8]}/{file}#{anchor or ''}"
                elif issue:
                    repo, kind, number = issue.groups()
                    haystack = fetch_thread(repo, kind, number)
                    where = f"{repo} {kind} #{number}"
                else:
                    continue
                checked += 1
                ok = v.normalize(quote) in v.normalize(haystack)
                if blob and anchor and anchor not in v.anchors(local):
                    ok, where = False, where + " (якорь не найден)"
                failed += not ok
                print(f"{'OK  ' if ok else 'MISS'} {task} {where}: “{quote}”")
    print(f"итог: проверено {checked}, не найдено {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
