from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_record(slug: str) -> dict:
    return yaml.safe_load((ROOT / "tools" / f"{slug}.yaml").read_text(encoding="utf-8"))


def test_coderabbit_free_limits_match_current_official_plan_evidence():
    record = load_record("coderabbit")
    pools = {pool["id"]: pool for pool in record["free_tier"]["quota_pools"]}
    assert {key: pools[key]["amount"] for key in ("pr-reviews", "ide-reviews", "cli-reviews")} == {
        "pr-reviews": 1,
        "ide-reviews": 3,
        "cli-reviews": 3,
    }
    assert pools["files-per-review"]["amount"] == 150
    assert any(
        "per rolling hour" in claim.lower()
        for source in record["verification"]["sources"]
        for claim in source["supports"]
    )


def test_copilot_free_completion_period_is_monthly_and_supported():
    record = load_record("github-copilot")
    completion = next(
        pool for pool in record["free_tier"]["quota_pools"] if pool["id"] == "completions"
    )
    claims = " ".join(
        claim for source in record["verification"]["sources"] for claim in source["supports"]
    ).lower()
    assert completion["amount"] == 2000
    assert completion["period"] == "month"
    assert completion["reset"]["period"] == "monthly"
    assert "2,000 code completions per month" in claims


def test_zed_keeps_published_prediction_limit_without_inventing_a_reset():
    record = load_record("zed-ai")
    pool = record["free_tier"]["quota_pools"][0]
    assert pool["amount"] == 2000
    assert pool["period"] == "undisclosed"
    assert pool["reset"]["period"] == "undisclosed"
    assert record["authentication"]["account_required"] == "yes"
    assert "time_limited_trial" in record["free_tier"]["types"]
    assert record["trial"]["available"] is True


def test_warp_does_not_choose_between_conflicting_official_free_allowances():
    record = load_record("warp")
    assert record["verification"]["last_verified"] == "2026-08-27"
    assert record["verification"]["confidence"] == "mixed"
    assert record["free_tier"]["quota_pools"] == []
    assert any(
        "150 free AI requests per month" in claim
        for source in record["verification"]["sources"]
        for claim in source["supports"]
    )


def test_unresolved_plan_conflicts_keep_their_stale_verification_dates():
    for slug in ("emergent", "trae", "warp"):
        record = load_record(slug)
        assert record["verification"]["last_verified"] == "2026-08-27"

    emergent = load_record("emergent")
    assert emergent["free_tier"]["quota_pools"][0]["period"] == "undisclosed"
    assert emergent["free_tier"]["quota_pools"][0]["rollover"] == "unknown"

    trae = load_record("trae")
    assert trae["trial"]["available"] is True
    assert trae["trial"]["duration_days"] == 14
    assert trae["free_tier"]["quantity_published"] is False
