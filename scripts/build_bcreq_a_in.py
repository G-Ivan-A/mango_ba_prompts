#!/usr/bin/env python3
"""Render 24 complete A-IN draft prompts and website data from accepted contracts."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import bcreq_handoff  # noqa: E402  (issue #490: «Итог шага» из SSOT)
import bcreq_fragments as fragments  # noqa: E402
from prompt_purity import project  # noqa: E402  (issue #495: тело промпта без приватных ссылок и комментариев)
DRAFTS = ROOT / 'prompts/drafts/a-in'

def build():
    route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
    instructions = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-instructions.json').read_text())
    common = fragments.common()
    rfc = (ROOT/'docs/rfc/2026-11-a-in-decomposition.md').read_text()
    lessons = [line for line in rfc.splitlines() if re.match(r'\| LE-\d{2} \|', line)]
    assert len(lessons) == 21
    handoff = bcreq_handoff.load()
    outputs, kit = {}, []
    for step in route['steps']:
        sid = step['id']; instruction = instructions[sid]
        selected = fragments.lessons(sid)
        body = f'''---
id: mango-bcreq-{sid.lower()}-stepwise
title: "BCREQ {sid}: {step['name']}"
status: draft
version: {fragments.VERSION}
updated: {fragments.DATE}
temperature: 0.1
operation: understanding
processes: ["Приём и контекст"]
route_version: "{route['version']}"
assembled_by: scripts/build_bcreq_a_in.py
---

# {sid}. {step['name']}

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

{selected or 'Для этого шага достаточно общих граничных случаев контракта.'}

{bcreq_handoff.render([sid], handoff)}
Порядок ответа: {fragments.response_order()}.
Заверши полный ответ `КОНЕЦ {sid} {fragments.VERSION}`.
'''
        head, text = body.split('\n---\n', 1)
        body = head + '\n---\n' + project(text)
        path = DRAFTS / f'bcreq-{sid.lower()}-understanding-stepwise.md'
        outputs[path] = body
        anchor = f'''## Якорь контракта A-IN {fragments.VERSION}
- До выполнения проверь полный «Контракт A-IN {fragments.VERSION}» в этом чате.
- Контракт отсутствует, другой версии или утрачен — blocked: «Вставьте Контракт A-IN {fragments.VERSION}»; шаг не выполняй.
- Чтение не имитируй; доступ и ACCESS_GAP — по контракту, пробелы сохраняй в принятом пакете.
- Допуск — явно; Реестр решений БА сохраняй; память — только 08/16/24.
- Receipt — до трёх строк; порядок: {fragments.response_order()}.
- Версия промпта {fragments.VERSION}; маркер `КОНЕЦ {sid} {fragments.VERSION}`.
'''
        compact = body.replace(common, anchor.strip(), 1)
        kit.append({**step, 'promptPath':str(path.relative_to(ROOT)), 'prompt':body,
                    'promptSha256':hashlib.sha256(body.encode()).hexdigest(),
                    'compactPrompt':compact,
                    'compactPromptSha256':hashlib.sha256(compact.encode()).hexdigest()})
    contract = f'# Контракт A-IN {fragments.VERSION}\n\n{common}\n'
    outputs[ROOT/'site/data/a-in-kit.json'] = json.dumps({
        'routeVersion':route['version'], 'status':'draft', 'measured':False,
        'defaultForm':'full', 'contract':{'version':fragments.VERSION,'prompt':contract,
        'promptSha256':hashlib.sha256(contract.encode()).hexdigest()}, 'steps':kit,
    },ensure_ascii=False,indent=2)+'\n'
    return outputs

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--site-json',action='store_true',help='render site data to stdout without writing')
    args=parser.parse_args()
    outputs=build()
    if args.site_json:
        print(outputs[ROOT/'site/data/a-in-kit.json'], end='')
        return 0
    stale=[str(p.relative_to(ROOT)) for p,t in outputs.items() if not p.exists() or p.read_text()!=t]
    if args.check:
        if stale: print('Stale: '+', '.join(stale));return 1
    else:
        for path,body in outputs.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
    print('A-IN: 24 draft prompts and site data '+('verified' if args.check else 'rendered'));return 0
if __name__=='__main__':raise SystemExit(main())
