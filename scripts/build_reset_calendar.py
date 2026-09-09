from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from build_index import load_records
except ModuleNotFoundError:
    from scripts.build_index import load_records

ROOT = Path(__file__).resolve().parents[1]
SCHEDULED_RESET_PERIODS = {"daily", "weekly", "monthly", "billing_cycle"}
DYNAMIC_RESET_PERIODS = {"dynamic", "provider_specific", "undisclosed"}


def reset_row(record: dict[str, Any], pool: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool": record["slug"],
        "name": record["name"],
        "pool": pool["id"],
        "pool_name": pool["name"],
        "amount": pool["amount"] if pool["amount"] is not None else "undisclosed",
        "unit": pool["unit"],
        "reset_time": pool["reset"].get("time") or "undisclosed",
        "timezone": pool["reset"].get("timezone") or "undisclosed",
        "notes": pool["reset"].get("notes"),
    }


def build_reset_calendar() -> dict[str, Any]:
    scheduled: dict[str, list[dict[str, Any]]] = {}
    dynamic: dict[str, list[dict[str, Any]]] = {}
    for record in load_records():
        for pool in record["free_tier"]["quota_pools"]:
            period = pool["reset"]["period"]
            if period == "not_applicable":
                continue
            bucket = scheduled if period in SCHEDULED_RESET_PERIODS else dynamic
            bucket.setdefault(period, []).append(reset_row(record, pool))
    return {
        "schema_version": 2,
        "generated_from": "tools/*.yaml",
        "description": "Theoretical resets based on documented plan rules, not personal balances.",
        "scheduled_reset_groups": dict(sorted(scheduled.items())),
        "dynamic_or_provider_specific_groups": dict(sorted(dynamic.items())),
    }


def main() -> None:
    output = build_reset_calendar()
    (ROOT / "data/reset-calendar.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Wrote data/reset-calendar.json")


if __name__ == "__main__":
    main()
