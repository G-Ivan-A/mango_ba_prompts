#!/usr/bin/env python3
"""Замеры для проверки #425: промпты, классы и стандарты BCREQ.

Скрипт только читает репозиторий и пишет `metrics.json` рядом с собой.
Запуск из корня репозитория:

    python3 experiments/issue_425/measure_classes.py

Что считается:
1. Число классов в каталоге и файлов стандартов C01–C39.
2. Доля общего шаблонного текста в 39 стандартах: строка считается общей,
   если после замены номера класса она встречается не менее чем в 30 файлах.
3. Число экземпляров (вставок) по фазам из таблиц README каталога.
4. Отображение 14 действующих промптов на классы (поле `existing`).
5. Объём ручной вставки за полный проход: контракт состояния + стандарт
   класса на каждый экземпляр против маршрута stepwise из 14 промптов.
6. Отнесение классов к архетипам (`archetypes.json`) — полнота и уникальность.
7. Употребление терминов «39 промптов», «39 классов» и т. п. в отслеживаемых
   файлах.
"""
from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CLASSES_DIR = ROOT / "standards" / "bcreq-manual-classes"
CONTRACT = ROOT / "docs" / "contracts" / "bcreq-manual-state.md"
PROCESS = ROOT / "docs" / "ba-processes" / "bcreq-manual-process.md"
PROCESS_V01_REF = "a7fbf928^"
SHARED_MIN_FILES = 30
# Замер #425 сделан в нотации C01…C39. BL-153 (issue #430) переименовал
# операции в К-01…К-39; чтобы замер оставался воспроизводимым, тексты и ID
# приводятся обратно к нотации #425 (одна замена «К-NN» → «CNN»).
LEGACY_ID = re.compile(r"К-(\d\d)")


def legacy(text: str) -> str:
    return LEGACY_ID.sub(r"C\1", text)


def read(path: Path) -> str:
    return legacy(path.read_text(encoding="utf-8"))

TERMS = {
    "39 промптов": r"39\s+промпт",
    "39 классов": r"39\s+класс",
    "39 стандартов": r"39\s+(?:отдельных\s+)?(?:подробных\s+)?стандарт",
    "38 классов": r"38\s+класс",
    "14 промптов": r"14\s+(?:действующих\s+|старых\s+)?промпт",
    "класс промпта": r"класс\w*\s+(?:ручн\w+\s+)?промпт",
}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def load_catalog() -> dict:
    data = json.loads((CLASSES_DIR / "catalog.json").read_text(encoding="utf-8"))
    for item in data["classes"]:
        item["id"] = item.get("history", {}).get("previous_id", item["id"])
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = legacy(value)
    return data


def boilerplate(catalog: dict) -> dict:
    files = [CLASSES_DIR / c["file"] for c in catalog["classes"]]
    bodies = {f.name: strip_frontmatter(read(f)) for f in files}
    norm = {
        name: [re.sub(r"C\d\d", "C??", line).strip() for line in body.splitlines()]
        for name, body in bodies.items()
    }
    presence: collections.Counter[str] = collections.Counter()
    for lines in norm.values():
        presence.update({line for line in lines if line})
    shared_lines = {line for line, n in presence.items() if n >= SHARED_MIN_FILES}
    per_file = []
    for name, lines in norm.items():
        total = sum(len(line) for line in lines if line)
        shared = sum(len(line) for line in lines if line in shared_lines)
        per_file.append({"file": name, "chars": total, "shared_chars": shared})
    total_chars = sum(p["chars"] for p in per_file)
    shared_chars = sum(p["shared_chars"] for p in per_file)
    field_keys = ("name", "inputs", "outputs", "behavior", "stop", "checks")
    specific = [sum(len(c.get(k, "")) for k in field_keys) for c in catalog["classes"]]
    return {
        "files": len(files),
        "chars_total": total_chars,
        "chars_min": min(p["chars"] for p in per_file),
        "chars_max": max(p["chars"] for p in per_file),
        "shared_line_rule": f"строка после замены C?? встречается >= {SHARED_MIN_FILES} файлах",
        "shared_chars_total": shared_chars,
        "shared_share": round(shared_chars / total_chars, 3),
        "catalog_specific_fields": list(field_keys),
        "catalog_specific_chars_avg": round(sum(specific) / len(specific)),
        "catalog_specific_share_avg": round(sum(specific) / total_chars, 3),
    }


def instances() -> dict:
    text = read(CLASSES_DIR / "README.md")
    phase = None
    rows: dict[str, list[str]] = collections.OrderedDict()
    for line in text.splitlines():
        m = re.match(r"^###\s+(a-[a-z]+)\s*$", line)
        if m:
            phase = m.group(1)
            rows[phase] = []
            continue
        if line.startswith("## "):
            phase = None
        m = re.match(r"^\|\s*(a-[a-z]+)/(C\d\d)\s*\|", line)
        if phase and m:
            rows[phase].append(m.group(2))
    per_phase = {p: len(v) for p, v in rows.items()}
    usage = collections.Counter(c for v in rows.values() for c in v)
    return {
        "per_phase": per_phase,
        "total": sum(per_phase.values()),
        "distinct_classes": len(usage),
        "classes_in_all_four_phases": sorted(
            c for c in usage if all(c in v for v in rows.values())
        ),
        "max_repeats_in_one_phase": max(
            collections.Counter(v).most_common(1)[0][1] for v in rows.values() if v
        ),
        "sequence": rows,
    }


