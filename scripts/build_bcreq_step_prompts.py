#!/usr/bin/env python3
"""Сборщик промптов шагов потока BCREQ «по тесту» (BL-156, issue #438).

Порядок сборки — RFC #427, раздел 9.3:

1. текст промпта v0.1 шага (``prompts/<файл>.md``) — без изменений, кроме
   ссылок на runtime ``blob/main`` → ``blob/<SHA реестра>`` (ТС-1, раздел 7
   реестра справочников: «Промпты шагов BL-156 собираются уже со ссылками на
   срез раздела 1»);
2. блок базового стандарта — правила БС, кроме расходящихся с текстом v0.1
   (``EXCLUDED_BASE``; каждое — строка отчёта «расхождения»);
3. MUST-правила профилей шага по таблице «Шаги и профили» стандарта профилей
   (для Ш-В — ANALYZE, VERIFY, TRANSFORM, поручение issue #438);
4. контракты операций шага из ``catalog.json``: вход, выход, специальный
   стоп, специальные проверки;
5. ссылки И-N по SHA из реестра справочников, строка ТС-6 дословно,
   текст чтения каталога (М-4, раздел 2.2 реестра) для шагов с И-2 и
   заглушки раздела 4 реестра там, где справочника нет (после BL-156а,
   issue #444, активна одна З-2).

Источники читаются из файлов репозитория при каждом запуске; ни одно
правило не пишется в сборщике руками. Руками заданы только решения сборки:
таблица исключений (с причинами), соответствие терминов, примечания к шагам
и текст заглушки Ш-Р (пилот, RFC, раздел 9.2). Все они попадают в манифест.

Запуск::

    python3 scripts/build_bcreq_step_prompts.py          # записать черновики
    python3 scripts/build_bcreq_step_prompts.py --check  # сверить без записи

Выход: ``prompts/drafts/*.md`` (11 файлов шагов и заглушка Ш-Р) и
``prompts/drafts/manifest.json``. Блоки уроков (``--apply-prompts``) сборщик
не добавляет: они ждут ADR-017.
"""

import argparse
import hashlib
import json
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "standards/bcreq-prompt-base-standard.md"
PROFILES = ROOT / "standards/bcreq-prompt-profiles.md"
CATALOG = ROOT / "standards/bcreq-manual-classes/catalog.json"
REGISTRY = ROOT / "standards/bcreq-runtime-references.md"
RFC = ROOT / "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
PROMPTS = ROOT / "prompts"
DRAFTS = PROMPTS / "drafts"
MANIFEST = DRAFTS / "manifest.json"

REPO_BLOB = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"
RUNTIME_MAIN = "github.com/G-Ivan-A/mango-ba-ai-runtime/blob/main/"
BUILD_DATE = "2026-11-04"
#: Правки после RUN-0089: дата только у изменённых файлов, остальные черновики не меняются ни на байт.
FIX_DATE = "2026-11-05"
#: Гейты, решение которых принимает человек и записывает К-34 (стандарт гейтов, Г3).
#: Г-W здесь нет: черновик Ш-В — измеренный RUN-0081 текст, шаг идёт по `prompts/`, запись задаёт его карточка.
RECORDED_GATES = {"Г-IN", "Г-С1", "Выпуск"}
GATE_RECORD = [
    "**Запись решения гейта (К-34, RUN-0089, P05).** Когда человек решил, добавь запись в 8.5",
    "и покажи её в ответе одной строкой: `gate_id`; `gate_type`; решение; кто решил; причина.",
    "У гейта типа `гибрид` добавь `model_recommendation` и `divergence` (да или нет). Запись без типа",
    "гейта, а у гибрида без расхождения, неполна. Источник — стандарт гейтов, правило Г3:",
    f"[`docs/contracts/bcreq-stage-gates.md`]({REPO_BLOB}docs/contracts/bcreq-stage-gates.md).",
    "",
]
ROUTE = ["Ш-0", "Ш-1", "Ш-2", "Ш-3", "Ш-4", "Ш-5", "Ш-6", "Ш-7", "Ш-8", "Ш-9", "Ш-В", "Ш-Р", "Ш-С"]
RELEASE_FILE = "bcreq-release-readiness-oneshot"
BEGIN = "<!-- bl-156: by-test -->"
END = "<!-- /bl-156: by-test -->"
# Маркер черновика по временному workflow промптов (CONTRIBUTING.md, шаг 3).
EXPERIMENTAL = "<!-- Experimental: for BL-156 https://github.com/G-Ivan-A/mango_ba_prompts/issues/438, no formal research yet -->\n"
MODE_LINE = "Редакция по тесту (#427): действует до ADR обратного согласования."

