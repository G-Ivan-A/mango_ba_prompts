"""Rebuild Gate 0 evidence from pinned Git objects, without network access.

Usage: python3 experiments/issue_407/inventory.py [--check]
No active documents or historical artifacts are modified by this script.
"""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
SHA = re.compile(r'[0-9a-f]{40}')


def parse_tree(raw):
    if raw and not raw.endswith(b'\0'):
        raise ValueError('Incomplete NUL-delimited Git tree')
    rows = []
    for record in raw.split(b'\0'):
        if not record:
            continue
        metadata, path = record.split(b'\t', 1)
        mode, kind, sha, size = metadata.decode('ascii').split()
        if kind != 'blob' or not SHA.fullmatch(sha):
            raise ValueError('Unsupported Git entry; inspect before claiming full coverage')
        rows.append(dict(path=path.decode('utf-8'), mode=mode,
                         blob_sha=sha, bytes=int(size)))
    return rows


def validate_sources(baseline, hub):
    for key in ('target', 'hub'):
        source = baseline[key]
        if not SHA.fullmatch(source['commit_sha']) or not SHA.fullmatch(source['tree_sha']):
            raise ValueError('Source baseline requires full immutable Git SHAs')
        if not source['repository_url'].startswith('https://github.com/'):
            raise ValueError('Source requires an absolute repository URL')
    if hub.get('truncated') is not False or hub['sha'] != baseline['hub']['tree_sha']:
        raise ValueError('Hub tree is truncated or does not match pinned source')
    paths = [entry['path'] for entry in hub['tree']]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate paths in Hub tree')
    # Verify every tree object, not just the API's truncated flag and root label.
    # An omitted hidden file or subtree must invalidate the captured baseline.
    directories = {'': []}
    for entry in hub['tree']:
        if entry['type'] == 'tree':
            directories[entry['path']] = []
    for entry in hub['tree']:
        parent = str(PurePosixPath(entry['path']).parent)
        parent = '' if parent == '.' else parent
        if parent not in directories:
            raise ValueError('Hub tree entry has no parent tree')
        directories[parent].append(entry)
    expected = {entry['path']: entry['sha'] for entry in hub['tree']
                if entry['type'] == 'tree'}
    expected[''] = hub['sha']
    for path, entries in directories.items():
        def order(entry):
            name = PurePosixPath(entry['path']).name
            return (name + ('/' if entry['type'] == 'tree' else '')).encode()
        data = b''.join(entry['mode'].lstrip('0').encode() + b' '
                        + PurePosixPath(entry['path']).name.encode() + b'\0'
                        + bytes.fromhex(entry['sha']) for entry in sorted(entries, key=order))
        sha = hashlib.sha1(f'tree {len(data)}\0'.encode() + data).hexdigest()
        if sha != expected[path]:
            raise ValueError(f'Incomplete or altered Hub tree: {path or "/"}')


def blob_prefixes(repo, rows):
    # A file for stdin avoids pipe deadlock for trees larger than a pipe buffer.
    # Stream one object at a time; never load the whole repository in memory.
    with tempfile.TemporaryFile() as source:
        source.write(''.join(r['blob_sha'] + '\n' for r in rows).encode('ascii'))
        source.seek(0)
        with subprocess.Popen(['git', '-C', str(repo), 'cat-file', '--batch'],
                              stdin=source, stdout=subprocess.PIPE) as process:
            for row in rows:
                header = process.stdout.readline().decode('ascii').split()
                if header != [row['blob_sha'], 'blob', str(row['bytes'])]:
                    raise ValueError(f'Git object mismatch for {row["path"]}')
                remaining = row['bytes']
                prefix = process.stdout.read(min(remaining, 65536))
                remaining -= len(prefix)
                while remaining:
                    block = process.stdout.read(min(remaining, 1024 * 1024))
                    if not block:
                        raise ValueError('Incomplete Git object')
                    remaining -= len(block)
                if process.stdout.read(1) != b'\n':
                    raise ValueError('Invalid Git batch separator')
                yield prefix
            if process.wait() != 0:
                raise ValueError('Git cat-file failed')


def describe(path, prefix):
    suffix = PurePosixPath(path).suffix.lower()
    try:
        text = prefix.decode('utf-8') if b'\0' not in prefix else ''
    except UnicodeDecodeError as error:
        # A byte-limited prefix may split its final UTF-8 character. Preserve
        # the preceding text; invalid bytes elsewhere still identify a binary.
        text = (prefix[:error.start].decode('utf-8')
                if error.reason == 'unexpected end of data' and error.end == len(prefix)
                else '')
    kinds = {'.md': 'markdown', '.json': 'json', '.jsonl': 'json-lines',
             '.yml': 'yaml', '.yaml': 'yaml', '.py': 'python', '.sh': 'shell',
             '.mjs': 'javascript', '.js': 'javascript', '.cjs': 'javascript',
             '.html': 'html', '.css': 'css', '.png': 'image', '.svg': 'vector',
             '.xls': 'spreadsheet', '.xlsx': 'spreadsheet', '.log': 'log',
             '.tsv': 'tabular', '.gitkeep': 'placeholder'}
    kind = kinds.get(suffix, 'text' if text or not prefix else 'binary')
    title, status = '', ''
    if suffix == '.md':
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        if match:
            found = re.search(r'^status:\s*(.*?)\s*$', match[1], re.M)
            if found:
                status = found[1].strip('"\'')
        found = re.search(r'^#\s+(.+)$', text, re.M)
        if found:
            title = found[1].strip()
    return kind, status, title


