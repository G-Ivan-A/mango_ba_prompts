"""Resolve merge conflicts of PR #436 with upstream main after PR #435 (issue #432)."""
import re, pathlib

def blocks(path):
    t = pathlib.Path(path).read_text(encoding="utf-8")
    pat = re.compile(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> upstream/main\n", re.S)
    return t, pat

def resolve(path, fn):
    t, pat = blocks(path)
    n = [0]
    def rep(m):
        n[0] += 1
        return fn(n[0], m.group(1), m.group(2))
    t2 = pat.sub(rep, t)
    assert "<<<<<<<" not in t2 and ">>>>>>>" not in t2, path
    pathlib.Path(path).write_text(t2, encoding="utf-8")
    print(path, n[0])

# CHANGELOG: both entries; #433 merges after #435 -> on top.
resolve("CHANGELOG.md", lambda i, a, b: a.replace("v0.4.1, архитектура", "v0.5.1, архитектура")
        .replace("версию RFC 0.4.1", "версию RFC 0.5.1") + "\n" + b)
# RFC: patch on top of 0.5
resolve("docs/rfc/2026-11-bcreq-flow-processes-prompts.md", lambda i, a, b: "version: 0.5.1\n")
# validator #427
resolve("scripts/validate_issue_427_r13_acceptance.py", lambda i, a, b:
        "        # тип гейта; 0.5 — #432, Р-14) статус RFC не меняют; 0.5.1 — #433,\n"
        "        # типизация гейтов BL-159.\n"
        "        self.assertIn(self.fm.get(\"version\"), (\"0.3\", \"0.4\", \"0.5\", \"0.5.1\"))\n")
# overrides: README hash recomputed later; keep ours' other entries, README reason combined
def ov(i, a, b):
    ours_rest = a.split("\n", 2)[2]  # drop README sha/reason lines
    return ('      "sha256": "RECOMPUTE",\n'
            '      "reason": "#430: словарь потока BCREQ и реестр справочников runtime в карте стандартов; '
            '#432: базовый стандарт и профили промпта BCREQ «по тесту» в карте стандартов (сайт не меняется)"\n'
            + ours_rest)
resolve("experiments/issue_413/site-baseline-overrides.json", ov)
# BACKLOG
def bl(i, a, b):
    if i == 1:
        return a.replace("BL-158, BL-161 — после прогонов |", "BL-158, BL-161 — после прогонов; BL-160 — к этапу 3 |")
    a_lines = a.splitlines(True); b_lines = b.splitlines(True)
    return a_lines[0] + b_lines[1] + "".join(a_lines[1:])
resolve("pr-ops/BACKLOG.md", bl)
# backlog-ba-model
def bm(i, a, b):
    if i == 1:
        return ("  обязателен с первой редакции. Записано в «Что меняется» каждой карточки.\n"
                "  BL-151 и BL-152 сделаны (issue #432, PR #435): правило БС-29 и раздел 4\n"
                "  [базового стандарта](../standards/bcreq-prompt-base-standard.md#4-типы-гейтов-базового-стандарта),\n"
                "  правила VE-05 и RE-06 профилей; остаются BL-230, BL-231, BL-141.\n"
                "- [x] Журнал К-34: поле «рекомендация модели» и «расхождение с решением»\n")
    return b + "\n" + a
resolve("pr-ops/backlog-ba-model.md", bm)
