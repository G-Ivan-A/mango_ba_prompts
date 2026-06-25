#!/usr/bin/env python3
"""Validate issue #225 artifact-chain research deliverables."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md"
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

    required_fragments = [
        "issue: \"https://github.com/G-Ivan-A/mango_ba_prompts/issues/225\"",
        "# Исследование гипотезы цепочки артефактов",
        "## 1. Введение",
        "## 2. Международные практики",
        "## 3. Анализ видения Фаундера",
        "## 4. Анализ текущего RFC-процесса",
        "## 5. BPMN-диаграммы процессов",
        "## 6. Ответы на вопросы",
        "## 7. Дополнительные предложения",
        "## 8. Заключение",
        "## Источники",
        "research → analytics → report → rfc/adr → standard → artifact",
        "Архитектор методологий",
        "BA-эксперт",
        "AI-инженер",
    ]
    for fragment in required_fragments:
        require(fragment in text, f"missing required fragment: {fragment}")

    mermaid_count = text.count("```mermaid")
    require(mermaid_count >= 4, f"expected at least 4 Mermaid diagrams, found {mermaid_count}")

    source_urls = sorted(set(re.findall(r"https://[^\s>)]+", text)))
    require(len(source_urls) >= 10, f"expected at least 10 unique external URLs, found {len(source_urls)}")

    risk_count = len(re.findall(r"\|\s*R-[0-9]+", text))
    opportunity_count = len(re.findall(r"\|\s*O-[0-9]+", text))
    require(risk_count >= 5, f"expected at least 5 risks, found {risk_count}")
    require(opportunity_count >= 5, f"expected at least 5 opportunities, found {opportunity_count}")

    diagram_titles = [
        "Основная цепочка артефактов",
        "Процесс RFC",
        "Процесс ADR",
        "Процесс согласования",
    ]
    for title in diagram_titles:
        require(title in text, f"missing diagram title: {title}")

    changelog = CHANGELOG.read_text(encoding="utf-8")
    require("Issue #225" in changelog, "CHANGELOG.md missing Issue #225 entry")
    require(
        "docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md" in changelog,
        "CHANGELOG.md missing report path",
    )

    print("OK: issue #225 artifact-chain research deliverables validated")


if __name__ == "__main__":
    main()
