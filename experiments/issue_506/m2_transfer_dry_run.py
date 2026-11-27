#!/usr/bin/env python3
"""Issue #506, M2: пробная передача SSOT этапа 1 в runtime без публикации.

Что делает (ничего не пушит, спица и клон runtime не меняются):

1. создаёт отсоединённый git worktree клона runtime на ``origin/main``;
2. до копии — прогоняет ``python3 -m unittest discover -s tests`` runtime;
3. копирует 135 артефактов манифеста 0.2 побайтно с ``source_commit`` спицы в
   ``ssot/mango_ba_prompts/<путь в спице>``; рядом — копии манифеста и карты
   ссылок и журнал ``ssot/TRANSFERS.md`` (раскладка раздела 12 RFC-RT-003);
4. сверяет sha256 каждой копии с манифестом; набор файлов каталога копии равен
   набору манифеста; порча одного байта ловится (отрицательная проверка);
5. проверяет согласованность карты гейтов: её ``sources`` совпадают по sha256
   с артефактами передачи, ``runtime_path`` указывает в каталог копии;
6. считает совпадения шаблонов персональных данных (почта, телефон),
   секретов и внутреннего контура (корпоративные хосты, локальные домены,
   частные IP) в переносимых байтах — только пути и счёт, без содержимого:
   runtime публичен, перенос публикует байты;
7. после копии — тесты runtime и ``tests/runtime-smoke.sh``; отдельно —
   ``test_ide_layer`` с проверкой, что ``test_map_matches_the_layer`` не
   пропущен;
8. удаляет worktree.

Запуск::

    RUNTIME_CLONE=/путь/к/клону python3 -I experiments/issue_506/m2_transfer_dry_run.py \
        > experiments/issue_506/m2-transfer-dry-run.log 2>&1
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.json"
LINK_MAP = ROOT / "docs/contracts/ssot-stage1-link-map.json"
EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(rb"(?<![\d.])(?:\+7|8)[\s(-]*\d{3}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)")
SECRET = re.compile(rb"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")
# Внутренний контур: корпоративные хосты, локальные домены, частные адреса.
INTERNAL = re.compile(rb"https?://[^\s)>\]]*(?:jira|confluence|wiki|gitlab|corp|intra)[^\s)>\]]*"
                      rb"|\b[\w-]+\.(?:local|lan|corp|internal)\b"
                      rb"|\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d+\.\d+(?:\.\d+)?\b")
KINDS = (("почта", EMAIL), ("телефон", PHONE), ("секрет", SECRET), ("внутренний контур", INTERNAL))


def run(cmd: list[str], cwd: Path, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)


def tail(text: str, n: int = 4) -> str:
    return "\n".join("    " + line for line in text.strip().splitlines()[-n:])


def show(commit: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True,
                          capture_output=True).stdout


def unittest_all(wt: Path, label: str) -> bool:
    res = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], wt)
    print(f"[{label}] unittest runtime: rc={res.returncode}\n{tail(res.stderr)}")
    return res.returncode == 0


def main() -> int:
    clone = Path(os.environ.get("RUNTIME_CLONE", "/tmp/rt")).resolve()
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    commit, target_dir, t = m["source_commit"], m["transfer"]["target_dir"], m["transfer"]
    runtime_main = run(["git", "rev-parse", "origin/main"], clone).stdout.strip()
    print(f"манифест {m['version']}: {m['summary']['artifacts']} артефактов, source_commit={commit}")
    print(f"runtime origin/main={runtime_main}")
    failures = []

    tmp = Path(tempfile.mkdtemp(prefix="m2-dry-"))
    wt = tmp / "rt"
    run(["git", "worktree", "add", "--detach", str(wt), runtime_main], clone, check=True)
    try:
        print("\n## До копии")
        print(f"ssot/ в runtime: {'есть' if (wt / 'ssot').exists() else 'нет'}")
        if not unittest_all(wt, "до"):
            failures.append("тесты runtime падают до копии")

        print("\n## Копия")
        dest = wt / target_dir
        for a in m["artifacts"]:
            data = show(commit, a["path"])
            out = dest / a["path"]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        shutil.copyfile(MANIFEST, wt / t["manifest_copy"])
        shutil.copyfile(LINK_MAP, wt / t["link_map_copy"])
        (wt / t["journal"]).write_text(
            "# Журнал передач SSOT (пробный, не публикуется)\n\n"
            "| № | Источник | source_commit | Манифест | Артефактов | Карточки |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            f"| {t['number']} | {m['source_repository']} | `{commit}` | {m['version']} | "
            f"{m['summary']['artifacts']} | {', '.join(t['cards'])} |\n", encoding="utf-8")

        copied = {p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file()}
        expected = {a["path"] for a in m["artifacts"]}
        print(f"файлов в {target_dir}: {len(copied)}; в манифесте: {len(expected)}; "
              f"лишних: {len(copied - expected)}; недостающих: {len(expected - copied)}")
        if copied != expected:
            failures.append("набор файлов копии не равен манифесту")
        bad = [a["path"] for a in m["artifacts"]
               if hashlib.sha256((dest / a["path"]).read_bytes()).hexdigest() != a["sha256"]]
        print(f"сверка sha256: совпало {len(expected) - len(bad)} из {len(expected)}")
        if bad:
            failures.append(f"sha256 не совпал: {bad}")

        probe = dest / m["artifacts"][0]["path"]
        original = probe.read_bytes()
        probe.write_bytes(original + b"\n")
        caught = hashlib.sha256(probe.read_bytes()).hexdigest() != m["artifacts"][0]["sha256"]
        probe.write_bytes(original)
        print(f"отрицательная проверка (лишний байт в {m['artifacts'][0]['path']}): "
              f"{'поймана' if caught else 'НЕ поймана'}")
        if not caught:
            failures.append("порча байта не поймана")

        gates = json.loads((dest / "docs/ba-processes/bcreq-ide-gates.json").read_text(encoding="utf-8"))
        by_path = {a["path"]: a["sha256"] for a in m["artifacts"]}
        mism = [p for p, h in gates["sources"].items() if by_path.get(p) != h]
        print(f"карта гейтов {gates['version']} ({gates['status']}): источников {len(gates['sources'])}, "
              f"не совпало с передачей: {len(mism)}; runtime_path в каталоге копии: "
              f"{gates['runtime_path'].startswith(target_dir)}")
        if mism or not gates["runtime_path"].startswith(target_dir):
            failures.append(f"карта гейтов расходится с передачей: {mism}")

        print("\n## Публикация: шаблоны персональных данных и секретов в переносимых байтах")
        hits = {}
        for a in m["artifacts"]:
            data = (dest / a["path"]).read_bytes()
            found = {k: len(rx.findall(data)) for k, rx in KINDS}
            if any(found.values()):
                hits[a["path"]] = found
        total = {k: sum(h[k] for h in hits.values()) for k, _ in KINDS}
        print(f"файлов с совпадениями: {len(hits)}; всего: {total}")
        size = sum((dest / a["path"]).stat().st_size for a in m["artifacts"])
        crlf = sum(b"\r\n" in (dest / a["path"]).read_bytes() for a in m["artifacts"])
        print(f"объём передачи: {size} байт; файлов с CRLF: {crlf}")
        for path, found in sorted(hits.items()):
            print(f"  {path}: {found}")
        print("  (совпадение шаблона — кандидат на ручной просмотр перед публикацией, не вывод о данных)")

        print("\n## После копии")
        if not unittest_all(wt, "после"):
            failures.append("тесты runtime падают после копии")
        res = run([sys.executable, "-m", "unittest", "-v", "tests.test_ide_layer"], wt)
        line = next((ln for ln in res.stderr.splitlines() if "test_map_matches_the_layer" in ln), "")
        print(f"test_ide_layer: rc={res.returncode}; {line.strip()}")
        if res.returncode or "ok" not in line or "skipped" in line:
            failures.append("test_map_matches_the_layer не прошёл или пропущен")
        res = run(["bash", "tests/runtime-smoke.sh"], wt)
        print(f"runtime-smoke.sh: rc={res.returncode}\n{tail(res.stdout + res.stderr, 2)}")
        if res.returncode:
            failures.append("runtime-smoke.sh падает после копии")
        status = run(["git", "status", "--porcelain", "--untracked-files=normal"], wt).stdout.splitlines()
        print(f"git status worktree: {len(status)} записей, все внутри ssot/: "
              f"{all(s[3:].startswith('ssot/') for s in status)}")
        if not all(s[3:].startswith("ssot/") for s in status):
            failures.append("копия меняет файлы вне ssot/")
    finally:
        run(["git", "worktree", "remove", "--force", str(wt)], clone)
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\nworktree удалён; клон runtime: {run(['git', 'status', '--short'], clone).stdout.strip() or 'чист'}")

    print("\nИТОГ:", "OK" if not failures else "FAIL")
    for f in failures:
        print("  -", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
