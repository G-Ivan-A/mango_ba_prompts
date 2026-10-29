"""Check PDF extraction conservation and heading boundary metadata locally."""
import json
from pathlib import Path
import pymupdf

BASE = Path(__file__).resolve().parent
p = pymupdf.open(BASE / 'raw/CC_manual_1.26.42_compressed.pdf')
s = json.loads((BASE / 'raw/pdf-sections.json').read_text())
print('all page chars', sum(len(page.get_text()) for page in p))
print('content page chars', sum(len(page.get_text()) for page in list(p)[8:]))
print('section chars', sum(len(x['text']) for x in s))
print('TOC 8', p[7].get_text())
print('short sections', [(x['id'], x['title'], len(x['text'])) for x in s if len(x['text']) < 100])
for page in list(p)[8:10]:
 print('header', [(round(l['bbox'][1],1), ''.join(s['text'] for s in l['spans']))
                  for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])][:4])
