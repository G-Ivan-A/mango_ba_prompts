"""Check that every «КС К-NN: «quote»» in a standards file is present
verbatim in the class file of К-NN (standards/bcreq-manual-classes/NN-slug.md)."""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
cat = json.loads((root/'standards/bcreq-manual-classes/catalog.json').read_text(encoding='utf-8'))
files = {}
for c in cat['classes']:
    n = c['id'].split('-')[1]
    files[c['id']] = (root/'standards/bcreq-manual-classes'/f"{n}-{c['slug']}.md").read_text(encoding='utf-8')
text = (root/sys.argv[1]).read_text(encoding='utf-8')
bad = 0; total = 0
for m in re.finditer(r'КС (К-\d\d): «([^»]+)»', text):
    total += 1
    k, q = m.group(1), m.group(2)
    norm = lambda s: re.sub(r'\s+', ' ', s)
    if norm(q) not in norm(files[k]):
        bad += 1
        print('MISSING', k, q)
print('total', total, 'missing', bad)
