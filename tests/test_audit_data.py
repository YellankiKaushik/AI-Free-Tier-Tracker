from __future__ import annotations

import yaml

from scripts.audit_data import audit_record


def test_audit_flags_hosted_open_source_byok_without_dynamic_semantics(tmp_path):
    record = yaml.safe_load(
        """
category: model-api
platforms: [api]
repo_url: null
status: {availability: active}
free_tier:
  available: true
  types: [open_source_byok]
  quota_pools: []
trial: {available: false}
notes: []
deployment: []
runtime_limits: []
eligibility: []
regions: []
"""
    )
    findings = audit_record(tmp_path / "example.yaml", record)
    assert any("open_source_byok" in finding for finding in findings)


def test_audit_allows_mixed_dynamic_byok_record(tmp_path):
    record = yaml.safe_load(
        """
category: coding-assistant
platforms: [web]
repo_url: null
status: {availability: active}
free_tier:
  available: true
  types: [dynamic_rate_limit, open_source_byok]
  quota_pools: []
trial: {available: false}
notes: []
deployment: []
runtime_limits: []
eligibility: []
regions: []
"""
    )
    assert audit_record(tmp_path / "zed.yaml", record) == []
