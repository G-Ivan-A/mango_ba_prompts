---
status: draft
version: 0.1
updated: 2026-10-23
ai-generated: true
type: contract
scope: bcreq-stage-gates
related_artifacts:
  - "standards/bcreq-process-standard.md"
  - "standards/bcreq-sections/README.md"
  - "standards/bcreq-prompt-architecture.md"
  - "docs/adr/2026-10-adr-012-bcreq-meta-standards.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/387"
---

# Контракт стадий A-IN / A-CORE / A-WORK и гейтов BCREQ

> Носитель — [ADR-012](../adr/2026-10-adr-012-bcreq-meta-standards.md).
> Нормативный словарь [RFC 2119](https://www.rfc-editor.org/info/bcp14).
> Конвейер П1–П6 и гейты G1–G3 —
> [bcreq-process-standard](../../standards/bcreq-process-standard.md#2-конвейер-подпроцессов-оптимальное-число--6).

Контракт связывает три слоя: стадии БА мета-модели, шаги промптов
([архитектура промптов](../../standards/bcreq-prompt-architecture.md)) и
мета-стандарты разделов ([bcreq-sections](../../standards/bcreq-sections/README.md)).
Каждая стадия завершается гейтом с проверяемыми критериями.

## 1. Стадии и шаги

Стадии — по постановке БА: A-IN [р. 746, Ч-01](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L35), A-CORE [р. 746, Ч-02](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L36),
A-WORK [р. 746, Ч-03](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L37). Распределение шагов по стадиям предложено
моделью [р. 763, Ч-28](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L62) и принято в issue #387. Номер шага — в
пространстве `Ш-` (RFC-387-02); исходный номер 2.x указан в скобках.

| Стадия | Цель | Шаги (порядок выполнения) | Разделы BCREQ | Выход |
| --- | --- | --- | --- | --- |
| A-IN | подготовка данных для ФТ | Ш-1 (2.1) · Ш-2 (2.2) | 1, 2, ＋2.5, 8.4 | контекст, термины, границы, продукты и стейкхолдеры, вопросы |
| A-CORE | документация для Согласования 1 и оценки «от» | Ш-3 (2.3) · Ш-4 (2.5) · Ш-5 (2.4) | 3, 4, 7 (прогон 1) | ФТ, НФТ, UC, матрица UC × ФТ |
| A-WORK | документация для внутренних согласований и итоговой оценки | Ш-6 (2.6 + 2.7) · Ш-7 (2.8) · Ш-8 (2.9) · Ш-9 (2.14) · Ш-В | 5, 6, 7 (прогон 2), 8 | ОРР L1/L2, ограничения, граничные кейсы, риски, зависимости, план приёмки |
| вне стадий | независимые промпты | Ш-3 с флагом `вариант: new` (2.10) · Ш-С сценарии: US (2.12), UC (2.13) | 3, 7 | ФТ «с нуля», US, UC по контексту |

Шаг 2.11 не выполняется по решению БА [р. 752, Ч-22](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L56). Промпты
расшифровки встреч остаются вне стадий [р. 752, Ч-23](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L57) [р. 796, Ч-43](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L77).
A-RELEASE — следующая стадия после гейта Г-W [р. 746, Ч-54](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L88); её
содержание не входит в контракт.

## 2. Гейты

Все гейты контракта — человеческие. Правило B3
[процесса](../../standards/bcreq-process-standard.md#3-human-gates-в-ключевых-точках)
действует для каждого: LLM **НЕ ДОЛЖНА** проходить гейт и **НЕ ДОЛЖНА**
ставить статус готовности (АП2 аудита Задачи 1). Модель выводит отчёт по
критериям; решение принимает человек.

| Гейт | Переход | Кто решает | Необходимые критерии | Исходы |
| --- | --- | --- | --- | --- |
| Г-IN | A-IN → A-CORE | БА [р. 746, Ч-51](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L85) | Г-IN.1 Разделы 1 и 2 проходят чек-листы мета-стандартов. Г-IN.2 Границы 2.3 и 2.4 заданы. Г-IN.3 ＋2.5: продукты по таксономии, продуктовые команды, согласующие стейкхолдеры [р. 746, Ч-55](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L89). Г-IN.4 Открытые вопросы закрыты или записаны в 8.4 с адресатом. Г-IN.5 Расхождения терминов с индустриальными словарями показаны БА. | дальше / доработать A-IN |
| Г-С1 «Согласование 1» | A-CORE → A-WORK | Заказчик [р. 746, Ч-52](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L86) | Г-С1.1 Разделы 1–4 проходят чек-листы. Г-С1.2 Покрытие ФТ сценариями UC — 100 % (раздел 7, прогон 1, внутренний). Г-С1.3 Каждое ФТ — дельта или индустриально значимое с решением БА. Г-С1.4 Есть верхнеуровневая оценка «от». Г-С1.5 Блокирующих вопросов в 8.4 нет. | согласование → A-WORK; уточнение → возврат (§3); отказ → стоп |
| Г-W | A-WORK → A-RELEASE | ПО продукта, архитектор продукта, руководитель КК [р. 746, Ч-53](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L87) | Г-W.1 Разделы 5–8 проходят чек-листы. Г-W.2 Таблица трассировки ФТ ↔ ОРР полна; стыковые ФТ описаны по правилу К4 [композиции](../../standards/bcreq-composition-standard.md#2-правила-композиции). Г-W.3 Ш-В выполнен, замечания закрыты или приняты человеком. Г-W.4 Риски 8.1 имеют владельца (G2). Г-W.5 Итоговая оценка готова к передаче Заказчику [р. 796, Ч-42](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L76). | согласование → A-RELEASE; уточнение → возврат (§3); отказ → стоп |

Ш-В (валидация второй ролью) стоит перед Г-W: отдельный прогон проверяет
разделы 1–8 по чек-листам и выдаёт список замечаний «пункт → проблема →
вариант», без оценки «готово». Ш-В закрывает наблюдение Н8 аудита — в
структуре 2.1–2.14 нет шага П5.

Итоговая оценка, раздел 5 L1 и раздел 6 после Г-W передаются Заказчику на
согласование (issue #387: «Разделы 5–6 → детализация для Заказчика +
внутренняя»). Это не отдельный гейт стадии: отказ Заказчика здесь — исход
«уточнение» гейта Г-W.

## 3. Возвраты

БА: при уточнении — возврат в цикл A-IN, A-CORE или A-WORK
[р. 746, Ч-05](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L39); при работе промптами решение о возврате принимает БА
[р. 748, Ч-09](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/experiments/issue_387/chat-2026-10-22-23-register.md?plain=1#L43).

| Причина уточнения | Стадия возврата | Шаг-точка входа |
| --- | --- | --- |
| Термин, контекст, границы, состав продуктов | A-IN | Ш-1 или Ш-2 |
| ФТ, НФТ, полнота UC | A-CORE | Ш-3, Ш-4 или Ш-5 |
| ОРР, ограничения, граничные кейсы, риски | A-WORK | Ш-6 … Ш-9 |

- **Правило Г1 (кто решает).** Ручной прогон (stepwise): возврат выбирает БА;
  промпт только рекомендует. Агентный прогон (oneshot): агент останавливается
  и выдаёт рекомендацию «стадия · шаг · причина»; возврат выполняется после
  решения человека (B3).
- **Правило Г2 (что устаревает).** После возврата разделы шагов, следующих
  за точкой входа, помечаются `устарело` и проходят шаги заново
  (правило B7 [процесса](../../standards/bcreq-process-standard.md)).
  Разделы предыдущих шагов не меняются без решения БА.
- **Правило Г3 (журнал).** Каждый возврат записывается в 8.5: гейт,
  причина, кто решил, точка входа.

## 4. Маппинг стандартов на стадии

| Стадия | Разделы | Мета-стандарты | Стиль | Отраслевая основа |
| --- | --- | --- | --- | --- |
| A-IN | 1, 2, ＋2.5 | [01](../../standards/bcreq-sections/01-glossary.md), [02](../../standards/bcreq-sections/02-business-context.md), [профили продуктов](../../standards/bcreq-composition-standard.md#4-профили-продуктов) | 1 — бюрократический; 2 — короткий | BABOK 10.23, 6.1; IREB CPRE; ISO/IEC/IEEE 24765; словари D1–D11 |
| A-CORE | 3, 4, 7 (прогон 1) | [03](../../standards/bcreq-sections/03-functional-requirements.md), [04](../../standards/bcreq-sections/04-non-functional-requirements.md), [07](../../standards/bcreq-sections/07-use-cases.md) | 3, 4 — бюрократический; 7 — табличный | BABOK 7.1, 10.47; ISO/IEC/IEEE 29148; EARS; ISO/IEC 25010 |
| A-WORK | 5, 6, 7 (прогон 2), 8 | [05](../../standards/bcreq-sections/05-solution-description.md), [06](../../standards/bcreq-sections/06-implementation-constraints.md), [07](../../standards/bcreq-sections/07-use-cases.md), [08](../../standards/bcreq-sections/08-supplementary.md) | 5 L1, 6 — короткий; 5 L2 — технический; 7, 8 — табличный | arc42; C4; OpenAPI; AsyncAPI; доменные профили; ISTQB; ISO 31000; TM Forum ODA — альтернатива |

## 5. Связь с конвейером П1–П6

Стадии не заменяют конвейер П1–П6, а размещают его подпроцессы на
коммерческом цикле КК (RFC-387-04).

| Подпроцесс | Стадия, шаг | Гейт процесса | Гейт контракта |
| --- | --- | --- | --- |
| П1 Приём и нормализация | A-IN, Ш-1 | operation | — |
| П2 Декомпозиция на уровни | A-IN, Ш-2 | G1 | Г-IN |
| П3 Моделирование сценариев | A-CORE, Ш-5; A-WORK, Ш-8 | operation | — |
| П4 Документирование | A-CORE, Ш-3, Ш-4; A-WORK, Ш-6, Ш-7, Ш-9 | operation | Г-С1 (бизнес-слой) |
| П5 Валидация и риски | A-WORK, Ш-9, Ш-В | G2 | Г-W |
| П6 Утверждение и baselining | A-RELEASE | G3 | вне контракта |

## 6. Критерии соответствия

- [ ] Каждый шаг промпта отнесён к одной стадии или помечен «вне стадий».
- [ ] Каждый гейт проходит человек из колонки «Кто решает»; модель выдаёт только отчёт по критериям.
- [ ] Г-С1 не пройден при покрытии ФТ сценариями UC ниже 100 %.
- [ ] Возвраты записаны в 8.5; разделы после точки входа помечены `устарело`.
- [ ] oneshot-промпт не пересекает границу гейта (см. [архитектуру промптов](../../standards/bcreq-prompt-architecture.md#4-stepwise-и-oneshot)).

## Источники

- BABOK Guide v3 (5.1 Trace Requirements, 5.5 Approve Requirements, 7.2 Verify Requirements): <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/>
- ISO/IEC/IEEE 29148:2018: <https://www.iso.org/standard/72089.html>
- Реестр цитат чата 21–23.10.2026: [chat-2026-10-22-23-register.md](../../experiments/issue_387/chat-2026-10-22-23-register.md)
