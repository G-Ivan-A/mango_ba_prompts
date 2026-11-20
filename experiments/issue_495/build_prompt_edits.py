#!/usr/bin/env python3
"""Реестр обратимых правок промптов issue #495 (``prompt-edits.json``).

Регрессии сохранности прошлых задач (#391, #393, #395, #438, #446, #448, #450,
#464, #474, #476) сверяют байты промптов с эталонами замеров. Issue #495
меняет тексты (приватные ссылки, HTML-комментарии, кейс-лексика, балласт), поэтому
в цепочку откатов (``experiments/issue_474/prompt_changes.py`` и далее) добавлен
слой: ``prompt_changes.revert`` снимает сначала #488, затем #495. Правка вне
реестра после отката остаётся, и старая регрессия падает — тихая правка промпта
по-прежнему невозможна.

Ханки строятся по строкам (difflib) между срезом до #488 и рабочим деревом
после снятия #488. Для каждого файла проверяется точный обратный переход.

Запуск: ``python3 experiments/issue_495/build_prompt_edits.py`` (запись) или
``--check`` (сверка без записи). LLM не вызывается.
"""
import argparse
import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("prompt-edits.json")
#: База побайтовых регрессий до #488. База аудита задаётся в map_baseline.py.
PRE_RELEASE = "e051e0fa46e22c43004a6af19e8c53b827ce1b1d"
#: Пути, чьи байты сверяют прошлые регрессии.
SCOPE = ["prompts"]

sys.path.insert(0, str(Path(__file__).parent))
from prompt_changes import RELEASE, apply_hunks  # noqa: E402


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def hunks(before, after, context):
    a, b = before.splitlines(keepends=True), after.splitlines(keepends=True)
    out, prev = [], 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        # Контекст — только из неизменённых строк после предыдущего ханка.
        lo = max(prev, j1 - context)
        lead = i1 - (j1 - lo)
        tail = 1 if lo == j1 == j2 else 0  # удаление в начале: контекст — следующая строка
        out.append({"before": "".join(a[lead:i2 + tail]), "after": "".join(b[lo:j2 + tail])})
        prev = j2 + tail
    # Пустой «after» (удаление в начале файла без контекста) искать нельзя.
    if any(not h["after"] for h in out):
        return None
    return out


def build():
    files = {}
    names = git("diff", "--name-only", PRE_RELEASE, "--", *SCOPE).split()
    for rel in sorted(names):
        path = ROOT / rel
        if not path.exists():
            continue
        before = git("show", f"{PRE_RELEASE}:{rel}")
        after = RELEASE.revert(rel, path.read_text(encoding="utf-8"))
        if after == before:
            continue
        for context in range(1, 8):
            hs = hunks(before, after, context)
            if hs is not None and apply_hunks(after, hs) == before:
                break
        else:
            raise SystemExit(f"{rel}: не удалось построить однозначные ханки")
        files[rel] = {"sha256_before": sha(before), "sha256_after": sha(after), "hunks": hs}
    return {"issue": 495, "base": PRE_RELEASE, "scope": SCOPE, "revert_order": [488, 495],
            "note": "Ханки #495 применяются к тексту после снятия #488.",
            "files": files}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    data = json.dumps(build(), ensure_ascii=False, indent=1) + "\n"
    if args.check:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == data
        print("OK: prompt-edits.json актуален" if ok else "устарел: prompt-edits.json")
        return 0 if ok else 1
    OUT.write_text(data, encoding="utf-8")
    print(f"записано: {OUT.relative_to(ROOT)} — {len(json.loads(data)['files'])} файлов")
    return 0


if __name__ == "__main__":
    sys.exit(main())
