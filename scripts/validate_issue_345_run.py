#!/usr/bin/env python3
"""Regression checks for issue #345 / RUN-0064."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0064"


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_markers(text: str, markers: tuple[str, ...], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label} missing marker: {marker}")


def main() -> int:
    errors: list[str] = []

    for directory in ("inputs", "outputs", "feedback", "logs", "reports"):
        path = RUN / directory
        if not path.is_dir():
            errors.append(f"missing directory: {path.relative_to(ROOT)}")

    metadata = read(RUN / "metadata.yaml", errors)
    inputs = read(RUN / "inputs/README.md", errors)
    report = read(RUN / "reports/error-analysis.md", errors)
    requirements = read(RUN / "outputs/functional-requirements.md", errors)
    output_index = read(RUN / "outputs/README.md", errors)
    trace = read(RUN / "logs/traceability-and-gates.md", errors)
    review = read(RUN / "feedback/review-notes.md", errors)
    registry = read(ROOT / "runs/README.md", errors)
    changelog = read(ROOT / "CHANGELOG.md", errors)

    require_markers(
        metadata,
        (
            "run_id: RUN-0064",
            "run_type: execution",
            "https://github.com/G-Ivan-A/mango_ba_prompts/issues/345",
            "reports/error-analysis.md",
            "outputs/functional-requirements.md",
            "logs/traceability-and-gates.md",
        ),
        "metadata",
        errors,
    )
    require_markers(
        inputs,
        ("1074.json", "752b2c97-5a1f-423f-a551-70616719295e", "90c018d6-fad1-425c-871f-78618e3cba94", "не коммит"),
        "input manifest",
        errors,
    )

    categories = (
        "Нарушение контракта",
        "Отсутствие контракта",
        "Неоднозначность промпта",
        "Техническое ограничение",
    )
    require_markers(
        report,
        categories
        + (
            "Первопричина",
            "Рекомендации",
            "текстовая матрица состояний и взаимодействий",
            "CBAP",
            "eTOM",
        ),
        "error analysis",
        errors,
    )
    if len(re.findall(r"^\| ERR-\d{2} \|", report, flags=re.MULTILINE)) < 6:
        errors.append("error analysis must classify at least six concrete errors")

    headings = re.findall(r"^## (\d+)\. ", requirements, flags=re.MULTILINE)
    if headings != [str(i) for i in range(1, 7)]:
        errors.append("requirements must contain exactly six numbered sections")

    fr_ids = set(re.findall(r"^### (FR-\d{2})\. ", requirements, flags=re.MULTILINE))
    expected_fr_ids = {"FR-01", "FR-02", "FR-03"}
    if fr_ids != expected_fr_ids:
        errors.append(f"requirements must define {sorted(expected_fr_ids)}")
    for fr_id in sorted(expected_fr_ids):
        match = re.search(
            rf"^### {fr_id}\..*?(?=^### FR-\d{{2}}\.|^## 5\.)",
            requirements,
            flags=re.MULTILINE | re.DOTALL,
        )
        detail = match.group(0) if match else ""
        require_markers(
            detail,
            ("**Источник", "**Бизнес-цель", "**Критерии приемки", "**CBAP/eTOM"),
            fr_id,
            errors,
        )

    require_markers(
        requirements,
        (
            "классический вид",
            "новый вид",
            "шестерен",
            "чекбокс",
            "множествен",
            "Drag-and-Drop",
            "порядок колонок",
            "сессии",
            "профил",
            "Дата и время звонка",
            "Номер, инициировавший звонок",
            "Номер абонента",
            "Название услуги",
            "Оператор связи",
            "Длительность звонка",
            "Сумма в рублях",
            "Номер договора",
            "Скачать: CSV",
            "CSV-выгрузка не меняет состав и порядок данных",
            "логическому И",
            "Fulfillment",
            "Assurance",
        ),
        "requirements",
        errors,
    )
    if "FR-04" in requirements or "FR-05" in requirements or "FR-06" in requirements:
        errors.append("requirements must not retain the obsolete RUN-0063 FR-04..FR-06 model")

    require_markers(output_index, ("functional-requirements.md", "error-analysis.md"), "output index", errors)
    require_markers(trace, ("GATE-01", "GATE-02", "GATE-03", "GATE-04", "GATE-05", "PASS"), "gate log", errors)
    require_markers(review, ("Фокус human review", "Открытые решения", "Механизм проверки"), "review notes", errors)
    if "RUN-0064" not in registry or "Issue #345" not in changelog or "RUN-0064" not in changelog:
        errors.append("RUN-0064 must be registered in runs/README.md and CHANGELOG.md")

    if errors:
        print("Issue #345 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #345 validation passed: RUN-0064 satisfies the executable contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
