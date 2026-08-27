---
status: draft
version: 0.1
updated: 2026-08-26
temperature: 0.1
analysis-subtype: options
source: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/331"
scope: repo
based_on: "Индустриальные источники по Architecture Spike / ADR / RFC и техника BABOK «Interface Analysis»"
related_artifacts:
  - "runs/2026/RUN-0059/outputs/architecture-spike.md"
  - "standards/runs-contract-standard.md"
---

# Формат артефакта «архитектурный спайк» и передача БА → СА: индустриальные практики

Исследование выполнено по инициативе, явно разрешённой постановкой [#331](https://github.com/G-Ivan-A/mango_ba_prompts/issues/331): исполнитель вправе изучить практики оформления «BA-to-SA handoff» / «Architecture Spike» и предложить структуру. Цель — не описать интеграцию (это делает [`runs/2026/RUN-0059/outputs/architecture-spike.md`](../../runs/2026/RUN-0059/outputs/architecture-spike.md)), а **обосновать выбор жанра и структуры** этого документа.

## 1. Почему это не ADR

Индустрия разводит три жанра, и разница между ними — не в объёме, а в моменте жизненного цикла и в том, что документ утверждает.

| Жанр | Что утверждает | Когда пишется | Срок жизни |
| --- | --- | --- | --- |
| **Spike** | «Вот что мы выяснили и чего ещё не знаем» | До принятия решения, ограничен по времени | До закрытия неопределённости |
| **RFC / Design proposal** | «Предлагаю такую систему, обсудим» | До принятия решения, шире спайка | До мерджа реализации |
| **ADR** | «Выбрано X, потому что Y, ценой Z» | В момент принятия решения | Долгосрочно, переживает переписывание системы |

Опорные формулировки источников:

- Spike — «time-boxed research or investigation activity that helps a team reduce uncertainty before committing», он «produces knowledge, not working software»; в SAFe это разновидность Enabler Story для «exploration, architecture, infrastructure, research, design, and prototyping» с целью «gain the knowledge necessary to reduce the risk of a technical approach» ([Scaled Agile Framework, Spikes](https://scaledagileframework.com/spikes/)).
- Ограничение по времени и объёму — то, что отличает спайк от бесконечного «исследовательского энейблера»: по истечении таймбокса команда фиксирует найденное и принимает решение по имеющейся информации ([AgileSeekers, Spikes, Enablers, and Architectural Runway](https://agileseekers.com/blog/spikes-enablers-and-architectural-runway-for-uncertain-work)).
- Связка со спайком: «each time teams need to do some investigation they raise a spike, and the outcome of the spike is written up into an ADR» — то есть **спайк предшествует ADR, а не заменяет его** ([Dan Leech, Why I don't write ADRs](https://www.dantleech.com/blog/2024/03/10/why-i-dont-write-adrs/)).
- ADR «deliberately narrower than a software design document»: фиксирует один выбор и не описывает реализацию — «they describe why a particular approach was chosen» ([Scribelet, Architecture decision record examples](https://scribelet.app/blog/architecture-decision-record-examples)); RFC же используется, «when the main purpose is to propose, discuss, and refine a larger design before a decision is made», и один RFC может породить несколько ADR ([James Collerton, How to Write RFCs and ADRs](https://jc1175.medium.com/how-to-write-requests-for-comments-rfcs-and-architecture-decision-reviews-aa0992e3149f)).
- Канонический набор разделов ADR — контекст, решение, рассмотренные альтернативы, последствия ([AWS Prescriptive Guidance, ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)).

**Вывод для репозитория.** Артефакт RUN-0059 отвечает на вопрос «выполнима ли интеграция и какой ценой», а не «что мы решили». Ключевой факт прогона — часть контракта Mango закрыта публичной документацией лишь частично, а гипотеза Г1 не проверена на боевом доступе. Документ с непроверенными гипотезами не может быть ADR: ADR по определению утверждает принятое решение и живёт долго, а этот текст обязан устареть в момент, когда внутренний контракт Mango будет раскрыт. Поэтому дом артефакта — `runs/2026/RUN-0059/outputs/`, а не `docs/adr/`. Это совпадает с требованием постановки и с общей логикой «spike → ADR»: ADR по каналу HH.ru будет уместен **после** закрытия внутренних вопросов Mango.

## 2. Что берём из BABOK для части «БА → СА»

Передача от бизнес-анализа к системному анализу в BABOK покрывается техникой **Interface Analysis** (10.24): она «used to identify where, what, why, when, how, and for whom information is exchanged between solution components or across solution boundaries» и завершается шагом *Defining Interfaces* — «specify the interface requirements by describing the inputs, outputs, associated validation rules, and any event triggers» ([IIBA, BABOK Guide, 10.24 Interface Analysis](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-24-interface-analysis/); см. также разбор шагов у [Learning Tree](https://blog.learningtree.com/business-analysis-technique-interface-analysis/)).

Отсюда три обязательных элемента, которых нет в шаблоне ADR и которые постановка требует прямо:

1. **Триггеры и последовательность** — диаграммы последовательности (кто кого вызывает, в каком порядке, что происходит при сбое).
2. **Входы и выходы в терминах полей** — матрица маппинга данных `Сущность → поле источника → логика преобразования → поле приёмника`.
3. **Правила валидации и ограничения** — лимиты, идемпотентность, коды ошибок, размеры полей.

## 3. Итоговая структура, применённая в RUN-0059

Гибрид: каркас Design Proposal (контекст → варианты → рекомендация → последствия) + интерфейсная часть по BABOK.

| Раздел | Откуда взят | Адресат |
| --- | --- | --- |
| Контекст и рамки | ADR/RFC | БА, ПО |
| Что уже установлено (SSOT) | Spike: «produces knowledge» | все |
| Критический путь: диаграммы последовательности | Interface Analysis (триггеры) | СА, разработчик |
| Матрица маппинга данных | Interface Analysis (inputs/outputs) | СА, разработчик |
| Примеры JSON | Interface Analysis (валидация) | разработчик |
| Варианты решения и сравнение | RFC/ADR (alternatives) | архитектор, ПО |
| Рекомендация и митигация GAP-R1 | ADR (decision) | ПО, архитектор |
| Последствия и открытые вопросы | ADR (consequences) + Spike (что не узнали) | все |

## 4. Правило маркировки незакрытого

Спайк обязан отличать проверенное от предполагаемого — иначе он превращается в источник галлюцинаций. В RUN-0059 применены два маркера:

- `⚠️ ТРЕБУЕТСЯ УТОЧНЕНИЕ ВНУТРЕННЕГО КОНТРАКТА MANGO: публичный API не покрывает поле X` — форма задана постановкой #331 и ставится там, где публичная документация MDAPI молчит;
- `Г<N>` — непроверенная гипотеза, унаследованная из [`RUN-0058`](../../runs/2026/RUN-0058/outputs/L3-integration-architecture-notes.md).

Ни один эндпоинт, метод или JSON-структура Mango в артефакте не придуманы: каждый снабжён ссылкой на раздел `kb/processed/mdialogi-api`.

## Источники

- [Scaled Agile Framework — Spikes](https://scaledagileframework.com/spikes/)
- [AgileSeekers — Spikes, Enablers, and Architectural Runway](https://agileseekers.com/blog/spikes-enablers-and-architectural-runway-for-uncertain-work)
- [Dan Leech — Why I don't write ADRs](https://www.dantleech.com/blog/2024/03/10/why-i-dont-write-adrs/)
- [Scribelet — Architecture decision record examples: 10 real ADRs + template](https://scribelet.app/blog/architecture-decision-record-examples)
- [James Collerton — How to Write Requests for Comments (RFCs) and Architecture Decision Reviews (ADRs)](https://jc1175.medium.com/how-to-write-requests-for-comments-rfcs-and-architecture-decision-reviews-aa0992e3149f)
- [AWS Prescriptive Guidance — Architectural decision record process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [IIBA — BABOK Guide, 10.24 Interface Analysis](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-24-interface-analysis/)
- [Learning Tree — Business Analysis Technique: Interface Analysis](https://blog.learningtree.com/business-analysis-technique-interface-analysis/)
