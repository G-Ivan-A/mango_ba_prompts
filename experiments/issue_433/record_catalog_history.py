"""Записать в history каталога прежние значения полей, изменённых BL-159 (issue #433).

Каталог хранит прежний ID (history.previous_id, BL-153). По тому же правилу
BL-159 сохраняет прежние значения полей в history.previous_fields: срезы,
снятые с каталога до правки (experiments/issue_405), сверяются с ними, а
не переписываются. Идемпотентно: базовый срез — e1e9a3ea (main до #433).
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "standards/bcreq-manual-classes/catalog.json"
BASE = "e1e9a3eafbb01f0de9506b408af56562835dbea9"

old = json.loads(subprocess.run(
    ["git", "show", f"{BASE}:standards/bcreq-manual-classes/catalog.json"],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout)
data = json.loads(CATALOG.read_text())
before = {c["id"]: c for c in old["classes"]}
for item in data["classes"]:
    history = item.setdefault("history", {})
    history.pop("previous_name", None)
    history.pop("name_changed_in", None)
    prior = before[item["id"]]
    recorded = history.get("previous_fields", {})
    changed = {k: prior[k] for k in prior if k != "history" and prior[k] != item.get(k)}
    changed = {**changed, **recorded}
    if changed:
        history["previous_fields"] = dict(sorted(changed.items()))
        history["fields_changed_in"] = "BL-159 (issue #433)"
CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print({c["id"]: sorted(c["history"].get("previous_fields", {})) for c in data["classes"] if "previous_fields" in c["history"]})
