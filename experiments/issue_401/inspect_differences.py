"""Print bounded source-linked token diff contexts for manual review, locally."""
import argparse
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path
from compare import tokens

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'docs/taxonomy'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('section', nargs='+')
    p.add_argument('--source', choices=['docs', 'portal399'], default='docs')
    p.add_argument('--limit', type=int, default=12)
    args = p.parse_args()
    reference = {s['id']: s for s in json.loads((BASE/'raw/pdf-sections.json').read_text())}
    data = json.loads((OUT/'cc-source-comparison.json').read_text())
    for row in data['sources'][args.source]['sections']:
        if row['id'] not in args.section:
            continue
        print(row['id'], row['title'], row['source_url'], row['difference_pct'])
        text = []
        for candidate in row['candidate_pages']:
            folder = BASE / ('cache' if args.source == 'docs' else 'cache/portal/cache')
            r = json.loads((folder/(hashlib.sha256(candidate['url'].encode()).hexdigest()+'.json')).read_text())
            text.append(r['text'])
            print(candidate['url'])
        a,b = tokens(reference[row['id']]['text']),tokens('\n'.join(text))
        changes = [o for o in SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if o[0] != 'equal']
        for op,i,j,k,l in sorted(changes,key=lambda o:-(o[2]-o[1]+o[4]-o[3]))[:args.limit]:
            print(op, 'PDF:', ' '.join(a[max(0,i-4):min(j+4,i+65)]), '\n WEB:', ' '.join(b[max(0,k-4):min(l+4,k+65)]))


if __name__ == '__main__':
    main()