def build_inventory(repo, sha, url):
    if not SHA.fullmatch(sha):
        raise ValueError('Inventory requires an immutable commit SHA')
    rows = parse_tree(subprocess.check_output(
        ['git', '-C', str(repo), 'ls-tree', '-rlz', sha]))
    for row, prefix in zip(rows, blob_prefixes(repo, rows), strict=True):
        path = row['path']
        kind, status, title = describe(path, prefix)
        historical = path.startswith(('.archive/', 'runs/', 'experiments/',
                                     'prompts/archive/', 'docs/audit/',
                                     'docs/analysis/', 'docs/adr/', 'docs/rfc/',
                                     'docs/reviews/', 'docs/report/'))
        row.update(component=path.split('/')[0] if '/' in path else '(root)',
                   artifact_type=kind, declared_status=status, title=title,
                   decision_status='OBSERVED',
                   disposition='preserve_as_evidence' if historical else 'preserve_in_place',
                   url=f'{url}/blob/{sha}/{quote(path, safe="/")}')
    return rows


def check_coverage(expected, actual):
    paths = [r['path'] for r in actual]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate inventory path')
    wanted = {r['path']: (r['blob_sha'], int(r['bytes'])) for r in expected}
    found = {r['path']: (r['blob_sha'], int(r['bytes'])) for r in actual}
    if wanted != found:
        raise ValueError('Inventory paths or Git metadata differ from source baseline')


def render_tsv(rows):
    output = io.StringIO(newline='')
    if rows:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), delimiter='\t',
                                lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()


def read_tsv(path):
    with path.open(newline='') as source:
        return list(csv.DictReader(source, delimiter='\t'))


def summarize(rows):
    return {'files': len(rows), 'bytes': sum(r['bytes'] for r in rows),
            'components': dict(sorted(Counter(r['component'] for r in rows).items())),
            'artifact_types': dict(sorted(Counter(r['artifact_type'] for r in rows).items())),
            'declared_statuses': dict(sorted(Counter(r['declared_status'] or '(absent)'
                                                     for r in rows).items())),
            'coverage': 'Git tree enumeration only; semantic review is pending'}


def derived_artifacts(base, rows):
    baseline = json.loads((base / 'source-baseline.json').read_text())
    hub = json.loads((base / 'hub-tree.json').read_text())
    validate_sources(baseline, hub)
    existing = [row for row in rows if (
        row['path'].startswith(('docs/audit/', 'docs/analysis/', 'docs/adr/',
                                'docs/rfc/', 'docs/reviews/', 'docs/report/', 'pr-ops/'))
        or (row['path'].startswith('runs/') and row['path'].endswith('/metadata.yaml'))
        or (row['path'].startswith('experiments/')
            and row['artifact_type'] in ('markdown', 'json', 'json-lines')))]
    candidates = []
    for entry in hub['tree']:
        path = entry['path']
        if entry['type'] != 'blob' or not (
            path.startswith(('standards/', 'ai-governance/', 'ai-rules/', 'templates/htom/'))
            or path in ('AGENTS.md', 'README.md', 'GOVERNANCE.md', 'ops/repo-model.md',
                        'docs/ecosystem-map.md', 'docs/ecosystem-map-Index.md')):
            continue
        candidates.append(dict(path=path, blob_sha=entry['sha'], bytes=entry['size'],
                               classification='UNRESOLVED', applicability='pending_iteration_2',
                               url=f'{baseline["hub"]["repository_url"]}/blob/'
                                   f'{baseline["hub"]["commit_sha"]}/{quote(path, safe="/")}'))
    return {'repository-inventory.tsv': render_tsv(rows),
            'inventory-summary.json': json.dumps(summarize(rows), ensure_ascii=False, indent=2) + '\n',
            'existing-work.tsv': render_tsv(existing),
            'standards-candidates.tsv': render_tsv(candidates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify without writing')
    args = parser.parse_args()
    baseline = json.loads((BASE / 'source-baseline.json').read_text())
    rows = build_inventory(ROOT, baseline['target']['commit_sha'],
                           baseline['target']['repository_url'])
    outputs = derived_artifacts(BASE, rows)
    for name, content in outputs.items():
        destination = BASE / name
        if args.check:
            if destination.read_text() != content:
                raise SystemExit(f'Outdated or incomplete inventory artifact: {destination}')
        else:
            destination.write_text(content)
    print(f'PASS: {len(rows)} baseline files; {len(outputs)} reproducible artifacts')


if __name__ == '__main__':
    main()
