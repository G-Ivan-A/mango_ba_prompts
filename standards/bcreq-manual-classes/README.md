---
status: draft
version: 0.1
updated: 2026-10-29
temperature: 0.1
owner: G-Ivan-A
---

# Инвентарь ручных промптов BCREQ

38 классов = 38 отдельных подробных стандартов. Класс определяется целью, обязательными входами и формой результата, а не числом файлов. Повторения одного класса в фазах — экземпляры с одинаковым контрактом. Индекс и общий транспорт не являются дополнительными стандартами классов. Статус всех новых правил — проект.

## Полный реестр

| Класс | Назначение / стандарт | Фазы | Существующий носитель (аналог, не готовая реализация) |
| --- | --- | --- | --- |
| C01 | [Приём исходного запроса](01-intake.md) | a-in | [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md) |
| C02 | [Атомарная нормализация](02-normalize.md) | a-in | [bcreq-context-understanding-stepwise.md](../../prompts/bcreq-context-understanding-stepwise.md) |
| C03 | [Оценка неоднозначности](03-ambiguity.md) | a-in, a-core, a-work | [bcreq-context-understanding-stepwise.md](../../prompts/bcreq-context-understanding-stepwise.md) |
| C04 | [Пакет вопросов](04-questions.md) | a-in, a-core, a-work, a-release | [bcreq-context-understanding-stepwise.md](../../prompts/bcreq-context-understanding-stepwise.md) |
| C05 | [Сопоставление с таксономией](05-taxonomy.md) | a-in | [bcreq-products-impact-analysis-stepwise.md](../../prompts/bcreq-products-impact-analysis-stepwise.md) |
| C06 | [Границы изменения](06-scope.md) | a-in, a-core, a-work | [bcreq-products-impact-analysis-stepwise.md](../../prompts/bcreq-products-impact-analysis-stepwise.md) |
| C07 | [Извлечение из web](07-web-evidence.md) | a-in, a-core, a-work | [bcreq-products-impact-analysis-stepwise.md](../../prompts/bcreq-products-impact-analysis-stepwise.md) |
| C08 | [Извлечение из PDF и runtime](08-document-evidence.md) | a-in, a-core, a-work | [bcreq-products-impact-analysis-stepwise.md](../../prompts/bcreq-products-impact-analysis-stepwise.md) |
| C09 | [Дообогащение материалами БА](09-ba-enrichment.md) | a-in, a-core, a-work | [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md) |
| C10 | [Разрешение конфликтов источников](10-source-conflicts.md) | a-in, a-core, a-work | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C11 | [Контроль полноты зависимостей](11-dependency-check.md) | a-in, a-core, a-work | [bcreq-products-impact-analysis-stepwise.md](../../prompts/bcreq-products-impact-analysis-stepwise.md) |
| C12 | [Полная сборка фазы](12-phase-assembly.md) | a-in, a-core, a-work, a-release | [bcreq-in-understanding-oneshot.md](../../prompts/bcreq-in-understanding-oneshot.md) |
| C13 | [Проверка переносимого контекста](13-handoff-check.md) | a-in, a-core, a-work, a-release | [bcreq-constitution-governance-oneshot.md](../../prompts/bcreq-constitution-governance-oneshot.md) |
| C14 | [Глоссарий](14-glossary.md) | a-in, a-core, a-work | [bcreq-context-understanding-stepwise.md](../../prompts/bcreq-context-understanding-stepwise.md) |
| C15 | [Бизнес-контекст](15-business-context.md) | a-in, a-core, a-work | [bcreq-context-understanding-stepwise.md](../../prompts/bcreq-context-understanding-stepwise.md) |
| C16 | [ФТ изменения существующего поведения](16-fr-delta.md) | a-core, a-work | [bcreq-fr-documentation-stepwise.md](../../prompts/bcreq-fr-documentation-stepwise.md) |
| C17 | [ФТ нового поведения с нуля](17-fr-new.md) | a-core, a-work | [bcreq-fr-documentation-stepwise.md](../../prompts/bcreq-fr-documentation-stepwise.md) |
| C18 | [Нефункциональные требования](18-nfr.md) | a-core, a-work | [bcreq-nfr-documentation-stepwise.md](../../prompts/bcreq-nfr-documentation-stepwise.md) |
| C19 | [Первый прогон UC и покрытие ФТ](19-uc-coverage.md) | a-core | [bcreq-uc-modeling-stepwise.md](../../prompts/bcreq-uc-modeling-stepwise.md) |
| C20 | [Подготовка доказательств человеческого гейта](20-gate-evidence.md) | a-in, a-core, a-work, a-release | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C21 | [ОРР L1](21-solution-l1.md) | a-work | [bcreq-orr-solution-design-stepwise.md](../../prompts/bcreq-orr-solution-design-stepwise.md) |
| C22 | [ОРР L2 и контракты стыков](22-solution-l2.md) | a-work | [bcreq-orr-solution-design-stepwise.md](../../prompts/bcreq-orr-solution-design-stepwise.md) |
| C23 | [Особенности и ограничения](23-constraints.md) | a-work | [bcreq-constraints-documentation-stepwise.md](../../prompts/bcreq-constraints-documentation-stepwise.md) |
| C24 | [Второй прогон UC и граничные случаи](24-uc-boundaries.md) | a-work | [bcreq-uc-modeling-stepwise.md](../../prompts/bcreq-uc-modeling-stepwise.md) |
| C25 | [Анализ рисков](25-risks.md) | a-work | [bcreq-extra-risk-analysis-stepwise.md](../../prompts/bcreq-extra-risk-analysis-stepwise.md) |
| C26 | [Реестр зависимостей поставки](26-delivery-dependencies.md) | a-work | [bcreq-extra-risk-analysis-stepwise.md](../../prompts/bcreq-extra-risk-analysis-stepwise.md) |
| C27 | [План приёмки](27-acceptance.md) | a-work | [bcreq-extra-risk-analysis-stepwise.md](../../prompts/bcreq-extra-risk-analysis-stepwise.md) |
| C28 | [Независимая содержательная проверка](28-independent-review.md) | a-core, a-work, a-release | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C29 | [Анализ влияния изменения](29-impact.md) | a-core, a-work, a-release | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C30 | [Адресная правка](30-targeted-edit.md) | a-core, a-work, a-release | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C31 | [Структурная сверка документа](31-conformance.md) | a-core, a-work, a-release | [bcreq-core-documentation-oneshot.md](../../prompts/bcreq-core-documentation-oneshot.md) |
| C32 | [Подготовка пакетов адресатам](32-audience-projection.md) | a-release | [letter-customer-documentation-legacy.md](../../prompts/letter-customer-documentation-legacy.md) |
| C33 | [Контроль выпускного комплекта](33-release-audit.md) | a-release | [bcreq-review-validation-oneshot.md](../../prompts/bcreq-review-validation-oneshot.md) |
| C34 | [Регистрация решений и согласований](34-human-record.md) | a-in, a-core, a-work, a-release | [bcreq-constitution-governance-oneshot.md](../../prompts/bcreq-constitution-governance-oneshot.md) |
| C35 | [Фиксация baseline и передача](35-baseline-handover.md) | a-release | [bcreq-constitution-governance-oneshot.md](../../prompts/bcreq-constitution-governance-oneshot.md) |
| C36 | [Загрузка правил и параметров чата](36-rule-bundle.md) | a-in, a-core, a-work, a-release | [bcreq-constitution-governance-oneshot.md](../../prompts/bcreq-constitution-governance-oneshot.md) |
| C37 | [User Story по запросу БА](37-user-story.md) | a-in, a-core, a-work | [bcreq-scenarios-modeling-oneshot.md](../../prompts/bcreq-scenarios-modeling-oneshot.md) |
| C38 | [Отдельное моделирование UC по запросу БА](38-requested-uc.md) | a-in, a-core, a-work | [bcreq-scenarios-modeling-oneshot.md](../../prompts/bcreq-scenarios-modeling-oneshot.md) |

