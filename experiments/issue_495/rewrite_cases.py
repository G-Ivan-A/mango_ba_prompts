#!/usr/bin/env python3
"""Универсализация кейс-специфики и чистка остаточного балласта в SSOT (issue #495).

Второй шаг после ``clean_sources.py``: точечные смысловые замены, которые
нельзя сделать механически. Каждая замена — точная пара «было → стало» с
ожидаемым числом вхождений; несовпадение числа — ошибка (скрипт ничего не
пишет). Правятся только рукописные источники (SSOT); сгенерированные файлы
пересобираются генераторами.

Реестр «что → куда» для PR печатается флагом ``--register``.

    python3 experiments/issue_495/rewrite_cases.py --dry-run
    python3 experiments/issue_495/rewrite_cases.py
"""
import argparse
import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AMO_OLD = ("Задержка появления записи amoCRM не доказывает способ API-привязки по ID,\n"
           "тайминг SLA или возможность другой CRM.")
AMO_NEW = ("Наблюдаемое поведение внешней системы (например, задержка появления записи)\n"
           "не доказывает способ интеграции, тайминг SLA или переносимость на другую систему.")
AMO_FILES = [
    "prompts/bcreq-constitution-governance-oneshot.md",
    "prompts/bcreq-context-understanding-stepwise.md",
    "prompts/bcreq-core-documentation-oneshot.md",
    "prompts/bcreq-fr-documentation-stepwise.md",
    "prompts/bcreq-in-understanding-oneshot.md",
    "prompts/bcreq-products-impact-analysis-stepwise.md",
    "docs/ba-processes/bcreq-a-in-common.md",
    "docs/ba-processes/bcreq-evidence-normalization.md",
]
ENTRY_FILES = [
    "prompts/bcreq-constitution-governance-oneshot.md",
    "prompts/bcreq-context-understanding-stepwise.md",
    "prompts/bcreq-core-documentation-oneshot.md",
    "prompts/bcreq-fr-documentation-stepwise.md",
    "prompts/bcreq-in-understanding-oneshot.md",
    "prompts/bcreq-products-impact-analysis-stepwise.md",
]
CONST = "prompts/bcreq-constitution-governance-oneshot.md"
PIA = "prompts/bcreq-products-impact-analysis-stepwise.md"
ASR = "prompts/asr-ingestion-oneshot.md"
SDB = "prompts/session-debug-documentation-oneshot.md"
COMMON = "docs/ba-processes/bcreq-a-in-common.md"
HANDOFF = "docs/ba-processes/bcreq-step-handoff.md"
ROUTE = "docs/ba-processes/bcreq-a-in-route.json"
INSTR = "docs/ba-processes/bcreq-a-in-instructions.json"

