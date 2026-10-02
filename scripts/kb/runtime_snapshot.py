"""Read the immutable runtime KB snapshot used after issue #361 migration.

The runtime checkout is fetched on demand outside this repository. Historical
validators use it to keep checking their original extraction contracts.
"""

from __future__ import annotations

import fcntl
import os
import subprocess
import tempfile
from pathlib import Path

RUNTIME_REPOSITORY = "https://github.com/G-Ivan-A/mango-ba-ai-runtime"
RUNTIME_COMMIT = "ed42b3cd0eed2774c9b080232ca00484d9a4f7cd"


def _ready(root: Path) -> bool:
    if not (root / ".git").exists() or not (root / "docs/kb").is_dir():
        return False
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], text=True,
                          capture_output=True)
    return head.returncode == 0 and head.stdout.strip() == RUNTIME_COMMIT


def processed_root() -> Path:
    checkout = os.environ.get("MANGO_BA_RUNTIME_CHECKOUT")
    if checkout:
        root = Path(checkout).resolve()
    else:
        root = Path(tempfile.gettempdir()) / "mango-ba-runtime-kb" / RUNTIME_COMMIT
        root.parent.mkdir(parents=True, exist_ok=True)
        # validate_all.py runs validators in parallel: serialize clone/checkout
        # so concurrent git commands do not collide on index.lock (issue #367).
        with open(root.parent / f"{RUNTIME_COMMIT}.lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if not _ready(root):
                if not (root / ".git").exists():
                    subprocess.run(["git", "clone", "--filter=blob:none", "--no-checkout", "--quiet",
                                    f"{RUNTIME_REPOSITORY}.git", str(root)], check=True)
                subprocess.run(["git", "-C", str(root), "sparse-checkout", "set", "docs/kb"], check=True)
                subprocess.run(["git", "-C", str(root), "checkout", "--detach", RUNTIME_COMMIT], check=True,
                               stdout=subprocess.DEVNULL)
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if head != RUNTIME_COMMIT:
        raise RuntimeError(f"runtime checkout must be {RUNTIME_COMMIT}, got {head}")
    kb = root / "docs/kb"
    if not kb.is_dir():
        raise RuntimeError(f"runtime KB is missing: {kb}")
    return kb
