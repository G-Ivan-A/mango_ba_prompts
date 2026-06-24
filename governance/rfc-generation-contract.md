---
id: rfc-generation-contract
status: active
version: 0.1
updated: 2026-06-24
ai-generated: true
executable: true
machine_readable: true
type: contract
scope: rfc-generation
layer: L1
rule_class: combat
contract_registry_id: rfc-generation-contract
integrates: []
validated_by:
  - "scripts/validate_issue_226_rfc_generation_contract.py"
---
contract_id: rfc-generation-contract
artifact_type: rfc
output_artifact_layer: L3
output_format: "Markdown with YAML frontmatter"
output_language: ru
normative_keywords:
  - "ДОЛЖЕН"
  - "НЕ ДОЛЖЕН"
  - "СЛЕДУЕТ"
  - "МОЖНО"

purpose:
  applies_when: "Нужно сгенерировать RFC-документ L3 в Markdown с YAML frontmatter для governance, стандартов, процессов, контрактов, knowledge base или продуктовых артефактов."
  goals:
    - "Сделать RFC проверяемым предложением, а не скрытой реализацией."
    - "Заставить RFC явно отделять контекст, проблему, предложение, альтернативы, rationale, impact, implementation plan и canonical criteria."
    - "Сделать каждую проблему и каждое предложение machine-readable и трассируемым к источникам."
    - "Зафиксировать downstream impact через поля requires_adr, requires_standard и target_artifacts без описания transition rules."
    - "Сохранить краткий, однозначный и проверяемый стиль RFC."
  boundaries:
    result_role: "Generated RFC is a proposal artifact, not an approval decision, not an ADR, not a standard, and not an implementation patch."
    contract_does_not_define:
      - "RFC approval workflow."
      - "Transition rules from RFC to ADR."
      - "Transition rules from RFC to standard."
      - "Rules for editing existing RFC files."
      - "Rules for changing governance/rfc-process.md."
    human_owned_decisions:
      - "acceptance of the RFC"
      - "approval of downstream ADR creation"
      - "approval of downstream standard creation"
      - "approval of target artifact changes"

inputs:
  analytics_sources:
    required: true
    description: "Аналитические материалы, issue, PR discussion, audit, inventory, problem report или decision notes, из которых извлекаются проблемы и мотивация."
    accepted_shapes:
      - "repository_path"
      - "issue_or_pr_url"
      - "run_output_path"
      - "quoted_user_decision"
    read_rule: "Читать полностью релевантный источник; не заменять анализ пересказом по памяти."
    extraction_targets:
      - "confirmed_problems"
      - "business_or_governance_need"
      - "constraints"
      - "stakeholder_decisions"
      - "known_risks"
  report_sources:
    required: true
    description: "Отчёты, run logs, validation reports, self-test evidence, investigation notes или CI logs, подтверждающие наблюдения и edge cases."
    accepted_shapes:
      - "runs/YYYY/RUN-XXXX/outputs/*.md"
      - "runs/YYYY/RUN-XXXX/logs/*.md"
      - "docs/analysis/*.md"
      - "ci-logs/*.log"
      - "issue_comment_url"
    read_rule: "Использовать report source как evidence; если report отсутствует, явно остановиться или запросить недостающий источник."
    extraction_targets:
      - "observed_failures"
      - "validation_results"
      - "test_cases"
      - "before_after_state"
  research_sources:
    required: true
    description: "Внешние или внутренние практики RFC/design-doc/KEP/ADR, используемые для структуры, критериев и качества предложения."
    accepted_shapes:
      - "official_documentation_url"
      - "repository_policy_url"
      - "standard_url"
      - "local_research_dependency"
    read_rule: "Использовать только проверенный источник; не переносить внешнюю практику без связи с локальной проблемой."
    extraction_targets:
      - "required_sections"
      - "traceability_practices"
      - "status_lifecycle_clues"
      - "quality_criteria"
      - "prior_art_or_alternatives"
  existing_rfcs:
    required: true
    description: "Все существующие RFC-like документы репозитория, релевантные теме или формату нового RFC."
    accepted_shapes:
      - "governance/rfc/*.md"
      - "governance/rfc-to-hub-*.md"
      - "docs/analysis/rfc-*.md"
      - "docs/analysis/*-rfc.md"
    read_rule: "Проверять дублирование, статус, style drift, ID allocation и возможные conflicts before generation."
    extraction_targets:
      - "existing_problem_ids"
      - "existing_proposal_ids"
      - "status_patterns"
      - "duplicate_or_superseded_scope"
      - "local_section_patterns"
  product_docs:
    required: true
    description: "Product documentation, KB sections, taxonomy registries или domain docs, если RFC влияет на продукт, данные, user workflow или terminology."
    accepted_shapes:
      - "kb/mango-product-docs/**"
      - "kb/*/registry.json"
      - "standards/*.md"
      - "docs/*.md"
      - "official_product_doc_url"
    read_rule: "Если RFC затрагивает продукт или термин, привязать утверждение к product_docs; если не затрагивает, записать explicit not_applicable decision в RFC context."
    extraction_targets:
      - "official_terms"
      - "current_behavior"
      - "target_artifacts"
      - "taxonomy_refs"
      - "product_constraints"
  missing_required_source_policy:
    action: "stop_or_return_needs_clarification"
    generated_rfc_result: "not_created_until_source_is_available"
    forbidden_action: "Нельзя выдумывать source, заменять source общим знанием или оформлять неподтверждённую проблему как confirmed."

