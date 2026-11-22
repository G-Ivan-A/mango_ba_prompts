#!/usr/bin/env python3
"""Read the BL-230 tables and check offline examples of navigation decisions."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re

import bcreq_handoff

ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "docs/ba-processes/bcreq-manual-process.md"
FORMATS = ("system", "decomposed")
BOTH = "оба"
EMPTY = "—"
TERMINAL = {"СТОП", "CS", "BASELINE"}
GATE_OWNERS = {
    "AIN-21": {"БА"}, "Г-IN": {"БА"}, "Г-С1": {"Заказчик"},
    "Г-W": {"ПО продукта", "архитектор продукта", "руководитель КК"},
    "Выпуск": {"БА"},
}
OTHER_TARGETS = {
    "выйти в CS": "CS", "остановить": "СТОП", "выпустить": "BASELINE",
    "уточнить с моделью": "текущий", "уточнить с Заказчиком": "текущий",
    "сценарии по запросу": "Ш-С", "вернуться в контекст": "исходный",
    "остановить по решению БА": "СТОП",
}
SCOPE = ("task_id", "attempt", "route_version", "snapshot_id", "snapshot_version")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def table(text, heading, columns):
    heading = f"#### {heading}\n\n"
    require(text.count(heading) == 1, f"Нужен один раздел {heading.strip()}")
    block = text.split(heading, 1)[1].split("\n#### ", 1)[0]
    rows = re.search(r"(?m)(?:^\| .+ \|\n?)+", block)
    require(rows is not None, f"{heading.strip()}: нет таблицы")

    def cells(line):
        return [cell.strip() for cell in line.strip("|").split("|")]

    header, separator, *body = map(cells, rows[0].splitlines())
    require(set(columns) <= set(header) and len(header) == len(set(header)),
            f"{heading.strip()}: неверные колонки")
    require(separator == ["---"] * len(header), f"{heading.strip()}: неверный разделитель")
    result = []
    for row in body:
        require(len(row) == len(header) and all(row), f"{heading.strip()}: неполная строка {row}")
        values = dict(zip(header, row))
        result.append({key: values[label] for label, key in columns.items()})
    require(result, f"{heading.strip()}: нет строк")
    return result


def index(rows, field):
    indexed = {}
    for row in rows:
        key = row[field]
        require(key not in indexed, f"{key}: повторная строка ({field})")
        indexed[key] = row
    return indexed


def edition(link):
    match = re.fullmatch(r"\[[^\]]+\]\((\.\./\.\./prompts/[^)]+\.md)\)", link)
    require(match, f"Отсутствует ссылка на редакцию: {link}")
    path = (PROCESS.parent / match[1]).resolve()
    require(path.is_relative_to(ROOT / "prompts") and path.is_file(),
            f"Редакция отсутствует: {match[1]}")
    require(not path.is_relative_to(ROOT / "prompts/archive"), f"Редакция в архиве: {path.name}")
    header = path.read_text(encoding="utf-8").split("---", 2)
    require(len(header) == 3 and all(re.search(rf"(?m)^{key}: \S", header[1])
                                    for key in ("id", "version", "status")),
            f"Нет ID, статуса или версии: {path.name}")
    require(not re.search(r'(?m)^status:\s*["\']?archived\b', header[1]),
            f"Редакция архивная: {path.name}")
    return path.relative_to(ROOT).as_posix()


def available(route, step, track):
    return step in route["ain"] and track == "decomposed" or (
        step in route["steps"] and route["steps"][step]["format"] in (BOTH, track)
    )


def load(text=None):
    """Read the SSOT and check it against the current run kit, handoff and A-IN."""
    if text is None:
        text = PROCESS.read_text(encoding="utf-8")
    require(re.search(r"(?m)^version: 0\.3$", text), "Нужен ручной процесс v0.3")
    kit = json.loads((ROOT / "site/data/test-kit.json").read_text(encoding="utf-8"))["steps"]
    ain = json.loads((PROCESS.parent / "bcreq-a-in-route.json").read_text(encoding="utf-8"))
    handoff = bcreq_handoff.load()["steps"]

    steps = index(table(text, "Шаги этапа 1", {
        "№": "number", "Код шага": "id", "Шаг": "name", "Процесс": "process",
        "Стадия": "stage", "Промпт маршрута v0.1": "v01", "Параметры": "params",
        "Что подготовить": "input", "Зачем шаг": "goal", "Редакция": "edition",
        "Формат": "format", "Режим": "mode", "Результат": "result",
        "Гейт после шага": "gate", "Варианты дальше": "options",
    }), "id")
    gates = index(table(text, "Решения гейтов", {
        "Код гейта": "id", "Тип": "type", "Ключевой": "key", "Проверяет": "reviewer",
        "Решает": "deciders", "Исходы": "outcomes", "Запись решения": "record",
    }), "id")
    returns = index(table(text, "Возвраты маршрута", {
        "Причина возврата": "id", "Когда": "when", "Стадия возврата маршрута": "stage",
        **{track: track for track in FORMATS},
    }), "id")
    actions = table(text, "Действия после шага", {
        "Из шага": "source", "Формат действия": "format", "Действие": "name",
        "Когда": "when", "Допуск": "guard", "Подтверждённые условия": "facts", "Цель": "target",
    })
    stages = table(text, "Порядок вызовов по стадиям", {
        "Стадия маршрута": "stage", "Формат": "format",
        "Вызовы по порядку": "calls", "Выход": "output",
    })
    ain_steps = index(ain["steps"], "id")
    for code, step in ain_steps.items():
        step["check"] = handoff[code]["checkKind"]
    route = {"steps": steps, "gates": gates, "returns": returns, "actions": actions,
             "ain": ain_steps, "ain_version": ain["version"]}
    check_steps(route, kit, handoff)
    check_actions(route, stages)
    return route


def check_steps(route, kit, handoff):
    steps = route["steps"]
    require(list(steps) == [entry["step"].split()[0] for entry in kit],
            "Шаги и порядок должны совпадать с комплектом прогона")
    for number, (code, entry) in enumerate(zip(steps, kit), 1):
        step = steps[code]
        assigned = entry["system"] or entry["published" if entry["mode"] == "published" else "draft"]
        require(step["number"] == (str(number) if code != "Ш-С" else EMPTY), f"{code}: неверный номер")
        step["edition"] = edition(step["edition"])
        require(step["edition"] == assigned["sourcePath"] and step["mode"] == entry["mode"],
                f"{code}: редакция или режим расходятся с комплектом прогона")
        require(step["format"] == ("system" if entry["system"] else BOTH), f"{code}: неверный формат")
        require(step["gate"] == (entry["gate"].split(",")[0] if entry["gate"] else EMPTY),
                f"{code}: гейт расходится с комплектом прогона")
        require(not entry["params"] or step["params"] == f"`{entry['params']}`",
                f"{code}: нужен параметр прогона UC")
        step["check"] = handoff[code]["checkKind"]

    gates = route["gates"]
    require(set(gates) == set(GATE_OWNERS), "Не хватает гейта или указан неизвестный гейт")
    for code, gate in gates.items():
        kind = "гибрид" if code in ("AIN-21", "Г-IN") else "человек"
        require(gate["type"] == kind and gate["key"] == "да", f"{code}: неверный тип или ключевость")
        actual = gate["deciders"].removesuffix(" по процессу A-RELEASE").split(", ")
        require(set(actual) == GATE_OWNERS[code], f"{code}: неверная роль принятия решения")

    for reason, destination in route["returns"].items():
        for track in FORMATS:
            target = destination[track]
            if target != EMPTY:
                require(available(route, target, track), f"{reason}: {target} недоступен в {track}")
                stage = steps[target]["stage"] if target in steps else "A-IN"
                require(stage == destination["stage"], f"{reason}: неверная стадия {target}")
        require(any(destination[track] != EMPTY for track in FORMATS), f"{reason}: нет точки входа")


def slot(action, track):
    return action["format"] in (track, BOTH)


def check_actions(route, stages):
    paths = {}
    for track in FORMATS:
        chain = []
        for row in stages:
            if not slot(row, track):
                continue
            stage = row["stage"]
            if stage == "по запросу":
                require(row["calls"] == "Ш-С", "Ш-С доступен только по запросу")
                continue
            calls = row["calls"].split(" → ")
            if row["calls"] == "[AIN-01…AIN-24](bcreq-a-in-route.json)":
                require(track == "decomposed" and stage == "A-IN", "AIN доступен в своём формате")
                calls = list(route["ain"])
            for code in calls:
                require(available(route, code, track) and code != "Ш-С",
                        f"{code}: недоступный шаг в последовательности {track}")
                require(code not in chain, f"{code}: повторный шаг в последовательности {track}")
                require(route["steps"].get(code, {"stage": "A-IN"})["stage"] == stage,
                        f"{code}: неверная стадия {stage}")
                chain.append(code)
        expected = list(step for step in route["steps"] if step != "Ш-С" and available(route, step, track))
        if track == "decomposed":
            expected[1:1] = route["ain"]
        require(chain == expected, f"Неполная или неверно упорядоченная последовательность {track}")
        paths[track] = chain
    route["paths"] = paths

    for track, chain in paths.items():
        forward = {}
        seen = set()
        for row in route["actions"]:
            require(row["format"] in (*FORMATS, BOTH), f"Неизвестный формат: {row['format']}")
            if not slot(row, track):
                continue
            source, target, name, guard = (row[key] for key in ("source", "target", "name", "guard"))
            edge = (source, name, target)
            require(edge not in seen, f"Повторное действие {edge} ({track})")
            seen.add(edge)
            require(source == "*" or available(route, source, track),
                    f"{source}: неизвестный или недоступный источник в {track}")
            require(target in TERMINAL or target in {"текущий", "исходный"} or available(route, target, track),
                    f"{target}: неизвестная или недоступная цель в {track}")
            gate, _, outcome = guard.partition("/")
            require(guard in (EMPTY, "БА") or (
                gate in route["gates"] and outcome
                and outcome.casefold() in route["gates"][gate]["outcomes"].casefold()
            ), f"{source}: неизвестный допуск {guard}")
            require(name == "продолжить" or OTHER_TARGETS.get(name) == target,
                    f"{source}: неизвестное действие или недопустимая цель {name} → {target}")
            if name == "продолжить":
                require(source not in forward, f"{source}: два продолжения в {track}")
                forward[source] = target
                step = route["steps"].get(source)
                if source in ("AIN-21", "AIN-24"):
                    expected_guard = {"AIN-21": "AIN-21/allow", "AIN-24": "Г-IN/дальше"}[source]
                else:
                    require(step and source != "Ш-С", f"{source}: продолжение вне нормативного маршрута")
                    if step["gate"] != EMPTY:
                        expected_guard = "Г-IN/дальше" if step["gate"] == "Г-IN" else step["gate"] + "/согласование"
                    else:
                        expected_guard = "БА" if step["check"] == "required" else EMPTY
                require(guard == expected_guard, f"{source} → {target}: обход обязательной проверки или гейта")
            elif target == "BASELINE":
                require(source == "Ш-Р" and guard == "Выпуск/выпуск", "Обход гейта выпуска")
            elif target == "CS":
                cs_guards = {"Ш-1": "БА", "Ш-2": "Г-IN/CS", "AIN-24": "Г-IN/CS"}
                require(cs_guards.get(source) == guard, f"{source}: обход проверки выхода в CS")

        require(("Ш-Р", "выпустить", "BASELINE") in seen, "Нет конечного исхода выпуска")
        require(("*", "сценарии по запросу", "Ш-С") in seen and
                ("Ш-С", "вернуться в контекст", "исходный") in seen, "Ветка Ш-С неполна")
        for source, target in zip(chain, chain[1:]):
            if source in route["ain"] and source not in ("AIN-21", "AIN-24"):
                require(source not in forward and route["ain"][source]["next"] == target,
                        f"{source}: внутреннее продолжение задаёт маршрут A-IN")
            else:
                require(forward.pop(source, None) == target,
                        f"{source}: продолжение должно вести к {target} без обхода")
        require(not forward, f"Продолжение вне основной последовательности: {forward}")


def checked(state, source):
    revision = state["results"].get(source)
    require(revision and state["accepted"].get(source) == revision,
            f"{source}: нужно явное подтверждение БА для текущего результата")


def decision(route, state, source, gate, outcome):
    record = state["decisions"].get(gate, {})
    revision = state["results"].get(source)
    require(revision and record.get("explicit") and record.get("step") == source
            and record.get("outcome") == outcome and record.get("revision") == revision
            and record.get("locator") and record.get("date")
            and set(record.get("roles", [])) == GATE_OWNERS[gate],
            f"{gate}: нужен явный актуальный допуск ({outcome})")
    if source in route["ain"]:
        scope = state["scope"]
        signed = record.get("scope", {})
        require(all(scope.get(key) and signed.get(key) == scope[key] for key in SCOPE)
                and scope["route_version"] == route["ain_version"],
                f"{gate}: неверная задача, попытка, маршрут или snapshot")
        if gate == "AIN-21":
            require(record.get("report_version"), "AIN-21: нет версии отчёта")
    require(all(previous["revoked"].get(gate) != record for previous in state.get("returns", [])),
            f"{gate}: допуск отозван при возврате")


def check_sh3_input(route, state):
    """Check the two supported inputs to the common Ш-3 edition."""
    if state["format"] == "decomposed":
        decision(route, state, "AIN-21", "AIN-21", "allow")
        checked(state, "AIN-24")
        source = "AIN-24"
    else:
        checked(state, "Ш-2")
        source = "Ш-2"
    decision(route, state, source, "Г-IN", "дальше")


def navigate(route, state, action, target, *, reason=None):
    """Exercise a requested edge on a synthetic state, with no external effects."""
    track = state["format"]
    source = state["current"]
    require(track in FORMATS and available(route, source, track), f"{source}: нет активного шага в {track}")
    require(not any(state.get(key) for key in ("BLOCKED", "ACCESS_GAP", "critical_conflict")),
            "BLOCKED: устраните причину перед переходом")
    require(target in TERMINAL or available(route, target, track), f"{target}: недоступная цель в {track}")
    updated = deepcopy(state)
    if action == "вернуться":
        check_return(route, state, target, reason)
        chain = route["paths"][track]
        affected = chain[chain.index(target):]
        stale = updated.setdefault("stale", [])
        for step in affected:
            updated["accepted"].pop(step, None)
            if updated["results"].pop(step, None) and step not in stale:
                stale.append(step)
        revoked = {}
        for gate, record in state["decisions"].items():
            if record["step"] in affected:
                revoked[gate] = updated["decisions"].pop(gate)
        # В журнале исходные решения остаются доступными, но отозванные записи
        # больше не участвуют в проверке входа.
        updated.setdefault("returns", []).append({
            "source": source, "target": target, "reason": reason, "revoked": revoked,
        })
    else:
        if action == "вернуться в контекст":
            require(source == "Ш-С" and saved_context(state, target) == state.get("origin"),
                    "Ш-С: неверный исходный контекст")
            table_target = "исходный"
            updated.pop("origin")
        elif action.startswith("уточнить"):
            require(target == source, "Уточнение сохраняет текущий шаг")
            table_target = "текущий"
        else:
            table_target = target
        rows = [row for row in route["actions"]
                if slot(row, track) and row["name"] == action and row["target"] == table_target
                and row["source"] in (source, "*")]
        if action == "продолжить" and not rows and source in route["ain"]:
            require(route["ain"][source]["next"] == target, f"{source}: нет такого ребра A-IN")
            if route["ain"][source]["check"] == "required":
                checked(state, source)
            else:
                require(source in state["results"] and "ввод-промпта" in state["facts"],
                        f"{source}: нужен результат технического шага и следующий промпт")
        else:
            require(len(rows) == 1, f"{source}: недопустимое действие {action} → {target}")
            check_action(route, state, rows[0])
        if target == "Ш-С" and target != source:
            updated["origin"] = saved_context(state, source)
    updated["current"] = target
    return updated


def saved_context(state, step):
    return {"step": step, "format": state["format"], "revision": state["results"].get(step),
            "scope": state["scope"].copy()}


def check_action(route, state, row):
    source = state["current"]
    gate, _, outcome = row["guard"].partition("/")
    if gate == "БА" or (outcome and row["name"] in ("продолжить", "выпустить", "выйти в CS")):
        checked(state, source)
    if outcome:
        decision(route, state, source, gate, outcome)
    facts = set() if row["facts"] == EMPTY else set(row["facts"].split(", "))
    require(facts.issubset(state["facts"]), f"{source}: не подтверждены условия {sorted(facts - state['facts'])}")
    if row["name"] == "сценарии по запросу":
        require(source != "Ш-С" and source not in route["ain"], "Ш-С: контекст не допускает сценарии")
    if row["name"] == "уточнить с Заказчиком" and source in route["ain"]:
        require(source == "AIN-16", "Вопросы Заказчику в AIN — только через AIN-16")
    if row["name"] == "продолжить" and (row["target"] == "Ш-3" or source == "Ш-3"):
        try:
            check_sh3_input(route, state)
        except ValueError as error:
            raise ValueError(f"BLOCKED: вход Ш-3, {error}") from error


def check_return(route, state, target, reason):
    source = state["current"]
    track = state["format"]
    if source in route["ain"]:
        step = route["ain"][source]
        require(target in [*step["returns"], step["failure"]], f"{source}: нет возврата A-IN к {target}")
        require(reason, "Нужна причина возврата A-IN")
    else:
        choice = route["returns"].get(reason, {})
        chain = route["paths"][track]
        require(choice.get(track) == target and source in chain
                and chain.index(target) <= chain.index(source), f"{source}: нет возврата к {target} по причине {reason}")
    require("возврат-БА" in state["facts"], "БА должен выбрать точку возврата")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="вывести производный маршрут в stdout")
    args = parser.parse_args()
    try:
        route = load()
    except ValueError as error:
        parser.exit(1, f"{error}\n")
    if args.json:
        print(json.dumps(route, ensure_ascii=False, indent=2))
    else:
        print(f"BCREQ v0.3: {len(route['steps'])} шагов, {len(route['actions'])} действий, "
              f"{len(route['returns'])} причин возврата, A-IN {route['ain_version']}")


if __name__ == "__main__":
    main()
