"""Issue 395: offline/hybrid retrieval contract and additive prompt preservation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
START = b'\n<!-- issue-395: runtime-fallback -->\n'
END = b'<!-- /issue-395: runtime-fallback -->\n'
bl156a_spec = importlib.util.spec_from_file_location('bl156a_prompt_changes', ROOT / 'experiments/issue_444/bl156a_prompt_changes.py')
bl156a = importlib.util.module_from_spec(bl156a_spec)
bl156a_spec.loader.exec_module(bl156a)


def original_bytes(data):
    """Remove exactly one bounded addition; compare all remaining bytes."""
    if START not in data:
        return data
    before, addition = data.split(START, 1)
    _, after = addition.split(END, 1)
    return before + after


class PromptContractTests(unittest.TestCase):
    def test_all_fourteen_originals_are_preserved(self):
        baseline = json.loads((ROOT / 'experiments/issue_395/prompt-baseline.json').read_text())
        self.assertEqual(set(baseline), {str(p.relative_to(ROOT)) for p in (ROOT / 'prompts').glob('bcreq-*.md')})
        for name, digest in baseline.items():
            with self.subTest(prompt=name):
                # Issue 444 (BL-156а): revert typed gates and pinned runtime links.
                data = bl156a.revert_bytes(name, (ROOT / name).read_bytes())
                self.assertEqual(data.count(START), 1)
                self.assertEqual(data.count(END), 1)
                self.assertEqual(hashlib.sha256(original_bytes(data)).hexdigest(), digest)

    def test_each_copied_prompt_has_the_complete_retrieval_contract(self):
        # Each prompt is copied independently; none may depend on another block
        # being downloaded from runtime. These are acceptance obligations.
        obligations = [
            'Р1–Р7', 'АД-1…АД-11', 'КС1–КС7', 'БС1–БС5', 'CB-0.6',
            'детальные стандарты недоступны', 'полный текст конституции',
            'Domain → Capability → Feature → Atomic Function',
            'всей продуктовой линейке', 'требует доработки',
            'product_ids', 'sections_map', 'source_refs',
            'сначала класс', 'инициирует БА', 'без БЗ', 'файлы', 'текст',
            'противореч', '8.4', '8.5', 'Г-IN', 'Г-С1', 'Г-W',
        ]
        for path in sorted((ROOT / 'prompts').glob('bcreq-*.md')):
            with self.subTest(prompt=path.name):
                data = path.read_bytes()
                self.assertTrue(START in data, 'missing fallback block')
                block = data.split(START)[1].split(END)[0].decode()
                for obligation in obligations:
                    self.assertIn(obligation, block)
                for target in re.findall(r'\]\(([^)]+)\)', block):
                    self.assertTrue(target.startswith('https://'), target)


if __name__ == '__main__':
    unittest.main()
