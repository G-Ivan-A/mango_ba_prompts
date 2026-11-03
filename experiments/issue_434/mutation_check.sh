#!/bin/sh
# Мутационная проверка валидатора issue #434: каждая порча RFC/каталога
# должна сделать валидатор красным. Файлы восстанавливаются из git.
# Запуск из корня репозитория: sh experiments/issue_434/mutation_check.sh
set -u
RFC=docs/rfc/2026-11-runtime-product-catalog-golden-set.md
V=scripts/validate_issue_434_runtime_tasks.py
mutate() {
  name=$1; file=$2; expr=$3
  cp "$file" /tmp/mut.bak
  sed -i "$expr" "$file"
  if python3 "$V" >/dev/null 2>&1; then r="NOT DETECTED"; else r="detected"; fi
  cp /tmp/mut.bak "$file"
  printf '%-40s %s\n' "$name" "$r"
}
mutate "drop link М-6"            "$RFC" '/^| М-6 |/d'
mutate "wrong AF count cc"        "$RFC" 's/| `contact-center` | `contact-center` | 17 | 59 | 66 |/| `contact-center` | `contact-center` | 17 | 59 | 65 |/'
mutate "runtime link on main"     "$RFC" '0,/mango-ba-ai-runtime\/blob\/5d8c2015[0-9a-f]*/s//mango-ba-ai-runtime\/blob\/main/'
mutate "relative link in РТ-1"    "$RFC" 's|^- Полный URL постановки: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/rfc/|- Полный URL постановки: [x](../rfc/)|'
mutate "drop #427 link"           "$RFC" 's|issues/427|issues/999|g'
mutate "drop obligation"          "$RFC" 's/обязывает runtime зафиксировать актуальную/предлагает runtime/'
mutate "drop НФТ in body"         "$RFC" '0,/^## НФТ$/s//## НФТ-x/'
mutate "drop Почему in step"      "$RFC" '0,/^   Почему: тела задач/s//   Так как тела задач/'
mutate "invented function in cat" docs/taxonomy/products.json 's/"callback-scheduling"/"queue-callback-offer"/'