source_priority:
  - "Явное решение пользователя, issue или PR review по текущей задаче."
  - "Локальные governance стандарты и L1/L2 контракты."
  - "Report sources and run evidence from repository."
  - "Product docs and taxonomy registries."
  - "Existing RFC corpus and previous accepted proposals."
  - "External research sources from official project or standards documentation."

id_rules:
  rfc_id:
    required_format: "RFC-NNN"
    allocation_rule: "Использовать номер issue, если RFC создаётся для issue; иначе выбрать следующий свободный NNN после проверки existing_rfcs."
    stability_rule: "ID RFC не меняется после публикации, кроме явного supersede."
  problem_id:
    required_format: "RFC-NNN-P1"
    sequence_rule: "Проблемы нумеруются P1..Pn без пропусков внутри RFC."
    reuse_rule: "ID problem НЕ ДОЛЖЕН переиспользоваться для другой проблемы после публикации RFC."
  proposal_id:
    required_format: "RFC-NNN-R1"
    sequence_rule: "Правила или proposals нумеруются R1..Rn без пропусков внутри RFC."
    reuse_rule: "ID proposal НЕ ДОЛЖЕН переиспользоваться для другой proposal after publication."
  alternative_id:
    required_format: "RFC-NNN-A1"
    sequence_rule: "Alternatives нумеруются A1..An без пропусков внутри RFC."
  criteria_id:
    required_format: "RFC-NNN-C1"
    sequence_rule: "Canonical criteria нумеруются C1..Cn без пропусков внутри RFC."
  display_rule:
    - "При первом упоминании ID использовать backticks."
    - "В YAML-значениях ID записывать без backticks."

generation_process:
  step_1_load_inputs:
    id: RFC-GEN-STEP-01
    actions:
      - "Прочитать analytics_sources, report_sources, research_sources, existing_rfcs и product_docs."
      - "Отметить для каждого source stable_ref, title, type и used_for."
      - "Если required source отсутствует, остановить генерацию и вернуть needs_clarification."
  step_2_extract_evidence:
    id: RFC-GEN-STEP-02
    actions:
      - "Извлечь только подтверждённые problems, constraints, affected artifacts and decisions."
      - "Разделить observed problem, goal, proposed solution and implementation detail."
      - "Пометить каждое утверждение source_ref до генерации секции Problem."
  step_3_check_existing_rfcs:
    id: RFC-GEN-STEP-03
    actions:
      - "Проверить duplicates, superseded scope and conflicting accepted proposals."
      - "Определить next stable IDs for problem, proposal, alternative and criteria lists."
      - "Добавить related_contracts только для контрактов, которые RFC реально использует or changes."
  step_4_compose_output:
    id: RFC-GEN-STEP-04
    actions:
      - "Сформировать YAML frontmatter по frontmatter_schema."
      - "Сформировать sections 1..8 in the exact order from sections."
      - "Заполнить machine-readable YAML lists or indexes before explanatory prose inside each section."
  step_5_validate_output:
    id: RFC-GEN-STEP-05
    actions:
      - "Применить validation checks RFC-GEN-VAL-01..RFC-GEN-VAL-16."
      - "Если validation fails, вернуть RFC draft with explicit validation_errors or stop before publication."

