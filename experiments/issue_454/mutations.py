#!/usr/bin/env python3
"""Мутации: каждая должна ронять валидатор issue #454; файл восстанавливается."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RFC = "docs/rfc/2026-11-bcreq-prompts-publication-roadmap.md"
B = "pr-ops/BACKLOG.md"
M = [(B, "| BL-232 | [Публикация сайта на прод и приёмка](backlog-repository.md#bl-232-публикация-сайта-на-прод-и-приёмка) | P0 | — | TODO |", "| BL-232 | [Публикация сайта на прод и приёмка](backlog-repository.md#bl-232-публикация-сайта-на-прод-и-приёмка) | P0 | — | DONE |"),
     (B, "BL-156г — `DONE`", "BL-156г — `review`"),
     (B, "**Движение по цепочке (на 2026-11-05, issue #454).**", "**Цепочка.**"),
     (B, "| Текущий — закрывается |", "| Текущий |", -1),
     (B, "| Р-15, Р-19; этап BL-157в — BL-111, BL-232 |", "| Р-15; этап BL-157в — BL-111 |"),
     (B, "BL-231, BL-232, BL-233", "BL-231, BL-233"),
     (RFC, "| ЧАСТИЧНО | исполнитель |", "| DONE | исполнитель |"),
     (RFC, "| DONE, DONE |", "| DONE |"),
     (RFC, "| Ш-Р | `bcreq-release-readiness-oneshot` | by-test | нет |", "| Ш-Х | `bcreq-release-readiness-oneshot` | by-test | нет |"),
     (RFC, "| Ш-В | `bcreq-review-validation-oneshot` | published | 0.3 |", "| Ш-В | `bcreq-review-validation-oneshot` | published | 0.2 |"),
     (RFC, "| Ш-0 | `bcreq-constitution-governance-oneshot` | by-test |", "| Ш-0 | `bcreq-constitution-governance-oneshot` | published |"),
     (RFC, "**Пробел П-6**, задачи нет", "задачи нет"),
     (RFC, "#bl-232-публикация-сайта-на-прод-и-приёмка)", "#bl-232-деплой)"),
     (RFC, "**4 из 13**", "**13 из 13**", -1),
     (RFC, "| 7.11 |", "| 8.11 |", -1),
     (RFC, "(BL-232), повторить аудит", ", повторить аудит"),
     (RFC, "| DEC-454-03 |", "| DEC-454-30 |"),
     ("site/data/test-kit.json", '"step": "Ш-Р', '"step": "Ш-Х'),
     ("docs/rfc/rfc-register.md", "| [RFC-PUB-001](2026-11-bcreq-prompts-publication-roadmap.md) |", "| RFC-PUB-001 |"),
     ("pr-ops/artifact-map.md", "`/docs/rfc/2026-11-bcreq-prompts-publication-roadmap.md`", "`/docs/rfc/other.md`"),
     ("docs/rfc/2026-11-runtime-product-catalog-golden-set.md", "## 17. Поправка 0.8", "## 17. Поправка"),
     (RFC, "| DEC-454-07 |", "| DEC-454-70 |"),
     (RFC, "**не доказано: BL-172, пакеты правит БА**", "доказано"),
     ("runs/2026/RUN-0092/outputs/summary.json", '"R4": {\n    "passed": true', '"R4": {\n    "passed": false'),
     (RFC, "| A-WORK | Ш-6", "| A-W | Ш-6"),
     (RFC, "Отдельных промптов гейтов нет", "Промпты гейтов есть", -1),
     (RFC, "| 6 Особенности реализации |", "| Особенности реализации |"),
     (RFC, "| **Итого** | 8 из 8 | **41** |", "| **Итого** | 8 из 8 | **42** |"),
     (RFC, "| 5 Описание решения | [`05-solution-description`](../../standards/bcreq-sections/05-solution-description.md) | 6 |", "| 5 Описание решения | [`05-solution-description`](../../standards/bcreq-sections/05-solution-description.md) | 5 |"),
     (RFC, "У гейта «Выпуск» нет критериев", "У гейта «Выпуск» есть критерии"),
     (RFC, "Сайт сам не движется", "Сайт движется"),
     (RFC, "Однозначной готовности нет", "Сайт готов"),
     (RFC, "**заблокировано: нужен БА**", "доказано"),
     (B, "| **Р-20** |", "| Р-20 |"),
     ("experiments/issue_454/kit_vs_machine_base.json", '"prod_kit": "0.6"', '"prod_kit": "0.7"'),
     (RFC, "различаются [9 из 12]", "различаются [3 из 12]", -1),
     (RFC, "различаются Ш-2…Ш-9 и Ш-Р, 9 шагов из 12", "различаются Ш-2…Ш-9 и Ш-Р, 3 шага из 12"),
     ("docs/rfc/2026-11-bcreq-machine-run-baseline.md", "9 шагах из 12", "3 шагах из 12"),
     ("docs/rfc/2026-11-bcreq-machine-run-baseline.md", "**не читая** RUN-0090", "RUN-0090"),
     (RFC, "| DEC-454-09 |", "| DEC-454-90 |"),
     (RFC, "не читая RUN-0090 и RUN-0091", "читая RUN-0090 и RUN-0091"),
     (RFC, "прогон не считается независимым", "прогон считается независимым"),
     (RFC, "доказано с ограничением, не приёмка", "доказано"),
     (RFC, "**не доказано: BL-157в**", "доказано"),
     (RFC, "**не доказано: BL-173, BL-170**", "доказано"),
     (RFC, "`contact-center` не проверен. `analytics-reporting`: RUN-0091", "все классы проверены. `analytics-reporting`: RUN-0091"),
     (RFC, "По Р-МР-4 кандидаты", "Кандидаты"),
     (B, "Кандидаты BL-171 сюда не входят", "Кандидаты входят"),
     (B, "DEC-454-05…09", "DEC-454-05…08"),
     (B, "`review` → `DONE` (PR #459 слит)", "`review`"),
     (B, "создаёт владелец, Р-МР-2", "создаст исполнитель"),
     ("experiments/issue_454/audit_flow_coverage.json", '"steps_current": 4', '"steps_current": 5')]
bad = 0
for path, a, b, *count in M:
    f = ROOT / path; src = f.read_text(encoding="utf-8")
    assert a in src, (path, a)
    f.write_text(src.replace(a, b, *(count or [1])), encoding="utf-8")
    try:
        rc = subprocess.run([sys.executable, str(ROOT / "scripts/validate_issue_454_publication_roadmap.py")], capture_output=True).returncode
    finally:
        f.write_text(src, encoding="utf-8")
    print("caught" if rc else "MISSED", path, a[:40].replace("\n", " ")); bad += not rc
print(f"мутаций: {len(M)}, пропущено: {bad}")
raise SystemExit(bad)
