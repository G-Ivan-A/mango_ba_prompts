"""Verify all curated citations against the original, private local attachments."""
from datetime import datetime, timezone
import hashlib
import json

from extract import BASE, answer_text, messages


def verify():
    evidence = json.loads((BASE / 'evidence.json').read_text())
    checked = 0
    for chat, source in evidence['exports'].items():
        path = BASE / 'raw' / f'chat-export-{chat}.json'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], chat
        assert path.stat().st_size == source['bytes'], chat
        _, items = messages(path)
        assert sum(visible for _, visible in items) == source['visible_messages'], chat
        assert sum(not visible for _, visible in items) == source['history_only_messages'], chat
        for row in evidence['entries']:
            if row['chat'] != chat:
                continue
            message, visible = items[row['turn'] - 1]
            text = answer_text(message)
            assert message['id'] == row['message_id'], row['key']
            assert message['role'] == row['role'] and visible == row['visible'], row['key']
            assert datetime.fromtimestamp(message['timestamp'], timezone.utc).isoformat() == row['utc'], row['key']
            assert hashlib.sha256(text.encode()).hexdigest() == row['answer_sha256'], row['key']
            for quote in row['quotes']:
                assert quote and quote in text, row['key']
                checked += 1
    print(f'PASS: {len(evidence["exports"])} export hashes; '
          f'{len(evidence["entries"])} message IDs/roles/answer hashes; {checked} exact quotes')


if __name__ == '__main__':
    verify()
