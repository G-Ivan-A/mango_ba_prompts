"""Gate 0 inventory must cover the immutable Git tree, including hidden files."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'experiments/issue_407'
spec = importlib.util.spec_from_file_location('issue407_inventory', BASE / 'inventory.py')
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryTests(unittest.TestCase):
    def test_multibyte_character_at_prefix_boundary_preserves_frontmatter(self):
        prefix = '---\nstatus: draft\n---\n# Заголовок\n'.encode() + b'\xd1'
        kind, status, title = inventory.describe('large.md', prefix)
        self.assertEqual((kind, status, title), ('markdown', 'draft', 'Заголовок'))

    def test_tree_parser_preserves_hidden_unicode_and_unusual_paths(self):
        sha = 'a' * 40
        paths = ['.github/workflows/check.yml', 'new-component/данные\t1.md',
                 'arbitrary/unexpected\nfile.txt', 'README.md']
        raw = b''.join(f'100644 blob {sha} 12\t{p}\0'.encode() for p in paths)
        self.assertEqual([r['path'] for r in inventory.parse_tree(raw)], paths)

    def test_tree_rejects_truncated_records_and_submodules(self):
        with self.assertRaises(ValueError):
            inventory.parse_tree(b'100644 blob broken')
        with self.assertRaises(ValueError):
            inventory.parse_tree(f'160000 commit {"a" * 40} -\tsubmodule\0'.encode())

    def test_coverage_rejects_omission_duplicate_and_modified_metadata(self):
        expected = [{'path': '.hidden/data', 'blob_sha': 'a' * 40, 'bytes': 10}]
        inventory.check_coverage(expected, expected)
        for rows in [[], expected * 2, [dict(expected[0], bytes=11)],
                     [dict(expected[0], path='another')]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                inventory.check_coverage(expected, rows)

    def test_sources_require_immutable_shas_and_complete_hub_tree(self):
        baseline = json.loads((BASE / 'source-baseline.json').read_text())
        hub = json.loads((BASE / 'hub-tree.json').read_text())
        inventory.validate_sources(baseline, hub)
        for bad in [dict(hub, truncated=True), dict(hub, sha='a' * 40)]:
            with self.assertRaises(ValueError):
                inventory.validate_sources(baseline, bad)
        with self.assertRaises(ValueError):
            inventory.validate_sources(baseline, dict(hub, tree=hub['tree'][1:]))
        bad = json.loads(json.dumps(baseline))
        bad['target']['commit_sha'] = 'main'
        with self.assertRaises(ValueError):
            inventory.validate_sources(bad, hub)

    def test_snapshot_uses_git_objects_not_dirty_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args])
            git('init', '-q')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'user.name', 'Fixture')
            (repo / '.hidden').mkdir()
            (repo / '.hidden/evidence.md').write_text('---\nstatus: draft\n---\nOld\n')
            (repo / 'unexpected').mkdir()
            (repo / 'unexpected/данные.bin').write_bytes(b'\x00\xff')
            git('add', '.')
            git('commit', '-qm', 'Fixture baseline')
            sha = git('rev-parse', 'HEAD').decode().strip()
            first = inventory.build_inventory(repo, sha, 'https://github.com/example/repo')
            (repo / '.hidden/evidence.md').write_text('New dirty content')
            (repo / 'untracked.txt').write_text('not in the baseline')
            self.assertEqual(first, inventory.build_inventory(
                repo, sha, 'https://github.com/example/repo'))
            self.assertEqual(len(first), 2)
            self.assertEqual(first[0]['declared_status'], 'draft')
            self.assertEqual(first[1]['artifact_type'], 'binary')
            self.assertIn('%D0', first[1]['url'])

    def test_committed_artifacts_are_complete_and_reproducible(self):
        baseline = json.loads((BASE / 'source-baseline.json').read_text())
        actual = inventory.build_inventory(ROOT, baseline['target']['commit_sha'],
                                           baseline['target']['repository_url'])
        committed = inventory.read_tsv(BASE / 'repository-inventory.tsv')
        inventory.check_coverage(actual, committed)
        self.assertEqual(inventory.render_tsv(actual),
                         (BASE / 'repository-inventory.tsv').read_text())
        self.assertEqual(inventory.summarize(actual),
                         json.loads((BASE / 'inventory-summary.json').read_text()))
        for name, content in inventory.derived_artifacts(BASE, actual).items():
            with self.subTest(artifact=name):
                self.assertEqual((BASE / name).read_text(), content)

    def test_assignment_register_preserves_all_acceptance_criteria(self):
        spec = importlib.util.spec_from_file_location(
            'issue407_requirements', BASE / 'build_requirements.py')
        builder = importlib.util.module_from_spec(spec)
        # The standalone evidence scripts share their sibling inventory module.
        from unittest.mock import patch
        import sys
        with patch.dict(sys.modules, {'inventory': inventory}):
            spec.loader.exec_module(builder)
        register = json.loads((BASE / 'requirements.json').read_text())
        self.assertEqual(register, builder.build())
        rows = register['requirements']
        ids = {row['id'] for row in rows}
        self.assertEqual(len(ids), len(rows))
        self.assertTrue({f'AC{n:02d}' for n in range(1, 13)} <= ids)
        self.assertTrue({f'R{n}' for n in range(1, 6)} <= ids)
        for row in rows:
            self.assertTrue(row['source_url'].startswith('https://'))
            self.assertTrue(row['source_body_lines'])
            self.assertEqual(len(row['source_body_sha256']), 64)
            if row['implementation_state'] == 'gate_0_evidence':
                self.assertTrue(row['evidence_urls'])


if __name__ == '__main__':
    unittest.main()
