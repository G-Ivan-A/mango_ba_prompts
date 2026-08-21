#!/usr/bin/env bash
# Негативная проверка scripts/validate_issue_272_run_0013.py: валидатор должен
# падать на ручной правке порождаемого файла, на разъехавшихся метриках и на
# несогласованном вердикте эпизода. Изменения откатываются в конце.
set -u
cd "$(dirname "$0")/.."
RUN=runs/2026/RUN-0013
fail=0

expect_fail() {
  local label="$1"
  if python3 scripts/validate_issue_272_run_0013.py >/tmp/neg.log 2>&1; then
    echo "NOT DETECTED: $label"; fail=1
  else
    echo "detected: $label — $(sed -n '2p' /tmp/neg.log)"
  fi
  git checkout -- "$RUN"
}

sed -i 's/^| Сообщений в ветке | 34 |/| Сообщений в ветке | 999 |/' "$RUN/logs/metrics.md"
expect_fail "ручная правка порождаемых метрик"

sed -i 's/^  output_tokens: 27219$/  output_tokens: 1/' "$RUN/metadata.yaml"
expect_fail "метрика metadata.yaml разошлась с экспортом"

sed -i 's/^| E2 | Критическая переоценка и проверка API | `\[4\]`–`\[9\]` | works |/| E2 | Критическая переоценка и проверка API | `[4]`–`[9]` | fails |/' "$RUN/outputs/episodes.md"
expect_fail "вердикт эпизода разошёлся между файлами"

python3 scripts/validate_issue_272_run_0013.py && echo "baseline PASS restored" || { echo "BASELINE BROKEN"; fail=1; }
exit $fail
