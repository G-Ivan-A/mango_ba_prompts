import json
ref=json.load(open('kb/industry/reference-taxonomy.json'))
gold={g['n']:g for g in json.load(open('experiments/issue-176-convergence/gold.json'))}
pred={p['n']:p for p in json.load(open('experiments/issue-176-convergence/ai-predictions.json'))}

valid_paths=set()
def walk_node(roots):
    for dom in roots:
        dpath=(dom['id'],); valid_paths.add(dpath)
        for cap in dom.get('capabilities',[]):
            cpath=dpath+(cap['id'],); valid_paths.add(cpath)
            for feat in cap.get('features',[]):
                fpath=cpath+(feat['id'],); valid_paths.add(fpath)
                for fn in feat.get('functions',[]):
                    valid_paths.add(fpath+(fn['id'],))
walk_node(ref['domains'])
walk_node(ref['cross_domain_layers'])

def gold_primary(g):
    for a in g['gold_alignment']:
        if a['alignment_type']=='primary': return a
    return g['gold_alignment'][0]
def path_of(d):
    out=[]
    for k in ['domain','capability','feature','function']:
        v=d.get(k)
        if v: out.append(v)
        else: break
    return tuple(out)

levels=['domain','capability','feature','function']
counts={l:[0,0] for l in levels}
exact=0; prefix=0; resolves=0; align_ok=0; deeper=0
rows=[]
for n in range(1,28):
    g=gold[n]; p=pred[n]; ga=gold_primary(g); gref=ga['industry_ref']
    for l in levels:
        gv=gref.get(l)
        if gv is not None:
            counts[l][1]+=1
            if p.get(l)==gv: counts[l][0]+=1
    gp=path_of(gref); pp=path_of(p)
    exact_ok = gp==pp
    # prefix: AI agrees on every level gold defines (AI may go deeper)
    prefix_ok = len(pp)>=len(gp) and pp[:len(gp)]==gp
    res = pp in valid_paths
    a_ok = p['alignment_type']==ga['alignment_type']
    is_deeper = prefix_ok and len(pp)>len(gp)
    if exact_ok: exact+=1
    if prefix_ok: prefix+=1
    if res: resolves+=1
    if a_ok: align_ok+=1
    if is_deeper: deeper+=1
    rows.append(dict(n=n,id=g['id'],level=g['level'],gold='/'.join(gp),ai='/'.join(pp),
                     exact=exact_ok,prefix=prefix_ok,resolves=res,deeper=is_deeper))

print("PER-LEVEL (where gold defines level):")
for l in levels:
    c,t=counts[l]; print(f"  {l:11}: {c}/{t} = {100*c/t:.0f}%")
print(f"\nExact full-path match : {exact}/27 = {100*exact/27:.0f}%")
print(f"Prefix match (agree on all gold levels, AI may go deeper): {prefix}/27 = {100*prefix/27:.0f}%")
print(f"  of which AI went strictly deeper than gold: {deeper}")
print(f"AI node resolves in reference taxonomy: {resolves}/27 = {100*resolves/27:.0f}%")
print(f"Alignment-type match: {align_ok}/27 = {100*align_ok/27:.0f}%")
print("\nMISMATCHES (prefix-level domain/capability disagreements):")
for r in rows:
    if not r['prefix']:
        print(f"  #{r['n']:2} {r['id']} ({r['level']}): gold={r['gold']}  ai={r['ai']}")
print("\nDEEPER-THAN-GOLD (AI correct but added unverified deeper levels):")
for r in rows:
    if r['deeper']:
        flag='' if r['resolves'] else '  <-- AI leaf NOT in reference taxonomy'
        print(f"  #{r['n']:2} {r['id']}: gold={r['gold']}  ai={r['ai']}{flag}")
json.dump(rows,open('experiments/issue-176-convergence/scored.json','w'),ensure_ascii=False,indent=2)
