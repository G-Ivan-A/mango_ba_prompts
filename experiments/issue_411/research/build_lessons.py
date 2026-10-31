#!/usr/bin/env python3
"""Build lessons_inventory.json and lessons_coverage.md for issue #411.

Data below is hand-curated from runs/2026/RUN-00xx feedback and outputs,
docs/analysis, docs/rfc and the four artifact groups. Every evidence string
is "path:line «quote»". Run: python3 -I build_lessons.py
"""
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent

MC = "standards/bcreq-manual-classes/"
ST = "docs/contracts/bcreq-manual-state.md"
SG = "docs/contracts/bcreq-stage-gates.md"
CP = "prompts/bcreq-constitution-governance-oneshot.md"
FRP = "prompts/bcreq-fr-documentation-stepwise.md"
SEC = "standards/bcreq-sections/"
E73 = "runs/2026/RUN-0073/outputs/error-statistics.md"
E74 = "runs/2026/RUN-0074/outputs/error-statistics.md"
E75 = "runs/2026/RUN-0075/outputs/error-statistics.md"
E76 = "runs/2026/RUN-0076/outputs/error-statistics.md"
PI76 = "runs/2026/RUN-0076/outputs/prompt-improvements.md"
SP74 = "runs/2026/RUN-0074/outputs/section-prompts.md"
GS = "runs/2026/RUN-0074/outputs/golden-set-candidates.json"
V403 = "scripts/validate_issue_403_manual_pipeline.py"
COMMON = "(общий шаблон всех 39 классов; номер строки дан для 16-fr-delta.md)"

RUN74_COUNTS = {"C01": 18, "C02": 7, "C03": 5, "C04": 3, "C05": 1, "C06": 11, "C07": 8,
                "C08": 1, "C09": 32, "C10": 42, "C11": 3, "C12": 8, "C13": 1, "C14": 1,
                "C15": 4, "C16": 1, "C17": 0, "C18": 0, "C19": 5, "C20": 8, "C21": 5,
                "C22": 2, "C23": 10, "C24": 11, "C25": 6}


def e74(cid):
    return f"{E74}:{47 + int(cid[1:])} ({cid}={RUN74_COUNTS[cid]})"


# Each lesson: id, title, failure, rule, phase, section, severity, freq, sources,
# cids, cov{a,b,c,d: [level, evidence]}, examples, guard, old (older explicit
# rule outside the 39 classes or None), notes (uncertainty).
L = []


def lesson(**kw):
    kw.setdefault("notes", "")
    kw.setdefault("old", None)
    L.append(kw)


lesson(id="I-01", title="Угодничество: согласие с замечанием без проверки",
       failure="Модель отвечает «Вы абсолютно правы», хвалит, переписывает текст под замечание БА, не проверив его по источнику.",
       rule="На замечание — проверка и ответ «проверено: <локатор>» либо контраргумент с цитатой; формулы согласия запрещены.",
       phase="все (диалог)", section="— (диалог)", severity="critical",
       freq="RUN-0074 C10=42 (вместе с самосертификацией); RUN-0076 C10=57, из них 55 повторов после замечания БА; RUN-0075 C04=11; RUN-0073 C10=15; RUN-0018, RUN-0020 [34].",
       sources=[e74("C10"), f"{PI76}:33", f"{E75}:51", f"{E73}:57", "runs/2026/RUN-0020/feedback/ba-review-notes.md:22"],
       cids=["C10"],
       cov={"a": ["generic", f"{MC}30-targeted-edit.md:103 «При возражении эксперта дать доводы и варианты, а не автоматически соглашаться» — единственная строка в 39 классах, и только в классе правки C30; в остальных 38 классах запрета формул согласия нет"],
            "b": ["generic", f"{ST}:128-141 двухфакторная апелляция спорной команды; {ST}:113 «молчание не согласие» — про процесс, не про формулы ответа"],
            "c": ["explicit", f"{CP}:143 АД-4 «На замечание БА — проверка и ответ «проверено: <локатор>» или контраргумент»"],
            "d": ["generic", f"{SEC}README.md:130 Р3 «не оспариваются молча» — обратное направление, запрета согласия нет"]},
       examples="Класс: нет. Golden: GS-375-DLG-01 «Подтверждение: Да, абсолютно верно.» (negative, C10) в RUN-0074, к классам не подключён.",
       guard="нет; test_issue_395_bcreq.py:37 проверяет только наличие строки «АД-1…АД-11» в промптах (c)",
       old=f"{CP}:143 АД-4 (14 промптов bcreq-*)")

lesson(id="I-02", title="Самосертификация: «готово», «согласовано», прохождение гейта моделью",
       failure="Модель объявляет раздел готовым или согласованным, ставит ✅, «проходит» Г-С1 за заказчика.",
       rule="Статус и прохождение гейта ставит человек; модель перечисляет, что и чем проверено.",
       phase="a-core / a-work / a-release", section="все; гейты Г-IN, Г-С1, Г-W", severity="critical",
       freq="RUN-0074 C10=42 (общая категория); RUN-0075 C05=6; RUN-0018 Г7 «готова к передаче в разработку»; RUN-0076 I-007 (шаблон предписывал «Контекст валиден и готов»).",
       sources=[e74("C10"), f"{E75}:52", "runs/2026/RUN-0018/feedback/review-notes.md:46", f"{PI76}:67"],
       cids=["C10"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:138 «Рекомендация не названа одобрением, отправкой или выпуском» {COMMON}; {MC}20-gate-evidence.md:101 «eligible_for_review не означает approved», :143; {MC}34-human-record.md:113,147"],
            "b": ["explicit", f"{ST}:109-113 (только человек утверждает); {SG}:59-63 (LLM не проходит гейт)"],
            "c": ["explicit", f"{CP}:126 Р7; {CP}:173 АП2 «Нет ✅, «валидно», «готово»»; {CP}:142 АД-3"],
            "d": ["explicit", f"{SEC}README.md:144 Р7 «Модель не пишет «согласовано», «готово», «выполнено»»"]},
       examples="Класс: 20-gate-evidence.md:143 «Ошибка: Модель прошла Г-С1 за заказчика.»; 34-human-record.md:147. Golden: нет отдельного кейса.",
       guard=f"{V403}:162-173 (check_replay: только человеческое approval разрешает release) — проверяет состояние, а не текст ответа модели")

lesson(id="I-03", title="Ложные утверждения о диалоге, правках, памяти и прочитанном",
       failure="«Исправлено», «перечитал руководство», «в памяти зафиксировано» — без фактического действия.",
       rule="«Исправлено» только с локатором правки; не имитировать чтение и вызовы инструментов; память модели не источник.",
       phase="все", section="— (диалог)", severity="critical",
       freq="RUN-0075 C13=11; RUN-0021 Г2 (ссылка на «персональную память»); RUN-0020 [68].",
       sources=[f"{E75}:60", "runs/2026/RUN-0021/feedback/review-notes.md:25", "runs/2026/RUN-0020/feedback/ba-review-notes.md:25"],
       cids=["C10", "C09"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:128 «не имитировать вызовы web/инструментов» {COMMON}; {MC}11-dependency-check.md:104,146 «Критик сообщил, что повторно изучил недоступное руководство»; {MC}07-web-evidence.md:113"],
            "b": ["explicit", f"{ST}:21-23 «Не восстанавливать по памяти»"],
            "c": ["explicit", f"{CP}:142 АД-3 «исправлено» только со ссылкой"],
            "d": ["generic", f"{SEC}README.md:128-129 Р2 «а не заполняется по памяти модели»"]},
       examples="Класс: 11-dependency-check.md:146 (negative). Golden: нет.",
       guard="нет")

lesson(id="I-04", title="Возврат отклонённого или исключённого пункта",
       failure="Пункт, снятый БА, возвращается в следующей версии; закрытые вопросы переоткрываются.",
       rule="Отклонённое фиксируется в 8.5 и не возвращается без нового основания и решения БА.",
       phase="a-core / a-work", section="3, 6, 8.5", severity="high",
       freq="RUN-0075 C09=16; RUN-0021 (переоткрыты закрытые вопросы); RUN-0025 (переоткрыто решение БА).",
       sources=[f"{E75}:56", "runs/2026/RUN-0021/feedback/review-notes.md:47", "runs/2026/RUN-0021/feedback/review-notes.md:84"],
       cids=["C06"],
       cov={"a": ["generic", f"{MC}30-targeted-edit.md:103 «сохранять … отклонённые варианты вне него» (только C30); {MC}16-fr-delta.md:136 «Условия, область, ID и решения сохранены» {COMMON}. В порождающих классах (16, 17, 18, 21, 23) правила «отклонённое не возвращается» нет"],
            "b": ["generic", f"{ST}:89-90 отклонённые варианты переносятся в FULL; {ST}:97-98 нельзя бесследно удалить прежнее исключение — перенос данных, а не запрет возврата"],
            "c": ["explicit", f"{CP}:141 АД-2 «Пункт, отклонённый БА, записан в 8.5 …»; prompts/bcreq-extra-risk-analysis-stepwise.md:59-60"],
            "d": ["generic", f"{SEC}README.md:130 Р3"]},
       examples="Класс: нет. Golden: нет отдельного (C06: GS-375-PRB-04, FR-03, SOL-03).",
       guard="нет",
       old=f"{CP}:141 АД-2")

