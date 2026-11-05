"""Публикация по решениям RUN-0085/86/87: применяет правки к prompts/ один раз.

Запускается только после `score` с publish=true. Обратный ход — prompt_changes.revert.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, HERE / rel)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


A3 = load("a3_rule", "run0085/a3_rule.py")
BLOCK = load("block_rule", "run0086/block_rule.py")
SES = load("session_rules", "run0087/session_rules.py")
PC = load("prompt_changes", "prompt_changes.py")
EDITS = {
    PC.SHV: A3.apply,
    BLOCK.S1: lambda t: BLOCK.apply(BLOCK.S1, t),
    BLOCK.S3: lambda t: BLOCK.apply(BLOCK.S3, t),
    BLOCK.S6: lambda t: BLOCK.apply(BLOCK.S6, t),
    SES.PROMPT: SES.apply,
}
for path, edit in EDITS.items():
    p = ROOT / path
    before = p.read_text(encoding="utf-8")
    old_v, new_v, old_u = PC.FRONT[path]
    after = edit(before)
    assert after.count(f"version: {old_v}\n") == 1 and after.count(f"updated: {old_u}\n") == 1, path
    after = after.replace(f"version: {old_v}\n", f"version: {new_v}\n").replace(f"updated: {old_u}\n", f"updated: {PC.UPDATED}\n")
    assert PC.revert(path, after) == PC.revert_pin(before), path
    p.write_text(after, encoding="utf-8")
    print(path, old_v, "->", new_v)
