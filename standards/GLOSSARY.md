---
status: canonical
version: 1.0
updated: 2026-06-04
ai-generated: false
source_hub: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/038868dd125b4e2d849ff73604890f1d2787ac0f/standards/GLOSSARY.md"
source_sha: "038868dd125b4e2d849ff73604890f1d2787ac0f"
source_of_truth: "hybrid-Intelligence-lab"
sync_policy: "explicit spoke sync from pinned Hub commit"
---

# Glossary

> Source of truth остаётся в Хабе (`hybrid-Intelligence-lab`). Этот файл в
> споке — воспроизводимая рабочая копия на `source_sha`; синхронизация
> выполняется только явным действием спока.

Версия: 1.0

Дата: 2026-05-26

Этот глоссарий фиксирует рабочие определения терминов для
`hybrid-Intelligence-lab`. Он нужен, чтобы issues, standards, governance-файлы
и AI-assisted changes использовали одни и те же различия между типами правил,
артефактов и режимов работы.

## Как использовать

1. При написании документа сверяйся с этим глоссарием до добавления нового
   термина или смены значения существующего.
2. Если термина нет, предложи добавление через Issue и укажи, какую
   операционную путаницу он снижает.
3. Используй `Policy`, `Standard`, `Contract` и `Guideline` как разные уровни
   обязательности, а не как взаимозаменяемые слова.
4. Для AI-assisted work явно указывай `Operating Mode`, если задача требует
   поведения, отличного от обычной structured work.
5. Ссылайся на canonical artifacts; historical migration records можно
   использовать как context, но не как активный источник правил.

## Термины

