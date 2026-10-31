"""Issue 395: offline/hybrid retrieval contract and additive prompt preservation."""
from pathlib import Path
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
START = b'\n<!-- issue-395: runtime-fallback -->\n'
END = b'<!-- /issue-395: runtime-fallback -->\n'


LESSONS = re.compile(rb'\n<!-- issue-411: run-lessons -->\n.*?<!-- /issue-411: run-lessons -->\n', re.S)


def original_bytes(data):
    """Remove exactly one bounded addition; compare all remaining bytes.

    Issue 411 appends a generated run-lessons block after this one and bumps
    the prompt version; scripts/validate_issue_411_lessons_pipeline.py
    verifies that block against the lessons registry.
    """
    data = LESSONS.sub(b'', data)
    data = data.replace(b'version: 0.2\nupdated: 2026-10-31\n', b'version: 0.1\nupdated: 2026-10-24\n', 1)
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
                data = (ROOT / name).read_bytes()
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
