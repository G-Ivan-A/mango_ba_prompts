#!/usr/bin/env python3
"""Refresh the bounded, local documentation cache; never run in BA workflows/CI."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
GOOSE = "https://goose-docs.ai/docs/"
CLINE = "https://docs.cline.bot/"
SOURCES = {
    "G01": GOOSE + "quickstart.md",
    "G02": GOOSE + "guides/context-engineering/using-goosehints.md",
    "G03": GOOSE + "guides/context-engineering/using-skills.md",
    "G04": GOOSE + "guides/managing-tools/goose-permissions.md",
    "G05": GOOSE + "guides/managing-tools/tool-permissions.md",
    "G06": GOOSE + "guides/recipes/recipe-reference.md",
    "G07": GOOSE + "guides/sessions/session-management.md",
    "G08": GOOSE + "guides/sessions/smart-context-management.md",
    "G09": GOOSE + "guides/config-files.md",
    "G10": GOOSE + "guides/goose-cli-commands.md",
    "G11": GOOSE + "getting-started/using-extensions.md",
    "G12": GOOSE + "mcp/memory-mcp.md",
    "G13": GOOSE + "guides/logs.md",
    "G14": GOOSE + "guides/usage-data.md",
    "G15": GOOSE + "getting-started/providers.md",
    "G16": GOOSE + "getting-started/installation.md",
    "O01": "https://opencode.ai/docs/rules/",
    "O02": "https://opencode.ai/docs/skills/",
    "O03": "https://opencode.ai/docs/permissions/",
    "O04": "https://opencode.ai/docs/agents/",
    "O05": "https://opencode.ai/docs/config/",
    "O06": "https://opencode.ai/docs/tui/",
    "O07": "https://opencode.ai/docs/mcp-servers/",
    "O08": "https://opencode.ai/docs/enterprise/",
    "O09": "https://opencode.ai/docs/",
    "L01": CLINE + "customization/cline-rules.md",
    "L02": CLINE + "customization/skills.md",
    "L03": CLINE + "features/auto-approve.md",
    "L04": CLINE + "core-workflows/plan-and-act.md",
    "L05": CLINE + "best-practices/memory-bank.md",
    "L06": CLINE + "core-workflows/checkpoints.md",
    "L07": CLINE + "core-workflows/working-with-files.md",
    "L08": CLINE + "running-models-locally/overview.md",
    "L09": CLINE + "enterprise-solutions/monitoring/telemetry.md",
    "L10": CLINE + "enterprise-solutions/configuration/infrastructure-configuration/control-other-cline-features/mcp-server-controls.md",
}


def fetch():
    cache = HERE / ".sources"
    cache.mkdir(exist_ok=True)
    observations = []
    for identifier, url in SOURCES.items():
        row = {"id": identifier, "url": url,
               "accessed_at": datetime.now(timezone.utc).isoformat()}
        try:
            with urlopen(Request(url, headers={"User-Agent": "BA-research/1.0"})) as response:
                body = response.read(2_000_001)
                if len(body) > 2_000_000:
                    raise ValueError("Document exceeds research cache limit")
                content_type = response.headers.get("Content-Type", "")
                if "text" not in content_type:
                    raise ValueError("Not a text document: " + content_type)
                row.update(status=response.status, resolved_url=response.url,
                           content_type=content_type, bytes=len(body),
                           sha256=hashlib.sha256(body).hexdigest())
                (cache / (identifier + ".txt")).write_bytes(body)
        except Exception as error:
            row["error"] = str(error)
        observations.append(row)
        print(identifier, row.get("status", row.get("error")))
    (HERE / "source-observations.json").write_text(
        json.dumps(observations, ensure_ascii=False, indent=2) + "\n")
    return not any("error" in row for row in observations)


if __name__ == "__main__":
    raise SystemExit(0 if fetch() else 1)