# Правила базового стандарта, которые расходятся с текстом v0.1 (RFC, 9.3, п. 6;
# базовый стандарт, раздел 2: «его НЕ ДОЛЖНО вносить молча»). Решаются по golden
# set и в ADR BL-158; до тех пор действует текст v0.1.
EXCLUDED_BASE = {
    "БС-01": "v0.1 берёт вход из блока «Состояние BCREQ» без полей task/phase/class/revision/rule_bundle и режимов START/CONTINUE; правило остановило бы каждый вызов v0.1 (WAITING) из-за отсутствующих полей",
    "БС-04": "в v0.1 нет режима CONTINUE с base и slices: шаг получает документ и «Состояние BCREQ» целиком",
    "БС-07": "v0.1 задаёт свой «Формат вывода» и блок «Состояние BCREQ»; один блок `BCREQ_OUTPUT` заменил бы формат, который проверен прогонами и RUN-0079",
    "БС-09": "SLICE и FULL — типы результата `BCREQ_OUTPUT` (БС-07); в v0.1 их нет, сборку фазы выполняет Ш-Р",
    "БС-11": "«поле payload» — часть `BCREQ_OUTPUT` (БС-07); в v0.1 то же требование записано как «[ТРЕБУЕТСЯ УТОЧНЕНИЕ] и вопрос в 8.4»",
    "БС-13": "v0.1 рекомендует следующий шаг маршрута (Ш-N) и оставляет выбор БА; правило требует следующую операцию (К-NN) — другая единица маршрута",
}

# Соответствие терминов стандартов и текста v0.1: не новое правило, а словарь,
# чтобы правила стандартов не вводили второй маркер рядом с маркером v0.1.
TERMS = [
    ("UNKNOWN", "`[ТРЕБУЕТСЯ УТОЧНЕНИЕ]` с вопросом в 8.4 (маркер v0.1)"),
    ("WAITING, BLOCKED, INCOMPLETE", "остановка по CB с перечнем недостающего; статус — в строке «текущий» блока «Состояние BCREQ»"),
    ("receipt", "блок «Проверки (receipt)» после блока «Состояние BCREQ»: выполненные проверки, прочитанные и непрочитанные источники, ограничения, расхождения с блоком «по тесту»"),
    ("операция К-NN", "часть шага; контракт операции — ниже, раздел «Контракты операций»"),
]

# Примечания к шагам: где профиль из таблицы «Шаги и профили» встречается с
# прямым запретом текста v0.1, примечание называет, к чему правило относится.
NOTES = {
    "Ш-В": [
        "Профиль TRANSFORM в этом шаге относится к варианту исправления в замечании "
        "(операция К-30 — адресная правка): документ ты не меняешь — текст v0.1, "
        "раздел 4: «Не меняй текст документа» (АД-2). `before` — цитата из документа, "
        "`after` — вариант, semantic_diff — смысл правки.",
    ],
    "Ш-0": [
        "Профиль RECORD (К-34) записывает только явный ответ БА; на шаге Ш-0 "
        "это параметры и правила, которые БА подтвердил, а не согласие по умолчанию.",
    ],
}

