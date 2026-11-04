#!/usr/bin/env bash
# Локальный прогон команд CI-воркфлоу (validate.yml, github-pages.yml, kb.yml):
# CI не запускается на PR из форка. Формат вывода: «код_возврата  команда».
# Изменения site/data (только поле generatedAt) после generate-pages-data отбрасываются.
cd "$(dirname "$0")/../.."
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  bash -c "$cmd" >/dev/null 2>&1; echo "$?  $cmd"
done <<'CMDS'
make validate-frontmatter
make validate-file-naming
make validate-structure
make validate-onboarding
make validate-full
node scripts/generate-pages-data.mjs
CMDS
for s in $(grep -ho 'python3 scripts/[a-z0-9_]*\.py' .github/workflows/github-pages.yml .github/workflows/kb.yml | awk '{print $2}' | sort -u); do
  python3 "$s" >/dev/null 2>&1; echo "$?  python3 $s"
done
git checkout -- site/data 2>/dev/null
