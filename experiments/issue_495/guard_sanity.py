"""Проверка, что тесты BaselineMapTest ловят отключение каждого сторожа map_baseline.

    python3 experiments/issue_495/guard_sanity.py
Каждый сценарий отключает одно правило и ожидает падения хотя бы одного теста.
"""
import importlib.util
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("v495", ROOT / "scripts/validate_issue_495_prompt_purity.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def run(patch):
    orig = v.load_module

    def load(path, name):
        mod = orig(path, name)
        if "map_baseline" in path:
            patch(mod)
        return mod
    v.load_module = load
    try:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(v.BaselineMapTest)
        res = unittest.TextTestRunner(stream=open("/dev/null", "w")).run(suite)
        return len(res.failures) + len(res.errors)
    finally:
        v.load_module = orig


cases = {
    "без носителей": lambda m: setattr(m, "CARRIERS", {}),
    "без правила полной ссылки": lambda m: setattr(m, "LINK", re.compile(r"(?!x)x")),
    "без коротких фрагментов (SHORT=100)": lambda m: setattr(m, "SHORT", 100),
}
bad = 0
for name, patch in cases.items():
    n = run(patch)
    print(f"{name}: падений {n}")
    bad += n == 0
print("baseline:", run(lambda m: None))
sys.exit(1 if bad else 0)
