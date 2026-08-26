from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_generated_index_is_deterministic():
    index = ROOT / "data/index.json"
    before = hashlib.sha256(index.read_bytes()).hexdigest()
    subprocess.run([sys.executable, "scripts/build_index.py"], cwd=ROOT, check=True)
    after = hashlib.sha256(index.read_bytes()).hexdigest()
    assert before == after
