#!/usr/bin/env python3
"""Local regression check for issue #72 Smart Sync from Hub PRs #224/#226/#229/#230."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SESSION_HANDOVER_SHA = "f3e8b265b1577d0ee1fe173dbe16728cc3c7e31b"
HUB_SHA = "b683341d22d4f518618917a02d9c7c394658b156"
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
        ".archive/ai-rules/agent-onboarding-protocol_old.md",
        "pr-ops/session-digests.md",
        "pr-ops/artifact-map.md",
        ".hub-profile.json",
        "AI_GOVERNANCE.md",
        "CONTRIBUTING.md",
        "docs/hub-research-dependencies.md",
        "docs/task-for-konard-template.md",
        "docs/adr/0002-issue48-handover-local-enrichment.md",
        "docs/adr/0003-creative-mode-governance.md",
        "docs/analysis/migration-strategy-rfc.md",
        "docs/reviews/migration-rfc-human-review-2026-06.md",
        "pr-ops/BACKLOG.md",
        "pr-ops/migration-phase1-issues.md",
        "README.md",
        "CHANGELOG.md",
    ):
        errors += require_file(path)

    if not errors:
        errors += require(
            "AI_SESSION_HANDOVER_PROMPT.md",
            "version: 0.5",
            SESSION_HANDOVER_SHA,
            "Периодическая суммаризация сессии",
            "pr-ops/session-digests.md",
            "агент-исполнитель",
            "Пользователь",
            "Исполнитель",
        )
        errors += reject("AI_SESSION_HANDOVER_PROMPT.md", OLD_SHA, "Иосполнитель")

        errors += require(
            ".archive/ai-rules/agent-onboarding-protocol_old.md",
            SESSION_HANDOVER_SHA,
            "Периодическая суммаризация сессии",
            "pr-ops/session-digests.md",
            "Пользователь",
            "Исполнитель",
        )
        errors += reject(".archive/ai-rules/agent-onboarding-protocol_old.md", OLD_SHA, "Иосполнитель")

        errors += require(
            "pr-ops/session-digests.md",
            "# Session Digests — Mango BA Prompts",
            "Индекс",
            "Шаблон блока суммарии",
            "Пользователь",
            "Исполнитель",
            "агент-исполнитель",
            "issue #72",
        )
        errors += reject(
            "pr-ops/session-digests.md",
            "Архитектура документации и баланс Anti-Inflation vs атомарность",
            "Иосполнитель",
        )

        errors += require(
            "pr-ops/artifact-map.md",
            "# Artifact Map — mango_ba_prompts",
            "/AI_SESSION_HANDOVER_PROMPT.md",
            "/pr-ops/session-digests.md",
            "/pr-ops/migration-manifest.md",
            "/prompts/",
            "Пользователь",
            "Исполнитель",
            HUB_SHA,
            "Hub PR #229",
            "Hub PR #230",
        )
        errors += reject("pr-ops/artifact-map.md", "Иосполнитель")

        errors += require(
            "docs/hub-research-dependencies.md",
            "external-sources-registry.md",
            "ext-003",
            "ext-007",
            "Spec-Driven Development",
            "Контекст-инжиниринг",
            HUB_SHA,
            "reference-only",
            "не копируется в локальный `research/`",
        )
        if (ROOT / "research/external-knowledge/external-sources-registry.md").exists():
            errors.append("research/external-knowledge/external-sources-registry.md: Base Registry must stay reference-only in mango")

        errors += require(
            "AI_GOVERNANCE.md",
            HUB_SHA,
            "Пользователь",
            "молчание = согласие",
            "комментарий + ручной перезапуск",
            "`research/` Хаба, а не в команду",
        )
        errors += reject("AI_GOVERNANCE.md", "Founder & PO", "Фаундер", "Иосполнитель")

        errors += require(
            "CONTRIBUTING.md",
            "Пользователь",
            "молчание = согласие",
            "ручной перезапуск",
            "не создают `research/` в споке",
        )
        errors += reject("CONTRIBUTING.md", "Фаундер", "Иосполнитель")

        # Точку синка issue #72 хранит sync_history: last_sync принадлежит
        # последнему синку (issue #265) и обязан двигаться вперёд, иначе эта
        # проверка запрещала бы любой следующий синк из Хаба.
        profile = json.loads(read(".hub-profile.json"))
        history = profile.get("sync_history", [])
        last_sync = next(
            (
                entry
                for entry in [profile.get("last_sync", {})] + history
                if entry.get("issue") == "https://github.com/G-Ivan-A/mango_ba_prompts/issues/72"
            ),
            None,
        )
        if last_sync is None:
            errors.append(".hub-profile.json: sync_history has no record for issue #72")
            last_sync = {}
        if last_sync.get("hub_sha") != HUB_SHA:
            errors.append(".hub-profile.json: issue #72 record hub_sha is not Hub main SHA after PR #229/#230")
        hub_prs = set(last_sync.get("hub_prs", []))
        for hub_pr in (224, 226, 229, 230):
            if hub_pr not in hub_prs:
                errors.append(f".hub-profile.json: hub_prs missing {hub_pr}")
        # Журнал синка фиксирует пути на момент события: здесь проверяется
        # содержание записи, а не текущее размещение файлов. Актуальные пути
        # перенесённых артефактов — в .hub-profile.json > path_migrations
        # (issue #291).
        synced_paths = set(last_sync.get("synced_paths", []))
        for path in (
            "AI_SESSION_HANDOVER_PROMPT.md",
            "ai-rules/agent-onboarding-protocol_old.md",
            "pr-ops/session-digests.md",
            "pr-ops/artifact-map.md",
            "docs/hub-research-dependencies.md",
            "docs/task-for-konard-template.md",
            "docs/adr/0002-issue48-handover-local-enrichment.md",
            "docs/adr/0003-creative-mode-governance.md",
            "docs/analysis/migration-strategy-rfc.md",
            "docs/reviews/migration-rfc-human-review-2026-06.md",
            "pr-ops/BACKLOG.md",
            "pr-ops/migration-phase1-issues.md",
            "AI_GOVERNANCE.md",
            "CONTRIBUTING.md",
        ):
            if path not in synced_paths:
                errors.append(f".hub-profile.json: synced_paths missing {path}")

        errors += require(
            "docs/task-for-konard-template.md",
            "version: 0.2",
            "updated: 2026-06-13",
            "Пользователь",
            "молчание = согласие",
            "ручной перезапуск",
        )
        errors += reject("docs/task-for-konard-template.md", "Фаундер", "Иосполнитель")

        for path in (
            "docs/adr/0002-issue48-handover-local-enrichment.md",
            "docs/adr/0003-creative-mode-governance.md",
            "docs/analysis/migration-strategy-rfc.md",
            "docs/reviews/migration-rfc-human-review-2026-06.md",
            "pr-ops/BACKLOG.md",
            "pr-ops/migration-phase1-issues.md",
        ):
            errors += require(path, "Пользовател")
            errors += reject(path, "Фаундер", "фаундер", "Иосполнитель")

        errors += require(
            "README.md",
            "pr-ops/artifact-map.md",
            "pr-ops/session-digests.md",
            "Пользователь",
        )
        errors += reject("README.md", "Founder & PO", "Иосполнитель")

        errors += require(
            "CHANGELOG.md",
            "Issue #72",
            "pr-ops/session-digests.md",
            "pr-ops/artifact-map.md",
            "Hub PR #229",
            "Hub PR #230",
            "reference-only",
            HUB_SHA,
        )
        errors += reject("CHANGELOG.md", "Фаундер", "Иосполнитель")

        errors += require(
            "pr-ops/migration-manifest.md",
            "PR [#229]",
            "PR [#230]",
            "external-sources-registry.md",
            HUB_SHA,
            "not-migrated",
        )

    if errors:
        print("issue-72 hub sync validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-72 hub sync validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
