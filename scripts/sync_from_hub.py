#!/usr/bin/env python3
"""Воспроизводимый ре-синк методологии Хаба в спицу `mango_ba_prompts`.

Зачем скрипт, а не ручное копирование
-------------------------------------
Ручной перенос файлов Хаба — это источник дефекта, зафиксированного в §4.2
анализа готовности Хаба: «некритично скопированный контекст». Файл приезжает
вместе с hub-относительными ссылками (`../CONCEPT.md`, `../pr-ops/repo-model.md`),
цели которых в споке не существуют, — так в `standards/GLOSSARY.md` появились
20 битых ссылок. Скрипт делает перенос детерминированным: каждая относительная
ссылка либо переписывается на локальный путь спицы (если цель тоже перенесена),
либо превращается в permalink в Хаб, закреплённый за SHA синхронизации.

Политика синхронизации (ADR-0004)
---------------------------------
* Source of truth остаётся в Хабе; файлы в спице — рабочие копии на `source_sha`.
* Локальные правки в синхронизированные файлы не вносятся: расхождение
  устраняется следующим синком, а не редактированием копии.
* Прямые hub-относительные ссылки (`../../...`) в споке запрещены — только
  локальные пути или полные URL в Хаб (см. `scripts/validate_issue_265_hub_sync.py`).

Использование
-------------
    python3 scripts/sync_from_hub.py --hub-dir /path/to/hybrid-Intelligence-lab
    python3 scripts/sync_from_hub.py --hub-dir <dir> --check   # только проверка

`--check` ничего не пишет и завершается ненулевым кодом, если рабочая копия
в споке отличается от того, что дал бы синк на текущем `source_sha`.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"

# Манифест ре-синка. Отбор выполнен по §4.4 анализа готовности Хаба и по
# фильтрам видения спицы (issue #263): переносится методология, которая нужна
# исполнителю BA-прогона, и не переносятся общерепозиторные контракты Хаба,
# для которых у спицы есть собственная норма (обоснование — docs/adr/0004).
MANIFEST: dict[str, str] = {
    # Правила поведения агента-исполнителя прогона.
    "ai-rules/README.md": "ai-rules/README.md",
    "ai-rules/agent-work-rules.md": "ai-rules/agent-work-rules.md",
    "ai-rules/agent-onboarding-protocol.md": "ai-rules/agent-onboarding-protocol.md",
    "ai-rules/adversarial-stress-testing.md": "ai-rules/adversarial-stress-testing.md",
    # Периметр безопасности при работе с приватными данными Mango.
    "ai-governance/README.md": "ai-governance/README.md",
    # Слот ai-governance/ai-governance.md занят операционным контрактом самой
    # спицы (геном HTOM в редакции RFC #532), поэтому рабочая копия стандарта
    # Хаба живёт рядом под именем hub-*: два SSOT в одном файле невозможны.
    "ai-governance/ai-governance.md": "ai-governance/hub-ai-governance.md",
    "ai-governance/agent-security-checklist.md": "ai-governance/agent-security-checklist.md",
    # Стандарты. GLOSSARY.md сохраняет историческое имя файла спицы: на него
    # ссылаются prompts/ и standards/ спицы (в Хабе файл переименован в glossary.md).
    "standards/glossary.md": "standards/GLOSSARY.md",
    "standards/evals-contract-standard.md": "standards/evals-contract-standard.md",
    "standards/analysis-standard.md": "standards/analysis-standard.md",
    "standards/research-standard.md": "standards/research-standard.md",
}

# Баннер рабочей копии — вставляется сразу после H1.
BANNER_LINES = [
    "> **Рабочая копия стандарта Хаба.** Source of truth — "
    "[`hybrid-Intelligence-lab`]({hub_url}/blob/{sha}/{hub_path}) на `source_sha`.",
    "> Локально файл не редактируется: расхождение устраняется следующим синком",
    "> (`python3 scripts/sync_from_hub.py --hub-dir <клон Хаба>`), а не правкой копии.",
]

SPOKE_FRONTMATTER_KEYS = (
    "source_hub",
    "source_sha",
    "source_of_truth",
    "sync_policy",
    "scope",
)

LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\((?!https?:|mailto:|tel:|#)([^)\s]+)\)")


class SyncError(RuntimeError):
    """Синк не может продолжаться без решения человека."""


def hub_sha(hub_dir: Path) -> str:
    """SHA снимка Хаба, за который закрепляется синк."""
    out = subprocess.run(
        ["git", "-C", str(hub_dir), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def split_frontmatter(text: str) -> tuple[list[str], str]:
    """Вернуть (строки frontmatter без разделителей, тело)."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---\n", 3)
    if end == -1:
        return [], text
    return text[4:end].splitlines(), text[end + 5 :]


def hub_permalink(sha: str, hub_target: str, is_dir: bool) -> str:
    kind = "tree" if is_dir else "blob"
    return f"{HUB_URL}/{kind}/{sha}/{hub_target}"


def rewrite_link(hub_file: str, target: str, sha: str, hub_dir: Path) -> str:
    """Переписать одну относительную ссылку hub-файла под спицу.

    Правила:
    1. цель тоже синхронизирована -> относительный путь внутри спицы;
    2. иначе -> permalink в Хаб на `sha` (каталог -> `/tree/`, файл -> `/blob/`).
    """
    path_part, _, anchor = target.partition("#")
    anchor = f"#{anchor}" if anchor else ""
    if not path_part:  # ссылка вида "#anchor" — внутренняя, не трогаем
        return target

    hub_target = _normalize(Path(hub_file).parent / path_part)
    if hub_target in MANIFEST:
        local_from = Path(MANIFEST[hub_file]).parent
        local_to = Path(MANIFEST[hub_target])
        rel = _relpath(local_to, local_from)
        return f"{rel}{anchor}"

    resolved = hub_dir / hub_target
    if not resolved.exists():
        raise SyncError(
            f"{hub_file}: ссылка `{target}` не разрешается и в Хабе "
            f"(ожидался {hub_target}). Требуется правка в Хабе, не в спице."
        )
    is_dir = resolved.is_dir() or path_part.endswith("/")
    return f"{hub_permalink(sha, hub_target, is_dir)}{anchor}"


