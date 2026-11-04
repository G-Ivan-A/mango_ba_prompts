#!/bin/sh
# Мутационная проверка валидаторов issue #442 (BL-163): каждая порча реестра,
# RFC или копии каталога в клоне runtime должна сделать валидатор красным.
# Файлы восстанавливаются из копии. Запуск из корня репозитория:
#   RUNTIME_CLONE=/path/to/runtime sh experiments/issue_442/mutation_check.sh
set -u
REG=standards/bcreq-runtime-references.md
RFC=docs/rfc/2026-11-runtime-product-catalog-golden-set.md
V430=scripts/validate_issue_430_runtime_refs.py
V434=scripts/validate_issue_434_runtime_tasks.py
mutate() {
  name=$1; validator=$2; file=$3; expr=$4
  cp "$file" /tmp/mut442.bak
  sed -i "$expr" "$file"
  if python3 "$validator" >/dev/null 2>&1; then r="NOT DETECTED"; else r="detected"; fi
  cp /tmp/mut442.bak "$file"
  printf '%-44s %s\n' "$name" "$r"
}
echo "# baseline"
for v in "$V430" "$V434"; do
  if python3 "$v" >/dev/null 2>&1; then echo "$v green"; else echo "$v RED (baseline broken)"; fi
done
echo "# реестр"
mutate "registry SHA back to 5d8c201"          "$V430" "$REG" 's/2db0ef5106883b01b096fe8c4af50334899e9fe0/5d8c201511fd730a596c9f9b4588470a7b01edc9/g'
mutate "И-2 link on main"                      "$V430" "$REG" '/^| И-2 /s|blob/2db0ef5106883b01b096fe8c4af50334899e9fe0/taxonomy/mango-products.yaml|blob/main/taxonomy/mango-products.yaml|'
mutate "И-2 back to Нет"                       "$V430" "$REG" '/^| И-2 /s/| Да: закрытый каталог/| Нет: закрытый каталог/'
mutate "drop З-1 tombstone row"                "$V430" "$REG" '/^Снятые заглушки\./,/^| З-1 /{/^| З-1 /d}'
mutate "tombstone without BL-163"              "$V430" "$REG" '/^| З-1 /s/BL-163/BL-999/'
mutate "drop РТ-6 row"                         "$V430" "$REG" '/^| РТ-6 /d'
mutate "РТ-1 without PR #16"                   "$V430" "$REG" '/^| РТ-1 /s|pull/16|pull/99|g'
mutate "drop section 2.1"                      "$V430" "$REG" 's/^### 2\.1\. /### 2.9. /'
echo "# RFC"
mutate "drop readiness heading 12.1"           "$V434" "$RFC" 's/^### 12\.1\. Проверка готовности/### 12.1. Готовность/'
mutate "РТ-6 body loses НФТ"                   "$V434" "$RFC" '/^Заголовок: `РТ-6\./,/^````$/s/^## НФТ$/## НФТ-x/'
mutate "old SHA in section 12"                 "$V434" "$RFC" '/^## 12\. /,$s|mango-ba-ai-runtime/pull/16|mango-ba-ai-runtime/blob/5d8c201511fd730a596c9f9b4588470a7b01edc9/x|'
mutate "BL-163 not in review"                  "$V434" pr-ops/BACKLOG.md '/^| BL-163 |/s/| review |/| todo |/'
if [ -n "${RUNTIME_CLONE:-}" ]; then
  CAT="$RUNTIME_CLONE/taxonomy/mango-products.yaml"
  echo "# клон runtime ($RUNTIME_CLONE)"
  mutate "catalog not closed"                  "$V430" "$CAT" 's/^closed: true$/closed: false/'
  mutate "catalog loses a node"                "$V430" "$CAT" '0,/^  - {id: "agent-workspace\/feature\/agent-session"/{/^  - {id: "agent-workspace\/feature\/agent-session"/d}'
  mutate "wrong parent"                        "$V430" "$CAT" '/^  - {id: "agent-workspace\/feature\/agent-session"/s/parents: \["agent-workspace"\]/parents: ["analytics"]/'
  mutate "source_sha256 tampered"              "$V430" "$CAT" 's/^source_sha256: \(.\)c/source_sha256: \1d/; s/^source_sha256: c/source_sha256: d/'
  mutate "lifecycle drift outside 2.1"         "$V430" "$CAT" '0,/lifecycle: retained}/s//lifecycle: deprecated}/'
fi
