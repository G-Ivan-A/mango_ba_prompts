"""Accepted A-IN route with complete draft prompts; legacy kit remains available."""
from html import escape
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
    items = '\n'.join(f'''            <li data-ain-step="{s['id']}">
              <strong>{s['id']}: {escape(s['name'])}</strong><p>{escape(s['output'])}.</p>
              <p>Проверка: {escape(s['checks'])}.</p>
              <button type="button" class="testkit-copy" data-ain-copy="{s['id']}" aria-label="Копировать полный промпт {s['id']}">⧉ Копировать {s['id']}</button>
              <details data-ain-preview="{s['id']}"><summary>Полный текст промпта {s['id']}</summary><pre class="testkit-prompt-text" aria-live="polite">Откройте для загрузки полного текста.</pre></details>
            </li>''' for s in route['steps'])
    return f'''{START}
        <details class="process-help" id="a-in-proposal" open>
          <summary>A-IN: {route['step_count']} отдельных шага · draft</summary>
          <p><strong>RFC-AIN-001 принят · промпты draft, эффективность не измерена.</strong> Начните с Ш-0 (полная конституция) в комплекте ниже, затем копируйте один полный AIN-промпт за вызов. Передайте правила и принятый пакет; после результата решение принимает БА.</p>
          <p>Раздел 2 строго после явного актуального допуска БА AIN-21 и отдельной команды AIN-22. Вопросы — Заказчику нумерованным списком AIN-16. Принятие RFC и команда new не заменяют допуск. AIN-24 и Г-IN разрешают переход к ФТ.</p>
          <p><a href="{GUIDE}" target="_blank" rel="noreferrer">Инструкция БА: запуск, версии, вопросы, возвраты и восстановление длинного чата</a></p>
          <ol class="v2-list">
{items}
          </ol>
          <p>Прежний комплект ниже сохранён для совместимости и других стадий. Его Ш-А/Ш-1/Ш-2 и one-shot адаптированы к этому порядку; прежние результаты тестов не измеряют новые тексты. 39 классов остаются библиотекой операций.</p>
          <p><a href="{RFC}" target="_blank" rel="noreferrer">Принятый RFC: контракты, возвраты, роли и бюджет</a></p>
          <p id="rfc-audit-link"><a href="{AUDIT}" target="_blank" rel="noreferrer">Аудит RFC и ограничения проверки поведения модели</a></p>
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
