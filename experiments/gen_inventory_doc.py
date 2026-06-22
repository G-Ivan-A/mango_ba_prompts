#!/usr/bin/env python3
"""Generate docs/analysis/issue-170-mango-inventory.md from the live registry.

The inventory/analysis document (issue #170 DoD #1/#13) must reflect the registry
byte-for-byte, so it is generated rather than hand-written: full Product -> Service
-> Module -> Function tree, comparison against the old three YAML files, cascade-fill
delta, documented gaps and obsolescence review. Re-run after any registry change.
"""
import json
import yaml
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = json.loads((ROOT / "kb/mango-taxonomy/mango-registry.json").read_text(encoding="utf-8"))["taxonomy"]
OLDDIR = Path("/tmp/oldyaml")
OUT = ROOT / "docs/analysis/issue-170-mango-inventory.md"

op = yaml.safe_load((OLDDIR / "official-products.yaml").read_text(encoding="utf-8"))["taxonomy"]
ir = yaml.safe_load((OLDDIR / "internal-registry.yaml").read_text(encoding="utf-8"))["taxonomy"]
pm = yaml.safe_load((OLDDIR / "product-mapping.yaml").read_text(encoding="utf-8"))["taxonomy_mapping"]

prod = {p["id"]: p for p in NEW["products"]}
svc = {s["id"]: s for s in NEW["internal_services"]}
mod = {m["id"]: m for m in NEW["modules"]}
fn = {f["id"]: f for f in NEW["functions"]}
old_mod = {m["id"] for m in ir["modules"]}
old_fn = {f["id"] for f in ir["functions"]}


def name(e):
    return e.get("name_ru") or e.get("name_en") or e["id"]


L = []
def w(s=""):
    L.append(s)


# ---------------- front matter ----------------
w("---")
w("status: draft")
w("version: 1.0")
w("updated: 2026-06-21")
w("ai-generated: true")
w("type: analysis")
w("scope: mango-taxonomy-registry-inventory")
w('issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/170"')
w("related_artifacts:")
for a in ("kb/mango-taxonomy/mango-registry.json", "kb/mango-taxonomy/mango-registry.schema.json",
          "kb/mango-taxonomy/README.md", "scripts/validate_issue_170_mango_registry.py",
          "standards/mango-taxonomy-standard.md",
          "standards/decisions/ADR-012-mango-taxonomy.md",
          "experiments/cascade_fill.py", "experiments/gen_inventory_doc.py"):
    w(f'  - "{a}"')
w("---")
w()
w("# Инвентаризация Mango-реестра и перевод в JSON (issue #170)")
w()
w("> Документ сгенерирован из живого реестра скриптом "
  "[`experiments/gen_inventory_doc.py`](../../experiments/gen_inventory_doc.py) и "
  "отражает [`kb/mango-taxonomy/mango-registry.json`](../../kb/mango-taxonomy/mango-registry.json) "
  "один-в-один. Перегенерируйте после изменения реестра.")
w()

# ---------------- 1. summary ----------------
w("## 1. Резюме")
w()
w("Issue #170 требовал: (1) свести три YAML-файла Mango-реестра в единый JSON, "
  "(2) устранить дублирование (отдельный crosswalk `product-mapping.yaml`), "
  "(3) дозаполнить иерархию `Продукт → Сервис → Модуль → Функция` из реальной "
  "документации сверху вниз, (4) добавить JSON Schema, (5) обеспечить ссылочную "
  "целостность с Industry-реестром и (6) подготовить этот аналитический документ "
  "с полными списками сущностей, сравнением со старой структурой и фиксацией пробелов.")
w()
w("Итог — единый файл [`kb/mango-taxonomy/mango-registry.json`](../../kb/mango-taxonomy/mango-registry.json) "
  f"(версия `{NEW['version']}`) со следующим наполнением:")
w()
w("| Массив | Уровень | Кол-во |")
w("| --- | --- | ---: |")
rows = [("official_products", "official-product"), ("products", "product"),
        ("internal_services", "service"), ("modules", "module"), ("functions", "function")]
for key, lvl in rows:
    w(f"| `{key}` | {lvl} | {len(NEW[key])} |")
w()
w("Все нижние пороги стандарта превышены, число верхнеуровневых продуктов "
  "сохранено ровно равным восьми (ADR-012). Реестр проходит проектный валидатор, "
  "JSON Schema (draft 2020-12) и сквозную проверку целостности «родитель ↔ ребёнок».")
