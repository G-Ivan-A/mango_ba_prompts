#!/usr/bin/env python3
"""Check an observed, tool-assisted model response. No generated model answers.

--fetch re-reads the pinned source with gh and verifies its hash and quotation.
Default is an offline integrity/regression check, not a model evaluation.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check(fetch=False):
    data = json.loads((HERE/'recording-observation.json').read_text())
    evidence = data['output']['evidence'][0]
    assert data['execution']['mode'] == 'tool'
    assert data['execution']['independent_model_run'] is False
    assert data['output']['customer_questions'] == []
    assert data['output']['removed_questions'] == ['TECH-1']
    assert data['output']['feasibility'] == 'Да'
    assert len(data['output']['not_established']) >= 3
    assert evidence['quote'] == 'запись разговора может отобразиться в карточке контакта с небольшой задержкой.'
    assert evidence['locator'].endswith('#L34')
    kit = json.loads((ROOT/'site/data/a-in-kit.json').read_text())
    prompt = kit['steps'][8]['prompt']
    assert hashlib.sha256(prompt.encode()).hexdigest() == data['execution']['prompt_sha256']
    assert 'resolved_technical_questions' in prompt
    assert 'Доказательную базу проверки' in prompt
    for case in data['negative_cases']:
        assert case['feasibility'] is None
        assert case['technical_question_to_ba'] is False
        assert case['marker'].startswith('[ACCESS_GAP: Требуется ручной поиск в БЗ по теме: ')
        assert case['marker'].endswith(']')
    if fetch:
        source = data['source']
        raw = subprocess.run(['gh','api',
            f"repos/{source['repo']}/contents/{source['path']}?ref={source['commit']}",
            '-H','Accept: application/vnd.github.raw+json'],
            check=True, capture_output=True).stdout
        assert hashlib.sha256(raw).hexdigest() == source['sha256'], 'Pinned source bytes changed'
        assert evidence['quote'] in raw.decode()
        print('Pinned KB source fetched; full SHA-256 and L34 quotation verified.')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    check(args.fetch)
    print('Observed response integrity OK (not an independent LLM evaluation).')
