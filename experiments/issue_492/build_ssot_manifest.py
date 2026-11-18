#!/usr/bin/env python3
"""ФТ-3 issue #492: манифест передачи SSOT этапа 1 в mango-ba-ai-runtime.

Скрипт статический: читает файлы спицы на закреплённом коммите-источнике
(``git show <commit>:<path>``), считает sha256, берёт версию из frontmatter или
JSON, строит цепочку эволюции и политику синхронизации. Клиентские данные и
вложения в манифест не попадают: только пути, версии, хэши и метаданные.
Runtime не меняется: клон читается только для проверки, есть ли в нём уже
побайтная копия артефакта.

Выход:

* ``docs/contracts/ssot-stage1-handoff-manifest.json`` — машиночитаемый манифест;
* ``docs/contracts/ssot-stage1-handoff-manifest.md`` — та же информация для чтения.

Запуск::

    RUNTIME_CLONE=/путь/к/клону python3 experiments/issue_492/build_ssot_manifest.py \
        > experiments/issue_492/build-ssot-manifest.log

``SOURCE_COMMIT`` — merge PR #491 в main, база ветки issue #492. Смена коммита —
это новая закреплённая передача: новый манифест, а не правка копии в runtime.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_runtime_deps import ROOT, git, registry_sha, runtime_clone  # noqa: E402

SOURCE_COMMIT = os.environ.get("SOURCE_COMMIT", "7dea8f716d69e55c183865630d10f40cdb6e46b1")
HUB_REPO = "G-Ivan-A/mango_ba_prompts"
RUNTIME_REPO = "G-Ivan-A/mango-ba-ai-runtime"
OUT_JSON = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.json"
OUT_MD = ROOT / "docs/contracts/ssot-stage1-handoff-manifest.md"
MANIFEST_VERSION = "0.1"
ROUTE = "docs/ba-processes/bcreq-a-in-route.json"
INSTRUCTIONS = "docs/ba-processes/bcreq-a-in-instructions.json"
ARCHIVE_MANIFEST = "prompts/archive/a-in-v2.7.0/manifest.json"
RUN_KIT = "docs/ba-processes/bcreq-run-kit.md"
FORBIDDEN_PREFIXES = ("runs/", "kb/", "inputs/", "attachments/")

V01_STEP = {
    "prompts/bcreq-context-understanding-stepwise.md": "Ш-1",
    "prompts/bcreq-products-impact-analysis-stepwise.md": "Ш-2",
    "prompts/bcreq-in-understanding-oneshot.md": "A-IN one-shot",
    "prompts/drafts/bcreq-intake-questionnaire-stepwise.md": "Ш-А",
    "prompts/drafts/bcreq-context-understanding-stepwise.md": "Ш-1",
    "prompts/drafts/bcreq-products-impact-analysis-stepwise.md": "Ш-2",
}

# Группы ФТ-3 в порядке issue. ``card`` — карточка ФТ-4, которой группа
# переносится в runtime закреплённой копией.
GROUPS = [
    ("ain-route", "Маршрут A-IN и 24 контракта шагов", "BL-186",
     lambda p: p in {ROUTE, INSTRUCTIONS, "docs/ba-processes/bcreq-a-in-common.md",
                     "docs/ba-processes/bcreq-a-in-execution.md",
                     "docs/rfc/2026-11-a-in-decomposition.md"} or p.startswith("prompts/drafts/a-in/")),
    ("system-format", "Системный формат шагов (#490)", "BL-185",
     lambda p: p.startswith("prompts/drafts/system/")),
    ("archive-2.7.0", "Архив 2.7.0 и его манифест", "BL-185",
     lambda p: p.startswith("prompts/archive/a-in-v2.7.0/")),
    ("drafts", "Черновики Ш-ХХ «по тесту»", "BL-185",
     lambda p: p.startswith("prompts/drafts/") and p.count("/") == 2),
    ("prompts-v0.1", "14 промптов v0.1 и комплект прогона", "BL-185",
     lambda p: (p.startswith("prompts/bcreq-") and p.count("/") == 1) or p == RUN_KIT),
    ("step-handoff", "Итог шага (step-handoff)", "BL-186",
     lambda p: p == "docs/ba-processes/bcreq-step-handoff.md"),
    ("base-standard", "Базовый стандарт и профили", "BL-187",
     lambda p: p in {"standards/bcreq-prompt-base-standard.md", "standards/bcreq-prompt-profiles.md"}),
    ("catalog-39", "Каталог 39 операций", "BL-187",
     lambda p: p.startswith("standards/bcreq-manual-classes/")),
    ("section-meta-standards", "Мета-стандарты разделов", "BL-187",
     lambda p: p.startswith("standards/bcreq-sections/")),
    ("industry-practice", "Отраслевая практика", "BL-187",
     lambda p: p == "standards/bcreq-industry-practice.md"),
    ("evidence-normalization", "Нормализация доказательств", "BL-186",
     lambda p: p == "docs/ba-processes/bcreq-evidence-normalization.md"),
    ("lessons", "Реестр уроков", "BL-187",
     lambda p: p.startswith("standards/bcreq-lessons/")),
    ("runtime-references", "Реестр справочников runtime", "BL-187",
     lambda p: p == "standards/bcreq-runtime-references.md"),
    # Нормы класса (б) из ФТ-2, которых нет в перечне issue, но без которых
    # шаги не исполняются: включены, чтобы перенос был полным.
    ("execution-norms", "Прочие нормы исполнения шагов (ФТ-2, класс б)", "BL-187",
     lambda p: p in {"standards/bcreq-composition-standard.md", "standards/bcreq-prompt-architecture.md",
                     "standards/product-classification-contract.md"}),
    ("gates-and-cs", "Контракт гейтов и поток CS (ФТ-2, класс б)", "BL-188",
     lambda p: p in {"docs/contracts/bcreq-stage-gates.md", "docs/ba-processes/cs-flow-stub.md"}),
]


def show(path: str) -> bytes:
    import subprocess
    return subprocess.run(["git", "show", f"{SOURCE_COMMIT}:{path}"], cwd=ROOT,
                          check=True, capture_output=True).stdout


def frontmatter(text: str) -> dict:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep and not line.startswith((" ", "-")):
                meta[key.strip()] = value.strip().strip('"')
    return meta


def version_of(path: str, data: bytes) -> tuple[str | None, str]:
    text = data.decode("utf-8")
    if path.endswith(".json"):
        payload = json.loads(text)
        if isinstance(payload, dict):
            for key in ("version", "siteVersion"):
                if key in payload:
                    return str(payload[key]), f"JSON `{key}`"
        return None, "нет версии в файле: фиксирует sha256"
    meta = frontmatter(text)
    if meta.get("version"):
        return meta["version"], "frontmatter `version`"
    return None, "нет версии в файле: фиксирует sha256"


def run_kit_modes() -> dict[str, str]:
    text = show(RUN_KIT).decode("utf-8")
    modes = {}
    for row in re.findall(r"^\| (?:\d+|—) \| (.*)$", text, re.M):
        cells = [c.strip() for c in row.split(" | ")]
        if len(cells) < 4:
            continue
        link = re.search(r"\(\.\./\.\./(prompts/[^)]+\.md)\)", cells[1])
        if link:
            modes.setdefault(link.group(1), cells[2].split()[0].strip("`"))
        draft = re.search(r"\(\.\./\.\./(prompts/drafts/[^)]+\.md)\)", cells[3])
        if draft:
            modes.setdefault(draft.group(1), "by-test")
    return modes


def chain_status(path: str, group: str, modes: dict, replaced: dict) -> tuple[str, str]:
    step = V01_STEP.get(path)
    if step and step in replaced:
        return "заменён", (f"{step}: в A-IN заменён шагами {', '.join(replaced[step])} "
                           "(RFC-AIN-001, надстройка #474); файл сохранён для библиотеки и истории")
    if group == "archive-2.7.0":
        return "архив", "Замороженная редакция сайта 2.7.0: только история и источник системного формата"
    if group == "ain-route":
        return "действует", "Формат шагов по умолчанию; RFC-AIN-001 принят (#474); тексты draft, не измерены"
    if group == "system-format":
        return "действует", "Альтернативный формат «системные (комплексные шаги)» (#490), собран из архива 2.7.0"
    if path == RUN_KIT:
        return "действует", "Комплект прогона: таблица шагов и режимов, определяет действующие редакции"
    if path == "prompts/drafts/manifest.json":
        return "действует", "Манифест сборки черновиков «по тесту» (`scripts/build_bcreq_step_prompts.py`)"
    if path in modes:
        return "действует", f"Комплект прогона: режим `{modes[path]}`"
    if path.endswith("-oneshot.md") and group == "prompts-v0.1":
        return "действует", "Стадийный one-shot библиотеки (A-CORE или A-WORK); в таблице комплекта — альтернатива шагам"
    if group == "drafts":
        return "черновик", "Черновик «по тесту» вне таблицы комплекта"
    return "действует", "Норма исполнения шагов этапа 1"


def main() -> int:
    clone = runtime_clone()
    pinned = registry_sha()
    runtime_main = git("rev-parse", "origin/main", cwd=clone).strip()
    runtime_blobs = set()
    for ref in (runtime_main, pinned):
        runtime_blobs |= {line.split()[2] for line in git("ls-tree", "-r", ref, cwd=clone).splitlines()}

    tracked = git("ls-tree", "-r", "--name-only", SOURCE_COMMIT).splitlines()
    archive = json.loads(show(ARCHIVE_MANIFEST))
    replaced = {entry["step"]: entry["replacedBy"] for entry in archive["entries"]}
    modes = run_kit_modes()

    artifacts = []
    seen = set()
    for gid, title, card, match in GROUPS:
        for path in tracked:
            if path in seen or not match(path):
                continue
            if not (path.endswith(".md") or path.endswith(".json")):
                continue
            seen.add(path)
            data = show(path)
            version, version_source = version_of(path, data)
            meta = frontmatter(data.decode("utf-8")) if path.endswith(".md") else {}
            status, status_note = chain_status(path, gid, modes, replaced)
            blob = git("rev-parse", f"{SOURCE_COMMIT}:{path}").strip()
            item = {
                "path": path, "group": gid, "version": version, "version_source": version_source,
                "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "git_blob": blob,
                "source_commit": SOURCE_COMMIT,
                "last_changed_commit": git("log", "-1", "--format=%H", SOURCE_COMMIT, "--", path).strip(),
                "file_status": meta.get("status"), "chain_status": status, "chain_note": status_note,
                "transfer_card": card, "in_runtime": blob in runtime_blobs,
            }
            if meta.get("based_on"):
                base = meta["based_on"]
                item["based_on"] = base
                item["based_on_sha256"] = meta.get("based_on_sha256")
                try:
                    item["based_on_sha256_matches_source_commit"] = (
                        hashlib.sha256(show(base)).hexdigest() == meta.get("based_on_sha256"))
                except Exception:  # noqa: BLE001 — цель могла быть удалена до коммита-источника
                    item["based_on_sha256_matches_source_commit"] = None
            if meta.get("assembled_by"):
                item["assembled_by"] = meta["assembled_by"]
            artifacts.append(item)

    for item in artifacts:
        if item["path"].startswith(FORBIDDEN_PREFIXES):
            raise SystemExit(f"клиентские данные или вложения в манифесте: {item['path']}")

    route = json.loads(show(ROUTE))
    instructions = json.loads(show(INSTRUCTIONS))
    by_path = {a["path"]: a for a in artifacts}
    contracts = []
    for step in route["steps"]:
        number = step["id"].split("-")[1]
        prompt = next(p for p in by_path if p.startswith(f"prompts/drafts/a-in/bcreq-ain-{number}-"))
        canonical = json.dumps(instructions[step["id"]], ensure_ascii=False, sort_keys=True).encode("utf-8")
        contracts.append({
            "id": step["id"], "name": step["name"], "operation": step["operation"],
            "next": step["next"], "route_version": route["version"],
            "prompt": prompt, "prompt_version": by_path[prompt]["version"],
            "prompt_sha256": by_path[prompt]["sha256"],
            "instruction_sha256": hashlib.sha256(canonical).hexdigest(),
        })

    v01 = [a["path"] for a in artifacts if a["group"] == "prompts-v0.1" and a["path"] != RUN_KIT]
    evolution = [
        {"stage": "v0.1", "title": "14 промптов потока BCREQ",
         "paths": v01, "count": len(v01),
         "in_force": [p for p in v01 if by_path[p]["chain_status"] == "действует"],
         "replaced": {p: replaced[V01_STEP[p]] for p in v01 if p in V01_STEP and V01_STEP[p] in replaced},
         "note": "Ш-0, Ш-3…Ш-9, Ш-В, Ш-С действуют в комплекте прогона; Ш-1, Ш-2 и A-IN one-shot "
                 "в A-IN заменены AIN-01…24, файлы сохранены для библиотеки и истории."},
        {"stage": "по тесту", "title": "Черновики Ш-ХХ (BL-156), собраны из v0.1",
         "paths": [a["path"] for a in artifacts if a["group"] == "drafts"],
         "based_on": {a["path"]: a.get("based_on") for a in artifacts if a["group"] == "drafts"},
         "note": "Черновики собираются `scripts/build_bcreq_step_prompts.py` из базового стандарта, "
                 "профилей, каталога и реестра; Ш-А и Ш-Р существуют только как черновики."},
        {"stage": "2.7.0", "title": "Комплект сайта 2.7.0 (архив)",
         "paths": [a["path"] for a in artifacts if a["group"] == "archive-2.7.0"],
         "archive_source_commit": archive["sourceCommit"],
         "publication_commit": archive["publicationCommit"],
         "replaced": replaced,
         "note": "Ш-А, Ш-1, Ш-2 и A-IN one-shot заморожены как полные тексты 2.7.0; замены — в manifest.json архива."},
        {"stage": "AIN v0.3", "title": "24 отдельных вызова A-IN по RFC-AIN-001",
         "paths": [c["prompt"] for c in contracts], "route_version": route["version"],
         "route_status": route["status"], "decision": route["decision"],
         "note": "Действующий формат по умолчанию: Ш-0 → AIN-01…24 → ФТ после handover AIN-24 и Г-IN."},
        {"stage": "системный формат", "title": "Комплексные шаги Ш-А, Ш-1, Ш-2 из архива 2.7.0",
         "paths": [a["path"] for a in artifacts if a["group"] == "system-format"],
         "based_on": {a["path"]: a.get("based_on") for a in artifacts if a["group"] == "system-format"},
         "note": "Альтернатива AIN v0.3 по выбору БА на сайте (#490); остальные шаги общие."},
    ]

    sync_policy = {
        "pattern": "hub-sync: закреплённая копия",
        "rules": [
            "Runtime хранит побайтную копию артефактов манифеста, закреплённую на `source_commit`; "
            "SSOT остаётся в mango_ba_prompts.",
            "Локальные правки закреплённых копий в runtime запрещены: расхождение устраняется "
            "следующей передачей, а не редактированием копии.",
            "Обновление — только новой закреплённой передачей: новый манифест с новым "
            "`source_commit`, новыми sha256 и записью в журнале передач runtime.",
            "Проверка копии — равенство sha256 файла в runtime значению манифеста; несовпадение — дефект передачи.",
            "Ссылки внутри перенесённых файлов переписываются на путь в runtime, если цель тоже "
            "перенесена, иначе на permalink спицы с закреплённым SHA (как `scripts/sync_from_hub.py`).",
            "Тексты промптов в спице до принятия манифеста не меняются; замена ссылок (б) — отдельная задача BL-190.",
        ],
        "precedents": [
            {"where": HUB_REPO, "what": "ADR-0004 и scripts/sync_from_hub.py: рабочие копии Хаба на "
             "`source_sha`, локальные правки запрещены, обновление — следующим синком; .hub-profile.json "
             "хранит last_sync и sync_history."},
            {"where": RUNTIME_REPO, "what": "compilation-manifest.yaml: база знаний скопирована из спицы "
             "на 8cbf82aa73129ec5747af07f790aaf438b0fb6e9, каталог продуктов — на "
             "e3597fd74da9c4f631ca46697c643462e2cf0b85; `hub_access_required_at_runtime: false`."},
        ],
        "runtime_task": "Приём манифеста — RFC-задача в runtime; issue в runtime создаёт владелец (раздел 6 реестра справочников).",
    }

    groups = []
    for gid, title, card, _ in GROUPS:
        items = [a for a in artifacts if a["group"] == gid]
        groups.append({"id": gid, "title": title, "transfer_card": card, "count": len(items),
                       "chain_status": dict(Counter(a["chain_status"] for a in items))})
        if not items:
            raise SystemExit(f"пустая группа {gid}")

    deps = json.loads((ROOT / "experiments/issue_492/runtime-deps.json").read_text(encoding="utf-8"))
    links = json.loads((ROOT / "experiments/issue_492/prompt-links.json").read_text(encoding="utf-8"))
    manifest = {
        "manifest": "ssot-stage1-handoff", "version": MANIFEST_VERSION, "issue": 492,
        "status": "draft: ждёт принятия владельцем и RFC-задачи в runtime",
        "source_repository": HUB_REPO, "source_commit": SOURCE_COMMIT,
        "target_repository": RUNTIME_REPO, "runtime_registry_sha": pinned,
        "runtime_main_observed": runtime_main, "hash": "sha256 байтов файла на source_commit",
        "excluded": "Клиентские данные и вложения не включаются: только пути, версии, хэши и "
                    "метаданные; пути runs/, kb/, inputs/, attachments/ запрещены.",
        "runtime_changed": False,
        "summary": {
            "artifacts": len(artifacts), "contracts": len(contracts),
            "in_runtime": sum(a["in_runtime"] for a in artifacts),
            "chain_status": dict(Counter(a["chain_status"] for a in artifacts)),
            "transfer_cards": dict(Counter(a["transfer_card"] for a in artifacts)),
        },
        "inputs": {
            "dependency_audit": {"path": "experiments/issue_492/runtime-deps.json",
                                 "summary": {k: deps["summary"][k] for k in deps["summary"]
                                             if k in {"runtime_paths", "by_status", "in_scope_rows", "by_ref_type_in_scope"}}},
            "link_classification": {"path": "experiments/issue_492/prompt-links.json",
                                    "by_class": links["summary"]["by_class"],
                                    "missing_in_runtime": links["summary"]["missing_in_runtime"],
                                    "replacement_candidates": links["summary"]["replacement_candidates"]},
        },
        "groups": groups,
        "contracts": contracts,
        "evolution": evolution,
        "sync_policy": sync_policy,
        "artifacts": artifacts,
    }
    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(manifest), encoding="utf-8")

    print(f"source_commit={SOURCE_COMMIT} registry_sha={pinned} runtime_main={runtime_main}")
    print(json.dumps(manifest["summary"], ensure_ascii=False))
    for group in groups:
        print(f"group {group['id']}: {group['count']} → {group['transfer_card']} {group['chain_status']}")
    for item in artifacts:
        print(f"{item['sha256']} {item['version'] or '—':>8} {item['chain_status']:<10} "
              f"{item['transfer_card']} runtime={item['in_runtime']} {item['path']}")
    mismatched = [a["path"] for a in artifacts if a.get("based_on_sha256_matches_source_commit") is False]
    print("based_on_sha256 не совпадает с источником на source_commit (редакция-основа обновлена позже "
          "сборки черновика):", mismatched or "—")
    return 0


def render(m: dict) -> str:
    s = m["summary"]
    lines = [
        "---",
        "status: draft",
        f"version: {m['version']}",
        "updated: 2026-11-18",
        "temperature: 0.1",
        "owner: G-Ivan-A",
        "type: contract",
        "scope: ssot-stage1-handoff",
        "related_artifacts:",
        '  - "docs/contracts/ssot-stage1-handoff-manifest.json"',
        '  - "docs/audit/2026-11-18-runtime-dependencies-ssot-handoff.md"',
        '  - "standards/bcreq-runtime-references.md"',
        "related_issues:",
        '  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/492"',
        "---",
        "",
        "# Манифест передачи SSOT этапа 1 в mango-ba-ai-runtime (issue #492)",
        "",
        "Сгенерировано `experiments/issue_492/build_ssot_manifest.py` из "
        "[JSON-манифеста](ssot-stage1-handoff-manifest.json); не править вручную.",
        "Статус: черновик, ждёт принятия владельцем и RFC-задачи в runtime. Runtime этой задачей не менялся.",
        "",
        f"- Источник: `{m['source_repository']}` на коммите `{m['source_commit']}` (merge PR #491).",
        f"- Получатель: `{m['target_repository']}`; SHA реестра справочников `{m['runtime_registry_sha']}`, "
        f"наблюдавшийся main `{m['runtime_main_observed']}`.",
        f"- Хэш: {m['hash']}. {m['excluded']}",
        f"- Артефактов: {s['artifacts']}; контрактов шагов A-IN: {s['contracts']}; уже есть в runtime "
        f"побайтно: {s['in_runtime']}.",
        "- Статусы цепочки: " + ", ".join(f"{k} — {v}" for k, v in sorted(s["chain_status"].items())) + ".",
        "",
        "## 1. Группы и карточки переноса",
        "",
        "| Группа | Содержание | Артефактов | Статусы цепочки | Карточка ФТ-4 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for g in m["groups"]:
        statuses = ", ".join(f"{k} {v}" for k, v in sorted(g["chain_status"].items()))
        lines.append(f"| `{g['id']}` | {g['title']} | {g['count']} | {statuses} | {g['transfer_card']} |")
    lines += ["", "## 2. Цепочка эволюции", "",
              "| Этап | Что это | Файлов | Что действует, что заменено, что в архиве |",
              "| --- | --- | --- | --- |"]
    for e in m["evolution"]:
        lines.append(f"| {e['stage']} | {e['title']} | {len(e['paths'])} | {e['note']} |")
    lines += ["", "Замены по манифесту архива 2.7.0 (`prompts/archive/a-in-v2.7.0/manifest.json`):", "",
              "| Прежний вход | Заменён |", "| --- | --- |"]
    for step, repl in m["evolution"][2]["replaced"].items():
        lines.append(f"| {step} | {', '.join(repl)} |")
    lines += ["", "## 3. Политика синхронизации", ""]
    lines += [f"{i}. {rule}" for i, rule in enumerate(m["sync_policy"]["rules"], 1)]
    lines += ["", "Прецеденты:", ""]
    lines += [f"- `{p['where']}`: {p['what']}" for p in m["sync_policy"]["precedents"]]
    lines += ["", m["sync_policy"]["runtime_task"], "",
              "## 4. Маршрут A-IN: 24 контракта шагов", "",
              "| Шаг | Название | Операция | Дальше | Версия маршрута | Промпт | Версия | sha256 промпта | sha256 инструкции |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for c in m["contracts"]:
        lines.append(f"| {c['id']} | {c['name']} | {c['operation']} | {c['next']} | {c['route_version']} | "
                     f"[`{Path(c['prompt']).name}`](../../{c['prompt']}) | {c['prompt_version']} | "
                     f"`{c['prompt_sha256'][:16]}…` | `{c['instruction_sha256'][:16]}…` |")
    lines += ["", "## 5. Артефакты", "",
              "Полные sha256 и коммиты последнего изменения — в JSON.", "",
              "| Путь | Группа | Версия | Статус цепочки | sha256 | Последнее изменение | Карточка |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for a in m["artifacts"]:
        lines.append(f"| [`{a['path']}`](../../{a['path']}) | `{a['group']}` | {a['version'] or '—'} | "
                     f"{a['chain_status']} | `{a['sha256'][:16]}…` | `{a['last_changed_commit'][:8]}` | "
                     f"{a['transfer_card']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
