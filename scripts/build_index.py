from __future__ import annotations

from datetime import date
from pathlib import Path
import json

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_records() -> list[dict]:
    rows = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        rows.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    rows.sort(key=lambda r: (r["category"], r["name"].lower()))
    return rows


def freshness(last_verified: str) -> str:
    age = (date.today() - date.fromisoformat(last_verified)).days
    if age <= 30:
        return "current"
    if age <= 60:
        return "needs_recheck"
    return "stale"


def main() -> None:
    records = load_records()
    tools = []
    for d in records:
        tools.append(
            {
                "slug": d["slug"],
                "name": d["name"],
                "vendor": d["vendor"],
                "category": d["category"],
                "status": d["status"]["availability"],
                "status_notes": d["status"].get("notes"),
                "platforms": d.get("platforms", []),
                "free_tier_types": d["free_tier"]["types"],
                "plan_name": d["free_tier"]["plan_name"],
                "account_required": d["authentication"]["account_required"],
                "credit_card_required": d["authentication"]["credit_card_required"],
                "quantity_published": d["free_tier"].get("quantity_published", False),
                "quota_pools": d["free_tier"]["quota_pools"],
                "after_exhaustion": d["free_tier"]["after_exhaustion"],
                "product_url": d["product_url"],
                "pricing_url": d.get("pricing_url"),
                "repo_url": d.get("repo_url"),
                "trial": d.get("trial"),
                "models": d.get("models", {}),
                "last_verified": d["verification"]["last_verified"],
                "freshness": freshness(d["verification"]["last_verified"]),
                "confidence": d["verification"]["confidence"],
                "confidence_score": d["verification"]["confidence_score"],
                "sources": d["verification"]["sources"],
            }
        )
    stats = {
        "total": len(tools),
        "active": sum(1 for t in tools if t["status"] == "active"),
        "legacy": sum(1 for t in tools if t["status"] == "legacy"),
        "discontinued": sum(1 for t in tools if t["status"] == "discontinued"),
        "recurring": sum(
            1
            for t in tools
            if any(kind.startswith("recurring_") or kind == "dynamic_rate_limit" for kind in t["free_tier_types"])
        ),
        "trials": sum(1 for t in tools if "time_limited_trial" in t["free_tier_types"] or t["trial"]["available"]),
        "open_source_byok": sum(1 for t in tools if "open_source_byok" in t["free_tier_types"]),
        "official_exact": sum(1 for t in tools if t["confidence"] == "official_exact"),
        "official_undisclosed": sum(1 for t in tools if t["confidence"] == "official_undisclosed"),
        "needs_verification": sum(1 for t in tools if t["confidence"] == "needs_verification"),
        "current": sum(1 for t in tools if t["freshness"] == "current"),
        "needs_recheck": sum(1 for t in tools if t["freshness"] == "needs_recheck"),
        "stale": sum(1 for t in tools if t["freshness"] == "stale"),
    }
    out = {"schema_version": 2, "generated_from": "tools/*.yaml", "stats": stats, "tools": tools}
    (ROOT / "data/index.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote data/index.json with {len(tools)} tools")


if __name__ == "__main__":
    main()
