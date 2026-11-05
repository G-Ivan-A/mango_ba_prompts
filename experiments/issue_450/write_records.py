#!/usr/bin/env python3
"""Метаданные и отчёты RUN-0085…0087: числа берутся из outputs/summary.json и tokens-summary.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FM = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-11-05\ntemperature: 0.1\n---\n\n"
TOK = json.loads((ROOT / "experiments/issue_450/tokens-summary.json").read_text())
PR = "https://github.com/G-Ivan-A/mango_ba_prompts/issues/450"
COMMON_LIMITS = (
    "Оценка модели-судьи без подтверждения человеком (`ba_reviewed: false`), "
    "судья не калиброван по БА. Это не приёмка: приёмка возможна только по "
    "реальному прогону БА (BL-157в).\n"
)
INFO = {
    "85": dict(
        process="bcreq-stage1-golden-set-review-validation-no-split-a3",
        bl="BL-156г", prompts=["prompts/bcreq-review-validation-oneshot.md"],
        title="Ш-В: уточнение правила против избыточной декомпозиции (A3) против контроля A2 (v0.2)",
        verdict="A3 не хуже контроля, сторож Р-18 пуст — публикуется как Ш-В v0.3.",
        extra="GS-BCREQ-25: A2 1/3 → A3 0/3. GS-BCREQ-12: A2 0/3 → A3 1/3. GS-BCREQ-26 падает 3/3 в обоих плечах: не ядро сторожа, остаётся открытым; A3 его не лечит и не вызывает.",
    ),
    "86": dict(
        process="bcreq-industry-practice-block-steps-1-3-6",
        bl="BL-167", prompts=["prompts/bcreq-context-understanding-stepwise.md", "prompts/bcreq-fr-documentation-stepwise.md", "prompts/bcreq-orr-solution-design-stepwise.md"],
        title="Блок «Индустриальная практика на решение БА» в Ш-1, Ш-3, Ш-6 против контроля v0.1",
        verdict="Блок не хуже контроля и даёт прирост пользы на всех трёх шагах, сторож Р-18 пуст — Ш-1, Ш-3, Ш-6 публикуются как v0.2.",
        extra="S6-a1 падает 3/3 в обоих плечах: на Ш-6 практика в этом кейсе не предлагается и с блоком, открытый дефект. Проверка Ш-В: чистая подача — в 3 из 3 повторов ожидаемый вердикт (`outputs/shv-check/`): практика вне требований не считается дефектом (F1), практика внутри ФТ считается (F2); правило снятия блока не сработало.",
    ),
    "87": dict(
        process="bcreq-long-session-rules-constitution",
        bl="BL-168", prompts=["prompts/bcreq-constitution-governance-oneshot.md"],
        title="Правила длинной сессии АД-12…15 в Ш-0 против контроля v0.1",
        verdict="Правила не хуже контроля, польза выше, сторож Р-18 пуст — Ш-0 публикуется как v0.2.",
        extra="Сценарий S3 падает: контроль 3/3, с правилами 1/3. Многоходовая часть замера — два хода на сценарий, то есть проверка принципа, а не длинной сессии реального чата.",
    ),
}
DEV = {
    "85": ["Инструкции подавались подагентам файлом `/tmp/ins/*.txt` — один дополнительный вызов Read у каждого; на сравнение не влияет: одинаково в обоих плечах."],
    "86": [
        "Инструкции подавались файлом — один дополнительный Read, одинаково в обоих плечах.",
        "**Ошибка исполнителя.** Первая проверка Ш-В получила фрагменты, в заголовках которых стоял ожидаемый вердикт (загрязнённая подача). Результат отброшен и не использован; проверка повторена с нейтральными `fragments.md` тремя новыми подагентами. Потери — 56 945 токенов, учтены в `tokens.tsv` как `check-discarded` и в итоге прогона.",
        "Проверка Ш-В шла по рабочему дереву с текстом Ш-В v0.3 до коммита публикации; текст совпадает с `ce4fc8aa`.",
    ],
    "87": ["Инструкции подавались файлом — один дополнительный Read, одинаково в обоих плечах."],
}


def files(run, sub):
    return sorted(str(p.relative_to(run)) for p in (run / sub).rglob("*") if p.is_file() and p.name != "metadata.yaml")


def table(s, n):
    if n == "85":
        m = s["median"]
        rows = [f"| {a} | {m[a]['passed']}/62 | {m[a]['core']}/11 | {m[a]['negatives_false_positive']}/10 | " + ", ".join(str(s['replicates'][a][r]['passed']) for r in ('r1', 'r2', 'r3')) + " |" for a in ("A2", "A3")]
        return "| Плечо | Сдано (медиана) | Ядро | Ложные дефекты | Повторы |\n| --- | --- | --- | --- | --- |\n" + "\n".join(rows)
    groups = s if n == "86" else {"SES": s}
    rows = []
    for g, v in groups.items():
        for a in ("C", "B"):
            x = v["median"][a]
            rows.append(f"| {g} | {a} | {x['passed']} | {x['core']} | {x['false']} | {x['benefit']} | {', '.join(map(str, x['replicates_passed']))} |")
    return "| Группа | Плечо | Сдано | Ядро | Ложные | Польза | Повторы |\n| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(rows)


def write(n):
    i, run = INFO[n], ROOT / f"runs/2026/RUN-00{n}"
    s = json.loads((run / "outputs/summary.json").read_text())
    t = TOK[n]
    pre = f"experiments/issue_450/run00{n}/preregistration.md"
    freq = json.dumps(s["fail_frequency"] if n != "86" else {g: s[g]["fail_frequency"] for g in s}, ensure_ascii=False)
    (run / "inputs/README.md").write_text(FM + f"# Вход RUN-00{n}\n\n{i['title']}.\n\nТексты плеч и кейсы — в этом каталоге; они одинаковы во всех повторах. Правило решения и SHA-256 текстов записаны до запуска: [`preregistration.md`](../../../../{pre}). Метки плеч для судей заданы seed, ключ — `outputs/rN/judge-key.json`.\n", encoding="utf-8")
    (run / "outputs/golden-set-report.md").write_text(FM + f"# Отчёт RUN-00{n}: {i['title']}\n\nРешение {i['bl']} по Р-03 (одновременный контроль, N = 3, медиана) и Р-18 (issue [#450]({PR})).\n\n{table(s, n)}\n\nЧастота падений кейсов по плечам: `{freq}`.\n\n**Решение.** {i['verdict']}\n\n{i['extra']}\n\n## Токены\n\nИтого {t['total']} (`experiments/issue_450/run00{n}/tokens.tsv`).\n\n## Ограничения\n\n{COMMON_LIMITS}", encoding="utf-8")
    (run / "outputs/README.md").write_text(FM + f"# Результат RUN-00{n}\n\n[`golden-set-report.md`](golden-set-report.md) — итог и решение; [`summary.json`](summary.json) — медианы и проверки; `r1/`…`r3/` — ответы исполнителей, оценки судей, ключ.\n\n{i['verdict']} {COMMON_LIMITS}", encoding="utf-8")
    (run / "logs/experiment-log.md").write_text(FM + f"# Журнал RUN-00{n}\n\n## Цель\n\n{i['title']}. Бюджет подтверждён владельцем в issue [#450]({PR}).\n\n## Процедура\n\n1. Коммит пред-регистрации `b94d5cc0` — до запуска подагентов.\n2. `experiments/issue_450/run00{n}/run.py prepare`, запуск изолированных подагентов opus (исполнители, затем слепые судьи).\n3. `run.py judge`, `run.py score`; итог в `outputs/summary.json`.\n4. `experiments/issue_450/fixate.py` и `write_records.py` — фиксация.\n\n## Отклонения\n\n" + "\n".join(f"- {d}" for d in DEV[n]) + "\n", encoding="utf-8")
    (run / "feedback/review-notes.md").write_text(FM + f"# Замечания к RUN-00{n}\n\n## Статус проверки человеком\n\n{COMMON_LIMITS}\n## Что осталось открытым\n\n{i['extra']}\n", encoding="utf-8")
    md = [f"run_id: RUN-00{n}", f"process: {i['process']}", 'version: "0.1"', "date: 2026-11-05", 'author: "Claude Code (claude-opus-5-5), issue #450"', 'model: "claude-opus-5-5 — исполнители и слепые судьи, изолированные подагенты"', "status: draft", "run_type: execution", "source_paths:", "  - inputs/README.md"]
    for sec, sub in (("inputs", "inputs"), ("outputs", "outputs"), ("logs", "logs"), ("feedback", "feedback")):
        md += [f"{sec}:"] + [f"  - {f}" for f in files(run, sub)]
    md += [f"preregistration: {pre}", "replicates: 3", "lessons: []", "golden_promotion: []", "ba_reviewed: false", "metrics:", "  verdict: works-with-edits", f"  tokens_total: {t['total']}", "  measured: true", f'  eval: "{i["verdict"]}"', "related_runs:", "  - RUN-0084", "related_issues:", f"  - {PR}", "related_artifacts:"]
    md += [f"  - {p}" for p in i["prompts"]] + [f"  - {pre}", f"  - experiments/issue_450/run00{n}/tokens.tsv", ""]
    (run / "metadata.yaml").write_text("\n".join(md), encoding="utf-8")


for n in INFO:
    write(n)
readme = ROOT / "runs/README.md"
txt = readme.read_text(encoding="utf-8").splitlines()
idx = max(k for k, l in enumerate(txt) if l.startswith("| [`RUN-00"))
new = [f"| [`RUN-00{n}`](2026/RUN-00{n}/metadata.yaml) | 2026-11-05 | `execution` | {INFO[n]['process']} | [Отчёт](2026/RUN-00{n}/outputs/golden-set-report.md), [`outputs/README.md`](2026/RUN-00{n}/outputs/README.md), [сводка](2026/RUN-00{n}/outputs/summary.json), [`logs/experiment-log.md`](2026/RUN-00{n}/logs/experiment-log.md), [review](2026/RUN-00{n}/feedback/review-notes.md) |" for n in INFO if f"RUN-00{n}`" not in "\n".join(txt)]
txt[idx + 1:idx + 1] = new
readme.write_text("\n".join(txt) + "\n", encoding="utf-8")
