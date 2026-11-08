#!/usr/bin/env python3
"""Проверка аудита #470: каталоги граничных случаев, источники, имена docs/rfc, сборка сайта."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = 'docs/audit/2026-11-07-bcreq-ttz-rfc-audit.md'
AIN = 'docs/rfc/2026-11-a-in-decomposition.md'
TTZ = 'docs/rfc/2026-11-ttz-feasibility-flow.md'
errors = []


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def check(condition, message):
    if not condition:
        errors.append(message)


def rows(text, prefix):
    found = {}
    for line in text.splitlines():
        match = re.match(rf'\| ({prefix}-\d+) \|', line)
        if match:
            found[match[1]] = [cell.strip() for cell in line.strip().strip('|').split(' | ')]
    return found


def check_catalog(text, prefix, count):
    catalog = rows(text, prefix)
    expected = {f'{prefix}-{n:02d}' for n in range(1, count + 1)}
    check(set(catalog) == expected, f'{prefix}: неполный каталог {sorted(expected ^ set(catalog))}')
    for key, cells in catalog.items():
        check(len(cells) == 5 and all(cells), f'{key}: нужны случай, действие, граничный случай и место')


audit, ain, ttz = read(AUDIT), read(AIN), read(TTZ)
check_catalog(ain, 'LE', 20)
check_catalog(ttz, 'LT', 10)
for code in ('S01', 'S27', 'Р-AIN-1', 'Р-AIN-2', 'Р-AIN-3', '### 7.2.'):
    check(code in ain, f'RFC-AIN-001: нет {code}')
for code in ('Р-ТТЗ-1', 'Р-ТТЗ-3', 'Р-ТТЗ-4', 'Р-ТТЗ-5', '### 8.1.', '### 8.2.'):
    check(code in ttz, f'RFC-TTZ-001: нет {code}')
# #474 accepts A-IN explicitly; TTZ still awaits its own decision.
check(re.search(r'^status: accepted$', ain, re.M), 'RFC-AIN-001: нет принятия #474')
check(re.search(r'^status: proposed$', ttz, re.M), 'RFC-TTZ-001: статус должен остаться proposed')

ledger = json.loads(read('experiments/issue_468/practice-ledger.json'))
items = ledger if isinstance(ledger, list) else next(v for v in ledger.values() if isinstance(v, list))
known_p = {item['id'] for item in items}
remarks = read('runs/2026/RUN-0090/outputs/review-remarks.md')
problems = rows(audit, '1135')
check(len(problems) == 14, f'1135: ожидалось 14 проблем, найдено {len(problems)}')
for key, cells in problems.items():
    check(len(cells) == 6 and all(cells), f'{key}: нужны все колонки')
    for ref in re.findall(r'\bP\d{2}\b', cells[2]):
        check(ref in known_p, f'{key}: нет {ref} в ledger')
    for ref in re.findall(r'\bR(\d+)\b', cells[2]):
        check(re.search(rf'^\| {ref} \|', remarks, re.M), f'{key}: нет замечания {ref}')
    check(re.findall(r'LE-\d{2}', cells[5]), f'{key}: нет ссылки на правило')
    for ref in re.findall(r'LE-\d{2}', cells[5]):
        check(f'| {ref} |' in ain, f'{key}: нет {ref} в RFC')

bad = [p.name for p in (ROOT / 'docs/rfc').rglob('*.md')
       if not re.match(r'^(\d{4}-\d{2}-.+|.+-registry|README)\.md$', p.name)]
check(not bad, f'нестандартные имена: {bad}')
check('docs/rfc/' not in read('tools/file-naming-legacy-allowlist.txt'), 'docs/rfc вернулся в allowlist')

stats = json.loads(read('site/data/stats.json'))
check('"version": "2.8.4"' in json.dumps(stats, indent=2), 'stats.json: версия не 2.8.4')
index = read('site/index.html')
check('>v2.8.4<' in index and '>v2.8.1<' not in index, 'site/index.html: версия не 2.8.4')
check('rfc-audit-link' in index, 'site/index.html: нет ссылки на аудит')
backlog = read('pr-ops/BACKLOG.md')
check(re.search(r'^\| BL-181 \|.*\| DONE \|', backlog, re.M), 'нет BL-181 в статусе DONE после #472')

if errors:
    print('\n'.join(f'ERROR: {e}' for e in errors))
    sys.exit(1)
print('issue #470 audit: OK')
