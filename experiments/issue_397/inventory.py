"""Read-only inventory of recent RUN evidence, independent of PR summaries."""
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
rows = []
for n in range(73, 77):
    base = ROOT / f'runs/2026/RUN-{n:04d}/outputs'
    data = json.loads((base / 'golden-set-candidates.json').read_text())
    cases = [case for group in data['sets'] for case in group['cases']]
    criteria = set(re.findall(r'\bSC-\d+\b', (base / 'success-criteria.md').read_text()))
    rows.append({'run': f'RUN-{n:04d}', 'status': data['status'], 'sets': len(data['sets']),
                 'cases': len(cases), 'success_criteria': len(criteria),
                 'confirmed_by': dict(Counter(case['confirmed_by'] for case in cases)),
                 'kinds': dict(Counter(case['kind'] for case in cases))})
result = {'runs': rows, 'total_cases': sum(r['cases'] for r in rows),
          'total_success_criteria': sum(r['success_criteria'] for r in rows),
          'meaning': 'confirmed_by records source-case confirmation, not approval of the entire draft golden set.'}
Path(__file__).with_name('run-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(f"PASS: {result['total_success_criteria']} criteria; {result['total_cases']} candidates")
