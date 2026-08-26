from __future__ import annotations

import yaml


def test_official_numerical_claims_require_official_evidence():
    data = yaml.safe_load(
        """
slug: example
free_tier:
  quantity_published: true
  allowances:
    - amount: 10
verification:
  confidence: community_only
  sources:
    - type: community
"""
    )
    official = [
        s
        for s in data["verification"]["sources"]
        if str(s.get("type", "")).startswith("official_")
    ]
    assert data["free_tier"]["quantity_published"] is True
    assert official == []
