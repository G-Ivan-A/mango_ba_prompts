#!/usr/bin/env python3
"""Разовая чистка ручных исходников промптов (issue #495, ФТ-2).

Применяет к ручным (не генерируемым) исходникам исполнимую проекцию
``scripts/prompt_purity.project``: ссылки на приватный репозиторий и
относительные ссылки → подпись, служебные HTML-комментарии → удалены.
Смысловые правки (балласт, кейс-специфика) — отдельными коммитами вручную,
реестр удалений — в описании PR. Генерируемые файлы не трогает: их чистят
сборщики. Повторный запуск идемпотентен.

    python3 experiments/issue_495/clean_sources.py [--dry-run]
"""
import argparse
import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import prompt_purity  # noqa: E402

HAND = [
    "prompts/*.md",
    "prompts/archive/*.md",
    "prompts/archive/a-in-v2.7.0/*.md",
    "standards/bcreq-manual-classes/[0-9]*.md",
]
SKIP = {"prompts/README.md", "prompts/README.executable.md",
        "prompts/AI_SESSION_HANDOVER_PROMPT.executable.md", "prompts/archive/a-in-v2.7.0/README.md"}


def split(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5:]
    return "", text


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    changed = []
    for pattern in HAND:
        for name in sorted(glob.glob(str(ROOT / pattern))):
            rel = Path(name).relative_to(ROOT).as_posix()
            if rel in SKIP:
                continue
            text = Path(name).read_text(encoding="utf-8")
            head, body = split(text)
            new = head + prompt_purity.project(body)
            if new != text:
                changed.append(rel)
                if not args.dry_run:
                    Path(name).write_text(new, encoding="utf-8")
    print("\n".join(changed))
    print(f"изменено файлов: {len(changed)}")


if __name__ == "__main__":
    main()
