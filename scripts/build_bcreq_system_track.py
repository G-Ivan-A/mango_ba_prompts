#!/usr/bin/env python3
"""Системный формат шагов Ш-А, Ш-1, Ш-2 из архива сайта 2.7.0 (issue #490).

Issue #490, п. 2.2: вернуть прежние не декомпозированные (системные) промпты
Ш-ХХ «как и было» — параллельно декомпозированным AIN-01…24, а не вместо них.
Источник — полные неизменённые файлы ``prompts/archive/a-in-v2.7.0`` (их SHA
закреплены в ``manifest.json`` архива). Сборщик:

* копирует тело архивного файла без изменений, кроме трёх точечных правок:
  ссылки «Промпт 0» ведут на черновик Ш-0 с выбором формата шагов, параметр
  «режим» в «Состоянии BCREQ» заменён на «формат шагов=системный», баннер
  «действует до ADR» помечен как история;
* добавляет в начало блок ``issue-490:system`` — что это за формат и какие
  защиты #474 (доказательная нормализация, вопросы Заказчику, нет согласия
  без проверки) действуют поверх текста 2.7.0;
* добавляет в конец блок «Итог шага» из SSOT ``bcreq-step-handoff.md``.

Результат — ``prompts/drafts/system/*-system.md``. ``--check`` сверяет файлы,
ничего не записывая. LLM не вызывается.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bcreq_handoff  # noqa: E402

ARCHIVE = ROOT / "prompts/archive/a-in-v2.7.0"
OUT = ROOT / "prompts/drafts/system"
DATE = "2026-11-18"
ISSUE = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/490"
BLOB = "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/"
PUBLISHED_P0 = BLOB + "prompts/bcreq-constitution-governance-oneshot.md"
DRAFT_P0 = BLOB + "prompts/drafts/bcreq-constitution-governance-oneshot.md"
NORMALIZATION = ROOT / "docs/ba-processes/bcreq-evidence-normalization.md"
BEGIN, END = "<!-- issue-490:system -->", "<!-- /issue-490:system -->"
BANNER_OLD = "> **Редакция по тесту (#427): действует до ADR обратного согласования.**"
BANNER_NEW = ("> **Системный формат шагов (#490): текст редакции сайта 2.7.0.** "
              "История баннера: «Редакция по тесту (#427): действует до ADR обратного согласования».")

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
    return NORMALIZATION.read_text(encoding="utf-8").split("---", 2)[2].strip()


def system_block(step, title, extra):
    return f"""{BEGIN}
## Системный формат шагов (#490)

Это системный (комплексный) шаг {step} «{title}» — текст редакции сайта 2.7.0,
восстановленный параллельно декомпозированным шагам AIN-01…24
([issue #490]({ISSUE})). БА выбрал системный формат на сайте: не предлагай
другой формат и не переводи работу на AIN-шаги без явной просьбы БА. Ниже —
текст 2.7.0 без изменений, кроме ссылок на Промпт 0 и параметра «формат шагов».
При конфликте с текстом ниже действует этот блок.

- {extra}
- Вопросы к Заказчику — нумерованным списком, без таблицы; адресат — Заказчик,
  БА — куратор, а не адресат. Неоднозначность не выдавай за факт: «Неясно: …»
  и вопрос Заказчику.
- Не соглашайся с БА без проверки: на возражение БА сначала сверь источник,
  затем прими правку или покажи цитату, которая ей противоречит.
- Положения для явного решения БА дублируй человекочитаемым блоком
  «На согласование БА» (см. «Итог шага» в конце); техническая разметка остаётся.

{normalization()}
{END}

"""


def build_one(step):
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
    # Баннер меняем только в шапке; копия в блоке «по тесту» — история BL-156.
    for old, new, limit in [(PUBLISHED_P0, DRAFT_P0, -1), (BANNER_OLD, BANNER_NEW, 1),
                            ("- параметры: режим=<…>;", "- параметры: формат шагов=системный;", -1)]:
        if old == BANNER_OLD and old not in body:
            raise SystemExit(f"{src.name}: нет баннера «{old[:40]}»")
        body = body.replace(old, new, limit)
    experimental, rest = body.lstrip("\n").split("\n", 1)
    if not experimental.startswith("<!-- Experimental:"):
        raise SystemExit(f"{src.name}: нет строки Experimental после frontmatter")
    head, tail = rest.split("\n\n", 2)[0:2], rest.split("\n\n", 2)[2]
    text = (f"---\n{fm_text}\n---\n"
            f"<!-- Experimental: for {ISSUE}, no formal research yet -->\n"
            + "\n\n".join(head) + "\n\n" + system_block(step, title, extra) + tail.rstrip("\n")
            + "\n\n" + bcreq_handoff.render([step]))
    return OUT / f"{out_name}.md", text


def build():
    return dict(build_one(step) for step in STEPS)


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