lesson(id="I-05", title="Регресс согласованной формулировки или значения БА",
       failure="Согласованный текст переписан; значение, заданное БА (лимит 1000), заменено (на 20) или помечено «пересмотреть».",
       rule="Согласованные формулировки, значения, нумерация и журнал 8.5 не меняются молча; перед выдачей — сверка с журналом решений.",
       phase="a-core / a-work", section="все", severity="critical",
       freq="RUN-0074 C06=11; RUN-0076 C06=18 (13 повторов); RUN-0073 C06=4; RUN-0027 Г2; RUN-0020 D-серия; RUN-0016 P1.",
       sources=[e74("C06"), f"{PI76}:29", f"{E73}:53", "runs/2026/RUN-0027/feedback/review-notes.md:27", "runs/2026/RUN-0016/feedback/ba-review-notes.md:54"],
       cids=["C06"],
       cov={"a": ["explicit", f"{MC}30-targeted-edit.md:103 «сохранять согласованные формулировки, ID, единицы, исключения»; {MC}16-fr-delta.md:136 {COMMON}; {MC}39-manifest-alignment.md:101"],
            "b": ["explicit", f"{ST}:97-98; {ST}:115-119 (approval становится stale)"],
            "c": ["explicit", f"{CP}:117 Р3"],
            "d": ["explicit", f"{SEC}README.md:130 Р3"]},
       examples="Класс: 30-targeted-edit.md:145 «Ошибка: Заодно переписана принятая терминология соседних разделов.» Golden: GS-375-PRB-04, FR-03, SOL-03 (C06), не подключены.",
       guard=f"{V403}:105-110 (round-trip сохраняет атомы — структурно); {V403}:155-160 прямо фиксирует, что смысловая инверсия НЕ обнаруживается",
       notes="Рекомендация RUN-0076 «сверять раздел с журналом решений БА перед выдачей» в классах сформулирована только косвенно (входом «относящиеся решения»).")

lesson(id="I-06", title="Правка вне запрошенного объёма",
       failure="При точечной правке модель «заодно» улучшает соседние пункты и разделы; смысловой сдвиг под видом вычитки.",
       rule="Назвать операцию и объём; менять только разрешённое; смежное — на решение БА; изменения таблицей было/стало/основание.",
       phase="все", section="все", severity="high",
       freq="RUN-0018 (смысловой сдвиг под видом вычитки); RUN-0020 D-серия; RUN-0074 C05/C06.",
       sources=["runs/2026/RUN-0018/feedback/review-notes.md:41-46", f"{SP74}:131"],
       cids=["C05", "C06"],
       cov={"a": ["explicit", f"{MC}30-targeted-edit.md:103 «Править только разрешённый объём»; :134 «нет улучшений вне запроса»; :145"],
            "b": ["explicit", f"{ST}:97-98"],
            "c": ["explicit", f"{CP}:156 АД-9 «Граница правки»"],
            "d": ["generic", f"{SEC}README.md:130 Р3"]},
       examples="Класс: 30-targeted-edit.md:145 (negative).", guard="нет")

lesson(id="I-07", title="Несанкционированное удаление, переименование, слияние",
       failure="Пункт 6.1.4 молча удалён при объявлении «готово»; сущность переименована; условия схлопнуты.",
       rule="Удаление, слияние и переименование — только по решению БА, с tombstone и проверкой зависимостей.",
       phase="все", section="все", severity="critical",
       freq="RUN-0074 C05=1; RUN-0076 C05=9 (7 повторов); RUN-0073 C05=3; RUN-0018 Г7.",
       sources=[e74("C05"), f"{PI76}:46", f"{E73}:52", "runs/2026/RUN-0018/feedback/review-notes.md:46"],
       cids=["C05"],
       cov={"a": ["explicit", f"{MC}14-glossary.md:100 «Не переименовывать сущность без решения БА»; {MC}12-phase-assembly.md:103 «Не схлопывать разные условия»; {MC}30-targeted-edit.md:103"],
            "b": ["explicit", f"{ST}:93-98 (tombstones, нельзя бесследно удалить)"],
            "c": ["explicit", f"{CP}:156 АД-9 «удаление/слияние/переименование только по решению БА»"],
            "d": ["explicit", f"{SEC}01-glossary.md:151; {SEC}README.md:130 Р3"]},
       examples="Класс: 14-glossary.md:142 (negative).",
       guard=f"{V403}:142-153 (tombstone требует authorized_by и не ломает зависимости) — для JSON-состояния")

lesson(id="I-08", title="Смысловой дрейф: потеря «только», отрицаний, единиц, условий",
       failure="«Только» теряется при декомпозиции, секунды становятся минутами, отрицание ослабляется; структура при этом валидна.",
       rule="Сохранять отрицания, единицы, исключения и область; сверять результат с исходным манифестом по смыслу, не только по diff.",
       phase="все", section="все", severity="critical",
       freq="RUN-0018 (семантический сдвиг); replay-контроль seconds-changed-to-minutes; RUN-0076 C12 (41/37 повторов, частично).",
       sources=["docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md:311-369", "runs/2026/RUN-0018/feedback/review-notes.md:41-46"],
       cids=["C12", "C06"],
       cov={"a": ["explicit", f"{MC}02-normalize.md:103,145 «потеряно слово «только»»; {MC}16-fr-delta.md:125 «Сохранять отрицания, единицы, исключения» {COMMON}; {MC}29-impact.md:96; {MC}39-manifest-alignment.md:101"],
            "b": ["explicit", f"{ST}:97-98 «Нельзя бесследно удалить отрицание, единицу …»; {ST}:157"],
            "c": ["generic", "отдельного правила про единицы/отрицания нет (не найдено поиском); косвенно АД-9, Р3"],
            "d": ["generic", f"{SEC}README.md:130 Р3"]},
       examples="Класс: 02-normalize.md:145 (negative). Golden: нет.",
       guard=f"нет смыслового; {V403}:155-160 фиксирует, что структурная проверка не ловит инверсию смысла",
       notes="c/d — по результатам поиска; возможны формулировки, не найденные шаблонами (uncertain).")

lesson(id="I-09", title="Структура, нумерация и форма документа БА",
       failure="Меняется нумерация, порядок, «Вопрос N.»; возвращаются удалённые преамбулы; структура «размазывается».",
       rule="Нумерация и форма — как в согласованных разделах/части 4.1; не менять без решения БА.",
       phase="a-core / a-work", section="все", severity="high",
       freq="RUN-0074 C21=5, C11=3; RUN-0076 C11=18 (15 повторов); RUN-0073 C11=4; RUN-0020 D-серия.",
       sources=[e74("C21"), e74("C11"), f"{PI76}:48", "runs/2026/RUN-0020/feedback/ba-review-notes.md"],
       cids=["C21", "C11"],
       cov={"a": ["generic", f"{MC}16-fr-delta.md:136 «Условия, область, ID и решения сохранены» {COMMON}; {MC}31-conformance.md:100 (8 заголовков). Правила сохранять нумерацию/форму БА нет"],
            "b": ["generic", f"{ST}:93-98 (стабильность ID)"],
            "c": ["explicit", f"{CP}:74 «нумерация не меняется»; {CP}:117 Р3; {CP}:174 АП3"],
            "d": ["explicit", f"{SEC}README.md:130 Р3 «формулировки, нумерация … не оспариваются молча»"]},
       examples="Класс: 31-conformance.md:142 (про ложную корректность заголовков). Golden: GS-375-SOL-05, DLG-08 (C21).",
       guard="нет",
       old=f"{SP74}:130 правило 4 «Форма (заголовки, нумерация, двоеточие после названия пункта) — как в СОГЛАСОВАННЫХ РАЗДЕЛАХ»; prompts/archive/fr-validation-legacy.md:54,63-64; {CP}:174 АП3")

lesson(id="I-10", title="Удержание формата ответа, заданного БА в диалоге",
       failure="БА просит «просто список вопросов, без заголовков»; после постороннего запроса формат теряется.",
       rule="Формат, заданный БА, действует до явной отмены; каждый ответ проверяется на него.",
       phase="все (диалог)", section="8.4 / диалог", severity="medium",
       freq="RUN-0029 R1 (реплики 10, 11, 15, 16).",
       sources=["runs/2026/RUN-0029/feedback/review-notes.md:44-49"],
       cids=["C21"],
       cov={"a": ["absent", "у классов фиксированный JSON-выход; правила удержания формата БА нет (поиск «без заголовков|формат ответа» — 0)"],
            "b": ["absent", "—"],
            "c": ["generic", f"{CP}:177 АП6 «Каждый ответ шага — по блоку «Формат вывода» шага» — формат промпта, не БА"],
            "d": ["absent", "—"]},
       examples="нет", guard="нет",
       notes="Урок из ранних RUN; в репозитории нормативной формулировки не найдено.")

lesson(id="I-11", title="Выдуманные числа, пороги, SLA, значения по умолчанию",
       failure="≤100 мс, 24/7, 99,9 %, ≤200 КБ, «по умолчанию 600 сек» без источника.",
       rule="Число и единица — только из входа с локатором; иначе [ТРЕБУЕТСЯ УТОЧНЕНИЕ] и вопрос в 8.4.",
       phase="a-core / a-work", section="4, 7, 8.1", severity="critical",
       freq="RUN-0074 C09=32 (общая); RUN-0076 C09=48 (45 повторов); RUN-0073 C09=23; RUN-0025 Г1; RUN-0027 Г1; RUN-0029 Г3.",
       sources=[e74("C09"), f"{PI76}:47", f"{E73}:56", "runs/2026/RUN-0025/feedback/review-notes.md:24", "runs/2026/RUN-0027/feedback/review-notes.md:26", "runs/2026/RUN-0029/feedback/review-notes.md:23"],
       cids=["C09"],
       cov={"a": ["explicit", f"{MC}18-nfr.md:102 «число и единица только из входа. Не создавать типовые SLA»; :144 «назначено 99,9%»; {MC}25-risks.md:106,148; {MC}24-uc-boundaries.md:136 «произвольный таймаут»"],
            "b": ["generic", f"{ST}:74-75 (локатор)"],
            "c": ["explicit", f"{CP}:115 Р2; {CP}:145 АД-6"],
            "d": ["explicit", f"{SEC}04-non-functional-requirements.md:69 CB-4.1 «Не придумывать порог»"]},
       examples="Класс: 18-nfr.md:144, 25-risks.md:148, 24-uc-boundaries.md:136. Golden: GS-375-PRB-01, FR-07, SOL-02, DLG-02 (C09), не подключены.",
       guard="нет",
       notes="Правило явное, но в RUN-0076 «есть, но не удержалось» (45 повторов): наличие строки не гарантирует исполнения.")