RELEASE_BODY = """
# BCREQ Ш-Р. Выпуск: заглушка шага (пилот)

Шаг Ш-Р — заглушка выпуска (пилот): у него нет промпта v0.1
([RFC #427, раздел 9.2](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-bcreq-flow-processes-prompts.md#92-состав)).
Текст шага ниже собран из контрактов операций К-31, К-12, К-33, К-32, К-35 и
гейта «Выпуск»; сверх них — только правила пакетов раздела 4 (BL-123, RUN-0089, P16).
Отдельный вызов, новая сессия.

## 0. Позиция

- **Пройдено:** Ш-0…Ш-9, Ш-В; гейт Г-W — решение людей гейта, записанное
  в 8.5 (К-34). Нет записи — шаг не начинается: молчание не согласие.
- **Текущий:** Ш-Р, выпуск документа BCREQ (стадия выпуска, ПБ-7).
- **Рекомендуемый следующий:** решение человека на гейте «Выпуск» (тип
  `человек`, ключевой). Модель выпуск и отправку не объявляет.

## 1. Роль

Ты — аналитик, который готовит выпускной комплект и отчёт для человека.
Ты не выпускаешь, не отправляешь и не одобряешь.

## 2. Вход и остановки

**Вход:** согласованный кандидат документа BCREQ и его ревизия; блок
«Состояние BCREQ»; записи решений 8.5 (К-34); политика адресатов.

**Остановки:** специальные стопы операций — раздел «Контракты операций»
ниже.

## 3. Шаги

1. **К-31.** Структурная сверка документа: отчёт соответствия.
2. **К-12.** Полная сборка: каждый живой ID с полным текстом.
3. **К-33.** Контроль выпускного комплекта: отчёт о готовности к выпуску
   человеком.
4. **К-32.** Пакеты адресатам по разделу 4: только draft-пакеты, пока нет
   решения человека на гейте «Выпуск» (`человек`).
5. **К-35.** Кандидат baseline: состав версии и открытые вопросы; статус
   `released` — только по записи выпуска человеком.

## 4. Пакеты К-32

**Состав.** Его задаёт политика адресатов. Если БА её не приложил, действует
политика по умолчанию:

| Пакет | Состав |
| --- | --- |
| «ФТ на согласование» | разделы 1, 2.1–2.4, 3, 4 |
| «ТЗ в договор» | разделы 1, 2.1–2.4, 3, 4, 6; сквозная нумерация; номер документа — заполнитель `<номер ТЗ>`; раздел 5 — только если политика включает его явно |
| Внутренний | документ целиком, без очистки |

**Очистка пакетов «ФТ на согласование» и «ТЗ в договор».** Пакет идёт полным
текстом, без рассуждений и служебного слоя. Убери из него:

- маркеры вида `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`, `[ТРЕБУЕТСЯ …]`;
- ссылки на вопросы и решения (`В-NN`, `Р-NN`) и на разделы вне пакета;
- строки статуса разделов и блок «Состояние BCREQ»;
- столбцы и пометки источника, если таблица без них остаётся понятной.

**Смысл не меняй.** Убирай пометку, а не факт; новых формулировок не добавляй.
Пункт, который без маркера теряет смысл или утверждает непроверенное, в пакет
не включай.

**Манифест пакета.** Под каждым пакетом перечисли:

- `Исключено`: разделы и столбцы вне состава;
- `Открытые пункты`: каждый убранный маркер и невключённый пункт с локатором
  в документе и номером вопроса;
- `Готов к отправке`: `да`, только если открытых пунктов нет; иначе `нет`.
  Статус пакета `draft` не меняется в обоих случаях: отправку решает человек.

Служебные обозначения разрешены только в манифесте, он не входит в текст пакета.

## 5. Формат вывода

```text
Ш-Р. Выпускной комплект BCREQ <ID задачи>, ревизия <N>
Отчёт К-31: <пропуски, дубликаты, битые ссылки, порядок разделов, счётчики, вердикт>
Отчёт К-33: <ревизии, одобрения, недостающее, устаревшее, готово к выпуску человеком: да/нет>
Пакеты К-32: <полный текст каждого пакета, под ним манифест: исключено, открытые пункты, готов к отправке> — статус draft
Baseline К-35: <кандидат; released — только по записи выпуска>
Решение по гейту «Выпуск» (`человек`, ключевой): за людьми гейта.
```

## 6. Состояние BCREQ

```text
Состояние BCREQ
- задача: <ID и название>
- пройдено: …; Ш-Р — комплект собран
- гейты: Г-IN — <решение>; Г-С1 — <решение>; Г-W — <решение>; Выпуск — ожидает решения
- текущий: Ш-Р
- рекомендуемый следующий: <гейт «Выпуск» | возврат: стадия · шаг>
- открытые вопросы: 8.4 — <N> (<M> блокируют)
```
"""


