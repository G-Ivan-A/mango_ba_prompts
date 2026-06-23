---
id: bcreq-fr-generation-contract
status: active
version: 0.4
updated: 2026-06-23
ai-generated: true
executable: true
machine_readable: true
type: contract
scope: bcreq-fr
layer: L1
rule_class: combat
contract_registry_id: bcreq-fr-generation-contract
integrates:
  - "kb/industry-taxonomy/registry.json"
  - "kb/mango-taxonomy/registry.json"
validated_by:
  - "scripts/validate_issue_196_bcreq_fr_contract.py"
  - "scripts/validate_issue_208_bcreq_fr_l3_boundary.py"
  - "scripts/validate_issue_211_golden_examples_contract.py"
  - "scripts/validate_issue_215_bcreq_fr_yaml_contract.py"
---
contract_id: bcreq-fr-generation-contract
artifact_type: bcreq-fr
output_language: ru
normative_keywords:
  - "ДОЛЖЕН"
  - "НЕ ДОЛЖЕН"
  - "СЛЕДУЕТ"
  - "МОЖНО"

scope_rules:
  - id: BCREQ-FR-GEN-SCOPE-01
    source_rule: RFC-184-S1
    statement: "BCREQ-FR describes the requested change, not current functionality."
    applies_to:
      - "section-2"
      - "section-3"
      - "section-4"
      - "section-6"
    rationale: >
      Контракт локально встраивает правило чистого scope, чтобы агент не читал
      RFC-документы во время генерации BCREQ-FR.
  - id: BCREQ-FR-GEN-SCOPE-02
    source_rule: RFC-184-S2
    statement: "A single-user request does not justify changing functionality already closed explicitly or alternatively."
    applies_to:
      - "normalization"
      - "section-2"
      - "section-3"
      - "section-4"
    rationale: >
      Правило защищает BCREQ-FR от расширения scope за счёт потребностей,
      уже закрытых текущей функциональностью или альтернативным поведением.

purpose:
  applies_when: "Нужно получить документ BCREQ-FR с разделами 1, 2, 3, 4, 5, 6, 7 и итоговыми комментариями валидации."
  goals:
    - "Зафиксировать, какие разделы генерируются полностью, а какие выводятся заглушкой."
    - "Отделить бизнес-смысл, ожидаемое решение, функциональные требования, ограничения и материалы для разработки."
    - "Встроить правила чистого scope BCREQ-ФТ в локальные BCREQ-FR-GEN-SCOPE-01/02 без runtime-чтения RFC."
    - "Обеспечить атомарность, однозначность, краткость и проверяемую трассируемость на источники, taxonomy nodes, product docs и Golden Examples."
  agent_boundary:
    result_role: "Документ для согласования."
    human_owned_decisions:
      - "business scope"
      - "выбор варианта решения"
      - "принятие рисков"
      - "утверждение документа"

inputs:
  business_request:
    required: true
    description: "Сырой запрос заказчика, change decision, issue или transcript."
    read_rule: "Читать через доступный инструмент чтения."
  discussion_sources:
    required: true
    description: "Диалоги команд C/Q через репозиторный эквивалент, permalink или другой stable ref."
    read_rule: "Читать через permalink, репозиторный эквивалент или другой stable ref."
  golden_example:
    required: false
    status: "no-golden-standard"
    source_attachments:
      - status: "no-golden-standard"
    read_rule: "Approved Golden Example читать только через path + sha после явного согласования."
    lifecycle_contract: "kb/golden-examples/CONTRACT.md"
    replacement_rule: "Замена placeholder на path + sha требует 2-факторное подтверждение."
    rationale: >
      Пока утверждённого Golden Example нет, агент не должен читать внешние
      вложения, использовать bare filename или восстанавливать пример по памяти.
  scope_rules:
    required: true
    description: "Локальные BCREQ-FR-GEN-SCOPE-01/02 из этого контракта."
  taxonomy_sources:
    required: true
    description: "Industry/Mango Taxonomy registries."
    paths:
      - "kb/industry-taxonomy/registry.json"
      - "kb/mango-taxonomy/registry.json"
  product_docs:
    required: "if_requirement_describes_product_behavior"
    description: "Официальные Mango docs, processed KB или другой проверяемый источник."
  research_practices:
    required: false
    description: "Практики и исследования для best-practice вариантов."
    rationale: "Если источника нет, best practice не выдумывается."
  missing_required_source_policy:
    action: "stop_or_return_needs_clarification"
    forbidden_action: "Нельзя заполнять пробел предположением, памятью, названием файла или общим знанием."

