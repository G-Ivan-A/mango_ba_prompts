"""Offline, bounded documentation locator. Output is a reading plan, not As-Is facts.

python3 experiments/issue_399/route.py 'WFM статус API amoCRM'
Cross-product candidates require the BA to select scope before reading a new
runtime class, as required by the existing hybrid-KB contract.
"""
import argparse
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[2]
KB = 'https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/b67410f627801345309281faa15e7219722bfb1a/docs/kb/'
CONNECTORS = {'amocrm': r'amo.?crm', 'bpmsoft': r'bpm.?soft', 'bitrix24': r'bitrix|битрикс', 'ldap': r'ldap'}


def select_pages(records, query, limit=12, capabilities=(), connector=None):
    if limit < 1:
        raise ValueError('limit must be positive')
    connectors = {c for c, pattern in CONNECTORS.items() if re.search(pattern, query, re.I)}
    if connector:
        connectors = {connector}
    workforce = bool(re.search(r'wfm|рабоч.{0,8}врем|пунктуаль|смен|план.{0,8}работ', query, re.I))
    agent = bool(re.search(r'статус|status|session|сесси|логин|вход', query, re.I))
    required = []
    if workforce or agent:
        required += ['cc-desktop', 'cc-web', 'pbx-account', 'administration']
    if re.search(r'api|апи', query, re.I):
        required += ['api']
    for product, pattern in [('sip-trunk', r'sip.?trunk|sip trunk'),
                             ('speech-analytics', r'речев.{0,4}аналит|speech'),
                             ('mango-talker', r'talker|талкер'),
                             ('mango-dialogi', r'диалог|mdialogi'),
                             ('report-builder', r'конструктор.{0,5}отчет'),
                             ('wallboard', r'wallboard')]:
        if re.search(pattern, query, re.I):
            required.append(product)
    required = list(dict.fromkeys(required))
    required += ['connector:'+c for c in sorted(connectors)]
    tokens = re.findall(r'[\w-]{3,}', query.lower())
    ranked = []
    for row in records:
        if row.get('http_status') != 200:
            continue
        if row.get('documentation_lifecycle') in ('deprecated-method', 'archived-location') and not re.search(r'устар|архив|legacy|deprecated', query, re.I):
            continue
        # A connector-specific claim cannot be answered by another connector.
        if row.get('connector_id') and connectors and row['connector_id'] not in connectors:
            continue
        if connectors and row['portal_product'] == 'integrations' and not row.get('connector_id'):
            continue
        text = (row.get('title', '') + ' ' + row['url']).lower()
        matched = [t for t in tokens if t in text]
        caps = {m['node_id'] for m in row.get('taxonomy_matches', [])}
        score = len(matched)*3 + len(caps.intersection(capabilities))*8
        if workforce and re.search(r'wfm|пунктуальн|рабоч.{0,8}врем|11_plan_raboty', text):
            score += 12
        if agent and re.search(r'статус|status|session|авторизац|порядок входа|\bправ[ао]?\b|\bролевая', text):
            score += 8
        if agent:
            if row['portal_product'] == 'api' and re.search(r'статус.{0,12}(пользовател|сесси)|upravlenie_statusami_i_sessiyami', text):
                score += 18
            if re.search(r'статус.{0,35}(автосекрет|сервер|запис)|status.{0,15}(server|record)', text):
                score -= 20
            if row['portal_product'] == 'pbx-account' and re.search(r'вход|выход|авторизац|/10_vhod/', text):
                score += 18
            if row.get('connector_id') in connectors and re.search(r'контакт.?центр|kontakt.?tsentr', text):
                score += 16
                if re.search(r'контакт.?центр', row.get('title', ''), re.I):
                    score += 8
            if any(m.get('status') == 'curated' and '/function/cc-api-' in m['node_id'] for m in row.get('taxonomy_matches', [])):
                score += 5
        if score or row['portal_product'] in required or row.get('connector_id') in connectors:
            ranked.append((score, row['url'], row, matched))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    chosen, gaps = [], []
    # Reserve one locator per requested product; API lexical matches cannot
    # consume the entire budget and erase client-side or authorization scope.
    for requirement in required:
        candidates = [item for item in ranked if
                      (item[2].get('connector_id') == requirement[10:] if requirement.startswith('connector:')
                       else item[2]['portal_product'] == requirement)]
        if candidates:
            if candidates[0] not in chosen:
                chosen.append(candidates[0])
        else:
            gaps.append(requirement)
    if agent:
        for c in sorted(connectors):
            if not any(item[2].get('connector_id') == c and re.search(r'статус|status', item[2].get('title', '')+' '+item[2]['url'], re.I)
                       for item in ranked):
                gaps.append('connector-status-locator:'+c)
    minimum = len(chosen)
    budget = max(limit, minimum)
    for item in ranked:
        if len(chosen) >= budget:
            break
        if item not in chosen:
            chosen.append(item)
    pages = [{**row, 'routing_score': score, 'matched_terms': terms,
              'reading_reason': 'requested-product-coverage-or-metadata-match',
              'next_action': 'read-article' if row.get('is_llm_readable') else 'targeted-runtime-or-visual-review'}
             for score, _, row, terms in chosen]
    return {'query': query, 'evidence_status': 'locators-only', 'pages': pages, 'coverage_gaps': gaps,
            'requested_limit': limit, 'coverage_minimum': minimum,
            'scope_gate': 'BA selects adjacent runtime classes before reading; no automatic requirement expansion',
            'fallback_required': bool(gaps or any(not p.get('is_llm_readable') for p in pages)),
            'fallback': {'read_order': [KB+'README.md', KB+'MAP.json', 'selected-class', 'document-index', 'targeted-sections'],
                         'image_semantics': 'description-not-guaranteed; verify OCR/caption/description against source',
                         'missing_evidence': 'record gap and route As-Is question to product/documentation owner'},
            'question_owner': {'as_is': 'product-team-or-documentation-owner', 'customer_need': 'customer'}}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('query')
    cli.add_argument('--map', type=Path, default=BASE/'docs/taxonomy/portal-map.jsonl')
    cli.add_argument('--limit', type=int, default=12)
    cli.add_argument('--capability', action='append', default=[])
    cli.add_argument('--connector', choices=sorted(CONNECTORS))
    args = cli.parse_args()
    rows = [json.loads(line) for line in args.map.read_text().splitlines()]
    print(json.dumps(select_pages(rows, args.query, args.limit, args.capability, args.connector), ensure_ascii=False, indent=2))
