#!/usr/bin/env python3
"""Проба правила A-SPOKE-PATH (голые пути спицы в теле живого промпта) на дереве или базе.

Перед включением правила в аудитор показывает, что оно ловит: регулярное
выражение берётся из политики рабочего дерева (``links.spoke_path_regex``),
контур — ``prompt_texts`` указанного корня, frontmatter не проверяется.

    python3 experiments/issue_495/probe_spoke_paths.py [КОРЕНЬ]

Скрипт ничего не меняет и не вызывает LLM.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_prompt_purity as audit  # noqa: E402

POLICY = audit.load_policy(ROOT / "standards/bcreq-prompt-purity.json")
RX = re.compile(POLICY["links"]["spoke_path_regex"])


def probe(root):
    au = audit.Auditor(Path(root), POLICY)
    au.run()
    c, out = Counter(), []
    for rel, kind in sorted(au.files.items()):
        if kind != "prompt_texts":
            continue
        text = (Path(root) / rel).read_text(encoding="utf-8")
        fm, _ = audit.split_frontmatter(text)
        for no, line in enumerate(text.splitlines(), 1):
            if no <= fm:
                continue
            for m in RX.finditer(line):
                c[m.group(0)] += 1
                out.append(f"{rel}:{no}: {m.group(0)}")
    return c, out


if __name__ == "__main__":
    counts, lines = probe(sys.argv[1] if len(sys.argv) > 1 else ROOT)
    print("\n".join(lines))
    print(sum(counts.values()), counts.most_common(30))