source_priority:
  - "Явное решение issue/PR/review по текущей задаче."
  - "Диалоги команд C/Q через permalink или репозиторный эквивалент; approved Golden Example только при наличии path + sha."
  - "Локальные scope rules BCREQ-FR-GEN-SCOPE-01/02."
  - "Industry/Mango Taxonomy registries."
  - "Product docs / processed KB."
  - "Ранее созданные run-артефакты и patterns."

sections:
  - id: BCREQ-FR-SECTION-01
    number: 1
    title: "Термины и определения"
    generation_enabled: true
  - id: BCREQ-FR-SECTION-02
    number: 2
    title: "Проблема, цель, задачи"
    generation_enabled: true
    allowed_subsections:
      - "2.1"
      - "2.2"
      - "2.3"
      - "2.4"
  - id: BCREQ-FR-SECTION-03
    number: 3
    title: "Ожидаемое решение"
    generation_enabled: true
    allowed_subsections:
      - "3.1"
      - "3.2"
      - "3.3"
      - "3.4"
      - "3.5"
      - "3.6"
  - id: BCREQ-FR-SECTION-04
    number: 4
    title: "Функциональные требования и сценарии использования"
    generation_enabled: true
    hierarchy:
      - "4.x"
      - "4.x.x"
      - "4.x.x.x"
  - id: BCREQ-FR-SECTION-05-STUB
    number: 5
    title: "Нефункциональные требования"
    generation_enabled: false
    output: "stub"
  - id: BCREQ-FR-SECTION-06
    number: 6
    title: "Особенности реализации"
    generation_enabled: true
    allowed_subsections:
      - "6.1"
      - "6.2"
  - id: BCREQ-FR-SECTION-07-STUB
    number: 7
    title: "Материалы для разработки"
    generation_enabled: false
    known_structure:
      - "7.1"
      - "7.2"
      - "7.3"
      - "7.4"
    output: "stub"
  - id: BCREQ-FR-VALIDATION-SUMMARY
    title: "Комментарии: резюме тестирования и валидации"
    generation_enabled: true

generation_process:
  step_1_load_and_normalize_sources:
    description: "Загрузка и нормализация источников."
    actions:
      - "Прочитать issue, discussion sources, approved Golden Example при наличии, taxonomy registries и применимые product docs."
      - "Извлечь только подтверждённые проблемы, цели, задачи, роли, продукты, каналы, системы, функции и ограничения."
      - "Разделить текущую функциональность, исторический контекст и предмет доработки."
      - "Применить BCREQ-FR-GEN-SCOPE-01: требования, полностью закрытые текущей функциональностью, исключаются из BCREQ-FR."
      - "Применить BCREQ-FR-GEN-SCOPE-02: требования, альтернативно закрытые текущей функциональностью, исключаются из BCREQ-FR."
      - "Фиксировать обоснование исключений в run-log или analysis, но не в самом BCREQ-FR."
      - "Не переносить исторический контекст в раздел 2.1, если он не влияет на проектируемое решение."
  step_2_taxonomy_and_documentation_binding:
    description: "Taxonomy and documentation binding."
    per_entity_required_refs:
      - "industry_ref из kb/industry-taxonomy/registry.json."
      - "mango_ref из kb/mango-taxonomy/registry.json."
      - "Человекочитаемое русское бизнес-наименование, а не только slug."
      - "Product doc, processed KB section или иной проверяемый источник, когда требование описывает поведение продукта."
    missing_exact_node_policy:
      action: "Сослаться на ближайший canonical parent и пометить mapping_gap в итоговом validation summary."
      forbidden_action: "Запрещено придумывать taxonomy slug."
  step_3_result_decomposition:
    description: "Декомпозиция результата."
    section_order:
      - 1
      - 2
      - 3
      - 4
      - 5
      - 6
      - 7
      - "comments"
    bridge_rule: "Раздел 4 нельзя начинать, пока не построен верхнеуровневый мост раздела 3.6: FR-01 ... FR-N."
    subsection_growth_rule: "Разделы 2, 3, 4 и 6 нельзя расширять новыми подразделами сверх списка в этом контракте."
    quality_rule: "Качество повышается за счёт краткости, источников, трассируемости и валидации, а не за счёт разрастания структуры."

