"""Issue #434, PR #437 comment (2026-11-03): inventory of the industry (international/market)
classification layer in the Hub research and how it links to the spoke catalog.

Usage: python3 -I industry_taxonomy_inventory.py <hub_clone> <spoke_root> <runtime_clone>
Read-only; prints facts used in RFC-RT-001 section 12.
"""
import collections, json, re, subprocess, sys
from pathlib import Path

hub, spoke, rt = map(Path, sys.argv[1:4])
cls = (hub / "research/mango/2026-05-22-classification.md").read_text()
dec = (hub / "research/mango/2026-05-27-capability-decomposition.md").read_text()
cat = json.loads((spoke / "docs/taxonomy/products.json").read_text())
nodes = cat["nodes"]

print("hub HEAD:", subprocess.run(["git", "-C", str(hub), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
same = subprocess.run(["git", "-C", str(hub), "diff", "--quiet", "cd5d6e4b72700e43ccca6c96119308ab5a6d7379", "HEAD", "--",
                       "research/mango/2026-05-22-classification.md"]).returncode == 0
print("classification.md unchanged since catalog source commit cd5d6e4b:", same)

# 1. International comparative table: rows with TM Forum + UNSPSC columns
sec = cls.split("## Сравнительная таблица международной классификации", 1)[1].split("\n## ", 1)[0]
rows = [l for l in sec.splitlines() if re.match(r"^\| *\d+ *\|", l)]
print("international table rows:", len(rows), "columns:", sec.split("\n| №", 1)[1].split("\n", 1)[0].count("|"))
unspsc = sorted({c for l in rows for c in re.findall(r"\b(\d{8})\b", l)})
print("distinct UNSPSC codes in table:", len(unspsc))
sec_ru = cls.split("## Сравнительная таблица к российским стандартам", 1)[1].split("\n## ", 1)[0]
rows_ru = [l for l in sec_ru.splitlines() if re.match(r"^\| *\d+ *\|", l)]
print("russian table rows (ОКПД 2 / ГОСТ / НПА):", len(rows_ru))
print("working taxonomy fields (4 keys):", re.findall(r"^\| (TM Forum domain|TM Forum capability|UNSPSC code|ОКПД 2 class|Russian standards overlay) \|", cls, re.M))

# 2. Spoke catalog bridge: Capability.row -> table row
caps = [n for n in nodes if n["level"] == "Capability"]
with_row = [n for n in caps if "row" in n]
print(f"spoke capabilities: {len(caps)}, with row -> international table: {len(with_row)}; without: {[n['id'] for n in caps if 'row' not in n]}")
print("industry fields stored in spoke catalog nodes:", sorted(k for k in {k for n in nodes for k in n} if re.search(r"tm|unspsc|okpd|industry|market", k, re.I)) or "none")

# 3. Atomic-function level: international_sources in capability-decomposition
blocks = re.findall(r"- id: \"([a-z0-9-]+)\"(.*?)(?=\n  - id: |\n```)", dec, re.S)
fids = [b[0] for b in blocks]
srcs = collections.Counter()
vend = collections.Counter()
for _, body in blocks:
    m = re.search(r"international_sources:(.*?)(?:\n    [a-z_]+:|\Z)", body, re.S)
    for s in re.findall(r"\"([^\"]+)\"", m.group(1) if m else ""):
        srcs[s.split(":")[0].strip()] += 1
cat_f = {n["id"].split("/")[-1] for n in nodes if n["level"] == "Atomic Function"}
print(f"capability-decomposition atomic functions: {len(fids)} ({len(set(fids))} unique); in spoke catalog by short id: {len(set(fids) & cat_f)}")
print("international_sources by source family (top 15):")
for k, v in srcs.most_common(15):
    print(f"  {v:3d} {k}")

# 4. Runtime: any industry mapping?
hits = subprocess.run(["grep", "-rIl", "-E", "-i", "TM Forum|UNSPSC|ОКПД|industry|tm_forum", str(rt)], capture_output=True, text=True).stdout.split()
print("runtime files mentioning TM Forum/UNSPSC/ОКПД/industry:", [str(Path(h).relative_to(rt)) for h in hits if "/.git/" not in h] or "none")
