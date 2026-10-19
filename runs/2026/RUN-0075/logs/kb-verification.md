---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/378"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb"
---

# Журнал сверки с базой знаний — RUN-0075

> Файл **порождён** скриптом [`experiments/issue_378_golden_set.py`](../../../../experiments/issue_378_golden_set.py) из разметки [`experiments/issue_378_golden_data.py`](../../../../experiments/issue_378_golden_data.py) — не редактируйте вручную. Каждая цитата сверена с экспортом чата ([`../logs/quote-verification.md`](../logs/quote-verification.md)).

База знаний — `docs/kb` mango-ba-ai-runtime на SHA `91406e430aeb70dabf20548eee0ea95127f42690`. Локатор — код документа, раздел и файл раздела КБ.

## Локаторы

| Локатор | Файл раздела КБ |
| --- | --- |
| CC §2.3.3 | [`docs/kb/mango-cc-manual/sections/09-instrumenty-obrascheniya-ochered-obrasch.md («Заказы обратного звонка», с. 26–32: ручной и автоматический режим виджета, срок 14 дней)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-cc-manual/sections/09-instrumenty-obrascheniya-ochered-obrasch.md) |
| CC §9.3 | [`docs/kb/mango-cc-manual/sections/65-propuschennye-vyzovy.md (столбца «Статус автоперезвона» и фильтра «Скрыть попытки автоперезвона» нет)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-cc-manual/sections/65-propuschennye-vyzovy.md) |
| LK §4.5.2.1–4.5.2.2 | [`docs/kb/mango-lk-manual/sections/130-vse-vyzovy.md, 131-propuschennye-vyzovy.md (фильтр «Скрыть попытки автоперезвона», «Статус автоперезвона»)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/sections/130-vse-vyzovy.md, 131-propuschennye-vyzovy.md) |
| LK §4.5.9.1.1 | [`docs/kb/mango-lk-manual/index.md (с. 240; пункта 4.5.9.1.5 с этим содержанием нет)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/index.md) |
| LK §4.5.7 | [`docs/kb/mango-lk-manual/sections/145-zakaz-zvonka.md («Заказ звонка» из ЛК, с. 223–224 — не виджет ЗОЗ КЦ)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/sections/145-zakaz-zvonka.md) |
| LK §4.6.2 | [`docs/kb/mango-lk-manual/sections/277-audiofayly.md (с. 446–448)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/sections/277-audiofayly.md) |
| LK §4.4.6.1.5 | [`docs/kb/mango-lk-manual/sections/117-vkladka-avtosekretar.md (с. 157–162)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/sections/117-vkladka-avtosekretar.md) |
| LK §4.6.5.6 | [`docs/kb/mango-lk-manual/sections/304-avtoperezvon.md (с. 486–487)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/mango-lk-manual/sections/304-avtoperezvon.md) |
| VPBXAPI §4.3 | [`docs/kb/vpbx-api/sections/158-upravlenie-zadachey-na-avtoperezvon.md (с. 215)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/158-upravlenie-zadachey-na-avtoperezvon.md) |
| VPBXAPI §4.8 | [`docs/kb/vpbx-api/sections/214-rabota-s-obrascheniyami-v-kontakt-centre.md (с. 300)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/214-rabota-s-obrascheniyami-v-kontakt-centre.md) |
| VPBXAPI §1 | [`docs/kb/vpbx-api/sections/01-opredeleniya-i-sokrascheniya.md (термин «Внешняя система»)`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/91406e430aeb70dabf20548eee0ea95127f42690/docs/kb/vpbx-api/sections/01-opredeleniya-i-sokrascheniya.md) |

## Вхождения, сверенные с КБ

| ID | Р. | Кат. | Продукт | Цитата модели | Локатор | Что показывает КБ |
| --- | --- | --- | --- | --- | --- | --- |
| I-008 | 5 | C01 | `cc` | «дать операторам инструкцию фильтровать вкладку «Пропущенные вызовы» по колонке «Статус автоперезвона»» | CC §9.3 | в КЦ столбца «Статус автоперезвона» нет — он только в ЛК 4.5.2.2 |
| I-016 | 17 | C11 | `cc` | «Доступен фильтр «Скрыть попытки автоперезвона» (п. 9.1.1)» | LK §4.5.2.1–4.5.2.2 | фильтр есть только в ЛК 4.5.2.1/4.5.2.2, не в п. 9.1.1 КЦ |
| I-020 | 19 | C01 | `cc` | «#### Б. Контакт-Центр (КЦ) -> История вызовов -> Пропущенные вызовы» | CC §9.3 | описание раздела КЦ с атрибутами, которых в CC 9.3 нет |
| I-021 | 19 | C01 | `cc` | «**Столбец «Статус автоперезвона»**: Аналогично ЛК ВАТС» | CC §9.3 | — |
| I-049 | 39 | C11 | `vpbx` | «(ЛК ВАТС, п. 4.5.9.1.5 и Аналитика)» | LK §4.5.9.1.1 | верный пункт — 4.5.9.1.1, с. 240 |
| I-050 | 39 | C01 | `cc` | «**Цитата из документации (КЦ, п. 9.3. Пропущенные вызовы):**» | CC §9.3 | выдуманная цитата: «Статус автоперезвона» в CC 9.3 отсутствует |
| I-055 | 41 | C01 | `cc` | «(значения: «В работе», «Обработан», «Не дозвонились», «Сотрудник сам перезвонил»)» | CC §9.3 | значения перенесены из ЛК в КЦ |
| I-058 | 43 | C11 | `vpbx` | «ЛК ВАТС, п. 4.5.9.1.5 «Количество "перезвонов" по пропущенным звонкам», стр. 240; п. 4.5.9.1.1.5, стр. 248.» | LK §4.5.9.1.1 | — |
| I-061 | 45 | C01 | `cc` | «В разделах 9.3 (КЦ) и 4.5.2.2 (ЛК ВАТС) жестко зафиксирован исчерпывающий список столбцов отчета «Пропущенные вызовы»» | CC §9.3 | для КЦ список столбцов с «Статус автоперезвона» выдуман |
| I-068 | 47 | C01 | `cc` | «**ЛОЖНАЯ (Архитектурное противоречие).**» | CC §2.3.3 | собственная цитата модели из CC 2.2 противоречит выводу |
| I-080 | 49 | C11 | `vpbx` | «(ЛК ВАТС, п. 4.5.9.1.5)» | LK §4.5.9.1.1 | — |
| I-141 | 85 | C01 | `cc` | «**Нет, документация не подтверждает, что текущий функционал работает именно так.**» | CC §2.3.3 | первая часть вопроса БА (кнопка «Позвонить» в ЗОЗ) описана в CC 2.3.3 |
| I-156 | 105 | C11 | `cc` | «Согласно разделу 4.5.7 "Заказ звонка"» | LK §4.5.7 | ЛК 4.5.7 — инструмент «Заказ звонка» из ЛК, а не виджет ЗОЗ КЦ |