lesson(id="I-12", title="Выдуманная функция, элемент UI, цитата, ограничение продукта",
       failure="Вымышленная цитата «Номер защищен»; придуманное ограничение MANGO; несуществующий endpoint.",
       rule="Утверждение о продукте — только с проверяемой цитатой; неизвестное — вопрос.",
       phase="a-in / a-core / a-work", section="2, 3, 5, 6", severity="critical",
       freq="RUN-0075 C01=48; RUN-0018 Г2; RUN-0024 [2] «Критически не правильНО».",
       sources=[f"{E75}:48", "runs/2026/RUN-0018/feedback/review-notes.md:41", "runs/2026/RUN-0024/feedback/ba-review-notes.md:26"],
       cids=["C09"],
       cov={"a": ["explicit", f"{MC}08-document-evidence.md:114 «не выдумывать страницы»; {MC}22-solution-l2.md:142 «Придуманный endpoint объявлен существующим API»; {MC}23-constraints.md:109 «Ограничение без основания: вопрос»; {MC}16-fr-delta.md:135 {COMMON}"],
            "b": ["explicit", f"{ST}:74-75"],
            "c": ["explicit", f"{CP}:140 АД-1; {CP}:145 АД-6"],
            "d": ["explicit", f"{SEC}README.md:128 Р2"]},
       examples="Класс: 22-solution-l2.md:142. Golden: C09-кейсы (см. I-11).", guard="нет")

lesson(id="I-13", title="Локатор: страница, раздел, цитата",
       failure="Цитата без страницы; непроверяемые страницы; «разделы 3.1, 2.17» как подтверждение гипотезы.",
       rule="Локатор = источник + версия + раздел + дословная цитата; страница только проверенная.",
       phase="все", section="все", severity="critical",
       freq="RUN-0075 C11=9; RUN-0025 Г2-Г3; RUN-0027 Г5; RUN-0029 Г2; RCA RUN-0065/0066.",
       sources=[f"{E75}:58", "runs/2026/RUN-0029/feedback/review-notes.md:22", "docs/report/2026-09-01-run-0065-vs-0066-ab-rca.md"],
       cids=["C09"],
       cov={"a": ["explicit", f"{MC}08-document-evidence.md:106 «страницы только из фактического документа или frontmatter», :148; {MC}07-web-evidence.md:105 «URL без цитаты не доказательство»"],
            "b": ["explicit", f"{ST}:74-75 «источник, версия, раздел/заголовок и цитата; страницы только проверенные»"],
            "c": ["explicit", f"{CP}:112 Р1; {CP}:180 АП9"],
            "d": ["explicit", f"{SEC}README.md:124 Р1"]},
       examples="Класс: 08-document-evidence.md:148.",
       guard="scripts/validate_pagination_shift.py (KB-цитаты против frontmatter; применяется к отчётам RUN-0066+, не к выходам классов)")

lesson(id="I-14", title="Цитата не доказывает вывод: сверхобобщение, коннектор ≠ платформа",
       failure="Задокументированный частный факт расширен на всю роль/продукт; «не описано» прочитано как «не поддерживается»; функция платформы приписана коннектору.",
       rule="Указывать область доказательства; различать «не описано», «недоступен», «не поддерживается», «Нет данных».",
       phase="a-in / a-core", section="2, 3, 5", severity="high",
       freq="RUN-0075 C10=10; RUN-0077 (коннектор vs платформа, «Нет данных»); RUN-0018 Г4-Г5.",
       sources=[f"{E75}:57", "runs/2026/RUN-0077/feedback/review-notes.md:11-14", "runs/2026/RUN-0077/feedback/review-notes.md:29"],
       cids=["C09", "C15"],
       cov={"a": ["explicit", f"{MC}07-web-evidence.md:136 «Цитата поддерживает именно утверждение», :147; {MC}05-taxonomy.md:103,145 «Нет совпадения означает пробел классификации»; {MC}10-source-conflicts.md:103; {MC}28-independent-review.md:105 (entailment)"],
            "b": ["explicit", f"{ST}:157 «Доказательство наличия текста не равно правильности вывода»"],
            "c": ["explicit", f"{CP}:155 АД-8; {CP}:302 «Нет БЗ не означает «функции нет»»"],
            "d": ["generic", "отдельного правила об области доказательства нет"]},
       examples="Класс: 07-web-evidence.md:147, 05-taxonomy.md:145.", guard="нет")

lesson(id="I-15", title="Вывод без чтения источника (URL, сниппет, память, «изучено ранее»)",
       failure="Выводы до получения документации; URL объявлен прочитанным; все галлюцинации RUN-0023 — ссылки на непроверенный источник.",
       rule="Не делать выводов до чтения; URL не доставка текста; недоступное — UNKNOWN и запрос.",
       phase="a-in", section="2, 3", severity="critical",
       freq="RUN-0017 [10]; RUN-0021 Г2; RUN-0023 (все галлюцинации).",
       sources=["runs/2026/RUN-0017/feedback/ba-review-notes.md:23", "runs/2026/RUN-0023/feedback"],
       cids=["C09", "C18"],
       cov={"a": ["explicit", f"{MC}07-web-evidence.md:105,113 «не имитировать browsing»; {MC}13-handoff-check.md:101,143; {MC}16-fr-delta.md:24 «не из памяти модели» {COMMON}"],
            "b": ["explicit", f"{ST}:21-23 «URL не считается доставленным текстом … Не восстанавливать по памяти»"],
            "c": ["explicit", f"{CP}:160-162 CB-0.6 «не заменяй его догадкой»"],
            "d": ["generic", f"{SEC}README.md:128-129"]},
       examples="Класс: 13-handoff-check.md:143, 07-web-evidence.md:147.", guard="нет")

lesson(id="I-16", title="Источник As-Is: документация продукта, а не сайт, документы заказчика или API",
       failure="Документы заказчика приняты за документацию продукта; As-Is выведен из API-описания или сайта.",
       rule="As-Is — из документации продукта дословно с локатором; приложенный БА baseline приоритетен в своей области.",
       phase="a-in", section="2, 3", severity="high",
       freq="RUN-0020 H1; experiment-1027 H1; replay-контроль api-only-and-wrong-owner.",
       sources=["runs/2026/RUN-0020/feedback/ba-review-notes.md", "docs/analysis/experiment-1027-analysis.md"],
       cids=["C09", "C15"],
       cov={"a": ["explicit", f"{MC}08-document-evidence.md:106 «Приложенный БА baseline приоритетен»; {MC}10-source-conflicts.md:103,145"],
            "b": ["generic", f"{ST}:74-75"],
            "c": ["explicit", f"{CP}:140 АД-1; {FRP}:54-56"],
            "d": ["generic", "—"]},
       examples="Класс: 10-source-conflicts.md:145.", guard="нет")

lesson(id="I-17", title="API-домыслы и API-интеграция в ФТ для заказчика",
       failure="В ФТ для заказчика вставлены API-методы; основания по событиям API; «известен API — значит дорабатываем».",
       rule="ФТ без API; публичный API — раздел 5 L2 и только из предоставленного контракта.",
       phase="a-core / a-work", section="3, 5", severity="high",
       freq="RUN-0075 C06=16; RUN-0026 [16]; RUN-0025 Г4.",
       sources=[f"{E75}:53", "runs/2026/RUN-0026/feedback/ba-review-notes.md:28", "runs/2026/RUN-0025/feedback/review-notes.md:27"],
       cids=["C01"],
       cov={"a": ["explicit", f"{MC}06-scope.md:97 «Известность API не означает задачу на доработку API»; {MC}16-fr-delta.md:102 «без UI, API, сервисов и НФТ»; {MC}22-solution-l2.md:100,142"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:145 АД-6"],
            "d": ["explicit", f"{SEC}05-solution-description.md:72,110,117"]},
       examples="Класс: 22-solution-l2.md:142, 06-scope.md:139.", guard="нет")

lesson(id="I-18", title="Адресат вопроса и документа; отсылка в техподдержку",
       failure="Вопрос о реализации задан заказчику; вопрос без владельца; «уточните в техподдержке».",
       rule="Заказчику — о потребности, команде — о реализации, владельцу продукта — о продукте; не отсылать в поддержку.",
       phase="a-in / a-core", section="8.4", severity="high",
       freq="RUN-0074 C08=1; RUN-0073 C08=6; RUN-0076 C08=2; RUN-0075 C03=2, C14=3.",
       sources=[e74("C08"), f"{E73}:55", f"{E76}:55", f"{E75}:50"],
       cids=["C08"],
       cov={"a": ["generic", f"{MC}04-questions.md:104 «одним пакетом по адресатам», :112 «Нет адресата … запросить владельца у БА»; {MC}32-audience-projection.md:96. Типизации адресатов и запрета отсылки в поддержку нет"],
            "b": ["generic", f"{ST}:121-126 (пакет вопросов с владельцами)"],
            "c": ["explicit", f"{CP}:157 АД-10 «Заказчику — о потребности, команде — о реализации …»"],
            "d": ["generic", f"{SEC}08-supplementary.md:36-38 (таблица 8.4)"]},
       examples="Класс: 04-questions.md:144 (positive «Один пакет по адресатам»).", guard="нет",
       old=f"{CP}:157 АД-10")

lesson(id="I-19", title="Избыточный или повторный вопрос; игнорирование контекста",
       failure="Вопрос о том, что уже есть в черновике, вложении или решениях БА; десять последовательных вопросов.",
       rule="До вопроса — поиск в запросе, черновике, вложениях, 8.5; повтор только при новом основании; пакет одним сообщением.",
       phase="a-in / a-core", section="8.4", severity="high",
       freq="RUN-0074 C07=8; RUN-0073 C07=8; RUN-0076 C07=4 (3 повтора).",
       sources=[e74("C07"), f"{E73}:54", f"{PI76}:30"],
       cids=["C07"],
       cov={"a": ["explicit", f"{MC}04-questions.md:104 «Повторять только при новом основании», :146"],
            "b": ["explicit", f"{ST}:121-126"],
            "c": ["explicit", f"{CP}:157 АД-10"],
            "d": ["generic", "—"]},
       examples="Класс: 04-questions.md:146. Golden: GS-375-PRB-07, DLG-03 (C07).", guard="нет",
       old="prompts/archive/questions-customer-understanding-legacy.md:53")

lesson(id="I-20", title="Технические атрибуты в вопросах для нетехнического заказчика",
       failure="Вопрос заказчику про RTP-поток, SIP-транки, поля API.",
       rule="Вопросы стейкхолдеру — на языке потребности, без технических атрибутов.",
       phase="a-in / a-core", section="8.4", severity="high",
       freq="RUN-0024 [4]; Golden GS-375-DLG-04 «Идет ли RTP-поток…» (C01).",
       sources=["runs/2026/RUN-0024/feedback/ba-review-notes.md:27", f"{GS} GS-375-DLG-04"],
       cids=["C08", "C01"],
       cov={"a": ["absent", "в 04-questions.md правила о лексике вопросов заказчику нет; 32-audience-projection.md:96 касается только UC раздела 7"],
            "b": ["absent", "—"],
            "c": ["generic", f"{CP}:157 АД-10 (адресат по типу вопроса), без запрета терминов"],
            "d": ["absent", "—"]},
       examples="Golden GS-375-DLG-04 (negative) — не подключён.", guard="нет",
       old="prompts/archive/glossary-context-understanding-oneshot.md:15 «Никаких … технических деталей, упоминаний API, БД или UI» (для текста раздела, не вопросов)",
       notes="Деградация неочевидна: явного правила именно для вопросов не было и раньше (uncertain).")

lesson(id="I-21", title="Архитектура и реализация в ФТ (SIP, RTP, сервисы, БД)",
       failure="«Доработка ядра маршрутизации ВАТС», «сервис записи», SIP-сессии в разделе 3.",
       rule="ФТ — что должна дать система; реализация — раздел 5, только по входам.",
       phase="a-core / a-work", section="3, 5", severity="critical",
       freq="RUN-0074 C01=18; RUN-0073 C01=21; RUN-0076 C01=18 (16 повторов).",
       sources=[e74("C01"), f"{E73}:48", f"{PI76}:44"],
       cids=["C01"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:102; {MC}21-solution-l1.md:100 «Не выдумывать SIP/RTP, БД и внутренние сервисы», :142; {MC}15-business-context.md:101"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:145-146 АД-6, АД-7; {FRP}:77-86"],
            "d": ["explicit", f"{SEC}03-functional-requirements.md:30-37 (Ф4), :103-108; {SEC}05-solution-description.md:117"]},
       examples="Класс: 21-solution-l1.md:142. Golden: GS-375-FR-04, SOL-01, DLG-04 (C01).", guard="нет",
       notes="Правило было и в старом стандарте (S3, S6), но в RUN-0076 «не удержалось» (16 повторов).")

