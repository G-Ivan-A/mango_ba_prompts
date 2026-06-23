---
status: draft
version: 0.1
updated: 2026-06-23
ai-generated: true
type: standard
layer: L3
rule_class: management
scope: executable-contracts
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/212"
depends_on:
  - "docs/analysis/executable-contracts-and-rfc-problems.md"
related_artifacts:
  - "standards/prompt-standard.md"
  - "standards/cascading-context-loading-standard.md"
  - "governance/rfc-process.md"
  - "governance/bcreq-fr-generation-contract.md"
  - "governance/contracts-registry.md"
  - "kb/golden-examples/CONTRACT.md"
validated_by:
  - "scripts/validate_issue_212_executable_contract_standard.py"
---

# Стандарт создания исполнимых контрактов

## 1. Введение

Этот документ закрывает Issue #212 и является L3-стандартом управления
контрактами, а не L1-исполняемым контрактом. Его задача — определить, как
создавать, размещать и проверять исполнимые контракты AI-агента так, чтобы
runtime-входы L1 не зависели от управленческих материалов L3.

Основание стандарта — отчёт
[`docs/analysis/executable-contracts-and-rfc-problems.md`](../docs/analysis/executable-contracts-and-rfc-problems.md),
а также существующие базовые артефакты:
[`standards/prompt-standard.md`](prompt-standard.md),
[`standards/cascading-context-loading-standard.md`](cascading-context-loading-standard.md),
[`governance/rfc-process.md`](../governance/rfc-process.md) и
[`governance/bcreq-fr-generation-contract.md`](../governance/bcreq-fr-generation-contract.md).
Если предложения отчёта расходятся с согласованными решениями Фаундера, этот
стандарт применяет согласованные решения Фаундера.

Нормативная классификация использует два независимых признака:

| Признак | Допустимые значения | Смысл |
| --- | --- | --- |
| `layer: L1\|L2\|L3` | `L1`, `L2`, `L3` | Уровень использования артефакта: runtime-инструкция, данные/реестр или управленческий стандарт. |
| `rule_class` | `combat`, `management`, `data` | Тип правила: боевое исполнение, управление изменениями или справочные данные. |
| `loading_layer` | например `loading_layer: executable` | Технический слой загрузки из стандарта cascading context; он не заменяет `layer`. |

Нормативная запись поля слоя в шаблоне: `layer: L1|L2|L3`.

Ключевой инвариант: L1-контракт должен быть самодостаточным для выполнения
задачи. Если правило L3 нужно агенту во время выполнения, оно переносится в L1
как локальное правило или в L2 как данные, а не подключается как runtime-вход L3.
Формат L1-контракта — 100% YAML: Markdown-проза запрещена, обоснования живут
только в `rationale:` или YAML-комментариях `#`.

## 2. Самостоятельная классификация артефактов

Классификация ниже выполнена по текущей структуре `standards/`, `governance/`,
`prompts/`, `runs/` и data-near контрактам `kb/`, а не по заранее заданному
списку. Для каждого класса использовались роль артефакта, место применения,
наличие исполнимых MUST/SHOULD правил и то, должен ли AI-агент читать файл при
выполнении конкретной задачи.