def read(path):
    return path.read_text(encoding="utf-8")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def absolutize(text, source):
    """Относительные ссылки стандарта → ссылки от корня репозитория на GitHub.

    Правило переносится дословно, но лежит в другом каталоге: ссылка
    ``bcreq-runtime-references.md#…`` из ``standards/`` в ``prompts/drafts/``
    сломалась бы.
    """
    base = posixpath.dirname(rel(source))

    def repl(match):
        target = match.group(1)
        if re.match(r"^(https?:|#|mailto:)", target):
            return match.group(0)
        return "](" + REPO_BLOB + posixpath.normpath(posixpath.join(base, target)) + ")"

    return re.sub(r"\]\(([^)\s]+)\)", repl, text)


def frontmatter_value(body, key):
    match = re.search(rf"(?m)^{key}:\s*\"?([^\"\n]+)\"?\s*$", body.split("\n---\n", 1)[0])
    return match.group(1).strip() if match else None


def split_frontmatter(body):
    match = re.match(r"^---\n(.*?)\n---\n", body, re.S)
    if not match:
        raise SystemExit("нет frontmatter")
    return match.group(1), body[match.end():]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split(" | ")]


def section(body, heading):
    start = body.index(heading)
    level = len(heading) - len(heading.lstrip("#"))
    rest = body[start + len(heading):]
    stop = re.search(rf"(?m)^#{{1,{level}}} ", rest)
    return rest[: stop.start()] if stop else rest


# --- Источники -------------------------------------------------------------

def load_base():
    body = read(BASE)
    groups, current = [], None
    for line in section(body, "## 3. Правила").splitlines():
        heading = re.match(r"^### 3\.\d+\. (.+)$", line)
        if heading:
            current = (heading.group(1), [])
            groups.append(current)
        rule = re.match(r"^\| (БС-\d\d) \| (.+) \| (.+) \|$", line)
        if rule:
            current[1].append((rule.group(1), absolutize(rule.group(2), BASE)))
    gates = []
    for line in section(body, "## 4. Типы гейтов базового стандарта").splitlines():
        if line.startswith("| ") and not line.startswith(("| Гейт", "| ---")):
            gates.append(dict(zip(("gate", "where", "type", "key", "model", "source"), cells(absolutize(line, BASE)))))
    return frontmatter_value(body, "version"), groups, gates


