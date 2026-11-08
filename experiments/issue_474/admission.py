"""Offline specification examples with expected labels. Never runs a chat or gate.

Extends #468's oracle with the explicit, version-bound BA decision needed to
write section 2. Prompt semantics and actual LLM obedience need separate review.
"""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('ain468', Path(__file__).resolve().parents[1]/'issue_468/contract_check.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
KEYS = ('task_id', 'attempt', 'route_version', 'snapshot_id', 'snapshot_version')


def violations(state):
    errors = legacy.violations(state)
    gate = state.get('gate21', {})
    if not (gate.get('gate') == 'AIN-21' and gate.get('decision') == 'allow'
            and gate.get('actor_role') == 'BA' and gate.get('actor')
            and gate.get('date') and gate.get('locator') and gate.get('report_version')):
        errors.append('explicit_ba_gate_missing')
    if any(not state.get(k) or state[k] != gate.get(k) for k in KEYS):
        errors.append('gate_version_mismatch')
    if state.get('current_step') != 'AIN-22' or not state.get('execute_current'):
        errors.append('separate_call_missing')
    if state.get('question_states') and any(s in ('pending', 'rework') for s in state['question_states']):
        errors.append('questions_pending')
    if state.get('paused'):
        errors.append('paused_execution')
    return sorted(set(errors))


def evidence_violations(claim):
    """Offline counterexamples for the existing feasibility scale, no new enum.

    This is a review oracle, not a product classifier or a provenance adapter.
    """
    errors = []
    verdict = claim.get('feasibility')
    if verdict not in (None, 'Да', 'Нет', 'Частично'):
        errors.append('unknown_feasibility')
    if verdict is not None:
        if not (claim.get('exact_scope') and claim.get('evidence_ids')
                and claim.get('access') == 'read' and claim.get('freshness') == 'current'
                and not claim.get('contradiction')):
            errors.append('unsupported_feasibility')
        if claim.get('origin') == 'ba_hypothesis':
            errors.append('hypothesis_as_fact')
    return errors
