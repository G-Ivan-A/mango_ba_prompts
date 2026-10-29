"""Inspect exact prose overlap before choosing comparison alignment parameters."""
import json
from pathlib import Path
import compare

BASE = Path(__file__).resolve().parent
sections = json.loads((BASE / 'raw/pdf-sections.json').read_text())
rows = [json.loads(p.read_text()) for p in (BASE/'cache').glob('*.json')]
rows = [r for r in rows if '3_kontakt-tsentr' in r['url']]
for s in sections[:16]:
 a=compare.tokens(s['text']); aset=set(tuple(a[i:i+5]) for i in range(len(a)-4))
 hits=[]
 for r in rows:
  b=compare.tokens(r['text']); bset=set(tuple(b[i:i+5]) for i in range(len(b)-4))
  score=len(aset&bset)/len(aset) if aset else 0
  hits.append((score,r['title'],len(b),r['url']))
 print(s['id'],s['title'],len(a),sorted(hits,reverse=True)[:2])
