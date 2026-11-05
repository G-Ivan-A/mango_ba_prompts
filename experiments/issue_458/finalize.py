#!/usr/bin/env python3
"""Карточка, отчёт, журнал RUN-0090 и RUN-0091 из зафиксированных данных (issue #458).

Запускается после `run.py fixate`; `/tmp/run458/prompts-sha256.json` нужен для prompt_ref.
Числа судьи и проверок берутся из outputs/, затраты — из отчётов Claude Code о подагентах.

    python3 experiments/issue_458/finalize.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = "68ad8fcffd47439fc3051852d9a2fbbe23815855"
BASE = "56029742"
PROMPTS = json.loads(Path("/tmp/run458/prompts-sha256.json").read_text(encoding="utf-8"))
SESSIONS = ("C1", "C2", "C3", "C4", "C5")
FRONT = "---\nstatus: draft\nversion: 0.1\nupdated: 2026-11-05\ntemperature: 0.1\n---\n\n"
CRITICAL = re.compile(r"^(J0[1-4]|A[1-3]|B[1-3])$")

COMMON_DEVIATIONS = """| Подагент | Отклонение | Влияние |
| --- | --- | --- |
| Все исполнители и судьи | Инструкция разрешала Grep и Glob, в сеансе подагента их не было. Чтение и поиск шли через Bash: `grep`, `sed`, `head`, `wc`, `ls`, `cd`, `echo`, цикл `for`. Часть из них инструкцией не разрешена | Нет: команды только читали снимок и папку своей сессии. Записи в промпты нет, C08 пройден |
| C5 | Читал `C4/state.md`, хотя в шаблоне списка чтения его нет. Файл назван входом сессии: замечания Ш-В без него недоступны | Дефект обвязки, не исполнителя: шаблон списка не учитывал замечания |
"""


RUNS = {
    "RUN-0090": {
        "task": "BCREQ-1135",
        "other": "RUN-0091",
        "title": "Единая история звонков и заявок: телефония Mango Office и HelpDeskEddy",
        "process": "bcreq-stage1-machine-run-task-1135",
        "input": "../inputs/request.md",
        "tokens": (61581, 90676, 113977, 70901, 86381),
        "tools": (124, 134, 166, 109, 65),
        "ms": (2363110, 2359656, 3036867, 1414581, 1864974),
        "judge": (110732, 49, 857604),
        "turns": 57,
        "questions": "39 → 51 → 81 → 107 (блокируют 79)",
        "markers": 238,
        "remarks": "39 (блокирует гейт 10, важно 22, стиль 7)",
        "feedback": "90 (блокирует 3, важно 44, мелочь 43)",
        "extra_deviations": """| C5 | Записал `state.md` один раз в конце сессии; цитату замечания Ш-В для Q-104 не сверил. В политике БА нет правила для гейта «Выпуск», и сессия остановилась на нём | Гейт остался `pending`, как и должен. Пробел политики — дефект обвязки |
| Судья | Использовал `cd`, `wc`, `head` | Нет: только чтение разрешённых файлов; цитаты перепроверены скриптом |
""",
        "summary": (
            "Документ из 8 разделов получен: 174 669 байт, 107 вопросов, из них 79 блокирующих. Все 12 шагов и "
            "возврат выполнены, скриптовые проверки 8/8. По правилу пред-регистрации — `partial-success`: "
            "провалены критические J01, J02, J03. Все запрошенные Заказчиком пункты A1–A6 в документе отражены."
        ),
        "findings": """1. **Неверное обобщение факта (J01).** Н-06: «Автоматическая запись разговора без места в облачном
   хранилище: ВАТС не выполняет.» Руководство описывает опцию «Перезаписывать самые старые звонки»:
   `docs/kb/mango-lk-manual/sections/139-nastroyki.md:68` и `299-oblachnoe-hranilische.md:64` на срезе
   `68ad8fcf`. Проверено вручную. Дефект содержания, правится в прогоне БА.
2. **Трассировка рвётся после возврата (J03).** Судья нашёл 18 разрывов. К-31 называет причину:
   «разрыв создан правкой №1», то есть правкой возврата по Ш-В. К-31 разрыв поймал, а исправить его в
   этом потоке некому: вариант замечания не перечисляет зависимые места.
