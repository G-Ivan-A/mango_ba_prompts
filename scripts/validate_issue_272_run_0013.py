#!/usr/bin/env python3
"""Regression check for issue #272 — фиксация реального прогона RUN-0013.

Проверяется то, что легко сломать незаметно:

- структура прогона и обязательные поля ``metadata.yaml`` (контракт ``runs/``);
- метрики в ``metadata.yaml`` совпадают с фактическими числами из экспорта чата
  (а не разъезжаются при ручном редактировании);
- ``inputs/chat-transcript.md`` и ``logs/metrics.md`` побайтово воспроизводятся
  из сырого экспорта генератором ``scripts/chat_export_to_transcript.py``;
- вердикты по эпизодам согласованы между ``outputs/episodes.md`` и
  ``outputs/README.md``;
- прогон зарегистрирован в ``runs/README.md`` и ``CHANGELOG.md``;
- сохранена оговорка, что материалы прогона не являются эталоном.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "runs" / "2026" / "RUN-0013"
EXPORT = RUN_DIR / "inputs" / "chat-export-1064.json"
GENERATOR = ROOT / "scripts" / "chat_export_to_transcript.py"

REQUIRED_FILES = (
    "metadata.yaml",
    "inputs/README.md",
    "inputs/chat-export-1064.json",
    "inputs/chat-transcript.md",
    "outputs/README.md",
    "outputs/final-artifact.md",
    "outputs/prompts-chain.md",
    "outputs/episodes.md",
    "logs/experiment-log.md",
    "logs/metrics.md",
    "feedback/README.md",
)

REQUIRED_METADATA_FIELDS = (
    "run_id",
    "process",
    "version",
    "date",
    "author",
    "model",
    "status",
)

EPISODES = ("E1", "E2", "E3", "E4", "E5", "E6", "E7")
VERDICTS = ("works", "works-with-edits", "fails")

# Ядро метрик по standards/experiment-log-standard.md.
EXPERIMENT_LOG_METRICS = ("iterations", "ba_edits", "quality", "prompts_used", "verdict", "outcome")


def load_generator():
    spec = importlib.util.spec_from_file_location("chat_export_to_transcript", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metadata_scalars(text: str) -> dict[str, str]:
    """Плоские пары ``ключ: значение`` верхнего уровня и вложенного ``metrics``."""
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^(\s*)([A-Za-z_]+):\s*(.*)$", line)
        if not match or not match.group(3).strip():
            continue
        values[match.group(2)] = match.group(3).strip().strip('"')
    return values


def episode_verdicts(text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    return {match.group(1): match.group(2) for match in pattern.finditer(text)}


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (RUN_DIR / relative).is_file():
            errors.append(f"missing file: runs/2026/RUN-0013/{relative}")
    for subdir in ("inputs", "outputs", "feedback", "logs"):
        if not (RUN_DIR / subdir).is_dir():
            errors.append(f"missing dir: runs/2026/RUN-0013/{subdir}/")

    if errors:
        # Дальнейшие проверки читают эти файлы — без них они бессмысленны.
        print("issue-272 RUN-0013 validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    metadata_text = (RUN_DIR / "metadata.yaml").read_text(encoding="utf-8")
    metadata = metadata_scalars(metadata_text)

    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            errors.append(f"metadata.yaml: missing required field `{field}`")
    if metadata.get("run_id") != "RUN-0013":
        errors.append("metadata.yaml: run_id must be RUN-0013 and match the directory name")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", metadata.get("date", "")):
        errors.append("metadata.yaml: date must be YYYY-MM-DD")
    if metadata.get("verdict") not in VERDICTS:
        errors.append(f"metadata.yaml: metrics.verdict must be one of {VERDICTS}")
    if metadata.get("status") != metadata.get("verdict"):
        errors.append("metadata.yaml: status and metrics.verdict must agree")
    if "https://github.com/G-Ivan-A/mango_ba_prompts/issues/272" not in metadata_text:
        errors.append("metadata.yaml: related_issues must reference issue #272")

    # Метрики против фактов экспорта.
    generator = load_generator()
    chat = generator.load_chat(EXPORT)
    messages = generator.ordered_messages(chat)
    assistant = [m for m in messages if m.get("role") == "assistant"]
    facts = {
        "iterations": len(assistant),
        "output_tokens": sum(generator.usage(m).get("output_tokens", 0) for m in assistant),
        "reasoning_tokens": sum(
            (generator.usage(m).get("output_tokens_details") or {}).get("reasoning_tokens", 0)
            for m in assistant
        ),
        "input_tokens_max_per_call": max(
            (generator.usage(m).get("input_tokens", 0) for m in assistant), default=0
        ),
        "input_tokens_sum": sum(generator.usage(m).get("input_tokens", 0) for m in assistant),
    }
    for key, expected in facts.items():
        actual = metadata.get(key)
        if actual is None:
            errors.append(f"metadata.yaml: missing metric `{key}` (expected {expected})")
        elif actual != str(expected):
            errors.append(f"metadata.yaml: metric `{key}` = {actual}, but export gives {expected}")

    if metadata.get("model") != (chat["chat"].get("models") or [None])[0]:
        errors.append("metadata.yaml: model must match the model recorded in the chat export")

    # Порождаемые файлы должны быть воспроизводимы побайтово.
    source = EXPORT.relative_to(ROOT).as_posix()
    generated = {
        "inputs/chat-transcript.md": generator.render_transcript(chat, messages, source),
        "logs/metrics.md": generator.render_metrics(chat, messages, source),
    }
    for relative, expected_text in generated.items():
        if (RUN_DIR / relative).read_text(encoding="utf-8") != expected_text:
            errors.append(
                f"runs/2026/RUN-0013/{relative} is out of sync with the raw export; "
                f"regenerate it with scripts/chat_export_to_transcript.py instead of editing by hand"
            )

    # Вердикты по эпизодам согласованы между разбором и навигацией.
    episodes_text = (RUN_DIR / "outputs" / "episodes.md").read_text(encoding="utf-8")
    outputs_readme = (RUN_DIR / "outputs" / "README.md").read_text(encoding="utf-8")
    detailed = episode_verdicts(
        episodes_text, re.compile(r"^## (E\d)\..*— `(works|works-with-edits|fails)`$", re.M)
    )
    summary = episode_verdicts(
        episodes_text, re.compile(r"^\| (E\d) \|[^|]*\|[^|]*\| (works|works-with-edits|fails) \|", re.M)
    )
    navigation = episode_verdicts(
        outputs_readme, re.compile(r"^\| (E\d) \|[^|]*\| (works|works-with-edits|fails) \|", re.M)
    )
    for name, table in (("episodes.md summary", summary), ("outputs/README.md", navigation)):
        missing = [episode for episode in EPISODES if episode not in table]
        if missing:
            errors.append(f"{name}: no verdict for {', '.join(missing)}")
    for episode in EPISODES:
        verdicts = {detailed.get(episode), summary.get(episode), navigation.get(episode)}
        verdicts.discard(None)
        if len(verdicts) > 1:
            errors.append(f"{episode}: verdict differs across files: {sorted(verdicts)}")

    experiment_log = (RUN_DIR / "logs" / "experiment-log.md").read_text(encoding="utf-8")
    for field in EXPERIMENT_LOG_METRICS:
        if f"- {field}:" not in experiment_log:
            errors.append(f"logs/experiment-log.md: missing metric `{field}` required by the standard")

    # Прогон — не эталон: оговорка обязана присутствовать в видимых артефактах.
    for relative in ("outputs/README.md", "outputs/final-artifact.md"):
        if "golden case" not in (RUN_DIR / relative).read_text(encoding="utf-8"):
            errors.append(
                f"runs/2026/RUN-0013/{relative}: missing the disclaimer that the run "
                f"is not an approved template / golden case"
            )

    for relative, marker in (
        ("runs/README.md", "2026/RUN-0013/metadata.yaml"),
        ("CHANGELOG.md", "RUN-0013"),
    ):
        if marker not in (ROOT / relative).read_text(encoding="utf-8"):
            errors.append(f"{relative}: RUN-0013 is not registered")

    if errors:
        print("issue-272 RUN-0013 validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-272 RUN-0013 validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