def _normalize(path: Path) -> str:
    parts: list[str] = []
    for part in path.parts:
        if part in (".", ""):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _relpath(target: Path, base: Path) -> str:
    t = [p for p in target.parts if p not in (".", "")]
    b = [p for p in base.parts if p not in (".", "")]
    common = 0
    while common < min(len(t), len(b)) and t[common] == b[common]:
        common += 1
    up = [".."] * (len(b) - common)
    return "/".join(up + t[common:]) or "."


def render(hub_file: str, hub_dir: Path, sha: str) -> str:
    """Собрать содержимое локальной рабочей копии для одного hub-файла."""
    source = (hub_dir / hub_file).read_text(encoding="utf-8")
    fm_lines, body = split_frontmatter(source)
    if not fm_lines:
        raise SyncError(f"{hub_file}: отсутствует frontmatter — синк не выполняется")

    # frontmatter: hub-поля сохраняются, spoke-поля traceability переписываются.
    kept = [
        line
        for line in fm_lines
        if not any(line.startswith(f"{key}:") for key in SPOKE_FRONTMATTER_KEYS)
    ]
    spoke = [
        f'source_hub: "{hub_permalink(sha, hub_file, is_dir=False)}"',
        f'source_sha: "{sha}"',
        'source_of_truth: "hybrid-Intelligence-lab"',
        'sync_policy: "explicit spoke sync from pinned Hub commit; no local edits"',
        "scope: mango_ba_prompts",
    ]

    body = LINK_RE.sub(
        lambda m: f"[{m.group(1)}]({rewrite_link(hub_file, m.group(2), sha, hub_dir)})",
        body,
    )
    body = _insert_banner(body, hub_file, sha)

    return "---\n" + "\n".join(kept + spoke) + "\n---\n" + body


def _insert_banner(body: str, hub_file: str, sha: str) -> str:
    banner = "\n".join(
        line.format(hub_url=HUB_URL, sha=sha, hub_path=hub_file) for line in BANNER_LINES
    )
    lines = body.splitlines(keepends=True)
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            head = lines[: idx + 1]
            tail = lines[idx + 1 :]
            while tail and not tail[0].strip():
                tail.pop(0)
            return "".join(head) + "\n" + banner + "\n\n" + "".join(tail)
    raise SyncError(f"{hub_file}: не найден H1 — некуда вставить баннер рабочей копии")


def update_profile(sha: str, changed: list[str]) -> None:
    """Зафиксировать точку синка в `.hub-profile.json`."""
    profile_path = REPO_ROOT / ".hub-profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["last_sync"]["hub_sha"] = sha
    profile["last_sync"]["synced_paths"] = sorted(
        set(profile["last_sync"].get("synced_paths", [])) | set(changed)
    )
    profile_path.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hub-dir",
        required=True,
        type=Path,
        help="локальный клон https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
    )
    parser.add_argument(
        "--sha",
        help="SHA Хаба для закрепления ссылок (по умолчанию HEAD клона)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="ничего не писать; упасть, если рабочие копии расходятся с Хабом",
    )
    parser.add_argument(
        "--no-profile",
        action="store_true",
        help="не обновлять .hub-profile.json",
    )
    args = parser.parse_args(argv)

    hub_dir: Path = args.hub_dir.expanduser().resolve()
    if not hub_dir.is_dir():
        print(f"ОШИБКА: клон Хаба не найден: {hub_dir}", file=sys.stderr)
        return 2
    sha = args.sha or hub_sha(hub_dir)

    diverged: list[str] = []
    written: list[str] = []
    try:
        for hub_file, local_file in sorted(MANIFEST.items()):
            rendered = render(hub_file, hub_dir, sha)
            dest = REPO_ROOT / local_file
            current = dest.read_text(encoding="utf-8") if dest.exists() else None
            if current == rendered:
                print(f"= {local_file}")
                continue
            if args.check:
                diverged.append(local_file)
                diff = difflib.unified_diff(
                    (current or "").splitlines(keepends=True),
                    rendered.splitlines(keepends=True),
                    fromfile=f"spoke/{local_file}",
                    tofile=f"hub@{sha[:7]}/{hub_file}",
                    n=1,
                )
                print("".join(list(diff)[:40]), end="")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(rendered, encoding="utf-8")
            written.append(local_file)
            print(f"{'+' if current is None else '~'} {local_file}")
    except SyncError as exc:
        print(f"ОШИБКА синка: {exc}", file=sys.stderr)
        return 3

    if args.check:
        if diverged:
            print(
                f"\nFAIL: {len(diverged)} рабочих копий расходятся с Хабом @ {sha[:7]}: "
                + ", ".join(diverged),
                file=sys.stderr,
            )
            return 1
        print(f"\nOK: все {len(MANIFEST)} рабочих копий соответствуют Хабу @ {sha[:7]}")
        return 0

    if written and not args.no_profile:
        update_profile(sha, sorted(MANIFEST.values()))
        print("~ .hub-profile.json")
    print(f"\nСинк выполнен на Хаб @ {sha}; изменено файлов: {len(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
