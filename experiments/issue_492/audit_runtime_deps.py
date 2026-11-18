#!/usr/bin/env python3
"""ФТ-1 issue #492: аудит зависимостей mango_ba_prompts от mango-ba-ai-runtime.

Что делает
----------
Статически и воспроизводимо (модель не запускается) находит каждую ссылку
репозитория на mango-ba-ai-runtime и строит таблицу

    файл-источник → путь runtime → тип ссылки → потребитель → статус.

* **Тип ссылки.** ``SHA`` (закреплённый срез; отмечается, совпадает ли он с SHA
  реестра ``standards/bcreq-runtime-references.md``), ``main`` (плавающая
  ветка), ``корень`` (ссылка на репозиторий без пути), ``клон`` (код читает
  путь из локального клона runtime), ``шаблон`` (``<SHA>`` в тексте нормы).
* **Потребитель.** ``модель`` — текст промпта (``prompts/**``, кроме README);
  ``сайт`` — исходник сайта, генератор ``scripts/generate-pages-data.mjs`` или
  ссылка, дословно попавшая в собранные ``site/data/*.json``; ``валидатор`` —
  код валидатора или файл, который валидатор, работающий с runtime, реально
  читает (наблюдение через ``scripts/_validator_trace.py``); ``сборка`` —
  генератор промптов или снимок БЗ, читающий runtime.
* **Статус.** ``защищённый`` — путь читает сайт, валидатор или сборка;
  ``защищённый (двойной)`` — путь одновременно читают сайт и модель: меняется
  только согласованной миграцией; ``свободный`` — иначе.

Запуск::

    RUNTIME_CLONE=/путь/к/клону/mango-ba-ai-runtime \
        python3 experiments/issue_492/audit_runtime_deps.py

Без ``RUNTIME_CLONE`` скрипт клонирует runtime (публичный) во временный
каталог (``--filter=blob:none``). Результат: ``runtime-deps.json``,
``runtime-deps.md`` рядом со скриптом; сводка — в stdout (лог
``audit-runtime-deps.log``).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
RUNTIME_URL = "https://github.com/G-Ivan-A/mango-ba-ai-runtime"
REGISTRY = "standards/bcreq-runtime-references.md"

# Область ФТ-1 (issue #492): защищаемые слои. Остальной репозиторий тоже
# сканируется и попадает в приложение «вне области» — для полноты.
SCOPE = (
    "prompts/",
    "standards/",
    "docs/contracts/",
    "docs/ba-processes/",  # область ТС-5 валидатора #430 и вход генератора сайта
    "site/",
    "scripts/",
)
TEXT_SUFFIXES = {
    ".md", ".json", ".py", ".mjs", ".js", ".html", ".yaml", ".yml", ".txt",
    ".tsv", ".csv", ".sh", ".css",
}
# Ссылка на runtime: github.com/…/(blob|tree|raw|commit)/<ref>/<path> и raw.
LINK = re.compile(
    r"(?:https?://)?(?:github\.com/G-Ivan-A/mango-ba-ai-runtime(?:\.git)?"
    r"(?:/(?P<kind>blob|tree|raw|commit|commits|issues|pull|pulls)"
    r"(?:/(?P<ref>[^/\s)`\"'<>\]\\]+)(?P<path>/[^\s)`\"'<>\]\\|*]*)?)?)?"
    r"|raw\.githubusercontent\.com/G-Ivan-A/mango-ba-ai-runtime"
    r"/(?P<rref>[^/\s)`\"'<>\]\\]+)(?P<rpath>/[^\s)`\"'<>\]\\|*]*)?)"
)
SHA40 = re.compile(r"\b[0-9a-f]{40}\b")
# Строковый литерал пути в коде скрипта, работающего с клоном runtime.
LITERAL = re.compile(r"[\"']((?:docs/kb|taxonomy|golden|evaluation|templates|contracts|routes|skills)"
                     r"(?:/[^\"'\s{}<>]*)?)[\"']")
CLONE_ENV = re.compile(r"RUNTIME_CLONE|MANGO_BA_RUNTIME_CHECKOUT|MANGO_BA_RUNTIME_MAIN")
# Сборка: код, который читает runtime не ради проверки, а ради результата.
BUILDERS = {"scripts/build_bcreq_step_prompts.py", "scripts/kb/runtime_snapshot.py"}


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout


def runtime_clone() -> Path:
    env = os.environ.get("RUNTIME_CLONE")
    if env:
        return Path(env)
    target = Path(tempfile.gettempdir()) / "issue-492-runtime-clone"
    if not (target / ".git").exists():
        subprocess.run(["git", "clone", "--quiet", "--filter=blob:none", RUNTIME_URL + ".git",
                        str(target)], check=True)
    return target


def registry_sha() -> str:
    text = (ROOT / REGISTRY).read_text(encoding="utf-8")
    match = re.search(r"^runtime_sha:\s*\"?([0-9a-f]{40})", text, re.M)
    if not match:
        raise SystemExit("в реестре нет runtime_sha")
    return match.group(1)


def tracked_files() -> list[str]:
    return [p for p in git("ls-files").splitlines()
            if Path(p).suffix in TEXT_SUFFIXES and (ROOT / p).is_file()]


def in_scope(path: str) -> bool:
    return path.startswith(SCOPE)


def classify_ref(kind: str | None, ref: str | None, pinned: str) -> str:
    if not kind and not ref:
        return "корень"
    if kind in {"issues", "pull", "pulls"}:
        return "корень"  # обсуждение в runtime, не путь пакета
    if ref == "main" or ref == "HEAD":
        return "main"
    if ref and re.fullmatch(r"[0-9a-f]{7,40}", ref):
        return "SHA (реестр)" if pinned.startswith(ref) else "SHA (иной срез)"
    return "шаблон"


def norm_path(path: str | None, kind: str | None) -> str:
    if kind in {"issues", "pull", "pulls", "commit", "commits"} or not path:
        return "/"
    path = unquote(path.split("#", 1)[0].split("?", 1)[0]).strip("/").rstrip(".,;:")
    if not path:
        return "/"
    return path + ("/" if kind == "tree" else "")


def extract(path: str, text: str, pinned: str) -> list[dict]:
    rows = []
    for number, line in enumerate(text.splitlines(), 1):
        for match in LINK.finditer(line):
            kind = match.group("kind") or ("raw" if match.group("rref") else None)
            ref = match.group("ref") or match.group("rref")
            raw_path = match.group("path") or match.group("rpath")
            if kind in {"commit", "commits"}:
                ref_type = classify_ref("blob", ref, pinned)
            else:
                ref_type = classify_ref(kind, ref, pinned)
            rows.append({
                "source": path, "line": number, "kind": kind or "repo",
                "ref": ref or "", "ref_type": ref_type,
                "runtime_path": norm_path(raw_path, kind),
            })
    if path.startswith("scripts/") and path.endswith(".py") and (
        "mango-ba-ai-runtime" in text or CLONE_ENV.search(text)
    ):
        shas = sorted(set(SHA40.findall(text)))
        uses_clone = bool(CLONE_ENV.search(text))
        for number, line in enumerate(text.splitlines(), 1):
            for match in LITERAL.finditer(line):
                literal = match.group(1)
                # Локальные пути спицы (docs/contracts/…) не трогаем: LITERAL
                # начинается с каталогов runtime, а docs/ — только docs/kb.
                rows.append({
                    "source": path, "line": number, "kind": "code",
                    "ref": shas[0] if len(shas) == 1 else "",
                    "ref_type": (classify_ref("blob", shas[0], pinned) if len(shas) == 1
                                 else "клон" if uses_clone else "шаблон"),
                    "runtime_path": literal.rstrip("/") + ("/" if "." not in literal.rsplit("/", 1)[-1] else ""),
                })
    return rows


def traced_reads(files: list[str]) -> dict[str, set[str]]:
    """Какие файлы реально читают валидаторы, работающие с runtime."""
    validators = [p for p in files if re.match(r"scripts/(validate_issue_\d+.*|test_.*)\.py$", p)]
    reads: dict[str, set[str]] = defaultdict(set)
    for script in validators:
        body = (ROOT / script).read_text(encoding="utf-8")
        if "mango-ba-ai-runtime" not in body and "runtime_snapshot" not in body:
            continue
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as handle:
            out = handle.name
        env = dict(os.environ, VALIDATE_TRACE_OUT=out)
        env.pop("RUNTIME_CLONE", None)  # наблюдаем обычный прогон make validate-full
        subprocess.run([sys.executable, str(ROOT / "scripts/_validator_trace.py"), str(ROOT / script)],
                       cwd=ROOT, env=env, capture_output=True, text=True, timeout=600)
        try:
            payload = json.loads(Path(out).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            payload = {"files": []}
        finally:
            Path(out).unlink(missing_ok=True)
        for read in payload.get("files", []):
            reads[read].add(script)
    return reads


def site_urls() -> str:
    chunks = []
    for path in sorted((ROOT / "site/data").glob("*.json")):
        chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def consumers(row: dict, reads: dict[str, set[str]], site_blob: str, line_text: str) -> tuple[list[str], list[str]]:
    source = row["source"]
    found, evidence = [], []
    name = Path(source).name
    if source.startswith("prompts/") and not name.startswith("README") and source.endswith(".md"):
        found.append("модель")
        evidence.append("текст промпта")
    url = LINK.search(line_text)
    if source.startswith("site/") or source == "scripts/generate-pages-data.mjs":
        found.append("сайт")
        evidence.append("исходник сайта")
    elif url and url.group(0).split("://")[-1] in site_blob:
        found.append("сайт")
        evidence.append("ссылка в site/data/*.json")
    if source.startswith("scripts/") and source.endswith(".py") and source not in BUILDERS:
        found.append("валидатор")
        evidence.append("код валидатора")
    elif source in reads:
        found.append("валидатор")
        evidence.append("читает " + ", ".join(sorted(Path(s).name for s in reads[source])))
    if source in BUILDERS:
        found.append("сборка")
        evidence.append("генератор/снимок")
    return found, evidence


def status(found: list[str]) -> str:
    if "сайт" in found and "модель" in found:
        return "защищённый (двойной)"
    if {"сайт", "валидатор", "сборка"} & set(found):
        return "защищённый"
    return "свободный"


def exists(clone: Path, ref: str, path: str) -> bool | None:
    if path == "/":
        return True
    if not ref:
        return None
    probe = subprocess.run(["git", "-C", str(clone), "cat-file", "-e", f"{ref}:{path.rstrip('/')}"],
                           capture_output=True)
    return probe.returncode == 0


def main() -> int:
    pinned = registry_sha()
    clone = runtime_clone()
    subprocess.run(["git", "-C", str(clone), "fetch", "--quiet", "origin"], check=False)
    runtime_main = git("rev-parse", "origin/main", cwd=clone).strip()
    files = tracked_files()
    reads = traced_reads(files)
    site_blob = site_urls()

    occurrences = []
    for path in files:
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        if "mango-ba-ai-runtime" not in text and not (path.startswith("scripts/") and CLONE_ENV.search(text)):
            continue
        lines = text.splitlines()
        for row in extract(path, text, pinned):
            found, evidence = consumers(row, reads, site_blob, lines[row["line"] - 1])
            row.update(consumer=found, evidence=evidence, status=status(found), in_scope=in_scope(path))
            occurrences.append(row)

    # Строки таблицы: (источник, путь, ссылка) с числом вхождений.
    grouped: dict[tuple, dict] = {}
    for row in occurrences:
        key = (row["source"], row["runtime_path"], row["ref_type"], row["ref"])
        entry = grouped.setdefault(key, {**row, "lines": []})
        entry["lines"].append(row["line"])
    table = sorted(grouped.values(), key=lambda r: (not r["in_scope"], r["source"], r["runtime_path"]))
    for row in table:
        row.pop("line", None)

    # Свод по путям runtime.
    paths: dict[str, dict] = {}
    for row in table:
        item = paths.setdefault(row["runtime_path"], {
            "runtime_path": row["runtime_path"], "sources": set(), "consumer": set(),
            "ref_types": set(), "refs": set(), "in_scope_sources": 0,
        })
        item["sources"].add(row["source"])
        item["consumer"].update(row["consumer"])
        item["ref_types"].add(row["ref_type"])
        if re.fullmatch(r"[0-9a-f]{7,40}", row["ref"] or ""):
            item["refs"].add(row["ref"])
        item["in_scope_sources"] += int(row["in_scope"])
    path_rows = []
    for item in sorted(paths.values(), key=lambda i: i["runtime_path"]):
        found = sorted(item["consumer"])
        path_rows.append({
            "runtime_path": item["runtime_path"],
            "sources": len(item["sources"]),
            "in_scope_sources": item["in_scope_sources"],
            "consumer": found,
            "ref_types": sorted(item["ref_types"]),
            "status": status(found),
            "exists_at_registry_sha": exists(clone, pinned, item["runtime_path"]),
            "exists_at_runtime_main": exists(clone, runtime_main, item["runtime_path"]),
            "exists_at_own_ref": (all(exists(clone, ref, item["runtime_path"]) for ref in sorted(item["refs"]))
                                  if item["refs"] else None),
        })

    head = git("rev-parse", "HEAD").strip()
    summary = {
        "issue": 492,
        "repository_commit": head,
        "registry_sha": pinned,
        "runtime_main": runtime_main,
        "files_scanned": len(files),
        "occurrences": len(occurrences),
        "table_rows": len(table),
        "in_scope_rows": sum(r["in_scope"] for r in table),
        "runtime_paths": len(path_rows),
        "validators_traced": sorted({s for v in reads.values() for s in v}),
        "by_status": {},
        "by_ref_type_in_scope": {},
    }
    for row in path_rows:
        summary["by_status"][row["status"]] = summary["by_status"].get(row["status"], 0) + 1
    for row in table:
        if row["in_scope"]:
            key = row["ref_type"]
            summary["by_ref_type_in_scope"][key] = summary["by_ref_type_in_scope"].get(key, 0) + 1

    payload = {"summary": summary, "paths": path_rows, "rows": table}
    (OUT_DIR / "runtime-deps.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1, default=sorted) + "\n", encoding="utf-8")
    (OUT_DIR / "runtime-deps.md").write_text(render(payload), encoding="utf-8")

    print(f"commit={head} registry_sha={pinned} runtime_main={runtime_main}")
    print(f"files={len(files)} occurrences={len(occurrences)} rows={len(table)} "
          f"in_scope_rows={summary['in_scope_rows']} runtime_paths={len(path_rows)}")
    print("validators traced:", ", ".join(Path(s).name for s in summary["validators_traced"]))
    print("paths by status:", json.dumps(summary["by_status"], ensure_ascii=False, sort_keys=True))
    print("in-scope rows by ref type:", json.dumps(summary["by_ref_type_in_scope"], ensure_ascii=False, sort_keys=True))
    missing = [r["runtime_path"] for r in path_rows
               if r["in_scope_sources"] and r["exists_at_own_ref"] is False]
    print("in-scope paths missing at their own pinned ref:", missing or "—")
    for row in path_rows:
        print(f"PATH {row['runtime_path']} | {row['status']} | {'/'.join(row['consumer']) or '—'} | "
              f"{','.join(row['ref_types'])} | sources={row['sources']} | "
              f"own_ref={row['exists_at_own_ref']} pinned={row['exists_at_registry_sha']} main={row['exists_at_runtime_main']}")
    return 0


def render(payload: dict) -> str:
    s = payload["summary"]
    out = [
        "# Аудит зависимостей от runtime: таблица (issue #492, ФТ-1)",
        "",
        "Сгенерировано `experiments/issue_492/audit_runtime_deps.py`; не править вручную.",
        "",
        f"- Коммит спицы: `{s['repository_commit']}`.",
        f"- SHA реестра: `{s['registry_sha']}`; main runtime: `{s['runtime_main']}`.",
        f"- Файлов просмотрено: {s['files_scanned']}; вхождений: {s['occurrences']}; "
        f"строк таблицы: {s['table_rows']} (в области ФТ-1: {s['in_scope_rows']}); путей runtime: {s['runtime_paths']}.",
        "",
        "## 1. Свод по путям runtime",
        "",
        "| Путь runtime | Источников (в области) | Потребитель | Тип ссылки | Статус | Есть на своём SHA | Есть на SHA реестра | Есть на main |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    yes = {True: "да", False: "нет", None: "—"}
    for row in payload["paths"]:
        out.append(
            f"| `{row['runtime_path']}` | {row['sources']} ({row['in_scope_sources']}) | "
            f"{', '.join(row['consumer']) or '—'} | {', '.join(row['ref_types'])} | {row['status']} | "
            f"{yes[row['exists_at_own_ref']]} | {yes[row['exists_at_registry_sha']]} | {yes[row['exists_at_runtime_main']]} |")
    out += [
        "",
        "## 2. Таблица ФТ-1: область аудита",
        "",
        "Файл-источник → путь runtime → тип ссылки → потребитель → статус.",
        "",
        "| Файл-источник | Строки | Путь runtime | Тип ссылки | Потребитель | Основание | Статус |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["rows"]:
        if not row["in_scope"]:
            continue
        lines = ",".join(str(n) for n in row["lines"][:6]) + ("…" if len(row["lines"]) > 6 else "")
        out.append(
            f"| `{row['source']}` | {lines} | `{row['runtime_path']}` | {row['ref_type']} | "
            f"{', '.join(row['consumer']) or '—'} | {'; '.join(row['evidence']) or '—'} | {row['status']} |")
    out += [
        "",
        "## 3. Вне области ФТ-1 (справочно)",
        "",
        "Прогоны, RFC, анализы, эксперименты и прочее фиксируют срез на свою дату.",
        "",
        "| Файл-источник | Вхождений | Путей | Типы ссылок | Потребитель | Статус |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    by_source: dict[str, dict] = {}
    for row in payload["rows"]:
        if row["in_scope"]:
            continue
        item = by_source.setdefault(row["source"], {"n": 0, "paths": set(), "types": set(), "cons": set(), "st": set()})
        item["n"] += len(row["lines"])
        item["paths"].add(row["runtime_path"])
        item["types"].add(row["ref_type"])
        item["cons"].update(row["consumer"])
        item["st"].add(row["status"])
    for source, item in sorted(by_source.items()):
        out.append(f"| `{source}` | {item['n']} | {len(item['paths'])} | {', '.join(sorted(item['types']))} | "
                   f"{', '.join(sorted(item['cons'])) or '—'} | {', '.join(sorted(item['st']))} |")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    raise SystemExit(main())