def old_prompt_mapping(catalog: dict) -> dict:
    bcreq = sorted(p.name for p in (ROOT / "prompts").glob("bcreq-*.md"))
    mapping: dict[str, list[str]] = {name: [] for name in bcreq}
    other: dict[str, list[str]] = collections.defaultdict(list)
    for c in catalog["classes"]:
        name = Path(c["existing"]).name
        (mapping if name in mapping else other)[name].append(c["id"])
    return {
        "bcreq_prompts": len(bcreq),
        "classes_per_prompt": {k: v for k, v in mapping.items()},
        "prompts_without_class_successor": [k for k, v in mapping.items() if not v],
        "classes_mapped_outside_bcreq": dict(other),
        "max_classes_per_prompt": max(len(v) for v in mapping.values()),
    }


def paste_volume(catalog: dict, inst: dict) -> dict:
    contract = len(read(CONTRACT))
    std = {c["id"]: len(read(CLASSES_DIR / c["file"]))
           for c in catalog["classes"]}
    full = sum(contract + std[c] for seq in inst["sequence"].values() for c in seq)
    without_release = sum(
        contract + std[c]
        for phase, seq in inst["sequence"].items() if phase != "a-release"
        for c in seq
    )
    # Нижняя граница: в одном чате фазы контракт вставлен один раз, стандарт
    # каждого класса — один раз, повторные экземпляры ссылаются на него.
    lower = sum(
        contract + sum(std[c] for c in set(seq))
        for phase, seq in inst["sequence"].items() if phase != "a-release"
    )
    # Маршрут v0.1 на 14 промптах удалён из main в a7fbf928 (#423); читаем его
    # из истории, чтобы сравнение оставалось воспроизводимым.
    process = subprocess.run(
        ["git", "show", f"{PROCESS_V01_REF}:docs/ba-processes/bcreq-manual-process.md"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    route = re.findall(r"\|\s*\d+\s*\|\s*Ш-[^|]*\|[^|]*\|\s*\[(bcreq-[a-z-]+)\]", process)
    old = sum(len((ROOT / "prompts" / f"{n}.md").read_text(encoding="utf-8")) for n in route)
    return {
        "contract_chars": contract,
        "standard_chars_avg": round(sum(std.values()) / len(std)),
        "manual_classes_full_pass_chars": full,
        "manual_classes_without_release_chars": without_release,
        "manual_classes_without_release_lower_bound_chars": lower,
        "stepwise_route_source": f"{PROCESS_V01_REF}:docs/ba-processes/bcreq-manual-process.md (v0.1)",
        "stepwise_route_steps": len(route),
        "stepwise_route_prompts": route,
        "stepwise_route_chars": old,
        "ratio_classes_to_stepwise": round(without_release / old, 2) if old else None,
        "ratio_lower_bound_to_stepwise": round(lower / old, 2) if old else None,
        "note": "Символы вставляемого текста без входных данных задачи; не токены и не стоимость.",
    }


def archetypes(catalog: dict) -> dict:
    data = json.loads((HERE / "archetypes.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in catalog["classes"]]
    assigned = [c for a in data["archetypes"].values() for c in a["classes"]]
    dup = sorted(c for c, n in collections.Counter(assigned).items() if n > 1)
    return {
        "archetypes": len(data["archetypes"]),
        "per_archetype": {k: len(v["classes"]) for k, v in data["archetypes"].items()},
        "unassigned": sorted(set(ids) - set(assigned)),
        "unknown": sorted(set(assigned) - set(ids)),
        "duplicates": dup,
    }


def terminology() -> dict:
    files = subprocess.run(
        ["git", "ls-files", "*.md", "*.json", "*.html", "*.js", "*.yaml", "*.yml"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    skip = ("experiments/issue_425/", "runs/")
    result = {}
    for label, pattern in TERMS.items():
        rx = re.compile(pattern, re.IGNORECASE)
        hits = []
        for rel in files:
            if rel.startswith(skip):
                continue
            path = ROOT / rel
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            n = len(rx.findall(text))
            if n:
                hits.append((rel, n))
        result[label] = {
            "files": len(hits),
            "matches": sum(n for _, n in hits),
            "top": [f"{rel}: {n}" for rel, n in sorted(hits, key=lambda x: -x[1])[:8]],
        }
    return result


def main() -> int:
    catalog = load_catalog()
    class_files = sorted(p.name for p in CLASSES_DIR.glob("[0-9][0-9]-*.md"))
    inst = instances()
    metrics = {
        "issue": 425,
        "catalog_version": catalog["version"],
        "catalog_classes": len(catalog["classes"]),
        "class_files": len(class_files),
        "executable_prompt_files_for_classes": len(list((ROOT / "prompts").glob("**/c[0-9][0-9]-*.md"))),
        "boilerplate": boilerplate(catalog),
        "instances": inst,
        "old_prompts": old_prompt_mapping(catalog),
        "paste_volume": paste_volume(catalog, inst),
        "archetypes": archetypes(catalog),
        "terminology": terminology(),
    }
    out = HERE / "metrics.json"
    out.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    b, i, p = metrics["boilerplate"], metrics["instances"], metrics["paste_volume"]
    print(f"classes={metrics['catalog_classes']} files={metrics['class_files']} "
          f"exec_prompts={metrics['executable_prompt_files_for_classes']}")
    print(f"shared_share={b['shared_share']} specific_share={b['catalog_specific_share_avg']}")
    print(f"instances={i['total']} per_phase={i['per_phase']}")
    print(f"paste classes(no release)={p['manual_classes_without_release_chars']} "
          f"stepwise={p['stepwise_route_chars']} ratio={p['ratio_classes_to_stepwise']}")
    print(f"archetypes={metrics['archetypes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
