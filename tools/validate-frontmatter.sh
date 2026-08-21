#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

errors=0

required_fields=(
  "status"
  "version"
  "updated"
  "temperature"
)

error() {
  local path="$1"
  local line="$2"
  local message="$3"

  printf '%s:%s: ERROR: %s\n' "$path" "$line" "$message" >&2
  errors=$((errors + 1))
}

trim_value() {
  local value="$1"

  value="${value%%#*}"
  value="${value//$'\r'/}"
  value="${value##+([[:space:]])}"
  value="${value%%+([[:space:]])}"

  if [[ "$value" =~ ^\"(.*)\"$ ]]; then
    value="${BASH_REMATCH[1]}"
  elif [[ "$value" =~ ^\'(.*)\'$ ]]; then
    value="${BASH_REMATCH[1]}"
  fi

  printf '%s' "$value"
}

is_source_template() {
  local path="$1"

  case "$path" in
    templates/htom/*.md | ./templates/htom/*.md | \
    templates/htom/.github/ISSUE_TEMPLATE/*.md | ./templates/htom/.github/ISSUE_TEMPLATE/*.md | \
    templates/spoke/*.md | ./templates/spoke/*.md | \
    templates/spoke/.github/ISSUE_TEMPLATE/*.md | ./templates/spoke/.github/ISSUE_TEMPLATE/*.md | \
    templates/product-concept-template.md | ./templates/product-concept-template.md | \
    templates/solution-concept-template.md | ./templates/solution-concept-template.md | \
    templates/webportal-product-concept-template.md | ./templates/webportal-product-concept-template.md | \
    templates/webportal-solution-concept-template.md | ./templates/webportal-solution-concept-template.md)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

normalize_path() {
  local path="$1"

  path="${path#"$ROOT_DIR"/}"
  path="${path#./}"

  printf '%s' "$path"
}

document_class() {
  local path
  path="$(normalize_path "$1")"

  case "$path" in
    docs/audit/*.md)
      printf 'audit'
      ;;
    research/*.md | docs/analysis/*.md | docs/report/*.md)
      printf 'knowledge'
      ;;
    docs/rfc/README.md)
      printf 'governance'
      ;;
    docs/rfc/*.md)
      printf 'rfc'
      ;;
    docs/adr/README.md)
      printf 'governance'
      ;;
    docs/adr/*.md)
      printf 'adr'
      ;;
    standards/*.md)
      printf 'standard'
      ;;
    .github/ISSUE_TEMPLATE/*.md | templates/*/.github/ISSUE_TEMPLATE/*.md)
      printf 'issue-template'
      ;;
    templates/*.md | templates/*/*.md | templates/*/*/*.md)
      printf 'template'
      ;;
    guides/*.md | docs/guides/*.md)
      printf 'guide'
      ;;
    practices/*.md | practices/*/*.md)
      printf 'practice'
      ;;
    *)
      printf 'default'
      ;;
  esac
}

is_governance_class() {
  case "$1" in
    governance | rfc | adr | standard)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_knowledge_class() {
  case "$1" in
    knowledge | audit)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_approved_field() {
  local class="$1"
  local key="$2"

  case "$class:$key" in
    *:status | *:version | *:updated | *:temperature)
      return 0
      ;;
    *:ai-generated)
      return 1
      ;;
    knowledge:owner | knowledge:type | knowledge:context | knowledge:method | knowledge:scope | \
    knowledge:source | knowledge:source_id | knowledge:stage | knowledge:projects | \
    knowledge:related_artifacts | knowledge:related_issues | knowledge:related_issue | \
    knowledge:external_artifacts | knowledge:based_on | knowledge:report-subtype | \
    knowledge:analysis-subtype | knowledge:supersedes)
      return 0
      ;;
    audit:owner | audit:type | audit:context | audit:method | audit:scope | \
    audit:source | audit:source_id | audit:stage | audit:projects | \
    audit:related_artifacts | audit:related_issues | audit:related_issue | \
    audit:external_artifacts | audit:based_on | audit:audit_target | \
    audit:evidence_model | audit:verdict | audit:severity_scale | \
    audit:follow_up | audit:related_norm)
      return 0
      ;;
    governance:owner | governance:executable | governance:entrypoint)
      return 0
      ;;
    rfc:owner | rfc:rfc-scope | rfc:executable | rfc:entrypoint | \
    rfc:type | rfc:context | rfc:method | rfc:scope | rfc:source | \
    rfc:related_artifacts | rfc:related_issues)
      return 0
      ;;
    adr:owner | adr:decision-type | adr:executable | adr:entrypoint | \
    adr:supersedes)
      return 0
      ;;
    standard:owner | standard:executable | standard:entrypoint | standard:scope | \
    standard:level | standard:concept_type | standard:related_standards | \
    standard:related_templates | standard:related_issues)
      return 0
      ;;
    issue-template:name | issue-template:about | issue-template:title | \
    issue-template:labels | issue-template:assignees)
      return 0
      ;;
    template:executable | template:entrypoint | template:level | template:standard)
      return 0
      ;;
    guide:audience | guide:entrypoint | guide:executable)
      return 0
      ;;
    practice:source | practice:executable | practice:entrypoint)
      return 0
      ;;
    default:executable | default:entrypoint | default:source | default:based_on | \
    default:author | default:session | default:self-report | default:scope | \
    default:type | default:context | default:method | default:related_artifacts | \
    default:related_issues)
      return 0
      ;;
    # --- Локальная дельта спицы (issue #267) ---------------------------------
    # Хабовый валидатор не знает о полях, которые появляются только в спице.
    # Каждое поле ниже реально потребляется локальной механикой, поэтому
    # разрешено по правилу frontmatter-docs-standard.md («Extra fields are
    # allowed only when a validator, index, template, executable contract,
    # provenance rule or document class consumes them»):
    #   owner                                     — governance-ответственный;
    #   research_deps                             — docs/hub-research-dependencies.md;
    #   source_hub/source_sha/source_of_truth/sync_policy
    #                                             — scripts/sync_from_hub.py (SYNC_FIELDS);
    #   layer/full_version/related_standard/related_issue
    #                                             — standards/cascading-context-loading-standard.md.
    # Дельта только расширяет список допустимых полей; ни одно правило
    # канонического валидатора не ослаблено (см. tools/README.md).
    default:owner | default:research_deps | default:source_hub | default:source_sha | \
    default:source_of_truth | default:sync_policy | default:layer | \
    default:full_version | default:related_standard | default:related_issue)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