## Последовательности экземпляров

Каждая запись — самостоятельный вставляемый промпт соответствующего класса. БА может повторить его или пропустить при выполненных предпосылках. Вопросы, обновление глоссария, решения и проверки повторяются при изменении входов. Это не автоматические переходы.

### a-in

| Экземпляр | Класс | Обязательный вход | Результат |
| --- | --- | --- | --- |
| a-in/C36 | Загрузка правил и параметров чата | `full_constitution, applicable_standards, versions, task_parameters, access_receipts` | `rule_receipt{documents,versions,available,missing,precedence}, task_config` |
| a-in/C01 | Приём исходного запроса | `raw_request, questionnaire?, additional_comments[{text,author_role?}]` | `request_id, raw_verbatim, questionnaire, comments, source_register` |
| a-in/C02 | Атомарная нормализация | `raw_verbatim, comments, source_register` | `atoms[{id,text,kind,actor,condition,source_id,locator}], ambiguities` |
| a-in/C03 | Оценка неоднозначности | `atoms, candidate_readings, known_decisions` | `ambiguities[{id,readings,impact,blocking,owner,needed_evidence}], resolved_ids` |
| a-in/C04 | Пакет вопросов | `ambiguities, missing_evidence, prior_questions, owners` | `questions[{id,text,options,recipient,blocks,deadline,source}], no_repeat_ids` |
| a-in/C05 | Сопоставление с таксономией | `atoms, taxonomy_snapshot, taxonomy_version` | `matches[{atom_id,domain,capability,feature,atomic_function,status,evidence}], gaps` |
| a-in/C06 | Границы изменения | `atoms, matches, BA_decisions, adjacent_dependencies` | `in_scope, out_of_scope, context_only, dependencies, owners` |
| a-in/C07 | Извлечение из web | `source_plan, accessible_page_bodies, URLs, versions` | `claims[{id,feature,verdict,quote,url,heading,version}], coverage, access_gaps` |
| a-in/C08 | Извлечение из PDF и runtime | `source_plan, attached_documents, runtime_sections?, provenance` | `claims[{id,feature,verdict,quote,document,section,pages?,version}], coverage, gaps` |
| a-in/C09 | Дообогащение материалами БА | `missing_evidence, BA_raw_materials?, author_roles, provenance` | `enriched_claims, cleaned_fragments, markup, source_links, remaining_gaps` |
| a-in/C10 | Разрешение конфликтов источников | `claims, versions, source_priorities, BA_decisions` | `conflicts[{id,claims,scope,versions,resolution,authority}], accepted_claims` |
| a-in/C11 | Контроль полноты зависимостей | `scope, claims, actors, settings, product_links, unresolved` | `dependency_manifest[{id,prerequisite,evidence,status}], retrieval_requests, recommendation` |
| a-in/C37 | User Story по запросу БА | `explicit_BA_request, atoms, scope, value, FR?` | `stories[{id,role,action,value,acceptance,fr_ids,source}], story_questions` |
| a-in/C38 | Отдельное моделирование UC по запросу БА | `explicit_BA_request, atoms, scope, actors, FR?` | `requested_UC[{id,actor,precondition,flow,alternatives,result,fr_ids,source}]` |
| a-in/C14 | Глоссарий | `terms_in_sections_2_to_6, raw_wording, supplied_lexicons` | `section_1[{term,definition,source,lexicon_comparison}], term_questions` |
| a-in/C15 | Бизнес-контекст | `atoms, scope, business_problem, value, decisions` | `section_2{context,problem,goal,in_scope,out_of_scope,products_owners}` |
| a-in/C34 | Регистрация решений и согласований | `human_message, actor_role, authority, candidate_revision, scope, timestamp` | `section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status}` |
| a-in/C12 | Полная сборка фазы | `base_snapshot, ordered_slices, tombstones, source_register, decisions` | `full_snapshot, entity_register, unresolved, superseded, completeness_receipt` |
| a-in/C13 | Проверка переносимого контекста | `full_snapshot, required_inputs_for_target, source_bodies, rule_bundle` | `handoff_receipt[{input,status,locator}], missing_inputs, recommendation` |
| a-in/C20 | Подготовка доказательств человеческого гейта | `gate_id, candidate_revision, applicable_gate_contract, checklist_evidence, human_records` | `gate_report{criteria,evidence,gaps,eligible_for_review,required_actors}, recommendation` |
### a-core

