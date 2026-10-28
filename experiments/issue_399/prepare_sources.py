"""Normalize locally supplied source snapshots; never publish the raw chat.

Input filenames and immutable URLs are documented in docs/taxonomy/README.md.
The chat adapter is shared with issue 397 (published answers, separate history).
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
HUB = 'https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/cd5d6e4b72700e43ccca6c96119308ab5a6d7379/research/mango/2026-05-22-classification.md'
CHAT = 'https://github.com/user-attachments/files/34090086/chat-export-1131.json'
PATTERNS = {
    'scope-by-source': {'turns': [53, 55, 56, 58, 61, 62, 63], 'control': 'preserve requested clients and distinguish public API from internal behavior'},
    'wrong-knowledge-owner': {'turns': [57, 63, 73], 'control': 'route undocumented As-Is semantics to product/development; ask customer about desired outcome'},
    'cross-product-omission': {'turns': [8, 12, 14, 53, 55, 65, 73], 'control': 'include WFM, clients, permissions, session and connector candidates'},
    'connector-substitution': {'turns': [65, 66, 67, 68, 69, 70, 72], 'control': 'connector identity and exact source entailment are mandatory'},
    'coverage-without-receipt': {'turns': [58, 68, 70, 72], 'control': 'record actual URLs, scope, missing evidence and confidence; page count is not semantic coverage'},
}


def baseline():
    path = BASE/'classification.source.txt'
    text = path.read_text()
    product = text.split('## 📊 Product Layer\n', 1)[1].split('## 🛒 Commercial Layer', 1)[0]
    domains, caps, current = [], [], []
    for line in product.splitlines():
        if match := re.match(r'### 📦 Domain: (\S+)', line):
            current = [match[1]]
            domains.append({'id': match[1], 'name': ''})
        elif line.startswith('**Name**:') and domains:
            domains[-1]['name'] = line.split(':', 1)[1].strip()
        elif line.startswith('### 🧩'):
            current = []
        elif match := re.match(r'#### 🔹 Capability: (\S+) \((.*?)\)', line):
            caps.append({'id': match[1], 'name': match[2], 'domain_ids': current.copy(),
                         'features': [], 'atomic_functions': []})
        elif line.startswith('- **Features**:'):
            caps[-1]['features'] = [s.strip() for s in line.split(':', 1)[1].split(',')]
        elif match := re.match(r'  - `([^`]+)` \(params: (.*?)\)', line):
            caps[-1]['atomic_functions'].append({'id': match[1], 'params': match[2].split(', ')})
        elif line.startswith('- **related_commercial_fields**:'):
            caps[-1]['related_commercial_fields'] = line.split(':', 1)[1].strip().split(', ')
        elif match := re.match(r'- \*\*Mango status\*\*: (.*?) · \*\*row\*\*: (\d+)', line):
            caps[-1].update(mango_status=match[1], row=int(match[2]))
    assert (len(domains), len(caps), sum(len(c['features']) for c in caps),
            sum(len(c['atomic_functions']) for c in caps)) == (7, 42, 132, 98)
    result = {'source_url': HUB, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'domains': domains, 'capabilities': caps}
    (BASE/'baseline.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')


def forensic():
    spec = importlib.util.spec_from_file_location('extract_397', BASE.parent/'issue_397/extract.py')
    extract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extract)
    path = BASE/'chat-export-1131.source.json'
    _, items = extract.messages(path)
    selected = {n for p in PATTERNS.values() for n in p['turns']}
    evidence = []
    for number, (message, visible) in enumerate(items, 1):
        content = extract.answer_text(message)
        if number in selected:
            evidence.append({'turn': number, 'message_id': message['id'], 'role': message['role'],
                             'visible': visible, 'chars': len(content),
                             'answer_sha256': hashlib.sha256(content.encode()).hexdigest()})
    output = {'source_url': CHAT, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'visible_messages': sum(v for _, v in items), 'history_only_messages': sum(not v for _, v in items),
              'extraction': 'published answer only; visible order first; history-only messages kept separate',
              'privacy': 'no raw transcript, customer brief, names or reasoning content',
              'patterns': PATTERNS, 'evidence': evidence,
              'step1_url': 'https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md'}
    out = BASE.parents[1]/'docs/taxonomy'
    out.mkdir(exist_ok=True)
    (out/'forensic-evidence.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    baseline()
    forensic()
