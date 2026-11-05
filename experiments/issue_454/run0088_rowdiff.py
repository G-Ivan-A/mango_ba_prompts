#!/usr/bin/env python3
"""RUN-0088: compare 8.4 and 8.5 rows of a step with the previous document. Usage: run0088_rowdiff.py PREV LABEL."""
import json,re,sys,subprocess
prev,lab=sys.argv[1],sys.argv[2]
new=open(f'runs/2026/RUN-0088/outputs/steps/{lab}/blocks.md',encoding='utf-8').read()
blocks=dict(re.findall(r'<!-- block:(\S+) -->\n(.*?)\n<!-- /block -->',new,re.S))
def rows(t): 
    d={}
    for l in t.split('\n'):
        m=re.match(r'\|\s*([ВД]-\d+)\s*\|',l)
        if m: d[m.group(1)]=l
    return d
old=open(f'runs/2026/RUN-0088/outputs/document/after-{prev}.md',encoding='utf-8').read()
O=rows(old)
for k in ('8.4','8.5'):
    if k not in blocks: print(k,'unchanged'); continue
    N=rows(blocks[k]); pre='В-' if k=='8.4' else 'Д-'
    o={a:b for a,b in O.items() if a.startswith(pre)}
    print(k,'old',len(o),'new',len(N),'added',len(set(N)-set(o)),'lost',sorted(set(o)-set(N)),'changed',len([a for a in o if a in N and N[a]!=o[a]]))
    for a in [a for a in o if a in N and N[a]!=o[a]][:12]:
        print('  ',a,'\n   -',o[a][:200],'\n   +',N[a][:200])
print('blocks',list(blocks), 'size',len(old))
