from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_data import validate_record


def base_record() -> dict:
    return yaml.safe_load(
        """
schema_version: 2
name: Example
slug: example
vendor: Example
category: model-api
product_url: https://example.com
pricing_url: https://example.com/pricing
repo_url: null
status:
  availability: active
  notes: null
platforms: [api]
authentication:
  account_required: 'yes'
  credit_card_required: unknown
  notes: null
free_tier:
  available: true
  types: [recurring_daily]
  plan_name: Free
  quantity_published: true
  quota_pools:
    - id: requests
      name: Requests
      amount: 5
      unit: requests
      period: day
      cap: 10/day
      reset:
        period: daily
        time: null
        timezone: null
        notes: null
      rollover: 'no'
      notes: null
  after_exhaustion: Wait for reset.
  rollover: 'no'
models:
  available: []
  restrictions: []
project_limits: []
deployment: []
runtime_limits: []
storage_limits: []
concurrency_limits: []
eligibility: []
regions: []
trial:
  available: false
  duration_days: null
  allowance: null
  recurring: false
  notes: null
notes: []
verification:
  last_verified: '2026-09-08'
  confidence: official_exact
  sources:
    - url: https://example.com/pricing
      type: official_pricing
      retrieved_at: '2026-09-08'
      supports_fields:
        - free_tier.quota_pools.requests
      supports:
        - Free plan includes 5 requests per day with a 10/day cap.
      page_sha256: null
"""
    )


def errors_for(record: dict, filename: str = "example.yaml") -> list[str]:
    errors: list[str] = []
    validate_record(Path(filename), record, set(), errors)
    return errors


def test_https_urls_pass_url_policy():
    assert errors_for(base_record()) == []


import pytest


@pytest.mark.parametrize("url", ["javascript:alert(1)", "data:text/html,hi", "file:///etc/passwd"])
def test_unsafe_product_url_schemes_fail(url: str):
    record = base_record()
    record["product_url"] = url
    assert any("product_url must be an http(s) URL" in error for error in errors_for(record))


def test_numeric_string_amount_requires_evidence():
    record = base_record()
    record["free_tier"]["quota_pools"][0]["amount"] = "5/day"
    record["verification"]["sources"][0]["supports"] = ["Free plan exists."]
    assert any("amount needs explicit official support" in error for error in errors_for(record))


def test_amount_and_cap_both_require_support():
    record = base_record()
    record["verification"]["sources"][0]["supports"] = ["Free plan includes 5 requests per day."]
    assert any("cap needs explicit official support" in error for error in errors_for(record))


def test_supports_fields_must_match_claim_path():
    record = base_record()
    record["verification"]["sources"][0]["supports_fields"] = ["authentication.credit_card_required"]
    assert any("amount needs explicit official support" in error for error in errors_for(record))


def test_unknown_supports_field_path_fails():
    record = base_record()
    record["verification"]["sources"][0]["supports_fields"] = ["free_tier.nope"]
    assert any("unknown path" in error for error in errors_for(record))


def test_future_last_verified_fails():
    record = base_record()
    record["verification"]["last_verified"] = "2999-01-01"
    assert any("last_verified cannot be in the future" in error for error in errors_for(record))


def test_last_verified_cannot_be_later_than_official_retrieval():
    record = base_record()
    record["verification"]["last_verified"] = "2026-09-08"
    record["verification"]["sources"][0]["retrieved_at"] = "2026-09-07"
    assert any("later than all official source retrieved_at" in error for error in errors_for(record))