| Путь | Слой | Класс | rationale |
| --- | --- | --- | --- |
| `standards/artifact-naming-standard.md` | L3 | management | Определяет правила именования для будущих артефактов, но не является входом runtime-задачи. |
| `standards/ba-ontology.executable.md` | L3 | management | Имеет `loading_layer: executable`, но по содержанию загружает онтологический стандарт, а не боевую задачу. |
| `standards/ba-ontology.md` | L3 | management | Формализует модель БА и типы артефактов для проектного управления. |
| `standards/cascading-context-loading-standard.md` | L3 | management | Стандарт загрузки контекста; его правила применяются при проектировании L1, но не должны быть runtime-зависимостью L1. |
| `standards/industry-standards-standard.md` | L3 | management | Описывает требования к стандарту индустриальных классификаций. |
| `standards/industry-taxonomy-standard.md` | L3 | management | Определяет контракт таксономии и её registry/schema, а не конкретное выполнение задачи. |
| `standards/kb-standard.md` | L3 | management | Управляет структурой knowledge base. |
| `standards/mango-taxonomy-standard.md` | L3 | management | Определяет правила локальной таксономии Mango. |
| `standards/pattern-standard.md` | L3 | management | Стандартизирует карточки паттернов. |
| `standards/product-classification-contract.md` | L3 | management | Исторически назван contract, но по функции задаёт классификационную модель продукта. |
| `standards/prompt-standard.md` | L3 | management | Определяет контракт промпта и требования к frontmatter. |
| `standards/readme-standard.md` | L3 | management | Управляет структурой README. |
| `standards/runs-contract-standard.md` | L3 | management | Стандарт для run-контрактов; не является самим runtime-контрактом run. |
| `standards/GLOSSARY.md` | L2 | data | Справочник терминов; текущее размещение в `standards/` допустимо как legacy, но требует осознанного использования. |
| `standards/team-directory.md` | L2 | data | Справочник ролей и участников, а не нормативный стандарт. |
| `governance/approval-contract.md` | L1 | combat | Даёт агенту исполнимую процедуру согласования документов. |
| `governance/bcreq-fr-generation-contract.md` | L1 | combat | Исполнимый контракт генерации BCREQ-FR с локальными scope-правилами. |
| `governance/contracts-registry.md` | L2 | data | Реестр source/provenance контрактов; L1-контракт хранит только `contract_registry_id`. |
| `governance/rfc-process.md` | L3 | management | Описывает lifecycle RFC и статусы управленческих решений. |
| `governance/rfc-register.md` | L2 | data | Реестр RFC и их статусов. |
| `governance/rfc/bcreq-ft-scope-formation-rules-proposal.md` | L3 | management | RFC с proposed-правилами, которые нельзя подключать как runtime-вход L1 без локального переноса. |
| `prompts/README.executable.md` | L1 | combat | Исполнимая навигация по prompts с `loading_layer: executable`. |
| `prompts/README.md` | L3 | management | Навигация и правила каталога prompts; не является конкретным промптом. |
| `prompts/fr-documentation-stepwise.md` | L1 | combat | Активный prompt asset для выполнения задачи БА. |
| `prompts/questions-customer-understanding-stepwise.md` | L1 | combat | Активный prompt asset для выполнения задачи БА. |
| `prompts/session-debug-documentation-oneshot.md` | L1 | combat | Prompt asset для разового runtime-действия. |
| `prompts/archive/tz-stats-generator-legacy.md` | L1 | combat | Архивный, но по природе исполнимый prompt asset. |
| `runs/CONTRACT.md` | L1 | combat | Data-near контракт, который задаёт правила записи run. |
| `kb/golden-examples/CONTRACT.md` | L1 | combat | Data-near lifecycle-контракт для создания и проверки будущих Golden Examples; сами утверждённые examples остаются L2-данными. |
| `runs/README.md` | L2 | data | Навигация по run-хранилищу. |
| `runs/REGISTRY.md` | L2 | data | Реестр run-записей. |
| `runs/stats/by-type.md` | L2 | data | Агрегированная статистика по run-типам. |

## 3. Нормативный формат по уровням и YAML-шаблон L1

Новый или мигрируемый L1-контракт MUST быть 100% YAML-документом.
Markdown-проза запрещена. Пояснения и обоснования допустимы только в полях
`rationale:` или YAML-комментариях `#`. L1-контракт не хранит source/provenance
и не содержит гиперссылок на L3-артефакты; вместо этого он содержит только
`contract_registry_id`, а источники и решения фиксируются в
[`governance/contracts-registry.md`](../governance/contracts-registry.md).