3. **Устаревшие снимки в теле документа.** «39 вопросов» и «21 блокирующий вопрос» остались в теле при
   итоговых 107 и 79; предупреждение есть только в служебном реестре в конце.
4. **Реестр 8.4 не приоритизирован.** 107 вопросов идут без порядка, срок у всех «см. выше». Ключевые
   Q-03, Q-13, Q-14, Q-16, Q-19, Q-21 перемешаны с 18 вопросами к кандидатам в риски.
5. **База знаний использована не полностью.** Не применены `sip_call_id`, `command_id` и «Простые
   звонки» с helpdesk-системами (`docs/kb/mango-lk-manual/sections/308-podklyuchit-integraciyu.md`,
   `318-moi-integracii.md`). Q-105 снимается уже процитированным источником.
6. **Требования непроверяемы (J07).** В документе: «Не проверяемы до ответов на вопросы: ПР-01,
   ПР-03…ПР-15». При симуляторе это ожидаемо: ответов БА в прогоне нет.
""",
        "next": "Первым делом при прогоне БА: снять Q-13 и Q-19 (что именно видно в HDE и кто делает связку), затем Q-03, Q-14, Q-16, Q-21. Машинный документ читать после своего прогона, чтобы не заякорить решение.",
    },
    "RUN-0091": {
        "task": "BCREQ-1137",
        "other": "RUN-0090",
        "title": "Доступ сотрудника партнёра только к интеграции с Яндекс Директом в Коллтрекинге",
        "process": "bcreq-stage1-machine-run-task-1137",
        "input": "../inputs/request.md",
        "tokens": (35066, 55432, 93819, 92705, 102397),
        "tools": (106, 81, 103, 70, 47),
        "ms": (2187119, 1606620, 2406074, 1353293, 1920690),
        "judge": (109124, 23, 502998),
        "turns": 61,
        "questions": "32 → 43 → 57 → 70 (блокируют 37)",
        "markers": 256,
        "remarks": "33 (блокирует гейт 5, важно 20, стиль 8)",
        "feedback": "90 (блокирует 3, важно 45, мелочь 42)",
        "extra_deviations": """| Судья | Выполнял `sed` и `python` через Bash по `/tmp/rt458` и `bcreq.md` | Нет: только чтение разрешённых файлов; цитаты перепроверены скриптом |
""",
        "summary": (
            "Документ из 8 разделов получен: 149 498 байт, 70 вопросов, из них 37 блокирующих. Все 12 шагов и "
            "возврат выполнены, скриптовые проверки 8/8. По правилу пред-регистрации — `partial-success`: "
            "провалены критические J01, J02, J03. Описание текущего поведения Коллтрекинга осталось пустым из-за "
            "расхождения маршрута: документы о нём лежат в другом классе поиска."
        ),
        "findings": """1. **Расхождение маршрута каталог ↔ база знаний (первопричина J01, B7).** На срезе `68ad8fcf`
   `taxonomy/mango-products.yaml:36` даёт `call-tracking` класс `analytics-reporting`, а `docs/kb/MAP.json`
   относит `mango-lk-manual` и `rolevaya-model-vats` только к `voice-ucaas`. В 17 разделах `mango-lk-manual`
   Коллтрекинг упомянут, в документах класса `analytics-reporting` есть лишь отдельные упоминания в `speech-analytics`. Ш-0 запрещает
   читать другой класс без решения БА, симулятор такого решения не дал. Модель поступила верно: подняла
   Q-01 и предложила именно эти два документа, поэтому As-Is собран по ЛК Речевой аналитики с маркерами.
   Класс в карточке задан обвязкой по каталогу, так что это дефект данных, а не выбора исполнителя.
2. **Пропущенные факты (следствие п. 1).** `rolevaya-model-vats` §5.2.6, §5.2.24, §5.4.4
   (`sections/23-dinamicheskiy-kolltreking.md`, `55-integracii.md`) описывает права; плитка «Яндекс.Директ» есть
   в блоке «Интеграции» на иллюстрации `192-whatsapp-7.png`. Q-02, Q-30, Q-50, Q-51 частично снимаются чтением.