| Термин | Краткое определение | Контекст использования | Пример артефакта |
| --- | --- | --- | --- |
| Standard | Переиспользуемое правило или шаблон, который задает обязательный формат, минимальные поля или review-критерии для группы артефактов. Standard создается только при повторяющейся coordination или review problem. | Отличается от `Guideline` обязательностью, от `Policy` - фокусом на формате и качестве артефакта, а не на разрешениях или запретах поведения. | [standards/README.md](README.md), [standards/GLOSSARY.md](GLOSSARY.md) |
| Concept | Базовое описание цели, границ, аудитории и операционной модели решения. Concept объясняет, почему репозиторий или область устроены именно так. | Используется как смысловой источник для standards и policies. Отличается от `Framework`: concept фиксирует назначение и границы, framework задает метод работы. | [CONCEPT.md](../CONCEPT.md) |
| Policy | Обязательное правило принятия решений или ограничения поведения: что разрешено, запрещено, требует review или эскалации. | Используется там, где нарушение создает риск для безопасности, публикации, governance или качества. Отличается от `Standard`: policy регулирует действия участников, standard регулирует форму и готовность артефактов. | [AI_GOVERNANCE.md](../AI_GOVERNANCE.md), [governance/REPO_MODEL.md](../governance/REPO_MODEL.md) |
| Contract | Операционное соглашение между ролями, системами или репозиториями: обязанности, входы, выходы, lifecycle и критерии готовности. | Используется, когда важно зафиксировать взаимные ожидания, а не только отдельное правило. Contract может включать policies, standards и escalation rules. | [AI_GOVERNANCE.md](../AI_GOVERNANCE.md), future `TEAM_CONTRACT.md` |
| Practice | Повторяемый способ работы, который помогает достигать качества или скорости, но может адаптироваться к контексту. | Используется для описания привычек команды: локальная проверка, source-backed analysis, review checklist. Practice может стать guideline или standard, если повторяется и дает устойчивую пользу. | [CONTRIBUTING.md](../CONTRIBUTING.md), [tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh) |
| Framework | Структурированная методология для класса задач: понятия, роли, workflow, decision points, ограничения и примеры применения. | Создается только после сравнения с существующими подходами и выявленного gap. Отличается от `Practice`: framework связывает несколько practices и concepts в целостную модель. | `frameworks/<slug>/README.md` по правилу [governance/REPO_MODEL.md](../governance/REPO_MODEL.md) |
| Guideline | Рекомендация с объяснением, как действовать в типовом случае, без статуса жесткого правила. | Используется, когда полезен общий ориентир, но допустимы локальные исключения с объяснением в issue или PR. Отличается от `Policy`: guideline можно обоснованно обойти. | [CONTRIBUTING.md](../CONTRIBUTING.md), [standards/README.md](README.md) |
| Artifact | Проверяемый объект репозитория, который хранит знание, решение, шаблон, правило, эксперимент или вспомогательную проверку. | Используется как единица review и traceability. Artifact не обязан быть документом: validation script тоже artifact, если он поддерживает governance. | [CONCEPT.md](../CONCEPT.md), [tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh) |
| Canonical | Текущий утвержденный источник истины для темы. Canonical artifact используется по умолчанию в issues, reviews и AI context. | Отличается от `Draft`: canonical можно применять как действующее правило или reference. Если canonical artifact изменяется, нужна reviewable причина и обновление навигации. | [CONCEPT.md](../CONCEPT.md) с `status: canonical` |
| Draft | Черновик или proposal, который еще не является источником истины и требует review, проверки или решения owner. | Используется для исследовательских вариантов, будущих шаблонов и PR work-in-progress. Draft не должен отменять canonical artifact без явного решения в PR. | `research/<domain>/<topic>.md` до review, draft PR |
| Operating Mode | Явно заданный режим работы AI-assisted task, который определяет ожидаемую автономию, тип результата и допустимый уровень исследования. | `structured` используется по умолчанию для конкретных инструкций; `creative` подходит, когда дана цель и нужны варианты; `research`, `education` и `project` уточняют тип работы. | [AI_GOVERNANCE.md](../AI_GOVERNANCE.md), [.github/ISSUE_TEMPLATE/task.yml](../.github/ISSUE_TEMPLATE/task.yml) |
| Profile | Контекстная настройка framework, standard или risk model под конкретную область, проект, аудиторию или класс риска. | Используется, когда общий framework сохраняется, но нужны domain-specific controls, priorities или examples. Отличается от нового framework: profile адаптирует существующую модель, а не создает новую. | `projects/<project-slug>/README.md`, NIST AI RMF profile as external pattern |
| Bootstrap-клонирование (Кейс 2) | Процесс создания нового spoke-репозитория из шаблонов Хаба (`templates/spoke/`). Результат — физическая, постоянная структура репозитория с правильными файлами. | Ортогонален `Runtime-онбордингу`: bootstrap создаёт файлы один раз при рождении проекта, а не загружает контекст в память агента. Operating Mode задачи — `Project`. | [governance/proposals/rfc-two-cases-of-project-initialization.md](../governance/proposals/rfc-two-cases-of-project-initialization.md), [governance/proposals/rfc-creative-template-design.md](../governance/proposals/rfc-creative-template-design.md) |
| Runtime-онбординг (Кейс 1) | Процесс загрузки контекста проекта из репозитория в оперативную память агента, работающего в чате диалога. Результат — агент знает правила и контекст проекта; файлы при этом не создаются. | Ортогонален `Bootstrap-клонированию`: онбординг повторяется при каждом чате и является read-only до апрува человека. Operating Mode задачи — `Structured`. | [governance/proposals/rfc-agent-onboarding-protocol.md](../governance/proposals/rfc-agent-onboarding-protocol.md), [governance/proposals/rfc-two-cases-of-project-initialization.md](../governance/proposals/rfc-two-cases-of-project-initialization.md) |
| Handover Prompt | Шаблон промпта, который пользователь вставляет в чат LLM для инициации `Runtime-онбординга` агента. Параметризуется плейсхолдером `{{REPO_NAME}}` для переиспользования в споках. | Используется как «доверенность»: человек каждый раз уполномочивает агента действовать в границах проекта, не меняя структуру репозитория. | [governance/proposals/rfc-agent-onboarding-protocol.md](../governance/proposals/rfc-agent-onboarding-protocol.md) |
| Readback | Отчёт агента пользователю о прочитанных файлах и понятом контексте (цель, границы, стандарты, план) перед началом работы. Аналогия — «читка обратно» (readback) в авиации и health check в DevOps. | Ключевой анти-галлюцинационный момент `Runtime-онбординга`: расхождение в понимании обнаруживается здесь, а не в коде. | [governance/proposals/rfc-agent-onboarding-protocol.md](../governance/proposals/rfc-agent-onboarding-protocol.md) |
| Среда работы агента | Чат диалога (LLM-интерфейс), где агент «думает» и общается с пользователем. Агент НЕ работает внутри репозитория. | Ортогональна `Источнику контекста`. Введена, чтобы устранить ложную модель «агент живёт в репозитории» (см. issue #99). | [governance/proposals/rfc-two-cases-of-project-initialization.md](../governance/proposals/rfc-two-cases-of-project-initialization.md) |
| Источник контекста | Репозиторий (GitHub, файловая система) как внешняя база знаний, к которой агент обращается по алгоритму протокола. | Ортогонален `Среде работы агента`: агент *читает* источник, а не «живёт» внутри него. Постоянный результат `Bootstrap-клонирования`. | [governance/proposals/rfc-two-cases-of-project-initialization.md](../governance/proposals/rfc-two-cases-of-project-initialization.md) |
| North Star | Долгосрочное стратегическое направление проекта, выраженное одной формулировкой: куда репозиторий движется как продукт и какую нишу занимает. North Star задаёт *направление*, но не *темп* внедрения. | Используется как ориентир для приоритизации, не как обязательное `Policy`. Отличается от `Concept`: concept фиксирует текущие цель и границы, North Star указывает целевую нишу на горизонте. Темп движения регулируется матрицей применимости и `Триггерами внедрения`. | [research/hub/external-governance-patterns-review-2026-06.md](../research/hub/external-governance-patterns-review-2026-06.md) |
| Триггер внедрения | Заранее зафиксированное условие (операционная боль, инцидент или порог масштаба), при наступлении которого отложенную идею или артефакт нужно пересмотреть и, возможно, внедрить. | Операционализирует принцип «нет governance-артефакта без операционной боли» (Anti-Inflation). Используется в матрицах применимости: пока триггер не сработал — идея остаётся отложенной. Отличается от срока: триггер событийный, а не календарный. | [research/hub/external-governance-patterns-review-2026-06.md](../research/hub/external-governance-patterns-review-2026-06.md), [governance/REPO_MODEL.md](../governance/REPO_MODEL.md) |

## Связи терминов

| Связь | Как понимать |
| --- | --- |
| Concept -> Standard | Concept задает смысловые границы; standard превращает повторяющуюся часть этих границ в проверяемый формат. |
| Policy -> Contract | Policy задает обязательное правило; contract собирает несколько правил, ролей и ожиданий в рабочее соглашение. |
| Guideline -> Practice -> Standard | Guideline описывает рекомендуемый подход; practice показывает повторяемое применение; standard появляется, когда практику нужно сделать обязательной. |
| Framework -> Practice | Framework объединяет набор practices и decision rules в методологию для класса задач. |
| Framework -> Profile | Profile адаптирует framework под контекст без создания конкурирующей методологии. |
| Artifact -> Canonical / Draft | Artifact имеет lifecycle; canonical artifact действует как источник истины, draft artifact ожидает review. |
| Operating Mode -> Artifact | Operating Mode задает, какой тип артефакта ожидается и насколько исполнитель может исследовать варианты. |
| Standard -> Validation | Если standard можно проверить автоматически, правило добавляется в validation script или checklist. |
| Bootstrap-клонирование ⟂ Runtime-онбординг | Два ортогональных кейса инициализации проекта: первый создаёт постоянную структуру репо один раз, второй каждый раз загружает контекст в память агента. Манифест разделения — [governance/proposals/rfc-two-cases-of-project-initialization.md](../governance/proposals/rfc-two-cases-of-project-initialization.md). |
| Среда работы агента ⟂ Источник контекста | Чат диалога, где работает агент, и репозиторий, который он читает, — разные сущности. Агент не «живёт» в репозитории. |
| North Star -> Триггер внедрения | North Star задаёт направление движения; триггеры внедрения задают темп — момент, когда отложенная идея становится задачей. Вместе они не дают проекту ни застопориться, ни «убежать» в premature architecture. |

## Источники и адаптация

| Источник | Что адаптировано для репозитория |
| --- | --- |
| [GitHub Docs: rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) | Идея явных, видимых и исполняемых правил репозитория: policies и standards должны быть обнаружимы, а критичные правила желательно связывать с validation или review. |
| [CNCF governance templates](https://contribute.cncf.io/resources/templates/governance-intro/) | Governance documents должны описывать реальный способ принятия решений, а не имитировать зрелость. Это поддерживает Anti-Inflation principle в [governance/REPO_MODEL.md](../governance/REPO_MODEL.md). |
| [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html) | Разделение framework, artifacts, commitments и transparency адаптировано для knowledge hub: artifact должен давать reviewable основу для адаптации. |
| [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework) | Для AI governance взяты идеи govern/map/measure/manage, documented context и profiles как context-specific adaptation. |
| [RFC 2119 / BCP 14](https://datatracker.ietf.org/doc/rfc2119/) | Уровни обязательности нужно использовать экономно: обязательные слова должны появляться там, где нарушение действительно создает риск или ломает совместимость работы. |