def load_profiles():
    body = read(PROFILES)
    rules, current = {}, None
    for line in section(body, "## 2. Профили").splitlines():
        heading = re.match(r"^### 2\.\d+\. ([A-Z]+) — (.+)$", line)
        if heading:
            current = heading.group(1)
            rules[current] = {"title": heading.group(2), "rules": []}
        rule = re.match(r"^\| ([A-Z]{2}-\d\d) \| (.+?) \| .+ \|$", line)
        if rule and current:
            rules[current]["rules"].append((rule.group(1), absolutize(rule.group(2), PROFILES)))
    steps = {}
    table = body.split("Шаги и профили (выведено из таблицы выше):", 1)[1]
    for line in table.splitlines():
        row = re.match(r"^\| (Ш-.) \| ([A-Z, ]+) \| (.+) \|$", line)
        if row:
            steps[row.group(1)] = {
                "profiles": [p.strip() for p in row.group(2).split(",")],
                "operations": [o.strip() for o in row.group(3).split(",")],
            }
        elif steps and not line.startswith("|"):
            break
    return frontmatter_value(body, "version"), rules, steps


def load_rfc_steps():
    rows = {}
    for line in section(read(RFC), "### 9.2. Состав").splitlines():
        row = re.match(r"^\| (Ш-.) \| ([^|]+) \| ([^|]+) \|", line)
        if row:
            name = re.search(r"`([a-z0-9-]+)`", row.group(3))
            rows[row.group(1)] = {
                "processes": [p.strip() for p in row.group(2).split(",")],
                "file": name.group(1) if name else RELEASE_FILE,
                "run": (re.search(r"прогон: (\d)", row.group(3)) or [None, None])[1],
            }
    return rows


def load_registry():
    body = read(REGISTRY)
    sha = frontmatter_value(body, "runtime_sha")
    refs = []
    for line in section(body, "## 2. Перечень").splitlines():
        if re.match(r"^\| И-\d+ \|", line):
            c = cells(line)
            refs.append({"id": c[0], "name": c[1], "link": c[2], "status": c[3], "include": c[4], "steps": c[5]})
    stubs_section = section(body, "## 4. Заглушки")
    stub_block = re.search(r"```text\n(.*?)\n```", stubs_section, re.S).group(1)
    stubs = []
    for line in stubs_section.splitlines():
        if re.match(r"^\| З-\d \|", line):
            c = cells(line)
            if len(c) < 6:  # таблица снятых заглушек (BL-163): id, справочник, строка, снята, почему
                continue
            stubs.append({"id": c[0], "ref": c[1].split()[0], "condition": absolutize(c[2], REGISTRY), "steps": c[3], "name": c[4].strip("`"), "task": c[5]})
    ts6 = re.search(r"```text\n(.*?)\n```", section(body, "## 5. Строка для промпта (ТС-6)"), re.S).group(1)
    ts6 = ts6.replace("<SHA из раздела 1>", f"`{sha}`")
    # М-4 (RFC-RT-001, раздел 4): как промпт шага читает каталог; раздел 2.2 реестра.
    m4 = re.search(r"```text\n(.*?)\n```", section(body, "### 2.2. Как промпт шага читает каталог (М-4)"), re.S).group(1)
    m4 = m4.replace("<SHA реестра>", sha)
    return frontmatter_value(body, "version"), sha, refs, stub_block, stubs, ts6, m4


def steps_of(cell):
    if cell.strip() == "все шаги":
        return set(ROUTE)
    return {s.strip() for s in cell.split(",")}


# --- Сборка -----------------------------------------------------------------

def gates_for(step, gates, rfc):
    """Гейт относится к последнему шагу маршрута своего процесса ПБ-N."""
    result = []
    for gate in gates:
        where = gate["where"]
        if where.startswith("Каждая операция"):
            result.append(gate)
            continue
        named = set(re.findall(r"Ш-.", where))
        processes = re.findall(r"ПБ-\d", where)
        owners = [s for s in ROUTE if s in rfc and set(rfc[s]["processes"]) & set(processes)]
        if step in named or (owners and owners[-1] == step):
            result.append(gate)
    return result


def closes_human_gate(steps, gates, rfc):
    return any(g["gate"] in RECORDED_GATES for step in steps for g in gates_for(step, gates, rfc))


