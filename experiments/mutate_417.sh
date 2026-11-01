#!/usr/bin/env bash
# Mutation check: each edit must make the #417 acceptance validator fail.
f=docs/rfc/2026-10-ba-automation-strategy.md
r=docs/rfc/rfc-register.md
a=docs/analysis/2026-10-31-industry-practice-check.md
cp $f /tmp/rfc417.bak; cp $r /tmp/reg417.bak; cp $a /tmp/ana417.bak
run() {
  sed -i "$2" "$1"
  if python3 scripts/validate_issue_417_rfc_acceptance.py >/dev/null 2>&1; then echo "NOT CAUGHT: $1: $2"; else echo "caught: $1: $2"; fi
  cp /tmp/rfc417.bak $f; cp /tmp/reg417.bak $r; cp /tmp/ana417.bak $a
}
run $f 's/^status: accepted/status: proposed/'
run $f 's/^version: 0.2/version: 0.1/'
run $f 's/| принято предварительно |/| принято |/'
run $f 's/OpenCode (решение владельца, #417)/OpenCode/'
run $f 's/выделенном сервере/сервере/g'
run $f 's/без n8n/с n8n/g'
run $f 's/agentic coding/AI/g'
run $f 's/по требованию владельца/по графику/g'
run $f 's/14 промптов/15 промптов/'
run $f 's/<a id="dec-415-11"><\/a>//'
run $r '/RFC-415-DEC-10/s/`accepted` (#417)/`proposed`/'
run $r '/^| \[REC-417-03\]/s/`proposed`/`accepted`/'
run $a 's/Критичных отклонений нет/Критичные отклонения есть/'
run $a 's/<a id="rec-417-05"><\/a>//'
run $a '0,/| совпадает |/s//| отклоняется |/'
