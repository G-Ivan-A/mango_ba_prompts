"""Keep absolute, pinned source links reproducible in the research report."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
MANGO = 'https://github.com/G-Ivan-A/mango_ba_prompts'
HUB = 'https://github.com/G-Ivan-A/hybrid-Intelligence-lab'
RUNTIME = 'https://github.com/G-Ivan-A/mango-ba-ai-runtime'
MSHA = '12844ec7e156a5bcfd6f8e07ffbeeeb588e74aae'
HSHA = 'f2e5c9b645502d457441f0a37427780f42fa43af'
RSHA = 'b67410f627801345309281faa15e7219722bfb1a'
EXPERIMENT = ('https://github.com/konard/G-Ivan-A-mango_ba_prompts/blob/'
              'issue-397-97e1903ee376/experiments/issue_397/')
MARKER = '<!-- issue-397: absolute source references -->'


def main():
    refs = {
        'issue': MANGO + '/issues/397', 'pr': MANGO + '/pull/398',
        'site': 'https://g-ivan-a.github.io/mango_ba_prompts',
        'mango-snapshot': MANGO + '/tree/' + MSHA,
        'hub-snapshot': HUB + '/tree/' + HSHA,
        'runtime-snapshot': RUNTIME + '/tree/' + RSHA,
    }
    paths = {
        'hub-agents': (HUB, HSHA, 'AGENTS.md'),
        'collaboration': (HUB, HSHA, 'ai-rules/agent-collaboration-rules.md'),
        'adr21': (HUB, HSHA, 'docs/adr/2026-09-adr-021-agent-collaboration-layer.md'),
        'root-rfc': (HUB, HSHA, 'docs/rfc/2026-09-03-rfc-agents-md-root-contract.md'),
        'mango-work': (MANGO, MSHA, 'ai-rules/agent-work-rules.md'),
        'runtime-agents': (RUNTIME, RSHA, 'AGENTS.md'),
        'dist-agents': (HUB, HSHA, 'projects/ba-ai-process/dist/execution-package-gigacode-cli/AGENTS.md'),
        'dist-manifest': (HUB, HSHA, 'projects/ba-ai-process/dist/execution-package-gigacode-cli/package-manifest.yaml'),
        'legacy': (HUB, HSHA, 'research/ba-requirements/2026-09-09-legacy-normative-influence-facts.md'),
        'skill-format': (HUB, HSHA, 'research/ba-requirements/2026-09-10-skill-granularity-format-facts.md'),
        'forensics': (HUB, HSHA, 'projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md'),
        'constitution': (MANGO, MSHA, 'prompts/bcreq-constitution-governance-oneshot.md'),
        'sections': (MANGO, MSHA, 'standards/bcreq-sections/README.md'),
        'gates': (MANGO, MSHA, 'docs/contracts/bcreq-stage-gates.md'),
        'review391': (MANGO, MSHA, 'docs/reviews/issue-391-bcreq-review.md'),
        'inventory391': (MANGO, MSHA, 'docs/reviews/issue-391-golden-inventory.md'),
        'test391': (MANGO, MSHA, 'scripts/test_issue_391_lessons.py'),
    }
    for key, (repo, sha, path) in paths.items():
        refs[key] = f'{repo}/blob/{sha}/{path}'
    for n in [358, 384]:
        refs[f'm{n}'] = f'{MANGO}/issues/{n}'
    for n in [389, 390, 392, 396]:
        refs[f'p{n}'] = f'{MANGO}/pull/{n}'
    for n in [547, 551, 559, 563, 571, 580, 589, 593, 605, 625, 631]:
        refs[f'h{n}'] = f'{HUB}/issues/{n}'
    for n in range(73, 78):
        refs[f'run{n}'] = f'{MANGO}/tree/{MSHA}/runs/2026/RUN-{n:04d}/outputs'
    files = {
        'evidence': 'evidence.md', 'verify': 'verify.py', 'probe': 'prompt-probe.json',
        'run-inventory': 'run-inventory.json', 'replay-cases': 'replay-cases.json',
        'replay-results': 'replay-results.json', 'experiment-readme': 'README.md',
    }
    refs.update({key: EXPERIMENT + name for key, name in files.items()})
    evidence = json.loads((BASE / 'evidence.json').read_text())
    refs['split-export'] = evidence['exports']['split']['url']
    refs['task-export'] = evidence['exports']['1131']['url']
    refs.update({row['key']: refs['evidence'] + '#' + row['key'].lower()
                 for row in evidence['entries']})
    report = ROOT / 'docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md'
    body = report.read_text().split(MARKER)[0].rstrip()
    report.write_text(body + '\n\n' + MARKER + '\n\n' +
                      '\n'.join(f'[{key}]: {url}' for key, url in refs.items()) + '\n')
    print(f'Wrote {len(refs)} absolute source references')


if __name__ == '__main__':
    main()
