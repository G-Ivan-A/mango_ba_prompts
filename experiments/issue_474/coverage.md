---
status: draft
version: 0.1
updated: 2026-11-07
type: verification
scope: issue-474
---

# Покрытие практик и контрпримеров

Проверка здесь — контрактов и размеченных состояний, не реального ответа LLM.
Общая рамка встроена в каждый из 24 промптов. Применимые LE — отдельным
списком в том же тексте; практики — в route и конкретных действиях.
Для S09/S15/S16 и тона/полноты всех правил выполнен смысловой review текста;
следующая проверка на моделях/БА остаётся BL-175 по ADR-018.

| Правило | Реализация | Проверка |
| --- | --- | --- |
| P01 | common + AIN-03, AIN-07, AIN-08, AIN-09, AIN-11, AIN-12, AIN-19 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P02 | common + AIN-03, AIN-04, AIN-05, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P03 | common + AIN-05, AIN-12, AIN-15, AIN-17, AIN-18, AIN-21 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P04 | common + AIN-01, AIN-02, AIN-16, AIN-17, AIN-22, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P05 | common + AIN-04, AIN-17, AIN-19, AIN-20, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P06 | common + AIN-01, AIN-05, AIN-13, AIN-17, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P07 | common + AIN-02, AIN-19, AIN-20 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P08 | common + AIN-01, AIN-17, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P09 | common + AIN-02, AIN-04, AIN-15, AIN-16, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P10 | common + AIN-05, AIN-06, AIN-10, AIN-11, AIN-15 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P11 | common + AIN-06, AIN-12, AIN-15, AIN-16, AIN-18, AIN-21 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P12 | common + AIN-15, AIN-16, AIN-17, AIN-18 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P13 | common + AIN-04, AIN-05, AIN-08, AIN-09, AIN-12, AIN-19, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P14 | common + AIN-04, AIN-05, AIN-14, AIN-15, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P15 | common + AIN-04, AIN-06, AIN-10, AIN-12, AIN-17, AIN-19, AIN-23 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P16 | common + AIN-05, AIN-12, AIN-15, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P17 | common + AIN-05, AIN-11, AIN-19, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P18 | common + AIN-04, AIN-05, AIN-15, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P19 | common + AIN-03, AIN-05, AIN-12, AIN-15, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| P20 | common + AIN-01, AIN-17, AIN-19, AIN-20, AIN-23, AIN-24 | `scripts/test_issue_468_dialogue.py` + смысловой review действий |
| S01 | Stop; вопрос до текста; Gate fixture, 15…21 | gate-cases.json / validate_issue_468_a_in.py |
| S02 | Stop; rework/гипотеза/ответ; Gate fixture, 17 | gate-cases.json / validate_issue_468_a_in.py |
| S03 | Возврат к графу, не «всё new»; Coverage fixture, 06/10 | gate-cases.json / validate_issue_468_a_in.py |
| S04 | Не подтверждено; извлечь обе границы; Coverage fixture, 12 | gate-cases.json / validate_issue_468_a_in.py |
| S05 | Правдивый blocked, запрос документа БА; Gate fixture, 08/09 | gate-cases.json / validate_issue_468_a_in.py |
| S06 | Два прохода → stop, frontier открыт; §5; fixture | gate-cases.json / validate_issue_468_a_in.py |
| S07 | Запрет передачи; Gate fixture, 20 | gate-cases.json / validate_issue_468_a_in.py |
| S08 | Stop и invalidation; Gate fixture, 03/19/20 | gate-cases.json / validate_issue_468_a_in.py |
| S09 | Разные атомы; контроль полноты/кванторов; Ручная проверка принципов 04/05; без LLM-замера | gate-cases.json / validate_issue_468_a_in.py; смысловой review текста, LLM не измерена |
| S10 | Отозвать зависимые решения и повторить retrieval; Gate fixture, 19 | gate-cases.json / validate_issue_468_a_in.py |
| S11 | Условный допуск, видимая гипотеза; Gate fixture, 18/21 | gate-cases.json / validate_issue_468_a_in.py |
| S12 | Пустой принятый список; без искусственных вопросов; Gate fixture, 16/21 | gate-cases.json / validate_issue_468_a_in.py |
| S13 | Запрет, отдельно выполнить текущий шаг; Gate fixture, 21 | gate-cases.json / validate_issue_468_a_in.py |
| S14 | Предыдущий фактический, один текущий, служебное скрыто; route JSON; структурная проверка | gate-cases.json / validate_issue_468_a_in.py |
| S15 | Считать данными, не выполнять/публиковать; §3/5; checklist производства | gate-cases.json / validate_issue_468_a_in.py; смысловой review текста, LLM не измерена |
| S16 | Stop; только нормализация/документы; §6, checklist производства | gate-cases.json / validate_issue_468_a_in.py; смысловой review текста, LLM не измерена |
| S17 | Только разрешённый анализ/статус; продолжение после подходящего указания; Review fixtures, P04/P07/P08; смысловой checklist | review-cases.json / test_issue_468_dialogue.py |
| S18 | Сохранить до evidence, impact, coverage и BA-review; Review fixture + preservation baseline, P05/P15 | review-cases.json / test_issue_468_dialogue.py |
| S19 | Unknown до достаточного источника; empty и access gap отдельно; Review fixture, P01/P13; checklist достаточности | review-cases.json / test_issue_468_dialogue.py |
| S20 | Разные типы provenance, полные обратные ссылки; Review fixture + ручная сверка, P02/P09/P15/P18 | review-cases.json / test_issue_468_dialogue.py |
| S21 | Частичное принятие или отклонение по тезисам с основанием; Review fixture, P06/P20; нормативный ФТ-NN | review-cases.json / test_issue_468_dialogue.py |
| S22 | Сослаться на ответ; спрашивать оставшееся бизнес-решение в разрешённом режиме; Review fixtures + checklist, P09/P12 | review-cases.json / test_issue_468_dialogue.py |
| S23 | Это не противоречие; реальную зависимость проверять отдельно; Review fixture, P10; S03 сохраняется | review-cases.json / test_issue_468_dialogue.py |
| S24 | Вопрос о границе/ответственности или допустимая гипотеза, не ложное closed; Review fixture, P11; гейт S02/S11 | review-cases.json / test_issue_468_dialogue.py |
| S25 | Классифицировать по мета-стандартам 3…7, без нового L3/выдуманных НФТ; Review fixture + ручной checklist, P13/P16/P18…P20 | review-cases.json / test_issue_468_dialogue.py |
| S26 | Разделить понятия и условия, подтвердить термин; Review fixture + glossary checklist, P14/P15 | review-cases.json / test_issue_468_dialogue.py |
| S27 | Конфликт → повторная проверка и гейт; Review fixture + cross-section checklist, P17/P18 | review-cases.json / test_issue_468_dialogue.py |
| LE-01 | §3; БА: новый чат с пакетом после AIN-20 и при длинном чате; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-02 | §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-03 | §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-04 | §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-05 | §3; БА: принимать только блок с маркером конца; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-06 | §3, шаги 03/08/09; БА; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-07 | Шаги 08/09/12; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-08 | Шаги 04/12; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-09 | Шаги 04/05/22; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-10 | §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-11 | §3, §2.6; шаг 23; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-12 | Шаги 15/16; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-13 | Шаги 16/17/18; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-14 | Шаги 06/10/19; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-15 | Шаги 04/14; §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-16 | Шаги 05/22; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-17 | Шаги 22/23; §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-18 | Шаг 22; §3; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-19 | §3, §1.2; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |
| LE-20 | §3; БА; встроено генератором в указанные AIN | validate_issue_474_execution.py + review; контроль БА для 01/05/06/20 |


Специальные новые контрпримеры #474: явный allow без отдельного запуска,
allow другой версии task/attempt/route/snapshot, pending/rework, подпись модели,
простое yes, пауза; проверяет `experiments/issue_474/admission.py`.
Evidence: VERIFIED отрицательного утверждения совместим с «Нет»; CONFLICT,
PARTIAL, empty/access_gap, stale и неизвестная область не дают однозначной
исполнимости. Эти тесты не объявляют экспериментальный профиль утверждённым.
