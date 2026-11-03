#!/usr/bin/env bash
# Локальный прогон команд CI-воркфлоу (validate.yml, github-pages.yml, kb.yml):
# CI не запускается на PR из форка. Список — как в ci-local.log первого прогона.
cd "$(dirname "$0")/../.."
fail=0
for cmd in "make validate-frontmatter" "make validate-file-naming" "make validate-structure" \
           "make validate-onboarding" "node scripts/generate-pages-data.mjs"; do
  echo "== $cmd"; $cmd >/dev/null 2>&1; rc=$?; echo "rc=$rc"; [ $rc -ne 0 ] && fail=$((fail+1))
done
for s in $(grep -ho 'python3 scripts/[a-z0-9_]*\.py' .github/workflows/github-pages.yml .github/workflows/kb.yml | awk '{print $2}' | awk '!seen[$0]++'); do
  python3 "$s" >/dev/null 2>&1; rc=$?; echo "rc=$rc $s"; [ $rc -ne 0 ] && fail=$((fail+1))
done
echo "== make validate-full"; make validate-full >/dev/null 2>&1; rc=$?; echo "rc=$rc"; [ $rc -ne 0 ] && fail=$((fail+1))
echo "failures=$fail"
