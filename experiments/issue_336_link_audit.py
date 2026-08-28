#!/usr/bin/env python3
"""Аудит ссылок на публичную вики TWIN: отчёт RUN-0057 + диалог human review (issue #336).

Зачем: задача #336 фиксирует статистику процесса human review прогона RUN-0057 с
приоритетом «проверка ссылок на TWIN». Утверждение «по ссылкам из отчёта неудобно
проверять» само по себе не измеримо, поэтому скрипт считает его детерминированно
по двум источникам:

1. **Отчёт** ``runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md`` —
   ссылки на TWIN живут там как текстовые токены ``[twin: <путь>]``. Для каждого
   токена считается: сколько страниц он адресует, есть ли якорь ``#``, есть ли
   указание раздела/страницы (как в ``[ROBOTFIL, §5, с.46-49]``), кликабелен ли он.
   Для сравнения тем же способом разбираются токены ``[ROBOTFIL…]`` и ``[SA…]``.
2. **Диалог** (транскрипт экспорта чата) — реплики ассистента после замечания БА
   содержат уже полные URL и строку «Раздел на странице». Каждая пара
   «ссылка → заявленный раздел» проверяется по живой странице вики: существует ли
   страница (HTTP), есть ли на ней заголовок с таким названием и, значит, якорь,
   которым ссылку можно было бы сделать точной.

Сеть используется только на чтение публичной вики (GET). Ответы кэшируются в
``--cache``, поэтому повторный запуск воспроизводим без обращений к сети.

Статус: локальный инструмент воспроизводимости, из CI не вызывается.

Использование:
    python3 experiments/issue_336_link_audit.py \
        --report runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md \
        --transcript experiments/issue_336/transcript.md \
        --cache experiments/issue_336/wiki-cache \
        --json experiments/issue_336/link-audit.json
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

WIKI = "https://wiki.twin24.ai"
UA = "mango-ba-prompts/issue-336 link audit (+https://github.com/G-Ivan-A/mango_ba_prompts)"

#: Токен ссылки на TWIN в отчёте: `[twin: scripts/blocks/question; bpl/functions/nlu]`.
TWIN_TOKEN = re.compile(r"\[twin:\s*([^\]]*)\]")
#: Токены источников Mango, с которыми сравнивается точность ссылок TWIN.
MANGO_TOKEN = re.compile(r"\[(ROBOTFIL|SA)([^\]]*)\]")
#: Путь страницы вики; всё остальное в токене — легенда формата, а не адрес.
PAGE_PATH = re.compile(r"^[a-z0-9][a-z0-9/_.-]*$")
#: Полный URL вики в реплике ассистента.
WIKI_URL = re.compile(r"https://wiki\.twin24\.ai[^\s)\]\"'>]*")
#: Строка «Раздел на странице» в принятом БА формате ответа.
SECTION_LINE = re.compile(r"Раздел на странице:?\*{0,2}\s*(.+)")
#: Заголовок страницы вики вместе с его якорем.
HEADING = re.compile(r"<h([1-6])[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</h\1>", re.S)
TITLE = re.compile(r"<title>([^<]*)</title>")
TAG = re.compile(r"<[^>]+>")


def clean(text: str) -> str:
    """Текст без html-разметки, неразрывных пробелов и якорной решётки Docusaurus."""
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", text)).replace(" ", " ")).strip(" ¶#").strip()


def fetch(url: str, cache: Path, pause: float = 0.5) -> tuple[int, str]:
    """GET страницы вики с файловым кэшем. Возвращает (http-код, html)."""
    cache.mkdir(parents=True, exist_ok=True)
    key = cache / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".html")
    meta = key.with_suffix(".status")
    if key.exists() and meta.exists():
        return int(meta.read_text().strip()), key.read_text(encoding="utf-8", errors="replace")
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status, body = response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        status, body = error.code, ""
    except OSError as error:  # сеть недоступна — фиксируем как 0, а не как «страницы нет»
        status, body = 0, f"<!-- {error} -->"
    time.sleep(pause)
    key.write_text(body, encoding="utf-8")
    meta.write_text(str(status), encoding="utf-8")
    return status, body


def headings(page_html: str) -> list[dict]:
    return [
        {"level": int(level), "anchor": anchor, "text": clean(text)}
        for level, anchor, text in HEADING.findall(page_html)
    ]


def split_pages(token_body: str) -> list[str]:
    """Один токен может адресовать несколько страниц через `;` или `,`."""
    return [part.strip() for part in re.split(r"[;,]", token_body) if part.strip()]


def audit_report(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    twin_tokens = TWIN_TOKEN.findall(text)
    pages: list[str] = []
    multi = 0
    for token in twin_tokens:
        found = split_pages(token)
        multi += len(found) > 1
        pages += found
    counter = Counter(pages)
    # Кликабельность: токен считается кликабельным, только если он оформлен как
    # markdown-ссылка `[twin: …](https://…)`, а не как голый текст.
    clickable = len(re.findall(r"\[twin:[^\]]*\]\(https?://", text))

    mango: dict[str, dict] = {}
    for source, body in MANGO_TOKEN.findall(text):
        row = mango.setdefault(source, {"tokens": 0, "with_section": 0, "with_page": 0})
        row["tokens"] += 1
        row["with_section"] += "§" in body
        row["with_page"] += bool(re.search(r"с\.\s*\d", body))

    return {
        "path": str(path),
        "twin_tokens": len(twin_tokens),
        "twin_tokens_multipage": multi,
        "twin_page_mentions": len(pages),
        "twin_pages_distinct": len(counter),
        "twin_tokens_clickable": clickable,
        "twin_tokens_with_anchor": sum("#" in page for page in pages),
        "twin_tokens_with_section_pointer": sum(
            ("§" in token or re.search(r"с\.\s*\d", token) is not None) for token in twin_tokens
        ),
        "twin_top_pages": counter.most_common(10),
        "twin_pages_all": sorted(page for page in counter if PAGE_PATH.match(page)),
        "twin_tokens_placeholder": sum(
            1 for token in twin_tokens if not all(PAGE_PATH.match(p) for p in split_pages(token))
        ),
        "twin_pages_cited_3plus": sum(1 for _, n in counter.items() if n >= 3),
        "twin_mentions_on_pages_cited_3plus": sum(n for n in counter.values() if n >= 3),
        "mango_tokens": mango,
    }


def parse_transcript(path: Path) -> list[dict]:
    """Реплики транскрипта: [{index, role, body}] — формат scripts/chat_export_to_markdown.py."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^===== \[(\d+)\] (\w+)(.*?)=====$", text)
    return [
        {"index": int(parts[i]), "role": parts[i + 1], "body": parts[i + 3]}
        for i in range(1, len(parts), 4)
    ]


