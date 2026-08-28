#!/usr/bin/env python3
"""Сборка веб-представления отчёта RUN-0060 (задача 765, issue #335).

Отчёт собирается из markdown-источника прогона в один самодостаточный HTML:
CSS встроен, диаграммы Mermaid заменены на инлайновый SVG, внешних запросов
страница не делает. Это нужно для копирования отчёта в Confluence одним
действием (Ctrl+A / Ctrl+C / Ctrl+V) и для работы на статическом хостинге без
бэкенда.

Диаграммы рендерятся `@mermaid-js/mermaid-cli` (нужен один раз, результат
кэшируется в ``site/reports/run-0060/diagrams/``):

    python3 experiments/issue_335_build_report_site.py --render-diagrams

Обычная пересборка (SVG берутся из кэша):

    python3 experiments/issue_335_build_report_site.py

Добавление следующего прогона: добавить запись в ``REPORTS`` и запустить
скрипт — индекс, страница входа и отчёт создаются по тем же шаблонам.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPORTS = [
    {
        "slug": "run-0060",
        "task": "765",
        "title": "Интеграция КЦ Mango Office ↔ HH.ru Чаты",
        "subtitle": "Задача 765 — детальный отчёт о разрывах",
        "actualized": "2026-08-27",
        "runs": ["RUN-0056", "RUN-0058", "RUN-0059", "RUN-0060"],
        "source": "runs/2026/RUN-0060/outputs/L4-combined-gap-report.md",
        "file": "detailed-gap-report.html",
    },
]

# Сводные вердикты четырёх прогонов задачи 765. Источники:
# RUN-0056/outputs/L1-executive-summary.md, RUN-0058/outputs/L1-executive-summary.md,
# RUN-0059/outputs/architecture-spike.md, RUN-0060/outputs/L4-combined-gap-report.md.
CROSS_RUN_VERDICTS = [
    ("ФТ-01", "OAuth-авторизация в HeadHunter из ЛК", "Да", "Да", "—", "Да"),
    ("ФТ-02", "Подключение и настройка канала HH в ЛК", "Да", "Да", "—", "Да"),
    ("ФТ-03", "Маршрутизация обращений на сотрудника/группу", "Да", "Да", "—", "Да"),
    ("ФТ-04", "Фильтрация входящих по вакансии", "Частично", "Частично", "—", "Частично"),
    ("ФТ-05", "Создание обращения по первому входящему + контекст", "Частично", "Да", "модель потока", "Частично"),
    ("ФТ-06", "Двусторонняя синхронизация в реальном времени", "Нет", "Частично", "модель потока", "Частично"),
    ("ФТ-07", "Склейка сообщений нескольких Акторов", "Частично", "Частично", "модель потока", "Частично"),
    ("ФТ-08", "Передача контекста (вакансия, резюме, кандидат)", "Частично", "Частично", "маппинг полей", "Частично"),
    ("ФТ-09", "Автосопоставление кандидата с Адресной книгой", "Частично", "Частично", "маппинг полей", "Частично"),
    ("ФТ-10", "Отчёты и выгрузка по каналу HH", "Частично", "Да", "—", "Да"),
]

CHANGE_HISTORY = [
    (
        "RUN-0056",
        "2026-08-25",
        "Первичный gap-анализ по репозиторию документации hhru/api: 7 из 10 ФТ "
        "оценены полностью, 7 разрывов. OpenAPI-спецификация из среды прогона "
        "была недоступна.",
    ),
    (
        "RUN-0058",
        "2026-08-26",
        "Переоценка по действующей OpenAPI-спецификации: 10 из 10 ФТ. "
        "Публичный API чатов найден (14 операций, события CHAT_CREATED и "
        "CHAT_MESSAGE_CREATED) — вердикт ФТ-06 повышен с «Нет» до «Частично», "
        "GAP-1 и GAP-2 закрыты, добавлено 6 новых разрывов.",
    ),
    (
        "RUN-0059",
        "2026-08-26",
        "Архитектурный spike в роли СА: 3 sequence-диаграммы, 27 строк маппинга "
        "полей, 8 JSON-примеров. Найдено 7 разрывов внутреннего контракта Mango; "
        "ни один эндпоинт Mango не выдуман.",
    ),
    (
        "RUN-0060",
        "2026-08-27",
        "Сведение вердиктов БА и моделей СА в один отчёт L4: 27 оценённых "
        "подпунктов ТЗ, 11 Activity-диаграмм, 53 сноски на источники, версия "
        "спецификации закреплена SHA-256. Вердикт ФТ-05 понижен до «Частично» "
        "(GAP-R11).",
    ),
    (
        "issue #335",
        "2026-08-28",
        "Human review ссылок: проверены все 53 сноски, в таблицы источников "
        "добавлены колонки «Где смотреть» и «Цитата из спецификации». "
        "Опубликовано веб-представление отчёта.",
    ),
]

CSS = """
:root { --fg:#1b1b1f; --muted:#5b6472; --line:#dfe3e8; --accent:#0b5fff;
        --ok:#12805c; --warn:#a35b00; --bad:#c2352b; --bg:#fff; --code:#f5f6f8; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.6 -apple-system,
       "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
.wrap { max-width:1080px; margin:0 auto; padding:32px 24px 96px; }
h1 { font-size:30px; line-height:1.25; margin:0 0 8px; }
h2 { font-size:23px; margin:40px 0 12px; padding-top:12px; border-top:1px solid var(--line); }
h3 { font-size:19px; margin:28px 0 10px; }
h4 { font-size:17px; margin:22px 0 8px; }
p, li { font-size:16px; }
a { color:var(--accent); }
table { border-collapse:collapse; width:100%; margin:16px 0; font-size:14px; }
th, td { border:1px solid var(--line); padding:8px 10px; text-align:left; vertical-align:top; }
th { background:#f2f4f7; font-weight:600; }
code { background:var(--code); padding:1px 5px; border-radius:4px;
       font:13px/1.5 "SFMono-Regular", Consolas, monospace; }
pre { background:var(--code); padding:14px 16px; border-radius:8px; overflow:auto; }
pre code { background:none; padding:0; }
blockquote { margin:16px 0; padding:8px 16px; border-left:4px solid var(--line);
             color:var(--muted); }
.meta { color:var(--muted); font-size:14px; margin:0 0 24px; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px;
         font-weight:600; }
.badge-ok { background:#e3f4ee; color:var(--ok); }
.badge-warn { background:#fdf0df; color:var(--warn); }
.badge-bad { background:#fdeceb; color:var(--bad); }
.toolbar { position:sticky; top:0; z-index:5; display:flex; gap:12px; align-items:center;
           background:var(--bg); border-bottom:1px solid var(--line); padding:12px 0;
           margin-bottom:24px; }
button { font:inherit; padding:8px 14px; border-radius:8px; border:1px solid var(--accent);
         background:var(--accent); color:#fff; cursor:pointer; }
button.secondary { background:#fff; color:var(--accent); }
.diagram { margin:16px 0; overflow:auto; }
.diagram svg { max-width:100%; height:auto; }
.toc { background:#f7f8fa; border:1px solid var(--line); border-radius:10px; padding:12px 20px; }
.gate { max-width:420px; margin:15vh auto; padding:28px; border:1px solid var(--line);
        border-radius:14px; }
.gate input { width:100%; padding:10px 12px; font:inherit; border:1px solid var(--line);
              border-radius:8px; margin:12px 0; }
.gate .err { color:var(--bad); min-height:22px; font-size:14px; }
@media print { .toolbar { display:none; } }
"""

GATE_JS = """
const SLUG = "%(slug)s";
const HASHES_URL = "%(hashes)s";
const KEY = "report-access:" + SLUG;

async function digest(text) {
  const bytes = new TextEncoder().encode(text);
  const buffer = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(buffer)].map(b => b.toString(16).padStart(2, "0")).join("");
}

async function check(password) {
  const response = await fetch(HASHES_URL, { cache: "no-store" });
  const entry = (await response.json())[SLUG];
  return (await digest(entry.salt + password)) === entry.hash ? entry.hash : null;
}
"""


# --- markdown -> html --------------------------------------------------------

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_AUTOLINK = re.compile(r"<(https?://[^>]+)>")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def slugify_anchor(text: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", cleaned.strip())


def inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(markup: str) -> str:
        placeholders.append(markup)
        return f"\x00{len(placeholders) - 1}\x00"

    text = _INLINE_CODE.sub(lambda m: stash("<code>" + html.escape(m.group(1)) + "</code>"), text)
    text = _AUTOLINK.sub(
        lambda m: stash(f'<a href="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>'),
        text,
    )
    text = _LINK.sub(
        lambda m: stash(f'<a href="{html.escape(m.group(2))}">{html.escape(m.group(1))}</a>'),
        text,
    )
    text = html.escape(text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    for index, markup in enumerate(placeholders):
        text = text.replace(f"\x00{index}\x00", markup)
    return text


def verdict_badge(cell: str) -> str:
    plain = re.sub(r"[*`]", "", cell).strip()
    css = {"Да": "badge-ok", "Частично": "badge-warn", "Нет": "badge-bad"}.get(plain)
    return f'<span class="badge {css}">{html.escape(plain)}</span>' if css else inline(cell)


def render_table(rows: list[str]) -> str:
    cells = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows]
    header, body = cells[0], cells[2:]
    out = ["<table>", "<thead><tr>"]
    out += [f"<th>{inline(cell)}</th>" for cell in header]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{verdict_badge(cell)}</td>" for cell in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def markdown_to_html(text: str, diagrams: dict[int, str]) -> tuple[str, list[tuple[int, str, str]]]:
    lines = text.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    index = 0
    diagram_number = 0
    list_open = ""

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            out.append(f"</{list_open}>")
            list_open = ""

    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            language = line[3:].strip()
            block: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                block.append(lines[index])
                index += 1
            index += 1
            close_list()
            if language == "mermaid":
                svg = diagrams.get(diagram_number)
                diagram_number += 1
                out.append(
                    f'<figure class="diagram">{svg}</figure>'
                    if svg
                    else "<pre><code>" + html.escape("\n".join(block)) + "</code></pre>"
                )
            else:
                out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
            continue

        if line.startswith("|") and index + 1 < len(lines) and set(
            re.sub(r"[|:\s]", "", lines[index + 1])
        ) == {"-"}:
            block = []
            while index < len(lines) and lines[index].startswith("|"):
                block.append(lines[index])
                index += 1
            close_list()
            out.append(render_table(block))
            continue

        heading = _HEADING.match(line)
        if heading:
            close_list()
            level = len(heading.group(1))
            title = heading.group(2)
            anchor = slugify_anchor(title)
            toc.append((level, anchor, re.sub(r"[*`]", "", title)))
            out.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
            index += 1
            continue

        if line.startswith("> "):
            block = []
            while index < len(lines) and lines[index].startswith(">"):
                block.append(lines[index].lstrip(">").strip())
                index += 1
            close_list()
            out.append("<blockquote>" + inline(" ".join(block)) + "</blockquote>")
            continue

        item = re.match(r"^\s*(?:[-*]|(\d+)\.)\s+(.*)$", line)
        if item:
            tag = "ol" if item.group(1) else "ul"
            if list_open and list_open != tag:
                close_list()
            if not list_open:
                out.append(f"<{tag}>")
                list_open = tag
            block = [item.group(2)]
            index += 1
            while index < len(lines) and re.match(r"^\s{2,}\S", lines[index]):
                block.append(lines[index].strip())
                index += 1
            out.append("<li>" + inline(" ".join(block)) + "</li>")
            continue

        if line.strip() == "---":
            close_list()
            index += 1
            continue

        if line.strip():
            block = [line.strip()]
            index += 1
            while index < len(lines) and lines[index].strip() and not lines[index].startswith(
                ("#", "|", ">", "```")
            ) and not re.match(r"^\s*(?:[-*]|\d+\.)\s+", lines[index]):
                block.append(lines[index].strip())
                index += 1
            close_list()
            out.append("<p>" + inline(" ".join(block)) + "</p>")
            continue

        close_list()
        index += 1

    return "\n".join(out), toc


# --- диаграммы ---------------------------------------------------------------


def extract_mermaid(text: str) -> list[str]:
    return re.findall(r"```mermaid\n(.*?)```", text, re.DOTALL)


def render_diagrams(sources: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "puppeteer.json"
        config.write_text(json.dumps({"args": ["--no-sandbox", "--disable-setuid-sandbox"]}))
        for number, source in enumerate(sources):
            mmd = Path(tmp) / f"d{number}.mmd"
            mmd.write_text(source, encoding="utf-8")
            target = out_dir / f"diagram-{number:02d}.svg"
            subprocess.run(
                ["npx", "-y", "@mermaid-js/mermaid-cli@11", "-p", str(config),
                 "-i", str(mmd), "-o", str(target), "-b", "white"],
                check=True,
            )
            print(f"диаграмма {number}: {target}")


def load_diagrams(out_dir: Path, count: int) -> dict[int, str]:
    diagrams: dict[int, str] = {}
    for number in range(count):
        path = out_dir / f"diagram-{number:02d}.svg"
        if path.exists():
            svg = path.read_text(encoding="utf-8")
            # mermaid-cli выдаёт каждый SVG с одинаковым id="my-svg", и все его
            # CSS-правила привязаны к этому id: без переименования и селекторов,
            # и идентификаторов одиннадцать диаграмм на одной странице
            # перекрывают стили друг друга и теряют заливку
            svg = svg.replace("my-svg", f"mermaid-{number}")
            svg = re.sub(r'\sstyle="max-width:[^"]*"', "", svg)
            diagrams[number] = svg
    return diagrams


# --- страницы ----------------------------------------------------------------


def cross_run_section(report: dict) -> str:
    rows = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            ft,
            html.escape(name),
            verdict_badge(a),
            verdict_badge(b),
            html.escape(c),
            verdict_badge(d),
        )
        for ft, name, a, b, c, d in CROSS_RUN_VERDICTS
    )
    history = "".join(
        f"<tr><td>{html.escape(run)}</td><td>{date}</td><td>{html.escape(what)}</td></tr>"
        for run, date, what in CHANGE_HISTORY
    )
    return f"""
<h2 id="svodnyj-verdikt">Сводный вердикт по четырём прогонам</h2>
<p>Таблица раскрывает ссылки на предыдущие прогоны: вердикт по каждому требованию
показан в динамике, отдельно открывать отчёты RUN-0056, RUN-0058 и RUN-0059 не нужно.</p>
<table>
<thead><tr><th>ФТ</th><th>Требование</th><th>RUN-0056</th><th>RUN-0058</th>
<th>RUN-0059 (СА)</th><th>RUN-0060 — итог</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p><strong>Итог:</strong> 4 требования из 10 закрываются полностью, 6 — частично.
Требований, для которых нет документированных средств, не осталось.</p>
<h2 id="istoriya-izmenenij">История изменений</h2>
<table>
<thead><tr><th>Прогон</th><th>Дата</th><th>Что изменилось</th></tr></thead>
<tbody>{history}</tbody>
</table>
"""


def build_report_page(report: dict, body: str, toc: list[tuple[int, str, str]]) -> str:
    toc_items = "".join(
        f'<li style="margin-left:{(level - 2) * 16}px">'
        f'<a href="#{anchor}">{html.escape(title)}</a></li>'
        for level, anchor, title in toc
        if level == 2
    )
    gate = GATE_JS % {"slug": report["slug"], "hashes": "../../password-hashes.json"}
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Задача {report['task']} — {html.escape(report['title'])}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap" id="content" hidden>
  <div class="toolbar">
    <button id="copy" type="button">Скопировать для Конфы</button>
    <button class="secondary" id="logout" type="button">Выйти</button>
    <span id="copy-status" class="meta" style="margin:0"></span>
  </div>
  <h1>Задача {report['task']}. {html.escape(report['title'])}</h1>
  <p class="meta">Актуализировано: {report['actualized']}, на основе прогонов
  {', '.join(report['runs'])}</p>
  <nav class="toc"><strong>Содержание</strong><ul>{toc_items}</ul></nav>
  {cross_run_section(report)}
  {body}
</div>
<div class="gate" id="gate">
  <h1>Отчёт защищён</h1>
  <p class="meta">Задача {report['task']} — {html.escape(report['title'])}</p>
  <input id="password" type="password" placeholder="Пароль" autocomplete="off" />
  <div class="err" id="error"></div>
  <button id="submit" type="button">Открыть отчёт</button>
</div>
<script>
{gate}
const gate = document.getElementById("gate");
const content = document.getElementById("content");

function unlock() {{
  gate.hidden = true;
  content.hidden = false;
  // якорь из адресной строки применяется после снятия скрытия: пока контент
  // скрыт, браузер не может прокрутить страницу к целевому разделу
  if (location.hash) {{
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target) target.scrollIntoView();
  }}
}}

async function submit() {{
  const error = document.getElementById("error");
  error.textContent = "";
  try {{
    const token = await check(document.getElementById("password").value.trim());
    if (!token) {{ error.textContent = "Неверный пароль"; return; }}
    localStorage.setItem(KEY, token);
    unlock();
  }} catch (e) {{
    error.textContent = "Не удалось проверить пароль: " + e.message;
  }}
}}

document.getElementById("submit").addEventListener("click", submit);
document.getElementById("password").addEventListener("keydown", e => {{
  if (e.key === "Enter") submit();
}});
document.getElementById("logout").addEventListener("click", () => {{
  localStorage.removeItem(KEY);
  location.reload();
}});
document.getElementById("copy").addEventListener("click", async () => {{
  const status = document.getElementById("copy-status");
  const node = document.getElementById("content").cloneNode(true);
  node.querySelector(".toolbar").remove();
  try {{
    await navigator.clipboard.write([new ClipboardItem({{
      "text/html": new Blob([node.innerHTML], {{ type: "text/html" }}),
      "text/plain": new Blob([node.innerText], {{ type: "text/plain" }}),
    }})]);
    status.textContent = "Скопировано — вставьте в Confluence (Ctrl+V)";
  }} catch (e) {{
    const range = document.createRange();
    range.selectNode(node);
    status.textContent = "Буфер недоступен: выделите страницу (Ctrl+A) и скопируйте";
  }}
}});

(async () => {{
  const saved = localStorage.getItem(KEY);
  if (!saved) return;
  const response = await fetch("../../password-hashes.json", {{ cache: "no-store" }});
  if (saved === (await response.json())[SLUG].hash) unlock();
}})();
</script>
</body>
</html>
"""


def build_gate_page(report: dict) -> str:
    gate = GATE_JS % {"slug": report["slug"], "hashes": "../../password-hashes.json"}
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Задача {report['task']} — вход</title>
<style>{CSS}</style>
</head>
<body>
<div class="gate">
  <h1>Задача {report['task']}</h1>
  <p class="meta">{html.escape(report['title'])}<br />Актуализировано:
  {report['actualized']}, на основе прогонов {', '.join(report['runs'])}</p>
  <input id="password" type="password" placeholder="Пароль" autocomplete="off" />
  <div class="err" id="error"></div>
  <button id="submit" type="button">Открыть отчёт</button>
</div>
<script>
{gate}
async function submit() {{
  const error = document.getElementById("error");
  error.textContent = "";
  try {{
    const token = await check(document.getElementById("password").value.trim());
    if (!token) {{ error.textContent = "Неверный пароль"; return; }}
    localStorage.setItem(KEY, token);
    location.href = "{report['file']}";
  }} catch (e) {{
    error.textContent = "Не удалось проверить пароль: " + e.message;
  }}
}}
document.getElementById("submit").addEventListener("click", submit);
document.getElementById("password").addEventListener("keydown", e => {{
  if (e.key === "Enter") submit();
}});
(async () => {{
  const saved = localStorage.getItem(KEY);
  if (!saved) return;
  const response = await fetch("../../password-hashes.json", {{ cache: "no-store" }});
  if (saved === (await response.json())[SLUG].hash) location.href = "{report['file']}";
}})();
</script>
</body>
</html>
"""


def build_index_page() -> str:
    cards = "".join(
        f"""<tr><td><a href="{report['slug']}/">Задача {report['task']} —
        {html.escape(report['title'])}</a></td><td>{report['actualized']}</td>
        <td>{', '.join(report['runs'])}</td><td>по паролю</td></tr>"""
        for report in REPORTS
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Отчёты — Mango BA Prompts</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>Отчёты</h1>
  <p class="meta">Отчёты по задачам, подготовленные для передачи Заказчику.
  Доступ к каждому отчёту закрыт паролем; пароль передаётся отдельно от ссылки.</p>
  <table>
    <thead><tr><th>Отчёт</th><th>Актуализирован</th><th>Прогоны</th><th>Доступ</th></tr></thead>
    <tbody>{cards}</tbody>
  </table>
  <p><a href="../index.html">← Каталог промптов</a></p>
</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-diagrams", action="store_true",
                        help="перерисовать диаграммы через mermaid-cli")
    args = parser.parse_args()

    reports_dir = ROOT / "site" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "index.html").write_text(build_index_page(), encoding="utf-8")

    for report in REPORTS:
        target_dir = reports_dir / report["slug"]
        target_dir.mkdir(parents=True, exist_ok=True)
        text = (ROOT / report["source"]).read_text(encoding="utf-8")
        text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)

        sources = extract_mermaid(text)
        diagrams_dir = target_dir / "diagrams"
        if args.render_diagrams:
            render_diagrams(sources, diagrams_dir)
        diagrams = load_diagrams(diagrams_dir, len(sources))

        body, toc = markdown_to_html(text, diagrams)
        (target_dir / report["file"]).write_text(
            build_report_page(report, body, toc), encoding="utf-8"
        )
        (target_dir / "index.html").write_text(build_gate_page(report), encoding="utf-8")
        print(
            f"{report['slug']}: диаграмм {len(diagrams)}/{len(sources)}, "
            f"разделов {sum(1 for level, _, _ in toc if level == 2)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