validate_status() {
  local path="$1"
  local class="$2"
  local line="$3"
  local value="$4"

  if is_knowledge_class "$class"; then
    case "$value" in
      draft | reviewed | canonical | superseded)
        ;;
      *)
        error "$path" "$line" "invalid knowledge status '$value' (expected one of: draft, reviewed, canonical, superseded)"
        ;;
    esac
    return
  fi

  if is_governance_class "$class"; then
    case "$value" in
      draft | proposed | accepted | rejected | deprecated | superseded)
        ;;
      *)
        error "$path" "$line" "invalid governance status '$value' (expected one of: draft, proposed, accepted, rejected, deprecated, superseded)"
        ;;
    esac
    return
  fi

  case "$value" in
    draft | reviewed | published | superseded | canonical | experimental | \
    proposed | accepted | rejected | deprecated)
      ;;
    *)
      error "$path" "$line" "invalid status '$value' (expected a controlled lifecycle status)"
      ;;
  esac
}

validate_field() {
  local path="$1"
  local class="$2"
  local field="$3"
  local line="$4"
  local value="$5"

  case "$field" in
    status)
      validate_status "$path" "$class" "$line" "$value"
      ;;
    version)
      if [[ ! "$value" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
        error "$path" "$line" "invalid version '$value' (expected SemVer X.Y or X.Y.Z)"
      fi
      ;;
    updated)
      if [[ ! "$value" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        if is_source_template "$path" && [[ "$value" == "{{date}}" ]]; then
          return
        fi
        error "$path" "$line" "invalid updated '$value' (expected ISO8601 date YYYY-MM-DD)"
      fi
      ;;
    temperature)
      if [[ ! "$value" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        error "$path" "$line" "invalid temperature '$value' (expected number from 0 to 2)"
      elif ! awk -v value="$value" 'BEGIN { exit !(value >= 0 && value <= 2) }'; then
        error "$path" "$line" "invalid temperature '$value' (expected number from 0 to 2)"
      fi
      ;;
    executable)
      case "$value" in
        true | false)
          ;;
        *)
          error "$path" "$line" "invalid executable '$value' (expected true or false)"
          ;;
      esac
      ;;
    entrypoint)
      case "$value" in
        true)
          ;;
        *)
          error "$path" "$line" "invalid entrypoint '$value' (expected true)"
          ;;
      esac
      ;;
    owner)
      if [[ -z "$value" ]]; then
        error "$path" "$line" "invalid owner '$value' (expected non-empty owner)"
      fi
      ;;
    audit_target | evidence_model | verdict)
      if [[ -z "$value" ]]; then
        error "$path" "$line" "invalid $field '$value' (expected non-empty audit metadata)"
      fi
      ;;
    decision-type)
      case "$value" in
        governance | methodology | product | curriculum | runtime)
          ;;
        *)
          error "$path" "$line" "invalid decision-type '$value' (expected one of: governance, methodology, product, curriculum, runtime)"
          ;;
      esac
      ;;
    rfc-scope)
      case "$value" in
        A | B | C | D | multi)
          ;;
        *)
          error "$path" "$line" "invalid rfc-scope '$value' (expected one of: A, B, C, D, multi)"
          ;;
      esac
      ;;
  esac
}

