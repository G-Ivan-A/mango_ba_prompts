#!/usr/bin/env python3
"""Выгружает публичную базу знаний TWIN (https://wiki.twin24.ai/ru/) для #325.

Зачем понадобилось: RUN-0057 зафиксировал в `logs/source-availability.md`, что
публичные материалы twin24.ai «носят маркетинговый характер», и колонка «У2 (twin)»
матрицы исполнимости осталась пустой. Проверка показала обратное — у платформы есть
открытая техническая вики на Wiki.js.

Особенности API, из-за которых нужен именно этот скрипт:

* GraphQL-запрос `pages.list` открыт без авторизации и отдаёт перечень страниц
  (сохранён в `pages.json`), а `pages.single` закрыт — `PageViewForbidden (6013)`;
  поэтому текст берётся не из API, а из отрендеренного HTML страницы;
* кириллица в путях требует `urllib.parse.quote`, иначе `urllib` падает на
  `'ascii' codec can't encode`.

Результат — `wiki/pages_full.json` (путь, заголовок, URL, текст) — рабочий корпус
для колонки 6; сам корпус в репозиторий не коммитится, в нём нет собственного
содержания проекта. В репозитории остаётся только перечень страниц —
`twin-wiki-pages.tsv`, он фиксирует состав публичной документации на дату анализа.

Запуск (из каталога `experiments/issue_325`):

    curl -s https://wiki.twin24.ai/graphql \\
        -H 'Content-Type: application/json' \\
        -d '{"query":"{pages{list(locale:\\"ru\\"){path title}}}"}' > pages.json
    python3 fetch_wiki.py
"""

import html
import json
import os
import re
import urllib.parse
import urllib.request

pages = json.load(open("pages.json"))["data"]["pages"]["list"]
os.makedirs("wiki", exist_ok=True)
out = {}


def text(page_html: str) -> str:
    """Достаёт читаемый текст из отрендеренной страницы Wiki.js."""
    match = re.search(
        r'(?s)<div[^>]*class="contents"[^>]*>(.*?)</div>\s*</div>', page_html
    )
    body = match.group(1) if match else page_html
    body = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?i)</(p|div|li|tr|h\d)>", "\n", body)
    body = re.sub(r"(?i)</t[dh]>", " | ", body)  # таблицы вики несут ключевые матрицы
    body = re.sub(r"(?s)<[^>]+>", "", body)
    body = html.unescape(body)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", body)).strip()


for index, page in enumerate(pages):
    url = "https://wiki.twin24.ai/ru/" + urllib.parse.quote(page["path"])
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        raw = urllib.request.urlopen(request, timeout=30).read().decode("utf-8", "replace")
    except Exception as error:  # 403 на части страниц — это ответ, а не сбой скрипта
        print("ERR", page["path"], error, flush=True)
        continue
    out[page["path"]] = {
        "path": page["path"],
        "title": page["title"],
        "url": url,
        "text": text(raw),
    }
    if index % 50 == 0:
        print(index, page["path"], len(out[page["path"]]["text"]), flush=True)

json.dump(out, open("wiki/pages_full.json", "w"), ensure_ascii=False, indent=1)
print("total", len(out), "chars", sum(len(v["text"]) for v in out.values()))
