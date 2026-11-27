"""Resolve merge conflicts keeping both sides; order chosen per file."""
import re, sys
path, order = sys.argv[1], sys.argv[2]  # order: 'theirs-first' or 'ours-first'
text = open(path, encoding='utf-8').read()
pat = re.compile(r'^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n', re.S | re.M)
def rep(m):
    ours, theirs = m.group(1), m.group(2)
    a, b = (theirs, ours) if order == 'theirs-first' else (ours, theirs)
    return a.rstrip('\n') + '\n\n' + b
open(path, 'w', encoding='utf-8').write(pat.sub(rep, text))