def render_block(steps, ctx):
    base_version, groups, gates = ctx["base"]
    prof_version, prules, ptable = ctx["profiles"]
    reg_version, sha, refs, stub_block, stubs, ts6, m4 = ctx["registry"]
    catalog = ctx["catalog"]
    rfc = ctx["rfc"]
    out = [BEGIN, "## Дополнение «по тесту» (BL-156): стандарты шага", ""]
    out += [f"> **{MODE_LINE}**", ""]
    out += [
        "Блок собран сборщиком `scripts/build_bcreq_step_prompts.py` по",
        f"[RFC #427, раздел 9.3]({REPO_BLOB}docs/rfc/2026-11-bcreq-flow-processes-prompts.md#93-как-промпт-собирается-из-стандартов)",
        f"из [базового стандарта]({REPO_BLOB}standards/bcreq-prompt-base-standard.md) {base_version},",
        f"[профилей]({REPO_BLOB}standards/bcreq-prompt-profiles.md) {prof_version},",
        f"[каталога операций]({REPO_BLOB}standards/bcreq-manual-classes/catalog.json) и",
        f"[реестра справочников runtime]({REPO_BLOB}standards/bcreq-runtime-references.md) {reg_version}.",
        "Правила перенесены дословно с номером; источник правила — в стандарте.",
        "",
        "**Приоритет.** Где правило ниже расходится с текстом шага выше",
        "(v0.1), действует текст v0.1; расхождение запиши в receipt.",
        "",
        "**Как читать.** «Промпт ДОЛЖЕН …» читай как «ты ДОЛЖЕН …». Термины",
        "стандартов в этом шаге пишутся так:",
        "",
    ]
    out += [f"- {term} → {meaning};" for term, meaning in TERMS[:-1]]
    out += [f"- {TERMS[-1][0]} → {TERMS[-1][1]}.", ""]

    # Шаг, профили, операции.
    profiles, operations = [], []
    for step in steps:
        for p in ptable[step]["profiles"]:
            if p not in profiles:
                profiles.append(p)
        operations += [(step, op) for op in ptable[step]["operations"]]
    out += ["### Шаг", ""]
    for step in steps:
        run = rfc[step]["run"]
        label = f"{step} (прогон: {run})" if run else step
        out.append(
            f"- **{label}**, процесс {', '.join(rfc[step]['processes'])}: профили "
            f"{', '.join(ptable[step]['profiles'])}; операции {', '.join(ptable[step]['operations'])}."
        )
    for step in steps:
        for note in NOTES.get(step, []):
            out += ["", note]
    out.append("")

    # Гейты.
    out += [
        "### Гейты шага",
        "",
        "Тип гейта — по базовому стандарту, раздел 4 (этап 1). Гейт типа `человек`",
        "или `гибрид` проходит только человек; без записи решения (К-34) он не пройден.",
        "",
        "| Шаг | Гейт | Тип (этап 1) | Ключевой | Что делает модель |",
        "| --- | --- | --- | --- | --- |",
    ]
    for step in steps:
        for gate in gates_for(step, gates, rfc):
            out.append(f"| {step} | {gate['gate']} | {gate['type']} | {gate['key']} | {gate['model']} |")
    out.append("")
    if closes_human_gate(steps, gates, rfc):
        out += GATE_RECORD

    # Базовый стандарт.
    out += ["### Базовый стандарт", ""]
    for title, rules in groups:
        kept = [(rid, text) for rid, text in rules if rid not in EXCLUDED_BASE]
        if not kept:
            continue
        out += [f"#### {title}", ""]
        out += [f"- **{rid}.** {text}" for rid, text in kept]
        out.append("")
    out += [
        "Не внесены, потому что расходятся с текстом v0.1 (отчёт BL-156): "
        + ", ".join(EXCLUDED_BASE) + ". Для них действует текст v0.1.",
        "",
    ]

    # Профили.
    for p in profiles:
        out += [f"### Профиль {p} — {prules[p]['title']}", ""]
        out += [f"- **{rid}.** {text}" for rid, text in prules[p]["rules"]]
        out.append("")

    # Контракты операций.
    out += ["### Контракты операций", ""]
    by_id = {c["id"]: c for c in catalog["classes"]}
    for step, op in operations:
        c = by_id[op]
        prefix = f"{step} · " if len(steps) > 1 else ""
        out += [
            f"#### {prefix}{c['id']} {c['name']}",
            "",
            f"- Вход: `{c['inputs']}`",
            f"- Выход: `{c['outputs']}`",
            f"- Специальный стоп: {c['stop']}",
            f"- Специальные проверки: {c['checks']}",
            "",
        ]

    # Справочники runtime.
    out += ["### Справочники runtime", "", ts6, ""]
    used_refs = [r for r in refs if steps_of(r["steps"]) & set(steps) if r["steps"] != "—"]
    for r in used_refs:
        link = r["link"] if "](" in r["link"] else "нет в срезе"
        out.append(f"- **{r['id']} {r['name']}:** {link}.")
    out.append("")
    if any(r["id"] == "И-2" for r in used_refs):
        out += ["Как читать каталог (реестр, раздел 2.2; RFC-RT-001, звено М-4):", "", "```text", m4, "```", ""]
    used_stubs = [s for s in stubs if steps_of(s["steps"]) & set(steps)]
    if used_stubs:
        out += ["Заглушки справочников (реестр, раздел 4): заглушка — известный пробел, а не дефект.", ""]
        for s in used_stubs:
            out += [f"{s['id']} — условие: {s['condition']}.", "", "```text"]
            out.append(stub_block.replace("<имя>", s["name"]))
            out += ["```", ""]
    out.append(END)
    return "\n".join(out) + "\n", profiles, [op for _, op in operations], used_refs, used_stubs


