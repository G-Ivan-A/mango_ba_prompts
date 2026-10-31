"""Helper: grep lesson keyword patterns across artifact groups (read-only)."""
import glob, re, sys, json, os
ROOT = "/tmp/gh-issue-solver-1793457454005"
GROUPS = {
  "a": sorted(glob.glob(ROOT+"/standards/bcreq-manual-classes/[0-9]*.md"))+[ROOT+"/standards/bcreq-manual-classes/README.md", ROOT+"/standards/bcreq-manual-classes/catalog.json"],
  "b": [ROOT+"/docs/contracts/bcreq-manual-state.md", ROOT+"/docs/contracts/bcreq-stage-gates.md"],
  "c": sorted(glob.glob(ROOT+"/prompts/bcreq-*.md")),
  "d": sorted(glob.glob(ROOT+"/standards/bcreq-sections/*.md")),
  "old": sorted(glob.glob(ROOT+"/prompts/archive/*.md"))+sorted(p for p in glob.glob(ROOT+"/prompts/*.md") if "/bcreq-" not in p),
}
def run(pattern, groups="abcdold", maxper=6, width=230):
    rx = re.compile(pattern, re.I)
    for g in groups if groups!="abcdold" else ["a","b","c","d","old"]:
        hits=[]
        for f in GROUPS[g]:
            try: lines=open(f,encoding="utf-8").read().split("\n")
            except Exception: continue
            for i,l in enumerate(lines,1):
                if re.match(r"^\[[A-Za-z0-9-]+\]: ", l): continue
                if rx.search(l): hits.append((os.path.relpath(f,ROOT),i,l.strip()))
        print(f"  [{g}] {len(hits)} hits")
        for h in hits[:maxper]:
            print(f"    {h[0]}:{h[1]}: {h[2][:width]}")
if __name__=="__main__":
    spec=json.load(open(sys.argv[1]))
    for k,v in spec.items():
        print("##",k,v if isinstance(v,str) else v[0])
        if isinstance(v,str): run(v)
        else: run(v[0], maxper=v[1])
