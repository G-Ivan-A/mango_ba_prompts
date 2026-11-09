#!/usr/bin/env python3
"""Print the existing #476 Playwright MCP smoke with current checkout paths."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'experiments/issue_476/browser-smoke.js').read_text()
shots = ROOT / 'site/screenshots/issue-480'
shots.mkdir(parents=True, exist_ok=True)
print(re.sub(r"  const shots = '[^']+';", f'  const shots = {json.dumps(str(shots) + "/")};', source))
