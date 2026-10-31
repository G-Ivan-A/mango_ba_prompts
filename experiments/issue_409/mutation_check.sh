#!/usr/bin/env bash
# Мутационная проверка приёмки #409: каждая порча артефакта должна ронять
# scripts/validate_issue_409_audit_artifacts.py. Файлы восстанавливаются из копии.
set -u
cd "$(dirname "$0")/../.."
V=scripts/validate_issue_409_audit_artifacts.py
mutate() {  # file sed-expression description
  cp "$1" /tmp/mut.bak
  sed -i "$2" "$1"
  if python3 "$V" >/dev/null 2>&1; then echo "MISSED: $3"; rc=1; else echo "caught: $3"; fi
  cp /tmp/mut.bak "$1"
}
rc=0
mutate docs/analysis/2026-10-31-file-disposition-register.md 's/^| `docs` | 46 |/| `docs` | 47 |/' "register area count"
mutate docs/rfc/2026-10-repository-modernization.md 's/F-01…F-20/F-01…F-19/' "stale finding range"
mutate docs/rfc/2026-10-repository-modernization.md '0,/^## Summary/s//## Summary\n\nСм. T-10./' "undefined task id"
mutate docs/rfc/rfc-register.md 's/#dec-03-видимость-f-05/#dec-03-видимость/' "broken DEC anchor"
mutate docs/audit/2026-10-31-repository-audit.md 's/233$/234/;s/^   актуальны, 113/   актуальны, 114/' "audit total drift"
mutate docs/analysis/2026-10-31-follow-up-tasks.md 's#(\.\./audit/#(https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/x/docs/audit/#' "fork link"
mutate docs/analysis/2026-10-31-follow-up-tasks.md 's/^updated: 2026-10-31/updated: 2026-10-31\nai-generated: true/' "forbidden ai-generated field"
mutate docs/audit/2026-10-31-repository-audit.md 's/ владелец / Фаундер /' "forbidden term"
mutate docs/rfc/2026-10-repository-modernization.md 's/hybrid-Intelligence-lab\/blob\/32b5fa52/hybrid-Intelligence-lab\/blob\/main/' "unpinned Hub link"
exit $rc