frontmatter_schema:
  required_fields:
    id:
      type: string
      required_format: "RFC-NNN"
    status:
      type: string
      allowed_values:
        - draft
        - review
        - canonical
        - deprecated
    title:
      type: string
      rule: "Короткое имя предложения без solution hype."
    author:
      type: string
      rule: "Human, team or agent attribution."
    created:
      type: date
      required_format: "YYYY-MM-DD"
    updated:
      type: date
      required_format: "YYYY-MM-DD"
    layer:
      type: string
      required_value: "L3"
    type:
      type: string
      required_value: "rfc"
    related_contracts:
      type: list
      item_type: string
      rule: "Указывать only relevant L1/L2 contracts or empty list."
    target_artifacts:
      type: list
      item_type: string
      rule: "Указывать concrete repository paths, artifact classes, or empty list when none."
  forbidden_frontmatter_fields:
    - "implementation_status_without_decision"
    - "unreviewed_owner"
    - "implicit_source"
  ordering:
    - id
    - status
    - title
    - author
    - created
    - updated
    - layer
    - type
    - related_contracts
    - target_artifacts

sections:
  - id: RFC-GEN-SECTION-01
    number: 1
    title: "Context and motivation"
    required: true
    output_heading: "## 1. Context and motivation"
    purpose: "Explain why the RFC is needed now and what evidence triggered it."
    machine_readable_shape:
      context:
        source_refs: []
        affected_area: []
        current_state: []
        motivation: []
        not_in_scope: []
    required_fields:
      - "source_refs"
      - "affected_area"
      - "motivation"
      - "not_in_scope"
    rules:
      - "НЕ ДОЛЖЕН contain proposals as if already accepted."
      - "ДОЛЖЕН state product_docs not_applicable if no product behavior is affected."
  - id: RFC-GEN-SECTION-02
    number: 2
    title: "Problem"
    required: true
    output_heading: "## 2. Problem"
    purpose: "Define the complete problem list before proposing changes."
    machine_readable_shape:
      problems:
        - id: "RFC-NNN-P1"
          statement: "One problem, not goal and not solution."
          source_refs: []
          evidence: []
          impact: []
          affected_artifacts: []
    required_fields:
      - "problems"
      - "id"
      - "statement"
      - "source_refs"
      - "evidence"
      - "impact"
    rules:
      - "Every problem ID ДОЛЖЕН match RFC-NNN-Pn."
      - "Every problem ДОЛЖЕН have at least one source_ref."
      - "Problem statement НЕ ДОЛЖЕН include proposed solution wording."
      - "The problem list ДОЛЖЕН be complete for the RFC scope, not illustrative examples."
  - id: RFC-GEN-SECTION-03
    number: 3
    title: "Proposal"
    required: true
    output_heading: "## 3. Proposal"
    purpose: "Define the complete rule or change index that addresses the problem list."
    machine_readable_shape:
      proposal:
        RFC-NNN-R1:
          statement: "One proposed rule or change."
          problem_ids:
            - "RFC-NNN-P1"
          target_artifacts: []
          required_changes: []
          validation: []
          status: "proposed"
    required_fields:
      - "proposal"
      - "statement"
      - "problem_ids"
      - "target_artifacts"
      - "required_changes"
      - "validation"
    rules:
      - "Every proposal key ДОЛЖЕН match RFC-NNN-Rn."
      - "Every proposal ДОЛЖЕН link to at least one problem_id from section 2."
      - "Proposal ДОЛЖЕН be an index of proposed rules or changes, not narrative-only prose."
      - "Proposal НЕ ДОЛЖЕН contain implementation diff unless implementation_plan explicitly requires it."
  - id: RFC-GEN-SECTION-04
    number: 4
    title: "Alternatives considered"
    required: true
    output_heading: "## 4. Alternatives considered"
    purpose: "Record viable alternatives and why they are not selected."
    machine_readable_shape:
      alternatives:
        - id: "RFC-NNN-A1"
          summary: "Alternative approach."
          problem_ids: []
          tradeoffs: []
          decision: "not_selected"
          reason: "Short reason."
    required_fields:
      - "alternatives"
      - "id"
      - "summary"
      - "tradeoffs"
      - "decision"
      - "reason"
    rules:
      - "At least one alternative ДОЛЖЕН be recorded unless RFC explains no viable alternative."
      - "Alternative НЕ ДОЛЖЕН be a strawman or empty phrase."
  - id: RFC-GEN-SECTION-05
    number: 5
    title: "Rationale"
    required: true
    output_heading: "## 5. Rationale"
    purpose: "Explain why the proposal is preferred after alternatives."
    machine_readable_shape:
      rationale:
        decision_drivers: []
        source_refs: []
        problem_coverage: []
        rejected_tradeoffs: []
    required_fields:
      - "decision_drivers"
      - "source_refs"
      - "problem_coverage"
    rules:
      - "Rationale ДОЛЖЕН justify the proposal; it НЕ ДОЛЖЕН introduce new untraced requirements."
      - "Rationale ДОЛЖЕН distinguish evidence from preference."
  - id: RFC-GEN-SECTION-06
    number: 6
    title: "Impact"
    required: true
    output_heading: "## 6. Impact"
    purpose: "Expose downstream governance and artifact impact without defining transition rules."
    machine_readable_shape:
      impact:
        requires_adr: false
        adr_reason: "none"
        requires_standard: false
        standard_reason: "none"
        target_artifacts: []
        affected_contracts: []
        migration_or_backfill: []
        risks: []
    required_fields:
      - "requires_adr"
      - "requires_standard"
      - "target_artifacts"
      - "affected_contracts"
      - "risks"
    explicit_transition_fields:
      - "requires_adr"
      - "requires_standard"
      - "target_artifacts"
    rules:
      - "requires_adr ДОЛЖЕН be true when the RFC changes architecture, governance decision records, ownership boundaries or irreversible tradeoffs."
      - "requires_standard ДОЛЖЕН be true when the RFC changes reusable normative project rules."
      - "target_artifacts ДОЛЖЕН list concrete artifact paths or classes affected by the proposal."
      - "Section 6 НЕ ДОЛЖЕН define the process for converting RFC to ADR or standard."
  - id: RFC-GEN-SECTION-07
    number: 7
    title: "Implementation plan"
    required: false
    output_heading: "## 7. Implementation plan"
    purpose: "Describe non-binding execution sequence when implementation is known."
    machine_readable_shape:
      implementation_plan:
        steps:
          - id: "RFC-NNN-STEP-1"
            action: "One action."
            target_artifacts: []
            depends_on: []
        rollout: []
        validation: []
    required_when:
      - "RFC proposes changes to concrete repository artifacts."
      - "RFC has migration_or_backfill impact."
    omit_policy: "If omitted, write implementation_plan: not_specified with reason."
    rules:
      - "Implementation plan НЕ ДОЛЖЕН turn draft proposal into accepted implementation."
      - "Steps ДОЛЖНЫ link back to proposal IDs when possible."
  - id: RFC-GEN-SECTION-08
    number: 8
    title: "Canonical criteria"
    required: true
    output_heading: "## 8. Canonical criteria"
    purpose: "Define pass/fail criteria for deciding whether the RFC result is canonical."
    machine_readable_shape:
      canonical_criteria:
        - id: "RFC-NNN-C1"
          statement: "Observable criterion."
          verifies:
            - "RFC-NNN-R1"
          check: "Manual or automated check."
    required_fields:
      - "canonical_criteria"
      - "id"
      - "statement"
      - "verifies"
      - "check"
    rules:
      - "Every criterion ДОЛЖЕН be observable."
      - "Every proposal ДОЛЖЕН be covered by at least one canonical criterion."

