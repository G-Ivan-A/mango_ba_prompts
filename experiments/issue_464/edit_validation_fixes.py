"""Issue #464: правки по итогам make validate-full. Одноразовая правка.

- чек-листы разделов 2, 3, 5 сведены к 7 пунктам: лимит 3–7 задан стандартом разделов;
- прежние поля классов сохранены в history.previous_fields: срез #405 снят до этих правок;
- допущена версия 0.7 RFC в регрессии #427;
- метка fields_changed_in: «issue #464» поставлена отдельной правкой: регрессия #433 сверяет только свою метку BL-159.
"""
import json
import subprocess
from pathlib import Path

from _edit import edit

ROOT = Path(__file__).resolve().parents[2]

edit("standards/bcreq-sections/02-business-context.md", [
    ("- [ ] Есть 2.1–2.4; 2.1 называет актора и ситуацию; 2.3 — одна фраза.\n"
     "- [ ] 2.1 называет акторов, сценарии и продукты Mango, на уровне которых зафиксирована проблема.\n",
     "- [ ] Есть 2.1–2.4; 2.3 — одна фраза; 2.1 называет акторов, сценарии и продукты Mango, на уровне которых зафиксирована проблема.\n"),
    ("записаны в 2.4.1 или 2.4.2.\n- [ ] Условия работы и сценарные исключения — в 6.2, а не в 2.4.\n",
     "записаны в 2.4.1 или 2.4.2; условия работы и сценарные исключения — в 6.2, а не в 2.4.\n"),
    ("вывод в эксплуатацию.\n- [ ] Ограничения платформы и версий — в 2.4.2 (кроме задач старой структуры).\n",
     "вывод в эксплуатацию; ограничения платформы и версий — в 2.4.2 (кроме задач старой структуры).\n"),
])
edit("standards/bcreq-sections/03-functional-requirements.md", [
    ("- [ ] Каждое ФТ проходит Ф1 (для В-Д), Ф2, Ф3, Ф4.\n"
     "- [ ] ФТ верхнего уровня 3–7 либо есть «Обоснование отклонения 5±2».\n"
     "- [ ] Каждое ФТ — по формуле «Система должна …» с субъектом и объектом.\n",
     "- [ ] Каждое ФТ проходит Ф1 (для В-Д), Ф2, Ф3, Ф4 и записано по формуле «Система должна …» с субъектом и объектом.\n"
     "- [ ] ФТ верхнего уровня 3–7 либо есть «Обоснование отклонения 5±2».\n"),
])
edit("standards/bcreq-sections/05-solution-description.md", [
    ("- [ ] Скобки покрытия стоят только на уровне 5.х, каждое ФТ раздела 3 указано хотя бы в одном пункте.\n"
     "- [ ] Каждое ФТ раздела 3 есть в таблице трассировки; нет строк L2 без строки L1.\n",
     "- [ ] Скобки покрытия стоят только на уровне 5.х; каждое ФТ раздела 3 указано хотя бы в одном пункте и в таблице трассировки; нет строк L2 без строки L1.\n"),
])
edit("scripts/validate_issue_427_r13_acceptance.py", [
    ('("0.3", "0.4", "0.5", "0.5.1", "0.6")', '("0.3", "0.4", "0.5", "0.5.1", "0.6", "0.7")'),
])

catalog_path = ROOT / "standards/bcreq-manual-classes/catalog.json"
raw = catalog_path.read_text(encoding="utf-8")
catalog = json.loads(raw)
upstream = json.loads(subprocess.run(
    ["git", "show", "upstream/main:standards/bcreq-manual-classes/catalog.json"],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout)
before = {item["id"]: item for item in upstream["classes"]}
for item in catalog["classes"]:
    old = before[item["id"]]
    changed = {key: old[key] for key in ("behavior", "stop") if item.get(key) != old.get(key)}
    if changed:
        previous = item["history"].setdefault("previous_fields", {})
        for key, value in changed.items():
            previous.setdefault(key, value)
catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
