#!/usr/bin/env python3
"""Validate issue #231 BCREQ-FR contract process-analysis deliverables."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/analysis/bcreq-fr-contract-process-analysis.md"
CHANGELOG = ROOT / "CHANGELOG.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    require(REPORT.exists(), f"missing report: {REPORT.relative_to(ROOT)}")
    text = REPORT.read_text(encoding="utf-8")

    # Frontmatter and analysis-only framing.
    required_fragments = [
        'issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/231"',
        "type: analysis",
        "operating_mode: creative",
        "# Структурный анализ применения контракта BCREQ-FR",
        # Mandatory document sections (Stage 7).
        "## Методология и роли экспертов",
        "## 1. Введение",
        "## 2. Гипотезы",
        "## 3. Структурный анализ проблемы",
        "## 4. Анализ причин",
        "## 5. Тесты применения",
        "## 6. Выявленные проблемы",
        "## 7. Граничные кейсы",
        "## 8. Дополнительные исследования",
        "## 9. Заключение",
        "## Источники",
        # Three mandatory expert roles (sequential).
        "Архитектор процессов",
        "AI-инженер",
        "BA-эксперт",
        # Analysis-only constraints (no decisions; protected files cited, not modified).
        "только анализ",
        "не принимает решений",
        "governance/bcreq-fr-generation-contract.md",
        "runs/CONTRACT.md",
        # Central thesis: the three application regimes and the natural experiment.
        "Режим 1",
        "Режим 2",
        "Режим 3",
        "RUN-0014",
        "RUN-0010",
    ]
    for fragment in required_fragments:
        require(fragment in text, f"missing required fragment: {fragment}")

    # The monolith-vs-sequence conclusion must be stated.
    require(
        re.search(r"монолит", text, re.IGNORECASE) is not None,
        "missing monolith conclusion (no 'монолит' wording found)",
    )

    # At least two process diagrams (regimes + root cause).
    mermaid_count = text.count("```mermaid")
    require(mermaid_count >= 2, f"expected at least 2 Mermaid diagrams, found {mermaid_count}")

    # Stage 6: at least six edge cases with EC-N headings.
    edge_cases = re.findall(r"^### EC-[0-9]+", text, re.MULTILINE)
    require(len(edge_cases) >= 6, f"expected at least 6 edge cases (EC-N), found {len(edge_cases)}")

    # Hypotheses table must enumerate at least six hypotheses (H1..Hn).
    hypotheses = re.findall(r"\|\s*H[0-9]+", text)
    require(len(hypotheses) >= 6, f"expected at least 6 hypotheses (H-N), found {len(hypotheses)}")

    # Stage 5: maximum problem set across the three roles plus versioning.
    pa_problems = re.findall(r"\|\s*PA-[0-9]+", text)
    aie_problems = re.findall(r"\|\s*AIE-[0-9]+", text)
    ba_problems = re.findall(r"\|\s*BA-[0-9]+", text)
    ver_problems = re.findall(r"\|\s*VER-[0-9]+", text)
    require(len(pa_problems) >= 5, f"expected at least 5 process-architect problems, found {len(pa_problems)}")
    require(len(aie_problems) >= 5, f"expected at least 5 ai-engineer problems, found {len(aie_problems)}")
    require(len(ba_problems) >= 4, f"expected at least 4 ba-expert problems, found {len(ba_problems)}")
    require(len(ver_problems) >= 3, f"expected at least 3 versioning problems, found {len(ver_problems)}")
    total_problems = len(pa_problems) + len(aie_problems) + len(ba_problems) + len(ver_problems)
    require(total_problems >= 15, f"expected at least 15 catalogued problems, found {total_problems}")

    # Required problem dimensions: subprocess/operation, traceability, versioning.
    dimension_markers = [
        "подпроцесс",
        "операц",
        "трассируемост",
        "версионирование",
        "переиспользован",
        "статистик",
    ]
    for marker in dimension_markers:
        require(
            re.search(marker, text, re.IGNORECASE) is not None,
            f"missing required problem dimension marker: {marker}",
        )

    # CHANGELOG must record the deliverable and the validator.
    require(CHANGELOG.exists(), "missing CHANGELOG.md")
    changelog = CHANGELOG.read_text(encoding="utf-8")
    require("Issue #231" in changelog, "CHANGELOG.md missing Issue #231 entry")
    require(
        "docs/analysis/bcreq-fr-contract-process-analysis.md" in changelog,
        "CHANGELOG.md missing report path",
    )
    require(
        "scripts/validate_issue_231_bcreq_fr_contract_process_analysis.py" in changelog,
        "CHANGELOG.md missing validator path",
    )

    print("OK: issue #231 BCREQ-FR contract process-analysis deliverables validated")


if __name__ == "__main__":
    main()
