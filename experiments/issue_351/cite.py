"""Резолвер атомарных ссылок [ИСТОЧНИК, §X, с.Y].

Номера страниц НИКОГДА не задаются в коде: они читаются из frontmatter
раздела kb/processed в момент генерации отчёта. Это структурно устраняет
корневую причину дефекта RUN-0065 (сдвиг пагинации в ссылках).
"""
import os
import re

from evidence import EVIDENCE, WEB

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_cache = {}


def _frontmatter(path):
    if path in _cache:
        return _cache[path]
    text = open(os.path.join(REPO, path), encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("no frontmatter: " + path)
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^([a-z_]+):\s*(.*?)\s*$', line)
        if km:
            value = km.group(2)
            if len(value) > 1 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            fm[km.group(1)] = value
    _cache[path] = fm
    return fm


def cite(key, rel_prefix="../../../../"):
    """Возвращает markdown-ссылку с достоверными §/страницами из БЗ."""
    if key.startswith("web."):
        url, title = WEB[key]
        return "[%s](%s)" % (title, url)
    path = EVIDENCE[key]
    fm = _frontmatter(path)
    doc = fm.get("doc_code") or fm.get("source") or "kb"
    sec = fm.get("pdf_section", "")
    if sec in ("", "-", "\u2014"):
        sec = fm.get("section", "")
    if sec in ("", "0", "-", "\u2014"):
        sec = ""
    pages = fm.get("pages") or "n/a"
    title = fm.get("title", "")
    if sec:
        label = "%s, \u00a7%s \u00ab%s\u00bb, \u0441.%s" % (doc, sec, title, pages)
    else:
        label = "%s, \u00ab%s\u00bb, \u0441.%s" % (doc, title, pages)
    return "[%s](%s%s)" % (label, rel_prefix, path)


def cites(keys, rel_prefix="../../../../"):
    return " ".join(cite(k, rel_prefix) for k in keys)
