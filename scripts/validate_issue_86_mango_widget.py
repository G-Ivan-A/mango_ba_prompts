#!/usr/bin/env python3
"""Local regression check for issue #86 Mango Office widget integration."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(text: str, path: str, *needles: str) -> list[str]:
    return [f"{path}: missing {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    errors: list[str] = []

    index_html = read_text("site/index.html")
    changelog = read_text("CHANGELOG.md")

    widget_needles = (
        "<!-- Mango Office Widget -->",
        "(function(w, d, u, i, o, s, p) {",
        "d.getElementById(i)",
        "w['MangoObject'] = o",
        "s.async = 1",
        "s.id = i",
        "s.src = u",
        "s.charset = 'utf-8'",
        "//widgets.mango-office.ru/widgets/mango.js",
        "'mango-js'",
        "'mgo'",
        "mgo({multichannel: {id: 23303}});",
    )
    errors += require(index_html, "site/index.html", *widget_needles)

    if index_html.count("mgo({multichannel: {id: 23303}});") != 1:
        errors.append("site/index.html: expected exactly one Mango multichannel widget init")
    if index_html.count("id: 23303") != 1:
        errors.append("site/index.html: expected exactly one Mango multichannel id 23303")

    body_close_index = index_html.rfind("</body>")
    widget_index = index_html.find("<!-- Mango Office Widget -->")
    if body_close_index == -1:
        errors.append("site/index.html: missing closing </body> tag")
    elif widget_index == -1 or widget_index > body_close_index:
        errors.append("site/index.html: Mango Office widget must be placed before closing </body>")

    errors += require(changelog, "CHANGELOG.md", "Issue #86", "Mango Office Multichannel")

    if errors:
        print("issue-86 mango widget validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("issue-86 mango widget validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
