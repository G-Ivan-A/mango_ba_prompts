#!/usr/bin/env bash
# Совместимость бэклога issue #418 с открытыми PR: слить их голову во
# временное дерево и перезапустить проверку бэклога и make validate-fast.
#   bash experiments/issue_418/merge_compat_check.sh <sha> [<sha> ...]
set -u
root=$(git rev-parse --show-toplevel)
for sha in "$@"; do
  tree=$(mktemp -d)/wt
  git -C "$root" worktree add -q --detach "$tree" HEAD
  if git -C "$tree" -c user.name=check -c user.email=check@localhost merge -q --no-edit "$sha" >/dev/null 2>&1; then
    echo "merge $sha: clean"
    python3 "$tree/scripts/validate_issue_418_backlog.py" >/dev/null 2>&1 && echo "  backlog validator: OK" || echo "  backlog validator: FAIL"
    (cd "$tree" && make validate-fast >/dev/null 2>&1) && echo "  make validate-fast: OK" || echo "  make validate-fast: FAIL"
  else
    echo "merge $sha: CONFLICT"; git -C "$tree" diff --name-only --diff-filter=U
  fi
  git -C "$root" worktree remove --force "$tree"
done
