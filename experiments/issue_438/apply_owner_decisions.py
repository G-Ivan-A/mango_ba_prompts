"""Apply owner decisions from PR #439 comment 6630337995 (one-off edit script)."""
import re
from pathlib import Path
C = "https://github.com/G-Ivan-A/mango_ba_prompts/pull/439#issuecomment-6630337995"
def edit(path, *pairs, count=1):
    p = Path(path); s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in s, (path, old[:60]); s = s.replace(old, new, count)
    p.write_text(s, encoding="utf-8")
def resub(path, pat, repl, flags=re.M):
    p = Path(path); s = p.read_text(encoding="utf-8"); s2, n = re.subn(pat, repl, s, flags=flags)
    assert n, (path, pat); p.write_text(s2, encoding="utf-8")

RFC = "docs/rfc/2026-11-bcreq-flow-processes-prompts.md"
OLD_A, NEW_A = "поправка-06-промпты-шагов-проект-ждёт-р-15-issue-438", "поправка-06-промпты-шагов-принята-р-15-issue-438"
for f in (RFC, "docs/analysis/2026-11-04-bl-156-157-readiness-check.md"):
    edit(f, (OLD_A, NEW_A))
edit(RFC,
 ("version: 0.5.1\n", "version: 0.6\n"),
 ("Р-15 ждёт ответа владельца: проект записи — [поправка 0.6](#" + NEW_A + ").",
  f"Р-15 принято ([комментарий к PR #439]({C})) — [поправка 0.6](#{NEW_A})."),
 ("| DEC-427-04. Основная линия этапа 1 — шаги v0.1 | `proposed` | ждёт Р-15 |",
  f"| DEC-427-04. Основная линия этапа 1 — шаги v0.1 | `accepted` | Р-15 ([PR #439]({C})) |"),
 ("| DEC-427-12. Раздел «Процессы» в форме до 2.0.0 | `proposed` | ждёт Р-15 |",
  f"| DEC-427-12. Раздел «Процессы» в форме до 2.0.0 | `accepted` | Р-15 ([PR #439]({C})) |"),
 ("### Поправка 0.6: промпты шагов (проект, ждёт Р-15; issue #438)\n\n**Статус поправки: проект.** Версия RFC остаётся 0.5.1, DEC-427-04 и\nDEC-427-12 — `proposed`, пока владелец не ответит «Р-15 да» (или выберет\nдругой вариант) одной строкой по правилу\n[решений владельца](../../pr-ops/backlog-instruction.md#решения-владельца).\nОбразец — поправка 0.2 ADR-003 «проект, ждёт Р-16».",
  "### Поправка 0.6: промпты шагов (принята Р-15; issue #438)\n\n"
  f"**Статус поправки: принята.** Владелец ответил одной строкой в\n[комментарии к PR #439]({C}):\n"
  "«Р-15 да. Закрыть слитые: BL-150...BL-155, BL-159 → DONE. П-П: BL-157\nсначала (через BL-157а). Р-16 да (А+).» Версия RFC — 0.6, DEC-427-04 и\n"
  "DEC-427-12 — `accepted`. Порядок (П-П): BL-157а (комплект прогона в\nрежиме v0.1, без черновиков «по тесту») → BL-156 → BL-157б (колонка «по\n"
  "тесту» и первый прогон BL-111). `prompts/` в этом PR не меняются: тип\nгейта в 14 промптах — часть BL-156.\n\n"
  "**История записи.** Ниже — текст, с которым поправка ждала ответа; он\nсохранён как обоснование, что Р-15 не было принято до этого ответа."),
 ("BL-156 и BL-157 — `deferred (triggered)`: триггер — ответ на Р-15 и\nотдельная постановка владельца.",
  "После ответа: BL-157а исполнена в PR #439, BL-156 — `TODO` (после\nBL-157а, отдельной постановкой), BL-157б — `deferred (triggered)` до\nBL-156 `DONE`."),
 ("**Порядок BL-157 и BL-156 — открытый вопрос.**", "**Порядок BL-157 и BL-156 — решён (П-П: BL-157 сначала).** До ответа:"),
)
REG = "docs/rfc/rfc-registry.md"
for n in ("04", "12"):
    resub(REG, rf"^(\| \[RFC-427-DEC-{n}\].*\| )`proposed` \| — \|$", rf"\1`accepted` ([Р-15]({C})) | — |")
