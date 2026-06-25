#!/usr/bin/env python3
"""Validate issue #233 BA-processes industry-analysis deliverables."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/analysis/ba-processes-industry-analysis.md"
RESEARCH = ROOT / "docs/analysis/telecom-vendors-ba-practices-research.md"
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
        'issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/233"',
        "type: analysis",
        "operating_mode: creative",
        "# Структурный анализ БА-процессов и артефактов",
        # Methodology + three mandatory expert roles (sequential).
        "## Методология и роли экспертов",
        "Архитектор БА-методологий",
        "AI-инженер",
        "BA-эксперт",
        # Mandatory document sections 1-12 (Stage 10).
        "## 1. Введение",
        "## 2. Текущее состояние БА-процессов",
        "## 3. Индустриальные практики телекома",
        "## 4. Фреймворки БА",
        "## 5. Таксономия БА-артефактов",
        "## 6. Сравнительный анализ",
        "## 7. Сильные/слабые стороны и рекомендации",
        "## 8. Проверка стандартов проекта",
        "## 9. Полный список артефактов",
        "## 10. Вход для RFC",
        "## 11. Дополнительные исследования",
        "## 12. Заключение",
        "## Источники",
        # Analysis-only constraints (no decisions; protected files cited, not modified).
        "только анализ",
        "не принимает решений",
        "не меняет",
        # Protected / cited internal artifacts.
        "standards/ba-ontology.md",
        "standards/executable-contract-standard.md",
        "governance/bcreq-fr-generation-contract.md",
        "runs/CONTRACT.md",
        "docs/ba-processes/00-index.md",
        # Companion empirical research deliverable.
        "docs/analysis/telecom-vendors-ba-practices-research.md",
        # Composite vs atomic taxonomy (industry terms).
        "Singular",
        "atomic",
        "composite",
        "User Story",
        "Use Case",
        # Project-standards check (L1-L3, contracts vs standards, mis-classification).
        "L1",
        "L2",
        "L3",
        "rule_class",
        "product-classification-contract.md",
        "runs-contract-standard.md",
        # Focus company + below-band finding (H4/H6).
        "Манго",
        "Mavenir",
        # RFC input.
        "Вход для RFC",
        "RFC-IN-1",
    ]
    for fragment in required_fragments:
        require(fragment in text, f"missing required fragment: {fragment}")

    # Frameworks: at least three studied (BABOK, IREB, BCS/PMI-PBA/Agile BA).
    framework_markers = ["BABOK", "IREB", "BCS", "PMI-PBA", "SAFe"]
    found_frameworks = [m for m in framework_markers if m in text]
    require(
        len(found_frameworks) >= 3,
        f"expected at least 3 BA frameworks, found {len(found_frameworks)}: {found_frameworks}",
    )

    # TM Forum industry anchor must be present.
    require(
        re.search(r"TM\s*Forum", text, re.IGNORECASE) is not None,
        "missing TM Forum industry anchor",
    )
    require(
        re.search(r"Open\s*API|OpenAPI", text, re.IGNORECASE) is not None,
        "missing OpenAPI / Open API de-facto contract artifact",
    )

    # At least two diagrams (taxonomy + classification check).
    mermaid_count = text.count("```mermaid")
    require(mermaid_count >= 2, f"expected at least 2 Mermaid diagrams, found {mermaid_count}")

    # Hypotheses table must enumerate at least six hypotheses (H1..Hn).
    hypotheses = re.findall(r"\|\s*\*\*H[0-9]+\*\*|\|\s*H[0-9]+", text)
    require(len(hypotheses) >= 6, f"expected at least 6 hypotheses (H-N), found {len(hypotheses)}")

    # Gaps and excesses must be catalogued (Stage 5/6).
    gaps = re.findall(r"\|\s*G[0-9]+", text)
    excesses = re.findall(r"\|\s*E[0-9]+", text)
    recs = re.findall(r"\|\s*R[0-9]+", text)
    rfc_inputs = re.findall(r"RFC-IN-[0-9]+", text)
    require(len(gaps) >= 3, f"expected at least 3 gaps (G-N), found {len(gaps)}")
    require(len(excesses) >= 3, f"expected at least 3 excesses (E-N), found {len(excesses)}")
    require(len(recs) >= 5, f"expected at least 5 recommendations (R-N), found {len(recs)}")
    require(len(set(rfc_inputs)) >= 5, f"expected at least 5 RFC inputs, found {len(set(rfc_inputs))}")

    # Evidence labelling discipline.
    for label in ["[CONFIRMED]", "[INFERRED]", "[HYPOTHESIS]", "NOT FOUND"]:
        require(label in text, f"missing evidence label: {label}")

    # At least ten distinct telecom companies named in the synthesis.
    companies = [
        "Mavenir", "Манго", "Amdocs", "Netcracker", "CSG", "Optiva", "Hansen",
        "Twilio", "RingCentral", "8x8", "Vonage", "Telenor", "Orange",
        "Vodafone", "Deutsche Telekom", "AT&T",
    ]
    found_companies = [c for c in companies if c in text]
    require(
        len(found_companies) >= 10,
        f"expected at least 10 telecom companies, found {len(found_companies)}: {found_companies}",
    )

    # Source URLs must be present (https links).
    https_links = re.findall(r"https?://", text)
    require(len(https_links) >= 20, f"expected at least 20 source URLs, found {len(https_links)}")

    # Companion empirical research file must exist and carry sources.
    require(RESEARCH.exists(), f"missing empirical research file: {RESEARCH.relative_to(ROOT)}")
    research = RESEARCH.read_text(encoding="utf-8")
    require("https://" in research, "empirical research file missing source URLs")

    # CHANGELOG must record the deliverable and the validator.
    require(CHANGELOG.exists(), "missing CHANGELOG.md")
    changelog = CHANGELOG.read_text(encoding="utf-8")
    require("Issue #233" in changelog, "CHANGELOG.md missing Issue #233 entry")
    require(
        "docs/analysis/ba-processes-industry-analysis.md" in changelog,
        "CHANGELOG.md missing report path",
    )
    require(
        "scripts/validate_issue_233_ba_processes_industry_analysis.py" in changelog,
        "CHANGELOG.md missing validator path",
    )
    require(
        "только анализ" in changelog,
        "CHANGELOG.md missing analysis-only disclaimer for Issue #233",
    )

    print("OK: issue #233 BA-processes industry-analysis deliverables validated")


if __name__ == "__main__":
    main()
