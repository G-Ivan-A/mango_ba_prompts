"""Filter issue 397 exports before reading; never publish entire conversations.

Usage: python3 experiments/issue_397/extract.py
Raw attachments belong in raw/ (see README); generated turns/ is ignored.
No model calls, third-party dependencies, or network access.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
TOPICS = re.compile(
    r"AGENTS|контракт|критич|возраж|фактор|подтвержд|сокращ|оптимиз|"
    r"деграда|утра[тч]|потер|наслед|golden|эталон|гейт|circuit|"
    r"правил|режим|микроменедж|упрощ|1131|конституц|SSOT|доказ|"
    r"качество|токен|согласован|промпт|БЗ|хаб|hub|runtime",
    re.I,
)


def answer_text(message):
    """Read published answers, not the export's reasoning summaries or metadata."""
    if message.get('content'):
        return message['content']
    return '\n\n'.join(
        block['content'] for block in (message.get('content_list') or [])
        if block.get('phase') == 'answer' and isinstance(block.get('content'), str)
        and block['content']
    )


def messages(path):
    """Use visible message order; retain history-only variants as separate evidence."""
    data = json.loads(path.read_text())[0]
    visible = data['chat']['messages']
    ids = {m['id'] for m in visible}
    extra = [m for m in data['chat']['history']['messages'].values() if m['id'] not in ids]
    return data['title'], [(m, True) for m in visible] + [(m, False) for m in extra]


def extract():
    out = BASE / 'turns'
    out.mkdir(exist_ok=True)
    manifest = {}
    for source in ('split', '1131'):
        path = BASE / 'raw' / f'chat-export-{source}.json'
        title, items = messages(path)
        counts = {'visible': 0, 'history_only': 0, 'selected': 0}
        index = []
        for number, (m, visible) in enumerate(items, 1):
            counts['visible' if visible else 'history_only'] += 1
            content = answer_text(m)
            if not isinstance(content, str):
                raise ValueError(f"Unsupported content for {m['id']}")
            stamp = datetime.fromtimestamp(m.get('timestamp') or 0, timezone.utc).isoformat()
            role = m.get('role')
            relevant = bool(TOPICS.search(content))
            selected = source == '1131' or (relevant and stamp >= '2026-08-01')
            row = {'n': number, 'id': m['id'], 'role': role, 'utc': stamp,
                   'visible': visible, 'chars': len(content), 'selected': selected}
            # The compact index prioritises Founder dialogue; full selected turns
            # are separate files, so no accidental 20 MB transcript in a read call.
            if role == 'user':
                row['preview'] = re.sub(r'\s+', ' ', content)[:650]
            index.append(row)
            if selected:
                counts['selected'] += 1
                (out / f'{source}-{number:04d}.txt').write_text(
                    f"# {source} {number} | {role} | {stamp}\n"
                    f"ID: {m['id']} | visible: {visible}\n\n{content}\n")
        (out / f'{source}-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
        manifest[source] = {'title': title, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                            'bytes': path.stat().st_size, **counts}
    (out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    extract()