def build_frontmatter(original_fm, file_id_suffix, extra, updated=BUILD_DATE):
    lines = []
    for line in original_fm.splitlines():
        key = line.split(":", 1)[0]
        if key == "id":
            line = f"{line}-by-test"
        elif key == "title":
            line = re.sub(r'"$', ' (по тесту)"', line)
        elif key == "status":
            line = "status: draft"
        elif key == "updated":
            line = f"updated: {updated}"
        lines.append(line)
    lines += extra
    return "---\n" + "\n".join(lines) + "\n---\n"


def build_all():
    ctx = {
        "base": load_base(),
        "profiles": load_profiles(),
        "registry": load_registry(),
        "catalog": json.loads(read(CATALOG)),
        "rfc": load_rfc_steps(),
    }
    sha = ctx["registry"][1]
    files = {}
    for step in ROUTE:
        name = ctx["rfc"][step]["file"]
        files.setdefault(name, []).append(step)
    outputs, manifest = {}, []
    for name, steps in files.items():
        block, profiles, operations, refs, stubs = render_block(steps, ctx)
        extra = [
            "mode: by-test",
            f"steps: [{', '.join(steps)}]",
            f"runtime_sha: {sha}",
            "assembled_by: scripts/build_bcreq_step_prompts.py",
        ]
        header = f"\n> **{MODE_LINE}** Черновик BL-156 (issue #438): "
        if name == RELEASE_FILE:
            # Суффиксы «-by-test» и «(по тесту)» добавляет build_frontmatter
            # (до issue #446 они удваивались у заглушки).
            fm = "\n".join([
                f"id: mango-{RELEASE_FILE}",
                'title: "BCREQ Ш-Р: выпуск, заглушка"',
                "status: draft",
                "version: 0.2",
                f"updated: {FIX_DATE}",
                "temperature: 0.1",
                "operation: release_readiness",
                'processes: ["Выпуск BCREQ"]',
            ])
            v01, body, substitutions, based_on = None, RELEASE_BODY, 0, []
            header += "шаг без промпта v0.1 — заглушка выпуска (пилот, RFC #427, раздел 9.2); блок «по тесту» — в конце файла.\n"
        else:
            source = PROMPTS / f"{name}.md"
            v01 = read(source)
            fm, body = split_frontmatter(v01)
            substitutions = body.count(RUNTIME_MAIN)
            body = body.replace(RUNTIME_MAIN, RUNTIME_MAIN.replace("/main/", f"/{sha}/"))
            based_on = [
                f"based_on: prompts/{name}.md",
                f"based_on_sha256: {hashlib.sha256(v01.encode('utf-8')).hexdigest()}",
            ]
            # После BL-156а (issue #444) ссылки v0.1 уже закреплены по SHA: подстановок нет.
            header += (
                "текст шага v0.1 ниже не изменён, кроме ссылок на runtime по SHA "
                "реестра; блок «по тесту» — в конце файла.\n"
                if substitutions else
                "текст шага v0.1 ниже не изменён; блок «по тесту» — в конце файла.\n"
            )
        updated = FIX_DATE if closes_human_gate(steps, ctx["base"][2], ctx["rfc"]) else BUILD_DATE
        text = build_frontmatter(fm, "-by-test", based_on + extra, updated) + EXPERIMENTAL + header + body.rstrip("\n") + "\n\n" + block
        outputs[DRAFTS / f"{name}.md"] = text
        manifest.append({
            "file": f"prompts/drafts/{name}.md",
            "steps": steps,
            "based_on": f"prompts/{name}.md" if v01 else None,
            "based_on_sha256": hashlib.sha256(v01.encode("utf-8")).hexdigest() if v01 else None,
            "runtime_main_to_sha": substitutions,
            "profiles": profiles,
            "operations": operations,
            "runtime_refs": [r["id"] for r in refs],
            "stubs": [s["id"] for s in stubs],
            "gates": [g["gate"] for s in steps for g in gates_for(s, ctx["base"][2], ctx["rfc"])],
            "excluded_base_rules": sorted(EXCLUDED_BASE),
        })
    outputs[MANIFEST] = json.dumps({
        "source_issue": "https://github.com/G-Ivan-A/mango_ba_prompts/issues/438",
        "task": "BL-156",
        "build_date": BUILD_DATE,
        "runtime_sha": sha,
        "standards": {
            "base": f"standards/bcreq-prompt-base-standard.md@{ctx['base'][0]}",
            "profiles": f"standards/bcreq-prompt-profiles.md@{ctx['profiles'][0]}",
            "runtime_references": f"standards/bcreq-runtime-references.md@{ctx['registry'][0]}",
            "catalog": f"standards/bcreq-manual-classes/catalog.json@{ctx['catalog']['version']}",
        },
        "excluded_base_rules": EXCLUDED_BASE,
        "terms": dict(TERMS),
        "notes": NOTES,
        "lessons_blocks": "не добавлены: ждут ADR-017 (--apply-prompts)",
        "drafts": manifest,
    }, ensure_ascii=False, indent=2) + "\n"
    return outputs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true", help="сверить черновики с выходом сборщика, не записывая")
    args = parser.parse_args(argv)
    outputs = build_all()
    stale = [rel(p) for p, text in outputs.items() if not p.exists() or read(p) != text]
    extra = sorted(
        rel(p) for p in DRAFTS.glob("*") if p.is_file() and p not in outputs
    ) if DRAFTS.exists() else []
    if args.check:
        for path in stale:
            print(f"устарел или отсутствует: {path}")
        for path in extra:
            print(f"лишний файл в prompts/drafts/: {path}")
        if stale or extra:
            return 1
        print(f"OK: {len(outputs) - 1} черновиков и манифест совпадают с выходом сборщика")
        return 0
    DRAFTS.mkdir(parents=True, exist_ok=True)
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    print(f"записано: {len(outputs) - 1} черновиков и манифест; изменено {len(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
