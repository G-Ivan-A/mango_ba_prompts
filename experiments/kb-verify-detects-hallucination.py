#!/usr/bin/env python3
"""Проверка, что детектор галлюцинаций из issue #310 действительно ловит вымысел.

На реальном прогоне (issue #310) перекрёстная проверка дала 0 неподтверждённых
токенов — то есть pdfplumber и PyMuPDF согласны по всем четырём документам.
Само по себе «0 находок» не доказывает, что механизм работает: он мог бы
молчать и на подделке. Этот эксперимент — negative test: в копию раздела БЗ
подставляются вымышленные функциональные значения (несуществующий параметр
API, лимит и URL), после чего проверка обязана их пометить.

Запуск (исходные PDF должны лежать в kb/sources/, см. README задачи):

    python3 experiments/kb-verify-detects-hallucination.py

Exit code 0 = детектор поймал вымысел и не тронул подлинные значения.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "kb"))

import verify_extraction as V  # noqa: E402

DOC = ROOT / "kb" / "processed" / "lk-vats-sso"

# Вымышленные значения: таких строк в исходном PDF нет.
FABRICATED = [
    "max_parallel_sso_sessions",          # несуществующий параметр
    "https://sso.example-not-in-pdf.tld", # несуществующий URL
    "987654",                             # несуществующий числовой лимит
    "Zzyzxprovider",                      # несуществующее имя сущности
]


def main() -> int:
    meta = json.loads((DOC / "meta.json").read_text(encoding="utf-8"))
    source_pdfs = meta["source_pdfs"]
    for rel in source_pdfs:
        if not (ROOT / rel).exists():
            print(f"SKIP: нет исходного PDF {rel} — эксперимент требует локальной копии")
            return 0

    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp) / DOC.name
        shutil.copytree(DOC, sandbox)

        target = meta["sections"][-1]
        section_path = sandbox / target["file"]
        text = V.strip_verify_blocks(section_path.read_text(encoding="utf-8"))
        injected = (
            "\n\nПри настройке провайдера задаётся "
            f"`{FABRICATED[0]}` = {FABRICATED[2]}, адрес метаданных — "
            f"{FABRICATED[1]}, провайдер {FABRICATED[3]}.\n"
        )
        section_path.write_text(text.rstrip("\n") + injected, encoding="utf-8")

        report = V.verify_doc(sandbox, "2026-08-22")

    flagged: set[str] = set()
    for section in report["sections"]:
        flagged.update(section["unconfirmed"])

    missed = [value for value in FABRICATED if value not in flagged]
    genuine = {"Keycloak", "SAML", "SSO"} & flagged

    print(f"помечено неподтверждённых токенов: {len(flagged)}")
    print(f"из них вымышленных пойманo: {len(FABRICATED) - len(missed)}/{len(FABRICATED)}")

    if missed:
        print(f"FAIL: детектор пропустил вымысел: {', '.join(missed)}")
        return 1
    if genuine:
        print(f"FAIL: ложное срабатывание на подлинных значениях: {', '.join(sorted(genuine))}")
        return 1
    print("PASS: вымышленные значения помечены, подлинные — нет")
    return 0


if __name__ == "__main__":
    sys.exit(main())
