#!/usr/bin/env python3
"""Аудит каталога `prompts/` (issue #384, PR #385).

Зачем
-----
Отчёт `docs/analysis/2026-10-23-prompts-catalog-audit.md` классифицирует все
файлы `prompts/` на снимке `dbf1d3c5` и опирается на данные двух read-only
скриптов (`experiments/issue_384_prompts_inventory.py`,
`experiments/issue_384_prompt_provenance.py`). Валидатор проверяет, что отчёт
не разошёлся с данными и с контрактом:

1. контракт Analysis (`standards/analysis-standard.md`): frontmatter `status`,
   `version`, `updated`, `temperature`, `source`, `scope`, `analysis-subtype` из
   словаря стандарта, без `ai-generated`; имя файла `YYYY-MM-DD-*.md`; секции
   Summary / BLUF (первой), Context / Scope, Findings, Recommendations,
   Related Artifacts; раздел «Архитектурные наблюдения»;
2. таблица `<!-- inventory:table -->` содержит ровно файлы снимка
   (`experiments/issue_384/inventory.json`), у каждого — тема и один статус из
   словаря issue; итоговая таблица статусов совпадает с подсчётом;
3. маркеры и прогоны в таблице совпадают с `inventory.json`;
4. числа происхождения дефектов (§3.4) совпадают с `prompt-provenance.json`;
5. все ссылки — полные абсолютные URL (требование issue): нет относительных
   Markdown-ссылок;
6. якоря `?plain=1#L<n>` на файлы снимка указывают на существующие строки
   (если коммит снимка есть в локальном клоне; в shallow-клоне CI — пропуск);
7. контекст чата 21–23.10.2026 (версия 0.2): каждая ссылка
   «[р. N, Ч-NN](…chat-2026-10-22-23-register.md?plain=1#L<n>)» ведёт на строку
   Ч-NN реестра цитат, и номер реплики совпадает с реестром; незаменённых
   `{Ч-NN}` нет; `chat-quote-check.json` — `ok`, тот же SHA-256 экспорта и те же
   ID, что в реестре; матрица §3.7.1 содержит «Промпт 0» и пункты 2.1–2.14;
   число наблюдений Н1…Нn в §3.7.3 совпадает с числом в Summary; следов
   «BLOCKED» версии 0.1 нет.

Запуск: ``python3 scripts/validate_issue_384_prompts_audit.py``
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "analysis" / "2026-10-23-prompts-catalog-audit.md"
INVENTORY = ROOT / "experiments" / "issue_384" / "inventory.json"
PROVENANCE = ROOT / "experiments" / "issue_384" / "prompt-provenance.json"
REGISTER = ROOT / "experiments" / "issue_384" / "chat-2026-10-22-23-register.md"
QUOTE_CHECK = ROOT / "experiments" / "issue_384" / "chat-quote-check.json"
REGISTER_URL = (
    "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"
    "experiments/issue_384/chat-2026-10-22-23-register.md?plain=1#L"
)
SHA = "dbf1d3c58ca5a4c145929e644b2b31803b0ea11d"
SUBTYPES = ("inventory", "matrix", "options", "recommendation")
SECTIONS = ("Summary / BLUF", "Context / Scope", "Findings", "Recommendations", "Related Artifacts")
STATUSES = ("оставить", "доработать", "удалить", "промпт для расшифровки")
THEMES = set("АБВГДЕЖЗ")
MARKERS = {
    "R": "role_methodology", "S": "old_section_model", "Б": "ban_system_must",
    "C": "self_certification", "К": "creative_generation", "E": "english_labels",
    "Н": "no_invention_rule", "G": "stop_gates", "F": "status_field",
}
TABLE = re.compile(r"<!-- inventory:table -->\n(.*?)<!-- /inventory:table -->", re.S)
ANCHOR = re.compile(
    rf"https://github\.com/G-Ivan-A/mango_ba_prompts/blob/{SHA}/([^\s)?#]+)(?:\?plain=1)?(?:#L(\d+))?"
)


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    return dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M))


def check_frontmatter(text: str) -> list[str]:
    errors = []
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md", DOC.name):
        errors.append(f"{DOC.name}: имя не по шаблону YYYY-MM-DD-name.md")
    fm = frontmatter(text)
    for key in ("status", "version", "updated", "temperature", "source", "scope", "analysis-subtype"):
        if not fm.get(key):
            errors.append(f"frontmatter: нет поля {key}")
    if fm.get("analysis-subtype") and fm["analysis-subtype"] not in SUBTYPES:
        errors.append(f"frontmatter: analysis-subtype={fm['analysis-subtype']!r} вне словаря {SUBTYPES}")
    if "ai-generated" in fm:
        errors.append("frontmatter: ai-generated запрещён стандартом Analysis")
    headings = re.findall(r"^## (.+)$", text, re.M)
    for section in SECTIONS:
        if not any(section in h for h in headings):
            errors.append(f"нет секции «{section}» (standards/analysis-standard.md)")
    if headings and "Summary / BLUF" not in headings[0]:
        errors.append("первая секция — не Summary / BLUF")
    if not re.search(r"^## .*[Аа]рхитектурные наблюдения", text, re.M):
        errors.append("нет раздела «Архитектурные наблюдения» (DoD issue #384)")
    return errors


def table_rows(text: str) -> tuple[list[list[str]], list[str]]:
    m = TABLE.search(text)
    if not m:
        return [], ["нет блока <!-- inventory:table -->"]
    rows = []
    for line in m.group(1).strip().splitlines()[2:]:
        rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows, []


def check_table(text: str, inventory: list[dict]) -> list[str]:
    rows, errors = table_rows(text)
    if errors:
        return errors
    by_path = {r["path"]: r for r in inventory}
    seen, counts = [], dict.fromkeys(STATUSES, 0)
    for cells in rows:
        if len(cells) != 9:
            errors.append(f"строка таблицы {cells[:2]}: {len(cells)} столбцов вместо 9")
            continue
        num, link, theme, _, _, runs, markers, status, reason = cells
        name = re.match(r"\[([^\]]+)\]\((\S+)\)", link)
        if not name:
            errors.append(f"№ {num}: в столбце «Файл» нет ссылки")
            continue
        path = f"prompts/{name.group(1)}"
        if not name.group(2).endswith(f"/{SHA}/{path}"):
            errors.append(f"№ {num}: ссылка {name.group(2)} не ведёт на {path} снимка")
        seen.append(path)
        if theme not in THEMES:
            errors.append(f"№ {num}: тема {theme!r} вне легенды {sorted(THEMES)}")
        if status not in STATUSES:
            errors.append(f"№ {num}: статус {status!r} вне словаря issue {STATUSES}")
        else:
            counts[status] += 1
        if not reason:
            errors.append(f"№ {num}: нет обоснования статуса")
        row = by_path.get(path)
        if row is None:
            continue
        got = {MARKERS[m] for m in markers.split() if m in MARKERS}
        if got != set(row["flags"]):
            errors.append(f"№ {num} {path}: маркеры {sorted(got)} ≠ inventory.json {row['flags']}")
        expected_runs = ", ".join(r[4:] for r in row["run_ids"]) or "—"
        if runs != expected_runs:
            errors.append(f"№ {num} {path}: прогоны {runs!r} ≠ inventory.json {expected_runs!r}")
    missing = sorted(set(by_path) - set(seen))
    extra = sorted(set(seen) - set(by_path))
    dup = sorted({p for p in seen if seen.count(p) > 1})
    if missing:
        errors.append(f"в таблице нет файлов снимка: {missing}")
    if extra:
        errors.append(f"в таблице файлы вне снимка: {extra}")
    if dup:
        errors.append(f"файлы в таблице повторяются: {dup}")
    for status, n in counts.items():
        if not re.search(rf"^\| {re.escape(status)} \| {n} \|", text, re.M):
            errors.append(f"итоговая таблица: нет строки «| {status} | {n} |»")
    return errors


def check_provenance(text: str, prov: dict) -> list[str]:
    errors = []
    total = f"| **Итого** | **{prov['prompt_incidents']}** | **{prov['matched_incidents']}** |"
    if total not in text:
        errors.append(f"§3.4: нет итоговой строки {total}")
    for run, data in prov["by_run"].items():
        if not re.search(rf"^\| {run} \| {data['prompt_incidents']} \| {data['matched']} \|", text, re.M):
            errors.append(f"§3.4: строка {run} не совпадает с prompt-provenance.json ({data})")
    for name, incidents in prov["by_prompt"].items():
        # BLUF: «[`<file>.md`](<url>) (<число инцидентов>)».
        if not re.search(rf"\[`{re.escape(Path(name).name)}`\]\([^)]+\)\s*\({len(incidents)}\)", text):
            errors.append(f"Summary: для {name} не указано {len(incidents)} совпавших инцидентов")
    for run, n in prov.get("model_drafted_prompt_rows", {}).items():
        if not re.search(rf"{n} строк[аи]? реестра {run}", text):
            errors.append(f"§3.4: нет числа {n} строк реестра {run}, написанных моделью")
    return errors


def check_links(text: str) -> list[str]:
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    rel = [t for t in re.findall(r"\]\(([^)\s]+)\)", body) if not t.startswith("https://")]
    return [f"относительная ссылка {t!r}: нужны полные абсолютные URL" for t in rel]


def register_rows(register: str) -> dict[str, tuple[int, int]]:
    """ID строки реестра → (номер реплики, номер строки файла)."""
    rows = {}
    for number, line in enumerate(register.splitlines(), 1):
        m = re.match(r"^\| (Ч-\d{2}) \| (\d+) \|", line)
        if m:
            rows[m.group(1)] = (int(m.group(2)), number)
    return rows


def check_chat_context(text: str, register: str, quote_check: dict) -> list[str]:
    errors = []
    rows = register_rows(register)
    if not rows:
        return ["реестр цитат: нет строк Ч-NN"]
    links = re.findall(rf"\[р\. (\d+), (Ч-\d{{2}})\]\({re.escape(REGISTER_URL)}(\d+)\)", text)
    if not links:
        errors.append("нет ссылок на реестр цитат чата 21–23.10.2026")
    for turn, rid, line in links:
        if rid not in rows:
            errors.append(f"ссылка на {rid}: такой строки в реестре нет")
        elif rows[rid] != (int(turn), int(line)):
            errors.append(f"ссылка «р. {turn}, {rid}» → L{line}; в реестре р. {rows[rid][0]}, L{rows[rid][1]}")
    loose = len(re.findall(r"chat-2026-10-22-23-register\.md\?plain=1#L", text)) - len(links)
    if loose:
        errors.append(f"{loose} ссылок на строки реестра не в форме «[р. N, Ч-NN](…#Ln)»")
    if "{Ч-" in text:
        errors.append("остались незаменённые плейсхолдеры {Ч-NN}")
    if "BLOCKED" in text:
        errors.append("в отчёте остался статус BLOCKED версии 0.1")

    sha = re.search(r"^\| SHA-256 \| `([0-9a-f]{64})` \|$", register, re.M)
    if not quote_check.get("ok"):
        errors.append("chat-quote-check.json: ok=false — цитаты не сверены с экспортом")
    if sha is None or quote_check.get("export_sha256") != sha.group(1):
        errors.append("chat-quote-check.json: SHA-256 экспорта не совпадает с провенансом реестра")
    checked = [r["id"] for r in quote_check.get("results", [])]
    if sorted(checked) != sorted(rows):
        errors.append(f"chat-quote-check.json: сверено {len(checked)} строк, в реестре {len(rows)}")

    matrix = re.search(r"^#### 3\.7\.1\..*?(?=^#### )", text, re.M | re.S)
    if matrix is None:
        errors.append("нет матрицы §3.7.1 «Пункты структуры и каталог»")
    else:
        for item in ["Промпт 0", *(f"2.{n}" for n in range(1, 15))]:
            if not re.search(rf"^\| {re.escape(item)} \|", matrix.group(0), re.M):
                errors.append(f"§3.7.1: нет строки пункта «{item}»")
    observations = re.findall(r"^\| Н(\d+) \|", text, re.M)
    if observations != [str(n) for n in range(1, len(observations) + 1)]:
        errors.append(f"§3.7.3: наблюдения не идут подряд Н1…Нn: {observations}")
    claimed = re.search(r"(\d+) наблюдени", text)
    if claimed is None or int(claimed.group(1)) != len(observations):
        errors.append(f"Summary: число наблюдений не совпадает с §3.7.3 ({len(observations)})")
    return errors


def check_anchors(text: str) -> tuple[list[str], str]:
    probe = subprocess.run(["git", "cat-file", "-e", f"{SHA}^{{commit}}"], cwd=ROOT,
                           capture_output=True, check=False)
    if probe.returncode:
        return [], f"якоря не проверены: коммита {SHA[:8]} нет в клоне"
    errors, cache, checked = [], {}, 0
    for path, line in sorted(set(ANCHOR.findall(text))):
        if path not in cache:
            res = subprocess.run(["git", "show", f"{SHA}:{path}"], cwd=ROOT,
                                 capture_output=True, text=True, check=False)
            cache[path] = None if res.returncode else res.stdout.splitlines()
        lines = cache[path]
        if lines is None:
            errors.append(f"ссылка на {path}: файла нет в снимке {SHA[:8]}")
        elif line and not 1 <= int(line) <= len(lines):
            errors.append(f"якорь {path}#L{line}: в файле {len(lines)} строк")
        elif line and not lines[int(line) - 1].strip():
            errors.append(f"якорь {path}#L{line} указывает на пустую строку")
        checked += 1
    return errors, f"{checked} ссылок на снимок"


def main() -> int:
    for path in (DOC, INVENTORY, PROVENANCE, REGISTER, QUOTE_CHECK):
        if not path.exists():
            print(f"FAIL: нет {path.relative_to(ROOT)}")
            return 1
    text = DOC.read_text(encoding="utf-8")
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    prov = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    errors = check_frontmatter(text)
    errors += check_table(text, inventory)
    errors += check_provenance(text, prov)
    errors += check_links(text)
    errors += check_chat_context(text, REGISTER.read_text(encoding="utf-8"),
                                 json.loads(QUOTE_CHECK.read_text(encoding="utf-8")))
    anchor_errors, anchor_note = check_anchors(text)
    errors += anchor_errors
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print(f"OK: {DOC.relative_to(ROOT)} — {len(inventory)} файлов снимка классифицированы, "
          f"маркеры, прогоны, provenance и цитаты чата согласованы; {anchor_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