L3-стандарты, включая этот документ, остаются Markdown-документами с YAML
frontmatter. L2-данные используют YAML/JSON для структур и Markdown для
текстовых знаний.

```yaml
# JSON-compatible YAML 1.2 payload for deterministic validation.
{
  "executable_contract_standard": {
    "standard_id": "executable-contract-standard",
    "version": "0.1",
    "layer": "L3",
    "rule_class": "management",
    "rationale": "The artifact defines how L1 contracts are created and governed, so it must not become a runtime dependency of those L1 contracts.",
    "classification_criteria": {
      "layer": {
        "L1": {
          "description": "Runtime execution artifact used directly by an AI agent for a concrete task.",
          "characteristics": [
            "contains imperative execution steps",
            "declares task inputs and outputs",
            "can be validated without reading L3 during task execution"
          ],
          "examples": [
            "governance/bcreq-fr-generation-contract.md",
            "governance/approval-contract.md",
            "runs/CONTRACT.md",
            "kb/golden-examples/CONTRACT.md",
            "prompts/fr-documentation-stepwise.md"
          ],
          "rationale": "L1 artifacts are combat-facing: they guide a task and therefore must be complete at runtime."
        },
        "L2": {
          "description": "Reference data, registry, glossary, taxonomy data, or navigation index consumed by L1 or humans.",
          "characteristics": [
            "stores facts or registry rows",
            "does not define lifecycle governance",
            "may be a runtime input when the L1 contract names it explicitly"
          ],
          "examples": [
            "runs/REGISTRY.md",
            "runs/stats/by-type.md",
            "standards/GLOSSARY.md"
          ],
          "rationale": "L2 artifacts provide stable data to L1 without forcing the agent to interpret management standards."
        },
        "L3": {
          "description": "Standard, RFC, ADR, process, audit, or other governance artifact used to design or change L1 and L2.",
          "characteristics": [
            "sets policy or lifecycle",
            "contains design rationale",
            "must be converted into L1 or L2 before becoming runtime input"
          ],
          "examples": [
            "standards/prompt-standard.md",
            "standards/cascading-context-loading-standard.md",
            "governance/rfc-process.md"
          ],
          "rationale": "L3 artifacts manage the system and prevent uncontrolled drift, but they are not task instructions."
        }
      },
      "rule_class": {
        "combat": {
          "description": "Rule used in a live task run or prompt execution.",
          "characteristics": [
            "has direct agent behavior",
            "affects task output",
            "belongs in L1 when normative"
          ],
          "examples": [
            "BCREQ-FR-GEN-SCOPE-01",
            "RUN-REC-META-01"
          ],
          "rationale": "Combat rules must be available exactly where the task executes."
        },
        "management": {
          "description": "Rule used to govern artifacts, processes, reviews, migrations, or standards.",
          "characteristics": [
            "changes how assets are created or approved",
            "does not directly produce task output",
            "belongs in L3 unless copied into L1 as a local runtime rule"
          ],
          "examples": [
            "PROMPT-STD-FM-01",
            "RFC status lifecycle"
          ],
          "rationale": "Management rules protect structure and governance, but runtime agents should not depend on them implicitly."
        },
        "data": {
          "description": "Registry or reference value consumed by a contract.",
          "characteristics": [
            "has factual rows or mappings",
            "can be checked for schema consistency",
            "does not issue procedural commands"
          ],
          "examples": [
            "runs/REGISTRY.md",
            "governance/rfc-register.md"
          ],
          "rationale": "Data artifacts are valid runtime inputs only when an L1 contract references them as data, not as policy."
        }
      }
    },
    "classification_inventory": [
      {
        "path": "standards/artifact-naming-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "Naming rules are governance for future artifacts."
      },
      {
        "path": "standards/ba-ontology.executable.md",
        "layer": "L3",
        "rule_class": "management",
        "loading_layer": "executable",
        "rationale": "The executable loading companion exposes ontology context, but the content remains a management standard."
      },
      {
        "path": "standards/ba-ontology.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The ontology defines project-wide analytical concepts."
      },
      {
        "path": "standards/cascading-context-loading-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document defines the context-loading governance model."
      },
      {
        "path": "standards/industry-standards-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document standardizes industry standards artifacts."
      },
      {
        "path": "standards/industry-taxonomy-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document defines taxonomy contract and schema expectations."
      },
      {
        "path": "standards/kb-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs knowledge base structure."
      },
      {
        "path": "standards/mango-taxonomy-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs Mango taxonomy structure."
      },
      {
        "path": "standards/pattern-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs pattern cards."
      },
      {
        "path": "standards/product-classification-contract.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The file name says contract, but the function is product-classification governance."
      },
      {
        "path": "standards/prompt-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs prompt structure and metadata."
      },
      {
        "path": "standards/readme-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs README structure."
      },
      {
        "path": "standards/runs-contract-standard.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document is the standard for run contracts, not the run contract itself."
      },
      {
        "path": "standards/GLOSSARY.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The glossary is reference data even though it currently lives under standards."
      },
      {
        "path": "standards/team-directory.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The team directory is reference data for roles and ownership."
      },
      {
        "path": "governance/approval-contract.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The contract drives an agent approval workflow."
      },
      {
        "path": "governance/bcreq-fr-generation-contract.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The contract drives BCREQ-FR generation at runtime."
      },
      {
        "path": "governance/contracts-registry.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The registry stores source/provenance for contracts so L1 contracts can carry only contract_registry_id."
      },
      {
        "path": "governance/rfc-process.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The document governs RFC lifecycle and statuses."
      },
      {
        "path": "governance/rfc-register.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The document records RFC rows and status data."
      },
      {
        "path": "governance/rfc/bcreq-ft-scope-formation-rules-proposal.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The RFC proposes scope rules; accepted runtime rules must be copied into L1."
      },
      {
        "path": "prompts/README.executable.md",
        "layer": "L1",
        "rule_class": "combat",
        "loading_layer": "executable",
        "rationale": "The file is an executable navigation entry for prompt use."
      },
      {
        "path": "prompts/README.md",
        "layer": "L3",
        "rule_class": "management",
        "rationale": "The README governs prompt catalog usage rather than performing one task."
      },
      {
        "path": "prompts/fr-documentation-stepwise.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The prompt is a runtime instruction asset."
      },
      {
        "path": "prompts/questions-customer-understanding-stepwise.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The prompt is a runtime instruction asset."
      },
      {
        "path": "prompts/session-debug-documentation-oneshot.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The prompt is a runtime instruction asset."
      },
      {
        "path": "prompts/archive/tz-stats-generator-legacy.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "Archived prompts remain executable in nature, even when inactive."
      },
      {
        "path": "runs/CONTRACT.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The contract is used to create and validate run records."
      },
      {
        "path": "kb/golden-examples/CONTRACT.md",
        "layer": "L1",
        "rule_class": "combat",
        "rationale": "The data-near lifecycle contract is used to create and validate future Golden Example records while approved examples remain L2 data."
      },
      {
        "path": "runs/README.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The README navigates run storage and does not issue task procedure."
      },
      {
        "path": "runs/REGISTRY.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The registry stores run rows."
      },
      {
        "path": "runs/stats/by-type.md",
        "layer": "L2",
        "rule_class": "data",
        "rationale": "The file stores aggregated run statistics."
      }
    ],
    "layer_format_matrix": {
      "L1": {
        "format": "100% YAML",
        "prose_policy": "Markdown prose is forbidden; use rationale fields or YAML comments only.",
        "rationale": "Runtime contracts must be parseable by agents and CI without a Markdown interpretation step."
      },
      "L2": {
        "format": "YAML/JSON for structured data; Markdown for textual knowledge",
        "prose_policy": "Markdown is allowed only when the artifact is knowledge text rather than a schema, registry, or validation fixture.",
        "rationale": "L2 can be consumed as data or reference knowledge; the format follows the data shape."
      },
      "L3": {
        "format": "Markdown with YAML frontmatter",
        "prose_policy": "Governance explanation, analysis, RFC, and standards prose belongs in L3.",
        "rationale": "L3 exists for human governance and design rationale, not direct runtime execution."
      }
    },
    "format_rules": [
      {
        "id": "EXEC-CONTRACT-FORMAT-01",
        "content_type": "L1 executable contracts",
        "format": "100% YAML",
        "criterion": "Use a single parseable YAML document for runtime rules, task scope, inputs, outputs, validation, and stop conditions.",
        "rationale": "Stable structured fields prevent hybrid Markdown/YAML contracts from drifting or requiring prose parsing."
      },
      {
        "id": "EXEC-CONTRACT-FORMAT-02",
        "content_type": "L1 rationale and explanations",
        "format": "YAML rationale fields or YAML comments",
        "criterion": "Put explanation only in rationale fields or comments beginning with #; do not add Markdown sections to L1.",
        "rationale": "Reviewers still get context while the runtime contract remains machine-readable."
      },
      {
        "id": "EXEC-CONTRACT-FORMAT-03",
        "content_type": "L1 source/provenance",
        "format": "contract_registry_id only",
        "criterion": "Store sources, approvals, L3 decisions, and historical links in governance/contracts-registry.md, not in the L1 contract.",
        "rationale": "Runtime inputs stay clean while traceability remains auditable in an L2 registry."
      },
      {
        "id": "EXEC-CONTRACT-FORMAT-04",
        "content_type": "L2 structured data",
        "format": "YAML/JSON for structured data; Markdown for textual knowledge",
        "criterion": "Use YAML/JSON for registries, taxonomies, enumerations, schemas, and fixtures; use Markdown only for narrative knowledge.",
        "rationale": "Structured L2 data should be consumed without inferring semantics from prose tables."
      },
      {
        "id": "EXEC-CONTRACT-FORMAT-05",
        "content_type": "L3 governance artifacts",
        "format": "Markdown with YAML frontmatter",
        "criterion": "Use Markdown with frontmatter for standards, RFC, ADR, analysis, and process documents.",
        "rationale": "L3 documents optimize for human review, not direct task execution."
      }
    ],
    "provenance_rules": {
      "registry_path": "governance/contracts-registry.md",
      "registry_layer": "L2",
      "l1_contract_field": "contract_registry_id",
      "l1_allowed_provenance_shape": "single opaque registry id only",
      "forbidden_l1_fields": [
        "source_hub",
        "source_sha",
        "governance_sources",
        "related_artifacts",
        "depends_on",
        "L3 hyperlinks"
      ],
      "registry_records": [
        "id",
        "path",
        "version",
        "status",
        "layer",
        "rule_class",
        "provenance",
        "integrates",
        "related_artifacts",
        "validated_by",
        "approved_decisions",
        "rationale"
      ],
      "rationale": "Provenance is governance data, not runtime instruction. Keeping it in one registry avoids direct L3 hyperlinks in L1 contracts."
    },
    "contract_template": {
      "format": "100% YAML",
      "markdown_prose": "forbidden",
      "top_level_fields": {
        "status": {
          "required": true,
          "allowed": [
            "draft",
            "active",
            "canonical",
            "archived"
          ],
          "rationale": "The lifecycle state must be machine-checkable."
        },
        "version": {
          "required": true,
          "example": "0.1",
          "rationale": "Versioned contracts can be reviewed and migrated deterministically."
        },
        "type": {
          "required": true,
          "value": "contract",
          "rationale": "The artifact declares its role without relying on filename heuristics."
        },
        "executable": {
          "required": true,
          "value": true,
          "rationale": "L1 contracts are direct runtime inputs."
        },
        "layer": {
          "required": true,
          "value": "L1",
          "rationale": "The L1 layer marks direct task execution."
        },
        "rule_class": {
          "required": true,
          "value": "combat",
          "rationale": "L1 executable contracts contain combat rules."
        },
        "contract_registry_id": {
          "required": true,
          "example": "bcreq-fr-generation-contract",
          "rationale": "The contract points to source/provenance in governance/contracts-registry.md without embedding L3 links."
        },
        "created": {
          "required": true,
          "example": "YYYY-MM-DD",
          "rationale": "Creation date supports lifecycle review."
        },
        "updated": {
          "required": true,
          "example": "YYYY-MM-DD",
          "rationale": "Update date supports drift detection."
        },
        "owner": {
          "required": true,
          "example": "role-or-team",
          "rationale": "Ownership is needed for escalation and review."
        },
        "runtime_inputs": {
          "required": true,
          "allowed_layers": [
            "L1",
            "L2"
          ],
          "forbidden_layers": [
            "L3"
          ],
          "example": [
            {
              "id": "taxonomy_registry",
              "path": "kb/mango-taxonomy/registry.json",
              "layer": "L2",
              "required": true,
              "rationale": "Taxonomy registries are data inputs, not governance instructions."
            }
          ],
          "rationale": "Runtime dependencies must be explicit and must not require L3 interpretation."
        },
        "outputs": {
          "required": true,
          "example": [
            {
              "id": "target_artifact",
              "path_pattern": "runs/YYYY/RUN-XXXX/outputs/*.md",
              "rationale": "Outputs are part of the executable task boundary."
            }
          ],
          "rationale": "A contract must declare what task evidence it creates."
        },
        "rules": {
          "required": true,
          "example": [
            {
              "id": "CONTRACT-GEN-SCOPE-01",
              "statement": "An executable generation contract MUST declare concrete task scope, runtime inputs, expected outputs, and stop conditions.",
              "applies_to": [
                "generation_contract"
              ],
              "validation": "Check top-level fields for scope, runtime_inputs, outputs, and stop_conditions.",
              "rationale": "Generation contracts are L1 combat artifacts and must not force the agent to reconstruct task boundaries from L3 prose."
            },
            {
              "id": "RUN-REC-META-01",
              "statement": "A run recording contract MUST define required metadata, registry update rules, and evidence placement.",
              "applies_to": [
                "runs_contract"
              ],
              "validation": "Check metadata requirements, registry update rules, and output/log placement.",
              "rationale": "Run records are audit evidence and need stable data-near execution rules."
            },
            {
              "id": "PROMPT-STD-FM-01",
              "statement": "A prompt standard MUST distinguish prompt metadata rules from runtime prompt instructions.",
              "applies_to": [
                "prompt_standard"
              ],
              "validation": "Check that standard rules stay in L3 and runtime prompt instructions are embedded in prompt assets.",
              "rationale": "Prompt authors need governance, while prompt users need self-contained L1 execution."
            }
          ],
          "rationale": "Stable rule IDs make validation and review deterministic."
        },
        "validation": {
          "required": true,
          "example": [
            {
              "id": "L1-ONLY-INPUTS",
              "check": "Every runtime_inputs row has layer L1 or L2.",
              "rationale": "L1 must not require L3 artifacts at runtime."
            }
          ],
          "rationale": "Each contract must declare how its own invariants can be checked."
        },
        "stop_conditions": {
          "required": false,
          "example": [
            "required_input_missing",
            "L3_runtime_input_detected"
          ],
          "rationale": "Stop conditions prevent silent fallback to governance interpretation."
        },
        "change_control": {
          "required": false,
          "example": {
            "requires_review": true,
            "registry_update_required": true
          },
          "rationale": "Change governance belongs in structured fields, not Markdown prose."
        }
      }
    },
    "placement_rules": [
      {
        "id": "EXEC-CONTRACT-PLACE-01",
        "target": "governance/<scope>-contract.md",
        "criterion": "Place cross-cutting L1 governance or generation contracts in governance root.",
        "rationale": "These contracts govern agent behavior across product artifacts."
      },
      {
        "id": "EXEC-CONTRACT-PLACE-02",
        "target": "<data-domain>/CONTRACT.md",
        "criterion": "Place data-near L1 contracts beside the data they validate, such as runs/CONTRACT.md or kb/golden-examples/CONTRACT.md.",
        "rationale": "Data-near contracts reduce lookup distance and clarify ownership."
      },
      {
        "id": "EXEC-CONTRACT-PLACE-03",
        "target": "prompts/",
        "criterion": "Place L1 prompt assets in prompts/ and archive inactive executable prompts in prompts/archive/.",
        "rationale": "Prompts are user-facing execution tools and belong in the prompt catalog."
      },
      {
        "id": "EXEC-CONTRACT-PLACE-04",
        "target": "standards/<scope>-standard.md",
        "criterion": "Place L3 standards in standards/ and do not make them required runtime inputs for L1.",
        "rationale": "Standards manage construction and review, not task execution."
      },
      {
        "id": "EXEC-CONTRACT-PLACE-05",
        "target": "governance/rfc/ or docs/adr/",
        "criterion": "Place proposals and architectural decisions in RFC/ADR locations, then copy accepted runtime rules into L1.",
        "rationale": "Proposal status must not silently become runtime behavior."
      },
      {
        "id": "EXEC-CONTRACT-PLACE-06",
        "target": "governance/contracts-registry.md",
        "criterion": "Place contract source/provenance, approved L3 decisions, and historical links in the L2 contracts registry.",
        "rationale": "L1 contracts must carry only contract_registry_id, not direct L3 provenance links."
      }
    ],
    "input_invariant": {
      "rule": "L1 runtime inputs MUST NOT require L3 artifacts",
      "allowed": [
        "L1 contract references another L1 contract as an explicit companion",
        "L1 contract references L2 registry or taxonomy data",
        "L1 contract embeds accepted L3 rule text as a local rule and points to registry provenance only through contract_registry_id"
      ],
      "forbidden": [
        "L1 contract requires reading standards/* at runtime",
        "L1 contract requires reading governance/rfc/* at runtime",
        "L1 contract contains direct hyperlinks to L3 artifacts",
        "L1 contract contains contract source/provenance fields other than contract_registry_id",
        "Prompt instructions depend on unstated RFC or ADR interpretation"
      ],
      "validation": "Run an L1-only input test: parse the YAML contract, collect runtime_inputs, and fail if any row is classified as L3 or if the contract contains contract source/provenance fields other than contract_registry_id.",
      "rationale": "Runtime behavior must be reproducible from executable instructions and data, not from live interpretation of governance documents."
    },
    "validation_examples": [
      {
        "artifact": "governance/bcreq-fr-generation-contract.md",
        "expected_layer": "L1",
        "expected_rule_class": "combat",
        "template_result": "The active contract keeps local scope rules and L2 taxonomy registries, uses 100% YAML, and replaces embedded contract source/provenance with contract_registry_id.",
        "rationale": "This is the canonical generation contract example; accepted RFC rules become local L1 rules while provenance moves to governance/contracts-registry.md."
      },
      {
        "artifact": "runs/CONTRACT.md",
        "expected_layer": "L1",
        "expected_rule_class": "combat",
        "template_result": "Target migration converts the contract to 100% YAML with explicit layer, rule_class, contract_registry_id, runtime_inputs, outputs, and RUN-REC-META-01 in rules.",
        "rationale": "The file is data-near and executable because it controls how run records are created and validated."
      },
      {
        "artifact": "standards/prompt-standard.md",
        "expected_layer": "L3",
        "expected_rule_class": "management",
        "template_result": "The L1 template does not apply directly: the artifact remains Markdown with YAML frontmatter because it is L3. PROMPT-STD-FM-01 stays a management rule for prompt authors.",
        "rationale": "The prompt standard governs prompt construction; active prompts must carry the runtime instructions themselves."
      }
    ],
    "expert_review": [
      {
        "role": "Архитектор контрактов",
        "focus": "Layer boundaries, placement, input invariant, and rule ID stability.",
        "pass_criteria": "No L1 contract depends on L3 as runtime input."
      },
      {
        "role": "BA-эксперт",
        "focus": "Business-analysis usability, prompt/contract distinction, and examples from existing BA artifacts.",
        "pass_criteria": "The template is understandable for authors of prompts, BCREQ contracts, and run evidence."
      },
      {
        "role": "AI-инженер",
        "focus": "Machine readability, validation hooks, deterministic parsing, and L1-only input test automation.",
        "pass_criteria": "A script can validate key fields, examples, and project wiring without LLM interpretation."
      }
    ]
  }
}
```

