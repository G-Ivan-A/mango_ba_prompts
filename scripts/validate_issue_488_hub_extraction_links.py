#!/usr/bin/env python3
"""Issue #488: no new floating links into Hub paths removed after the BA meta-model extraction.

The Hub moved `projects/ba-ai-process/` and `research/mango/` to
G-Ivan-A/ba-ai-metamodel (Hub B-249) and deletes its working copies, so links into
those paths on a branch of the Hub (`blob/main/...`) stop resolving. Links pinned to a
Hub SHA keep working. A link into the moved tree goes to ba-ai-metamodel by SHA.

LOCKED lists the byte-locked files (published prompts, drafts, archive, measured
run inputs and transcripts, site data) that may keep floating links until the prompt
release of issue #488. A count may only go down; when a file is fixed, drop its row.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOVED = ("projects/ba-ai-process", "research/mango", "docs/ba-meta-model-overview.md")
LINK = re.compile(
    r"(?:github\.com/G-Ivan-A/hybrid-Intelligence-lab/(?:blob|tree|raw)"
    r"|raw\.githubusercontent\.com/G-Ivan-A/hybrid-Intelligence-lab)"
    r"/([^/\s)\]>'\"]+)/(?:" + "|".join(re.escape(m) for m in MOVED) + ")",
    re.I,
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
LOCKED = {
    "prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md": 1,
    "prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md": 1,
    "prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md": 1,
    "prompts/bcreq-constitution-governance-oneshot.md": 1,
    "prompts/bcreq-constraints-documentation-stepwise.md": 1,
    "prompts/bcreq-context-understanding-stepwise.md": 1,
    "prompts/bcreq-core-documentation-oneshot.md": 1,
    "prompts/bcreq-extra-risk-analysis-stepwise.md": 1,
    "prompts/bcreq-fr-documentation-stepwise.md": 1,
    "prompts/bcreq-in-understanding-oneshot.md": 1,
    "prompts/bcreq-nfr-documentation-stepwise.md": 1,
    "prompts/bcreq-orr-solution-design-stepwise.md": 1,
    "prompts/bcreq-products-impact-analysis-stepwise.md": 1,
    "prompts/bcreq-review-validation-oneshot.md": 1,
    "prompts/bcreq-scenarios-modeling-oneshot.md": 1,
    "prompts/bcreq-uc-modeling-stepwise.md": 1,
    "prompts/bcreq-work-solution-design-oneshot.md": 1,
    "prompts/drafts/bcreq-constitution-governance-oneshot.md": 1,
    "prompts/drafts/bcreq-constraints-documentation-stepwise.md": 1,
    "prompts/drafts/bcreq-context-understanding-stepwise.md": 1,
    "prompts/drafts/bcreq-extra-risk-analysis-stepwise.md": 1,
    "prompts/drafts/bcreq-fr-documentation-stepwise.md": 1,
    "prompts/drafts/bcreq-nfr-documentation-stepwise.md": 1,
    "prompts/drafts/bcreq-orr-solution-design-stepwise.md": 1,
    "prompts/drafts/bcreq-products-impact-analysis-stepwise.md": 1,
    "prompts/drafts/bcreq-review-validation-oneshot.md": 1,
    "prompts/drafts/bcreq-scenarios-modeling-oneshot.md": 1,
    "prompts/drafts/bcreq-uc-modeling-stepwise.md": 1,
    "runs/2026/RUN-0084/inputs/prompt-A0.md": 1,
    "runs/2026/RUN-0084/inputs/prompt-A1.md": 1,
    "runs/2026/RUN-0084/inputs/prompt-A2.md": 1,
    "runs/2026/RUN-0085/inputs/prompt-A2.md": 1,
    "runs/2026/RUN-0085/inputs/prompt-A3.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S1-B.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S1-C.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S3-B.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S3-C.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S6-B.md": 1,
    "runs/2026/RUN-0086/inputs/prompt-S6-C.md": 1,
    "runs/2026/RUN-0087/inputs/prompt-B.md": 1,
    "runs/2026/RUN-0087/inputs/prompt-C.md": 1,
    "runs/2026/RUN-0088/outputs/steps/Ш-7/transcript.md": 1,
    "runs/2026/RUN-0089/outputs/T-transcript.md": 13,
    "site/data/prompts.json": 34,
    "site/data/test-kit.json": 12,
}


def floating():
    found = {}
    files = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], check=True,
                           capture_output=True).stdout.decode("utf-8").split("\0")
    for rel in files:
        path = ROOT / rel
        if not rel or not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data[:8192]:
            continue
        refs = LINK.findall(data.decode("utf-8", "replace"))
        count = sum(1 for ref in refs if not SHA40.match(ref.lower()))
        if count:
            found[rel] = count
    return found


def main():
    errors = []
    for rel, count in sorted(floating().items()):
        limit = LOCKED.get(rel, 0)
        if count > limit:
            errors.append(f"{rel}: {count} floating Hub link(s) into a moved path (allowed {limit}); "
                          "pin to https://github.com/G-Ivan-A/ba-ai-metamodel/blob/<sha>/...")
    if errors:
        raise SystemExit("issue #488 hub extraction links: FAIL\n" + "\n".join(errors))
    print(f"issue #488 hub extraction links: OK ({len(LOCKED)} locked file(s) pending the prompt release)")


if __name__ == "__main__":
    main()
