#!/usr/bin/env bash
# Мутационная проверка валидатора #438: каждая порча должна ронять проверку.
set -u
cd "$(dirname "$0")/../.."
V=scripts/validate_issue_438_step_prompts.py
run() { # $1 — описание, $2 — файл, $3 — команда порчи
  cp "$2" /tmp/mut_backup
  eval "$3"
  if python3 "$V" >/dev/null 2>&1; then echo "MISSED: $1"; else echo "caught: $1"; fi
  cp /tmp/mut_backup "$2"
}
run "v0.1 Ш-В изменён без пересборки" prompts/bcreq-review-validation-oneshot.md 'echo >> prompts/bcreq-review-validation-oneshot.md'
run "черновик правлен руками" prompts/drafts/bcreq-fr-documentation-stepwise.md 'sed -i "0,/Ш-/s//Ш_/" prompts/drafts/bcreq-fr-documentation-stepwise.md'
run "лишний файл в drafts" prompts/drafts/manifest.json "touch prompts/drafts/extra.md"; rm -f prompts/drafts/extra.md
run "лишняя колонка в комплекте" docs/ba-processes/bcreq-run-kit.md 'sed -i "0,/^| 2 | Ш-1 /s//| 2 | x | Ш-1 /" docs/ba-processes/bcreq-run-kit.md'
run "метрика RUN-0080 подправлена" runs/2026/RUN-0080/outputs/metrics.json 'sed -i "0,/\"passed\": 55/s//\"passed\": 56/" runs/2026/RUN-0080/outputs/metrics.json'
run "Р-16 принят без валидатора 433" pr-ops/BACKLOG.md 'sed -i "/^| \*\*Р-16\*\* |/s/| ждёт |$/| принято |/" pr-ops/BACKLOG.md'
run "цитата ADR-0003 изменена" docs/adr/0003-creative-mode-governance.md 'sed -i "s/молчание = согласие/молчание - согласие/" docs/adr/0003-creative-mode-governance.md'
git status --short