| Экземпляр | Класс | Обязательный вход | Результат |
| --- | --- | --- | --- |
| a-core/C36 | Загрузка правил и параметров чата | `full_constitution, applicable_standards, versions, task_parameters, access_receipts` | `rule_receipt{documents,versions,available,missing,precedence}, task_config` |
| a-core/C13 | Проверка переносимого контекста | `full_snapshot, required_inputs_for_target, source_bodies, rule_bundle` | `handoff_receipt[{input,status,locator}], missing_inputs, recommendation` |
| a-core/C03 | Оценка неоднозначности | `atoms, candidate_readings, known_decisions` | `ambiguities[{id,readings,impact,blocking,owner,needed_evidence}], resolved_ids` |
| a-core/C04 | Пакет вопросов | `ambiguities, missing_evidence, prior_questions, owners` | `questions[{id,text,options,recipient,blocks,deadline,source}], no_repeat_ids` |
| a-core/C06 | Границы изменения | `atoms, matches, BA_decisions, adjacent_dependencies` | `in_scope, out_of_scope, context_only, dependencies, owners` |
| a-core/C07 | Извлечение из web | `source_plan, accessible_page_bodies, URLs, versions` | `claims[{id,feature,verdict,quote,url,heading,version}], coverage, access_gaps` |
| a-core/C08 | Извлечение из PDF и runtime | `source_plan, attached_documents, runtime_sections?, provenance` | `claims[{id,feature,verdict,quote,document,section,pages?,version}], coverage, gaps` |
| a-core/C09 | Дообогащение материалами БА | `missing_evidence, BA_raw_materials?, author_roles, provenance` | `enriched_claims, cleaned_fragments, markup, source_links, remaining_gaps` |
| a-core/C10 | Разрешение конфликтов источников | `claims, versions, source_priorities, BA_decisions` | `conflicts[{id,claims,scope,versions,resolution,authority}], accepted_claims` |
| a-core/C11 | Контроль полноты зависимостей | `scope, claims, actors, settings, product_links, unresolved` | `dependency_manifest[{id,prerequisite,evidence,status}], retrieval_requests, recommendation` |
| a-core/C14 | Глоссарий | `terms_in_sections_2_to_6, raw_wording, supplied_lexicons` | `section_1[{term,definition,source,lexicon_comparison}], term_questions` |
| a-core/C15 | Бизнес-контекст | `atoms, scope, business_problem, value, decisions` | `section_2{context,problem,goal,in_scope,out_of_scope,products_owners}` |
| a-core/C16 | ФТ изменения существующего поведения | `request_atoms, verified_as_is, scope, BA_accepted_recommendations` | `section_3[{id,capability,requirement,delta,source}], rejected_candidates` |
| a-core/C17 | ФТ нового поведения с нуля | `explicit_new_mode_decision, request_atoms, scope, product_context` | `section_3_new[{id,capability,requirement,source}], novelty_boundary` |
| a-core/C18 | Нефункциональные требования | `supplied_quality_requirements, scope, applicable_source_thresholds` | `section_4[{id,characteristic,metric,threshold,conditions,source}], nfr_questions` |
| a-core/C37 | User Story по запросу БА | `explicit_BA_request, atoms, scope, value, FR?` | `stories[{id,role,action,value,acceptance,fr_ids,source}], story_questions` |
| a-core/C38 | Отдельное моделирование UC по запросу БА | `explicit_BA_request, atoms, scope, actors, FR?` | `requested_UC[{id,actor,precondition,flow,alternatives,result,fr_ids,source}]` |
| a-core/C19 | Первый прогон UC и покрытие ФТ | `sections_2_3_4, scope` | `section_7_first[{id,actor,precondition,flow,alternatives,result,fr_ids,class}], coverage_matrix` |
| a-core/C28 | Независимая содержательная проверка | `frozen_candidate, source_bodies, applicable_rules, approved_scope, decisions` | `findings[{id,claim,source,rule,severity,affected_ids}], checked_claims, unresolved` |
| a-core/C29 | Анализ влияния изменения | `baseline_revision, change_request, dependency_graph, prior_approvals` | `impact_set, stale_ids, invalidated_approvals, proposed_edit_scope` |
| a-core/C30 | Адресная правка | `candidate_revision, authorized_edit_scope, findings, human_instructions` | `patch[{id,before,after,reason}], preserved_ids, semantic_diff, stale_ids` |
| a-core/C31 | Структурная сверка документа | `candidate, schema_version, entity_register, trace_matrix` | `conformance_report{missing,duplicates,broken_refs,section_order,counts,verdict}` |
| a-core/C34 | Регистрация решений и согласований | `human_message, actor_role, authority, candidate_revision, scope, timestamp` | `section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status}` |
| a-core/C12 | Полная сборка фазы | `base_snapshot, ordered_slices, tombstones, source_register, decisions` | `full_snapshot, entity_register, unresolved, superseded, completeness_receipt` |
| a-core/C20 | Подготовка доказательств человеческого гейта | `gate_id, candidate_revision, applicable_gate_contract, checklist_evidence, human_records` | `gate_report{criteria,evidence,gaps,eligible_for_review,required_actors}, recommendation` |
### a-work

