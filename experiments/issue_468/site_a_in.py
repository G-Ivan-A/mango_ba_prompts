"""Accepted A-IN guidance inside the existing Processes help disclosure."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RFC = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/2026-11-a-in-decomposition.md'
AUDIT = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/audit/2026-11-07-bcreq-ttz-rfc-audit.md'
GUIDE = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/ba-processes/bcreq-a-in-execution.md'
START = '        <!-- issue-468:start -->'
END = '        <!-- issue-468:end -->'

def panel():
    route = json.loads((ROOT/'docs/ba-processes/bcreq-a-in-route.json').read_text())
    return f'''{START}
        <div id="a-in-proposal">
          <p><strong>A-IN: {route['step_count']} отдельных шага · draft</strong></p>
          <p><strong>RFC-AIN-001 принят · промпты draft, эффективность не измерена.</strong> Начните с Ш-0 (полная конституция) в комплекте ниже, затем копируйте один полный AIN-промпт из карточки за вызов. Передайте правила и принятый пакет; после результата решение принимает БА.</p>
          <p>Раздел 2 строго после явного актуального допуска БА AIN-21 и отдельной команды AIN-22. Вопросы — Заказчику нумерованным списком AIN-16. Принятие RFC и команда new не заменяют допуск. AIN-24 и Г-IN разрешают переход к ФТ.</p>
          <p><a href="{GUIDE}" target="_blank" rel="noreferrer">Инструкция БА: запуск, версии, вопросы, возвраты и восстановление длинного чата</a></p>
          <p>Карточки AIN-01…24 находятся в этапе «Старт и разделы 1–2» ниже: инструкция, полный текст и копирование в форме 2.7.0. Ш-0 остаётся стартером; остальные стадии и сравнение редакций сохранены. 39 классов остаются библиотекой операций.</p>
          <p><a href="{RFC}" target="_blank" rel="noreferrer">Принятый RFC: контракты, возвраты, роли и бюджет</a></p>
          <p id="rfc-audit-link"><a href="{AUDIT}" target="_blank" rel="noreferrer">Аудит RFC и ограничения проверки поведения модели</a></p>
        </div>
{END}
'''

def apply(html):
    if START in html:
        start = html.index(START)
        end = html.index(END, start) + len(END)
        if html[end:end+1] == '\n':
            end += 1
        html = html[:start]+html[end:]
    marker = '        <details class="process-help" id="process-help">\n          <summary>Как пользоваться</summary>\n'
    if html.count(marker) != 1:
        raise ValueError('process help anchor must be unique')
    return html.replace(marker, marker+panel(), 1)
