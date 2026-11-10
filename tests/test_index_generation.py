from __future__ import annotations

import hashlib
import json
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
    assert json.loads(index.read_text(encoding="utf-8")) == build_index()


def test_public_index_includes_query_fields_and_omits_confidence_score():
    index = build_index()
    tool = index["tools"][0]
    assert index["schema_version"] == 4
    for field in (
        "status",
        "free_tier_types",
        "quota_pools",
        "quota_summary",
        "reset_summary",
        "authentication",
        "models",
        "trial",
        "last_verified",
        "confidence",
        "sources",
    ):
        assert field in tool
    assert "freshness" not in tool
    assert "confidence_score" not in tool
    assert set(index["stats"]).isdisjoint({"current", "needs_recheck", "stale"})


def test_nvidia_dynamic_examples_are_not_in_available_model_list():
    record = yaml.safe_load((ROOT / "tools" / "nvidia-nim.yaml").read_text(encoding="utf-8"))
    assert record["models"]["available"] == []
    assert any("examples" in note.lower() for note in record["notes"])


def test_nvidia_source_repair_preserves_undisclosed_quota_and_verification_date():
    record = yaml.safe_load((ROOT / "tools" / "nvidia-nim.yaml").read_text(encoding="utf-8"))
    sources = record["verification"]["sources"]
    source_urls = [source["url"] for source in sources]
    retired_source_url = "https://docs.api.nvidia.com/nim/re/docs/" "run-anywhere"
    assert record["pricing_url"] == "https://docs.api.nvidia.com/nim/docs/product"
    assert retired_source_url not in source_urls
    assert len(source_urls) == len(set(source_urls))
    assert record["free_tier"]["quantity_published"] is False
    assert record["free_tier"]["quota_pools"] == []
    assert record["verification"]["last_verified"] == "2026-09-09"
