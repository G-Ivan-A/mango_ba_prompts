#!/usr/bin/env python3
"""Render 24 complete A-IN draft prompts and website data from accepted contracts."""
import argparse
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / 'prompts/drafts/a-in'

def build():
    route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
    instructions = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-instructions.json').read_text())
    common = (ROOT/'docs/ba-processes/bcreq-a-in-common.md').read_text().split('---', 2)[2].strip()
    rfc = (ROOT/'docs/rfc/2026-11-a-in-decomposition.md').read_text()
    lessons = [line for line in rfc.splitlines() if re.match(r'\| LE-\d{2} \|', line)]
    assert len(lessons) == 20
    outputs, kit = {}, []
    for step in route['steps']:
        sid = step['id']; instruction = instructions[sid]
        selected = []
        for line in lessons:
            cells = [c.strip() for c in line.split('|')[1:-1]]
            # Rules assigned to the common contract apply to every prompt.
            if '§3' in cells[-1] or re.search(rf'(?<!\d){sid[-2:]}(?!\d)', cells[-1]):
                selected.append(f'- **{cells[0]}.** {cells[1]} → {cells[2]}. Граница: {cells[3]}.')
        body = f'''---
id: mango-bcreq-{sid.lower()}-stepwise
title: "BCREQ {sid}: {step['name']}"
status: draft
version: 0.2
updated: 2026-11-08
temperature: 0.1
operation: understanding
processes: ["Приём и контекст"]
route_version: "{route['version']}"
assembled_by: scripts/build_bcreq_a_in.py
---
<!-- Experimental: for https://github.com/G-Ivan-A/mango_ba_prompts/issues/474, no formal research yet -->

# {sid}. {step['name']}

Draft для ручной проверки БА; эффективность модели не измерена.

{common}

## Только текущий контракт: {sid}

- Зачем: {step['why']}.
- Вход: {step['input']}.
- Единственный результат: {step['output']}.
- Операции существующих классов: {step['operation']}.
- Review: {', '.join(step['review'])}; решение результата — БА.
- Практики, сохранённые из наблюдений: {', '.join(step['practice_ids']) or 'общий контракт'}.

### Выполни

{instruction['action']}

### Форма результата

{instruction['shape']}

### Проверка до ответа

{step['checks']}.

Запреты: {step['forbidden']}. Отдельно проверь соблюдение общего контракта,
правдивость receipt, происхождение каждого утверждения и отсутствие будущих действий.

### Отказ и возврат

Нет входа или проверка не пройдена — blocked/rework, недостающее и причина.
Цель возврата: {', '.join(step['returns']) or step['failure']}; при отказе: {step['failure']}.
Допустимый следующий после принятия: {step['next']}. Не выполняй его сейчас.

Контрпример: {instruction['negative_example']}

### Граничные случаи LLM для этого контракта

{chr(10).join(selected)}

Сначала результат, затем receipt, затем `КОНЕЦ {sid} <версия результата>`.
'''
        path = DRAFTS / f'bcreq-{sid.lower()}-understanding-stepwise.md'
        outputs[path] = body
        kit.append({**step, 'promptPath':str(path.relative_to(ROOT)), 'prompt':body,
                    'promptSha256':hashlib.sha256(body.encode()).hexdigest()})
    outputs[ROOT/'site/data/a-in-kit.json'] = json.dumps({'routeVersion':route['version'],'status':'draft','measured':False,'steps':kit},ensure_ascii=False,indent=2)+'\n'
    return outputs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=build();stale=[str(p.relative_to(ROOT)) for p,t in outputs.items() if not p.exists() or p.read_text()!=t]
    if args.check:
        if stale: print('Stale: '+', '.join(stale));return 1
    else:
        for path,body in outputs.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
    print('A-IN: 24 draft prompts and site data '+('verified' if args.check else 'rendered'));return 0
if __name__=='__main__':raise SystemExit(main())
