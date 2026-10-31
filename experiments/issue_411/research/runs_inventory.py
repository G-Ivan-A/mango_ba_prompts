#!/usr/bin/env python3
"""Read-only inventory of runs/2026/RUN-* for issue #411.

Answers: how complete is the run evidence for re-using successful and failed
prompt usages when creating BA artifacts.

Stdlib only (PyYAML is not installed): a minimal YAML subset parser is used
for metadata.yaml (scalars, lists, nested maps by indentation).

Usage (from repository root):
    python3 -I experiments/issue_411/research/runs_inventory.py

Writes experiments/issue_411/research/runs_inventory.json, never touches runs/.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RUNS_DIR = os.path.join(ROOT, "runs", "2026")
OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs_inventory.json")

SUBDIRS = ("inputs", "outputs", "feedback", "logs")


# ---------------------------------------------------------------- mini YAML
def _scalar(v: str):
    v = v.strip()
    if not v:
        return None
    if v[0] in "\"'" and v[-1] == v[0] and len(v) >= 2:
        return v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    if v in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _strip_comment(line: str) -> str:
    out, q = [], None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def parse_yaml(text: str):
    lines = []
    for raw in text.splitlines():
        if raw.strip() in ("---", "...") or not raw.strip():
            continue
        s = _strip_comment(raw)
        if not s.strip():
            continue
        lines.append((len(s) - len(s.lstrip(" ")), s.strip()))

    def block(i, indent):
        if i >= len(lines):
            return None, i
        if lines[i][1].startswith("- ") or lines[i][1] == "-":
            res = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("-"):
                item = lines[i][1][1:].strip()
                i += 1
                m = re.match(r"^([^:\s][^:]*):(\s+.*)?$", item)
                if m and not item.startswith(("http", '"', "'")):
                    # map item inside list
                    d = {m.group(1).strip(): _scalar(m.group(2) or "")}
                    if i < len(lines) and lines[i][0] > indent:
                        sub, i = block(i, lines[i][0])
                        if isinstance(sub, dict):
                            d.update(sub)
                    res.append(d)
                elif item:
                    res.append(_scalar(item))
                elif i < len(lines) and lines[i][0] > indent:
                    sub, i = block(i, lines[i][0])
                    res.append(sub)
            return res, i
        res = {}
        while i < len(lines) and lines[i][0] == indent:
            content = lines[i][1]
            m = re.match(r"^([^:]+?):(\s+(.*))?$", content)
            if not m:
                i += 1
                continue
            key, val = m.group(1).strip().strip("\"'"), (m.group(3) or "").strip()
            i += 1
            if val in ("|", ">", "|-", ">-"):
                buf = []
                while i < len(lines) and lines[i][0] > indent:
                    buf.append(lines[i][1])
                    i += 1
                res[key] = "\n".join(buf)
            elif val:
                if val.startswith("[") and val.endswith("]"):
                    res[key] = [_scalar(x) for x in val[1:-1].split(",") if x.strip()]
                else:
                    res[key] = _scalar(val)
            elif i < len(lines) and (lines[i][0] > indent or
                                     (lines[i][0] == indent and lines[i][1].startswith("-"))):
                sub, i = block(i, lines[i][0])
                res[key] = sub
            else:
                res[key] = None
        return res, i

    data, _ = block(0, lines[0][0] if lines else 0)
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------- helpers
def files_in(path):
    out = []
    for dp, _, fns in os.walk(path):
        for fn in fns:
            if fn == ".gitkeep":
                continue
            fp = os.path.join(dp, fn)
            out.append((os.path.relpath(fp, ROOT), os.path.getsize(fp)))
    return sorted(out)


def read(fp, limit=None):
    try:
        with open(os.path.join(ROOT, fp), encoding="utf-8", errors="replace") as fh:
            return fh.read(limit) if limit else fh.read()
    except OSError:
        return ""


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def period_of(n: int) -> str:
    if n <= 12:
        return "P0 Phase 0 / перенос (RUN-0001–0012)"
    if n <= 29:
        return "P1 экспорт чатов + metrics (RUN-0013–0029)"
    if n <= 54:
        return "P2 пакетная фиксация #309 (RUN-0030–0054)"
    if n <= 72 or n == 77:
        return "P3 AI-исполнение / feasibility (RUN-0055–0072, 0077)"
    if n <= 76:
        return "P4 реестры инцидентов и golden-кандидаты (RUN-0073–0076)"
    return "P5 имитация по критериям (RUN-0078)"


RAW_CHAT_RE = re.compile(r"(chat-export|export.*\.json$|transcript)", re.I)
REGISTER_RE = re.compile(r"(incident|error|quality-findings|golden|rubric|criteria|findings|check-results)", re.I)
RULE_RE = re.compile(r"(правил[оа]|\brule\b|не делать|how-not-to|как не надо|запрещ)", re.I)
TARGET_PROMPT_RE = re.compile(r"prompts/[\w./-]+\.md")
VERSION_NEAR_RE = re.compile(r"(\bv\d+\.\d+|version[:\s]+\"?\d|верси[яи]\s+\d|[0-9a-f]{7,40}\b)", re.I)

# Feedback classification: first H1 heading has priority, then content markers.
FB_AUTO_LIMITS = re.compile(r"(Ограничения чтения|Содержимое диалога в записи отсутствует)", re.I)
FB_AI_SELF = re.compile(r"(Заметки для ревью|Заметки к ревью|Заметки ревью|Review notes RUN-00(5|6|7)|Замечания к результатам|"
                        r"Проверка результата|Самооценка|self-review|Author review|Фокус human review)", re.I)
FB_RECONSTRUCTED = re.compile(r"(Явной обратной связи БА в выгрузке нет|реконструкция по наблюдаемому поведению)", re.I)
FB_NO_REVIEW = re.compile(r"Ревью прогона на момент фиксации \*\*не проводилось", re.I)
FB_HUMAN_BA = re.compile(r"(Обратная связь БА|решения БА|БА-ревью|Заметки БА|вердикты БА|со стороны БА|реплик[аи]? БА|"
                         r"Разбор прогона|Дефекты достоверности|Обратная связь \*\*реальная|Review notes прогона RUN-00[12])", re.I)
QUOTE_RE = re.compile(r"«[^»]{15,}»")


def classify_feedback(fb_files):
    """Return (kind, bytes, quotes).

    kind: none | auto-limitations | ai-self-review | ba-reconstructed |
          no-review-declared | human-ba | other
    """
    if not fb_files:
        return "none", 0, 0
    text = "\n".join(read(p) for p, _ in fb_files)
    size = sum(s for _, s in fb_files)
    quotes = len(QUOTE_RE.findall(text))
    h1 = next((l for l in text.splitlines() if l.startswith("# ")), "")
    if FB_AUTO_LIMITS.search(h1) or FB_AUTO_LIMITS.search(text[:3000]) and not FB_HUMAN_BA.search(h1):
        return "auto-limitations", size, quotes
    if FB_AI_SELF.search(h1):
        return "ai-self-review", size, quotes
    if FB_RECONSTRUCTED.search(text):
        return "ba-reconstructed", size, quotes
    if FB_NO_REVIEW.search(text):
        return "no-review-declared", size, quotes
    if FB_HUMAN_BA.search(h1) or FB_HUMAN_BA.search(text):
        return "human-ba", size, quotes
    if FB_AI_SELF.search(text):
        return "ai-self-review", size, quotes
    return "other", size, quotes


LESSON_SECTION_RE = re.compile(r"^#+ .*(Предложения по (промпту|библиотеке)|Что править|Выводы для библиотеки|"
                               r"кандидаты на перенос|Правила, которые|Улучшени[яй] промпт|RFC на улучшение)", re.I | re.M)


def get_metric(meta, key):
    for container in (meta.get("metrics"), meta.get("eval"),
                      (meta.get("metrics") or {}).get("eval") if isinstance(meta.get("metrics"), dict) else None,
                      meta):
        if isinstance(container, dict) and key in container:
            return container[key]
    return None


def parse_rate(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.match(r"\s*(\d+(?:\.\d+)?)", v)
        if m:
            f = float(m.group(1))
            return f if f <= 1 else None
    return None


# ---------------------------------------------------------------- main
def _scan_prompt_backlinks():
    res = defaultdict(list)
    pdir = os.path.join(ROOT, "prompts")
    for dp, _, fns in os.walk(pdir):
        for fn in fns:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, fn), ROOT)
                for rid in sorted(set(re.findall(r"RUN-\d{4}", read(rel)))):
                    res[rid].append(rel)
    return res


def _scan_golden_inventory():
    t = read("docs/reviews/issue-391-golden-inventory.md")
    return Counter(m.group(1) for m in re.finditer(r"^\| (\d{4}) \|", t, re.M))


def _scan_rfc_register():
    t = read("docs/rfc/rfc-register.md")
    return Counter(re.findall(r"runs/2026/(RUN-\d{4})", t))


PROMPT_BACKLINKS = _scan_prompt_backlinks()
RFC_REGISTER = _scan_rfc_register()
GOLDEN_INVENTORY = _scan_golden_inventory()


def inventory():
    runs = []
    for name in sorted(os.listdir(RUNS_DIR)):
        rdir = os.path.join(RUNS_DIR, name)
        if not (name.startswith("RUN-") and os.path.isdir(rdir)):
            continue
        n = int(name[4:])
        meta = parse_yaml(read(os.path.relpath(os.path.join(rdir, "metadata.yaml"), ROOT)))
        sub = {d: files_in(os.path.join(rdir, d)) for d in SUBDIRS}
        extra_dirs = sorted(d for d in os.listdir(rdir)
                            if os.path.isdir(os.path.join(rdir, d)) and d not in SUBDIRS)
        extra = []
        for d in extra_dirs:
            extra += files_in(os.path.join(rdir, d))
        all_files = [p for d in SUBDIRS for p, _ in sub[d]] + [p for p, _ in extra]

        raw_chat = [p for p, _ in sub["inputs"] if RAW_CHAT_RE.search(os.path.basename(p))]
        raw_chat_external = any("chat-export" in str(s) or "user-attachments" in str(s)
                                for s in as_list(meta.get("source_paths")))
        registers = [p for p in all_files if REGISTER_RE.search(os.path.basename(p))
                     and not p.endswith("README.md")]
        incident_register = [p for p in registers if re.search(r"incident|error-analysis", p)]
        golden = [p for p in registers if "golden" in p]
        criteria = [p for p in registers if re.search(r"criteria|rubric", p)]

        fb_kind, fb_size, fb_quotes = classify_feedback(sub["feedback"])

        # lessons-as-rules: look in feedback + register/how-not-to/improvement files
        lesson_files = [p for p, _ in sub["feedback"]] + [
            p for p in all_files if re.search(r"how-not-to|improvement|quality-findings|review|error-analysis|prompts-chain",
                                              os.path.basename(p))]
        lesson_files = sorted(set(p for p in lesson_files if p.endswith(".md")))
        rule_hits = {}
        lesson_section_files = []
        lesson_prompt_links = []       # prompts/ path inside a file that has a lesson section
        version_used_lines = []        # prompts/ path + version on the same line (any md file of the run)
        for p in sorted(set(lesson_files + [x for x in all_files if x.endswith(".md")])):
            t = read(p)
            if p in lesson_files:
                hits = len(RULE_RE.findall(t))
                if hits:
                    rule_hits[p] = hits
            has_lesson_section = bool(LESSON_SECTION_RE.search(t))
            if has_lesson_section:
                lesson_section_files.append(p)
            for line in t.splitlines():
                for m in TARGET_PROMPT_RE.finditer(line):
                    with_ver = bool(VERSION_NEAR_RE.search(line))
                    if with_ver:
                        version_used_lines.append({"file": p, "target": m.group(0)})
                    if has_lesson_section:
                        lesson_prompt_links.append({"file": p, "target": m.group(0), "version_on_line": with_ver})
        lesson_to_prompt = bool(lesson_prompt_links)
        lesson_to_prompt_version = any(x["version_on_line"] for x in lesson_prompt_links)
        prompt_backlinks = PROMPT_BACKLINKS.get(name, [])
        golden_inventory_rows = GOLDEN_INVENTORY.get(name[4:], 0)

        related_artifacts = [a for a in as_list(meta.get("related_artifacts"))
                             if isinstance(a, str) and a.startswith(("prompts/", "standards/"))]
        related_prompts = [a for a in related_artifacts if a.startswith("prompts/")]

        sr = parse_rate(get_metric(meta, "success_rate"))
        sr_basis = get_metric(meta, "success_rate_basis")
        verdict = get_metric(meta, "verdict")
        has_metrics = isinstance(meta.get("metrics"), dict) or any(
            k in meta for k in ("success_rate", "verdict", "tokens", "duration", "eval"))
        ba_detected = get_metric(meta, "incidents_detected_by_ba")

        human_fb = fb_kind == "human-ba"
        dialog_stored = bool(raw_chat) or any("/steps/" in x for x in all_files)
        fb_text = "\n".join(read(p) for p, _ in sub["feedback"])
        structured = bool(incident_register) or any("quality-findings" in p for p in registers) or bool(
            re.search(r"Реестр (дефектов|галлюцинаций)|^\| *(Г|Д-|D|C|E)\d", fb_text, re.M))
        ba_signal = human_fb or fb_kind == "ba-reconstructed" or bool(ba_detected)

        # Completeness scale L0..L4 (see runs_evolution.md):
        #  L0 metadata + outputs only (no dialog, no BA signal)
        #  L1 + dialog of usage stored (export/transcript/steps) -- what the prompt did
        #  L2 + human BA verdict/feedback on errors (free text, quotes)
        #  L3 + structured, countable error register (IDs, categories, detection)
        #  L4 + closed loop: lesson -> target prompt file + version -> regression case/check
        closed_loop = lesson_to_prompt_version and bool(prompt_backlinks) and bool(golden)
        if closed_loop:
            level = 4
        elif structured and ba_signal:
            level = 3
        elif ba_signal:
            level = 2
        elif dialog_stored:
            level = 1
        else:
            level = 0

        status = str(meta.get("status", ""))
        failed_signal = status in ("needs-rework", "invalid", "partial-success", "works-with-edits") or \
            (sr is not None and sr < 0.8) or bool(incident_register)
        success_signal = status == "success" or (sr is not None and sr >= 0.8) or bool(golden) or \
            any("success-criteria" in p for p in all_files)

        runs.append({
            "run_id": meta.get("run_id", name),
            "num": n,
            "period": period_of(n),
            "date": str(meta.get("date", "")),
            "process": meta.get("process"),
            "run_type": meta.get("run_type", "(absent→execution)"),
            "status": status,
            "model": meta.get("model"),
            "author": meta.get("author"),
            "files": {d: {"count": len(sub[d]), "bytes": sum(s for _, s in sub[d])} for d in SUBDIRS},
            "non_contract_files": [p for p, _ in extra],
            "has_metrics": has_metrics,
            "success_rate": sr,
            "success_rate_basis": sr_basis if isinstance(sr_basis, str) else None,
            "verdict": verdict,
            "related_artifacts_prompts_standards": related_artifacts,
            "related_prompts": related_prompts,
            "prompt_version_recorded": any(VERSION_NEAR_RE.search(a) for a in related_prompts),
            "related_issues": [str(x) for x in as_list(meta.get("related_issues"))],
            "raw_chat_in_inputs": raw_chat,
            "raw_chat_external_only": (not raw_chat) and raw_chat_external,
            "structured_registers": registers,
            "incident_register": incident_register,
            "golden_candidates": golden,
            "criteria_or_rubric": criteria,
            "feedback_kind": fb_kind,
            "feedback_bytes": fb_size,
            "feedback_quotes": fb_quotes,
            "feedback_substantive_ba": human_fb and fb_size > 300,
            "lessons_as_rules_hits": rule_hits,
            "lesson_section_files": lesson_section_files,
            "lesson_to_prompt": lesson_to_prompt,
            "lesson_to_prompt_version": lesson_to_prompt_version,
            "lesson_prompt_links": lesson_prompt_links,
            "prompt_version_used_lines": version_used_lines,
            "prompt_files_backlinking_run": prompt_backlinks,
            "golden_inventory_391_rows": golden_inventory_rows,
            "rfc_register_mentions": RFC_REGISTER.get(name, 0),
            "incidents_detected_by_ba": ba_detected,
            "dialog_stored": dialog_stored,
            "structured_error_register": structured,
            "closed_loop": closed_loop,
            "completeness_level": level,
            "failed_usage_signal": failed_signal,
            "success_usage_signal": success_signal,
        })
    return runs


def main():
    runs = inventory()
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(runs, fh, ensure_ascii=False, indent=2)

    N = len(runs)
    p = lambda *a: print(*a)
    p(f"runs: {N}  -> {os.path.relpath(OUT_JSON, ROOT)}")
    for key in ("run_type", "status", "feedback_kind", "completeness_level"):
        p(f"\n{key}:", dict(Counter(str(r[key]) for r in runs).most_common()))
    p("\nmodel not-recorded / missing:",
      sum(1 for r in runs if not r["model"] or "not-recorded" in str(r["model"]) or "не предоставлен" in str(r["model"])))
    p("has metrics:", sum(r["has_metrics"] for r in runs),
      "| numeric success_rate:", sum(r["success_rate"] is not None for r in runs),
      "| with basis:", sum(bool(r["success_rate_basis"]) for r in runs))
    p("raw chat in inputs:", sum(bool(r["raw_chat_in_inputs"]) for r in runs),
      "| external-only chat:", sum(r["raw_chat_external_only"] for r in runs))
    p("empty inputs:", sum(r["files"]["inputs"]["count"] == 0 for r in runs),
      "| empty feedback:", sum(r["files"]["feedback"]["count"] == 0 for r in runs),
      "| empty logs:", sum(r["files"]["logs"]["count"] == 0 for r in runs))
    p("incident register:", [r["run_id"] for r in runs if r["incident_register"]])
    p("golden candidates:", [r["run_id"] for r in runs if r["golden_candidates"]])
    p("criteria/rubric:", [r["run_id"] for r in runs if r["criteria_or_rubric"]])
    p("incidents_detected_by_ba:", {r["run_id"]: r["incidents_detected_by_ba"] for r in runs if r["incidents_detected_by_ba"]})
    p("substantive human BA feedback:", [r["run_id"] for r in runs if r["feedback_substantive_ba"]])
    p("lessons-as-rules (any hit):", sum(bool(r["lessons_as_rules_hits"]) for r in runs))
    p("lesson sections (Предложения/Что править/...):", [r["run_id"] for r in runs if r["lesson_section_files"]])
    p("lesson -> prompts/ path:", [r["run_id"] for r in runs if r["lesson_to_prompt"]])
    p("lesson -> prompt + version:", [r["run_id"] for r in runs if r["lesson_to_prompt_version"]])
    p("prompt version used recorded in run files:", [r["run_id"] for r in runs if r["prompt_version_used_lines"]])
    p("prompts/ files back-linking run:", {r["run_id"]: r["prompt_files_backlinking_run"] for r in runs if r["prompt_files_backlinking_run"]})
    p("issue-391 golden inventory rows:", {r["run_id"]: r["golden_inventory_391_rows"] for r in runs if r["golden_inventory_391_rows"]})
    p("docs/rfc/rfc-register.md mentions:", {r["run_id"]: r["rfc_register_mentions"] for r in runs if r["rfc_register_mentions"]})
    p("closed loop (L4):", [r["run_id"] for r in runs if r["closed_loop"]])
    p("dialog stored:", sum(r["dialog_stored"] for r in runs), "| structured error register:", sum(r["structured_error_register"] for r in runs))
    p("related prompts/ in metadata:", sum(bool(r["related_prompts"]) for r in runs),
      "| with version/SHA:", sum(r["prompt_version_recorded"] for r in runs))
    p("failed-usage signal:", sum(r["failed_usage_signal"] for r in runs),
      "| success-usage signal:", sum(r["success_usage_signal"] for r in runs))
    p("non-contract dirs:", {r["run_id"]: r["non_contract_files"] for r in runs if r["non_contract_files"]})

    by_period = defaultdict(Counter)
    for r in runs:
        by_period[r["period"]][r["completeness_level"]] += 1
    p("\nlevel by period:")
    for per in sorted(by_period):
        p(f"  {per}: " + ", ".join(f"L{k}={v}" for k, v in sorted(by_period[per].items())))
    p("\nper run: id period level fb_kind status sr")
    for r in runs:
        p(f"  {r['run_id']} {r['period'][:2]} L{r['completeness_level']} {r['feedback_kind']:<17} "
          f"{r['status']:<17} {r['success_rate']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
