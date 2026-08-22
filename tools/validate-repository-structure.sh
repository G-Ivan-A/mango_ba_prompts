#!/usr/bin/env bash
#
# Валидатор базовой структуры HTOM-команды (issue #291).
#
# Адаптация «иммунной системы» генома Хаба
# (templates/htom/tools/validate-repository-structure.sh, редакция RFC #532 /
# PR #538) под спицу mango_ba_prompts.
#
# Что взято из генома в редакции RFC #532:
#   * управляющий контракт нормируется по НАЛИЧИЮ, а не по размещению:
#     допустимые дома — корень (обратная совместимость), governance/ (переходный)
#     и канонические ai-governance/ + ai-rules/;
#   * контракт в двух домах сразу = ошибка (два SSOT);
#   * классификация каталогов верхнего уровня: канонический | задекларированный
#     в .hub-profile.json специфичный | архивный .archive/ | иначе ошибка;
#   * .archive/ обязан объяснять себя через README.md.
#
# Локальные дельты спицы (осознанные, с обоснованием):
#   D1. Замок на корень: markdown в корне разрешён только из канонического
#       списка. Именно отсутствие этой проверки дало дрейф issue #291 — геном
#       требовал файлы в корне, но не запрещал добавлять туда новые.
#   D2. Запрет `*_old*.md` вне .archive/ (issue #291, контракт 5).
#   D3. Обязательные дома runs/ и kb/ — контракт 2 issue #291.
#   D4. Проверка плейсхолдера {{REPO_NAME}} в handover prompt не применяется:
#       handover спицы локально обогащён (docs/adr/0002-issue48-handover-local-enrichment.md)
#       и содержит реальное имя репозитория, а `{{...}}` — рабочий синтаксис
#       слотов промптов и паттернов (prompts/, patterns/).
#   D5. Классификация каталогов пропускает git-ignored каталоги (.validate-cache/):
#       геном обходит рабочее дерево и спотыкается о кэш локального раннера.
#   D6. Файловый минимум генома (.github/ISSUE_TEMPLATE/task*.md) не требуется:
#       у спицы свой набор шаблонов issue. Расхождение отмечено в pr-ops/BACKLOG.md.
#
# Разбор причин дрейфа — docs/audit/2026-08-21-root-structure-audit.md.
#
#   ./tools/validate-repository-structure.sh
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0
warnings=0

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  failures=$((failures + 1))
}

warn() {
  printf 'WARN: %s\n' "$1" >&2
  warnings=$((warnings + 1))
}

# --- 1. Обязательный минимум генома HTOM ------------------------------------
required_directories=(
  "ai-governance"
  "ai-rules"
  "docs/adr"
  "docs/audit"
  ".github/ISSUE_TEMPLATE"
  ".github/workflows"
  "tools"
)

required_files=(
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  ".hub-profile.json"
  ".github/workflows/validate.yml"
  "tools/validate-repository-structure.sh"
)

for dir in "${required_directories[@]}"; do
  [[ -d "$dir" ]] || fail "missing directory: $dir"
done

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || fail "missing file: $file"
done

# --- 2. Управляющие контракты: наличие + ровно один дом ----------------------
# Порядок кандидатов задаёт приоритет разрешения; первый — канонический дом
# в редакции RFC #532, последний — легаси-корень (обратная совместимость).
contracts=(
  "governance contract:ai-governance/ai-governance.md:governance/AI_GOVERNANCE.md:AI_GOVERNANCE.md"
  "quick rules:ai-rules/ai-quick-rules.md:governance/AI_QUICK_RULES.md:AI_QUICK_RULES.md"
  "handover prompt:ai-rules/AI_SESSION_HANDOVER_PROMPT.md:governance/AI_SESSION_HANDOVER_PROMPT.md:AI_SESSION_HANDOVER_PROMPT.md"
)

for entry in "${contracts[@]}"; do
  IFS=':' read -r -a parts <<<"$entry"
  label="${parts[0]}"
  candidates=("${parts[@]:1}")

  found=()
  for candidate in "${candidates[@]}"; do
    [[ -f "$candidate" ]] && found+=("$candidate")
  done

  if [[ "${#found[@]}" -eq 0 ]]; then
    fail "missing $label: ожидался один из ${candidates[*]}"
  elif [[ "${#found[@]}" -gt 1 ]]; then
    fail "duplicate $label: ${found[*]} — два дома означают два SSOT, оставьте ровно одно размещение"
  elif [[ "${found[0]}" != "${candidates[0]}" ]]; then
    warn "$label лежит в ${found[0]}, а канонический дом — ${candidates[0]} (RFC #532: governance/ и корень — переходные)."
  fi
done

# --- 3. Замок на корень (дельта D1) -----------------------------------------
allowed_root_markdown=(
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
)

is_allowed_root_markdown() {
  local candidate="$1" allowed
  for allowed in "${allowed_root_markdown[@]}"; do
    [[ "$candidate" == "$allowed" ]] && return 0
  done
  return 1
}

while IFS= read -r file; do
  name="${file#./}"
  if ! is_allowed_root_markdown "$name"; then
    fail "root markdown file is not in the canonical HTOM root set: $name (перенеси в каталог-дом: ai-governance/, ai-rules/, prompts/, standards/, docs/ — или заведи ADR и расширь список)"
  fi