edit(REG, ("version: 0.15\n", "version: 0.16\n"))
edit(REG, ("  `proposed`; колонки реализации не меняются.\n",
  "  `proposed`; колонки реализации не меняются.\n"
  f"- **2026-11-04** — issue #438 (PR #439): Р-15 принято ([комментарий]({C})) —\n"
  "  поправка 0.6 RFC #427 принята, RFC v0.6; RFC-427-DEC-04, 12 → `accepted`.\n"))

BL = "pr-ops/BACKLOG.md"
resub(BL, r"^(\| \*\*Р-15\*\* \|.*\| )ждёт \|$", rf"\1принято ([PR #439]({C})) |")
resub(BL, r"^(\| \*\*Р-16\*\* \|.*\| )ждёт \|$", rf"\1принято, вариант А+ ([PR #439]({C})) |")
for t in ("BL-150", "BL-151", "BL-152", "BL-153", "BL-154", "BL-155", "BL-159"):
    resub(BL, rf"^(\| {t} \|(?:[^|]*\|){{3}}) review \|", r"\1 DONE |")
resub(BL, r"^(\| BL-162 \|.*?\| BL-159; Р-16 \| )TODO( \|.*?\| )Применить подготовленную поправку 0\.2 ADR-003 к ADR и онтологии по ответу на Р-16;",
      r"\1TODO\2Р-16 принято (А+): применить поправку 0.2 ADR-003 с тремя уточнениями А+ к ADR и онтологии;")

# --- BL-156 / BL-157 split (П-П: BL-157 сначала через BL-157а)
s = Path(BL).read_text(encoding="utf-8")
row156 = re.search(r"(?m)^\| BL-156 \|.*$", s).group(0)
row157 = re.search(r"(?m)^\| BL-157 \|.*$", s).group(0)
READY = "[разбор готовности](../docs/analysis/2026-11-04-bl-156-157-readiness-check.md)"
new156 = ("| BL-156 | [Промпты шагов потока из стандартов по тесту](backlog-ba-model.md#bl-156-промпты-шагов-потока-из-стандартов-по-тесту) | P0 | BL-151, BL-152, BL-153, BL-155, BL-157а; Р-14, Р-15 | TODO | — (planned) | RFC #427, DEC-427-11 | "
          f"Р-15 принято; по П-П стартует после BL-157а отдельной постановкой ({READY}). Входы — заготовка PR #439: сборщик, 12 черновиков в `prompts/drafts/`, `prompt-typing.json`, замер Ш-В RUN-0080. | Creative |")
new157 = ("| BL-157а | [Комплект прогона в режиме v0.1](backlog-ba-model.md#bl-157а-комплект-прогона-в-режиме-v01) | P0 | Р-15 | review | [#438](https://github.com/G-Ivan-A/mango_ba_prompts/issues/438), [PR #439](https://github.com/G-Ivan-A/mango_ba_prompts/pull/439) | RFC #427, раздел 9.4 | "
          f"П-П: BL-157 сначала ({READY}). Комплект `docs/ba-processes/bcreq-run-kit.md` опубликован в режиме `published` (промпты v0.1); колонка «по тесту» — не применять до BL-157б. | Structured |\n"
          "| BL-157б | [Комплект прогона: промпты по тесту и первый прогон](backlog-ba-model.md#bl-157б-комплект-прогона-промпты-по-тесту-и-первый-прогон) | P0 | BL-156, BL-157а, BL-111 | deferred (triggered) | — (deferred) | RFC #427, раздел 9.4 | "
          "Триггер: BL-156 `DONE`. Режим `by-test` в комплекте и первый прогон BL-111 с ним, записанный в `runs/`. | Structured |")
s = s.replace(row156, new156).replace(row157, new157)
Path(BL).write_text(s, encoding="utf-8")