3. **Опровержимые утверждения (J01).** «Для Коллтрекинга в документации не описано» без локатора. Судья
   показал, что это верно только для прочитанного класса.
4. **Обход запрета не рассмотрен (B5).** В документе нет прямой ссылки, API, отчётов и выгрузки ни как
   сценария, ни как вопроса; поиск по тексту совпадений не дал. Для запрета «не в коем случае» это важный пробел.
5. **Партнёр как субъект подключения (B4).** Q-19 предлагает «сотрудник для партнера; клиент; иной»,
   самостоятельного подключения партнёром нет. Подключение записано без субъекта.
6. **Реестр 8.4 и снимки (J03, J07).** 70 вопросов без порядка; ВКЛ-07…ВКЛ-10 не доходят до 8.3; К-33 называет
   устаревшие места и не исправляет их.
""",
        "next": "Первым делом при прогоне БА: ответить на Q-01 и разрешить `mango-lk-manual` и `rolevaya-model-vats`. Это снимает большую часть пробелов As-Is. Затем задать вопрос об обходе запрета (B5) и о субъекте подключения (B4). Машинный документ читать после своего прогона.",
    },
}


def spaced(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def scores(run: str) -> tuple[dict, dict]:
    out = ROOT / "runs/2026" / run / "outputs"
    return (
        json.loads((out / "judge-scores.json").read_text(encoding="utf-8")),
        json.loads((out / "check.json").read_text(encoding="utf-8")),
    )


def prompt_version(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    m = re.search(r'^version:\s*"?([^"\n]+)"?', text, re.M)
    ver = m.group(1).strip() if m else "н/д"
    return f"{ver}-by-test (реестр 0.5)" if "/drafts/" in path else ver


def metadata(run: str, cfg: dict) -> str:
    judge, check = scores(run)
    crit = judge["criteria"]
    passed = sorted(k for k, v in crit.items() if v["verdict"] == "pass")
    failed = sorted(k for k, v in crit.items() if v["verdict"] != "pass")
    critical = sorted(k for k in crit if CRITICAL.match(k))
    c_pass = sum(1 for k, v in check.items() if re.fullmatch(r"C0\d", k) and v["pass"])
    assert c_pass == 8, run
    prompts = "\n".join(
        f'  - {{step: {s}, path: {v["path"]}, version: "{prompt_version(v["path"])}", sha256: {v["sha256"]}}}'
        for s, v in PROMPTS.items()
    )
    outs = sorted(p.name for p in (ROOT / "runs/2026" / run / "outputs" / "transcripts").glob("*.md"))
    executor = sum(cfg["tokens"])
    eval_text = (
        f"Машинный прогон потока BCREQ по задаче {cfg['task'][-4:]}: 5 изолированных сессий, 12 шагов, возврат по Ш-В, "
        f"гейты `pending`, реплики БА — симулятор. Скриптовые проверки 8/8; слепой судья {len(passed)}/{len(crit)}, "
        f"провалы {', '.join(failed)}. Вердикт по правилу пред-регистрации. N = 1, судья не откалиброван, БА не проверял."
    )
    return f"""run_id: {run}
process: {cfg['process']}
version: "0.1"
date: 2026-11-05
author: "Claude Code (claude-opus-5-5), issue #458"
model: "claude-opus-5-5 — исполнитель (5 изолированных подагентов по сессиям) и слепой судья (1 изолированный подагент)"
status: draft
run_type: execution
input_kind: real
task:
  id: {cfg['task']}
  title: "{cfg['title']}"
source_paths:
  - inputs/request.md
  - inputs/task-card.md
inputs:
  - inputs/request.md
  - inputs/task-card.md
outputs:
  - outputs/README.md
  - outputs/report.md
  - outputs/bcreq.md
  - outputs/release-readiness.md
  - outputs/review-remarks.md
  - outputs/check.json
  - outputs/judge-scores.json
{chr(10).join(f'  - outputs/transcripts/{n}' for n in outs)}
logs:
  - logs/experiment-log.md
  - logs/gate-journal.md
  - logs/session-journal.md
  - logs/preregistration.md
  - logs/executor-instruction.md
  - logs/judge-instruction.md
  - logs/ba-policy.md