# (id, файлы, было, стало, ожидаемое число вхождений в файле, класс, куда перенесено)
EDITS = [
    ("U-01", AMO_FILES, AMO_OLD, AMO_NEW, 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-01; в промпте — принцип"),
    ("U-02", [HANDOFF],
     "Нужен, чтобы новизна коннектора не скрыла доработку существующих подсистем.",
     "Нужен, чтобы новизна решения не скрыла доработку существующих подсистем.", 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-03", [HANDOFF], "у каждой связи есть источник; ЛК, права и настройки рассмотрены",
     "у каждой связи есть источник; интерфейсы настройки, права доступа и параметры рассмотрены", 1, "б",
     "продуктовый профиль → runtime taxonomy/product-profiles.yaml"),
    ("U-04", [ROUTE], '"why": "Новизна коннектора не отменяет дельту существующих подсистем"',
     '"why": "Новизна решения не отменяет дельту существующих подсистем"', 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-05", [ROUTE], "статус candidate; ЛК/права/настройки рассмотрены;",
     "статус candidate; интерфейсы настройки, права доступа и параметры рассмотрены;", 1, "б",
     "продуктовый профиль → runtime taxonomy/product-profiles.yaml"),
    ("U-06", [ROUTE], '"decision": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/474"',
     '"decision": "issue #474"', 1, "а", "ссылка → номер решения (карточка)"),
    ("U-07", [INSTR], "опорные и внешние компоненты; ЛК, права, настройки, хранение,",
     "опорные и внешние компоненты; интерфейсы настройки, права доступа, параметры, хранение,", 1, "б",
     "продуктовый профиль → runtime taxonomy/product-profiles.yaml"),
    ("U-08", [INSTR], '"negative_example": "Новый коннектор не отменяет дельту ЛК. ',
     '"negative_example": "Новое решение не отменяет дельту существующих интерфейсов и настроек. ', 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-09", [INSTR], "Аналогия amoCRM не доказывает полный HDE-сценарий.",
     "Аналогия с другой системой не доказывает полный сценарий в целевой системе.", 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-03"),
    ("U-10", [CONST], "наличие функции в продукте не доказывает её доступность в коннекторе или базовом тарифе.",
     "наличие функции в продукте не доказывает её доступность в конкретной интеграции, модуле или тарифе.", 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-11", [PIA], "передачу этих функций через коннектор.", "передачу этих функций через интеграцию.", 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-12", [CONST], "| `продукты` | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи |",
     "| `продукты` | профили продуктов из справочника профилей продуктов runtime (И-11) |", 1, "б",
     "перечень профилей → runtime taxonomy/product-profiles.yaml"),
    ("U-13", [PIA],
     "4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари\n"
     "   профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;\n"
     "   КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).",
     "4. **Набор словарей.** Возьми минимальный набор словарей раздела 1 и\n"
     "   словари профилей задействованных продуктов из справочника профилей\n"
     "   продуктов runtime (И-11). Справочника нет во входе — назови пробел\n"
     "   ACCESS_GAP, возьми минимальный набор и отметь `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`.", 1, "б",
     "соответствие профиль → словари → runtime taxonomy/product-profiles.yaml"),
    ("U-14", [ASR], '"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").',
     '"срмка" → "CRM", "апишка" → "API", "питон" → "Python"); продуктовые\n'
     'термины — по глоссарию продуктов, если он передан во входе.', 1, "б",
     "продуктовые синонимы → runtime taxonomy/domain-glossary*.yaml"),
    ("U-15", [ASR], '| 7 | "амо" | amoCRM | "интеграция с амо" |',
     '| 7 | "срмка" | CRM | "интеграция со срмкой" |', 1, "б", "пример формы — обезличен"),
    ("U-16", [ASR], '- "амо" → "amoCRM"\n- "вакс" → "ВАТС"\n',
     '- "срмка" → "CRM"\n- "апишка" → "API"\n', 1, "б", "пример формы — обезличен"),
    ("U-17", ["standards/bcreq-manual-classes/01-intake.md"], "операторы, номера ВАТС и сторонние номера",
     "операторы, номера телефонии продукта и сторонние номера", 1, "б", "обобщено"),
    # --- балласт (в): происхождение правил и история ---------------------------
    ("D-01", [CONST],
     "Защиты выведены из 168 инцидентов прогона\nRUN-0075\nи уточняют Р1–Р7. Критерии успеха БА —\n"
     "success-criteria,\nпредложенные формулировки —\nruntime-improvements.\n",
     "Защиты уточняют Р1–Р7.\n", 1, "в",
     "происхождение (RUN-0075, success-criteria, runtime-improvements) → репозиторий runs/2026/RUN-0075"),
    ("D-02", [CONST], "| ID | Защита | Правило | Категория RUN-0075 |\n| --- | --- | --- | --- |",
     "| ID | Защита | Правило |\n| --- | --- | --- |", 1, "в",
     "столбец категорий инцидентов RUN-0075 → репозиторий runs/2026/RUN-0075"),
    ("D-03", [CONST], "#### Дополнения по ревизии Golden Set (issue #391)\n\n"
     "Действуют во всех шагах и стадиях вместе с АД-1…АД-7. Это защиты от\n"
     "ошибок из кандидатов Golden Set, а не утверждение кандидатов эталонами.\n",
     "#### Дополнительные защиты (АД-8…АД-15)\n\n"
     "Действуют во всех шагах и стадиях вместе с АД-1…АД-7.\n", 1, "в",
     "происхождение (issue #391, кандидаты Golden Set) → карточка Ш-0 и issue #391"),
    ("D-04", [CONST], "об отсутствии ошибки, которой во входе не было (RUN-0076, SC-65).",
     "об отсутствии ошибки, которой во входе не было.", 1, "в", "происхождение → runs/2026/RUN-0076"),
    ("D-05", ENTRY_FILES, "Полные 24 draft контракта и инструкция БА.\n",
     "Полный промпт каждого AIN-ID БА передаёт отдельным вызовом.\n", 1, "в",
     "ссылка на инструкцию БА (приватный репозиторий) → сайт, раздел A-IN"),
    ("D-06", [SDB], "можно было вставить в Issue или скопировать как блок в\n   `pr-ops/session-digests.md` без ручной переработки.",
     "можно было вставить в задачу трекера или в журнал суммарий без ручной\n   переработки.", 1, "в",
     "имя файла репозитория → репозиторий pr-ops/session-digests.md"),
    ("D-07", [SDB], "совместима с шаблоном блока суммарии в\n(блоки",
     "совместима с шаблоном блока суммарии\n(блоки", 1, "в", "ссылка на шаблон → репозиторий pr-ops/session-digests.md"),
    ("D-08", [SDB],
     "\n# КОНТЕКСТ И СВЯЗАННЫЕ АРТЕФАКТЫ\n- Стандарт промптов (ADR-001):\n"
     "- Навигация по библиотеке промптов (сначала executable-слой):\n- Механизм суммаризации сессий:\n"
     "- Таксономия (когнитивные операции и процессы):\n- Экосистема БА:\n- Репозиторий:\n"
     "- Хаб (механизм-источник): <https://github.com/G-Ivan-A/hybrid-Intelligence-lab>\n", "", 1, "в",
     "раздел ссылок на артефакты репозитория → prompts/README.md и карточка промпта"),
    ("D-09", [COMMON],
     "Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):",
     "Решение БА по техническому шагу (блок «Итог шага»):", 1, "а",
     "ссылка на SSOT итога шага → блок «Итог шага» в самом промпте"),
    ("D-10", [COMMON],
     "Источники:\n"
     "- [Ш-0: полная конституция](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/prompts/bcreq-constitution-governance-oneshot.md).\n"
     "- [Мета-стандарты 1…8](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-sections/README.md).\n"
     "- [Маршрут и решения RFC-AIN-001](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md).\n"
     "- [Runtime: версии и источники](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/bcreq-runtime-references.md).\n",
     "Источники норм: полный текст Ш-0 (Промпт 0) и нормы, которые БА передал\n"
     "в этот чат; справочники runtime — только по закреплённому SHA. Ссылка на\n"
     "закрытый репозиторий источником не считается.\n", 1, "а",
     "4 приватные ссылки → Ш-0 во входе; контракты runtime — задачи BL-241, BL-242"),
]

ARCHIVE_BANNER = ("> **Архив (issue #388).** Промпт заменён", "> **Архив.** Промпт заменён")
FRONTMATTER_LINKS = [
    ("prompts/README.executable.md",
     'related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"', 'related_issue: "#125"'),
    ("prompts/AI_SESSION_HANDOVER_PROMPT.executable.md",
     'related_issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/125"', 'related_issue: "#125"'),
    (HANDOFF, "issue: https://github.com/G-Ivan-A/mango_ba_prompts/issues/490", 'issue: "#490"'),
]


#: Правки в исходниках сборщиков и в блоке-стражe Ш-А (experiments/issue_474/intake_guard.md):
#: внесены руками в тот же коммит, что и сборщики; в реестр замен попадают отсюда.
REGISTER_ONLY = [
    ("U-01b", ["experiments/issue_474/intake_guard.md"], AMO_OLD, AMO_NEW, 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-01; в промпте — принцип"),
    ("U-11b", ["scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный)"], "передачу этих функций через коннектор.",
     "передачу этих функций через интеграцию.", 1, "б", "кейс → runtime golden/prompt-regressions.yaml PR-02"),
    ("U-13b", ["scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный)"], "минимальный набор D1, D2, D11 … оператор связи — D9",
     "минимальный набор словарей раздела 1 … справочника профилей продуктов runtime (И-11)", 1, "б",
     "соответствие профиль → словари → runtime taxonomy/product-profiles.yaml"),
    ("U-18", ["scripts/build_bcreq_step_prompts.py (INTAKE_BODY)", "scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)"], "3. Сколько номеров Mango ВАТС?",
     "3. Сколько номеров телефонии продукта?", 1, "б", "имя продукта → runtime taxonomy/product-profiles.yaml"),
    ("U-19", ["scripts/build_bcreq_step_prompts.py (INTAKE_BODY)", "scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)"], "- номера ВАТС: <…|UNKNOWN>",
     "- номера телефонии продукта: <…|UNKNOWN>", 1, "б", "имя продукта → runtime taxonomy/product-profiles.yaml"),
    ("D-13", ["scripts/build_bcreq_step_prompts.py"],
     "> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.",
     "— (баннер удалён; режим — поле `mode: by-test` frontmatter)", 1, "в", "frontmatter карточки, манифест сборки"),
    ("D-14", ["scripts/build_bcreq_step_prompts.py"],
     "<!-- bl-156: by-test --> ## Дополнение «по тесту» (BL-156): стандарты шага … Блок собран сборщиком … из [базового стандарта](…) … [реестра справочников runtime](…)",
     "## Стандарты шага / Правила базового стандарта, профилей шага и контракты операций — с номером правила.", 1, "в",
     "версии стандартов — prompts/drafts/manifest.json"),
    ("D-15", ["scripts/build_bcreq_step_prompts.py"],
     "**Приоритет.** Где правило ниже расходится с текстом шага выше (v0.1), действует текст v0.1; расхождение запиши в receipt.",
     "**Приоритет.** Где правило ниже расходится с текстом шага выше, действует текст шага выше; расхождение запиши в receipt.", 1, "в",
     "правило приоритета сохранено явно (комментарий 2 владельца)"),
    ("D-16", ["scripts/build_bcreq_step_prompts.py"],
     "Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.",
     "— (строка удалена)", 1, "в", "prompts/drafts/manifest.json → excluded_base_rules"),
    ("D-17", ["scripts/build_bcreq_step_prompts.py"],
     "**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3: [`docs/contracts/bcreq-stage-gates.md`](…).",
     "**Запись решения гейта (К-34).** … неполна (стандарт гейтов, правило Г3).", 1, "а, в",
     "контракт гейтов → runtime (BL-241)"),
    ("D-19", ["standards/bcreq-prompt-base-standard.md"], "БС-21: … блок заглушки раздела 4 реестра (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка …",
     "БС-21: … блок заглушки раздела 4 реестра; заглушка … (история заглушек — колонка «Источник»)", 1, "в",
     "колонка «Источник» стандарта, реестр справочников раздел 4"),
    ("D-20", ["standards/bcreq-runtime-references.md"], "[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]",
     "[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>]", 1, "в", "RFC #427, раздел 8.4; pr-ops/BACKLOG.md BL-155"),
    ("D-21", ["scripts/build_bcreq_a_in.py (PROVENANCE)"], "LE-19: … модель выбирает сама (обратная связь RUN-0090) → …",
     "LE-19: … модель выбирает сама → …", 1, "в", "RFC A-IN, таблица LE (источник урока остаётся там)"),
    ("D-22", ["scripts/build_bcreq_system_track.py"], "> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архивный блок «Дополнение «по тесту» (BL-156)»",
     "— (баннер удалён; архивный блок заменён текущим блоком «Стандарты шага»)", 1, "в",
     "архив prompts/archive/a-in-v2.7.0 (историческая сущность)"),
    ("U-20", ["standards/bcreq-manual-classes/catalog.json (К-01 behavior)", "docs/ba-processes/bcreq-run-kit.md (шаг 2, «Что подготовить»)"],
     "номера ВАТС и сторонние номера", "номера телефонии продукта и сторонние номера", 1, "б",
     "имя продукта → runtime taxonomy/product-profiles.yaml; поля попадают в site/data (каталог, тестовый набор)"),
    ("A-01", ["scripts/generate-pages-data.mjs (repoUrl)", "site/app.js (repoHref)"],
     "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/<путь> в полях url/promptPath/sourceUrl site/data/*.json",
     "<путь от корня репо>; ссылку сопровождающего строит интерфейс (REPO_BLOB + repoHref)", 1, "а",
     "СУПЕР-ПРАВИЛО: данные сайта без приватных URL"),
    ("D-18", ["scripts/build_bcreq_step_prompts.py", "scripts/build_bcreq_a_in.py", "scripts/build_bcreq_system_track.py"],
     "<!-- Experimental: for … issues/438|474|490, no formal research yet -->",
     "— (строка удалена)", 1, "а, в", "статус draft — поле frontmatter `status`"),
]


def plan():
    """Список (путь, было, стало, id) после проверки числа вхождений."""
    out, errors = [], []
    for eid, files, old, new, count, *_ in EDITS:
        for rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            n = text.count(old)
            if n != count:
                errors.append(f"{eid} {rel}: ожидалось {count}, найдено {n}")
            out.append((rel, old, new, eid))
    for rel in sorted(glob.glob(str(ROOT / "prompts/archive/*.md"))):
        rel = Path(rel).relative_to(ROOT).as_posix()
        if ARCHIVE_BANNER[0] in (ROOT / rel).read_text(encoding="utf-8"):
            out.append((rel, *ARCHIVE_BANNER, "D-11"))
    for rel, old, new in FRONTMATTER_LINKS:
        if (ROOT / rel).read_text(encoding="utf-8").count(old) != 1:
            errors.append(f"D-12 {rel}: нет строки frontmatter")
        out.append((rel, old, new, "D-12"))
    return out, errors


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--register", action="store_true", help="напечатать реестр замен (Markdown)")
    args = parser.parse_args(argv)
    if args.register:
        print("| ID | Класс | Файлы | Было | Стало | Куда перенесено |\n| --- | --- | --- | --- | --- | --- |")
        for eid, files, old, new, _, cls, where in EDITS + REGISTER_ONLY:
            cell = lambda s: (s.replace("\n", " ").replace("|", "\\|")[:160] or "—")
            print(f"| {eid} | {cls} | {', '.join(f'`{f}`' for f in files)} | {cell(old)} | {cell(new)} | {where} |")
        return 0
    edits, errors = plan()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    changed = set()
    for rel, old, new, _ in edits:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if not args.dry_run:
            path.write_text(text.replace(old, new), encoding="utf-8")
        changed.add(rel)
    print(f"{'проверено' if args.dry_run else 'изменено'} файлов: {len(changed)}; замен: {len(edits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