traceability_rules:
  - id: RFC-GEN-TRACE-01
    statement: "Every problem has source."
    pass_condition: "Each problems[].source_refs list is non-empty and points to analytics_sources, report_sources, research_sources, existing_rfcs or product_docs."
  - id: RFC-GEN-TRACE-02
    statement: "Every proposal links to problem."
    pass_condition: "Each proposal entry has problem_ids and every ID exists in section 2."
  - id: RFC-GEN-TRACE-03
    statement: "Every canonical criterion verifies proposal."
    pass_condition: "Each canonical criteria verifies at least one RFC-NNN-Rn proposal."
  - id: RFC-GEN-TRACE-04
    statement: "Section 6 transition fields are explicit."
    pass_condition: "requires_adr, requires_standard and target_artifacts exist even when false or empty."
  - id: RFC-GEN-TRACE-05
    statement: "No untraced normative statement."
    pass_condition: "Any sentence using normative_keywords maps to a problem_id or proposal_id."
  - id: RFC-GEN-TRACE-06
    statement: "Existing RFC conflicts are handled."
    pass_condition: "RFC records duplicate check result in context or rationale."

style_rules:
  - id: RFC-GEN-STYLE-01
    rule: "Be concise."
    forbidden_patterns:
      - "long background not needed for decision"
      - "repeated motivation in multiple sections"
  - id: RFC-GEN-STYLE-02
    rule: "Be unambiguous."
    forbidden_patterns:
      - "можно улучшить"
      - "в целом"
      - "по возможности"
      - "желательно"
      - "и так далее"
  - id: RFC-GEN-STYLE-03
    rule: "Be verifiable."
    requirement: "Every proposal statement ДОЛЖЕН have validation or canonical criterion."
  - id: RFC-GEN-STYLE-04
    rule: "Do not use empty phrases."
    forbidden_patterns:
      - "повысить качество"
      - "сделать лучше"
      - "оптимизировать процесс"
      - "улучшить UX"
  - id: RFC-GEN-STYLE-05
    rule: "Do not mix problem, goal and solution."
    requirement: "Section 2 contains problems only; Section 3 contains proposal only; Section 5 contains rationale only."
  - id: RFC-GEN-STYLE-06
    rule: "Use active subject."
    requirement: "Prefer named actor or artifact subject over passive impersonal wording."
  - id: RFC-GEN-STYLE-07
    rule: "Use straight quotes for terms."
    requirement: "Use ASCII double quotes for terms; do not use curly quotes."
  - id: RFC-GEN-STYLE-08
    rule: "Use backticks for stable IDs in Markdown prose."
    requirement: "IDs like `RFC-NNN-P1` and `RFC-NNN-R1` use backticks outside YAML blocks."
  - id: RFC-GEN-STYLE-09
    rule: "Examples are illustrative only."
    requirement: "If examples appear, they must not replace the full required lists."