feedback:
  - feedback/step-feedback.md
prompt_set:
  mode: "run kit v0.5: Ш-0, Ш-1, Ш-2, Ш-Р — by-test; остальные — published"
  commit: {BASE}
prompt_ref:
{prompts}
standards:
  base: standards/bcreq-prompt-base-standard.md@0.1.3
  profiles: standards/bcreq-prompt-profiles.md@0.1.1
  runtime_references: standards/bcreq-runtime-references.md@0.5
runtime:
  repo: G-Ivan-A/mango-ba-ai-runtime
  commit: {PIN}
preregistration: experiments/issue_458/preregistration.md
replicates: 1
lessons: []
golden_promotion: []
ba_reviewed: false
metrics:
  verdict: partial-success
  steps_done: 12
  scripted_checks: 8
  scripted_passed: {c_pass}
  criteria: {len(crit)}
  passed: {len(passed)}
  failed: [{', '.join(failed)}]
  critical: [{', '.join(critical)}]
  gates_pending: [Г-IN, Г-С1, Г-W, Выпуск]
  tokens_executor: {executor}
  tokens_judge: {cfg['judge'][0]}
  tokens_total: {executor + cfg['judge'][0]}
  token_method: "subagent_tokens из отчёта Claude Code о подагенте; при сжатии контекста внутри сессии возможна недооценка"
  measured: true
  eval: "{eval_text}"
related_runs:
  - {cfg['other']}
related_issues:
  - https://github.com/G-Ivan-A/mango_ba_prompts/issues/458
related_artifacts:
  - docs/rfc/2026-11-bcreq-machine-run-baseline.md
  - experiments/issue_458/task-statement.md
  - experiments/issue_458/run.py
  - experiments/issue_458/preregistration.md
  - scripts/validate_issue_458_machine_runs.py
"""


def judge_table(run: str) -> str:
    judge, _ = scores(run)
    rows = ["| Критерий | Критический | Вердикт | Обоснование судьи |", "| --- | --- | --- | --- |"]
    for key, val in sorted(judge["criteria"].items()):
        why = re.sub(r"\s+", " ", val.get("why") or val.get("rationale") or val.get("reason") or "").replace("|", "\\|")
        rows.append(f"| {key} | {'да' if CRITICAL.match(key) else 'нет'} | `{val['verdict']}` | {why} |")
    return "\n".join(rows)


def report(run: str, cfg: dict) -> str:
    judge, check = scores(run)
    total = sum(cfg["tokens"]) + cfg["judge"][0]
    passed = sum(1 for v in judge["criteria"].values() if v["verdict"] == "pass")
    return FRONT + f"""# Отчёт {run}: машинный прогон BCREQ по задаче {cfg['task'][-4:]}

## Итог

**Вердикт `partial-success`.** {cfg['summary']}

Это кандидат, а не принятая спецификация. Гейты Г-IN, Г-С1, Г-W и «Выпуск» остаются `pending`, решений людей нет,
`ba_reviewed: false`. К-31 — FAIL, К-33 — `ready_for_human_release: нет`, ничего не отправлено. Прогон не заменяет
BL-157в: он не проверяет работу БА и не проходит человеческие гейты.

Результат: [`bcreq.md`](bcreq.md); вход: [запрос]({cfg['input']}).

## Как получен

