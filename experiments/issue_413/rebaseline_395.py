#!/usr/bin/env python3
"""Record intentional #413 changes to files frozen by the #395 site baseline.

`experiments/issue_395/site-baseline.json` is historical evidence and is not
edited. This script writes `experiments/issue_413/site-baseline-overrides.json`
with the current hashes of only the files and sections listed in CHANGES.
`scripts/test_issue_395_site.py` checks those against the override and
everything else against the original baseline.

Run after changing a listed file: python3 experiments/issue_413/rebaseline_395.py
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "experiments/issue_413/site-baseline-overrides.json"

FILES = {
    "standards/prompt-standard.md": "#413: раздел «Обобщение содержимого промпта», правила G1–G5",
    "standards/pages-ux-standard.md": "#413: раздел «Дорожная карта» описывает четыре этапа и запуск этапа 1",
    "site/styles.css": "#413: полоса этапов на дашборде из четырёх колонок, блок запуска этапа 1",
}
SECTIONS = {
    "dashboard": "#413: заголовок дашборда называет четыре этапа ADR-017 вместо «промптов, агентов и мультиагентов»",
    "roadmap": "#413: раздел показывает четыре этапа ADR-017 и запуск этапа 1 из docs/roadmap.md",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    html = (ROOT / "site/index.html").read_text()
    sections = {
        re.search(r'\bid="([^"]+)"', part).group(1): part
        for part in re.findall(r"<section\b.*?</section>", html, re.S)
    }
    data = {
        "source_issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/413",
        "base": "experiments/issue_395/site-baseline.json",
        "files": {
            name: {"sha256": sha((ROOT / name).read_bytes()), "reason": reason}
            for name, reason in FILES.items()
        },
        "sections": {
            name: {"sha256": sha(sections[name].encode()), "reason": reason}
            for name, reason in SECTIONS.items()
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
