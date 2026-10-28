"""Rebuild six-area inspection and short routing receipts from public metadata.

Semantic probes check explicit row/column associations, including a conditional
API field. Visual semantics remain unknown; no image download or LLM call.
"""
from collections import Counter
import json
from pathlib import Path

from route import select_pages

OUT = Path(__file__).resolve().parents[2]/'docs/taxonomy'
P = 'https://www.mango-office.ru/support/'
SPEECH = P+'3_produkty-i-prilozheniya/8_rechevaya-analitika-i-skoring/1_rechevaya-analitika/4_integratsiya_i_nastroiki/'
API = P+'5_api-i-razrabotka/1_api-mango-office/6_opisanie_metodov_api_kontakt_tsentra_mango/2_4_upravlenie_statusami_i_sessiyami/1_4_1_statusy/4_4_1_2_smena_statusa_polzovatelya/'
CASES = [
    ('products-applications', '3_produkty-i-prilozheniya', P+'3_produkty-i-prilozheniya/12_konstruktor-otchetov/1_otchety/dobavlenie_otcheta/'),
    ('integrations', '4_integratsii', P+'4_integratsii/1_vse-integratsii/5_bpm-soft/2_dopolnitelnye_nastroyki_integratsii/4_4_dopolnitelnye_nastroyki_integratsii/7_ispolzovat_statusy_kontakt_tsentra/statusy_kontakt_tsentra_v_interfeyse_bpmsoft/'),
    ('api-development', '5_api-i-razrabotka', API),
    ('administration', '6_administrirovanie', P+'6_administrirovanie/1_roli-i-prava/1_rolevaya-model-vats/4_nastroyka_prav_dostupa_roli/'),
    ('contact-center', '3_kontakt-tsentr', P+'3_produkty-i-prilozheniya/3_kontakt-tsentr/11_plan_raboty/8_3_otchety/'),
    ('speech-analytics', '8_rechevaya-analitika-i-skoring', SPEECH),
]


def main():
    rows = [json.loads(s) for s in (OUT/'portal-audit.jsonl').read_text().splitlines()]
    pages = {r['url']: r for r in rows}
    cases = []
    for name, branch, url in CASES:
        page = pages[url]
        assert page['http_status'] == 200 and page['body_found'], url
        group = [r for r in rows if '/'+branch+'/' in r['url']]
        cases.append({'area': name, 'source_url': url, 'title': page['title'],
                      'source_sha256': page['sha256'], 'observed_at': page['observed_at'],
                      'branch_pages': len(group), 'branch_http_status': dict(Counter(str(r['http_status']) for r in group)),
                      'article_text_chars': page['text_chars'], 'table_count': len(page['tables']),
                      'image_count': len(page['images']), 'inline_svg_canvas_or_mermaid': page['inline_diagrams'],
                      'readability': page['readability'], 'static_article_extracted': True,
                      'visual_semantics': 'not-inspected; only HTML metadata; do not infer UI/diagram behavior'})
    # The first matrix has three data columns. The third is SIP Trunk, and
    # identity attribution differs from transcription in that column.
    matrix = pages[SPEECH]['tables'][0]['sample_rows']
    assert matrix[0][-1] == 'SIP Trunk'
    assert 'Транскрибация' in matrix[1][0] and matrix[1][-1] == 'Да'
    assert 'Привязка к личности' in matrix[2][0] and matrix[2][-1] == 'Нет'
    table = pages[API]['tables'][0]['sample_rows']
    status = next(r for r in table if len(r)>1 and r[1] == 'status')
    assert status[3] == 'Да' and 'при отсутствии поля status_alias' in status[4]
    probes = [
        {'source_url': SPEECH, 'question': 'Does the SIP Trunk column distinguish transcription from employee attribution?',
         'row_column_result': {'transcription': True, 'employee_attribution': False},
         'result': 'pass: separate row/column values preserved; not an assertion about all routing paths'},
        {'source_url': API, 'question': 'Can required=Да for status be interpreted without the description cell?',
         'row_column_result': {'required_cell': 'Да', 'condition': 'required if status_alias is absent'},
         'result': 'pass: conditional description retained; required cell alone is insufficient'},
        {'source_url': cases[4]['source_url'], 'question': 'Can all WFM report image semantics be recovered from HTML metadata?',
         'result': 'not-established: no visual content downloaded; targeted fallback/verified description required'},
    ]
    result = {'method': 'structural extraction plus manually specified semantic cell probes; no LLM accuracy evaluation',
              'areas': cases, 'probes': probes,
              'inline_visual_caveat': 'SVG/canvas/mermaid presence is conservative; may include decorative controls',
              'connector_comparison': {
                  'bpmsoft_source': cases[1]['source_url'],
                  'amocrm_source': P+'4_integratsii/1_vse-integratsii/3_amocrm/14_integratsiya_s_kontakt_tsentrom_mango_office/14_1_uchet_kampaniy_ishodyaschego_obzvona_v_amocrm/',
                  'conclusion': 'different connector and documented operation; no transfer of BPMSoft status claims and no negative amoCRM capability inference'}}
    (OUT/'readability-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    mapping = [json.loads(s) for s in (OUT/'portal-map.jsonl').read_text().splitlines()]
    receipts = []
    for query in ('WFM статус API amoCRM', 'статус API BPMSoft', 'SIP Trunk речевая аналитика'):
        plan = select_pages(mapping, query)
        receipts.append({k: v for k, v in plan.items() if k != 'pages'} | {
            'pages': [{k: row.get(k) for k in ('url', 'title', 'portal_product', 'connector_id', 'readability', 'routing_score', 'next_action')}
                      for row in plan['pages']]})
    (OUT/'routing-examples.json').write_text(json.dumps(receipts, ensure_ascii=False, indent=2)+'\n')
    print('Verified six areas, two table cell probes; recorded three routing receipts.')


if __name__ == '__main__':
    main()