## 4. Применение шаблона к существующим контрактам

1. `governance/bcreq-fr-generation-contract.md` является L1/combat-контрактом
   с локальными правилами `BCREQ-FR-GEN-SCOPE-01/02`, L2 runtime-входами
   таксономий и 100% YAML-структурой. Для contract source/provenance он
   оставляет только `contract_registry_id`.
2. `runs/CONTRACT.md` является L1/combat-контрактом рядом с данными. При
   следующем изменении его стоит перевести в YAML-структуру с `layer: L1`,
   `rule_class: combat`, `contract_registry_id`, `runtime_inputs`, `outputs` и
   правилом `RUN-REC-META-01`.
3. `standards/prompt-standard.md` является L3/management-стандартом. Для него
   правило `PROMPT-STD-FM-01` описывает frontmatter и структуру prompt assets,
   но активный prompt не должен требовать чтения этого стандарта во время
   выполнения.

Эти проверки не изменяют существующие контракты: Issue #212 требует создать
стандарт и шаблон, а не мигрировать все артефакты сразу.

## 5. Экспертная проверка

Последовательная экспертная проверка:

1. Архитектор контрактов проверяет, что L1/L2/L3 отделены, `loading_layer:
   executable` не подменяет бизнес-слой, а L1 runtime-входы не требуют L3 и не
   содержат прямых L3-гиперссылок.
