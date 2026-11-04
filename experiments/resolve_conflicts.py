import re,sys
for f,mode in [("CHANGELOG.md","both"),("docs/rfc/rfc-register.md","both"),("pr-ops/BACKLOG.md","theirs"),("pr-ops/backlog-ba-model.md","theirs")]:
    s=open(f).read()
    def r(m):
        o,t=m.group(1),m.group(2)
        if o.startswith("updated:") or mode=="theirs": return t
        return t+"\n"+o if f=="CHANGELOG.md" else o+t
    s=re.sub(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> upstream/main\n",r,s,flags=re.S)
    open(f,"w").write(s)
