#!/usr/bin/env python3
"""Regression check for issue #203: VPBX API is findable from KB search terms.

Issue #203 was opened after an AI agent used Mango Dialogi/API MD material for a
VPBX API task. The VPBX source existed, but the generated KB did not expose
enough machine-readable product, taxonomy, and query-term metadata for an agent
to reliably pick it from a short query such as ``event onAppealClose``.

This check locks the intended contract:

- the VPBX source manifest carries product aliases and Mango Taxonomy traceability;
- generated ``vpbx-api`` metadata preserves that traceability;
- the index maps the literal query ``event onAppealClose`` to section 4.8.3.1;
- the event and method chunks keep endpoint, parameter, and source trace details.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_META = ROOT / "kb/mango-product-docs/sources/vpbx-api/meta.json"
PROCESSED = ROOT / "kb/mango-product-docs/processed/vpbx-api"
PROCESSED_META = PROCESSED / "meta.json"
INDEX = PROCESSED / "index.md"
ON_APPEAL_CLOSE = PROCESSED / "sections/216-obschenie-zakryto.md"
CREATE_CLOSED_APPEAL = PROCESSED / "sections/214-sozdanie-zakrytogo-obrascheniya.md"
CHANGELOG = ROOT / "CHANGELOG.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"{rel(path)}: missing")
        return ""
    return path.read_text(encoding="utf-8")


def load_json(path: Path, errors: list[str]) -> dict:
    text = read_text(path, errors)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(path)}: invalid JSON ({exc})")
        return {}


def require_contains(text: str, path: Path, *needles: str) -> list[str]:
    return [f"{rel(path)}: missing {needle!r}" for needle in needles if needle not in text]


def require_list_contains(values: object, path: Path, field: str, *needles: str) -> list[str]:
    if not isinstance(values, list):
        return [f"{rel(path)}: {field} must be a list"]
    missing = [needle for needle in needles if needle not in values]
    return [f"{rel(path)}: {field} missing {needle!r}" for needle in missing]


def check_source_manifest() -> list[str]:
    errors: list[str] = []
    meta = load_json(SOURCE_META, errors)
    if not meta:
        return errors
    errors += require_list_contains(meta.get("aliases"), SOURCE_META, "aliases", "API VPBX", "VPBX API", "API ВАТС")
    taxonomy = meta.get("mango_taxonomy")
    if not isinstance(taxonomy, dict):
        errors.append(f"{rel(SOURCE_META)}: mango_taxonomy must be an object")
        return errors
    if taxonomy.get("primary_cluster") != "vats-core":
        errors.append(f"{rel(SOURCE_META)}: mango_taxonomy.primary_cluster must be 'vats-core'")
    secondary = taxonomy.get("secondary_clusters")
    errors += require_list_contains(
        secondary,
        SOURCE_META,
        "mango_taxonomy.secondary_clusters",
        "contact-center-core",
        "platform-integrations",
    )
    return errors


def check_processed_meta() -> list[str]:
    errors: list[str] = []
    meta = load_json(PROCESSED_META, errors)
    if not meta:
        return errors
    if meta.get("product") != "Mango VPBX":
        errors.append(f"{rel(PROCESSED_META)}: product must be 'Mango VPBX'")
    errors += require_list_contains(meta.get("aliases"), PROCESSED_META, "aliases", "API VPBX", "VPBX API", "API ВАТС")
    taxonomy = meta.get("mango_taxonomy")
    if not isinstance(taxonomy, dict):
        errors.append(f"{rel(PROCESSED_META)}: mango_taxonomy must be an object")
    elif taxonomy.get("primary_cluster") != "vats-core":
        errors.append(f"{rel(PROCESSED_META)}: mango_taxonomy.primary_cluster must be 'vats-core'")
    if meta.get("section_count", 0) < 250:
        errors.append(f"{rel(PROCESSED_META)}: expected full VPBX extraction with at least 250 sections")
    if meta.get("table_count", 0) < 400:
        errors.append(f"{rel(PROCESSED_META)}: expected full VPBX extraction with at least 400 tables")
    return errors


def check_index() -> list[str]:
    errors: list[str] = []
    text = read_text(INDEX, errors)
    if not text:
        return errors
    errors += require_contains(
        text,
        INDEX,
        "API VPBX",
        "Mango VPBX",
        "vats-core",
        "event onAppealClose",
        "/events/md/onAppealClose",
        "[sections/216-obschenie-zakryto.md](sections/216-obschenie-zakryto.md)",
        "/cc/appeals/create-closed-appeals",
        "[sections/214-sozdanie-zakrytogo-obrascheniya.md](sections/214-sozdanie-zakrytogo-obrascheniya.md)",
    )
    other_indexes = sorted(PROCESSED.parent.glob("*/index.md"))
    competitors = [
        path
        for path in other_indexes
        if path != INDEX and "onAppealClose" in path.read_text(encoding="utf-8", errors="ignore")
    ]
    if competitors:
        rendered = ", ".join(rel(path) for path in competitors)
        errors.append(f"{rel(INDEX)}: query onAppealClose also appears in competing indexes: {rendered}")
    return errors


def check_chunks() -> list[str]:
    errors: list[str] = []
    event_text = read_text(ON_APPEAL_CLOSE, errors)
    method_text = read_text(CREATE_CLOSED_APPEAL, errors)
    if event_text:
        errors += require_contains(
            event_text,
            ON_APPEAL_CLOSE,
            "product: \"Mango VPBX\"",
            "mango_taxonomy_primary_cluster: \"vats-core\"",
            "/events/md/onAppealClose",
            "Параметры события",
            "conversion_id",
            "result",
            "chat",
            "sender_name",
            "contact",
            "source_refs:",
            "> Трассировка: PDF §4.8.3.1",
        )
    if method_text:
        errors += require_contains(
            method_text,
            CREATE_CLOSED_APPEAL,
            "product: \"Mango VPBX\"",
            "mango_taxonomy_primary_cluster: \"vats-core\"",
            "/cc/appeals/create-closed-appeals",
            "Параметры метода",
            "product_id",
            "channel_type",
            "result",
            "appeal_id",
            "source_refs:",
            "> Трассировка: PDF §4.8.2",
        )
    return errors


def check_changelog() -> list[str]:
    errors: list[str] = []
    text = read_text(CHANGELOG, errors)
    if not text:
        return errors
    return require_contains(
        text,
        CHANGELOG,
        "Issue #203",
        "event onAppealClose",
        "vpbx-api",
        "vats-core",
        "validate_issue_203_vpbx_api_retrieval.py",
    )


def main() -> int:
    errors: list[str] = []
    errors += check_source_manifest()
    errors += check_processed_meta()
    errors += check_index()
    errors += check_chunks()
    errors += check_changelog()
    if errors:
        print("Issue #203 VPBX API retrieval validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Issue #203 VPBX API retrieval validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