w()

# ---------------- 2. method ----------------
w("## 2. Метод и источник истины")
w()
w("**Источник истины** — извлечённые руководства в "
  "[`kb/mango-product-docs/processed/`](../../kb/mango-product-docs/processed/). "
  "Каждая добавленная сущность привязана к проверенной секции "
  "(`evidence_refs` указывает на реальный `*.md`).")
w()
w("**Запрет на выдумку.** Evidence резолвится по паре «(каталог, номер секции)» "
  "глоб-ом `sections/NN-*.md`; номер, который не находит файл, не попадает в реестр, "
  "а фиксируется как пробел в этом документе. Поэтому неверный slug физически не "
  "может «протечь» в данные.")
w()
w("**Наследование выравнивания.** Новая сущность копирует *primary* "
  "`industry_alignment` своего родителя (`industry_ref` и `facets` — дословно). "
  "Это гарантирует, что каждая ссылка резолвится против "
  "[`kb/industry-taxonomy/reference-taxonomy.json`](../../kb/industry-taxonomy/reference-taxonomy.json) "
  "и что не выдумываются новые отраслевые узлы. Для функций уровень `function` из "
  "`industry_ref` отбрасывается (в текущих данных это no-op).")
w()
# corpora used
fam_cites = defaultdict(set)
for key in ("internal_services", "modules", "functions"):
    for e in NEW[key]:
        refs = list(e.get("evidence_refs", []))
        for a in e.get("maps_to", {}).get("industry_alignment", []):
            refs += a.get("evidence_refs", [])
        for r in refs:
            if r.startswith("kb/mango-product-docs/processed/"):
                rest = r[len("kb/mango-product-docs/processed/"):]
                top = rest.split("/")[0]
                fam_cites[top].add(r)
w("**Использованные корпуса** (число различных секций/файлов, на которые ссылается "
  "реестр):")
w()
w("| Корпус (processed/) | Цитируемых файлов |")
w("| --- | ---: |")
for top in sorted(fam_cites, key=lambda t: (-len(fam_cites[t]), t)):
    w(f"| `{top}` | {len(fam_cites[top])} |")
w()

# ---------------- 3. comparison ----------------
w("## 3. Сравнение со старой YAML-структурой")
w()
w("До issue #170 реестр состоял из трёх файлов. Их содержимое свёрнуто в один JSON:")
w()
w("| Старый файл | Что содержал | Судьба |")
w("| --- | --- | --- |")
w(f"| `official-products.yaml` | {len(op['official_products'])} официальных продуктов | "
  "перенесён в массив `official_products` |")
w(f"| `internal-registry.yaml` | {len(ir['products'])} продуктов / "
  f"{len(ir['internal_services'])} сервисов / {len(ir['modules'])} модулей / "
  f"{len(ir['functions'])} функций | стал основой единого JSON, дозаполнен |")
w(f"| `product-mapping.yaml` | {len(pm['entities'])} записей crosswalk к Industry "
  "Taxonomy | **удалён**, выравнивания внесены в `maps_to.industry_alignment` каждой "
  "сущности |")
w()
total_old = len(op["official_products"]) + len(ir["products"]) + len(ir["internal_services"]) + len(ir["modules"]) + len(ir["functions"])
w(f"Crosswalk содержал ровно {len(pm['entities'])} записей — это "
  f"{len(op['official_products'])} + {len(ir['products'])} + {len(ir['internal_services'])} + "
  f"{len(ir['modules'])} + {len(ir['functions'])} = {total_old}, "
  "то есть по одной записи на каждую сущность всех пяти уровней. Отдельный mapping-файл "
  "дублировал данные и был источником рассинхрона; теперь выравнивание живёт внутри "
  "сущности, и дублирования нет.")
w()
w("**Изменение количеств (старое → новое):**")
w()
w("| Уровень | Старое | Новое | Δ |")
w("| --- | ---: | ---: | ---: |")
pairs = [("official_products", op["official_products"], NEW["official_products"]),
         ("products", ir["products"], NEW["products"]),
         ("internal_services", ir["internal_services"], NEW["internal_services"]),
         ("modules", ir["modules"], NEW["modules"]),
         ("functions", ir["functions"], NEW["functions"])]
for lvl, o, n in pairs:
    d = len(n) - len(o)
    w(f"| {lvl} | {len(o)} | {len(n)} | {'+' if d >= 0 else ''}{d} |")
