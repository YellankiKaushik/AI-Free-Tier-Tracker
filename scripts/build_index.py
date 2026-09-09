from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import yaml

try:
    from record_utils import (
        has_recurring_or_dynamic_hosted_access,
        has_trial_or_signup_grant,
        is_open_source_byok,
        quota_summary,
        reset_summary,
    )
except ModuleNotFoundError:
    from scripts.record_utils import (
        has_recurring_or_dynamic_hosted_access,
        has_trial_or_signup_grant,
        is_open_source_byok,
        quota_summary,
        reset_summary,
    )

ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA_VERSION = 3


def load_records() -> list[dict[str, Any]]:
    rows = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        rows.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    rows.sort(key=lambda r: (r["category"], r["name"].lower()))
    return rows


def freshness(last_verified: str) -> str:
    age = (datetime.now(UTC).date() - date.fromisoformat(last_verified)).days
    if age <= 30:
        return "current"
    if age <= 60:
        return "needs_recheck"
    return "stale"


def public_tool_record(data: dict[str, Any]) -> dict[str, Any]:
    verification = data["verification"]
    free_tier = data["free_tier"]
    auth = data["authentication"]
    return {
        "slug": data["slug"],
        "name": data["name"],
        "vendor": data["vendor"],
        "category": data["category"],
        "status": data["status"]["availability"],
        "status_notes": data["status"].get("notes"),
        "platforms": data.get("platforms", []),
        "free_tier_types": free_tier["types"],
        "plan_name": free_tier["plan_name"],
        "account_required": auth["account_required"],
        "credit_card_required": auth["credit_card_required"],
        "authentication": auth,
        "quantity_published": free_tier.get("quantity_published", False),
        "quota_pools": free_tier["quota_pools"],
        "quota_summary": quota_summary(data),
        "reset_summary": reset_summary(data),
        "after_exhaustion": free_tier["after_exhaustion"],
        "product_url": data["product_url"],
        "pricing_url": data.get("pricing_url"),
        "repo_url": data.get("repo_url"),
        "trial": data.get("trial"),
        "models": data.get("models", {}),
        "deployment": data.get("deployment", []),
        "runtime_limits": data.get("runtime_limits", []),
        "eligibility": data.get("eligibility", []),
        "notes": data.get("notes", []),
        "last_verified": verification["last_verified"],
        "freshness": freshness(verification["last_verified"]),
        "confidence": verification["confidence"],
        "sources": verification["sources"],
        "source_count": len(verification["sources"]),
    }


def stats_for(tools: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(tools),
        "active": sum(1 for t in tools if t["status"] == "active"),
        "legacy": sum(1 for t in tools if t["status"] == "legacy"),
        "discontinued": sum(1 for t in tools if t["status"] == "discontinued"),
        "recurring": sum(1 for r in records if has_recurring_or_dynamic_hosted_access(r)),
        "trials": sum(1 for r in records if has_trial_or_signup_grant(r)),
        "open_source_byok": sum(1 for r in records if is_open_source_byok(r)),
        "official_exact": sum(1 for t in tools if t["confidence"] == "official_exact"),
        "official_undisclosed": sum(1 for t in tools if t["confidence"] == "official_undisclosed"),
        "needs_verification": sum(1 for t in tools if t["confidence"] == "needs_verification"),
        "current": sum(1 for t in tools if t["freshness"] == "current"),
        "needs_recheck": sum(1 for t in tools if t["freshness"] == "needs_recheck"),
        "stale": sum(1 for t in tools if t["freshness"] == "stale"),
    }


def build_index() -> dict[str, Any]:
    records = load_records()
    tools = [public_tool_record(record) for record in records]
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "generated_from": "tools/*.yaml",
        "stats": stats_for(tools, records),
        "tools": tools,
    }


def main() -> None:
    out = build_index()
    (ROOT / "data/index.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote data/index.json with {len(out['tools'])} tools")


if __name__ == "__main__":
    main()
