#!/usr/bin/env python3
"""Local regression check for issue #103: UI catalog fixes.

Locks the requirements:
- ФТ-1: top card arrow removed; bottom has "Перейти в репо" button with repo link;
- ФТ-2: status filter block removed from renderFilters;
- ФТ-3: filter groups visually separated (border, background, bold titles);
- ФТ-4: date sort descending by default (↓ indicator in option);
- ФТ-5: sort/export toolbar above search; export button has clear label;
- ФТ-6: "Очистить поиск" and "Сбросить фильтры" buttons present.
"""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def forbid(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: must not contain {needle!r}" for needle in needles if needle in text]


def main() -> int:
    errors: list[str] = []

    index_html = read_text("site/index.html")
    app_js = read_text("site/app.js")
    styles_css = read_text("site/styles.css")

    # --- ФТ-1: prompt card ---------------------------------------------------
    card_match = re.search(
        r"function promptCard\(prompt\)\s*\{(.+?)^}", app_js, re.DOTALL | re.MULTILINE
    )
    if not card_match:
        errors.append("site/app.js: promptCard function not found")
    else:
        card_body = card_match.group(1)
        # Top arrow removed: source-link must not appear in the head construction.
        if re.search(r'el\("a",\s*"source-link"', card_body):
            errors.append("site/app.js: promptCard must not have source-link (top arrow) in head")
        # Repo link button present at the bottom.
        if "repo-link" not in card_body:
            errors.append("site/app.js: promptCard must contain 'repo-link' button")
        if "Перейти в репо" not in card_body:
            errors.append("site/app.js: promptCard must contain 'Перейти в репо' text")
        # Repo link URL must point to GitHub prompt file.
        if "prompt.url" not in card_body:
            errors.append("site/app.js: promptCard repo-link must use prompt.url")

    # --- ФТ-2: status filter removed -----------------------------------------
    render_filters_match = re.search(
        r"function renderFilters\(\)\s*\{(.+?)^}", app_js, re.DOTALL | re.MULTILINE
    )
    if not render_filters_match:
        errors.append("site/app.js: renderFilters function not found")
    else:
        rf_body = render_filters_match.group(1)
        if '"Статус"' in rf_body or "renderFilterGroup(\"Статус\"" in rf_body:
            errors.append("site/app.js: renderFilters must not render status filter group")
        if "status:${status}" in rf_body:
            errors.append("site/app.js: renderFilters must not generate status: filter tokens")

    # --- ФТ-3: filter group visual separation --------------------------------
    if ".filter-group--processes" not in styles_css:
        errors.append("site/styles.css: missing .filter-group--processes style")
    if ".filter-group--operations" not in styles_css:
        errors.append("site/styles.css: missing .filter-group--operations style")
    if ".filter-group--modes" not in styles_css:
        errors.append("site/styles.css: missing .filter-group--modes style")
    # Filter group must have border and background styling.
    filter_group_match = re.search(r"\.filter-group\s*\{([^}]+)\}", styles_css)
    if filter_group_match:
        fg_body = filter_group_match.group(1)
        if "border" not in fg_body:
            errors.append("site/styles.css: .filter-group must have border styling")
        if "background" not in fg_body:
            errors.append("site/styles.css: .filter-group must have background styling")
    else:
        errors.append("site/styles.css: .filter-group rule not found")

    # --- ФТ-4: date sort descending indicator --------------------------------
    if "По дате ↓" not in index_html and "По дате обновления ↓" not in index_html:
        errors.append("site/index.html: sort option must show descending indicator (↓) for date sort")

    # --- ФТ-5: toolbar layout (sort + export above search) -------------------
    if "toolbar-top" not in index_html:
        errors.append("site/index.html: must have toolbar-top container (sort/export row)")
    if "toolbar-bottom" not in index_html:
        errors.append("site/index.html: must have toolbar-bottom container (search row)")
    # Export button must have a text label.
    if "Скачать" not in index_html:
        errors.append("site/index.html: export button must have text label 'Скачать'")
    if "export-button" not in index_html:
        errors.append("site/index.html: export-button element required")
    # Sort control must be above search in the DOM.
    sort_pos = index_html.find("sort-select")
    search_pos = index_html.find("search-input")
    if sort_pos == -1 or search_pos == -1:
        errors.append("site/index.html: sort-select and search-input must be present")
    elif sort_pos > search_pos:
        errors.append("site/index.html: sort-select must appear before search-input in DOM")

    # --- ФТ-6: clear search + reset filters buttons --------------------------
    if "clear-search-button" not in index_html:
        errors.append("site/index.html: missing clear-search-button element")
    if "clear-filters-button" not in index_html:
        errors.append("site/index.html: missing clear-filters-button element")
    if "Очистить поиск" not in index_html:
        errors.append("site/index.html: missing 'Очистить поиск' button text")
    if "Сбросить фильтры" not in index_html:
        errors.append("site/index.html: missing 'Сбросить фильтры' button text")
    # Buttons start as hidden (only shown when active).
    if 'id="clear-search-button"' in index_html and "hidden" not in index_html[
        index_html.find('id="clear-search-button"') - 200:
        index_html.find('id="clear-search-button"') + 200
    ]:
        errors.append("site/index.html: clear-search-button must start as hidden")
    # Event handlers wired in app.js.
    if "clearSearch" not in app_js and "clear-search-button" not in app_js:
        errors.append("site/app.js: clear search button handler missing")
    if "clearFilters" not in app_js and "clear-filters-button" not in app_js:
        errors.append("site/app.js: clear filters button handler missing")
    if "updateClearButtonVisibility" not in app_js:
        errors.append("site/app.js: updateClearButtonVisibility function missing")

    if errors:
        print("issue-103 ui-fixes validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-103 ui-fixes validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
