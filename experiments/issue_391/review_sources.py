"""Summarize all source rows for review without copying customer quotations."""
from pathlib import Path
import re
import json
import hashlib
root = Path(__file__).resolve().parents[2]
for run in ('0073', '0074', '0075', '0076'):
    folder = root / 'runs/2026' / f'RUN-{run}'
    print(f'RUN-{run}')
    for path in sorted((folder / 'outputs').glob('*.md')):
        if not any(k in path.name for k in ('success-criteria','how-not-to-do','error-statistics','golden-set-candidates')):
            continue
        print(path.relative_to(root))
        for line in path.read_text().splitlines():
            if line.startswith('#'):
                print(line)
            elif line.startswith('| SC-'):
                cols = line.split('|')
                print(' | '.join(cols[1:6]))
            elif line.startswith('| C'):
                print(line)
            elif re.match(r'\| GS-', line):
                cols = line.split('|')
                # Hide only the quoted input; preserve verdict and reasoning.
                print(' | '.join([cols[1], *cols[3:]]))
            elif line.startswith('| N-'):
                cols = line.split('|')
                print(' | '.join(cols[1:6] + cols[7:]))
