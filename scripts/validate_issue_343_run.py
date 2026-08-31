#!/usr/bin/env python3
"""Regression checks for issue #343 / RUN-0063."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/2026/RUN-0063"
REPORT = RUN / "outputs/functional-requirements-bcreq-1074.md"


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    for directory in ("inputs", "outputs", "logs", "feedback"):
        path = RUN / directory
        if not path.is_dir():
            errors.append(f"missing directory: {path.relative_to(ROOT)}")

    metadata = read(RUN / "metadata.yaml", errors)
    report = read(REPORT, errors)
    gate_log = read(RUN / "logs/source-and-gate-log.md", errors)
    review = read(RUN / "feedback/review-notes.md", errors)
    readme = read(ROOT / "runs/README.md", errors)
    changelog = read(ROOT / "CHANGELOG.md", errors)

    for marker in (
        "run_id: RUN-0063",
        "run_type: execution",
        "https://github.com/G-Ivan-A/mango_ba_prompts/issues/343",
        "outputs/functional-requirements-bcreq-1074.md",
        "logs/source-and-gate-log.md",
        "feedback/review-notes.md",
    ):
        if marker not in metadata:
            errors.append(f"metadata missing marker: {marker}")

    headings = re.findall(r"^## (\d+)\. (.+)$", report, flags=re.MULTILINE)
    if [number for number, _ in headings] != [str(i) for i in range(1, 7)]:
        errors.append("report must contain exactly six numbered top-level sections")

    fr_summary = set(re.findall(r"^### (FR-\d{2})\.", report, flags=re.MULTILINE))
    fr_details = set(re.findall(r"^#### (FR-\d{2})\.", report, flags=re.MULTILINE))
    if not fr_summary:
        errors.append("section 3 must define upper-level FR-XX requirements")
    if fr_summary != fr_details:
        errors.append("every upper-level FR-XX must have one detailed requirement")

    for fr_id in sorted(fr_details):
        detail_match = re.search(
            rf"^#### {fr_id}\..*?(?=^#### FR-\d{{2}}\.|^## 5\.)",
            report,
            flags=re.MULTILINE | re.DOTALL,
        )
        detail = detail_match.group(0) if detail_match else ""
        for marker in ("**Источник:", "**Статус:", "**Критерии приемки:"):
            if marker not in detail:
                errors.append(f"{fr_id} missing {marker}")

    for required in (
        "Номер, инициировавший звонок",
        "Номер абонента",
        "Оператор связи",
        "Длительность звонка",
        "Сумма в рублях",
        "Номер договора",
        "Название услуги",
        "без агрегированного отчета по всем ЛС",
        "Не заполняется в рамках issue #343",
        "Вопросы Заказчику",
        "Вопросы владельцу продукта",
    ):
        if required not in report:
            errors.append(f"report missing requirement: {required}")

    gate_ids = set(re.findall(r"^## GATE-(\d{2})", gate_log, flags=re.MULTILINE))
    if gate_ids != {f"{i:02d}" for i in range(1, 7)}:
        errors.append("source log must record uninterrupted GATE-01 through GATE-06")
    for marker in ("Подтверждено", "Гипотеза", "Открытый вопрос", "Вердикт"):
        if marker not in gate_log:
            errors.append(f"gate log missing classification marker: {marker}")

    for marker in ("Вопросы Заказчику", "Вопросы владельцу продукта", "Фокус human review"):
        if marker not in review:
            errors.append(f"review notes missing section: {marker}")

    if "RUN-0063" not in readme:
        errors.append("runs/README.md does not register RUN-0063")
    if "Issue #343" not in changelog or "RUN-0063" not in changelog:
        errors.append("CHANGELOG.md does not register issue #343 and RUN-0063")

    if errors:
        print("Issue #343 validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Issue #343 validation passed: RUN-0063 satisfies the executable contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
