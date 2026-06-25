#!/usr/bin/env python3
"""Validate issue #229 runs-observability research deliverables."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/analysis/runs-observability-research.md"
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
        "issue: \"https://github.com/G-Ivan-A/mango_ba_prompts/issues/229\"",
        "# Исследование трассируемости промптов в runs и внешних практик контроля проходов",
        "## 1. Введение",
        "## 2. Выявленные проблемы",
        "## 3. Внешние практики",
        "## 4. Граничные кейсы",
        "## 5. Области дополнительного анализа",
        "## 6. Рекомендации",
        "## 7. Заключение",
        "## Источники",
        "Архитектор процессов",
        "AI-инженер",
        "BA-эксперт",
        "только анализ и рекомендации",
    ]
    for fragment in required_fragments:
        require(fragment in text, f"missing required fragment: {fragment}")

    # Problems P1..P5 must each appear as a sub-section.
    for pid in ("P1", "P2", "P3", "P4", "P5"):
        require(
            re.search(rf"### 2\.\d+\. {pid}: ", text) is not None,
            f"missing problem sub-section for {pid}",
        )

    # At least 5 external practices with sources.
    practice_count = len(re.findall(r"### 3\.\d+\. ", text))
    require(practice_count >= 5, f"expected >= 5 external practices, found {practice_count}")

    # At least 6 edge cases.
    case_count = len(re.findall(r"### 4\.\d+\. Кейс ", text))
    require(case_count >= 6, f"expected >= 6 edge cases, found {case_count}")

    # At least 8 areas of further analysis.
    area_count = len(re.findall(r"### 5\.\d+\. Область ", text))
    require(area_count >= 8, f"expected >= 8 analysis areas, found {area_count}")

    # Recommendations with explicit IDs and priorities.
    rec_ids = set(re.findall(r"R-(?:LOG|TRACE|VER|NAME|MAP)-\d+", text))
    require(len(rec_ids) >= 10, f"expected >= 10 recommendation IDs, found {len(rec_ids)}")

    # Mermaid diagrams (problem graph, area graph, ...).
    mermaid_count = text.count("```mermaid")
    require(mermaid_count >= 2, f"expected >= 2 Mermaid diagrams, found {mermaid_count}")

    # External sources: enough unique URLs covering all five practice families.
    urls = sorted(set(re.findall(r"https://[^\s>)]+", text)))
    require(len(urls) >= 15, f"expected >= 15 unique URLs, found {len(urls)}")
    for domain in ("langfuse.com", "mlflow.org", "opentelemetry.io", "anthropic.com", "pact.io"):
        require(
            any(domain in url for url in urls),
            f"missing source for external practice domain: {domain}",
        )

    changelog = CHANGELOG.read_text(encoding="utf-8")
    require("Issue #229" in changelog, "CHANGELOG.md missing Issue #229 entry")
    require(
        "docs/analysis/runs-observability-research.md" in changelog,
        "CHANGELOG.md missing report path",
    )

    print("OK: issue #229 runs-observability research deliverables validated")


if __name__ == "__main__":
    main()