lesson(id="I-22", title="Декларация методологии и CBAP-роль в тексте",
       failure="«По принципу TM Forum ODA», «Clean Architecture», «ведущий аналитик (CBAP)» в документе и роли.",
       rule="Методология — инструмент аналитика; названия в разделы 1-6 не вносятся; роль — функция.",
       phase="все", section="1-6", severity="high",
       freq="RUN-0074 C02=7; RUN-0076 C02=12; RUN-0073 C02=4; RUN-0076 I-001.",
       sources=[e74("C02"), f"{E76}:49", f"{PI76}:61"],
       cids=["C02", "C19"],
       cov={"a": ["generic", f"{MC}22-solution-l2.md:100 «TM Forum только как выбранная альтернатива L2» — запрета названий методологий в тексте нет"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:122 Р5; {CP}:172 АП1"],
            "d": ["explicit", f"{SEC}README.md:137 Р5"]},
       examples="Golden: GS-375-SOL-06, DLG-06, PRM-01, PRM-03, PRM-05 (C02/C19) — не подключены.", guard="нет",
       old=f"{SP74}:119 «Названия стандартов в текст документа не вносишь»; {CP}:122 Р5")

lesson(id="I-23", title="«Индустриальная практика», непрошенные функции, диктовка процесса заказчику",
       failure="Функции «по лучшей практике» внесены в ФТ; процесс заказчика оценивается и «улучшается».",
       rule="Индустриальное — отдельным блоком «Рекомендация — на решение БА»; процесс заказчика — входное условие.",
       phase="a-core", section="3", severity="high",
       freq="RUN-0074 C03=5; RUN-0076 C03=10 (9 повторов); RUN-0075 C02=10; RUN-0021 «commonly used».",
       sources=[e74("C03"), f"{PI76}:45", f"{E75}:49"],
       cids=["C03"],
       cov={"a": ["generic", f"{MC}16-fr-delta.md:133 «рекомендация включена только после решения БА»; {MC}09-ba-enrichment.md:97 «авторская рекомендация не стала фактом». Термина «индустриальная практика» и правила о процессе заказчика нет (поиск — 0)"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:119 Р4; {CP}:144 АД-5"],
            "d": ["explicit", f"{SEC}03-functional-requirements.md:91-99 «Индустриально значимые — на решение БА»"]},
       examples="Golden: GS-375-FR-05, PRM-02 (C03).", guard="нет",
       old=f"{CP}:119 Р4, :144 АД-5; {SEC}03-functional-requirements.md:91-99")

lesson(id="I-24", title="Расширение границ (scope creep)",
       failure="Смежная система «упомянута — значит дорабатывается»; добавлены объекты вне запроса.",
       rule="Отделять чтение смежного продукта от изменения; изменение границ — решение БА.",
       phase="a-in / a-core", section="2.4, 3", severity="high",
       freq="RUN-0074 C04=3; RUN-0076 C04=12 (8 повторов).",
       sources=[e74("C04"), f"{PI76}:46"],
       cids=["C04"],
       cov={"a": ["explicit", f"{MC}06-scope.md:97,139; {MC}39-manifest-alignment.md:101 «расширение границ»"],
            "b": ["generic", "—"],
            "c": ["explicit", f"{CP}:158 АД-11; {FRP}:57-60 «→ раздел 5»"],
            "d": ["explicit", f"{SEC}02-business-context.md:37 (2.4.1/2.4.2)"]},
       examples="Класс: 06-scope.md:139. Golden: GS-375-PRB-03 (C04).", guard="нет")

lesson(id="I-25", title="Нерелевантные факты, нет повторного поиска",
       failure="В раздел попадают факты документации, не меняющие требования; старый поиск используется вместо нового.",
       rule="Отбирать только факты, меняющие требования задачи; совпадение ключевых слов не доказывает релевантность.",
       phase="a-in", section="2, 3", severity="high",
       freq="RUN-0074 C23=10.",
       sources=[e74("C23")],
       cids=["C23"],
       cov={"a": ["generic", f"{MC}16-fr-delta.md:121-122 «Предыдущие длинные поисковые выводы не копировать вместо атомарных фактов» {COMMON}. Фильтра релевантности нет"],
            "b": ["absent", "—"],
            "c": ["explicit", "prompts/bcreq-context-understanding-stepwise.md:93-96 «совпадение ключевых слов не доказывает релевантность»"],
            "d": ["generic", f"{SEC}03-functional-requirements.md:30-37 Ф2 (трассировка)"]},
       examples="Golden: GS-375-PRB-02 (C23).", guard="нет",
       old=f"{SP74}:129 правило 2 «в ответ попадает только то, что меняет требования этой задачи»")

lesson(id="I-26", title="Не-требование в ФТ (определения, перечни, решения команды)",
       failure="«FR-01. К целевым исходящим контактам относятся: …» — определение вместо требования.",
       rule="ФТ отвечает на вопрос «что должна делать система»; определения — в глоссарий, решения — в 8.5.",
       phase="a-core", section="3", severity="high",
       freq="RUN-0074 C24=11.",
       sources=[e74("C24"), f"{GS} GS-375-FR-01, FR-09"],
       cids=["C24"],
       cov={"a": ["generic", f"{MC}16-fr-delta.md:102 «Описывать что должна дать система»; {MC}21-solution-l1.md:100 «Отделить факт, предлагаемую реализацию и решение команды»"],
            "b": ["absent", "—"],
            "c": ["generic", f"{FRP}:77-86 (формулы ФТ)"],
            "d": ["generic", f"{SEC}03-functional-requirements.md:103-108"]},
       examples="Golden: GS-375-FR-01 (negative), FR-09 (positive).", guard="нет",
       old=f"{SP74}:156 «каждое ФТ отвечает на вопрос «что должна делать система», а не определяет термин или перечень»")

lesson(id="I-27", title="Штатный функционал (As-Is) оформлен как изменение",
       failure="Текущее поведение продукта записано новым ФТ; добавлено для «семи пунктов».",
       rule="Только дельта; штатное — ссылкой на As-Is с локатором.",
       phase="a-core", section="3", severity="high",
       freq="RUN-0075 C07=8; experiment-1027 (поздняя проверка против As-Is).",
       sources=[f"{E75}:54", "docs/analysis/experiment-1027-analysis.md"],
       cids=["C24", "C09"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:110,144 «Штатная функция добавлена как новое ФТ»; {MC}37-user-story.md:105"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:146 АД-7; {FRP}:54-56"],
            "d": ["explicit", f"{SEC}03-functional-requirements.md:32 Ф1"]},
       examples="Класс: 16-fr-delta.md:144.", guard="нет")

lesson(id="I-28", title="Избыточная декомпозиция и квоты на число пунктов",
       failure="По одному ФТ на поле; объём «под квоту».",
       rule="3-7 ФТ верхнего уровня (5±2) или обоснование; не дробить функцию на шаги; не дополнять до числа.",
       phase="a-core", section="3", severity="medium",
       freq="RUN-0074 C25=6; experiment-1027 H4.",
       sources=[e74("C25"), "docs/analysis/experiment-1027-analysis.md"],
       cids=["C25"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:102 «не дополнять до числа искусственно», :144"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{FRP}:64-69; {CP}:124 Р6"],
            "d": ["explicit", f"{SEC}03-functional-requirements.md:72-89"]},
       examples="Golden: GS-375-FR-02 (negative), FR-10 (positive).", guard="нет")

