#!/usr/bin/env python3
"""Валидатор сайта версии 2 (issue #423): визуализация PR #422.

Зачем: issue #423 обновляет сайт по PR #422 — 39 классов ручных промптов
BCREQ вместо 14 промптов этапа 1, процесс BCREQ v0.2 и страницы, одобренные
в RFC страницы «Стандарты» v0.2. Валидатор фиксирует критерии готовности:

1. Страницы: меню «О проекте · Каталог · Стандарты · Процессы · Дашборд ·
   Справочник», у каждого пункта есть раздел ``data-page`` и маршрут в
   ``PAGES`` (``site/app.js``).
2. Каталог: 39 действующих классов — ровно файлы
   ``standards/bcreq-manual-classes/NN-*.md``, ``classId`` C01–C39 как в
   ``catalog.json``; 14 промптов ``prompts/bcreq-*.md`` — в архиве каталога
   (``family: archive``, ``archived``), ``successors`` совпадают с полем
   ``existing`` в ``catalog.json``. Тексты промптов на сайте совпадают с
   файлами (промпты не дорабатываются — вне рамок issue).
3. Процесс BCREQ: ``bcreq-flow.json`` — 39 шагов Ш-1…Ш-39, каждый класс
   ровно один раз, шаги по стадиям A-IN…A-RELEASE; документ процесса
   синхронизирован с классами (``build_process_steps.py --check``).
4. Страницы PR #422 опубликованы без расхождений с прототипом
   (``port_site_v2.py --check``).
5. Версия сайта вычислена и записана: ``stats.json → siteVersion`` (SemVer),
   та же версия в шапке и подвале ``index.html`` и в CHANGELOG (Issue #423).

Запуск: ``python3 scripts/validate_issue_423_site.py``
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CLASSES = ROOT / "standards" / "bcreq-manual-classes"
NAV = ["about", "catalog", "standards", "processes", "dashboard", "glossary"]
REQUIRED_PAGES = {"about", "catalog", "standards", "dashboard", "glossary"}  # DoD issue #423
STAGES = ["A-IN · Приём задачи", "A-CORE · Требования", "A-WORK · Решение", "A-RELEASE · Выпуск"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def load(name: str) -> dict:
    return json.loads((SITE / "data" / name).read_text(encoding="utf-8"))


def check_pages() -> list[str]:
    errors = []
    html = (SITE / "index.html").read_text(encoding="utf-8")
    nav = re.findall(r'data-nav="([a-z]+)"', html)
    if nav != NAV:
        errors.append(f"site/index.html: меню {nav}, ожидалось {NAV}")
    if not REQUIRED_PAGES <= set(nav):
        errors.append(f"site/index.html: нет страниц {sorted(REQUIRED_PAGES - set(nav))}")
    pages = set(re.findall(r'<section\b[^>]*data-page="([a-z]+)"', html))
    for page in NAV:
        if page not in pages:
            errors.append(f"site/index.html: нет раздела data-page={page!r}")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    match = re.search(r"const PAGES = \[([^\]]*)\]", app)
    routes = set(re.findall(r'"([a-z]+)"', match.group(1))) if match else set()
    if not set(NAV) <= routes:
        errors.append(f"site/app.js: PAGES без {sorted(set(NAV) - routes)}")
    for asset in ("v2.css", "v2.js"):
        if asset not in html:
            errors.append(f"site/index.html: не подключён {asset}")
    return errors


def check_catalog() -> list[str]:
    errors = []
    data = load("prompts.json")
    catalog = json.loads((CLASSES / "catalog.json").read_text(encoding="utf-8"))["classes"]
    class_files = {str(p.relative_to(ROOT)) for p in CLASSES.glob("[0-9][0-9]-*.md")}
    archive_files = {str(p.relative_to(ROOT)) for p in (ROOT / "prompts").glob("bcreq-*.md")}
    if len(class_files) != 39 or len(catalog) != 39:
        errors.append(f"standards/bcreq-manual-classes: ожидалось 39 классов, файлов {len(class_files)}, в catalog.json {len(catalog)}")
    if len(archive_files) != 14:
        errors.append(f"prompts/: ожидалось 14 промптов этапа 1, найдено {len(archive_files)}")

    active = [p for p in data["prompts"] if not p.get("archived")]
    archived = [p for p in data["prompts"] if p.get("archived")]
    if {p["sourcePath"] for p in active} != class_files:
        errors.append("prompts.json: действующий каталог не совпадает с 39 файлами классов")
    if {p["sourcePath"] for p in archived} != archive_files:
        errors.append("prompts.json: архив не совпадает с 14 промптами prompts/bcreq-*.md")
    if sorted(p.get("classId") for p in active) != sorted(item["id"] for item in catalog):
        errors.append("prompts.json: classId действующих промптов не совпадают с catalog.json")
    for prompt in active:
        if prompt.get("family") != "bcreq" or prompt.get("mode") != "manual":
            errors.append(f"prompts.json: {prompt['id']} — нужны family=bcreq и mode=manual")
        if not prompt.get("processes") or not set(prompt["processes"]) <= set(STAGES):
            errors.append(f"prompts.json: {prompt['id']} — стадии вне A-IN…A-RELEASE: {prompt.get('processes')}")

    successors: dict[str, list[str]] = {}
    for item in catalog:
        successors.setdefault(Path(item.get("existing", "")).name, []).append(item["id"])
    for prompt in archived:
        if prompt.get("family") != "archive":
            errors.append(f"prompts.json: {prompt['id']} — архивный промпт без family=archive")
        expected = successors.get(Path(prompt["sourcePath"]).name, [])
        if prompt.get("successors") != expected:
            errors.append(f"prompts.json: {prompt['id']} — successors {prompt.get('successors')} != catalog.json {expected}")

    for prompt in data["prompts"]:
        if prompt["content"] != (ROOT / prompt["sourcePath"]).read_text(encoding="utf-8"):
            errors.append(f"prompts.json: текст {prompt['sourcePath']} отличается от файла (перегенерируйте данные)")

    families = [f["id"] for f in data["filters"]["families"]]
    if sorted(families) != ["archive", "bcreq"]:
        errors.append(f"prompts.json: фильтр «Набор» — bcreq и archive, найдено {families}")
    if [p["label"] for p in data["filters"]["processes"]] != STAGES:
        errors.append("prompts.json: фильтр стадий — A-IN, A-CORE, A-WORK, A-RELEASE")

    totals = load("stats.json")["totals"]
    for key, value in (("activePrompts", 39), ("archivedPrompts", 14), ("allPrompts", 53)):
        if totals.get(key) != value:
            errors.append(f"stats.json: totals.{key}={totals.get(key)}, ожидалось {value}")
    return errors


def check_process() -> list[str]:
    errors = []
    manual = load("bcreq-flow.json")["manual"]
    steps = manual["steps"]
    if [s["number"] for s in steps] != list(range(1, 40)):
        errors.append("bcreq-flow.json: шаги должны идти Ш-1…Ш-39 по порядку")
    for step in steps:
        if not step["step"].startswith(f"Ш-{step['number']} "):
            errors.append(f"bcreq-flow.json: шаг {step['number']} назван {step['step']!r}")
        if not step.get("stages") or not step.get("actions") or not step.get("result"):
            errors.append(f"bcreq-flow.json: шаг {step['step']} без стадий, действий или результата")
    classes = [s["prompt"].get("classId") for s in steps]
    if sorted(classes) != [f"C{n:02d}" for n in range(1, 40)]:
        errors.append("bcreq-flow.json: каждый из 39 классов должен встречаться ровно в одном шаге")
    if manual.get("route") != "manual" or len(manual.get("sequences", [])) != 4:
        errors.append("bcreq-flow.json: маршрут manual и 4 последовательности стадий")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    for needle in ("function renderBcreqRoute", "#processes?step=", "bcreq-step-"):
        if needle not in app:
            errors.append(f"site/app.js: нет {needle!r}")
    html = (SITE / "index.html").read_text(encoding="utf-8")
    if 'id="bcreq-route"' not in html or "Ш-1…Ш-39" not in html:
        errors.append("site/index.html: нет маршрута по стадиям или шагов Ш-1…Ш-39")
    return errors


def check_generated() -> list[str]:
    errors = []
    for script in ("experiments/issue_423/build_process_steps.py", "experiments/issue_423/port_site_v2.py"):
        result = subprocess.run([sys.executable, script, "--check"], cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            errors.append(f"{script} --check: {(result.stdout + result.stderr).strip()}")
    return errors


def check_version() -> list[str]:
    errors = []
    version = load("stats.json").get("siteVersion", {})
    number = version.get("version", "")
    if not SEMVER.match(number):
        errors.append(f"stats.json: siteVersion.version {number!r} — не SemVer")
        return errors
    if version.get("issue") != 423 or not version.get("released") or not version.get("basis"):
        errors.append("stats.json: siteVersion без issue, даты или основания")
    if load("prompts.json").get("siteVersion") != version:
        errors.append("prompts.json: siteVersion не совпадает со stats.json")
    html = (SITE / "index.html").read_text(encoding="utf-8")
    shown = re.findall(r"data-site-version[^>]*>v([^<]+)<", html)
    if len(shown) < 2 or set(shown) != {number}:
        errors.append(f"site/index.html: версия в шапке и подвале {shown}, ожидалось v{number}")
    if 'id="about-version"' not in html:
        errors.append("site/index.html: нет панели «Версия сайта» на странице «О проекте»")
    app = (SITE / "app.js").read_text(encoding="utf-8")
    if "function renderSiteVersion" not in app:
        errors.append("site/app.js: нет renderSiteVersion")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    unreleased = changelog.split("## Unreleased", 1)[-1].split("\n## ", 1)[0]
    if "Issue #423" not in unreleased or f"версия сайта {number}" not in unreleased.lower():
        errors.append(f"CHANGELOG.md: нет записи Issue #423 с «версия сайта {number}»")
    return errors


def main() -> int:
    errors = check_pages() + check_catalog() + check_process() + check_generated() + check_version()
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("OK: issue #423 — 6 страниц, 39 классов и архив 14, Ш-1…Ш-39, версия сайта записана")
    return 0


if __name__ == "__main__":
    sys.exit(main())