validate_audit_body_sections() {
  local path="$1"

  local labels=(
    "Summary / BLUF"
    "Scope / Target"
    "Method / Evidence"
    "Findings / Verdict"
    "Remediation / Deviation"
    "Related Artifacts"
  )
  local patterns=(
    "Summary|BLUF"
    "Scope|Target"
    "Method|Evidence"
    "Findings|Verdict"
    "Remediation|Deviation"
    "Related Artifacts"
  )

  local i
  for i in "${!labels[@]}"; do
    if ! grep -Eiq "^##[[:space:]].*(${patterns[$i]})" "$path"; then
      error "$path" 1 "missing required Audit body section: ${labels[$i]}"
    fi
  done
}

validate_file() {
  local path="$1"
  local line=""
  local line_no=0
  local closed=0
  local class
  declare -A values=()
  declare -A lines=()
  local fields=()

  class="$(document_class "$path")"

  if [[ ! "$path" == *.md ]]; then
    error "$path" 1 "not a markdown file"
    return
  fi

  if [[ ! -f "$path" ]]; then
    error "$path" 1 "file does not exist"
    return
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    line_no=$((line_no + 1))

    if [[ "$line_no" -eq 1 ]]; then
      if [[ "$line" != "---" ]]; then
        error "$path" 1 "missing frontmatter block"
        return
      fi
      continue
    fi

    if [[ "$line" == "---" ]]; then
      closed=1
      break
    fi

    if [[ "$line" =~ ^[[:space:]]*([A-Za-z0-9_-]+)[[:space:]]*:(.*)$ ]]; then
      local key="${BASH_REMATCH[1]}"
      local raw_value="${BASH_REMATCH[2]}"

      if [[ -n "${lines[$key]+set}" ]]; then
        error "$path" "$line_no" "duplicate frontmatter field: $key"
      else
        fields+=("$key")
        lines["$key"]="$line_no"
        values["$key"]="$(trim_value "$raw_value")"
      fi
    fi
  done < "$path"

  if [[ "$line_no" -eq 0 ]]; then
    error "$path" 1 "missing frontmatter block"
    return
  fi

  if [[ "$closed" -eq 0 ]]; then
    error "$path" 1 "frontmatter block is not closed"
    return
  fi

  local field
  for field in "${fields[@]}"; do
    if [[ "$field" == "ai-generated" ]]; then
      error "$path" "${lines[$field]}" "frontmatter field is forbidden: ai-generated"
      continue
    fi

    if ! is_approved_field "$class" "$field"; then
      error "$path" "${lines[$field]}" "frontmatter field is not approved for this document class: $field"
      continue
    fi

    validate_field "$path" "$class" "$field" "${lines[$field]}" "${values[$field]}"
  done

  for field in "${required_fields[@]}"; do
    if [[ -z "${lines[$field]+set}" ]]; then
      error "$path" 1 "missing required frontmatter field: $field"
    fi
  done

  if is_governance_class "$class" && [[ -z "${lines[owner]+set}" ]]; then
    error "$path" 1 "missing required frontmatter field for governance artifact: owner"
  fi

  if [[ "$class" == "adr" && -z "${lines[decision-type]+set}" ]]; then
    error "$path" 1 "missing required frontmatter field for ADR artifact: decision-type"
  fi

  if [[ "$class" == "rfc" && -z "${lines[rfc-scope]+set}" ]]; then
    error "$path" 1 "missing required frontmatter field for RFC artifact: rfc-scope"
  fi

  if [[ "$class" == "audit" ]]; then
    for field in audit_target evidence_model verdict; do
      if [[ -z "${lines[$field]+set}" ]]; then
        error "$path" 1 "missing required frontmatter field for Audit artifact: $field"
      fi
    done

    validate_audit_body_sections "$path"
  fi
}

collect_files() {
  local target="$1"

  if [[ -d "$target" ]]; then
    find "$target" -type f -name '*.md' | sort
  else
    printf '%s\n' "$target"
  fi
}

main() {
  local targets=("$@")

  if [[ "${#targets[@]}" -eq 0 ]]; then
    targets=(".")
  fi

  local target
  while IFS= read -r target; do
    validate_file "$target"
  done < <(
    for target in "${targets[@]}"; do
      if [[ -d "$target" ]]; then
        collect_files "$target"
      elif [[ -e "$target" ]]; then
        collect_files "$target"
      else
        printf '%s\n' "$target"
      fi
    done
  )

  if [[ "$errors" -gt 0 ]]; then
    printf 'Frontmatter validation failed with %d error(s).\n' "$errors" >&2
    exit 1
  fi

  printf 'Frontmatter validation passed.\n'
}

main "$@"
