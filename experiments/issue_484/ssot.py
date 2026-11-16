#!/usr/bin/env python3
"""Доступ к доверенным источникам оценки BCREQ-1199 v2 (issue #484).

Общий слой для `verify_quotes.py` и `generate_run.py`: тексты пунктов «Шаблона ТЗ для
тендеров v4» (`tv4:`), разделы базы знаний runtime-репозитория (`kb:`) и построение ссылок
колонки 4 отчёта. Шаблон тот же, что в RUN-0070…RUN-0093 (SHA-256 612e5e09…), индекс
п/п — `experiments/issue_367/tender_index.json`.

Каталог БЗ задаётся переменной окружения `MANGO_BA_RUNTIME_MAIN` (по умолчанию /tmp/runtime).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issue_482"))
from tender_similarity import ITEM, P5, PAGE  # noqa: E402

ROOT = HERE.parents[1]
RUNTIME = Path(os.environ.get("MANGO_BA_RUNTIME_MAIN", "/tmp/runtime"))
KB = RUNTIME / "docs/kb"
COMMIT = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
BLOB = f"https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/{COMMIT}/docs/kb/"

SOURCE_URL = "https://github.com/user-attachments/files/34788103/SoC_.29-10.xlsx"
TENDER_URL = "https://github.com/user-attachments/files/34787757/-.-v4.pdf"
TENDER_SHA = "612e5e0938b9d4edad8e341f7fb03ba8498f7ec12dea0fe88f71e6817169d4cc"
SOURCE_SHA = "ca63c6f751770d2296394612971819e24a1f1c56db1f4b81028ab75b9edde32e"
TENDER_P5_TITLE = "2. Общие требования к оказанию услуг Исполнителем"


def front(path: Path) -> dict[str, str]:
    """frontmatter раздела БЗ -> словарь скалярных полей."""
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if ":" in line and not line.startswith((" ", "-")):
            value = value.strip()
            # YAML-скаляр в кавычках: снимается только внешняя пара
            if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            data[key.strip()] = value
    return data


def doc_dirs() -> dict[str, str]:
    """doc_code -> каталог документа БЗ (по frontmatter первого раздела)."""
    dirs: dict[str, str] = {}
    for sections in sorted(KB.glob("**/sections")):
        first = next(iter(sorted(sections.glob("*.md"))), None)
        if first is not None:
            dirs[front(first)["doc_code"]] = str(sections.parent.relative_to(KB))
    return dirs


DOCS = doc_dirs()


def kb_path(ref: str) -> Path:
    """`DOC/NN-slug.md` -> путь раздела БЗ."""
    doc, _, section_file = ref.partition("/")
    return KB / DOCS[doc] / "sections" / section_file


def body(path: Path) -> str:
    """Тело раздела БЗ без frontmatter."""
    text = path.read_text(encoding="utf-8")
    return text.split("\n---\n", 1)[1] if text.startswith("---\n") else text


def tender_text(item: str) -> str:
    """Текст пункта шаблона: `2.18.1` либо `p5:N` (ненумерованный раздел с.5)."""
    if item.startswith("p5"):
        _, _, idx = item.partition(":")
        return "\n".join(P5) if not idx else P5[int(idx) - 1]
    return ITEM[item]


def kb_link(ref: str) -> str:
    """Атомарная ссылка `[ДОК, §X «Заголовок», с.Y](url)` по frontmatter раздела."""
    doc, _, section_file = ref.partition("/")
    fm = front(kb_path(ref))
    assert fm["doc_code"] == doc, ref
    number = fm.get("pdf_section", "")
    if number in ("", "0", "-", "—"):
        number = fm.get("section", "")
    if number in ("", "0", "-", "—"):
        number = ""
    sect = f"§{number} " if number else ""
    return f"[{doc}, {sect}«{fm['title']}», с.{fm['pages']}]({BLOB}{DOCS[doc]}/sections/{section_file})"


def tv4_link(item: str) -> str:
    """Ссылка на пункт шаблона ТЗ-тендеров-v4 с номером страницы PDF."""
    if item.startswith("p5"):
        return f"[ТЗ-тендеров-v4, «{TENDER_P5_TITLE}», с.5]({TENDER_URL})"
    return f"[ТЗ-тендеров-v4, п/п {item}, с.{PAGE[item]}]({TENDER_URL})"


def link(ref: str) -> str:
    """Ссылка колонки 4 по идентификатору источника (`kb:` / `tv4:` / `portal:`)."""
    kind, _, value = ref.partition(":")
    if kind == "kb":
        return kb_link(value)
    if kind == "tv4":
        return tv4_link(value)
    if kind == "portal":
        url, _, title = value.partition("|")
        return f"[Портал Mango — {title}]({url})"
    raise AssertionError(f"неизвестный вид ссылки: {ref}")


def norm(s: str) -> str:
    """Нормализация для дословного сравнения цитаты с источником."""
    s = s.replace("<br>", " ")
    s = s.replace(" ", " ").replace("**", "").replace("", " ").replace("•", " ")
    return re.sub(r"\s+", " ", s).strip()


def research() -> dict[str, dict]:
    """Объединение `research/*.json`; пересечение ключей запрещено."""
    out: dict[str, dict] = {}
    for path in sorted((HERE / "research").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        overlap = set(out) & set(data)
        assert not overlap, f"{path.name}: повтор строк {overlap}"
        for rid, entry in data.items():
            entry["batch"] = path.stem
            out[rid] = entry
    return out