2. BA-эксперт проверяет, что шаблон понятен авторам BA-промптов, BCREQ-FR
   контрактов и run evidence, а примеры отражают реальные рабочие сценарии.
3. AI-инженер проверяет машинную читаемость 100% YAML L1-контракта,
   стабильность rule ID, наличие `contract_registry_id`, возможность L1-only
   input test и подключение валидатора к CI.

## 6. DoD стандарта

- Создан L3-стандарт `standards/executable-contract-standard.md`, а не новый
  L1-контракт.
- Определены критерии L1/L2/L3 и combat/management/data с rationale.
- Зафиксировано разделение форматов: L1 = 100% YAML, L2 = JSON/YAML для
  структур и Markdown для текстовых знаний, L3 = Markdown with YAML frontmatter.
- Зафиксирован YAML-шаблон L1-контракта с `contract_registry_id`, `rationale` и
  комментариями; Markdown-проза запрещена.
- Зафиксировано правило provenance: source/provenance контрактов хранится в
  `governance/contracts-registry.md`, а не в L1-контракте.
- Определены правила размещения для `governance/`, `prompts/`, `runs/`, `kb/`,
  `standards/`, RFC и ADR.
- Зафиксирован жёсткий инвариант: L1 runtime inputs MUST NOT require L3
  artifacts; прямые гиперссылки на L3-артефакты в L1 запрещены.
- Выполнена самостоятельная классификация артефактов из `standards/`,
  `governance/`, `prompts/`, `runs/` и data-near контрактов `kb/`.
- Шаблон проверен на трёх существующих артефактах:
  `governance/bcreq-fr-generation-contract.md`, `runs/CONTRACT.md` и
  `standards/prompt-standard.md`.
- Существующие контракты и промпты не изменяются в рамках этого стандарта.
