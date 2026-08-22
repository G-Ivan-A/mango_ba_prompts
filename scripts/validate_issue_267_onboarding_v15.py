#!/usr/bin/env python3
"""Валидатор issue #267: актуализация onboarding-протокола до v1.5.

Регрессионный тест для дефекта, из-за которого агент, пришедший по навигации,
попадал на архивную v1.2 вместо актуальной v1.5.

Проверки
--------
A. **Актуальный протокол.** `ai-rules/agent-onboarding-protocol.md` существует,
   несёт `version: 1.5` и обязательный для governance-артефакта frontmatter
   (`status`, `version`, `updated`, `owner`, `executable`, `entrypoint`).
B. **Архив не потерян и не является точкой входа.** `_old`-файлы существуют
   (traceability), имеют `status: superseded`, не объявляют `entrypoint` и
   содержат баннер со ссылкой на актуальную версию.
C. **Навигация.** Ни один активный навигационный артефакт не ведёт агента на
   `_old` как на рабочий протокол; каждый ссылается на актуальный файл.
D. **Валидаторы.** `tools/validate-frontmatter.sh` (в области спицы) и
   `tools/validate-file-naming.sh` проходят успешно; allowlist именования не
   маскирует новые нарушения.

Запуск (stdlib-only, без сети):

    python3 scripts/validate_issue_267_onboarding_v15.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CURRENT = "ai-rules/agent-onboarding-protocol.md"
ARCHIVE = [
    ".archive/ai-rules/agent-onboarding-protocol_old.md",
    ".archive/ai-rules/agent-onboarding-protocol_old.executable.md",
]
# Активная навигация: файлы, по которым агент или человек находит протокол.
NAVIGATION = [
    "README.md",
    "ai-rules/AI_SESSION_HANDOVER_PROMPT.md",
    "prompts/AI_SESSION_HANDOVER_PROMPT.executable.md",
    "pr-ops/artifact-map.md",
    "standards/cascading-context-loading-standard.md",
]
# Строки навигации, где `_old` упоминается намеренно — как архив.
ARCHIVE_MENTION_RE = re.compile(r"архив", re.IGNORECASE)

FRONTMATTER_SCOPE = ["ai-rules", "tools"]


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return fields


def check_current() -> list[str]:
    errors: list[str] = []
    path = REPO_ROOT / CURRENT
    if not path.exists():
        return [f"{CURRENT}: актуальный протокол v1.5 отсутствует"]
    fields = frontmatter(path)
    if fields.get("version") != "1.5":
        errors.append(f"{CURRENT}: version={fields.get('version')!r}, ожидается 1.5")
    for field in ("status", "version", "updated", "owner", "executable", "entrypoint"):
        if field not in fields:
            errors.append(f"{CURRENT}: отсутствует обязательное поле frontmatter: {field}")
    print(f"[A] актуальный протокол: {CURRENT} v{fields.get('version')}")
    return errors


def check_archive() -> list[str]:
    errors: list[str] = []
    for rel in ARCHIVE:
        path = REPO_ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: архив удалён, а traceability требует его сохранения")
            continue
        fields = frontmatter(path)
        if fields.get("status") != "superseded":
            errors.append(f"{rel}: status={fields.get('status')!r}, ожидается superseded")
        if "entrypoint" in fields:
            errors.append(f"{rel}: архив не должен объявлять entrypoint")
        if "agent-onboarding-protocol.md)" not in path.read_text(encoding="utf-8"):
            errors.append(f"{rel}: нет ссылки на актуальную версию протокола")
    print(f"[B] архив сохранён и помечен superseded: {len(ARCHIVE)} файла")
    return errors


def check_navigation() -> list[str]:
    errors: list[str] = []
    for rel in NAVIGATION:
        path = REPO_ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: навигационный артефакт отсутствует")
            continue
        text = path.read_text(encoding="utf-8")
        if "agent-onboarding-protocol.md" not in text.replace("_old", ""):
            errors.append(f"{rel}: нет ссылки на актуальный протокол {CURRENT}")
        for number, line in enumerate(text.split("\n"), start=1):
            if "agent-onboarding-protocol_old" in line and not ARCHIVE_MENTION_RE.search(line):
                errors.append(
                    f"{rel}:{number}: ссылка на архивный протокол вне контекста архива"
                )
    print(f"[C] проверено навигационных артефактов: {len(NAVIGATION)}")
    return errors


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        command, cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def check_validators() -> list[str]:
    errors: list[str] = []
    scope = sorted(p.name for p in REPO_ROOT.glob("*.md")) + FRONTMATTER_SCOPE
    code, output = run(["./tools/validate-frontmatter.sh", *scope])
    if code != 0:
        errors.append(f"tools/validate-frontmatter.sh завершился с кодом {code}:\n{output}")
    code, output = run(["./tools/validate-file-naming.sh"])
    if code != 0:
        errors.append(f"tools/validate-file-naming.sh завершился с кодом {code}:\n{output}")

    # Allowlist не должен маскировать новые нарушения: файл с неверным именем
    # обязан быть отклонён. Проба ставится в изолированной песочнице, а не в
    # рабочем дереве (issue #299): валидаторы запускаются параллельно, и запись
    # во время чужого прогона делала результат соседа недетерминированным.
    sandbox = Path(tempfile.mkdtemp(prefix="onboarding-selfcheck-"))
    try:
        shutil.copytree(REPO_ROOT / "tools", sandbox / "tools")
        probe_dir = sandbox / "docs/adr"
        probe_dir.mkdir(parents=True)
        (probe_dir / "validator-self-check.md").write_text(
            "---\nstatus: draft\n---\n", encoding="utf-8"
        )
        code, _ = run([str(sandbox / "tools/validate-file-naming.sh")])
        if code == 0:
            errors.append(
                "tools/validate-file-naming.sh пропустил файл с некорректным именем: "
                "allowlist маскирует новые нарушения"
            )
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)
    print("[D] валидаторы Хаба проходят, allowlist не маскирует новые нарушения")
    return errors


def main() -> int:
    errors = check_current() + check_archive() + check_navigation() + check_validators()
    if errors:
        print(f"\nFAIL: {len(errors)} проблем:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("\nOK: протокол онбординга актуализирован до v1.5, навигация согласована")
    return 0


if __name__ == "__main__":
    sys.exit(main())
