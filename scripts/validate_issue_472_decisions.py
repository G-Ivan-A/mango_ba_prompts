#!/usr/bin/env python3
"""Check that the four owner decisions remain recorded and linked."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADR = 'docs/adr/2026-11-adr-018-rfc-audit-decisions.md'
text = (ROOT / ADR).read_text()
checks = {
    'deployment': ('2.7.0', '2.8.x', 'комплексной приёмке', 'BL-232'),
    'TTZ preparation': ('Р-ТТЗ-5 решено', 'параллельно BCREQ', 'этапе 2'),
    'link audit': ('все внутренние', 'BL-237', 'Владелец определяет охват'),
    'hypothesis gates': ('двух моделей', 'несколько итераций', 'положительного сигнала БА', 'BL-175'),
}
for name, required in checks.items():
    for phrase in required:
        assert phrase in text, f'{name}: missing {phrase}'
for path in (
    'docs/rfc/2026-11-a-in-decomposition.md',
    'docs/rfc/2026-11-ttz-feasibility-flow.md',
    'docs/audit/2026-11-07-bcreq-ttz-rfc-audit.md',
    'docs/site-access.md',
    'pr-ops/BACKLOG.md',
    'pr-ops/backlog-ba-model.md',
    'pr-ops/backlog-repository.md',
):
    assert Path(ADR).name in (ROOT / path).read_text(), f'{path}: decision link missing'
card = (ROOT / 'pr-ops/backlog-repository.md').read_text().split('### BL-237.')[1]
for repo in ('hybrid-Intelligence-lab', 'mango-ba-ai-runtime', 'ai-ba-playbooks'):
    assert repo in card, f'external audit scope missing {repo}'
assert '`TODO`' in card, 'external audit must remain open until performed'
print('issue #472 decisions: OK')