| Экземпляр | Класс | Обязательный вход | Результат |
| --- | --- | --- | --- |
| a-work/C36 | Загрузка правил и параметров чата | `full_constitution, applicable_standards, versions, task_parameters, access_receipts` | `rule_receipt{documents,versions,available,missing,precedence}, task_config` |
| a-work/C13 | Проверка переносимого контекста | `full_snapshot, required_inputs_for_target, source_bodies, rule_bundle` | `handoff_receipt[{input,status,locator}], missing_inputs, recommendation` |
| a-work/C03 | Оценка неоднозначности | `atoms, candidate_readings, known_decisions` | `ambiguities[{id,readings,impact,blocking,owner,needed_evidence}], resolved_ids` |
| a-work/C04 | Пакет вопросов | `ambiguities, missing_evidence, prior_questions, owners` | `questions[{id,text,options,recipient,blocks,deadline,source}], no_repeat_ids` |
| a-work/C06 | Границы изменения | `atoms, matches, BA_decisions, adjacent_dependencies` | `in_scope, out_of_scope, context_only, dependencies, owners` |
| a-work/C07 | Извлечение из web | `source_plan, accessible_page_bodies, URLs, versions` | `claims[{id,feature,verdict,quote,url,heading,version}], coverage, access_gaps` |
| a-work/C08 | Извлечение из PDF и runtime | `source_plan, attached_documents, runtime_sections?, provenance` | `claims[{id,feature,verdict,quote,document,section,pages?,version}], coverage, gaps` |
| a-work/C09 | Дообогащение материалами БА | `missing_evidence, BA_raw_materials?, author_roles, provenance` | `enriched_claims, cleaned_fragments, markup, source_links, remaining_gaps` |
| a-work/C10 | Разрешение конфликтов источников | `claims, versions, source_priorities, BA_decisions` | `conflicts[{id,claims,scope,versions,resolution,authority}], accepted_claims` |
| a-work/C11 | Контроль полноты зависимостей | `scope, claims, actors, settings, product_links, unresolved` | `dependency_manifest[{id,prerequisite,evidence,status}], retrieval_requests, recommendation` |
| a-work/C14 | Глоссарий | `terms_in_sections_2_to_6, raw_wording, supplied_lexicons` | `section_1[{term,definition,source,lexicon_comparison}], term_questions` |
| a-work/C15 | Бизнес-контекст | `atoms, scope, business_problem, value, decisions` | `section_2{context,problem,goal,in_scope,out_of_scope,products_owners}` |
| a-work/C16 | ФТ изменения существующего поведения | `request_atoms, verified_as_is, scope, BA_accepted_recommendations` | `section_3[{id,capability,requirement,delta,source}], rejected_candidates` |
| a-work/C17 | ФТ нового поведения с нуля | `explicit_new_mode_decision, request_atoms, scope, product_context` | `section_3_new[{id,capability,requirement,source}], novelty_boundary` |
| a-work/C18 | Нефункциональные требования | `supplied_quality_requirements, scope, applicable_source_thresholds` | `section_4[{id,characteristic,metric,threshold,conditions,source}], nfr_questions` |
| a-work/C21 | ОРР L1 | `sections_1_to_4, UC_first, verified_claims, scope` | `section_5_1{actors,context,behavior,interactions,fr_trace}, design_questions` |
| a-work/C22 | ОРР L2 и контракты стыков | `BA_level_decision, section_5_1, supplied_API_events, product_profiles` | `section_5_2{components,contract_deltas,compatibility,owners,fr_trace}, unresolved_contracts` |
| a-work/C23 | Особенности и ограничения | `section_5, source_constraints, scope_exclusions` | `section_6{features_refs,external_constraints[{id,source,consequence}]}` |
| a-work/C24 | Второй прогон UC и граничные случаи | `sections_3_to_6, UC_first, supplied_UI_API_contracts` | `section_7_second, boundary_matrix, uncovered_behavior` |
| a-work/C25 | Анализ рисков | `scope, design, uncertainty, evidence` | `section_8_1[{id,cause,event,consequence,probability,impact,measure,owner,source}], risk_questions` |
| a-work/C26 | Реестр зависимостей поставки | `dependency_manifest, design, team_responses, scope` | `section_8_2[{id,depends_on,type,blocks,human_status,owner,source}]` |
| a-work/C27 | План приёмки | `FR, NFR, UC, source_thresholds, proposed_acceptors` | `section_8_3[{id,given,when,then,requirement_id,method,acceptor}], acceptance_gaps` |
| a-work/C37 | User Story по запросу БА | `explicit_BA_request, atoms, scope, value, FR?` | `stories[{id,role,action,value,acceptance,fr_ids,source}], story_questions` |
| a-work/C38 | Отдельное моделирование UC по запросу БА | `explicit_BA_request, atoms, scope, actors, FR?` | `requested_UC[{id,actor,precondition,flow,alternatives,result,fr_ids,source}]` |
| a-work/C28 | Независимая содержательная проверка | `frozen_candidate, source_bodies, applicable_rules, approved_scope, decisions` | `findings[{id,claim,source,rule,severity,affected_ids}], checked_claims, unresolved` |
| a-work/C29 | Анализ влияния изменения | `baseline_revision, change_request, dependency_graph, prior_approvals` | `impact_set, stale_ids, invalidated_approvals, proposed_edit_scope` |
| a-work/C30 | Адресная правка | `candidate_revision, authorized_edit_scope, findings, human_instructions` | `patch[{id,before,after,reason}], preserved_ids, semantic_diff, stale_ids` |
| a-work/C31 | Структурная сверка документа | `candidate, schema_version, entity_register, trace_matrix` | `conformance_report{missing,duplicates,broken_refs,section_order,counts,verdict}` |
| a-work/C34 | Регистрация решений и согласований | `human_message, actor_role, authority, candidate_revision, scope, timestamp` | `section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status}` |
| a-work/C12 | Полная сборка фазы | `base_snapshot, ordered_slices, tombstones, source_register, decisions` | `full_snapshot, entity_register, unresolved, superseded, completeness_receipt` |
| a-work/C20 | Подготовка доказательств человеческого гейта | `gate_id, candidate_revision, applicable_gate_contract, checklist_evidence, human_records` | `gate_report{criteria,evidence,gaps,eligible_for_review,required_actors}, recommendation` |
### a-release

