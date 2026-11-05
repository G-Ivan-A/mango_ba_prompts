#!/usr/bin/env python3
"""Issue #452: read-only comparison of the site on main with production.

Run from the repository root: python3 experiments/issue_452/audit_publication.py
"""
import json
import re
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

PROD = "https://g-ivan-a.github.io/mango_ba_prompts/"
FILES = ["index.html", "app.js", "v2.js", "v2.css", "data/stats.json", "data/prompts.json",
         "data/bcreq-flow.json", "data/test-kit.json", "data/checks.json"]


def fetch(path):
    try:
        with urllib.request.urlopen(PROD + path, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        return None if error.code == 404 else (_ for _ in ()).throw(error)


def pages(html):
    return sorted(set(re.findall(r'data-page="([^"]+)"', html)))


def summary(prompts, kit):
    items = prompts["prompts"]
    steps = kit["steps"] if kit else []
    return {
        "generatedAt": prompts["generatedAt"],
        "siteVersion": prompts.get("siteVersion", {}).get("version"),
        "classes": sum(1 for p in items if p.get("classId")),
        "archive": sum(1 for p in items if p.get("archived")),
        "kit_steps": len(steps),
        "kit_drafts_with_text": sorted(s["draft"]["file"] for s in steps if s.get("draft")),
    }


local = {f: (Path("site") / f).read_bytes() for f in FILES}
remote = {f: fetch(f) for f in FILES}
print("## Files: production vs main")
for name in FILES:
    size = "404" if remote[name] is None else len(remote[name])
    print(f"{name}: prod={size} main={len(local[name])} same={remote[name] == local[name]}")

print("\n## Content")
main = summary(json.loads(local["data/prompts.json"]), json.loads(local["data/test-kit.json"]))
prod_kit = remote["data/test-kit.json"]
prod = summary(json.loads(remote["data/prompts.json"]), json.loads(prod_kit) if prod_kit else None)
print("main:", json.dumps(main, ensure_ascii=False))
print("prod:", json.dumps(prod, ensure_ascii=False))

print("\n## Pages (data-page)")
main_pages, prod_pages = pages(local["index.html"].decode()), pages(remote["index.html"].decode())
print("main:", main_pages)
print("prod:", prod_pages)
print("missing on prod:", sorted(set(main_pages) - set(prod_pages)))
print("nav on main:", re.findall(r'data-nav="([^"]+)"', local["index.html"].decode()))
print("nav on prod:", re.findall(r'data-nav="([^"]+)"', remote["index.html"].decode()))

print("\n## Profiles (standards/bcreq-prompt-profiles.md, section 3)")
table = re.findall(r"^\| (К-\d\d) \|.*\| ([A-Z]+) \|$",
                   Path("standards/bcreq-prompt-profiles.md").read_text(), re.M)
profile = dict(table)
print("operations mapped:", len(profile), dict(sorted(Counter(profile.values()).items())))
for label, raw in (("main", local), ("prod", remote)):
    ids = {p["classId"] for p in json.loads(raw["data/prompts.json"])["prompts"] if p.get("classId")}
    print(f"{label}: operations with a catalog card per profile:",
          dict(sorted(Counter(profile[i] for i in ids if i in profile).items())))
    print(f"{label}: word 'profile' exposed in prompt fields:",
          any("profile" in key.lower() for p in json.loads(raw["data/prompts.json"])["prompts"] for key in p))

print("\n## By-test drafts (prompts/drafts/manifest.json)")
drafts = json.loads(Path("prompts/drafts/manifest.json").read_text())["drafts"]
kit_files = {Path(s["draft"]["file"]).name for s in json.loads(local["data/test-kit.json"])["steps"] if s.get("draft")}
for draft in drafts:
    name = Path(draft["file"]).name
    print(f"{name}: steps={draft['steps']} profiles={draft['profiles']} text_on_site_main={name in kit_files}")
covered = {x for d in drafts for x in d["profiles"]}
on_site = {x for d in drafts if Path(d["file"]).name in kit_files for x in d["profiles"]}
print("profiles in drafts:", sorted(covered), "| with a draft on main site:", sorted(on_site))

print("\n## Prompts outside the publication boundary (prompts/*.md, not bcreq-*)")
print(sorted(p.name for p in Path("prompts").glob("*.md") if not p.name.startswith("bcreq-")))
print("site/reports on prod:", "absent" if fetch("reports/index.html") is None else "present")
