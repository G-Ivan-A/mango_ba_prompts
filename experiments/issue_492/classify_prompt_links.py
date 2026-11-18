#!/usr/bin/env python3
"""ФТ-2 issue #492: классификация ссылок текстов промптов на mango_ba_prompts.

Что делает (статически, без модельных прогонов, тексты промптов не меняет):

1. Находит в каждом отслеживаемом ``prompts/**/*.md`` (кроме ``README.md``)
   все ссылки ``https://github.com/G-Ivan-A/mango_ba_prompts/...``
   (относительных ссылок из текстов промптов нет — проверяется в журнале).
2. Классифицирует каждое вхождение по упорядоченной таблице правил ``RULES``:
   (а) внутренняя governance-ссылка — допустима, не переносится;
   (б) нормативная для исполнения моделью — должна читаться извне.
   Правило выбирается по контексту (frontmatter, HTML-комментарий, абзац
   происхождения, служебный промпт) и по цели ссылки.
3. Для каждой цели класса (б) проверяет наличие в runtime: точная копия
   (тот же git blob) на main runtime или на SHA реестра, либо явный аналог из
   ``ANALOGS`` с проверкой существования путей на SHA реестра. Есть —
   «кандидат на замену ссылки»; нет — карточка бэклога из ``CARDS``.
4. Сверяет действующие заглушки раздела 4 реестра справочников с ``STUB_CARDS``.

Выход: ``prompt-links.json``, ``prompt-links.md`` рядом со скриптом и журнал
в stdout (сохраняется в ``classify-prompt-links.log``).

Запуск::

    RUNTIME_CLONE=/путь/к/клону python3 experiments/issue_492/classify_prompt_links.py \
        > experiments/issue_492/classify-prompt-links.log

Без ``RUNTIME_CLONE`` скрипт клонирует runtime (``--filter=blob:none``) во
временный каталог. Неизвестная цель или правило без карточки — код выхода 1.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_runtime_deps import REGISTRY, ROOT, git, registry_sha, runtime_clone  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
HUB = "https://github.com/G-Ivan-A/mango_ba_prompts"
LINK = re.compile(
    r"https://(?:github\.com|raw\.githubusercontent\.com)/G-Ivan-A/mango_ba_prompts"
    r"(?:/(?P<kind>blob|tree|raw)/(?P<ref>[^/\s)>\]]+))?"
    r"(?P<path>/[^\s)\]>\"'`|*\\]*)?"
)
RELATIVE = re.compile(r"\]\((?:\.\./|\./)[^)]+\)")

CONSTITUTION = {
    "prompts/bcreq-constitution-governance-oneshot.md",
    "prompts/drafts/bcreq-constitution-governance-oneshot.md",
}
AIN_RFC = "docs/rfc/2026-11-a-in-decomposition.md"
GOVERNANCE_PREFIXES = (
    "docs/rfc/", "docs/adr/", "pr-ops/", "runs/", ".github/", "docs/analysis/",
    "docs/audit/", "experiments/", "prompts/archive/", "prompts/README",
    "docs/ba-ecosystem.md", "(корень)", "issues/*", "pull/*",
)
PROVENANCE = ("Блок собран", "собран сборщиком", "Архив (issue", "заменён набором",
              "Файл сохранён для ссылок", "выведены из")

# Упорядоченная таблица правил: (id, класс, условие, обоснование).
RULES = [
    ("А-0", "а", "ссылка во frontmatter",
     "Метаданные файла (related_issue и т. п.): модель их не исполняет."),
    ("А-1", "а", "ссылка в HTML-комментарии",
     "Служебная пометка (Experimental, маркер сборки): не инструкция модели."),
    ("А-2", "а", "цель — issue или PR",
     "Трассировка решения владельца; правило уже записано в тексте промпта."),
    ("А-3", "а", "служебный промпт вне потока BCREQ",
     "Промпт обслуживания сессий спицы: результат сохраняется в pr-ops спицы, "
     "обязательная структура вывода перечислена в самом тексте."),
    ("А-4", "а", "абзац происхождения встроенного текста",
     "Указывает, из чего собран или чем заменён текст; правила перенесены "
     "дословно, модели не нужно открывать источник."),
    ("А-5", "а", "цель — RFC, ADR, pr-ops, runs, архив, issue-шаблоны, анализ",
     "Документ управления и истории решений; норма для исполнения в нём не "
     "вынесена (RFC #427, раздел 8.1: правила исполнения в справочник не выносятся)."),
    ("Б-1", "б", "цель — конституция Ш-0",
     "Шаги требуют «Прочитай полную конституцию из Ш-0»: Р1…Р7, АД, АП, КС, БС "
     "и гейты действуют на каждом шаге."),
    ("Б-2", "б", "цель — RFC-AIN-001",
     "Общий контракт A-IN: «приоритет у принятого RFC-AIN-001 и этого контракта»."),
    ("А-6", "а", "цель — другой промпт набора без якоря",
     "Навигация: модель называет следующий промпт, текст промпта вводит БА."),
    ("Б-3", "б", "цель — правило другого промпта по якорю",
     "Шаг ссылается на конкретное правило другого шага как на действующую норму."),
    ("Б-4", "б", "цель — реестр справочников runtime",
     "БС-18 «промпт ДОЛЖЕН ссылаться» на И-7; AIN «Runtime: версии и источники»."),
    ("Б-5", "б", "цель — стандарт в standards/",
     "Мета-стандарт или стандарт, по которому модель строит вывод шага."),
    ("Б-6", "б", "цель — контракт в docs/contracts/",
     "Контракт гейтов и возвратов, по которому шаг принимает решение."),
    ("Б-7", "б", "цель — процесс в docs/ba-processes/",
     "Процессный SSOT (итог шага, исполнение A-IN, поток CS), читаемый шагом."),
]
RULE_INDEX = {rule[0]: rule for rule in RULES}

# Аналоги в runtime, которые полностью заменяют нормативную функцию цели.
ANALOGS = {
    "standards/bcreq-runtime-references.md": {
        "note": "Нормативная функция реестра для модели — указать справочники "
                "И-1…И-8 на закреплённом SHA; сами справочники есть в runtime "
                "(БС-18 → И-7 `taxonomy/source-tiers.yaml`). Замена: прямые "
                "закреплённые ссылки на справочники runtime; реестр остаётся "
                "governance-индексом спицы и входит в манифест ФТ-3.",
        "registry_ids": True,
    },
}
# Частичные аналоги: отмечаются, но не снимают задачу.
PARTIAL = {
    "docs/contracts/bcreq-stage-gates.md": "В runtime есть только чек-лист G-human "
        "`evaluation/g-human-checklist.md` (И-8); гейты Г-IN/Г-W и возвраты — нет.",
    "standards/product-classification-contract.md": "В runtime есть значения "
        "таксономии `taxonomy/mango-products.yaml` (И-2), но не правила классификации.",
    "standards/bcreq-sections/README.md": "В runtime есть шаблон документа "
        "`templates/bcreq-skeleton.md` (И-3), но не мета-стандарты разделов.",
}

# Карточки ФТ-4: группа переноса = то, что runtime принимает одним закреплённым
# переносом (одни потребители, одна версия). Деление по файлам — инфляция.
CARDS = {
    "BL-185": {
        "title": "Конституция Ш-0 и промпты набора этапа 1 в runtime",
        "match": lambda p: p in CONSTITUTION or (p.startswith("prompts/") and not p.startswith("prompts/archive/")),
    },
    "BL-186": {
        "title": "Маршрут A-IN, контракты AIN и итог шага в runtime",
        "match": lambda p: p in {AIN_RFC, "docs/ba-processes/bcreq-a-in-execution.md",
                                 "docs/ba-processes/bcreq-step-handoff.md",
                                 "docs/ba-processes/bcreq-evidence-normalization.md"},
    },
    "BL-187": {
        "title": "Стандарты исполнения шагов в runtime",
        "match": lambda p: p.startswith("standards/") and p != "standards/bcreq-runtime-references.md",
    },
    "BL-188": {
        "title": "Контракт гейтов и поток CS в runtime",
        "match": lambda p: p in {"docs/contracts/bcreq-stage-gates.md", "docs/ba-processes/cs-flow-stub.md"},
    },
}
STUB_CARDS = {"З-2": "BL-189"}
LINK_FIX_CARD = "BL-190"


def group_of(path: str) -> str:
    if path.startswith("prompts/drafts/a-in/"):
        return "AIN v0.3"
    if path.startswith("prompts/drafts/system/"):
        return "системный формат"
    if path.startswith("prompts/archive/a-in-v2.7.0/"):
        return "архив 2.7.0"
    if path.startswith("prompts/archive/"):
        return "архив до BCREQ"
    if path.startswith("prompts/drafts/"):
        return "черновики Ш-ХХ"
    if Path(path).name.startswith("bcreq-"):
        return "v0.1 (14 промптов)"
    return "служебные промпты"


def target_of(match: re.Match) -> tuple[str, str]:
    raw = match.group("path") or "/"
    path, _, anchor = raw.partition("#")
    path = path.rstrip(".,;:")
    parts = path.strip("/").split("/")
    if parts[0] in {"issues", "pull"} and len(parts) >= 2:
        return f"{parts[0]}/*", anchor
    if path in {"", "/"}:
        return "(корень)", anchor
    return path.lstrip("/"), anchor


def is_kit_prompt(path: str) -> bool:
    return path.startswith("prompts/") and not path.startswith("prompts/archive/") and path.endswith(".md")


def classify(prompt: str, target: str, anchor: str, in_front: bool, in_comment: bool,
             paragraph: str) -> str:
    if in_front:
        return "А-0"
    if in_comment:
        return "А-1"
    if target in {"issues/*", "pull/*"}:
        return "А-2"
    if group_of(prompt) == "служебные промпты":
        return "А-3"
    if any(key in paragraph for key in PROVENANCE):
        return "А-4"
    if target in CONSTITUTION:
        return "Б-1"
    if target == AIN_RFC:
        return "Б-2"
    if target.startswith(GOVERNANCE_PREFIXES):
        return "А-5"
    if is_kit_prompt(target):
        return "Б-3" if anchor else "А-6"
    if target == "standards/bcreq-runtime-references.md":
        return "Б-4"
    if target.startswith("standards/"):
        return "Б-5"
    if target.startswith("docs/contracts/"):
        return "Б-6"
    if target.startswith("docs/ba-processes/"):
        return "Б-7"
    raise SystemExit(f"нет правила для {prompt} → {target}")


def spans(pattern: str, text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(pattern, text, re.S)]


def inside(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in ranges)


def paragraph_at(text: str, pos: int) -> str:
    start = text.rfind("\n\n", 0, pos)
    end = text.find("\n\n", pos)
    return text[start + 1 if start >= 0 else 0: end if end >= 0 else len(text)]


def runtime_blobs(clone: Path, ref: str) -> dict[str, str]:
    out = git("ls-tree", "-r", ref, cwd=clone)
    blobs = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        blobs.setdefault(meta.split()[2], path)
    return blobs


def registry_runtime_paths(pinned: str) -> dict[str, list[str]]:
    text = (ROOT / REGISTRY).read_text(encoding="utf-8")
    result = {}
    for row in re.findall(r"^\| (И-\d+) \|(.*)$", text, re.M):
        paths = re.findall(rf"mango-ba-ai-runtime/blob/{pinned}/([^)\s]+)\)", row[1])
        result[row[0]] = sorted(set(paths))
    return result


def active_stubs() -> list[dict]:
    text = (ROOT / REGISTRY).read_text(encoding="utf-8")
    section = text.split("## 4. Заглушки", 1)[1].split("Снятые заглушки", 1)[0]
    stubs = []
    for row in re.findall(r"^\| (З-\d+) \|(.*)$", section, re.M):
        cells = [cell.strip() for cell in row[1].strip(" |").split("|")]
        stubs.append({"id": row[0], "handbook": cells[0], "steps": cells[2],
                      "label": cells[3].strip("`"), "runtime_task": cells[4]})
    return stubs


def path_exists(clone: Path, ref: str, path: str) -> bool:
    return bool(git("ls-tree", ref, "--", path, cwd=clone).strip())


def main() -> int:
    clone = runtime_clone()
    pinned = registry_sha()
    runtime_main = git("rev-parse", "origin/main", cwd=clone).strip()
    head = git("rev-parse", "HEAD").strip()
    blobs = {"main": runtime_blobs(clone, runtime_main), "pinned": runtime_blobs(clone, pinned)}
    handbooks = registry_runtime_paths(pinned)

    prompts = [p for p in git("ls-files", "prompts").split("\n")
               if p.endswith(".md") and Path(p).name != "README.md"]
    relative = []
    occurrences = []
    for prompt in prompts:
        text = (ROOT / prompt).read_text(encoding="utf-8")
        relative += [f"{prompt}: {m.group(0)}" for m in RELATIVE.finditer(text)]
        front = spans(r"\A---\n.*?\n---\n", text)
        comments = spans(r"<!--.*?-->", text)
        for match in LINK.finditer(text):
            target, anchor = target_of(match)
            line_no = text.count("\n", 0, match.start()) + 1
            rule = classify(prompt, target, anchor, inside(match.start(), front),
                            inside(match.start(), comments), paragraph_at(text, match.start()))
            occurrences.append({
                "prompt": prompt, "group": group_of(prompt), "line": line_no,
                "target": target, "anchor": anchor, "ref": match.group("ref") or "",
                "rule": rule, "class": RULE_INDEX[rule][1],
            })

    targets: dict[str, dict] = {}
    for occ in occurrences:
        item = targets.setdefault(occ["target"], {
            "target": occ["target"], "occurrences": 0, "classes": Counter(),
            "rules": Counter(), "groups": Counter(), "prompts": set()})
        item["occurrences"] += 1
        item["classes"][occ["class"]] += 1
        item["rules"][occ["rule"]] += 1
        item["groups"][occ["group"]] += 1
        item["prompts"].add(occ["prompt"])

    problems = []
    for name, item in targets.items():
        item["prompts"] = len(item["prompts"])
        normative = item["classes"].get("б", 0) > 0
        item["normative"] = normative
        decision = {"runtime": None, "decision": "governance: остаётся ссылкой спицы, не переносится",
                    "card": None, "note": ""}
        if normative:
            local = ROOT / name
            blob = git("hash-object", str(local)).strip() if local.is_file() else None
            copy = {ref: blobs[ref].get(blob) for ref in blobs} if blob else {}
            if any(copy.values()):
                decision.update(runtime=[p for p in copy.values() if p],
                                decision="кандидат на замену ссылки: в runtime есть точная копия",
                                card=LINK_FIX_CARD)
            elif name in ANALOGS:
                paths = sorted({p for key, ps in handbooks.items() for p in ps})
                missing = [p for p in paths if not path_exists(clone, pinned, p)]
                if missing:
                    problems.append(f"{name}: аналоги отсутствуют на SHA реестра: {missing}")
                decision.update(runtime=paths, decision="кандидат на замену ссылки: "
                                "справочники реестра есть в runtime на SHA реестра",
                                card=LINK_FIX_CARD, note=ANALOGS[name]["note"])
            else:
                card = next((cid for cid, spec in CARDS.items() if spec["match"](name)), None)
                if card is None:
                    problems.append(f"{name}: (б) без артефакта в runtime и без карточки")
                decision.update(decision="нет в runtime: задача в бэклог на перенос "
                                "закреплённой копией", card=card, note=PARTIAL.get(name, ""))
        item.update(decision)

    stubs = active_stubs()
    for stub in stubs:
        stub["card"] = STUB_CARDS.get(stub["id"])
        if not stub["card"]:
            problems.append(f"заглушка {stub['id']} без карточки")

    by_class = Counter(occ["class"] for occ in occurrences)
    by_rule = Counter(occ["rule"] for occ in occurrences)
    by_group = defaultdict(Counter)
    for occ in occurrences:
        by_group[occ["group"]][occ["class"]] += 1
    normative_targets = [t for t in targets.values() if t["normative"]]
    cards_used = sorted({t["card"] for t in normative_targets if t["card"]} | set(STUB_CARDS.values()))

    def plain(item: dict) -> dict:
        return {**item, "classes": dict(item["classes"]), "rules": dict(item["rules"]),
                "groups": dict(item["groups"])}

    payload = {
        "summary": {
            "issue": 492, "repository_commit": head, "registry_sha": pinned,
            "runtime_main": runtime_main, "prompt_files": len(prompts),
            "prompt_files_with_links": len({o["prompt"] for o in occurrences}),
            "occurrences": len(occurrences), "relative_links": len(relative),
            "targets": len(targets), "normative_targets": len(normative_targets),
            "by_class": dict(by_class), "by_rule": dict(sorted(by_rule.items())),
            "by_group": {g: dict(c) for g, c in sorted(by_group.items())},
            "replacement_candidates": sorted(t["target"] for t in normative_targets
                                             if t["card"] == LINK_FIX_CARD),
            "missing_in_runtime": sorted(t["target"] for t in normative_targets
                                         if t["card"] != LINK_FIX_CARD),
            "cards": cards_used, "problems": problems,
        },
        "rules": [{"id": r[0], "class": r[1], "condition": r[2], "rationale": r[3]} for r in RULES],
        "cards": {cid: spec["title"] for cid, spec in CARDS.items()}
                 | {STUB_CARDS["З-2"]: "Примеры разделов И-4 (РТ-2, заглушка З-2)",
                    LINK_FIX_CARD: "Замена ссылок (б) в текстах промптов на runtime"},
        "registry_handbooks": handbooks,
        "stubs": stubs,
        "targets": [plain(t) for t in sorted(targets.values(), key=lambda t: (-t["occurrences"], t["target"]))],
        "occurrences": occurrences,
    }
    (OUT_DIR / "prompt-links.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT_DIR / "prompt-links.md").write_text(render(payload), encoding="utf-8")

    s = payload["summary"]
    print(f"commit={head} registry_sha={pinned} runtime_main={runtime_main}")
    print(f"prompt_files={s['prompt_files']} with_links={s['prompt_files_with_links']} "
          f"occurrences={s['occurrences']} targets={s['targets']} relative_links={s['relative_links']}")
    print("by class:", json.dumps(s["by_class"], ensure_ascii=False))
    print("by rule:", json.dumps(s["by_rule"], ensure_ascii=False))
    for group, counts in s["by_group"].items():
        print(f"group {group}: {json.dumps(counts, ensure_ascii=False)}")
    for item in payload["targets"]:
        if item["normative"]:
            print(f"(б) {item['target']} | {item['occurrences']} вхожд. | {item['decision']} | "
                  f"карточка {item['card']} | runtime {item['runtime'] or '—'}")
    for item in payload["targets"]:
        if not item["normative"]:
            print(f"(а) {item['target']} | {item['occurrences']} вхожд. | правила {dict(item['rules'])}")
    for stub in stubs:
        print(f"stub {stub['id']} {stub['handbook']} → {stub['runtime_task']} → карточка {stub['card']}")
    print("problems:", problems or "—")
    return 1 if problems else 0


def render(payload: dict) -> str:
    s = payload["summary"]
    lines = [
        "# Классификация ссылок промптов на mango_ba_prompts (issue #492, ФТ-2)",
        "",
        "Сгенерировано `experiments/issue_492/classify_prompt_links.py`; не править вручную.",
        "Тексты промптов не менялись: это инвентаризация, решения и задачи.",
        "",
        f"- Коммит спицы: `{s['repository_commit']}`; SHA реестра: `{s['registry_sha']}`; "
        f"main runtime: `{s['runtime_main']}`.",
        f"- Файлов промптов: {s['prompt_files']}, со ссылками на спицу: {s['prompt_files_with_links']}; "
        f"вхождений: {s['occurrences']}; целей: {s['targets']}; относительных ссылок: {s['relative_links']}.",
        f"- Класс (а): {s['by_class'].get('а', 0)} вхождений; класс (б): {s['by_class'].get('б', 0)} "
        f"вхождений, {s['normative_targets']} целей.",
        "",
        "## 1. Правила классификации (порядок применения)",
        "",
        "| Правило | Класс | Условие | Обоснование | Вхождений |",
        "| --- | --- | --- | --- | --- |",
    ]
    for rule in payload["rules"]:
        lines.append(f"| {rule['id']} | ({rule['class']}) | {rule['condition']} | {rule['rationale']} | "
                     f"{s['by_rule'].get(rule['id'], 0)} |")
    lines += ["", "## 2. Свод по группам промптов", "",
              "| Группа | (а) | (б) |", "| --- | --- | --- |"]
    for group, counts in s["by_group"].items():
        lines.append(f"| {group} | {counts.get('а', 0)} | {counts.get('б', 0)} |")
    lines += ["", "## 3. Цели класса (б): решение", "",
              "| Цель | Вхождений (б/всего) | Промптов | Есть в runtime | Решение | Карточка | Примечание |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for item in payload["targets"]:
        if not item["normative"]:
            continue
        runtime = ", ".join(f"`{p}`" for p in item["runtime"]) if item["runtime"] else "нет"
        lines.append(f"| `{item['target']}` | {item['classes'].get('б', 0)}/{item['occurrences']} | "
                     f"{item['prompts']} | {runtime} | {item['decision']} | {item['card']} | "
                     f"{item['note'] or '—'} |")
    lines += ["", "## 4. Цели только класса (а): обоснование", "",
              "| Цель | Вхождений | Правила |", "| --- | --- | --- |"]
    for item in payload["targets"]:
        if item["normative"]:
            continue
        rules = ", ".join(f"{rule} ×{count}" for rule, count in sorted(item["rules"].items()))
        lines.append(f"| `{item['target']}` | {item['occurrences']} | {rules} |")
    lines += ["", "## 5. Заглушки реестра справочников (ФТ-4)", "",
              "| Заглушка | Справочник | Шаги | Задача runtime | Карточка |", "| --- | --- | --- | --- | --- |"]
    for stub in payload["stubs"]:
        lines.append(f"| {stub['id']} | {stub['handbook']} | {stub['steps']} | {stub['runtime_task']} | {stub['card']} |")
    lines += ["", "## 6. Карточки бэклога", "", "| Карточка | Содержание |", "| --- | --- |"]
    for cid, title in sorted(payload["cards"].items()):
        lines.append(f"| {cid} | {title} |")
    lines += ["", "## 7. Все вхождения", "",
              "| Промпт | Строка | Группа | Цель | Якорь | Правило | Класс |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for occ in payload["occurrences"]:
        anchor = occ["anchor"].replace("|", "\\|") or "—"
        lines.append(f"| `{occ['prompt']}` | {occ['line']} | {occ['group']} | `{occ['target']}` | "
                     f"{anchor} | {occ['rule']} | ({occ['class']}) |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
