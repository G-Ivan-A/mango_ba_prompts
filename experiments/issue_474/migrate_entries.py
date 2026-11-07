"""Apply migration guards to existing entry points; old text stays traceable."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[2]
base='https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/'
files={
'bcreq-constitution-governance-oneshot':'Ш-0 остаётся стартером: прими полную конституцию ниже без вывода, зафиксируй задачу/режим/исходный запрос без анализа. Затем остановись перед AIN-01. Ш-А разрешён только после принятого AIN-01 и выполняет исключительно AIN-02.',
'bcreq-context-understanding-stepwise':'Ш-1 теперь диспетчер 24 отдельных контрактов. По переданному пакету назови один текущий AIN-ID и недостающий вход; предложи скопировать его полный промпт. Не выполняй подшаги исторического Ш-1 ниже. Нет принятого предшественника — возврат к нему; нет пакета — AIN-01.',
'bcreq-products-impact-analysis-stepwise':'Ш-2 теперь проверяет пакет AIN-24, а не добывает продукты после написания контекста. Нет актуального AIN-21 и принятого AIN-24/Г-IN — остановись и назови возврат. Продукты/2.5 собирает AIN-13/22, гейт — AIN-24. Историческую последовательность ниже не запускай.',
'bcreq-in-understanding-oneshot':'One-shot A-IN больше не выполняет стадию за один ответ. Определи только текущий AIN-ID по пакету и остановись перед его отдельным полным промптом. Не запускай исторический алгоритм ниже, даже при new или просьбе сделать всё.',
'bcreq-fr-documentation-stepwise':'До алгоритма Ш-3 проверь явные AIN-21 и AIN-24/Г-IN, их task/attempt/route/snapshot и актуальность. Без одного из них — blocked, возврат к указанному AIN-ID; ФТ не создавай. При действующем Г-IN выполняй прежний алгоритм ФТ ниже.',
'bcreq-core-documentation-oneshot':'До A-CORE проверь явные AIN-21 и AIN-24/Г-IN для текущего task/attempt/route/snapshot. Нет допуска или он stale — blocked, без ФТ/НФТ/UC. Принятый Г-IN разрешает прежнюю стадию A-CORE ниже.'}
for stem,action in files.items():
 p=ROOT/f'prompts/{stem}.md';t=p.read_text()
 if '<!-- issue-474:entry -->' in t:continue
 end=t.index('\n---',4)+4
 guard=f'''\n\n<!-- issue-474:entry -->
## Действующий вход A-IN — приоритет над прежним маршрутом

{action}

СТРОГО ЗАПРЕЩЕНО генерировать текст раздела 2 до явного allow AIN-21
текущего принятого snapshot; раздел создаёт только AIN-22 отдельным вызовом.
Все stakeholder-вопросы адресованы Заказчику нумерованным списком AIN-16.
БА — куратор, не адресат этих вопросов. New/delta, молчание и согласие с RFC
не проходят гейт. Пауза/analysis-only не запускают следующий шаг.

[Полные 24 draft контракта и инструкция БА]({base}docs/ba-processes/bcreq-a-in-execution.md).
Конституция/мета-стандарты и прежние операции вне мигрировавшей A-IN сохраняются.
Исторические команды ниже применяются только в пределах разрешённого действия
этого входа; прежние переходы/производство раздела 2 здесь не исполняются.
<!-- /issue-474:entry -->
'''
 t=t[:end]+guard+t[end:]
 m=re.search(r'^version: (\d+)\.(\d+)$',t,re.M)
 if m:t=t[:m.start()]+f'version: {m[1]}.{int(m[2])+1}'+t[m.end():]
 t=re.sub(r'^updated: .*$', 'updated: 2026-11-07',t,count=1,flags=re.M)
 p.write_text(t)
