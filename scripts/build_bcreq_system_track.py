#!/usr/bin/env python3
"""Системный формат шагов Ш-А, Ш-1, Ш-2 из архива сайта 2.7.0 (issue #490).

Issue #490, п. 2.2: вернуть прежние не декомпозированные (системные) промпты
Ш-ХХ «как и было» — параллельно декомпозированным AIN-01…24, а не вместо них.
Источник — полные неизменённые файлы ``prompts/archive/a-in-v2.7.0`` (их SHA
закреплены в ``manifest.json`` архива). Сборщик:

* берёт текст шага архивного файла (до архивного блока «по тесту») без
  изменений, кроме точечных правок: параметр «режим» в «Состоянии BCREQ»
  заменён на «формат шагов=системный», ссылка на вынесенную из Хаба
  метамодель закреплена по SHA (#488), кейс-лексика заменена принципом
  (``CASE_EDITS``, issue #495);
* вместо архивного блока «по тесту» ставит блок «Стандарты шага» из текущих
  стандартов — тот же, что у черновиков Ш-ХХ (``build_bcreq_step_prompts``);
* добавляет в начало раздел «Системный формат шагов» — что это за формат и
  какие защиты #474 (доказательная нормализация, вопросы Заказчику, нет
  согласия без проверки) действуют поверх текста 2.7.0;
* добавляет в конец блок «Итог шага» из SSOT ``bcreq-step-handoff.md``;
* пропускает тело через ``prompt_purity.project``: в промпте нет ссылок на
  приватный репозиторий и HTML-комментариев (стандарт чистоты, issue #495).

Архив 2.7.0 — историческая сущность (комментарий 2 владельца к issue #495,
п. 14): стандарт чистоты применяется к нему только в части ссылок, а очищенный
текст для исполнения собирает этот сборщик.

Результат — ``prompts/drafts/system/*-system.md``. ``--check`` сверяет файлы,
ничего не записывая. LLM не вызывается.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bcreq_handoff  # noqa: E402
import bcreq_fragments as fragments  # noqa: E402
import build_bcreq_step_prompts as steps_builder  # noqa: E402
from build_bcreq_step_prompts import HUB_FLOATING, HUB_PINNED  # noqa: E402
from prompt_purity import project  # noqa: E402

ARCHIVE = ROOT / "prompts/archive/a-in-v2.7.0"
OUT = ROOT / "prompts/drafts/system"
DATE = "2026-11-26"
NORMALIZATION = ROOT / "docs/ba-processes/bcreq-evidence-normalization.md"
#: Границы раздела системного формата в промпте: заголовок и строка перед
#: текстом 2.7.0 (HTML-комментарии в промпте запрещены, issue #495).
BEGIN = "## Системный формат шагов"
END = "Ниже — текст шага редакции 2.7.0."
#: Начало архивного блока «по тесту» — его заменяет блок «Стандарты шага».
ARCHIVE_BLOCK = "\n## Дополнение «по тесту» (BL-156): стандарты шага\n"
#: Баннер архивной редакции — служебная история сборки, в промпт не идёт.
BANNER = re.compile(r"^> \*\*Редакция по тесту \(#427\): действует до ADR обратного согласования\.\*\*[^\n]*\n\n", re.M)
#: Кейс-лексика архивного текста → принцип (реестр замен PR #497, ID в скобках).
#: Шаг → [(было, стало, сколько раз)].
CASE_EDITS = {
    "Ш-А": [  # U-18, U-19; A-07 — те же три фразы, что в INTAKE_BODY черновика шага
        ("3. Сколько номеров Mango ВАТС?", "3. Сколько номеров телефонии продукта?", 1),
        ("- номера ВАТС: <…|UNKNOWN>", "- номера телефонии продукта: <…|UNKNOWN>", 1),
        ("до разбора запроса. У него нет\nпромпта v0.1: текст шага собран из контракта операции К-01 и правил\n"
         "справочника стандартов.",
         "до разбора запроса:\nконтракт операции К-01 и правила выбора стандартов (раздел 4В ниже).", 1),
        ("Конституция —\nПромпт 0;\nв чат её не выводи.",
         "Конституция — Промпт 0 (Ш-0), принятый в этом чате; в чат её не выводи.", 1),
        ("**В. Согласие со стандартами** (подробно — в\nсправочнике стандартов):",
         "**В. Согласие со стандартами** (варианты по умолчанию):", 1),
    ],
    "Ш-2": [  # U-11, U-13
        ("передачу этих функций через коннектор.", "передачу этих функций через интеграцию.", 1),
        ("4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари\n"
         "   профилей задействованных продуктов (ЛК — D1, D2, D11; ВАТС — D5, D6;\n"
         "   КЦ — D6, D11; РА — D11, D3; API — D8; оператор связи — D9).",
         "4. **Набор словарей.** Возьми минимальный набор D1, D2, D11 и словари\n"
         "   профилей задействованных продуктов из справочника профилей продуктов\n"
         "   runtime (И-11). Справочника нет во входе — назови пробел ACCESS_GAP,\n"
         "   возьми минимальный набор D1, D2, D11 и отметь `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`.", 1),
    ],
}

#: шаг → (архивный файл, файл системного формата, название, что добавляет блок)
STEPS = {
    "Ш-А": ("bcreq-intake-questionnaire-stepwise", "bcreq-intake-questionnaire-system",
            "анкета и согласие со стандартами",
            "Анкету заполняй только сведениями из переданного пакета БА; неизвестное — "
            "`UNKNOWN`, пропуск не означает нулевые величины. Выбор стандартов — решение БА."),
    "Ш-1": ("bcreq-context-understanding-stepwise", "bcreq-context-understanding-system",
            "контекст, глоссарий",
            "Разделы 1 и 2 пиши только после того, как БА явно принял факты, "
            "неоднозначности и вердикт исполнимости (подшаги до разделов). До решения "
            "БА — только эти подшаги; черновик раздела 2 «на всякий случай» не выводи."),
    "Ш-2": ("bcreq-products-impact-analysis-stepwise", "bcreq-products-impact-analysis-system",
            "продукты, стейкхолдеры",
            "Гейт Г-IN решает БА явным ответом. Без записи решения в журнале гейтов "
            "и 8.5 Ш-3 не запускается; молчание и «продолжай» без решения — не решение."),
}


def normalization():
    return fragments.access()


def system_block(step, title, extra):
    return f"""{BEGIN}

