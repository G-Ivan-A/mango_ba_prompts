"""Shared executable fragments for both BCREQ formats (issue #509)."""
from pathlib import Path
import re

from bcreq_handoff import load
from prompt_purity import project

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/ba-processes"
VERSION = "0.4"


def body(name):
    return (DOCS / name).read_text(encoding="utf-8").split("---", 2)[2].strip()


def response_order():
    return load()["responseOrder"]


def access():
    # The access policy is unchanged until Р-ОТЛ-1/2; reuse the #474 SSOT.
    return "## Доступ и пробелы\n\n" + body("bcreq-evidence-normalization.md")


def output():
    return body("bcreq-ba-output.md").replace("{{response_order}}", response_order())


def decisions():
    return body("bcreq-decision-context.md")


def lessons(sid=None):
    """Common lessons belong in the once-per-chat contract, others in a step."""
    source = (ROOT / "docs/rfc/2026-11-a-in-decomposition.md").read_text()
    result = []
    for line in source.splitlines():
        if not re.match(r"\| LE-\d{2} \|", line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        general = "§3" in cells[-1]
        if (sid is None and general) or (sid and not general and re.search(rf"(?<!\d){sid[-2:]}(?!\d)", cells[-1])):
            rule = f"- **{cells[0]}.** {cells[1]} → {cells[2]}. Граница: {cells[3]}."
            result.append(re.sub(r" \(обратная связь RUN-\d{4}\)", "", rule))
    return "\n".join(result)


def common():
    source = body("bcreq-a-in-common.md")
    normal = body("bcreq-evidence-normalization.md")
    if source.count(normal) != 1:
        raise ValueError("A-IN common and evidence normalization SSOT differ")
    return project(source.replace(normal, access())
                   .replace("{{ba_output}}", output())
                   .replace("{{general_lessons}}", lessons())
                   .replace("{{decision_context}}", decisions()))
