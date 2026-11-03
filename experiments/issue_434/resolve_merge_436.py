"""Resolve merge conflicts of issue-434 branch with upstream/main after PR #436 (issue #433).

Both sides are kept: upstream adds Р-16, BL-160…BL-162; this branch adds Р-17, BL-163.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
PAT = re.compile(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> upstream/main\n", re.S)


def resolve(path, resolver):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    idx = [0]

    def sub(m):
        i = idx[0]
        idx[0] += 1
        return resolver(i, m.group(1), m.group(2))

    new = PAT.sub(sub, text)
    assert "<<<<<<<" not in new and ">>>>>>>" not in new, path
    p.write_text(new, encoding="utf-8")
    print(f"{path}: {idx[0]} hunks resolved")


def both_upstream_first(i, ours, theirs):
    return theirs + "\n" + ours if not theirs.endswith("\n\n") else theirs + ours


def changelog(i, ours, theirs):
    return ours + "\n" + theirs


PR428 = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/428"
PR436 = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/436"
PR437 = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/437"


def backlog(i, ours, theirs):
    if i == 0:
        return ("2. Раздел 2 — семнадцать решений владельца `Р-01…Р-17`. Без них задачи не\n"
                "   стартуют. У каждого решения есть рекомендация; ответ — одна строка в\n"
                "   комментарии к PR #421 (`Р-13…Р-15` — к PR #428, `Р-16` — к PR #436,\n"
                "   `Р-17` — к PR #437).\n")
    if i == 1:  # code dictionary rows: keep both
        return theirs + ours
    if i == 2:
        return ours
    if i == 3:
        lines = theirs.splitlines(keepends=True)
        lines[0] = "| 0 | — | — | Решения `Р-01…Р-17` | Ответ владельца в PR #421, PR #428, PR #436 и PR #437 |\n"
        assert lines[3].rstrip().endswith("BL-160 — к этапу 3 |"), lines[3]
        lines[3] = lines[3].rstrip()[:-2] + "; BL-163 — после слияния РТ-1 в runtime |\n"
        return "".join(lines)
    if i == 4:  # decisions table: Р-16 then Р-17
        return theirs + ours
    if i == 5:
        return (f"к [PR #428]({PR428}), для Р-16 —\n"
                f"к [PR #436]({PR436}), для Р-17 — к\n"
                f"[PR #437]({PR437})) на каждое\n")
    if i == 6:
        t = theirs.replace("(../docs/adr/003-ba-ontology.md#поправка-02-тип-гейта-проект-ждёт-р-16)).\n",
                           "(../docs/adr/003-ba-ontology.md#поправка-02-тип-гейта-проект-ждёт-р-16);\n"
                           "«Р-17 да» — к PR #437).\n")
        assert t != theirs
        return t
    if i == 7:
        return ("**Критерий закрытия.** BL-150…BL-157, BL-159, BL-162, BL-230, BL-231 `DONE`;\n"
                "BL-158, BL-161 — `deferred (triggered)` до прогонов на новых задачах; BL-160 —\n"
                "`deferred (triggered)` до старта стенда n8n (BL-141); BL-163 —\n"
                "`deferred (triggered)` до слияния РТ-1 в runtime.\n")
    if i == 8:  # task rows: BL-161, BL-162, then BL-163
        return theirs + ours
    raise SystemExit(f"unexpected hunk {i}")


def model(i, ours, theirs):
    return theirs + "\n" + ours


resolve("CHANGELOG.md", changelog)
resolve("pr-ops/BACKLOG.md", backlog)
resolve("pr-ops/backlog-ba-model.md", model)