Это системный (комплексный) шаг {step} «{title}» — текст редакции сайта 2.7.0,
восстановленный параллельно декомпозированным шагам AIN-01…24.
БА выбрал системный формат на сайте: не предлагай
другой формат и не переводи работу на AIN-шаги без явной просьбы БА.
При конфликте с текстом шага ниже действует этот раздел.

- {extra}
- Вопросы к Заказчику — нумерованным списком, без таблицы; адресат — Заказчик,
  БА — куратор, а не адресат. Неоднозначность не выдавай за факт: «Неясно: …»
  и вопрос Заказчику.
- Темп задаёт БА: список вопросов Заказчику выводи, когда БА перешёл к
  вопросам (принял факты и неоднозначности или попросил вопросы). В ответе
  вопросы идут перед блоком «На согласование БА».
- Вопрос Заказчику — коротко и по существу: одно бизнес-решение на пункт,
  нейтральный тон, без объяснения Заказчику его же процесса.
- Если Заказчик пишет «как» (экран, кнопка, механизм, сленг), сохрани его
  слова цитатой, а требование запиши как «что» нормативным термином продукта
  или отрасли; сленг в требования не переноси.
- Не соглашайся с БА без проверки: на возражение БА сначала сверь источник,
  затем прими правку или покажи цитату, которая ей противоречит.
- Положения для явного решения БА дублируй человекочитаемым блоком
  «На согласование БА» (см. «Итог шага» в конце); техническая разметка остаётся.

{normalization()}

{fragments.decisions()}

{fragments.output()}

{END}

"""


def build_one(step, ctx):
    src_name, out_name, title, extra = STEPS[step]
    src = ARCHIVE / f"{src_name}.md"
    original = src.read_text(encoding="utf-8")
    _, fm, body = original.split("---", 2)
    lines = fm.strip("\n").splitlines()
    keep = []
    for line in lines:
        key = line.split(":", 1)[0]
        if key == "id":
            line = f"id: mango-bcreq-{out_name.removeprefix('bcreq-')}"
        elif key == "title":
            line = line.replace("(по тесту)", "(системный формат)")
        elif key == "updated":
            line = f"updated: {DATE}"
        elif key == "version":
            line = f"version: {fragments.VERSION}"
        elif key in ("mode", "based_on", "based_on_sha256", "assembled_by", "runtime_sha"):
            continue
        keep.append(line)
    keep += [
        "track: system",
        f"steps: [{step}]" if not any(l.startswith("steps:") for l in keep) else None,
        f"based_on: {src.relative_to(ROOT)}",
        f"based_on_sha256: {hashlib.sha256(original.encode('utf-8')).hexdigest()}",
        "assembled_by: scripts/build_bcreq_system_track.py",
    ]
    fm_text = "\n".join(l for l in keep if l)
    if body.count(ARCHIVE_BLOCK) != 1:
        raise SystemExit(f"{src.name}: нет архивного блока «по тесту»")
    body = body.split(ARCHIVE_BLOCK, 1)[0]
    body, banners = BANNER.subn("", body.lstrip("\n"), count=1)
    if banners != 1:
        raise SystemExit(f"{src.name}: нет баннера архивной редакции")
    for old, new, count in [("- параметры: режим=<…>;", "- параметры: формат шагов=системный;", None),
                            (HUB_FLOATING, HUB_PINNED, None)] + CASE_EDITS.get(step, []):
        if count is not None and body.count(old) != count:
            raise SystemExit(f"{src.name}: «{old[:40]}» встречается {body.count(old)} раз, ожидалось {count}")
        body = body.replace(old, new)
    # Заголовок шага (первая строка «# …») остаётся первым; раздел формата — сразу за ним.
    title_line, rest = body.split("\n", 1)
    if not title_line.startswith("# "):
        raise SystemExit(f"{src.name}: текст шага не начинается с заголовка «# …»")
    block = steps_builder.render_block([step], ctx)[0]
    text = (title_line + "\n\n" + system_block(step, title, extra) + rest.strip("\n")
            + "\n\n" + block.rstrip("\n") + "\n\n" + bcreq_handoff.render([step]))
    return OUT / f"{out_name}.md", f"---\n{fm_text}\n---\n\n" + project(text)


def build():
    ctx = steps_builder.context()
    return dict(build_one(step, ctx) for step in STEPS)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--check", action="store_true", help="сверить файлы, не записывая")
    args = parser.parse_args(argv)
    outputs = build()
    stale = [str(p.relative_to(ROOT)) for p, t in outputs.items()
             if not p.exists() or p.read_text(encoding="utf-8") != t]
    extra = sorted(str(p.relative_to(ROOT)) for p in OUT.glob("*.md") if p not in outputs) if OUT.exists() else []
    if args.check:
        if stale or extra:
            print("устарели: " + ", ".join(stale + extra))
            return 1
        print(f"OK: системный формат — {len(outputs)} промпта совпадают с архивом 2.7.0 и SSOT")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    print(f"записано: {len(outputs)} промпта системного формата в {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
