#!/usr/bin/env python3
"""Local regression check for issue #97 — formalization of the BA ontology and
the supporting living standards.

It locks the deliverables produced for issue #97 so later edits cannot silently
break them:

- **ADR-003..010 exist** and each carries the seven ФТ-9 mandatory sections
  (Title, Status, Context, Decision, Consequences, References, Examples);
- the **seven living-standard contracts** exist, each anchored to RFC 2119 /
  BCP 14 and with a "Критерии соответствия (DoD)" block that calls this
  validator;
- the **GitHub Pages process tree** (ФТ-8) data invariants hold:
  ``shownSubprocesses`` equals the number of subprocesses with ``hasPrompts``,
  processes with zero such subprocesses are dropped from ``shownProcesses``,
  ``useTree`` is exactly ``shownSubprocesses > treeThreshold`` (threshold 20 per
  the issue), and every *shown* subprocess links to a real **active** prompt
  (``prompts/<name>.md``; ``prompts/archive/`` never counts as "has prompt");
- the **hard constraints** hold: the team directory lists exactly two teams
  (``BCREQ``, ``CCMO``); no fabricated team command (``KK``, ``UCaaS``, ``DIG``,
  ``AI``, ``ANL``, ``HW``, ``SEC``) appears in the registry; the ``risk_analysis``
  operation is preserved;
- **CHANGELOG** and the **GitHub Pages workflow** reference issue #97 /
  this validator, so the check actually runs in CI.

Run: ``python3 scripts/validate_issue_97_ontology_standards.py`` (exit 0 = PASS).
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# ADR number -> path. ФТ-9 requires Title/Status/Context/Decision/Consequences/
# References/Examples in every ADR; the house format expresses them in Russian.
ADRS = {
    "003": "docs/adr/003-ba-ontology.md",
    "004": "docs/adr/004-operations-taxonomy.md",
    "005": "docs/adr/005-artifact-team-naming.md",
    "006": "docs/adr/006-prompt-naming.md",
    "007": "docs/adr/007-kb-standard.md",
    "008": "docs/adr/008-industry-standards-standard.md",
    "009": "docs/adr/009-bcreq-formation-process.md",
    "010": "docs/adr/010-pages-ux.md",
}

# Living-standard contracts authored for issue #97. Each must cite BCP 14, carry
# a DoD, and reference this validator from its DoD.
STANDARDS = (
    "standards/ba-ontology.md",
    "standards/artifact-naming-standard.md",
    "standards/team-directory.md",
    "standards/kb-standard.md",
    "standards/industry-standards-standard.md",
    "standards/bcreq-process-standard.md",
    "standards/pages-ux-standard.md",
)

BCP14_URL = "https://www.rfc-editor.org/info/bcp14"
DOD_HEADING = "## Критерии соответствия (DoD)"
VALIDATOR_REF = "scripts/validate_issue_97_ontology_standards.py"

# Hard constraints from the issue.
EXPECTED_TEAMS = {"BCREQ", "CCMO"}
FORBIDDEN_TEAM_CODES = ("KK", "UCaaS", "DIG", "AI", "ANL", "HW", "SEC")
TREE_THRESHOLD = 20  # ">20 → дерево" задан самим ФТ-8.


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


def require_file(path: str) -> list[str]:
    if not (ROOT / path).exists():
        return [f"{path}: file does not exist"]
    return []


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def check_adrs() -> list[str]:
    """ФТ-9: every ADR-003..010 carries the seven mandatory sections."""
    errors: list[str] = []
    for num, path in ADRS.items():
        missing = require_file(path)
        if missing:
            errors += missing
            continue
        text = read_text(path)

        # Title.
        if f"# ADR-{num}:" not in text:
            errors.append(f"{path}: missing title '# ADR-{num}:' (ФТ-9 Title)")
        # Status (frontmatter + house blockquote).
        if not re.search(r"(?m)^status:\s*\S+", text):
            errors.append(f"{path}: missing frontmatter 'status:' (ФТ-9 Status)")
        if "**Статус:**" not in text:
            errors.append(f"{path}: missing '**Статус:**' status line (ФТ-9 Status)")
        # Context / Decision / Consequences.
        for needle, label in (
            ("## Контекст", "Context"),
            ("## Решение", "Decision"),
            ("## Последствия", "Consequences"),
        ):
            if needle not in text:
                errors.append(f"{path}: missing '{needle}' (ФТ-9 {label})")
        # Examples.
        if "## Примеры" not in text:
            errors.append(f"{path}: missing '## Примеры' (ФТ-9 Examples)")
        # References: linked artifacts + a full-URL sources subsection.
        if "## Связанные артефакты" not in text:
            errors.append(f"{path}: missing '## Связанные артефакты' (ФТ-9 References)")
        if not re.search(r"###\s+(Международные стандарты|Внешние источники)", text):
            errors.append(
                f"{path}: missing full-URL sources subsection (ФТ-9 References)"
            )
    return errors


def check_standards() -> list[str]:
    """Every living-standard contract cites BCP 14, has a DoD, and calls us."""
    errors: list[str] = []
    for path in STANDARDS:
        missing = require_file(path)
        if missing:
            errors += missing
            continue
        text = read_text(path)
        if BCP14_URL not in text:
            errors.append(f"{path}: missing RFC 2119 / BCP 14 link ({BCP14_URL})")
        if DOD_HEADING not in text:
            errors.append(f"{path}: missing '{DOD_HEADING}'")
        if VALIDATOR_REF not in text:
            errors.append(f"{path}: DoD must reference '{VALIDATOR_REF}'")
    return errors


def check_team_directory() -> list[str]:
    """Hard constraint: exactly BCREQ + CCMO; no fabricated team commands."""
    path = "standards/team-directory.md"
    missing = require_file(path)
    if missing:
        return missing
    errors: list[str] = []
    text = read_text(path)

    # Registry codes are markdown rows that start with "| `CODE` |". The §4
    # prohibition note lists forbidden codes as inline code inside a paragraph
    # (never at line start with a table pipe), so it is correctly ignored here.
    codes = set(re.findall(r"(?m)^\|\s*`([A-Za-z][\w:-]*)`\s*\|", text))
    if codes != EXPECTED_TEAMS:
        errors.append(
            f"{path}: team registry must be exactly {sorted(EXPECTED_TEAMS)}, "
            f"found {sorted(codes)}"
        )
    for bad in FORBIDDEN_TEAM_CODES:
        if bad in codes:
            errors.append(f"{path}: fabricated team code {bad!r} present in registry")
        # The prohibition note must keep listing the forbidden code.
        if f"`{bad}`" not in text:
            errors.append(f"{path}: forbidden-codes note must still list {bad!r}")
    return errors


def check_process_tree() -> list[str]:
    """ФТ-8 data invariants for site/data/process-tree.json."""
    path = "site/data/process-tree.json"
    missing = require_file(path)
    if missing:
        return missing
    errors: list[str] = []
    tree = read_json(path)
    processes = tree.get("processes", [])

    if len(processes) != tree.get("totalProcesses"):
        errors.append(
            f"{path}: totalProcesses {tree.get('totalProcesses')} != "
            f"len(processes) {len(processes)}"
        )

    total_sub = 0
    shown_sub = 0
    shown_proc = 0
    for proc in processes:
        pid = proc.get("id")
        subs = proc.get("subprocesses", [])
        total_sub += len(subs)
        if len(subs) != proc.get("subprocessTotal"):
            errors.append(
                f"{path}: process {pid} subprocessTotal "
                f"{proc.get('subprocessTotal')} != len(subprocesses) {len(subs)}"
            )

        has_prompts = 0
        for sub in subs:
            order = sub.get("order")
            kind = sub.get("kind")
            flag = sub.get("hasPrompts")
            prompts = sub.get("prompts", [])
            expected = kind in ("direct", "support")
            if flag != expected:
                errors.append(
                    f"{path}: process {pid} sub {order}: hasPrompts {flag} "
                    f"inconsistent with kind {kind!r}"
                )
            if flag:
                has_prompts += 1
                if not prompts:
                    errors.append(
                        f"{path}: process {pid} sub {order}: hasPrompts but no "
                        "prompt links"
                    )
                for prm in prompts:
                    pfile = prm.get("file", "")
                    purl = prm.get("url", "")
                    if "archive/" in pfile or "/archive/" in purl:
                        errors.append(
                            f"{path}: process {pid} sub {order}: shown subprocess "
                            f"links archive prompt {pfile!r} (archive != has prompt)"
                        )
                        continue
                    if not (ROOT / "prompts" / pfile).exists():
                        errors.append(
                            f"{path}: process {pid} sub {order}: prompt file "
                            f"prompts/{pfile} does not exist"
                        )
            elif prompts:
                errors.append(
                    f"{path}: process {pid} sub {order}: kind {kind!r} must have "
                    f"no prompt links, found {len(prompts)}"
                )

        if proc.get("subprocessShown") != has_prompts:
            errors.append(
                f"{path}: process {pid} subprocessShown "
                f"{proc.get('subprocessShown')} != hasPrompts count {has_prompts}"
            )
        shown_sub += has_prompts
        if has_prompts > 0:
            shown_proc += 1

    if total_sub != tree.get("totalSubprocesses"):
        errors.append(
            f"{path}: totalSubprocesses {tree.get('totalSubprocesses')} != "
            f"sum {total_sub}"
        )
    if shown_sub != tree.get("shownSubprocesses"):
        errors.append(
            f"{path}: shownSubprocesses {tree.get('shownSubprocesses')} != "
            f"hasPrompts count {shown_sub}"
        )
    if shown_proc != tree.get("shownProcesses"):
        errors.append(
            f"{path}: shownProcesses {tree.get('shownProcesses')} != "
            f"processes-with-prompts {shown_proc}"
        )

    threshold = tree.get("treeThreshold")
    if threshold != TREE_THRESHOLD:
        errors.append(
            f"{path}: treeThreshold must be {TREE_THRESHOLD} (ФТ-8), found {threshold}"
        )
    elif tree.get("useTree") != (shown_sub > threshold):
        errors.append(
            f"{path}: useTree {tree.get('useTree')} != (shown {shown_sub} > "
            f"{threshold}) — ФТ-8 '>20 → дерево'"
        )
    return errors


def check_hard_constraints() -> list[str]:
    """risk_analysis must stay; the operation appears in ontology, taxonomy, tree."""
    errors: list[str] = []
    for path in (
        "standards/ba-ontology.md",
        "docs/adr/004-operations-taxonomy.md",
        "site/data/process-tree.json",
    ):
        missing = require_file(path)
        if missing:
            errors += missing
            continue
        if "risk_analysis" not in read_text(path):
            errors.append(f"{path}: 'risk_analysis' operation must be preserved")
    return errors


def check_wiring() -> list[str]:
    """ФТ-8 UI is wired, and the checks run in CHANGELOG / CI."""
    errors: list[str] = []
    for path in ("site/index.html", "site/app.js", "CHANGELOG.md",
                 ".github/workflows/github-pages.yml"):
        errors += require_file(path)
    if errors:
        return errors

    errors += require(read_text("site/index.html"), "site/index.html",
                      'id="processes"', "process-tree")
    errors += require(read_text("site/app.js"), "site/app.js",
                      "renderProcessTree", "process-tree.json")
    errors += require(read_text("CHANGELOG.md"), "CHANGELOG.md", "Issue #97")
    errors += require(read_text(".github/workflows/github-pages.yml"),
                      ".github/workflows/github-pages.yml", VALIDATOR_REF)
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_adrs()
    errors += check_standards()
    errors += check_team_directory()
    errors += check_process_tree()
    errors += check_hard_constraints()
    errors += check_wiring()

    if errors:
        print("issue-97 ontology & standards validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-97 ontology & standards validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