Реплики БА заданы до запуска ([политика симулятора](../logs/ba-policy.md)), промпты не менялись (C08), прогон не читал
выход {cfg['other']} (C07). Каждая сессия — отдельный подагент; Ш-В и судья работали в отдельных сессиях. Подробности:
[журнал](../logs/experiment-log.md), [правило вердикта](../logs/preregistration.md#правило-вердикта).

## Скриптовые проверки

Все C01–C08 пройдены: [`check.json`](check.json). C02 и C03 сверяют пути и ID со срезом runtime `{PIN[:8]}`.

## Оценка слепого судьи

Сдано {passed} из {len(judge['criteria'])}. Сырые оценки: [`judge-scores.json`](judge-scores.json). Судья не откалиброван,
N = 1. Цитаты судьи сверены скриптом с документом дословно, ключевые утверждения о базе знаний — вручную по клону runtime.

{judge_table(run)}

## Находки

{cfg['findings']}
## Что сработало

- Запрет соблюдён: ни один гейт не показан пройденным, выдуманных пройденных статусов нет (J04, C04).
- К-31 и К-33 сами нашли разрывы и не выдали готовность. Механизм честный, не хватает способа закрыть найденное.
- Ш-В в новой сессии дал замечания в требуемой форме: {cfg['remarks']}.

## Обратная связь по промптам

Строк: {cfg['feedback']}: [`step-feedback.md`](../feedback/step-feedback.md). Правки промптов здесь не вносились.

## Затраты

Исполнитель {spaced(sum(cfg['tokens']))} токенов, судья {spaced(cfg['judge'][0])}, всего {spaced(total)} (оценка пред-регистрации 0,5–0,9 млн).
Таблица по сессиям — в [журнале](../logs/experiment-log.md#затраты).

## Пределы

N = 1; один исполнитель и один судья одной модели; ответы БА — симулятор, поэтому часть провалов J07 ожидаема;
счётчики в К-31 и К-12 посчитаны моделью вручную; сравнения с документом БА нет. Метрики качества и экономии отсюда не
выводятся.

## Что дальше

{cfg['next']} Общие решения — в [RFC-MR-001](../../../../docs/rfc/2026-11-bcreq-machine-run-baseline.md).
"""


def readme(run: str, cfg: dict) -> str:
    return FRONT + f"""# Результат {run}

Машинный прогон потока BCREQ по задаче {cfg['task'][-4:]}: {cfg['title']}.
Вердикт `partial-success`, статус документа — кандидат, гейты `pending`, `ba_reviewed: false`.

| Файл | Что внутри |
| --- | --- |
| [`report.md`](report.md) | Итог, оценки судьи, находки, пределы |
| [`bcreq.md`](bcreq.md) | Бизнес-спецификация: 8 разделов, полная сборка К-12 |
| [`release-readiness.md`](release-readiness.md) | Заглушка выпуска: К-31, К-12, К-33, К-32 draft, К-35 |
| [`review-remarks.md`](review-remarks.md) | Состояние сессии Ш-В с замечаниями, {cfg['remarks']} |
| [`check.json`](check.json) | Скриптовые проверки C01–C08 |
| [`judge-scores.json`](judge-scores.json) | Оценки слепого судьи с цитатами |
| [`transcripts/`](transcripts/) | Транскрипты шагов: {cfg['turns']} ходов модели |
"""


def experiment_log(run: str, cfg: dict) -> str:
    rows = []
    for name, tok, tool, ms in zip(SESSIONS, cfg["tokens"], cfg["tools"], cfg["ms"]):
        rows.append(f"| Исполнитель {name} | {tok:,} | {tool} | {round(ms / 60000)} мин |".replace(",", " "))
    jt, jc, jm = cfg["judge"]
    rows.append(f"| Судья | {jt:,} | {jc} | {round(jm / 60000)} мин |".replace(",", " "))
    total = sum(cfg["tokens"]) + jt
    rows.append(f"| **Итого** | **{total:,}** | {sum(cfg['tools']) + jc} | |".replace(",", " "))
    table = "\n".join(rows)
    return FRONT + f"""# Журнал {run}

## Цель

Получить бизнес-спецификацию BCREQ из 8 разделов по задаче {cfg['task'][-4:]} машинным проходом всех шагов потока
(issue #458): «параллельно сделать машинный прогон по новым задачам по всем необходимым шагам потока BCREQ».
Правило вердикта записано до запуска: [`preregistration.md`](preregistration.md).

## Процедура

1. **Подготовка.** Клон runtime на `{PIN[:8]}`; снимок Хаба и промптов; SHA-256 промптов записаны
   (`experiments/issue_458/run.py prepare`). Основа — `{BASE}`.
2. **Исполнение.** Сессии C1 (Ш-0, Ш-1, Ш-2), C2 (Ш-3, Ш-4, Ш-5), C3 (Ш-6, Ш-7, Ш-8, Ш-9), C4 (Ш-В), C5 (возврат, Ш-Р) —
   отдельные подагенты `claude-opus-5-5` ([инструкция](executor-instruction.md)). Состояние передавалось только
   файлом `state.md`. {cfg['other']} шёл параллельно: первые транскрипты задач появились в 08:32 и 08:37, сессии
   пересекались по времени, чтения чужого выхода нет (C07).
3. **Реплики БА.** Симулятор по заранее заданным правилам ([политика](ba-policy.md)). Модель реплик не сочиняла:
   решения гейтов не передавались, в журнале `pending` ([журнал гейтов](gate-journal.md)).
4. **Проверка.** `run.py check {run}` → [`check.json`](../outputs/check.json).
5. **Оценка.** Один изолированный слепой судья ([инструкция](judge-instruction.md)) →
   [`judge-scores.json`](../outputs/judge-scores.json). Цитаты сверены скриптом; утверждения о базе знаний — по клону.
6. **Фиксация.** `run.py fixate {run}`, затем `experiments/issue_458/finalize.py`.

## Отклонения от инструкции

{COMMON_DEVIATIONS}{cfg['extra_deviations']}
## Отступления обвязки

- **Исправление разбора C01 после первого запуска.** Первый запуск дал провал C01 у задачи 1135 только из-за разбора:
  подразделы записаны как `2.1 Контекст` простой строкой, а `**2.1 Контекст:**` — жирным. Критерий требует наличия
  подразделов, а не разметки, поэтому правило не менялось. После исправления обе задачи — 8/8.
- **Перенумерация.** Прогон задуман как RUN-0088 (1135) и RUN-0089 (1137). RUN-0088 занял PR #455, RUN-0089 заявлен в его
  сценариях. Номера заменены на RUN-0090 и RUN-0091 точной подстановкой во всех выходах, проверки C01–C08 повторены.
  Пред-регистрация до замены — в коммите `4a118040`; правила вердикта замена не касается.
- **Заголовок карточки 1137.** Заголовок обвязки «Доступ сотрудника партнёра» отличается от запроса: «сотрудника для
  партнера». Модель подняла это вопросом Q-11. Это артефакт обвязки, а не дефект промпта.

## Затраты

| Подагент | Токены (`subagent_tokens`) | Вызовы инструментов | Время |
| --- | --- | --- | --- |
{table}

Внутри сессий было сжатие контекста, поэтому `subagent_tokens` может занижать реальный расход. Ходов модели: {cfg['turns']}.

## Итог

Все 12 шагов и возврат выполнены, вопросов по шагам: {cfg['questions']}, маркеров `[ТРЕБУЕТСЯ УТОЧНЕНИЕ]`: {cfg['markers']}.
Вердикт `partial-success` по правилу пред-регистрации. Разбор — в [отчёте](../outputs/report.md).

## Воспроизведение

```bash
git clone https://github.com/G-Ivan-A/mango-ba-ai-runtime /tmp/rt458 && git -C /tmp/rt458 checkout {PIN}
python3 experiments/issue_458/run.py prepare
python3 experiments/issue_458/run.py instr {run} C1   # инструкция сессии для подагента; далее C2…C5
python3 experiments/issue_458/run.py check {run}
python3 experiments/issue_458/run.py judge {run}      # инструкция судьи
python3 experiments/issue_458/run.py fixate {run}
python3 experiments/issue_458/finalize.py
```

Модель недетерминирована: тот же документ не получится, повторяются процедура и проверки.
"""


def main() -> int:
    for run, cfg in RUNS.items():
        base = ROOT / "runs/2026" / run
        (base / "metadata.yaml").write_text(metadata(run, cfg), encoding="utf-8")
        (base / "outputs/report.md").write_text(report(run, cfg), encoding="utf-8")
        (base / "outputs/README.md").write_text(readme(run, cfg), encoding="utf-8")
        (base / "logs/experiment-log.md").write_text(experiment_log(run, cfg), encoding="utf-8")
        print("ok", run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
