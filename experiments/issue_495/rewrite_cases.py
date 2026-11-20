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
     "кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)"),
    ("U-11", [PIA], "передачу этих функций через коннектор.", "передачу этих функций через интеграцию.", 1, "б",
     "кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)"),
    ("U-12", [CONST], "| `продукты` | профили: ЛК, ВАТС, КЦ, РА, API, оператор связи |",
     "| `продукты` | профили продуктов из справочника профилей продуктов runtime (И-11) |", 1, "б",
     "перечень профилей → runtime taxonomy/product-profiles.yaml"),
    ("U-13", [PIA],
     "4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари\n"
     "   профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;\n"
     "   КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).",
     "4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари\n"
     "   профилей задействованных продуктов из справочника профилей продуктов\n"
     "   runtime (И-11). Справочника нет во входе — назови пробел ACCESS_GAP,\n"
     "   возьми минимальный набор D1, D2, D11 и отметь `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`.", 1, "б",
     "соответствие профиль → словари → runtime taxonomy/product-profiles.yaml (profiles[].dictionaries); "
     "минимальный набор D1, D2, D11 остаётся в промпте и дублируется в runtime minimal_set"),
    ("U-14", [ASR], '"амо" → "amoCRM", "вакс" → "ВАТС", "питон" → "Python").',
     '"срмка" → "CRM", "апишка" → "API", "питон" → "Python"); разговорные\n'
     'формы продуктов и внешних систем — по справочнику профилей продуктов\n'
     'runtime (И-11, раздел spoken_aliases), если он передан во входе.', 1, "б",
     "пары «амо» → amoCRM, «вакс» → ВАТС → runtime taxonomy/product-profiles.yaml spoken_aliases "
     "(И-11; тест test_spoken_aliases_resolve); неоднозначная форма — «Требует проверки» по правилу промпта"),
    ("U-15", [ASR], '| 7 | "амо" | amoCRM | "интеграция с амо" |',
     '| 7 | "срмка" | CRM | "интеграция со срмкой" |', 1, "б", "пример формы — обезличен; значения пар → runtime taxonomy/product-profiles.yaml spoken_aliases (И-11)"),
    ("U-16", [ASR], '- "амо" → "amoCRM"\n- "вакс" → "ВАТС"\n',
     '- "срмка" → "CRM"\n- "апишка" → "API"\n', 1, "б", "пример формы — обезличен; значения пар → runtime taxonomy/product-profiles.yaml spoken_aliases (И-11)"),
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
     "столбец категорий инцидентов RUN-0075 → реестр уроков standards/bcreq-lessons (run_taxonomies RUN-0075: "
     "категория → урок → якорь АД; 10 из 11 пар базы совпадают; пара АД-7 ↔ C10 в реестре — L-30 с якорем АД-8, "
     "расхождение Р-28 вынесено владельцу) и источник runs/2026/RUN-0075"),
    ("D-03", [CONST], "#### Дополнения по ревизии Golden Set (issue #391)\n\n"
     "Действуют во всех шагах и стадиях вместе с АД-1…АД-7. Это защиты от\n"
     "ошибок из кандидатов Golden Set, а не утверждение кандидатов эталонами.\n",
     "#### Дополнительные защиты (АД-8…АД-15)\n\n"
     "Действуют во всех шагах и стадиях вместе с АД-1…АД-7.\n", 1, "в",
     "происхождение (issue #391, кандидаты Golden Set) и снятая оговорка «Это защиты от ошибок из кандидатов "
     "Golden Set, а не утверждение кандидатов эталонами» → CHANGELOG.md, раздел «Changed — Issue #391: BCREQ-каталог, ревизия Golden Set» "
     "(абзац «кандидаты не повышены в статусе») и docs/reviews/issue-391-bcreq-review.md (строки 44, 70, 98: источники "
     "АД-8…АД-11, кандидаты — не эталоны); статус golden set задаёт runtime, а не промпт"),
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
     "передачу этих функций через интеграцию.", 1, "б", "кейс → runtime golden/prompt-regressions.yaml PR-04 (CR-04)"),
    ("U-13b", ["scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-2 системный)"], "минимальный набор D1, D2, D11 … оператор связи — D9",
     "минимальный набор D1, D2, D11 … справочника профилей продуктов\n   runtime (И-11)", 1, "б",
     "соответствие профиль → словари → runtime taxonomy/product-profiles.yaml (profiles[].dictionaries); минимальный набор D1, D2, D11 сохранён"),
    ("U-18", ["scripts/build_bcreq_step_prompts.py (INTAKE_BODY)", "scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)"], "3. Сколько номеров Mango ВАТС?",
     "3. Сколько номеров телефонии продукта?", 1, "б", "имя продукта → runtime taxonomy/product-profiles.yaml"),
    ("U-19", ["scripts/build_bcreq_step_prompts.py (INTAKE_BODY)", "scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)"], "- номера ВАТС: <…|UNKNOWN>",
     "- номера телефонии продукта: <…|UNKNOWN>", 1, "б", "имя продукта → runtime taxonomy/product-profiles.yaml"),
    ("D-02b", [CONST + " (таблица АД-1…АД-7, ручная правка вместе с D-02)"],
     "АД-1: | Р1, Р2 | C01, C11 |\nАД-2: | Р3 | C09 |\nАД-3: | Р7 | C13, C05 |\nАД-4: | Р3 | C04 |\nАД-5: | Р4 | C02 |\nАД-6: | Р2 | C06 |\nАД-7: | Р6 | C07, C08, C10 |",
     "АД-1…АД-7: | <правило> | (ячейка категории удалена вместе со столбцом D-02)", 1, "в",
     "пары АД → категория RUN-0075 → реестр уроков standards/bcreq-lessons (run_taxonomies RUN-0075); "
     "10 из 11 пар совпадают, пара АД-7 ↔ C10 — расхождение Р-28 (вопрос владельцу); источник runs/2026/RUN-0075"),
    # Раунд 3 роли Б: сборщик базы писал четыре варианта верхнего баннера; все
    # они здесь. Носитель записи — черновики шагов (map_baseline.CARRIERS): тот
    # же хвост баннера в системном формате — запись D-22.
    ("D-13", ["scripts/build_bcreq_step_prompts.py (черновики шагов)"],
     "> **Редакция по тесту (#427): действует до ADR обратного согласования.** Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.\n"
     "> **Редакция по тесту (#427): действует до ADR обратного согласования.**\n"
     "Черновик BL-156 (issue #438): текст шага v0.1 ниже не изменён, кроме формата шагов … ; блок «по тесту» — в конце файла.\n"
     "Черновик BL-156 (issue #438): шаг без промпта v0.1 (issue #464); блок «по тесту» — в конце файла.\n"
     "Черновик BL-156 (issue #438): шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «по тесту» — в конце файла.\n"
     "Черновик BL-156 (issue #438):",
     "— (верхний баннер удалён во всех четырёх вариантах; баннер внутри блока удалён вместе с заголовком «по тесту», D-14)", 1, "в",
     "режим — поле `mode: by-test` frontmatter черновика шага; задача BL-156 и issue #438 — prompts/drafts/manifest.json; "
     "«шаг без промпта v0.1 (issue #464)» — комментарий INTAKE_FILE в scripts/build_bcreq_step_prompts.py; "
     "«заглушка выпуска (пилот)» — заголовок и первая строка черновика Ш-Р; «(#490)» — запись D-25"),
    ("D-14", ["scripts/build_bcreq_step_prompts.py"],
     # Строки блока в выводе сборщика базы; ссылки записаны после проекции (подпись).
     "<!-- bl-156: by-test -->\n"
     "## Дополнение «по тесту» (BL-156): стандарты шага\n"
     "Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по\n"
     "RFC #427, раздел 9.3\n"
     "из базового стандарта 0.1.3,\n"
     "профилей 0.1.2,\n"
     "каталога операций и\n"
     "реестра справочников runtime 0.5.\n"
     "Правила перенесены дословно с номером; источник правила — в стандарте.\n"
     "<!-- /bl-156: by-test -->",
     "## Стандарты шага / Правила базового стандарта, профилей шага и контракты операций — с номером правила.", 1, "в",
     "версии стандартов — prompts/drafts/manifest.json"),
    ("D-15", ["scripts/build_bcreq_step_prompts.py"],
     "**Приоритет.** Где правило ниже расходится с текстом шага выше (v0.1), действует текст v0.1; расхождение запиши в receipt.",
     "**Приоритет.** Где правило ниже расходится с текстом шага выше, действует текст шага выше; расхождение запиши в receipt.", 1, "в",
     "правило приоритета сохранено явно (комментарий 2 владельца)"),
    ("D-16", ["scripts/build_bcreq_step_prompts.py"],
     "Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): БС-01, БС-04, БС-07, БС-09, БС-11, БС-13. Для них действует текст v0.1.",
     "— (строка удалена)", 1, "в", "prompts/drafts/manifest.json → excluded_base_rules (ID и причины); тексты этих "
     "правил модель не видит ни в одном промпте, поэтому перечень неисполним; сторож сверхчистки зачитывает "
     "их ID только при наличии в манифесте"),
    ("D-17", ["scripts/build_bcreq_step_prompts.py"],
     "**Запись решения гейта (К-34, RUN-0089, P05).** … Источник — стандарт гейтов, правило Г3:\n"
     "[`docs/contracts/bcreq-stage-gates.md`](…).",
     "**Запись решения гейта (К-34).** … гейта, а у гибрида без расхождения, неполна.", 1, "а, в",
     "правило изложено в шаге целиком (поля записи, условие неполноты), отсылка к стандарту гейтов снята; "
     "происхождение К-34 — runs/2026/RUN-0089/outputs/report.md (P05), правило Г3 — docs/contracts/bcreq-stage-gates.md; "
     "в runtime выносить нечего"),
    ("D-19", ["standards/bcreq-prompt-base-standard.md"], "БС-21: … блок заглушки раздела 4 реестра … (сейчас только З-2; З-1 снята BL-163, З-3 и З-4 — BL-156а); заглушка …",
     "БС-21: … блок заглушки раздела 4 реестра; заглушка … (история заглушек — колонка «Источник»)", 1, "в",
     "колонка «Источник» стандарта, реестр справочников раздел 4"),
    ("D-20", ["standards/bcreq-runtime-references.md", "scripts/build_bcreq_step_prompts.py (заглушки З-n из реестра)"],
     "[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>; задача BL-155]\n"
     "[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов … ОРР; задача BL-155]",
     "[СПРАВОЧНИК ОТСУТСТВУЕТ: <имя>]\n[СПРАВОЧНИК ОТСУТСТВУЕТ: И-4 примеры разделов ФТ, НФТ, UC, US, ОРР]",
     1, "в", "RFC #427, раздел 8.4; pr-ops/BACKLOG.md BL-155"),
    ("D-21", ["scripts/build_bcreq_a_in.py (PROVENANCE)"], "LE-19: … модель выбирает сама (обратная связь RUN-0090) → …",
     "LE-19: … модель выбирает сама → …", 1, "в", "RFC A-IN, таблица LE (источник урока остаётся там)"),
    ("D-22", ["scripts/build_bcreq_system_track.py"], "> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** История баннера: …; архивный блок «Дополнение «по тесту» (BL-156)»\n"
     "История баннера: «Редакция … «Редакция по тесту (#427): действует до ADR … Черновик BL-156 (issue #438)\n"
     "> **Редакция по тесту (#427): действует до ADR обратного согласования.**",
     "— (баннер удалён; архивный блок вместе с его баннером заменён текущим блоком «Стандарты шага»)", 1, "в",
     "архив prompts/archive/a-in-v2.7.0 (историческая сущность); носитель записи — системный формат "
     "(prompts/drafts/system/, steps[].system в site/data/test-kit.json), поле `track: system` frontmatter"),
    ("D-23", ["scripts/build_bcreq_a_in.py"], "Draft для ручной проверки БА; эффективность модели не измерена.",
     "— (строка удалена)", 1, "в",
     "статус — поле frontmatter `status: draft` каждого AIN-промпта и `status: draft`, `measured: false` "
     "в site/data/a-in-kit.json (собирает тот же build_bcreq_a_in.py)"),
    ("D-24", ["scripts/build_bcreq_system_track.py"],
     "<!-- issue-490:system -->\n<!-- /issue-490:system -->\n## Системный формат шагов (#490)\n"
     "([issue #490](https://github.com/G-Ivan-A/mango_ba_prompts/issues/490)). БА выбрал системный формат",
     "## Системный формат шагов\n(граница раздела — сам заголовок; ссылка на issue снята)\nБА выбрал системный формат", 1, "а, в",
     "граница раздела — заголовок `## Системный формат шагов` (константа BEGIN сборщика); происхождение формата — "
     "docs/rfc/2026-11-bcreq-step-format.md и issue #490 в CHANGELOG.md"),
    ("D-25", ["scripts/build_bcreq_step_prompts.py (CASE_EDITS, Ш-0 и Ш-3; заголовок по тесту)"],
     "Формат шагов (#490) задаёт сайт строкой\n**Формат шагов (#490).** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из\n"
     "проверь вход по формату шагов из «Состояния BCREQ» (#490).\n"
     "ниже не изменён, кроме формата шагов (#490); блок «по тесту» — в конце файла.",
     "Формат шагов задаёт сайт строкой\n**Формат шагов.** Системный — комплексные шаги Ш-А, Ш-1, Ш-2 из\n"
     "проверь вход по формату шагов из «Состояния BCREQ».\n— (заголовок «по тесту» удалён вместе с баннером D-13)", 1, "в",
     "номер решения (#490) → docs/rfc/2026-11-bcreq-step-format.md и CHANGELOG.md; правило формата шагов в промпте сохранено"),
    ("D-26", ["scripts/build_bcreq_step_prompts.py (RELEASE_BODY, Ш-Р)"],
     "Шаг Ш-Р — заглушка выпуска (пилот): у него нет промпта v0.1\n"
     "([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).\n"
     "гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).",
     "Шаг Ш-Р — заглушка выпуска (пилот). Текст шага ниже — контракты операций\n"
     "пакетов раздела 4. Отдельный вызов, новая сессия.", 1, "а, в",
     "состав шагов → docs/rfc/2026-11-bcreq-flow-processes-prompts.md, раздел 9.2; происхождение правил пакетов → "
     "pr-ops/BACKLOG.md BL-123 и runs/2026/RUN-0089/outputs/report.md (P16)"),
    ("D-27", [HANDOFF + " (раздел 2, шаблон блока)", "scripts/bcreq_handoff.py (BEGIN, END)"],
     "<!-- issue-490:handoff -->\n## Итог шага для БА (#490)\n<!-- /issue-490:handoff -->",
     "## Итог шага для БА\n(границы блока — заголовок и последняя строка «без записи — декомпозированный.»; "
     "константы BEGIN, END сборщика)", 1, "в",
     "номер решения (#490) → frontmatter SSOT `issue: \"#490\"` (D-12) и CHANGELOG.md; границы блока проверяет "
     "bcreq_handoff.py (assert без «<!--»)"),
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
    # Раунд 2 (замечания роли Б к M-01 и U-12): снятая ссылка оставила голый путь или
    # название файла спицы. Правки ручные; сторож — правило A-SPOKE-PATH аудитора.
    ("A-02", ["standards/bcreq-prompt-profiles.md (GE-01; сборщик копирует правило в 9 черновиков)"],
     "Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела (`standards/bcreq-sections/NN-*.md`); стиль",
     "Раздел **ДОЛЖЕН** следовать мета-стандарту своего раздела (раздел «Правила раздела» промпта шага); стиль",
     1, "а", "указатель на файл спицы → раздел «4. Правила раздела» того же промпта; профиль 0.1.3"),
    ("U-12b", [CONST + " (раздел 4.1)"],
     "Профили продуктов и их словари — в\nстандарте композиции §4.",
     "Профили продуктов и их словари — в справочнике профилей продуктов\nruntime (И-11).", 1, "а",
     "указатель на стандарт композиции спицы → runtime taxonomy/product-profiles.yaml (И-11, по SHA реестра справочников)"),
    ("A-03", [CONST + " (раздел 4.1)"],
     "Стандарт каждого раздела — файл `NN-*.md` в\nstandards/bcreq-sections.",
     "Правила каждого раздела — в разделе «Правила раздела» промпта его шага.", 1, "а",
     "указатель на каталог спицы → раздел «Правила раздела» промпта шага (Ш-0 передаётся в каждый шаг)"),
    ("A-04", [CONST + " (раздел 4.2)"], "Полный текст —\nREADME §2.", "— (строка удалена)", 1, "а",
     "стили изложены в разделе 4.2 Ш-0 целиком; полный текст README §2 — в спице standards/bcreq-sections/README.md"),
    ("A-05", ["standards/bcreq-manual-classes/05-taxonomy.md (шаг 2)", "standards/bcreq-manual-classes/catalog.json (К-05 behavior)"],
     "Локальный каталог docs/taxonomy и runtime taxonomy/products.yaml — разные носители",
     "Каталог продуктов репозитория и runtime-каталог taxonomy/products.yaml — разные носители", 1, "а",
     "путь спицы → роль носителя; поле попадает в site/data (каталог классов)"),
    ("D-06b", [SDB + " (вступление)"],
     "структурированное резюме, пригодное для человеческого анализа и для сохранения\nв `pr-ops/session-digests.md`.",
     "структурированное резюме, пригодное для человеческого анализа и для сохранения\nв журнал суммарий.", 1, "а",
     "имя файла репозитория → роль («журнал суммарий»), как в D-06; файл — pr-ops/session-digests.md"),
    # Раунд 3 (разночтение Р-26): ID внутреннего RFC в исполнимом тексте — справочное,
    # исполнителю недоступно (ЧП-1, ЧП-3). Сторож — шаблон BP-13 аудитора.
    ("D-28", [COMMON + " (приоритет норм; сборщик копирует в 24 черновика AIN)"],
     "у принятого RFC-AIN-001 и этого контракта: раздел 2 только после AIN-21;",
     "у маршрута A-IN из 24 шагов и этого контракта: раздел 2 только после AIN-21;", 1, "в",
     "ID RFC → правило изложено в контракте (маршрут из 24 шагов, раздел 2 после AIN-21, вопросы только Заказчику); "
     "RFC-AIN-001 — docs/rfc/2026-11-a-in-decomposition.md в спице"),
    ("D-29", ["scripts/build_bcreq_step_prompts.py (заголовок блока М-4, Ш-2 и системный Ш-2)"],
     "Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):", "Как читать каталог:", 1, "а, в",
     "указатель на реестр и ID RFC → правило чтения каталога изложено блоком ниже заголовка; "
     "источник — standards/bcreq-runtime-references.md, раздел 2.2, и RFC-RT-001 в спице"),
    # Раунд 2 роли Б: переименование блока в словаре терминов сборщика (TERMS, receipt)
    # шло без записи «что → куда» и пряталось в группах G.
    ("D-30", ["scripts/build_bcreq_step_prompts.py (TERMS, строка receipt)"],
     "расхождения с блоком «по тесту»", "расхождения с блоком «Стандарты шага»", 1, "в",
     "название блока — BLOCK_HEADING сборщика (блок переименован записью D-14); смысл строки receipt не изменён"),
    # Раунд 3 (замечание роли А): после снятия ссылки осталась отсылка к справочнику
    # спицы, недоступному исполнителю; правило уже изложено в промпте — строка его называет.
    # Роль А, раунд 4, замечание 2: BABOK задаёт категории, а не порядок
    # (standards/bcreq-industry-practice.md, раздел 2, «Группировка ФТ»); порядок — из шага группировки.
    ("A-06", ["prompts/bcreq-orr-solution-design-stepwise.md (раздел 4)", "prompts/bcreq-fr-documentation-stepwise.md (раздел 4)"],
     "- Правила вывода структуры — справочник стандартов.\n- Группировка и пункты BABOK — справочник стандартов.",
     "- Структура раздела выводится из метамодели выбранного стандарта (C4 или TM Forum ODA), а не из номеров ФТ.\n"
     "- Группировка — по BABOK Guide v3: блок — одна бизнес-возможность (10.6), категории — по 7.1; "
     "порядок категорий — как в шаге группировки выше.", 1, "а",
     "отсылка к справочнику спицы → правило в самом промпте (метамодель C4/ODA; группировка BABOK); источник — "
     "standards/bcreq-industry-practice.md, разделы 2 и 3, в спице"),
    # Раунд 3 роли Б (замечания 1 и 3): три фразы Ш-А переписаны в сборщике без
    # записи «что → куда», а в системном формате Ш-А та же отсылка осталась.
    # Носитель — только Ш-А (map_baseline.CARRIERS): «Промпт 0;» в других шагах —
    # копия ручных промптов.
    ("A-07", ["scripts/build_bcreq_step_prompts.py (INTAKE_BODY)",
              "scripts/build_bcreq_system_track.py (CASE_EDITS, Ш-А системный)"],
     "Шаг Ш-А собирает данные о Заказчике и выбор стандартов до разбора запроса. У него нет\n"
     "промпта v0.1: текст шага собран из контракта операции К-01 и правил\nсправочника стандартов.\n…\n"
     "Конституция —\nПромпт 0;\nв чат её не выводи.\n…\n"
     "**В. Согласие со стандартами** (подробно — в\nсправочнике стандартов):",
     "Шаг Ш-А собирает данные о Заказчике и выбор стандартов до разбора запроса:\n"
     "контракт операции К-01 и правила выбора стандартов (раздел 4В ниже).\n…\n"
     "Конституция — Промпт 0 (Ш-0), принятый в этом чате; в чат её не выводи.\n…\n"
     "**В. Согласие со стандартами** (варианты по умолчанию):", 1, "а, в",
     "отсылка к справочнику спицы, недоступному исполнителю → правила выбора стандартов изложены в самом шаге "
     "(раздел 4В: таблица «Что | По умолчанию | Другие варианты»); источник — standards/bcreq-industry-practice.md, "
     "раздел 1, в спице; ссылка на Промпт 0 → Ш-0, принятый в том же чате (порядок маршрута A-IN); "
     "«нет промпта v0.1» — комментарий INTAKE_FILE сборщика"),
    # Раунд 3 роли Б (замечание 3): вход Ш-А пишет не ручной промпт, а вставка
    # experiments/issue_474/intake_guard.md; её маркеры и ссылку правили без записи.
    ("A-08", ["experiments/issue_474/intake_guard.md (вход Ш-А; сборщик build_bcreq_step_prompts вставляет его в черновик)"],
     "<!-- issue-474:entry -->\n…\nAIN-02.\n…\n<!-- /issue-474:entry -->",
     "— (маркеры удалены)\n…\nAIN-02.\n…\n— (маркер удалён)", 1, "а, в",
     "служебные маркеры сборки → граница входа — заголовок «## Действующий Ш-А» (scripts/validate_issue_474_execution.py, "
     "test_all_legacy_entries_are_guarded); ссылка на черновик AIN-02 → ID шага маршрута A-IN, подпись сохранена"),
    # Раунд 3 роли Б (замечание 7, вслед за ролью А): после снятия ссылок в разделе 4
    # семи промптов осталась подпись «Мета-стандарт раздела N» — отсылка к документу
    # спицы без адресата. Правила раздела уже идут списком ниже.
    ("A-09", ["prompts/bcreq-constraints-documentation-stepwise.md (раздел 4)",
              "prompts/bcreq-fr-documentation-stepwise.md (раздел 4)",
              "prompts/bcreq-nfr-documentation-stepwise.md (раздел 4)",
              "prompts/bcreq-extra-risk-analysis-stepwise.md (раздел 4)",
              "prompts/bcreq-uc-modeling-stepwise.md (раздел 4)",
              "prompts/bcreq-orr-solution-design-stepwise.md (раздел 4)",
              "prompts/bcreq-scenarios-modeling-oneshot.md (раздел 4)"],
     "Мета-стандарт раздела 6.\n…\nМета-стандарт раздела 3.\n…\nМета-стандарт раздела 4.\n…\n"
     "Мета-стандарт раздела 8.\n…\nМета-стандарт раздела 7.\n…\nМета-стандарт раздела 5;\nправила композиции.\n…\n"
     "Мета-стандарт раздела 7\n(шаблон UC общий для Ш-С и Ш-5/Ш-8, правило М4\nархитектуры промптов).",
     "— (подпись удалена в шести промптах)\n…\nШаблон UC — общий для Ш-С и Ш-5/Ш-8 (правило М4).", 1, "а",
     "подпись снятой ссылки на мета-стандарт раздела (standards/bcreq-sections/*.md, в спице; исполнителю недоступен) "
     "удалена: правила раздела изложены списком ниже в том же разделе 4 промпта; в Ш-С сохранены общий шаблон UC и ID правила М4"),
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
