"""Run the same panel regression against the prepared pre-fix commit."""
import importlib.util
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ain_acceptance',ROOT/'scripts/validate_issue_468_a_in.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=subprocess.run(['git','show','b4109ef38c8277163e685315335cc37fec61c809:site/index.html'],cwd=ROOT,capture_output=True,text=True,check=True).stdout
read=Path.read_text
log=io.StringIO()
with patch.object(Path,'read_text',lambda p,*a,**k: old if p==ROOT/'site/index.html' else read(p,*a,**k)):
    result=unittest.TextTestRunner(stream=log).run(m.AINAcceptance('test_proposed_panel_and_reproducible_overlay'))
print(log.getvalue())
if len(result.failures)!=1 or result.errors:
    raise SystemExit('Expected precisely the pre-fix missing-panel regression')
print('Expected pre-fix failure reproduced; run current validator for after-fix result.')
