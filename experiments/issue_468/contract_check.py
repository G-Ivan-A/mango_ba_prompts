"""Offline oracle for RFC-AIN-001 admission examples; NOT a chat runtime.

The input is a sanitised review state, not customer text. This makes gate
counterexamples inspectable without pretending to evaluate LLM behaviour.
"""
def violations(state):
    errors = []
    for field in ('rules_read', 'pool_approved', 'glossary_approved',
                  'atoms_traceable', 'questions_reviewed', 'snapshot_approved',
                  'snapshot_current', 'receipt_truthful'):
        if not state.get(field):
            errors.append(field)
    if state.get('action') != 'section2':
        errors.append('future_action')
    if state.get('frontier') or state.get('unchecked_dependencies'):
        errors.append('coverage_open')
    for claim in state.get('claims', []):
        if claim.get('basis') == 'analogy' and claim.get('verdict') == 'confirmed':
            errors.append('analogy_as_fact')
    for gap in state.get('gaps', []):
        if gap.get('evidence'):
            continue
        h = gap.get('hypothesis', {})
        if not (h.get('kind') == 'ba_hypothesis' and h.get('accepted')
                and h.get('owner') and h.get('risk') == 'bounded'
                and h.get('review_trigger') and h.get('visible')):
            errors.append('unresolved_gap')
    if state.get('no_progress_passes', 0) >= 2 and state.get('frontier'):
        errors.append('retrieval_stalled')
    return sorted(set(errors))