validation:
  checks:
    - id: RFC-GEN-VAL-01
      name: "contract_yaml_stream"
      applies_to: "this_contract"
      pass_condition: "Contract parses as YAML stream with metadata document and body document."
    - id: RFC-GEN-VAL-02
      name: "contract_has_no_markdown_prose"
      applies_to: "this_contract"
      pass_condition: "Contract contains no Markdown headings, tables or fenced blocks outside YAML scalar strings."
    - id: RFC-GEN-VAL-03
      name: "required_inputs_present"
      applies_to: "this_contract"
      pass_condition: "inputs contains analytics_sources, report_sources, research_sources, existing_rfcs and product_docs."
    - id: RFC-GEN-VAL-04
      name: "frontmatter_complete"
      applies_to: "generated_rfc"
      pass_condition: "Generated RFC frontmatter has id, status, title, author, created, updated, layer, type, related_contracts and target_artifacts."
    - id: RFC-GEN-VAL-05
      name: "required_sections_present"
      applies_to: "generated_rfc"
      pass_condition: "Generated RFC contains sections 1..8 in required order; section 7 may state not_specified."
    - id: RFC-GEN-VAL-06
      name: "problem_list_machine_readable"
      applies_to: "generated_rfc"
      pass_condition: "Section 2 has YAML problems list with stable RFC-NNN-Pn IDs."
    - id: RFC-GEN-VAL-07
      name: "problem_source_traceability"
      applies_to: "generated_rfc"
      pass_condition: "Every problem has non-empty source_refs; RFC without explicit source fails."
    - id: RFC-GEN-VAL-08
      name: "proposal_index_machine_readable"
      applies_to: "generated_rfc"
      pass_condition: "Section 3 has YAML proposal index keyed by stable RFC-NNN-Rn IDs."
    - id: RFC-GEN-VAL-09
      name: "proposal_problem_links"
      applies_to: "generated_rfc"
      pass_condition: "Every proposal links to at least one existing problem ID."
    - id: RFC-GEN-VAL-10
      name: "impact_fields_explicit"
      applies_to: "generated_rfc"
      pass_condition: "Section 6 explicitly has requires_adr, requires_standard and target_artifacts."
    - id: RFC-GEN-VAL-11
      name: "requires_adr_edge_case"
      applies_to: "generated_rfc"
      pass_condition: "When architectural or governance decision record is required, requires_adr is true and adr_reason is non-empty."
    - id: RFC-GEN-VAL-12
      name: "requires_standard_edge_case"
      applies_to: "generated_rfc"
      pass_condition: "When reusable normative rule changes, requires_standard is true and standard_reason is non-empty."
    - id: RFC-GEN-VAL-13
      name: "target_artifacts_complete"
      applies_to: "generated_rfc"
      pass_condition: "target_artifacts in frontmatter and section 6 are consistent."
    - id: RFC-GEN-VAL-14
      name: "style_rules_pass"
      applies_to: "generated_rfc"
      pass_condition: "Generated RFC avoids empty phrases, mixed problem/goal/solution and unverifiable proposal statements."
    - id: RFC-GEN-VAL-15
      name: "no_transition_rules"
      applies_to: "generated_rfc"
      pass_condition: "Generated RFC records requires_adr/requires_standard flags but does not define RFC-to-ADR or RFC-to-standard transition process."
    - id: RFC-GEN-VAL-16
      name: "existing_rfc_duplicate_check"
      applies_to: "generated_rfc"
      pass_condition: "Generated RFC records relation to existing_rfcs or confirms no duplicate scope."

