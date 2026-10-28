"""Counterfactual safeguard design, NOT a runtime policy or LLM evaluator.

Inputs are human annotations of observed episodes or explicitly synthetic controls.
Only the decision protocol is exercised; semantic annotations are not inferred.
"""
import json
from pathlib import Path


def decide(state):
    kind = state['kind']
    if kind == 'delivery':
        return ('continue' if set(state['required']) <= set(state['delivered'])
                else 'block_release')
    if kind == 'baseline':
        return ('continue' if set(state['changed']) <= set(state['authorized_changes'])
                else 'block_disputed')
    if kind == 'evidence':
        # A relevant unavailable source creates a disclosed gap, never a fake read.
        verified = state['retrieved'] and state['entails_claim']
        addressed = state['question_owner'] == state['knowledge_owner']
        covered = set(state['relevant_products']) <= set(state['checked_products'])
        return 'continue' if verified and addressed and covered else 'block_disputed'
    if kind != 'appeal':
        raise ValueError(f'Unknown design case: {kind}')
    if state.get('hard_ban'):
        return 'block_disputed'
    if not state['inefficient']:
        return 'continue'
    # Neither ordinary approval nor two words in one message are two decisions.
    appeal_seen = False
    risk_message = None
    for event in state['events']:
        if event['decision'] != state['decision'] or event['revision'] != state['revision']:
            continue
        if event['actor'] == 'assistant' and event['action'] == 'reasoned_appeal':
            appeal_seen, risk_message = True, None
        elif appeal_seen and event['actor'] == 'human':
            if event['action'] == 'acknowledge_consequence':
                risk_message = event['message_id']
            elif (event['action'] == 'choose_inefficient_option' and risk_message
                  and event['message_id'] != risk_message):
                return 'execute_override'
    return 'block_disputed'


def main():
    base = Path(__file__).resolve().parent
    rows = json.loads((base / 'replay-cases.json').read_text())
    results = []
    for row in rows:
        actual = decide(row['input'])
        assert actual == row['expected'], (row['id'], actual, row['expected'])
        results.append({'id': row['id'], 'basis': row['basis'], 'hypotheses': row['hypotheses'],
                        'expected': row['expected'], 'actual': actual})
    result = {'scope': 'Annotated deterministic counterfactuals; no LLM run, '
                       'no product fact verification, no active policy changed.', 'cases': results}
    (base / 'replay-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: {len(results)} annotated counterfactual/control cases')


if __name__ == '__main__':
    main()
