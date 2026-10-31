#!/usr/bin/env bash
# Mutation check for scripts/validate_issue_413_prompt_generalization.py.
# Each mutation must make the validator fail; files are restored from a copy.
set -u
V=scripts/validate_issue_413_prompt_generalization.py
cd "$(dirname "$0")/../.."
run() { if python3 "$V" >/dev/null 2>&1; then echo "MISSED: $1"; else echo "caught: $1"; fi; }
mutate() { # file, description, command
  cp "$1" /tmp/issue413.bak; eval "$3"; run "$2"; cp /tmp/issue413.bak "$1"; }
P=prompts/bcreq-core-documentation-oneshot.md
C=prompts/bcreq-constitution-governance-oneshot.md
S=standards/prompt-standard.md
mutate "$P" "new question id"   "echo 'Уточни Q-2.1' >> $P"
mutate "$P" "new task id"       "echo 'как в BCREQ-1024' >> $P"
mutate "$P" "new run id"        "echo 'см. RUN-0080' >> $P"
mutate "$P" "new issue ref"     "echo 'см. #411' >> $P"
mutate "$C" "stale allowlist"   "sed -i 's/(RUN-0076, SC-65)//' $C"
mutate "$S" "rule G3 removed"   "sed -i 's/\*\*G3\.\*\*/G3./' $S"
mutate "$S" "section renamed"   "sed -i 's/^## Обобщение содержимого промпта (issue #413)/## Обобщение/' $S"
python3 "$V" >/dev/null && echo "baseline: pass"