| Экземпляр | Класс | Обязательный вход | Результат |
| --- | --- | --- | --- |
| a-release/C36 | Загрузка правил и параметров чата | `full_constitution, applicable_standards, versions, task_parameters, access_receipts` | `rule_receipt{documents,versions,available,missing,precedence}, task_config` |
| a-release/C13 | Проверка переносимого контекста | `full_snapshot, required_inputs_for_target, source_bodies, rule_bundle` | `handoff_receipt[{input,status,locator}], missing_inputs, recommendation` |
| a-release/C04 | Пакет вопросов | `ambiguities, missing_evidence, prior_questions, owners` | `questions[{id,text,options,recipient,blocks,deadline,source}], no_repeat_ids` |
| a-release/C29 | Анализ влияния изменения | `baseline_revision, change_request, dependency_graph, prior_approvals` | `impact_set, stale_ids, invalidated_approvals, proposed_edit_scope` |
| a-release/C30 | Адресная правка | `candidate_revision, authorized_edit_scope, findings, human_instructions` | `patch[{id,before,after,reason}], preserved_ids, semantic_diff, stale_ids` |
| a-release/C31 | Структурная сверка документа | `candidate, schema_version, entity_register, trace_matrix` | `conformance_report{missing,duplicates,broken_refs,section_order,counts,verdict}` |
| a-release/C28 | Независимая содержательная проверка | `frozen_candidate, source_bodies, applicable_rules, approved_scope, decisions` | `findings[{id,claim,source,rule,severity,affected_ids}], checked_claims, unresolved` |
| a-release/C34 | Регистрация решений и согласований | `human_message, actor_role, authority, candidate_revision, scope, timestamp` | `section_8_5_record{id,decision,actor,authority,revision,scope,time,evidence,status}` |
| a-release/C12 | Полная сборка фазы | `base_snapshot, ordered_slices, tombstones, source_register, decisions` | `full_snapshot, entity_register, unresolved, superseded, completeness_receipt` |
| a-release/C20 | Подготовка доказательств человеческого гейта | `gate_id, candidate_revision, applicable_gate_contract, checklist_evidence, human_records` | `gate_report{criteria,evidence,gaps,eligible_for_review,required_actors}, recommendation` |
| a-release/C32 | Подготовка пакетов адресатам | `approved_or_draft_candidate, audience_policy, scope, approvals` | `customer_packet, internal_packet, delivery_manifest, excluded_items` |
| a-release/C33 | Контроль выпускного комплекта | `delivery_manifest, packets, candidate_revision, required_approvals, source_receipts` | `release_report{revision_checks,approval_checks,missing,stale,ready_for_human_release}` |
| a-release/C35 | Фиксация baseline и передача | `release_report, human_release_record?, final_packets, unresolved, owners` | `baseline_manifest{revision,artifacts,decisions,open_items,owners,delivery_status}, change_entrypoint` |

