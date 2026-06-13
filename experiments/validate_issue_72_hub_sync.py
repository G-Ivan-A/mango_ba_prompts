#!/usr/bin/env python3
"""Local regression check for issue #72 Smart Sync from Hub PRs #224/#226."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB_SHA = "f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b"
OLD_SHA = "117e4a553815af9b05d841c81dd725dd4a4c4d44"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(path: str, *needles: str) -> list[str]:
    text = read(path)
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def reject(path: str, *needles: str) -> list[str]:
    text = read(path)
    return [f"{path}: contains stale/forbidden {needle!r}" for needle in needles if needle in text]


def require_file(path: str) -> list[str]:
    if not (ROOT / path).exists():
        return [f"{path}: file does not exist"]
    return []


def main() -> int:
    errors: list[str] = []

    for path in (
        "AI_SESSION_HANDOVER_PROMPT.md",
        "governance/agent-onboarding-protocol.md",
        "governance/session-digests.md",
        "governance/artifact-map.md",
        ".hub-profile.json",
        "README.md",
        "CHANGELOG.md",
    ):
        errors += require_file(path)

    if not errors:
        errors += require(
            "AI_SESSION_HANDOVER_PROMPT.md",
            "version: 0.5",
            HUB_SHA,
            "Периодическая суммаризация сессии",
            "governance/session-digests.md",
            "агент-исполнитель",
            "Пользователь",
            "Исполнитель",
        )
        errors += reject("AI_SESSION_HANDOVER_PROMPT.md", OLD_SHA, "Иосполнитель")

        errors += require(
            "governance/agent-onboarding-protocol.md",
            HUB_SHA,
            "Периодическая суммаризация сессии",
            "governance/session-digests.md",
            "Пользователь",
            "Исполнитель",
        )
        errors += reject("governance/agent-onboarding-protocol.md", OLD_SHA, "Иосполнитель")

        errors += require(
            "governance/session-digests.md",
            "# Session Digests — Mango BA Prompts",
            "Индекс",
            "пока нет",
            "Пользователь",
            "Исполнитель",
            "агент-исполнитель",
            "issue #72",
        )
        errors += reject(
            "governance/session-digests.md",
            "Архитектура документации и баланс Anti-Inflation vs атомарность",
            "Иосполнитель",
        )

        errors += require(
            "governance/artifact-map.md",
            "# Artifact Map — mango_ba_prompts",
            "/AI_SESSION_HANDOVER_PROMPT.md",
            "/governance/session-digests.md",
            "/governance/migration-manifest.md",
            "/prompts/",
            "Пользователь",
            "Исполнитель",
            HUB_SHA,
        )
        errors += reject("governance/artifact-map.md", "Иосполнитель")

        profile = json.loads(read(".hub-profile.json"))
        last_sync = profile.get("last_sync", {})
        if last_sync.get("issue") != "https://github.com/G-Ivan-A/mango_ba_prompts/issues/72":
            errors.append(".hub-profile.json: last_sync.issue is not issue #72")
        if last_sync.get("hub_sha") != HUB_SHA:
            errors.append(".hub-profile.json: last_sync.hub_sha is not PR #226 merge SHA")
        synced_paths = set(last_sync.get("synced_paths", []))
        for path in (
            "AI_SESSION_HANDOVER_PROMPT.md",
            "governance/agent-onboarding-protocol.md",
            "governance/session-digests.md",
            "governance/artifact-map.md",
        ):
            if path not in synced_paths:
                errors.append(f".hub-profile.json: synced_paths missing {path}")

        errors += require(
            "README.md",
            "governance/artifact-map.md",
            "governance/session-digests.md",
        )
        errors += reject("README.md", "Иосполнитель")

        errors += require(
            "CHANGELOG.md",
            "Issue #72",
            "governance/session-digests.md",
            "governance/artifact-map.md",
            HUB_SHA,
        )
        errors += reject("CHANGELOG.md", "Иосполнитель")

    if errors:
        print("issue-72 hub sync validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-72 hub sync validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
