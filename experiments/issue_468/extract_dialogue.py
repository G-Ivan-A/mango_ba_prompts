#!/usr/bin/env python3
"""Compare exported visible dialogue, without publishing source or reasoning.

Raw inputs and extracted text belong in the ignored private/ directory. The
report contains hashes, counts and array locators only. No model calls.
"""
import argparse
import hashlib
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def visible(message):
    if message['role'] == 'assistant':
        # Never fall back to content: it may contain hidden reasoning.
        return '\n'.join(part['content'] for part in message.get('content_list', [])
                         if part.get('phase') == 'answer')
    if message['role'] != 'user':
        raise ValueError('Unexpected role in active dialogue')
    return message['content']


def load_export(path):
    raw = path.read_bytes()
    exported = json.loads(raw)
    if not isinstance(exported, list) or len(exported) != 1:
        raise ValueError('Expected exactly one exported conversation')
    chat = exported[0]['chat']
    messages = chat['messages']
    ids = [m['id'] for m in messages]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Empty dialogue or duplicate active message IDs')
    for i, message in enumerate(messages):
        if message.get('parentId') != (ids[i - 1] if i else None):
            raise ValueError('Active messages are not an ordered parent chain')
    if chat['history']['currentId'] != ids[-1]:
        raise ValueError('Active branch does not end at history.currentId')
    history = chat['history']['messages']
    if not set(ids) <= set(history):
        raise ValueError('Active messages missing from history')
    return {
        'sha256': digest(raw),
        'messages': messages,
        'history_count': len(history),
        'inactive_history_count': len(set(history) - set(ids)),
        'texts': [visible(m) for m in messages],
    }


def compare(before, after):
    old = {m['id']: (i, m['role'], before['texts'][i])
           for i, m in enumerate(before['messages'])}
    unchanged, added, changed, moved = [], [], [], []
    for i, message in enumerate(after['messages']):
        previous = old.get(message['id'])
        if previous is None:
            added.append(i)
        elif previous[1:] != (message['role'], after['texts'][i]):
            changed.append({'before': previous[0], 'after': i})
        else:
            unchanged.append(i)
        if previous is not None and previous[0] != i:
            moved.append({'before': previous[0], 'after': i})
    current = {m['id'] for m in after['messages']}
    removed = [i for i, m in enumerate(before['messages']) if m['id'] not in current]
    prefix = 0
    for i, (a, b) in enumerate(zip(before['messages'], after['messages'])):
        if (a['id'], a['role'], before['texts'][i]) != (b['id'], b['role'], after['texts'][i]):
            break
        prefix += 1
    return {
        'schema_version': 1,
        'selection': 'chat.messages ordered parent chain; assistant content_list phase=answer only',
        'sources': {
            name: {**{k: data[k] for k in ('sha256', 'history_count', 'inactive_history_count')},
                   'active_count': len(data['messages']),
                   'empty_visible_indices': [i for i, text in enumerate(data['texts']) if not text]}
            for name, data in (('before', before), ('after', after))
        },
        'common_visible_prefix': prefix,
        'unchanged_indices': unchanged,
        'added_indices': added,
        'changed_indices': changed,
        'removed_indices': removed,
        'moved_indices': moved,
        'delta': [
            {'index': i, 'role': after['messages'][i]['role'],
             'visible_sha256': digest(after['texts'][i].encode()),
             'characters': len(after['texts'][i])}
            for i in sorted(added + [x['after'] for x in changed])
        ],
        'raw_committed': False,
        'limitations': [
            'Visible text equality does not verify attachments or tool execution.',
            'Inactive history and hidden reasoning are excluded from practice evidence.',
            'Reported retrieval and assistant self-correction are claims, not product verification.',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    args = parser.parse_args()
    private_root = Path(__file__).resolve().parent / 'private'
    if not args.private_output.resolve().is_relative_to(private_root):
        parser.error('--private-output must stay inside the ignored issue_468/private directory')
    if args.report.resolve().is_relative_to(args.private_output.resolve()):
        parser.error('--report must be separate from the private extraction directory')
    before, after = load_export(args.before), load_export(args.after)
    report = compare(before, after)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    args.private_output.mkdir(parents=True, exist_ok=True)
    for entry in report['delta']:
        i = entry['index']
        (args.private_output / f'{i:02}-{entry["role"]}.md').write_text(after['texts'][i] + '\n')
    print(f"Visible prefix: {report['common_visible_prefix']}; "
          f"added: {len(report['added_indices'])}; changed: {len(report['changed_indices'])}; "
          f"removed: {len(report['removed_indices'])}; moved: {len(report['moved_indices'])}")


if __name__ == '__main__':
    main()
