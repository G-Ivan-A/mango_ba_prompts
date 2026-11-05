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
     (B, "| Текущий — закрывается | Роадмэп", "| Текущий | Роадмэп"),
     (B, "| Р-15, Р-19; этап BL-157в — BL-111, BL-232 |", "| Р-15; этап BL-157в — BL-111 |"),
     (B, "BL-230, BL-231, BL-232 `DONE`", "BL-230, BL-231 `DONE`"),
     (RFC, "| ЧАСТИЧНО | исполнитель |", "| DONE | исполнитель |"),
     (RFC, "| DONE, DONE |", "| DONE |"),
     (RFC, "| Ш-Р | `bcreq-release-readiness-oneshot` | by-test | нет | нет | нет | заглушка шага | BL-232, затем BL-170 |\n", ""),
     (RFC, "| Ш-В | `bcreq-review-validation-oneshot` | published | 0.3 |", "| Ш-В | `bcreq-review-validation-oneshot` | published | 0.2 |"),
     (RFC, "| Ш-0 | `bcreq-constitution-governance-oneshot` | by-test |", "| Ш-0 | `bcreq-constitution-governance-oneshot` | published |"),
     (RFC, "**Пробел П-6**, задачи нет", "задачи нет"),
     (RFC, "#bl-232-публикация-сайта-на-прод-и-приёмка) (был", "#bl-232-деплой) (был"),
     (RFC, "**0 из 13**", "**13 из 13**"),
     (RFC, "| 7.11 |", "| 8.11 |", -1),
     (RFC, "проверка пароля в чистой вкладке (BL-232)", "проверка пароля в чистой вкладке"),
     (RFC, "| DEC-454-03 |", "| DEC-454-30 |"),
     ("site/data/test-kit.json", '"step": "Ш-Р', '"step": "Ш-Х'),
     ("docs/rfc/rfc-register.md", "| [RFC-PUB-001](2026-11-bcreq-prompts-publication-roadmap.md) |", "| RFC-PUB-001 |"),
     ("pr-ops/artifact-map.md", "`/docs/rfc/2026-11-bcreq-prompts-publication-roadmap.md`", "`/docs/rfc/other.md`"),
     ("docs/rfc/2026-11-runtime-product-catalog-golden-set.md", "## 17. Поправка 0.8", "## 17. Поправка"),
     ("experiments/issue_454/audit_flow_coverage.json", '"steps_current": 0', '"steps_current": 5')]
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
