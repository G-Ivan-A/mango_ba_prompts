"""Render the RFC opening table from the proposed route SSOT."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def table():
    route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
    lines = ['| Шаг | Что / результат | Зачем | Как принимаем | Почему не дробим дальше сейчас |',
             '| --- | --- | --- | --- | --- |']
    for s in route['steps']:
        lines.append(f"| {s['id']} {s['name']} | {s['output']} | {s['why']} | {s['checks']} | {s['granularity']} |")
    return '\n'.join(lines)
if __name__ == '__main__':
    p = ROOT/'docs/rfc/2026-11-a-in-decomposition.md'
    a,b = '<!-- route-table:start -->','<!-- route-table:end -->'
    old=p.read_text(); start=old.index(a)+len(a); end=old.index(b)
    p.write_text(old[:start]+'\n'+table()+'\n'+old[end:])