done < <(find . -maxdepth 1 -type f -name '*.md' | sort)

# --- 4. Классификация каталогов верхнего уровня (RFC #532) -------------------
PROFILE_FILE=".hub-profile.json"

canonical_directories=(
  ".git"
  ".github"
  "docs"
  "tools"
  "governance"
  "ai-governance"
  "ai-rules"
)

read_profile() {
  python3 - "$PROFILE_FILE" <<'PYEOF'
import json, sys

try:
    with open(sys.argv[1], encoding="utf-8") as fh:
        profile = json.load(fh)
except Exception as exc:  # noqa: BLE001 — сообщение уходит в валидатор как FAIL
    print("error\t%s" % exc)
    sys.exit(0)

until = profile.get("structure_grandfather_until")
if until:
    print("grandfather\t%s" % until)

for entry in profile.get("project_specific_directories", []) or []:
    if isinstance(entry, str):
        # Строка без причины — декларация без обоснования: не принимается.
        print("invalid\t%s" % entry)
        continue
    path = (entry.get("path") or "").strip().strip("/")
    reason = (entry.get("reason") or "").strip()
    if not path or not reason:
        print("invalid\t%s" % (path or "<empty>"))
        continue
    print("declared\t%s" % path)
PYEOF
}

declared_directories=()
grandfather_until=""

if [[ -f "$PROFILE_FILE" ]]; then
  while IFS=$'\t' read -r kind value; do
    [[ -n "$kind" ]] || continue
    case "$kind" in
      declared) declared_directories+=("$value") ;;
      grandfather) grandfather_until="$value" ;;
      invalid) fail "$PROFILE_FILE: декларация каталога '$value' неполна — нужны непустые поля path и reason" ;;
      error) fail "$PROFILE_FILE не разбирается как JSON: $value" ;;
    esac
  done < <(read_profile)
else
  fail "missing file: $PROFILE_FILE"
fi

in_list() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    [[ "$item" == "$needle" ]] && return 0
  done
  return 1
}

# Льготный период: существующий недекларированный каталог даёт WARN до даты и
# ERROR после неё — один цикл синхронизации на приведение в порядок.
grandfather_active=0
if [[ -n "$grandfather_until" ]] && [[ "$(date -u +%F)" < "$grandfather_until" || "$(date -u +%F)" == "$grandfather_until" ]]; then
  grandfather_active=1
fi

while IFS= read -r dir; do
  name="${dir#./}"
  [[ -n "$name" && "$name" != "." ]] || continue
  in_list "$name" "${canonical_directories[@]}" && continue
  [[ "$name" == ".archive" ]] && continue
  # Дельта D5: git-ignored каталоги — рабочий мусор, а не структура репозитория.
  if git check-ignore -q "$name" 2>/dev/null; then
    continue
  fi
  if in_list "$name" ${declared_directories[@]+"${declared_directories[@]}"}; then
    continue
  fi
  message="недекларированный каталог: $name/ — он не входит в каноническую структуру генома. Либо задекларируйте его как специфичный для проекта в $PROFILE_FILE (project_specific_directories: path + reason), либо перенесите содержимое в канонический дом, либо перенесите каталог в .archive/ с README.md."
  if [[ "$grandfather_active" -eq 1 ]]; then
    warn "$message (льготный период до $grandfather_until)"
  else
    fail "$message"
  fi
done < <(find . -maxdepth 1 -type d ! -name '.')

# Декларация, потерявшая свой каталог, — мёртвая запись конфигурации.
for declared in ${declared_directories[@]+"${declared_directories[@]}"}; do
  [[ -d "$declared" ]] || warn "$PROFILE_FILE декларирует каталог '$declared', которого нет в репозитории — удалите запись."
done

# --- 5. Архив: вынесен, объяснён и не соседствует с активными артефактами ----
if [[ -d ".archive" ]] && [[ ! -f ".archive/README.md" ]]; then
  fail ".archive/ существует без README.md: архив обязан объяснять, что и почему в нём лежит."
fi

while IFS= read -r file; do
  fail "superseded artifact outside .archive/: ${file#./} (перенеси в .archive/, см. .archive/README.md)"
done < <(
  find . -type f -name '*_old*.md' \
    -not -path './.archive/*' \
    -not -path './.git/*' \
    -not -path './runs/*' \
    -not -path './kb/*' | sort
)

# --- 6. Неприкосновенные каталоги (контракт 2 issue #291) -------------------
for protected in "runs" "kb"; do
  [[ -d "$protected" ]] || fail "protected directory is missing: $protected/"
done

# --- 7. Мягкие проверки -----------------------------------------------------
if [[ -d "research" ]]; then
  warn "research/ найдена в HTOM-команде: зафиксируйте отклонение как ADR в docs/adr/ или вынесите знания в research/ Хаба."
fi

if (( warnings > 0 )); then
  printf '\n%d warning(s) — не блокируют, но требуют внимания.\n' "$warnings" >&2
fi

if (( failures > 0 )); then
  printf '\nRepository structure validation failed with %d error(s).\n' "$failures" >&2
  exit 1
fi

printf 'Repository structure validation passed.\n'
