import re,json,sys
from pathlib import Path
REPO=Path('/tmp/gh-issue-solver-1793863999837/experiments/issue_454/run0089')
J=Path('/tmp/run88/judge')
text=(REPO/'judge-instruction.md').read_text(encoding='utf-8')
blocks=re.findall(r'```text\n(.*?)```',text,re.S)
doc,proc,part=blocks
crit={m.group(1):m.group(0).strip() for m in re.finditer(r'(?m)^(P\d\d) .*$',proc)}
SC=str(REPO/'ba-script.md'); MAT=str(REPO/'customer-materials.md'); RT='/tmp/rt454'
PIECES={"core":("P01","P02","P03","P04","P05","P06","P08","P09","P10","P13","P14"),
"work":("P01","P02","P04","P05","P06","P07","P08","P09","P10","P13","P14"),
"end":("P02","P05","P08","P11","P12","P13","P14","P15","P16")}
DESC={"core":"steps Ш-3, Ш-4, Ш-5 up to gate Г-С1, the return from that gate after \"уточнение\", and Ш-3, Ш-4, Ш-5 passed again, with the executor log of this part",
"work":"steps Ш-6, Ш-7, Ш-8, Ш-9 after the customer's approval at gate Г-С1, with the executor log of this part; the document assembly and journal files are not in this part",
"end":"a new chat for Ш-В, a new chat for Ш-Р, a new chat for Ш-С, the executor logs of these chats, and the gate journal of the whole run"}
for label in 'XY':
    for piece,codes in PIECES.items():
        b=part
        for k,v in {'{PART}':str(J/f'{label}-{piece}.md'),'{SCRIPT}':SC,'{MATERIALS}':MAT,'{RUNTIME}':RT,'{OUTPUT}':str(J/f'p-{label}-{piece}.json'),'{PART_DESCRIPTION}':DESC[piece],'{CRITERIA}':', '.join(codes),'{CRITERIA_TEXT}':'\n'.join(crit[c] for c in codes)}.items():
            b=b.replace(k,v)
        (J/'prompts'/f'{label}-{piece}.txt').write_text(b,encoding='utf-8')
b=part
for k,v in {'{PART}':str(J/'common.md'),'{SCRIPT}':SC,'{MATERIALS}':MAT,'{RUNTIME}':RT,'{OUTPUT}':str(J/'p-common.json'),'{PART_DESCRIPTION}':'the shared first stage (Ш-0, Ш-1, Ш-2)','{CRITERIA}':'P00','{CRITERIA_TEXT}':crit['P00']}.items():
    b=b.replace(k,v)
(J/'prompts'/'common.txt').write_text(b,encoding='utf-8')
b=doc
for k,v in {'{X}':str(J/'X-document.md'),'{Y}':str(J/'Y-document.md'),'{CHECKLISTS}':'/tmp/run88/checklists.md','{MATERIALS}':MAT,'{RUNTIME}':RT,'{OUTPUT}':str(J/'document.json')}.items():
    b=b.replace(k,v)
b=b.replace('Reply with one line','Then answer: "overall": "X" | "Y" | "tie": which document a BA could take to release with fewer corrections, and why (two sentences). Add the keys "overall" and "overall_reason" to the JSON.\n\nReply with one line')
(J/'prompts'/'document.txt').write_text(b,encoding='utf-8')
print(sorted(p.name for p in (J/'prompts').iterdir()))
