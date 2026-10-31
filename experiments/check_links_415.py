import re, sys
from pathlib import Path
sys.path.insert(0, "scripts")
from validate_issue_409_audit_artifacts import anchors, LINK
ROOT = Path(".").resolve()
doc = ROOT / sys.argv[1]
text = doc.read_text(encoding="utf-8")
bad = 0
for target in LINK.findall(text):
    if target.startswith(("http://", "https://", "mailto:")):
        continue
    path, _, frag = target.partition("#")
    p = (doc.parent / path).resolve() if path else doc
    if not p.exists():
        print("MISSING", target); bad += 1; continue
    if frag and p.suffix == ".md" and frag not in anchors(p):
        print("ANCHOR", target); bad += 1
print("bad:", bad)
