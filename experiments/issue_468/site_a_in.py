"""Proposed A-IN panel; existing copyable kit remains owned by its sources."""
from html import escape
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RFC = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md'
START = '        <!-- issue-468:start -->'
END = '        <!-- issue-468:end -->'

def panel():
    route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
    items = '\n'.join(f'            <li data-ain-step="{s["id"]}"><strong>{escape(s["name"])}</strong> — {escape(s["output"])}.</li>' for s in route['steps'])
    return f'''{START}
        <details class="process-help" id="a-in-proposal">
          <summary>Проект A-IN: {route['step_count']} шага до перехода к следующей стадии</summary>
          <p><strong>RFC-AIN-001 · на рассмотрении.</strong> Предлагаем разделить сбор, проверку источников, вопросы и написание контекста. Это принципы будущих промптов; текущий комплект из 14 шагов ниже пока сохраняется.</p>
          <p>На каждом шаге — проверяемый результат и отчёт об источниках. Вопросы адресованы Заказчику; БА принимает пакет и может явно согласовать гипотезу. До допуска по данным и вопросам раздел 2 не создаётся.</p>
          <ol class="v2-list">
{items}
          </ol>
          <p>Если evidence недостаточно, возвращаемся к сбору и извлечению из БЗ. В память следующего шага переносится только согласованное БА, с происхождением и статусом гипотез.</p>
          <p><a href="{RFC}" target="_blank" rel="noreferrer">Подробный RFC: контракты, возвраты, роли, бюджет и план производства промптов</a></p>
        </details>
{END}
'''

def apply(html):
    if START in html:
        start = html.index(START)
        end = html.index(END, start) + len(END)
        if html[end:end+1] == '\n':
            end += 1
        html = html[:start]+html[end:]
    marker = '        <details class="process-help" id="process-help">'
    if html.count(marker) != 1:
        raise ValueError('process help anchor must be unique')
    return html.replace(marker, panel()+marker, 1)
