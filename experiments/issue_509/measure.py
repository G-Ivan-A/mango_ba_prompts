#!/usr/bin/env python3
"""Repeat #505 measurement and count the actual shipped compact route."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import bcreq_fragments as fragments


def main():
    spec = importlib.util.spec_from_file_location("redundancy", ROOT / "experiments/issue_505/prompt_redundancy.py")
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    result = previous.main()
    kit = json.loads((ROOT / "site/data/a-in-kit.json").read_text())
    anchors = sum(len(s["compactPrompt"].split("## Якорь контракта", 1)[1]
                      .split("## Только текущий контракт:", 1)[0])
                  + len("## Якорь контракта") for s in kit["steps"])
    contract_once = len(kit["contract"]["prompt"])
    repeated = len(fragments.common()) * len(kit["steps"])
    compact_route = (sum(result["route_other_prompts_chars"].values()) + contract_once
                     + sum(len(s["compactPrompt"]) for s in kit["steps"]))
    result["actual_shipped"] = {
        "contract_version": kit["contract"]["version"],
        "full_repeated_contract_chars": repeated,
        "contract_once_chars": contract_once,
        "compact_anchors_chars": anchors,
        "contract_saving_share_including_anchors": round(1 - (contract_once + anchors) / repeated, 4),
        "compact_route_chars": compact_route,
        "route_saving_share": round(1 - compact_route / result["route_total_chars_as_pasted"], 4),
    }
    return result


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
