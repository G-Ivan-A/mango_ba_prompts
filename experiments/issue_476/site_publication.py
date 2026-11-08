"""Add current A-IN guidance from section standards using the existing site overlays."""
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REPO = 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/'


def apply(src):
    for number, name in ((1,'01-glossary.md'),(2,'02-business-context.md')):
        path=ROOT/'standards/bcreq-sections'/name
        note=re.search(r'^> \*\*Действующий порядок A-IN.*(?:\n>.*)*',path.read_text(),re.M).group()
        note=' '.join(line.removeprefix('> ') for line in note.splitlines()).replace('**','').replace('`','')
        parts=[]; cursor=0
        for link in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',note):
            parts.append(html.escape(note[cursor:link.start()]))
            target=(path.parent/link[2]).resolve().relative_to(ROOT).as_posix()
            parts.append(f'<a href="{REPO}{target}" target="_blank" rel="noreferrer">{html.escape(link[1])}</a>')
            cursor=link.end()
        parts.append(html.escape(note[cursor:]))
        anchor=f'<h2 id="standard-title-{number}">'
        end=src.index('</div></div>',src.index(anchor))+len('</div></div>')
        src=src[:end]+'<p class="standard-summary" data-ain-guidance="'+str(number)+'">'+''.join(parts)+'</p>'+src[end:]
    return re.sub(r'(· каталог: 39 классов BCREQ, архив:) [^<\n]+',
                  r'\1 14 промптов этапа 1 и 4 редакции 2.7.0', src)
