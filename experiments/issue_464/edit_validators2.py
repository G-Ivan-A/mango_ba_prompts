"""Issue #464: валидаторы 446 и 450 — числа шагов и сравнение с плечами замера через слой отката."""
from _edit import edit

edit("scripts/validate_issue_446_test_kit.py", [
    ("self.assertEqual(len(self.rows), 13)", "self.assertEqual(len(self.rows), 14)"),
    ('self.assertEqual(counts["steps"], 13)', 'self.assertEqual(counts["steps"], 14)'),
    ('self.assertEqual(counts["byTest"] + counts["published"], 13)', 'self.assertEqual(counts["byTest"] + counts["published"], 14)'),
    ('        for step in A_IN:\n            self.assertEqual(modes[step], expected, step)\n',
     '        for step in A_IN:\n            self.assertEqual(modes[step], expected, step)\n'
     '        # Ш-А (issue #464) в RUN-0083 не было; по тесту он идёт как черновик без опубликованного текста.\n'
     '        self.assertEqual(modes["Ш-А Анкета"], "by-test")\n'),
])

edit("scripts/validate_issue_450_bl156g_167_168.py", [
    ('import json, re, unittest\nfrom pathlib import Path\n',
     'import importlib.util, json, re, unittest\nfrom pathlib import Path\n'),
    ('    def test_arm_b_equals_published_body(self):\n'
     '        strip = lambda t: re.sub(r"\\A---\\n.*?\\n---\\n", "", t, count=1, flags=re.S)  # noqa: E731\n',
     '    def test_arm_b_equals_published_body(self):\n'
     '        # Issue #464 правит тексты поверх измеренных: плечо сравнивается с текстом без слоя #464.\n'
     '        # Ш-В слой не трогает: сравнение с RUN-0085 идёт побайтово, как раньше.\n'
     '        spec = importlib.util.spec_from_file_location("i464_for_450", ROOT / "experiments/issue_464/prompt_changes.py")\n'
     '        i464 = importlib.util.module_from_spec(spec)\n'
     '        spec.loader.exec_module(i464)\n'
     '        measured = lambda p: i464.revert(p, read(p))  # noqa: E731\n'
     '        strip = lambda t: re.sub(r"\\A---\\n.*?\\n---\\n", "", t, count=1, flags=re.S)  # noqa: E731\n'),
    ('            self.assertEqual(strip(read(path)), strip(arm), path)\n',
     '            self.assertEqual(strip(measured(path)), strip(arm), path)\n'),
    ('self.assertEqual(strip(read("prompts/bcreq-constitution-governance-oneshot.md")), strip(arm))',
     'self.assertEqual(strip(measured("prompts/bcreq-constitution-governance-oneshot.md")), strip(arm))'),
])