C16/C17 — альтернативы delta/new по решению БА, C22 — по уровню, C37/C38 — только по запросу. C07/C08/C09 — доступные и необходимые пути доказательств, не обязательное тройное чтение каждого источника. C29/C30 — только при изменениях. C34 выполняется после фактической реплики человека; отсутствие реплики сохраняется как pending. C12 готовит фазу, C20 предлагает гейт, человек решает, C34 фиксирует, C12 обновляет полный результат.

## Почему классы разделены

Нормализация не классифицирует продукт. Неоднозначность не формулирует пакет вопросов. Web и PDF/runtime имеют разные локаторы и риски доступа. Очистка, извлечение и разметка сырого материала БА остаются одной операцией C09 по прямому указанию основателя. C11 проверяет знания, C26 фиксирует зависимости поставки. C12 собирает текст, C13 проверяет переносимость, C36 проверяет правила. C19 проверяет покрытие, C24 проверяет решение и границы, C38 моделирует выбранный UC без заявления полноты. C25 и C26 имеют разные объекты и выходы. C28 проверяет смысл, C31 структуру, C33 комплект выпуска. C32 меняет аудиторию, C35 фиксирует baseline. Разница продукта сама по себе не порождает новый класс.

## Связанные контракты

- [Состояние и ручная работа](../../docs/contracts/bcreq-manual-state.md).
- [Обоснование и маршрут](../../docs/rfc/2026-10-bcreq-manual-pipeline.md).
- [Checkpoint до стандартов](../../docs/analysis/2026-10-29-bcreq-checkpoint.md).