def link_claims(body: str) -> list[dict]:
    """Пары «URL → заявленный раздел страницы» в порядке появления в реплике."""
    claims: list[dict] = []
    for line in body.splitlines():
        for url in WIKI_URL.findall(line):
            claims.append({"url": url, "section": None})
        section = SECTION_LINE.search(line)
        if section and claims and claims[-1]["section"] is None:
            claims[-1]["section"] = clean(section.group(1)).strip("«»\"' .")
    return claims


def normalize(text: str) -> str:
    """Сравнимая форма: без регистра, ё→е, без кавычек и служебной пунктуации.

    Пара «Чёрный список» (в отчёте) / «Черный список» (в вики) — реальный случай
    из диалога: без нормализации ё поиск по странице у ревьюера не срабатывает.
    """
    lowered = text.lower().replace("ё", "е")
    return re.sub(r"\s+", " ", re.sub(r"[«»\"'`()\[\].,:;—–-]", " ", lowered)).strip()


def match_section(section: str, page_title: str, page_html: str, page_headings: list[dict]) -> dict:
    """Резолвится ли заявленный раздел страницы в якорь, в заголовок страницы или ни во что.

    Категории:
    - ``anchor-available`` — раздел совпал с заголовком страницы, у которого есть
      якорь: ссылку можно было сделать точной (``…#якорь``), но в диалоге якоря нет;
    - ``page-title-only`` — «раздел» повторяет название всей страницы и потому
      ничего не локализует;
    - ``text-only`` — формулировка встречается в тексте страницы, но не заголовком:
      поиском найти можно, якоря нет;
    - ``not-found-on-page`` — на странице такой формулировки нет (пересказ названия
      раздела или не та страница) — ревьюер не находит место проверки.
    """
    if not section:
        return {"resolution": "no-section-claimed", "anchor": None, "matched": None}
    candidates = [
        part.strip()
        for part in re.split(r"\s+и\s+|→|/|»\s*,", section)
        if len(normalize(part)) >= 4
    ]
    for candidate in candidates:
        needle = normalize(candidate)
        for heading in page_headings:
            head = normalize(heading["text"])
            if not needle or not head:
                continue
            # Совпадением считается равенство, вхождение заголовка в формулировку
            # или вхождение формулировки в заголовок, если она покрывает большую
            # его часть. Иначе «Чёрный список» ошибочно сошёлся бы с заголовком
            # «Добавление номера в чёрный список» — это разные адреса проверки.
            precise = head == needle or head in needle or (
                needle in head and len(needle) >= 0.6 * len(head)
            )
            if precise:
                return {
                    "resolution": "anchor-available",
                    "anchor": heading["anchor"],
                    "matched": heading["text"],
                }
    title = normalize(page_title.replace("| TWIN", ""))
    for candidate in candidates:
        needle = normalize(candidate)
        if needle and title and (needle in title or title in needle):
            return {"resolution": "page-title-only", "anchor": None, "matched": page_title}
    plain = normalize(clean(page_html))
    for candidate in candidates:
        needle = normalize(candidate)
        if needle and needle in plain:
            return {"resolution": "text-only", "anchor": None, "matched": candidate}
    return {"resolution": "not-found-on-page", "anchor": None, "matched": None}