section_rules:
  section_1_terms:
    id: BCREQ-FR-SECTION-01
    include_only:
      - "Термины, без которых требования будут неоднозначными."
      - "Названия систем, продуктов, модулей и ролей, если они используются далее."
      - "Термины, для которых нужен taxonomy/product-doc binding."
      - "Определения, которые влияют на scope, права, состояния, события или проверки."
    exclude:
      - "Очевидные общеязыковые слова."
      - "Дубли общеизвестных понятий."
    definition_rule: "Каждый термин должен быть кратким: одно определение, один смысл."
    taxonomy_note_rule: "В конце раздела 1 должна быть краткая taxonomy note с Industry/Mango nodes, русскими названиями и registry paths."
  section_2_problem_goal_tasks:
    id: BCREQ-FR-SECTION-02
    purpose: "Ответить на вопрос, зачем делается изменение."
    allowed_subsections:
      "2.1":
        title: "Проблема"
        rule: "Описать текущую ситуацию, недостатки, причины и последствия для бизнеса, пользователей или системы; исторические варианты решения и исключённые требования не включать."
      "2.2":
        title: "Цель"
        rule: "Сформулировать целевое состояние как бизнес-результат; не описывать способ реализации."
      "2.3":
        title: "Задачи"
        rule: "Дать только достаточные и необходимые бизнес-задачи; не плодить детальные задачи, технические шаги и требования, закрытые As-Is."
      "2.4":
        title: "Ожидаемые результаты и эффект"
        rule: "Указать подтверждённый эффект: время, ошибки, качество данных, нормативы, снижение ручного труда, прозрачность процесса; если метрик нет, не раздувать раздел."
    task_scope_rule: "Каждая задача 2.3 должна проходить BCREQ-FR-GEN-SCOPE-01/02."
    as_is_policy: "Если задача описывает текущую функциональность, она исключается из BCREQ-FR и фиксируется только вне результирующего документа."
  section_3_expected_solution:
    id: BCREQ-FR-SECTION-03
    purpose: "Мост между бизнес-задачей и разделом 4: что меняется на верхнем уровне без детальных требований."
    allowed_subsections:
      "3.1":
        title: "Концепция решения"
        rule: "BPMN/UML Activity/Sequence или другая проверяемая high-level model, если источник и формат позволяют; текст 3-5 коротких абзацев только как пояснение к модели."
      "3.2":
        title: "Границы решения (Scope)"
        rule: "Минимальная таблица: продукты/модули, каналы, роли, out of scope; использовать taxonomy slugs и русские бизнес-наименования."
      "3.3":
        title: "Затрагиваемые системы и компоненты"
        rule: "Таблица система/компонент -> тип воздействия: новая разработка, изменение, использование без изменений, интеграция."
      "3.4":
        title: "Пользователи и заинтересованные стороны"
        rule: "Таблица роль -> влияние; не описывать обязанности подробно."
      "3.5":
        title: "Моделирование вариантов решения"
        rule: "Коротко описать 2-3 варианта: quick win, recommended/best practice, target; best practice должен опираться на Industry Taxonomy и проверенные practices/research; если источника нет, вариант помечается как не подтверждённый."
      "3.6":
        title: "Функциональные требования верхнего уровня"
        rule: "Список FR-01 ... FR-N без подуровней; формат: \"Система должна предоставлять\" + роль + возможность + контекст/условие."
    forbidden_in_3_6:
      - "FR-01.1"
      - "сценарии"
      - "атомарные параметры"
      - "UI-состояния"
      - "технические детали"
    detail_target: "Все детализации переносятся в раздел 4."
    variant_binding_rule: "FR-01 ... FR-N должны отражать выбранный или рекомендованный вариант из 3.5."
  section_4_functional_requirements:
    id: BCREQ-FR-SECTION-04
    purpose: "Ответить на вопрос, что должна делать система."
    decomposition_rule: "Каждый родительский FR-XX из 3.6 раскрывается в отдельный блок 4.x."
    hierarchy_rules:
      "4.x": "Родительское функциональное требование в формате \"Система должна...\" или \"Система должна предоставлять...\"."
      "4.x.x": "Короткая детализация поведения, сценария, правила, состояния или проверки; формулировка достаточная и не канцелярская."
      "4.x.x.x": "Атомарные значения, параметры, статусы, варианты, условия."
    forbidden_hierarchy: "Четвёртый уровень иерархии запрещён."
    atomicity_rule: "Одна строка требования описывает одно проверяемое поведение."
    concise_style_rule: "Для 4.x.x и 4.x.x.x использовать краткий стиль локальных правил и approved Golden Example, если он закреплён через path + sha."
    source_trace_template:
      source: "<business_request / discussion / product_doc / taxonomy / FR-XX>"
      industry: "<industry_ref + русское название>"
      mango: "<mango_ref + русское название>"
    implementation_boundary:
      forbidden: "Требования не должны описывать API, таблицы БД, классы, методы или внутреннюю реализацию, если это не единственный способ снять неоднозначность поведения."
      target_section: "Такие материалы относятся к разделу 7, который в BCREQ-FR не генерируется."
  section_5_nonfunctional_requirements:
    id: BCREQ-FR-SECTION-05-STUB
    generation_enabled: false
    stub_text: "Раздел не генерируется в рамках BCREQ-FR. Правила раздела зафиксированы в контракте governance/bcreq-fr-generation-contract.md; НФТ оформляются отдельным артефактом при наличии подтверждённого источника."
    nfr_like_input_policy: "Вынести NFR-like утверждения в run-log/analysis как candidates, но не включать в BCREQ-FR без отдельного решения."
  section_6_implementation_notes:
    id: BCREQ-FR-SECTION-06
    generation_enabled: true
    allowed_subsections:
      "6.1":
        title: "Ограничения"
        rule: "Зафиксировать ограничения, влияющие на требования: продуктовые, клиентские, правовые, организационные, релизные; не дублировать текущее поведение и не превращать ограничения в НФТ."
      "6.2":
        title: "Используемые технологии"
        rule: "Указать технологические опоры, платформы, сервисы или зависимости на уровне, достаточном для понимания решения; не раскрывать API/data model/architecture details."
    scope_filter_rule: "Ограничения 6.1 должны проходить BCREQ-FR-GEN-SCOPE-01/02."
    as_is_policy: "Если ограничение пересказывает As-Is без влияния на доработку, оно исключается."
  section_7_development_materials:
    id: BCREQ-FR-SECTION-07-STUB
    generation_enabled: false
    known_structure:
      "7.1": "Макеты пользовательского интерфейса"
      "7.2": "Интеграционные взаимодействия"
      "7.3": "Модели данных"
      "7.4": "Архитектурные материалы"
    stub_text: "Раздел не генерируется в рамках BCREQ-FR. UI, API, события, модели данных, очереди сообщений, C4/UML/DFD и архитектурные схемы оформляются отдельным техническим артефактом или ссылкой на уже существующий источник."
    leak_rule: "Запрещено переносить материалы 7.1-7.4 в разделы 3, 4 или 6 ради полноты."

