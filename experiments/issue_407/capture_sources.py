"""Normalize saved gh API responses into the Gate 0 source baseline.

Input directory: issue-rest.json, issue-comments.json, pr-rest.json,
pr-comments.json, pr-inline.json, pr-reviews.json, subissues.json,
hub-head.json, hub-tree.json, all-issues-pages.json, all-prs-pages.json.
API bodies and prior conversations stay local; the public registry stores
only discovery metadata and explicitly does not claim content review.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from inventory import BASE, ROOT, render_tsv, validate_sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('responses', type=Path)
    args = parser.parse_args()

    def read(name):
        return json.loads((args.responses / f'{name}.json').read_text())

    def git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()

    target = read('pr-rest')['base']['sha']
    hub = read('hub-head')
    issue = read('issue-rest')
    baseline = {
        'schema_version': 1,
        'observed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'decision_status': 'OBSERVED',
        'target': {
            'repository_url': 'https://github.com/G-Ivan-A/mango_ba_prompts',
            'commit_sha': target, 'tree_sha': git('rev-parse', target + '^{tree}'),
            'committed_at_utc': datetime.fromisoformat(
                git('show', '-s', '--format=%cI', target)).astimezone(timezone.utc).isoformat(),
            'commit_url': f'https://github.com/G-Ivan-A/mango_ba_prompts/commit/{target}',
        },
        'hub': {
            'repository_url': 'https://github.com/G-Ivan-A/hybrid-Intelligence-lab',
            'commit_sha': hub['sha'], 'tree_sha': hub['commit']['tree']['sha'],
            'committed_at_utc': hub['commit']['committer']['date'],
            'commit_url': f'https://github.com/G-Ivan-A/hybrid-Intelligence-lab/commit/{hub["sha"]}',
        },
        'prepared_branch': {
            'name': 'issue-407-28502daafccb',
            'bootstrap_sha': read('pr-rest')['head']['sha'],
            'difference_from_target': 'Bootstrap .gitkeep only; not a product component',
        },
        'issue': {
            'url': issue['html_url'], 'updated_at_utc': issue['updated_at'],
            'body_sha256': hashlib.sha256(issue['body'].encode()).hexdigest(),
            'comments_url': issue['comments_url'],
            'comments_count': len(read('issue-comments')),
            'required_subissues': [r['html_url'] for r in read('subissues')],
        },
        'pull_request': {
            'url': 'https://github.com/G-Ivan-A/mango_ba_prompts/pull/408',
            'conversation_comments_count': len(read('pr-comments')),
            'inline_comments_count': len(read('pr-inline')),
            'reviews_count': len(read('pr-reviews')),
            'founder_stage_acceptance': 'UNRESOLVED: no acceptance record at capture time',
        },
        'exclusions': [
            'Untracked/ignored local files, .git object database, remote branch build output',
            'Bootstrap .gitkeep: outside pinned upstream product baseline',
        ],
        'content_review': 'Discovery metadata only; comprehensive semantic audit awaits Gate 0 acceptance',
    }
    tree = read('hub-tree')
    validate_sources(baseline, tree)
    (BASE / 'source-baseline.json').write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + '\n')
    (BASE / 'hub-tree.json').write_text(json.dumps(tree, ensure_ascii=False, indent=2) + '\n')
    rows = []
    for kind, name in [('issue', 'all-issues-pages'), ('pull_request', 'all-prs-pages')]:
        for page in read(name):
            for item in page:
                if kind == 'issue' and 'pull_request' in item:
                    continue
                rows.append(dict(kind=kind, url=item['html_url'], title=item['title'],
                                 created_at=item['created_at'], updated_at=item['updated_at'],
                                 closed_at=item['closed_at'] or '',
                                 merged_at=item.get('merged_at') or '', state=item['state'],
                                 review_status='discovered_metadata_only',
                                 decision_status='OBSERVED'))
    rows.sort(key=lambda row: (row['created_at'], row['url']))
    (BASE / 'github-activity.tsv').write_text(render_tsv(rows))
    print(f'Pinned both source commits; discovered {len(rows)} issue/PR metadata records')


if __name__ == '__main__':
    main()
