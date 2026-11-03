"""BL-159 (issue #433): тип гейта в каталоге и стандартах классов.

Идемпотентно: повторный запуск ничего не меняет.
- К-20: имя «Подготовка доказательств гейта», вход gate_type?.
- К-34: поля журнала gate_id, gate_type, model_recommendation, divergence.
- 39 стандартов: строка самопроверки называет тип гейта; версия 0.1.1 → 0.1.2.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLASSES = ROOT / "standards/bcreq-manual-classes"
CATALOG = CLASSES / "catalog.json"
README = CLASSES / "README.md"
PROCESS = ROOT / "docs/ba-processes/bcreq-manual-process.md"

OLD_SELF = "Самопроверка не меняет полномочия и не проходит человеческие гейты."
NEW_SELF = (
    "Самопроверка не меняет полномочия и не проходит гейты с решением\n"
    "человека (тип `человек` или `гибрид`, в том числе ключевые)."
)

K20_OLD_NAME = "Подготовка доказательств человеческого гейта"
K20_NAME = "Подготовка доказательств гейта"
K20_OLD_IN = "gate_id, candidate_revision, applicable_gate_contract, checklist_evidence, human_records"
K20_IN = "gate_id, gate_type, candidate_revision, applicable_gate_contract, checklist_evidence, human_records"
K20_OLD_BEH_TAIL = "Роли и решение берутся от человека."
K20_BEH_TAIL = (
    "Тип гейта (`человек`, `гибрид`, `llm`, `код`) и ключевость — по словарю потока; "
    "для `человек` и `гибрид` роли и решение берутся от человека, recommendation — только рекомендация."
)

K34_OLD_IN = "human_message, actor_role, authority, candidate_revision, scope, timestamp"
K34_IN = "human_message, actor_role, authority, candidate_revision, scope, timestamp, gate_id?, gate_type?, model_recommendation?"
K34_OLD_OUT = "section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status}"
K34_OUT = "section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status,gate_id,gate_type,model_recommendation,divergence}"
K34_OLD_BEH_TAIL = "после изменения кандидата зависимое одобрение stale."
K34_BEH_TAIL = (
    "после изменения кандидата зависимое одобрение stale. "
    "Для решения гейта записать gate_id и gate_type; для `гибрид` — model_recommendation "
    "и divergence (совпало или расходится, с причиной): это журнал для решения о типе гейта."
)


def sub_once(text, old, new, where):
    if new in text and old not in text:
        return text
    count = text.count(old)
    assert count >= 1, (where, old[:60])
    return text.replace(old, new)


def catalog():
    data = json.loads(CATALOG.read_text())
    for item in data["classes"]:
        if item["id"] == "К-20":
            item["name"] = K20_NAME
            item["inputs"] = K20_IN
            if K20_BEH_TAIL not in item["behavior"]:
                item["behavior"] = item["behavior"].replace(K20_OLD_BEH_TAIL, K20_BEH_TAIL)
            item.setdefault("history", {})["previous_name"] = K20_OLD_NAME
            item["history"]["name_changed_in"] = "BL-159 (issue #433)"
        if item["id"] == "К-34":
            item["inputs"] = K34_IN
            item["outputs"] = K34_OUT
            if K34_BEH_TAIL not in item["behavior"]:
                item["behavior"] = item["behavior"].replace(K34_OLD_BEH_TAIL, K34_BEH_TAIL)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return {x["id"]: x for x in data["classes"]}


def k34_example(text):
    old = '"status": "pending"\n  }\n}'
    new = (
        '"status": "pending",\n'
        '    "gate_id": null,\n'
        '    "gate_type": null,\n'
        '    "model_recommendation": null,\n'
        '    "divergence": null\n  }\n}'
    )
    if '"divergence"' in text:
        return text
    assert text.count(old) == 1
    text = text.replace(old, new)
    old_in = '"timestamp": "<передать timestamp>"\n'
    new_in = (
        '"timestamp": "<передать timestamp>",\n'
        '    "gate_id": "<передать gate_id или null>",\n'
        '    "gate_type": "<передать gate_type или null>",\n'
        '    "model_recommendation": "<передать model_recommendation или null>"\n'
    )
    assert text.count(old_in) == 1
    return text.replace(old_in, new_in)


def k20_example(text):
    old = '"gate_id": "<передать gate_id>",\n'
    new = old + '    "gate_type": "<передать gate_type>",\n'
    if '"gate_type"' in text:
        return text
    assert text.count(old) == 1, "К-20 example"
    return text.replace(old, new)


def standards(entries):
    for path in sorted(CLASSES.glob("[0-9][0-9]-*.md")):
        text = path.read_text()
        before = text
        text = sub_once(text, OLD_SELF, NEW_SELF, path.name)
        if path.name.startswith("20-"):
            text = sub_once(text, K20_OLD_NAME, K20_NAME, path.name)
            text = sub_once(text, "подготовка доказательств человеческого гейта", "подготовка доказательств гейта", path.name)
            text = sub_once(text, f"`{K20_OLD_IN}`", f"`{K20_IN}`", path.name)
            text = sub_once(text, K20_OLD_BEH_TAIL, K20_BEH_TAIL, path.name)
            text = k20_example(text)
        if path.name.startswith("34-"):
            text = sub_once(text, f"`{K34_OLD_IN}`", f"`{K34_IN}`", path.name)
            text = sub_once(text, f"`{K34_OLD_OUT}`", f"`{K34_OUT}`", path.name)
            text = sub_once(text, K34_OLD_BEH_TAIL, K34_BEH_TAIL, path.name)
            text = k34_example(text)
        if text != before:
            text = re.sub(r"^version: 0\.1\.1$", "version: 0.1.2", text, count=1, flags=re.M)
            path.write_text(text)


def safe(text, old, new):
    """Заменить, если новое значение ещё не записано (идемпотентность)."""
    return text if new in text else text.replace(old, new)


def index():
    for path in (README, PROCESS):
        text = path.read_text()
        text = text.replace(K20_OLD_NAME, K20_NAME)
        text = safe(text, K20_OLD_IN, K20_IN)
        text = safe(text, K34_OLD_IN, K34_IN)
        text = safe(text, K34_OLD_OUT, K34_OUT)
        path.write_text(text)


if __name__ == "__main__":
    entries = catalog()
    standards(entries)
    index()
    print("ok")
