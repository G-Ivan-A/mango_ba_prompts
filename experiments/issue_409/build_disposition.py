#!/usr/bin/env python3
"""Построить реестр диспозиции файлов для issue #409.

Скрипт читает дерево базового коммита (по умолчанию ``upstream/main`` на
момент исследования), присваивает каждому файлу диспозицию по упорядоченным
правилам и подсчитывает входящие ссылки как свидетельство использования.

Выход:
  * experiments/issue_409/disposition.json — машиночитаемый реестр;
  * docs/analysis/2026-10-31-file-disposition-register.md — человекочитаемый
    реестр (генерируется, вручную не правится).

Запуск: ``python3 experiments/issue_409/build_disposition.py [BASE_SHA]``.
Повторный запуск на том же SHA даёт байт-в-байт тот же результат.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "6f6cbc477f4b482d3c10bd4d941cbfb481fccf1f"
OUT_JSON = ROOT / "experiments/issue_409/disposition.json"
OUT_MD = ROOT / "docs/analysis/2026-10-31-file-disposition-register.md"
AUDIT_DOC = "../audit/2026-10-31-repository-audit.md"

# --- Словарь диспозиций ------------------------------------------------------
# Порядок важен только для отчёта. Значения согласованы с жизненным циклом
# standards/artifact-deprecation-standard.md Хаба (active / deprecated /
# superseded / archived) и с ограничением issue #409 о статистике runs/.
DISPOSITIONS = {
    "current": "Актуален: роль и содержание соответствуют текущим требованиям; оставить как есть.",
    "update": "Актуальная роль, устаревшее содержание: актуализировать отдельной задачей по RFC/ADR.",
    "relocate": "Содержание актуально, но дом или имя нарушают структуру Хаба: перенести отдельной задачей с редиректом ссылок.",
    "historical": "Историческое свидетельство: оставить на месте, не актуализировать; разметка — правилом каталога или блоком перехода.",
    "archive-candidate": "Не используется или заменён: active → deprecated/superseded → archived по стандарту депрекации Хаба.",
    "archived": "Уже в архиве: только metadata и обязательные ссылки.",
    "generated": "Производный файл: SSOT — генератор и его источники; руками не правится.",
    "statistics": "Статистика runs/: заморожена по ограничению issue #409; не изменяется и не актуализируется.",
}

# --- Последующие задачи (полные постановки — в docs/analysis/2026-10-31-follow-up-tasks.md)
TASKS = {
    "T-01": "Bootstrap Хаба: AGENTS.md, archetype/environment в .hub-profile.json, docs/README.md",
    "T-02": "Стратегические документы: docs/vision.md, concept.md, architecture.md, roadmap.md + ADR, заменяющий границы #263",
    "T-03": "Разделение docs/ba-ecosystem.md и перевод дорожной карты сайта на docs/roadmap.md",
    "T-04": "Актуализация карты процессов, таксономии и паттернов под BCREQ A-IN/A-CORE",
    "T-05": "Вывод локального KB-конвейера после переезда KB в mango-ba-ai-runtime (#361)",
    "T-06": "Структура docs/: docs/contracts, файлы корня docs/, дубли, регистрация RFC",
    "T-07": "Разметка истории: блоки перехода, политика датированных свидетельств, статусы ADR, архив логов",
    "T-08": "SSOT и связи: синхронизация с Хабом, mango-ba-ai-runtime, видимость (ADR-009), ссылки на ветки форка",
    "T-09": "Этап 2: единый источник пакета OpenCode (ADR-016 ↔ dist/execution-package-opencode Хаба)",
}

# Файлы, которые по разделам аудита требуют содержательной актуализации.
# Ключ — путь, значение — (код причины, задача).
UPDATE = {
    "README.md": ("Видение #263 «только уровни 1–2, без сервера и агентов», «evals и golden-set отсутствуют», ссылка на ветку форка, ai-ba-playbooks как публичная витрина", "T-02"),
    "ai-governance/ai-governance.md": ("Закреплено «GitHub — единственная платформа» и приватизация по ADR-009; противоречит этапам 3–4", "T-02"),
    "ai-rules/ai-quick-rules.md": ("Краткие правила наследуют формулировки видения #263; синхронизировать после T-02", "T-02"),
    "ai-rules/AI_SESSION_HANDOVER_PROMPT.md": ("Шаблон передачи сессии ссылается на ворота видения #263; синхронизировать после T-02", "T-02"),
    "scripts/validate_issue_263_vision_alignment.py": ("Валидатор запирает видение #263 (REQUIRED_TEXT/CONCEPT_DOCS); меняется вместе с ADR из T-02", "T-02"),
    "docs/ba-ecosystem.md": ("Сборный документ: методология + дорожная карта L1–L4 + границы «уровни 3–4 не план»; ai-generated во frontmatter; источник roadmap.json сайта", "T-03"),
    "scripts/generate-pages-data.mjs": ("Дорожная карта сайта парсится из docs/ba-ecosystem.md; ссылки на docs/contracts/", "T-03"),
    "docs/ba-processes/00-index.md": ("Процессы «Формирование/Валидация ФТ/ТЗ» заменены стадиями A-IN/A-CORE; источник дерева процессов сайта", "T-04"),
    "docs/ba-processes/00-index.executable.md": ("Исполняемый спутник 00-index.md; синхронно с T-04", "T-04"),
    "docs/ba-processes/README.md": ("Навигация по процессам 2026-06; синхронно с T-04", "T-04"),
    "docs/taxonomy.md": ("Таксономия операций 2026-06 — источник сайта; сверить с BCREQ и метамоделью Хаба", "T-04"),
    "standards/kb-standard.md": ("Стандарт KB описывает локальный kb/processed, который перенесён в mango-ba-ai-runtime", "T-05"),
    "kb/README.md": ("Описывает локальную KB до переезда (#361)", "T-05"),
    "kb/USAGE.md": ("9 ссылок на kb/processed после переезда KB", "T-05"),
    "kb/sources/README.md": ("21 ссылка на kb/processed после переезда KB", "T-05"),
    "kb/processed/README.md": ("Указатель актуален, но frontmatter содержит запрещённый Хабом ai-generated", "T-05"),
    "Makefile": ("Цели kb-* пишут в kb/processed (MANGO_OUT, LK_OUT), который перенесён", "T-05"),
    ".github/workflows/kb.yml": ("CI KB-конвейера целится в kb/processed после переезда", "T-05"),
    "CONTRIBUTING.md": ("4 ссылки на kb/processed после переезда", "T-05"),
    "scripts/validate_issue_111_kb_pipeline.py": ("Валидатор KB-конвейера ссылается на kb/processed", "T-05"),
    "scripts/validate_issue_115_kb_mango_pipeline.py": ("Валидатор KB-конвейера ссылается на kb/processed", "T-05"),
    "scripts/validate_issue_310_kb_pdf_ingestion.py": ("Валидатор KB-конвейера ссылается на kb/processed", "T-05"),
    "scripts/test_validate_pagination_shift.py": ("Тест ссылается на kb/processed", "T-05"),
    "scripts/validate_pagination_shift.py": ("Проверка пагинации KB работает с kb/processed", "T-05"),
    "docs/contracts/kb-citations.md": ("Контракт цитирования KB ссылается на kb/processed; дом docs/contracts запрещён", "T-05"),
    ".hub-profile.json": ("Нет archetype/environment (bootstrap v2.0); last_sync 3bfa4103 от 2026-08-17", "T-01"),
    "docs/hub-research-dependencies.md": ("Мост к Хабу актуален, но не называет mango-ba-ai-runtime и projects/ba-ai-process", "T-08"),
    "pr-ops/artifact-map.md": ("Карта артефактов: ADR-009 Хаба смешан с локальным ADR 009; нет mango-ba-ai-runtime", "T-08"),
    "pr-ops/BACKLOG.md": ("Маркеры «evals отсутствуют» устарели после golden-set #373–#378", "T-08"),
    "docs/rfc-hub-integration.md": ("RFC в корне docs/ (нарушение HTOM) и описание ai-ba-playbooks как публичной методологии", "T-06"),
    "docs/rfc/rfc-register.md": ("Реестр не содержит RFC 2026-10 (manual pipeline, modernization); ai-generated во frontmatter", "T-06"),
    "docs/adr/2026-10-adr-016-ide-client-process.md": ("Не связан с dist/execution-package-opencode Хаба (#652) и средами 1–4", "T-09"),
    "docs/analysis/2026-10-30-ide-clients-stage-2.md": ("Рекомендация OpenCode V1 без сверки с пакетом Хаба; дополнить по T-09", "T-09"),
    "prompts/README.md": ("Навигация актуальна; ai-generated во frontmatter и ссылка на docs/contracts", "T-06"),
    "standards/README.md": ("Перечень стандартов: отметить исторические стандарты 2026-06 после T-04/T-05", "T-07"),
}

UPDATE["patterns/README.md"] = ("Матрица паттернов привязана к процессам «Формирование/Валидация ФТ/ТЗ»", "T-04")

RELOCATE = {
    "docs/contracts/bcreq-manual-state.md": ("Хаб запрещает docs/contracts/; дом — standards/ или docs/ba-processes/", "T-06"),
    "docs/contracts/bcreq-stage-gates.md": ("Хаб запрещает docs/contracts/; дом — standards/ или docs/ba-processes/; на файл ссылается сайт", "T-06"),
    "docs/kb-experiment-report.md": ("Отчёт в корне docs/; дом — docs/report/ (историческое свидетельство)", "T-06"),
    "docs/site-access.md": ("Инструкция доступа к сайту в корне docs/; дом определяет docs/README.md", "T-06"),
}

ARCHIVE = {
    "docs/ba-process/README.md": ("Дубль docs/ba-processes/ (2026-06-18)", "T-06"),
    "docs/task-for-konard-template.md": ("Шаблон постановки на конкретного исполнителя (2026-06-13); шаблоны не хранятся как документы (HTOM)", "T-06"),
    "docs/superpowers/plans/2026-08-31-issue-339-followup.md": ("План инструмента без frontmatter, задача закрыта", "T-07"),
    "docs/superpowers/plans/2026-08-31-issue-343-run-0063.md": ("План инструмента без frontmatter, задача закрыта", "T-07"),
    "docs/.gitkeep": ("Каталог docs/ не пуст; маркер не нужен", "T-06"),
    ".gitkeep": ("Маркер пустого каталога в корне репозитория не нужен", "T-06"),
    "docs/adr/.gitkeep": ("Каталог docs/adr/ не пуст; маркер не нужен", "T-06"),
    "kb/.gitkeep": ("Каталог kb/ не пуст; маркер не нужен", "T-05"),
    "prompts/asr-ingestion-legacy.md": ("Режим legacy 2026-06; в каталоге сайта BCREQ-only (#391); заменён asr-ingestion-oneshot", "T-07"),
    "prompts/letter-customer-documentation-legacy.md": ("Режим legacy 2026-06; в каталоге сайта BCREQ-only (#391)", "T-07"),
    "pr-ops/migration-issues-registry.md": ("Миграция 2026-06 завершена; нет frontmatter", "T-07"),
    "pr-ops/migration-manifest.md": ("Миграция 2026-06 завершена", "T-07"),
    "pr-ops/migration-phase1-issues.md": ("Миграция 2026-06 завершена", "T-07"),
    "pr-ops/session-digests.md": ("Дайджесты сессий 2026-06; заменены runs/ и CHANGELOG", "T-07"),
    "pr-ops/sync-matrix-2026-06-17.md": ("Матрица синхронизации на 2026-06-17; заменена ADR-0004 и .hub-profile.json", "T-07"),
    "docs/adr/009-bcreq-formation-process.md": ("proposed 2026-06; процесс BCREQ заменён ADR-012/015 и стадиями A-IN…A-RELEASE; номер конфликтует с ADR-009 Хаба", "T-07"),
    "docs/rfc/knowledge-transfer-to-hub/README.md": ("Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба", "T-07"),
    "docs/rfc/knowledge-transfer-to-hub/ba-ontology.md": ("Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба", "T-07"),
    "docs/rfc/knowledge-transfer-to-hub/bcreq-process.md": ("Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба", "T-07"),
    "docs/rfc/knowledge-transfer-to-hub/operations-taxonomy.md": ("Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба", "T-07"),
    "docs/rfc/knowledge-transfer-to-hub/pages-ux.md": ("Передача знаний в Хаб 2026-06 выполнена через research/ba-requirements Хаба", "T-07"),
    "docs/rfc/rfc-to-hub-001-knowledge-transfer.md": ("RFC в Хаб 2026-06; результат поглощён метамоделью Хаба", "T-07"),
}

# Июньские ADR в статусе proposed: решение (accept / reject / supersede) не
# зафиксировано — это недостающее представление жизненного цикла.
ADR_DECIDE = {
    "docs/adr/003-ba-ontology.md", "docs/adr/004-operations-taxonomy.md",
    "docs/adr/005-artifact-team-naming.md", "docs/adr/006-prompt-naming.md",
    "docs/adr/007-kb-standard.md", "docs/adr/008-industry-standards-standard.md",
    "docs/adr/010-pages-ux.md",
}

# Июньские стандарты, опирающиеся на до-BCREQ модель процессов.
STANDARD_UPDATE = {
    "standards/pattern-standard.md": ("Паттерны 2026-06 до BCREQ; синхронно с T-04", "T-04"),
    "standards/product-classification-contract.md": ("Контракт 2026-06-04; сверить с таксономией #399 и ADR-013", "T-04"),
    "standards/team-directory.md": ("Справочник команд 2026-06; сверить с portal-маппингом ADR-013", "T-04"),
    "standards/pages-ux-standard.md": ("UX сайта 2026-06 (дерево процессов); сайт стал BCREQ-only (#391)", "T-03"),
}

LOOSE_EXPERIMENT_LOG = re.compile(r"^experiments/[^/]+\.log$")

# Ссылки на временные ветки форка исполнителя: после удаления ветки они
# ломаются, а все их цели существуют в main апстрима (находка F-19).
FORK_LINK = re.compile(r"github\.com/konard/G-Ivan-A-mango_ba_prompts/(?:blob|tree)/")
FORK_LINK_EXEMPT = {
    # Записи журнала изменений — история, не правятся.
    "CHANGELOG.md": "записи журнала — история",
    # Аналитика #407: ссылки заменены на main в PR #410.
    "docs/analysis/2026-10-30-repository-current-state.md": "исправлено в PR #410",
    "docs/analysis/2026-10-30-ecosystem-compliance.md": "исправлено в PR #410",
    "docs/analysis/2026-10-30-october-requirements-evolution.md": "исправлено в PR #410",
    # RFC модернизации переписан до v0.3 в PR #410.
    "docs/rfc/2026-10-repository-modernization.md": "переписан в PR #410",
}

# ---------------------------------------------------------------------------


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True,
                          capture_output=True).stdout


def tracked_files(base: str) -> list[str]:
    return sorted(line for line in git("ls-tree", "-r", "--name-only", base).splitlines() if line)


def read_blob(base: str, path: str) -> str:
    try:
        raw = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, check=True,
                             capture_output=True).stdout
    except subprocess.CalledProcessError:
        return ""
    if b"\0" in raw[:4096]:
        return ""
    return raw.decode("utf-8", errors="replace")


FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def frontmatter(text: str) -> dict:
    match = FM_RE.match(text)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def classify(path: str, fm: dict, machine_refs: int, text: str = "") -> tuple[str, str, str]:
    """Вернуть (диспозиция, основание, задача)."""

    disposition, reason, task = classify_base(path, fm, machine_refs)
    if disposition == "current" and path not in FORK_LINK_EXEMPT and FORK_LINK.search(text):
        return ("update", "Ссылки на временную ветку форка konard/G-Ivan-A-mango_ba_prompts; "
                "цели существуют в main (F-19)", "T-08")
    return disposition, reason, task


def classify_base(path: str, fm: dict, machine_refs: int) -> tuple[str, str, str]:
    """Диспозиция по роли и каталогу, без проверки ссылок форка."""

    status = fm.get("status", "")

    if path.startswith("runs/"):
        return "statistics", "Каталог runs/ — статистика; ограничение issue #409", ""
    if path.startswith(".archive/"):
        return "archived", "Каталог .archive/ — канонический архив (issue #291)", ""
    if path.startswith("prompts/archive/"):
        return "archived", "Каталог архивных промптов (issue #388); источник раздела «архив» на сайте", ""
    if path in UPDATE:
        reason, task = UPDATE[path]
        return "update", reason, task
    if path in RELOCATE:
        reason, task = RELOCATE[path]
        return "relocate", reason, task
    if path in ARCHIVE:
        reason, task = ARCHIVE[path]
        return "archive-candidate", reason, task
    if path in STANDARD_UPDATE:
        reason, task = STANDARD_UPDATE[path]
        return "update", reason, task
    if path in ADR_DECIDE:
        return "update", f"ADR в статусе {status or '—'} с 2026-06: нужно решение accept / reject / supersede", "T-07"
    if path.startswith("site/data/"):
        return "generated", "Генерирует scripts/generate-pages-data.mjs (github-pages.yml)", ""
    if path.startswith("site/reports/"):
        return "generated", "Статический отчётный сайт issue #335 (experiments/issue_335_build_report_site.py)", ""
    if path.startswith("site/screenshots/"):
        return "historical", "Скриншоты приёмки сайта; свидетельство PR", ""
    if path == "site/password-hashes.json":
        return "generated", "Генерирует scripts/set-site-password.mjs (issue #388)", ""
    if path.startswith("site/"):
        return "current", "Код сайта Этапа 1 (GitHub Pages)", ""
    if path.startswith("docs/screenshots/"):
        return "historical", "Скриншоты приёмки PR; свидетельство", ""
    if LOOSE_EXPERIMENT_LOG.match(path):
        return "archive-candidate", "Несвязанный лог эксперимента в корне experiments/ (issue #317)", "T-07"
    if path.startswith("experiments/"):
        if machine_refs:
            return "historical", "Данные эксперимента, читаемые валидатором/скриптом; свидетельство задачи", ""
        return "historical", "Скрипт или данные эксперимента закрытой задачи; свидетельство", ""
    if path.startswith("docs/taxonomy/"):
        return "current", "Данные каталога продуктов и документации (#399, #401; ADR-013/014)", ""
    if path.startswith(("docs/audit/", "docs/report/", "docs/reviews/")):
        return "historical", "Датированное свидетельство (HTOM: audit/reviews — evidence)", ""
    if path.startswith("docs/analysis/"):
        if path.startswith(("docs/analysis/2026-10-30-", "docs/analysis/ide-clients-stage-2/")):
            return "current", "Аналитика, на которую опирается открытое RFC модернизации / ADR-016", ""
        if path.startswith("docs/analysis/2026-10-31-"):
            return "current", "Аналитика issue #409", ""
        return "historical", "Анализ — снимок на дату; выводы перенесены в стандарты/ADR или устарели", ""
    if path.startswith("docs/adr/"):
        return "current", f"Решение в статусе {status or '—'}; действует", ""
    if path.startswith("docs/rfc/"):
        if status in ("proposed", "draft"):
            return "current", f"RFC в статусе {status}; ожидает решения владельца", ""
        return "current", "RFC", ""
    if path.startswith("docs/contracts/"):
        return "relocate", "Хаб запрещает docs/contracts/", "T-06"
    if path.startswith("docs/ba-processes/"):
        return "current", "Процесс BCREQ (источник вкладки «Процессы» сайта)", ""
    if path.startswith("patterns/"):
        return "update", "Пример паттерна 2026-06 для до-BCREQ процесса; синхронно с T-04", "T-04"
    if path.startswith("standards/bcreq"):
        return "current", "Стандарт BCREQ (#387, #395, #403)", ""
    if path.startswith("standards/"):
        return "current", f"Локальный стандарт ({status or '—'})", ""
    if path.startswith("prompts/"):
        return "current", "Промпт или навигация каталога", ""
    if path.startswith("scripts/kb/"):
        return "update", "Скрипт KB-конвейера пишет в kb/processed, перенесённый в mango-ba-ai-runtime", "T-05"
    if path.startswith("kb/sources/"):
        return "update", "Метаданные источников KB; SSOT KB теперь mango-ba-ai-runtime/docs/kb", "T-05"
    if path.startswith("kb/"):
        if path == "kb/STRUCTURE_REVIEW.md":
            return "historical", "Ревью структуры KB 2026-08 до переезда", ""
        return "update", "Локальная KB после переезда в mango-ba-ai-runtime", "T-05"
    if path.startswith("scripts/"):
        return "current", "Валидатор, тест или инструмент, подключённый к validate_all/CI", ""
    if path.startswith("tools/"):
        return "current", "Валидаторы Хаба и локальная дельта", ""
    if path.startswith(".github/"):
        return "current", "CI и шаблоны issue", ""
    if path.startswith(("ai-rules/", "ai-governance/")):
        return "current", f"Правила работы AI ({status or '—'})", ""
    if path.startswith("pr-ops/"):
        return "current", "Операционный реестр", ""
    if path in ("CHANGELOG.md", "LICENSE", ".gitignore", ".gitattributes"):
        return "current", "Служебный файл корня", ""
    return "current", "Без признаков устаревания", ""


def main() -> None:
    files = tracked_files(BASE)
    texts = {p: read_blob(BASE, p) for p in files}
    # Ссылки ищем только в нестатистических файлах: runs/ заморожен и не
    # является потребителем, который нужно мигрировать.
    consumers = {p: t for p, t in texts.items() if t and not p.startswith("runs/")}
    machine = {p: t for p, t in consumers.items()
               if p.startswith(("scripts/", "tools/", ".github/")) or p == "Makefile"}

    entries = []
    for path in files:
        fm = frontmatter(texts[path]) if path.endswith(".md") else {}
        needle = path
        refs = sum(1 for p, t in consumers.items() if p != path and needle in t)
        mrefs = sum(1 for p, t in machine.items() if p != path and needle in t)
        disposition, reason, task = classify(path, fm, mrefs, texts[path])
        entries.append({
            "path": path,
            "area": path.split("/")[0] if "/" in path else "(корень)",
            "status": fm.get("status", ""),
            "updated": fm.get("updated", ""),
            "ai_generated": "ai-generated" in fm,
            "disposition": disposition,
            "reason": reason,
            "task": task,
            "inbound_refs": refs,
            "machine_refs": mrefs,
        })

    counts = Counter(e["disposition"] for e in entries)
    by_area = defaultdict(Counter)
    for e in entries:
        by_area[e["area"]][e["disposition"]] += 1
    by_task = Counter(e["task"] for e in entries if e["task"])

    payload = {
        "issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409",
        "baseline_sha": BASE,
        "generator": "experiments/issue_409/build_disposition.py",
        "file_count": len(entries),
        "dispositions": DISPOSITIONS,
        "tasks": TASKS,
        "counts": dict(sorted(counts.items())),
        "ai_generated_files": sorted(e["path"] for e in entries if e["ai_generated"]),
        "entries": entries,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload, by_area, by_task), encoding="utf-8")
    print(json.dumps(payload["counts"], ensure_ascii=False))


def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def render_md(payload: dict, by_area: dict, by_task: Counter) -> str:
    base = payload["baseline_sha"]
    entries = payload["entries"]
    order = list(DISPOSITIONS)
    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        "updated: 2026-10-31",
        "temperature: 0.1",
        "analysis-subtype: inventory",
        'source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/409"',
        "scope: repo",
        f'based_on: "https://github.com/G-Ivan-A/mango_ba_prompts/tree/{base}"',
        "---",
        "",
        "# Реестр диспозиции файлов: актуален, обновить, история, архив",
        "",
        "Файл сгенерирован скриптом "
        "[`experiments/issue_409/build_disposition.py`](../../experiments/issue_409/build_disposition.py) "
        "из дерева коммита "
        f"[`{base[:8]}`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/{base}); "
        "вручную не правится. Машиночитаемая копия — "
        "[`experiments/issue_409/disposition.json`](../../experiments/issue_409/disposition.json). "
        f"Выводы и обоснования — в [аудите репозитория]({AUDIT_DOC}).",
        "",
        "Реестр отвечает на требование issue #409 «файлы репозитория или актуальны, или вынесены "
        "в архив; исторические файлы размечены». Диспозиция — **предложение**: ни один файл "
        "этим PR не перемещён и не изменён. Исполнение — задачи T-01…T-09 после согласования RFC.",
        "",
        "## Словарь диспозиций",
        "",
        "| Диспозиция | Что означает | Файлов |",
        "| --- | --- | ---: |",
    ]
    for key in order:
        lines.append(f"| `{key}` | {DISPOSITIONS[key]} | {payload['counts'].get(key, 0)} |")
    lines.append(f"| **Итого** | Все отслеживаемые файлы базового коммита | **{payload['file_count']}** |")
    lines += [
        "",
        "Метод доказательства использования: «входящие ссылки» — число нестатистических файлов "
        "(вне `runs/`), содержащих полный путь файла; «машинные» — то же только среди `scripts/`, "
        "`tools/`, `.github/` и `Makefile`. Это нижняя граница: относительные ссылки внутри каталога "
        "по одному имени файла не учитываются. Ноль ссылок не доказывает ненужность, но снижает риск "
        "архивирования; ненулевые машинные ссылки означают, что перенос требует правки потребителя.",
        "",
        "## Сводка по областям",
        "",
        "| Область | " + " | ".join(f"`{k}`" for k in order) + " | Всего |",
        "| --- | " + " | ".join("---:" for _ in order) + " | ---: |",
    ]
    for area in sorted(by_area):
        row = by_area[area]
        lines.append(f"| `{area}` | " + " | ".join(str(row.get(k, 0)) for k in order)
                     + f" | {sum(row.values())} |")
    lines += [
        "",
        "## Сводка по задачам",
        "",
        "| Задача | Содержание | Файлов |",
        "| --- | --- | ---: |",
    ]
    for task, title in TASKS.items():
        lines.append(f"| {task} | {title} | {by_task.get(task, 0)} |")
    lines += [
        "",
        "## Запрещённое поле ai-generated",
        "",
        "Хаб запрещает `ai-generated` во frontmatter (AGENTS.md Хаба, раздел запретов; локальный "
        "`tools/validate-frontmatter.sh` отклоняет поле, но проверяет только корень, `ai-rules/` и `tools/`). "
        f"Поле найдено в {len(payload['ai_generated_files'])} файлах; из них "
        f"{sum(1 for p in payload['ai_generated_files'] if p.startswith('runs/'))} — в `runs/` "
        "(статистика, не исправляется). Вне `runs/` (задача T-07, удаление поля — правка metadata, "
        "допустимая и для исторических файлов):",
        "",
    ]
    for path in payload["ai_generated_files"]:
        if not path.startswith("runs/"):
            lines.append(f"- `{path}`")
    lines += [
        "",
        "## Статистика runs/",
        "",
        "Каталог `runs/` целиком имеет диспозицию `statistics`: он не актуализируется, не "
        "переносится и не размечается заново. Новая статистика по изменившимся требованиям "
        "накапливается новыми RUN; сравнение со старыми RUN — задача анализа, а не правки.",
        "",
        "| Каталог RUN | Файлов |",
        "| --- | ---: |",
    ]
    run_dirs = Counter("/".join(e["path"].split("/")[:3]) if e["path"].count("/") >= 2 else e["path"]
                       for e in entries if e["disposition"] == "statistics")
    for run_dir in sorted(run_dirs):
        lines.append(f"| `{run_dir}` | {run_dirs[run_dir]} |")
    lines += [
        "",
        "## Пофайловый реестр (вне runs/)",
        "",
        "| Путь | status | updated | Диспозиция | Основание | Задача | Ссылки (всего / машинные) |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for e in entries:
        if e["disposition"] == "statistics":
            continue
        lines.append(
            f"| `{md_escape(e['path'])}` | {e['status'] or '—'} | {e['updated'] or '—'} | "
            f"`{e['disposition']}` | {md_escape(e['reason'])} | {e['task'] or '—'} | "
            f"{e['inbound_refs']} / {e['machine_refs']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
