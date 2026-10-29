"""Extract the explicitly attached PDF locally; publish hashes and locators only.

Requires PyMuPDF 1.28.2. No network, images are counted but never exported.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'
PDF_URL = 'https://github.com/user-attachments/files/34130556/CC_manual_1.26.42_compressed.pdf'


def extract(path):
    import pymupdf
    doc = pymupdf.open(path)
    toc_text = '\n'.join(doc[i].get_text() for i in range(1, 8))
    toc = [{'id': m[0].rstrip('.'), 'title': re.sub(r'\s+', ' ', m[1]).strip(), 'page': int(m[2])}
           for m in re.findall(r'(?m)^\s*(\d+(?:\.\d+)*\.)\s*\n?([^\n]+?)\.{2,}\s*(\d+)\s*$', toc_text)]
    sections, pages = [], []
    current = None
    for i, page in enumerate(doc):
        raw_text = page.get_text()
        pages.append({'page': i+1, 'source_url': PDF_URL + f'#page={i+1}',
                      'text_chars': len(raw_text), 'text_sha256': hashlib.sha256(raw_text.encode()).hexdigest(),
                      'images': len(page.get_images()), 'is_front_matter': i < 8})
        if i < 8:
            continue
        heading_continuation = False
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                spans = line['spans']
                text = ''.join(s['text'] for s in spans).strip()
                if not text:
                    continue
                # Page numbers are Calibri in a fixed header band.
                if text == str(i+1) and all(s['font'] == 'Calibri' for s in spans):
                    continue
                is_heading = any('Cambria' in s['font'] and 'Bold' in s['font'] for s in spans)
                match = re.match(r'^(\d+(?:\.\d+)*\.)\s+(.+)', text) if is_heading else None
                if match:
                    current = {'id': match[1].rstrip('.'), 'title': match[2],
                               'page_start': i+1, 'page_end': i+1, 'text': '',
                               'source_url': PDF_URL + f'#page={i+1}'}
                    sections.append(current)
                    heading_continuation = True
                elif heading_continuation and is_heading:
                    current['title'] += ' ' + text
                elif current:
                    current['text'] += text + '\n'
                    current['page_end'] = i+1
                    heading_continuation = False
    identifiers = [s['id'] for s in sections]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError('Duplicate PDF section identifiers')
    missing = [s for s in toc if s['id'] not in identifiers]
    if missing:
        raise ValueError('TOC sections not extracted: ' + str(missing))
    manifest = {'source_url': PDF_URL, 'issue_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/issues/401',
                'version': '1.26.42', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'bytes': path.stat().st_size, 'pages': len(doc), 'metadata': doc.metadata,
                'extractor': f'PyMuPDF {pymupdf.VersionBind}', 'outline_entries': len(doc.get_toc()),
                'section_method': 'Cambria Bold numbered headings; wrapped title lines joined; all TOC IDs verified',
                'toc': toc, 'sections': [{k:v for k,v in s.items() if k != 'text'} | {
                    'text_chars': len(s['text']), 'text_sha256': hashlib.sha256(s['text'].encode()).hexdigest()}
                    for s in sections], 'page_extraction': pages,
                'scope': 'All 590 pages extracted locally; cover and TOC excluded from prose comparison; image text not OCRed.'}
    (BASE / 'raw/pdf-sections.json').write_text(json.dumps(sections, ensure_ascii=False))
    (OUT / 'cc-pdf-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'pages': len(doc), 'sections': len(sections), 'toc_entries': len(toc),
                      'text_chars': sum(len(s['text']) for s in sections),
                      'empty_sections': [s['id'] for s in sections if not s['text'].strip()]}, ensure_ascii=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf', type=Path)
    extract(p.parse_args().pdf)
