#!/usr/bin/env python3
"""Local regression check for issue #95: prompt ID in copied text.

Locks the requirements:
- copyText call prepends <!-- {prompt.id} --> HTML comment (ФТ-1);
- format matches <!-- {prompt.id} -->\n\n{body} (ФТ-1);
- HTML comment is only added on copy, not in the rendered card (ФТ-1);
- five target prompts have valid IDs in prompts.json (ФТ-3);
- CHANGELOG.md mentions Issue #95 (ФТ-4).
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TARGET_PROMPT_IDS = [
    "mango-fr-documentation-stepwise",
    "mango-asr-ingestion-oneshot",
    "mango-uc-modeling-oneshot",
    "mango-questions-customer-understanding-stepwise",
    "mango-meeting-customer-documentation-stepwise",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    errors: list[str] = []

    app_js = read_text("site/app.js")

    # ФТ-1: copyText is called with <!-- {prompt.id} --> prefix.
    errors += require(
        app_js,
        "site/app.js",
        "<!-- ${prompt.id} -->",
    )
    # The format must be <!-- id -->\n\n{body}.
    if "<!-- ${prompt.id} -->\\n\\n${body}" not in app_js and (
        "<!-- ${prompt.id} -->\\n\\n" not in app_js
        and "`<!-- ${prompt.id} -->\\n\\n${body}`" not in app_js
    ):
        # Check template literal form (backticks escape differently in source).
        if not re.search(
            r"copyText\(`<!-- \$\{prompt\.id\} -->\\n\\n\$\{body\}`\)",
            app_js,
        ):
            errors.append(
                "site/app.js: copyText must use format `<!-- ${prompt.id} -->\\n\\n${body}`"
            )

    # ФТ-1: HTML comment must NOT appear in the rendered card (promptCard function).
    prompt_card_match = re.search(
        r"function promptCard\(prompt\)\s*\{(.+?)^}", app_js, re.DOTALL | re.MULTILINE
    )
    if prompt_card_match:
        card_body = prompt_card_match.group(1)
        if "<!-- ${prompt.id} -->" in card_body:
            errors.append(
                "site/app.js: HTML comment must not appear in promptCard (display only)"
            )

    # ФТ-3: prompts.json exists and contains the 5 target prompts with valid IDs.
    prompts_json_path = "site/data/prompts.json"
    if not (ROOT / prompts_json_path).exists():
        errors.append(f"{prompts_json_path}: file does not exist")
    else:
        prompts_data = read_json(prompts_json_path)
        prompt_ids = {p["id"] for p in prompts_data.get("prompts", [])}
        for target_id in TARGET_PROMPT_IDS:
            if target_id not in prompt_ids:
                errors.append(f"{prompts_json_path}: missing target prompt id {target_id!r}")

        # Verify IDs follow mango-[operation]-[mode] pattern.
        id_pattern = re.compile(r"^mango-[a-z][a-z0-9]*(?:-[a-z][a-z0-9]*)*$")
        for prompt in prompts_data.get("prompts", []):
            prompt_id = prompt.get("id", "")
            if not id_pattern.match(prompt_id):
                errors.append(
                    f"{prompts_json_path}: prompt id {prompt_id!r} does not match mango-[operation]-[mode] format"
                )

    # ФТ-4: CHANGELOG.md documents the change.
    changelog = read_text("CHANGELOG.md")
    errors += require(changelog, "CHANGELOG.md", "Issue #95")

    if errors:
        print("issue-95 prompt-id-in-copy validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-95 prompt-id-in-copy validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
