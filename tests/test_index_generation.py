from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import yaml

from scripts.build_index import build_index

ROOT = Path(__file__).resolve().parents[1]


def test_generated_index_is_deterministic():
    index = ROOT / "data/index.json"
    before = hashlib.sha256(index.read_bytes()).hexdigest()
    subprocess.run([sys.executable, "scripts/build_index.py"], cwd=ROOT, check=True)
    after = hashlib.sha256(index.read_bytes()).hexdigest()
    assert before == after


def test_public_index_includes_query_fields_and_omits_confidence_score():
    index = build_index()
    tool = index["tools"][0]
    for field in (
        "status",
        "free_tier_types",
        "quota_pools",
        "quota_summary",
        "reset_summary",
        "authentication",
        "models",
        "trial",
        "freshness",
        "confidence",
        "sources",
    ):
        assert field in tool
    assert "confidence_score" not in tool


def test_nvidia_dynamic_examples_are_not_in_available_model_list():
    record = yaml.safe_load((ROOT / "tools" / "nvidia-nim.yaml").read_text(encoding="utf-8"))
    assert record["models"]["available"] == []
    assert any("examples" in note.lower() for note in record["notes"])
