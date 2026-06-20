---
status: draft
version: 0.1
updated: 2026-06-18
ai-generated: true
experiment: multichannel-agent-workload-2026-06-18
scope: prompts
related_artifacts:
  - "prompts/glossary-context-understanding-stepwise.md"
  - "prompts/questions-customer-understanding-stepwise.md"
  - "prompts/us-modeling-stepwise.md"
  - "prompts/uc-modeling-stepwise.md"
  - "prompts/technical-details-solution-design-stepwise.md"
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/109"
---

# Эксперимент: Многоканальная нагрузка агента (early-stage разбор)

> Фиксация по [`standards/experiment-log-standard.md`](../../../../standards/experiment-log-standard.md),
> Уровень 1 (прогон становится доказательной базой для RFC по промптам).

## Метрики (ядро из 6 полей)

- **iterations:** 5 (по одному прогону на шаг 1–5, с human-gate между шагами)
- **ba_edits:** 7 (ручные вставки: архитектурный слой Ф10; весь шаг нормализации 2.1/2.2/2.5; адаптация solution-design под ранний «Раздел 3»; пометки `?Bn` в US/UC; матрица gap; раздел «не найдено в документации»)
- **quality:** 4 (бизнес-уровень получился почти без правок; правки — это структурные пробелы цепочки, а не качество текста)
- **prompts_used:** [mango-glossary-context-understanding-stepwise, mango-questions-customer-understanding-stepwise, mango-us-modeling-stepwise, mango-uc-modeling-stepwise, mango-technical-details-solution-design-stepwise]
- **verdict:** works-with-edits
- **outcome:** Цепочка довела сырое требование до раннего разбора (нормализация + вопросы + US/UC + варианты). Три структурных пробела цепочки → RFC-MCH (P1 якорь арх-слоя, P2 шаг нормализации, P3 промпт «early-options»).

## Что генерировали

Ранний BA-разбор сырого требования о многоканальной одновременной работе агента
(голос/чат/e-mail, лимит 3, приоритет) для продукта Mango Office (КЦ + ЛК ВАТС).
Объём: глоссарий + As-Is, нормализация, вопросы заказчику, User Story/Use Case,
варианты доработки (Раздел 3). Не финальное ТЗ.

## Что сработало (с цитатами)

- **Проверка существующих решений (Эксперт по продукту) в questions-промпте.**
  Цитата БЗ: *«Очередь текстовых обращений и звонков не зависимы друг от друга»*
  [CC, §4.2, с.127] и *«максимальное количество текстовых обращений, которые может
  обрабатывать один сотрудник»* [LK, с.129] → шаг сразу выявил, что лимит **уже есть,
  но только для текста**. Это сняло ~3 потенциально лишних вопроса заказчику.
- **ШАГ 0 glossary-промпта (контекст из БЗ).** Заставил собрать выжимку As-Is до
  интерпретаций — корневой gap (нет единого счётчика + нет приоритета) проявился уже
  на контексте, а не на этапе вариантов.
- **us/uc-modeling-stepwise.** Бизнес-формулировка требования («возможность
  одновременной работы») чисто легла на Job Story и Cockburn-UC почти без правок.

## Что не сработало / правки БА (с цитатами)

- **Нет шага «нормализация требования».** Декомпозицию на атомарные A1–A7,
  разведение «боль vs решение» и gap-анализ пришлось делать вручную между glossary и
  questions. → правка структуры цепочки, не текста.
- **ШАГ 0 glossary не просит явно архитектурный слой (ЛК ВАТС vs КЦ).** Факт Ф10
  (*«настройка автоматического распределения … доступна только Руководителю и
  Администратору»* [CC, §4.2, с.127]; настройки — в ЛК, исполнение — в КЦ) добавлен
  вручную. Повтор паттернов Б1/Б5 из BCREQ-1025.
- **technical-details-solution-design-stepwise заточен под Раздел 7.** Для раннего
  «Раздела 3» (продуктовые варианты A/B/C без детального тех-дизайна) промпт
  адаптирован вручную — отдельного промпта «early-options» нет.

## Инсайты для онтологии

- Между операциями `understanding` (контекст) и `understanding` (вопросы) практически
  отсутствует под-операция **«нормализация требования»** — устойчивый разрыв (повтор
  на втором кейсе после BCREQ-1025).
- Якорь «архитектурный слой продукта» (ЛК ВАТС ↔ КЦ) нужен как **общий приём** для
  всех ранних промптов (связь с ADR-005, product-classification-contract).

## Предложения по промптам (RFC)

См. [`governance/rfc/prompt-improvement-multichannel-proposal.md`](../../../../governance/rfc/prompt-improvement-multichannel-proposal.md):

- **RFC-MCH-P1** → `glossary-context-understanding-stepwise`: добавить в ШАГ 0 явный
  под-шаг «зафиксировать архитектурный слой (ЛК ВАТС vs КЦ)».
- **RFC-MCH-P2** → новый шаг/промпт «нормализация требования» (декомпозиция + боль/решение + gap).
- **RFC-MCH-P3** → новый промпт `early-options` (варианты доработки «Раздел 3»),
  отделённый от `technical-details-solution-design` (Раздел 7).

## Вопросы для согласования

- Делать RFC-MCH-P2 отдельным промптом или под-шагом в glossary/questions?
- Объединять ли P1 с уже предложенным в BCREQ-1025 улучшением (избежать дублей в реестре RFC)?

## Полный лог

Пошаговые промежуточные результаты — в [`steps/`](../outputs/steps/); вход —
[`inputs/`](../inputs/); сводка — [`final-artifact.md`](../outputs/final-artifact.md).
