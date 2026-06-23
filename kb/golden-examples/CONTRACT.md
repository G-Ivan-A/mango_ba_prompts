# Golden Examples lifecycle contract.
contract_id: golden-examples-lifecycle-contract
status: draft
version: 0.1
updated: 2026-06-23
ai-generated: true
type: contract
scope: golden-examples
issue: "https://github.com/G-Ivan-A/mango_ba_prompts/issues/211"

rationale: >
  Golden Examples must be reproducible repository artifacts, not GitHub
  user-attachments or bare filenames. The contract keeps runtime inputs at L1/L2:
  an executable generation contract may read an approved example only through
  repository path + sha, while L3 approval rules stay referenced as the explicit
  governance process for promoting draft examples.

storage:
  base_path: "kb/golden-examples/"
  artifact_type_directories:
    - artifact_type: bcreq-fr
      path: "kb/golden-examples/bcreq-fr/"
    - artifact_type: rfc
      path: "kb/golden-examples/rfc/"
    - artifact_type: adr
      path: "kb/golden-examples/adr/"

file_format:
  extension: ".md"
  content_format: "Markdown"
  rationale: >
    Golden examples are reviewed by humans and reused by agents as readable
    style/structure references; Markdown preserves reviewability while
    frontmatter preserves machine-readable metadata.

required_frontmatter:
  # Template required at the top of every future Golden Example file.
  type: golden-example
  artifact_type: bcreq-fr # | rfc | adr
  status: draft # | approved
  created: YYYY-MM-DD
  related_contract: "governance/bcreq-fr-generation-contract.md"

naming:
  pattern: "example-NNN-<short-description>.md"
  rules:
    - "NNN is a zero-padded sequence unique inside the artifact-type directory."
    - "short-description uses lowercase ASCII slug words separated by hyphens."
    - "The filename must not encode approval status; status lives in frontmatter."

linking:
  existing_golden_standard:
    # Use path + sha only after the artifact is explicitly approved.
    required_fields:
      - path
      - sha
    path_rule: "Repository-relative path under kb/golden-examples/<artifact_type>/."
    sha_rule: "Full commit SHA containing the approved artifact content."
    example:
      path: "kb/golden-examples/bcreq-fr/example-001-short-fr-style.md"
      sha: "<40-character-commit-sha>"
  missing_golden_standard:
    # ПОЯСНЕНИЕ: Заглушка заменяется на path+sha только после явного согласования
    # пользователем эталонного артефакта.
    source_attachments:
      - status: "no-golden-standard"

approval_process:
  status_values:
    - draft
    - approved
  draft_to_approved:
    requires_explicit_user_confirmation: true
    approval_contract: "governance/approval-contract.md"
    automatic_transition_allowed: false
    rationale: >
      An AI agent may prepare a candidate example, but approval changes the
      reusable evidence base for later generation. That decision belongs to the
      user through the approval contract.
  replacement_policy:
    placeholder_to_path_sha: "allowed only after draft_to_approved passes"
    approved_artifact_changes: "require a new pull request and explicit approval"
    automatic_replacement_allowed: false

bcreq_fr_contract_change_control:
  # 2-факторное подтверждение protects the executable BCREQ-FR contract from
  # silently adopting a new style/source reference.
  requires_2_factor_confirmation: true
  factors:
    - "User explicitly approves the Golden Example artifact status change to approved."
    - "User separately approves replacing no-golden-standard in governance/bcreq-fr-generation-contract.md with path + sha."
  automatic_update_allowed: false

validation:
  validator: "scripts/validate_issue_211_golden_examples_contract.py"
  checks:
    - "Storage directories and README exist."
    - "No real Golden Example artifact is created by issue #211."
    - "BCREQ-FR source_attachments uses status: no-golden-standard until approval."
    - "Contract changes are documented in CHANGELOG.md and project navigation."
