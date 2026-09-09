from __future__ import annotations

from scripts.build_reset_calendar import build_reset_calendar


def test_reset_calendar_separates_scheduled_and_dynamic_groups():
    calendar = build_reset_calendar()
    assert "scheduled_reset_groups" in calendar
    assert "dynamic_or_provider_specific_groups" in calendar
    assert "not_applicable" not in calendar["scheduled_reset_groups"]
    assert "not_applicable" not in calendar["dynamic_or_provider_specific_groups"]


def test_reset_calendar_rows_include_pool_names():
    calendar = build_reset_calendar()
    daily = calendar["scheduled_reset_groups"].get("daily", [])
    assert any(row["pool_name"] == "PR reviews" for row in daily)
