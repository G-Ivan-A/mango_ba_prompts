#!/usr/bin/env python3
"""Валидатор набора промптов BCREQ, legacy-каталога и сайта (issue #388).

Зачем: Задача 3 программы пересборки промптов BCREQ кладёт новый набор в
``prompts/``, выносит заменённые промпты в ``prompts/archive/`` и отражает всё
на сайте: метка и фильтр набора, копирование по иконке, ручной процесс БА,
согласование с командой и Заказчиком и парольный вход.

Проверки:

1. ``prompts/``: 14 файлов ``bcreq-*.md`` с frontmatter (``id`` =
   ``mango-<имя>``, ``status: draft``); Промпт 0 содержит защиты АД-1…АД-7;
   остальные 13 начинаются блоком «Пройдено / Текущий / Рекомендуемый
   следующий» и содержат «Состояние BCREQ»; ссылки — абсолютные URL.
2. Подкаталогов в ``prompts/`` нет, кроме ``archive/``; 18 заменённых
   промптов лежат в архиве со ``status: archived`` и баннером «Архив
   (issue #388)», в основном каталоге их нет.
3. Парольный вход: ``gate.js`` подключён во всех HTML-страницах сайта; запись
   ``"site"`` в ``password-hashes.json`` — соль и SHA-256; пароль открытым
   текстом не лежит на сайте и в документации (сверка по хэшу, сам пароль
   валидатор не знает). Если задан ``SITE_PASSWORD`` — хэш сверяется с ним.
4. Данные сайта: у промптов BCREQ ``family: bcreq`` и ``isNew``; фильтр
   «Набор»; ``bcreq-flow.json`` — 11 шагов ручного процесса, у каждого
   действующий промпт; пять этапов согласования с гейтами Г-IN, Г-С1, Г-W.
5. Интерфейс: ``app.js`` грузит данные после входа, рисует иконку копирования
   и процесс BCREQ; ``index.html`` содержит разделы процесса на вкладке
   «Процессы».
6. Документация: CHANGELOG, маршрутизация ``prompts/README.md``,
   ``docs/site-access.md`` (порядок смены пароля).

Запуск: ``python3 scripts/validate_issue_388_bcreq_site.py``
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
ARCHIVE = PROMPTS / "archive"
SITE = ROOT / "site"
BASE_URL = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"

BCREQ_PROMPTS = (
    "bcreq-constitution-governance-oneshot",
    "bcreq-context-understanding-stepwise",
    "bcreq-products-impact-analysis-stepwise",
    "bcreq-in-understanding-oneshot",
    "bcreq-fr-documentation-stepwise",
    "bcreq-nfr-documentation-stepwise",
    "bcreq-uc-modeling-stepwise",
    "bcreq-core-documentation-oneshot",
    "bcreq-orr-solution-design-stepwise",
    "bcreq-constraints-documentation-stepwise",
    "bcreq-extra-risk-analysis-stepwise",
    "bcreq-work-solution-design-oneshot",
    "bcreq-review-validation-oneshot",
    "bcreq-scenarios-modeling-oneshot",
)
CONSTITUTION = BCREQ_PROMPTS[0]
ARCHIVED_PROMPTS = (
    "constraints-documentation-oneshot", "constraints-documentation-stepwise",
    "fr-documentation-oneshot", "fr-documentation-stepwise",
    "fr-validation-legacy", "fr-validation-oneshot", "fr-validation-stepwise",
    "glossary-context-understanding-oneshot", "glossary-context-understanding-stepwise",
    "questions-customer-understanding-legacy", "questions-customer-understanding-stepwise",
    "technical-details-solution-design-legacy", "technical-details-solution-design-oneshot",
    "technical-details-solution-design-stepwise",
    "uc-modeling-oneshot", "uc-modeling-stepwise",
    "us-modeling-oneshot", "us-modeling-stepwise",
)
POSITION_MARKERS = ("**Пройдено:**", "**Текущий:**", "**Рекомендуемый следующий:**")

GATED_PAGES = {
    SITE / "index.html": '<script src="gate.js"></script>',
    SITE / "reports" / "index.html": '<script src="../gate.js" data-base="../"></script>',
    SITE / "reports" / "run-0060" / "index.html": '<script src="../../gate.js" data-base="../../"></script>',
    SITE / "reports" / "run-0060" / "detailed-gap-report.html":
        '<script src="../../gate.js" data-base="../../"></script>',
}
# Где пароль открытым текстом запрещён: страницы и данные сайта, документация.
NO_PLAINTEXT = (SITE, ROOT / "docs", ROOT / "README.md", PROMPTS / "README.md", ROOT / "CHANGELOG.md")
TEXT_SUFFIXES = {".md", ".html", ".js", ".json", ".css", ".txt", ".csv", ".yml", ".yaml"}

MANUAL_TITLE = "Создание спецификации бизнес-требований и дизайна решения (BCREQ)"
APPROVAL_TITLE = "Согласование BCREQ с командой и Заказчиком"
APPROVAL_PDF = "https://github.com/user-attachments/files/33892143/KK-289887877-231026-2259-652.pdf"

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "-")):
            fields[key.strip()] = value.strip().strip('"')
    return fields


def check_prompts() -> list[str]:
    errors = []
    actual = sorted(p.stem for p in PROMPTS.glob("bcreq-*.md"))
    if actual != sorted(BCREQ_PROMPTS):
        errors.append(f"prompts/bcreq-*.md: ожидалось {len(BCREQ_PROMPTS)} файлов набора, найдено {actual}")
    for name in BCREQ_PROMPTS:
        path = PROMPTS / f"{name}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("id") != f"mango-{name}":
            errors.append(f"{name}: id во frontmatter должен быть mango-{name}")
        if meta.get("status") != "draft":
            errors.append(f"{name}: status должен быть draft")
        if name == CONSTITUTION:
            missing = [f"АД-{n}" for n in range(1, 8) if f"АД-{n}" not in text]
            if missing:
                errors.append(f"{name}: нет защит {', '.join(missing)}")
        else:
            missing = [m for m in POSITION_MARKERS if m not in text]
            if missing:
                errors.append(f"{name}: нет блока позиции {missing}")
            if "Состояние BCREQ" not in text:
                errors.append(f"{name}: нет блока «Состояние BCREQ»")
            if f"{BASE_URL}prompts/{CONSTITUTION}.md" not in text:
                errors.append(f"{name}: нет ссылки на Промпт 0")
        relative = [t for t in LINK.findall(text) if not t.startswith(("https://", "#"))]
        if relative:
            errors.append(f"{name}: ссылки должны быть абсолютными URL: {relative[:3]}")
    return errors


def check_archive() -> list[str]:
    errors = []
    subdirs = sorted(p.name for p in PROMPTS.iterdir() if p.is_dir())
    if subdirs != ["archive"]:
        errors.append(f"prompts/: допустим только подкаталог archive/, найдено {subdirs}")
    for name in ARCHIVED_PROMPTS:
        if (PROMPTS / f"{name}.md").exists():
            errors.append(f"prompts/{name}.md: заменённый промпт остался в основном каталоге")
        path = ARCHIVE / f"{name}.md"
        if not path.exists():
            errors.append(f"prompts/archive/{name}.md: нет файла в архиве")
            continue
        text = path.read_text(encoding="utf-8")
        if frontmatter(text).get("status") != "archived":
            errors.append(f"prompts/archive/{name}.md: status должен быть archived")
        if "**Архив (issue #388).**" not in text or f"{BASE_URL}prompts/bcreq-" not in text:
            errors.append(f"prompts/archive/{name}.md: нет баннера архива со ссылкой на замену BCREQ")
    return errors


def plaintext_hits(entry: dict) -> list[str]:
    """Файлы, где встречается слово, хэш которого совпадает с паролем сайта."""
    salt, expected = entry["salt"], entry["hash"]
    seen: dict[str, bool] = {}
    hits = []
    files: list[Path] = []
    for root in NO_PLAINTEXT:
        files.extend([root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file()))
    for path in files:
        if path.suffix not in TEXT_SUFFIXES or path.name == "password-hashes.json":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for word in set(re.findall(r"[^\W_]{3,40}", text)):
            key = word.upper()
            if key not in seen:
                digest = hashlib.sha256((salt + key).encode("utf-8")).hexdigest()
                seen[key] = digest == expected
            if seen[key]:
                hits.append(str(path.relative_to(ROOT)))
                break
    return hits


def check_gate() -> list[str]:
    errors = []
    gate = SITE / "gate.js"
    if not gate.exists():
        return ["site/gate.js: нет скрипта парольного входа"]
    gate_text = gate.read_text(encoding="utf-8")
    for needle in ("password-hashes.json", 'const ENTRY = "site"', "crypto.subtle.digest", "window.siteGate"):
        if needle not in gate_text:
            errors.append(f"site/gate.js: нет {needle!r}")
    for page, tag in GATED_PAGES.items():
        rel = page.relative_to(ROOT)
        if not page.exists():
            errors.append(f"{rel}: нет страницы")
            continue
        html = page.read_text(encoding="utf-8")
        head = html.split("</head>", 1)[0]
        if tag not in head:
            errors.append(f"{rel}: в <head> нет подключения {tag}")
    hashes = json.loads((SITE / "password-hashes.json").read_text(encoding="utf-8"))
    entry = hashes.get("site") or {}
    if set(entry) != {"algorithm", "salt", "hash"}:
        errors.append('site/password-hashes.json: запись "site" — только algorithm, salt, hash')
        return errors
    if not re.fullmatch(r"[0-9a-f]{16}", entry["salt"]) or not re.fullmatch(r"[0-9a-f]{64}", entry["hash"]):
        errors.append('site/password-hashes.json: запись "site" — соль 16 hex и SHA-256 64 hex')
        return errors
    password = os.environ.get("SITE_PASSWORD")
    if password:
        digest = hashlib.sha256((entry["salt"] + password.strip().upper()).encode("utf-8")).hexdigest()
        if digest != entry["hash"]:
            errors.append('site/password-hashes.json: хэш "site" не совпадает с SITE_PASSWORD')
    for rel in plaintext_hits(entry):
        errors.append(f"{rel}: пароль сайта открытым текстом (запрет issue #388)")
    return errors


def check_site_data() -> list[str]:
    errors = []
    data = json.loads((SITE / "data" / "prompts.json").read_text(encoding="utf-8"))
    by_file = {Path(p.get("sourcePath", "")).name: p for p in data["prompts"]}
    by_id = {p["id"]: p for p in data["prompts"]}
    for name in BCREQ_PROMPTS:
        prompt = by_file.get(f"{name}.md")
        if not prompt:
            errors.append(f"site/data/prompts.json: нет промпта {name}")
        elif prompt.get("family") != "bcreq" or prompt.get("isNew") is not True:
            errors.append(f"site/data/prompts.json: {name} — нужны family=bcreq и isNew=true")
    families = {f.get("id") for f in data.get("filters", {}).get("families", [])}
    if not {"bcreq", "archive"} <= families:
        errors.append(f"site/data/prompts.json: фильтр «Набор» без bcreq/archive: {sorted(families)}")

    flow = json.loads((SITE / "data" / "bcreq-flow.json").read_text(encoding="utf-8"))
    steps = flow["manual"]["steps"]
    if len(steps) != 11:
        errors.append(f"bcreq-flow.json: ожидалось 11 шагов ручного процесса, найдено {len(steps)}")
    if flow["manual"]["route"] != "stepwise" or flow["manual"]["title"] != MANUAL_TITLE:
        errors.append("bcreq-flow.json: ручной процесс — stepwise с названием раздела по issue #388")
    for step in steps:
        prompt = by_id.get(step["prompt"]["id"])
        if not prompt or prompt.get("family") != "bcreq":
            errors.append(f"bcreq-flow.json: шаг {step['step']} — промпт {step['prompt']['id']} не из набора BCREQ")
        if not step["actions"]:
            errors.append(f"bcreq-flow.json: шаг {step['step']} без инструкций БА")
    approval = flow["approval"]
    gates = {stage["gate"] for stage in approval["stages"]}
    if len(approval["stages"]) != 5 or not {"Г-IN", "Г-С1", "Г-W"} <= gates:
        errors.append(f"bcreq-flow.json: согласование — 5 этапов с гейтами Г-IN, Г-С1, Г-W; найдено {sorted(gates)}")
    if approval["basis"]["url"] != APPROVAL_PDF:
        errors.append("bcreq-flow.json: основа согласования — приложенный PDF issue #388")
    if not approval["improvements"] or not approval["returns"]:
        errors.append("bcreq-flow.json: нет усовершенствований или возвратов процесса согласования")
    return errors


def check_ui() -> list[str]:
    errors = []
    app = (SITE / "app.js").read_text(encoding="utf-8")
    for needle in (
        "window.siteGate?.ready", 'fetch("data/bcreq-flow.json")', "function renderBcreqFlow",
        "function copyIconButton", 'selectedValues("family")', "★ BCREQ · новый", "nodes.bcreqSteps?.addEventListener",
    ):
        if needle not in app:
            errors.append(f"site/app.js: нет {needle!r}")
    html = (SITE / "index.html").read_text(encoding="utf-8")
    for section, title in (("bcreq-manual", MANUAL_TITLE), ("bcreq-approval", APPROVAL_TITLE)):
        match = re.search(rf'<section[^>]*id="{section}"[^>]*>', html)
        if not match or 'data-page="processes"' not in match.group(0):
            errors.append(f"site/index.html: нет раздела #{section} на вкладке «Процессы»")
        if f">{title}</h2>" not in html:
            errors.append(f"site/index.html: нет заголовка «{title}»")
    return errors


def check_docs() -> list[str]:
    errors = []
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    unreleased = changelog.split("## Unreleased", 1)[-1].split("\n## ", 1)[0]
    if "Issue #388" not in unreleased:
        errors.append("CHANGELOG.md: нет записи Issue #388 в Unreleased")
    readme = (PROMPTS / "README.md").read_text(encoding="utf-8")
    for name in BCREQ_PROMPTS:
        if f"{BASE_URL}prompts/{name}.md" not in readme:
            errors.append(f"prompts/README.md: нет маршрута на {name}.md")
    if f"{BASE_URL}docs/ba-processes/bcreq-manual-process.md" not in readme:
        errors.append("prompts/README.md: нет ссылки на ручной процесс BCREQ")
    access = ROOT / "docs" / "site-access.md"
    if not access.exists():
        errors.append("docs/site-access.md: нет порядка смены пароля")
    elif "scripts/set-site-password.mjs" not in access.read_text(encoding="utf-8"):
        errors.append("docs/site-access.md: нет команды смены пароля")
    return errors


def main() -> int:
    errors = check_prompts() + check_archive() + check_gate() + check_site_data() + check_ui() + check_docs()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"OK: issue #388 — {len(BCREQ_PROMPTS)} промптов BCREQ, {len(ARCHIVED_PROMPTS)} в архиве, "
          f"парольный вход на {len(GATED_PAGES)} страницах, процесс BCREQ и согласование на сайте")
    return 0


if __name__ == "__main__":
    sys.exit(main())
