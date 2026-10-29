"""Build the four-level product catalog and portal mapping from recorded evidence.

No network. The historical Product Layer is normalized in baseline.json;
bindings below are editorial associations, not new product availability claims.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
OUT = ROOT / 'docs/taxonomy'
PORTAL = 'https://www.mango-office.ru/support/'
LEVELS = ['Domain', 'Capability', 'Feature', 'Atomic Function']
RUNTIME = 'https://github.com/G-Ivan-A/mango-ba-ai-runtime/blob/b67410f627801345309281faa15e7219722bfb1a/taxonomy/products.yaml'
NEW_CAPABILITIES = [
    {'id': 'report-builder', 'name': 'Конструктор отчётов',
     'domain_ids': ['voice-ucaas', 'contact-center', 'analytics'],
     'source_url': PORTAL+'3_produkty-i-prilozheniya/12_konstruktor-otchetov/',
     'mango_status': 'Документация обнаружена; коммерческая доступность не проверялась'}
]

# One binding per historical feature, in its original order. A function can
# participate in several features; this remains a four-level DAG, not a fifth level.
BINDINGS = {
 'cloud-pbx': 'extension-provisioning;auto-attendant;working-hours-routing;voicemail-to-email',
 'sip-connectivity': 'sip-trunk-registration;codec-selection;trunk-failover',
 'number-management': 'number-assignment;tollfree-routing;number-assignment;number-porting',
 'ivr-voice-menu': 'ivr-menu-navigation,service-availability-routing;auto-secretary-greeting;auto-secretary-greeting',
 'call-recording': 'call-recording-capture,recording-access-control;call-log-export;call-log-export',
 'callback': 'callback-request-intake;callback-request-intake;callback-scheduling',
 'unified-communications': 'softphone-call;corporate-chat;presence-update',
 'video-conferencing': 'meeting-host;meeting-recording;screen-share',
 'number-branding': 'caller-id-labeling;carousel-number-rotation;reachability-monitoring;reachability-monitoring',
 'voice-sms-broadcast': 'voice-message-broadcast;voice-message-broadcast,consent-filter;delivery-confirmation',
 'call-routing': 'skill-based-routing;queue-management;overflow-routing',
 'omnichannel-contact-center': 'interaction-routing;unified-agent-desktop;interaction-routing',
 'agent-workspace': 'interaction-handling;customer-card-popup;interaction-handling',
 'outbound-calling': 'disposition-code-assignment,callback-scheduling;predictive-dialing;campaign-realtime-view;campaign-history-view',
 'quality-management': 'scorecard-evaluation;scorecard-evaluation;evaluation-appeal',
 'workforce-management': 'shift-scheduling;load-forecasting;punctuality-report-view',
 'knowledge-base': 'article-lifecycle;script-guidance;article-lifecycle',
 'deal-management': 'deal-pipeline-tracking;communication-logging;communication-logging',
 'crm-platform': 'crm-record-management;crm-record-management',
 'self-service-portal': 'self-service-login;service-self-provisioning;self-service-recording-access;service-self-provisioning',
 'operator-mobile-app': 'mobile-interaction-handling;push-notification-delivery;mobile-interaction-handling',
 'sms-messaging': 'bulk-sms-dispatch,advertising-consent-check;bulk-sms-dispatch;opt-out-handling',
 'omnichannel-messaging': 'channel-ingestion;channel-ingestion;channel-ingestion;unified-inbox-routing',
 'website-chat': 'chat-widget-embed;chat-widget-embed;visitor-data-capture',
 'messenger-marketing': 'messenger-campaign-dispatch;messenger-campaign-dispatch;messenger-optin-management',
 'chatbot': 'agent-handoff;intent-classification;agent-handoff',
 'voice-bot': 'speech-to-text;voice-dialog-flow;text-to-speech',
 'process-robot': 'automated-action-execution;automated-action-execution;action-audit-logging',
 'speech-analytics': 'call-transcription;sentiment-scoring;keyword-spotting',
 'call-tracking': 'dynamic-number-substitution;source-attribution;source-attribution',
 'end-to-end-analytics': 'romi-calculation;romi-calculation;funnel-tracking',
 'multichannel-analytics': 'attribution-modeling;lead-deduplication;attribution-modeling',
 'email-tracking': 'email-event-tracking;email-event-tracking;unsubscribe-handling',
 'product-analytics': 'sku-performance-analysis;sku-performance-analysis;data-quality-check',
 'competitor-analysis': 'competitor-data-collection;competitor-data-collection',
 'telephony-equipment': 'device-provisioning;device-compatibility-check;device-compatibility-check',
 'information-security': 'role-based-access-control;security-audit-logging;data-classification;security-audit-logging',
 'platform-integration': 'crm-bidirectional-sync;crm-bidirectional-sync;directory-sync;crm-bidirectional-sync',
 'open-api': 'api-rate-limiting;webhook-subscription;webhook-subscription',
 'cpaas': 'programmable-voice-call;programmable-message-send;programmable-voice-call',
 'service-desk': 'ticket-lifecycle;ticket-lifecycle;ticket-lifecycle',
 'vendor-support-services': 'application-maintenance;crm-customization;application-maintenance',
}

# Search aliases are conservative candidate routing rules. Matching a title or
# branch supplies a documentation locator, never proof of a product claim.
ALIASES = {
 'cloud-pbx': r'виртуальн.*атс|личн.*кабинет|настройк.*атс',
 'sip-connectivity': r'sip.?trunk|sip trunk|sip-телефон|sip-оборудован',
 'number-management': r'номер|нумерац',
 'ivr-voice-menu': r'голосов.*меню|ivr|автосекретар|приветств',
 'call-recording': r'запис.*(разговор|вызов)|журнал.*звон|история.*вызов',
 'callback': r'обратн.*звон|callback|автоперезвон',
 'unified-communications': r'mango.?talker|mango talker|присутств|корпоративн.*чат',
 'video-conferencing': r'видеоконференц|видеовстреч|демонстрац.*экран',
 'number-branding': r'этикетк|карусел|маркировк.*номер|антиспам',
 'voice-sms-broadcast': r'автоинформ|голосов.*рассыл',
 'call-routing': r'распределен.*(вызов|звон)|очеред.*(вызов|звон)|маршрутиз',
 'omnichannel-contact-center': r'контакт.?центр|омниканал',
 'agent-workspace': r'рабоч.*место|обработ.*обращен|карточк.*клиент',
 'outbound-calling': r'исходящ.*обзвон|предиктив|кампани.*обзвон',
 'quality-management': r'контрол.*качеств|оценк.*качеств|чек-лист|скоринг',
 'workforce-management': r'wfm|пунктуальн|график.*(работ|смен)|план.*работ|нагрузк.*оператор',
 'knowledge-base': r'баз.*знаний|скрипт.*(оператор|разговор)',
 'deal-management': r'сделк|воронк.*продаж',
 'crm-platform': r'crm-платформ|crm core',
 'self-service-portal': r'личн.*кабинет|самообслуж',
 'operator-mobile-app': r'мобильн.*(оператор|контакт.?центр)',
 'sms-messaging': r'sms|смс',
 'omnichannel-messaging': r'манго.?диалог|мессенджер|whatsapp|telegram|канал.*email',
 'website-chat': r'чат.*сайт|сайт.*чат|виджет.*чат',
 'messenger-marketing': r'whatsapp.*рассыл|мессенджер.*маркетинг',
 'chatbot': r'чат.?бот',
 'voice-bot': r'голосов.*робот|ai-робот|распознав.*реч|синтез.*реч',
 'process-robot': r'робот.*администратор',
 'speech-analytics': r'речев.*аналит|rechevaya-analitika|транскрибац',
 'call-tracking': r'коллтрекинг|kolltreking|подмен.*номер',
 'end-to-end-analytics': r'сквозн.*аналит|romi|roi|доход',
 'multichannel-analytics': r'мультиканальн|атрибуц|уникальност.*(звон|лид)',
 'email-tracking': r'email.?трекинг|email.?tracking',
 'product-analytics': r'товарн.*аналит|sku|ecommerce',
 'competitor-analysis': r'конкурент',
 'telephony-equipment': r'sip-оборудован|sip-телефон|гарнитур|прошивк',
 'information-security': r'\bрол[ьи]\b|\bправ[ао]?\b|sso|безопасн|авторизац|аутентификац',
 'platform-integration': r'интеграц|integratsii|amocrm|bpm.?soft|ldap|битрикс|1с',
 'open-api': r'api|вебхук|webhook|событи',
 'cpaas': r'программируем|cpaas',
 'service-desk': r'helpdesk|service desk|itsm',
 'vendor-support-services': r'vendor.service|развити.*crm',
 'report-builder': r'конструктор.*отчет|konstruktor-otchetov',
}


def dump(path, data):
    """Valid JSON with one record per line, keeping large catalogs reviewable."""
    lines = ['{']
    for key, value in data.items():
        prefix = '  ' + json.dumps(key) + ': '
        if isinstance(value, list):
            lines.append(prefix + '[')
            lines.extend('    ' + json.dumps(row, ensure_ascii=False, separators=(',', ':')) +
                         (',' if i < len(value)-1 else '') for i, row in enumerate(value))
            lines.append('  ],')
        else:
            lines.append(prefix + json.dumps(value, ensure_ascii=False) + ',')
    lines[-1] = lines[-1].rstrip(',')
    lines.append('}')
    path.write_text('\n'.join(lines) + '\n')


def product_id(url):
    groups = {
        '1_virtualnaya-ats-i-lichnyi-kabinet': 'pbx-account', '2_mobilnyi-lk': 'mobile-account',
        '3_kontakt-tsentr': 'cc-desktop', '3_web_cc': 'cc-web', '4_kontrol-kachestva': 'quality',
        '5_kolltreking-i-analitika': 'marketing-analytics', '7_mango-talker': 'mango-talker',
        '8_rechevaya-analitika-i-skoring': 'speech-analytics', '9_roboty-i-ai-roboty': 'robots',
        '10_sip-trunk': 'sip-trunk', '11_wallboard': 'wallboard',
        '6_mango-dialogi': 'mango-dialogi', '5_tekstovye_kommunikatsii': 'text-communications',
        '12_konstruktor-otchetov': 'report-builder',
    }
    for part, product in groups.items():
        if '/' + part + '/' in url:
            return product
    if '/4_integratsii/' in url:
        return 'integrations'
    if '/5_api-i-razrabotka/' in url:
        return 'api'
    if '/6_administrirovanie/' in url:
        return 'administration'
    return 'navigation-or-legacy'


def connector_id(url):
    for expression, connector in [(r'amo.?crm', 'amocrm'), (r'bpm.?soft', 'bpmsoft'),
                                  (r'bitrix|bitriks', 'bitrix24'), (r'ldap', 'ldap')]:
        if re.search(expression, url, re.I):
            return connector
    return None


def build():
    OUT.mkdir(exist_ok=True)
    baseline = json.loads((BASE / 'baseline.json').read_text())
    audit = [json.loads(line) for line in (OUT / 'portal-audit.jsonl').read_text().splitlines()]
    additions = json.loads((BASE / 'additions.json').read_text())
    by_url = {p['url']: p for p in audit}
    capabilities = baseline['capabilities'] + NEW_CAPABILITIES
    nodes = []
    for domain in baseline['domains']:
        nodes.append({**domain, 'level': 'Domain', 'parent_ids': [], 'source_urls': [baseline['source_url']], 'origin': 'inherited'})
    for cap in baseline['capabilities']:
        nodes.append({'id': cap['id'], 'level': 'Capability', 'name': cap['name'],
                      'parent_ids': cap['domain_ids'] or [d['id'] for d in baseline['domains']],
                      'cross_domain': not bool(cap['domain_ids']), 'origin': 'inherited',
                      'mango_status_at_baseline': cap['mango_status'], 'row': cap['row'],
                      'related_commercial_fields': cap['related_commercial_fields'],
                      'source_urls': [baseline['source_url']]})
        bindings = BINDINGS[cap['id']].split(';')
        assert len(bindings) == len(cap['features']), cap['id']
        for feature, functions in zip(cap['features'], bindings):
            nodes.append({'id': cap['id'] + '/feature/' + feature, 'name': feature, 'level': 'Feature',
                          'parent_ids': [cap['id']], 'legacy_id': feature, 'origin': 'inherited', 'source_urls': [baseline['source_url']]})
        for function in cap['atomic_functions']:
            parents = [cap['id'] + '/feature/' + f for f, fs in zip(cap['features'], bindings) if function['id'] in fs.split(',')]
            assert parents, (cap['id'], function['id'])
            nodes.append({'id': cap['id'] + '/function/' + function['id'], 'name': function['id'],
                          'level': 'Atomic Function', 'parent_ids': parents, 'params': function['params'],
                          'origin': 'inherited', 'legacy_id': function['id'], 'binding_basis': 'editorial-association-of-inherited-lists',
                          'source_urls': [baseline['source_url']]})
    for cap in NEW_CAPABILITIES:
        assert by_url[cap['source_url']]['http_status'] == 200
        nodes.append({'id': cap['id'], 'name': cap['name'], 'level': 'Capability',
                      'parent_ids': cap['domain_ids'], 'cross_domain': True,
                      'origin': 'portal-update', 'source_urls': [cap['source_url']]})
    for addition in additions:
        assert addition['url'] in by_url, addition['url']
        page = by_url[addition['url']]
        assert page['http_status'] == 200 and page.get('body_found'), addition['url']
        if addition.get('heading'):
            assert any(addition['heading'] in h['text'] for h in page['headings']), addition
        else:
            assert addition['title'] == page['title'], addition
        cap = addition['capability']
        feature_id = cap + '/feature/' + addition['feature']
        if feature_id not in {n['id'] for n in nodes}:
            nodes.append({'id': feature_id, 'name': addition['feature_name'], 'level': 'Feature',
                          'parent_ids': [cap], 'origin': 'portal-update', 'source_urls': [addition['url']]})
        nodes.append({'id': cap + '/function/' + addition['function'], 'name': addition['name'],
                      'level': 'Atomic Function', 'parent_ids': [feature_id],
                      'params': addition.get('params', []), 'origin': 'portal-update',
                      'binding_basis': 'curated-page-or-heading', 'source_urls': [addition['url']],
                      'locator': addition.get('heading', addition['title']), 'verification': addition['verification'],
                      'evidence_scope': 'documented-operation; exact semantics require article text and visual context'})
    by_id = {n['id']: n for n in nodes}
    assert len(by_id) == len(nodes), 'duplicate node ID'
    maps = []
    for page in audit:
        url = page['url']
        product = product_id(url)
        search = page.get('title', '') + ' ' + url
        cap_ids = [c['id'] for c in capabilities if re.search(ALIASES[c['id']], search, re.I)]
        direct = [a for a in additions if a['url'] == url]
        cap_ids = sorted(set(cap_ids + [a['capability'] for a in direct]))
        domains = sorted({d for c in cap_ids for d in by_id[c]['parent_ids']})
        direct_links = [{'target_url': link, 'target_product': product_id(link), 'basis': 'observed-content-link'}
                        for link in page.get('content_links', []) if link in by_url and product_id(link) != product
                        and product_id(link) != 'navigation-or-legacy']
        good = page['http_status'] == 200 and page.get('text_chars', 0) > 0
        maps.append({'url': url, 'title': page.get('title', ''), 'portal_product': product,
                     'documentation_lifecycle': 'deprecated-method' if 'ustarevsh' in url else
                                                'archived-location' if 'arhiv-integratsii' in url else 'current-or-unspecified',
                     'connector_id': connector_id(url),
                     'taxonomy_matches': ([{'node_id': c, 'level': 'Capability', 'status': 'candidate',
                                            'basis': 'title-or-url-alias'} for c in cap_ids] +
                                          [{'node_id': a['capability'] + '/feature/' + a['feature'], 'level': 'Feature',
                                            'status': 'curated', 'basis': a.get('heading', a['title'])} for a in direct] +
                                          [{'node_id': a['capability'] + '/function/' + a['function'], 'level': 'Atomic Function',
                                            'status': 'curated', 'basis': a.get('heading', a['title'])} for a in direct]),
                     'candidate_domains': domains,
                     'unmapped_reason': None if cap_ids else 'navigation-or-no-supported-rule; manual classification required',
                     'http_status': page['http_status'], 'relevance_for_BA':
                     {'FT': 3 if good and cap_ids else 1 if good else 0,
                      'NFT': 3 if good and product in ('administration', 'api', 'sip-trunk') else 1 if good else 0,
                      'integrations': 3 if good and product in ('integrations', 'api') else 1 if good else 0,
                      'basis': 'editorial 0..3 routing heuristic; not a measured relevance score'},
                     'has_visual_context': page.get('has_visual_context', False),
                     'is_llm_readable': page.get('is_llm_readable', False),
                     'readability': page.get('readability', 'unavailable'),
                     'update_frequency': {'value': 'unknown', 'basis': 'single observation; Last-Modified is not frequency',
                                          'last_modified': page.get('last_modified'), 'recheck_days': 30},
                     'cross_product_links': direct_links,
                     'question_owner': {'as_is': 'product-team-or-documentation-owner', 'customer_need': 'customer'},
                     'observed_at': page['observed_at'], 'source_sha256': page.get('sha256'),
                     'source_urls': [url]})
    # Every inherited node retains provenance; portal links are locators only.
    # Absence of an alias match never changes product lifecycle or availability.
    for node in nodes:
        cap_id = node['id'].split('/')[0]
        relevant = [m['url'] for m in maps if any(t['node_id'] == cap_id for t in m['taxonomy_matches'])]
        node['portal_locator_urls'] = relevant[:3] if node['level'] != 'Domain' else []
        node['availability'] = 'not-established-by-taxonomy'
        node['lifecycle'] = 'retained' if node['origin'] == 'inherited' else 'added-for-review'
    dump(OUT / 'products.json', {'schema_version': '1.0', 'catalog_version': '2026-10-28.1',
         'status': 'review', 'levels': LEVELS, 'binding_level': 'Atomic Function',
         'contract_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md',
         'source_urls': [baseline['source_url'], RUNTIME],
         'runtime_compatibility': {'analytics-reporting': 'analytics', 'contact-center': 'contact-center',
                                 'voice-ucaas': 'voice-ucaas', 'profiles': ['P-SETTINGS', 'P-NO-SETTINGS', 'P-DEVICE', 'P-API'],
                                 'publication': 'spoke catalog; runtime source was read only'}, 'nodes': nodes})
    (OUT / 'portal-map.jsonl').write_text(''.join(json.dumps(m, ensure_ascii=False, separators=(',', ':')) + '\n' for m in maps))
    # Compact entry point: prompts can select ranges before reading JSONL.
    # Ranges refer to 1-based records, not a further taxonomy level.
    product_ranges = []
    for product in sorted({m['portal_product'] for m in maps}):
        numbers = [i for i, m in enumerate(maps, 1) if m['portal_product'] == product]
        ranges = []
        for number in numbers:
            if ranges and number == ranges[-1][1]+1:
                ranges[-1][1] = number
            else:
                ranges.append([number, number])
        product_ranges.append({'portal_product': product, 'page_count': len(numbers),
                               'record_ranges_1_based': ranges,
                               'entry_url': min(maps[i-1]['url'] for i in numbers)})
    dump(OUT / 'portal-index.json', {
        'map_url': 'https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-399-c3c0e96510d8/docs/taxonomy/portal-map.jsonl',
        'map_sha256': hashlib.sha256((OUT/'portal-map.jsonl').read_bytes()).hexdigest(),
        'usage': 'select product/ranges, then candidate or curated nodes, then exact articles; do not load the entire map into a prompt',
        'products': product_ranges,
        'capabilities': [{'id': c['id'], 'name': c['name'], 'title_url_alias': ALIASES[c['id']],
                          'domain_ids': by_id[c['id']]['parent_ids']} for c in capabilities]})
    summary = {'nodes_by_level': dict(Counter(n['level'] for n in nodes)), 'pages': len(maps),
               'curated_functions': len(additions), 'candidate_pages': sum(bool(m['taxonomy_matches']) for m in maps),
               'unmapped_pages': sum(bool(m['unmapped_reason']) for m in maps),
               'audit_sha256': hashlib.sha256((OUT / 'portal-audit.jsonl').read_bytes()).hexdigest(),
               'http_status': dict(Counter(str(p['http_status']) for p in audit)),
               'readability': dict(Counter(m['readability'] for m in maps)),
               'pages_with_tables': sum(bool(p.get('tables')) for p in audit),
               'pages_with_images': sum(bool(p.get('images')) for p in audit),
               'table_count': sum(len(p.get('tables', [])) for p in audit),
               'image_count': sum(len(p.get('images', [])) for p in audit)}
    dump(OUT / 'coverage.json', summary)
    dump(OUT / 'catalog-diff.json', {
        'baseline_counts': {'Domain': 7, 'Capability': 42, 'Feature': 132, 'Atomic Function': 98},
        'added_nodes': [{'id': n['id'], 'level': n['level'], 'source_urls': n['source_urls']}
                        for n in nodes if n['origin'] == 'portal-update'],
        'removed_ids': [], 'renamed_legacy_ids': [], 'confirmed_deprecated_ids': [],
        'deprecated_portal_sections': [{'url': m['url'], 'title': m['title'],
                                        'basis': 'explicit obsolete-methods HTML branch; does not deprecate entire capability'}
                                       for m in maps if m['documentation_lifecycle'] == 'deprecated-method'],
        'deprecation_policy': 'archive navigation or missing alias is not product deprecation evidence',
        'hierarchy_changes': 'explicit Feature/Function associations normalize previously flat lists; seven domains and four levels retained',
        'capability_coverage': [{'id': c['id'], 'historical_status': c['mango_status'],
                                 'candidate_pages': sum(any(t['node_id'] == c['id'] for t in m['taxonomy_matches']) for m in maps),
                                 'curated_atomic_additions': sum(a['capability'] == c['id'] for a in additions),
                                 'documentation_status': 'candidate-locators-only; absence does not prove product absence',
                                 'source_urls': sorted({a['url'] for a in additions if a['capability'] == c['id']}) or
                                                [m['url'] for m in maps if any(t['node_id'] == c['id'] for t in m['taxonomy_matches'])][:3]}
                                for c in capabilities]})
    render(nodes, baseline, summary)
    print(json.dumps(summary, ensure_ascii=False))


def render(nodes, baseline, summary):
    prefix = 'https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/issue-399-c3c0e96510d8/docs/taxonomy/'
    lines = ['---', 'status: review', 'version: 0.1', 'updated: 2026-10-28', 'temperature: 0.1', '---', '',
             '# Product Layer Mango: полный каталог четырёх уровней', '',
             'Узлы классификации не утверждают наличие функции в продукте. Исторические статусы и параметры',
             'сохранены; связь исходных плоских списков Feature ↔ Atomic Function — редакционная гипотеза.',
             'Новые операции имеют проверенный локатор страницы/заголовка. Для факта As-Is прочитайте статью.', '',
             f'Контракт: https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md',
             f'Машинный каталог: {prefix}products.json', f'Метод и ограничения: {prefix}README.md', '',
             'Полнота: ' + ', '.join(f'{k}: {v}' for k, v in summary['nodes_by_level'].items()) + '.', '']
    for cap in baseline['capabilities'] + NEW_CAPABILITIES:
        cid = cap['id']
        lines.extend([f"## {cid} — {cap['name']}", '',
                      'Domain: ' + ', '.join(cap['domain_ids'] or ['cross-domain: семь существующих Domain']) + '.',
                      f"Статус источника: {cap['mango_status']}; историческая строка {cap.get('row', 'новая capability')}.",
                      f"Источник: {cap.get('source_url', baseline['source_url'])}", '',
                      '| Feature | Atomic Function / параметры | Источник операции |', '| --- | --- | --- |'])
        for feature in [n for n in nodes if n['level'] == 'Feature' and n['parent_ids'] == [cid]]:
            funcs = [n for n in nodes if n['level'] == 'Atomic Function' and feature['id'] in n['parent_ids']]
            for func in funcs:
                params = ', '.join(func['params']) or 'не заявлены'
                lines.append(f"| {feature['name']} | `{func['id'].rsplit('/',1)[1]}` ({params}) | {func['source_urls'][0]} |")
        lines.append('')
    (OUT / 'product-layer.md').write_text('\n'.join(lines).rstrip() + '\n')


if __name__ == '__main__':
    build()
