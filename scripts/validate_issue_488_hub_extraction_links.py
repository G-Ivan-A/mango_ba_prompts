#!/usr/bin/env python3
"""Issue #488: no new floating links into Hub paths removed after the BA meta-model extraction.

The Hub moved `projects/ba-ai-process/` and `research/mango/` to
G-Ivan-A/ba-ai-metamodel (Hub B-249) and deletes its working copies, so links into
those paths on a branch of the Hub (`blob/main/...`) stop resolving. Links pinned to a
Hub SHA keep working. A link into the moved tree goes to ba-ai-metamodel by SHA.

The prompt release of issue #488 pinned the link in the published prompts
(`prompts/bcreq-*.md`, new minor versions), rebuilt the step drafts and the site
data. The step builder pins the link itself (`HUB_FLOATING` → `HUB_PINNED`), so a
new version built from a published text with the floating link does not bring it
back; `test_builder_pins` proves it on the measured texts.

HISTORY lists the files that keep a floating link for good (issue #488, item 2):
the 2.7.0 archive, the inputs of measured runs, the transcripts, the archive cards
of the site catalog and the revert layer of the release itself. They are records of
what was sent or measured; rewriting them would falsify the history. A count may
only go down; any other file must not have a floating link.
"""
import importlib.util
import json
import re
import subprocess
import sys
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
HISTORY = {
    # Архив редакции 2.7.0: байт в байт исходники коммита sourceCommit.
    "prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md": 1,
    "prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md": 1,
    "prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md": 1,
    # Входы измеренных прогонов: текст, который получила модель.
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
    # Транскрипты прогонов.
    "runs/2026/RUN-0088/outputs/steps/Ш-7/transcript.md": 1,
    "runs/2026/RUN-0089/outputs/T-transcript.md": 13,
    # Карточки архива 2.7.0 в каталоге сайта: content и body трёх файлов выше.
    "site/data/prompts.json": 6,
    # Обратимый слой релиза: поле floating и «before» 25 правок — измеренный текст.
    "experiments/issue_488/prompt-edits.json": 26,
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_builder_pins(errors):
    """Build the drafts from the measured texts (floating link) and expect pinned output."""
    sys.path.insert(0, str(ROOT / "scripts"))
    builder = load("step_builder_488_check", ROOT / "scripts/build_bcreq_step_prompts.py")
    layer = load("p488_check", ROOT / "experiments/issue_488/prompt_changes.py")
    read = builder.read

    def measured(path):
        text = read(path)
        rel = path.relative_to(ROOT).as_posix()
        return layer.revert(rel, text) if rel.startswith("prompts/bcreq-") else text

    builder.read = measured
    try:
        outputs = builder.build_all()
    finally:
        builder.read = read
    pinned = 0
    for path, text in outputs.items():
        refs = [ref for ref in LINK.findall(text) if not SHA40.match(ref.lower())]
        if refs:
            errors.append(f"{path.relative_to(ROOT)}: the step builder kept {len(refs)} floating Hub link(s)")
        pinned += path.name == "manifest.json" and sum(
            d["hub_main_to_metamodel_sha"] for d in json.loads(text)["drafts"])
    if pinned != 11:
        errors.append(f"step builder pinned {pinned} draft link(s) from the measured texts, expected 11")


def main():
    errors = []
    for rel, count in sorted(floating().items()):
        limit = HISTORY.get(rel, 0)
        if count > limit:
            errors.append(f"{rel}: {count} floating Hub link(s) into a moved path (allowed {limit}); "
                          "pin to https://github.com/G-Ivan-A/ba-ai-metamodel/blob/<sha>/...")
    check_builder_pins(errors)
    release = subprocess.run([sys.executable, str(ROOT / "experiments/issue_488/release.py"), "--check"],
                             capture_output=True, text=True)
    if release.returncode:
        errors.append(release.stdout + release.stderr)
    if errors:
        raise SystemExit("issue #488 hub extraction links: FAIL\n" + "\n".join(errors))
    print(f"issue #488 hub extraction links: OK (prompts, drafts and site pinned; "
          f"{len(HISTORY)} historical file(s); builder pins measured texts)")


if __name__ == "__main__":
    main()
