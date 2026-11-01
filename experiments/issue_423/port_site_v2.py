#!/usr/bin/env python3
"""Port the issue #420 site-v2 pages into the live site (issue #423).

Issue #423 DoD: «сайт содержит страницы: о проекте, каталог, стандарты,
дашборд, справочник». The texts of these pages were approved in PR #422
(experiments/issue_420/site-v2/content.py, RFC appendix) but deliberately not
published there («не меняем страницы сайта»). This script publishes them.

content.py and build.py of issue #420 are read-only inputs: they are imported,
and only the facts that PR #422 itself made stale are overridden in memory
(OVERRIDES below). The RFC, its appendix and pages.md are not touched.

Changes applied to site/:
- index.html: menu О проекте · Каталог · Стандарты · Процессы · Дашборд ·
  Справочник; sections #about and #glossary; the Standards page by the v0.2
  template; the two process streams as collapsible <details>; the
  «Версия сайта» panel on #about (filled by app.js from stats.json);
- v2.css, v2.js copied from experiments/issue_420/site-v2/;
- app.js: PAGES gain about/glossary, #standards?section=0 opens the intro.

Usage:
    python3 experiments/issue_423/port_site_v2.py           # apply (idempotent)
    python3 experiments/issue_423/port_site_v2.py --check   # verify site/ is in sync
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
V2 = ROOT / "experiments" / "issue_420" / "site-v2"
SITE = ROOT / "site"
REPO = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main"

sys.path.insert(0, str(V2))
_spec = importlib.util.spec_from_file_location("issue_420_site_v2_build", V2 / "build.py")
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)  # imports content.py as B.C; nothing is written
C = B.C

# ------------------------------------------------------------------ overrides
# Only facts changed by PR #422 / issue #423; everything else is content.py as approved.
GLOSSARY_OVERRIDES = {
    "sh": (
        "sh", "Ш-1 … Ш-39", "Шаги ручного процесса",
        "Порядок запуска 39 классов промптов BCREQ на странице «Процессы»: один шаг — один класс C01–C39 по процессу v0.2.",
        "Ручной процесс BCREQ", f"{REPO}/docs/ba-processes/bcreq-manual-process.md", "process",
    ),
    "prompt": (
        "prompt", "Промпт", "Инструкция для модели",
        "Текст, который БА копирует в чат с моделью на шаге процесса. Каталог — 39 классов ручного процесса BCREQ; 14 промптов этапа 1 — в архиве каталога.",
        "Классы ручных промптов BCREQ", f"{REPO}/standards/bcreq-manual-classes/README.md", "project",
    ),
}
GLOSSARY_ADDITIONS = [
    ("class", "C01–C39", "Класс ручного промпта BCREQ",
     "Стандарт одного вызова модели: вход, выход, стоп-условие и проверки. Каталог сайта показывает 39 классов; номер класса не равен номеру шага.",
     "Классы ручных промптов BCREQ", f"{REPO}/standards/bcreq-manual-classes/README.md", "project"),
    ("state", "Контракт состояния", "Общие правила ручного чата BCREQ",
     "Документ, который БА вставляет вместе с каждым классом: подготовка вызова, блок BCREQ_OUTPUT, перенос в новый чат.",
     "Контракт состояния", f"{REPO}/docs/contracts/bcreq-manual-state.md", "project"),
    ("archive", "Архив", "14 промптов этапа 1",
     "Промпты prompts/bcreq-*.md, заменённые 39 классами. Видны в каталоге при фильтре «Архив»; файлы сохранены для ссылок из стандартов, RFC и прогонов.",
     "Каталог промптов", f"{REPO}/prompts/README.md", "project"),
]
ZONE_OVERRIDES = {
    "catalog": "39 классов промптов BCREQ с фильтрами; 14 промптов этапа 1 — в архиве.",
    "processes": "Маршрут 39 классов по стадиям, шаги Ш-1…Ш-39 и согласование документа.",
}


def apply_overrides() -> None:
    C.GLOSSARY = [GLOSSARY_OVERRIDES.get(item[0], item) for item in C.GLOSSARY] + GLOSSARY_ADDITIONS
    C.TERM_BY_LABEL = {item[1]: item[0] for item in C.GLOSSARY}
    C.TERM_BY_LABEL.update({"В-Д": "vd", "В-Н": "vd", "Ш-В": "sh", "Ш-0": "sh", "Ш-1": "sh"})
    C.TERM_IDS = {item[0] for item in C.GLOSSARY}
    C.ABOUT = dict(C.ABOUT)
    C.ABOUT["zones"] = [(name, page, ZONE_OVERRIDES.get(page, text)) for name, page, text in C.ABOUT["zones"]]


ABOUT_VERSION_PANEL = (
    '        <article class="v2-panel" id="about-version" aria-live="polite"><h2>Версия сайта</h2></article>\n'
)


# ------------------------------------------------------------------ helpers
def section_span(src: str, section_id: str) -> tuple[int, int]:
    """Span of <section … id="section_id" …>…</section>, nested sections included."""
    m = re.search(rf'<section\b[^>]*\bid="{re.escape(section_id)}"', src)
    if not m:
        raise SystemExit(f"index.html: section #{section_id} not found")
    depth = 0
    for tag in re.finditer(r"<(/?)section\b", src[m.start():]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            end = m.start() + tag.start()
            return m.start(), src.index(">", end) + 1
    raise SystemExit(f"index.html: section #{section_id} is not closed")


def about_html() -> str:
    html = B.about_html().strip()
    marker = '        <article class="v2-panel"><h2>Этапы автоматизации</h2>'
    if marker not in html:
        raise SystemExit("about: stages panel not found")
    return html.replace(marker, ABOUT_VERSION_PANEL + marker, 1)


def port_index(src: str) -> str:
    if 'data-page="about"' not in src:
        # First port: the issue #420 patch (menu, css/js links, streams), then our sections.
        src = B.patch_index(src)
    # (Re)generate the sections owned by content.py so the port stays idempotent.
    for sid, html in (("about", about_html()), ("standards", B.standards_html().strip()), ("glossary", B.glossary_html().strip())):
        start, end = section_span(src, sid)
        src = src[:start] + html + src[end:]
    nav_start = src.index('<nav class="topnav"')
    first = src.index("<a ", nav_start)
    nav_end = src.index("        <button\n          class=\"icon-button\"\n          id=\"site-logout\"", nav_start)
    src = src[:first - 8] + B.nav_html() + "\n" + src[nav_end:]
    src = src.replace('<a class="brand" href="#catalog"', '<a class="brand" href="#about"', 1)
    return src


def port_app(js: str) -> str:
    for old, new in B.APP_JS_PATCHES:
        if new in js:
            continue
        js = B.replace_once(js, old, new, "app.js")
    return js


def targets() -> dict[Path, str]:
    apply_overrides()
    return {
        SITE / "index.html": port_index((SITE / "index.html").read_text(encoding="utf-8")),
        SITE / "app.js": port_app((SITE / "app.js").read_text(encoding="utf-8")),
        SITE / "v2.css": (V2 / "v2.css").read_text(encoding="utf-8"),
        SITE / "v2.js": (V2 / "v2.js").read_text(encoding="utf-8"),
    }


def main(argv: list[str]) -> int:
    expected = targets()
    if "--check" in argv:
        stale = [p for p, text in expected.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        for path in stale:
            print("ERROR: stale, run port_site_v2.py:", path.relative_to(ROOT))
        print("site-v2 port:", "FAIL" if stale else "in sync")
        return 1 if stale else 0
    for path, text in expected.items():
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
