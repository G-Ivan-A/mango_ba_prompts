#!/usr/bin/env python3
"""Show the new retrieval-contract regression failing on the previous kit.

This reproduces the missing instruction, not the old model's response. Uses
only git's small existing JSON object; does not check out or build the repo.
"""
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('tests474', ROOT/'scripts/validate_issue_474_execution.py')
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)
tests.Execution.setUpClass()
previous = subprocess.run(['git','show','a55ab964:site/data/a-in-kit.json'],
                          check=True,capture_output=True,text=True)
tests.Execution.kit = json.loads(previous.stdout)
result = unittest.TestResult()
tests.Execution('test_retrieval_contract_and_deferred_provenance').run(result)
if len(result.failures) != 1 or result.errors:
    raise SystemExit('Expected one missing-contract failure on the previous kit')
print('Reproduced: old kit fails the new complete retrieval-contract assertion.')