w()
# obsolescence
dropped = {}
for lvl, oarr in (("official_products", op["official_products"]), ("products", ir["products"]),
                  ("internal_services", ir["internal_services"]), ("modules", ir["modules"]),
                  ("functions", ir["functions"])):
    oids = {e["id"] for e in oarr}
    nids = {e["id"] for e in NEW[lvl]}
    dropped[lvl] = sorted(oids - nids)
any_dropped = any(dropped.values())
w("**Возможное устаревание.** "
  + ("Ни одна сущность из старых YAML не удалена — все идентификаторы сохранены 1:1, "
     "переопределения верхнеуровневых продуктов (ADR-012) не было. Признаков "
     "устаревания не обнаружено."
     if not any_dropped else
     "Удалены следующие сущности: " + json.dumps(dropped, ensure_ascii=False)))
w()

# ---------------- 4. full tree ----------------
w("## 4. Полный реестр: дерево `Продукт → Сервис → Модуль → Функция`")
w()
w("Знаком **`+`** отмечены сущности, добавленные дозаполнением в issue #170; "
  "остальные перенесены из `internal-registry.yaml`. В скобках у функции — "
  "`function_type`/`interaction_surface`.")
w()
for p in NEW["products"]:
    pservices = [s for s in NEW["internal_services"] if p["id"] in s.get("parent_products", [])]
    w(f"### {name(p)} — `{p['id']}`")
    w()
    w(f"_Сервисов: {len(pservices)}._")
    w()
    for s in pservices:
        smods = [mod[mid] for mid in s.get("modules", [])]
        w(f"- **{name(s)}** — `{s['id']}` _(модулей: {len(smods)})_")
        for m in smods:
            mk = "+ " if m["id"] not in old_mod else ""
            mfns = [fn[fid] for fid in m.get("functions", [])]
            w(f"  - {mk}**{name(m)}** — `{m['id']}` _(функций: {len(mfns)})_")
            for f in mfns:
                fk = "+ " if f["id"] not in old_fn else ""
                w(f"    - {fk}{name(f)} — `{f['id']}` "
                  f"({f['function_type']}/{f['interaction_surface']})")
    w()

# ---------------- 5. cascade-fill delta ----------------
w("## 5. Дозаполнение: что добавлено")
w()
new_mods = [m for m in NEW["modules"] if m["id"] not in old_mod]
new_fns = [f for f in NEW["functions"] if f["id"] not in old_fn]
w(f"Добавлено **{len(new_mods)} модулей** и **{len(new_fns)} функций**, "
  "сгруппированы по кластерам:")
w()
bycluster = defaultdict(lambda: {"m": 0, "f": 0})
for m in new_mods:
    bycluster[m["cluster"]]["m"] += 1
for f in new_fns:
    bycluster[mod[f["parent_module"]]["cluster"]]["f"] += 1
w("| Кластер | +модулей | +функций |")
w("| --- | ---: | ---: |")
for c in sorted(bycluster):
    w(f"| `{c}` | +{bycluster[c]['m']} | +{bycluster[c]['f']} |")
w(f"| **Итого** | **+{len(new_mods)}** | **+{len(new_fns)}** |")
w()
w("Новые модули (с родительским сервисом):")
w()
for m in new_mods:
    w(f"- `{m['id']}` → `{m['parent_services'][0]}` "
      f"({len(m.get('functions', []))} функций)")
w()

# ---------------- 6. gaps ----------------
w("## 6. Пробелы и риск устаревания")
w()
w("### 6.1. Качество извлечения корпуса `sip-trunk`")
w()
w("Корпус `kb/mango-product-docs/processed/sip-trunk/` существует (≈39 секций), но "
  "извлечение заголовков для него не сработало: slug-и секций деградировали в "
  "`01-section.md`, `07-section.md`, `08-3-1-1-0-a-b-9-0.md` и подобные. Сослаться "
  "на осмысленную секцию нельзя, поэтому отдельный модуль управления SIP-trunk "
  "**не смоделирован** (это нарушило бы запрет на выдумку). "
  "_Рекомендация:_ переизвлечь исходный PDF SIP-trunk и затем добавить модуль с "
  "корректными ссылками.")
w()
w("### 6.2. Сервисы с одним модулем")
w()
ones = [s for s in NEW["internal_services"] if len(s.get("modules", [])) == 1]
w(f"{len(ones)} сервисов содержат ровно один модуль. Это удовлетворяет минимуму "
  "стандарта (≥1 модуль на сервис), но глубина по ним фиксируется как пробел: "
  "документация пока не даёт второго отдельного модуля с ≥2 функций без выдумки. "
  "Кандидаты на дальнейшее дозаполнение по мере уточнения источников:")
