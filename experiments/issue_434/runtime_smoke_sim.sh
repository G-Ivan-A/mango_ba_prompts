#!/bin/sh
# Симуляция механизма РТ-1/РТ-3 (issue #434) на копии runtime.
#
# Берёт клон mango-ba-ai-runtime на закреплённом SHA (RUNTIME_CLONE), копирует
# его во временный каталог, дописывает в tests/runtime-smoke.sh проверки,
# предложенные в RFC docs/rfc/2026-11-runtime-product-catalog-golden-set.md
# (раздел «Механизм»), и прогоняет четыре сценария:
#   1. missing   — каталога нет: проверка обязана упасть;
#   2. catalog   — каталог из прототипа положен: проверка проходит;
#   3. invented  — в golden/cases.yaml atomic_function выдуманный (как сейчас в
#                  markdown эталона GS-CC-01): проверка обязана упасть;
#   4. catalogid — atomic_function — id каталога: проверка проходит.
#
# Запуск: RUNTIME_CLONE=/tmp/runtime sh experiments/issue_434/runtime_smoke_sim.sh
set -u

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CLONE=${RUNTIME_CLONE:?укажите RUNTIME_CLONE}
CATALOG="$HERE/prototype/mango-products.yaml"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

printf 'runtime HEAD: %s\n' "$(git -C "$CLONE" rev-parse HEAD)"

prepare() {
  rm -rf "$WORK/rt"
  mkdir -p "$WORK/rt"
  git -C "$CLONE" archive HEAD | tar -x -C "$WORK/rt"
  # Проверки, предлагаемые РТ-1 (часть А) и РТ-3: вставляются перед итогом.
  awk '
    /^if \[ "\$FAILURES" -ne 0 \]; then$/ && !done {
      print "require_file taxonomy/mango-products.yaml"
      print "require_text taxonomy/mango-products.yaml '\''^closed: true$'\'' '\''product catalog is closed'\''"
      print "for af in $(grep -hEo '\''atomic_function: *\"?[a-z0-9/-]+'\'' \"$ROOT\"/golden/cases*.yaml | sed '\''s/.*: *\"\\{0,1\\}//'\''); do"
      print "  if grep -Fq \"{id: \\\"$af\\\", level: function,\" \"$ROOT/taxonomy/mango-products.yaml\" 2>/dev/null; then pass \"golden atomic_function $af is in catalog\"; else fail \"golden atomic_function $af is in catalog\"; fi"
      print "done"
      done = 1
    }
    { print }
  ' "$WORK/rt/tests/runtime-smoke.sh" > "$WORK/smoke.sh"
  mv "$WORK/smoke.sh" "$WORK/rt/tests/runtime-smoke.sh"
}

set_case_af() {
  # Первый положительный случай получает поле atomic_function (форма РТ-3).
  awk -v af="$1" '
    { print }
    /^  - id: GS-CC-01$/ { print "    product_class: contact-center"; print "    atomic_function: " af }
  ' "$WORK/rt/golden/cases.yaml" > "$WORK/cases.yaml"
  mv "$WORK/cases.yaml" "$WORK/rt/golden/cases.yaml"
}

run() {
  printf '\n=== scenario %s ===\n' "$1"
  sh "$WORK/rt/tests/runtime-smoke.sh" 2>&1 | grep -E 'mango-products|catalog|smoke test'
  printf 'exit: %s\n' "$(sh "$WORK/rt/tests/runtime-smoke.sh" >/dev/null 2>&1; echo $?)"
}

prepare
run missing

prepare
mkdir -p "$WORK/rt/taxonomy" && cp "$CATALOG" "$WORK/rt/taxonomy/mango-products.yaml"
run catalog

set_case_af queue-callback-offer
run invented

prepare
cp "$CATALOG" "$WORK/rt/taxonomy/mango-products.yaml"
set_case_af callback/function/callback-request-intake
run catalogid
