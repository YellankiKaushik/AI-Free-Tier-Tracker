from __future__ import annotations

from collections.abc import Iterable
from typing import Any

RECURRING_OR_DYNAMIC_TYPES = {
    "recurring_daily",
    "recurring_weekly",
    "recurring_monthly",
    "dynamic_rate_limit",
}
TRIAL_OR_GRANT_TYPES = {"one_time_signup", "time_limited_trial", "promotional", "student"}
OPEN_SOURCE_BYOK = "open_source_byok"


def free_tier_types(record: dict[str, Any]) -> set[str]:
    return set(record.get("free_tier", {}).get("types", []))


def has_recurring_or_dynamic_hosted_access(record: dict[str, Any]) -> bool:
    types = free_tier_types(record)
    return bool(types & RECURRING_OR_DYNAMIC_TYPES)


def has_trial_or_signup_grant(record: dict[str, Any]) -> bool:
    types = free_tier_types(record)
    trial = record.get("trial") or {}
    return bool(types & TRIAL_OR_GRANT_TYPES) or bool(trial.get("available"))


def is_open_source_byok(record: dict[str, Any]) -> bool:
    return OPEN_SOURCE_BYOK in free_tier_types(record)


def _human_period(value: str) -> str:
    return str(value).replace("_", " ")


def _compact_period(value: str) -> str:
    return _human_period(value).replace(" ", "_")


def _format_unit(amount: Any, unit: str) -> str:
    if amount == 1 and unit.endswith("s") and "/" not in unit:
        return unit[:-1]
    return unit


def format_pool_amount(pool: dict[str, Any]) -> str:
    amount = pool.get("amount")
    amount_text = "undisclosed" if amount is None else str(amount)
    unit = _format_unit(amount, str(pool.get("unit", "unit")))
    period = str(pool.get("period", "not_applicable"))
    if period == "not_applicable":
        return f"{amount_text} {unit}"
    return f"{amount_text} {unit}/{_human_period(period)}"


def quota_summary(record: dict[str, Any]) -> str:
    pools = record.get("free_tier", {}).get("quota_pools", [])
    if pools:
        include_labels = len(pools) > 1
        parts: list[str] = []
        for pool in pools:
            text = format_pool_amount(pool)
            cap = pool.get("cap")
            if cap not in (None, ""):
                text = f"{text} (cap {cap})"
            if include_labels:
                text = f"{pool['name']}: {text}"
            parts.append(text)
        return "; ".join(parts)

    status = record.get("status", {}).get("availability")
    if status in {"discontinued", "legacy"}:
        return "Legacy/discontinued entry; no current hosted quota"

    types = free_tier_types(record)
    after = str(record.get("free_tier", {}).get("after_exhaustion", "")).lower()
    plan_name = str(record.get("free_tier", {}).get("plan_name") or "").lower()
    if OPEN_SOURCE_BYOK in types and not (types & RECURRING_OR_DYNAMIC_TYPES):
        return "Open-source client; inference/provider limits apply"
    if "prototyp" in after or "developer program" in plan_name:
        return "Free developer/prototyping access; universal quota undisclosed"
    if "dynamic_rate_limit" in types:
        return "Free access available; exact allowance undisclosed"
    if types & TRIAL_OR_GRANT_TYPES:
        return "Trial/signup access; exact allowance undisclosed"
    return "Free access available; exact allowance undisclosed"


def reset_periods(record: dict[str, Any]) -> list[str]:
    periods = {
        pool.get("reset", {}).get("period", "undisclosed")
        for pool in record.get("free_tier", {}).get("quota_pools", [])
    }
    return sorted(_human_period(period) for period in periods if period)


def reset_summary(record: dict[str, Any]) -> str:
    periods = reset_periods(record)
    if periods:
        return ", ".join(periods)
    types = free_tier_types(record)
    if "dynamic_rate_limit" in types:
        return "dynamic/undisclosed"
    if OPEN_SOURCE_BYOK in types:
        return "provider specific/not applicable"
    if types & TRIAL_OR_GRANT_TYPES:
        return "not applicable"
    return "undisclosed"


def category_records(records: Iterable[dict[str, Any]], *categories: str) -> list[dict[str, Any]]:
    wanted = set(categories)
    return [record for record in records if record.get("category") in wanted]