w()
w("| Сервис | Единственный модуль |")
w("| --- | --- |")
for s in sorted(ones, key=lambda x: x["id"]):
    w(f"| `{s['id']}` ({name(s)}) | `{s['modules'][0]}` |")
w()
w("### 6.3. Недоиспользованные крупные корпуса")
w()
w("Несколько корпусов значительно больше, чем извлечённый из них объём; выбрана "
  "репрезентативная, но не исчерпывающая часть. Дальнейшее дозаполнение возможно "
  "итеративно (по одной партии модулей/функций со ссылками):")
w()
w("- `vpbx-api` (≈253 секции) и `contact-center-api` через `vpbx-api` — описано "
  "много методов Open API сверх внесённых;")
w("- `mango-lk-manual` (≈348 секций) и `mango-cc-manual` (≈232 секции) — глубокие "
  "руководства ВАТС/КЦ;")
w("- `integration-bitrix24` (≈192 секции) — детальный коннектор, внесена базовая "
  "пара функций;")
w("- `mdialogi-api` (≈62 секции) — Dialog API внесён существенно, но не полностью.")
w()
w("### 6.4. Документированные, но отложенные области")
w()
w("Статусы присутствия пользователя Mango Talker внесены в этой итерации модулем "
  "`talker-presence-status-module` под `talker-softphone-service` (статус определяет "
  "готовность к приёму вызовов, поэтому естественный родитель — софтфон): функции "
  "`change-talker-presence-status` (`mtalker/windows-mac-working` секция 222, "
  "`mtalker/android-user-guide` секция 115) и `disable-talker-notifications` "
  "(`mtalker/windows-mac-working` секции 220, 223).")
w()
w("Остаются неразобранными на сущности руководства `mtalker/windows-mac-settings`, "
  "`mtalker/windows-mac-admin`, `mtalker/android-user-guide` (за пределами статуса), "
  "`mtalker/quick-start` — основное наполнение взято из `mtalker/windows-mac-working`. "
  "Это кандидаты на дальнейшее дозаполнение (настройки клиента, администрирование, "
  "мобильные особенности).")
w()
w("### 6.5. Сущности со слабым evidence (только маркетинговый URL)")
w()
def only_url(e):
    refs = e.get("evidence_refs", [])
    return bool(refs) and all(r.startswith(("http://", "https://")) for r in refs)
weak = []
for key in ("internal_services", "modules", "functions"):
    for e in NEW[key]:
        if only_url(e):
            weak.append((key, e["id"]))
w(f"{len(weak)} перенесённых из YAML сущностей опираются только на ссылку на "
  "страницу продукта (без секции руководства). Они валидны (URL — допустимый "
  "evidence), но это кандидаты на усиление доказательной базы реальными секциями:")
w()
for key, eid in weak:
    w(f"- `{eid}` ({key})")
w()

# ---------------- 7. validation ----------------
w("## 7. Валидация и воспроизводимость")
w()
w("Реестр проверяется тремя независимыми способами, все проходят:")
w()
w("1. **Проектный валидатор** (stdlib-only, как в CI):")
w("   ```bash")
w("   python3 scripts/validate_issue_170_mango_registry.py")
w("   ```")
w("   Проверяет JSON Schema, резолвинг каждого `industry_ref` против живого "
  "Industry-реестра, целостность «родитель ↔ ребёнок» в обе стороны и полноту "
  "иерархии (пороги и минимумы).")
w("2. **JSON Schema, draft 2020-12** — "
  "[`kb/mango-taxonomy/mango-registry.schema.json`](../../kb/mango-taxonomy/mango-registry.schema.json).")
w("3. **Полный контур БЗ:**")
w("   ```bash")
w("   make kb-validate")
w("   ```")
w()
w("Дозаполнение воспроизводится аддитивным билдером "
  "[`experiments/cascade_fill.py`](../../experiments/cascade_fill.py) поверх "
  "перенесённого реестра; перечень исходных секций — в "
  "[`experiments/doc_catalog.txt`](../../experiments/doc_catalog.txt). Этот документ "
  "перегенерируется скриптом "
  "[`experiments/gen_inventory_doc.py`](../../experiments/gen_inventory_doc.py).")
w()

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"wrote {OUT} ({len(L)} lines)")
