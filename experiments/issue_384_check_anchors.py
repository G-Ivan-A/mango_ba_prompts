#!/usr/bin/env python3
"""Issue #384: print the target line of every snapshot `?plain=1#L<n>` anchor in the audit report."""
import re, subprocess, sys
SHA = "dbf1d3c58ca5a4c145929e644b2b31803b0ea11d"
DOC = sys.argv[1] if len(sys.argv) > 1 else "docs/analysis/2026-10-23-prompts-catalog-audit.md"
text = open(DOC, encoding="utf-8").read()
rx = re.compile(rf"https://github\.com/G-Ivan-A/mango_ba_prompts/blob/{SHA}/([^\s)?#]+)(?:\?plain=1)?(?:#L(\d+))?")
seen = set()
bad = 0
for path, line in rx.findall(text):
    if (path, line) in seen:
        continue
    seen.add((path, line))
    r = subprocess.run(["git", "show", f"{SHA}:{path}"], capture_output=True, text=True)
    if r.returncode:
        print(f"MISSING {path}"); bad += 1; continue
    if line:
        lines = r.stdout.splitlines()
        n = int(line)
        if n > len(lines):
            print(f"OUT-OF-RANGE {path}#L{n} ({len(lines)})"); bad += 1; continue
        print(f"{path.split('/')[-1][:40]:<40} L{n:<4} {lines[n-1][:150]}")
print("bad:", bad)
