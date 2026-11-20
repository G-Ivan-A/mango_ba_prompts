#!/usr/bin/env python3
"""Защищённые маркеры базы для сторожа сверхчистки (issue #495, комментарий 2, раздел 3).

Считает в базе ``e051e0fa`` маркеры раздела 4 стандарта чистоты (ID правил,
``[ТРЕБУЕТСЯ УТОЧНЕНИЕ]``, ACCESS_GAP, «Состояние BCREQ», «Пакет памяти
проекта», «КОНЕЦ <ID>», «Итог шага», «На согласование БА», «Промпт ДОЛЖЕН»,
receipt, стоп-краны) по каждому промпту и черновику и пишет снимок
``audit/protected-baseline.json``. Валидатор #495 сверяет с ним рабочее дерево:
маркеров не меньше, чем в базе. Снимок нужен, чтобы сторож работал без истории
git. Политика (шаблоны, контур, исключённые ID) берётся из рабочего дерева.

    python3 experiments/issue_495/protected_baseline.py [--base-root ПУТЬ] [--check]

Скрипт ничего не меняет вне ``audit/protected-baseline.json`` и не вызывает LLM.
"""
import argparse
import glob
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import map_baseline as mb  # noqa: E402
import prompt_purity  # noqa: E402

OUT = HERE / "audit" / "protected-baseline.json"


def settings(root=ROOT):
    policy = json.loads((root / "standards/bcreq-prompt-purity.json").read_text(encoding="utf-8"))
    spec = policy["protected_markers"]
    rel, key = spec["exempt_ids_from"].split("#")
    exempt = sorted(json.loads((root / rel).read_text(encoding="utf-8"))[key])
    return spec, exempt


def files(root, spec):
    out = set()
    for pattern in spec["files"]:
        out |= {Path(p).relative_to(root).as_posix() for p in glob.glob(str(root / pattern), recursive=True)}
    return sorted(out)


def counts(root, spec, exempt):
    return {rel: prompt_purity.protected_counts((root / rel).read_text(encoding="utf-8"), spec["patterns"], exempt)
            for rel in files(root, spec)}


def snapshot(base_root):
    spec, exempt = settings()
    return {"base": mb.BASE, "exempt_ids": exempt, "files": counts(base_root, spec, exempt)}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-root")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        base_root = Path(args.base_root) if args.base_root else Path(tmp)
        if not args.base_root:
            mb.export_base(base_root)
        data = snapshot(base_root)
        text = json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if args.check:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print("OK: снимок актуален" if ok else "ERROR: снимок устарел — перезапустите без --check")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    print(f"записано: {OUT.relative_to(ROOT)} — файлов {len(data['files'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
