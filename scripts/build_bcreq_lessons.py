#!/usr/bin/env python3
"""Build run-lesson artefacts from the SSOT registry (issue #411).

Source of truth: standards/bcreq-lessons/lessons.json (lesson definitions and
the mapping of every run-local defect code to one lesson). Incident counts are
NOT stored in the registry; they are read from the frozen run statistics
(runs/**/outputs/error-statistics.md, RUN-0064 error-analysis) on every build.

Generated artefacts:
  * standards/bcreq-lessons/README.md         — human index, coverage, gaps
  * standards/bcreq-lessons/coverage.json     — computed counts for site/validator
  * prompts/bcreq-*.md                         — bounded block «Уроки прогонов»
  * standards/bcreq-manual-classes/NN-*.md     — bounded block «Уроки прогонов»

Usage:
  python3 scripts/build_bcreq_lessons.py          # write artefacts
  python3 scripts/build_bcreq_lessons.py --check  # fail if anything is stale
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "standards/bcreq-lessons"
REGISTRY = LESSONS_DIR / "lessons.json"
README = LESSONS_DIR / "README.md"
COVERAGE = LESSONS_DIR / "coverage.json"
CLASSES_DIR = ROOT / "standards/bcreq-manual-classes"
REPO_BLOB = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"

PROMPT_START = "<!-- issue-411: run-lessons -->"
PROMPT_END = "<!-- /issue-411: run-lessons -->"
PROMPT_BLOCK_RE = re.compile(r"\n<!-- issue-411: run-lessons -->\n.*?<!-- /issue-411: run-lessons -->\n", re.S)
CLASS_START = "<!-- issue-411: class-lessons -->"
CLASS_END = "<!-- /issue-411: class-lessons -->"
CLASS_BLOCK_RE = re.compile(r"<!-- issue-411: class-lessons -->\n.*?<!-- /issue-411: class-lessons -->\n\n", re.S)

PROMPT_VERSION = "0.2"
PROMPT_UPDATED = "2026-10-31"
TASK_ID_RE = re.compile(r"\b(?:RUN-\d{4}|SC-\d+|GC-\d+|TASK-\d+|BCREQ-\d+|#\d{2,})\b")


# ---------------------------------------------------------------- run counts
def parse_error_statistics(path: Path) -> dict[str, dict]:
    """Return {code: {name, total, confirmed, ba_immediate, ba_later, at_fix, repeats}}."""
    text = path.read_text(encoding="utf-8")
    section = text.split("## 2. По категориям", 1)[1].split("\n## ", 1)[0]
    header: list[str] | None = None
    rows: dict[str, dict] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "Код":
            header = cells
            continue
        if header is None or not re.fullmatch(r"C\d{2}", cells[0]):
            continue
        row = dict(zip(header, cells))

        def num(*keys: str) -> int:
            for key in keys:
                value = row.get(key, "")
                if value.isdigit():
                    return int(value)
            return 0

        rows[cells[0]] = {
            "name": cells[1],
            "total": num("Всего"),
            "confirmed": num("confirmed"),
            "ba_immediate": num("БА сразу"),
            "ba_later": num("БА позже"),
            "at_fix": num("при фиксации"),
            "repeats": num("Повторов после замечания"),
        }
    return rows


def parse_err_table(path: Path) -> dict[str, dict]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (ERR-\d{2}) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
        if m:
            rows[m.group(1)] = {"name": m.group(2)[:160], "total": 1, "confirmed": 1,
                                "ba_immediate": 0, "ba_later": 0, "at_fix": 0, "repeats": 0}
    return rows


def discover_statistics() -> dict[str, Path]:
    return {p.parts[-3]: p for p in sorted(ROOT.glob("runs/*/RUN-*/outputs/error-statistics.md"))}


def compute_coverage(registry: dict) -> dict:
    lessons = {lesson["id"]: lesson for lesson in registry["lessons"]}
    taxonomies = registry["run_taxonomies"]
    unregistered_runs = sorted(set(discover_statistics()) - set(taxonomies))
    per_lesson = {lid: {"total": 0, "confirmed": 0, "ba_caught": 0, "repeats": 0, "runs": {}} for lid in lessons}
    unmapped: list[dict] = []
    stale: list[dict] = []
    run_totals = {}
    for run, spec in sorted(taxonomies.items()):
        path = ROOT / spec["source"]
        rows = parse_err_table(path) if spec["format"] == "err-table" else parse_error_statistics(path)
        run_totals[run] = {"source": spec["source"], "codes": len(rows), "incidents": sum(r["total"] for r in rows.values())}
        for code, row in rows.items():
            lid = spec["map"].get(code)
            if lid is None or lid not in lessons:
                unmapped.append({"run": run, "code": code, "name": row["name"], "lesson": lid})
                continue
            agg = per_lesson[lid]
            agg["total"] += row["total"]
            agg["confirmed"] += row["confirmed"]
            agg["ba_caught"] += row["ba_immediate"] + row["ba_later"]
            agg["repeats"] += row["repeats"]
            agg["runs"].setdefault(run, []).append({"code": code, "name": row["name"], "total": row["total"]})
        for code in sorted(set(spec["map"]) - set(rows)):
            stale.append({"run": run, "code": code})
    for source in registry.get("qualitative_sources", []):
        for lid in source["lessons"]:
            per_lesson[lid].setdefault("qualitative", []).append(source["run"])
    repeats_total = sum(agg["repeats"] for agg in per_lesson.values())
    for lid, lesson in lessons.items():
        if lesson.get("evidence_metric") == "repeats_after_ba_remark":
            per_lesson[lid]["repeats"] = repeats_total
    return {
        "generated_by": "scripts/build_bcreq_lessons.py",
        "repeats_after_ba_remark_total": repeats_total,
        "registry": str(REGISTRY.relative_to(ROOT)),
        "runs": run_totals,
        "incidents_total": sum(r["incidents"] for r in run_totals.values()),
        "unregistered_runs": unregistered_runs,
        "unmapped_codes": unmapped,
        "stale_mappings": stale,
        "lessons": per_lesson,
    }


# ------------------------------------------------------------- prompt blocks
def lesson_order(registry: dict, coverage: dict) -> list[dict]:
    totals = coverage["lessons"]
    return sorted(registry["lessons"], key=lambda l: (-totals[l["id"]]["total"], l["id"]))


def lessons_for_prompt(registry: dict, coverage: dict, key: str) -> list[dict]:
    out = []
    for lesson in lesson_order(registry, coverage):
        if lesson["level"] != "runtime" or lesson["status"] != "active":
            continue
        if lesson["prompts"] == ["all"] or key in lesson["prompts"]:
            out.append(lesson)
    return out


def render_lesson_item(lesson: dict) -> str:
    anchors = ", ".join(lesson["anchors"])
    return (
        f"- **{lesson['id']}. {lesson['title']}** ({anchors}).\n"
        f"  Правило: {lesson['rule']}\n"
        f"  Проверка: {lesson['check']}\n"
        f"  Не так: {lesson['bad']}\n"
        f"  Так: {lesson['good']}\n"
    )


def render_prompt_block(registry: dict, coverage: dict, key: str) -> str:
    items = lessons_for_prompt(registry, coverage, key)
    closing = [l for l in items if l.get("placement") == "closing"]
    body = "\n".join(render_lesson_item(lesson) for lesson in items if lesson not in closing)
    after = "".join(
        f"\n**После замечания БА ({l['id']}. {l['title']}).** {l['rule']} Проверка: {l['check']}\n"
        for l in closing
    )
    return (
        f"\n{PROMPT_START}\n"
        "## Уроки прогонов: проверка перед выдачей\n\n"
        "Блок собран из реестра уроков прогонов "
        f"([standards/bcreq-lessons]({REPO_BLOB}standards/bcreq-lessons/README.md)) "
        "и не редактируется вручную. Уроки уточняют Р1–Р7, АД-1…АД-11 и АП1–АП9; "
        "при расхождении действует конституция. Порядок — от частых ошибок к редким.\n\n"
        "Перед каждым ответом пройди строки «Проверка» по своему черновику ответа. "
        "Найденное нарушение исправь до выдачи — не жди замечания БА. "
        "В ответ не выводи этот список и не объявляй ответ проверенным: "
        "перечисли только то, что сверено и по какому источнику (Р7).\n\n"
        f"{body}{after}"
        f"{PROMPT_END}\n"
    )


def apply_prompt(text: str, block: str) -> str:
    text = PROMPT_BLOCK_RE.sub("", text)
    text = re.sub(r"^version: [^\n]*$", f"version: {PROMPT_VERSION}", text, count=1, flags=re.M)
    text = re.sub(r"^updated: [^\n]*$", f"updated: {PROMPT_UPDATED}", text, count=1, flags=re.M)
    if not text.endswith("\n"):
        text += "\n"
    return text + block


# -------------------------------------------------------------- class blocks
def render_class_block(registry: dict, coverage: dict, entry: dict, key_by_file: dict) -> str:
    key = key_by_file.get(entry["existing"])
    items = lessons_for_prompt(registry, coverage, key) if key else [
        l for l in lesson_order(registry, coverage)
        if l["level"] == "runtime" and l["status"] == "active" and l["prompts"] == ["all"]
    ]
    items = [l for l in items] + [
        l for l in lesson_order(registry, coverage)
        if entry["id"] in l.get("classes", []) and l not in items
    ]
    rows = "\n".join(f"| {l['id']} | {l['title']} | {l['check']} |" for l in items)
    source = f"`{Path(entry['existing']).name}`"
    return (
        f"{CLASS_START}\n"
        "## Уроки прогонов\n\n"
        f"Класс наследует уроки текущего промпта {source}. Определения, правила и примеры — "
        "в [реестре уроков](../bcreq-lessons/README.md); блок генерирует "
        "`scripts/build_bcreq_lessons.py`. Выход класса проверяется по каждой строке до передачи дальше.\n\n"
        "| Урок | Название | Проверка перед выдачей |\n|---|---|---|\n"
        f"{rows}\n"
        f"{CLASS_END}\n\n"
    )


def apply_class(text: str, block: str) -> str:
    text = CLASS_BLOCK_RE.sub("", text)
    marker = "\n## Паттерн"
    if marker not in text:
        raise SystemExit("class standard without «## Паттерн» section")
    head, tail = text.split(marker, 1)
    return head + "\n" + block.rstrip("\n") + "\n" + marker + tail


# -------------------------------------------------------------------- README
def render_readme(registry: dict, coverage: dict) -> str:
    totals = coverage["lessons"]
    runs = coverage["runs"]
    lines = [
        "---",
        "status: draft",
        f"version: {registry['version']}",
        f"updated: {registry['updated']}",
        f"owner: {registry['owner']}",
        "---",
        "",
        "# Реестр уроков прогонов BCREQ",
        "",
        "<!-- Сгенерировано scripts/build_bcreq_lessons.py из lessons.json и статистик прогонов. Не редактировать вручную. -->",
        "",
        "## Назначение",
        "",
        "Единый источник (SSOT) того, чему научили прогоны: каждый код ошибки из реестров прогонов "
        "сопоставлен ровно одному уроку, а урок — промптам этапа 1, классам ручного pipeline и кейсу golden set. "
        "Решение о реестре — [ADR-017](../../docs/adr/2026-10-adr-017-run-lessons-ssot.md); "
        "процесс — [RFC](../../docs/rfc/2026-10-bcreq-run-lessons-pipeline.md).",
        "",
        "| Файл | Роль |",
        "|---|---|",
        "| [`lessons.json`](lessons.json) | SSOT: уроки, правила, проверки, маппинг кодов прогонов |",
        "| [`coverage.json`](coverage.json) | Сгенерировано: счётчики по урокам из статистик прогонов |",
        "| [`golden-set-bcreq-stage1.md`](golden-set-bcreq-stage1.md) | Эталонные кейсы: по одному на урок и контрольные |",
        "| [`rubric-bcreq-stage1.md`](rubric-bcreq-stage1.md) | Бинарные критерии оценки ответа |",
        "",
        "Обновление: новый прогон → коды его `error-statistics.md` добавляются в `run_taxonomies` → "
        "`python3 scripts/build_bcreq_lessons.py` → `make validate-full`. Код без урока валидатор не пропускает.",
        "",
        "## Покрытие прогонов",
        "",
        "| Прогон | Источник | Кодов | Инцидентов |",
        "|---|---|---:|---:|",
    ]
    for run, info in runs.items():
        lines.append(f"| {run} | [`{Path(info['source']).name}`](../../{info['source']}) | {info['codes']} | {info['incidents']} |")
    lines += [
        f"| **Итого** | | **{sum(i['codes'] for i in runs.values())}** | **{coverage['incidents_total']}** |",
        "",
        f"Несопоставленных кодов: **{len(coverage['unmapped_codes'])}**. "
        f"Прогонов со статистикой вне реестра: **{len(coverage['unregistered_runs'])}**. "
        f"Устаревших сопоставлений: **{len(coverage['stale_mappings'])}**.",
        "",
        "Качественные источники (отзывы БА без статистики) учтены как свидетельства уроков: "
        + ", ".join(sorted({s["run"] for s in registry.get("qualitative_sources", [])})) + ".",
        "",
        "## Уроки",
        "",
        "Порядок — по числу инцидентов. «Поймал БА» — инциденты, на которые БА указал в диалоге; "
        "«Повторы» — вхождения после первого замечания БА по той же категории.",
        "",
        "| Урок | Название | Уровень | Якоря | Инцидентов | Поймал БА | Повторы | Коды прогонов | Промпты | Golden |",
        "|---|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for lesson in lesson_order(registry, coverage):
        agg = totals[lesson["id"]]
        codes = "; ".join(f"{run}: {', '.join(c['code'] for c in items)}" for run, items in sorted(agg["runs"].items()))
        if agg.get("qualitative"):
            codes = (codes + "; " if codes else "") + "отзывы: " + ", ".join(agg["qualitative"])
        prompts = "все" if lesson["prompts"] == ["all"] else (", ".join(lesson["prompts"]) or "— (авторский)")
        lines.append(
            f"| {lesson['id']} | {lesson['title']} | {lesson['level']} | {', '.join(lesson['anchors'])} | "
            f"{agg['total']} | {agg['ba_caught']} | {agg['repeats']} | {codes or '—'} | {prompts} | "
            f"{', '.join(lesson['golden'])} |"
        )
    lines += ["", "## Правила уроков", ""]
    for lesson in sorted(registry["lessons"], key=lambda l: l["id"]):
        lines += [
            f"### {lesson['id']}. {lesson['title']}",
            "",
            f"- Уровень: {lesson['level']}; якоря конституции: {', '.join(lesson['anchors'])}.",
            f"- Правило: {lesson['rule']}",
            f"- Проверка перед выдачей: {lesson['check']}",
            f"- Не так: {lesson['bad']}",
            f"- Так: {lesson['good']}",
            "",
        ]
    lines += ["## Матрица «промпт × урок»", "", "| Промпт | Файл | Уроков | Уроки |", "|---|---|---:|---|"]
    for key, path in registry["prompt_keys"].items():
        items = lessons_for_prompt(registry, coverage, key)
        lines.append(f"| {key} | [`{Path(path).name}`](../../{path}) | {len(items)} | {', '.join(l['id'] for l in items)} |")
    lines += [
        "",
        "Уровень `authoring` (дефект текста промпта) в промпты не вставляется: он проверяется при изменении "
        "промпта по [ADR-017](../../docs/adr/2026-10-adr-017-run-lessons-ssot.md).",
        "",
        "## Сопоставление кодов прогонов",
        "",
        "Коды категорий локальны для прогона: один и тот же код в разных прогонах означает разные ошибки. "
        "Таблица ниже — единственное место, где они сведены.",
        "",
        "| Прогон | Код | Категория прогона | Урок |",
        "|---|---|---|---|",
    ]
    for lid in sorted(totals):
        for run, items in sorted(totals[lid]["runs"].items()):
            for item in items:
                lines.append(f"| {run} | {item['code']} | {item['name']} | {lid} |")
    lines += [
        "",
        "## Related Artifacts",
        "",
        "- [Конституция BCREQ](../../prompts/bcreq-constitution-governance-oneshot.md) — Р1–Р7, АД-1…АД-11, АП1–АП9",
        "- [Классы ручного pipeline](../bcreq-manual-classes/README.md)",
        "- [Ручной процесс BCREQ](../../docs/ba-processes/bcreq-manual-process.md)",
        "- [Аналитический отчёт](../../docs/analysis/2026-10-31-bcreq-pipeline-run-experience-review.md)",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------- main
def build(check: bool) -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    coverage = compute_coverage(registry)
    outputs: dict[Path, str] = {
        README: render_readme(registry, coverage),
        COVERAGE: json.dumps(coverage, ensure_ascii=False, indent=2) + "\n",
    }
    for key, rel in registry["prompt_keys"].items():
        path = ROOT / rel
        block = render_prompt_block(registry, coverage, key)
        leaked = TASK_ID_RE.findall(block)
        if leaked:
            raise SystemExit(f"{rel}: task identifiers leaked into prompt block: {leaked}")
        outputs[path] = apply_prompt(path.read_text(encoding="utf-8"), block)
    key_by_file = {v: k for k, v in registry["prompt_keys"].items()}
    catalog = json.loads((CLASSES_DIR / "catalog.json").read_text(encoding="utf-8"))
    for entry in catalog["classes"]:
        path = CLASSES_DIR / entry["file"]
        outputs[path] = apply_class(path.read_text(encoding="utf-8"), render_class_block(registry, coverage, entry, key_by_file))

    stale = [p for p, content in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != content]
    if check:
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}", file=sys.stderr)
        problems = coverage["unmapped_codes"] or coverage["unregistered_runs"] or coverage["stale_mappings"]
        if problems:
            print(json.dumps({k: coverage[k] for k in ("unmapped_codes", "unregistered_runs", "stale_mappings")},
                             ensure_ascii=False, indent=2), file=sys.stderr)
        return 1 if stale or problems else 0
    for p in stale:
        p.write_text(outputs[p], encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    print(f"lessons={len(registry['lessons'])} incidents={coverage['incidents_total']} "
          f"unmapped={len(coverage['unmapped_codes'])} unregistered_runs={len(coverage['unregistered_runs'])}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if generated artefacts are stale")
    return build(parser.parse_args().check)


if __name__ == "__main__":
    raise SystemExit(main())
