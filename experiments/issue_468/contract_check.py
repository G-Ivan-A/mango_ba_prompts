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


def review_violations(state):
    """Check human-labelled decisions, not the semantics of generated text."""
    errors = []
    if state.get('mode') in ('paused', 'analysis_only') and state.get('produces_artifact'):
        errors.append('paused_execution')
    if state.get('authorization') == 'future_note' and state.get('produces_artifact'):
        errors.append('future_note_execution')
    if state.get('removed_rule') and not all(state.get(field) for field in
            ('change_evidence', 'impact_reviewed', 'replacement_coverage', 'ba_approved')):
        errors.append('unapproved_removal')
    if state.get('product_verdict') == 'confirmed' and state.get('basis') in (
            'analogy', 'search_report', 'memory', 'unknown'):
        errors.append('unsupported_product_fact')
    if state.get('raw_origin') == 'customer' and state.get('actual_origin') == 'knowledge':
        errors.append('source_substitution')
    if state.get('norm_conflict') and state.get('review_outcome') == 'accept':
        errors.append('uncritical_agreement')
    if state.get('question') and (state.get('already_answered') or state.get('asks_design')):
        errors.append('unnecessary_or_misaddressed_question')
    if state.get('contradiction_basis') == 'exists_but_out_of_scope':
        errors.append('scope_as_contradiction')
    if state.get('delivery_boundary_closed') and state.get('boundary_basis') == 'mechanism_only':
        errors.append('unresolved_delivery_boundary')
    if state.get('classification') == 'functional' and state.get('item_kind') in (
            'quality', 'design_example', 'api_workaround'):
        errors.append('what_how_mixed')
    if state.get('terms_conflated'):
        errors.append('meaning_lost')
    if state.get('artifact_available') == 'after_event' and state.get('requires_at_event'):
        errors.append('event_timing_conflict')
    return sorted(set(errors))
