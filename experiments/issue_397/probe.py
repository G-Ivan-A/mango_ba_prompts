"""Measure pasted prompt revisions, without publishing the task conversation."""
import hashlib
import json
import re
import subprocess

from extract import BASE, answer_text, messages

REVISIONS = ['f27dbd40', '29390d5e', '7d92ec41', '1148a690']


def body(text):
    text = text.replace('\r\n', '\n').strip()
    text = re.sub(r'^<!-- mango-bcreq-[^>]+-->\s*', '', text)
    if text.startswith('---\n'):
        text = text.split('---\n', 2)[2]
    return text.strip()


def main():
    _, items = messages(BASE / 'raw/chat-export-1131.json')
    revisions = [subprocess.check_output(['git', 'rev-parse', rev], text=True).strip()
                 for rev in REVISIONS]
    rows = []
    for n in [1, 5, 15, 77]:
        message, _ = items[n-1]
        content = answer_text(message)
        marker = re.search(r'<!-- mango-(bcreq-[^>]+) -->', content)
        name = marker[1] + '.md'
        observed = body(content)
        matches = []
        for revision in revisions:
            old = subprocess.check_output(['git', 'show', f'{revision}:prompts/{name}'], text=True)
            if observed == body(old):
                matches.append(revision)
        rows.append({'turn': n, 'message_id': message['id'], 'file': name,
                     'normalized_chars': len(observed),
                     'normalized_sha256': hashlib.sha256(observed.encode()).hexdigest(),
                     'has_issue_395_fallback': '<!-- issue-395: runtime-fallback -->' in observed,
                     'exact_body_matches': matches})
    result = {'method': 'Strip copy marker/frontmatter/outer whitespace; normalize CRLF only. '
                        'Compare full bodies at four revisions; not a deployment reconstruction.',
              'sampled_revisions': revisions, 'pasted_prompts': rows}
    (BASE / 'prompt-probe.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