style_rules:
  - "Писать коротко, однозначно и проверяемо."
  - "Не использовать вводные фразы без содержания: важно отметить, следует понимать, в целом, можно сказать."
  - "Не смешивать проблему, цель, решение, требование и ограничение в одном предложении."
  - "Не использовать разговорные формулировки и технический сленг разработчиков."
  - "Избегать предложений длиннее 25-30 слов; если мысль длиннее, разбить её."
  - "В требованиях использовать активный субъект: \"Система должна...\"."
  - "Для терминов, систем, продуктов, экранов, полей, кнопок и статусов использовать прямые кавычки."
  - "Stable IDs и paths писать в backticks."
  - "Не заменять ссылку пересказом, если источник доступен."

traceability:
  normative_statement_sources:
    - "входной запрос / transcript / attachment"
    - "FR-XX из раздела 3.6"
    - "Industry Taxonomy node"
    - "Mango Taxonomy entity"
    - "product doc / processed KB"
    - "локальное scope rule BCREQ-FR-GEN-SCOPE-01/02"
    - "accepted issue/PR/review decision"
  section_4_minimum_table_columns:
    - "FR"
    - "Раздел 4"
    - "Источник"
    - "Industry ref"
    - "Mango ref"
    - "Статус"
  missing_source_policy: "Если источник отсутствует, требование не попадает в финальный scope; оно фиксируется как open question или needs-clarification."

golden_examples_policy:
  current_state: "no-golden-standard"
  missing_standard_rule: "Агент не должен читать внешние вложения, использовать bare filename или восстанавливать пример по памяти."
  approved_standard_rule: "После появления approved Golden Example ссылка фиксируется только как path + sha по правилам kb/golden-examples/CONTRACT.md."
  replacement_controls:
    requires_2_factor_confirmation: true
    factors:
      - "Пользователь явно утверждает сам Golden Example через governance/approval-contract.md."
      - "Пользователь отдельным решением утверждает замену no-golden-standard в этом BCREQ-FR контракте на path + sha."
    automatic_replacement_allowed: false
  non_golden_example:
    path: "runs/2026/RUN-0012/outputs/2026-06-22-bcreq-180-mt-group-video-call-ft.md"
    usage_rule: "Можно использовать как близкий неэталонный пример структуры и traceability с учётом BCREQ-FR-GEN-SCOPE-01/02."
    exclusion_rule: "Исторический контекст и закрытая текущей функциональностью потребность исключаются."

