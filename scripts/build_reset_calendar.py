from __future__ import annotations

from pathlib import Path
import json

try:
    from build_index import load_records
except ModuleNotFoundError:
    from scripts.build_index import load_records

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    buckets: dict[str, list[dict]] = {}
    for record in load_records():
        for pool in record["free_tier"]["quota_pools"]:
            period = pool["reset"]["period"]
            buckets.setdefault(period, []).append(
                {
                    "tool": record["slug"],
                    "name": record["name"],
                    "pool": pool["id"],
                    "amount": pool["amount"] if pool["amount"] is not None else "undisclosed",
                    "unit": pool["unit"],
                    "reset_time": pool["reset"].get("time") or "undisclosed",
                    "timezone": pool["reset"].get("timezone") or "undisclosed",
                    "notes": pool["reset"].get("notes"),
                }
            )
    output = {
        "generated_from": "tools/*.yaml",
        "description": "Scheduled theoretical resets based on documented plan rules, not personal balances.",
        "reset_groups": dict(sorted(buckets.items())),
    }
    (ROOT / "data/reset-calendar.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Wrote data/reset-calendar.json")


if __name__ == "__main__":
    main()