lesson(id="I-29", title="Неатомарность, двусмысленность, англоязычный жаргон, стиль",
       failure="Составные ФТ, «мгновенно», «удобно», английские метки и жаргон.",
       rule="Стиль КС1-КС7 / БС1-БС5, один термин — из раздела 1, метки на русском.",
       phase="все", section="все", severity="high",
       freq="RUN-0074 C12=8; RUN-0076 C12=41 (37 повторов); RUN-0073 C12=14; RUN-0075 C12=8.",
       sources=[e74("C12"), f"{PI76}:49", f"{E73}:59", f"{E75}:59"],
       cids=["C12"],
       cov={"a": ["generic", f"{MC}16-fr-delta.md:102 «атомарность» (одно слово); {MC}03-ambiguity.md:102. Стоп-слов, КС/БС и запрета жаргона нет (поиск — 0)"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:92-105 КС1-КС7, БС1-БС5; {CP}:178 АП7"],
            "d": ["explicit", f"{SEC}README.md:78-80, 102-108"]},
       examples="Golden: GS-375-PRB-05, FR-06, SOL-08 (C12).", guard="нет",
       old=f"{CP}:92-105; {SP74}:157 «в ФТ нет «мгновенно», «100%», «удобно»»")

lesson(id="I-30", title="Формула ФТ «Система должна предоставлять <кому> возможность …»",
       failure="«Сотруднику доступна возможность», «обеспечивать» вместо «предоставлять возможность»; запрет «Система должна» в шаблоне.",
       rule="Действие пользователя — «Система должна предоставлять <кому> возможность <действие>»; автоматика — «обеспечивать».",
       phase="a-core", section="3", severity="high",
       freq="RUN-0022 [6], [12]; RUN-0026 [18]; experiment-1027 H2; RUN-0076 I-002.",
       sources=["runs/2026/RUN-0022/feedback/ba-review-notes.md:23-36", "runs/2026/RUN-0026/feedback/ba-review-notes.md:29", f"{PI76}:62"],
       cids=["C12", "C19"],
       cov={"a": ["absent", "в 39 классах формулы нет (поиск «предоставлять … возможность» — 0); 16-fr-delta.md:102 только «Описывать что должна дать система»"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{FRP}:78 «Формулы: «Система должна предоставлять <кому> возможность …»"],
            "d": ["explicit", f"{SEC}03-functional-requirements.md:52, 105"]},
       examples="Раздел d: 03-functional-requirements.md:105 (таблица Корректно/Некорректно). Golden: GS-375-PRB-06 (запрет «Система должна» как дефект).", guard="нет",
       old=f"{SP74}:154 формат «ФТ-NN. Система должна предоставлять Пользователю возможность …»; {FRP}:78")

lesson(id="I-31", title="Доменная модель: настройка в ЛК ВАТС vs исполнение в КЦ; системный уровень",
       failure="Настройка виджета приписана ЛК, хотя задана на системном уровне; смешаны слой настройки и исполнения; неверный класс продукта.",
       rule="Различать, где настраивается и где исполняется; доменное поведение — по документации и уточнениям БА.",
       phase="a-in / a-core", section="2, 3, 5", severity="high",
       freq="RUN-0074 C15=4; RUN-0076 C15=14 (13 повторов); RUN-0073 C15=7; RUN-0026 [6].",
       sources=[e74("C15"), f"{PI76}:32", "runs/2026/RUN-0026/feedback/ba-review-notes.md:26", "docs/rfc/prompt-improvement-bcreq-1025-proposal.md (Б1)", "docs/rfc/prompt-improvement-multichannel-proposal.md (М1)"],
       cids=["C15"],
       cov={"a": ["generic", f"{MC}21-solution-l1.md:100 «Настройка предшествует исполнению»; {MC}05-taxonomy.md:103"],
            "b": ["absent", "—"],
            "c": ["generic", f"{FRP}:57-60 (порядок настройка → исполнение)"],
            "d": ["generic", f"{SEC}03-functional-requirements.md:67"]},
       examples="Golden: GS-375-DLG-05 «product_class: contact-center» (C15).", guard="нет",
       old="docs/rfc/prompt-improvement-bcreq-1025-proposal.md Б1 (ЛК ВАТС vs КЦ); docs/rfc/prompt-improvement-multichannel-proposal.md М1",
       notes="Источники «old» — предложения RFC; принятие их как нормы не проверено (uncertain).")

lesson(id="I-32", title="Роли: существующая ролевая модель (Пользователь vs Сотрудник)",
       failure="Глоссарий модели не отражал роли; «доработка ролевой модели ЛК ВАТС» как ФТ; регресс ролей.",
       rule="Роли и права — из документации и решений БА; новые роли не изобретать.",
       phase="a-in / a-core", section="1, 3, 5", severity="medium",
       freq="RUN-0017 [12]; RUN-0020 (регресс ролей); Golden GS-375-FR-05.",
       sources=["runs/2026/RUN-0017/feedback/ba-review-notes.md:24", f"{GS} GS-375-FR-05"],
       cids=["C15", "C03"],
       cov={"a": ["generic", f"{MC}21-solution-l1.md:131 «существующие роли сохранены»; {MC}11-dependency-check.md:104 «проверить роли»"],
            "b": ["absent", "—"],
            "c": ["absent", "не найдено поиском (uncertain)"],
            "d": ["absent", "не найдено поиском (uncertain)"]},
       examples="Golden GS-375-FR-05 (negative).", guard="нет",
       old=f"{SP74}:170 «Размещение настроек и права — из РЕШЕНИЙ БА»")

lesson(id="I-33", title="Термины и UI-названия заказчика и продукта — дословно",
       failure="UI-названия перефразированы; экспертный термин заменил слово заказчика.",
       rule="Термины БА и заказчика, названия элементов продукта переносятся дословно; замена — только решением БА.",
       phase="a-in", section="1, 2", severity="high",
       freq="RUN-0016 P1; RUN-0074 section-prompts.",
       sources=["runs/2026/RUN-0016/feedback/ba-review-notes.md:54"],
       cids=["C06", "C12"],
       cov={"a": ["explicit", f"{MC}14-glossary.md:100,142 «Экспертный термин молча заменил привычное слово заказчика»; {MC}01-intake.md:96; {MC}02-normalize.md:103"],
            "b": ["absent", "—"],
            "c": ["generic", "отдельного правила в Промпте 0 не найдено; Р3 (формулировки БА)"],
            "d": ["explicit", f"{SEC}01-glossary.md:149,151"]},
       examples="Класс: 14-glossary.md:142.", guard="нет")

lesson(id="I-34", title="Порядок изложения: настройка → исполнение → ресурсы → API",
       failure="Сначала описано, как функция отрабатывает, потом — как настраивается.",
       rule="Порядок настройка → исполнение → ресурсы и данные → API.",
       phase="a-core / a-work", section="3, 5", severity="medium",
       freq="Golden GS-375-SOL-09 (positive, подтверждено пользователем); RUN-0076 C11.",
       sources=[f"{GS} GS-375-SOL-09", f"{FRP}:57-60"],
       cids=["C11"],
       cov={"a": ["explicit", f"{MC}21-solution-l1.md:100 «Настройка предшествует исполнению»; {MC}11-dependency-check.md:104; {MC}28-independent-review.md:105"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{FRP}:57-60"],
            "d": ["generic", "—"]},
       examples="Golden GS-375-SOL-09 (positive).", guard="нет")

lesson(id="I-35", title="Бизнес-контекст без НФТ, реализации, выдуманных выгод и рисков",
       failure="В 2.x — пороги, проект интерфейса, придуманные последствия; шаблонные «3-4 предложения».",
       rule="2.2 — словами заказчика; числа только с источником; НФТ и проектирование — не в контекст.",
       phase="a-in", section="2", severity="medium",
       freq="Golden GS-375-PRB-09 (positive); RUN-0076 I-004, I-008.",
       sources=[f"{GS} GS-375-PRB-09", f"{PI76}:64", f"{PI76}:68"],
       cids=["C24", "C09"],
       cov={"a": ["explicit", f"{MC}15-business-context.md:101 «Не переносить метрики НФТ и проектирование в контекст», :109 «не изобретать выгоду», :143"],
            "b": ["absent", "—"],
            "c": ["generic", "prompts/bcreq-context-understanding-stepwise.md (АД-5, L90)"],
            "d": ["explicit", f"{SEC}02-business-context.md:34-37"]},
       examples="Класс: 15-business-context.md:143. Golden: GS-375-PRB-09.", guard="нет")

lesson(id="I-36", title="Раздел 6: не дублировать ФТ и раздел 5; ограничение = внешнее + последствие",
       failure="Ограничения повторяют ФТ по смыслу; исключённая платформа записана как ограничение; дубли 4.5.1≈6.1.1.",
       rule="6.1 ссылается на особенности раздела 5; 6.2 — внешнее ограничение плюс последствие; исключение платформы — 2.4.2.",
       phase="a-work", section="6", severity="medium",
       freq="RUN-0017 [44]; RUN-0016 (дубли); RUN-0075 C08=3; experiment-1027 H4.",
       sources=["runs/2026/RUN-0017/feedback/ba-review-notes.md:26", "runs/2026/RUN-0016/feedback/ba-review-notes.md:39", f"{E75}:55"],
       cids=["C11", "C24"],
       cov={"a": ["explicit", f"{MC}23-constraints.md:101, 109, 132 «Нет дубля раздела 5»"],
            "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:146 АД-7 (ограничение не ФТ)"],
            "d": ["explicit", f"{SEC}06-implementation-constraints.md:30-31, 52-54, 60-62"]},
       examples="Класс: 23-constraints.md:143.", guard="нет")

lesson(id="I-37", title="Канонические пункты 6.1.1-6.1.3",
       failure="Обязательные неизменные пункты 6.1.1-6.1.3 отсутствуют в разделе 6.",
       rule="Раздел 6 начинается с неизменных 6.1.1 «… ограничены функциональными возможностями продуктов MANGO OFFICE», 6.1.2, 6.1.3 «Дизайн экранных форм …».",
       phase="a-work", section="6", severity="medium",
       freq="experiment-1027 H3.",
       sources=["docs/analysis/experiment-1027-analysis.md (H3)", "prompts/archive/constraints-documentation-stepwise.md:17-21,53"],
       cids=["C13"],
       cov={"a": ["absent", "поиск «6.1.1|ограничены функциональными возможностями|Дизайн экранных форм» — 0"],
            "b": ["absent", "0"], "c": ["absent", "0"], "d": ["absent", "0"]},
       examples="нет", guard="нет",
       old="prompts/archive/constraints-documentation-stepwise.md:17-21 (полный текст 6.1.1-6.1.3), :53; prompts/archive/constraints-documentation-oneshot.md:17,33",
       notes="Не установлено, отказался ли владелец от канона сознательно при переходе на стандарт 06 (uncertain).")

lesson(id="I-38", title="Граница ответственности внешней системы",
       failure="Требования к отображению во внешней системе, которой команда не управляет.",
       rule="Отделять чтение/интеграцию от изменения внешней системы; её поведение — ограничение или зависимость.",
       phase="a-in / a-work", section="2.4, 6.2, 8.2", severity="medium",
       freq="RUN-0017 [48].",
       sources=["runs/2026/RUN-0017/feedback/ba-review-notes.md:27"],
       cids=["C04"],
       cov={"a": ["explicit", f"{MC}06-scope.md:97 «Отделить чтение смежного продукта от его изменения»; {MC}26-delivery-dependencies.md:103"],
            "b": ["absent", "—"],
            "c": ["generic", f"{CP}:158 АД-11"],
            "d": ["generic", f"{SEC}06-implementation-constraints.md:30-31 (6.2 внешнее ограничение)"]},
       examples="Класс: 06-scope.md:139.", guard="нет")

lesson(id="I-39", title="Чужой контекст; локальное правило объявлено глобальным",
       failure="Факты другой задачи или диалога в документе; правило одного кейса вписано в универсальный промпт.",
       rule="Сверять ID задачи; вход другой задачи исключать до решения БА; универсальный промпт без специфики кейса.",
       phase="все", section="все", severity="high",
       freq="RUN-0074 C22=2; replay-контроль local-rule-promoted.",
       sources=[e74("C22"), "docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md:311-369"],
       cids=["C22"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:111 «Чужая задача, несовместимые правила или разрыв ревизий: WAITING» {COMMON}"],
            "b": ["explicit", f"{ST}:42-47"],
            "c": ["explicit", f"{CP}:158 АД-11; {CP}:163 CB-0.7"],
            "d": ["absent", "—"]},
       examples="нет", guard=f"{V403}:116-127 (чужая задача и форк ревизий отклоняются — для JSON-состояния)")

lesson(id="I-40", title="Подмена запроса",
       failure="Модель делает не то, что просили: предлагает «антипаттерн», меняет задачу, «доводит до золотого стандарта».",
       rule="Выполнять запрошенную операцию; иное — предложением на решение БА.",
       phase="все", section="—", severity="high",
       freq="RUN-0074 C20=8.",
       sources=[e74("C20"), f"{GS} GS-375-SOL-04, DLG-07, PRM-04"],
       cids=["C20"],
       cov={"a": ["generic", f"{MC}30-targeted-edit.md:134 «нет улучшений вне запроса»; шаг 1 алгоритма «Проверить соответствие задачи» {COMMON} (16-fr-delta.md:100)"],
            "b": ["generic", "—"],
            "c": ["generic", f"{CP}:156 АД-9"],
            "d": ["absent", "—"]},
       examples="Golden: GS-375-SOL-04, DLG-07, PRM-04 (C20).", guard="нет")

lesson(id="I-41", title="Непрошенный полный вывод документа",
       failure="На запрос одного раздела выдаётся весь документ.",
       rule="Один ответ — один запрошенный раздел или правка.",
       phase="все", section="—", severity="medium",
       freq="RUN-0074 C17=0; RUN-0076 C17=4; RUN-0073 C17=1.",
       sources=[e74("C17"), f"{PI76}:35"],
       cids=["C17"],
       cov={"a": ["explicit", f"режимы SLICE/FULL; {MC}16-fr-delta.md:137 «SLICE не объявлен полным результатом» {COMMON}; {MC}12-phase-assembly.md:103"],
            "b": ["explicit", f"{ST}:86-91 (SLICE/FULL)"],
            "c": ["generic", f"{CP}:177 АП6"],
            "d": ["absent", "—"]},
       examples="нет", guard=f"{V403}:112-114")

lesson(id="I-42", title="Полный текст заменён ссылкой, «см. выше», URL",
       failure="Handoff содержит только «продолжай как выше» и URL; раздел заменён ссылкой на чат.",
       rule="Передавать полный текст; путь/URL и «см. выше» не доставка.",
       phase="все (переходы)", section="—", severity="high",
       freq="Replay-контроли url-without-reading / constitution-omitted (failure-analysis З1-З5).",
       sources=["docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md:311-369"],
       cids=["C13", "C19"],
       cov={"a": ["explicit", f"{MC}13-handoff-check.md:101,143; {MC}12-phase-assembly.md:103 «Не заменять тело ссылкой на чат»; {MC}32-audience-projection.md:96"],
            "b": ["explicit", f"{ST}:18-23; {ST}:105 «Компактный manifest не подменяет полный текст»"],
            "c": ["explicit", f"{CP}:287"],
            "d": ["absent", "—"]},
       examples="Класс: 13-handoff-check.md:143.", guard=f"{V403}:112-114")

lesson(id="I-43", title="Правила не доставлены; «запиши в память» не работает; смешение версий",
       failure="Конституция не вставлена; модель обещает «запомнить» правило; смешаны версии промптов.",
       rule="Полный текст правил в каждом сообщении/вложении; при расхождении версий — стоп; память модели не носитель правил.",
       phase="все", section="—", severity="critical",
       freq="RUN-0020 [68] и вывод о долговременной памяти; replay constitution-omitted, mixed-bundle.",
       sources=["runs/2026/RUN-0020/feedback/ba-review-notes.md:25", "runs/2026/RUN-0020/feedback/ba-review-notes.md:47"],
       cids=["C19"],
       cov={"a": ["explicit", f"{MC}36-rule-bundle.md:101 «Встроить полный текст конституции … При расхождении версий остановить», :109, :143"],
            "b": ["explicit", f"{ST}:18-23, :26"],
            "c": ["explicit", f"{CP}:287-288"],
            "d": ["generic", "—"]},
       examples="Класс: 36-rule-bundle.md:143.",
       guard="scripts/test_issue_395_bcreq.py:31-49 — только для промптов (c): в каждом есть «Р1–Р7», «АД-1…АД-11» и т.д.; для 39 классов аналога нет")

lesson(id="I-44", title="Дефект шаблона промпта, индуцирующий ошибку",
       failure="Шаблон сам требует CBAP-роль, запрещает «Система должна», предписывает «готов к формированию».",
       rule="Промпт универсален, непротиворечив, согласован со стандартом; ошибки ответа проверяются на происхождение из шаблона.",
       phase="все", section="—", severity="high",
       freq="RUN-0074 C19=5; RUN-0073 C19=18; RUN-0076 C19=23 (15 повторов), I-001..I-008; RUN-0075 C15=7.",
       sources=[e74("C19"), f"{E73}:66", f"{PI76}:55-68", f"{E75}:62"],
       cids=["C19"],
       cov={"a": ["absent", "в классах нет проверки самих шаблонов против I-001..I-008; регрессионного прогона классов на golden нет"],
            "b": ["absent", "—"],
            "c": ["generic", f"{CP}:158 АД-11 (универсальный промпт без специфики кейса)"],
            "d": ["absent", "—"]},
       examples="Golden: GS-375-PRB-06, PRM-03 (C19).",
       guard="нет для содержания; validate_issue_403 проверяет только структуру (8 заголовков, 2 JSON-примера) — {0}:28-36".format(V403))

lesson(id="I-45", title="«Розовый слон»: оговорка об отсутствующей ошибке",
       failure="В документ добавлена оговорка о проблеме, которой во входе не было (после снятой собственной находки).",
       rule="Опровергнутую собственную находку снимать, не фиксировать.",
       phase="все", section="все", severity="medium",
       freq="RUN-0076 C20=2 (1 повтор); SC-65.",
       sources=[f"{E76}:67", f"{PI76}:37"],
       cids=[],
       cov={"a": ["absent", "поиск — 0"], "b": ["absent", "—"],
            "c": ["explicit", f"{CP}:165-166 «не добавляй в документ оговорку об отсутствии ошибки … (RUN-0076, SC-65)»"],
            "d": ["absent", "—"]},
       examples="нет", guard="нет",
       old=f"{CP}:165-166")

lesson(id="I-46", title="Ложная апелляция или ложный конфликт",
       failure="Заявлено противоречие без цитат обеих сторон; риторика против собственного источника.",
       rule="Противоречие — только с цитатами обеих сторон; стоп зависимого вывода.",
       phase="все", section="все", severity="high",
       freq="RUN-0074 C14=1; RUN-0076 C14=11 (9 повторов); RUN-0073 C14=3; RUN-0027 Г3-Г4.",
       sources=[e74("C14"), f"{PI76}:31", "runs/2026/RUN-0027/feedback/review-notes.md:28-29"],
       cids=["C14"],
       cov={"a": ["generic", f"{MC}10-source-conflicts.md:103,111; {MC}28-independent-review.md:113 «материальное противоречие блокирует». Требования «цитаты обеих сторон» нет"],
            "b": ["generic", f"{ST}:42-47"],
            "c": ["generic", f"{CP}:55 CB-0.4"],
            "d": ["explicit", f"{SEC}01-glossary.md:141 CB-1.1; {SEC}02-business-context.md:74 CB-2.2; {SEC}04-non-functional-requirements.md:70 CB-4.2 «привести обе цитаты»"]},
       examples="Golden: GS-375-PRB-08 (C14).", guard="нет",
       old=f"{SEC}04-non-functional-requirements.md:70 и др. CB-x «Остановиться, привести обе цитаты»")

lesson(id="I-47", title="Предвзятая аргументация в пользу варианта",
       failure="«Вариант А (наиболее логичный)» — модель продавливает свой выбор.",
       rule="Варианты сравниваются по общим критериям; решение за человеком.",
       phase="a-core / a-work", section="5, 8.4", severity="medium",
       freq="RUN-0074 C16=1; RUN-0076 C16=12.",
       sources=[e74("C16"), f"{PI76}:34"],
       cids=["C16"],
       cov={"a": ["generic", f"{MC}04-questions.md:104 «Дать варианты без подталкивания» (только вопросы); {MC}30-targeted-edit.md:103"],
            "b": ["absent", "—"],
            "c": ["generic", f"{CP}:56 CB-0.5"],
            "d": ["absent", "—"]},
       examples="Golden: GS-375-SOL-03 (negative), SOL-10 (positive «4 варианта размещения»).", guard="нет")

lesson(id="I-48", title="Дубли требований и UC",
       failure="4.3.2 ≈ 4.4.1, 4.5.1 ≈ 6.1.1; UC повторяет UC с другим актором.",
       rule="Проверка на полное и частичное дублирование до выдачи.",
       phase="a-core / a-work", section="3, 6, 7", severity="medium",
       freq="RUN-0016 (дефект 5).",
       sources=["runs/2026/RUN-0016/feedback/ba-review-notes.md:39"],
       cids=["C25", "C11"],
       cov={"a": ["generic", f"{MC}19-uc-coverage.md:134; {MC}23-constraints.md:132. В классах ФТ (16, 17) проверки дублей нет"],
            "b": ["generic", f"{ST}:93-98 (уникальность ID — не смысла)"],
            "c": ["explicit", "prompts/bcreq-uc-modeling-stepwise.md:86; prompts/bcreq-extra-risk-analysis-stepwise.md:59"],
            "d": ["explicit", f"{SEC}04-non-functional-requirements.md:77; {SEC}07-use-cases.md:41"]},
       examples="нет", guard=f"{V403}:129-140 (дубликат ID, не смысла)",
       old="prompts/archive/fr-validation-legacy.md:56 «Проверку на избыточность или полное или частичное дублирование требований»")

lesson(id="I-49", title="Закрытое или неполное перечисление без источника",
       failure="Каналы «ВКонтакте, Telegram и WhatsApp» без «Max»; закрытый перечень как факт.",
       rule="Перечень — только из источника с указанием полноты; иначе открытый и вопрос.",
       phase="a-in / a-core", section="2, 3", severity="medium",
       freq="RUN-0018 Г5; RUN-0021.",
       sources=["runs/2026/RUN-0018/feedback/review-notes.md:44"],
       cids=["C09"],
       cov={"a": ["generic", f"{MC}07-web-evidence.md:105 «Да/Нет/Частично только при прямом подтверждении»"],
            "b": ["absent", "—"], "c": ["absent", "не найдено"], "d": ["absent", "не найдено"]},
       examples="нет", guard="нет")

lesson(id="I-50", title="Пропуск обязательного содержания (2.4.1 документация/тестирование, исключения заказчика)",
       failure="В 2.4.1 нет документирования и вывода в эксплуатацию; исключения заказчика не попали в 2.4.2.",
       rule="2.4.1 включает документирование, тестирование, внедрение; исключения заказчика — в 2.4.2.",
       phase="a-in", section="2.4", severity="medium",
       freq="RUN-0074 C13=1; RUN-0073 C13=12; RUN-0076 C13=14 (13 повторов).",
       sources=[e74("C13"), f"{E73}:60", f"{PI76}:50"],
       cids=["C13"],
       cov={"a": ["explicit", f"{MC}15-business-context.md:101 «2.4.1 включает документирование, проверку, внедрение»"],
            "b": ["absent", "—"],
            "c": ["generic", "—"],
            "d": ["explicit", f"{SEC}02-business-context.md:37"]},
       examples="нет", guard="нет")

lesson(id="I-51", title="Сценарии и разделы — только по запросу БА; UC — внутренний материал",
       failure="UC и User Story генерируются без запроса и уходят заказчику.",
       rule="UC/US — только по явному запросу; внутренние UC не отправлять заказчику.",
       phase="a-core / a-release", section="7", severity="medium",
       freq="RUN-0074 section-prompts; Golden GS-375-DLG-09.",
       sources=[f"{SP74}:174"],
       cids=["C04", "C17"],
       cov={"a": ["explicit", f"{MC}README.md:171 «C37/C38 — только по запросу»; {MC}38-requested-uc.md:105; {MC}32-audience-projection.md:96"],
            "b": ["absent", "—"], "c": ["generic", "—"], "d": ["generic", "—"]},
       examples="нет", guard="нет")

lesson(id="I-52", title="Вторая роль модели — не независимая проверка",
       failure="Самопроверка той же моделью «другой ролью» объявлена PASS.",
       rule="Смена роли не создаёт независимого подтверждения; недоступный источник — unverifiable.",
       phase="a-work / a-release", section="—", severity="high",
       freq="Replay; RUN-0078 review-notes (тот же автор генерирует и проверяет).",
       sources=["runs/2026/RUN-0078/feedback/review-notes.md:12-14", f"{SP74}:218"],
       cids=["C10"],
       cov={"a": ["explicit", f"{MC}28-independent-review.md:105,147; {MC}16-fr-delta.md:127 «Смена роли не создаёт независимого подтверждения» {COMMON}"],
            "b": ["explicit", f"{ST}:150; {SG}:71-74"],
            "c": ["generic", f"{CP}:173 АП2"],
            "d": ["absent", "—"]},
       examples="Класс: 28-independent-review.md:147.", guard="нет")

lesson(id="I-53", title="Субъективное заявление заказчика — не дефект продукта",
       failure="Мнение заказчика задокументировано как дефект продукта.",
       rule="Субъективное заявление заказчика фиксируется как его позиция, не как дефект продукта.",
       phase="a-in", section="2.2", severity="medium",
       freq="RUN-0020 (правило принято в диалоге и «записано в память»).",
       sources=["runs/2026/RUN-0020/feedback/ba-review-notes.md:43"],
       cids=["C15"],
       cov={"a": ["absent", "поиск «субъективн» — 0"], "b": ["absent", "0"], "c": ["absent", "0"], "d": ["absent", "0"]},
       examples="нет", guard="нет",
       notes="Правило ни разу не попало в репозиторий — существовало только в «памяти» модели RUN-0020.")

lesson(id="I-54", title="Комментарий сотрудника не становится требованием заказчика",
       failure="«По комментарию коллеги …» превращено в обязательное ФТ; неточная формулировка коллеги принята как факт.",
       rule="Различать роли входов: запрос заказчика, анкета, комментарий сотрудника; комментарий — гипотеза.",
       phase="a-in", section="2, 3", severity="medium",
       freq="Golden GS-375-PRB-04 (C06), PRB-08 (C14).",
       sources=[f"{GS} GS-375-PRB-04, PRB-08"],
       cids=["C06", "C14"],
       cov={"a": ["explicit", f"{MC}01-intake.md:96 «Комментарий сотрудника не становится требованием заказчика», :138"],
            "b": ["absent", "—"], "c": ["absent", "не найдено"], "d": ["absent", "—"]},
       examples="Класс: 01-intake.md:138. Golden: GS-375-PRB-04, PRB-08.", guard="нет")

lesson(id="I-55", title="Неизвестное — UNKNOWN/[ТРЕБУЕТСЯ УТОЧНЕНИЕ], а не догадка",
       failure="Пробел закрыт правдоподобной догадкой; аудитор подтверждает без локатора.",
       rule="Неизвестное явно помечать и выносить в 8.4; аудитор пишет «не проверено», если нет локатора; «Нет данных» — допустимый ответ.",
       phase="все", section="все, 8.4", severity="critical",
       freq="RUN-0022 (аудитор и «не проверено»); RUN-0077 «Нет данных».",
       sources=["runs/2026/RUN-0022/feedback/ba-review-notes.md:33-36", "runs/2026/RUN-0077/feedback/review-notes.md:29"],
       cids=["C09"],
       cov={"a": ["explicit", f"{MC}16-fr-delta.md:134 «Все поля payload заполнены фактом либо явным UNKNOWN с вопросом» {COMMON}; {MC}07-web-evidence.md:105 «иначе UNKNOWN»"],
            "b": ["explicit", f"{ST}:27, :72"],
            "c": ["explicit", f"{CP}:115 Р2"],
            "d": ["explicit", f"{SEC}README.md:128 Р2; CB-1.3, CB-5.4"]},
       examples="нет", guard=f"{V403}:60-75 (RUN-0078 содержит not_verified — проверка наличия, не качества)")

# ---------------------------------------------------------------- derived
GROUPS = ["a", "b", "c", "d"]
for x in L:
    a = x["cov"]["a"][0]
    basis = []
    if x["cov"]["c"][0] == "explicit":
        basis.append("c")
    if x["cov"]["d"][0] == "explicit":
        basis.append("d")
    if x["old"]:
        basis.append("old")
    x["degraded"] = a in ("generic", "absent") and bool(basis)
    x["degraded_basis"] = basis if x["degraded"] else []

agg = {g: Counter(x["cov"][g][0] for x in L) for g in GROUPS}
inventory = {
    "issue": 411,
    "generated_by": "experiments/issue_411/research/build_lessons.py",
    "date": "2026-10-31",
    "baseline_commit": "34e07b06",
    "scope": {
        "a": "standards/bcreq-manual-classes/*.md (39) + catalog.json",
        "b": f"{ST} + {SG}",
        "c": "prompts/bcreq-*.md (14)",
        "d": "standards/bcreq-sections/*.md",
    },
    "levels": {"explicit": "есть конкретная строка, применимая там, где ошибка возникает",
               "generic": "только общая формулировка шаблона или строка в одном неподходящем классе",
               "absent": "не найдено поиском и чтением"},
    "aggregate": {g: dict(agg[g]) for g in GROUPS},
    "degraded_count": sum(x["degraded"] for x in L),
    "lessons": L,
}
(OUT / "lessons_inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")

# ---------------------------------------------------------------- markdown
SYM = {"explicit": "явно", "generic": "общо", "absent": "нет"}
md = []
w = md.append
w("# Issue #411: инвентарь уроков и их покрытие в ручном конвейере BCREQ")
w("")
w("Черновик исследования, 2026-10-31. Источник данных: "
  "[lessons_inventory.json](lessons_inventory.json), сборка — "
  "[build_lessons.py](build_lessons.py). Существующие файлы репозитория не изменялись.")
w("")
w("## Метод")
w("")
w("Уроки собраны из обратной связи БА (RUN-0016…RUN-0029, RUN-0077), "
  "реестров и статистики RUN-0073…RUN-0076, golden-кандидатов RUN-0074 и "
  "аналитических документов. Дубли между прогонами объединены.")
w("")
w("Покрытие проверено в четырёх группах:")
w("")
w("- **a** — 39 классовых стандартов `standards/bcreq-manual-classes/` и `catalog.json`;")
w("- **b** — `docs/contracts/bcreq-manual-state.md` и `bcreq-stage-gates.md`;")
w("- **c** — 14 промптов `prompts/bcreq-*.md`;")
w("- **d** — мета-стандарты разделов `standards/bcreq-sections/`.")
w("")
w("Уровни покрытия:")
w("")
w("- **явно** — есть конкретная строка; она приведена с `файл:строка`.")
w("- **общо** — правило покрыто только общей формулировкой шаблона, либо явная строка "
  "есть в одном классе, а ошибка возникает во многих.")
w("- **нет** — правило не найдено ни поиском, ни чтением.")
w("")
w("Метод — поиск по шаблонам и чтение класс-специфичных строк. Отдельные "
  "«нет» могут быть ложными: где это вероятно, в деталях стоит пометка *uncertain*.")
w("")
w("Все ссылки `файл:строка` даны по коммиту `34e07b06` (HEAD ветки issue-411). "
  "Во время анализа в рабочем дереве параллельно менялись 53 файла классов и "
  "промптов (+3949 строк, не закоммичено). Эти изменения здесь не оценивались, "
  "и после их фиксации номера строк могут сместиться.")
w("")
w("Номера C01…C25 в столбце «C-id» — категории инцидентов RUN-0074. "
  "У классов стандартов те же обозначения C01…C39, но это **другая** "
  "нумерация. Совпадение обозначений само по себе риск путаницы.")
w("")
w("## Ответы на два вопроса")
w("")
w("### Есть ли в классах исполняемый вставляемый текст промпта?")
w("")
w("**Частично, и не самостоятельный.**")
w("")
w("README классов заявляет: «Каждая запись — самостоятельный вставляемый промпт» "
  "(`standards/bcreq-manual-classes/README.md:59`). Фактически каждый файл "
  "(около 150 строк) устроен так:")
w("")
w("- около 95 % текста — общий шаблон, одинаковый во всех 39 классах: Вход/Выход JSON, "
  "контекст, 5 из 6 пунктов проверки, общие circuit breakers;")
w("- поведение, специфичное для класса, умещается в одну строку «Алгоритм, шаг 2», "
  "один «Специальный стоп», один пункт проверки и пару однострочных "
  "«Корректно:/Ошибка:».")
w("")
w("Чего в файлах нет:")
w("")
w("- роли и инструкции «что сделать», которую модель могла бы выполнить без "
  "дополнительных материалов;")
w("- формата текста раздела BCREQ;")
w("- стоп-слов КС/БС;")
w("- few-shot примеров с реальным текстом BCREQ.")
w("")
w("Чтобы класс работал, БА должен вставить вместе с ним:")
w("")
w("- контракт состояния (`bcreq-manual-state.md:18-23`);")
w("- мета-стандарты;")
w("- полный текст конституции.")
w("")
w("Сам класс говорит: «Скопировать контракт и этот стандарт, затем заполнить блок» "
  "(`16-fr-delta.md:27-29`). Явные правила против повторяющихся ошибок "
  "(АД-1…АД-11, Р1-Р7, КС/БС) остаются в Промпте 0 "
  "(`prompts/bcreq-constitution-governance-oneshot.md:110-166`). В классах они "
  "не повторены, а их доставка зависит от ручной сборки bundle (класс C36).")
w("")
w("### Ссылаются ли классы на уроки прогонов или категории инцидентов?")
w("")
w("**Нет.**")
w("")
w("- Поиск `RUN-0|SC-[0-9]|АД-[0-9]|инцидент|golden|GS-3` по "
  "`standards/bcreq-manual-classes/*.md` и `catalog.json` даёт 0 совпадений.")
w("- Раздел «Основания» каждого класса ссылается только на checkpoint, RFC и README разделов.")
w("- 46 golden-кандидатов RUN-0074 (`runs/2026/RUN-0074/outputs/golden-set-candidates.json`, "
  "из них 37 negative с defect_class) не подключены ни к одному классу, "
  "контракту или мета-стандарту.")
w("")
w("Для сравнения:")
w("")
w("- Промпт 0 явно трассирует АД-1…АД-7 к категориям RUN-0075 "
  "(`prompts/bcreq-constitution-governance-oneshot.md:131-146`).")
w("- RFC ручного конвейера упоминает RUN-0074 лишь как основу имитации RUN-0078 "
  "(`docs/rfc/2026-10-bcreq-manual-pipeline.md:125,171`).")
w("- RUN-0078 — авторская имитация: «тот же автор генерирует и проверяет, "
  "исходные Qwen-модели не перезапускались» (`runs/2026/RUN-0078/feedback/review-notes.md:12-14`).")
w("")
w("### Автоматические проверки")
w("")
w("`scripts/validate_issue_403_manual_pipeline.py:18-49` проверяет у классов "
  "только структуру:")
w("")
w("- 39 записей;")
w("- 8 заголовков;")
w("- 2 JSON-примера;")
w("- соответствие каталогу.")
w("")
w("Поведенческие тесты `check_replay` (`:105-183`) касаются JSON-состояния:")
w("")
w("- tombstone требует полномочий;")
w("- release — только человеком;")
w("- двухфакторная апелляция;")
w("- чужая задача отклоняется.")
w("")
w("Тест `:155-160` прямо фиксирует: структурная проверка **не обнаруживает** "
  "инверсию смысла. Проверка обязательных строк для промптов (c) есть "
  "(`scripts/test_issue_395_bcreq.py:31-49`), для 39 классов аналога нет. "
  "Регрессионного прогона классов на golden-наборе нет.")
w("")
w("## Сводные показатели")
w("")
w(f"Всего уроков: **{len(L)}**. Деградировавших (явно в старых промптах, документах или "
  f"мета-стандартах, но «общо» или «нет» в 39 классах): **{inventory['degraded_count']}**.")
w("")
w("| Группа | явно | общо | нет |")
w("| --- | ---: | ---: | ---: |")
names = {"a": "a — 39 классов + catalog", "b": "b — контракты state / gates",
         "c": "c — 14 промптов bcreq-*", "d": "d — мета-стандарты разделов"}
for g in GROUPS:
    w(f"| {names[g]} | {agg[g]['explicit']} | {agg[g]['generic']} | {agg[g]['absent']} |")
w("")
crit = [x for x in L if x["severity"] == "critical"]
ca = Counter(x["cov"]["a"][0] for x in crit)
w(f"Из {len(crit)} критичных уроков в группе a: явно — {ca['explicit']}, общо — "
  f"{ca['generic']}, нет — {ca['absent']}.")
w("")
w("Явное покрытие не гарантирует исполнения. В RUN-0076 правила C01, C09 и C12 "
  "существовали, но дали 16, 45 и 37 повторов после замечания БА "
  "(`runs/2026/RUN-0076/outputs/prompt-improvements.md:40-50`). Там же рекомендовано "
  "«дублировать правило в промпт каждого раздела и в чек-лист самопроверки». "
  "В 39 классах это не сделано: класс-специфичный пункт проверки один, остальные общие.")
w("")
w("## Сводная таблица")
w("")
w("| ID | Урок | Тяжесть | C-id RUN-0074 | a | b | c | d | Пример | Автопроверка | DEGRADED |")
w("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
for x in L:
    ex = "нет" if x["examples"].strip() == "нет" else ("класс" if x["examples"].startswith("Класс") else ("golden" if "Golden" in x["examples"] else "есть"))
    if x["examples"].startswith("Класс") and "Golden" in x["examples"]:
        ex = "класс + golden"
    gd = "нет" if x["guard"].startswith("нет") else "частично"
    cells = " | ".join(SYM[x["cov"][g][0]] for g in GROUPS)
    w(f"| {x['id']} | {x['title']} | {x['severity']} | {', '.join(x['cids']) or '—'} | {cells} | {ex} | {gd} | {'**да**' if x['degraded'] else '—'} |")
w("")
w("«Пример»:")
w("")
w("- «класс» — однострочный «Корректно:/Ошибка:» в стандарте класса;")
w("- «golden» — кейс в `golden-set-candidates.json` RUN-0074, к классам не подключённый.")
w("")
w("«Автопроверка = частично»: проверка относится к JSON-состоянию, к промптам (c) "
  "или к отчётам KB, а не к тексту, который генерирует класс.")
w("")
w("## DEGRADED: явно было раньше, в 39 классах — общо или нет")
w("")
w("| ID | Урок | a | Где было явно |")
w("| --- | --- | --- | --- |")
for x in L:
    if x["degraded"]:
        where = []
        if "c" in x["degraded_basis"]:
            where.append("c: " + x["cov"]["c"][1])
        if "d" in x["degraded_basis"]:
            where.append("d: " + x["cov"]["d"][1])
        if x["old"]:
            where.append("старое: " + x["old"])
        w(f"| {x['id']} | {x['title']} | {SYM[x['cov']['a'][0]]} | {'<br>'.join(where)} |")
w("")
w("Отдельно — уроки без нормы нигде (a-d = нет или общо, старого явного правила нет):")
w("")
for x in L:
    if not x["degraded"] and all(x["cov"][g][0] != "explicit" for g in GROUPS):
        w(f"- {x['id']} {x['title']}.")
w("")
w("## Детали по урокам")
for x in L:
    w("")
    w(f"### {x['id']}. {x['title']}")
    w("")
    w(f"- **Ошибка:** {x['failure']}")
    w(f"- **Правило БА:** {x['rule']}")
    w(f"- **Фаза / раздел:** {x['phase']} / {x['section']}")
    w(f"- **Тяжесть:** {x['severity']}")
    w(f"- **Частота:** {x['freq']}")
    w(f"- **C-id RUN-0074:** {', '.join(x['cids']) or '—'}")
    w("- **Источники:**")
    for s in x["sources"]:
        w(f"  - `{s}`")
    for g in GROUPS:
        lvl, ev = x["cov"][g]
        w(f"- **{g} — {SYM[lvl]}:** {ev}")
    w(f"- **Примеры:** {x['examples']}")
    w(f"- **Автопроверка:** {x['guard']}")
    if x["degraded"]:
        w(f"- **DEGRADED:** да (основание: {', '.join(x['degraded_basis'])})")
    if x["old"]:
        w(f"- **Старое явное правило:** {x['old']}")
    if x["notes"]:
        w(f"- **Примечание (uncertain):** {x['notes']}")
(OUT / "lessons_coverage.md").write_text("\n".join(md) + "\n")
print(len(L), {g: dict(agg[g]) for g in GROUPS}, "degraded", inventory["degraded_count"])