validation:
  cadence: "Выполнять проверки после каждого крупного шага и вывести итоговый блок в конце документа."
  final_block_title: "Комментарии: резюме тестирования и валидации"
  checks:
    - id: BCREQ-FR-VAL-01
      name: "Полнота источников"
      condition: "Все обязательные источники прочитаны или явно отмечены needs-clarification."
    - id: BCREQ-FR-VAL-02
      name: "Scope rules"
      condition: "BCREQ-FR-GEN-SCOPE-01/02 применены к разделам 2, 3, 4, 6."
    - id: BCREQ-FR-VAL-03
      name: "Структура"
      condition: "Разделы 1, 2, 3, 4, 6 сгенерированы; разделы 5 и 7 выведены stub."
    - id: BCREQ-FR-VAL-04
      name: "Раздел 3 как мост"
      condition: "3.6 содержит только FR-01 ... FR-N без подуровней и детализации."
    - id: BCREQ-FR-VAL-05
      name: "Атомарность раздела 4"
      condition: "Каждое 4.x/4.x.x/4.x.x.x описывает одно проверяемое поведение."
    - id: BCREQ-FR-VAL-06
      name: "Однозначность"
      condition: "Нет местоимений без референта, двойных отрицаний и смешения ролей."
    - id: BCREQ-FR-VAL-07
      name: "Taxonomy traceability"
      condition: "Industry/Mango refs найдены в registry или помечен mapping_gap."
    - id: BCREQ-FR-VAL-08
      name: "Documentation traceability"
      condition: "Product behavior подкреплён официальным doc/KB source или помечен как gap."
    - id: BCREQ-FR-VAL-09
      name: "Style"
      condition: "Нет воды, 4.x.x краткие, термины/системы/поля оформлены прямыми кавычками."
    - id: BCREQ-FR-VAL-10
      name: "Stub discipline"
      condition: "НФТ и материалы разработки не просочились в разделы 3, 4, 6."

output_format:
  document_structure:
    - "# <Название BCREQ-FR>"
    - "## 1. Термины и определения"
    - "## 2. Проблема, цель, задачи"
    - "### 2.1. Проблема"
    - "### 2.2. Цель"
    - "### 2.3. Задачи"
    - "### 2.4. Ожидаемые результаты и эффект"
    - "## 3. Ожидаемое решение"
    - "### 3.1. Концепция решения"
    - "### 3.2. Границы решения (Scope)"
    - "### 3.3. Затрагиваемые системы и компоненты"
    - "### 3.4. Пользователи и заинтересованные стороны"
    - "### 3.5. Моделирование вариантов решения"
    - "### 3.6. Функциональные требования верхнего уровня"
    - "## 4. Функциональные требования и сценарии использования"
    - "### 4.1. <FR-01 title>"
    - "4.1. Система должна..."
    - "4.1.1. <short behavior>"
    - "4.1.1.1. <atomic value/state/condition>"
    - "## 5. Нефункциональные требования"
    - "<stub>"
    - "## 6. Особенности реализации"
    - "### 6.1. Ограничения"
    - "### 6.2. Используемые технологии"
    - "## 7. Материалы для разработки"
    - "<stub>"
    - "## Комментарии: резюме тестирования и валидации"
  validation_table_columns:
    - "Проверка"
    - "Результат"
    - "Комментарий"

self_review:
  contract_architect:
    checks:
      - "Файл является YAML stream без Markdown-прозы и fenced blocks."
      - "Provenance вынесен в governance/contracts-registry.md."
      - "Frontmatter integrates содержит только L2 registry paths."
      - "YAML rule index начинается сразу после metadata document."
    result: "pass"
  ba_expert:
    checks:
      - "Правила разделов 1-7 сохранены и разложены по YAML-структурам."
      - "Обоснования перенесены в rationale и policy fields."
      - "Scope rules BCREQ-FR-GEN-SCOPE-01/02 сохранены без изменения бизнес-смысла."
    result: "pass"
  ai_engineer:
    checks:
      - "Контракт парсится YAML parser."
      - "Stable IDs BCREQ-FR-* сохранены."
      - "Validator scripts фиксируют отсутствие Markdown fences, L3 links и старого provenance в контракте."
    result: "pass"
