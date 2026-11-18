#!/usr/bin/env python3
"""Exact revert of the issue #490 additions to A-IN prompts (history checks).

Measured or observed texts (e.g. the #474 AIN-09 recording) were taken on the
v0.2 prompts. ``revert_ain`` removes exactly what #490 added — the «Итог шага»
block, the answer-order line, the technical-acceptance paragraph of the common
contract and the version bump — and fails if any piece is not found once.
"""
import re

COMMON_490 = """Решение БА по техническому шагу (#490, [итог шага](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-step-handoff.md)):
ввод БА следующего промпта — явное принятие текущей версии результата;
молчание по-прежнему не решение. Шаг с обязательной проверкой БА принимается
только явным решением; AIN-21 и Г-IN техническими не бывают.
"""
BLOCK = re.compile(r"<!-- issue-490:handoff -->\n.*?<!-- /issue-490:handoff -->\n\n", re.S)


def _once(text, old, new):
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


def revert_ain(text, sid):
    text = _once(text, "version: 0.3\nupdated: 2026-11-18\n", "version: 0.2\nupdated: 2026-11-08\n")
    text = _once(text, COMMON_490, "")
    assert len(BLOCK.findall(text)) == 1, "handoff block"
    text = BLOCK.sub("", text)
    return _once(text,
                 f"Порядок ответа: результат, «На согласование БА» (если есть), receipt,\n"
                 f"«Итог шага», затем `КОНЕЦ {sid} <версия результата>`.\n",
                 f"Сначала результат, затем receipt, затем `КОНЕЦ {sid} <версия результата>`.\n")
