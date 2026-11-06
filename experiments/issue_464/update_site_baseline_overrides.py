#!/usr/bin/env python3
"""Issue #464: обновить закреплённые хэши файлов, которые issue меняет намеренно.

Эталон #395 не трогаем: отклонения записываются в overrides #413 с причиной. Файл попадает
сюда, только если он есть в эталоне и изменён в ветке относительно слияния с main,
иначе случайная правка не получила бы прикрытие. Запускать после всех правок документов.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = json.loads((ROOT / "experiments/issue_395/site-baseline.json").read_text(encoding="utf-8"))
PATH = ROOT / "experiments/issue_413/site-baseline-overrides.json"
REASON = "#464: корректировки стандартов и A-IN по замечаниям владельца (комплект 0.8, сайт 2.7.0)"


def changed():
    base = subprocess.run(["git", "merge-base", "HEAD", "upstream/main"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    out = subprocess.run(["git", "diff", "--name-only", base], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return set(out.split())


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    touched = changed()
    for name in BASE["files"]:
        file = ROOT / name
        if not file.exists() or name not in touched:
            continue
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        known = data["files"].get(name, {}).get("sha256", BASE["files"][name])
        if digest == known:
            continue
        reason = data["files"].get(name, {}).get("reason", "")
        reason = reason if REASON in reason else (f"{reason}; {REASON}" if reason else REASON)
        data["files"][name] = {"sha256": digest, "reason": reason}
        print("закреплён:", name)
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
