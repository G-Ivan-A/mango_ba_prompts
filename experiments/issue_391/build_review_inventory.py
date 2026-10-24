"""Build traceability inventory; mappings record review, never Golden promotion."""
from pathlib import Path
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/'
COMMON = {
'C01':'Р5; АД-6; Ш-6 L1/L2', 'C02':'Р5; АП5', 'C03':'Р4; АП4',
'C04':'Р6; Ш-3 Ф1/Ф2', 'C05':'АД-9 (добавлено); Р3', 'C06':'АД-2; Р3',
'C07':'АД-10 (добавлено); CB-0.6 (добавлено)', 'C08':'АД-10 (добавлено); Ш-6 L1/L2',
'C09':'АД-1; Р1/Р2', 'C10':'АД-3/АД-4; Р7',
'C11':'Ш-3 порядок; Ш-6 последовательность (добавлено)',
'C12':'Ш-3 Ф3/Ф4; глоссарий; АП7',
'C13':'Ш-В чек-листы; Ш-6/Ш-8 условия контракта (добавлено)',
'C14':'CB-0.4; Р3', 'C15':'АД-1/АД-6; Ш-2', 'C16':'CB-0.5',
'C17':'АД-9 (добавлено); пошаговые стоп-гейты', 'C18':'АД-1/АД-7; Ш-7',
'C19':'АП1–АП9; АД-11 (добавлено)',
}
OVERRIDES = {
74: {'C20':'АД-9 (добавлено)', 'C21':'Р3; АД-9 (добавлено)', 'C22':'АД-11/CB-0.7 (добавлено)',
     'C23':'Ш-1 релевантность As-Is (добавлено)', 'C24':'Ш-3 Ф1/Ф2/Ф4', 'C25':'Ш-3 Ф3; 3–7 ФТ с обоснованием отклонения'},
75: {'C01':'АД-1; Р1/Р2', 'C02':'АД-5; Р4', 'C03':'АД-10 (добавлено)',
     'C04':'АД-4', 'C05':'АД-3; Р7', 'C06':'АД-6', 'C07':'АД-7; Ш-3 Ф1',
     'C08':'АД-7; Ш-7', 'C09':'АД-2', 'C10':'АД-8 (добавлено)',
     'C11':'АД-1; Ш-В источники', 'C12':'АП7; Ш-3 Ф3/Ф4',
     'C13':'АД-3', 'C14':'АД-5; АД-10 (добавлено)', 'C15':'АП1–АП9'},
76: {'C20':'Конституция: снятие ложной находки (добавлено)'},
}

def rules(run, categories):
    mapping = COMMON | OVERRIDES.get(run, {})
    return '; '.join(dict.fromkeys(mapping[c] for c in categories))

rows = ['# Инвентарь сопоставления Golden Set — issue #391', '',
        'Это статическая трассировка защит к источникам, не результаты исполнения LLM и не утверждение кандидатов.', '',
        '| RUN | Кандидат | Тип | Категория в данном RUN | Защита / решение ревизии |',
        '| --- | --- | --- | --- | --- |']
summary = []
for run in (73,74,75,76):
    prefix = Path(f'runs/2026/RUN-{run:04}')
    candidates = json.loads((ROOT / prefix / 'outputs/golden-set-candidates.json').read_text())
    count = 0
    for group in candidates['sets']:
        for case in group['cases']:
            expect = case['expect']
            categories = [expect['defect_class']] if 'defect_class' in expect else expect['no_defect_of']
            rows.append(f"| {run:04} | [{case['id']}]({BASE}{prefix}/outputs/golden-set-candidates.md) | {case['kind']} | {', '.join(categories)} | {rules(run, categories)} |")
            count += 1
    criteria = []
    for line in (ROOT / prefix / 'outputs/success-criteria.md').read_text().splitlines():
        if line.startswith('| SC-'):
            identifier = line.split('|')[1].strip()
            cats = list(dict.fromkeys(re.findall(r'\bC\d{2}\b',line)))
            criteria.append((identifier,cats))
    summary.append({'run':f'RUN-{run:04}', 'candidate_cases':count,'criteria':len(criteria)})
    rows += ['', f'## RUN-{run:04}: критерии успеха', '', '| Критерий | Категории | Защита |', '| --- | --- | --- |']
    for identifier,cats in criteria:
        rows.append(f'| [{identifier}]({BASE}{prefix}/outputs/success-criteria.md) | {", ".join(cats)} | {rules(run,cats)} |')
    rows += ['', '| RUN | Кандидат | Тип | Категория в данном RUN | Защита / решение ревизии |', '| --- | --- | --- | --- | --- |']
rows = rows[:-3]
rows += ['', '## Источники и сохранность', '',
         'Для RUN-0073…0076 учтены success-criteria, error-statistics, how-not-to-do, JSON/Markdown кандидатов и журналы сверки цитат. Их SHA-256:', '',
         '| Файл | SHA-256 |', '| --- | --- |']
for run in (73,74,75,76,77):
    prefix = Path(f'runs/2026/RUN-{run:04}')
    for p in sorted((ROOT / prefix).rglob('*.md')) + sorted((ROOT / prefix).rglob('golden-set-candidates.json')):
        if any(term in p.name for term in ('success-criteria','error-statistics','how-not-to-do','golden-set-candidates','quote-verification','L0-feasibility')):
            relative = p.relative_to(ROOT)
            rows.append(f'| [{relative}]({BASE}{relative}) | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |')
output = ROOT / 'docs/reviews/issue-391-golden-inventory.md'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text('\n'.join(rows)+'\n')
print(json.dumps(summary,ensure_ascii=False))
