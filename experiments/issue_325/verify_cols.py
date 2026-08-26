"""Проверка: колонки 1–3 в новом L0 совпадают с исходной версией байт-в-байт."""
import re, subprocess, sys

def cols(text):
    app, res = 0, []
    for line in text.splitlines():
        if re.match(r"^## Лист «", line): app += 1; continue
        if app and line.startswith("|") and not line.startswith("| ---"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            res.append((app, tuple(c[:3])))
    return res

path = "runs/2026/RUN-0057/outputs/L0-customer-form-with-assessment.md"
old = cols(subprocess.run(["git","show",f"HEAD:{path}"],capture_output=True,text=True,check=True).stdout)
new = cols(open(path,encoding="utf-8").read())
assert len(old)==len(new), (len(old), len(new))
bad = [(o,n) for o,n in zip(old,new) if o!=n]
for o,n in bad: print("РАСХОЖДЕНИЕ:", o, "->", n)
# все строки таблиц ровно шестиколоночные
widths = set()
app=0
for line in open(path,encoding="utf-8"):
    if re.match(r"^## Лист «", line): app+=1; continue
    if app and line.startswith("|"):
        widths.add(len(line.strip().strip("|").split("|")))
print("ширины строк таблиц:", widths)
print("строк сравнено:", len(old), "| расхождений:", len(bad))
sys.exit(1 if bad or widths!={6} else 0)
