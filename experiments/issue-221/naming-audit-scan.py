#!/usr/bin/env python3
"""Scan tracked repository paths for issue #221 naming audit criteria."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class NamingFinding:
    path: Path
    kind: str
    artifact: str
    flags: tuple[str, ...]


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


def tracked_directories(files: list[Path]) -> set[Path]:
    directories: set[Path] = set()
    for file_path in files:
        current = Path()
        for part in file_path.parts[:-1]:
            current = current / part
            directories.add(current)
    return directories


def naming_flags(name: str) -> tuple[str, ...]:
    flags: list[str] = []
    if re.search(r"[A-Z]", name):
        flags.append("uppercase")
    if "_" in name:
        flags.append("snake_case")
    if " " in name:
        flags.append("space")
    if re.search(r"[^A-Za-z0-9._-]", name):
        flags.append("special")
    return tuple(flags)


def scan() -> list[NamingFinding]:
    files = tracked_files()
    directories = tracked_directories(files)
    paths = sorted(directories | set(files), key=lambda path: str(path))
    findings: list[NamingFinding] = []

    for path in paths:
        flags = naming_flags(path.name)
        if not flags:
            continue
        findings.append(
            NamingFinding(
                path=path,
                kind="dir" if path in directories else "file",
                artifact=path.name,
                flags=flags,
            )
        )

    return findings


def print_summary(findings: list[NamingFinding]) -> None:
    files = tracked_files()
    directories = tracked_directories(files)
    flag_counts = Counter(flag for finding in findings for flag in finding.flags)
    top_level_counts = Counter(finding.path.parts[0] for finding in findings)

    print(f"tracked_files: {len(files)}")
    print(f"tracked_directories: {len(directories)}")
    print(f"findings: {len(findings)}")
    print("flags:")
    for flag, count in sorted(flag_counts.items()):
        print(f"  {flag}: {count}")
    print("top_level:")
    for top_level, count in sorted(top_level_counts.items()):
        print(f"  {top_level}: {count}")


def print_tsv(findings: list[NamingFinding]) -> None:
    print("path\tkind\tartifact\tflags")
    for finding in findings:
        print(
            f"{finding.path}\t{finding.kind}\t{finding.artifact}\t"
            f"{','.join(finding.flags)}"
        )


def print_markdown(findings: list[NamingFinding]) -> None:
    print("| Path | Kind | Artifact | Flags |")
    print("| --- | --- | --- | --- |")
    for finding in findings:
        print(
            f"| `{finding.path}` | {finding.kind} | `{finding.artifact}` | "
            f"{', '.join(finding.flags)} |"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format",
        choices=("summary", "tsv", "markdown"),
        default="summary",
    )
    args = parser.parse_args()

    findings = scan()
    if args.format == "summary":
        print_summary(findings)
    elif args.format == "tsv":
        print_tsv(findings)
    else:
        print_markdown(findings)

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