testing_scenarios:
  - id: RFC-GEN-TEST-01
    name: "real_repository_issue"
    input_condition: "Issue asks for a governance RFC or contract change with analytics and existing RFC corpus."
    expected_result:
      - "Generated RFC uses RFC-NNN frontmatter."
      - "Problems use RFC-NNN-Pn IDs with source_refs."
      - "Proposal uses RFC-NNN-Rn index linked to problems."
      - "Impact includes requires_adr, requires_standard and target_artifacts."
  - id: RFC-GEN-TEST-02
    name: "rfc_without_explicit_source"
    input_condition: "A requested RFC has no analytics_sources, report_sources, research_sources, existing_rfcs or product_docs source for a problem."
    expected_result:
      - "Generation stops or returns needs_clarification without creating RFC."
      - "Validation fails RFC-GEN-VAL-07."
  - id: RFC-GEN-TEST-03
    name: "requires_adr_true"
    input_condition: "Proposal changes architecture, ownership boundary or irreversible governance decision."
    expected_result:
      - "Section 6 impact.requires_adr is true."
      - "Section 6 impact.adr_reason is non-empty."
      - "RFC does not define the ADR transition process."
  - id: RFC-GEN-TEST-04
    name: "requires_standard_true"
    input_condition: "Proposal changes reusable normative project rule."
    expected_result:
      - "Section 6 impact.requires_standard is true."
      - "Section 6 impact.standard_reason is non-empty."
      - "RFC does not define the RFC-to-standard transition process."

output_document_template:
  frontmatter_order:
    - "id"
    - "status"
    - "title"
    - "author"
    - "created"
    - "updated"
    - "layer"
    - "type"
    - "related_contracts"
    - "target_artifacts"
  body_order:
    - "## 1. Context and motivation"
    - "## 2. Problem"
    - "## 3. Proposal"
    - "## 4. Alternatives considered"
    - "## 5. Rationale"
    - "## 6. Impact"
    - "## 7. Implementation plan"
    - "## 8. Canonical criteria"
  yaml_blocks_required:
    - "context"
    - "problems"
    - "proposal"
    - "alternatives"
    - "rationale"
    - "impact"
    - "canonical_criteria"
  narrative_policy:
    allowed: true
    rule: "Markdown narrative may explain YAML blocks, but it must not replace machine-readable lists."

self_review:
  checklist:
    - "All five input groups were read or generation stopped with needs_clarification."
    - "Every problem has at least one source_ref."
    - "Every proposal links to at least one problem."
    - "Section 6 has requires_adr, requires_standard and target_artifacts."
    - "Section 7 is present or explicitly omitted with reason."
    - "Every proposal has a canonical criterion."
    - "No transition process beyond impact fields was introduced."
    - "No existing RFC file or governance/rfc-process.md was modified as part of generation."
