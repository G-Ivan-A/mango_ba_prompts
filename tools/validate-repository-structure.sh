#!/usr/bin/env bash
#
# Валидатор базовой структуры HTOM-команды (issue #291).
#
# Адаптация «иммунной системы» генома Хаба
# (templates/htom/tools/validate-repository-structure.sh) под спицу
# mango_ba_prompts: те же обязательные артефакты корня плюс замок на корень —
# любой markdown-файл в корне вне канонического списка считается ошибкой.
#
# Именно отсутствие этой проверки позволило структурному дрейфу дожить до
# issue #291: геном Хаба требовал файлы в корне, но не запрещал добавлять туда
# новые. Разбор — docs/audit/2026-08-21-root-structure-audit.md.
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
# Источник истины: templates/htom/ Хаба. AI_GOVERNANCE.md, AI_QUICK_RULES.md и
# AI_SESSION_HANDOVER_PROMPT.md обязаны лежать именно в корне — это жёсткое
# ограничение Хаба, а не «точки входа», придуманные локально.
required_directories=(
  "ai-governance"
  "ai-rules"
  "docs/adr"
  "docs/audit"
  ".github/ISSUE_TEMPLATE"
  "tools"
)

required_files=(
  "AI_GOVERNANCE.md"
  "AI_QUICK_RULES.md"
  "AI_SESSION_HANDOVER_PROMPT.md"
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  ".hub-profile.json"
  "tools/validate-repository-structure.sh"
)

for dir in "${required_directories[@]}"; do
  [[ -d "$dir" ]] || fail "missing directory: $dir"
done

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || fail "missing file: $file"
done

# --- 2. Замок на корень -----------------------------------------------------
# Корень закрыт: разрешён только канонический список. Новый корневой документ
# требует либо переноса в каталог-дом, либо ADR и явного расширения списка.
allowed_root_markdown=(
  "AI_GOVERNANCE.md"
  "AI_QUICK_RULES.md"
  "AI_SESSION_HANDOVER_PROMPT.md"
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
)

is_allowed_root_markdown() {
  local candidate="$1"
  local allowed
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

# --- 3. Архив не соседствует с активными артефактами ------------------------
# Superseded-копии живут в скрытом .archive/ (issue #291, контракт 5).
while IFS= read -r file; do
  fail "superseded artifact outside .archive/: ${file#./} (перенеси в .archive/, см. .archive/README.md)"
done < <(
  find . -type f -name '*_old*.md' \
    -not -path './.archive/*' \
    -not -path './.git/*' \
    -not -path './runs/*' \
    -not -path './kb/*' | sort
)

# --- 4. Неприкосновенные каталоги -------------------------------------------
# runs/ и kb/ — артефакты прогонов и база знаний; их целостность защищена
# контрактом 2 issue #291. Валидатор фиксирует само наличие домов.
for protected in "runs" "kb"; do
  [[ -d "$protected" ]] || fail "protected directory is missing: $protected/"
done

# --- 5. Мягкие проверки -----------------------------------------------------
# research/ по умолчанию не создаётся в HTOM-команде: фундаментальные знания
# живут в research/ Хаба (правило генома).
if [[ -d "research" ]]; then
  warn "research/ найдена в HTOM-команде: зафиксируйте отклонение как ADR в docs/adr/ или вынесите знания в research/ Хаба."
fi

# Проверка на незаменённые плейсхолдеры генома ({{REPO_NAME}}) в спице не
# применяется: `{{...}}` — рабочий синтаксис слотов промптов и паттернов
# (prompts/, patterns/), поэтому такая проверка даёт постоянный ложный сигнал.

if (( warnings > 0 )); then
  printf '\n%d warning(s) — не блокируют, но требуют внимания.\n' "$warnings" >&2
fi

if (( failures > 0 )); then
  printf '\nRepository structure validation failed with %d error(s).\n' "$failures" >&2
  exit 1
fi

printf 'Repository structure validation passed.\n'