def audit_report_pages(pages: list[str], cache: Path) -> list[dict]:
    """Проверка страниц, на которые ссылается отчёт: существуют ли и есть ли якоря.

    Отвечает на вопрос выполнимости исправления: можно ли вообще заменить
    страничную ссылку на якорную — то есть публикует ли вики якоря заголовков.
    """
    rows: list[dict] = []
    for page in pages:
        url = f"{WIKI}/{page.lstrip('/')}"
        status, page_html = fetch(url, cache)
        page_headings = headings(page_html)
        title = TITLE.search(page_html)
        rows.append(
            {
                "page": page,
                "url": url,
                "http": status,
                "title": clean(title.group(1)) if title else "",
                "headings": len(page_headings),
            }
        )
    return rows


def audit_dialog(transcript: Path, cache: Path) -> dict:
    turns = parse_transcript(transcript)
    rows: list[dict] = []
    checks: list[dict] = []
    for turn in turns:
        if turn["role"] != "assistant":
            continue
        body = turn["body"].strip()
        claims = link_claims(body)
        rows.append(
            {
                "turn": turn["index"],
                "chars": len(body),
                "urls": len(claims),
                "urls_distinct": len({c["url"] for c in claims}),
                "urls_with_locale_prefix": sum("/ru/" in c["url"] for c in claims),
                "urls_with_anchor": sum("#" in c["url"] for c in claims),
                "urls_page_omitted": sum(c["url"].endswith("/") for c in claims),
                "twin_text_tokens": len(TWIN_TOKEN.findall(body)),
                "section_claims": sum(c["section"] is not None for c in claims),
            }
        )
        for claim in claims:
            status, page_html = fetch(claim["url"], cache)
            page_headings = headings(page_html)
            title = TITLE.search(page_html)
            checks.append(
                {
                    "turn": turn["index"],
                    "url": claim["url"],
                    "http": status,
                    "title": clean(title.group(1)) if title else "",
                    "headings": len(page_headings),
                    "section_claimed": claim["section"],
                    **match_section(
                        claim["section"] or "",
                        clean(title.group(1)) if title else "",
                        page_html,
                        page_headings,
                    ),
                }
            )
    return {"turn_rows": rows, "link_checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--cache", type=Path, default=Path("experiments/issue_336/wiki-cache"))
    parser.add_argument("--json", type=Path)
    parser.add_argument(
        "--check-report-pages",
        action="store_true",
        help="проверить по сети каждую страницу, на которую ссылается отчёт",
    )
    args = parser.parse_args()

    report = audit_report(args.report)
    result = {"report": report, "dialog": audit_dialog(args.transcript, args.cache)}
    if args.check_report_pages:
        result["report"]["pages"] = audit_report_pages(report["twin_pages_all"], args.cache)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
