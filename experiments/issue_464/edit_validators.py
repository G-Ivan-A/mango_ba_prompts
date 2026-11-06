"""Issue #464: валидаторы, зафиксировавшие маршрут из 13 шагов. Одноразовая правка.

Смысл проверок не ослаблен: число шагов и файлов обновлено, Ш-А назван явно.
"""
from _edit import edit

edit("scripts/validate_issue_427_rfc.py", [
    ('STEPS = ("Ш-0", "Ш-1",', 'STEPS = ("Ш-0", "Ш-А", "Ш-1",'),
    ('numbered = re.findall(r"^\\| (\\d+) \\| (Ш-[0-9ВР]) ", block, re.M)',
     'numbered = re.findall(r"^\\| (\\d+) \\| (Ш-[0-9АВР]) ", block, re.M)'),
    ("list(range(1, 13)))", "list(range(1, 15)))"),
    ('table = [r for r in rows(block, r"Ш-[0-9ВРС]")]', 'table = [r for r in rows(block, r"Ш-[0-9АВРС]")]'),
    ('        self.assertEqual(len(names), 11, sorted(names))\n'
     '        for name in names:\n'
     '            with self.subTest(prompt=name):\n'
     '                self.assertTrue((PROMPTS / f"{name}.md").exists(), name)\n',
     '        self.assertEqual(len(names), 12, sorted(names))\n'
     '        for name in names:\n'
     '            with self.subTest(prompt=name):\n'
     '                # Ш-А (issue #464) — новый промпт: пока только черновик, как Ш-Р.\n'
     '                folder = PROMPTS / "drafts" if name == "bcreq-intake-questionnaire-stepwise" else PROMPTS\n'
     '                self.assertTrue((folder / f"{name}.md").exists(), name)\n'),
])

edit("scripts/validate_issue_430_flow.py", [
    ('FLOW_STEPS = ("Ш-0", "Ш-1",', 'FLOW_STEPS = ("Ш-0", "Ш-А", "Ш-1",'),
    ('if f"C{n:02d}" not in ("C01", "C09")])', 'if f"C{n:02d}" != "C09"])'),
    ("# C01 и C09 приходят в Ш-1 из входа БА (RFC #427, раздел 9.2).",
     "# C09 приходит в Ш-1 из входа БА; C01 — операция шага Ш-А (RFC #427, раздел 9.2; issue #464)."),
])

edit("scripts/validate_issue_438_step_prompts.py", [
    ("манифест покрывает 13 шагов маршрута в 12 файлах;", "манифест покрывает 14 шагов маршрута в 13 файлах;"),
    ('self.assertEqual(len(drafts), 12)', 'self.assertEqual(len(drafts), 13)'),
    ('self.assertEqual(item["steps"], ["Ш-Р"], "без v0.1 — только заглушка Ш-Р")',
     'self.assertIn(item["steps"], (["Ш-Р"], ["Ш-А"]), "без v0.1 — только заглушка Ш-Р и анкета Ш-А")'),
    ("self.assertEqual(len(rows), 13)", "self.assertEqual(len(rows), 14)"),
    ('self.assertRegex(text, r"(?m)^version: 0\\.6$")', 'self.assertRegex(text, r"(?m)^version: 0\\.7$")'),
])

edit("scripts/validate_issue_446_test_kit.py", [
    ("#: 2.5.0 — issue #460; 2.6.0 — issue #454 (режимы по RUN-0089, пакеты Ш-Р).\n"
     'SITE_VERSION = "2.6.0"\n',
     "#: 2.5.0 — issue #460; 2.6.0 — issue #454 (режимы по RUN-0089, пакеты Ш-Р);\n"
     "#: 2.7.0 — issue #464 (страница «Стандарты», шаг Ш-А).\n"
     'SITE_VERSION = "2.7.0"\n'),
])

edit("scripts/validate_issue_450_bl156g_167_168.py", [
    ('"prompts/bcreq-constitution-governance-oneshot.md": "0.2"', '"prompts/bcreq-constitution-governance-oneshot.md": "0.3"'),
    ('"prompts/bcreq-context-understanding-stepwise.md": "0.2"', '"prompts/bcreq-context-understanding-stepwise.md": "0.3"'),
    ('"prompts/bcreq-fr-documentation-stepwise.md": "0.2"', '"prompts/bcreq-fr-documentation-stepwise.md": "0.3"'),
    ('"prompts/bcreq-orr-solution-design-stepwise.md": "0.2"', '"prompts/bcreq-orr-solution-design-stepwise.md": "0.3"'),
])

edit("scripts/validate_issue_460_site_debug.py", [
    ('EXPECTED_CODES = {f"Ш-{n}" for n in range(10)} | {"Ш-В", "Ш-Р", "Ш-С"}',
     'EXPECTED_CODES = {f"Ш-{n}" for n in range(10)} | {"Ш-А", "Ш-В", "Ш-Р", "Ш-С"}'),
    ("self.assertGreaterEqual(len(table_codes), 13)", "self.assertGreaterEqual(len(table_codes), 14)"),
    ('self.assertEqual(outcome["minimum"], 13)', 'self.assertEqual(outcome["minimum"], 14)'),
    ('self.assertIn("минимум 13", ', 'self.assertIn("минимум 14", '),
])
