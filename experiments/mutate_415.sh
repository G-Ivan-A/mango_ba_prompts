#!/usr/bin/env bash
# Mutation check: each edit to the RFC must make the #415 validator fail.
f=docs/rfc/2026-10-ba-automation-strategy.md
cp $f /tmp/rfc415.bak
run() { sed -i "$1" $f; if python3 scripts/validate_issue_415_strategy_rfc.py >/dev/null 2>&1; then echo "NOT CAUGHT: $1"; else echo "caught: $1"; fi; cp /tmp/rfc415.bak $f; }
run 's/Идёт параллельно этапу 4/Идёт после этапа 4/'
run 's/^### Этап 5\./### Шаг 5./'
run 's/^status: accepted/status: draft/'  # #417: accepted is now valid
run 's/Других процессов на этапе 1 нет/Также оценка ТЗ/'
run 's/(..\/vision.md)/(..\/visio.md)/'
run 's/Фокус/фаундер/; s/Кратко для руководителя/Кратко для руководителя фаундер/'
run 's/<a id="dec-415-03"><\/a>//'
run 's/| \*\*Сколько\*\* |/| Объём |/'
